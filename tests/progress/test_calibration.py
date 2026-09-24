"""The calibration record behind the progress screen's curve (app/progress/calibration.py)."""
from datetime import date, timedelta

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.db.migrate import apply_additive_migrations, missing_columns
from app.engine.state import Confidence
from app.progress import calibration
from app.progress.calibration import RatedAttempt

TODAY = date(2026, 9, 23)

USER_ID = "USR-1"

OTHER_USER_ID = "USR-2"


def rated(confidence, correct):
   return RatedAttempt(Confidence(confidence), correct)


def mixed_attempts(total):
   levels = ("guess", "unsure", "confident")

   return [rated(levels[index % 3], index % 2 == 0) for index in range(total)]


@pytest.mark.parametrize(
   ("successes", "trials", "low", "high"),
   [
      (8, 10, 0.4902, 0.9433),
      (5, 10, 0.2366, 0.7634),
      (0, 10, 0.0, 0.2775),
      (10, 10, 0.7225, 1.0),
   ],
)
def test_wilson_interval_matches_published_values(successes, trials, low, high):
   computed_low, computed_high = calibration.wilson_interval(successes, trials)

   assert computed_low == pytest.approx(low, abs=1e-4)
   assert computed_high == pytest.approx(high, abs=1e-4)


def test_wilson_interval_refuses_zero_trials():
   with pytest.raises(ValueError):
      calibration.wilson_interval(0, 0)


def test_attempts_are_binned_by_stated_confidence():
   attempts = [
      rated("guess", False),
      rated("guess", True),
      rated("guess", False),
      rated("guess", False),
      rated("confident", True),
      rated("confident", True),
      rated("confident", False),
   ]

   record = calibration.calibration_record(attempts)
   by_level = {entry.confidence.value: entry for entry in record.bins}

   assert [entry.confidence.value for entry in record.bins] == ["guess", "unsure", "confident"]
   assert record.rated_attempts == 7
   assert (by_level["guess"].attempts, by_level["guess"].correct) == (4, 1)
   assert by_level["guess"].accuracy == pytest.approx(0.25)
   assert (by_level["confident"].attempts, by_level["confident"].correct) == (3, 2)
   assert by_level["confident"].accuracy == pytest.approx(2 / 3)
   assert by_level["unsure"].attempts == 0
   assert by_level["unsure"].accuracy is None
   assert by_level["unsure"].interval_low is None


def test_calibration_curve_threshold():
   short_view = calibration.calibration_view(calibration.calibration_record(mixed_attempts(29)), TODAY)
   full_view = calibration.calibration_view(calibration.calibration_record(mixed_attempts(30)), TODAY)

   assert short_view["available"] is False
   assert short_view["rated_attempts"] == 29
   assert short_view["attempts_needed"] == 1
   assert short_view["bins"] == []

   assert full_view["available"] is True
   assert full_view["rated_attempts"] == 30
   assert full_view["attempts_needed"] == 0
   assert [entry["attempts"] for entry in full_view["bins"]] == [10, 10, 10]
   assert sum(entry["attempts"] for entry in full_view["bins"]) == full_view["rated_attempts"]


def add_session(db, session_id, user_id):
   stamp = TODAY.isoformat()
   db.add(
      models.Session(
         id=session_id,
         user_id=user_id,
         mode="learning",
         started_at=stamp,
         queue="{}",
         snapshot_id="SNAP-1",
         created_at=stamp,
         updated_at=stamp,
      )
   )


def add_attempt(db, attempt_id, session_id, confidence, source, correct, submitted_day):
   stamp = f"{submitted_day.isoformat()}T10:00:00+00:00"
   db.add(
      models.Attempt(
         id=attempt_id,
         session_id=session_id,
         item_id="ITEM-1",
         started_at=stamp,
         submitted_at=stamp,
         confidence=confidence,
         confidence_source=source,
         correct=correct,
         served_stage="unsupported",
         format="short_answer",
         per_skill_states="{}",
         snapshot_id="SNAP-1",
         created_at=stamp,
         updated_at=stamp,
      )
   )


def test_only_graded_student_rated_attempts_inside_the_window_count(tmp_path):
   engine = models.make_engine(tmp_path / "calibration.db")
   first_day = TODAY - timedelta(days=calibration.WINDOW_DAYS - 1)

   with OrmSession(engine) as db:
      add_session(db, "SES-1", USER_ID)
      add_session(db, "SES-2", OTHER_USER_ID)
      add_attempt(db, "ATT-COUNTED-1", "SES-1", "confident", "student", 1, TODAY)
      add_attempt(db, "ATT-COUNTED-2", "SES-1", "guess", "student", 0, first_day)
      add_attempt(db, "ATT-UNGRADED", "SES-1", "confident", "student", None, TODAY)
      add_attempt(db, "ATT-UNRATED", "SES-1", None, None, 1, TODAY)
      add_attempt(db, "ATT-SWEPT", "SES-1", "unsure", "session_close", 1, TODAY)
      add_attempt(db, "ATT-UNATTRIBUTED", "SES-1", "unsure", None, 1, TODAY)
      add_attempt(db, "ATT-TOO-OLD", "SES-1", "confident", "student", 1, first_day - timedelta(days=1))
      add_attempt(db, "ATT-FUTURE", "SES-1", "confident", "student", 1, TODAY + timedelta(days=1))
      add_attempt(db, "ATT-OTHER-USER", "SES-2", "confident", "student", 1, TODAY)
      db.commit()

      counted = calibration.counted_attempts(db, USER_ID, TODAY)

   assert sorted(counted, key=lambda entry: entry.confidence.value) == [
      rated("confident", True),
      rated("guess", False),
   ]


def test_migration_attributes_only_ratings_the_sweep_could_not_have_written(tmp_path):
   engine = models.make_engine(tmp_path / "legacy.db")

   with OrmSession(engine) as db:
      add_session(db, "SES-1", USER_ID)
      add_attempt(db, "ATT-GUESS", "SES-1", "guess", None, 0, TODAY)
      add_attempt(db, "ATT-CONFIDENT", "SES-1", "confident", None, 1, TODAY)
      add_attempt(db, "ATT-UNSURE", "SES-1", "unsure", None, 1, TODAY)
      add_attempt(db, "ATT-UNRATED", "SES-1", None, None, 1, TODAY)
      db.commit()

   with engine.begin() as connection:
      connection.exec_driver_sql('ALTER TABLE "attempts" DROP COLUMN "confidence_source"')

   assert missing_columns(engine) == {"attempts": ("confidence_source",)}
   assert "attempts.confidence_source" in apply_additive_migrations(engine)

   with engine.connect() as connection:
      sources = dict(connection.execute(text("SELECT id, confidence_source FROM attempts")).all())

   assert sources == {
      "ATT-GUESS": "student",
      "ATT-CONFIDENT": "student",
      "ATT-UNSURE": None,
      "ATT-UNRATED": None,
   }
