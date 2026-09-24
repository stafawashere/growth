"""Synthetic students over the whole 541-skill graph, for the P2 gates and evals.

docs/plan/10-quality-and-evaluation.md "The world" puts synthetic students on the real graph; the
P1 runner in app/sim/runner.py kept to the 54-skill fixture, and this module is its whole-graph
counterpart. The library is loaded through app/content/loader.py and built into the same two
graphs the running app uses (app/runtime/graphs.py). The bank is synthetic, a fixed number of
verified items for every active archetype, because the published bank covers three units today
and the P2 gates are about the engine rather than about the bank's reach; the real bank's reach
is reported separately by the diagnostic's coverage gaps.

A student's hidden state is a knowledge state in the sense of knowledge space theory: every unit
gets an ability, each skill is known with a chance that rises with that ability and falls with
the skill's difficulty prior, and a skill whose hard parent is unknown is unknown, so the state is
closed under prerequisites. Observation noise is slip and guess, the guess floored at 0.25 on
MCQ, and forgetting is the P1 runner's exponential half-life curve, never FSRS.
"""
import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from functools import lru_cache

from app.content.loader import load_snapshot
from app.engine import constants, diagnostic
from app.engine.fringe import DictItemBank
from app.engine.prior import p_knowledge
from app.engine.retention import current_retrievability
from app.engine.state import Confidence, FadingStage
from app.engine.strength import sigmoid
from app.engine.update import Observation, apply_observation, rule_based_mastery_states
from app.runtime.context import DEFAULT_CONTENT_ROOT
from app.runtime.graphs import graphs_from_snapshot
from app.session.build import assemble_session
from app.session.seed import initial_states
from app.sim.runner import Trajectory, World

START_DAY = date(2026, 10, 1)
ITEMS_PER_ARCHETYPE = 3
ATTEMPT_MINUTES = constants.FORECAST_DEFAULT_MINUTES

ABILITY_LOW = -3.0
ABILITY_HIGH = 3.0
SLIP = 0.1
SHORT_ANSWER_GUESS = 0.02
NOT_LEARNED_WHEN_KNOWING_NONE = 0.8
NOT_LEARNED_WHEN_KNOWING_SOME = 0.1


@dataclass(frozen=True)
class Library:
   snapshot: object
   graph: object
   engine_graph: object


@dataclass(frozen=True)
class Student:
   name: str
   true_state: dict
   slip: float
   guess: float
   absence_days: int = 0
   unit_ability: dict = field(default_factory=dict)


@lru_cache(maxsize=1)
def library():
   snapshot = load_snapshot(DEFAULT_CONTENT_ROOT)
   graph, engine_graph = graphs_from_snapshot(snapshot)

   return Library(snapshot=snapshot, graph=graph, engine_graph=engine_graph)


def synthetic_bank(graph, items_per_archetype=ITEMS_PER_ARCHETYPE, archetype_ids=None):
   chosen = sorted(graph.archetypes) if archetype_ids is None else sorted(archetype_ids)
   items = []

   for archetype_id in chosen:
      for index in range(items_per_archetype):
         items.append({
            "id": f"{archetype_id}-SYN{index:02d}",
            "archetype_id": archetype_id,
            "status": "verified",
         })

   return DictItemBank(items)


def fresh_states():
   return initial_states(library().snapshot, START_DAY)


def topological_skills(graph, engine_graph):
   order = []
   placed = set()
   remaining = sorted(graph.skills)

   while remaining:
      progressed = []

      for skill_id in remaining:
         parents = [
            parent
            for parent in engine_graph.hard_parents.get(skill_id, ())
            if parent in graph.skills
         ]
         is_ready = all(parent in placed for parent in parents)

         if is_ready:
            order.append(skill_id)
            placed.add(skill_id)
            progressed.append(skill_id)

      if not progressed:
         order.extend(remaining)
         break

      remaining = [skill_id for skill_id in remaining if skill_id not in placed]

   return order


def make_student(name, rng, unit_ability=None):
   """A knowledge state closed under hard prerequisites, from one ability per unit."""
   world = library()
   graph = world.graph
   states = fresh_states()
   units = diagnostic.graph_units(graph)
   ability = dict(unit_ability) if unit_ability else {
      unit: rng.uniform(ABILITY_LOW, ABILITY_HIGH) for unit in units
   }
   known = {}

   for skill_id in topological_skills(graph, world.engine_graph):
      record = graph.skills[skill_id]
      unit_level = ability.get(record.get("unit"), 0.0)
      chance = sigmoid(unit_level + states[skill_id].beta)
      parents_known = all(
         known.get(parent, True)
         for parent in world.engine_graph.hard_parents.get(skill_id, ())
      )
      known[skill_id] = parents_known and rng.random() < chance

   return Student(
      name=name,
      true_state=known,
      slip=SLIP,
      guess=SHORT_ANSWER_GUESS,
      unit_ability=ability,
   )


