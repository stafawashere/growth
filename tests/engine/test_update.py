import hashlib
import math
import re
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings, strategies as st

from app.engine import constants
from app.engine import fsrs
from app.engine.fsrs_constants import (
   FSRS7_DEFAULT_PARAMETERS,
   MODEL_SOURCE_FIXTURE,
   MODEL_SOURCE_SHA256,
   SOURCE_COMMIT,
   SOURCE_SHA256,
)
from app.engine.state import (
   Confidence,
   FadingStage,
   MasteryState,
   PARTIAL_STATES,
   ResponseFormat,
   SkillState,
)
from app.engine.strength import strength
from app.engine.update import (
   Observation,
   apply_observation,
   credit_for,
   evaluate_mastery,
   grade_for,
   hard_ancestor_hops,
   rule_based_mastery_states,
)

TODAY = date(2026, 9, 19)
NO_FEEDBACK_ARCHETYPE = "BC-QA-01004"
SOURCE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "fsrs_rs_inference_v7_c137ee6.rs"
MODEL_SOURCE_PATH = Path(__file__).resolve().parents[2] / MODEL_SOURCE_FIXTURE
PROPERTY_EXAMPLES = 1000


def observation_for(archetype, skills, mastery_state, **overrides):
   fields = {
      "archetype_id": archetype,
      "skills": list(skills),
      "per_skill_states": {skill: mastery_state for skill in skills},
      "response_format": ResponseFormat.SHORT_ANSWER,
      "confidence": Confidence.CONFIDENT,
      "elapsed_ms": 90_000,
      "served_stage": FadingStage.UNSUPPORTED,
      "archetype_median_ms": 120_000,
   }
   fields.update(overrides)

   return Observation(**fields)


def test_credit_assignment_table(states, graph, archetypes):
   expected_short_answer = {
      MasteryState.MASTERED: (1.0, 0.0),
      MasteryState.PARTIAL_PROCEDURAL: (0.0, 0.5),
      MasteryState.PARTIAL_CONCEPTUAL: (0.0, 0.5),
      MasteryState.PARTIAL_UNSPECIFIED: (0.0, 0.5),
      MasteryState.NOTATION_ONLY: (0.25, 0.0),
      MasteryState.PREREQUISITE_GAP: (0.0, 0.0),
      MasteryState.NOT_MASTERED: (0.0, 1.0),
      MasteryState.NOT_ATTEMPTED: (0.0, 0.0),
   }

   for mastery_state, expected in expected_short_answer.items():
      assert credit_for(mastery_state, ResponseFormat.SHORT_ANSWER) == expected

   assert credit_for(MasteryState.MASTERED, ResponseFormat.MCQ) == (
      constants.MCQ_SUCCESS_CREDIT,
      0.0,
   )
   assert credit_for(MasteryState.NOTATION_ONLY, ResponseFormat.MCQ) == (
      0.25 * constants.MCQ_SUCCESS_CREDIT,
      0.0,
   )
   assert credit_for(MasteryState.NOT_MASTERED, ResponseFormat.MCQ) == (0.0, 1.0)

   for mastery_state, expected in expected_short_answer.items():
      skill = "BC-SKL-01024"
      state = SkillState(skill_id=skill, beta=0.0)
      probe_states = dict(states)
      probe_states[skill] = state
      apply_observation(
         probe_states,
         graph,
         observation_for(NO_FEEDBACK_ARCHETYPE, [skill], mastery_state),
         TODAY,
      )

      assert (state.c, state.f) == expected
      assert state.observation_count == 1

      is_full_success = mastery_state == MasteryState.MASTERED
      expected_days = {TODAY} if is_full_success else set()
      expected_archetypes = {NO_FEEDBACK_ARCHETYPE} if is_full_success else set()
      expected_unaided = 1 if is_full_success else 0

      assert state.success_days == expected_days
      assert state.distinct_archetypes_succeeded == expected_archetypes
      assert state.unaided_success_count == expected_unaided

   archetype = archetypes[NO_FEEDBACK_ARCHETYPE]
   loaded = archetype["skills"]
   primary = loaded[0]

   correct = rule_based_mastery_states(archetype, {"correct": True})
   assert set(correct) == set(loaded)
   assert set(correct.values()) == {MasteryState.MASTERED}

   error_path_skills = [loaded[2], loaded[3]]
   with_path = rule_based_mastery_states(
      archetype,
      {"correct": False, "error_path_skills": error_path_skills},
   )
   assert with_path[loaded[2]] == MasteryState.NOT_MASTERED
   assert with_path[loaded[3]] == MasteryState.NOT_MASTERED
   assert with_path[primary] == MasteryState.NOT_ATTEMPTED

   without_path = rule_based_mastery_states(archetype, {"correct": False})
   assert without_path[primary] == MasteryState.NOT_MASTERED
   assert set(without_path[skill] for skill in loaded[1:]) == {MasteryState.NOT_ATTEMPTED}

   misnotated = rule_based_mastery_states(
      archetype,
      {"correct": False, "equivalent_but_misnotated": True},
   )
   assert set(misnotated.values()) == {MasteryState.NOTATION_ONLY}

   target = "BC-SKL-03006"
   prerequisite = sorted(graph.hard_parents[target])[0]
   gap_observation = observation_for(
      "BC-QA-03008",
      [target],
      MasteryState.PREREQUISITE_GAP,
      named_prerequisite=prerequisite,
   )
   apply_observation(states, graph, gap_observation, TODAY)

   assert (states[target].c, states[target].f) == (0.0, 0.0)
   assert states[prerequisite].f == pytest.approx(constants.PREREQUISITE_GAP_FAILURE)

   for dependant in graph.hard_children[prerequisite]:
      is_target = dependant == target

      if is_target:
         continue

      assert states[dependant].f == pytest.approx(constants.PREREQUISITE_GAP_FORWARD_FAILURE)


