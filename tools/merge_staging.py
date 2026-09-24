"""Merge data/staging/*.json into the main registries and register their IDs.

A staging file is {"registry": "<name>", "<collection>": [records], ...}. Records replace any
existing record with the same id, so re-running is idempotent. A file that also carries
"merge": "fields" instead sets only the fields each record names on a record that already exists,
so a field added to a registry by one file cannot revert what a later edit changed elsewhere in
the record. "merge": "append" does the same but adds each list field's entries to the existing
list rather than replacing it, so a link added by one file survives links added by another.
Only this tool writes ids.json for minted families.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mint_id import load, save  # noqa: E402
from datetime import date  # noqa: E402

DATA = ROOT / "data"
STAGING = DATA / "staging"


def merge_file(path, registry_ids):
   staged = json.loads(path.read_text())
   registry_name = staged.pop("registry")
   merge_mode = staged.pop("merge", None)
   merges_fields = merge_mode in ("fields", "append")
   target = DATA / f"{registry_name}.json"
   current = json.loads(target.read_text())
   merged = 0

   for collection, records in staged.items():
      is_list = isinstance(records, list)

      if not is_list:
         continue

      current.setdefault(collection, [])
      by_id = {record["id"]: index for index, record in enumerate(current[collection])}

      for record in records:
         if merges_fields:
            merge_fields(current[collection], by_id, record, path, appends=merge_mode == "append")
            merged += 1
            continue

         record.setdefault("created", str(date.today()))
         record["updated"] = str(date.today())
         exists = record["id"] in by_id

         if exists:
            current[collection][by_id[record["id"]]] = record
         else:
            current[collection].append(record)
            by_id[record["id"]] = len(current[collection]) - 1

         registry_ids["ids"].setdefault(record["id"], {"name": record.get("name", ""), "created": str(date.today()), "status": "active"})
         merged += 1

   target.write_text(json.dumps(current, indent=1, sort_keys=True))
   return registry_name, merged


def merge_fields(records, by_id, fields, path, appends=False):
   is_known = fields["id"] in by_id

   if not is_known:
      raise SystemExit(f"{path.name}: {fields['id']} is not in the registry, so its fields cannot be merged")

   existing = records[by_id[fields["id"]]]

   if appends:
      fields = {
         name: appended(existing.get(name), value) if isinstance(value, list) else value
         for name, value in fields.items()
      }

   changed = any(existing.get(name) != value for name, value in fields.items())
   existing.update(fields)

   if changed:
      existing["updated"] = str(date.today())


def appended(current, additions):
   merged = list(current or [])

   for entry in additions:
      if entry not in merged:
         merged.append(entry)

   return merged


PHASE_ORDER = ["unit-", "taxonomy-", "scoring-points", "command-verbs", "chief-reader-", "mcq-", "frq-", "difficulty-factors", "representation-map", "archetype-consolidation", "misconception-consolidation", "error-consolidation", "signal-reference-remap", "sync-dependents", "link-evidence-", "cite-sync-", "tag-policy-", "adaptive-", "post-sync-", "assessability-", "errors-enrich-", "signals-", "gap-", "error-links-", "parameter-spec-"]


def phase_rank(path):
   """Later phases must replay after earlier ones so consolidation and linking edits win."""
   for index, prefix in enumerate(PHASE_ORDER):
      if path.name.startswith(prefix):
         return index

   return len(PHASE_ORDER)


def main():
   registry_ids = load()
   wanted = sys.argv[1:]

   for path in sorted(STAGING.glob("*.json"), key=lambda item: (phase_rank(item), item.name)):
      is_wanted = not wanted or path.name in wanted or path.stem in wanted

      if not is_wanted:
         continue

      registry_name, merged = merge_file(path, registry_ids)
      print(path.name, "->", registry_name, merged, "records")

   save(registry_ids)


if __name__ == "__main__":
   main()
