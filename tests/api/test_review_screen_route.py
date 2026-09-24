"""GET /review, the student's review screen (08, "Review"), over stored attempts."""
from datetime import timedelta

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine import constants
from app.review.screen import PROVISIONAL_POINT_KEYS
from tests.api.conftest import TODAY

SESSION_ID = "SES-REVIEW"


def stamp_for(day, hour=9):
   return f"{day.isoformat()}T{hour:02d}:00:00+00:00"


def seed_attempts(engine, user_id, rows):
   """rows: (attempt id, item id, day, correct, confidence, error note)."""
   first_stamp = stamp_for(TODAY - timedelta(days=5))

   with OrmSession(engine) as db:
      db.add(
         models.Session(
            id=SESSION_ID,
            user_id=user_id,
            mode="learning",
            started_at=first_stamp,
            ended_at=first_stamp,
            queue="{}",
            snapshot_id="SNAP-0001",
            created_at=first_stamp,
            updated_at=first_stamp,
         )
      )

      for attempt_id, item_id, day, correct, confidence, note in rows:
         stamp = stamp_for(day)
         db.add(
            models.Attempt(
               id=attempt_id,
               session_id=SESSION_ID,
               item_id=item_id,
               started_at=stamp,
               submitted_at=stamp,
               confidence=confidence,
               confidence_source="student",
               correct=correct,
               served_stage="unsupported",
               format="short_answer",
               per_skill_states="{}",
               error_note=note,
               snapshot_id="SNAP-0001",
               created_at=stamp,
               updated_at=stamp,
            )
         )

      db.commit()


def test_review_refuses_a_request_without_a_session_cookie(world):
   assert world.client().get("/review").status_code == 401


def test_review_refuses_an_unreadable_day(world):
   client = world.client()
   world.register(client)

   assert client.get("/review", params={"today": "not-a-day"}).status_code == 422


def test_the_confident_error_leads_the_list_and_retried_or_expired_items_are_gone(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   yesterday = TODAY - timedelta(days=1)
   expired = TODAY - timedelta(days=constants.REQUEUE_GAP_DAYS_MAX + 1)
   seed_attempts(world.engine, user_id, [
      ("ATT-UNSURE", "BC-QA-01004-V00", TODAY - timedelta(days=2), 0, "unsure", None),
      ("ATT-CONFIDENT", "BC-QA-01004-V01", yesterday, 0, "confident", None),
      ("ATT-TODAY", "BC-QA-01004-V02", TODAY, 0, "guess", None),
      ("ATT-EXPIRED", "BC-QA-02002-V00", expired, 0, "unsure", None),
      ("ATT-MISSED", "BC-QA-02002-V01", yesterday, 0, "unsure", None),
      ("ATT-RETRY", "BC-QA-02002-V01", TODAY, 1, "unsure", None),
   ])

   payload = client.get("/review", params={"today": TODAY.isoformat()}).json()
   rows = [(entry["attempt_id"], entry["lane"], entry["days_until"]) for entry in payload["coming_back"]]

   assert rows == [
      ("ATT-CONFIDENT", "hypercorrection", 0),
      ("ATT-UNSURE", "requeue", 0),
      ("ATT-TODAY", "requeue", constants.REQUEUE_GAP_DAYS_MIN),
   ]
   assert payload["coming_back"][2]["returns_on"] == (TODAY + timedelta(days=constants.REQUEUE_GAP_DAYS_MIN)).isoformat()


def test_error_notes_come_newest_first_and_an_edit_through_the_session_route_replaces_one(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   seed_attempts(world.engine, user_id, [
      ("ATT-OLD", "BC-QA-01004-V00", TODAY - timedelta(days=3), 0, "unsure", "I cancelled a term, not a factor."),
      ("ATT-NEW", "BC-QA-01004-V01", TODAY - timedelta(days=1), 0, "unsure", "I dropped the sign."),
      ("ATT-SILENT", "BC-QA-01004-V02", TODAY, 0, "unsure", None),
   ])

   before = client.get("/review", params={"today": TODAY.isoformat()}).json()["error_notes"]
   edited = client.post(
      f"/sessions/{SESSION_ID}/attempts/ATT-OLD/error-note",
      json={"note": "I cancelled a term instead of a common factor."},
   )
   after = client.get("/review", params={"today": TODAY.isoformat()}).json()["error_notes"]

   assert [(note["attempt_id"], note["session_id"]) for note in before] == [
      ("ATT-NEW", SESSION_ID),
      ("ATT-OLD", SESSION_ID),
   ]
   assert before[1]["written_on"] == (TODAY - timedelta(days=3)).isoformat()
   assert edited.status_code == 200
   assert [note["note"] for note in after] == ["I dropped the sign.", "I cancelled a term instead of a common factor."]


def test_grading_disputes_are_empty_until_gradings_exist(world):
   client = world.client()
   world.register(client)

   payload = client.get("/review", params={"today": TODAY.isoformat()}).json()

   assert payload["grading_available"] is False
   assert payload["provisional_points"] == []
   assert PROVISIONAL_POINT_KEYS == ("grading_id", "attempt_id", "label", "point_label", "reason", "disputed")


def test_another_students_notes_and_corrections_never_appear(world):
   first = world.client()
   first_id = world.register(first).json()["user"]["id"]
   seed_attempts(world.engine, first_id, [
      ("ATT-THEIRS", "BC-QA-01004-V00", TODAY - timedelta(days=1), 0, "confident", "their note"),
   ])

   with OrmSession(world.engine) as db:
      db.query(models.Session).filter(models.Session.id == SESSION_ID).update({"user_id": "USR-SOMEONE-ELSE"})
      db.commit()

   payload = first.get("/review", params={"today": TODAY.isoformat()}).json()

   assert payload["coming_back"] == []
   assert payload["error_notes"] == []
