"""docs/plan/04-item-generation.md, "Checks on the option set" and "Independent
key verification"; docs/plan/11-phased-delivery.md R9's settle-rate measurement.
"""
import json
from pathlib import Path

import pytest
import sympy

from app.items.mathjson import to_sympy
from app.items.verify import (
   UNSETTLED_VIOLATION,
   compare_expressions,
   distractor_checks,
   equivalence,
   verify_item,
)

ROOT = Path(__file__).resolve().parents[2]
PAIRS_PATH = ROOT / "tests" / "fixtures" / "answers_equiv" / "pairs.json"


def load_pairs():
   return json.loads(PAIRS_PATH.read_text())


def test_sympy_equivalence():
   pairs = load_pairs()
   equivalent_pairs = [pair for pair in pairs if pair["equivalent"]]
   nonequivalent_pairs = [pair for pair in pairs if not pair["equivalent"]]

   assert len(equivalent_pairs) == 40
   assert len(nonequivalent_pairs) == 13

   for pair in equivalent_pairs:
      left = to_sympy(pair["left"])
      right = to_sympy(pair["right"])
      assert equivalence(left, right) == "equivalent"

   unsettled_count = 0

   for pair in nonequivalent_pairs:
      left = to_sympy(pair["left"])
      right = to_sympy(pair["right"])
      result = equivalence(left, right)

      assert result != "equivalent"

      if result == "unsettled":
         unsettled_count += 1

   print(f"\ntest_sympy_equivalence: {unsettled_count} of {len(nonequivalent_pairs)} non-equivalent pairs unsettled")

   key = to_sympy("x")
   equals_key = to_sympy(["Add", "x", 0])
   equals_each_other_one = to_sympy(["Add", "x", 1])
   equals_each_other_two = to_sympy(["Add", "x", 1])
   missing_path = to_sympy(["Add", "x", 2])

   violations = distractor_checks(
      key,
      [equals_key, equals_each_other_one, equals_each_other_two, missing_path],
      [None, "BC-ERR-00001", "BC-ERR-00001", None],
      {"BC-ERR-00001"},
   )

   assert "rule_5" in violations
   assert "rule_6" in violations
   assert "rule_7" in violations

   bad_item = {
      "answer_key": "x",
      "options": [
         {"value": "x", "error_path": None},
         {"value": ["Add", "x", 0], "error_path": "BC-ERR-00002"},
      ],
      "provenance": {"model": "operator", "prompt_template_version": None, "generation_job_id": None},
   }

   verdict = verify_item(bad_item, {"BC-ERR-00002"})

   assert verdict["verified"] is False
   assert "rule_5" in verdict["violations"]


def eval_sympy_settle_rate(capsys):
   pairs = load_pairs()
   equivalent_pairs = [pair for pair in pairs if pair["equivalent"]]
   denominator = len(equivalent_pairs)
   settled = 0

   for pair in equivalent_pairs:
      left = to_sympy(pair["left"])
      right = to_sympy(pair["right"])
      result = equivalence(left, right)
      settled_this_pair = result in ("equivalent", "not_equivalent")

      if settled_this_pair:
         settled += 1

   assert denominator > 0

   with capsys.disabled():
      print(f"\neval_sympy_settle_rate: {settled}/{denominator} settled")


def test_equivalence_runs_off_the_main_thread():
   """FastAPI runs a sync route in a worker thread, where signal.signal raises ValueError."""
   import threading

   from sympy import Symbol

   x = Symbol("x")
   outcome = {}

   def compare():
      try:
         outcome["result"] = equivalence(x + x, 2 * x)
      except Exception as failure:
         outcome["failure"] = failure

   worker = threading.Thread(target=compare)
   worker.start()
   worker.join()

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"] == "equivalent"


OPERATOR_PROVENANCE = {"model": "operator", "prompt_template_version": None, "generation_job_id": None}


def mcq_item(options):
   return {"answer_key": "x", "options": options, "provenance": OPERATOR_PROVENANCE}


def test_a_distractor_with_a_null_error_path_is_not_taken_for_a_second_key():
   item = mcq_item([
      {"value": "x", "is_key": True, "error_path": None},
      {"value": ["Add", "x", 1], "is_key": False, "error_path": None},
      {"value": ["Add", "x", 2], "is_key": False, "error_path": "BC-ERR-00001"},
   ])

   verdict = verify_item(item, {"BC-ERR-00001"})

   assert verdict["verified"] is False
   assert "rule_7" in verdict["violations"]


