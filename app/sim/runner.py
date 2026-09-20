"""Offline simulation of the P1 engine against the synthetic students in tests/fixtures.

docs/plan/10-quality-and-evaluation.md, "Offline simulation of the engine against synthetic
students", fixes the world: a hidden true state per skill, slip and guess as the observation noise
with guess floored at 0.25 on MCQ, and a forgetting curve that is deliberately not FSRS, so that
the engine's own decay model is never also the world model. The curve here is the exponential one
with a per-skill half-life that grows on successful retrieval; the power-law second arm is out of
P1 scope and is not implemented.

Two arms run over the same fixtures and the same seeds. The policy arm is the shipped two-term
selection reached through app.session.build.assemble_session. The control arm is the same assembly
with every retrievability held at 1.0, which empties the due set, so due coverage scores 0 on every
candidate and the selection falls through to the uniform random choice inside the gated fringe.
That is the random-within-fringe control of gate 31, and it differs from the policy arm in the due
coverage term alone.

Nothing here writes to data/ and nothing here modifies the engine.
"""
import json
import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

from app.engine import constants
from app.engine.fringe import DictItemBank, Graph
from app.engine.prior import beta_for_skill, hard_ancestors, p_compensatory, p_knowledge
from app.engine.retention import current_retrievability
from app.engine.state import Confidence, ResponseFormat, SkillState
from app.engine.update import EngineGraph, Observation, apply_observation, rule_based_mastery_states
from app.session.build import assemble_session

FIXTURE_PATH = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "graph_p1.json"
TRAJECTORY_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "student_trajectories"

TRAJECTORY_NAMES = (
   "absent_30_days",
   "ceiling",
   "floor",
   "guesser",
   "prereq_gap_02025",
   "slipper",
)

START_DAY = date(2026, 3, 1)
SIMULATED_DAYS = 30
ABSENCE_AFTER_DAY = 9
ITEMS_PER_ARCHETYPE = 10

INITIAL_HALF_LIFE_DAYS = 5.0
HALF_LIFE_GROWTH = 1.7
HALF_LIFE_CAP_DAYS = 365.0

ATTEMPT_MINUTES = constants.FORECAST_DEFAULT_MINUTES


@dataclass(frozen=True)
class Trajectory:
   name: str
   true_state: dict
   slip: float
   guess: float
   absence_days: int


@dataclass
class SimulationResult:
   name: str
   arm: str
   items_served: int
   declared_mastered: int
   true_declared_mastered: int
   corroborated: int
   states: dict
   trace: list = field(default_factory=list)

   @property
   def mastery_per_item(self):
      if self.items_served == 0:
         return 0.0

      return self.declared_mastered / self.items_served

   @property
   def true_mastery_per_item(self):
      if self.items_served == 0:
         return 0.0

      return self.true_declared_mastered / self.items_served

   @property
   def corroborated_per_item(self):
      if self.items_served == 0:
         return 0.0

      return self.corroborated / self.items_served


def load_fixture():
   return json.loads(FIXTURE_PATH.read_text())


def load_trajectory(name):
   record = json.loads((TRAJECTORY_DIR / f"{name}.json").read_text())

   return Trajectory(
      name=name,
      true_state=record["true_state"],
      slip=record["slip"],
      guess=record["guess"],
      absence_days=record["absence_days"],
   )


def seed_for(name):
   """A fixed seed per trajectory, so both arms see the same student and the same draws."""
   return 1000 + TRAJECTORY_NAMES.index(name)


