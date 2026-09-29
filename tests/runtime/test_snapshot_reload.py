"""snapshot_reload through the composition root, docs/plan/06-architecture.md "Library updates and
retired IDs": build_session_context reconciles every user's skills_state rows when the loaded
digest differs from the active content_snapshots row, and only then.

Each test loads a copy of the live registries from a temporary directory, so data/ is read and
never written. The digest covers the registries, sources.json, prereq_edges.csv and ids.json, so a
tombstone alone gives the library a new digest; the tests written before ids.json was hashed still
append a newline to sources.json as well.
"""
import json
import shutil
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.content import reload as reload_module
from app.content.reconcile import ReloadRefused
from app.db import models
from app.runtime.context import build_session_context

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
TODAY = date(2026, 9, 28)
RETIRED_SKILL = "BC-SKL-01999"
DANGLING_SKILL = "BC-SKL-01998"
FIRST_USER = "USER-0001"
SECOND_USER = "USER-0002"


def copy_library(tmp_path):
   root = tmp_path / "data"
   root.mkdir()

   for path in DATA_ROOT.iterdir():
      is_registry_file = path.is_file() and path.suffix in (".json", ".csv")

      if is_registry_file:
         shutil.copy(path, root / path.name)

   return root


def live_skill_ids(root, count):
   registry = json.loads((root / "skills.json").read_text())

   return [record["id"] for record in registry["skills"][:count]]


def change_digest(root):
   sources = root / "sources.json"
   sources.write_text(sources.read_text() + "\n")


def add_tombstone(root, skill_id, superseded_by):
   path = root / "ids.json"
   registry = json.loads(path.read_text())
   registry["ids"][skill_id] = {
      "created": "2026-09-19",
      "name": "A skill merged into its successor",
      "status": "retired",
      "superseded_by": superseded_by,
   }
   path.write_text(json.dumps(registry))


def add_row(db, user_id, skill_id, snapshot_id, **overrides):
   fields = {
      "user_id": user_id,
      "skill_id": skill_id,
      "snapshot_id": snapshot_id,
      "beta": 0.0,
      "credited_successes": 0.0,
      "credited_failures": 0.0,
      "stability": None,
      "difficulty": None,
      "last_practised_at": None,
      "fading_stage": "example",
      "observation_count": 0,
      "credited_observation_count": 0,
      "unaided_success_count": 0,
      "distinct_archetypes_succeeded": "[]",
      "success_days": "[]",
      "mastered": 0,
      "mastered_at": None,
      "hypercorrection_due": None,
      "consecutive_successes": 0,
      "consecutive_failures": 0,
      "concept_opener_done": 0,
      "created_at": "2026-09-19T00:00:00+00:00",
      "updated_at": "2026-09-19T00:00:00+00:00",
   }
   fields.update(overrides)
   db.add(models.SkillState(**fields))


def snapshot_rows(engine):
   with OrmSession(engine) as db:
      return {row.id: (row.status, row.digest) for row in db.scalars(select(models.ContentSnapshot))}


def audit_rows(engine, action):
   with OrmSession(engine) as db:
      return [
         (row.subject, json.loads(row.detail) if row.detail else None)
         for row in db.scalars(select(models.AuditLog).where(models.AuditLog.action == action))
      ]


def state_rows(engine):
   with OrmSession(engine) as db:
      return {
         (row.user_id, row.skill_id): (row.snapshot_id, row.credited_successes, row.credited_failures)
         for row in db.scalars(select(models.SkillState))
      }


@pytest.fixture
def library(tmp_path):
   root = copy_library(tmp_path)
   engine = models.make_engine(tmp_path / "growth.db")
   first = build_session_context(engine, root, today=TODAY)

   return root, engine, first.snapshot_id


