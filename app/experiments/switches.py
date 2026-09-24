"""The A/B switches of docs/plan/10 "A/B readiness", per-item or per-skill randomisation within
the one student.

Only the two experiments 10 marks powered for a single student are defined. Each has a state:
off serves the shipped arm to every unit, on serves the treatment arm to every unit, randomised
assigns each new unit an arm and serves it. Turning a switch to randomised assigns only units first
seen after that instant, and a unit's arm is written once and never changed, so a skill put in the
3-success arm stays there for the life of the experiment.

Assignment is stratified, as 10 asks, so chance imbalance cannot dominate a small sample. A unit's
stratum is its primary skill plus, for item units, a band of the engine's predicted success
probability. The unit goes to whichever arm has fewer units in its stratum so far, and a tie is
broken by a draw seeded from the experiment's seed and the unit id, so the same history always
gives the same assignment.

No experiment changes the mastery rule, a gate, a threshold or a tolerance. RETRIEVAL_ENTRY moves
only a skill's entry to the block 3 mixed-review pool; the six-condition mastery rule keeps its 3
credited unaided successes in both arms (R8, fix 12).
"""
import hashlib
import json
import random
from dataclasses import dataclass

from sqlalchemy import select

from app.db import models

OFF = "off"
ON = "on"
RANDOMISED = "randomised"
STATES = (OFF, ON, RANDOMISED)

FEEDBACK_ELABORATION = "feedback_elaboration"
RETRIEVAL_ENTRY = "retrieval_entry"

PROBABILITY_BAND_EDGE = 0.5


@dataclass(frozen=True)
class Definition:
   name: str
   unit: str
   control_arm: str
   treatment_arm: str
   description: str

   @property
   def arms(self):
      return (self.control_arm, self.treatment_arm)


DEFINITIONS = {
   FEEDBACK_ELABORATION: Definition(
      name=FEEDBACK_ELABORATION,
      unit="item",
      control_arm="elaborated",
      treatment_arm="verification_only",
      description="Elaborated feedback against verification-only feedback on a wrong answer at stage unsupported.",
   ),
   RETRIEVAL_ENTRY: Definition(
      name=RETRIEVAL_ENTRY,
      unit="skill",
      control_arm="entry_1",
      treatment_arm="entry_3",
      description="A skill joins the mixed-review pool after 1 against 3 unaided successes at stage unsupported.",
   ),
}

ENTRY_THRESHOLDS = {"entry_1": 1, "entry_3": 3}


def default_seed(user_id, name):
   digest = hashlib.sha256(f"{user_id}:{name}".encode()).hexdigest()

   return int(digest[:8], 16)


def resolve_default(default_state, name):
   """default_state is one state for every experiment or a mapping from experiment name to state;
   an experiment the mapping does not name starts off."""
   if isinstance(default_state, dict):
      return default_state.get(name, OFF)

   return default_state