def diagnostic_outcome(world_model, record, response_format, today, rng):
   """A miss is declared not learned mostly when none of the item's skills is known, which is
   what the button on 08's diagnostic item offers a student who has not met the topic."""
   is_correct = world_model.answer(record, response_format, today)

   if is_correct:
      return diagnostic.OUTCOME_CORRECT

   knows_any = any(world_model.knows(skill_id) for skill_id in record["skills"])
   declare_share = NOT_LEARNED_WHEN_KNOWING_SOME if knows_any else NOT_LEARNED_WHEN_KNOWING_NONE
   says_not_learned = rng.random() < declare_share

   if says_not_learned:
      return diagnostic.OUTCOME_NOT_LEARNED

   return diagnostic.OUTCOME_INCORRECT


@dataclass
class DiagnosticOutcome:
   run: object
   states: dict
   measures: list


def run_diagnostic(student, bank, seed, states=None, today=START_DAY, response_format="short_answer"):
   """One diagnostic over the student, applying every scored answer through the ordinary update
   and the placement at the end, exactly as the service does."""
   world = library()
   graph = world.graph
   states = fresh_states() if states is None else states
   rng = random.Random(seed)
   world_model = World(student_trajectory(student), random.Random(seed + 7919))
   retrievability = current_retrievability(states, today)
   run = diagnostic.start_run(states, graph, bank, retrievability, rng, response_format)
   measures = [unit_measure(run)]

   while True:
      record = diagnostic.next_archetype(run, graph, bank, rng)

      if record is None:
         break

      outcome = diagnostic_outcome(world_model, record, response_format, today, rng)
      entry = run.pending
      diagnostic.record_outcome(run, record, outcome, item_id=f"{record['id']}-SYN00")

      if not entry["held_out"]:
         apply_diagnostic_observation(states, world.engine_graph, record, outcome, response_format, today)

      measures.append(unit_measure(run))

   diagnostic.place(run, states, graph, today)

   return DiagnosticOutcome(run=run, states=states, measures=measures)


def apply_diagnostic_observation(states, engine_graph, record, outcome, response_format, today):
   is_not_learned = outcome == diagnostic.OUTCOME_NOT_LEARNED

   if is_not_learned:
      per_skill = {skill_id: "not_attempted" for skill_id in record["skills"]}
   else:
      per_skill = rule_based_mastery_states(record, {"correct": outcome == diagnostic.OUTCOME_CORRECT})

   observation = Observation(
      archetype_id=record["id"],
      skills=list(record["skills"]),
      per_skill_states=per_skill,
      response_format=response_format,
      confidence=Confidence.UNSURE,
      served_stage=FadingStage.UNSUPPORTED,
   )
   apply_observation(states, engine_graph, observation, today)


def unit_measure(run):
   """The unit posterior after an item, which eval_diagnostic_information tracks item by item."""
   return {unit: list(values) for unit, values in run.posterior.items()}


def student_trajectory(student):
   return Trajectory(
      name=student.name,
      true_state=student.true_state,
      slip=student.slip,
      guess=student.guess,
      absence_days=student.absence_days,
   )


@dataclass
class DayRecord:
   day: date
   session: object
   records: list
   predictions: list = field(default_factory=list)


def served_records(session, graph):
   return [graph.archetypes[item["archetype_id"]] for item in session.served]


def run_days(
   student,
   bank,
   seed,
   days,
   states=None,
   arm="policy",
   start=START_DAY,
   rules=None,
   ordering=None,
):
   """Daily assembled sessions answered by the hidden student.

   arm "control" holds retrievability at 1.0, which empties the due set, so every choice is the
   uniform draw inside the gated fringe, the random-within-fringe control of 10. ordering, when
   given, replaces block 2's two-term ordering, which is how app/sim/five_term.py runs.
   """
   world = library()
   graph = world.graph
   engine_graph = world.engine_graph
   states = fresh_states() if states is None else states
   engine_rng = random.Random(seed)
   world_model = World(student_trajectory(student), random.Random(seed + 104729))
   attempts = []
   history = []
   served_total = 0

   for offset in range(days):
      today = start + timedelta(days=offset)
      is_control = arm == "control"
      retrievability = (
         {skill_id: 1.0 for skill_id in states}
         if is_control
         else current_retrievability(states, today)
      )
      options = {} if rules is None else {"rules": rules}

      if ordering is not None:
         options["ordering"] = ordering
      session = assemble_session(
         states,
         graph,
         bank,
         [],
         attempts,
         engine_rng,
         today,
         retrievability=retrievability,
         **options,
      )

      predictions = []

      for item in session.served:
         record = graph.archetypes[item["archetype_id"]]
         predicted = p_knowledge(record, states, engine_graph.hard_parents, retrievability)
         is_correct = world_model.answer(record, item["format"], today)
         predictions.append((predicted, is_correct))
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
         served_total += 1

      history.append(DayRecord(
         day=today,
         session=session,
         records=served_records(session, graph),
         predictions=predictions,
      ))

   return history, states, world_model, served_total


def true_known_mastered(states, world_model, graph):
   declared = [skill_id for skill_id in graph.skills if states[skill_id].mastered]
   truly = [skill_id for skill_id in declared if world_model.knows(skill_id)]

   return declared, truly

