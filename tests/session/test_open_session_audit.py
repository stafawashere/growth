"""open_session carries the fail-closed coverage gap into audit_log.

app/session/build.py writes the gap when it is handed a db session and a user id, and
app/session/service.py is the only production caller of assemble_session, so without this wiring
the audit trail docs/plan/06-architecture.md's traceability row asks for exists in tests only.
"""
import random
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session import repository, service
from app.session.build import COVERAGE_GAP_ACTION
from tests.engine.conftest_selection import (
   ACCOUNT_CREATED_AT,
   build_bank,
   build_graph,
   build_states,
   load_fixture,
)
from tests.session.test_service import SNAPSHOT_ID, USER_ID, engine_graph_from

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)
DRAFT_ARCHETYPE = "BC-QA-01008"


def test_open_session_writes_the_coverage_gap_audit_entry(tmp_path):
   fixture = load_fixture()
   engine = models.make_engine(tmp_path / "growth.db")
   graph = build_graph(fixture)
   bank = build_bank(fixture, draft_only={DRAFT_ARCHETYPE})
   archetypes = {record["id"]: record for record in fixture["archetypes"]}

   with OrmSession(engine) as db:
      repository.save_states(db, USER_ID, build_states(fixture), SNAPSHOT_ID, ACCOUNT_CREATED_AT)
      db.commit()

      row = service.open_session(
         db,
         USER_ID,
         "learning",
         graph,
         engine_graph_from(fixture),
         archetypes,
         bank,
         SNAPSHOT_ID,
         TODAY,
         random.Random(7),
         now=NOW,
      )
      db.commit()

      gap_rows = [
         entry
         for entry in db.scalars(select(models.AuditLog)).all()
         if entry.action == COVERAGE_GAP_ACTION
      ]
      subjects = {entry.subject for entry in gap_rows}

      assert row.queue is not None
      assert len(gap_rows) >= 1
      assert f"archetypes:{DRAFT_ARCHETYPE}" in subjects
      assert all(entry.actor == USER_ID for entry in gap_rows)


def test_the_audit_entry_is_stamped_with_the_real_moment(tmp_path):
   """audit_log.at is when the entry was written, not local midnight of the session date.

   assemble_session's `now` is the engine's session clock, which is a naive datetime built from
   `today` when the caller supplies no time, so stamping the row with it wrote a host-timezone
   dependent value years away from the real one.
   """
   fixture = load_fixture()
   engine = models.make_engine(tmp_path / "growth.db")
   graph = build_graph(fixture)
   bank = build_bank(fixture, draft_only={DRAFT_ARCHETYPE})
   archetypes = {record["id"]: record for record in fixture["archetypes"]}
   before = datetime.now(timezone.utc)

   with OrmSession(engine) as db:
      repository.save_states(db, USER_ID, build_states(fixture), SNAPSHOT_ID, ACCOUNT_CREATED_AT)
      db.commit()

      service.open_session(
         db,
         USER_ID,
         "learning",
         graph,
         engine_graph_from(fixture),
         archetypes,
         bank,
         SNAPSHOT_ID,
         TODAY,
         random.Random(7),
      )
      db.commit()

      gap_rows = [
         entry
         for entry in db.scalars(select(models.AuditLog)).all()
         if entry.action == COVERAGE_GAP_ACTION
      ]

      assert len(gap_rows) >= 1

      for entry in gap_rows:
         stamped = datetime.fromisoformat(entry.at)

         assert stamped.tzinfo is not None
         assert stamped >= before
