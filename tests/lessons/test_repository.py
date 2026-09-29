"""app/lessons/repository.py: what is servable, the user's state and the library payload
(docs/lessons/BUILD-PLAN.md Slice L1; docs/plan/15-lessons.md, State and Endpoints)."""
import json

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.lessons import repository
from app.lessons.ingest import ingest_lessons
from tests.lessons.test_ingest import LESSON_ID, NOW, SNAPSHOT_ID, signed_off, write_records

USER_ID = "USR-reader"
OTHER_USER_ID = "USR-other"
TARGET_ID = "BC-CON-02013"
UNIT_ID = "BC-UNIT-02"


@pytest.fixture()
def engine(tmp_path, context, hand_authored):
   engine = models.make_engine(tmp_path / "growth.db")
   directory = write_records(tmp_path / "lessons", signed_off(hand_authored))

   with OrmSession(engine) as db:
      ingest_lessons(db, directory, context.snapshot, SNAPSHOT_ID, now=NOW, context=context, verification_dir=tmp_path)
      db.commit()

   return engine


def test_a_signed_off_lesson_is_servable_for_its_target(engine):
   with OrmSession(engine) as db:
      assert repository.servable_map(db) == {TARGET_ID: (LESSON_ID, 1)}
      assert repository.servable(db, TARGET_ID).id == LESSON_ID
      assert repository.servable(db, "BC-CON-02014") is None


def test_a_stale_or_draft_row_is_not_servable(engine):
   with OrmSession(engine) as db:
      db.get(models.Lesson, (LESSON_ID, 1)).status = "stale"
      db.flush()

      assert repository.servable_map(db) == {}
      assert repository.servable_lesson(db, LESSON_ID) is None


def test_write_state_upserts_one_row_per_user_and_lesson(engine):
   with OrmSession(engine) as db:
      repository.write_state(db, USER_ID, LESSON_ID, now=NOW, status="served", version_seen=1)
      repository.write_state(db, USER_ID, LESSON_ID, now=NOW, status="read", read_source="library")
      states = repository.lesson_states(db, USER_ID)

   assert list(states) == [LESSON_ID]
   assert states[LESSON_ID]["status"] == "read"
   assert states[LESSON_ID]["version_seen"] == 1
   assert states[LESSON_ID]["read_source"] == "library"


def test_write_state_refuses_an_unknown_field(engine):
   with OrmSession(engine) as db:
      with pytest.raises(ValueError):
         repository.write_state(db, USER_ID, LESSON_ID, mastered=True)


def test_events_and_check_responses_are_written_and_attempts_untouched(engine):
   with OrmSession(engine) as db:
      repository.write_event(db, USER_ID, LESSON_ID, 1, "library", "opened", elapsed_ms=10, mode="text")
      repository.write_check_response(db, USER_ID, LESSON_ID, 1, f"{LESSON_ID}#chk-1", {"answer": 1}, False, None, 500)
      events = db.scalars(select(models.LessonEvent)).all()
      responses = db.scalars(select(models.LessonCheckResponse)).all()
      attempts = db.scalars(select(models.Attempt)).all()

   assert [(event.kind, event.event, event.mode) for event in events] == [("library", "opened", "text")]
   assert [(row.correct, json.loads(row.response)) for row in responses] == [(0, {"answer": 1})]
   assert attempts == []


def test_consume_lesson_slot_is_a_stub_until_the_session_layer_fills_it(engine):
   with OrmSession(engine) as db:
      assert repository.consume_lesson_slot(db, None, LESSON_ID, "completed") is None


def product_rule_entry(payload):
   concepts = payload["units"][0]["concepts"]

   return next(entry for entry in concepts if entry["concept_id"] == TARGET_ID)


def test_the_library_lists_units_in_curriculum_order(engine, snapshot):
   with OrmSession(engine) as db:
      payload = repository.library_listing(db, USER_ID, snapshot)

   curriculum = repository.load_curriculum()

   assert [unit["id"] for unit in payload["units"]] == [unit["id"] for unit in curriculum["units"]]
   assert all(entry["state"] == "not_available" for unit in payload["units"][2:] for entry in unit["concepts"])


def test_the_library_marks_a_signed_off_lesson_coming_up_then_read(engine, snapshot):
   with OrmSession(engine) as db:
      before = product_rule_entry(repository.library_listing(db, USER_ID, snapshot, unit_id=UNIT_ID))
      repository.write_state(db, USER_ID, LESSON_ID, now=NOW, status="read", read_at=NOW.isoformat())
      after = product_rule_entry(repository.library_listing(db, USER_ID, snapshot, unit_id=UNIT_ID))
      other = product_rule_entry(repository.library_listing(db, OTHER_USER_ID, snapshot, unit_id=UNIT_ID))

   assert before == {"concept_id": TARGET_ID, "name": "The product rule", "lesson_id": LESSON_ID, "version": 1, "servable": True, "state": "coming_up", "read_at": None}
   assert after["state"] == "read"
   assert after["read_at"] == NOW.isoformat()
   assert other["state"] == "coming_up"
