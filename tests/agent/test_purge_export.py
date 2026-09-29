"""The live tutor's four tables are in the export archive and emptied by the purge
(docs/agent/architecture.md, "Guard, pacing, audit, purge and export"; docs/plan/09 2026-09-29
amendment). Neither path names the tables: both follow owner_clause's user_id rule, so what is
tested is that every agent table carries user_id and is reached by it, with a second user's rows
left alone, and that an agent_consolidate job naming the student goes with the purge."""
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.export import archive
from app.session import purge
from tests.export.test_export import seeded_row

USER_ID = "USR-agent-student"
OTHER_USER_ID = "USR-agent-other"
NOW = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
AGENT_TABLES = ("agent_conversations", "agent_turns", "tutor_memories", "tutor_profiles")


def agent_table(name):
   return models.Base.metadata.tables[name]


def seed(engine):
   with engine.begin() as connection:
      for tag, user_id in (("mine", USER_ID), ("theirs", OTHER_USER_ID)):
         connection.execute(models.User.__table__.insert().values(**seeded_row(tag, user_id, models.User.__table__)))

         for name in AGENT_TABLES:
            connection.execute(agent_table(name).insert().values(**seeded_row(tag, user_id, agent_table(name))))

         connection.execute(
            models.Job.__table__.insert().values(
               id=f"JOB-{tag}",
               type="agent_consolidate",
               payload=json.dumps({"user_id": user_id, "conversation_id": f"{tag}-agent_conversations"}),
               idempotency_key=f"agent_consolidate:{tag}-agent_conversations",
               state="queued",
               attempts_made=0,
               not_before=NOW.isoformat(),
               priority=0,
               created_at=NOW.isoformat(),
               updated_at=NOW.isoformat(),
            )
         )


def owned_row_count(db, name, user_id):
   table = agent_table(name)

   return len(db.execute(select(table).where(table.c.user_id == user_id)).all())


def test_every_agent_table_is_in_the_archive_with_the_students_rows_only(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   seed(engine)

   with OrmSession(engine) as db:
      tables = archive.build_archive(db, USER_ID, NOW.isoformat())["tables"]

   for name in AGENT_TABLES:
      assert name in tables, name
      assert [row["user_id"] for row in tables[name]] == [USER_ID], name


def test_the_purge_empties_every_agent_table_and_the_consolidation_job(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   seed(engine)

   with OrmSession(engine) as db:
      purge.purge_user(db, USER_ID, NOW)
      db.commit()

   with OrmSession(engine) as db:
      for name in AGENT_TABLES:
         assert owned_row_count(db, name, USER_ID) == 0, name
         assert owned_row_count(db, name, OTHER_USER_ID) == 1, name

      remaining_job_ids = set(db.scalars(select(models.Job.id)).all())

   assert remaining_job_ids == {"JOB-theirs"}