@settings(max_examples=PROPERTY_EXAMPLES, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
   counted_successes=st.floats(min_value=0.0, max_value=60.0),
   counted_failures=st.floats(min_value=0.0, max_value=60.0),
   gap_flags=st.lists(st.booleans(), min_size=4, max_size=4),
)
def test_correct_never_lowers_m(
   states,
   graph,
   archetypes,
   counted_successes,
   counted_failures,
   gap_flags,
):
   """A demonstrated skill is never charged, not even as the named prerequisite of a gap."""
   for state in states.values():
      state.c = counted_successes
      state.f = counted_failures

   before = {skill: strength(state) for skill, state in states.items()}
   archetype = archetypes[NO_FEEDBACK_ARCHETYPE]
   loaded = archetype["skills"]
   named = loaded[0]
   per_skill = {named: MasteryState.MASTERED}

   for skill, is_gap in zip(loaded[1:], gap_flags):
      per_skill[skill] = MasteryState.PREREQUISITE_GAP if is_gap else MasteryState.MASTERED

   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         loaded,
         MasteryState.MASTERED,
         per_skill_states=per_skill,
         named_prerequisite=named,
      ),
      TODAY,
   )

   assert states[named].f == pytest.approx(counted_failures)

   for skill, state in states.items():
      assert strength(state) >= before[skill] - 1e-12


