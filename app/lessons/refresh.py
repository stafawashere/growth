"""Refreshers, docs/plan/15-lessons.md Re-teaching: triggers T1 to T4 read from state the engine
already writes, and the entries session assembly places before the matching item.

refresher_targets is pure. T5, method confusion, belongs to Slice L6 and is the named hook
method_confusion_targets, which returns nothing until the decision lessons land.
"""
from dataclasses import dataclass
from datetime import date, datetime

from app.engine import constants as engine_constants
from app.engine.select import retrievability_map
from app.engine.state import FadingStage
from app.lessons import constants
from app.lessons.gate import concept_of
from app.lessons.plan import plan_lesson

T1 = "T1"
T2 = "T2"
T3 = "T3"
T4 = "T4"
T5 = "T5"
REFRESHER = "refresher"
READ_AGAIN = "read_again"
REFRESHER_BAND = "low"

# 15 Re-teaching table, "Where the refresher goes"; the priority puts the failure triggers first
# and T2, which predicts a failure, last.
BLOCKS_FOR = {
   T1: ("block1", "block2"),
   T3: ("block1", "block2"),
   T4: ("block2",),
   T2: ("block1", "block2"),
}
PRIORITY = (T1, T3, T4, T2)


@dataclass(frozen=True)
class RefresherTarget:
   concept_id: str
   lesson_id: str
   version: int
   reason: str
   skills: tuple
   error_ids: tuple = ()
   prerequisite_ids: tuple = ()
   plan_state: dict | None = None

   @property
   def blocks(self):
      return BLOCKS_FOR[self.reason]


def as_day(stamp):
   if stamp is None:
      return None

   if isinstance(stamp, date) and not isinstance(stamp, datetime):
      return stamp

   if isinstance(stamp, datetime):
      return stamp.date()

   return datetime.fromisoformat(stamp).date()


def days_since(stamp, today):
   day = as_day(stamp)

   if day is None:
      return None

   return (today - day).days


def state_field(state, name):
   if state is None:
      return None

   return state.get(name)


def within_gap(state, today):
   """15 Re-teaching: a concept receives at most one refresher per REFRESHER_MIN_GAP_DAYS (L11)."""
   waited = days_since(state_field(state, "refresher_served_at"), today)

   return waited is not None and waited < constants.REFRESHER_MIN_GAP_DAYS


def lost_mastery(state):
   """T1 reads an un-mastery evaluate_unmastery wrote: the skill had reached the unaided-success
   count mastery needs, is unmastered now and has failed since. evaluate_unmastery clears
   mastered_at, so the success count is the trace the flip leaves."""
   has_had_mastery_count = state.unaided_success_count >= engine_constants.MASTERY_MIN_UNAIDED_SUCCESSES
   has_failed = state.consecutive_failures >= 1

   return has_had_mastery_count and not state.mastered and has_failed


def failed_since(skill_id, attempts_history, graph, since_day):
   for attempt in attempts_history:
      record = graph.archetypes.get(attempt.get("archetype_id"))
      loads_skill = record is not None and skill_id in record["skills"]
      is_failure = bool(attempt.get("corrected"))
      attempted_on = attempt.get("attempted_on")
      is_after = since_day is None or (attempted_on is not None and attempted_on >= since_day)

      if loads_skill and is_failure and is_after:
         return True

   return False


def failed_run_at_example(skill_id, attempts_history, graph):
   """The last FADING_DROP_AFTER attempts loading the skill, all corrected at stage example."""
   loading = [
      attempt
      for attempt in attempts_history
      if skill_id in (graph.archetypes.get(attempt.get("archetype_id")) or {}).get("skills", ())
   ]
   run = loading[-engine_constants.FADING_DROP_AFTER:]
   is_long_enough = len(run) >= engine_constants.FADING_DROP_AFTER

   return is_long_enough and all(attempt.get("corrected") and attempt.get("stage") == FadingStage.EXAMPLE for attempt in run)


def is_stuck_at_example(state, skill_id, attempts_history, graph):
   """T4: fading_stage example and FADING_DROP_AFTER failures in a row. move_counters resets
   consecutive_failures when the drop is reached, even where drop_fading clamps at example, so the
   run is also read from the attempts themselves."""
   at_example = state.fading_stage == FadingStage.EXAMPLE
   counted = state.consecutive_failures >= engine_constants.FADING_DROP_AFTER
   traced = failed_run_at_example(skill_id, attempts_history, graph)

   return at_example and (counted or traced)


def is_decayed(state, retrievability):
   """T2: a mastered skill below DECAYED_SUPPORT_CAP_RETRIEVABILITY (02 Decay, Q9 closed)."""
   below_cap = retrievability.get(state.skill_id, 1.0) < engine_constants.DECAYED_SUPPORT_CAP_RETRIEVABILITY

   return state.mastered and below_cap


def plan_state_of(state, today):
   """The two facts plan_lesson reads for a repeated T4 (app/lessons/plan.py is_repeat_t4)."""
   if state is None:
      return None

   return {
      "refresher_reason": state_field(state, "refresher_due_reason"),
      "days_since_refresher": days_since(state_field(state, "refresher_served_at"), today),
   }


