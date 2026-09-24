"""Metric 9: free-response items attempted per week and the read-back abandonment rate, each with
its denominator, over rows the real routes wrote."""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.frq import metrics


def test_weeks_with_no_item_are_listed_and_abandonment_counts_only_settled_captures(frq_world):
   confirmed = frq_world.open_attempt(capture_mode="typed")
   frq_world.client.post(f"/attempts/{confirmed}/typed", json={"read_back": {"parts": [], "unreadable": []}})
   abandoned = frq_world.open_attempt(capture_mode="photo", item_id="FRQ-AGT-05007-01")
   still_open = frq_world.open_attempt(capture_mode="photo")
   now = datetime.now(timezone.utc)

   with OrmSession(frq_world.engine) as db:
      three_weeks_ago = (now - timedelta(days=21)).isoformat()
      first = db.get(models.Attempt, confirmed)
      first.started_at = three_weeks_ago
      first.submitted_at = three_weeks_ago
      old = db.get(models.Attempt, abandoned)
      old.started_at = (now - timedelta(days=2)).isoformat()
      db.commit()

      measured = metrics.metric_nine(db, frq_world.user_id, now)

   weeks = measured["items_attempted_per_week"]

   assert len({confirmed, abandoned, still_open}) == 3
   assert weeks[0]["items_attempted"] == 1
   assert len(weeks) == 4
   assert len(measured["weeks_below_floor"]) == 3
   assert measured["abandonment"] == {"abandoned": 1, "captures_started": 2, "rate": 0.5, "still_open": 1}
   assert measured["pending_on_usage"] is False
   assert frq_world.client.get("/frq/metrics").status_code == 200
