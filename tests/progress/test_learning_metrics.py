"""The P7 learning metrics on fixtures with known answers (11 P7 test_brier_and_calibration)."""
import pytest

from app.experiments.analysis import newcombe_interval
from app.progress import learning_metrics
from app.progress.attempt_log import AttemptRecord

TODAY_ISO = "2026-10-20"


def record(index, correct, confidence=None, day="2026-10-20", primary="BC-SKL-01001", fmt="short_answer", option=None):
   return AttemptRecord(
      id=f"ATT-{index:03d}",
      session_id="SES-1",
      session_mode="learning",
      item_id=f"ITEM-{index:03d}",
      archetype_id="BC-QA-01001",
      primary_skill=primary,
      skills=(primary,),
      submitted_at=f"{day}T10:00:00+00:00",
      correct=correct,
      confidence=confidence,
      confidence_source="student" if confidence else None,
      elapsed_ms=60000,
      served_stage="unsupported",
      format=fmt,
      response={"option_id": option} if option else {},
      experiment_arms={},
      image_ids=None,
      transcription_confirmed=False,
      updates_mastery=True,
   )


def values_by_label(metric):
   return {entry["label"]: entry for entry in metric["values"]}


def test_brier_and_calibration():
   from datetime import date

   attempts = [
      record(1, True, "confident"),
      record(2, True, "confident"),
      record(3, False, "confident"),
      record(4, False, "confident"),
      record(5, False, "guess"),
      record(6, True, None),
   ]
   metric = learning_metrics.calibration(attempts, date.fromisoformat(TODAY_ISO))
   values = values_by_label(metric)
   brier = values["Brier score"]
   gap = values["confidence minus accuracy"]

   expected_brier = (0.1 ** 2 * 2 + 0.9 ** 2 * 2 + 0.25 ** 2) / 5
   expected_gap = (0.9 * 4 + 0.25) / 5 - 2 / 5

   assert brier["denominator"] == 5
   assert brier["value"] == pytest.approx(expected_brier)
   assert gap["value"] == pytest.approx(expected_gap)
   assert metric["status"] == "measured"


def test_calibration_with_no_rated_attempt_states_a_zero_denominator():
   from datetime import date

   metric = learning_metrics.calibration([record(1, True, None)], date.fromisoformat(TODAY_ISO))

   assert metric["status"] == "no_data"
   assert all(entry["denominator"] == 0 and entry["value"] is None for entry in metric["values"])


def test_retention_buckets_read_the_gap_since_the_last_success():
   attempts = [
      record(1, True, day="2026-09-01"),
      record(2, False, day="2026-09-08"),
      record(3, True, day="2026-09-09"),
      record(4, True, day="2026-10-09"),
      record(5, True, day="2026-10-12"),
      record(6, False, day="2026-09-01", primary="BC-SKL-02002"),
      record(7, True, day="2026-09-08", primary="BC-SKL-02002"),
   ]
   attempts.sort(key=lambda entry: entry.submitted_at)
   values = values_by_label(learning_metrics.retention(attempts))
   week = values["first-attempt accuracy 5 to 9 days after a success"]
   month = values["first-attempt accuracy 25 to 35 days after a success"]

   assert (week["numerator"], week["denominator"]) == (0, 1)
   assert (month["numerator"], month["denominator"]) == (1, 1)


def test_newcombe_interval_matches_the_published_example():
   low, high = newcombe_interval(56, 70, 48, 80)

   assert low == pytest.approx(0.0524, abs=0.0001)
   assert high == pytest.approx(0.3339, abs=0.0001)
