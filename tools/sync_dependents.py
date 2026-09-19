"""Make data/skills.json agree with the hard_prerequisite edges in data/prereq_edges.csv.

For every hard_prerequisite edge between two atomic skills, the downstream skill must list the
upstream one under "prerequisites" and the upstream one must list the downstream under
"dependents". Every skill that is an endpoint of such an edge is written whole to
data/staging/sync-dependents.json so that tools/merge_staging.py remains the only writer of the
registry and the staging file states the full set of links rather than only the last delta.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDGES = ROOT / "data" / "prereq_edges.csv"
SKILLS = ROOT / "data" / "skills.json"
OUT = ROOT / "data" / "staging" / "sync-dependents.json"


def main():
   registry = json.loads(SKILLS.read_text())
   by_id = {skill["id"]: skill for skill in registry["skills"]}
   touched = set()
   changed = set()

   with EDGES.open() as handle:
      edges = [row for row in csv.DictReader(handle)]

   for row in edges:
      source = row["from"]
      target = row["to"]
      is_hard = row["type"] == "hard_prerequisite"
      both_are_skills = source in by_id and target in by_id

      if not (is_hard and both_are_skills):
         continue

      downstream = by_id[target]
      upstream = by_id[source]
      touched.add(source)
      touched.add(target)

      needs_prerequisite = source not in downstream.get("prerequisites", [])

      if needs_prerequisite:
         downstream.setdefault("prerequisites", []).append(source)
         downstream["prerequisites"].sort()
         changed.add(target)

      needs_dependent = target not in upstream.get("dependents", [])

      if needs_dependent:
         upstream.setdefault("dependents", []).append(target)
         upstream["dependents"].sort()
         changed.add(source)

   records = [by_id[identifier] for identifier in sorted(touched)]
   OUT.write_text(json.dumps({"registry": "skills", "skills": records}, indent=1, sort_keys=True))
   print(len(records), "skill records staged;", len(changed), "of them needed a new link")


if __name__ == "__main__":
   main()
