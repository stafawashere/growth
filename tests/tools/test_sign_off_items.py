"""tools/sign_off_items.py: the operator's one command for adopting reviewed agent drafts.

Gates 17, 29 and 30 and exit criterion 7 count only provenance model operator. A signed-off
record must count on disk and in a database that ingested it before the sign-off, and nothing
the operator did not name may change.
"""
import json
import shutil
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db import models
from app.items import ingest
from tools import sign_off_items
from tools.draw_key_audit_sample import published_candidates

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = REPOSITORY_ROOT / "content" / "items_p1_agent"
DATA_DIR = REPOSITORY_ROOT / "data"
SIGNED_ITEM = "ITM-AGT-01004-00"
UNSIGNED_ITEM = "ITM-AGT-01004-01"
INGESTED_AT = "2026-09-23T09:00:00+00:00"


def copied_items(tmp_path):
   directory = tmp_path / "items"
   directory.mkdir()

   for item_id in (SIGNED_ITEM, UNSIGNED_ITEM):
      shutil.copy(AGENT_DIR / f"{item_id}.json", directory / f"{item_id}.json")

   return directory


def ingested_database(tmp_path, directory):
   engine = models.make_engine(tmp_path / "growth.db")
   snapshot = load_snapshot(DATA_DIR)

   with OrmSession(engine) as db:
      for path in sorted(directory.glob("ITM-*.json")):
         ingest.ingest_item(db, json.loads(path.read_text()), set(snapshot.errors), "SNAP-TEST", INGESTED_AT)

      db.commit()

   return engine, snapshot


def test_signing_off_one_item_counts_it_on_disk_and_in_the_database(tmp_path):
   directory = copied_items(tmp_path)
   engine, snapshot = ingested_database(tmp_path, directory)
   drafted_by = json.loads((directory / f"{SIGNED_ITEM}.json").read_text())["authored_by"]

   assert published_candidates(engine, snapshot) == []

   exit_code = sign_off_items.main(
      ["sign_off", SIGNED_ITEM, "--items-dir", str(directory), "--db", str(tmp_path / "growth.db")]
   )
   signed = json.loads((directory / f"{SIGNED_ITEM}.json").read_text())
   unsigned = json.loads((directory / f"{UNSIGNED_ITEM}.json").read_text())

   assert exit_code == 0
   assert ingest.is_operator_authored(signed)
   assert signed["drafted_by"] == drafted_by
   assert not ingest.is_operator_authored(unsigned)
   assert [row["item_id"] for row in published_candidates(engine, snapshot)] == [SIGNED_ITEM]


def test_an_unknown_id_changes_nothing(tmp_path):
   directory = copied_items(tmp_path)
   before = {path.name: path.read_text() for path in directory.glob("*.json")}

   exit_code = sign_off_items.main(["sign_off", SIGNED_ITEM, "ITM-AGT-99999-00", "--items-dir", str(directory)])
   after = {path.name: path.read_text() for path in directory.glob("*.json")}

   assert exit_code == 1
   assert after == before
