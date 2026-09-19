"""Mint the next ID for a prefix and register it in data/ids.json.

Usage: python3 tools/mint_id.py BC-SKL "name of the record" [count]
IDs are append-only. Retirement is a tombstone with superseded_by, never deletion.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDS = ROOT / "data" / "ids.json"

WIDTH = {"BC-UNIT": 2, "BC-REP": 2, "BC-DF": 2, "BC-CV": 2}
BLOCKED = {"BC-CON", "BC-SKL", "BC-PRQ", "BC-QA", "BC-PT", "BC-ERR", "BC-MIS", "BC-SIG"}


def load():
   return json.loads(IDS.read_text()) if IDS.exists() else {"ids": {}}


def save(registry):
   IDS.write_text(json.dumps(registry, indent=1, sort_keys=True))


def next_ids(registry, prefix, count, block="00"):
   """Blocked prefixes use a two-digit block (unit number, 00 for cross-cutting, 99 for synthesis) plus a three-digit sequence."""
   is_blocked = prefix in BLOCKED
   width = WIDTH.get(prefix, 4)
   head = f"{prefix}-{block}" if is_blocked else f"{prefix}-"
   pattern = re.compile("^" + re.escape(head) + r"(\d+)$")
   existing = [int(match.group(1)) for key in registry["ids"] for match in [pattern.match(key)] if match]
   start = max(existing, default=0) + 1
   digits = 3 if is_blocked else width
   return [f"{head}{number:0{digits}d}" for number in range(start, start + count)]


def mint(prefix, name, count=1, block="00"):
   registry = load()
   minted = next_ids(registry, prefix, count, block)

   for new_id in minted:
      registry["ids"][new_id] = {"name": name, "created": str(date.today()), "status": "active"}

   save(registry)
   return minted


def register(explicit_id, name):
   registry = load()
   is_new = explicit_id not in registry["ids"]

   if is_new:
      registry["ids"][explicit_id] = {"name": name, "created": str(date.today()), "status": "active"}
      save(registry)

   return explicit_id


if __name__ == "__main__":
   prefix, name = sys.argv[1], sys.argv[2]
   count = int(sys.argv[3]) if len(sys.argv) > 3 else 1
   block = sys.argv[4] if len(sys.argv) > 4 else "00"
   print("\n".join(mint(prefix, name, count, block)))
