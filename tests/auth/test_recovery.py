"""Recovery code generation, hashing and consumption, per docs/plan/09-security-and-privacy.md,
"Recovery": a code is generated once at sign-up, shown once and stored as a hash. Since passwords
replaced passkeys (ruled 2026-09-27) it resets the password once, signs every session out, and is
replaced by a new code shown once.
"""
from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.api.app import Settings
from app.auth import passwords, recovery, service
from app.db import models
from tests.api.conftest import NEW_PASSWORD, PASSWORD, USERNAME, world  # noqa: F401
from tests.auth.helpers import audit_rows, run_together, user_row

NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)
FAST_SETTINGS = Settings(password_scrypt_n=2 ** 10, password_scrypt_r=8, password_scrypt_p=1)
MIGRATED_USERNAME = "Migrated_Student"


@pytest.fixture
def db(tmp_path):
   """A user as the passkey retirement leaves one: no username and no password."""
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as session:
      user = models.User(
         id="USER-0001",
         display_name="student",
         exam_date="2027-05-10",
         purge_after="2027-06-09",
         created_at=NOW.isoformat(),
         updated_at=NOW.isoformat(),
      )
      session.add(user)
      session.add(
         models.AuthSession(
            id="AUS-OLD",
            user_id="USER-0001",
            token_hash="old-session-hash",
            expires_at="2099-01-01T00:00:00+00:00",
            created_at=NOW.isoformat(),
            updated_at=NOW.isoformat(),
         )
      )
      session.flush()
      yield session


def reset(db, code, username=MIGRATED_USERNAME, new_password=NEW_PASSWORD):
   return recovery.reset_password_via_recovery(db, FAST_SETTINGS, code, new_password, username=username, now=NOW)


def is_refusal(outcome, status_code):
   return isinstance(outcome, service.AuthRefusal) and outcome.status_code == status_code


def test_recovery_code_is_shown_once_and_stored_hashed(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)

   assert isinstance(code, str) and len(code) >= 16
   assert user.recovery_code_hash is not None
   assert code not in user.recovery_code_hash


def test_a_valid_code_sets_the_password_and_username_and_is_consumed(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)
   spent_hash = user.recovery_code_hash

   finished = reset(db, code)

   assert not isinstance(finished, service.AuthRefusal)

   stored = db.get(models.User, "USER-0001")

   assert passwords.verify_password(NEW_PASSWORD, stored.password_hash) is True
   assert stored.username == MIGRATED_USERNAME.lower()
   assert stored.recovery_code_hash != spent_hash
   assert recovery.recovery_code_matches(code, stored.recovery_code_hash) is False


def test_a_replayed_code_is_refused(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)
   reset(db, code)

   replayed = reset(db, code, new_password="a third long passphrase")

   assert is_refusal(replayed, 401)
   assert replayed.detail == recovery.RECOVERY_REFUSED_DETAIL
   assert passwords.verify_password(NEW_PASSWORD, db.get(models.User, "USER-0001").password_hash) is True


def test_the_replacement_code_is_returned_and_works_once(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)

   replacement = reset(db, code)["recovery_code"]

   assert replacement != code
   assert not isinstance(reset(db, replacement, new_password="a third long passphrase"), service.AuthRefusal)


def test_a_migrated_user_must_choose_a_username(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)

   refused = reset(db, code, username=None)

   assert is_refusal(refused, 400)
   assert db.get(models.User, "USER-0001").recovery_code_hash is not None
   assert not isinstance(reset(db, code), service.AuthRefusal)


def test_a_supplied_username_cannot_rename_an_account_that_has_one(db):
   user = db.get(models.User, "USER-0001")
   user.username = "original_name"
   code = recovery.issue_recovery_code(db, user, now=NOW)

   finished = reset(db, code, username="attacker_name")

   assert not isinstance(finished, service.AuthRefusal)
   assert db.get(models.User, "USER-0001").username == "original_name"


def test_a_reset_signs_every_session_out_and_opens_one_new_session(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)

   finished = reset(db, code)
   sessions = db.query(models.AuthSession).all()

   assert [row.id for row in sessions if row.id == "AUS-OLD"] == []
   assert len(sessions) == 1
   assert sessions[0].token_hash == service.token_hash(finished["token"])


def test_a_reset_writes_password_reset_via_recovery_for_the_user(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)
   reset(db, code)

   entry = (
      db.query(models.AuditLog)
      .filter(models.AuditLog.action == recovery.RECOVERY_AUDIT_ACTION)
      .one()
   )

   assert recovery.RECOVERY_AUDIT_ACTION == "password_reset_via_recovery"
   assert entry.actor == "USER-0001"
   assert entry.subject == "users:USER-0001"
   assert entry.detail is None


@pytest.mark.parametrize(
   "code_json",
   ["12345", '["ABCDE-FGHJK"]', "null", '{"code": "x"}', '""', '"' + "\\ud800" * 20 + '"'],
)
def test_a_code_that_is_not_usable_text_is_a_401_through_the_route(world, code_json):  # noqa: F811
   """Sent as raw JSON, because a lone surrogate escape is valid JSON that no client library will
   encode for us, and it decodes to a str that cannot be encoded as UTF-8."""
   world.register(world.client())
   raw_body = f'{{"recovery_code": {code_json}, "new_password": "{NEW_PASSWORD}"}}'

   refused = world.client().post(
      "/auth/recovery/reset", content=raw_body, headers={"content-type": "application/json"}
   )

   assert refused.status_code == 401
   assert refused.json() == {"detail": recovery.RECOVERY_REFUSED_DETAIL}


def test_two_resets_racing_with_one_code_let_exactly_one_through(world):  # noqa: F811
   code = world.register(world.client()).json()["recovery_code"]
   passwords_offered = ["first racer password", "second racer password"]
   calls = [
      (lambda password=password: world.recover(world.client(), code, new_password=password).status_code)
      for password in passwords_offered
   ]

   statuses = run_together(calls)

   assert sorted(statuses) == [200, 401]
   assert len(audit_rows(world.engine, recovery.RECOVERY_AUDIT_ACTION)) == 1

   winner = passwords_offered[statuses.index(200)]

   assert passwords.verify_password(winner, user_row(world.engine).password_hash) is True


def test_a_reset_through_the_route_ends_the_old_sessions_and_keeps_the_username(world):  # noqa: F811
   old = world.client()
   code = world.register(old).json()["recovery_code"]
   fresh = world.client()

   recovered = world.recover(fresh, code, username="another_name")

   assert recovered.status_code == 200
   assert set(recovered.json()) == {"user_id", "recovery_code"}
   assert old.get("/me").status_code == 401
   assert fresh.get("/me").status_code == 200
   assert world.login(world.client(), username=USERNAME, password=NEW_PASSWORD).status_code == 200
   assert world.login(world.client(), username=USERNAME, password=PASSWORD).status_code == 401
