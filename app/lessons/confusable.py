"""Confusable skill sets for decision lessons: docs/plan/15-lessons.md, Methods, decision lessons.

The sets are the connected components of the graph of confusable_with references between active
BC-SKL records, kept only when every member sits in one unit and the component holds two to
DECISION_SET_MAX skills.
"""
from collections import defaultdict

from app.lessons import constants


def confusable_graph(snapshot):
   """Undirected adjacency over active skills. A reference that leaves the unit is not an edge,
   so a component can never span units."""
   adjacency = defaultdict(set)

   for skill_id, skill in snapshot.skills.items():
      for other_id in skill.get("confusable_with") or []:
         other = snapshot.skills.get(other_id)
         is_active = other is not None
         is_same_unit = is_active and other["unit"] == skill["unit"]
         is_self = other_id == skill_id

         if is_same_unit and not is_self:
            adjacency[skill_id].add(other_id)
            adjacency[other_id].add(skill_id)

   return adjacency


def components(adjacency):
   seen = set()
   found = []

   for start in sorted(adjacency):
      already_placed = start in seen

      if already_placed:
         continue

      members = set()
      stack = [start]

      while stack:
         skill_id = stack.pop()

         if skill_id in members:
            continue

         members.add(skill_id)
         stack.extend(adjacency[skill_id] - members)

      seen |= members
      found.append(tuple(sorted(members)))

   return found


def confusable_sets(snapshot, set_max=constants.DECISION_SET_MAX):
   adjacency = confusable_graph(snapshot)
   candidates = components(adjacency)
   sized = [members for members in candidates if 2 <= len(members) <= set_max]

   return sorted(sized)
