"""POST /auth/password/change: a fresh reauth token and the current password set a new one, every
other session is signed out, and the current session and the recovery code are kept (ruled
2026-09-27)."""
from app.auth import passwords
from tests.api.conftest import NEW_PASSWORD, PASSWORD, world  # noqa: F401
from tests.auth.helpers import audit_rows, lockout_state, user_row

WRONG_PASSWORD = "not the right password"


def change(world, client, current_password=PASSWORD, new_password=NEW_PASSWORD):  # noqa: F811
   token = world.reauth(client).json()["reauth_token"]
   payload = {"current_password": current_password, "new_password": new_password, "reauth_token": token}

   return client.post("/auth/password/change", json=payload)


def test_a_wrong_current_password_is_refused_counted_and_changes_nothing(world):  # noqa: F811
   client = world.client()
   world.register(client)
   before = user_row(world.engine).password_hash

   refused = change(world, client, current_password=WRONG_PASSWORD)

   assert refused.status_code == 401
   assert refused.json() == {"detail": "the current password is incorrect"}
   assert user_row(world.engine).password_hash == before
   assert lockout_state(world.engine)[0] == 1


def test_a_new_password_the_rules_refuse_is_a_400_and_changes_nothing(world):  # noqa: F811
   client = world.client()
   world.register(client)
   before = user_row(world.engine).password_hash

   refused = change(world, client, new_password="short")

   assert refused.status_code == 400
   assert refused.json() == {"detail": passwords.PASSWORD_RULE}
   assert user_row(world.engine).password_hash == before


def test_the_new_password_logs_in_and_the_old_one_does_not(world):  # noqa: F811
   client = world.client()
   world.register(client)

   assert change(world, client).status_code == 200
   assert world.login(world.client(), password=PASSWORD).status_code == 401
   assert world.login(world.client(), password=NEW_PASSWORD).status_code == 200


def test_other_sessions_are_signed_out_and_the_current_one_survives(world):  # noqa: F811
   current = world.client()
   world.register(current)
   other = world.client()

   assert world.login(other).status_code == 200
   assert other.get("/me").status_code == 200

   assert change(world, current).status_code == 200
   assert current.get("/me").status_code == 200
   assert other.get("/me").status_code == 401


def test_a_change_keeps_the_recovery_code_and_writes_password_changed(world):  # noqa: F811
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   recovery_hash = user_row(world.engine).recovery_code_hash

   assert change(world, client).status_code == 200

   rows = audit_rows(world.engine, "password_changed")

   assert user_row(world.engine).recovery_code_hash == recovery_hash
   assert len(rows) == 1
   assert rows[0].actor == user_id
   assert rows[0].subject == f"users:{user_id}"
   assert rows[0].detail is None
