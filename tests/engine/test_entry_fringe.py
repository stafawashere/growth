"""A student who places into nothing starts at the front of the course.

docs/plan/02-adaptive-engine.md "Prerequisite gating and the outer fringe": the fringe is every
unmastered skill whose blocking parents are all mastered. A skill outside Unit 1 with no blocking
hard parent is open on day one to a student who knows no calculus, which is how polar dr/dtheta
reached a new account's first set on 2026-09-28.
"""
from app.engine.fringe import outer_fringe
from app.sim import whole_graph

ENTRY_UNIT = "BC-UNIT-01"


def test_fresh_student_fringe_holds_only_unit_one_skills():
   graph = whole_graph.library().graph
   fringe = outer_fringe(whole_graph.fresh_states(), graph)

   outside_entry_unit = sorted(
      skill_id
      for skill_id in fringe
      if graph.skills[skill_id]["unit"] != ENTRY_UNIT
   )

   assert fringe, "the fresh fringe is empty, so nothing was measured"
   assert outside_entry_unit == []

def test_every_teachable_skill_is_reachable_from_a_fresh_start():
   """A skill that is loaded only by archetypes whose primary skill is gated behind it can never
   be practised, so it never opens. Serving every archetype whose primary skill is open until
   nothing new is credited must reach every skill an archetype loads."""
   graph = whole_graph.library().graph
   teachable = {skill_id for skill_id in graph.skills if graph.has_archetype(skill_id)}
   reached = set()

   while True:
      open_skills = {
         skill_id
         for skill_id in teachable
         if all(parent in reached for parent in graph.blocking_parents(skill_id))
      }
      servable = [
         record
         for record in graph.archetypes.values()
         if graph.primary_skill(record["id"]) in open_skills
      ]
      newly_reached = {
         skill_id
         for record in servable
         for skill_id in record["skills"]
         if skill_id in teachable
      } - reached

      if not newly_reached:
         break

      reached |= newly_reached

   assert reached, "nothing was reached, so the walk did not run"
   assert sorted(teachable - reached) == []