@settings(max_examples=PROPERTY_EXAMPLES, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(
   gamma=st.floats(min_value=0.05, max_value=2.0),
   rho=st.floats(min_value=-2.0, max_value=-0.01),
   counted_successes=st.floats(min_value=0.0, max_value=60.0),
   counted_failures=st.floats(min_value=0.0, max_value=60.0),
   partial=st.sampled_from(sorted(PARTIAL_STATES)),
)
def test_partial_never_raises_m(
   states,
   graph,
   archetypes,
   gamma,
   rho,
   counted_successes,
   counted_failures,
   partial,
):
   original_gamma = constants.GAMMA
   original_rho = constants.RHO
   constants.GAMMA = gamma
   constants.RHO = rho

   try:
      for state in states.values():
         state.c = counted_successes
         state.f = counted_failures

      before = {skill: strength(state) for skill, state in states.items()}
      archetype = archetypes[NO_FEEDBACK_ARCHETYPE]
      apply_observation(
         states,
         graph,
         observation_for(NO_FEEDBACK_ARCHETYPE, archetype["skills"], partial),
         TODAY,
      )

      for skill, state in states.items():
         assert strength(state) <= before[skill] + 1e-12
   finally:
      constants.GAMMA = original_gamma
      constants.RHO = original_rho


def source_default_parameters():
   """The DEFAULT_PARAMETERS array in the pinned fsrs-rs inference_v7.rs (R28)."""
   text = SOURCE_PATH.read_text()
   block = re.search(
      r"pub static DEFAULT_PARAMETERS: \[f32; (\d+)\] = \[(.*?)\];",
      text,
      re.DOTALL,
   )

   assert block is not None

   declared_count = int(block.group(1))
   values = tuple(float(value) for value in block.group(2).replace("\n", " ").split(",") if value.strip())

   assert declared_count == len(values)

   return values


def test_retrievability_monotone():
   digest = hashlib.sha256(SOURCE_PATH.read_bytes()).hexdigest()

   assert digest == SOURCE_SHA256
   assert len(SOURCE_COMMIT) == 40

   model_text = MODEL_SOURCE_PATH.read_text()

   assert hashlib.sha256(MODEL_SOURCE_PATH.read_bytes()).hexdigest() == MODEL_SOURCE_SHA256
   assert re.search(r"const PARAM_LEN: usize = 34;", model_text) is not None

   from_source = source_default_parameters()

   assert len(from_source) == 34
   assert len(FSRS7_DEFAULT_PARAMETERS) == 34
   assert fsrs.DEFAULT_PARAMETERS is FSRS7_DEFAULT_PARAMETERS

   for index, value in enumerate(from_source):
      assert FSRS7_DEFAULT_PARAMETERS[index] == value

   previous = 1.1

   for elapsed_days in range(0, 120):
      current = fsrs.retrievability(10.0, elapsed_days)

      assert current < previous
      assert 0.0 < current <= 1.0

      previous = current

   assert fsrs.retrievability(None, 0) == 1.0
   assert fsrs.retrievability(None, 900) == 1.0
   assert fsrs.retrievability(10.0, 10.0) == pytest.approx(0.9096256493, abs=1e-9)
   assert abs(fsrs.retrievability(10.0, 10.0) - 0.9) > 1e-3


def satisfying_state(skill_id, today):
   state = SkillState(skill_id=skill_id, beta=0.0, fading_stage=FadingStage.UNSUPPORTED)
   state.c = 400.0
   state.distinct_archetypes_succeeded = {"BC-QA-01004", "BC-QA-01008"}
   state.success_days = {today - timedelta(days=9), today - timedelta(days=4), today}
   state.unaided_success_count = 3
   state.stability = 60.0
   state.last_practised_at = datetime(today.year, today.month, today.day)

   return state


MASTERY_VIOLATIONS = [
   ("strength_below_threshold", {"c": 1.0}),
   ("too_few_unaided_successes", {"unaided_success_count": 2}),
   ("too_few_archetypes", {"distinct_archetypes_succeeded": {"BC-QA-01004"}}),
   (
      "too_few_days",
      {"success_days": {TODAY - timedelta(days=8), TODAY}},
   ),
   (
      "span_under_seven_days",
      {
         "success_days": {
            TODAY - timedelta(days=2),
            TODAY - timedelta(days=1),
            TODAY,
         }
      },
   ),
   (
      "retrievability_below_desired",
      {"stability": 1.0, "last_practised_at": datetime(2026, 7, 1)},
   ),
]


@pytest.mark.parametrize("label,violation", MASTERY_VIOLATIONS, ids=[row[0] for row in MASTERY_VIOLATIONS])
def test_mastery_conditions(states, graph, label, violation):
   baseline = satisfying_state("BC-SKL-01024", TODAY)

   assert evaluate_mastery(baseline, TODAY) is True

   broken = satisfying_state("BC-SKL-01024", TODAY)

   for field, value in violation.items():
      setattr(broken, field, value)

   assert evaluate_mastery(broken, TODAY) is False

   skill = "BC-SKL-01024"
   states[skill] = SkillState(skill_id=skill, beta=0.0, fading_stage=FadingStage.UNSUPPORTED)
   repeat = observation_for(NO_FEEDBACK_ARCHETYPE, [skill], MasteryState.MASTERED)
   apply_observation(states, graph, repeat, TODAY)
   apply_observation(states, graph, repeat, TODAY)

   assert states[skill].success_days == {TODAY}
   assert states[skill].mastered is False


def test_fading_ladder(states, graph):
   skill = "BC-SKL-01024"
   state = SkillState(skill_id=skill, beta=0.0, fading_stage=FadingStage.EXAMPLE)
   states[skill] = state

   def push(mastery_state, stage):
      apply_observation(
         states,
         graph,
         observation_for(NO_FEEDBACK_ARCHETYPE, [skill], mastery_state, served_stage=stage),
         TODAY,
      )

   push(MasteryState.MASTERED, FadingStage.EXAMPLE)

   assert state.fading_stage == FadingStage.EXAMPLE

   push(MasteryState.MASTERED, FadingStage.EXAMPLE)

   assert state.fading_stage == FadingStage.COMPLETION

   push(MasteryState.MASTERED, FadingStage.COMPLETION)

   assert state.fading_stage == FadingStage.COMPLETION

   push(MasteryState.MASTERED, FadingStage.COMPLETION)

   assert state.fading_stage == FadingStage.UNSUPPORTED

   push(MasteryState.NOT_MASTERED, FadingStage.UNSUPPORTED)

   assert state.fading_stage == FadingStage.UNSUPPORTED
   assert state.hypercorrection_due == TODAY + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)

   push(MasteryState.NOT_MASTERED, FadingStage.UNSUPPORTED)

   assert state.fading_stage == FadingStage.COMPLETION

   state.mastered = True
   state.mastered_at = datetime(2026, 9, 1)
   state.consecutive_failures = 0
   state.fading_stage = FadingStage.UNSUPPORTED
   push(MasteryState.NOT_MASTERED, FadingStage.UNSUPPORTED)

   assert state.mastered is False
   assert state.mastered_at is None
   assert state.fading_stage == FadingStage.UNSUPPORTED


