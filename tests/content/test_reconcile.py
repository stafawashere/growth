"""docs/plan/06-architecture.md "Library updates and retired IDs"."""
import json
from datetime import date, datetime

import pytest
from sqlalchemy.orm import Session

from app.content.reconcile import ReloadRefused, reconcile_skills_state
from app.db.models import AuditLog, SkillState, make_engine

TODAY = date(2026, 9, 19)
USER = "user-1"
SNAPSHOT_ROW_ID = "snapshot-row-1"


class FakeSnapshot:
   def __init__(self, skills, prerequisites, digest):
      self.skills = skills
      self.prerequisites = prerequisites
      self.digest = digest


def _row(session, skill_id, **overrides):
   fields = {
      "user_id": USER,
      "skill_id": skill_id,
      "snapshot_id": "old-snapshot",
      "beta": 0.0,
      "credited_successes": 0.0,
      "credited_failures": 0.0,
      "stability": None,
      "difficulty": None,
      "last_practised_at": None,
      "fading_stage": "unsupported",
      "observation_count": 0,
      "distinct_archetypes_succeeded": "[]",
      "success_days": "[]",
      "mastered": 0,
      "mastered_at": None,
      "hypercorrection_due": None,
      "consecutive_successes": 0,
      "consecutive_failures": 0,
      "concept_opener_done": 0,
      "unaided_success_count": 0,
      "created_at": "2026-09-19T00:00:00",
      "updated_at": "2026-09-19T00:00:00",
   }
   fields.update(overrides)
   row = SkillState(**fields)
   session.add(row)

   return row


def _engine(tmp_path):
   return make_engine(tmp_path / "p1.sqlite")


def _reconcile(session, snapshot, ids_registry, today=TODAY, snapshot_row_id=SNAPSHOT_ROW_ID):
   return reconcile_skills_state(session, snapshot, ids_registry, today, snapshot_row_id)


