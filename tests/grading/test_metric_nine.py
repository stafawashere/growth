"""Metric 9: free-response items attempted per week and the read-back abandonment rate, each with
its denominator, over rows the real routes wrote."""
from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.frq import metrics
from app.progress import learning_metrics


def age(world, attempt_id, days):
   moment = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

   with OrmSession(world.engine) as db:
      attempt = db.get(models.Attempt, attempt_id)
      attempt.started_at = moment
      attempt.submitted_at = moment if attempt.transcription_confirmed else None
      db.commit()


def test_weeks_with_no_item_are_listed_and_abandonment_counts_only_settled_photographed_captures(frq_world):
   typed = frq_world.open_attempt(capture_mode="typed")
   frq_world.client.post(f"/attempts/{typed}/typed", json={"read_back": {"parts": [], "unreadable": []}})
   photographed = frq_world.open_attempt()
   frq_world.upload(photographed, "critical_point_full__clean.jpg")
   frq_world.client.post(f"/attempts/{photographed}/transcription")
   frq_world.client.post(f"/attempts/{photographed}/transcription/confirm", json={})
   abandoned = frq_world.open_attempt()
   frq_world.upload(abandoned, "critical_point_full__blur.jpg")
   still_open = frq_world.open_attempt()
   frq_world.upload(still_open, "critical_point_full__clean.jpg")
   never_photographed = frq_world.open_attempt()
   age(frq_world, typed, 21)
   age(frq_world, abandoned, 2)
   age(frq_world, never_photographed, 3)
   now = datetime.now(timezone.utc)

   with OrmSession(frq_world.engine) as db:
      measured = metrics.metric_nine(db, frq_world.user_id, now)
      viewed = learning_metrics.free_response_participation(db, frq_world.user_id, date.today())

   weeks = measured["items_attempted_per_week"]

   assert len({typed, photographed, abandoned, still_open, never_photographed}) == 5
   assert weeks[0]["items_attempted"] == 1
   assert weeks[-1]["items_attempted"] == 1
   assert len(weeks) == 4
   assert len(measured["weeks_below_floor"]) == 2
   assert measured["abandonment"] == {"abandoned": 1, "captures_started": 2, "rate": 0.5, "still_open": 1}
   assert measured["pending_on_usage"] is False
   assert [entry["numerator"] for entry in viewed["values"]] == [1, 1]
   assert [entry["denominator"] for entry in viewed["values"]] == [7, 2]
   assert frq_world.client.get("/frq/metrics").status_code == 200
