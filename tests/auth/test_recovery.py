"""Recovery code generation, hashing and consumption, per docs/plan/09-security-and-privacy.md,
"Recovery": a code is generated once at registration, shown once, stored as a hash, authenticates
one new passkey registration, and is then consumed.
"""
from datetime import datetime, timezone

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.auth import recovery
from app.auth.service import AuthError
from app.db import models

NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)
VERIFIED_CREDENTIAL = {
   "credential_id": b"recovered-cred-1",
   "public_key": b"recovered-key-1",
   "sign_count": 0,
   "transports": None,
}


@pytest.fixture
def db(tmp_path):
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
      session.flush()
      yield session


def test_recovery_code_is_shown_once_and_stored_hashed(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)

   assert isinstance(code, str) and len(code) >= 16
   assert user.recovery_code_hash is not None
   assert code not in user.recovery_code_hash


def test_recovery_code_authenticates_a_new_registration_once(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)

   credential_row = recovery.register_via_recovery(db, user, code, VERIFIED_CREDENTIAL, now=NOW)

   assert credential_row.user_id == user.id
   assert credential_row.credential_id == VERIFIED_CREDENTIAL["credential_id"]

   stored = (
      db.query(models.PasskeyCredential)
      .filter(models.PasskeyCredential.credential_id == VERIFIED_CREDENTIAL["credential_id"])
      .first()
   )

   assert stored is not None
   assert user.recovery_code_hash is None


def test_consumed_code_is_refused(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)
   recovery.register_via_recovery(db, user, code, VERIFIED_CREDENTIAL, now=NOW)

   with pytest.raises(AuthError):
      recovery.register_via_recovery(db, user, code, VERIFIED_CREDENTIAL, now=NOW)


def test_recovery_writes_an_audit_entry(db):
   user = db.get(models.User, "USER-0001")
   code = recovery.issue_recovery_code(db, user, now=NOW)
   credential_row = recovery.register_via_recovery(db, user, code, VERIFIED_CREDENTIAL, now=NOW)

   entry = (
      db.query(models.AuditLog)
      .filter(models.AuditLog.action == recovery.RECOVERY_AUDIT_ACTION)
      .first()
   )

   assert entry is not None
   assert entry.actor == user.id
   assert entry.subject == f"passkey_credentials:{credential_row.id}"
