"""Tests for app/session/purge.py, per docs/plan/09-security-and-privacy.md, Audit log."""
import json
from datetime import datetime, timezone

from sqlalchemy import event
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session import purge

USER_ID = "USER-0001"
NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)


def seed_user_rows(db):
   timestamp = NOW.isoformat()
   db.add(models.User(
      id=USER_ID,
      display_name="Student",
      exam_date="2027-05-10",
      purge_after=None,
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.SkillState(
      user_id=USER_ID,
      skill_id="BC-SKL-01024",
      snapshot_id="SNAP-0001",
      beta=0.0,
      fading_stage="example",
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.ProviderConfig(
      id="PRV-0001",
      user_id=USER_ID,
      provider="anthropic",
      enabled=0,
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.Budget(
      id="BUD-0001",
      user_id=USER_ID,
      role="tutor",
      day="2026-03-01",
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.PendingProbe(
      id="PRB-0001",
      user_id=USER_ID,
      archetype_id="BC-QA-01004",
      diagnosis_id="DIAG-0001",
      enqueued_at=timestamp,
      expires_at=timestamp,
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.Session(
      id="SES-0001",
      user_id=USER_ID,
      mode="learning",
      started_at=timestamp,
      ended_at=None,
      queue=json.dumps({"block1": [], "block2": [], "block3": [], "block4": [], "forecasts": {}}),
      snapshot_id="SNAP-0001",
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.Attempt(
      id="ATT-0001",
      session_id="SES-0001",
      item_id="BC-QA-01004-V00",
      started_at=timestamp,
      submitted_at=timestamp,
      response=json.dumps({"correct": True}),
      correct=1,
      served_stage="example",
      format="mcq",
      per_skill_states=json.dumps({"BC-SKL-01024": "mastered"}),
      snapshot_id="SNAP-0001",
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.Judgment(
      id="JDG-0001",
      user_id=USER_ID,
      session_id="SES-0001",
      scope="skill",
      scope_id="BC-SKL-01024",
      predicted_retention=0.6,
      made_at=timestamp,
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.add(models.AuditLog(
      id="AUD-PRIOR",
      at=timestamp,
      actor=USER_ID,
      action="provider_key_set",
      subject=USER_ID,
      created_at=timestamp,
      updated_at=timestamp,
   ))
   db.flush()


def test_purge_empties_user_tables_and_writes_final_audit(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      seed_user_rows(db)
      db.commit()

      assert db.query(models.User).filter_by(id=USER_ID).count() == 1
      assert db.query(models.AuditLog).count() == 1

      inserted_actions = []

      def record_insert(mapper, connection, target):
         inserted_actions.append(target.action)

      event.listen(models.AuditLog, "after_insert", record_insert)

      try:
         counts = purge.purge_user(db, USER_ID, NOW)
      finally:
         event.remove(models.AuditLog, "after_insert", record_insert)

      db.commit()

   assert inserted_actions[-1] == "purge"
   assert counts["sessions"] == 1
   assert counts["attempts"] == 1
   assert counts["judgments"] == 1
   assert counts["pending_probes"] == 1
   assert counts["skills_state"] == 1
   assert counts["provider_configs"] == 1
   assert counts["budgets"] == 1
   assert counts["users"] == 1
   assert counts["audit_log"] == 2

   with OrmSession(engine) as db:
      assert db.query(models.Session).filter_by(user_id=USER_ID).count() == 0
      assert db.query(models.Attempt).count() == 0
      assert db.query(models.Judgment).filter_by(user_id=USER_ID).count() == 0
      assert db.query(models.PendingProbe).filter_by(user_id=USER_ID).count() == 0
      assert db.query(models.SkillState).filter_by(user_id=USER_ID).count() == 0
      assert db.query(models.ProviderConfig).filter_by(user_id=USER_ID).count() == 0
      assert db.query(models.Budget).filter_by(user_id=USER_ID).count() == 0
      assert db.query(models.User).filter_by(id=USER_ID).count() == 0
      assert db.query(models.AuditLog).count() == 0


def test_purge_deletes_credentials_and_auth_sessions(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      seed_user_rows(db)
      timestamp = NOW.isoformat()
      db.add(models.PasskeyCredential(
         id="PKC-0001",
         user_id=USER_ID,
         credential_id=b"cred",
         public_key=b"key",
         sign_count=1,
         transports=None,
         created_at=timestamp,
         updated_at=timestamp,
      ))
      db.add(models.AuthSession(
         id="AUS-0001",
         user_id=USER_ID,
         token_hash="hash",
         expires_at=timestamp,
         created_at=timestamp,
         updated_at=timestamp,
      ))
      db.flush()
      counts = purge.purge_user(db, USER_ID, NOW)
      db.commit()

      assert counts["passkey_credentials"] == 1
      assert counts["auth_sessions"] == 1
      assert db.query(models.PasskeyCredential).count() == 0
      assert db.query(models.AuthSession).count() == 0
