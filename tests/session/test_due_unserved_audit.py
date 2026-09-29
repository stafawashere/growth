"""D4 of docs/pedagogy/today/design.md: a due skill block 1 leaves unserved is written to audit_log
with its reason, once per user, skill and day."""
import json
import random
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session.build import DUE_UNSERVED_ACTION, NO_PUBLISHED_ITEM, assemble_session
from tests.engine.conftest_selection import build_bank, build_graph, build_states, load_fixture

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0)
USER_ID = "USER-0001"
UNPUBLISHED_SKILL = "BC-SKL-02032"
ONLY_ARCHETYPE = "BC-QA-02007"


def assemble_with_unpublished_due_skill(db):
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture, mastered=frozenset({UNPUBLISHED_SKILL}))
   states[UNPUBLISHED_SKILL].stability = 2.0
   states[UNPUBLISHED_SKILL].difficulty = 5.0
   states[UNPUBLISHED_SKILL].last_practised_at = datetime(2026, 2, 1, 9, 0, 0)
   bank = build_bank(fixture, draft_only={ONLY_ARCHETYPE})

   return assemble_session(
      states, graph, bank, [], [], random.Random(1), TODAY, now=NOW, db=db, user_id=USER_ID,
   )


def unserved_rows(db):
   return db.scalars(select(models.AuditLog).where(models.AuditLog.action == DUE_UNSERVED_ACTION)).all()


def test_a_due_skill_with_no_published_item_is_recorded_with_its_reason(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      session = assemble_with_unpublished_due_skill(db)
      db.commit()
      rows = [row for row in unserved_rows(db) if row.subject == f"skills:{UNPUBLISHED_SKILL}"]

   assert UNPUBLISHED_SKILL in session.due_queue.skills
   assert session.due_queue.uncovered_reasons[UNPUBLISHED_SKILL] == NO_PUBLISHED_ITEM
   assert len(rows) == 1

   detail = json.loads(rows[0].detail)

   assert detail["reason"] == NO_PUBLISHED_ITEM
   assert detail["day"] == TODAY.isoformat()
   assert rows[0].actor == USER_ID


def test_a_second_assembly_the_same_day_writes_no_second_row(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      assemble_with_unpublished_due_skill(db)
      db.commit()
      first = len(unserved_rows(db))
      assemble_with_unpublished_due_skill(db)
      db.commit()
      second = len(unserved_rows(db))

   assert first >= 1
   assert second == first
