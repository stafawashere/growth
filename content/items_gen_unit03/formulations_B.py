"""Answers to the unit 3 generated items in stems_B.json, computed from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24, from the
stem text, figure tables, graph vertices and choice lists in stems_B.json only, never from a stored
key, template or worked solution. A statement item returns the text of the choice whose set of
points equals the computed set.
"""
import re

import sympy
from sympy import Rational, asin, atan, exp, sqrt

from tools.key_recheck import (
   derivative,
   horizontal_tangent_points,
   implicit_slope,
   second_derivative_along_solution,
   x,
   y,
)

ITEM_PREFIX = "ITM-GEN-"
POINT_PATTERN = re.compile(r"\((-?\d+), (-?\d+)\)")

unknown_slope = sympy.Symbol("unknown_slope")


def exact_derivative_value(expression, at):
   value = sympy.simplify(derivative(expression).subs(x, at))
   is_real = value.is_real

   if not is_real:
      raise ValueError(f"h'({at}) = {value} is not real, so {expression} is undefined near {at}")

   return value


def composite_slope_from_table(table, at):
   """table[x] = (outer(x), outer'(x), inner(x), inner'(x)); h = outer(inner(x))."""
   inner_value = table[at][2]
   inner_slope = table[at][3]
   outer_slope_at_inner = table[inner_value][1]

   return sympy.Integer(outer_slope_at_inner * inner_slope)


def missing_inner_slope(table, at, composite_slope):
   inner_value = table[at][2]
   outer_slope_at_inner = table[inner_value][1]
   solutions = sympy.solve(sympy.Eq(outer_slope_at_inner * unknown_slope, composite_slope), unknown_slope)
   is_unique = len(solutions) == 1

   if is_unique:
      return solutions[0]

   return solutions


def segment_containing(vertices, at):
   for (left_x, left_y), (right_x, right_y) in zip(vertices, vertices[1:]):
      is_interior = left_x < at < right_x

      if is_interior:
         slope = Rational(right_y - left_y, right_x - left_x)
         value = left_y + slope * (at - left_x)

         return value, slope

   raise ValueError(f"{at} is a vertex or outside the graph, so the slope there is not one number")


def composite_slope_from_graphs(outer_vertices, inner_vertices, at):
   """h = outer(inner(x)) with both graphs polygonal; the chain rule at a point inside a segment of
   the inner graph whose value lands inside a segment of the outer graph."""
   inner_value, inner_slope = segment_containing(inner_vertices, at)
   inner_is_flat = inner_slope == 0

   if inner_is_flat:
      return sympy.Integer(0)

   _, outer_slope = segment_containing(outer_vertices, inner_value)

   return outer_slope * inner_slope


def slope_on_curve(left_side, right_side, point):
   curve = left_side - right_side
   at_point = {x: point[0], y: point[1]}
   on_curve = sympy.simplify(curve.subs(at_point)) == 0

   if not on_curve:
      raise ValueError(f"{point} is not on the curve")

   return sympy.simplify(implicit_slope(curve).subs(at_point))


def horizontal_tangent_statement(item_id, scale, y_center, double_root, simple_root):
   """scale (y - y_center)^2 = (x - double_root)^2 (x - simple_root): the real points where the
   x-partial vanishes and the y-partial does not."""
   curve = scale * (y - y_center) ** 2 - (x - double_root) ** 2 * (x - simple_root)
   computed = {(int(px), int(py)) for px, py in horizontal_tangent_points(curve)}

   def names_computed_points(choice):
      named = {(int(px), int(py)) for px, py in POINT_PATTERN.findall(choice)}

      return named == computed

   matching = [choice for choice in CHOICES_BY_ID[item_id] if names_computed_points(choice)]
   is_unique = len(matching) == 1

   if is_unique:
      return matching[0]

   return matching


