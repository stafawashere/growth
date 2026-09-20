"""Build tests/fixtures/graph_p1.json from the registries under data/.

The fixture is the 54-skill P1 subgraph named in docs/plan/11-phased-delivery.md: the 13 P1
archetypes, the union of their skills arrays, every edge pointing into that set, and the parents
outside the set split into seeded assumed-mastered rows and inert BC-TOP nodes. Rerun after any
registry change; the engine unit tests read the file, never data/.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "fixtures" / "graph_p1.json"

P1_ARCHETYPES = [
   "BC-QA-01004", "BC-QA-01008", "BC-QA-01015",
   "BC-QA-02002", "BC-QA-02006", "BC-QA-02007", "BC-QA-02008", "BC-QA-02010", "BC-QA-02011",
   "BC-QA-03001", "BC-QA-03004", "BC-QA-03005", "BC-QA-03008",
]

ARCHETYPE_FIELDS = [
   "id", "family", "primary_unit", "skills", "prerequisites", "difficulty_factors",
   "representations", "calculator_status", "point_types", "expected_solution_path",
   "common_distractors", "status",
]


def main():
   archetypes = json.loads((ROOT / "data" / "archetypes.json").read_text())["archetypes"]
   skills_file = json.loads((ROOT / "data" / "skills.json").read_text())
   skills_by_id = {record["id"]: record for record in skills_file["skills"]}
   prerequisites_by_id = {record["id"]: record for record in skills_file["prerequisites"]}
   archetypes_by_id = {record["id"]: record for record in archetypes}

   with (ROOT / "data" / "prereq_edges.csv").open() as handle:
      edges = list(csv.DictReader(handle))

   chosen = [archetypes_by_id[archetype_id] for archetype_id in P1_ARCHETYPES]
   skill_ids = set()

   for record in chosen:
      skill_ids.update(record["skills"])

   inbound = [edge for edge in edges if edge["to"] in skill_ids]
   parents = {edge["from"] for edge in inbound} - skill_ids
   inert_top = sorted(parent for parent in parents if parent.startswith("BC-TOP-"))
   seeded = sorted(parent for parent in parents if not parent.startswith("BC-TOP-"))

   skills = []

   for skill_id in sorted(skill_ids):
      record = skills_by_id[skill_id]
      listing = [archetype_id for archetype_id in P1_ARCHETYPES if skill_id in archetypes_by_id[archetype_id]["skills"]]
      skills.append({
         "id": skill_id,
         "unit": record.get("unit"),
         "concept": record.get("concept"),
         "independently_assessable": record.get("independently_assessable", False),
         "p1_archetypes": listing,
      })

   seeded_rows = []

   for parent in seeded:
      kind = "BC-PRQ" if parent.startswith("BC-PRQ-") else "BC-SKL"
      known = parent in prerequisites_by_id or parent in skills_by_id
      seeded_rows.append({"id": parent, "kind": kind, "in_registry": known})

   fixture = {
      "built_from": "data/archetypes.json, data/skills.json, data/prereq_edges.csv",
      "archetypes": [
         {key: record.get(key) for key in ARCHETYPE_FIELDS}
         for record in chosen
      ],
      "skills": skills,
      "seeded_parents": seeded_rows,
      "inert_top": inert_top,
      "edges": [
         {"from": edge["from"], "to": edge["to"], "type": edge["type"]}
         for edge in inbound
      ],
      "completion_stage_unavailable": [
         record["id"] for record in chosen if len(record["expected_solution_path"]) < 2
      ],
   }

   OUT.parent.mkdir(parents=True, exist_ok=True)
   OUT.write_text(json.dumps(fixture, indent=2) + "\n")
   print(f"{OUT}: {len(skills)} skills, {len(inbound)} edges, {len(seeded_rows)} seeded parents, {len(inert_top)} inert BC-TOP")


if __name__ == "__main__":
   main()
