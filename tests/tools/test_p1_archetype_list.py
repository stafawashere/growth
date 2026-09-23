"""The 13 P1 archetype ids are typed in three places and checked against the plan in none.

tools/build_p1_fixture.py, tests/e2e/test_session_login_to_feedback.py and the item fixtures all
carry the list, and a test that reads one of those copies is checking a hand-copied list against
another hand-copied list. Scope item 2 of docs/plan/11-phased-delivery.md is the source, so every
copy is compared against the plan text itself.
"""
import ast
import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

PLAN_PATH = REPOSITORY_ROOT / "docs" / "plan" / "11-phased-delivery.md"

ARCHETYPE_ID = re.compile(r"\bBC-QA-\d{5}\b")


def plan_archetype_ids():
   """The ids in 11's P1 scope list, which are the bullet lines naming an archetype and its
   description, taken before the "Out of scope" heading so no later phase leaks in.
   """
   text = PLAN_PATH.read_text()
   p1_section = text.split("## P2 ")[0]
   bullets = [
      line for line in p1_section.splitlines() if line.strip().startswith("- BC-QA-")
   ]

   return {ARCHETYPE_ID.search(line).group(0) for line in bullets}


def tuple_literal_from(path, name):
   module = ast.parse(path.read_text())

   for node in ast.walk(module):
      is_assignment = isinstance(node, ast.Assign)

      if not is_assignment:
         continue

      names = [target.id for target in node.targets if isinstance(target, ast.Name)]

      if name in names:
         return set(ast.literal_eval(node.value))

   raise AssertionError(f"{name} is not assigned in {path}")


def test_the_plan_names_thirteen_p1_archetypes():
   ids = plan_archetype_ids()

   assert len(ids) == 13, f"11's P1 scope names {len(ids)} archetypes, not 13: {sorted(ids)}"


def test_the_fixture_builder_list_is_the_plans_list():
   built = tuple_literal_from(REPOSITORY_ROOT / "tools" / "build_p1_fixture.py", "P1_ARCHETYPES")

   assert built == plan_archetype_ids()


def test_the_end_to_end_gate_list_is_the_plans_list():
   gate_list = tuple_literal_from(
      REPOSITORY_ROOT / "tests" / "e2e" / "test_session_login_to_feedback.py", "P1_ARCHETYPES"
   )

   assert gate_list == plan_archetype_ids()


def test_every_fixture_item_names_an_archetype_the_plan_lists():
   import json

   fixture_dir = REPOSITORY_ROOT / "tests" / "fixtures" / "items_p1"
   ids = plan_archetype_ids()

   for path in sorted(fixture_dir.glob("*.json")):
      record = json.loads(path.read_text())

      assert record["archetype_id"] in ids, f"{path.name} names {record['archetype_id']}"