def inverse_slope_from_table(table, at):
   """table[x] = (p(x), p'(x)); q = p inverse, so q'(at) = 1 / p'(x0) where p(x0) = at."""
   preimages = [point for point, (value, _) in table.items() if value == at]
   has_one_preimage = len(preimages) == 1

   if not has_one_preimage:
      raise ValueError(f"the table has {len(preimages)} inputs where p = {at}")

   return Rational(1, table[preimages[0]][1])


def second_derivative_at(slope_field, point):
   return second_derivative_along_solution(slope_field).subs({x: point[0], y: point[1]})


CHOICES_BY_ID = {
   "ITM-GEN-03005-00": [
      "The tangent line is horizontal at \\( (-13, 20) \\) and \\( (-13, -12) \\).",
      "The tangent line is horizontal at \\( (-5, 4) \\) and \\( (-13, 4) \\).",
      "The tangent line is horizontal at \\( (-5, 4) \\) and \\( (-17, 4) \\).",
      "The tangent line is horizontal at \\( (-5, 4) \\), \\( (-13, 20) \\) and \\( (-13, -12) \\).",
   ],
   "ITM-GEN-03005-01": [
      "No point of the curve has a horizontal tangent line.",
      "The tangent line is horizontal at \\( (4, 1) \\) and \\( (36, 1) \\).",
      "The tangent line is horizontal at \\( (4, 1) \\) and \\( (52, 1) \\).",
      "The tangent line is horizontal only at \\( (4, 1) \\).",
   ],
   "ITM-GEN-03005-02": [
      "The tangent line is horizontal at \\( (-1, 5) \\) and \\( (-13, 5) \\).",
      "The tangent line is horizontal at \\( (-1, 5) \\) and \\( (-9, 5) \\).",
      "The tangent line is horizontal at \\( (-1, 5) \\), \\( (-9, 21) \\) and \\( (-9, -11) \\).",
      "The tangent line is horizontal at \\( (-9, 21) \\) and \\( (-9, -11) \\).",
   ],
   "ITM-GEN-03005-03": [
      "No point of the curve has a horizontal tangent line.",
      "The tangent line is horizontal at \\( (-3, 6) \\) and \\( (29, 6) \\).",
      "The tangent line is horizontal at \\( (-3, 6) \\) and \\( (45, 6) \\).",
      "The tangent line is horizontal only at \\( (-3, 6) \\).",
   ],
   "ITM-GEN-03005-04": [
      "The tangent line is horizontal at \\( (-11, 18) \\) and \\( (-11, -14) \\).",
      "The tangent line is horizontal at \\( (-3, 2) \\) and \\( (-11, 2) \\).",
      "The tangent line is horizontal at \\( (-3, 2) \\) and \\( (-15, 2) \\).",
      "The tangent line is horizontal at \\( (-3, 2) \\), \\( (-11, 18) \\) and \\( (-11, -14) \\).",
   ],
   "ITM-GEN-03005-05": [
      "The tangent line is horizontal at \\( (-14, 11) \\) and \\( (-14, -21) \\).",
      "The tangent line is horizontal at \\( (-6, -5) \\) and \\( (-14, -5) \\).",
      "The tangent line is horizontal at \\( (-6, -5) \\) and \\( (-18, -5) \\).",
      "The tangent line is horizontal at \\( (-6, -5) \\), \\( (-14, 11) \\) and \\( (-14, -21) \\).",
   ],
   "ITM-GEN-03005-06": [
      "No point of the curve has a horizontal tangent line.",
      "The tangent line is horizontal at \\( (-4, 1) \\) and \\( (4, 1) \\).",
      "The tangent line is horizontal at \\( (-4, 1) \\) and \\( (8, 1) \\).",
      "The tangent line is horizontal only at \\( (-4, 1) \\).",
   ],
   "ITM-GEN-03005-07": [
      "The tangent line is horizontal at \\( (-3, 0) \\) and \\( (-12, 0) \\).",
      "The tangent line is horizontal at \\( (-3, 0) \\) and \\( (-9, 0) \\).",
      "The tangent line is horizontal at \\( (-3, 0) \\), \\( (-9, 6) \\) and \\( (-9, -6) \\).",
      "The tangent line is horizontal at \\( (-9, 6) \\) and \\( (-9, -6) \\).",
   ],
   "ITM-GEN-03005-08": [
      "The tangent line is horizontal at \\( (-8, 6) \\) and \\( (-8, -10) \\).",
      "The tangent line is horizontal at \\( (0, -2) \\) and \\( (-12, -2) \\).",
      "The tangent line is horizontal at \\( (0, -2) \\) and \\( (-8, -2) \\).",
      "The tangent line is horizontal at \\( (0, -2) \\), \\( (-8, 6) \\) and \\( (-8, -10) \\).",
   ],
   "ITM-GEN-03005-09": [
      "The tangent line is horizontal at \\( (-32, 67) \\) and \\( (-32, -61) \\).",
      "The tangent line is horizontal at \\( (0, 3) \\) and \\( (-32, 3) \\).",
      "The tangent line is horizontal at \\( (0, 3) \\) and \\( (-48, 3) \\).",
      "The tangent line is horizontal at \\( (0, 3) \\), \\( (-32, 67) \\) and \\( (-32, -61) \\).",
   ],
   "ITM-GEN-03005-10": [
      "The tangent line is horizontal at \\( (-2, 1) \\) and \\( (-26, 1) \\).",
      "The tangent line is horizontal at \\( (-2, 1) \\) and \\( (-38, 1) \\).",
      "The tangent line is horizontal at \\( (-2, 1) \\), \\( (-26, 49) \\) and \\( (-26, -47) \\).",
      "The tangent line is horizontal at \\( (-26, 49) \\) and \\( (-26, -47) \\).",
   ],
   "ITM-GEN-03005-11": [
      "The tangent line is horizontal at \\( (-7, 12) \\) and \\( (-7, -20) \\).",
      "The tangent line is horizontal at \\( (1, -4) \\) and \\( (-11, -4) \\).",
      "The tangent line is horizontal at \\( (1, -4) \\) and \\( (-7, -4) \\).",
      "The tangent line is horizontal at \\( (1, -4) \\), \\( (-7, 12) \\) and \\( (-7, -20) \\).",
   ],
}

