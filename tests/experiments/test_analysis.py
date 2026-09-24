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