def test_propagation_weights(states, graph):
   target = "BC-SKL-03006"
   apply_observation(
      states,
      graph,
      observation_for("BC-QA-03008", [target], MasteryState.MASTERED),
      TODAY,
   )

   hops = hard_ancestor_hops(target, graph.hard_parents)
   supporting = graph.supporting_parents.get(target, set())

   assert len(hops) > 0

   for skill, hop_count in hops.items():
      is_one_hop = hop_count == 1
      is_two_hop = hop_count == 2

      if is_one_hop:
         expected = constants.PROPAGATION_HARD_ONE_HOP
      elif is_two_hop:
         expected = constants.PROPAGATION_HARD_TWO_HOP
      else:
         expected = 0.0

      assert states[skill].c == pytest.approx(expected)

   assert max(hops.values()) >= 3

   for skill in supporting:
      is_hard_ancestor = skill in hops

      if is_hard_ancestor:
         continue

      assert states[skill].c == pytest.approx(constants.PROPAGATION_SUPPORTING_ONE_HOP)

   ancestor = sorted(skill for skill, hop in hops.items() if hop == 1)[0]

   for _ in range(500):
      apply_observation(
         states,
         graph,
         observation_for("BC-QA-03008", [target], MasteryState.MASTERED),
         TODAY,
      )

   assert states[ancestor].c > 100.0
   assert states[ancestor].distinct_archetypes_succeeded == set()
   assert states[ancestor].success_days == set()
   assert states[ancestor].mastered is False
   assert states[ancestor].consecutive_successes == 0


def test_mcq_guess_discount(states, graph, archetypes):
   archetype = archetypes[NO_FEEDBACK_ARCHETYPE]
   loaded = archetype["skills"]
   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         loaded,
         MasteryState.MASTERED,
         response_format=ResponseFormat.MCQ,
      ),
      TODAY,
   )

   for skill in loaded:
      assert states[skill].c == pytest.approx(constants.MCQ_SUCCESS_CREDIT)
      assert states[skill].c < 1.0

   assert grade_for(MasteryState.MASTERED, Confidence.CONFIDENT, 10, 100) == 4
   assert grade_for(MasteryState.MASTERED, Confidence.UNSURE, 10, 100) == 3
   assert grade_for(MasteryState.MASTERED, Confidence.CONFIDENT, 500, 100) == 3
   assert grade_for(MasteryState.NOTATION_ONLY, Confidence.CONFIDENT, 10, 100) == 2
   assert grade_for(MasteryState.NOT_MASTERED, Confidence.GUESS, 10, 100) == 1
   assert grade_for(MasteryState.NOT_ATTEMPTED, Confidence.GUESS, 10, 100) is None
   assert math.isfinite(constants.MCQ_SUCCESS_CREDIT)


