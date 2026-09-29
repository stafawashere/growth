"""The P7 simulation of docs/plan/11 P7, run small. tools/p7_evals.py runs it at the recorded size
and writes docs/operator/p7-evals.md, whose decisions the live policy must match."""
import ast
import math
import random
from datetime import timedelta
from pathlib import Path

import pytest

from app.engine import constants, fringe, select
from app.sim import learning, p7_evals, whole_graph

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
RECORD_PATH = REPOSITORY_ROOT / "docs" / "operator" / "p7-evals.md"

STUDENTS = 4
DAYS = 12


def test_simulation_reproducible():
   first = learning.run_student(learning.ARMS["two_term"], 424242, DAYS, keep_trace=True)
   again = learning.run_student(learning.ARMS["two_term"], 424242, DAYS, keep_trace=True)
   other = learning.run_student(learning.ARMS["two_term"], 424243, DAYS, keep_trace=True)

   assert len(first.trace) > 0
   assert first.trace == again.trace
   assert first == again
   assert first.trace != other.trace


def test_the_world_stays_closed_under_hard_prerequisites_while_it_learns():
   library = whole_graph.library()
   student = learning.make_learning_student("closure", 77)
   world = learning.LearningWorld(student, library.engine_graph.hard_parents, random.Random(5))
   learnable = sorted(
      skill_id
      for skill_id in library.graph.skills
      if not world.knows(skill_id)
   )

   for _ in range(40):
      world.learn(learnable, learning.FadingStage.EXAMPLE, whole_graph.START_DAY)

   assert len(world.learned) > 0

   for skill_id in library.graph.skills:
      if not world.knows(skill_id):
         continue

      parents = library.engine_graph.hard_parents.get(skill_id, ())
      assert all(world.knows(parent) for parent in parents), skill_id


def lapsed_world(rules):
   library = whole_graph.library()
   student = learning.make_learning_student("lapsed", 78)
   record = next(iter(library.graph.archetypes.values()))
   world = learning.LearningWorld(
      student,
      library.engine_graph.hard_parents,
      random.Random(9),
      rules=rules,
      seed=9,
      start_day=whole_graph.START_DAY,
   )
   long_ago = whole_graph.START_DAY - timedelta(days=4000)

   for skill_id in record["skills"]:
      student.known[skill_id] = True
      world.half_life[skill_id] = 17.0
      world.last_success[skill_id] = long_ago

   return world, record, long_ago


def test_feedback_relearns_a_lapsed_skill_one_growth_step_down():
   """A known skill the student could not retrieve is re-anchored today with one growth step of
   its half-life undone, never below the initial half-life; the legacy world leaves it decaying."""
   today = whole_graph.START_DAY
   world, record, long_ago = lapsed_world(learning.WORLD)
   is_correct = world.answer(record, "short_answer", learning.FadingStage.UNSUPPORTED, today)

   assert is_correct is False

   for skill_id in record["skills"]:
      assert world.last_success[skill_id] == today
      assert world.half_life[skill_id] == pytest.approx(10.0)

   world.half_life[record["skills"][0]] = 6.0
   world.last_success[record["skills"][0]] = long_ago
   world.answer(record, "short_answer", learning.FadingStage.UNSUPPORTED, today + timedelta(days=1))

   assert world.half_life[record["skills"][0]] == learning.INITIAL_HALF_LIFE_DAYS

   legacy, record, long_ago = lapsed_world(learning.LEGACY_WORLD)
   legacy.answer(record, "short_answer", learning.FadingStage.UNSUPPORTED, today)

   for skill_id in record["skills"]:
      assert legacy.last_success[skill_id] == long_ago
      assert legacy.half_life[skill_id] == 17.0


def test_an_arm_restores_the_engine_it_patched():
   before = (constants.LAMBDA, constants.STAGE_HIGH, fringe.p_knowledge, select.p_knowledge)

   with learning.arm_engine(learning.ARMS["decay_lambda_2"]):
      assert constants.LAMBDA == 2.0

   with learning.arm_engine(learning.ARMS["compensatory_only"]):
      assert fringe.p_knowledge is not before[2]

   with learning.arm_engine(learning.ARMS["stage_high_0_7"]):
      assert constants.STAGE_HIGH == 0.70

   after = (constants.LAMBDA, constants.STAGE_HIGH, fringe.p_knowledge, select.p_knowledge)

   assert after == before


@pytest.fixture(scope="module")
def arms():
   return p7_evals.run_arms(["two_term", "random_control", "five_term"], STUDENTS, DAYS)