BY_SUFFIX = {
   "03001-00": lambda: exact_derivative_value(4*x*sqrt(17 - x**2), -1),
   "03001-01": lambda: exact_derivative_value(4*x**2*sqrt(2*x**2 + 7), 1),
   "03001-02": lambda: exact_derivative_value(x*(17 - 3*x**2)**2, -2),
   "03001-03": lambda: exact_derivative_value(3*x*(2*x**2 - 3)**4, 2),
   "03001-04": lambda: exact_derivative_value(x*(7 - 2*x**2)**2, 1),
   "03001-05": lambda: exact_derivative_value(5*x**2*(14 - 3*x**2)**3, 2),
   "03001-06": lambda: exact_derivative_value(x*sqrt(16 - 3*x**2), -2),
   "03001-07": lambda: exact_derivative_value(x**2*sqrt(13 - 3*x**2), -2),
   "03001-08": lambda: exact_derivative_value(4*x**2*sqrt(2*x**2 + 14), -1),
   "03001-09": lambda: exact_derivative_value(3*x**2*(30 - 3*x**2)**2, -3),
   "03001-10": lambda: exact_derivative_value(5*x**2*(x**2 - 7)**3, 3),
   "03001-11": lambda: exact_derivative_value(2*x**2*sqrt(25 - x**2), -3),

   "03002-00": lambda: missing_inner_slope({1: (3, 1, 2, None), 2: (5, -3, 2, -4), 3: (2, 2, 4, -1), 4: (-4, -2, 4, -2)}, 1, 9),
   "03002-01": lambda: composite_slope_from_table({1: (6, -5, 2, -4), 2: (-4, 5, 3, 4), 3: (2, 3, 4, -3), 4: (-3, -2, 1, 5)}, 2),
   "03002-02": lambda: composite_slope_from_table({1: (-1, 3, 2, -4), 2: (3, -3, 1, 3), 3: (6, 4, 1, 2), 4: (0, -4, 4, -5)}, 3),
   "03002-03": lambda: missing_inner_slope({1: (-1, 1, 2, None), 2: (-5, -1, 3, 1), 3: (4, -3, 4, -3), 4: (6, 4, 3, 0)}, 1, -1),
   "03002-04": lambda: composite_slope_from_table({1: (-2, 0, 3, 2), 2: (-6, 0, 3, 5), 3: (0, 4, 4, 2), 4: (-1, -3, 3, 1)}, 3),
   "03002-05": lambda: missing_inner_slope({1: (2, -2, 1, -2), 2: (2, 3, 4, 2), 3: (-1, -5, 4, None), 4: (6, 2, 3, 4)}, 3, -6),
   "03002-06": lambda: missing_inner_slope({1: (2, 5, 4, None), 2: (-1, 4, 2, 5), 3: (-6, -2, 3, 4), 4: (2, 1, 2, 3)}, 1, -4),
   "03002-07": lambda: missing_inner_slope({1: (4, 3, 1, 3), 2: (-3, -5, 4, None), 3: (5, -5, 2, -3), 4: (6, -1, 1, -1)}, 2, -5),
   "03002-08": lambda: composite_slope_from_table({1: (-3, 3, 2, 1), 2: (-4, -3, 3, 3), 3: (-6, 0, 1, 0), 4: (1, 4, 4, -5)}, 1),
   "03002-09": lambda: missing_inner_slope({1: (-5, 4, 4, -1), 2: (-5, -3, 1, -2), 3: (0, -1, 4, None), 4: (3, 2, 4, 3)}, 3, -8),
   "03002-10": lambda: missing_inner_slope({1: (1, 5, 4, 4), 2: (1, -4, 1, None), 3: (-2, 5, 4, -5), 4: (0, -5, 2, 0)}, 2, 5),
   "03002-11": lambda: missing_inner_slope({1: (-5, 3, 4, -2), 2: (-5, -2, 1, -2), 3: (3, 5, 1, None), 4: (-5, -4, 3, 3)}, 3, 3),
   "03002-12": lambda: missing_inner_slope({1: (-3, -2, 2, -4), 2: (3, -4, 4, None), 3: (3, 2, 3, 3), 4: (-5, -1, 1, -2)}, 2, -5),
   "03002-13": lambda: composite_slope_from_table({1: (-3, -3, 1, 2), 2: (-4, -3, 3, 5), 3: (2, -5, 4, 5), 4: (-1, -4, 1, 5)}, 3),
   "03002-14": lambda: composite_slope_from_table({1: (6, 1, 3, 1), 2: (5, -2, 4, 3), 3: (0, 1, 4, 3), 4: (-5, -3, 3, -4)}, 3),
   "03002-15": lambda: missing_inner_slope({1: (-6, -4, 4, None), 2: (5, 2, 4, -5), 3: (-5, 5, 4, -3), 4: (-2, 5, 4, -5)}, 1, 15),
   "03002-16": lambda: composite_slope_from_table({1: (-1, 1, 4, -2), 2: (-3, 2, 2, -4), 3: (-2, -5, 3, -5), 4: (2, -1, 4, -4)}, 1),
   "03002-17": lambda: missing_inner_slope({1: (-3, -3, 3, 2), 2: (1, 2, 1, 2), 3: (5, 3, 3, -1), 4: (0, -1, 3, None)}, 4, 12),
   "03002-18": lambda: composite_slope_from_table({1: (1, 0, 1, 3), 2: (-2, 5, 4, 3), 3: (5, -4, 4, 4), 4: (-6, 4, 1, 1)}, 2),
   "03002-19": lambda: composite_slope_from_table({1: (-2, -5, 4, -1), 2: (-1, 4, 4, -4), 3: (3, 5, 1, 2), 4: (5, 4, 3, 5)}, 1),
   "03002-20": lambda: missing_inner_slope({1: (1, -5, 3, -1), 2: (-6, 3, 1, None), 3: (1, -3, 1, -3), 4: (4, 0, 2, 2)}, 2, 5),
   "03002-21": lambda: missing_inner_slope({1: (1, 4, 3, 4), 2: (5, -5, 3, 3), 3: (-4, -4, 3, -4), 4: (3, -2, 2, None)}, 4, -5),

   "03003-00": lambda: composite_slope_from_graphs([(0, -4), (2, 1), (4, 4), (6, 2)], [(0, 6), (2, 5), (4, 6), (6, 0)], 5),
   "03003-01": lambda: composite_slope_from_graphs([(0, 1), (2, -1), (4, -4), (6, 2)], [(0, 3), (2, 6), (4, 4), (6, 2)], 5),
   "03003-02": lambda: composite_slope_from_graphs([(0, -3), (2, -1), (4, 4), (6, -4)], [(0, 6), (2, 0), (4, 2), (6, 4)], 1),
   "03003-03": lambda: composite_slope_from_graphs([(0, -1), (2, 1), (4, 3), (6, 0)], [(0, 6), (2, 2), (4, 4), (6, 2)], 5),
   "03003-04": lambda: composite_slope_from_graphs([(0, 1), (2, 4), (4, 2), (6, -1)], [(0, 2), (2, 6), (4, 4), (6, 2)], 5),
   "03003-05": lambda: composite_slope_from_graphs([(0, 3), (2, -2), (4, -3), (6, 3)], [(0, 1), (2, 5), (4, 6), (6, 4)], 1),
   "03003-06": lambda: composite_slope_from_graphs([(0, -2), (2, 4), (4, 3), (6, 3)], [(0, 1), (2, 5), (4, 5), (6, 0)], 1),
   "03003-07": lambda: composite_slope_from_graphs([(0, 0), (2, -4), (4, 3), (6, -1)], [(0, 3), (2, 2), (4, 6), (6, 0)], 5),
   "03003-08": lambda: composite_slope_from_graphs([(0, -2), (2, 3), (4, -4), (6, -3)], [(0, 3), (2, 4), (4, 4), (6, 2)], 5),
   "03003-09": lambda: composite_slope_from_graphs([(0, 0), (2, 4), (4, 0), (6, 1)], [(0, 6), (2, 4), (4, 5), (6, 1)], 5),
   "03003-10": lambda: composite_slope_from_graphs([(0, 1), (2, 4), (4, 2), (6, 4)], [(0, 1), (2, 2), (4, 0), (6, 5)], 3),
   "03003-11": lambda: composite_slope_from_graphs([(0, -4), (2, 2), (4, -1), (6, -2)], [(0, 6), (2, 4), (4, 5), (6, 5)], 1),
   "03003-12": lambda: composite_slope_from_graphs([(0, 0), (2, 4), (4, 3), (6, -4)], [(0, 6), (2, 4), (4, 0), (6, 6)], 1),
   "03003-13": lambda: composite_slope_from_graphs([(0, 0), (2, -2), (4, -3), (6, 2)], [(0, 1), (2, 2), (4, 0), (6, 6)], 3),
   "03003-14": lambda: composite_slope_from_graphs([(0, 4), (2, -4), (4, 3), (6, -1)], [(0, 6), (2, 0), (4, 3), (6, 3)], 1),
   "03003-15": lambda: composite_slope_from_graphs([(0, -4), (2, 3), (4, 2), (6, -2)], [(0, 1), (2, 2), (4, 0), (6, 4)], 3),
   "03003-16": lambda: composite_slope_from_graphs([(0, 1), (2, 0), (4, -2), (6, 1)], [(0, 4), (2, 2), (4, 0), (6, 1)], 1),
   "03003-17": lambda: composite_slope_from_graphs([(0, -4), (2, 4), (4, -1), (6, 4)], [(0, 1), (2, 0), (4, 5), (6, 1)], 5),
   "03003-18": lambda: composite_slope_from_graphs([(0, 1), (2, -2), (4, -4), (6, -4)], [(0, 0), (2, 2), (4, 0), (6, 4)], 3),
   "03003-19": lambda: composite_slope_from_graphs([(0, 3), (2, -2), (4, 0), (6, 2)], [(0, 1), (2, 5), (4, 4), (6, 5)], 1),
   "03003-20": lambda: composite_slope_from_graphs([(0, 3), (2, 1), (4, -2), (6, -4)], [(0, 5), (2, 4), (4, 6), (6, 0)], 5),
   "03003-21": lambda: composite_slope_from_graphs([(0, 2), (2, 4), (4, -2), (6, -1)], [(0, 1), (2, 5), (4, 1), (6, 3)], 1),

   "03004-00": lambda: slope_on_curve(x**2 + 3*x*y - 2*y**2, 6 - 4*x, (1, 1)),
   "03004-01": lambda: slope_on_curve(x**2 - 3*x*y + 2*y**2, -5*x - 10, (-2, -2)),
   "03004-02": lambda: slope_on_curve(x**2 + 4*x*y + 3*y**3, -x - 5, (1, -1)),
   "03004-03": lambda: slope_on_curve(x**2 - 4*x*y - 3*y**3, -3*x - 59, (-2, 3)),
   "03004-04": lambda: slope_on_curve(x**2 - 4*x*y + 2*y**3, 4*x - 69, (-3, -3)),
   "03004-05": lambda: slope_on_curve(x**2 - 3*x*y + 2*y**2, 2*x + 12, (-1, -3)),
   "03004-06": lambda: slope_on_curve(x**2 + x*y - 2*y**3, 2 - x, (3, 2)),
   "03004-07": lambda: slope_on_curve(x**2 - 2*x*y + 3*y**3, 5*x - 81, (-1, -3)),
   "03004-08": lambda: slope_on_curve(x**2 + x*y + 2*y**2, 14 - 3*x, (-3, -2)),
   "03004-09": lambda: slope_on_curve(x**2 + x*y - 2*y**3, 2*x - 12, (-2, 2)),
   "03004-10": lambda: slope_on_curve(x**2 - 4*x*y - 2*y**2, 4*x + 13, (3, -2)),
   "03004-11": lambda: slope_on_curve(x**2 - 4*x*y + 3*y**3, 30 - 3*x, (-1, 2)),

   "03005-00": lambda: horizontal_tangent_statement("ITM-GEN-03005-00", 1, 4, -5, -17),
   "03005-01": lambda: horizontal_tangent_statement("ITM-GEN-03005-01", 4, 1, 4, 52),
   "03005-02": lambda: horizontal_tangent_statement("ITM-GEN-03005-02", 1, 5, -1, -13),
   "03005-03": lambda: horizontal_tangent_statement("ITM-GEN-03005-03", 4, 6, -3, 45),
   "03005-04": lambda: horizontal_tangent_statement("ITM-GEN-03005-04", 1, 2, -3, -15),
   "03005-05": lambda: horizontal_tangent_statement("ITM-GEN-03005-05", 1, -5, -6, -18),
   "03005-06": lambda: horizontal_tangent_statement("ITM-GEN-03005-06", 4, 1, -4, 8),
   "03005-07": lambda: horizontal_tangent_statement("ITM-GEN-03005-07", 3, 0, -3, -12),
   "03005-08": lambda: horizontal_tangent_statement("ITM-GEN-03005-08", 4, -2, 0, -12),
   "03005-09": lambda: horizontal_tangent_statement("ITM-GEN-03005-09", 4, 3, 0, -48),
   "03005-10": lambda: horizontal_tangent_statement("ITM-GEN-03005-10", 3, 1, -2, -38),
   "03005-11": lambda: horizontal_tangent_statement("ITM-GEN-03005-11", 1, -4, 1, -11),

   "03006-00": lambda: inverse_slope_from_table({1: (-2, 2), 2: (0, 4), 3: (1, 2), 4: (3, 5)}, 3),
   "03006-01": lambda: inverse_slope_from_table({1: (-3, 4), 2: (0, 2), 3: (4, 2), 4: (5, 7)}, 4),
   "03006-02": lambda: inverse_slope_from_table({1: (-2, 1), 2: (-1, 7), 3: (4, 2), 4: (5, 3)}, 4),
   "03006-03": lambda: inverse_slope_from_table({1: (-3, 6), 2: (-2, 6), 3: (1, 7), 4: (3, 2)}, 3),
   "03006-04": lambda: inverse_slope_from_table({1: (2, 7), 2: (3, 1), 3: (6, 1), 4: (7, 3)}, 2),
   "03006-05": lambda: inverse_slope_from_table({1: (-1, 4), 2: (2, 1), 3: (4, 7), 4: (8, 6)}, 4),
   "03006-06": lambda: inverse_slope_from_table({1: (3, 7), 2: (4, 2), 3: (5, 5), 4: (7, 6)}, 4),
   "03006-07": lambda: inverse_slope_from_table({1: (-1, 6), 2: (1, 7), 3: (7, 2), 4: (8, 7)}, 1),
   "03006-08": lambda: inverse_slope_from_table({1: (0, 7), 2: (2, 5), 3: (4, 2), 4: (7, 3)}, 4),
   "03006-09": lambda: inverse_slope_from_table({1: (-2, 2), 2: (1, 4), 3: (2, 4), 4: (3, 5)}, 3),
   "03006-10": lambda: inverse_slope_from_table({1: (-1, 3), 2: (1, 3), 3: (2, 7), 4: (9, 6)}, 2),
   "03006-11": lambda: inverse_slope_from_table({1: (-2, 4), 2: (-1, 5), 3: (1, 7), 4: (6, 6)}, 1),
   "03006-12": lambda: inverse_slope_from_table({1: (-3, 6), 2: (1, 5), 3: (2, 2), 4: (7, 3)}, 1),
   "03006-13": lambda: inverse_slope_from_table({1: (-1, 2), 2: (3, 6), 3: (7, 4), 4: (9, 7)}, 3),
   "03006-14": lambda: inverse_slope_from_table({1: (-1, 4), 2: (1, 5), 3: (6, 4), 4: (8, 5)}, 1),
   "03006-15": lambda: inverse_slope_from_table({1: (0, 6), 2: (1, 5), 3: (2, 6), 4: (4, 3)}, 2),
   "03006-16": lambda: inverse_slope_from_table({1: (-3, 5), 2: (-2, 7), 3: (4, 5), 4: (9, 1)}, 4),
   "03006-17": lambda: inverse_slope_from_table({1: (-2, 4), 2: (0, 4), 3: (1, 5), 4: (2, 1)}, 1),
   "03006-18": lambda: inverse_slope_from_table({1: (-2, 7), 2: (1, 6), 3: (4, 4), 4: (9, 5)}, 1),
   "03006-19": lambda: inverse_slope_from_table({1: (-1, 3), 2: (3, 6), 3: (4, 5), 4: (7, 6)}, 4),
   "03006-20": lambda: inverse_slope_from_table({1: (-2, 6), 2: (1, 5), 3: (2, 1), 4: (3, 1)}, 1),
   "03006-21": lambda: inverse_slope_from_table({1: (-3, 2), 2: (3, 7), 3: (4, 3), 4: (5, 7)}, 4),

   "03007-00": lambda: exact_derivative_value(4*x**2*asin(3*x**2 - Rational(23, 2)), 2),
   "03007-01": lambda: exact_derivative_value(5*x**2*asin(2*x**2 - Rational(3, 2)), -1),
   "03007-02": lambda: exact_derivative_value(x**2*atan(17 - 4*x**2), 2),
   "03007-03": lambda: exact_derivative_value(6*x*asin(Rational(7, 2) - 4*x**2), -1),
   "03007-04": lambda: exact_derivative_value(4*x*atan(2*x**2 - 9), 2),
   "03007-05": lambda: exact_derivative_value(3*x**2*atan(3*x - 10), 3),
   "03007-06": lambda: exact_derivative_value(3*x*asin(-4*x - Rational(17, 2)), -2),
   "03007-07": lambda: exact_derivative_value(6*x*atan(-3*x - 10), -3),
   "03007-08": lambda: exact_derivative_value(x**2*atan(-4*x - 11), -3),
   "03007-09": lambda: exact_derivative_value(5*x**2*atan(7 - 3*x), 2),
   "03007-10": lambda: exact_derivative_value(5*x*atan(4*x**2 - 17), 2),
   "03007-11": lambda: exact_derivative_value(3*x*asin(Rational(19, 2) - 3*x), 3),
   "03007-12": lambda: exact_derivative_value(6*x**2*asin(4*x - Rational(15, 2)), 2),
   "03007-13": lambda: exact_derivative_value(3*x**2*atan(15 - 4*x**2), 2),
   "03007-14": lambda: exact_derivative_value(x**2*asin(4*x**2 - Rational(9, 2)), -1),
   "03007-15": lambda: exact_derivative_value(4*x**2*asin(2*x - Rational(9, 2)), 2),
   "03007-16": lambda: exact_derivative_value(3*x**2*asin(2*x**2 - Rational(15, 2)), -2),
   "03007-17": lambda: exact_derivative_value(4*x**2*atan(15 - 4*x**2), -2),
   "03007-18": lambda: exact_derivative_value(4*x*atan(x + 1), -2),
   "03007-19": lambda: exact_derivative_value(6*x*asin(-2*x - Rational(9, 2)), -2),
   "03007-20": lambda: exact_derivative_value(6*x**2*atan(-4*x - 11), -3),
   "03007-21": lambda: exact_derivative_value(x**2*atan(3 - x**2), -2),

   "03008-00": lambda: second_derivative_at(-3*x*y + x + 4*y, (-1, 1)),
   "03008-01": lambda: second_derivative_at(-3*x*y - 3*x - y, (2, -2)),
   "03008-02": lambda: second_derivative_at(-3*x*y - 5*x + y, (2, -1)),
   "03008-03": lambda: second_derivative_at(-3*x*y - 5*x + y, (-2, 1)),
   "03008-04": lambda: second_derivative_at(x*y - 5*x + 4*y, (1, -1)),
   "03008-05": lambda: second_derivative_at(-x*y + 4*x - 3*y, (0, 1)),
   "03008-06": lambda: second_derivative_at(x*y - 3*x + 4*y, (1, -3)),
   "03008-07": lambda: second_derivative_at(3*x*y - 5*x + 2*y, (0, -2)),
   "03008-08": lambda: second_derivative_at(-2*x*y + 4*x - y, (3, -2)),
   "03008-09": lambda: second_derivative_at(x*y + 5*x - 3*y, (1, 2)),
   "03008-10": lambda: second_derivative_at(-2*x*y + 3*x - 4*y, (3, 1)),
   "03008-11": lambda: second_derivative_at(2*x*y + x - y, (3, 2)),

   "03009-00": lambda: exact_derivative_value(3*x*exp(-x - 3), -1),
   "03009-01": lambda: exact_derivative_value(3*x*exp(3*x - 1), 2),
   "03009-02": lambda: exact_derivative_value(6*x**2*exp(-3*x - 1), 2),
   "03009-03": lambda: exact_derivative_value(4*x**3*exp(-3*x - 1), 2),
   "03009-04": lambda: exact_derivative_value(4*x**3*exp(2*x + 2), 1),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
