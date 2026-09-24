"""Blind re-solve of the items_gen_unit02 batch A3 statement items, one formulation per item.

Written from the stems, figures, tables and choices in stems_A3.json alone by claude-opus-5-5 on the
operator's delegation of 2026-09-24, never from a key, a worked solution or a template. Each helper
recomputes the mathematics from the item's own numbers, raises if the chosen choice text disagrees
with that computation, and returns the chosen text. The file reads nothing at run time.
"""
import sympy
from sympy import Abs, Rational, cos, latex, oo, real_root, sin, sqrt

x = sympy.Symbol("x")
step = sympy.Symbol("step", positive=True)

SQUEEZE_SAMPLES = 400
SQUEEZE_TOLERANCE = 1e-12


class ChoiceDisagrees(ValueError):
   pass


def require(condition, message):
   if not condition:
      raise ChoiceDisagrees(message)


def graph_limit(segments, filled_points, at, asks_value, chosen):
   """segments: ((x0, y0), (x1, y1)) pairs as drawn; filled_points: the filled marks."""
   left_limit = [end[1] for start, end in segments if end[0] == at][0]
   right_limit = [start[1] for start, end in segments if start[0] == at][0]
   plotted = [point[1] for point in filled_points if point[0] == at]
   value = int(plotted[0]) if plotted else None
   limit_exists = left_limit == right_limit

   if asks_value:
      value_matches = f"f({at}) = {value} \\)" in chosen
      limit_matches = f"f(x) = {left_limit} \\)" in chosen if limit_exists else "does not exist" in chosen
      require(value_matches and limit_matches, f"limit {left_limit}, {right_limit}, value {value}")

      return chosen

   if limit_exists:
      require(chosen.startswith(f"The limit is {left_limit},"), f"limit {left_limit}")
   else:
      require("approaches different values from the left and from the right" in chosen, f"one sided {left_limit}, {right_limit}")

   return chosen


def side_values(rows, at, from_left):
   side = [row for row in rows if (row[0] < at) == from_left]
   side.sort(key=lambda row: abs(row[0] - at))

   return [row[1] for row in side]


def table_limit(rows, at, chosen):
   sides = [side_values(rows, at, True), side_values(rows, at, False)]

   for values in sides:
      changes_every_step = all(values[index] != values[index + 1] for index in range(len(values) - 1))
      keeps_alternating = len(set(values)) == 2 and changes_every_step

      if keeps_alternating:
         require("keep alternating" in chosen, "outputs alternate")

         return chosen

   for values in sides:
      closing_in = all(abs(values[index] - round(values[0])) <= abs(values[index + 1] - round(values[0])) for index in range(len(values) - 1))
      require(closing_in, "outputs do not settle")

   left_estimate, right_estimate = (round(values[0]) for values in sides)

   if left_estimate != right_estimate:
      require("approach different values on the two sides" in chosen, f"sides {left_estimate}, {right_estimate}")
   else:
      require(chosen.startswith(f"The table suggests that the limit is {left_estimate},") and "from both sides" in chosen, f"limit {left_estimate}")

   return chosen


def squeeze_limit(function, center, lower, upper, chosen):
   for index in range(1, SQUEEZE_SAMPLES):
      for direction in (1, -1):
         point = center + direction * Rational(index, SQUEEZE_SAMPLES - 3)
         function_value = float(function.subs(x, point))
         above_lower = float(lower.subs(x, point)) - SQUEEZE_TOLERANCE <= function_value
         below_upper = function_value <= float(upper.subs(x, point)) + SQUEEZE_TOLERANCE
         require(above_lower and below_upper, f"bounds fail at {point}")

   lower_limit = sympy.limit(lower, x, center)
   upper_limit = sympy.limit(upper, x, center)
   require(lower_limit == upper_limit, "bounds have different limits")

   stated_both_bounds = "both bounds approach" in chosen
   require(chosen.startswith(f"The limit is {lower_limit},") and stated_both_bounds, f"limit {lower_limit}")

   return chosen


def continuity_at(left_piece, right_piece, value, at, chosen):
   left_limit = sympy.limit(left_piece, x, at, "-")
   right_limit = sympy.limit(right_piece, x, at, "+")

   if left_limit != right_limit:
      require(f"from the right are {left_limit} and {right_limit}" in chosen, f"one sided {left_limit}, {right_limit}")
   elif left_limit == value:
      require(chosen.startswith("f is continuous") and f"there is {value}, which equals f({at})" in chosen, "continuous")
   else:
      require(chosen.startswith("f is not continuous") and f"there is {left_limit} while f({at}) = {value}" in chosen, f"limit {left_limit}, value {value}")

   return chosen


