"""A synthetic world that learns, for the P7 policy comparison of docs/plan/10 "Offline simulation
of the engine against synthetic students".

The P2 world in app/sim/whole_graph.py fixes each student's hidden knowledge for the run, so its
"truly mastered per item" counted how fast a policy found what was already known. The ledger
recorded that as a defect before P7 could rule on the five-term score. Here a student also has a
per-skill learning rate drawn from a band, as 10 "The world" asks: an attempt on an item can turn
an unknown skill known, but only once every hard parent of that skill is known, so the hidden
state stays closed under prerequisites. Learning is likelier at the supported fading stages,
because a worked example teaches more than an unsupported attempt.

Forgetting is never FSRS. The exponential arm is the P1 runner's half-life curve; the power-law
arm uses the same half-life, retention (1 + t / h) ** -1, which is also 0.5 at t = h, so the two
arms differ in shape alone. Every number below marked as a band or a multiplier is invented for
the simulator, which is why every acceptance comparison in 10 is relative.

A run is a pure function of its seed: the student, the engine's draws and the world's draws each
come from their own random.Random derived from it, and nothing reads the clock.

WorldRules carries three corrections made in stage 12 (docs/operator/selection-study.md), each of
which LEGACY_WORLD turns off to reproduce the stage 8 record. Keyed draws give every chance the
world rolls its own uniform, fixed by the student's seed and by what is rolled (which skill or
archetype, which day, which occurrence that day), so two arms that serve the same item on the same
day see the same outcome however they got there, and a paired comparison is paired in its draws
and not only in its student. Consolidated prior knowledge starts every skill known before the run
at the capped half-life, where the stage 8 world held it at retention 1.0 until its first practice
and then let it decay from the initial half-life, so practising a known skill lowered its
retention. Daily growth lets a successful retrieval grow a half-life at most once per calendar
day, the plan's reading of Rohrer and Taylor 2006 in docs/plan/01 ("Same-day repeats | do not
count"), where the stage 8 world grew it on every correct answer and so rewarded massing.
"""
import random
import statistics
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import timedelta

from app.engine import constants, fringe, prior, select
from app.engine.interleave import FULL_RULES, InterleaveRules
from app.engine.retention import current_retrievability
from app.engine.state import Confidence, FadingStage
from app.engine.strength import probability
from app.engine.update import Observation, apply_observation, rule_based_mastery_states
from app.session.build import assemble_session
from app.sim import five_term, whole_graph
from app.sim.runner import HALF_LIFE_CAP_DAYS, HALF_LIFE_GROWTH, INITIAL_HALF_LIFE_DAYS

LEARNING_RATE_LOW = 0.05
LEARNING_RATE_HIGH = 0.30
STAGE_LEARNING = {
   FadingStage.EXAMPLE: 1.0,
   FadingStage.COMPLETION: 0.75,
   FadingStage.UNSUPPORTED: 0.5,
}

EXPONENTIAL = "exponential"
POWER_LAW = "power_law"
CURVES = (EXPONENTIAL, POWER_LAW)

RETENTION_PROBE_DAYS = (7, 30)

NO_INTERLEAVING = InterleaveRules(
   max_consecutive=False,
   block_skills=False,
   block_units=False,
   family_cap=False,
   translation_floor=False,
)


@dataclass(frozen=True)
class WorldRules:
   keyed_draws: bool = True
   consolidated_prior: bool = True
   daily_growth: bool = True
   relearn_on_feedback: bool = True


WORLD = WorldRules()
LEGACY_WORLD = WorldRules(
   keyed_draws=False, consolidated_prior=False, daily_growth=False, relearn_on_feedback=False
)


@dataclass(frozen=True)
class Arm:
   """One row of 10's arm list. overrides patches app.engine.constants for the run only.
   world_ordering, when given, is called with the hidden world and returns a block 2 ordering; it
   exists for the controls of docs/operator/selection-study.md, which may read what no policy can.
   retrieval_ordering does in block 3 what ordering does in block 2. learner, when given, is called
   once per student and returns an object with a block 2 ordering and an observe(record,
   is_correct, today) that sees every answer; it exists for policies that keep a running estimate,
   which a module-level arm shared by every student in a worker cannot hold."""
   name: str
   control: bool = False
   ordering: object = None
   rules: object = FULL_RULES
   overrides: tuple = ()
   compensatory: bool = False
   world_ordering: object = None
   retrieval_ordering: object = None
   learner: object = None


