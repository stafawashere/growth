"""Standing checks on every generated bank the app serves (content/items_gen_*).

- The key recheck in template mode: every stored key equals both the blind solver's answer and the
  template's own SymPy answer rebuilt from the item's seed, and the seed still reproduces the item.
- test_no_calculator_closed_form: every no-calculator item's key is exact and was reached with no
  numeric method (11 P4 unit test; rejection rule 8).
- test_distractor_distinct: no distractor equals the key or another distractor, symbolically or
  numerically (11 P4 unit test; rejection rules 5 and 6).
"""
import json
from pathlib import Path

import pytest
import sympy

from app.generation.template import library, numeric_methods_used, template_module
from app.items import ingest
from app.items.distractor_paths import error_ids_for_skills
from app.items.mathjson import to_sympy
from tools import key_recheck

CONTENT = Path(__file__).resolve().parents[2] / "content"
GENERATED_BANKS = sorted(path for path in CONTENT.glob("items_gen_*") if path.is_dir())


def records_in(bank):
   return [json.loads(path.read_text()) for path in sorted(bank.glob("ITM-GEN-*.json"))]


def every_generated_record():
   return [record for bank in GENERATED_BANKS for record in records_in(bank)]


def test_there_are_generated_banks():
   assert len(GENERATED_BANKS) > 0


@pytest.mark.parametrize("bank", GENERATED_BANKS, ids=lambda bank: bank.name)
def test_every_generated_bank_rechecks_clean_against_blind_and_template_answers(bank):
   formulations = key_recheck.load_formulations(bank / "key_formulations.py")
   results, blind_on = key_recheck.recheck(bank, formulations, template_answers=True)
   flagged = {result.item_id: result.flags for result in results if not result.is_clean}

   assert blind_on == []
   assert len(results) > 0
   assert flagged == {}


def test_no_calculator_closed_form():
   offenders = []
   templates_with_numeric_calls = {}

   for record in every_generated_record():
      is_no_calculator = record["calculator_status"] == "no_calculator"

      if not is_no_calculator:
         continue

      key = record["answer_key"]
      is_statement = key["form"] == "statement"

      if is_statement:
         continue

      value = to_sympy(key["mathjson"])
      is_exact = not value.has(sympy.Float) and not isinstance(key["mathjson"], float)

      if not is_exact:
         offenders.append(record["id"])

      archetype_id = record["archetype_id"]
      archetype = library().archetypes[archetype_id]
      is_no_calculator_archetype = archetype["calculator_status"] == "no_calculator"

      if is_no_calculator_archetype and archetype_id not in templates_with_numeric_calls:
         templates_with_numeric_calls[archetype_id] = numeric_methods_used(template_module(archetype_id))

   assert offenders == []
   assert {name: calls for name, calls in templates_with_numeric_calls.items() if calls} == {}


def test_distractor_distinct():
   failing = {}

   for record in every_generated_record():
      archetype = library().archetypes[record["archetype_id"]]
      error_ids = error_ids_for_skills(library(), archetype["skills"])
      outcomes = {result["check_type"]: result["outcome"] for result in ingest.run_checks(record, error_ids)}

      if outcomes.get("distractor_distinct") != ingest.PASS:
         failing[record["id"]] = outcomes

   assert failing == {}
