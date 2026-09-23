"""Tests for app/session/purge.py, per docs/plan/09-security-and-privacy.md, Audit log."""
import json
from datetime import datetime, timezone

from sqlalchemy import Column, Table, Text, event, select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.export import archive
from app.session import purge
from tests.export.test_export import OTHER_USER_ID, seed_every_table, seed_non_user_audit_row

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



def export_jobs_of(db, user_id):
   return archive.export_jobs_for(db, user_id)


def test_purge_removes_the_export_archive_and_its_job(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   archive_directory = archive.archive_directory_for(engine)

   with OrmSession(engine) as db:
      seed_user_rows(db)
      own_job = archive.produce_export(db, archive_directory, USER_ID, NOW)
      other_job = archive.produce_export(db, archive_directory, OTHER_USER_ID, NOW)
      own_archive = archive_directory / json.loads(own_job.payload)["archive"]
      other_archive = archive_directory / json.loads(other_job.payload)["archive"]
      db.commit()

   assert own_archive.is_file()
   assert other_archive.is_file()

   with OrmSession(engine) as db:
      purge.purge_user(db, USER_ID, NOW)
      db.commit()

   assert not own_archive.exists()
   assert other_archive.is_file()

   with OrmSession(engine) as db:
      assert export_jobs_of(db, USER_ID) == []
      assert len(export_jobs_of(db, OTHER_USER_ID)) == 1


def owned_row_count(connection, table, user_id):
   clause = archive.owner_clause(table, user_id)

   return len(connection.execute(select(table).where(clause)).all())


def rows_only_that_user_owns(connection, table, user_id):
   is_audit_log = table is models.AuditLog.__table__

   if is_audit_log:
      clause = table.c.actor == user_id
   else:
      clause = archive.owner_clause(table, user_id)

   return len(connection.execute(select(table).where(clause)).all())


def test_purge_empties_every_table_the_export_classifies_as_the_students(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   seed_every_table(engine, "mine", USER_ID)
   seed_every_table(engine, "theirs", OTHER_USER_ID)
   seed_non_user_audit_row(engine)
   owned_tables = [
      table
      for table in models.Base.metadata.sorted_tables
      if archive.owner_clause(table, USER_ID) is not None
   ]

   with engine.connect() as connection:
      other_counts_before = {
         table.name: rows_only_that_user_owns(connection, table, OTHER_USER_ID)
         for table in owned_tables
      }

      for table in owned_tables:
         assert owned_row_count(connection, table, USER_ID) > 0, table.name

   assert all(count > 0 for count in other_counts_before.values())

   with OrmSession(engine) as db:
      purge.purge_user(db, USER_ID, NOW)
      db.commit()

   with engine.connect() as connection:
      for table in owned_tables:
         assert owned_row_count(connection, table, USER_ID) == 0, table.name

      other_counts_after = {
         table.name: rows_only_that_user_owns(connection, table, OTHER_USER_ID)
         for table in owned_tables
      }

   assert other_counts_after == other_counts_before


def test_purge_reaches_user_tables_added_to_the_schema_later(tmp_path):
   later_notes = Table(
      "purge_later_notes",
      models.Base.metadata,
      Column("id", Text, primary_key=True),
      Column("user_id", Text, nullable=False),
   )
   later_gradings = Table(
      "purge_later_gradings",
      models.Base.metadata,
      Column("id", Text, primary_key=True),
      Column("attempt_id", Text, nullable=False),
   )

   try:
      engine = models.make_engine(tmp_path / "growth.db")

      with engine.begin() as connection:
         connection.execute(later_notes.insert().values(id="NOTE-mine", user_id=USER_ID))
         connection.execute(later_notes.insert().values(id="NOTE-theirs", user_id=OTHER_USER_ID))
         connection.execute(later_gradings.insert().values(id="GRD-mine", attempt_id="ATT-0001"))
         connection.execute(later_gradings.insert().values(id="GRD-theirs", attempt_id="ATT-theirs"))

      assert archive.owner_clause(later_notes, USER_ID) is not None
      assert archive.owner_clause(later_gradings, USER_ID) is not None

      with OrmSession(engine) as db:
         seed_user_rows(db)
         purge.purge_user(db, USER_ID, NOW)
         db.commit()

      with engine.connect() as connection:
         remaining_notes = connection.execute(select(later_notes.c.id)).scalars().all()
         remaining_gradings = connection.execute(select(later_gradings.c.id)).scalars().all()
   finally:
      models.Base.metadata.remove(later_notes)
      models.Base.metadata.remove(later_gradings)

   assert remaining_notes == ["NOTE-theirs"]
   assert remaining_gradings == ["GRD-theirs"]