ARMS = {
   "two_term": Arm("two_term"),
   "random_control": Arm("random_control", control=True),
   "five_term": Arm("five_term", ordering=five_term.five_term_ordering),
   "no_interleaving": Arm("no_interleaving", rules=NO_INTERLEAVING),
   "no_propagation": Arm(
      "no_propagation",
      overrides=(
         ("PROPAGATION_HARD_ONE_HOP", 0.0),
         ("PROPAGATION_HARD_TWO_HOP", 0.0),
         ("PROPAGATION_SUPPORTING_ONE_HOP", 0.0),
      ),
   ),
   "decay_lambda_2": Arm("decay_lambda_2", overrides=(("LAMBDA", 2.0),)),
   "compensatory_only": Arm("compensatory_only", compensatory=True),
   "stage_high_0_6": Arm("stage_high_0_6", overrides=(("STAGE_LOW", 0.40), ("STAGE_HIGH", 0.60))),
   "stage_high_0_7": Arm("stage_high_0_7", overrides=(("STAGE_HIGH", 0.70),)),
   "stage_high_0_8": Arm("stage_high_0_8", overrides=(("STAGE_HIGH", 0.80),)),
}


@contextmanager
def arm_engine(arm):
   """Applies the arm's constant overrides and, for the compensatory arm, swaps the conjunctive
   prediction for the compensatory one wherever selection reads it. Restores both on exit."""
   saved_constants = {name: getattr(constants, name) for name, _ in arm.overrides}
   saved_predictors = (fringe.p_knowledge, select.p_knowledge)

   for name, value in arm.overrides:
      setattr(constants, name, value)

   if arm.compensatory:
      def compensatory(archetype, states, hard_parents, retrievability=None):
         return prior.p_compensatory(archetype, states, retrievability)

      fringe.p_knowledge = compensatory
      select.p_knowledge = compensatory

   try:
      yield
   finally:
      for name, value in saved_constants.items():
         setattr(constants, name, value)

      fringe.p_knowledge, select.p_knowledge = saved_predictors


@dataclass
class LearningStudent:
   name: str
   known: dict
   learning_rate: dict
   slip: float
   guess: float


def make_learning_student(name, seed):
   """The P2 knowledge state closed under hard prerequisites, plus a learning rate per skill."""
   rng = random.Random(seed)
   base = whole_graph.make_student(name, rng)

   return learning_student_from(base, rng)


def learning_student_from(base, rng):
   """A P2 student given the per-skill learning rate of 10's world, drawn from the band."""
   rates = {
      skill_id: rng.uniform(LEARNING_RATE_LOW, LEARNING_RATE_HIGH)
      for skill_id in sorted(base.true_state)
   }

   return LearningStudent(
      name=base.name,
      known=dict(base.true_state),
      learning_rate=rates,
      slip=base.slip,
      guess=base.guess,
   )


def retention_after(elapsed_days, half_life, curve):
   is_power_law = curve == POWER_LAW

   if is_power_law:
      return (1.0 + elapsed_days / half_life) ** -1.0

   return 0.5 ** (elapsed_days / half_life)


class KeyedDraws:
   """One uniform per named roll: the same seed and the same key give the same number, and the
   n-th roll of a key on a day is the same n-th roll in every arm."""

   def __init__(self, seed):
      self.seed = seed
      self.counts = Counter()

   def random(self, *key):
      self.counts[key] += 1
      occurrence = self.counts[key]

      return random.Random(f"{self.seed}|{'|'.join(map(str, key))}|{occurrence}").random()


