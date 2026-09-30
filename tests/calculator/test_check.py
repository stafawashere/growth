"""The three-decimal check and the setup check against the rules in docs/calculator/architecture.md."""
import time

import pytest
import sympy

from app.calculator import check, registry
from app.calculator.check import check_setup, check_value
from app.calculator.kit import EQUATION, EXPRESSION, DrillTask, function_entry
from app.items import verify
from app.items.mathjson import from_sympy

KEY = sympy.Float("3.9008765432109876543", 20)
NEGATIVE_KEY = sympy.Float("-2.7182818284590452354", 20)

x = sympy.Symbol("x")
f_expression = sympy.exp(x / 2) + x**3 / 4


def task_for(setup, kind):
   return DrillTask(
      prompt="",
      function_tex="",
      setup_key=from_sympy(setup),
      setup_kind=kind,
      value_key=KEY,
      unit=None,
      radian_sensitive=False,
      draw={"functions": {"f": function_entry(x, f_expression)}},
      exclusion=None,
   )


INTEGRAL_TASK = task_for(sympy.Integral(f_expression, (x, 1, sympy.Rational(5, 2))), EXPRESSION)
DERIVATIVE_TASK = task_for(sympy.Subs(sympy.Derivative(f_expression, x), x, sympy.Rational(13, 10)), EXPRESSION)
EQUATION_TASK = task_for(sympy.Eq(f_expression, 7), EQUATION)


@pytest.mark.parametrize("entered", ["3.901", "3.900", "3.90087", "3.9008765", " 3.901 "])
def test_rounded_truncated_and_longer_entries_are_accurate(entered):
   verdict = check_value(entered, KEY)

   assert verdict.correct is True
   assert verdict.reason is None


def test_both_accepted_forms_come_back_with_every_verdict():
   verdict = check_value("12", KEY)

   assert (verdict.rounded, verdict.truncated) == ("3.901", "3.900")


@pytest.mark.parametrize("entered", ["2.72", "2.7", "3"])
def test_a_short_entry_that_agrees_is_asked_for_three_places(entered):
   verdict = check_value(entered, -NEGATIVE_KEY)

   assert verdict.correct is False
   assert verdict.reason == "not_three_places"


def test_a_short_entry_equal_to_a_padded_accepted_form_is_accurate():
   assert check_value("3.9", KEY).correct is True
   assert check_value("3.90", KEY).correct is True


@pytest.mark.parametrize("entered", ["3.902", "3.899", "3.8", "39.01", "-3.901"])
def test_a_wrong_value_is_outside_tolerance(entered):
   verdict = check_value(entered, KEY)

   assert verdict.correct is False
   assert verdict.reason == "outside_tolerance"


@pytest.mark.parametrize("entered", ["", "   ", None])
def test_a_blank_entry_is_missing(entered):
   assert check_value(entered, KEY).reason == "missing"


@pytest.mark.parametrize("entered", ["abc", "3.9.0", "3.901e0", "+3.901", "3,9 01x", "--3.901"])
def test_anything_but_a_plain_decimal_is_not_a_number(entered):
   verdict = check_value(entered, KEY)

   assert verdict.correct is False
   assert verdict.reason == "not_a_number"


def test_commas_and_spaces_are_stripped_before_parsing():
   key = sympy.Float("1234.5678", 20)

   assert check_value("1,234.567", key).correct is True
   assert check_value("1 234.568", key).correct is True


def test_a_negative_key_rounds_away_from_zero_and_truncates_toward_it():
   verdict = check_value("-2.718", NEGATIVE_KEY)

   assert (verdict.rounded, verdict.truncated) == ("-2.718", "-2.718")
   assert verdict.correct is True
   assert check_value("-2.719", NEGATIVE_KEY).reason == "outside_tolerance"
   assert check_value("-2.7", NEGATIVE_KEY).reason == "not_three_places"


def test_a_negative_key_with_distinct_forms_accepts_both():
   key = sympy.Float("-1.23456", 20)

   assert check_value("-1.235", key).correct is True
   assert check_value("-1.234", key).correct is True
   assert check_value("-1.236", key).reason == "outside_tolerance"


def test_the_forms_come_from_decimal_digits_not_binary_floats():
   key = sympy.Float("2.0005", 20)

   assert (check_value("", key).rounded, check_value("", key).truncated) == ("2.001", "2.000")


def test_an_integer_valued_key_accepts_the_integer_and_its_three_place_form():
   key = sympy.Float(4, 20)

   assert check_value("4", key).correct is True
   assert check_value("4.000", key).correct is True
   assert check_value("4.001", key).reason == "outside_tolerance"