def intermediate_value_brackets(rows, left, right, target):
   inside = [row for row in rows if left <= row[0] <= right]
   brackets = []

   for first in inside:
      for second in inside:
         is_later = first[0] < second[0]
         straddles = min(first[1], second[1]) < target < max(first[1], second[1])

         if is_later and straddles:
            brackets.append((first, second))

   return brackets


def ivt_must_exist(rows, left, right, target, chosen):
   brackets = intermediate_value_brackets(rows, left, right, target)

   if not brackets:
      require(chosen.startswith("No."), "no pair of tabulated values straddles the target")

      return chosen

   cites_a_bracket = any(f"f({first[0]}) = {first[1]}" in chosen and f"f({second[0]}) = {second[1]}" in chosen for first, second in brackets)
   uses_continuity = "Since f is differentiable, it is continuous on" in chosen and "Intermediate Value Theorem gives at least one" in chosen
   require(chosen.startswith("Yes.") and cites_a_bracket and uses_continuity, "a tabulated pair straddles the target")

   return chosen


def ivt_from_differentiability(rows, left, right, target, chosen):
   brackets = intermediate_value_brackets(rows, left, right, target)

   if not brackets:
      require(chosen.startswith("No,"), "no pair of tabulated values straddles the target")

      return chosen

   cites_a_bracket = any(f"g({first[0]}) = {first[1]}" in chosen and f"g({second[0]}) = {second[1]}" in chosen for first, second in brackets)
   uses_continuity = "because g is differentiable on" in chosen and "so it is continuous there" in chosen
   require(chosen.startswith("Yes") and cites_a_bracket and uses_continuity, "a tabulated pair straddles the target")

   return chosen


def limit_procedure(expression, point, chosen):
   left_limit = sympy.limit(expression, x, point, "-")
   right_limit = left_limit if point == oo else sympy.limit(expression, x, point, "+")
   is_finite = left_limit == right_limit and left_limit.is_finite

   if is_finite:
      require(chosen.endswith(f"which gives \\( {latex(left_limit)} \\)."), f"limit {left_limit}")
   elif left_limit == right_limit:
      require("check the sign on each side" in chosen and f"\\( {latex(left_limit)} \\) on both sides" in chosen, f"both sides {left_limit}")
   else:
      require("check the sign on each side" in chosen and "no limit exists" in chosen, f"sides {left_limit}, {right_limit}")

   return chosen


def limit_of_differentiable(rows, at, scale, shift, chosen):
   value = [row[1] for row in rows if row[0] == at][0]
   limit = scale * value + shift
   uses_continuity = f"g is differentiable at \\( x = {at} \\), so it is continuous there" in chosen
   require(chosen.startswith(f"The limit is {limit},") and uses_continuity, f"limit {limit}")

   return chosen


def root_differentiability(coefficient, order, power, center, shift, chosen):
   """f(x) = coefficient * (order-th real root of (x - center)) ** power + shift."""
   function = coefficient * real_root(x - center, order) ** power + shift
   right_quotient = (function.subs(x, center + step) - function.subs(x, center)) / step
   left_quotient = (function.subs(x, center - step) - function.subs(x, center)) / (-step)
   right_limit = sympy.limit(sympy.simplify(right_quotient), step, 0)
   left_limit = sympy.limit(sympy.simplify(left_quotient), step, 0)
   both_finite = right_limit.is_finite and left_limit.is_finite

   if both_finite:
      require(left_limit == right_limit, "one sided derivatives differ")
      require(chosen.startswith("f is differentiable") and f"= {left_limit} \\)" in chosen and "approaches 0 from both sides" in chosen, "differentiable")
   elif left_limit == right_limit:
      direction = "positive" if right_limit == oo else "negative"
      require(chosen.startswith("f is not differentiable") and f"staying {direction}, on both sides" in chosen, f"vertical tangent, {direction}")
   else:
      require(chosen.startswith("f is not differentiable") and "opposite signs on the two sides" in chosen, "cusp")

   return chosen


