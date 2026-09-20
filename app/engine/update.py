"""The update rules from docs/plan/02-adaptive-engine.md, Update rules and Decay.

Credit assignment is R2, propagation weights and the prerequisite-gap charge are the table under
Prerequisite propagation, mastery is the six-condition declaration under Mastery declaration and
un-mastery, and the fading ladder is the single counter pair of R7. The no-diagnostician
mastery_state rule is R12 and R26, specified in docs/plan/03-diagnosis-and-feedback.md.
"""
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from app.engine import constants, fsrs
from app.engine.state import (
   Confidence,
   FadingStage,
   FADING_ORDER,
   MasteryState,
   PARTIAL_STATES,
   ResponseFormat,
)
from app.engine.strength import probability

CREDIT_TABLE = {
   MasteryState.MASTERED: (1.0, 0.0),
   MasteryState.PARTIAL_PROCEDURAL: (0.0, 0.5),
   MasteryState.PARTIAL_CONCEPTUAL: (0.0, 0.5),
   MasteryState.PARTIAL_UNSPECIFIED: (0.0, 0.5),
   MasteryState.NOTATION_ONLY: (0.25, 0.0),
   MasteryState.PREREQUISITE_GAP: (0.0, 0.0),
   MasteryState.NOT_MASTERED: (0.0, 1.0),
   MasteryState.NOT_ATTEMPTED: (0.0, 0.0),
}

GRADE_EASY = 4
GRADE_GOOD = 3
GRADE_HARD = 2
GRADE_AGAIN = 1


@dataclass(frozen=True)
class EngineGraph:
   hard_parents: dict
   supporting_parents: dict
   hard_children: dict


@dataclass
class Observation:
   archetype_id: str
   skills: list
   per_skill_states: dict
   response_format: ResponseFormat = ResponseFormat.SHORT_ANSWER
   confidence: Confidence = Confidence.UNSURE
   elapsed_ms: int | None = None
   served_stage: FadingStage = FadingStage.EXAMPLE
   named_prerequisite: str | None = None
   archetype_median_ms: int | None = None
   error_path_skills: list = field(default_factory=list)


def as_datetime(moment):
   is_already_datetime = isinstance(moment, datetime)

   if is_already_datetime:
      return moment

   return datetime(moment.year, moment.month, moment.day)


def as_date(moment):
   is_datetime = isinstance(moment, datetime)

   if is_datetime:
      return moment.date()

   return moment


def elapsed_days(last_practised_at, today):
   has_no_history = last_practised_at is None

   if has_no_history:
      return 0.0

   return max((as_date(today) - as_date(last_practised_at)).days, 0)


def hard_ancestor_hops(skill_id, hard_parents, max_hops=None):
   """Every hard_prerequisite ancestor with its shortest hop count."""
   found = {}
   frontier = deque([(skill_id, 0)])

   while frontier:
      current, hops = frontier.popleft()
      next_hops = hops + 1
      past_limit = max_hops is not None and next_hops > max_hops

      if past_limit:
         continue

      for parent in hard_parents.get(current, ()):
         is_new = parent not in found

         if is_new:
            found[parent] = next_hops
            frontier.append((parent, next_hops))

   return found


def is_credited_failure_state(mastery_state):
   state = MasteryState(mastery_state)
   _, f_credit = CREDIT_TABLE[state]
   is_gap = state == MasteryState.PREREQUISITE_GAP

   return f_credit > 0.0 or is_gap


def credit_for(mastery_state, response_format):
   c_credit, f_credit = CREDIT_TABLE[MasteryState(mastery_state)]
   is_mcq = ResponseFormat(response_format) == ResponseFormat.MCQ

   if is_mcq:
      c_credit *= constants.MCQ_SUCCESS_CREDIT

   return (c_credit, f_credit)


def grade_for(mastery_state, confidence, elapsed_ms, archetype_median_ms):
   state = MasteryState(mastery_state)
   has_no_grade = state in (MasteryState.NOT_ATTEMPTED, MasteryState.PREREQUISITE_GAP)

   if has_no_grade:
      return None

   is_success = state == MasteryState.MASTERED

   if is_success:
      is_confident = Confidence(confidence) == Confidence.CONFIDENT
      has_times = elapsed_ms is not None and archetype_median_ms is not None
      is_fast = has_times and elapsed_ms < archetype_median_ms
      is_easy = is_confident and is_fast

      if is_easy:
         return GRADE_EASY

      return GRADE_GOOD

   is_hard = state in PARTIAL_STATES or state == MasteryState.NOTATION_ONLY

   if is_hard:
      return GRADE_HARD

   return GRADE_AGAIN


