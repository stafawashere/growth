import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "schemas"))
from common import ANY_ID, ID_PATTERNS, REGISTRY_FILES, EVIDENCE_TAGS, FORBIDDEN_PREDICTION  # noqa: E402

DATA = ROOT / "data"
RESEARCH = ROOT / "research"
CACHE = ROOT / "cache"


def load_json(name):
   path = DATA / name
   return json.loads(path.read_text()) if path.exists() else None


def all_records():
   """Yield (registry_key, record) for every record in every registry."""
   seen = set()

   for prefix, location in REGISTRY_FILES.items():
      file_name, key = location.split(":")
      is_seen = (file_name, key) in seen

      if is_seen:
         continue

      seen.add((file_name, key))
      data = load_json(file_name)
      has_data = data is not None and key in data

      if not has_data:
         continue

      for record in data[key]:
         yield f"{file_name}:{key}", record


def markdown_files():
   return sorted(RESEARCH.rglob("*.md")) + sorted(path for path in ROOT.glob("*.md") if path.name != "CLAUDE.md")


def ids_in_text(text):
   return set(ANY_ID.findall(text))


def prefix_of(identifier):
   parts = identifier.split("-")
   return "-".join(parts[:2])


def finish(name, failures, warnings=None):
   warnings = warnings or []

   for warning in warnings:
      print(f"WARN {name}: {warning}")

   for failure in failures:
      print(f"FAIL {name}: {failure}")

   print(f"{name}: {len(failures)} failures, {len(warnings)} warnings")
   sys.exit(1 if failures else 0)
