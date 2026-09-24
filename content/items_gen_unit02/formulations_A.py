"""Answers to the unit 2 generated items in stems_A.json, computed from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24, from the
stem text, figure tables and choice lists in stems_A.json only, never from a stored key, template
or worked solution. A statement item returns the text of the choice that the computation selects.
"""

import sympy
from sympy import Rational, ln, sqrt

from tools.key_recheck import derivative_by_definition, x

ITEM_PREFIX = "ITM-GEN-"

s = sympy.Symbol("s")
step = sympy.Symbol("step", positive=True)


def single_choice(item_id, predicate):
   matching = [choice for choice in CHOICES_BY_ID[item_id] if predicate(choice)]
   is_unique = len(matching) == 1

   if is_unique:
      return matching[0]

   return matching


def derivative_at_by_definition(expression, at):
   return derivative_by_definition(expression).subs(x, at)


def limit_statement(item_id, expression, variable, point):
   value = sympy.limit(expression, variable, point)
   has_limit = value.is_finite

   if not has_limit:
      return single_choice(item_id, lambda choice: "does not exist" in choice)

   expected_text = f"The limit is \\( {sympy.latex(value)} \\)."

   return single_choice(item_id, lambda choice: choice == expected_text)


def is_differentiable_implies_continuous(choice):
   return "is differentiable" in choice and "so it is continuous there" in choice


def limit_of_linear_in_g(item_id, coefficient, constant, value_at_point):
   """g is differentiable, hence continuous, so the limit of a g(x) + b is a g(c) + b."""
   limit_value = coefficient * value_at_point + constant
   opening = f"The limit is {limit_value}, "

   return single_choice(item_id, lambda choice: choice.startswith(opening) and is_differentiable_implies_continuous(choice))


def must_take_value(item_id, values_by_input, left, right, target):
   """IVT on [left, right] for a differentiable g: some pair of tabulated inputs in the interval must
   bracket the target, otherwise the table does not force such a c."""
   inside = [value for point, value in sorted(values_by_input.items()) if left <= point <= right]
   has_value_at_or_below = any(value <= target for value in inside)
   has_value_at_or_above = any(value >= target for value in inside)
   is_forced = has_value_at_or_below and has_value_at_or_above

   if is_forced:
      return single_choice(item_id, lambda choice: choice.startswith("Yes") and is_differentiable_implies_continuous(choice))

   return single_choice(item_id, lambda choice: choice.startswith("No"))


def root_power_behavior(coefficient, power, root_index):
   """f = coefficient * (root_index-th real root of (x - c))**power + k near x = c, root_index odd.
   Returns the one-sided limits of the difference quotient at c."""
   from_right = sympy.limit(coefficient * step ** Rational(power, root_index) / step, step, 0, "+")
   left_sign = (-1) ** power
   from_left = sympy.limit(coefficient * left_sign * step ** Rational(power, root_index) / (-step), step, 0, "+")

   return from_left, from_right


def differentiability_statement(item_id, coefficient, power, root_index):
   from_left, from_right = root_power_behavior(coefficient, power, root_index)
   both_finite = from_left.is_finite and from_right.is_finite

   if both_finite:
      is_zero_slope = from_left == 0 and from_right == 0

      if not is_zero_slope:
         raise ValueError(f"unexpected finite slope {from_left}, {from_right}")

      return single_choice(item_id, lambda choice: choice.startswith("f is differentiable") and "approaches 0 from both sides" in choice)

   is_vertical_up = from_left == sympy.oo and from_right == sympy.oo
   is_vertical_down = from_left == -sympy.oo and from_right == -sympy.oo

   if is_vertical_up:
      return single_choice(item_id, lambda choice: "vertical tangent" in choice and "staying positive" in choice)

   if is_vertical_down:
      return single_choice(item_id, lambda choice: "vertical tangent" in choice and "staying negative" in choice)

   return single_choice(item_id, lambda choice: "opposite signs" in choice and "cusp" in choice)


