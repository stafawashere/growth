"""app/auth/passwords.py: the scrypt hash format, the checks that must never raise on a value a JSON
body can carry, and the username and password rules (ruled 2026-09-27)."""
import pytest

from app.api.app import Settings
from app.auth import passwords
from app.auth.recovery import recovery_code_matches

FAST_N = 2 ** 10
FAST_R = 8
FAST_P = 1
OWASP_FLOOR_N = 2 ** 14
OWASP_FLOOR_R = 8
OWASP_FLOOR_P = 5
PASSWORD = "correct horse battery"
NOT_TEXT_VALUES = (12345678901234, ["correct horse battery"], None, {"password": "x"}, 1.5, True)


def fast_hash(password=PASSWORD):
   return passwords.hash_password(password, FAST_N, FAST_R, FAST_P)


def test_a_hash_verifies_its_own_password_and_no_other():
   stored = fast_hash()

   assert passwords.verify_password(PASSWORD, stored) is True
   assert passwords.verify_password(PASSWORD + "!", stored) is False
   assert PASSWORD not in stored


def test_two_hashes_of_one_password_use_different_salts():
   first = fast_hash()
   second = fast_hash()

   assert first != second
   assert passwords.parse_hash(first)[3] != passwords.parse_hash(second)[3]


def test_verify_uses_the_parameters_stored_in_the_hash_not_the_defaults():
   """A hash made at low parameters must still verify once the defaults are higher, or every
   password set before a parameter rise would stop working."""
   stored = fast_hash()
   algorithm, n_text, r_text, p_text, salt_hex, digest_hex = stored.split("$")

   assert (algorithm, int(n_text), int(r_text), int(p_text)) == ("scrypt", FAST_N, FAST_R, FAST_P)
   assert len(bytes.fromhex(salt_hex)) == passwords.SALT_BYTES
   assert len(bytes.fromhex(digest_hex)) == passwords.SCRYPT_DKLEN
   assert passwords.verify_password(PASSWORD, stored) is True


@pytest.mark.parametrize(
   "stored",
   [
      None,
      "",
      12345,
      ["scrypt"],
      "plaintext password",
      "scrypt$1024$8$1$zz$00",
      "scrypt$1000$8$1$00$00",
      "scrypt$1024$8$1$$",
      "scrypt$1024$8$1$00",
      "pbkdf2_sha256$1024$8$1$00$00",
      "scrypt$1048576000$8$1$00$00",
      "scrypt$1024$0$1$00$00",
   ],
)
def test_a_missing_or_malformed_stored_hash_is_a_non_match_and_never_raises(stored):
   assert passwords.verify_password(PASSWORD, stored) is False


@pytest.mark.parametrize("offered", NOT_TEXT_VALUES)
def test_a_password_that_is_not_text_is_refused_by_every_check(offered):
   stored = fast_hash()

   assert passwords.verify_password(offered, stored) is False
   assert passwords.can_be_verified(offered) is False
   assert passwords.password_problem(offered) == passwords.PASSWORD_RULE
   assert passwords.normalise_username(offered) is None
   assert recovery_code_matches(offered, "pbkdf2_sha256$1$00$00") is False


def test_a_hash_below_the_current_parameters_needs_rehashing():
   stored = fast_hash()

   assert passwords.needs_rehash(stored, FAST_N, FAST_R, FAST_P) is False
   assert passwords.needs_rehash(stored, FAST_N * 2, FAST_R, FAST_P) is True
   assert passwords.needs_rehash(stored, FAST_N, FAST_R, FAST_P + 1) is True
   assert passwords.needs_rehash(None, FAST_N, FAST_R, FAST_P) is True


def test_production_defaults_are_at_or_above_the_owasp_floor():
   """Tests run at n=2**10, so nothing else would notice the shipped defaults sliding down."""
   defaults = Settings()

   assert passwords.DEFAULT_SCRYPT_N >= OWASP_FLOOR_N
   assert passwords.DEFAULT_SCRYPT_R >= OWASP_FLOOR_R
   assert passwords.DEFAULT_SCRYPT_P >= OWASP_FLOOR_P
   assert defaults.password_scrypt_n == passwords.DEFAULT_SCRYPT_N
   assert defaults.password_scrypt_r == passwords.DEFAULT_SCRYPT_R
   assert defaults.password_scrypt_p == passwords.DEFAULT_SCRYPT_P


