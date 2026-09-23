"""An agent draft may be served, but it never counts as an operator-authored item.

The operator's ruling of 2026-09-23 (BUILD-LEDGER.md, "Decisions taken on the operator's
instruction, 2026-09-23") lets the drafts in content/items_p1_agent/ reach the bank while exit
criterion 7 of docs/plan/11-phased-delivery.md, gates 17 and 30, and gate 29's key-audit sample
count only items whose provenance model is operator. These tests put one operator record and one
agent draft of the same archetype side by side and check that every counter sees only the first.
"""
import json
import subprocess
import sys
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db import models
from app.items import ingest
from tools.draw_key_audit_sample import published_candidates

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ITEMS_FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "items_p1"
DATA_DIR = REPOSITORY_ROOT / "data"

AGENT_AUTHOR = "claude-opus-5-5 agent draft, pending operator review"
OPERATOR_ITEM_ID = "ITM-SYN-01008-00"
AGENT_ITEM_ID = "ITM-AGT-TEST-01008-00"
ARCHETYPE_ID = "BC-QA-01008"
INGESTED_AT = "2026-09-23T09:00:00+00:00"

OPERATOR_SECTION_HEADING = "operator-authored items per archetype"


def operator_and_agent_records():
   operator_record = json.loads((ITEMS_FIXTURE_DIR / f"{OPERATOR_ITEM_ID}.json").read_text())
   agent_record = dict(operator_record, id=AGENT_ITEM_ID, authored_by=AGENT_AUTHOR)

   return operator_record, agent_record


def write_mixed_directory(tmp_path):
   directory = tmp_path / "mixed_items"
   directory.mkdir()

   for record in operator_and_agent_records():
      (directory / f"{record['id']}.json").write_text(json.dumps(record))

   return directory


def section_counts(stdout, heading):
   """The archetype lines printed under one heading of tools/check_items.py's report."""
   lines = stdout.splitlines()
   starts = [index for index, line in enumerate(lines) if line.startswith(heading)]
   has_the_section = len(starts) == 1

   assert has_the_section, f"expected one {heading!r} section in:\n{stdout}"

   counts = {}

   for line in lines[starts[0] + 1:]:
      is_an_archetype_line = line.startswith("  BC-QA-")

      if not is_an_archetype_line:
         break

      archetype_id, count = line.strip().split(": ")
      counts[archetype_id] = int(count)

   return counts


def test_check_items_counts_an_agent_draft_as_a_record_but_not_as_operator_authored(tmp_path):
   directory = write_mixed_directory(tmp_path)

   result = subprocess.run(
      [sys.executable, "tools/check_items.py", str(directory)],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )

   assert result.returncode == 0, result.stdout + result.stderr
   assert section_counts(result.stdout, "items per archetype")[ARCHETYPE_ID] == 2
   assert section_counts(result.stdout, OPERATOR_SECTION_HEADING)[ARCHETYPE_ID] == 1


def test_the_key_audit_sample_draws_only_from_operator_items(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   snapshot = load_snapshot(DATA_DIR)
   active_error_ids = set(snapshot.errors)

   with OrmSession(engine) as db:
      for record in operator_and_agent_records():
         result = ingest.ingest_item(db, record, active_error_ids, "SNAP-TEST", INGESTED_AT)

         assert result["status"] == "verified", result

      db.commit()

   candidate_ids = [candidate["item_id"] for candidate in published_candidates(engine, snapshot)]

   assert candidate_ids == [OPERATOR_ITEM_ID]
