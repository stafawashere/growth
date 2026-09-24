"""The mastery map's node states and order (08, "Progress" and the Information architecture)."""
import json
from datetime import date, datetime

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine.fringe import Graph
from app.engine.state import SkillState
from app.progress import mastery

TODAY = date(2026, 3, 1)
STAMP = "2026-02-27T09:00:00+00:00"


def skill(skill_id, unit="BC-UNIT-02"):
   return {"id": skill_id, "unit": unit, "name": f"name of {skill_id}"}


def graph_of(skills, edges=()):
   return Graph.from_records(
      archetypes=[],
      skills=skills,
      edges=[{"from": parent, "to": child, "type": "hard_prerequisite"} for parent, child in edges],
      inert_top=(),
   )


def fresh_mastered(skill_id):
   return SkillState(
      skill_id=skill_id,
      mastered=True,
      stability=400.0,
      difficulty=5.0,
      last_practised_at=datetime(2026, 2, 28),
      observation_count=6,
      success_days={date(2026, 2, 20), date(2026, 2, 25)},
   )


def decayed_mastered(skill_id):
   return SkillState(
      skill_id=skill_id,
      mastered=True,
      stability=1.0,
      difficulty=5.0,
      last_practised_at=datetime(2026, 1, 1),
      observation_count=6,
      success_days={date(2025, 12, 20)},
   )


def record_gap(engine, skill_id):
   with OrmSession(engine) as db:
      db.add(
         models.Session(
            id="SES-1",
            user_id="USR-1",
            mode="learning",
            started_at=STAMP,
            queue="{}",
            snapshot_id="SNAP-0001",
            created_at=STAMP,
            updated_at=STAMP,
         )
      )
      db.add(
         models.Attempt(
            id="ATT-1",
            session_id="SES-1",
            item_id="ITEM-1",
            started_at=STAMP,
            submitted_at=STAMP,
            correct=0,
            served_stage="unsupported",
            format="short_answer",
            per_skill_states=json.dumps({skill_id: "prerequisite_gap"}),
            snapshot_id="SNAP-0001",
            created_at=STAMP,
            updated_at=STAMP,
         )
      )
      db.commit()


def map_of(engine, states, graph):
   with OrmSession(engine) as db:
      return mastery.mastery_map(db, "USR-1", states, graph, TODAY)


def nodes_by_id(payload):
   return {node["skill_id"]: node for unit in payload["units"] for node in unit["nodes"]}


def test_each_skill_takes_the_one_state_its_engine_record_implies(tmp_path):
   engine = models.make_engine(tmp_path / "map.db")
   graph = graph_of([skill(name) for name in ("S-FRESH", "S-DECAYED", "S-TRYING", "S-GAP", "S-UNSEEN")])
   states = {
      "S-FRESH": fresh_mastered("S-FRESH"),
      "S-DECAYED": decayed_mastered("S-DECAYED"),
      "S-TRYING": SkillState(skill_id="S-TRYING", observation_count=2),
      "S-GAP": SkillState(skill_id="S-GAP", observation_count=1),
      "S-UNSEEN": SkillState(skill_id="S-UNSEEN"),
   }
   record_gap(engine, "S-GAP")

   nodes = nodes_by_id(map_of(engine, states, graph))

   assert {skill_id: node["state"] for skill_id, node in nodes.items()} == {
      "S-FRESH": mastery.MASTERED,
      "S-DECAYED": mastery.FADING,
      "S-TRYING": mastery.IN_PROGRESS,
      "S-GAP": mastery.GAP,
      "S-UNSEEN": mastery.NOT_ATTEMPTED,
   }
   assert nodes["S-DECAYED"]["last_success_on"] == "2025-12-20"
   assert nodes["S-DECAYED"]["days_since_success"] == (TODAY - date(2025, 12, 20)).days


def test_a_seeded_mastered_skill_is_mastered_and_marked_assumed(tmp_path):
   engine = models.make_engine(tmp_path / "map.db")
   graph = graph_of([skill("S-SEEDED")])
   states = {"S-SEEDED": SkillState.seeded_mastered("S-SEEDED", datetime(2026, 1, 1))}

   node = nodes_by_id(map_of(engine, states, graph))["S-SEEDED"]

   assert (node["state"], node["assumed"]) == (mastery.MASTERED, True)


def test_units_run_in_number_order_and_a_skill_follows_its_hard_prerequisites(tmp_path):
   engine = models.make_engine(tmp_path / "map.db")
   skills = [
      skill("S-A", "BC-UNIT-10"),
      skill("S-Z-ROOT"),
      skill("S-M-MIDDLE"),
      skill("S-B-LEAF"),
   ]
   edges = [("S-Z-ROOT", "S-M-MIDDLE"), ("S-M-MIDDLE", "S-B-LEAF")]
   states = {record["id"]: SkillState(skill_id=record["id"]) for record in skills}

   payload = map_of(engine, states, graph_of(skills, edges))

   assert [unit["unit_id"] for unit in payload["units"]] == ["BC-UNIT-02", "BC-UNIT-10"]
   assert [node["skill_id"] for node in payload["units"][0]["nodes"]] == ["S-Z-ROOT", "S-M-MIDDLE", "S-B-LEAF"]
   assert payload["units"][0]["name"] == "Differentiation: Definition and Fundamental Properties"


def test_the_map_carries_no_aggregate_figure(tmp_path):
   engine = models.make_engine(tmp_path / "map.db")
   graph = graph_of([skill("S-FRESH")])
   payload = map_of(engine, {"S-FRESH": fresh_mastered("S-FRESH")}, graph)

   assert set(payload) == {"today", "states", "units"}
   assert set(payload["units"][0]) == {"unit_id", "number", "name", "nodes"}