def simulation_graph():
   """The selection Graph and the update EngineGraph over the same P1 fixture.

   The EngineGraph drops the inert BC-TOP endpoints and the co_requisite edge, as
   tests/engine/conftest.py does, because neither carries credit (R13, R30).
   """
   fixture = load_fixture()
   graph = Graph.from_records(
      archetypes=fixture["archetypes"],
      skills=fixture["skills"],
      edges=fixture["edges"],
      inert_top=fixture["inert_top"],
   )
   inert = set(fixture["inert_top"])
   hard_parents = {}
   supporting_parents = {}
   hard_children = {}

   for edge in fixture["edges"]:
      parent = edge["from"]
      child = edge["to"]
      touches_inert = parent in inert or child in inert
      is_co_requisite = edge["type"] == "co_requisite"

      if touches_inert or is_co_requisite:
         continue

      is_hard = edge["type"] == "hard_prerequisite"

      if is_hard:
         hard_parents.setdefault(child, set()).add(parent)
         hard_children.setdefault(parent, set()).add(child)
      else:
         supporting_parents.setdefault(child, set()).add(parent)

   archetype_counts = {}

   for record in fixture["archetypes"]:
      for skill_id in record["skills"]:
         archetype_counts[skill_id] = archetype_counts.get(skill_id, 0) + 1

   engine_graph = EngineGraph(
      hard_parents=hard_parents,
      supporting_parents=supporting_parents,
      hard_children=hard_children,
      archetype_counts=archetype_counts,
   )

   return graph, engine_graph


def build_states(fixture, graph):
   states = {}

   for record in fixture["skills"]:
      skill_id = record["id"]
      states[skill_id] = SkillState(skill_id, beta=beta_for_skill(skill_id, graph.archetypes))

   for record in fixture["seeded_parents"]:
      states[record["id"]] = SkillState.seeded_mastered(record["id"], START_DAY)

   return states


def build_bank(fixture):
   items = []

   for record in fixture["archetypes"]:
      archetype_id = record["id"]

      for index in range(ITEMS_PER_ARCHETYPE):
         items.append({
            "id": f"{archetype_id}-S{index:02d}",
            "archetype_id": archetype_id,
            "status": "verified",
         })

   return DictItemBank(items)


def calendar(absence_days):
   """One assembled session per calendar day, with the trajectory's absence inserted as a gap."""
   days = []
   day = START_DAY

   for index in range(SIMULATED_DAYS):
      days.append(day)
      day = day + timedelta(days=1)
      is_absence_point = index == ABSENCE_AFTER_DAY

      if is_absence_point:
         day = day + timedelta(days=absence_days)

   return days


class World:
   """The hidden student. Forgetting is exponential with a half-life that grows on retrieval."""

   def __init__(self, trajectory, rng):
      self.trajectory = trajectory
      self.rng = rng
      self.half_life = {}
      self.last_success = {}

   def knows(self, skill_id):
      return bool(self.trajectory.true_state.get(skill_id, True))

   def available(self, skill_id, today):
      if not self.knows(skill_id):
         return False

      practised_on = self.last_success.get(skill_id)
      is_fresh = practised_on is None

      if is_fresh:
         return True

      elapsed = (today - practised_on).days
      half_life = self.half_life.get(skill_id, INITIAL_HALF_LIFE_DAYS)
      retention = 0.5 ** (elapsed / half_life)

      return self.rng.random() < retention

   def reinforce(self, skill_ids, today):
      for skill_id in skill_ids:
         if not self.knows(skill_id):
            continue

         grown = self.half_life.get(skill_id, INITIAL_HALF_LIFE_DAYS) * HALF_LIFE_GROWTH
         self.half_life[skill_id] = min(grown, HALF_LIFE_CAP_DAYS)
         self.last_success[skill_id] = today

   def answer(self, archetype, response_format, today):
      loaded = archetype["skills"]
      all_available = all(self.available(skill_id, today) for skill_id in loaded)
      is_mcq = ResponseFormat(response_format) == ResponseFormat.MCQ
      floor = max(self.trajectory.guess, constants.MCQ_GUESS_FLOOR) if is_mcq else self.trajectory.guess

      if all_available:
         p_correct = 1.0 - self.trajectory.slip
      else:
         p_correct = floor

      is_correct = self.rng.random() < p_correct

      if is_correct and all_available:
         self.reinforce(loaded, today)

      return is_correct


