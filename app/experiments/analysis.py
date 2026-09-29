"""Delayed-accuracy comparisons for the two A/B switches, docs/plan/10 "A/B readiness".

Each comparison is within the one student, so it is a difference in delayed accuracy between arms
with a Newcombe hybrid score interval (method 10 of Newcombe 1998), built from the two Wilson
intervals app/progress/calibration.py already uses. Nothing here is an effect-size claim; 10 rules
that out for a single student. The interval is stated only once each arm holds
MINIMUM_OUTCOMES_PER_ARM outcomes, which is [inferred]: no source gives a floor, and 30 is the floor
the calibration curve already uses.

Outcomes:

- feedback_elaboration. The unit is the item. An outcome is a wrong answer at stage unsupported
  (the only place the arms differ) whose next attempt on the same archetype falls on a later
  calendar day; the outcome is whether that later attempt was correct.
- retrieval_entry. The unit is the skill. An outcome is the first attempt on an item whose primary
  skill is the assigned skill, submitted DELAY_LOW_DAYS to DELAY_HIGH_DAYS after the assignment,
  the two to four week delayed checkpoint of 01. Attempts inside a practice session only.
- tutor_profile (docs/agent/architecture.md, The self-tuning loop). The unit is the skill. An
  outcome follows an attempt the live tutor assisted before submission under a recorded arm: the
  next graded attempt on the same archetype, on a later calendar day, with no practice turn before
  its own submission. Which attempts were assisted, and under which arm, comes from
  app/agent/profile.py agent_assisted_arms, because the arm is kept on the student's turn and no
  attempts row exists before submission. Calibration per confidence level, by arm, over the
  assisted attempts themselves, rides with the comparison as a guard readout: it must not worsen in
  the profile_applied arm, and it is never an objective.
"""
import math
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select

from app.agent import profile
from app.db import models
from app.experiments import switches
from app.progress.calibration import CONFIDENCE_ORDER, calibration_bin, wilson_interval

MINIMUM_OUTCOMES_PER_ARM = 30
DELAY_LOW_DAYS = 14
DELAY_HIGH_DAYS = 28
UNSUPPORTED = "unsupported"


def newcombe_interval(successes_a, trials_a, successes_b, trials_b):
   """95 percent interval on p_a - p_b."""
   p_a = successes_a / trials_a
   p_b = successes_b / trials_b
   low_a, high_a = wilson_interval(successes_a, trials_a)
   low_b, high_b = wilson_interval(successes_b, trials_b)
   difference = p_a - p_b
   lower = difference - math.sqrt((p_a - low_a) ** 2 + (high_b - p_b) ** 2)
   upper = difference + math.sqrt((high_a - p_a) ** 2 + (p_b - low_b) ** 2)

   return lower, upper


@dataclass(frozen=True)
class ArmOutcomes:
   arm: str
   outcomes: int
   correct: int

   @property
   def accuracy(self):
      return self.correct / self.outcomes if self.outcomes else None


@dataclass(frozen=True)
class Comparison:
   name: str
   control: ArmOutcomes
   treatment: ArmOutcomes
   difference: float | None
   interval_low: float | None
   interval_high: float | None
   guards: dict | None = None

   @property
   def stated(self):
      return self.interval_low is not None


def compare(name, outcomes_by_arm, guards=None):
   definition = switches.DEFINITIONS[name]
   control_values = outcomes_by_arm.get(definition.control_arm, [])
   treatment_values = outcomes_by_arm.get(definition.treatment_arm, [])
   control = ArmOutcomes(definition.control_arm, len(control_values), sum(control_values))
   treatment = ArmOutcomes(definition.treatment_arm, len(treatment_values), sum(treatment_values))
   has_both = control.outcomes > 0 and treatment.outcomes > 0
   difference = treatment.accuracy - control.accuracy if has_both else None
   has_enough = min(control.outcomes, treatment.outcomes) >= MINIMUM_OUTCOMES_PER_ARM
   low = high = None

   if has_enough:
      low, high = newcombe_interval(treatment.correct, treatment.outcomes, control.correct, control.outcomes)

   return Comparison(name, control, treatment, difference, low, high, guards)


def feedback_outcomes(attempts):
   practice = [record for record in attempts if record.updates_mastery]
   outcomes = {}

   for index, record in enumerate(practice):
      arm = record.experiment_arms.get(switches.FEEDBACK_ELABORATION)
      was_manipulated = arm is not None and record.correct is False and record.served_stage == UNSUPPORTED

      if not was_manipulated:
         continue

      for later in practice[index + 1:]:
         is_same_archetype = later.archetype_id == record.archetype_id
         is_later_day = later.day > record.day
         is_graded = later.correct is not None

         if is_same_archetype and is_later_day and is_graded:
            outcomes.setdefault(arm, []).append(1 if later.correct else 0)
            break

   return outcomes


