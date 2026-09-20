import json
from datetime import datetime
from pathlib import Path

import pytest

from app.engine.state import SkillState
from app.engine.update import EngineGraph

FIXTURE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "graph_p1.json"
CREATED_AT = datetime(2026, 9, 1, 9, 0, 0)


@pytest.fixture(scope="session")
def graph_p1():
   with FIXTURE_PATH.open() as handle:
      return json.load(handle)


@pytest.fixture
def archetypes(graph_p1):
   return {record["id"]: record for record in graph_p1["archetypes"]}


@pytest.fixture
def graph(graph_p1):
   """hard_parents, supporting_parents and hard_children over the P1 edges.

   BC-TOP endpoints and co_requisite edges are inert (R13, R30) and are dropped here.
   """
   inert = set(graph_p1["inert_top"])
   hard_parents = {}
   supporting_parents = {}
   hard_children = {}

   for edge in graph_p1["edges"]:
      parent = edge["from"]
      child = edge["to"]
      touches_inert = parent in inert or child in inert
      is_co_requisite = edge["type"] == "co_requisite"
      is_skipped = touches_inert or is_co_requisite

      if is_skipped:
         continue

      is_hard = edge["type"] == "hard_prerequisite"

      if is_hard:
         hard_parents.setdefault(child, set()).add(parent)
         hard_children.setdefault(parent, set()).add(child)
      else:
         supporting_parents.setdefault(child, set()).add(parent)

   return EngineGraph(
      hard_parents=hard_parents,
      supporting_parents=supporting_parents,
      hard_children=hard_children,
   )


@pytest.fixture
def states(graph_p1):
   built = {}

   for record in graph_p1["skills"]:
      built[record["id"]] = SkillState(skill_id=record["id"], beta=0.0)

   for record in graph_p1["seeded_parents"]:
      built[record["id"]] = SkillState.seeded_mastered(record["id"], CREATED_AT)

   return built
