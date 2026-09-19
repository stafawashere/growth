"""Mark tombstones in data/ids.json for every registry record carrying status retired.

The registries are the source of truth. A record with "status": "retired" and a "superseded_by"
id gets the same status and successor written onto its ids.json entry, so that qa/02_ids.py
finds a valid tombstone. Run after tools/merge_staging.py.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mint_id import load, save  # noqa: E402

DATA = ROOT / "data"
REGISTRIES = [
   ("misconceptions.json", "misconceptions"),
   ("errors.json", "errors"),
   ("diagnostic_signals.json", "signals"),
   ("skills.json", "skills"),
   ("archetypes.json", "archetypes"),
   ("scoring_points.json", "scoring_points"),
]


def main():
   registry_ids = load()
   marked, skipped = 0, []

   for file_name, key in REGISTRIES:
      path = DATA / file_name
      has_file = path.exists()

      if not has_file:
         continue

      data = json.loads(path.read_text())

      for record in data.get(key, []):
         is_retired = record.get("status") == "retired"

         if not is_retired:
            continue

         successor = record.get("superseded_by")
         has_successor = bool(successor)
         successor_known = has_successor and successor in registry_ids["ids"]

         if not successor_known:
            skipped.append(f"{record['id']}: superseded_by {successor!r} is not a registered id")
            continue

         entry = registry_ids["ids"].setdefault(record["id"], {"name": record.get("name", ""), "status": "active"})
         entry["status"] = "retired"
         entry["superseded_by"] = successor
         marked += 1

   save(registry_ids)
   print(f"retire_ids: {marked} tombstones written")

   for problem in skipped:
      print(f"retire_ids: skipped {problem}")

   return 1 if skipped else 0


if __name__ == "__main__":
   sys.exit(main())
