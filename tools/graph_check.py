"""Structural report on the prerequisite graph: cycles, roots, leaves, unit dependencies."""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGES = ROOT / "data" / "prereq_edges.csv"
SKILLS = ROOT / "data" / "skills.json"


def unit_of(identifier):
   is_skill = identifier.startswith("BC-SKL-") or identifier.startswith("BC-CON-")

   if is_skill:
      return "BC-UNIT-" + identifier.split("-")[2][:2]

   is_topic = identifier.startswith("BC-TOP-")

   if is_topic:
      return "BC-UNIT-" + identifier.split("-")[2][:2]

   return None


def load_edges():
   with EDGES.open() as handle:
      return [row for row in csv.DictReader(handle)]


def find_cycles(adjacency):
   colour = {}
   stack = []
   cycles = []

   def walk(node):
      colour[node] = "grey"
      stack.append(node)

      for neighbour in adjacency.get(node, ()):
         state = colour.get(neighbour, "white")

         if state == "white":
            walk(neighbour)
         elif state == "grey":
            start = stack.index(neighbour)
            cycles.append(stack[start:] + [neighbour])

      stack.pop()
      colour[node] = "black"

   for node in sorted(adjacency):
      is_unvisited = colour.get(node, "white") == "white"

      if is_unvisited:
         walk(node)

   return cycles


def main():
   edges = load_edges()
   registry = json.loads(SKILLS.read_text())
   skill_ids = {skill["id"] for skill in registry["skills"]}

   hard = [row for row in edges if row["type"] == "hard_prerequisite"]
   adjacency = defaultdict(set)
   incoming = defaultdict(set)

   for row in hard:
      adjacency[row["from"]].add(row["to"])
      incoming[row["to"]].add(row["from"])

   cycles = find_cycles(adjacency)

   print("edges", len(edges), "hard", len(hard))
   print("cycles", len(cycles))

   for cycle in cycles:
      print("  cycle", " -> ".join(cycle))

   roots = sorted(identifier for identifier in skill_ids if not incoming.get(identifier))
   leaves = sorted(identifier for identifier in skill_ids if not adjacency.get(identifier))
   print("root skills", len(roots))
   print("leaf skills", len(leaves))

   depends_on = defaultdict(set)

   for row in edges:
      source_unit = unit_of(row["from"])
      target_unit = unit_of(row["to"])
      is_cross_unit = source_unit and target_unit and source_unit != target_unit

      if is_cross_unit:
         depends_on[target_unit].add(source_unit)

   units = sorted({f"BC-UNIT-{index:02d}" for index in range(1, 11)})
   print("unit dependencies")

   for unit in units:
      upstream = sorted(depends_on.get(unit, ()))
      downstream = sorted(other for other in units if unit in depends_on.get(other, ()))
      print(f"  {unit} depends on {','.join(upstream) or 'none'} | feeds {','.join(downstream) or 'none'}")

   fan_out = sorted(((len(adjacency.get(identifier, ())), identifier) for identifier in skill_ids), reverse=True)
   print("highest fan-out")

   for count, identifier in fan_out[:15]:
      print(f"  {identifier} {count}")


if __name__ == "__main__":
   main()