def update_memory(state, grade, today, weight=1.0):
   """Apply the FSRS forms at full weight, or interpolated by a propagation weight."""
   has_no_grade = grade is None

   if has_no_grade:
      return

   is_first_credited = state.stability is None

   if is_first_credited:
      state.stability = fsrs.initial_stability(grade)
      state.difficulty = fsrs.initial_difficulty(grade)

      return

   elapsed = elapsed_days(state.last_practised_at, today)
   recall_probability = fsrs.retrievability(
      state.stability, elapsed, difficulty=state.difficulty
   )
   is_lapse = grade <= GRADE_AGAIN

   if is_lapse:
      candidate_stability = fsrs.next_stability_lapse(
         state.stability, state.difficulty, recall_probability
      )
   else:
      candidate_stability = fsrs.next_stability_success(
         state.stability, state.difficulty, recall_probability, grade
      )

   candidate_difficulty = fsrs.next_difficulty(state.difficulty, grade, recall_probability)
   state.stability += weight * (candidate_stability - state.stability)
   state.difficulty += weight * (candidate_difficulty - state.difficulty)


def evaluate_mastery(state, today):
   """The six conditions of docs/plan/02, Q6 in docs/plan/11."""
   retention = fsrs.retrievability(
      state.stability,
      elapsed_days(state.last_practised_at, today),
      difficulty=state.difficulty,
   )
   days = sorted(state.success_days)
   has_days = len(days) > 0
   span_days = (days[-1] - days[0]).days if has_days else 0

   meets_strength = probability(state) >= constants.MASTERY_THRESHOLD
   meets_successes = state.unaided_success_count >= constants.MASTERY_MIN_UNAIDED_SUCCESSES
   meets_archetypes = (
      len(state.distinct_archetypes_succeeded) >= constants.MASTERY_MIN_DISTINCT_ARCHETYPES
   )
   meets_days = len(days) >= constants.MASTERY_MIN_DISTINCT_DAYS
   meets_span = span_days >= constants.MASTERY_MIN_DAY_SPAN
   meets_retention = retention >= constants.desired_retention(today)

   return (
      meets_strength
      and meets_successes
      and meets_archetypes
      and meets_days
      and meets_span
      and meets_retention
   )


def evaluate_unmastery(state, failed_at_unsupported):
   is_weak = probability(state) < constants.UNMASTERY_THRESHOLD

   return is_weak or failed_at_unsupported


def advance_fading(state):
   position = FADING_ORDER.index(state.fading_stage)
   is_top = position >= len(FADING_ORDER) - 1

   if is_top:
      return

   state.fading_stage = FADING_ORDER[position + 1]


def drop_fading(state):
   position = FADING_ORDER.index(state.fading_stage)
   is_bottom = position <= 0

   if is_bottom:
      return

   state.fading_stage = FADING_ORDER[position - 1]


def move_counters(state, is_credited_success, is_credited_failure):
   if is_credited_success:
      state.consecutive_successes += 1
      state.consecutive_failures = 0
      reached_advance = state.consecutive_successes >= constants.FADING_ADVANCE_AFTER

      if reached_advance:
         advance_fading(state)
         state.consecutive_successes = 0

   if is_credited_failure:
      state.consecutive_failures += 1
      state.consecutive_successes = 0
      reached_drop = state.consecutive_failures >= constants.FADING_DROP_AFTER

      if reached_drop:
         drop_fading(state)
         state.consecutive_failures = 0


def apply_propagated(state, weight, c_credit, f_credit, grade, today):
   """Fractional implicit repetition: counts and memory move, corroboration never does."""
   state.c += weight * c_credit
   state.f += weight * f_credit
   update_memory(state, grade, today, weight)
   state.last_practised_at = as_datetime(today)


def propagate_success(states, graph, skill_id, c_credit, grade, today, excluded):
   ancestors = hard_ancestor_hops(skill_id, graph.hard_parents, max_hops=2)

   for ancestor, hops in ancestors.items():
      is_one_hop = hops == 1
      weight = (
         constants.PROPAGATION_HARD_ONE_HOP if is_one_hop else constants.PROPAGATION_HARD_TWO_HOP
      )
      target = states.get(ancestor)
      is_skipped = target is None or ancestor in excluded

      if is_skipped:
         continue

      apply_propagated(target, weight, c_credit, 0.0, grade, today)

   for parent in graph.supporting_parents.get(skill_id, ()):
      target = states.get(parent)
      is_skipped = target is None or parent in excluded or parent in ancestors

      if is_skipped:
         continue

      apply_propagated(
         target, constants.PROPAGATION_SUPPORTING_ONE_HOP, c_credit, 0.0, grade, today
      )


