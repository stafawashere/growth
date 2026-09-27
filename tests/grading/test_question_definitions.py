"""Reading a calculator free-response answer through what its question defines (app/grading/latex.py
with_definitions, app/grading/checks.py QuestionContext and equation_setup).

With the grader off, a setup written with the stem's own function names, a limit written as a
numeric root, and a setup equation whose unknown is a root were all left provisional. Each case
here is decided now where the check can verify it, and stays provisional where it cannot: a name
the question does not define, a limit written to too few places, or an equation the check cannot
match to the reference."""
import pytest
import sympy

from app.grading import checks, latex
from app.grading import point as grader

t = sympy.Symbol("t")
ENTRY_RATE = "120 + 80*sin(t**2/12)"
FIVE_HUNDRED_CARS_AT = "3.455147467946511178034517911"
LABELS = {"BC-PT-99001": grader.DETERMINISTIC}


def line(content):
   return {"kind": "math", "content": content}


def setup_point(point_id, check):
   return {
      "point_id": point_id,
      "point_type_id": "BC-PT-99001",
      "skills": [],
      "criterion": "Writes the setup.",
      "eligible_only_if": [],
      "check": check,
   }


def garage(points_by_part, with_definitions=True):
   record = {
      "id": "FRQ-TEST-DEFS",
      "parts": [
         {"id": part_id, "prompt": "", "setup_required": True, "points": points}
         for part_id, points in points_by_part.items()
      ],
   }

   if with_definitions:
      record["functions"] = {"C": {"variable": "t", "expression": ENTRY_RATE}}
      record["roots"] = {
         "p": {"value": "-LambertW(-1/4)", "equation": "4*x*exp(-x) - 1", "variable": "x"},
         "q": {"value": "-LambertW(-1/4, -1)", "equation": "4*x*exp(-x) - 1", "variable": "x"},
      }

   return record


def decide(record, lines_by_part):
   work = {
      "parts": [
         {"part_id": part_id, "lines": [line(content) for content in lines], "answer": ""}
         for part_id, lines in lines_by_part.items()
      ],
   }
   grading = grader.grade_question(record, work, LABELS, None)

   return {decision.point_id: decision for decision in grading.decisions}


ENTRY_INTEGRAL = {"kind": "bounds_match", "lower": "0", "upper": "4", "integrand": ENTRY_RATE, "variable": "t"}


def test_a_stem_function_name_is_read_through_its_definition():
   definitions = latex.Definitions({"C": (t, sympy.sympify(ENTRY_RATE))})
   read = latex.to_sympy(r"\int_{0}^{4} C(t)\,dt", definitions)

   assert read == sympy.Integral(sympy.sympify(ENTRY_RATE), (t, 0, 4))
   assert latex.to_sympy(r"C'(2)", definitions) == sympy.diff(sympy.sympify(ENTRY_RATE), t).subs(t, 2)


def test_a_capital_name_the_question_does_not_define_is_refused():
   definitions = latex.Definitions({"C": (t, sympy.sympify(ENTRY_RATE))})

   with pytest.raises(latex.Unreadable, match="does not define"):
      latex.to_sympy(r"\int_{0}^{4} G(t)\,dt", definitions)


def test_an_integrand_written_with_the_stem_name_decides_the_setup_point_both_ways():
   record = garage({"a": [setup_point("a1", ENTRY_INTEGRAL)]})

   right = decide(record, {"a": [r"\int_{0}^{4} C(t)\,dt \approx 605.153"]})["a1"]
   wrong_limits = decide(record, {"a": [r"\int_{0}^{5} C(t)\,dt"]})["a1"]

   assert (right.decided_by, right.earned, right.provisional) == (grader.DETERMINISTIC, 1, False)
   assert (wrong_limits.decided_by, wrong_limits.earned) == (grader.DETERMINISTIC, 0)


def test_an_undefined_name_leaves_the_point_provisional_and_never_fails_it():
   record = garage({"a": [setup_point("a1", ENTRY_INTEGRAL)]})

   decision = decide(record, {"a": [r"\int_{0}^{4} G(t)\,dt"]})["a1"]

   assert decision.earned is None
   assert decision.provisional


def test_a_question_without_definitions_reads_as_before():
   record = garage({"a": [setup_point("a1", ENTRY_INTEGRAL)]}, with_definitions=False)

   decision = decide(record, {"a": [r"\int_{0}^{4} C(t)\,dt"]})["a1"]

   assert decision.earned is None


