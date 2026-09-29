"""The pure parts of tools/throughput.py, the instrument behind the mastery pace goal: the day
count of the continuous run, the per-condition failure reading, the unit completion reading
and the failure grouping. The simulation itself is exercised by one short run."""
from datetime import date, datetime

import pytest

from app.engine import constants
from app.engine.state import FadingStage, SkillState
from app.engine.update import evaluate_mastery
from app.sim import whole_graph
from tools import throughput

TODAY = date(2027, 1, 20)


def satisfying_state():
   return SkillState(
      skill_id="BC-SKL-01024",
      beta=0.0,
      c=12.0,
      f=0.0,
      stability=60.0,
      difficulty=5.0,
      last_practised_at=datetime(2027, 1, 19),
      fading_stage=FadingStage.UNSUPPORTED,
      unaided_success_count=3,
      distinct_archetypes_succeeded={"BC-QA-01001", "BC-QA-01002"},
      success_days={date(2027, 1, 5), date(2027, 1, 12), date(2027, 1, 19)},
   )


def test_the_run_covers_every_day_from_the_start_to_the_exam_eve_inclusive():
   assert throughput.day_count(whole_graph.START_DAY, throughput.EXAM_EVE) == 219
   assert throughput.day_count(date(2026, 10, 1), date(2026, 10, 1)) == 1


def test_a_satisfying_state_fails_nothing_and_is_mastered():
   state = satisfying_state()

   assert throughput.failing_conditions(state, TODAY, 2) == ()
   assert evaluate_mastery(state, TODAY, 2) is True


BREAKS = [
   ("strength", {"c": 1.0}),
   ("unaided_successes", {"unaided_success_count": 2}),
   ("distinct_archetypes", {"distinct_archetypes_succeeded": {"BC-QA-01001"}}),
   ("distinct_days", {"success_days": {date(2027, 1, 5), date(2027, 1, 19)}}),
   ("day_span", {"success_days": {date(2027, 1, 17), date(2027, 1, 18), date(2027, 1, 19)}}),
   ("retention", {"stability": 1.0, "last_practised_at": datetime(2026, 12, 1)}),
]


@pytest.mark.parametrize("condition,change", BREAKS, ids=[row[0] for row in BREAKS])
def test_each_broken_condition_is_named_and_only_it(condition, change):
   state = satisfying_state()

   for field, value in change.items():
      setattr(state, field, value)

   assert throughput.failing_conditions(state, TODAY, 2) == (condition,)
   assert evaluate_mastery(state, TODAY, 2) is False


def test_the_archetype_requirement_follows_what_the_snapshot_offers():
   state = satisfying_state()
   state.distinct_archetypes_succeeded = {"BC-QA-01001"}

   assert throughput.failing_conditions(state, TODAY, 1) == ()
   assert throughput.failing_conditions(state, TODAY, 2) == ("distinct_archetypes",)
   assert throughput.failing_conditions(state, TODAY, None) == ("distinct_archetypes",)


def test_unit_completion_is_the_first_day_every_skill_of_the_unit_is_mastered():
   by_unit = {"BC-UNIT-01": ["a", "b"], "BC-UNIT-02": ["c"]}
   snapshots = [
      (1, {"BC-UNIT-01": 1, "BC-UNIT-02": 0}),
      (2, {"BC-UNIT-01": 2, "BC-UNIT-02": 0}),
      (3, {"BC-UNIT-01": 1, "BC-UNIT-02": 0}),
      (4, {"BC-UNIT-01": 2, "BC-UNIT-02": 0}),
   ]

   assert throughput.unit_completion_days(snapshots, by_unit) == {"BC-UNIT-01": 2, "BC-UNIT-02": None}


def test_failure_groups_are_counted_most_common_first():
   rows = [
      {"failing": ("strength",)},
      {"failing": ("distinct_archetypes",)},
      {"failing": ("strength",)},
      {"failing": ()},
   ]

   assert throughput.group_failures(rows) == [
      (("strength",), 2),
      ((), 1),
      (("distinct_archetypes",), 1),
   ]


def test_a_short_run_reports_every_unit_and_never_a_false_mastery():
   checkpoints = [5, 10]
   result = throughput.run_one(1, 3.0, 10, checkpoints, min_observations=1, world=throughput.WORLD_LEARNING)

   assert result["days"] == 10
   assert result["teachable"] == 539
   assert set(result["unit_sizes"]) == {f"BC-UNIT-{index:02d}" for index in range(1, 11)}
   assert sum(result["unit_sizes"].values()) == 539
   assert sorted(result["checkpoints"]) == checkpoints
   assert result["false_mastered"] == []
   assert result["served"] > 0
   assert len(result["stuck"]) > 0

   for row in result["stuck"]:
      assert all(name in throughput.CONDITION_NAMES for name in row["failing"])
      assert row["observations"] >= 1


def test_the_fixed_and_learning_worlds_are_both_offered():
   assert throughput.parse_args(["--world", "learning"]).world == throughput.WORLD_LEARNING
   assert throughput.parse_args([]).world == throughput.WORLD_FIXED
   assert throughput.parse_args(["--fast"]).fast is True


def test_the_mastery_threshold_is_the_one_the_plan_states():
   assert constants.MASTERY_THRESHOLD == 0.9
   assert constants.MASTERY_MIN_UNAIDED_SUCCESSES == 3
   assert constants.MASTERY_MIN_DAY_SPAN == 7
