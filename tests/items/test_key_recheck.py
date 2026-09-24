"""tools/key_recheck.py over every item bank with its formulations file.

The first two tests are the standing gate: in every bank the app serves (app/main.py
default_item_directories, content/items_*), every key equals the answer computed from its stem, no
distractor equals it, and no stem is worded as a choice. The rest show the recheck can fail for
each reason it claims to check, so a clean run means something.
"""
import json
import shutil
from pathlib import Path

import pytest
import sympy

from app.main import default_item_directories
from tools import key_recheck

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = REPOSITORY_ROOT / "content" / "items_p1_agent"
FORMULATIONS = key_recheck.load_formulations(AGENT_DIR / "key_formulations.py")
ITEM_ID = "ITM-AGT-01004-00"


def one_item_bank(tmp_path, edit=None):
   directory = tmp_path / "bank"
   directory.mkdir()
   record = json.loads((AGENT_DIR / f"{ITEM_ID}.json").read_text())

   if edit is not None:
      edit(record)

   (directory / f"{ITEM_ID}.json").write_text(json.dumps(record))

   return directory


def flags_for(directory):
   results, blind_on = key_recheck.recheck(directory, FORMULATIONS)

   assert blind_on == []

   return results[0].flags


def test_every_p1_agent_item_rechecks_clean():
   results, blind_on = key_recheck.recheck(AGENT_DIR, FORMULATIONS)
   flagged = {result.item_id: result.flags for result in results if not result.is_clean}

   assert blind_on == []
   assert len(results) == 130
   assert flagged == {}


@pytest.mark.parametrize("bank", default_item_directories(), ids=lambda bank: bank.name)
def test_every_bank_rechecks_clean(bank):
   formulations_path = bank / "key_formulations.py"

   assert formulations_path.is_file(), f"{bank.name} has no key_formulations.py"

   results, blind_on = key_recheck.recheck(bank, key_recheck.load_formulations(formulations_path))
   flagged = {result.item_id: result.flags for result in results if not result.is_clean}

   assert blind_on == []
   assert len(results) > 0, f"{bank.name} holds no items"
   assert flagged == {}


def test_a_wrong_key_is_flagged(tmp_path):
   def wrong_key(record):
      record["answer_key"]["mathjson"] = ["Rational", 5, 7]

   assert key_recheck.KEY_DIFFERS in flags_for(one_item_bank(tmp_path, wrong_key))


def test_a_distractor_equal_to_the_key_is_flagged(tmp_path):
   def duplicate_key(record):
      distractor = next(option for option in record["options"] if not option["is_key"])
      distractor["value"] = record["answer_key"]["mathjson"]

   assert key_recheck.OPTION_MISMATCH in flags_for(one_item_bank(tmp_path, duplicate_key))


def test_a_choice_worded_stem_is_flagged(tmp_path):
   def choice_wording(record):
      record["stem"]["text"] = record["stem"]["text"] + " Which of the following is the limit?"

   assert key_recheck.CHOICE_WORDED_STEM in flags_for(one_item_bank(tmp_path, choice_wording))


def test_an_item_with_no_formulation_is_flagged(tmp_path):
   directory = one_item_bank(tmp_path)
   shutil.copy(directory / f"{ITEM_ID}.json", directory / "ITM-AGT-99999-00.json")
   record = json.loads((directory / "ITM-AGT-99999-00.json").read_text())
   record["id"] = "ITM-AGT-99999-00"
   (directory / "ITM-AGT-99999-00.json").write_text(json.dumps(record))
   results, _ = key_recheck.recheck(directory, FORMULATIONS)
   flags_by_item = {result.item_id: result.flags for result in results}

   assert flags_by_item["ITM-AGT-99999-00"] == [key_recheck.NOT_FORMULATED]


def test_a_comparison_that_cannot_be_evaluated_is_never_called_equal():
   unevaluable = sympy.Function("f")(key_recheck.x)

   with pytest.raises(key_recheck.ComparisonUndecided):
      key_recheck.equivalent(unevaluable, 0)


def test_the_control_holds_on_an_answer_of_minus_one(tmp_path):
   """2v + 1 leaves -1 fixed, so a bank whose sampled answer was -1 once failed its control while
   the comparator was sound (ITM-AGT-10003-04, 2026-09-24)."""
   def key_of_minus_one(record):
      record["answer_key"]["mathjson"] = -1

   directory = one_item_bank(tmp_path, key_of_minus_one)
   _, blind_on = key_recheck.recheck(directory, {ITEM_ID: lambda: -1})

   assert blind_on == []


def test_a_comparator_that_calls_everything_equal_fails_the_control(tmp_path, monkeypatch):
   monkeypatch.setattr(key_recheck, "equivalent", lambda left, right: True)

   _, blind_on = key_recheck.recheck(one_item_bank(tmp_path), FORMULATIONS)

   assert blind_on == [ITEM_ID]