def test_a_key_with_an_error_path_is_refused_and_not_compared_as_a_distractor():
   item = mcq_item([
      {"value": "x", "is_key": True, "error_path": "BC-ERR-00001"},
      {"value": ["Add", "x", 1], "is_key": False, "error_path": "BC-ERR-00001"},
      {"value": ["Add", "x", 2], "is_key": False, "error_path": "BC-ERR-00001"},
   ])

   verdict = verify_item(item, {"BC-ERR-00001"})

   assert verdict["verified"] is False
   assert "key_with_error_path" in verdict["violations"]
   assert "rule_5" not in verdict["violations"]


def test_an_option_set_without_exactly_one_key_is_refused():
   item = mcq_item([
      {"value": "x", "is_key": True, "error_path": None},
      {"value": ["Add", "x", 1], "is_key": True, "error_path": None},
      {"value": ["Add", "x", 2], "is_key": False, "error_path": "BC-ERR-00001"},
   ])

   verdict = verify_item(item, {"BC-ERR-00001"})

   assert verdict["verified"] is False
   assert "exactly_one_key" in verdict["violations"]


def test_an_option_without_is_key_is_refused():
   item = mcq_item([
      {"value": "x", "is_key": True, "error_path": None},
      {"value": ["Add", "x", 1], "error_path": "BC-ERR-00001"},
      {"value": ["Add", "x", 2], "is_key": False, "error_path": "BC-ERR-00001"},
   ])

   verdict = verify_item(item, {"BC-ERR-00001"})

   assert verdict["verified"] is False
   assert "option_without_is_key" in verdict["violations"]


def test_equations_are_equivalent_when_their_zero_forms_agree_up_to_sign():
   k, m = sympy.symbols("k m")

   assert equivalence(sympy.Eq(k + m, 2), sympy.Eq(2 - m, k)) == "equivalent"
   assert equivalence(sympy.Eq(2 * k, 4), sympy.Eq(k, 2)) != "equivalent"
   assert equivalence(sympy.Eq(k + m, 2), sympy.Eq(k + m, 3)) == "not_equivalent"


def test_an_equation_against_an_expression_raises_and_is_never_called_distinct():
   """03 sends a check that cannot decide to the model rather than calling it wrong, and whether
   k + m = 2 answers a key of k + m - 2 is a reading, not algebra. The comparison raises, as the
   subtraction always did, and the distractor checks read the raise as unsettled."""
   k, m = sympy.symbols("k m")

   with pytest.raises(TypeError):
      equivalence(sympy.Eq(k + m, 2), k + m - 2)

   violations = distractor_checks(k + m - 2, [sympy.Eq(k + m, 2)], ["BC-ERR-00001"], {"BC-ERR-00001"})

   assert violations == [UNSETTLED_VIOLATION]


def test_a_set_holding_an_equation_and_a_number_still_matches_element_by_element():
   k = sympy.Symbol("k")

   assert equivalence(sympy.FiniteSet(sympy.Eq(k, 5), 3), sympy.FiniteSet(3, sympy.Eq(k - 5, 0))) == "equivalent"
   assert equivalence(sympy.FiniteSet(sympy.Eq(k, 5), 3), sympy.FiniteSet(3, 5)) == "unsettled"


def test_finite_sets_compare_element_by_element():
   k, m = sympy.symbols("k m")
   key = sympy.FiniteSet(sympy.Eq(k, 5), sympy.Eq(m, -3))
   same = sympy.FiniteSet(sympy.Eq(m + 3, 0), sympy.Eq(k - 5, 0))
   other = sympy.FiniteSet(sympy.Eq(k, 5), sympy.Eq(m, 3))

   assert equivalence(key, same) == "equivalent"
   assert equivalence(key, other) == "not_equivalent"
   assert equivalence(sympy.FiniteSet(1, 2), sympy.FiniteSet(2, 1, 3)) == "not_equivalent"
   assert compare_expressions(key, same) == "equal"
   assert compare_expressions(key, other) == "distinct"


def test_nan_or_an_infinity_against_another_value_is_unsettled_and_against_itself_equivalent():
   """No point evaluates a difference with NaN or an infinity in it, so the comparison has not
   settled, and 04 counts an unsettled comparison as no pass in either direction."""
   assert compare_expressions(sympy.nan, sympy.Integer(3)) == UNSETTLED_VIOLATION
   assert equivalence(sympy.nan, sympy.Integer(3)) == "unsettled"
   assert equivalence(sympy.zoo, sympy.Integer(-1)) == "unsettled"
   assert equivalence(sympy.nan, sympy.nan) == "equivalent"
   assert equivalence(sympy.oo, sympy.oo) == "equivalent"
