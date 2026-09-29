"""The selection graph and the update graph over one loaded snapshot, shared by the runtime
context and the whole-graph simulation so the two never build the library differently.
"""
from app.engine.fringe import Graph
from app.engine.interleave import conversion_pairs_from
from app.engine.update import EngineGraph


def _blocking_ancestors(skill_id, graph, memo):
   if skill_id in memo:
      return memo[skill_id]

   ancestors = set()

   for parent in graph.blocking_parents(skill_id):
      ancestors.add(parent)
      ancestors |= _blocking_ancestors(parent, graph, memo)

   memo[skill_id] = frozenset(ancestors)

   return memo[skill_id]


def _archetype_primaries(graph):
   """The archetypes mastery condition 3 may ask a skill to be credited on, each with its primary
   skill: those that list the skill and can be served before it is mastered. An archetype whose
   primary skill is gated behind the skill is left out, since asking for a success there shuts the
   skill and everything under it for good."""
   memo = {}
   primaries = {}

   for record in graph.archetypes.values():
      primary = graph.primary_skill(record["id"])
      gate = _blocking_ancestors(primary, graph, memo)

      for skill_id in record["skills"]:
         is_gated_behind_skill = skill_id in gate

         if is_gated_behind_skill:
            continue

         primaries.setdefault(skill_id, []).append((record["id"], primary))

   return {skill_id: tuple(entries) for skill_id, entries in primaries.items()}


def _archetype_counts(primaries):
   return {skill_id: len(entries) for skill_id, entries in primaries.items()}


def graphs_from_snapshot(snapshot):
   graph = Graph.from_records(
      archetypes=list(snapshot.archetypes.values()),
      skills=list(snapshot.skills.values()),
      edges=list(snapshot.edges),
      inert_top=snapshot.inert_top_ids,
      conversion_pairs=conversion_pairs_from(snapshot.representations.values()),
      concepts=list(snapshot.concepts.values()),
   )
   primaries = _archetype_primaries(graph)
   engine_graph = EngineGraph(
      hard_parents=snapshot.hard_parents,
      supporting_parents=snapshot.supporting_parents,
      hard_children=snapshot.hard_children,
      archetype_counts=_archetype_counts(primaries),
      blocking_parents={skill_id: tuple(graph.blocking_parents(skill_id)) for skill_id in graph.skills},
      archetype_primaries=primaries,
   )

   return graph, engine_graph