def unmastered_hard_ancestors(skill_id, states, engine_graph):
   """Invariant 3 read off the served item: nothing above it on the hard chain is still open.

   The ancestors come from the EngineGraph, so the inert BC-TOP endpoints are already gone (R13).
   """
   ancestors = hard_ancestors(skill_id, engine_graph.hard_parents)

   return sorted(
      ancestor
      for ancestor in ancestors
      if ancestor in states and not states[ancestor].mastered
   )


def is_corroborated(state):
   """Diagnostic only, never a mastery claim.

   Mastery conditions 2, 4 and 5 of docs/plan/02, so 3 credited unaided successes on 3 distinct
   days spanning at least 7. It is reported beside the declared count because condition 3, two
   distinct archetypes, is unreachable for 53 of the 54 skills in tests/fixtures/graph_p1.json.
   """
   days = sorted(state.success_days)
   has_days = len(days) > 0
   span_days = (days[-1] - days[0]).days if has_days else 0

   meets_successes = state.unaided_success_count >= constants.MASTERY_MIN_UNAIDED_SUCCESSES
   meets_days = len(days) >= constants.MASTERY_MIN_DISTINCT_DAYS
   meets_span = span_days >= constants.MASTERY_MIN_DAY_SPAN

   return meets_successes and meets_days and meets_span


def retrievability_for(arm, states, today):
   is_control = arm == "control"

   if is_control:
      return {skill_id: 1.0 for skill_id in states}

   return current_retrievability(states, today)


def run_simulation(trajectory, seed, arm="policy", days=SIMULATED_DAYS):
   fixture = load_fixture()
   graph, engine_graph = simulation_graph()
   states = build_states(fixture, graph)
   bank = build_bank(fixture)
   engine_rng = random.Random(seed)
   world = World(trajectory, random.Random(seed + 7919))
   attempts = []
   trace = []
   items_served = 0

   for today in calendar(trajectory.absence_days)[:days]:
      retrievability = retrievability_for(arm, states, today)
      session = assemble_session(
         states,
         graph,
         bank,
         [],
         attempts,
         engine_rng,
         today,
         retrievability=retrievability,
      )

      for block_number, block in enumerate(session.blocks[:3], start=1):
         for item in block:
            record = graph.archetypes[item["archetype_id"]]
            primary = graph.primary_skill(record["id"])
            unmastered = unmastered_hard_ancestors(primary, states, engine_graph)
            split = p_knowledge(record, states, engine_graph.hard_parents, retrievability)
            compensatory = p_compensatory(record, states, retrievability)
            is_correct = world.answer(record, item["format"], today)
            per_skill = rule_based_mastery_states(record, {"correct": is_correct})

            observation = Observation(
               archetype_id=record["id"],
               skills=list(record["skills"]),
               per_skill_states=per_skill,
               response_format=item["format"],
               confidence=Confidence.UNSURE,
               served_stage=item["stage"],
            )
            apply_observation(states, engine_graph, observation, today)

            attempts.append({
               "archetype_id": record["id"],
               "item_id": item["id"],
               "attempted_on": today,
               "stage": item["stage"],
               "minutes": ATTEMPT_MINUTES,
               "corrected": not is_correct,
            })
            trace.append({
               "day": today.isoformat(),
               "block": block_number,
               "item_id": item["id"],
               "archetype_id": record["id"],
               "primary_skill": primary,
               "unmastered_hard_ancestors": unmastered,
               "stage": item["stage"].value,
               "format": ResponseFormat(item["format"]).value,
               "correct": is_correct,
               "p_split": split,
               "p_compensatory": compensatory,
            })
            items_served += 1

   simulated_ids = [record["id"] for record in fixture["skills"]]
   corroborated = [skill_id for skill_id in simulated_ids if is_corroborated(states[skill_id])]
   declared = [skill_id for skill_id in simulated_ids if states[skill_id].mastered]
   truly_known = [skill_id for skill_id in declared if world.knows(skill_id)]

   return SimulationResult(
      name=trajectory.name,
      arm=arm,
      items_served=items_served,
      declared_mastered=len(declared),
      true_declared_mastered=len(truly_known),
      corroborated=len(corroborated),
      states=states,
      trace=trace,
   )