def experiment_row(db, user_id, name, default_state, now):
   """The student's row for one experiment, created at its default state the first time it is
   read. A row created randomised starts randomising from that instant."""
   row = db.get(models.Experiment, (user_id, name))

   if row is not None:
      return row

   default_state = resolve_default(default_state, name)

   stamp = now.isoformat()
   is_randomised = default_state == RANDOMISED
   row = models.Experiment(
      user_id=user_id,
      name=name,
      state=default_state,
      seed=default_seed(user_id, name),
      randomised_from=stamp if is_randomised else None,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()

   return row


def set_state(db, user_id, name, state, default_state, now):
   is_known_state = state in STATES
   is_known_experiment = name in DEFINITIONS

   if not is_known_experiment:
      raise ValueError(f"no experiment named {name}")

   if not is_known_state:
      raise ValueError(f"an experiment state is one of {', '.join(STATES)}")

   row = experiment_row(db, user_id, name, default_state, now)
   starts_randomising = state == RANDOMISED and row.state != RANDOMISED

   if starts_randomising:
      row.randomised_from = now.isoformat()

   row.state = state
   row.updated_at = now.isoformat()
   db.flush()

   return row


def probability_band(p_predicted):
   if p_predicted is None:
      return "unknown"

   return "high" if p_predicted >= PROBABILITY_BAND_EDGE else "low"


def stratum_for(definition, primary_skill, p_predicted):
   is_item_unit = definition.unit == "item"

   if is_item_unit:
      return f"{primary_skill}|{probability_band(p_predicted)}"

   return primary_skill


def existing_assignment(db, user_id, name, unit_id):
   return db.get(models.ExperimentAssignment, (user_id, name, unit_id))


def stratum_counts(db, user_id, name, stratum):
   rows = db.execute(
      select(models.ExperimentAssignment.arm)
      .where(models.ExperimentAssignment.user_id == user_id)
      .where(models.ExperimentAssignment.experiment == name)
      .where(models.ExperimentAssignment.stratum == stratum)
   ).scalars()
   counts = {}

   for arm in rows:
      counts[arm] = counts.get(arm, 0) + 1

   return counts


def balanced_arm(definition, counts, seed, unit_id):
   control, treatment = definition.arms
   control_count = counts.get(control, 0)
   treatment_count = counts.get(treatment, 0)

   if control_count < treatment_count:
      return control

   if treatment_count < control_count:
      return treatment

   tie_break = random.Random(f"{seed}:{definition.name}:{unit_id}")

   return control if tie_break.random() < 0.5 else treatment


def arm_for(db, user_id, name, unit_id, primary_skill, p_predicted, default_state, now):
   """The arm a unit is served under. Off and on never write an assignment; randomised writes one
   the first time a unit is seen and returns it every time after."""
   definition = DEFINITIONS[name]
   row = experiment_row(db, user_id, name, default_state, now)

   if row.state == OFF:
      return definition.control_arm

   if row.state == ON:
      return definition.treatment_arm

   assigned = existing_assignment(db, user_id, name, unit_id)

   if assigned is not None:
      return assigned.arm

   stratum = stratum_for(definition, primary_skill, p_predicted)
   arm = balanced_arm(definition, stratum_counts(db, user_id, name, stratum), row.seed, unit_id)
   stamp = now.isoformat()
   db.add(
      models.ExperimentAssignment(
         user_id=user_id,
         experiment=name,
         unit_id=unit_id,
         arm=arm,
         stratum=stratum,
         assigned_at=stamp,
         created_at=stamp,
         updated_at=stamp,
      )
   )
   db.flush()

   return arm


def recorded_arms(attempt):
   return json.loads(attempt.experiment_arms) if attempt.experiment_arms else {}


def record_arm(attempt, name, arm):
   arms = recorded_arms(attempt)
   arms[name] = arm
   attempt.experiment_arms = json.dumps(arms, sort_keys=True)


def retrieval_entry_thresholds(db, user_id, skill_ids, default_state, now):
   """Maps each skill to its RETRIEVAL_ENTRY under the experiment, for session assembly."""
   return {
      skill_id: ENTRY_THRESHOLDS[
         arm_for(db, user_id, RETRIEVAL_ENTRY, skill_id, skill_id, None, default_state, now)
      ]
      for skill_id in sorted(skill_ids)
   }


def switch_view(db, user_id, default_state, now):
   views = []

   for name in sorted(DEFINITIONS):
      definition = DEFINITIONS[name]
      row = experiment_row(db, user_id, name, default_state, now)
      assigned = db.execute(
         select(models.ExperimentAssignment.arm)
         .where(models.ExperimentAssignment.user_id == user_id)
         .where(models.ExperimentAssignment.experiment == name)
      ).scalars().all()
      views.append({
         "name": name,
         "description": definition.description,
         "unit": definition.unit,
         "arms": list(definition.arms),
         "state": row.state,
         "randomised_from": row.randomised_from,
         "assigned_units": {arm: assigned.count(arm) for arm in definition.arms},
      })

   return views
