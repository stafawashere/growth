"""POST /auth/signup: the one account, claimed atomically while users is empty (ruled 2026-09-27)."""
import json

import pytest

from app.auth import passwords, service
from app.auth.cookies import SESSION_COOKIE
from tests.api.conftest import PASSWORD, USERNAME, world  # noqa: F401
from tests.auth.helpers import audit_rows, user_count, user_row, run_together


def test_signup_returns_the_user_the_seed_count_and_a_recovery_code(world):  # noqa: F811
   client = world.client()

   signed_up = world.register(client, username="Student_One")

   assert signed_up.status_code == 200

   body = signed_up.json()
   stored = user_row(world.engine)

   assert set(body) == {"user", "seeded_skill_states", "recovery_code"}
   assert body["user"]["id"] == stored.id
   assert body["user"]["display_name"] == "student"
   assert body["seeded_skill_states"] == len(world.states(stored.id)) > 0
   assert isinstance(body["recovery_code"], str) and body["recovery_code"] != ""
   assert stored.username == "student_one"
   assert passwords.verify_password(PASSWORD, stored.password_hash) is True
   assert PASSWORD not in stored.password_hash
   assert client.get("/me").status_code == 200


def test_signup_is_refused_once_the_installation_has_its_user(world):  # noqa: F811
   assert world.register(world.client()).status_code == 200

   second = world.register(world.client(), username="someone_else", password="someone else's password")

   assert second.status_code == 403
   assert second.json()["detail"] == service.SIGNUP_CLOSED_DETAIL
   assert SESSION_COOKIE not in second.cookies
   assert user_count(world.engine) == 1
   assert user_row(world.engine).username == USERNAME


def test_signups_that_all_pass_the_empty_check_still_claim_only_one_user(world, monkeypatch):  # noqa: F811
   """user_exists is forced to answer False, as it does for every request that reads the table
   before any of them inserts, so only the INSERT ... WHERE NOT EXISTS stands between the racers."""
   monkeypatch.setattr(service, "user_exists", lambda db: False)
   calls = [
      (lambda index=index: world.register(world.client(), username=f"racer_{index}").status_code)
      for index in range(6)
   ]

   statuses = run_together(calls)

   assert sorted(statuses) == [200, 403, 403, 403, 403, 403]
   assert user_count(world.engine) == 1


@pytest.mark.parametrize(
   "username, password",
   [
      ("ab", PASSWORD),
      ("abc\n", PASSWORD),
      (12345, PASSWORD),
      (["student"], PASSWORD),
      (None, PASSWORD),
      ({"name": "student"}, PASSWORD),
      (USERNAME, "short"),
      (USERNAME, "p" * 129),
      (USERNAME, 123456789012345),
      (USERNAME, [PASSWORD]),
      (USERNAME, None),
   ],
)
def test_a_signup_the_rules_refuse_is_a_400_and_claims_nothing(world, username, password):  # noqa: F811
   client = world.client()

   refused = client.post("/auth/signup", json={"username": username, "password": password})

   assert refused.status_code == 400
   assert refused.json()["detail"] in (passwords.USERNAME_RULE, passwords.PASSWORD_RULE)
   assert user_count(world.engine) == 0
   assert SESSION_COOKIE not in client.cookies


def test_signup_writes_account_created_with_the_seed_count(world):  # noqa: F811
   signed_up = world.register(world.client())
   user_id = signed_up.json()["user"]["id"]

   rows = audit_rows(world.engine, "account_created")

   assert len(rows) == 1
   assert rows[0].actor == user_id
   assert rows[0].subject == f"users:{user_id}"
   assert json.loads(rows[0].detail) == {"seeded_skill_states": signed_up.json()["seeded_skill_states"]}
   assert PASSWORD not in (rows[0].detail or "")


def test_signup_sets_an_httponly_lax_cookie_without_secure_on_loopback(world):  # noqa: F811
   signed_up = world.register(world.client())

   header = signed_up.headers["set-cookie"]

   assert header.startswith(f"{SESSION_COOKIE}=")
   assert "HttpOnly" in header
   assert "samesite=lax" in header.lower()
   assert "Secure" not in header
