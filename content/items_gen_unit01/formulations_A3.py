"""Blind re-solve of the items_gen_unit01 batch A3 statement items, one formulation per item.

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
   "01001-00": lambda: graph_limit([((0, -2), (3, -1)), ((3, -1), (5, 1)), ((5, -3), (8, 3))], [(0.0, -2.0), (3.0, 1.0), (8.0, 3.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-01": lambda: graph_limit([((0, -3), (2, 1)), ((2, 1), (5, 4)), ((5, 0), (8, -2))], [(0.0, -3.0), (2.0, -1.0), (8.0, -2.0), (5.0, -2.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-02": lambda: graph_limit([((0, 4), (2, 3)), ((2, 3), (6, 2)), ((6, 4), (8, -1))], [(0.0, 4.0), (2.0, 2.0), (8.0, -1.0), (6.0, -1.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),
   "01001-03": lambda: graph_limit([((0, 1), (3, 0)), ((3, 0), (6, 4)), ((6, 0), (8, 3))], [(0.0, 1.0), (3.0, 1.0), (8.0, 3.0)], 3, True, "\\( \\lim_{x \\to 3} f(x) = 0 \\), and \\( f(3) = 1 \\)."),
   "01001-04": lambda: graph_limit([((0, -3), (1, 4)), ((1, 4), (6, 4)), ((6, 2), (8, 2))], [(0.0, -3.0), (1.0, 1.0), (8.0, 2.0), (6.0, -2.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),
   "01001-05": lambda: graph_limit([((0, 1), (1, 2)), ((1, 2), (6, 4)), ((6, 2), (8, 0))], [(0.0, 1.0), (1.0, 3.0), (8.0, 0.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),
   "01001-06": lambda: graph_limit([((0, 2), (2, 4)), ((2, 4), (6, -1)), ((6, 3), (8, -1))], [(0.0, 2.0), (2.0, -2.0), (8.0, -1.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),
   "01001-07": lambda: graph_limit([((0, -2), (2, -2)), ((2, -2), (5, 4)), ((5, -3), (8, -1))], [(0.0, -2.0), (2.0, 3.0), (8.0, -1.0)], 2, True, "\\( \\lim_{x \\to 2} f(x) = -2 \\), and \\( f(2) = 3 \\)."),
   "01001-08": lambda: graph_limit([((0, 1), (3, 1)), ((3, 1), (5, 4)), ((5, 1), (8, 3))], [(0.0, 1.0), (3.0, 3.0), (8.0, 3.0)], 3, True, "\\( \\lim_{x \\to 3} f(x) = 1 \\), and \\( f(3) = 3 \\)."),
   "01001-09": lambda: graph_limit([((0, 2), (1, 4)), ((1, 4), (5, 1)), ((5, -1), (8, 0))], [(0.0, 2.0), (1.0, -1.0), (8.0, 0.0)], 1, True, "\\( \\lim_{x \\to 1} f(x) = 4 \\), and \\( f(1) = -1 \\)."),
   "01001-10": lambda: graph_limit([((0, -3), (3, 1)), ((3, 1), (6, -2)), ((6, 3), (8, 1))], [(0.0, -3.0), (3.0, -1.0), (8.0, 1.0), (6.0, 0.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),
   "01001-11": lambda: graph_limit([((0, 0), (1, 4)), ((1, 4), (5, 1)), ((5, -3), (8, 0))], [(0.0, 0.0), (1.0, -1.0), (8.0, 0.0), (5.0, 0.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-12": lambda: graph_limit([((0, -3), (1, 3)), ((1, 3), (6, 2)), ((6, -1), (8, 2))], [(0.0, -3.0), (1.0, -2.0), (8.0, 2.0), (6.0, -3.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),
   "01001-13": lambda: graph_limit([((0, -2), (2, 3)), ((2, 3), (6, 4)), ((6, 0), (8, -3))], [(0.0, -2.0), (2.0, -1.0), (8.0, -3.0), (6.0, 3.0)], 2, True, "\\( \\lim_{x \\to 2} f(x) = 3 \\), and \\( f(2) = -1 \\)."),
   "01001-14": lambda: graph_limit([((0, -1), (2, 2)), ((2, 2), (5, 0)), ((5, -3), (8, -3))], [(0.0, -1.0), (2.0, -1.0), (8.0, -3.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-15": lambda: graph_limit([((0, 2), (3, -3)), ((3, -3), (6, 3)), ((6, -2), (8, 1))], [(0.0, 2.0), (3.0, 3.0), (8.0, 1.0)], 3, True, "\\( \\lim_{x \\to 3} f(x) = -3 \\), and \\( f(3) = 3 \\)."),
   "01001-16": lambda: graph_limit([((0, 3), (2, 4)), ((2, 4), (6, 0)), ((6, -3), (8, 4))], [(0.0, 3.0), (2.0, -3.0), (8.0, 4.0)], 2, True, "\\( \\lim_{x \\to 2} f(x) = 4 \\), and \\( f(2) = -3 \\)."),
   "01001-17": lambda: graph_limit([((0, -3), (2, 2)), ((2, 2), (5, -3)), ((5, 0), (8, -2))], [(0.0, -3.0), (2.0, 4.0), (8.0, -2.0)], 2, True, "\\( \\lim_{x \\to 2} f(x) = 2 \\), and \\( f(2) = 4 \\)."),
   "01001-18": lambda: graph_limit([((0, -3), (1, 3)), ((1, 3), (5, -3)), ((5, 3), (8, -2))], [(0.0, -3.0), (1.0, -1.0), (8.0, -2.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-19": lambda: graph_limit([((0, 0), (3, -3)), ((3, -3), (5, -1)), ((5, 3), (8, 2))], [(0.0, 0.0), (3.0, -2.0), (8.0, 2.0), (5.0, 0.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-20": lambda: graph_limit([((0, 0), (2, -3)), ((2, -3), (5, 1)), ((5, -3), (8, 4))], [(0.0, 0.0), (2.0, 3.0), (8.0, 4.0)], 5, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5."),
   "01001-21": lambda: graph_limit([((0, 0), (3, -3)), ((3, -3), (6, 2)), ((6, -2), (8, -3))], [(0.0, 0.0), (3.0, 2.0), (8.0, -3.0), (6.0, 4.0)], 6, False, "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6."),

   "01002-00": lambda: table_limit([(0.9999, -4.0), (0.999, 0.0), (0.99, -4.0), (0.9, 0.0), (1.1, -4.0), (1.01, 0.0), (1.001, -4.0), (1.0001, 0.0)], 1, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1."),
   "01002-01": lambda: table_limit([(3.9999, 3.0), (3.999, 6.0), (3.99, 3.0), (3.9, 6.0), (4.1, 3.0), (4.01, 6.0), (4.001, 3.0), (4.0001, 6.0)], 4, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 4."),
   "01002-02": lambda: table_limit([(4.9999, -3.9996), (4.999, -3.996), (4.99, -3.9605), (4.9, -3.65), (5.1, -3.35), (5.01, -3.9305), (5.001, -3.993), (5.0001, -3.9993)], 5, "The table suggests that the limit is -4, because the outputs approach -4 from both sides of x = 5."),
   "01002-03": lambda: table_limit([(0.9999, -3.0), (0.999, 0.0), (0.99, -3.0), (0.9, 0.0), (1.1, -3.0), (1.01, 0.0), (1.001, -3.0), (1.0001, 0.0)], 1, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1."),
   "01002-04": lambda: table_limit([(0.9999, -3.0), (0.999, 6.0), (0.99, -3.0), (0.9, 6.0), (1.1, -3.0), (1.01, 6.0), (1.001, -3.0), (1.0001, 6.0)], 1, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1."),
   "01002-05": lambda: table_limit([(-2.0001, 0.0005), (-2.001, 0.005), (-2.01, 0.0498), (-2.1, 0.48), (-1.9, -0.22), (-1.99, -0.0202), (-1.999, -0.002), (-1.9999, -0.0002)], -2, "The table suggests that the limit is 0, because the outputs approach 0 from both sides of x = -2."),
   "01002-06": lambda: table_limit([(3.9999, 5.0), (3.999, -2.0), (3.99, 5.0), (3.9, -2.0), (4.1, 5.0), (4.01, -2.0), (4.001, 5.0), (4.0001, -2.0)], 4, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 4."),
   "01002-07": lambda: table_limit([(-1.0001, 3.9993), (-1.001, 3.993), (-1.01, 3.9295), (-1.1, 3.25), (-0.9, 3.65), (-0.99, 3.9695), (-0.999, 3.997), (-0.9999, 3.9997)], -1, "The table suggests that the limit is 4, because the outputs approach 4 from both sides of x = -1."),
   "01002-08": lambda: table_limit([(2.9999, 1.0005), (2.999, 1.005), (2.99, 1.0497), (2.9, 1.47), (3.1, 1.67), (3.01, 1.9697), (3.001, 1.997), (3.0001, 1.9997)], 3, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 3."),
   "01002-09": lambda: table_limit([(0.9999, -2.0), (0.999, 2.0), (0.99, -2.0), (0.9, 2.0), (1.1, -2.0), (1.01, 2.0), (1.001, -2.0), (1.0001, 2.0)], 1, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1."),
   "01002-10": lambda: table_limit([(-3.0001, -1.0), (-3.001, 6.0), (-3.01, -1.0), (-3.1, 6.0), (-2.9, -1.0), (-2.99, 6.0), (-2.999, -1.0), (-2.9999, 6.0)], -3, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches -3."),
   "01002-11": lambda: table_limit([(-0.0001, -2.0009), (-0.001, -2.009), (-0.01, -2.0905), (-0.1, -2.95), (0.1, -3.25), (0.01, -3.0205), (0.001, -3.002), (0.0001, -3.0002)], 0, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 0."),
   "01002-12": lambda: table_limit([(-1.0001, 4.0), (-1.001, 2.0), (-1.01, 4.0), (-1.1, 2.0), (-0.9, 4.0), (-0.99, 2.0), (-0.999, 4.0), (-0.9999, 2.0)], -1, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches -1."),
   "01002-13": lambda: table_limit([(4.9999, -2.0), (4.999, 5.0), (4.99, -2.0), (4.9, 5.0), (5.1, -2.0), (5.01, 5.0), (5.001, -2.0), (5.0001, 5.0)], 5, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 5."),
   "01002-14": lambda: table_limit([(2.9999, 4.0001), (2.999, 4.001), (2.99, 4.0101), (2.9, 4.11), (3.1, -4.39), (3.01, -4.0399), (3.001, -4.004), (3.0001, -4.0004)], 3, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 3."),
   "01002-15": lambda: table_limit([(0.9999, 1.9994), (0.999, 1.994), (0.99, 1.9402), (0.9, 1.42), (1.1, 1.82), (1.01, 1.0802), (1.001, 1.008), (1.0001, 1.0008)], 1, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 1."),
   "01002-16": lambda: table_limit([(2.9999, 3.0003), (2.999, 3.003), (2.99, 3.0296), (2.9, 3.26), (3.1, 3.76), (3.01, 3.0796), (3.001, 3.008), (3.0001, 3.0008)], 3, "The table suggests that the limit is 3, because the outputs approach 3 from both sides of x = 3."),
   "01002-17": lambda: table_limit([(2.9999, 3.9992), (2.999, 3.992), (2.99, 3.9195), (2.9, 3.15), (3.1, -0.45), (3.01, -0.0405), (3.001, -0.004), (3.0001, -0.0004)], 3, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 3."),
   "01002-18": lambda: table_limit([(4.9999, 5.0002), (4.999, 5.002), (4.99, 5.02), (4.9, 5.2), (5.1, -2.2), (5.01, -2.02), (5.001, -2.002), (5.0001, -2.0002)], 5, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 5."),
   "01002-19": lambda: table_limit([(-1.0001, 0.9996), (-1.001, 0.996), (-1.01, 0.9595), (-1.1, 0.55), (-0.9, -0.35), (-0.99, -0.0305), (-0.999, -0.003), (-0.9999, -0.0003)], -1, "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = -1."),
   "01002-20": lambda: table_limit([(-2.0001, 1.0004), (-2.001, 1.004), (-2.01, 1.0404), (-2.1, 1.44), (-1.9, 0.74), (-1.99, 0.9704), (-1.999, 0.997), (-1.9999, 0.9997)], -2, "The table suggests that the limit is 1, because the outputs approach 1 from both sides of x = -2."),
   "01002-21": lambda: table_limit([(-0.0001, -2.0), (-0.001, 2.0), (-0.01, -2.0), (-0.1, 2.0), (0.1, -2.0), (0.01, 2.0), (0.001, -2.0), (0.0001, 2.0)], 0, "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 0."),

   "01005-00": lambda: squeeze_limit(-3*(x - 2)**3*sin(1/(x - 2)) - 2, 2, -3*Abs(x - 2)**3 - 2, 3*Abs(x - 2)**3 - 2, "The limit is -2, because \\( -2 - 3 \\left|{x - 2}\\right|^{3} \\le f(x) \\le 3 \\left|{x - 2}\\right|^{3} - 2 \\) for \\( x \\ne 2 \\) and both bounds approach -2 as x approaches 2."),
   "01005-01": lambda: squeeze_limit(-3*x**3*sin(1/x) + 3, 0, 3 - 3*Abs(x)**3, 3*Abs(x)**3 + 3, "The limit is 3, because \\( 3 - 3 \\left|{x}\\right|^{3} \\le f(x) \\le 3 \\left|{x}\\right|^{3} + 3 \\) for \\( x \\ne 0 \\) and both bounds approach 3 as x approaches 0."),
   "01005-02": lambda: squeeze_limit(2*(x + 3)**3*sin(1/(x + 3)), -3, -2*Abs(x + 3)**3, 2*Abs(x + 3)**3, "The limit is 0, because \\( -2 \\left|{x + 3}\\right|^{3} \\le f(x) \\le 2 \\left|{x + 3}\\right|^{3} \\) for \\( x \\ne -3 \\) and both bounds approach 0 as x approaches -3."),
   "01005-03": lambda: squeeze_limit((8 - 4*x)*cos(1/(x - 2)) + 1, 2, 1 - 4*Abs(x - 2), 4*Abs(x - 2) + 1, "The limit is 1, because \\( 1 - 4 \\left|{x - 2}\\right| \\le f(x) \\le 4 \\left|{x - 2}\\right| + 1 \\) for \\( x \\ne 2 \\) and both bounds approach 1 as x approaches 2."),
   "01005-04": lambda: squeeze_limit((x + 3)*sin(1/(x + 3)) - 1, -3, -Abs(x + 3) - 1, Abs(x + 3) - 1, "The limit is -1, because \\( -1 - \\left|{x + 3}\\right| \\le f(x) \\le \\left|{x + 3}\\right| - 1 \\) for \\( x \\ne -3 \\) and both bounds approach -1 as x approaches -3."),
   "01005-05": lambda: squeeze_limit((4*x + 12)*sin(1/(x + 3)) + 1, -3, 1 - 4*Abs(x + 3), 4*Abs(x + 3) + 1, "The limit is 1, because \\( 1 - 4 \\left|{x + 3}\\right| \\le f(x) \\le 4 \\left|{x + 3}\\right| + 1 \\) for \\( x \\ne -3 \\) and both bounds approach 1 as x approaches -3."),
   "01005-06": lambda: squeeze_limit(2*(x + 1)**3*sin(1/(x + 1)) + 5, -1, 5 - 2*Abs(x + 1)**3, 2*Abs(x + 1)**3 + 5, "The limit is 5, because \\( 5 - 2 \\left|{x + 1}\\right|^{3} \\le f(x) \\le 2 \\left|{x + 1}\\right|^{3} + 5 \\) for \\( x \\ne -1 \\) and both bounds approach 5 as x approaches -1."),
   "01005-07": lambda: squeeze_limit(-4*(x + 2)**3*sin(1/(x + 2)) + 2, -2, 2 - 4*Abs(x + 2)**3, 4*Abs(x + 2)**3 + 2, "The limit is 2, because \\( 2 - 4 \\left|{x + 2}\\right|^{3} \\le f(x) \\le 4 \\left|{x + 2}\\right|^{3} + 2 \\) for \\( x \\ne -2 \\) and both bounds approach 2 as x approaches -2."),
   "01005-08": lambda: squeeze_limit((-4*x - 12)*sin(1/(x + 3)) + 2, -3, 2 - 4*Abs(x + 3), 4*Abs(x + 3) + 2, "The limit is 2, because \\( 2 - 4 \\left|{x + 3}\\right| \\le f(x) \\le 4 \\left|{x + 3}\\right| + 2 \\) for \\( x \\ne -3 \\) and both bounds approach 2 as x approaches -3."),
   "01005-09": lambda: squeeze_limit(-(x + 3)**3*sin(1/(x + 3)) - 3, -3, -Abs(x + 3)**3 - 3, Abs(x + 3)**3 - 3, "The limit is -3, because \\( -3 - \\left|{x + 3}\\right|^{3} \\le f(x) \\le \\left|{x + 3}\\right|^{3} - 3 \\) for \\( x \\ne -3 \\) and both bounds approach -3 as x approaches -3."),
   "01005-10": lambda: squeeze_limit((x - 2)**3*cos(1/(x - 2)) + 2, 2, 2 - Abs(x - 2)**3, Abs(x - 2)**3 + 2, "The limit is 2, because \\( 2 - \\left|{x - 2}\\right|^{3} \\le f(x) \\le \\left|{x - 2}\\right|^{3} + 2 \\) for \\( x \\ne 2 \\) and both bounds approach 2 as x approaches 2."),
   "01005-11": lambda: squeeze_limit(2*x**3*sin(1/x) - 1, 0, -2*Abs(x)**3 - 1, 2*Abs(x)**3 - 1, "The limit is -1, because \\( -1 - 2 \\left|{x}\\right|^{3} \\le f(x) \\le 2 \\left|{x}\\right|^{3} - 1 \\) for \\( x \\ne 0 \\) and both bounds approach -1 as x approaches 0."),
   "01005-12": lambda: squeeze_limit(-3*(x + 1)**3*sin(1/(x + 1)) + 2, -1, 2 - 3*Abs(x + 1)**3, 3*Abs(x + 1)**3 + 2, "The limit is 2, because \\( 2 - 3 \\left|{x + 1}\\right|^{3} \\le f(x) \\le 3 \\left|{x + 1}\\right|^{3} + 2 \\) for \\( x \\ne -1 \\) and both bounds approach 2 as x approaches -1."),
   "01005-13": lambda: squeeze_limit(-3*(x + 3)**2*cos(1/(x + 3)) + 1, -3, 1 - 3*(x + 3)**2, 3*(x + 3)**2 + 1, "The limit is 1, because \\( 1 - 3 \\left(x + 3\\right)^{2} \\le f(x) \\le 3 \\left(x + 3\\right)^{2} + 1 \\) for \\( x \\ne -3 \\) and both bounds approach 1 as x approaches -3."),
   "01005-14": lambda: squeeze_limit((2 - 2*x)*cos(1/(x - 1)) - 1, 1, -2*Abs(x - 1) - 1, 2*Abs(x - 1) - 1, "The limit is -1, because \\( -1 - 2 \\left|{x - 1}\\right| \\le f(x) \\le 2 \\left|{x - 1}\\right| - 1 \\) for \\( x \\ne 1 \\) and both bounds approach -1 as x approaches 1."),
   "01005-15": lambda: squeeze_limit(4*(x - 1)**3*cos(1/(x - 1)) - 3, 1, -4*Abs(x - 1)**3 - 3, 4*Abs(x - 1)**3 - 3, "The limit is -3, because \\( -3 - 4 \\left|{x - 1}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 1}\\right|^{3} - 3 \\) for \\( x \\ne 1 \\) and both bounds approach -3 as x approaches 1."),
   "01005-16": lambda: squeeze_limit(-2*(x - 1)**3*sin(1/(x - 1)) + 4, 1, 4 - 2*Abs(x - 1)**3, 2*Abs(x - 1)**3 + 4, "The limit is 4, because \\( 4 - 2 \\left|{x - 1}\\right|^{3} \\le f(x) \\le 2 \\left|{x - 1}\\right|^{3} + 4 \\) for \\( x \\ne 1 \\) and both bounds approach 4 as x approaches 1."),
   "01005-17": lambda: squeeze_limit(-x**2*cos(1/x) - 1, 0, -x**2 - 1, x**2 - 1, "The limit is -1, because \\( -1 - x^{2} \\le f(x) \\le x^{2} - 1 \\) for \\( x \\ne 0 \\) and both bounds approach -1 as x approaches 0."),
   "01005-18": lambda: squeeze_limit((3*x - 6)*cos(1/(x - 2)) + 2, 2, 2 - 3*Abs(x - 2), 3*Abs(x - 2) + 2, "The limit is 2, because \\( 2 - 3 \\left|{x - 2}\\right| \\le f(x) \\le 3 \\left|{x - 2}\\right| + 2 \\) for \\( x \\ne 2 \\) and both bounds approach 2 as x approaches 2."),
   "01005-19": lambda: squeeze_limit(-2*(x - 3)**3*sin(1/(x - 3)) + 2, 3, 2 - 2*Abs(x - 3)**3, 2*Abs(x - 3)**3 + 2, "The limit is 2, because \\( 2 - 2 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 2 \\left|{x - 3}\\right|^{3} + 2 \\) for \\( x \\ne 3 \\) and both bounds approach 2 as x approaches 3."),
   "01005-20": lambda: squeeze_limit(-4*(x - 3)**3*sin(1/(x - 3)), 3, -4*Abs(x - 3)**3, 4*Abs(x - 3)**3, "The limit is 0, because \\( -4 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 3}\\right|^{3} \\) for \\( x \\ne 3 \\) and both bounds approach 0 as x approaches 3."),
   "01005-21": lambda: squeeze_limit(4*(x - 3)**3*sin(1/(x - 3)) + 4, 3, 4 - 4*Abs(x - 3)**3, 4*Abs(x - 3)**3 + 4, "The limit is 4, because \\( 4 - 4 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 3}\\right|^{3} + 4 \\) for \\( x \\ne 3 \\) and both bounds approach 4 as x approaches 3."),

   "01006-00": lambda: continuity_at((2*x**2 - 16*x + 30)/(x - 3), (2*x**2 - 16*x + 30)/(x - 3), 4, 3, "f is not continuous at \\( x = 3 \\), because the limit of f(x) there is -4 while f(3) = 4."),
   "01006-01": lambda: continuity_at((2*x**2 - 7*x + 5)/(x - 1), (2*x**2 - 7*x + 5)/(x - 1), 4, 1, "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is -3 while f(1) = 4."),
   "01006-02": lambda: continuity_at(6 - 2*x, 6 - 3*x, 4, 1, "f is not continuous at \\( x = 1 \\), because the limits from the left and from the right are 4 and 3."),
   "01006-03": lambda: continuity_at((3*x**2 + 16*x + 20)/(x + 2), (3*x**2 + 16*x + 20)/(x + 2), 1, -2, "f is not continuous at \\( x = -2 \\), because the limit of f(x) there is 4 while f(-2) = 1."),
   "01006-04": lambda: continuity_at((-2*x**2 - 2*x)/(x + 1), (-2*x**2 - 2*x)/(x + 1), 3, -1, "f is not continuous at \\( x = -1 \\), because the limit of f(x) there is 2 while f(-1) = 3."),
   "01006-05": lambda: continuity_at((2*x**2 - 16*x + 30)/(x - 3), (2*x**2 - 16*x + 30)/(x - 3), 3, 3, "f is not continuous at \\( x = 3 \\), because the limit of f(x) there is -4 while f(3) = 3."),
   "01006-06": lambda: continuity_at((-x**2 + 5*x - 4)/(x - 1), (-x**2 + 5*x - 4)/(x - 1), 0, 1, "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is 3 while f(1) = 0."),
   "01006-07": lambda: continuity_at((x**2 + 2*x + 1)/(x + 1), (x**2 + 2*x + 1)/(x + 1), 0, -1, "f is continuous at \\( x = -1 \\), because the limit of f(x) there is 0, which equals f(-1)."),
   "01006-08": lambda: continuity_at((x**2 - 2*x + 1)/(x - 1), (x**2 - 2*x + 1)/(x - 1), -4, 1, "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is 0 while f(1) = -4."),
   "01006-09": lambda: continuity_at((2*x**2 + 8*x + 6)/(x + 1), (2*x**2 + 8*x + 6)/(x + 1), 4, -1, "f is continuous at \\( x = -1 \\), because the limit of f(x) there is 4, which equals f(-1)."),
   "01006-10": lambda: continuity_at((-2*x**2 + x)/x, (-2*x**2 + x)/x, 0, 0, "f is not continuous at \\( x = 0 \\), because the limit of f(x) there is 1 while f(0) = 0."),
   "01006-11": lambda: continuity_at((-2*x**2 + 15*x - 27)/(x - 3), (-2*x**2 + 15*x - 27)/(x - 3), 3, 3, "f is continuous at \\( x = 3 \\), because the limit of f(x) there is 3, which equals f(3)."),
   "01006-12": lambda: continuity_at(x + 1, 1 - 3*x, -2, 1, "f is not continuous at \\( x = 1 \\), because the limits from the left and from the right are 2 and -2."),
   "01006-13": lambda: continuity_at((x**2 + 8*x + 12)/(x + 2), (x**2 + 8*x + 12)/(x + 2), -4, -2, "f is not continuous at \\( x = -2 \\), because the limit of f(x) there is 4 while f(-2) = -4."),
   "01006-14": lambda: continuity_at((3*x**2 - 3*x)/x, (3*x**2 - 3*x)/x, -2, 0, "f is not continuous at \\( x = 0 \\), because the limit of f(x) there is -3 while f(0) = -2."),
   "01006-15": lambda: continuity_at((-2*x**2 + 15*x - 27)/(x - 3), (-2*x**2 + 15*x - 27)/(x - 3), 1, 3, "f is not continuous at \\( x = 3 \\), because the limit of f(x) there is 3 while f(3) = 1."),
   "01006-16": lambda: continuity_at((-3*x**2 + 9*x - 6)/(x - 1), (-3*x**2 + 9*x - 6)/(x - 1), -2, 1, "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is 3 while f(1) = -2."),
   "01006-17": lambda: continuity_at(-2*x - 1, -3*x - 4, -1, -1, "f is not continuous at \\( x = -1 \\), because the limits from the left and from the right are 1 and -1."),
   "01006-18": lambda: continuity_at((-3*x**2 + 6*x - 3)/(x - 1), (-3*x**2 + 6*x - 3)/(x - 1), 0, 1, "f is continuous at \\( x = 1 \\), because the limit of f(x) there is 0, which equals f(1)."),
   "01006-19": lambda: continuity_at((2*x**2 - 5*x + 3)/(x - 1), (2*x**2 - 5*x + 3)/(x - 1), -1, 1, "f is continuous at \\( x = 1 \\), because the limit of f(x) there is -1, which equals f(1)."),
   "01006-20": lambda: continuity_at((-3*x**2 + 3*x)/(x - 1), (-3*x**2 + 3*x)/(x - 1), -3, 1, "f is continuous at \\( x = 1 \\), because the limit of f(x) there is -3, which equals f(1)."),
   "01006-21": lambda: continuity_at(4 - 2*x, -2*x - 2, 2, 1, "f is not continuous at \\( x = 1 \\), because the limits from the left and from the right are 2 and -4."),

   "01011-00": lambda: ivt_must_exist([(2, -6), (3, -1), (4, -4), (9, 6)], 2, 9, -2, "Yes. Since f is differentiable, it is continuous on \\( [2, 9] \\), and \\( f(2) = -6 < -2 < f(9) = 6 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-01": lambda: ivt_must_exist([(1, -1), (4, 0), (6, -1), (7, 2)], 1, 7, -2, "No. Every tabulated value of f is greater than -2, so the Intermediate Value Theorem does not apply on \\( [1, 7] \\)."),
   "01011-02": lambda: ivt_must_exist([(0, -9), (2, -8), (6, -1), (7, 5)], 0, 7, -2, "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), and \\( f(0) = -9 < -2 < f(7) = 5 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-03": lambda: ivt_must_exist([(1, -7), (3, -7), (6, 0), (8, -8)], 1, 8, -4, "Yes. Since f is differentiable, it is continuous on \\( [3, 6] \\), and \\( f(3) = -7 < -4 < f(6) = 0 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-04": lambda: ivt_must_exist([(4, 4), (5, -1), (8, -7), (9, -7)], 4, 9, 3, "Yes. Since f is differentiable, it is continuous on \\( [4, 9] \\), and \\( f(9) = -7 < 3 < f(4) = 4 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-05": lambda: ivt_must_exist([(2, 7), (3, -3), (5, 6), (9, -2)], 2, 9, -4, "No. Every tabulated value of f is greater than -4, so the Intermediate Value Theorem does not apply on \\( [2, 9] \\)."),
   "01011-06": lambda: ivt_must_exist([(0, 0), (2, 7), (5, 6), (9, 4)], 0, 9, -3, "No. Every tabulated value of f is greater than -3, so the Intermediate Value Theorem does not apply on \\( [0, 9] \\)."),
   "01011-07": lambda: ivt_must_exist([(1, 2), (2, -1), (5, 6), (7, 8)], 1, 7, 7, "Yes. Since f is differentiable, it is continuous on \\( [1, 7] \\), and \\( f(1) = 2 < 7 < f(7) = 8 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-08": lambda: ivt_must_exist([(0, 7), (2, 8), (3, -6), (6, 2)], 0, 6, 3, "Yes. Since f is differentiable, it is continuous on \\( [0, 6] \\), and \\( f(6) = 2 < 3 < f(0) = 7 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-09": lambda: ivt_must_exist([(3, 0), (4, -4), (8, 4), (9, 4)], 3, 9, -3, "Yes. Since f is differentiable, it is continuous on \\( [4, 8] \\), and \\( f(4) = -4 < -3 < f(8) = 4 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-10": lambda: ivt_must_exist([(0, 5), (4, 9), (6, -4), (7, 5)], 0, 7, -7, "No. Every tabulated value of f is greater than -7, so the Intermediate Value Theorem does not apply on \\( [0, 7] \\)."),
   "01011-11": lambda: ivt_must_exist([(3, 5), (4, 4), (8, -5), (9, -9)], 3, 9, 0, "Yes. Since f is differentiable, it is continuous on \\( [3, 9] \\), and \\( f(9) = -9 < 0 < f(3) = 5 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-12": lambda: ivt_must_exist([(0, -2), (1, 3), (4, 0), (9, 2)], 0, 9, -8, "No. Every tabulated value of f is greater than -8, so the Intermediate Value Theorem does not apply on \\( [0, 9] \\)."),
   "01011-13": lambda: ivt_must_exist([(2, -6), (3, -1), (4, 1), (5, 2)], 2, 5, -4, "Yes. Since f is differentiable, it is continuous on \\( [2, 5] \\), and \\( f(2) = -6 < -4 < f(5) = 2 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-14": lambda: ivt_must_exist([(3, -9), (5, -4), (6, 8), (9, 3)], 3, 9, -5, "Yes. Since f is differentiable, it is continuous on \\( [3, 9] \\), and \\( f(3) = -9 < -5 < f(9) = 3 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-15": lambda: ivt_must_exist([(1, 6), (2, 4), (8, 2), (9, 2)], 1, 9, 3, "Yes. Since f is differentiable, it is continuous on \\( [1, 9] \\), and \\( f(9) = 2 < 3 < f(1) = 6 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-16": lambda: ivt_must_exist([(1, -1), (5, 0), (7, -1), (9, 2)], 1, 9, 5, "No. Every tabulated value of f is less than 5, so the Intermediate Value Theorem does not apply on \\( [1, 9] \\)."),
   "01011-17": lambda: ivt_must_exist([(0, 7), (2, -2), (3, 1), (6, -5)], 0, 6, 5, "Yes. Since f is differentiable, it is continuous on \\( [0, 6] \\), and \\( f(6) = -5 < 5 < f(0) = 7 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-18": lambda: ivt_must_exist([(2, 9), (3, -7), (4, -5), (6, -1)], 2, 6, -6, "Yes. Since f is differentiable, it is continuous on \\( [3, 4] \\), and \\( f(3) = -7 < -6 < f(4) = -5 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-19": lambda: ivt_must_exist([(1, 9), (2, -9), (3, 3), (5, 7)], 1, 5, -1, "Yes. Since f is differentiable, it is continuous on \\( [2, 3] \\), and \\( f(2) = -9 < -1 < f(3) = 3 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-20": lambda: ivt_must_exist([(0, 6), (3, -3), (6, -9), (7, -8)], 0, 7, -4, "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), and \\( f(7) = -8 < -4 < f(0) = 6 \\), so the Intermediate Value Theorem gives at least one such c."),
   "01011-21": lambda: ivt_must_exist([(3, 5), (4, 0), (7, 3), (9, 3)], 3, 9, 2, "Yes. Since f is differentiable, it is continuous on \\( [4, 7] \\), and \\( f(4) = 0 < 2 < f(7) = 3 \\), so the Intermediate Value Theorem gives at least one such c."),

   "01014-00": lambda: limit_procedure((x**2 - 3*x + 2)/(x**2 - x), 1, "Substitution gives 0/0, so factor both parts and cancel \\( x - 1 \\), and then substitute, which gives \\( -1 \\)."),
   "01014-01": lambda: limit_procedure((4*x + 5)/(3*x**2 + 4), oo, "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\)."),
   "01014-02": lambda: limit_procedure((x + 5)/(x - 1), 1, "Substitution gives \\( \\frac{6}{0} \\), so check the sign on each side of \\( x = 1 \\), which gives \\( -\\infty \\) and \\( \\infty \\), so no limit exists."),
   "01014-03": lambda: limit_procedure((sqrt(x + 12) - 3)/(x + 3), -3, "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 12} + 3 \\) and cancel \\( x + 3 \\), and then substitute, which gives \\( \\frac{1}{6} \\)."),
   "01014-04": lambda: limit_procedure((sqrt(x + 7) - 2)/(x + 3), -3, "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 7} + 2 \\) and cancel \\( x + 3 \\), and then substitute, which gives \\( \\frac{1}{4} \\)."),
   "01014-05": lambda: limit_procedure((Rational(1, 4) + 1/x)/(x + 4), -4, "Substitution gives 0/0, so combine the fractions over \\( -4 x \\) and cancel \\( x + 4 \\), and then substitute, which gives \\( - \\frac{1}{16} \\)."),
   "01014-06": lambda: limit_procedure((Rational(1, 5) + 1/x)/(x + 5), -5, "Substitution gives 0/0, so combine the fractions over \\( -5 x \\) and cancel \\( x + 5 \\), and then substitute, which gives \\( - \\frac{1}{25} \\)."),
   "01014-07": lambda: limit_procedure((x**2 - 9*x + 18)/(x**2 - 10*x + 21), 3, "Substitution gives 0/0, so factor both parts and cancel \\( x - 3 \\), and then substitute, which gives \\( \\frac{3}{4} \\)."),
   "01014-08": lambda: limit_procedure((-Rational(1, 2) + 1/x)/(x - 2), 2, "Substitution gives 0/0, so combine the fractions over \\( 2 x \\) and cancel \\( x - 2 \\), and then substitute, which gives \\( - \\frac{1}{4} \\)."),
   "01014-09": lambda: limit_procedure((Rational(1, 3) + 1/x)/(x + 3), -3, "Substitution gives 0/0, so combine the fractions over \\( -3 x \\) and cancel \\( x + 3 \\), and then substitute, which gives \\( - \\frac{1}{9} \\)."),
   "01014-10": lambda: limit_procedure((1 + 1/x)/(x + 1), -1, "Substitution gives 0/0, so combine the fractions over \\( -1 x \\) and cancel \\( x + 1 \\), and then substitute, which gives \\( -1 \\)."),
   "01014-11": lambda: limit_procedure((-Rational(1, 4) + 1/x)/(x - 4), 4, "Substitution gives 0/0, so combine the fractions over \\( 4 x \\) and cancel \\( x - 4 \\), and then substitute, which gives \\( - \\frac{1}{16} \\)."),
   "01014-12": lambda: limit_procedure((sqrt(x + 10) - 3)/(x + 1), -1, "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 10} + 3 \\) and cancel \\( x + 1 \\), and then substitute, which gives \\( \\frac{1}{6} \\)."),
   "01014-13": lambda: limit_procedure((x + 1)/(x - 2)**2, 2, "Substitution gives \\( \\frac{3}{0} \\), so check the sign on each side of \\( x = 2 \\), which gives \\( \\infty \\) on both sides."),
   "01014-14": lambda: limit_procedure((sqrt(x + 6) - 2)/(x + 2), -2, "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 6} + 2 \\) and cancel \\( x + 2 \\), and then substitute, which gives \\( \\frac{1}{4} \\)."),
   "01014-15": lambda: limit_procedure((2*x + 2)/(4*x**2 + 3), oo, "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\)."),
   "01014-16": lambda: limit_procedure((x + 7)/(x - 2), 2, "Substitution gives \\( \\frac{9}{0} \\), so check the sign on each side of \\( x = 2 \\), which gives \\( -\\infty \\) and \\( \\infty \\), so no limit exists."),
   "01014-17": lambda: limit_procedure((4*x + 5)/(x**2 - 5), oo, "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\)."),
   "01014-18": lambda: limit_procedure((x**2 - 4*x - 5)/(x**2 + 6*x + 5), -1, "Substitution gives 0/0, so factor both parts and cancel \\( x + 1 \\), and then substitute, which gives \\( - \\frac{3}{2} \\)."),
   "01014-19": lambda: limit_procedure((2*x - 4)/(6*x**2 + 2), oo, "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\)."),
   "01014-20": lambda: limit_procedure((x**2 + x - 12)/(x**2 + 5*x + 4), -4, "Substitution gives 0/0, so factor both parts and cancel \\( x + 4 \\), and then substitute, which gives \\( \\frac{7}{3} \\)."),
   "01014-21": lambda: limit_procedure((x**2 - 5*x - 6)/(x**2 - x - 2), -1, "Substitution gives 0/0, so factor both parts and cancel \\( x + 1 \\), and then substitute, which gives \\( \\frac{7}{3} \\)."),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