class LearningWorld:
   """The hidden student. knows() reads a state that attempts can grow."""

   def __init__(
      self,
      student,
      hard_parents,
      rng,
      curve=EXPONENTIAL,
      rules=LEGACY_WORLD,
      seed=None,
      start_day=None,
   ):
      self.student = student
      self.hard_parents = hard_parents
      self.rng = rng
      self.curve = curve
      self.rules = rules
      self.draws = KeyedDraws(seed) if rules.keyed_draws else None
      self.half_life = {}
      self.last_success = {}
      self.grown_on = {}
      self.learned = {}
      starts_consolidated = rules.consolidated_prior and start_day is not None

      if starts_consolidated:
         for skill_id, known in sorted(student.known.items()):
            if known:
               self.half_life[skill_id] = HALF_LIFE_CAP_DAYS
               self.last_success[skill_id] = start_day

   def roll(self, *key):
      if self.draws is None:
         return self.rng.random()

      return self.draws.random(*key)

   def knows(self, skill_id):
      return bool(self.student.known.get(skill_id, True))

   def retention(self, skill_id, today):
      if not self.knows(skill_id):
         return 0.0

      practised_on = self.last_success.get(skill_id)
      is_fresh = practised_on is None

      if is_fresh:
         return 1.0

      elapsed = (today - practised_on).days
      half_life = self.half_life.get(skill_id, INITIAL_HALF_LIFE_DAYS)

      return retention_after(elapsed, half_life, self.curve)

   def available(self, skill_id, today):
      if not self.knows(skill_id):
         return False

      return self.roll("available", skill_id, today) < self.retention(skill_id, today)

   def relearn(self, skill_ids, today):
      """A known skill that was not retrieved for this item is re-encoded by the feedback: last
      retrieved today, with one growth step of its half-life undone and never below the initial
      value. Restarting at the initial half-life instead threw a consolidated skill from 365 days
      to 5 on one unlucky roll, and mastery fell (222, 211 and 259 against 277, 255 and 288)."""
      for skill_id in skill_ids:
         shortened = self.half_life.get(skill_id, INITIAL_HALF_LIFE_DAYS) / HALF_LIFE_GROWTH
         self.half_life[skill_id] = max(shortened, INITIAL_HALF_LIFE_DAYS)
         self.last_success[skill_id] = today

   def reinforce(self, skill_ids, today):
      for skill_id in skill_ids:
         grew_today = self.grown_on.get(skill_id) == today
         holds_growth = self.rules.daily_growth and grew_today

         if not holds_growth:
            grown = self.half_life.get(skill_id, INITIAL_HALF_LIFE_DAYS) * HALF_LIFE_GROWTH
            self.half_life[skill_id] = min(grown, HALF_LIFE_CAP_DAYS)
            self.grown_on[skill_id] = today

         self.last_success[skill_id] = today

   def ready_to_learn(self, skill_id):
      parents = self.hard_parents.get(skill_id, ())
      parents_known = all(self.knows(parent) for parent in parents)

      return parents_known and not self.knows(skill_id)

   def learn(self, skill_ids, stage, today):
      multiplier = STAGE_LEARNING[FadingStage(stage)]

      for skill_id in sorted(skill_ids):
         if not self.ready_to_learn(skill_id):
            continue

         chance = self.student.learning_rate.get(skill_id, LEARNING_RATE_LOW) * multiplier
         learns = self.roll("learn", skill_id, today) < chance

         if learns:
            self.student.known[skill_id] = True
            self.learned[skill_id] = today
            self.last_success[skill_id] = today

   def answer(self, record, response_format, stage, today):
      loaded = record["skills"]
      relearns = self.rules.relearn_on_feedback

      if relearns:
         availability = {skill_id: self.available(skill_id, today) for skill_id in loaded}
         all_available = all(availability.values())
      else:
         availability = {}
         all_available = all(self.available(skill_id, today) for skill_id in loaded)

      is_mcq = response_format == "mcq"
      floor = max(self.student.guess, constants.MCQ_GUESS_FLOOR) if is_mcq else self.student.guess
      p_correct = 1.0 - self.student.slip if all_available else floor
      is_correct = self.roll("answer", record["id"], today) < p_correct

      if is_correct and all_available:
         self.reinforce(loaded, today)

      lapsed = [
         skill_id
         for skill_id in loaded
         if self.knows(skill_id) and not availability.get(skill_id, True)
      ]

      if relearns and lapsed:
         self.relearn(lapsed, today)

      self.learn(loaded, stage, today)

      return is_correct


@dataclass
class StudentRun:
   student: str
   seed: int
   arm: str
   curve: str
   items: int
   known_at_start: int
   learned: int
   taught_retained: float
   taught_retained_day_30: float
   declared_mastered: int
   declared_not_known: int
   placed_mastered: int
   placed_not_known: int
   retention_day_7: float
   retention_day_30: float
   measurement_bias: float
   trace: list = field(default_factory=list)

   @property
   def true_mastery_per_item(self):
      return self.taught_retained / self.items if self.items else 0.0

   @property
   def delayed_mastery_per_item(self):
      """What the run taught that the student can still retrieve 30 days after it, per item: the
      measure that sees spacing, where true_mastery_per_item reads retention the day after."""
      return self.taught_retained_day_30 / self.items if self.items else 0.0

   @property
   def false_mastery_share(self):
      return self.declared_not_known / self.declared_mastered if self.declared_mastered else 0.0


