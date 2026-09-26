"""The bank ingests every item directory it is given, and by default every content/items_* bank.

Items for Units 4 to 10 live in per-unit directories beside content/items_p1_agent, so a bank that
read only one directory would leave every unit but one unservable while its checks stayed green.
"""
import json
import os
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db import models
from app.main import DEFAULT_ITEMS_DIR, default_item_directories, default_retired_directories, items_directories
from app.runtime.bank import RETIRED_STATUS
from app.runtime.context import build_session_context

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = REPO_ROOT / "data"
CONTENT_DIR = REPO_ROOT / "content"
P1_RECORD = DEFAULT_ITEMS_DIR / "ITM-AGT-01004-00.json"


def bank_directory(root, name, item_id):
   directory = root / name
   directory.mkdir()
   record = json.loads(P1_RECORD.read_text())
   record["id"] = item_id
   (directory / f"{item_id}.json").write_text(json.dumps(record))

   return directory


def test_the_default_banks_are_every_content_items_directory():
   expected = sorted(path for path in CONTENT_DIR.iterdir() if path.is_dir() and path.name.startswith("items_"))

   assert list(default_item_directories()) == expected
   assert DEFAULT_ITEMS_DIR in expected
   assert CONTENT_DIR / "items_unit06_agent" in expected
   assert CONTENT_DIR / "items_unit10_agent" in expected
   assert items_directories({}) == tuple(expected)


def test_the_variable_names_several_directories(tmp_path):
   first = bank_directory(tmp_path, "first", "ITM-AGT-01004-90")
   second = bank_directory(tmp_path, "second", "ITM-AGT-01004-91")

   assert items_directories({"GROWTH_ITEMS_DIR": f"{first}{os.pathsep}{second}"}) == (first, second)
   assert items_directories({"GROWTH_ITEMS_DIR": "none"}) == ()

   with pytest.raises(ValueError):
      items_directories({"GROWTH_ITEMS_DIR": f"{first}{os.pathsep}{tmp_path / 'missing'}"})


def test_the_bank_serves_records_from_every_directory(tmp_path):
   first = bank_directory(tmp_path, "first", "ITM-AGT-01004-90")
   second = bank_directory(tmp_path, "second", "ITM-AGT-01004-91")
   engine = models.make_engine(tmp_path / "growth.db")

   context = build_session_context(engine, DATA_ROOT, items_directories=(first, second))
   served_ids = [item["id"] for item in context.bank.published_items("BC-QA-01004")]

   assert served_ids == ["ITM-AGT-01004-90", "ITM-AGT-01004-91"]


def test_an_id_in_two_directories_stops_ingestion(tmp_path):
   first = bank_directory(tmp_path, "first", "ITM-AGT-01004-90")
   second = bank_directory(tmp_path, "second", "ITM-AGT-01004-90")
   engine = models.make_engine(tmp_path / "growth.db")
   context = build_session_context(engine, DATA_ROOT, items_directories=(first, second))

   with pytest.raises(ValueError, match="ITM-AGT-01004-90"):
      context.bank.published_items("BC-QA-01004")


def test_the_snapshot_holds_every_archetype_the_default_banks_name():
   archetypes = load_snapshot(DATA_ROOT).archetypes
   named = set()

   for directory in default_item_directories():
      for path in directory.glob("ITM-*.json"):
         named.add(json.loads(path.read_text())["archetype_id"])

   assert sorted(named - set(archetypes)) == []


def test_every_record_file_is_named_by_its_id():
   """A copy such as "ITM-AGT-03009-00 3.json", which the file system left beside its original on
   2026-09-24, would be ingested as a second record with the same id."""
   misnamed = []

   for directory in default_item_directories():
      for path in directory.glob("*.json"):
         record_id = json.loads(path.read_text()).get("id")
         is_named_by_id = path.name == f"{record_id}.json"

         if not is_named_by_id:
            misnamed.append(str(path.relative_to(CONTENT_DIR)))

   assert misnamed == []


def test_an_item_retired_after_a_database_stored_it_stops_being_served(tmp_path):
   """P5 found ITM-GEN-01005-04 served from a database that had ingested it before it moved to
   content/generation_review/rejected, because ingestion never re-reads a stored id. A record in a
   retired directory now retires the stored row on the next start."""
   bank = bank_directory(tmp_path, "bank", "ITM-AGT-01004-90")
   bank_directory(tmp_path, "later", "ITM-AGT-01004-91")
   engine = models.make_engine(tmp_path / "growth.db")
   first_start = build_session_context(engine, DATA_ROOT, items_directories=(bank, tmp_path / "later"))

   assert [item["id"] for item in first_start.bank.published_items("BC-QA-01004")] == ["ITM-AGT-01004-90", "ITM-AGT-01004-91"]

   rejected = tmp_path / "rejected"
   rejected.mkdir()
   (tmp_path / "later" / "ITM-AGT-01004-91.json").rename(rejected / "ITM-AGT-01004-91.json")
   next_start = build_session_context(
      engine, DATA_ROOT, items_directories=(bank, tmp_path / "later"), retired_directories=(rejected,)
   )

   assert [item["id"] for item in next_start.bank.published_items("BC-QA-01004")] == ["ITM-AGT-01004-90"]

   with OrmSession(engine) as db:
      assert db.get(models.Item, "ITM-AGT-01004-91").status == RETIRED_STATUS


def test_the_running_app_reads_the_rejected_items_as_retired():
   assert default_retired_directories() == (CONTENT_DIR / "generation_review" / "rejected",)