ROOT_LIMITS = {"kind": "bounds_match", "lower": "p", "upper": "q", "integrand": None, "variable": "x"}


@pytest.mark.parametrize("written, earned", [
   (r"\pi\int_{p}^{q} \left(4xe^{-x} - 1\right)^{2}dx", 1),
   (r"\pi\int_{0.357}^{2.153} \left(4xe^{-x} - 1\right)^{2}dx", 1),
   (r"\pi\int_{0.3574}^{2.1532} \left(4xe^{-x} - 1\right)^{2}dx", 1),
   (r"\pi\int_{0.359}^{2.153} \left(4xe^{-x} - 1\right)^{2}dx", 0),
   (r"\pi\int_{0}^{2.153} \left(4xe^{-x} - 1\right)^{2}dx", 0),
])
def test_a_limit_written_as_a_numeric_root_is_checked_to_three_places(written, earned):
   record = garage({"a": [setup_point("a2", ROOT_LIMITS)]})

   decision = decide(record, {"a": [written]})["a2"]

   assert (decision.decided_by, decision.earned) == (grader.DETERMINISTIC, earned)


def test_a_limit_written_to_two_places_stays_provisional():
   record = garage({"a": [setup_point("a2", ROOT_LIMITS)]})

   decision = decide(record, {"a": [r"\pi\int_{0.36}^{2.15} \left(4xe^{-x} - 1\right)^{2}dx"]})["a2"]

   assert decision.earned is None


def test_a_limit_named_by_the_student_takes_the_value_they_set_elsewhere_in_the_question():
   record = garage({"a": [setup_point("a2", ROOT_LIMITS)], "b": []})
   limits = r"\pi\int_{A}^{B} \left(4xe^{-x} - 1\right)^{2}dx"

   set_right = decide(record, {"a": [limits], "b": [r"A \approx 0.357, \quad B \approx 2.153"]})["a2"]
   set_wrong = decide(record, {"a": [limits], "b": [r"A \approx 0.412, \quad B \approx 2.153"]})["a2"]
   never_set = decide(record, {"a": [limits]})["a2"]

   assert set_right.earned == 1
   assert set_wrong.earned == 0
   assert never_set.earned is None


FIVE_HUNDRED_CARS = {
   "kind": "equation_setup",
   "unknown": "T",
   "left": f"Integral({ENTRY_RATE}, (t, 0, T))",
   "right": "500",
   "interval": ["0", "10"],
}


@pytest.mark.parametrize("written", [
   r"\int_{0}^{T} C(t)\,dt = 500",
   r"500 = \int_{0}^{T} \left(120 + 80\sin\left(\frac{t^{2}}{12}\right)\right)dt",
   r"\int_{0}^{x} C(s)\,ds - 500 = 0",
   r"2\int_{0}^{T} C(t)\,dt = 1000",
   r"\int_{0}^{T} C(t)\,dt = 500 \implies T \approx 3.455",
])
def test_a_setup_equation_for_a_numeric_root_is_decided_in_any_equivalent_form(written):
   record = garage({"c": [setup_point("c1", FIVE_HUNDRED_CARS)]})

   decision = decide(record, {"c": [written]})["c1"]

   assert (decision.decided_by, decision.earned, decision.provisional) == (grader.DETERMINISTIC, 1, False)


@pytest.mark.parametrize("written", [
   r"T \approx 3.455",
   r"\int_{0}^{T} C(t)\,dt = 501",
   r"\int_{1}^{T} C(t)\,dt = 500",
   r"\int_{0}^{T} C(t)\,dt = 500T",
   r"\int_{0}^{T} G(t)\,dt = 500",
])
def test_a_setup_equation_the_check_cannot_match_stays_provisional_and_is_never_failed(written):
   record = garage({"c": [setup_point("c1", FIVE_HUNDRED_CARS)]})

   decision = decide(record, {"c": [written]})["c1"]

   assert decision.earned is None
   assert decision.provisional


def test_the_reference_equation_vanishes_at_the_stated_root():
   reference = sympy.Integral(sympy.sympify(ENTRY_RATE), (t, 0, sympy.Float(FIVE_HUNDRED_CARS_AT, 30))) - 500

   assert abs(float(reference.evalf(30))) < 1e-9
   assert checks.CHECKS["equation_setup"] is checks.equation_setup
