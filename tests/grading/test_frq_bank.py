"""The served free-response bank stays clean: every record passes tools/check_frq_items.py, every
checked point's key matches its blind formulation, and the recheck's control holds. A planted
wrong key must be flagged, so a clean result means the comparator was looking."""
import copy
import json
from pathlib import Path

import pytest

from app.content.loader import load_snapshot
from app.frq.items import load_frq_records
from tools import check_frq_items, frq_key_recheck

REPO_ROOT = Path(__file__).resolve().parents[2]
BANK = REPO_ROOT / "content" / "frq_items"
FORMULATIONS = BANK / "key_formulations.py"


@pytest.fixture(scope="module")
def snapshot():
   return load_snapshot(REPO_ROOT / "data")


def test_every_served_record_passes_the_bank_checker(snapshot):
   count, problems = check_frq_items.check_directory(BANK, snapshot)

   assert problems == []
   assert count >= 24


def test_every_checked_key_matches_its_blind_formulation_and_the_control_holds():
   records = load_frq_records(BANK)
   results = frq_key_recheck.check_bank(records, frq_key_recheck.load_formulations(FORMULATIONS))
   statuses = {status for _key, status, _detail in results}

   assert statuses == {"match"}
   assert len(results) >= 66
   assert frq_key_recheck.control_holds(results) is True


def test_a_planted_wrong_key_is_flagged():
   records = copy.deepcopy(load_frq_records(BANK))
   target = next(record for record in records if record["id"] == "FRQ-AGT-05007-01")
   answer_check = target["parts"][0]["points"][1]["check"]
   answer_check["expected"] = "4"

   results = frq_key_recheck.check_bank([target], frq_key_recheck.load_formulations(FORMULATIONS))
   flagged = [key for key, status, _detail in results if status == "key_differs"]

   assert flagged == ["FRQ-AGT-05007-01:a2"]


def test_every_record_file_is_named_by_its_id():
   for path in BANK.glob("*.json"):
      assert json.loads(path.read_text())["id"] == path.stem