def test_a_new_digest_merges_a_superseded_skill_and_records_the_reload(library):
   root, engine, first_id = library
   successor, other = live_skill_ids(root, 2)

   with OrmSession(engine) as db:
      add_row(db, FIRST_USER, successor, first_id, credited_successes=2.0)
      add_row(db, FIRST_USER, RETIRED_SKILL, first_id, credited_successes=3.0, credited_failures=1.0)
      add_row(db, FIRST_USER, other, first_id)
      add_row(db, SECOND_USER, other, first_id)
      db.commit()

   add_tombstone(root, RETIRED_SKILL, successor)
   change_digest(root)

   second = build_session_context(engine, root, today=TODAY)
   rows = state_rows(engine)
   snapshots = snapshot_rows(engine)

   assert second.snapshot_id != first_id
   assert snapshots[first_id][0] == "superseded"
   assert snapshots[second.snapshot_id][0] == "active"
   assert (FIRST_USER, RETIRED_SKILL) not in rows
   assert rows[(FIRST_USER, successor)] == (second.snapshot_id, 5.0, 1.0)
   assert {snapshot_id for snapshot_id, _, _ in rows.values()} == {second.snapshot_id}

   reloads = audit_rows(engine, "content_snapshot_reloaded")

   assert len(reloads) == 1
   assert reloads[0][0] == f"content_snapshots:{second.snapshot_id}"
   assert reloads[0][1]["users"] == 2
   assert reloads[0][1]["merged"] == 1
   assert reloads[0][1]["kept"] == 3
   assert reloads[0][1]["rewritten"] == 0
   assert reloads[0][1]["orphaned"] == 0
   assert reloads[0][1]["previous_digest"] == snapshots[first_id][1]
   assert len(audit_rows(engine, "skill_merged")) == 1


def test_a_dangling_id_refuses_the_reload_and_keeps_the_old_snapshot(library):
   root, engine, first_id = library
   successor, other = live_skill_ids(root, 2)

   with OrmSession(engine) as db:
      add_row(db, FIRST_USER, successor, first_id, credited_successes=2.0)
      add_row(db, FIRST_USER, RETIRED_SKILL, first_id, credited_successes=3.0)
      add_row(db, SECOND_USER, DANGLING_SKILL, first_id)
      db.commit()

   add_tombstone(root, RETIRED_SKILL, successor)
   change_digest(root)
   before = state_rows(engine)

   with pytest.raises(ReloadRefused, match=DANGLING_SKILL):
      build_session_context(engine, root, today=TODAY)

   snapshots = snapshot_rows(engine)
   active = [row_id for row_id, (status, _) in snapshots.items() if status == "active"]
   rejected = [row_id for row_id, (status, _) in snapshots.items() if status == "rejected"]

   assert active == [first_id]
   assert len(rejected) == 1
   assert state_rows(engine) == before
   assert audit_rows(engine, "content_snapshot_reloaded") == []
   assert audit_rows(engine, "skill_merged") == []


def test_an_unchanged_digest_runs_no_reconciliation(library, monkeypatch):
   root, engine, first_id = library
   (skill_id,) = live_skill_ids(root, 1)
   calls = []
   reconcile = reload_module.reconcile_skills_state

   def recording_reconcile(*args, **kwargs):
      calls.append(kwargs.get("user_id"))

      return reconcile(*args, **kwargs)

   monkeypatch.setattr(reload_module, "reconcile_skills_state", recording_reconcile)

   with OrmSession(engine) as db:
      add_row(db, FIRST_USER, skill_id, "an-earlier-row-id")
      db.commit()

   again = build_session_context(engine, root, today=TODAY)

   assert again.snapshot_id == first_id
   assert calls == []
   assert state_rows(engine)[(FIRST_USER, skill_id)][0] == "an-earlier-row-id"
   assert audit_rows(engine, "content_snapshot_reloaded") == []

   change_digest(root)
   changed = build_session_context(engine, root, today=TODAY)

   assert calls == [FIRST_USER]
   assert state_rows(engine)[(FIRST_USER, skill_id)][0] == changed.snapshot_id


def test_a_tombstone_alone_changes_the_digest_and_reconciles(library):
   root, engine, first_id = library
   successor, other = live_skill_ids(root, 2)
   first_digest = snapshot_rows(engine)[first_id][1]

   with OrmSession(engine) as db:
      add_row(db, FIRST_USER, successor, first_id, credited_successes=2.0)
      add_row(db, FIRST_USER, RETIRED_SKILL, first_id, credited_successes=3.0, credited_failures=1.0)
      add_row(db, FIRST_USER, other, first_id)
      db.commit()

   add_tombstone(root, RETIRED_SKILL, successor)

   second = build_session_context(engine, root, today=TODAY)
   snapshots = snapshot_rows(engine)
   rows = state_rows(engine)
   reloads = audit_rows(engine, "content_snapshot_reloaded")

   assert second.snapshot_id != first_id
   assert snapshots[second.snapshot_id][0] == "active"
   assert snapshots[second.snapshot_id][1] != first_digest
   assert (FIRST_USER, RETIRED_SKILL) not in rows
   assert rows[(FIRST_USER, successor)] == (second.snapshot_id, 5.0, 1.0)
   assert len(reloads) == 1
   assert reloads[0][1]["merged"] == 1

