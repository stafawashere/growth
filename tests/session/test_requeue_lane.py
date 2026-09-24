"""The hypercorrection lane of 08's Review screen: a correction rated confident returns first."""
from datetime import date, timedelta

from app.engine import constants
from app.engine.state import FadingStage
from app.session.build import requeue_pending, requeue_ready

CORRECTED_ON = date(2026, 3, 1)


def attempt(item_id, attempted_on, corrected, confidence=None):
   return {
      "attempt_id": f"ATT-{item_id}-{attempted_on.isoformat()}",
      "archetype_id": "BC-QA-01004",
      "item_id": item_id,
      "corrected": corrected,
      "confidence": confidence,
      "stage": FadingStage.UNSUPPORTED,
      "attempted_on": attempted_on,
   }


def test_a_confident_correction_is_served_ahead_of_an_earlier_unsure_one():
   history = [
      attempt("ITEM-UNSURE", CORRECTED_ON, True, "unsure"),
      attempt("ITEM-CONFIDENT", CORRECTED_ON + timedelta(days=1), True, "confident"),
   ]
   today = CORRECTED_ON + timedelta(days=2)

   assert [item_id for item_id, _ in requeue_ready(history, today)] == ["ITEM-CONFIDENT", "ITEM-UNSURE"]


def test_the_pending_list_holds_todays_correction_and_drops_a_retried_or_expired_one():
   today = CORRECTED_ON + timedelta(days=constants.REQUEUE_GAP_DAYS_MAX + 1)
   expired_on = today - timedelta(days=constants.REQUEUE_GAP_DAYS_MAX + 1)
   history = [
      attempt("ITEM-EXPIRED", expired_on, True, "unsure"),
      attempt("ITEM-RETRIED", today - timedelta(days=1), True, "unsure"),
      attempt("ITEM-RETRIED", today, False, "unsure"),
      attempt("ITEM-TODAY", today, True, "guess"),
   ]

   pending = requeue_pending(history, today)

   assert [correction.item_id for correction in pending] == ["ITEM-TODAY"]
   assert requeue_ready(history, today) == []
