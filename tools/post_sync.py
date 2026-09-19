"""Final consistency pass after all skill rewrites.

1. Every BC-SKL id in a skill's `prerequisites` becomes a hard_prerequisite edge if no edge exists.
2. `dependents` is rebuilt as the inverse of `prerequisites` across the registry.
3. `adaptive.next_dependent_skills` is filled from `dependents` where it is empty.
Writes data/staging/post-sync-skills.json and data/staging/post-sync.edges.csv, then the caller merges.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STAGING = DATA / "staging"


def main():
   skills = json.loads((DATA / "skills.json").read_text())
   records = skills["skills"]
   by_id = {record["id"]: record for record in records}
   existing = set()

   with (DATA / "prereq_edges.csv").open() as handle:
      for row in csv.DictReader(handle):
         existing.add((row["from"], row["to"]))

   new_edges = []
   dependents = defaultdict(list)

   for record in records:
      for prerequisite in record.get("prerequisites", []):
         is_skill = prerequisite.startswith("BC-SKL-") and prerequisite in by_id

         if not is_skill:
            continue

         dependents[prerequisite].append(record["id"])
         is_new = (prerequisite, record["id"]) not in existing

         if is_new:
            new_edges.append({"from": prerequisite, "to": record["id"], "type": "hard_prerequisite", "evidence_tag": "inferred", "note": f"From the prerequisites field of {record['id']}"})
            existing.add((prerequisite, record["id"]))

   changed = []

   for record in records:
      current = list(record.get("dependents", []))
      merged = list(dict.fromkeys(current + dependents.get(record["id"], [])))
      adaptive = record.setdefault("adaptive", {})
      next_skills = adaptive.get("next_dependent_skills") or []
      has_change = merged != current or (not next_skills and merged)

      if has_change:
         record["dependents"] = merged

         if not next_skills:
            adaptive["next_dependent_skills"] = merged

         changed.append(record)

   (STAGING / "post-sync-skills.json").write_text(json.dumps({"registry": "skills", "skills": changed}, indent=1))

   with (STAGING / "post-sync.edges.csv").open("w", newline="") as handle:
      writer = csv.DictWriter(handle, fieldnames=["from", "to", "type", "evidence_tag", "note"])
      writer.writeheader()
      writer.writerows(new_edges)

   print(len(changed), "skills updated,", len(new_edges), "edges added")


if __name__ == "__main__":
   main()
