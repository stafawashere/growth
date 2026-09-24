"""tools/key_recheck.py's mode for template-defined answers and the comparisons generated items
need: a statement compared by its label, a three-decimal key at its reported places, an
antiderivative up to a real constant of integration, and a stored item the seed no longer rebuilds.
"""
import json

import sympy

from app.generation.instantiate import instantiate
from app.generation.template import template_module
from tools import key_recheck

x = sympy.Symbol("x")
C = key_recheck.INTEGRATION_CONSTANT


def generated_bank(tmp_path, archetype_id, edit=None):
   directory = tmp_path / "bank"
   directory.mkdir()
   record = instantiate(template_module(archetype_id), 0, f"{archetype_id}:recheck-test:0", generated_at="test")

   if edit is not None:
      edit(record)

   (directory / f"{record['id']}.json").write_text(json.dumps(record))

   return directory, record


def template_flags(directory):
   records = [json.loads(path.read_text()) for path in directory.glob("ITM-*.json")]

   return key_recheck.template_check(records[0])[0]


def test_antiderivatives_that_differ_by_a_real_constant_are_equivalent():
   assert key_recheck.equivalent(sympy.sin(x) + C, sympy.sin(x) + 5)
   assert key_recheck.equivalent(sympy.log(sympy.Abs(2 * x + 1)) + C, sympy.log(sympy.Abs(2 * x + 1)))


def test_a_dropped_absolute_value_is_not_a_constant_of_integration():
   assert not key_recheck.equivalent(sympy.log(sympy.Abs(x - 5)) + C, sympy.log(x - 5))


def test_a_different_antiderivative_is_not_equivalent():
   assert not key_recheck.equivalent(sympy.sin(2 * x) / 2 + C, sympy.sin(2 * x) + C)


def test_a_statement_key_is_compared_by_its_label(tmp_path):
   directory, record = generated_bank(tmp_path, "BC-QA-10007")
   label = record["answer_key"]["label"]
   wrong = next(option["label"] for option in record["options"] if not option["is_key"])
   results, blind_on = key_recheck.recheck(directory, {record["id"]: lambda: label})
   wrong_results, _ = key_recheck.recheck(directory, {record["id"]: lambda: wrong})

   assert blind_on == []
   assert results[0].flags == [key_recheck.KEY_MATCHES]
   assert key_recheck.KEY_DIFFERS in wrong_results[0].flags


def test_a_three_decimal_key_is_compared_at_its_reported_places(tmp_path):
   directory, record = generated_bank(tmp_path, "BC-QA-08001")
   exact = sympy.Float(record["answer_key"]["mathjson"], 30)
   nudged_inside = exact + sympy.Float("0.00001")
   nudged_outside = exact + sympy.Float("0.002")

   inside, _ = key_recheck.recheck(directory, {record["id"]: lambda: nudged_inside})
   outside, _ = key_recheck.recheck(directory, {record["id"]: lambda: nudged_outside})

   assert inside[0].flags == [key_recheck.KEY_MATCHES]
   assert key_recheck.KEY_DIFFERS in outside[0].flags


def test_the_template_mode_passes_an_item_its_seed_rebuilds(tmp_path):
   directory, _record = generated_bank(tmp_path, "BC-QA-06004")

   assert template_flags(directory) == []


def test_the_template_mode_flags_a_key_the_template_does_not_give(tmp_path):
   def wrong_key(record):
      record["answer_key"]["mathjson"] = ["Rational", 5, 7]

   directory, _record = generated_bank(tmp_path, "BC-QA-06004", wrong_key)

   assert key_recheck.TEMPLATE_DIFFERS in template_flags(directory)


def test_the_template_mode_flags_a_stem_the_seed_no_longer_produces(tmp_path):
   def edited_stem(record):
      record["stem"]["text"] = record["stem"]["text"] + " Show the work."

   directory, _record = generated_bank(tmp_path, "BC-QA-06004", edited_stem)

   assert key_recheck.PROVENANCE_DRIFT in template_flags(directory)
