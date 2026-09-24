"""The selection graph and the update graph over one loaded snapshot, shared by the runtime
context and the whole-graph simulation so the two never build the library differently.
"""
from app.engine.fringe import Graph
from app.engine.interleave import conversion_pairs_from
from app.engine.update import EngineGraph


def _archetype_counts(archetypes):
   counts = {}

   for record in archetypes.values():
      for skill_id in record["skills"]:
         counts[skill_id] = counts.get(skill_id, 0) + 1

   return counts


def graphs_from_snapshot(snapshot):
   graph = Graph.from_records(
      archetypes=list(snapshot.archetypes.values()),
      skills=list(snapshot.skills.values()),
      edges=list(snapshot.edges),
      inert_top=snapshot.inert_top_ids,
      conversion_pairs=conversion_pairs_from(snapshot.representations.values()),
   )
   engine_graph = EngineGraph(
      hard_parents=snapshot.hard_parents,
      supporting_parents=snapshot.supporting_parents,
      hard_children=snapshot.hard_children,
      archetype_counts=_archetype_counts(snapshot.archetypes),
   )

   return graph, engine_graph
