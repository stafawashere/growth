"""Password hashing and the username and password rules, ruled 2026-09-27 when passwords replaced
passkeys.

A stored hash reads scrypt$<n>$<r>$<p>$<salthex>$<hashhex>, the same dollar-separated, parameters
first shape app/auth/recovery.py gives the recovery code, so a hash made under older parameters
still verifies after the defaults rise and can be rehashed on the next sign-in. The defaults are
n=2**14, r=8, p=5, one of the OWASP scrypt settings, at 16 MiB per hash.

Every check here treats a value that is not a str as a refusal rather than an error, because these
values arrive straight from a JSON body that can hold a number, a list or null.
"""
import hashlib
import hmac
import re
import secrets

SCRYPT_ALGORITHM = "scrypt"
DEFAULT_SCRYPT_N = 2 ** 14
DEFAULT_SCRYPT_R = 8
DEFAULT_SCRYPT_P = 5
LARGEST_STORED_SCRYPT_N = 2 ** 20
LARGEST_STORED_SCRYPT_R = 32
LARGEST_STORED_SCRYPT_P = 16
SCRYPT_DKLEN = 32
SALT_BYTES = 16
PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 128
PASSWORD_MAX_BYTES = 512
USERNAME_PATTERN = re.compile(r"[A-Za-z0-9_]{3,32}")
PASSWORD_RULE = f"a password of {PASSWORD_MIN_LENGTH} to {PASSWORD_MAX_LENGTH} characters is required"
USERNAME_RULE = "a username of 3 to 32 letters, digits or underscores is required"


def scrypt_maxmem(n, r):
   return 2 * 128 * r * n


def derive(password, salt, n, r, p):
   return hashlib.scrypt(
      password.encode("utf-8"),
      salt=salt,
      n=n,
      r=r,
      p=p,
      maxmem=scrypt_maxmem(n, r),
      dklen=SCRYPT_DKLEN,
   )


def hash_password(password, n=DEFAULT_SCRYPT_N, r=DEFAULT_SCRYPT_R, p=DEFAULT_SCRYPT_P):
   salt = secrets.token_bytes(SALT_BYTES)
   digest = derive(password, salt, n, r, p)

   return f"{SCRYPT_ALGORITHM}${n}${r}${p}${salt.hex()}${digest.hex()}"


def is_power_of_two(value):
   return value > 1 and (value & (value - 1)) == 0


def parse_hash(stored):
   """Returns (n, r, p, salt, digest), or None for anything that is not a well-formed scrypt hash
   inside the bounds this module would ever write."""
   is_text = isinstance(stored, str)

   if not is_text:
      return None

   parts = stored.split("$")
   has_six_parts = len(parts) == 6

   if not has_six_parts:
      return None

   algorithm, n_text, r_text, p_text, salt_hex, digest_hex = parts
   is_scrypt = algorithm == SCRYPT_ALGORITHM

   if not is_scrypt:
      return None

   try:
      n = int(n_text)
      r = int(r_text)
      p = int(p_text)
      salt = bytes.fromhex(salt_hex)
      digest = bytes.fromhex(digest_hex)
   except ValueError:
      return None

   n_is_usable = is_power_of_two(n) and n <= LARGEST_STORED_SCRYPT_N
   r_is_usable = 0 < r <= LARGEST_STORED_SCRYPT_R
   p_is_usable = 0 < p <= LARGEST_STORED_SCRYPT_P
   has_salt_and_digest = len(salt) > 0 and len(digest) > 0
   is_usable = n_is_usable and r_is_usable and p_is_usable and has_salt_and_digest

   if not is_usable:
      return None

   return n, r, p, salt, digest


def verify_password(password, stored):
   """False for a wrong password, a password that is not a str, and a stored value that is None or
   malformed. Never raises."""
   parsed = parse_hash(stored)
   is_offered = can_be_verified(password)
   can_compare = parsed is not None and is_offered

   if not can_compare:
      return False

   n, r, p, salt, expected = parsed
   candidate = derive(password, salt, n, r, p)

   return hmac.compare_digest(candidate, expected)


def needs_rehash(stored, n, r, p):
   parsed = parse_hash(stored)

   if parsed is None:
      return True

   stored_n, stored_r, stored_p, _, _ = parsed
   is_below = stored_n < n or stored_r < r or stored_p < p

   return is_below


def build_dummy_hash(n, r, p):
   """A hash of a random password nobody knows, verified in place of a missing one so an unknown
   username costs the same scrypt work as a known one."""
   return hash_password(secrets.token_urlsafe(24), n, r, p)


def normalise_username(raw):
   """The lowercase username, or None. fullmatch, because $ would accept a trailing newline, and
   ASCII only, so two names that look alike can never both exist."""
   is_text = isinstance(raw, str)

   if not is_text:
      return None

   matched = USERNAME_PATTERN.fullmatch(raw)

   if matched is None:
      return None

   return raw.lower()


def password_problem(password):
   """The refusal for a password that cannot be set, or None when it can."""
   is_text = isinstance(password, str)

   if not is_text:
      return PASSWORD_RULE

   is_too_short = len(password) < PASSWORD_MIN_LENGTH
   is_too_long = len(password) > PASSWORD_MAX_LENGTH
   has_wrong_length = is_too_short or is_too_long

   if has_wrong_length:
      return PASSWORD_RULE

   try:
      encoded = password.encode("utf-8")
   except UnicodeEncodeError:
      return PASSWORD_RULE

   is_too_many_bytes = len(encoded) > PASSWORD_MAX_BYTES

   if is_too_many_bytes:
      return PASSWORD_RULE

   return None


def can_be_verified(password):
   """A login or reauth candidate worth hashing: a str whose UTF-8 form is within the byte cap."""
   is_text = isinstance(password, str)

   if not is_text:
      return False

   try:
      encoded = password.encode("utf-8")
   except UnicodeEncodeError:
      return False

   return 0 < len(encoded) <= PASSWORD_MAX_BYTES
