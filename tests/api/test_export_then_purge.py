"""11 P8 test_export_then_purge: export produces a complete archive, purge removes everything, and
the downloaded export still opens afterwards. Checked by re-reading every table of the database
after the purge, not by trusting the purge's own counts.

The student practises, has a tutor call queued behind a usage limit (its job carries the student's
own attempt text), a grading point with a split review on it, and an error note. "Everything" is
read as: no row in any table names the student's id or the id of any row the student owned, so a
shared table (jobs, review_queue) is searched too.
"""
import json
from datetime import datetime, timezone

import pytest
from sqlalchemy import select, text
from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.db import models
from app.export import archive
from app.grading.service import open_review
from app.providers.subscription import SubscriptionProvider
from tests.api.test_tutor_budget import wrong_short_answer
from tests.providers.test_subscription import FakeCli

NOW = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


def owned_ids_by_table(engine, user_id):
   with OrmSession(engine) as db:
      owned = {}

      for table in models.Base.metadata.sorted_tables:
         clause = archive.owner_clause(table, user_id)
         is_unowned = clause is None
         has_single_key = len(table.primary_key.columns) == 1
         cannot_list_ids = is_unowned or not has_single_key

         if cannot_list_ids:
            continue

         key_column = list(table.primary_key.columns)[0]
         owned[table.name] = set(db.execute(select(key_column).where(clause)).scalars())

      return owned


def rows_naming(engine, needles):
   """Every row, in every table, whose text holds any of the needles."""
   found = []

   with engine.connect() as connection:
      for table in models.Base.metadata.sorted_tables:
         for row in connection.execute(select(table)).mappings():
            row_text = json.dumps({key: str(value) for key, value in row.items()})
            hits = [needle for needle in needles if needle in row_text]

            if hits:
               found.append((table.name, hits[0]))

   return found


def a_graded_point_under_review(engine, attempt_id):
   with OrmSession(engine) as db:
      grading = models.Grading(
         id="GRD-export-purge",
         attempt_id=attempt_id,
         part_id="a",
         point_id="a1",
         point_type_id="BC-PT-99012",
         decided_by="model",
         earned=None,
         samples="[]",
         agreement="split",
         provisional=1,
         rationale="the samples split",
         created_at=NOW.isoformat(),
         updated_at=NOW.isoformat(),
      )
      db.add(grading)
      open_review(db, "grading_split", grading.id, NOW)
      db.commit()


def test_export_then_purge(world, cli, tmp_path):
   cli.mode("weekly_limit")
   world.settings.tutor = SubscriptionProvider(environ=cli.environ())
   world.settings.purge_hook = None
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   session_id, attempt_id = wrong_short_answer(client)

   assert client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").status_code == 200
   assert client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "I cancelled before factoring."},
   ).status_code == 200

   a_graded_point_under_review(world.engine, attempt_id)
   owned = owned_ids_by_table(world.engine, user_id)
   export_token = world.reauth(client).json()["reauth_token"]
   produced = client.post("/export", json={"reauth_token": export_token})

   assert produced.status_code == 200, produced.text

   downloaded = client.get(f"/export/{produced.json()['id']}")

   assert downloaded.status_code == 200

   saved_copy = tmp_path / "saved-export.json"
   saved_copy.write_bytes(downloaded.content)
   exported = json.loads(saved_copy.read_text())
   exported_tables = exported["tables"]

   for table_name, ids in owned.items():
      has_rows = len(ids) > 0
      is_audit_log = table_name == "audit_log"
      should_match_one_for_one = has_rows and not is_audit_log

      if should_match_one_for_one:
         assert table_name in exported_tables, table_name
         assert len(exported_tables[table_name]) == len(ids), table_name

   with OrmSession(world.engine) as db:
      queued_jobs = db.scalars(select(models.Job).where(models.Job.type != "export")).all()

   assert len(queued_jobs) == 1
   assert user_id in queued_jobs[0].payload

   purge_token = world.reauth(client).json()["reauth_token"]
   purged = client.post("/purge", json={"confirmation": PURGE_CONFIRMATION, "reauth_token": purge_token})

   assert purged.status_code == 200, purged.text

   needles = {user_id}

   for ids in owned.values():
      needles.update(ids)

   assert rows_naming(world.engine, sorted(needles)) == []

   with world.engine.connect() as connection:
      remaining_users = connection.execute(text("SELECT COUNT(*) FROM users")).scalar()

   assert remaining_users == 0
   assert list(archive.archive_directory_for(world.engine).glob("*.json")) == []
   assert json.loads(saved_copy.read_text()) == exported
