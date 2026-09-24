"""Blind re-solve of generated unit 6 items, batch X, each answer computed from its stem alone.

Written from var/p4/resolve/items_gen_unit06/stems_X.json and nothing else about these items by a blind
solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The file is self-contained: each
graph's vertices and semicircle are copied into it from the stem's figure.
"""
import sympy

from tools.key_recheck import definite_integral, x


def graph_function(vertices, semicircle):
   """Line segments joining consecutive vertices, then a semicircle given as (centre, radius, side)
   on the x-axis, side 1 above it and -1 below it."""
   pieces = []

   for (left_x, left_y), (right_x, right_y) in zip(vertices, vertices[1:]):
      slope = sympy.Rational(right_y - left_y, right_x - left_x)
      pieces.append((left_y + slope * (x - left_x), x <= right_x))

   centre, radius, side = semicircle
   pieces.append((side * sympy.sqrt(radius**2 - (x - centre) ** 2), x <= centre + radius))

   return sympy.Piecewise(*pieces)


BY_SUFFIX = {
   "06004-00": lambda: definite_integral(graph_function([(0, 2), (1, 2), (2, -1), (3, -2), (4, 0)], (6, 2, -1)), 8, 2),
   "06004-01": lambda: definite_integral(graph_function([(0, 1), (1, 0), (2, 1), (3, -2), (4, 0)], (6, 2, 1)), 8, 1),
   "06004-02": lambda: definite_integral(graph_function([(0, 3), (1, 3), (2, -2), (3, 1), (4, 0)], (6, 2, 1)), 8, 1),
   "06004-03": lambda: definite_integral(graph_function([(0, -3), (1, 0), (2, 3), (3, -2), (4, 0)], (6, 2, 1)), 2, 8),
   "06004-04": lambda: definite_integral(graph_function([(0, 0), (1, 3), (2, -2), (3, 2), (4, 0)], (6, 2, -1)), 8, 0),
   "06004-05": lambda: definite_integral(graph_function([(0, -3), (1, 2), (2, -2), (3, -2), (4, 0)], (6, 2, -1)), 1, 8),
   "06004-06": lambda: definite_integral(graph_function([(0, -2), (1, -1), (2, 3), (3, -2), (4, 0)], (6, 2, 1)), 0, 8),
   "06004-07": lambda: definite_integral(graph_function([(0, 3), (1, -1), (2, 2), (3, 1), (4, 0)], (6, 2, -1)), 8, 0),
   "06004-08": lambda: definite_integral(graph_function([(0, -2), (1, 0), (2, -3), (3, 3), (4, 0)], (6, 2, 1)), 0, 8),
   "06004-09": lambda: definite_integral(graph_function([(0, -3), (1, 2), (2, -3), (3, -1), (4, 0)], (6, 2, 1)), 8, 2),
   "06004-10": lambda: definite_integral(graph_function([(0, 2), (1, -1), (2, -3), (3, -3), (4, 0)], (6, 2, -1)), 0, 8),
   "06004-11": lambda: definite_integral(graph_function([(0, 2), (1, 3), (2, 1), (3, 1), (4, 0)], (6, 2, -1)), 8, 1),
   "06004-12": lambda: definite_integral(graph_function([(0, -2), (1, -3), (2, -2), (3, -3), (4, 0)], (6, 2, -1)), 2, 8),
   "06004-13": lambda: definite_integral(graph_function([(0, 3), (1, -1), (2, 0), (3, 3), (4, 0)], (6, 2, -1)), 8, 2),
   "06004-14": lambda: definite_integral(graph_function([(0, 0), (1, -3), (2, 2), (3, -2), (4, 0)], (6, 2, 1)), 8, 1),
   "06004-15": lambda: definite_integral(graph_function([(0, 3), (1, 2), (2, -1), (3, -3), (4, 0)], (6, 2, -1)), 8, 1),
   "06004-16": lambda: definite_integral(graph_function([(0, 2), (1, 2), (2, -1), (3, -3), (4, 0)], (6, 2, 1)), 8, 1),
   "06004-17": lambda: definite_integral(graph_function([(0, -2), (1, -3), (2, -1), (3, 3), (4, 0)], (6, 2, -1)), 8, 2),
   "06004-18": lambda: definite_integral(graph_function([(0, 3), (1, 3), (2, -1), (3, 3), (4, 0)], (6, 2, 1)), 0, 8),
   "06004-19": lambda: definite_integral(graph_function([(0, -1), (1, 1), (2, 3), (3, -3), (4, 0)], (6, 2, 1)), 8, 2),
   "06004-20": lambda: definite_integral(graph_function([(0, -1), (1, 0), (2, 0), (3, 1), (4, 0)], (6, 2, 1)), 8, 0),
   "06004-21": lambda: definite_integral(graph_function([(0, 2), (1, -3), (2, 0), (3, -3), (4, 0)], (6, 2, -1)), 1, 8),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