def charge_prerequisite_gap(states, graph, prerequisite, today, excluded):
   """1.0 failure to the named prerequisite, 0.3 to its hard dependants, nothing to the target.

   A prerequisite the same observation marked mastered is not a gap, so the excluded guard covers
   it and the forward charge that hangs off it.
   """
   charged = []
   named = states.get(prerequisite)
   was_demonstrated_here = prerequisite in excluded

   if was_demonstrated_here:
      return charged

   has_named = named is not None

   if has_named:
      apply_propagated(named, 1.0, 0.0, constants.PREREQUISITE_GAP_FAILURE, GRADE_AGAIN, today)
      charged.append(prerequisite)

   for dependant in graph.hard_children.get(prerequisite, ()):
      target = states.get(dependant)
      is_skipped = target is None or dependant in excluded

      if is_skipped:
         continue

      apply_propagated(
         target,
         1.0,
         0.0,
         constants.PREREQUISITE_GAP_FORWARD_FAILURE,
         GRADE_AGAIN,
         today,
      )
      charged.append(dependant)

   return charged


def apply_observation(states, graph, observation, today):
   """Update every skill the item loaded, then propagate, then re-evaluate mastery."""
   observed = set(observation.skills)
   failed = set()
   touched = set()
   day = as_date(today)
   was_confident = Confidence(observation.confidence) == Confidence.CONFIDENT
   item_failed = any(
      is_credited_failure_state(observation.per_skill_states[skill_id])
      for skill_id in observation.skills
   )
   triggers_hypercorrection = was_confident and item_failed

   for skill_id in observation.skills:
      state = states.get(skill_id)
      is_absent = state is None

      if is_absent:
         continue

      mastery_state = MasteryState(observation.per_skill_states[skill_id])
      state.observation_count += 1
      is_not_attempted = mastery_state == MasteryState.NOT_ATTEMPTED

      if is_not_attempted:
         continue

      state.hypercorrection_due = None

      touched.add(skill_id)
      c_credit, f_credit = credit_for(mastery_state, observation.response_format)
      grade = grade_for(
         mastery_state,
         observation.confidence,
         observation.elapsed_ms,
         observation.archetype_median_ms,
      )
      is_gap = mastery_state == MasteryState.PREREQUISITE_GAP
      is_credited_success = c_credit > 0.0
      is_credited_failure = f_credit > 0.0 or is_gap

      state.c += c_credit
      state.f += f_credit
      update_memory(state, grade, today)
      state.last_practised_at = as_datetime(today)
      move_counters(state, is_credited_success, is_credited_failure)

      is_unaided = FadingStage(observation.served_stage) == FadingStage.UNSUPPORTED
      is_full_success = mastery_state == MasteryState.MASTERED
      records_corroboration = is_full_success and is_unaided

      if records_corroboration:
         state.distinct_archetypes_succeeded.add(observation.archetype_id)
         state.success_days.add(day)
         state.unaided_success_count += 1

      is_below_mastered = mastery_state != MasteryState.MASTERED
      sets_hypercorrection = triggers_hypercorrection and is_below_mastered

      if sets_hypercorrection:
         state.hypercorrection_due = day + timedelta(days=constants.HYPERCORRECTION_GAP_DAYS)

      if is_credited_failure:
         failed.add(skill_id)

      if is_credited_success:
         propagate_success(states, graph, skill_id, c_credit, grade, today, observed)

      if is_gap:
         has_named = observation.named_prerequisite is not None

         if has_named:
            charged = charge_prerequisite_gap(
               states, graph, observation.named_prerequisite, today, observed
            )
            failed.update(charged)
            touched.update(charged)

   for skill_id in touched:
      state = states[skill_id]
      is_failure = skill_id in failed
      failed_unaided = (
         is_failure
         and skill_id in observed
         and FadingStage(observation.served_stage) == FadingStage.UNSUPPORTED
      )

      if is_failure:
         lost_mastery = evaluate_unmastery(state, failed_unaided)

         if lost_mastery:
            state.mastered = False
            state.mastered_at = None

         continue

      is_mastered = evaluate_mastery(state, today)

      if is_mastered:
         state.mastered = True
         state.mastered_at = as_datetime(today)

   return states


def rule_based_mastery_states(archetype, answer):
   """R12 and R26: the P1 mastery_state per loaded skill with no diagnostician wired."""
   loaded = list(archetype["skills"])
   primary = loaded[0]
   is_misnotated = bool(answer.get("equivalent_but_misnotated"))

   if is_misnotated:
      return {skill: MasteryState.NOTATION_ONLY for skill in loaded}

   is_correct = bool(answer.get("correct"))

   if is_correct:
      return {skill: MasteryState.MASTERED for skill in loaded}

   error_path_skills = [skill for skill in (answer.get("error_path_skills") or []) if skill in loaded]
   has_error_path = len(error_path_skills) > 0
   blamed = set(error_path_skills) if has_error_path else {primary}

   return {
      skill: MasteryState.NOT_MASTERED if skill in blamed else MasteryState.NOT_ATTEMPTED
      for skill in loaded
   }
