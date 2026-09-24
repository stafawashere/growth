"""The three P2 evaluations of docs/plan/11 P2, "Tests that gate the phase", over app/sim/whole_graph.

The suite runs each at a small size through tests/eval/test_p2_evals.py; tools/p2_evals.py runs
them at the recorded size and writes docs/operator/p2-evals.md, the record the P7 gate reads.
Every number is a simulation's measurement on synthetic students, not a human's and not a real
student's.
"""
import random
import statistics
from dataclasses import dataclass

from app.engine import constants, diagnostic
from app.sim import five_term, whole_graph

SEED_BASE = 20260924


def total_variation(before, after):
   return sum(
      0.5 * sum(abs(left - right) for left, right in zip(before[unit], after[unit]))
      for unit in before
   )


@dataclass(frozen=True)
class DiagnosticInformation:
   students: int
   mean_movement_items_1_to_10: float
   mean_movement_after_item_10: float
   early_stop_share: float
   early_stops_after_an_entropy_rise: int
   early_stops: int
   longest_run: int
   median_run: float
   held_out_count: int
   held_out_mean_predicted: float
   held_out_observed_rate: float
   placed_skills: int
   placed_skills_truly_known: int


def diagnostic_information(students, seed_base=SEED_BASE):
   world = whole_graph.library()
   bank = whole_graph.synthetic_bank(world.graph)
   early_movements = []
   late_movements = []
   lengths = []
   early_stops = 0
   rise_stops = 0
   held_out = []
   placed = 0
   placed_known = 0

   for index in range(students):
      seed = seed_base + index
      student = whole_graph.make_student(f"information-{index}", random.Random(seed))
      outcome = whole_graph.run_diagnostic(student, bank, seed=seed)
      run = outcome.run
      measures = outcome.measures

      for position in range(1, len(measures)):
         movement = total_variation(measures[position - 1], measures[position])
         is_early = position <= constants.DIAG_MIN

         if is_early:
            early_movements.append(movement)
         else:
            late_movements.append(movement)

      lengths.append(len(run.asked))
      stopped_on_entropy = run.stop_reason == diagnostic.STOP_ENTROPY

      if stopped_on_entropy:
         early_stops += 1
         trace = run.entropy_trace
         last_steps = [trace[step] - trace[step + 1] for step in range(len(trace) - 4, len(trace) - 1)]
         rise_stops += any(step < 0 for step in last_steps)

      for entry in run.asked:
         if entry["held_out"]:
            held_out.append((entry["p_raw"], entry["outcome"] == diagnostic.OUTCOME_CORRECT))

      for skill_id in run.placement["newly_mastered"]:
         placed += 1
         placed_known += bool(student.true_state.get(skill_id))

   return DiagnosticInformation(
      students=students,
      mean_movement_items_1_to_10=statistics.mean(early_movements),
      mean_movement_after_item_10=statistics.mean(late_movements) if late_movements else 0.0,
      early_stop_share=early_stops / students,
      early_stops_after_an_entropy_rise=rise_stops,
      early_stops=early_stops,
      longest_run=max(lengths),
      median_run=statistics.median(lengths),
      held_out_count=len(held_out),
      held_out_mean_predicted=statistics.mean(predicted for predicted, _ in held_out),
      held_out_observed_rate=statistics.mean(1.0 if correct else 0.0 for _, correct in held_out),
      placed_skills=placed,
      placed_skills_truly_known=placed_known,
   )


@dataclass(frozen=True)
class ArmResult:
   arm: str
   sessions: int
   items: int
   declared_mastered: int
   truly_mastered: int
   mean_predicted: float
   observed_rate: float

   @property
   def true_mastery_per_item(self):
      return self.truly_mastered / self.items if self.items else 0.0

   @property
   def measurement_bias(self):
      """Mean predicted p_A_knowledge minus the observed success rate over served items: the
      feedback-loop bias 10 asks the control arm to expose."""
      return self.mean_predicted - self.observed_rate


def run_arm(arm, students, days, seed_base, ordering=None):
   world = whole_graph.library()
   graph = world.graph
   bank = whole_graph.synthetic_bank(graph)
   sessions = 0
   items = 0
   declared = 0
   truly = 0
   predicted = []
   observed = []

   for index in range(students):
      seed = seed_base + index
      student = whole_graph.make_student(f"arm-{index}", random.Random(seed))
      placed = whole_graph.run_diagnostic(student, bank, seed=seed)
      history, states, world_model, served = whole_graph.run_days(
         student,
         bank,
         seed=seed,
         days=days,
         states=placed.states,
         arm="control" if arm == "control" else "policy",
         ordering=ordering,
      )
      sessions += len(history)
      items += served
      mastered, known = whole_graph.true_known_mastered(states, world_model, graph)
      declared += len(mastered)
      truly += len(known)

      for day_record in history:
         for probability, correct in day_record.predictions:
            predicted.append(probability)
            observed.append(1.0 if correct else 0.0)

   return ArmResult(
      arm=arm,
      sessions=sessions,
      items=items,
      declared_mastered=declared,
      truly_mastered=truly,
      mean_predicted=statistics.mean(predicted) if predicted else 0.0,
      observed_rate=statistics.mean(observed) if observed else 0.0,
   )


def selection_bias_control(students, days, seed_base=SEED_BASE):
   return run_arm("policy", students, days, seed_base), run_arm("control", students, days, seed_base)


def two_term_against_five_term(students, days, seed_base=SEED_BASE):
   two_term = run_arm("two_term", students, days, seed_base)
   five = run_arm("five_term", students, days, seed_base, ordering=five_term.five_term_ordering)

   return two_term, five
