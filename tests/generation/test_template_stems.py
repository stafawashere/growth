"""A stem must print the function the template computes. BC-QA-01005 printed a factor x + 3 with
no brackets before sin(1/(x + 3)), so the student read a different function whose limit does not
exist (ITM-GEN-01005-04, retired 2026-09-24)."""
import pytest

from app.generation.templates import qa_01005


@pytest.mark.parametrize("coefficient", [1, -1])
def test_a_linear_factor_with_a_unit_coefficient_is_bracketed(coefficient):
   draw = {"target": -3, "shift": -1, "coefficient": coefficient, "power": 1, "wave": "sin", "naming": "open"}
   stem = qa_01005.build(draw).stem
   function_text = stem.split("f(x) = ")[1].split(r"\sin")[0]

   assert function_text.strip().endswith(r"\right)")