def test_reload_keeps_active_skill_and_sets_snapshot_id(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99001")
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99001": {}}, prerequisites={}, digest="dig-1")
      ids_registry = {"BC-SKL-99001": {"status": "active"}}

      report = _reconcile(session, snapshot, ids_registry)
      session.commit()

      row = session.get(SkillState, (USER, "BC-SKL-99001"))

      assert row.snapshot_id == SNAPSHOT_ROW_ID
      assert ("user-1", "BC-SKL-99001") in report.kept


def test_reload_rewrites_superseded_skill(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99002", credited_successes=5.0, credited_failures=1.0)
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-2")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      report = _reconcile(session, snapshot, ids_registry)
      session.commit()

      old_row = session.get(SkillState, (USER, "BC-SKL-99002"))
      new_row = session.get(SkillState, (USER, "BC-SKL-99003"))

      assert old_row is None
      assert new_row is not None
      assert new_row.credited_successes == 5.0
      assert new_row.snapshot_id == SNAPSHOT_ROW_ID
      assert ("BC-SKL-99002", "BC-SKL-99003") in report.rewritten


def test_reload_merges_into_existing_successor_and_recomputes_mastered(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      old_low_day = (TODAY.replace(day=10)).isoformat()
      old_mid_day = (TODAY.replace(day=13)).isoformat()
      high_day = TODAY.isoformat()

      _row(
         session,
         "BC-SKL-99002",
         credited_successes=200.0,
         stability=60.0,
         last_practised_at=datetime(TODAY.year, TODAY.month, TODAY.day).isoformat(),
         distinct_archetypes_succeeded='["BC-QA-01004"]',
         success_days=f'["{old_low_day}", "{old_mid_day}"]',
         unaided_success_count=1,
      )
      _row(
         session,
         "BC-SKL-99003",
         credited_successes=200.0,
         stability=60.0,
         last_practised_at=datetime(TODAY.year, TODAY.month, TODAY.day).isoformat(),
         distinct_archetypes_succeeded='["BC-QA-01008"]',
         success_days=f'["{high_day}"]',
         unaided_success_count=2,
      )
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-3")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      report = _reconcile(session, snapshot, ids_registry)
      session.commit()

      old_row = session.get(SkillState, (USER, "BC-SKL-99002"))
      merged_row = session.get(SkillState, (USER, "BC-SKL-99003"))

      assert old_row is None
      assert merged_row.credited_successes == 400.0
      assert merged_row.unaided_success_count == 3
      assert set(json.loads(merged_row.distinct_archetypes_succeeded)) == {
         "BC-QA-01004",
         "BC-QA-01008",
      }
      assert merged_row.mastered == 1
      assert merged_row.snapshot_id == SNAPSHOT_ROW_ID
      assert ("BC-SKL-99002", "BC-SKL-99003") in report.merged


def test_reload_merge_carries_difficulty_with_winning_stability(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99002", stability=30.0, difficulty=4.0)
      _row(session, "BC-SKL-99003", stability=60.0, difficulty=7.0)
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-7")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      _reconcile(session, snapshot, ids_registry)
      session.commit()

      merged_row = session.get(SkillState, (USER, "BC-SKL-99003"))

      assert merged_row.stability == 60.0
      assert merged_row.difficulty == 7.0


def test_reload_merge_carries_difficulty_from_old_row_when_it_wins(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99002", stability=90.0, difficulty=3.0)
      _row(session, "BC-SKL-99003", stability=20.0, difficulty=9.0)
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-8")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      _reconcile(session, snapshot, ids_registry)
      session.commit()

      merged_row = session.get(SkillState, (USER, "BC-SKL-99003"))

      assert merged_row.stability == 90.0
      assert merged_row.difficulty == 3.0


def test_reload_merge_preserves_flags_and_resets_consecutive_counters(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(
         session,
         "BC-SKL-99002",
         fading_stage="example",
         hypercorrection_due="2026-09-25",
         consecutive_successes=4,
         consecutive_failures=1,
         concept_opener_done=1,
      )
      _row(
         session,
         "BC-SKL-99003",
         fading_stage="unsupported",
         hypercorrection_due="2026-09-20",
         consecutive_successes=2,
         consecutive_failures=3,
         concept_opener_done=0,
      )
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-9")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      report = _reconcile(session, snapshot, ids_registry)
      session.commit()

      merged_row = session.get(SkillState, (USER, "BC-SKL-99003"))

      assert merged_row.fading_stage == "example"
      assert merged_row.hypercorrection_due == "2026-09-25"
      assert merged_row.concept_opener_done == 1
      assert merged_row.consecutive_successes == 0
      assert merged_row.consecutive_failures == 0
      assert any("consecutive" in note for note in report.notes)


def test_reload_merge_union_failing_d2_clears_mastered(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      only_day = TODAY.isoformat()

      _row(
         session,
         "BC-SKL-99002",
         credited_successes=200.0,
         stability=60.0,
         last_practised_at=datetime(TODAY.year, TODAY.month, TODAY.day).isoformat(),
         distinct_archetypes_succeeded='["BC-QA-01004"]',
         success_days=f'["{only_day}"]',
         unaided_success_count=3,
         mastered=1,
         mastered_at="2026-09-01T00:00:00",
      )
      _row(
         session,
         "BC-SKL-99003",
         credited_successes=200.0,
         stability=60.0,
         last_practised_at=datetime(TODAY.year, TODAY.month, TODAY.day).isoformat(),
         distinct_archetypes_succeeded='["BC-QA-01008"]',
         success_days=f'["{only_day}"]',
         unaided_success_count=3,
         mastered=1,
         mastered_at="2026-09-01T00:00:00",
      )
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-10")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      _reconcile(session, snapshot, ids_registry)
      session.commit()

      merged_row = session.get(SkillState, (USER, "BC-SKL-99003"))

      assert merged_row.mastered == 0
      assert merged_row.mastered_at is None


def test_reload_orphans_tombstone_without_successor(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99004")
      session.commit()

      snapshot = FakeSnapshot(skills={}, prerequisites={}, digest="dig-4")
      ids_registry = {"BC-SKL-99004": {"status": "retired"}}

      report = _reconcile(session, snapshot, ids_registry)
      session.commit()

      row = session.get(SkillState, (USER, "BC-SKL-99004"))

      assert row is not None
      assert ("user-1", "BC-SKL-99004") in report.orphaned


def test_reload_refuses_inactive_successor(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99005")
      session.commit()

      snapshot = FakeSnapshot(skills={}, prerequisites={}, digest="dig-5")
      ids_registry = {
         "BC-SKL-99005": {"status": "retired", "superseded_by": "BC-SKL-99999"},
      }

      with pytest.raises(ReloadRefused) as excinfo:
         _reconcile(session, snapshot, ids_registry)

      assert "BC-SKL-99005" in str(excinfo.value)
      assert "BC-SKL-99999" in str(excinfo.value)


def test_reload_writes_audit_entry(tmp_path):
   engine = _engine(tmp_path)

   with Session(engine) as session:
      _row(session, "BC-SKL-99002")
      session.commit()

      snapshot = FakeSnapshot(skills={"BC-SKL-99003": {}}, prerequisites={}, digest="dig-6")
      ids_registry = {
         "BC-SKL-99002": {"status": "retired", "superseded_by": "BC-SKL-99003"},
         "BC-SKL-99003": {"status": "active"},
      }

      _reconcile(session, snapshot, ids_registry)
      session.commit()

      entries = session.query(AuditLog).all()

      assert len(entries) == 1
      assert "BC-SKL-99002" in entries[0].detail
      assert "BC-SKL-99003" in entries[0].detail
