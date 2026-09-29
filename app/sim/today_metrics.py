"""What Today's assembly does on a synthetic student, counted without changing what it serves.

measure_student runs one student through app/sim/learning.run_student with the engine's own
functions wrapped for counting and restored afterwards, the monkeypatch style of
tools/selection_study.py. A block 2 choice is counted only when its item is served in block 2.
The window counterfactual reruns the same choice on a copied random.Random with no interleaving
rules, so the run's own draws are untouched. Every number is a simulation's measurement.
"""
import random
import statistics
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field

from app.engine import select
from app.session import build
from app.sim import learning, selection_study, whole_graph

DUE_COVERAGE = "due_coverage"
DUE_COVERAGE_TIE = "due_coverage_tie"
RANDOM = "random"
DECIDERS = (DUE_COVERAGE, DUE_COVERAGE_TIE, RANDOM)


@dataclass
class TodayMetrics:
   arm: str
   seed: int
   days: int
   curve: str
   world: str
   sessions: int = 0
   items: int = 0
   block2_choices: int = 0
   block2_tied: int = 0
   block2_tie_sizes: dict = field(default_factory=dict)
   block2_decided_by: dict = field(default_factory=lambda: {name: 0 for name in DECIDERS})
   window_sizes: dict = field(default_factory=dict)
   window_changed_pick: int = 0
   hypercorrection_served: int = 0
   requeues_served: int = 0
   due_per_session: list = field(default_factory=list)
   items_before_mastery: list = field(default_factory=list)
   forecast_minutes_total: float = 0.0
   simulated_minutes_total: float = 0.0
   trace: list = field(default_factory=list)

   @property
   def items_per_session(self):
      return self.items / self.sessions if self.sessions else 0.0

   @property
   def forecast_per_session(self):
      return self.forecast_minutes_total / self.sessions if self.sessions else 0.0

   @property
   def compression_ratios(self):
      """Due skills per archetype the cover chose, over sessions with a due skill and a cover."""
      ratios = []

      for due_count, cover_count, _uncovered in self.due_per_session:
         has_due = due_count > 0
         has_cover = cover_count > 0

         if has_due and has_cover:
            ratios.append(due_count / cover_count)

      return ratios

   @property
   def due_sessions(self):
      return sum(1 for due_count, _, _ in self.due_per_session if due_count > 0)

   @property
   def items_before_mastery_histogram(self):
      return dict(sorted(Counter(self.items_before_mastery).items()))

   def scalars(self):
      """One number per measure, None where the run gives the measure no denominator."""
      ratios = self.compression_ratios
      before = self.items_before_mastery
      choices = self.block2_choices
      window_removed = [
         (before_count - after_count) * count
         for (before_count, after_count), count in self.window_sizes.items()
      ]
      due_sessions = [row for row in self.due_per_session if row[0] > 0]

      return {
         "sessions": self.sessions,
         "items": self.items,
         "items per session": self.items_per_session,
         "forecast minutes per session": self.forecast_per_session,
         "forecast minutes total": self.forecast_minutes_total,
         "simulated minutes total": self.simulated_minutes_total,
         "forecast over simulated": (
            self.forecast_minutes_total / self.simulated_minutes_total if self.simulated_minutes_total else None
         ),
         "block 2 choices": choices,
         "block 2 tied": self.block2_tied,
         "block 2 tied share": self.block2_tied / choices if choices else None,
         "decided by due coverage": self.block2_decided_by[DUE_COVERAGE],
         "decided by due coverage tie": self.block2_decided_by[DUE_COVERAGE_TIE],
         "decided by random": self.block2_decided_by[RANDOM],
         "decided by random share": self.block2_decided_by[RANDOM] / choices if choices else None,
         "window candidates removed per choice": sum(window_removed) / choices if choices else None,
         "window changed the pick": self.window_changed_pick,
         "window changed the pick share": self.window_changed_pick / choices if choices else None,
         "hypercorrection items served": self.hypercorrection_served,
         "requeued items served": self.requeues_served,
         "sessions with a due skill": self.due_sessions,
         "due skills per due session": (
            statistics.mean(row[0] for row in due_sessions) if due_sessions else None
         ),
         "cover archetypes per due session": (
            statistics.mean(row[1] for row in due_sessions) if due_sessions else None
         ),
         "uncovered skills per due session": (
            statistics.mean(row[2] for row in due_sessions) if due_sessions else None
         ),
         "compression ratio, mean": statistics.mean(ratios) if ratios else None,
         "skills mastered from practice": len(before),
         "items before mastery, mean": statistics.mean(before) if before else None,
         "items before mastery, median": statistics.median(before) if before else None,
      }

   def to_json(self):
      return {
         "arm": self.arm,
         "seed": self.seed,
         "days": self.days,
         "curve": self.curve,
         "world": self.world,
         "scalars": self.scalars(),
         "block2_tie_sizes": {str(size): count for size, count in sorted(self.block2_tie_sizes.items())},
         "block2_decided_by": dict(self.block2_decided_by),
         "window_sizes": {
            f"{before_count},{after_count}": count
            for (before_count, after_count), count in sorted(self.window_sizes.items())
         },
         "due_per_session": [list(row) for row in self.due_per_session],
         "items_before_mastery": list(self.items_before_mastery),
         "items_before_mastery_histogram": {
            str(count): skills for count, skills in self.items_before_mastery_histogram.items()
         },
      }