CHOICES_BY_ID = {
   "ITM-GEN-02003-00": [
      "The limit does not exist.",
      "The limit is \\( 14 \\).",
      "The limit is \\( \\frac{7}{4} \\).",
      "The limit is \\( \\frac{\\sqrt{14}}{4} \\).",
   ],
   "ITM-GEN-02003-01": [
      "The limit does not exist.",
      "The limit is \\( - 9 \\ln{\\left(4 \\right)} \\).",
      "The limit is \\( - \\frac{9}{4} \\).",
      "The limit is \\( \\frac{1}{\\ln{\\left(4 \\right)}} \\).",
   ],
   "ITM-GEN-02003-02": [
      "The limit does not exist.",
      "The limit is \\( - \\frac{1}{\\ln{\\left(2 \\right)}} \\).",
      "The limit is \\( -14 \\).",
      "The limit is \\( 7 \\ln{\\left(2 \\right)} \\).",
   ],
   "ITM-GEN-02003-03": [
      "The limit does not exist.",
      "The limit is \\( 2 \\ln{\\left(4 \\right)} \\).",
      "The limit is \\( \\frac{1}{2} \\).",
      "The limit is \\( \\frac{1}{\\ln{\\left(4 \\right)}} \\).",
   ],
   "ITM-GEN-02003-04": [
      "The limit does not exist.",
      "The limit is \\( -18 \\).",
      "The limit is \\( 162 \\).",
      "The limit is \\( 9 \\).",
   ],
   "ITM-GEN-02004-00": [
      "The limit is 14, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
      "The limit is 14, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
      "The limit is 14, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
      "The limit is 14, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
   ],
   "ITM-GEN-02004-01": [
      "No, because although g is differentiable on \\( [4, 9] \\), so it is continuous there, every tabulated value of g is less than 4.",
      "Yes, such a c must exist, because g is a function that is continuous on \\( [4, 9] \\), and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is continuous on \\( [4, 9] \\), so it is differentiable there, and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is differentiable on \\( [4, 9] \\), so it is continuous there, and the Intermediate Value Theorem applies.",
   ],
   "ITM-GEN-02004-02": [
      "Yes, such a c must exist, because g is a function that is continuous on \\( [1, 8] \\), and \\( g(1) = -9 < -8 < g(8) = 1 \\).",
      "Yes, such a c must exist, because g is continuous on \\( [1, 8] \\), so it is differentiable there, and \\( g(1) = -9 < -8 < g(8) = 1 \\).",
      "Yes, such a c must exist, because g is differentiable on \\( [1, 8] \\), so it is continuous there, and \\( g(1) = -9 < -8 < g(8) = 1 \\).",
      "Yes, such a c must exist, because the table gives the value of g at each listed input, and \\( g(1) = -9 < -8 < g(8) = 1 \\).",
   ],
   "ITM-GEN-02004-03": [
      "The limit is -23, because g is a function that is continuous at \\( x = 3 \\), and \\( \\lim_{x \\to 3} g(x) = g(3) = -9 \\).",
      "The limit is -23, because g is continuous at \\( x = 3 \\), so it is differentiable there, and \\( \\lim_{x \\to 3} g(x) = g(3) = -9 \\).",
      "The limit is -23, because g is differentiable at \\( x = 3 \\), so it is continuous there, and \\( \\lim_{x \\to 3} g(x) = g(3) = -9 \\).",
      "The limit is -23, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 3} g(x) = g(3) = -9 \\).",
   ],
   "ITM-GEN-02004-04": [
      "The limit is -8, because g is a function that is continuous at \\( x = 7 \\), and \\( \\lim_{x \\to 7} g(x) = g(7) = 0 \\).",
      "The limit is -8, because g is continuous at \\( x = 7 \\), so it is differentiable there, and \\( \\lim_{x \\to 7} g(x) = g(7) = 0 \\).",
      "The limit is -8, because g is differentiable at \\( x = 7 \\), so it is continuous there, and \\( \\lim_{x \\to 7} g(x) = g(7) = 0 \\).",
      "The limit is -8, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 7} g(x) = g(7) = 0 \\).",
   ],
   "ITM-GEN-02004-05": [
      "No, because although g is differentiable on \\( [1, 8] \\), so it is continuous there, every tabulated value of g is greater than -5.",
      "Yes, such a c must exist, because g is a function that is continuous on \\( [1, 8] \\), and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is continuous on \\( [1, 8] \\), so it is differentiable there, and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is differentiable on \\( [1, 8] \\), so it is continuous there, and the Intermediate Value Theorem applies.",
   ],
   "ITM-GEN-02004-06": [
      "The limit is -4, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = 0 \\).",
      "The limit is -4, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 0 \\).",
      "The limit is -4, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 0 \\).",
      "The limit is -4, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = 0 \\).",
   ],
   "ITM-GEN-02004-07": [
      "Yes, such a c must exist, because g is a function that is continuous on \\( [0, 4] \\), and \\( g(4) = -4 < -3 < g(0) = 9 \\).",
      "Yes, such a c must exist, because g is continuous on \\( [0, 4] \\), so it is differentiable there, and \\( g(4) = -4 < -3 < g(0) = 9 \\).",
      "Yes, such a c must exist, because g is differentiable on \\( [0, 4] \\), so it is continuous there, and \\( g(4) = -4 < -3 < g(0) = 9 \\).",
      "Yes, such a c must exist, because the table gives the value of g at each listed input, and \\( g(4) = -4 < -3 < g(0) = 9 \\).",
   ],
   "ITM-GEN-02004-08": [
      "The limit is -26, because g is a function that is continuous at \\( x = 5 \\), and \\( \\lim_{x \\to 5} g(x) = g(5) = -9 \\).",
      "The limit is -26, because g is continuous at \\( x = 5 \\), so it is differentiable there, and \\( \\lim_{x \\to 5} g(x) = g(5) = -9 \\).",
      "The limit is -26, because g is differentiable at \\( x = 5 \\), so it is continuous there, and \\( \\lim_{x \\to 5} g(x) = g(5) = -9 \\).",
      "The limit is -26, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 5} g(x) = g(5) = -9 \\).",
   ],
   "ITM-GEN-02004-09": [
      "The limit is 23, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
      "The limit is 23, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
      "The limit is 23, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
      "The limit is 23, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\).",
   ],
   "ITM-GEN-02004-10": [
      "The limit is -25, because g is a function that is continuous at \\( x = 7 \\), and \\( \\lim_{x \\to 7} g(x) = g(7) = -6 \\).",
      "The limit is -25, because g is continuous at \\( x = 7 \\), so it is differentiable there, and \\( \\lim_{x \\to 7} g(x) = g(7) = -6 \\).",
      "The limit is -25, because g is differentiable at \\( x = 7 \\), so it is continuous there, and \\( \\lim_{x \\to 7} g(x) = g(7) = -6 \\).",
      "The limit is -25, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 7} g(x) = g(7) = -6 \\).",
   ],
   "ITM-GEN-02004-11": [
      "No, because although g is differentiable on \\( [0, 7] \\), so it is continuous there, every tabulated value of g is greater than -2.",
      "Yes, such a c must exist, because g is a function that is continuous on \\( [0, 7] \\), and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is continuous on \\( [0, 7] \\), so it is differentiable there, and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is differentiable on \\( [0, 7] \\), so it is continuous there, and the Intermediate Value Theorem applies.",
   ],
   "ITM-GEN-02004-12": [
      "No, because although g is differentiable on \\( [1, 8] \\), so it is continuous there, every tabulated value of g is greater than -5.",
      "Yes, such a c must exist, because g is a function that is continuous on \\( [1, 8] \\), and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is continuous on \\( [1, 8] \\), so it is differentiable there, and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is differentiable on \\( [1, 8] \\), so it is continuous there, and the Intermediate Value Theorem applies.",
   ],
   "ITM-GEN-02004-13": [
      "No, because although g is differentiable on \\( [0, 4] \\), so it is continuous there, every tabulated value of g is greater than -8.",
      "Yes, such a c must exist, because g is a function that is continuous on \\( [0, 4] \\), and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is continuous on \\( [0, 4] \\), so it is differentiable there, and the Intermediate Value Theorem applies.",
      "Yes, such a c must exist, because g is differentiable on \\( [0, 4] \\), so it is continuous there, and the Intermediate Value Theorem applies.",
   ],
   "ITM-GEN-02004-14": [
      "The limit is 19, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = 4 \\).",
      "The limit is 19, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 4 \\).",
      "The limit is 19, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 4 \\).",
      "The limit is 19, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = 4 \\).",
   ],
   "ITM-GEN-02004-15": [
      "The limit is 39, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = 9 \\).",
      "The limit is 39, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 9 \\).",
      "The limit is 39, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 9 \\).",
      "The limit is 39, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = 9 \\).",
   ],
   "ITM-GEN-02004-16": [
      "The limit is -1, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = -2 \\).",
      "The limit is -1, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = -2 \\).",
      "The limit is -1, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = -2 \\).",
      "The limit is -1, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = -2 \\).",
   ],
   "ITM-GEN-02004-17": [
      "The limit is -27, because g is a function that is continuous at \\( x = 2 \\), and \\( \\lim_{x \\to 2} g(x) = g(2) = -6 \\).",
      "The limit is -27, because g is continuous at \\( x = 2 \\), so it is differentiable there, and \\( \\lim_{x \\to 2} g(x) = g(2) = -6 \\).",
      "The limit is -27, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = -6 \\).",
      "The limit is -27, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 2} g(x) = g(2) = -6 \\).",
   ],
   "ITM-GEN-02004-18": [
      "The limit is -13, because g is a function that is continuous at \\( x = 4 \\), and \\( \\lim_{x \\to 4} g(x) = g(4) = -2 \\).",
      "The limit is -13, because g is continuous at \\( x = 4 \\), so it is differentiable there, and \\( \\lim_{x \\to 4} g(x) = g(4) = -2 \\).",
      "The limit is -13, because g is differentiable at \\( x = 4 \\), so it is continuous there, and \\( \\lim_{x \\to 4} g(x) = g(4) = -2 \\).",
      "The limit is -13, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 4} g(x) = g(4) = -2 \\).",
   ],
   "ITM-GEN-02004-19": [
      "The limit is -26, because g is a function that is continuous at \\( x = 1 \\), and \\( \\lim_{x \\to 1} g(x) = g(1) = -8 \\).",
      "The limit is -26, because g is continuous at \\( x = 1 \\), so it is differentiable there, and \\( \\lim_{x \\to 1} g(x) = g(1) = -8 \\).",
      "The limit is -26, because g is differentiable at \\( x = 1 \\), so it is continuous there, and \\( \\lim_{x \\to 1} g(x) = g(1) = -8 \\).",
      "The limit is -26, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 1} g(x) = g(1) = -8 \\).",
   ],
   "ITM-GEN-02004-20": [
      "The limit is 2, because g is a function that is continuous at \\( x = 5 \\), and \\( \\lim_{x \\to 5} g(x) = g(5) = 0 \\).",
      "The limit is 2, because g is continuous at \\( x = 5 \\), so it is differentiable there, and \\( \\lim_{x \\to 5} g(x) = g(5) = 0 \\).",
      "The limit is 2, because g is differentiable at \\( x = 5 \\), so it is continuous there, and \\( \\lim_{x \\to 5} g(x) = g(5) = 0 \\).",
      "The limit is 2, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 5} g(x) = g(5) = 0 \\).",
   ],
   "ITM-GEN-02004-21": [
      "The limit is 23, because g is a function that is continuous at \\( x = 3 \\), and \\( \\lim_{x \\to 3} g(x) = g(3) = 7 \\).",
      "The limit is 23, because g is continuous at \\( x = 3 \\), so it is differentiable there, and \\( \\lim_{x \\to 3} g(x) = g(3) = 7 \\).",
      "The limit is 23, because g is differentiable at \\( x = 3 \\), so it is continuous there, and \\( \\lim_{x \\to 3} g(x) = g(3) = 7 \\).",
      "The limit is 23, because the table gives the value of g at each listed input, and \\( \\lim_{x \\to 3} g(x) = g(3) = 7 \\).",
   ],
   "ITM-GEN-02005-00": [
      "f is differentiable at \\( x = -4 \\) with \\( f'(-4) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = -4 \\), because f is continuous at \\( x = -4 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -4 \\), because a sketch of the graph of f shows a corner at \\( x = -4 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = -4 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-01": [
      "f is differentiable at \\( x = 2 \\) with \\( f'(2) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 2 \\), because f is continuous at \\( x = 2 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 2 \\), because a sketch of the graph of f shows a corner at \\( x = 2 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 2 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-02": [
      "f is differentiable at \\( x = -3 \\) with \\( f'(-3) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = -3 \\), because f is continuous at \\( x = -3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -3 \\), because a sketch of the graph of f shows a corner at \\( x = -3 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = -3 \\), because the difference quotient grows without bound, staying positive, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-03": [
      "f is differentiable at \\( x = 0 \\) with \\( f'(0) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 0 \\), because f is continuous at \\( x = 0 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 0 \\), because a sketch of the graph of f shows a corner at \\( x = 0 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 0 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-04": [
      "f is differentiable at \\( x = -4 \\) with \\( f'(-4) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = -4 \\), because f is continuous at \\( x = -4 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -4 \\), because a sketch of the graph of f shows a corner at \\( x = -4 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = -4 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-05": [
      "f is differentiable at \\( x = 0 \\) with \\( f'(0) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 0 \\), because f is continuous at \\( x = 0 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 0 \\), because a sketch of the graph of f shows a corner at \\( x = 0 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 0 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there.",
   ],
   "ITM-GEN-02005-06": [
      "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the difference quotient approaches 0 from both sides.",
      "f is differentiable at \\( x = 3 \\), because f is continuous at \\( x = 3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 3 \\), because \\( f'(x) = - \\frac{7}{5}\\left(\\sqrt[5]{x - 3}\\right)^{2} \\) is 0 there, so the tangent is vertical.",
      "f is not differentiable at \\( x = 3 \\), because a sketch of the graph of f shows a sharp point at \\( x = 3 \\), where the root is 0.",
   ],
   "ITM-GEN-02005-07": [
      "f is differentiable at \\( x = -2 \\) with \\( f'(-2) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = -2 \\), because f is continuous at \\( x = -2 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -2 \\), because a sketch of the graph of f shows a corner at \\( x = -2 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = -2 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-08": [
      "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 3 \\), because f is continuous at \\( x = 3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 3 \\), because a sketch of the graph of f shows a corner at \\( x = 3 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 3 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-09": [
      "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 3 \\), because f is continuous at \\( x = 3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 3 \\), because a sketch of the graph of f shows a corner at \\( x = 3 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 3 \\), because the difference quotient grows without bound, staying positive, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-10": [
      "f is differentiable at \\( x = 2 \\) with \\( f'(2) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 2 \\), because f is continuous at \\( x = 2 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 2 \\), because a sketch of the graph of f shows a corner at \\( x = 2 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 2 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there.",
   ],
   "ITM-GEN-02005-11": [
      "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the difference quotient approaches 0 from both sides.",
      "f is differentiable at \\( x = 3 \\), because f is continuous at \\( x = 3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 3 \\), because \\( f'(x) = 4\\sqrt[3]{x - 3} \\) is 0 there, so the tangent is vertical.",
      "f is not differentiable at \\( x = 3 \\), because a sketch of the graph of f shows a sharp point at \\( x = 3 \\), where the root is 0.",
   ],
   "ITM-GEN-02005-12": [
      "f is differentiable at \\( x = 1 \\) with \\( f'(1) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 1 \\), because f is continuous at \\( x = 1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 1 \\), because a sketch of the graph of f shows a corner at \\( x = 1 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there.",
   ],
   "ITM-GEN-02005-13": [
      "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 3 \\), because f is continuous at \\( x = 3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 3 \\), because a sketch of the graph of f shows a corner at \\( x = 3 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 3 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-14": [
      "f is differentiable at \\( x = 1 \\) with \\( f'(1) = 0 \\), because the difference quotient approaches 0 from both sides.",
      "f is differentiable at \\( x = 1 \\), because f is continuous at \\( x = 1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 1 \\), because \\( f'(x) = - \\frac{14}{5}\\left(\\sqrt[5]{x - 1}\\right)^{2} \\) is 0 there, so the tangent is vertical.",
      "f is not differentiable at \\( x = 1 \\), because a sketch of the graph of f shows a sharp point at \\( x = 1 \\), where the root is 0.",
   ],
   "ITM-GEN-02005-15": [
      "f is differentiable at \\( x = 1 \\) with \\( f'(1) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 1 \\), because f is continuous at \\( x = 1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 1 \\), because a sketch of the graph of f shows a corner at \\( x = 1 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound, staying positive, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-16": [
      "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the difference quotient approaches 0 from both sides.",
      "f is differentiable at \\( x = 3 \\), because f is continuous at \\( x = 3 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 3 \\), because \\( f'(x) = - \\frac{4}{3}\\sqrt[3]{x - 3} \\) is 0 there, so the tangent is vertical.",
      "f is not differentiable at \\( x = 3 \\), because a sketch of the graph of f shows a sharp point at \\( x = 3 \\), where the root is 0.",
   ],
   "ITM-GEN-02005-17": [
      "f is differentiable at \\( x = -4 \\) with \\( f'(-4) = 0 \\), because the difference quotient approaches 0 from both sides.",
      "f is differentiable at \\( x = -4 \\), because f is continuous at \\( x = -4 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -4 \\), because \\( f'(x) = 5\\left(\\sqrt[3]{x + 4}\\right)^{2} \\) is 0 there, so the tangent is vertical.",
      "f is not differentiable at \\( x = -4 \\), because a sketch of the graph of f shows a sharp point at \\( x = -4 \\), where the root is 0.",
   ],
   "ITM-GEN-02005-18": [
      "f is differentiable at \\( x = 1 \\) with \\( f'(1) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 1 \\), because f is continuous at \\( x = 1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 1 \\), because a sketch of the graph of f shows a corner at \\( x = 1 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there.",
   ],
   "ITM-GEN-02005-19": [
      "f is differentiable at \\( x = -1 \\) with \\( f'(-1) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = -1 \\), because f is continuous at \\( x = -1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -1 \\), because a sketch of the graph of f shows a corner at \\( x = -1 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = -1 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there.",
   ],
   "ITM-GEN-02005-20": [
      "f is differentiable at \\( x = 1 \\) with \\( f'(1) = 0 \\), because the derivative formula has a zero denominator there, so the tangent is horizontal.",
      "f is differentiable at \\( x = 1 \\), because f is continuous at \\( x = 1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = 1 \\), because a sketch of the graph of f shows a corner at \\( x = 1 \\), where two straight pieces meet.",
      "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there.",
   ],
   "ITM-GEN-02005-21": [
      "f is differentiable at \\( x = -1 \\) with \\( f'(-1) = 0 \\), because the difference quotient approaches 0 from both sides.",
      "f is differentiable at \\( x = -1 \\), because f is continuous at \\( x = -1 \\), so the difference quotient has a limit there.",
      "f is not differentiable at \\( x = -1 \\), because \\( f'(x) = \\frac{21}{5}\\left(\\sqrt[5]{x + 1}\\right)^{2} \\) is 0 there, so the tangent is vertical.",
      "f is not differentiable at \\( x = -1 \\), because a sketch of the graph of f shows a sharp point at \\( x = -1 \\), where the root is 0.",
   ],
}

BY_SUFFIX = {
   "02002-00": lambda: derivative_at_by_definition(x**3 + 6*x + 9, 2),
   "02002-01": lambda: derivative_at_by_definition(-3*x**3 - 5*x - 5, -2),
   "02002-02": lambda: derivative_at_by_definition(2*x**2 - 5*x - 4, -3),
   "02002-03": lambda: derivative_at_by_definition(-2*x**3 + x - 1, 2),
   "02002-04": lambda: derivative_at_by_definition(3*x**2 - 2*x - 6, -1),
   "02002-05": lambda: derivative_at_by_definition(-2*x**3 - 5*x + 5, -2),
   "02002-06": lambda: derivative_at_by_definition(-3*x**2 + 5*x, 3),
   "02002-07": lambda: derivative_at_by_definition(3*x**3 + 2*x - 1, 3),
   "02002-08": lambda: derivative_at_by_definition(x**3 - 5*x - 2, -1),
   "02002-09": lambda: derivative_at_by_definition(-x**2 - 5*x - 4, -2),
   "02002-10": lambda: derivative_at_by_definition(-2*x**3 - 6*x - 4, -1),
   "02002-11": lambda: derivative_at_by_definition(-3*x**2 + 4*x + 7, 2),

   "02003-00": lambda: limit_statement("ITM-GEN-02003-00", (7*sqrt(x) - 14) / (x - 4), x, 4),
   "02003-01": lambda: limit_statement("ITM-GEN-02003-01", (-9*ln(s + 4) + 9*ln(4)) / s, s, 0),
   "02003-02": lambda: limit_statement("ITM-GEN-02003-02", (-7*ln(s + Rational(1, 2)) - 7*ln(2)) / s, s, 0),
   "02003-03": lambda: limit_statement("ITM-GEN-02003-03", (2*ln(x) - 2*ln(4)) / (x - 4), x, 4),
   "02003-04": lambda: limit_statement("ITM-GEN-02003-04", (9*x**2 - 9) / (x + 1), x, -1),

   "02004-00": lambda: limit_of_linear_in_g("ITM-GEN-02004-00", 3, 5, 3),
   "02004-01": lambda: must_take_value("ITM-GEN-02004-01", {4: 3, 5: 1, 8: -9, 9: -8}, 4, 9, 4),
   "02004-02": lambda: must_take_value("ITM-GEN-02004-02", {1: -9, 5: -3, 7: 6, 8: 1}, 1, 8, -8),
   "02004-03": lambda: limit_of_linear_in_g("ITM-GEN-02004-03", 3, 4, -9),
   "02004-04": lambda: limit_of_linear_in_g("ITM-GEN-02004-04", 3, -8, 0),
   "02004-05": lambda: must_take_value("ITM-GEN-02004-05", {1: 5, 4: 2, 5: 7, 8: 3}, 1, 8, -5),
   "02004-06": lambda: limit_of_linear_in_g("ITM-GEN-02004-06", 3, -4, 0),
   "02004-07": lambda: must_take_value("ITM-GEN-02004-07", {0: 9, 1: -9, 3: -5, 4: -4}, 0, 4, -3),
   "02004-08": lambda: limit_of_linear_in_g("ITM-GEN-02004-08", 3, 1, -9),
   "02004-09": lambda: limit_of_linear_in_g("ITM-GEN-02004-09", 5, 8, 3),
   "02004-10": lambda: limit_of_linear_in_g("ITM-GEN-02004-10", 3, -7, -6),
   "02004-11": lambda: must_take_value("ITM-GEN-02004-11", {0: 3, 5: 9, 6: 6, 7: 5}, 0, 7, -2),
   "02004-12": lambda: must_take_value("ITM-GEN-02004-12", {1: 7, 4: 0, 6: -3, 8: 0}, 1, 8, -5),
   "02004-13": lambda: must_take_value("ITM-GEN-02004-13", {0: -6, 1: 3, 3: 6, 4: 2}, 0, 4, -8),
   "02004-14": lambda: limit_of_linear_in_g("ITM-GEN-02004-14", 3, 7, 4),
   "02004-15": lambda: limit_of_linear_in_g("ITM-GEN-02004-15", 4, 3, 9),
   "02004-16": lambda: limit_of_linear_in_g("ITM-GEN-02004-16", 5, 9, -2),
   "02004-17": lambda: limit_of_linear_in_g("ITM-GEN-02004-17", 5, 3, -6),
   "02004-18": lambda: limit_of_linear_in_g("ITM-GEN-02004-18", 4, -5, -2),
   "02004-19": lambda: limit_of_linear_in_g("ITM-GEN-02004-19", 4, 6, -8),
   "02004-20": lambda: limit_of_linear_in_g("ITM-GEN-02004-20", 4, 2, 0),
   "02004-21": lambda: limit_of_linear_in_g("ITM-GEN-02004-21", 3, 2, 7),

   "02005-00": lambda: differentiability_statement("ITM-GEN-02005-00", -2, 1, 3),
   "02005-01": lambda: differentiability_statement("ITM-GEN-02005-01", -1, 1, 5),
   "02005-02": lambda: differentiability_statement("ITM-GEN-02005-02", 2, 1, 3),
   "02005-03": lambda: differentiability_statement("ITM-GEN-02005-03", -2, 1, 5),
   "02005-04": lambda: differentiability_statement("ITM-GEN-02005-04", -3, 1, 5),
   "02005-05": lambda: differentiability_statement("ITM-GEN-02005-05", -3, 2, 5),
   "02005-06": lambda: differentiability_statement("ITM-GEN-02005-06", -1, 7, 5),
   "02005-07": lambda: differentiability_statement("ITM-GEN-02005-07", -1, 3, 5),
   "02005-08": lambda: differentiability_statement("ITM-GEN-02005-08", -1, 1, 5),
   "02005-09": lambda: differentiability_statement("ITM-GEN-02005-09", 1, 1, 3),
   "02005-10": lambda: differentiability_statement("ITM-GEN-02005-10", -3, 2, 5),
   "02005-11": lambda: differentiability_statement("ITM-GEN-02005-11", 3, 4, 3),
   "02005-12": lambda: differentiability_statement("ITM-GEN-02005-12", 1, 4, 5),
   "02005-13": lambda: differentiability_statement("ITM-GEN-02005-13", -2, 1, 3),
   "02005-14": lambda: differentiability_statement("ITM-GEN-02005-14", -2, 7, 5),
   "02005-15": lambda: differentiability_statement("ITM-GEN-02005-15", 3, 1, 3),
   "02005-16": lambda: differentiability_statement("ITM-GEN-02005-16", -1, 4, 3),
   "02005-17": lambda: differentiability_statement("ITM-GEN-02005-17", 3, 5, 3),
   "02005-18": lambda: differentiability_statement("ITM-GEN-02005-18", -1, 4, 5),
   "02005-19": lambda: differentiability_statement("ITM-GEN-02005-19", -1, 3, 5),
   "02005-20": lambda: differentiability_statement("ITM-GEN-02005-20", 1, 2, 3),
   "02005-21": lambda: differentiability_statement("ITM-GEN-02005-21", 3, 7, 5),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
