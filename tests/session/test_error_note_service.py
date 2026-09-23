"""The one-note-per-attempt rule belongs to the service, not to the route.

03's "The student's one-line error note" says the student writes one line before the corrected
item is requeued. The route refuses a second note, but the route is not the only caller: anything
reaching record_error_note directly could overwrite the first note and destroy the record of what
the student first thought. The guard is structural here so that every caller gets it.
"""
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models
from app.session import service


@pytest.fixture
def note_attempt(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with Session(engine) as db:
      db.add(
         models.Attempt(
            id="ATT-note",
            session_id="SES-note",
            item_id="ITM-note",
            started_at="2026-09-20T12:00:00+00:00",
            transcription_confirmed=0,
            served_stage="unsupported",
            format="short_answer",
            per_skill_states="{}",
            snapshot_id="SNP-note",
            created_at="2026-09-20T12:00:00+00:00",
            updated_at="2026-09-20T12:00:00+00:00",
         )
      )
      db.flush()

      yield db, "ATT-note"


def stored_note(db, attempt_id):
   return db.execute(
      select(models.Attempt.error_note).where(models.Attempt.id == attempt_id)
   ).scalar_one()


def test_the_service_stores_the_first_note(note_attempt):
   db, attempt_id = note_attempt

   service.record_error_note(db, attempt_id, "I differentiated instead of integrating")

   assert stored_note(db, attempt_id) == "I differentiated instead of integrating"


def test_the_service_refuses_a_second_note(note_attempt):
   db, attempt_id = note_attempt

   service.record_error_note(db, attempt_id, "the first thing I thought")

   with pytest.raises(service.ErrorNoteAlreadyWritten):
      service.record_error_note(db, attempt_id, "a tidier second thought")


def test_the_refused_second_note_never_reaches_the_column(note_attempt):
   db, attempt_id = note_attempt

   service.record_error_note(db, attempt_id, "the first thing I thought")

   with pytest.raises(service.ErrorNoteAlreadyWritten):
      service.record_error_note(db, attempt_id, "a tidier second thought")

   assert stored_note(db, attempt_id) == "the first thing I thought"


def test_the_service_refuses_a_note_that_is_not_one_line(note_attempt):
   db, attempt_id = note_attempt

   with pytest.raises(service.ErrorNoteNotOneLine):
      service.record_error_note(db, attempt_id, "first line\nsecond line")

   assert stored_note(db, attempt_id) is None


def test_the_service_refuses_a_note_with_a_carriage_return(note_attempt):
   db, attempt_id = note_attempt

   with pytest.raises(service.ErrorNoteNotOneLine):
      service.record_error_note(db, attempt_id, "first line\rsecond line")

   assert stored_note(db, attempt_id) is None