BY_SUFFIX = {
   "02004-00": lambda: limit_of_differentiable([(1, 3, 0), (2, 3, -1), (6, -5, 2), (8, -3, -2)], 2, 3, 5, "The limit is 14, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\)."),
   "02004-01": lambda: ivt_from_differentiability([(4, 3), (5, 1), (8, -9), (9, -8)], 4, 9, 4, "No, because although g is differentiable on \\( [4, 9] \\), so it is continuous there, every tabulated value of g is less than 4."),
   "02004-02": lambda: ivt_from_differentiability([(1, -9), (5, -3), (7, 6), (8, 1)], 1, 8, -8, "Yes, such a c must exist, because g is differentiable on \\( [1, 8] \\), so it is continuous there, and \\( g(1) = -9 < -8 < g(8) = 1 \\)."),
   "02004-03": lambda: limit_of_differentiable([(0, 8, -5), (3, -9, 0), (6, -1, -2), (7, 0, 4)], 3, 3, 4, "The limit is -23, because g is differentiable at \\( x = 3 \\), so it is continuous there, and \\( \\lim_{x \\to 3} g(x) = g(3) = -9 \\)."),
   "02004-04": lambda: limit_of_differentiable([(1, -5, -2), (7, 0, 2), (8, 4, -5), (9, 8, 5)], 7, 3, -8, "The limit is -8, because g is differentiable at \\( x = 7 \\), so it is continuous there, and \\( \\lim_{x \\to 7} g(x) = g(7) = 0 \\)."),
   "02004-05": lambda: ivt_from_differentiability([(1, 5), (4, 2), (5, 7), (8, 3)], 1, 8, -5, "No, because although g is differentiable on \\( [1, 8] \\), so it is continuous there, every tabulated value of g is greater than -5."),
   "02004-06": lambda: limit_of_differentiable([(0, -5, -5), (2, 0, -5), (4, 0, 0), (7, 1, -2)], 2, 3, -4, "The limit is -4, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 0 \\)."),
   "02004-07": lambda: ivt_from_differentiability([(0, 9), (1, -9), (3, -5), (4, -4)], 0, 4, -3, "Yes, such a c must exist, because g is differentiable on \\( [0, 4] \\), so it is continuous there, and \\( g(4) = -4 < -3 < g(0) = 9 \\)."),
   "02004-08": lambda: limit_of_differentiable([(0, 9, -2), (5, -9, -3), (8, -5, -5), (9, 4, -5)], 5, 3, 1, "The limit is -26, because g is differentiable at \\( x = 5 \\), so it is continuous there, and \\( \\lim_{x \\to 5} g(x) = g(5) = -9 \\)."),
   "02004-09": lambda: limit_of_differentiable([(1, 2, 2), (2, 3, -5), (5, -8, 1), (7, -4, -1)], 2, 5, 8, "The limit is 23, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 3 \\)."),
   "02004-10": lambda: limit_of_differentiable([(4, 7, -2), (7, -6, -4), (8, -8, -4), (9, -8, 5)], 7, 3, -7, "The limit is -25, because g is differentiable at \\( x = 7 \\), so it is continuous there, and \\( \\lim_{x \\to 7} g(x) = g(7) = -6 \\)."),
   "02004-11": lambda: ivt_from_differentiability([(0, 3), (5, 9), (6, 6), (7, 5)], 0, 7, -2, "No, because although g is differentiable on \\( [0, 7] \\), so it is continuous there, every tabulated value of g is greater than -2."),
   "02004-12": lambda: ivt_from_differentiability([(1, 7), (4, 0), (6, -3), (8, 0)], 1, 8, -5, "No, because although g is differentiable on \\( [1, 8] \\), so it is continuous there, every tabulated value of g is greater than -5."),
   "02004-13": lambda: ivt_from_differentiability([(0, -6), (1, 3), (3, 6), (4, 2)], 0, 4, -8, "No, because although g is differentiable on \\( [0, 4] \\), so it is continuous there, every tabulated value of g is greater than -8."),
   "02004-14": lambda: limit_of_differentiable([(1, 8, 0), (2, 4, -2), (3, -3, 1), (7, 9, 2)], 2, 3, 7, "The limit is 19, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 4 \\)."),
   "02004-15": lambda: limit_of_differentiable([(1, 1, 3), (2, 9, 3), (3, -7, 3), (7, 6, -1)], 2, 4, 3, "The limit is 39, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = 9 \\)."),
   "02004-16": lambda: limit_of_differentiable([(0, -9, -5), (2, -2, -4), (3, 7, -1), (7, 2, 3)], 2, 5, 9, "The limit is -1, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = -2 \\)."),
   "02004-17": lambda: limit_of_differentiable([(1, 0, 5), (2, -6, -1), (6, -2, 3), (9, 2, 2)], 2, 5, 3, "The limit is -27, because g is differentiable at \\( x = 2 \\), so it is continuous there, and \\( \\lim_{x \\to 2} g(x) = g(2) = -6 \\)."),
   "02004-18": lambda: limit_of_differentiable([(2, -7, 4), (4, -2, 4), (8, -2, 3), (9, 4, 4)], 4, 4, -5, "The limit is -13, because g is differentiable at \\( x = 4 \\), so it is continuous there, and \\( \\lim_{x \\to 4} g(x) = g(4) = -2 \\)."),
   "02004-19": lambda: limit_of_differentiable([(0, 6, 0), (1, -8, -5), (2, -7, 0), (7, 2, 1)], 1, 4, 6, "The limit is -26, because g is differentiable at \\( x = 1 \\), so it is continuous there, and \\( \\lim_{x \\to 1} g(x) = g(1) = -8 \\)."),
   "02004-20": lambda: limit_of_differentiable([(2, -7, -1), (5, 0, 0), (6, -3, -4), (7, -2, 3)], 5, 4, 2, "The limit is 2, because g is differentiable at \\( x = 5 \\), so it is continuous there, and \\( \\lim_{x \\to 5} g(x) = g(5) = 0 \\)."),
   "02004-21": lambda: limit_of_differentiable([(0, -5, 5), (3, 7, 5), (7, 8, -5), (8, 1, 5)], 3, 3, 2, "The limit is 23, because g is differentiable at \\( x = 3 \\), so it is continuous there, and \\( \\lim_{x \\to 3} g(x) = g(3) = 7 \\)."),

   "02005-00": lambda: root_differentiability(-2, 3, 1, -4, -5, "f is not differentiable at \\( x = -4 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-01": lambda: root_differentiability(-1, 5, 1, 2, -5, "f is not differentiable at \\( x = 2 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-02": lambda: root_differentiability(2, 3, 1, -3, 4, "f is not differentiable at \\( x = -3 \\), because the difference quotient grows without bound, staying positive, on both sides, so the graph has a vertical tangent there."),
   "02005-03": lambda: root_differentiability(-2, 5, 1, 0, -2, "f is not differentiable at \\( x = 0 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-04": lambda: root_differentiability(-3, 5, 1, -4, 3, "f is not differentiable at \\( x = -4 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-05": lambda: root_differentiability(-3, 5, 2, 0, 2, "f is not differentiable at \\( x = 0 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there."),
   "02005-06": lambda: root_differentiability(-1, 5, 7, 3, 4, "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the difference quotient approaches 0 from both sides."),
   "02005-07": lambda: root_differentiability(-1, 5, 3, -2, 2, "f is not differentiable at \\( x = -2 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-08": lambda: root_differentiability(-1, 5, 1, 3, 0, "f is not differentiable at \\( x = 3 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-09": lambda: root_differentiability(1, 3, 1, 3, -5, "f is not differentiable at \\( x = 3 \\), because the difference quotient grows without bound, staying positive, on both sides, so the graph has a vertical tangent there."),
   "02005-10": lambda: root_differentiability(-3, 5, 2, 2, 5, "f is not differentiable at \\( x = 2 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there."),
   "02005-11": lambda: root_differentiability(3, 3, 4, 3, -3, "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the difference quotient approaches 0 from both sides."),
   "02005-12": lambda: root_differentiability(1, 5, 4, 1, 4, "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there."),
   "02005-13": lambda: root_differentiability(-2, 3, 1, 3, -5, "f is not differentiable at \\( x = 3 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-14": lambda: root_differentiability(-2, 5, 7, 1, -1, "f is differentiable at \\( x = 1 \\) with \\( f'(1) = 0 \\), because the difference quotient approaches 0 from both sides."),
   "02005-15": lambda: root_differentiability(3, 3, 1, 1, 5, "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound, staying positive, on both sides, so the graph has a vertical tangent there."),
   "02005-16": lambda: root_differentiability(-1, 3, 4, 3, -5, "f is differentiable at \\( x = 3 \\) with \\( f'(3) = 0 \\), because the difference quotient approaches 0 from both sides."),
   "02005-17": lambda: root_differentiability(3, 3, 5, -4, -5, "f is differentiable at \\( x = -4 \\) with \\( f'(-4) = 0 \\), because the difference quotient approaches 0 from both sides."),
   "02005-18": lambda: root_differentiability(-1, 5, 4, 1, -2, "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there."),
   "02005-19": lambda: root_differentiability(-1, 5, 3, -1, -5, "f is not differentiable at \\( x = -1 \\), because the difference quotient grows without bound, staying negative, on both sides, so the graph has a vertical tangent there."),
   "02005-20": lambda: root_differentiability(1, 3, 2, 1, 4, "f is not differentiable at \\( x = 1 \\), because the difference quotient grows without bound with opposite signs on the two sides, so the graph has a cusp there."),
   "02005-21": lambda: root_differentiability(3, 5, 7, -1, 3, "f is differentiable at \\( x = -1 \\) with \\( f'(-1) = 0 \\), because the difference quotient approaches 0 from both sides."),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
