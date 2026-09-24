"""GET /progress/calibration, the record the progress screen's calibration curve draws."""
from datetime import timedelta

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.progress.calibration import MINIMUM_RATED_ATTEMPTS
from tests.api.conftest import TODAY
from tests.api.test_routes import correct_answer_for, open_session


def attempt_once(client, session_id, today):
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": correct_answer_for(item),
         "elapsed_ms": 60000,
         "today": today.isoformat(),
      },
   )

   assert attempted.status_code == 200

   return attempted.json()["id"]


def seed_rated_attempts(engine, user_id, outcomes):
   stamp = f"{TODAY.isoformat()}T09:00:00+00:00"

   with OrmSession(engine) as db:
      db.add(
         models.Session(
            id="SES-SEEDED",
            user_id=user_id,
            mode="learning",
            started_at=stamp,
            ended_at=stamp,
            queue="{}",
            snapshot_id="SNAP-0001",
            created_at=stamp,
            updated_at=stamp,
         )
      )

      for index, (confidence, correct) in enumerate(outcomes):
         db.add(
            models.Attempt(
               id=f"ATT-SEEDED-{index:03d}",
               session_id="SES-SEEDED",
               item_id="ITEM-1",
               started_at=stamp,
               submitted_at=stamp,
               confidence=confidence,
               confidence_source="student",
               correct=correct,
               served_stage="unsupported",
               format="short_answer",
               per_skill_states="{}",
               snapshot_id="SNAP-0001",
               created_at=stamp,
               updated_at=stamp,
            )
         )

      db.commit()


def test_calibration_refuses_a_request_without_a_session_cookie(world):
   assert world.client().get("/progress/calibration").status_code == 401


def test_calibration_refuses_an_unreadable_day(world):
   client = world.client()
   world.register(client)

   assert client.get("/progress/calibration", params={"today": "not-a-day"}).status_code == 422


def test_a_student_rating_counts_and_a_rating_swept_in_at_close_does_not(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   rated_id = attempt_once(client, session_id, TODAY)
   rated = client.post(
      f"/sessions/{session_id}/attempts/{rated_id}/confidence",
      json={"confidence": "guess", "today": TODAY.isoformat()},
   )
   swept_id = attempt_once(client, session_id, TODAY)
   closed = client.post(f"/sessions/{session_id}/close", json={"today": TODAY.isoformat()})
   payload = client.get("/progress/calibration", params={"today": TODAY.isoformat()}).json()

   assert rated.status_code == 200
   assert closed.status_code == 200

   with OrmSession(world.engine) as db:
      rated_row = db.get(models.Attempt, rated_id)
      swept_row = db.get(models.Attempt, swept_id)

      assert (rated_row.confidence, rated_row.confidence_source) == ("guess", "student")
      assert (swept_row.confidence, swept_row.confidence_source) == ("unsure", "session_close")

   assert payload["available"] is False
   assert payload["rated_attempts"] == 1
   assert payload["attempts_needed"] == MINIMUM_RATED_ATTEMPTS - 1
   assert payload["bins"] == []


def test_thirty_rated_attempts_return_the_curve_with_counts_and_intervals(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   outcomes = (
      [("guess", 0)] * 8
      + [("guess", 1)] * 2
      + [("unsure", 0)] * 5
      + [("unsure", 1)] * 5
      + [("confident", 1)] * 8
      + [("confident", 0)] * 2
   )
   seed_rated_attempts(world.engine, user_id, outcomes)

   response = client.get("/progress/calibration", params={"today": TODAY.isoformat()})
   payload = response.json()
   bins = {entry["confidence"]: entry for entry in payload["bins"]}
   first_day = TODAY - timedelta(days=payload["window_days"] - 1)

   assert response.status_code == 200
   assert payload["available"] is True
   assert payload["rated_attempts"] == 30
   assert payload["attempts_needed"] == 0
   assert (payload["window_start"], payload["window_end"]) == (first_day.isoformat(), TODAY.isoformat())
   assert [entry["confidence"] for entry in payload["bins"]] == ["guess", "unsure", "confident"]
   assert (bins["confident"]["attempts"], bins["confident"]["correct"]) == (10, 8)
   assert bins["confident"]["accuracy"] == 0.8
   assert round(bins["confident"]["interval_low"], 4) == 0.4902
   assert round(bins["confident"]["interval_high"], 4) == 0.9433
   assert (bins["guess"]["attempts"], bins["guess"]["correct"]) == (10, 2)