def test_fsrs_forms_from_source():
   """The worked example of the FSRS-7 reference implementation, reproduced to three decimals."""
   parameters = fsrs.DEFAULT_PARAMETERS

   assert len(parameters) == 34

   stability = fsrs.initial_stability(3)
   fast_stability = fsrs.initial_fast_stability(3)
   difficulty = fsrs.initial_difficulty(3)

   assert stability == pytest.approx(3.9221, abs=5e-4)
   assert fast_stability == pytest.approx(3.1377, abs=5e-4)
   assert difficulty == pytest.approx(3.5307, abs=5e-4)
   assert fsrs.difficulty_anchor() == pytest.approx(0.2300, abs=5e-4)

   recall = fsrs.retrievability(stability, stability, fast_stability, difficulty)
   fast_recall = fsrs.fast_recall(fast_stability, stability)

   assert recall == pytest.approx(0.9066, abs=5e-4)
   assert fast_recall == pytest.approx(0.2337, abs=5e-4)

   next_stability = fsrs.next_stability_success(stability, difficulty, recall, 3)
   next_fast = fsrs.next_stability_success(
      fast_stability, difficulty, fast_recall, 3, block_base=fsrs.FAST_BLOCK_BASE
   )

   assert next_stability == pytest.approx(10.4425, abs=5e-4)
   assert next_fast == pytest.approx(170.1366, abs=5e-4)
   assert fsrs.next_difficulty(difficulty, 3, recall) == pytest.approx(3.4977, abs=5e-4)

   assert fsrs.next_difficulty(5.0, 1) > 5.0
   assert fsrs.next_difficulty(5.0, 4) < 5.0

   lapsed = fsrs.next_stability_lapse(stability, difficulty, recall)

   assert lapsed <= stability


def test_stability_bounded():
   stability = fsrs.initial_stability(3)
   difficulty = fsrs.initial_difficulty(3)

   for _ in range(20):
      recall = fsrs.retrievability(stability, stability, difficulty=difficulty)
      grown = fsrs.next_stability_success(stability, difficulty, recall, 3)
      difficulty = fsrs.next_difficulty(difficulty, 3, recall)
      stability = grown

      assert stability >= fsrs.STABILITY_MIN
      assert stability <= fsrs.STABILITY_MAX

   assert math.isfinite(stability)
   assert fsrs.retrievability(stability, 1e6, difficulty=difficulty) < 0.90


def test_hypercorrection_clears(states, graph):
   skill = "BC-SKL-01024"
   state = SkillState(skill_id=skill, beta=0.0, fading_stage=FadingStage.UNSUPPORTED)
   states[skill] = state
   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         [skill],
         MasteryState.NOT_MASTERED,
         confidence=Confidence.CONFIDENT,
      ),
      TODAY,
   )

   assert state.hypercorrection_due == TODAY + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)

   requeued = TODAY + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)
   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         [skill],
         MasteryState.MASTERED,
         confidence=Confidence.UNSURE,
      ),
      requeued,
   )

   assert state.hypercorrection_due is None

   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         [skill],
         MasteryState.NOT_MASTERED,
         confidence=Confidence.CONFIDENT,
      ),
      requeued,
   )

   assert state.hypercorrection_due == requeued + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)

   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         [skill],
         MasteryState.NOT_ATTEMPTED,
         confidence=Confidence.UNSURE,
      ),
      requeued,
   )

   assert state.hypercorrection_due == requeued + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)


def test_hypercorrection_spans_loaded_skills(states, graph, archetypes):
   loaded = archetypes[NO_FEEDBACK_ARCHETYPE]["skills"]
   blamed = loaded[0]
   notated = loaded[1]
   idle = loaded[2]
   per_skill = {skill: MasteryState.NOT_ATTEMPTED for skill in loaded}
   per_skill[blamed] = MasteryState.NOT_MASTERED
   per_skill[notated] = MasteryState.NOTATION_ONLY
   apply_observation(
      states,
      graph,
      observation_for(
         NO_FEEDBACK_ARCHETYPE,
         loaded,
         MasteryState.NOT_MASTERED,
         per_skill_states=per_skill,
         confidence=Confidence.CONFIDENT,
      ),
      TODAY,
   )

   expected_due = TODAY + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)

   assert states[blamed].hypercorrection_due == expected_due
   assert states[notated].hypercorrection_due == expected_due
   assert states[idle].hypercorrection_due is None

