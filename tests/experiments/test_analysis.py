"""Which attempts count as a delayed outcome for each A/B switch."""
from dataclasses import replace
from types import SimpleNamespace

from app.experiments import analysis, switches
from tests.progress.test_learning_metrics import record

ELABORATED = switches.DEFINITIONS[switches.FEEDBACK_ELABORATION].control_arm


def test_a_feedback_outcome_is_the_next_later_day_attempt_on_the_archetype():
   manipulated = replace(
      record(1, False, day="2026-10-01"),
      experiment_arms={switches.FEEDBACK_ELABORATION: ELABORATED},
   )
   same_day = record(2, False, day="2026-10-01")
   other_archetype = replace(record(3, False, day="2026-10-02"), archetype_id="BC-QA-09999")
   later = record(4, True, day="2026-10-03")
   after_that = record(5, False, day="2026-10-04")
   supported = replace(
      record(6, False, day="2026-10-05"),
      served_stage="completion",
      experiment_arms={switches.FEEDBACK_ELABORATION: ELABORATED},
   )

   outcomes = analysis.feedback_outcomes([manipulated, same_day, other_archetype, later, after_that, supported])

   assert outcomes == {ELABORATED: [1]}


def test_a_retrieval_outcome_is_the_first_attempt_two_to_four_weeks_after_assignment():
   assignment = SimpleNamespace(unit_id="BC-SKL-01001", arm="entry_3", assigned_at="2026-10-01T12:00:00+00:00")
   too_early = record(1, False, day="2026-10-14")
   first_in_window = record(2, True, day="2026-10-15")
   second_in_window = record(3, False, day="2026-10-20")

   outcomes = analysis.retrieval_outcomes([assignment], [too_early, first_in_window, second_in_window])

   assert outcomes == {"entry_3": [1]}


APPLIED = switches.DEFINITIONS[switches.TUTOR_PROFILE].treatment_arm
WITHHELD = switches.DEFINITIONS[switches.TUTOR_PROFILE].control_arm


def test_a_tutor_profile_outcome_is_the_next_later_day_unaided_attempt_on_the_archetype():
   assisted = record(1, False, day="2026-10-01")
   same_day = record(2, True, day="2026-10-01")
   later_but_assisted = record(3, True, day="2026-10-02")
   later_unaided = record(4, False, day="2026-10-03")
   withheld = record(5, True, day="2026-10-05")
   withheld_outcome = record(6, True, day="2026-10-06")
   switched_off = record(7, False, day="2026-10-07")
   after_switched_off = record(8, True, day="2026-10-08")
   assisted_arms = {
      assisted.id: APPLIED,
      later_but_assisted.id: APPLIED,
      withheld.id: WITHHELD,
      switched_off.id: None,
   }
   attempts = [assisted, same_day, later_but_assisted, later_unaided, withheld, withheld_outcome, switched_off, after_switched_off]

   outcomes = analysis.tutor_profile_outcomes(attempts, assisted_arms)

   assert outcomes == {APPLIED: [0, 0], WITHHELD: [1]}


def test_calibration_is_read_per_confidence_level_by_arm_over_assisted_attempts():
   attempts = [
      record(1, True, confidence="confident"),
      record(2, False, confidence="confident"),
      record(3, True, confidence="guess"),
      record(4, True, confidence="confident"),
      record(5, True, confidence=None),
      record(6, False, confidence="unsure"),
   ]
   assisted_arms = {"ATT-001": APPLIED, "ATT-002": APPLIED, "ATT-003": WITHHELD, "ATT-005": APPLIED, "ATT-006": None}

   guard = analysis.calibration_by_arm(attempts, assisted_arms)
   applied = {entry["confidence"]: entry for entry in guard[APPLIED]}
   withheld = {entry["confidence"]: entry for entry in guard[WITHHELD]}

   assert set(guard) == {APPLIED, WITHHELD}
   assert (applied["confident"]["attempts"], applied["confident"]["correct"]) == (2, 1)
   assert applied["guess"]["attempts"] == 0
   assert (withheld["guess"]["attempts"], withheld["guess"]["correct"]) == (1, 1)
   assert withheld["unsure"]["attempts"] == 0


def test_the_metrics_view_carries_the_tutor_profile_comparison_with_its_guard(tmp_path):
   from sqlalchemy.orm import Session as OrmSession

   from app.db import models

   engine = models.make_engine(tmp_path / "analysis.db")

   with OrmSession(engine) as db:
      views = [analysis.comparison_view(comparison) for comparison in analysis.comparisons(db, "USR-1", [])]

   named = {view["name"]: view for view in views}

   assert switches.TUTOR_PROFILE in named
   assert named[switches.TUTOR_PROFILE]["control"]["arm"] == WITHHELD
   assert named[switches.TUTOR_PROFILE]["stated"] is False
   assert set(named[switches.TUTOR_PROFILE]["guards"]["calibration"]) == {APPLIED, WITHHELD}
   assert named[switches.FEEDBACK_ELABORATION]["guards"] is None
