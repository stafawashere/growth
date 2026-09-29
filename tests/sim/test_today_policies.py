"""The Today candidate policies of app/sim/today_policies.py, and the block 3 hook the running app
never passes."""
import random
from datetime import date
from pathlib import Path

from app.engine.fringe import Graph
from app.engine.state import SkillState
from app.sim import learning, p7_evals, today_policies

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TODAY = date(2026, 10, 1)
SHUFFLE_SEEDS = range(20)


def archetype(archetype_id, skills, family="FAM-1", unit="U01"):
   return {
      "id": archetype_id,
      "skills": skills,
      "family": family,
      "primary_unit": unit,
      "difficulty_factors": [],
   }


def small_graph():
   archetypes = [
      archetype("A-DECAYED", ["S1"]),
      archetype("A-FRESH", ["S2", "S3"]),
   ]
   skills = [{"id": skill_id} for skill_id in ("S1", "S2", "S3")]

   return Graph.from_records(archetypes, skills, [], inert_top=())


def remembered_states():
   return {
      skill_id: SkillState(skill_id=skill_id, stability=10.0, last_practised_at=TODAY)
      for skill_id in ("S1", "S2", "S3")
   }


def ordered_ids(ordering, graph, states, retrievability, seed, history=()):
   records = list(graph.archetypes.values())
   ordered = ordering(records, states, graph, TODAY, retrievability, random.Random(seed), list(history))

   return [record["id"] for record in ordered]


def test_retrievability_priority_serves_the_decayed_reach_first():
   graph = small_graph()
   states = remembered_states()
   retrievability = {"S1": 0.4, "S2": 1.0, "S3": 1.0}

   for seed in SHUFFLE_SEEDS:
      order = ordered_ids(
         today_policies.retrievability_priority_ordering, graph, states, retrievability, seed
      )

      assert order == ["A-DECAYED", "A-FRESH"]


def test_the_elo_observer_moves_a_family_rating_with_the_outcome():
   graph = small_graph()
   states = remembered_states()
   elo = today_policies.EloTarget()
   record = graph.archetypes["A-FRESH"]
   elo.ordering(list(graph.archetypes.values()), states, graph, TODAY, {}, random.Random(1), [])

   elo.observe(record, True, TODAY)
   after_correct = elo.ratings["FAM-1"]

   assert after_correct > 0.0

   elo.observe(record, False, TODAY)

   assert elo.ratings["FAM-1"] < after_correct


def test_spread_serves_the_just_practised_skill_last():
   graph = small_graph()
   states = remembered_states()
   history = [{"archetype_id": "A-DECAYED"}]

   for seed in SHUFFLE_SEEDS:
      order = ordered_ids(today_policies.spread_ordering, graph, states, {}, seed, history)

      assert order[-1] == "A-DECAYED"


def daily_blocks(arm, monkeypatch, days=10):
   """Per day, the block 2 item ids and the block 3 item ids the arm served."""
   served = []
   original = learning.assemble_session

   def capturing(*args, **options):
      session = original(*args, **options)
      block2 = [entry["id"] for entry in session.block2 if entry.get("kind") == "item"]
      block3 = [entry["id"] for entry in session.block3]
      served.append((block2, block3))

      return session

   monkeypatch.setattr(learning, "assemble_session", capturing)
   learning.run_student(arm, p7_evals.SEED_BASE, days)
   monkeypatch.setattr(learning, "assemble_session", original)

   return served


def test_review_first_keeps_block_2_and_changes_block_3(monkeypatch):
   """Block 2 runs before block 3 each day, so block 2 must match two-term through the first day
   block 3 differs; after it the answers differ and so do the states both blocks read."""
   two_term = daily_blocks(learning.ARMS["two_term"], monkeypatch)
   review_first = daily_blocks(today_policies.TODAY_ARMS["review_first"], monkeypatch)
   block3_differs = [
      day for day, (first, second) in enumerate(zip(two_term, review_first)) if first[1] != second[1]
   ]

   assert len(block3_differs) > 0

   through_first_difference = block3_differs[0] + 1

   for day in range(through_first_difference):
      assert len(two_term[day][0]) > 0
      assert review_first[day][0] == two_term[day][0]


def test_the_running_app_passes_no_retrieval_ordering():
   for relative in ("app/session/service.py", "app/session/preview.py"):
      source = (REPOSITORY_ROOT / relative).read_text()

      assert "assemble_session" in source
      assert "retrieval_ordering" not in source
