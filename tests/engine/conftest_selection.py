"""Fixture helpers for tests/engine/test_selection.py.

Imported explicitly rather than named conftest.py, because tests/engine/conftest.py belongs to
another module in this phase.
"""
import json
from datetime import datetime
from pathlib import Path

from app.engine.fringe import DictItemBank, Graph
from app.engine.state import FadingStage, SkillState

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "graph_p1.json"
LIVE_SKILLS_PATH = Path(__file__).resolve().parents[2] / "data" / "skills.json"
ACCOUNT_CREATED_AT = datetime(2026, 1, 1, 9, 0, 0)


def load_fixture():
   return json.loads(FIXTURE_PATH.read_text())


def build_graph(fixture, with_co_requisite=True):
   edges = [
      edge
      for edge in fixture["edges"]
      if with_co_requisite or edge["type"] != "co_requisite"
   ]

   return Graph.from_records(
      archetypes=fixture["archetypes"],
      skills=fixture["skills"],
      edges=edges,
      inert_top=fixture["inert_top"],
   )


def seeded_parent_ids(fixture):
   return [record["id"] for record in fixture["seeded_parents"]]


def build_states(fixture, mastered=frozenset()):
   states = {}

   for record in fixture["skills"]:
      skill_id = record["id"]
      state = SkillState(skill_id)
      state.mastered = skill_id in mastered

      if state.mastered:
         state.mastered_at = ACCOUNT_CREATED_AT

      states[skill_id] = state

   for parent_id in seeded_parent_ids(fixture):
      states[parent_id] = SkillState.seeded_mastered(parent_id, ACCOUNT_CREATED_AT)

   return states


def build_bank(fixture, draft_only=frozenset(), items_per_archetype=3):
   items = []

   for record in fixture["archetypes"]:
      archetype_id = record["id"]
      is_draft = archetype_id in draft_only
      status = "draft" if is_draft else "verified"

      for index in range(items_per_archetype):
         items.append({
            "id": f"{archetype_id}-V{index:02d}",
            "archetype_id": archetype_id,
            "status": status,
         })

   return DictItemBank(items)


def live_state_rows():
   """The 618 skills_state rows of R27, 541 BC-SKL plus 77 BC-PRQ, read out of data/ and never written."""
   registry = json.loads(LIVE_SKILLS_PATH.read_text())
   skills = [record["id"] for record in registry["skills"]]
   prerequisites = [record["id"] for record in registry["prerequisites"]]

   return skills + prerequisites


def build_live_states(rng, mastered_probability=0.5, mastered_c=0.0):
   """One row per live id, mastery drawn independently per row, as test 21 specifies."""
   states = {}

   for skill_id in live_state_rows():
      state = SkillState(skill_id)
      state.mastered = rng.random() < mastered_probability

      if state.mastered:
         state.mastered_at = ACCOUNT_CREATED_AT
         state.c = mastered_c
         state.fading_stage = FadingStage.UNSUPPORTED
         state.unaided_success_count = 1

      states[skill_id] = state

   return states