def tie_outcome(covers):
   """The size of the pool choose_by_due_coverage shuffles, and what decided the choice."""
   best_cover = max(covers)
   is_uncovered = best_cover == 0

   if is_uncovered:
      return len(covers), RANDOM

   pool_size = sum(1 for cover in covers if cover == best_cover)
   is_unique = pool_size == 1

   return pool_size, DUE_COVERAGE if is_unique else DUE_COVERAGE_TIE


def record_choice(metrics, decision):
   pool_size, decider = decision["pool_size"], decision["decided_by"]
   metrics.block2_choices += 1
   metrics.block2_tie_sizes[pool_size] = metrics.block2_tie_sizes.get(pool_size, 0) + 1
   metrics.block2_decided_by[decider] += 1

   if pool_size > 1:
      metrics.block2_tied += 1

   window_key = (decision["window_before"], decision["window_after"])
   metrics.window_sizes[window_key] = metrics.window_sizes.get(window_key, 0) + 1

   if decision["window_changed_pick"]:
      metrics.window_changed_pick += 1


class Instruments:
   """The wrappers and the state they share while one run is measured."""

   def __init__(self, metrics):
      self.metrics = metrics
      self.in_block2 = False
      self.in_counterfactual = False
      self.decision = None
      self.session_choices = []
      self.mastered = None
      self.loaded_counts = Counter()

   def counting(self):
      return self.in_block2 and not self.in_counterfactual

   def wrap_constrained_candidates(self, original):
      def constrained_candidates(records, history, graph, bank, excluded_ids, rules, unit_counts):
         if self.counting():
            servable = select.servable_records(records, bank, excluded_ids)
            window_allowed = select.window_filter(servable, history, graph, rules)[0]
            self.decision["window_before"] = len(servable)
            self.decision["window_after"] = len(window_allowed)

         return original(records, history, graph, bank, excluded_ids, rules, unit_counts)

      return constrained_candidates

   def wrap_choose_by_due_coverage(self, original):
      def choose_by_due_coverage(records, states, graph, today, retrievability, rng):
         has_records = len(records) > 0

         if self.counting() and has_records:
            covers = [
               select.due_coverage(record, states, graph, today, retrievability)
               for record in records
            ]
            pool_size, decider = tie_outcome(covers)
            self.decision["pool_size"] = pool_size
            self.decision["decided_by"] = decider

         return original(records, states, graph, today, retrievability, rng)

      return choose_by_due_coverage

   def wrap_next_item_learning(self, original):
      def next_item_learning(states, graph, bank, probes, history, rng, today, **options):
         counterfactual_rng = random.Random()
         counterfactual_rng.setstate(rng.getstate())
         counterfactual_probes = list(probes) if probes is not None else None
         self.decision = {}
         self.in_block2 = True

         try:
            selection = original(states, graph, bank, probes, history, rng, today, **options)
         finally:
            self.in_block2 = False

         decision = self.decision
         self.decision = None
         was_scored = "decided_by" in decision
         has_item = selection.item is not None
         went_through_choice = was_scored and has_item

         if not went_through_choice:
            return selection

         unruled = dict(options, rules=learning.NO_INTERLEAVING)
         self.in_counterfactual = True

         try:
            alternative = original(
               states, graph, bank, counterfactual_probes, history, counterfactual_rng, today, **unruled
            )
         finally:
            self.in_counterfactual = False

         alternative_id = alternative.item["id"] if alternative.item is not None else None
         decision["window_changed_pick"] = alternative_id != selection.item["id"]
         self.session_choices.append((selection.item, decision))

         return selection

      return next_item_learning

   def wrap_assemble_session(self, original):
      def assemble_session(*args, **options):
         self.session_choices = []
         session = original(*args, **options)
         self.read_session(session)

         return session

      return assemble_session

   def read_session(self, session):
      metrics = self.metrics
      metrics.sessions += 1
      metrics.forecast_minutes_total += session.forecast_total

      for entry in session.block2:
         is_item = entry.get("kind") == build.ITEM_KIND

         if not is_item:
            continue

         for chosen, decision in self.session_choices:
            if chosen is entry:
               record_choice(metrics, decision)
               break

      queue = session.due_queue
      serves_hyper = len(queue.hypercorrection_skills) > 0

      for entry in session.block1:
         is_requeue = any(entry is requeued for requeued in session.requeued)

         if is_requeue:
            metrics.requeues_served += 1
         elif serves_hyper:
            metrics.hypercorrection_served += 1

      metrics.due_per_session.append(
         (len(queue.skills), len(queue.archetypes), len(queue.uncovered_skills))
      )
      self.session_choices = []

   def wrap_apply_observation(self, original):
      def apply_observation(states, graph, observation, today, *args, **options):
         if self.mastered is None:
            self.mastered = {skill_id for skill_id, state in states.items() if state.mastered}

         for skill_id in observation.skills:
            self.loaded_counts[skill_id] += 1

         self.metrics.items += 1
         self.metrics.simulated_minutes_total += whole_graph.ATTEMPT_MINUTES
         result = original(states, graph, observation, today, *args, **options)

         for skill_id, state in states.items():
            is_newly_mastered = state.mastered and skill_id not in self.mastered

            if is_newly_mastered:
               self.mastered.add(skill_id)
               self.metrics.items_before_mastery.append(self.loaded_counts[skill_id])

         return result

      return apply_observation


@contextmanager
def instrumented(metrics):
   instruments = Instruments(metrics)
   patches = [
      (select, "constrained_candidates", instruments.wrap_constrained_candidates),
      (select, "choose_by_due_coverage", instruments.wrap_choose_by_due_coverage),
      (build, "next_item_learning", instruments.wrap_next_item_learning),
      (learning, "assemble_session", instruments.wrap_assemble_session),
      (learning, "apply_observation", instruments.wrap_apply_observation),
   ]
   saved = [(module, name, getattr(module, name)) for module, name, _ in patches]

   for module, name, wrap in patches:
      setattr(module, name, wrap(getattr(module, name)))

   try:
      yield instruments
   finally:
      for module, name, original in reversed(saved):
         setattr(module, name, original)


def measure_student(arm_name, seed, days, curve, world_name="fixed", keep_trace=False):
   metrics = TodayMetrics(arm=arm_name, seed=seed, days=days, curve=curve, world=world_name)

   with instrumented(metrics):
      run = learning.run_student(
         selection_study.ALL_ARMS[arm_name],
         seed,
         days,
         curve,
         keep_trace=keep_trace,
         world_rules=selection_study.WORLDS[world_name],
      )

   metrics.trace = run.trace

   return metrics