def integral_entry(integrand, low, high):
   return ["Integrate", integrand, ["Tuple", "x", low, high]]


F_OF_X = ["f", "x"]
EXPLICIT_F = ["Add", ["Exp", ["Divide", "x", 2]], ["Divide", ["Power", "x", 3], 4]]


@pytest.mark.parametrize(
   "entered",
   [
      INTEGRAL_TASK.setup_key,
      integral_entry(F_OF_X, 1, 2.5),
      integral_entry(EXPLICIT_F, 1, ["Rational", 5, 2]),
      ["Add", integral_entry(F_OF_X, 1, 2), integral_entry(F_OF_X, 2, 2.5)],
   ],
)
def test_equivalent_integral_setups_are_correct(entered):
   verdict = check_setup(entered, INTEGRAL_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, True, None)


def test_an_integral_over_the_wrong_interval_is_not_equivalent():
   verdict = check_setup(integral_entry(F_OF_X, 1, 3), INTEGRAL_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


def test_a_derivative_at_the_point_is_compared_after_evaluation():
   typed = ["Subs", ["D", F_OF_X, ["Tuple", "x", 1]], ["Tuple", "x"], ["Tuple", 1.3]]
   elsewhere = ["Subs", ["D", F_OF_X, ["Tuple", "x", 1]], ["Tuple", "x"], ["Tuple", 1.4]]

   assert check_setup(typed, DERIVATIVE_TASK).correct is True
   assert check_setup(elsewhere, DERIVATIVE_TASK).reason == "not_equivalent"


@pytest.mark.parametrize(
   "entered",
   [
      ["Equal", F_OF_X, 7],
      ["Equal", 7, F_OF_X],
      ["Equal", ["Subtract", F_OF_X, 7], 0],
      ["Equal", ["Multiply", 2, F_OF_X], 14],
      ["Equal", ["Multiply", -3, EXPLICIT_F], -21],
   ],
)
def test_proportional_equations_are_the_same_setup(entered):
   verdict = check_setup(entered, EQUATION_TASK)

   assert (verdict.correct, verdict.reason) == (True, None)


@pytest.mark.parametrize(
   "entered",
   [
      ["Equal", F_OF_X, 6],
      ["Equal", ["Multiply", 2, F_OF_X], 7],
      ["Subtract", F_OF_X, 7],
   ],
)
def test_a_different_equation_or_a_bare_expression_is_not_equivalent(entered):
   verdict = check_setup(entered, EQUATION_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


@pytest.mark.parametrize("entered", [None, "", [], ["Sequence"], "Nothing"])
def test_nothing_entered_is_missing_and_not_shown(entered):
   verdict = check_setup(entered, INTEGRAL_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (False, None, "missing")


@pytest.mark.parametrize("entered", [["Foo", "x"], ["Integrate"], True])
def test_an_unreadable_entry_is_unsupported_and_counts_as_neither(entered):
   verdict = check_setup(entered, INTEGRAL_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, None, "unsupported")


def _never_settles(*_):
   time.sleep(10)


def test_a_comparison_that_outlives_its_bound_is_unsettled(monkeypatch):
   def bounded_stub(left, right, timeout_s=verify.COMPARISON_TIMEOUT_S):
      return verify.run_bounded(_never_settles, (left, right), 0.2, "unsettled")

   monkeypatch.setattr(check.verify, "equivalence", bounded_stub)
   began = time.monotonic()
   verdict = check_setup(integral_entry(F_OF_X, 1, 2.5), INTEGRAL_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, None, "unsettled")
   assert time.monotonic() - began < 5


def test_the_expected_setup_prints_drawn_decimals_as_decimals():
   verdict = check_setup(None, INTEGRAL_TASK)

   assert "{2.5}" in verdict.key_latex
   assert r"\frac{5}{2}" not in verdict.key_latex
   assert r"\frac{x}{2}" in verdict.key_latex


@pytest.mark.parametrize(
   "entered, task",
   [
      (5.51, INTEGRAL_TASK),
      ({"num": "5.5104371"}, INTEGRAL_TASK),
      (["Negate", 5.51], INTEGRAL_TASK),
      (["Equal", "x", 1.6813], EQUATION_TASK),
      (["Equal", ["Negate", {"num": "1.6813"}], "x"], EQUATION_TASK),
   ],
)
def test_a_bare_number_typed_as_the_setup_is_not_equivalent(entered, task):
   verdict = check_setup(entered, task)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


def test_a_bare_number_equal_to_the_key_value_is_still_not_a_setup():
   key_value = sympy.N(sympy.Integral(f_expression, (x, 1, sympy.Rational(5, 2))), 30)
   verdict = check_setup(float(key_value), INTEGRAL_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


def test_the_solution_typed_as_x_equals_a_number_is_not_the_equation():
   root = float(sympy.nsolve(f_expression - 7, x, 2))
   verdict = check_setup(["Equal", "x", root], EQUATION_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


DRAWN_DERIVATIVE_TASK = registry.draw_task("CDT-derivative-01", "CDT-derivative-01:v1:test:10")
DRAWN_PLOT_TASK = registry.draw_task("CDT-plot-01", "CDT-plot-01:v1:test:0")
DRAWN_VALUE_TASK = registry.draw_task("CDT-value-01", "CDT-value-01:v1:test:0")
SECOND_DERIVATIVE_TASK = task_for(
   sympy.Subs(sympy.Derivative(f_expression, (x, 2)), x, sympy.Rational(13, 10)), EXPRESSION
)
NOT_PURE = "'expected-pure-expression'"


def test_the_drawn_tasks_sit_at_the_points_the_prime_entries_use():
   assert DRAWN_DERIVATIVE_TASK.draw["used_moment"] == "9/2"
   assert DRAWN_VALUE_TASK.draw["used_point"] == "23/5"


@pytest.mark.parametrize(
   "entered",
   [
      ["Multiply", ["Prime", "P"], 4.5],
      ["Apply", ["Prime", "P"], 4.5],
      ["Multiply", ["Prime", "P", 1], 4.5],
   ],
)
def test_a_typed_prime_at_the_point_is_the_derivative_setup(entered):
   verdict = check_setup(entered, DRAWN_DERIVATIVE_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, True, None)


@pytest.mark.parametrize(
   "entered",
   [
      ["Multiply", ["Prime", "P"], 4.6],
      ["Multiply", "P", 4.5],
      ["Multiply", ["Prime", "P", 2], 4.5],
   ],
)
def test_a_prime_at_another_point_the_function_itself_or_a_second_derivative_is_not_equivalent(entered):
   verdict = check_setup(entered, DRAWN_DERIVATIVE_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


@pytest.mark.parametrize(
   "entered",
   [
      ["Equal", ["Error", NOT_PURE, ["Multiply", ["Prime", "f"], "x"]], 0],
      ["Equal", 0, ["Error", NOT_PURE, ["Multiply", ["Prime", "f"], "x"]]],
      ["Equal", ["Error", NOT_PURE, ["Multiply", 3, ["Prime", "f"], "x"]], 0],
      ["Equal", ["Multiply", ["Prime", "f"], "x"], 0],
      ["Equal", ["Apply", ["Prime", "f"], "x"], 0],
      ["Equal", ["Prime", "f"], 0],
   ],
)
def test_a_typed_prime_of_x_equal_to_zero_is_the_critical_point_equation(entered):
   verdict = check_setup(entered, DRAWN_PLOT_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, True, None)


@pytest.mark.parametrize(
   "entered",
   [
      ["Equal", ["Error", NOT_PURE, ["Multiply", ["Prime", "f", 2], "x"]], 0],
      ["Equal", ["Error", NOT_PURE, ["Multiply", ["Prime", "f"], "x"]], 1],
      ["Equal", ["Multiply", "f", "x"], 0],
   ],
)
def test_a_second_derivative_a_nonzero_side_or_the_function_itself_is_not_the_critical_point_equation(entered):
   verdict = check_setup(entered, DRAWN_PLOT_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, False, "not_equivalent")


@pytest.mark.parametrize(
   "entered",
   [
      ["Multiply", ["Prime", "f", 2], 1.3],
      ["Multiply", ["Prime", ["Prime", "f"]], 1.3],
   ],
)
def test_a_double_prime_at_the_point_is_the_second_derivative_setup(entered):
   verdict = check_setup(entered, SECOND_DERIVATIVE_TASK)

   assert (verdict.shown, verdict.correct, verdict.reason) == (True, True, None)


def test_a_function_name_times_the_point_is_the_value_setup():
   typed = ["Multiply", "f", 4.6]
   elsewhere = ["Multiply", "f", 4.7]

   assert check_setup(typed, DRAWN_VALUE_TASK).correct is True
   assert check_setup(elsewhere, DRAWN_VALUE_TASK).reason == "not_equivalent"