@pytest.mark.parametrize(
   "length, is_accepted",
   [(11, False), (12, True), (128, True), (129, False)],
)
def test_password_length_bounds(length, is_accepted):
   problem = passwords.password_problem("p" * length)

   assert (problem is None) is is_accepted


def test_a_password_that_cannot_be_encoded_is_refused_rather_than_raising():
   lone_surrogates = "\ud800" * passwords.PASSWORD_MIN_LENGTH

   assert passwords.password_problem(lone_surrogates) == passwords.PASSWORD_RULE
   assert passwords.can_be_verified(lone_surrogates) is False
   assert passwords.verify_password(lone_surrogates, fast_hash()) is False


def test_a_login_candidate_over_the_byte_cap_is_never_hashed():
   """Login has no character limit, so the byte cap is what stops a megabyte password reaching
   scrypt on an unauthenticated route."""
   at_cap = "a" * passwords.PASSWORD_MAX_BYTES
   over_cap = "a" * (passwords.PASSWORD_MAX_BYTES + 1)
   four_byte_characters = "\U0001F600" * (passwords.PASSWORD_MAX_BYTES // 4 + 1)

   assert passwords.can_be_verified(at_cap) is True
   assert passwords.can_be_verified(over_cap) is False
   assert passwords.can_be_verified(four_byte_characters) is False
   assert passwords.can_be_verified("") is False


@pytest.mark.parametrize(
   "raw, expected",
   [
      ("Student_1", "student_1"),
      ("abc", "abc"),
      ("a" * 32, "a" * 32),
      ("ab", None),
      ("a" * 33, None),
      ("abc\n", None),
      ("\nabc", None),
      ("ab c", None),
      ("abc-d", None),
      ("étudiant", None),
      ("ａbc", None),
      ("", None),
   ],
)
def test_username_rules(raw, expected):
   assert passwords.normalise_username(raw) == expected


def test_usernames_differing_only_in_case_normalise_to_one_name():
   assert passwords.normalise_username("StudentOne") == passwords.normalise_username("studentone")


@pytest.mark.parametrize(
   "variable, too_large",
   [
      ("GROWTH_SCRYPT_N", passwords.LARGEST_STORED_SCRYPT_N * 2),
      ("GROWTH_SCRYPT_R", passwords.LARGEST_STORED_SCRYPT_R + 1),
      ("GROWTH_SCRYPT_P", passwords.LARGEST_STORED_SCRYPT_P + 1),
   ],
)
def test_startup_refuses_a_scrypt_cost_whose_hashes_could_never_verify(variable, too_large):
   from app.main import scrypt_cost

   with pytest.raises(ValueError, match=variable):
      scrypt_cost({variable: str(too_large)}, variable, 1)


@pytest.mark.parametrize(
   "variable, ceiling",
   [
      ("GROWTH_SCRYPT_N", passwords.LARGEST_STORED_SCRYPT_N),
      ("GROWTH_SCRYPT_R", passwords.LARGEST_STORED_SCRYPT_R),
      ("GROWTH_SCRYPT_P", passwords.LARGEST_STORED_SCRYPT_P),
   ],
)
def test_startup_accepts_a_scrypt_cost_at_the_largest_value_a_stored_hash_may_carry(variable, ceiling):
   from app.main import scrypt_cost

   assert scrypt_cost({variable: str(ceiling)}, variable, 1) == ceiling


def test_a_hash_at_the_largest_stored_p_still_verifies():
   password = "correct horse battery staple"
   stored = passwords.hash_password(password, 2 ** 10, 8, passwords.LARGEST_STORED_SCRYPT_P)

   assert passwords.verify_password(password, stored)