def skill_triggers(states, attempts_history, graph, lesson_states, servable, today, retrievability):
   """(concept_id, reason, skill_id) for every skill a trigger names."""
   found = []

   for skill_id in sorted(states):
      state = states[skill_id]
      concept_id = concept_of(graph, skill_id)
      lesson = servable.get(concept_id) if concept_id is not None else None

      if lesson is None:
         continue

      lesson_state = lesson_states.get(lesson[0])
      since_day = as_day(state_field(lesson_state, "refresher_served_at"))

      if lost_mastery(state) and failed_since(skill_id, attempts_history, graph, since_day):
         found.append((concept_id, T1, skill_id))

      if is_stuck_at_example(state, skill_id, attempts_history, graph):
         found.append((concept_id, T4, skill_id))

      if is_decayed(state, retrievability):
         found.append((concept_id, T2, skill_id))

   return found


def gap_triggers(prerequisite_gaps, graph, servable):
   """T3: a diagnosed prerequisite_gap naming a BC-SKL; the refresher is that skill's concept
   lesson, placed before the next item loading a dependent skill. A BC-PRQ gap is served as its
   LSN-PRQ first-contact lesson by assembly instead (15 Re-teaching, T3 row)."""
   found = []

   for gap_id, dependent_skills in prerequisite_gaps:
      concept_id = concept_of(graph, gap_id)
      has_lesson = concept_id is not None and concept_id in servable

      if not has_lesson:
         continue

      for skill_id in dependent_skills:
         found.append((concept_id, T3, skill_id, gap_id))

   return found


def method_confusion_targets(states, attempts_history, lesson_states, today):
   """T5, method confusion on a confusable set, is Slice L6 (15 Methods); this is its hook."""
   return ()


def refresher_targets(
   states,
   attempts_history,
   lesson_states,
   today,
   graph=None,
   servable=None,
   prerequisite_gaps=(),
   retrievability=None,
):
   """One target per concept, for the trigger of highest priority, leaving out a concept inside
   its REFRESHER_MIN_GAP_DAYS window. graph and servable are needed to name a concept's lesson."""
   servable = servable or {}
   retrievability = retrievability_map(states, today, retrievability)
   by_concept = {}

   for concept_id, reason, skill_id in skill_triggers(states, attempts_history, graph, lesson_states, servable, today, retrievability):
      by_concept.setdefault(concept_id, {}).setdefault(reason, {"skills": [], "prerequisites": []})["skills"].append(skill_id)

   for concept_id, reason, skill_id, gap_id in gap_triggers(prerequisite_gaps, graph, servable):
      entry = by_concept.setdefault(concept_id, {}).setdefault(reason, {"skills": [], "prerequisites": []})
      entry["skills"].append(skill_id)
      entry["prerequisites"].append(gap_id)

   targets = []

   for concept_id in sorted(by_concept):
      lesson_id, version = servable[concept_id]
      lesson_state = lesson_states.get(lesson_id)

      if within_gap(lesson_state, today):
         continue

      reason = next(reason for reason in PRIORITY if reason in by_concept[concept_id])
      named = by_concept[concept_id][reason]
      targets.append(
         RefresherTarget(
            concept_id=concept_id,
            lesson_id=lesson_id,
            version=version,
            reason=reason,
            skills=tuple(sorted(set(named["skills"]))),
            prerequisite_ids=tuple(sorted(set(named["prerequisites"]))),
            plan_state=plan_state_of(lesson_state, today),
         )
      )

   return targets


def matching_target(targets, item, graph, block_name, taken):
   """The first open target whose skills the item loads, in a block its trigger allows."""
   record = graph.archetypes.get(item["archetype_id"])

   if record is None:
      return None

   loaded = set(record["skills"])

   for target in targets:
      is_taken = target.lesson_id in taken
      is_matching = len(loaded & set(target.skills)) > 0
      is_allowed = block_name in target.blocks

      if is_matching and is_allowed and not is_taken:
         return target

   return None


def refresher_entry(target, body, item):
   plan = plan_lesson(
      body,
      REFRESHER_BAND,
      target.reason,
      error_ids=target.error_ids,
      prerequisite_ids=target.prerequisite_ids,
      lesson_state=target.plan_state,
   )

   return {
      "kind": REFRESHER,
      "lesson_id": target.lesson_id,
      "version": target.version,
      "band": REFRESHER_BAND,
      "reason": target.reason,
      "concept_id": target.concept_id,
      "before_item_id": item["id"],
      "minutes": plan.minutes,
      "plan": plan.as_dict(),
   }


def read_again_entry(target):
   return {"kind": READ_AGAIN, "lesson_id": target.lesson_id, "version": target.version}


def serve_refresher(block, entry, served_count, reading_fits):
   """Append the refresher when the session is under REFRESHERS_PER_SESSION_MAX and the reading
   share cap holds with its minutes; the gap rule was applied when the target was named."""
   under_count = served_count < constants.REFRESHERS_PER_SESSION_MAX
   fits_share = reading_fits(entry["minutes"])
   is_served = under_count and fits_share

   if is_served:
      block.append(entry)

   return is_served
