"""A student who places into nothing starts at the front of the course.

docs/plan/02-adaptive-engine.md "Prerequisite gating and the outer fringe": the fringe is every
unmastered skill whose blocking parents are all mastered. A skill outside Unit 1 with no blocking
hard parent is open on day one to a student who knows no calculus, which is how polar dr/dtheta
reached a new account's first set on 2026-09-28.
"""
from app.engine.fringe import outer_fringe
from app.engine.update import required_distinct_archetypes
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


def test_every_teachable_skill_can_meet_the_distinct_archetype_condition():
   """Mastery condition 3 asks for successes on as many archetypes as the update graph counts for
   the skill, up to 2. An archetype whose primary skill is gated behind the skill cannot be served
   before the skill is mastered, so counting it asks for a success that cannot happen: on
   2026-09-29 BC-SKL-02005 needed BC-QA-02003, gated behind 02006, which is gated behind 02005.
   Crediting a skill only once enough servable archetypes load it must still reach every skill."""
   world = whole_graph.library()
   graph = world.graph
   counts = world.engine_graph.archetype_counts
   teachable = {skill_id for skill_id in graph.skills if graph.has_archetype(skill_id)}
   mastered = set()

   while True:
      servable = [
         record
         for record in graph.archetypes.values()
         if all(parent in mastered for parent in graph.blocking_parents(graph.primary_skill(record["id"])))
      ]
      servable_count = {}

      for record in servable:
         for skill_id in record["skills"]:
            servable_count[skill_id] = servable_count.get(skill_id, 0) + 1

      newly_mastered = {
         skill_id
         for skill_id in teachable - mastered
         if servable_count.get(skill_id, 0) >= required_distinct_archetypes(counts.get(skill_id))
      }

      if not newly_mastered:
         break

      mastered |= newly_mastered

   assert mastered, "nothing was mastered, so the walk did not run"
   assert sorted(teachable - mastered) == []


def test_condition_three_counts_the_archetypes_servable_today():
   """Corrected 2026-09-29, second: the denominator is the archetypes the student can be served
   now, so a skill whose second archetype waits behind another unit's chain is not held with it.
   BC-SKL-03002 waited 150 days for BC-QA-99001, a Unit 9 synthesis archetype, and 37 skills
   waited behind it."""
   world = whole_graph.library()
   graph = world.graph
   engine_graph = world.engine_graph
   skill = "BC-SKL-03002"
   states = whole_graph.fresh_states()
   entries = engine_graph.archetype_primaries[skill]

   assert len(entries) == 2
   assert engine_graph.archetype_counts[skill] == 2

   own = [primary for _, primary in entries if primary == skill]
   other = [primary for _, primary in entries if primary != skill]

   assert len(own) == 1 and len(other) == 1
   assert engine_graph.servable_archetype_count(skill, states) == 0

   for parent in graph.blocking_parents(skill):
      states[parent].mastered = True

   assert engine_graph.servable_archetype_count(skill, states) == 1
   assert required_distinct_archetypes(engine_graph.servable_archetype_count(skill, states)) == 1

   for parent in graph.blocking_parents(other[0]):
      states[parent].mastered = True

   assert engine_graph.servable_archetype_count(skill, states) == 2
   assert required_distinct_archetypes(engine_graph.servable_archetype_count(skill, states)) == 2