def eval_policy_against_random_control(arms):
   two_term = arms["two_term"]
   control = arms["random_control"]
   share = p7_evals.paired_share(two_term, control, p7_evals.mastery_per_item, strict=False)

   assert [run.seed for run in two_term] == [run.seed for run in control]
   assert 0.0 <= share <= 1.0
   assert all(math.isfinite(run.measurement_bias) for run in two_term + control)
   assert sum(run.items for run in control) > 0


def eval_five_term_against_two_term(arms):
   share = p7_evals.paired_share(arms["five_term"], arms["two_term"], p7_evals.mastery_per_item)

   assert 0.0 <= share <= 1.0
   five_outcomes = [(run.items, run.learned, run.taught_retained) for run in arms["five_term"]]
   two_outcomes = [(run.items, run.learned, run.taught_retained) for run in arms["two_term"]]
   assert five_outcomes != two_outcomes


def imports_five_term(path):
   tree = ast.parse(path.read_text())

   for node in ast.walk(tree):
      is_from = isinstance(node, ast.ImportFrom)
      is_plain = isinstance(node, ast.Import)

      if is_from and node.module and "five_term" in node.module:
         return True

      if is_from and any(alias.name == "five_term" for alias in node.names):
         return True

      if is_plain and any("five_term" in alias.name for alias in node.names):
         return True

   return False


def test_the_live_policy_matches_the_recorded_five_term_decision():
   record = RECORD_PATH.read_text()
   stays_off = "`EXPLORE_SHARE`: stays off." in record
   turned_on = "`EXPLORE_SHARE`: turned on." in record

   assert stays_off != turned_on
   assert f"seed base {p7_evals.SEED_BASE}" in record

   live_modules = sorted((REPOSITORY_ROOT / "app" / "engine").glob("*.py"))
   live_modules += sorted((REPOSITORY_ROOT / "app" / "session").glob("*.py"))
   live_reads_five_term = any(imports_five_term(path) for path in live_modules)

   assert live_reads_five_term == turned_on


def test_the_live_decay_term_matches_the_recorded_decision():
   record = RECORD_PATH.read_text()
   returns = "- `lambda`: returns to 2.0." in record
   stays = "- `lambda`: stays 0." in record

   assert returns != stays
   assert constants.LAMBDA == (2.0 if returns else 0.0)


def eval_false_mastery_within_ceiling():
   """10's ceiling on declared mastery the student does not have, over every source of a
   declaration: the account's seeded rows, the diagnostic's placement and practice."""
   by_arm = p7_evals.run_arms(["two_term", "random_control"], 20, 20, seed_base=p7_evals.SEED_BASE)

   for arm_name, runs in by_arm.items():
      summary = p7_evals.summarise(runs)

      assert summary.declared_mastered >= 20, arm_name
      assert summary.false_mastery_share <= p7_evals.FALSE_MASTERY_CEILING, (
         arm_name,
         summary.declared_not_known,
         summary.declared_mastered,
      )


def a_run(arm, seed, mastery):
   return learning.StudentRun(
      student=f"s{seed}",
      seed=seed,
      arm=arm,
      curve=learning.EXPONENTIAL,
      items=100,
      known_at_start=0,
      learned=10,
      taught_retained=mastery * 100,
      taught_retained_day_30=mastery * 50,
      declared_mastered=10,
      declared_not_known=0,
      placed_mastered=0,
      placed_not_known=0,
      retention_day_7=0.5,
      retention_day_30=0.5,
      measurement_bias=0.0,
   )


def test_the_bars_are_decided_by_the_mean_interval_not_the_share():
   """The operator's ruling of 2026-09-27: a challenger ahead on the mean with an interval above 0
   is turned on even when it wins on fewer than 90 percent of students, and two-term behind the
   control on most students but ahead on the mean still clears the floor."""
   seeds = range(200)
   baseline = [a_run("two_term", seed, 0.010) for seed in seeds]
   five = [a_run("five_term", seed, 0.012 if seed % 5 < 3 else 0.0095) for seed in seeds]
   control = [a_run("random_control", seed, 0.009 if seed % 5 < 2 else 0.0102) for seed in seeds]
   same = [a_run(arm, seed, 0.010) for seed in seeds for arm in ("decay_lambda_2",)]
   no_interleaving = [a_run("no_interleaving", seed, 0.010) for seed in seeds]
   decisions = p7_evals.decide({
      "two_term": baseline,
      "random_control": control,
      "five_term": five,
      "decay_lambda_2": same,
      "no_interleaving": no_interleaving,
   })

   assert decisions.five_term_beats_two_term_share < p7_evals.PAIRED_BAR
   assert decisions.five_term_on
   assert decisions.policy_at_least_random_share < p7_evals.PAIRED_BAR
   assert decisions.policy_beats_random
   assert not decisions.lambda_returns
   assert not decisions.interleaving_costs_retention
