"""The P7 simulation of docs/plan/11 P7, run small. tools/p7_evals.py runs it at the recorded size
and writes docs/operator/p7-evals.md, whose decisions the live policy must match."""
import ast
import math
import random
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
