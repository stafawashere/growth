"""R18's fail-closed coverage gap, written to audit_log alongside sessions.queue.

docs/plan/06-architecture.md's traceability row for the job worker names audit_log as where a
fringe archetype excluded from selection for want of a published item is recorded; before this,
app/session/build.py only ever put the gap in the in-memory Session's coverage_gaps, which
sessions.service serialises into the queue column and nowhere else. These tests drive
assemble_session with a real db session and a fixture archetype whose only item is a draft, the
same setup tests/engine/test_selection.py's test_fail_closed_no_item uses to force the gap, and
assert a real audit_log row exists and names the skill and the reason.
"""
import json
import random
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session.build import COVERAGE_GAP_ACTION, assemble_session
from tests.engine.conftest_selection import build_bank, build_graph, build_states, load_fixture

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0)
USER_ID = "USER-0001"
DRAFT_ARCHETYPE = "BC-QA-01008"


def audit_rows(db):
   return db.scalars(select(models.AuditLog)).all()


def test_a_fail_closed_coverage_gap_writes_an_audit_entry(tmp_path):
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture, draft_only={DRAFT_ARCHETYPE})
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      before = audit_rows(db)

      assert before == []

      session = assemble_session(
         states, graph, bank, [], [], random.Random(1), TODAY,
         now=NOW, db=db, user_id=USER_ID,
      )
      db.commit()

      assert DRAFT_ARCHETYPE in session.coverage_gaps

      after = audit_rows(db)
      gap_rows = [row for row in after if row.action == COVERAGE_GAP_ACTION]

      assert len(gap_rows) >= 1


def test_the_audit_entry_names_the_skill_and_the_reason(tmp_path):
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture, draft_only={DRAFT_ARCHETYPE})
   engine = models.make_engine(tmp_path / "growth.db")
   expected_skill = graph.primary_skill(DRAFT_ARCHETYPE)

   with OrmSession(engine) as db:
      assemble_session(
         states, graph, bank, [], [], random.Random(1), TODAY,
         now=NOW, db=db, user_id=USER_ID,
      )
      db.commit()

      gap_rows = [row for row in audit_rows(db) if row.action == COVERAGE_GAP_ACTION]

      assert len(gap_rows) == 1

      row = gap_rows[0]
      detail = json.loads(row.detail)

      assert detail["skill"] == expected_skill
      assert DRAFT_ARCHETYPE in row.subject
      assert "reason" in detail
      assert detail["reason"] != ""
      assert row.actor == USER_ID


def test_no_coverage_gap_writes_no_audit_entry(tmp_path):
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture)
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      assemble_session(
         states, graph, bank, [], [], random.Random(1), TODAY,
         now=NOW, db=db, user_id=USER_ID,
      )
      db.commit()

      gap_rows = [row for row in audit_rows(db) if row.action == COVERAGE_GAP_ACTION]

      assert gap_rows == []


def test_a_repeated_coverage_gap_writes_no_second_audit_entry(tmp_path):
   """One row per user per archetype. A gap persists until the operator authors the item, so a
   row per session opened would grow without bound and say nothing the first row did not."""
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture, draft_only={DRAFT_ARCHETYPE})
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      for _opening in range(3):
         assemble_session(
            states, graph, bank, [], [], random.Random(1), TODAY,
            now=NOW, db=db, user_id=USER_ID,
         )
         db.commit()

      gap_rows = [row for row in audit_rows(db) if row.action == COVERAGE_GAP_ACTION]

      assert len(gap_rows) == 1


def test_a_gap_recorded_for_another_user_still_writes_a_row(tmp_path):
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture, draft_only={DRAFT_ARCHETYPE})
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      for actor in (USER_ID, "USER-0002"):
         assemble_session(
            states, graph, bank, [], [], random.Random(1), TODAY,
            now=NOW, db=db, user_id=actor,
         )
         db.commit()

      gap_rows = [row for row in audit_rows(db) if row.action == COVERAGE_GAP_ACTION]
      actors = sorted(row.actor for row in gap_rows)

      assert actors == ["USER-0001", "USER-0002"]
