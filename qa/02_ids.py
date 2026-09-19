"""ID format, uniqueness, registration in ids.json, and tombstone integrity."""
import re
from qa_common import load_json, all_records, prefix_of, ID_PATTERNS, finish

failures = []
registry = load_json("ids.json") or {"ids": {}}
seen = {}

for location, record in all_records():
   identifier = record.get("id", "")
   prefix = prefix_of(identifier)
   pattern = ID_PATTERNS.get(prefix)
   is_known_prefix = pattern is not None
   is_well_formed = is_known_prefix and re.match(pattern, identifier) is not None

   if not is_well_formed:
      failures.append(f"{location}: malformed id {identifier!r}")
      continue

   is_duplicate = identifier in seen

   if is_duplicate:
      failures.append(f"{identifier} duplicated in {seen[identifier]} and {location}")

   seen[identifier] = location
   is_registered = identifier in registry["ids"]

   if not is_registered:
      failures.append(f"{identifier} not registered in ids.json")

for identifier, entry in registry["ids"].items():
   is_retired = entry.get("status") == "retired"
   has_successor = bool(entry.get("superseded_by"))
   is_dangling_tombstone = is_retired and has_successor and entry["superseded_by"] not in registry["ids"]
   is_unbacked = entry.get("status") == "active" and identifier not in seen

   if is_dangling_tombstone:
      failures.append(f"{identifier} superseded_by unknown id")

   if is_unbacked:
      failures.append(f"{identifier} registered but no record exists")

finish("02_ids", failures)