def assignments(db, user_id, name):
   return db.execute(
      select(models.ExperimentAssignment)
      .where(models.ExperimentAssignment.user_id == user_id)
      .where(models.ExperimentAssignment.experiment == name)
      .order_by(models.ExperimentAssignment.unit_id)
   ).scalars().all()


def retrieval_outcomes(assigned, attempts):
   practice = [record for record in attempts if record.updates_mastery and record.correct is not None]
   outcomes = {}

   for assignment in assigned:
      assigned_on = date.fromisoformat(assignment.assigned_at[:10])

      for record in practice:
         is_skill = record.primary_skill == assignment.unit_id
         delay = (record.day - assigned_on).days
         is_in_window = DELAY_LOW_DAYS <= delay <= DELAY_HIGH_DAYS

         if is_skill and is_in_window:
            outcomes.setdefault(assignment.arm, []).append(1 if record.correct else 0)
            break

   return outcomes


def tutor_profile_outcomes(attempts, assisted_arms):
   """assisted_arms maps each agent-assisted attempt id to its tutor_profile arm, or None when the
   switch was off for it; an attempt in the mapping never counts as unaided."""
   practice = [record for record in attempts if record.updates_mastery]
   outcomes = {}

   for index, record in enumerate(practice):
      arm = assisted_arms.get(record.id)

      if arm is None:
         continue

      for later in practice[index + 1:]:
         is_same_archetype = later.archetype_id == record.archetype_id
         is_later_day = later.day > record.day
         is_graded = later.correct is not None
         is_unaided = later.id not in assisted_arms
         is_outcome = is_same_archetype and is_later_day and is_graded and is_unaided

         if is_outcome:
            outcomes.setdefault(arm, []).append(1 if later.correct else 0)
            break

   return outcomes


def bin_view(entry):
   return {
      "confidence": entry.confidence.value,
      "attempts": entry.attempts,
      "correct": entry.correct,
      "accuracy": entry.accuracy,
      "interval_low": entry.interval_low,
      "interval_high": entry.interval_high,
   }


def calibration_by_arm(attempts, assisted_arms):
   """Accuracy per confidence level, by arm, over the rated and graded attempts each arm assisted."""
   definition = switches.DEFINITIONS[switches.TUTOR_PROFILE]
   outcomes = {arm: {level: [] for level in CONFIDENCE_ORDER} for arm in definition.arms}

   for record in attempts:
      arm = assisted_arms.get(record.id)
      is_in_an_arm = arm in outcomes
      is_rated = record.confidence in {level.value for level in CONFIDENCE_ORDER}
      is_graded = record.correct is not None
      is_counted = is_in_an_arm and is_rated and is_graded and record.updates_mastery

      if is_counted:
         level = next(level for level in CONFIDENCE_ORDER if level.value == record.confidence)
         outcomes[arm][level].append(bool(record.correct))

   return {
      arm: [bin_view(calibration_bin(level, by_level[level])) for level in CONFIDENCE_ORDER]
      for arm, by_level in outcomes.items()
   }


def tutor_profile_comparison(db, user_id, attempts):
   assisted_arms = profile.agent_assisted_arms(db, user_id)

   return compare(
      switches.TUTOR_PROFILE,
      tutor_profile_outcomes(attempts, assisted_arms),
      guards={"calibration": calibration_by_arm(attempts, assisted_arms)},
   )


def comparisons(db, user_id, attempts):
   return [
      compare(switches.FEEDBACK_ELABORATION, feedback_outcomes(attempts)),
      compare(
         switches.RETRIEVAL_ENTRY,
         retrieval_outcomes(assignments(db, user_id, switches.RETRIEVAL_ENTRY), attempts),
      ),
      tutor_profile_comparison(db, user_id, attempts),
   ]


def comparison_view(comparison):
   def arm_view(arm):
      return {"arm": arm.arm, "outcomes": arm.outcomes, "correct": arm.correct, "accuracy": arm.accuracy}

   view = {
      "name": comparison.name,
      "control": arm_view(comparison.control),
      "treatment": arm_view(comparison.treatment),
      "difference": comparison.difference,
      "interval_low": comparison.interval_low,
      "interval_high": comparison.interval_high,
      "stated": comparison.stated,
      "minimum_outcomes_per_arm": MINIMUM_OUTCOMES_PER_ARM,
   }
   has_guards = comparison.guards is not None

   if has_guards:
      view["guards"] = comparison.guards

   return view