def measurement_bias(states, world, today):
   """10's definition: the mean signed difference between sigmoid(m_k) and the hidden true
   competence, here the chance the student can retrieve the skill today, over observed skills."""
   differences = [
      probability(state) - world.retention(skill_id, today)
      for skill_id, state in sorted(states.items())
      if state.observation_count > 0
   ]

   return statistics.mean(differences) if differences else 0.0


def mean_retention(world, skill_ids, day):
   values = [world.retention(skill_id, day) for skill_id in skill_ids]

   return statistics.mean(values) if values else 0.0


def run_student(
   arm,
   seed,
   days,
   curve=EXPONENTIAL,
   keep_trace=False,
   world_rules=WORLD,
   engine_seed=None,
):
   """One student through a diagnostic and then one assembled session per day. engine_seed, when
   given, reseeds only the engine's draws after the diagnostic (tie-breaks and item picks), so the
   same policy can be run against itself on the same student and the same world."""
   library = whole_graph.library()
   graph = library.graph
   engine_graph = library.engine_graph
   bank = whole_graph.synthetic_bank(graph)
   student = make_learning_student(f"learner-{seed}", seed)
   known_at_start = {skill_id for skill_id, known in student.known.items() if known}

   placed = whole_graph.run_diagnostic(
      whole_graph.Student(
         name=student.name,
         true_state=dict(student.known),
         slip=student.slip,
         guess=student.guess,
      ),
      bank,
      seed=seed,
   )
   states = placed.states
   placed_ids = set(placed.run.placement["newly_mastered"])
   world = LearningWorld(
      student,
      engine_graph.hard_parents,
      random.Random(seed + 104729),
      curve,
      rules=world_rules,
      seed=seed + 104729,
      start_day=whole_graph.START_DAY,
   )
   engine_rng = random.Random(seed if engine_seed is None else engine_seed)
   learner = arm.learner() if arm.learner is not None else None
   ordering = arm.ordering

   if learner is not None:
      ordering = learner.ordering

   if arm.world_ordering is not None:
      ordering = arm.world_ordering(world)
   attempts = []
   trace = []
   items = 0
   today = whole_graph.START_DAY

   with arm_engine(arm):
      for offset in range(days):
         today = whole_graph.START_DAY + timedelta(days=offset)
         retrievability = (
            {skill_id: 1.0 for skill_id in states}
            if arm.control
            else current_retrievability(states, today)
         )
         options = {"rules": arm.rules}

         if ordering is not None:
            options["ordering"] = ordering

         if arm.retrieval_ordering is not None:
            options["retrieval_ordering"] = arm.retrieval_ordering

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

         for item in session.served:
            record = graph.archetypes[item["archetype_id"]]
            is_correct = world.answer(record, item["format"], item["stage"], today)

            if learner is not None:
               learner.observe(record, is_correct, today)

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
               "minutes": whole_graph.ATTEMPT_MINUTES,
               "corrected": not is_correct,
            })
            items += 1

            if keep_trace:
               trace.append((today.isoformat(), item["id"], FadingStage(item["stage"]).value, is_correct))

   end_day = today + timedelta(days=1)
   taught_retained = sum(world.retention(skill_id, end_day) for skill_id in sorted(world.learned))
   late_day = end_day + timedelta(days=RETENTION_PROBE_DAYS[1])
   taught_retained_day_30 = sum(world.retention(skill_id, late_day) for skill_id in sorted(world.learned))
   declared = [skill_id for skill_id in graph.skills if states[skill_id].mastered]
   declared_not_known = [skill_id for skill_id in declared if not world.knows(skill_id)]
   placed = [skill_id for skill_id in declared if skill_id in placed_ids]
   placed_not_known = [skill_id for skill_id in placed if not world.knows(skill_id)]
   known_now = sorted(skill_id for skill_id in graph.skills if world.knows(skill_id))

   return StudentRun(
      student=student.name,
      seed=seed,
      arm=arm.name,
      curve=curve,
      items=items,
      known_at_start=len(known_at_start),
      learned=len(world.learned),
      taught_retained=taught_retained,
      taught_retained_day_30=taught_retained_day_30,
      declared_mastered=len(declared),
      declared_not_known=len(declared_not_known),
      placed_mastered=len(placed),
      placed_not_known=len(placed_not_known),
      retention_day_7=mean_retention(world, known_now, end_day + timedelta(days=RETENTION_PROBE_DAYS[0])),
      retention_day_30=mean_retention(world, known_now, end_day + timedelta(days=RETENTION_PROBE_DAYS[1])),
      measurement_bias=measurement_bias(states, world, end_day),
      trace=trace,
   )
