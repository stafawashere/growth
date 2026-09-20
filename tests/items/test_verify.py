"""docs/plan/04-item-generation.md, "Checks on the option set" and "Independent
key verification"; docs/plan/11-phased-delivery.md R9's settle-rate measurement.
"""
import json
from pathlib import Path

from app.items.mathjson import to_sympy
from app.items.verify import distractor_checks, equivalence, verify_item

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
