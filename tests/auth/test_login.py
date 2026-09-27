"""POST /auth/login: one answer for every failure, the same scrypt work whether or not the username
exists, and a rehash when the stored parameters are below the current ones (ruled 2026-09-27)."""
from datetime import datetime, timedelta, timezone

import pytest

from app.auth import passwords, service
from app.auth.cookies import SESSION_COOKIE
from tests.api.conftest import FAST_SCRYPT_N, FAST_SCRYPT_P, FAST_SCRYPT_R, PASSWORD, USERNAME, world  # noqa: F401
from tests.auth.helpers import audit_rows, set_user_columns, user_row

WRONG_PASSWORD = "not the right password"


def far_future():
   return (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(timespec="microseconds")


def refusal_for(world, case):  # noqa: F811
   client = world.client()
   world.register(client)
   client.cookies.clear()
   is_unknown_user = case == "unknown user"
   is_wrong_password = case == "wrong password"
   is_no_password_yet = case == "no password yet"

   if is_unknown_user:
      return world.login(client, username="nobody_here")

   if is_wrong_password:
      return world.login(client, password=WRONG_PASSWORD)

   if is_no_password_yet:
      set_user_columns(world.engine, password_hash=None)

      return world.login(client)

   set_user_columns(world.engine, locked_until=far_future())

   return world.login(client)


@pytest.mark.parametrize("case", ["unknown user", "wrong password", "no password yet", "locked user"])
def test_every_login_failure_gets_the_same_401_and_no_cookie(world, case):  # noqa: F811
   """The locked and no-password cases offer the correct password for the stored name, so only
   the refusal rule itself can turn them away."""
   refused = refusal_for(world, case)

   assert refused.status_code == 401
   assert refused.json() == {"detail": service.LOGIN_REFUSED_DETAIL}
   assert "set-cookie" not in refused.headers
   assert SESSION_COOKIE not in refused.cookies


@pytest.mark.parametrize("case", ["unknown user", "no password yet", "locked user"])
def test_a_login_with_no_real_hash_to_check_still_runs_scrypt_on_the_dummy(world, monkeypatch, case):  # noqa: F811
   """Skipping the hash for an unknown or unusable account would make the refusal measurably
   faster, which tells an attacker which names exist."""
   dummy_hash = world.app.state.dummy_hashes.for_settings(world.settings)
   checked = []
   real_verify = passwords.verify_password

   def spy(password, stored):
      checked.append(stored)

      return real_verify(password, stored)

   monkeypatch.setattr(passwords, "verify_password", spy)

   refused = refusal_for(world, case)

   assert refused.status_code == 401
   assert checked == [dummy_hash]


def test_the_dummy_hash_is_built_at_startup_with_the_settings_parameters(world):  # noqa: F811
   built = world.app.state.dummy_hashes.by_parameters
   parameters = (FAST_SCRYPT_N, FAST_SCRYPT_R, FAST_SCRYPT_P)

   assert list(built) == [parameters]
   assert passwords.parse_hash(built[parameters])[:3] == parameters


def test_a_login_writes_session_established_for_the_user(world):  # noqa: F811
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   client.cookies.clear()

   logged_in = world.login(client, username=USERNAME.upper())

   assert logged_in.status_code == 200
   assert logged_in.json() == {"user_id": user_id}

   rows = audit_rows(world.engine, "session_established")

   assert len(rows) == 1
   assert rows[0].actor == user_id
   assert rows[0].subject == f"users:{user_id}"
   assert rows[0].detail is None


def test_login_sets_an_httponly_lax_cookie_and_logout_ends_the_session(world):  # noqa: F811
   client = world.client()
   world.register(client)
   client.cookies.clear()

   logged_in = world.login(client)
   header = logged_in.headers["set-cookie"]

   assert "HttpOnly" in header
   assert "samesite=lax" in header.lower()
   assert "Secure" not in header
   assert client.get("/me").status_code == 200

   logged_out = client.post("/auth/logout", json={})

   assert logged_out.status_code == 200
   assert client.get("/me").status_code == 401


def test_a_hash_below_the_current_parameters_is_replaced_at_login(world):  # noqa: F811
   client = world.client()
   world.register(client)
   weaker = passwords.hash_password(PASSWORD, FAST_SCRYPT_N // 2, FAST_SCRYPT_R, FAST_SCRYPT_P)
   set_user_columns(world.engine, password_hash=weaker)

   assert world.login(world.client()).status_code == 200

   rehashed = user_row(world.engine).password_hash

   assert rehashed != weaker
   assert passwords.parse_hash(rehashed)[:3] == (FAST_SCRYPT_N, FAST_SCRYPT_R, FAST_SCRYPT_P)
   assert passwords.verify_password(PASSWORD, rehashed) is True


def test_a_wrong_login_leaves_a_weaker_hash_alone(world):  # noqa: F811
   client = world.client()
   world.register(client)
   weaker = passwords.hash_password(PASSWORD, FAST_SCRYPT_N // 2, FAST_SCRYPT_R, FAST_SCRYPT_P)
   set_user_columns(world.engine, password_hash=weaker)

   assert world.login(world.client(), password=WRONG_PASSWORD).status_code == 401
   assert user_row(world.engine).password_hash == weaker
