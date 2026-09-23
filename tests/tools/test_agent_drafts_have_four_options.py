"""Operator ruling, 2026-09-23: every agent draft in content/items_p1_agent/ becomes MCQ-capable
with exactly four options, one key plus three distractors, whatever the item's own format field
says. app/items/verify.py's own checks (exercised through tools/check_items.py) accept a record
with fewer options or none at all, since they only check whatever option set is actually there,
so that gate alone would not have caught the options-less items the twenty-third session found.
This test reads the real directory and enforces the shape the ruling asked for.
"""
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ITEMS_DIR = REPOSITORY_ROOT / "content" / "items_p1_agent"


def item_records():
   paths = sorted(ITEMS_DIR.glob("*.json"))

   return [(path.name, json.loads(path.read_text())) for path in paths]


def test_every_agent_draft_carries_exactly_four_options():
   records = item_records()
   has_records = len(records) > 0

   assert has_records, f"no item records found under {ITEMS_DIR}"

   short_of_four = []

   for name, record in records:
      options = record.get("options") or []
      carries_four = len(options) == 4

      if not carries_four:
         short_of_four.append((name, len(options)))

   assert short_of_four == []


def test_every_option_set_carries_exactly_one_key_and_three_error_tagged_distractors():
   for name, record in item_records():
      options = record["options"]
      keys = [option for option in options if option.get("is_key") is True]
      distractors = [option for option in options if option.get("is_key") is not True]

      assert len(keys) == 1, name
      assert keys[0].get("error_path") is None, name
      assert len(distractors) == 3, name

      for distractor in distractors:
         assert distractor.get("error_path") is not None, name
