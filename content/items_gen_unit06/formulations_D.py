"""Blind re-solve of generated unit 6 items, batch D, each answer computed from its stem alone.

Written from var/p4/resolve/items_gen_unit06/stems_D.json and nothing else about these items by a blind
solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The file is self-contained: each
table and each graph's vertices and semicircle are copied into it from the stems. An answer asked
correct to three decimal places comes back at 30 significant digits, unrounded.
"""
import mpmath
import sympy
from sympy import Rational

from tools.key_recheck import (
   accumulation_derivative,
   definite_integral,
   pinned_antiderivative_value,
   trapezoidal_sum,
   t,
   x,
)

s = sympy.Symbol("s")
WORKING_DIGITS = 30


def expression(text):
   return sympy.sympify(text, locals={"x": x, "t": t, "s": s})


def riemann_sum(points, side):
   """points: (input, value) rows of the table; each subinterval uses its left or right value."""
   total = sympy.Integer(0)

   for (left_input, left_value), (right_input, right_value) in zip(points, points[1:]):
      height = left_value if side == "left" else right_value
      total += (sympy.nsimplify(right_input) - sympy.nsimplify(left_input)) * sympy.nsimplify(height)

   return total


def trapezoid_amount(points, initial_amount):
   return initial_amount + trapezoidal_sum(points)


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


def amount_exact(rate, known_time, known_amount, at):
   return pinned_antiderivative_value(rate, known_time, known_amount, at, variable=t)


def amount_to_three_places(rate, known_time, known_amount, at):
   """known_amount plus the integral of rate from known_time to at, by numerical quadrature."""
   rate_function = sympy.lambdify(t, rate, "mpmath")

   with mpmath.workdps(WORKING_DIGITS + 10):
      change = mpmath.quad(rate_function, [mpmath.mpf(sympy.Rational(known_time)), mpmath.mpf(sympy.Rational(at))])
      total = mpmath.mpf(known_amount) + change

      return sympy.Float(mpmath.nstr(total, WORKING_DIGITS), WORKING_DIGITS)


def antiderivative(integrand, variable):
   return sympy.integrate(integrand, variable)


BY_SUFFIX = {
   "06001-00": lambda: riemann_sum([(0, 11), (4, 20), (5, 16), (7, 20), (8, 11)], "left"),
   "06001-01": lambda: riemann_sum([(0, 8), (2, 18), (3, 5), (5, 17), (8, 10)], "right"),
   "06001-02": lambda: riemann_sum([(0, 9), (3, 16), (6, 13), (9, 18), (12, 16)], "left"),
   "06001-03": lambda: riemann_sum([(0, 14), (1, 18), (5, 11), (9, 13), (12, 12)], "left"),
   "06001-04": lambda: riemann_sum([(0, 4), (2, 12), (4, 10), (6, 8), (8, 3)], "left"),
   "06001-05": lambda: riemann_sum([(0, 10), (2, 12), (4, 6), (6, 20), (8, 5)], "left"),
   "06001-06": lambda: riemann_sum([(0, 6), (2, 12), (4, 17), (6, 20), (8, 17)], "right"),
   "06001-07": lambda: riemann_sum([(0, 12), (1, 12), (4, 7), (5, 11), (8, 11)], "right"),
   "06001-08": lambda: riemann_sum([(0, 13), (1, 13), (3, 20), (7, 3), (8, 14)], "right"),
   "06001-09": lambda: riemann_sum([(0, 20), (2, 7), (4, 13), (6, 18), (8, 8)], "left"),
   "06001-10": lambda: riemann_sum([(0, 20), (1, 17), (3, 5), (4, 5), (8, 18)], "right"),
   "06001-11": lambda: riemann_sum([(0, 7), (2, 2), (4, 15), (6, 10), (8, 17)], "right"),
   "06001-12": lambda: riemann_sum([(0, 5), (2, 4), (4, 5), (6, 2), (8, 19)], "right"),
   "06001-13": lambda: riemann_sum([(0, 19), (2, 8), (4, 7), (6, 15), (8, 8)], "right"),
   "06001-14": lambda: riemann_sum([(0, 7), (2, 12), (4, 8), (6, 11), (8, 3)], "left"),
   "06001-15": lambda: riemann_sum([(0, 5), (3, 10), (7, 7), (11, 2), (12, 9)], "left"),
   "06001-16": lambda: riemann_sum([(0, 9), (3, 20), (5, 11), (8, 3), (12, 4)], "left"),
   "06001-17": lambda: riemann_sum([(0, 16), (2, 3), (4, 5), (6, 4), (8, 18)], "right"),
   "06001-18": lambda: riemann_sum([(0, 3), (1, 16), (3, 13), (7, 2), (8, 11)], "right"),
   "06001-19": lambda: riemann_sum([(0, 6), (4, 17), (6, 15), (10, 9), (12, 19)], "left"),
   "06001-20": lambda: riemann_sum([(0, 13), (3, 7), (7, 9), (8, 14), (12, 11)], "left"),
   "06001-21": lambda: riemann_sum([(0, 12), (2, 7), (4, 5), (6, 4), (8, 19)], "left"),
   "06002-00": lambda: trapezoid_amount([(0, 20), (6, 11), (10, 18), (12, 20)], 45),
   "06002-01": lambda: trapezoid_amount([(0, 20), (4, 16), (10, 17), (12, 6)], 0),
   "06002-02": lambda: trapezoid_amount([(0, 8), (2, 2), (6, 8), (12, 12)], 0),
   "06002-03": lambda: trapezoid_amount([(0, 9), (2, 16), (6, 18), (12, 13)], 25),
   "06002-04": lambda: trapezoid_amount([(0, 12), (4, 7), (6, 12), (12, 3)], 80),
   "06003-00": lambda: definite_integral(graph_function([(0, 1), (2, -2), (4, 3), (6, 2), (8, 0)], (10, 2, 1)), 2, 12),
   "06003-01": lambda: accumulation_derivative(graph_function([(0, 2), (2, 3), (4, 2), (6, 2), (8, 0)], (10, 2, -1)).subs(x, t), 4, 2*x, Rational(7, 2)),
   "06003-02": lambda: definite_integral(graph_function([(0, 0), (2, -2), (4, -2), (6, 2), (8, 0)], (10, 2, -1)), 2, 12),
   "06003-03": lambda: definite_integral(graph_function([(0, 3), (2, -1), (4, 2), (6, 3), (8, 0)], (10, 2, 1)), 0, 12),
   "06003-04": lambda: accumulation_derivative(graph_function([(0, 2), (2, 3), (4, 3), (6, 1), (8, 0)], (10, 2, -1)).subs(x, t), 4, 2*x, Rational(3, 2)),
   "06003-05": lambda: definite_integral(graph_function([(0, -2), (2, 0), (4, 2), (6, -3), (8, 0)], (10, 2, -1)), 4, 12),
   "06003-06": lambda: definite_integral(graph_function([(0, -1), (2, 3), (4, 0), (6, -2), (8, 0)], (10, 2, 1)), 4, 12),
   "06003-07": lambda: accumulation_derivative(graph_function([(0, -2), (2, 3), (4, -2), (6, 1), (8, 0)], (10, 2, -1)).subs(x, t), 4, 2*x, Rational(3, 2)),
   "06003-08": lambda: definite_integral(graph_function([(0, -3), (2, -2), (4, 2), (6, -3), (8, 0)], (10, 2, -1)), 4, 12),
   "06003-09": lambda: definite_integral(graph_function([(0, -1), (2, 0), (4, -2), (6, -2), (8, 0)], (10, 2, 1)), 2, 12),
   "06003-10": lambda: accumulation_derivative(graph_function([(0, 0), (2, -2), (4, -3), (6, 2), (8, 0)], (10, 2, -1)).subs(x, t), 2, 2*x, Rational(3, 2)),
   "06003-11": lambda: definite_integral(graph_function([(0, 0), (2, -1), (4, 3), (6, 2), (8, 0)], (10, 2, 1)), 2, 12),
   "06003-12": lambda: definite_integral(graph_function([(0, 1), (2, -2), (4, -2), (6, 1), (8, 0)], (10, 2, -1)), 0, 12),
   "06003-13": lambda: accumulation_derivative(graph_function([(0, -2), (2, 3), (4, 3), (6, 3), (8, 0)], (10, 2, 1)).subs(x, t), 4, 2*x, Rational(3, 2)),
   "06003-14": lambda: accumulation_derivative(graph_function([(0, 2), (2, 3), (4, -2), (6, 1), (8, 0)], (10, 2, 1)).subs(x, t), 4, 2*x, Rational(7, 2)),
   "06003-15": lambda: definite_integral(graph_function([(0, 2), (2, -2), (4, -2), (6, -3), (8, 0)], (10, 2, 1)), 4, 12),
   "06003-16": lambda: accumulation_derivative(graph_function([(0, 1), (2, 2), (4, 3), (6, 2), (8, 0)], (10, 2, 1)).subs(x, t), 0, 2*x, Rational(1, 2)),
   "06003-17": lambda: accumulation_derivative(graph_function([(0, 0), (2, 3), (4, 0), (6, -2), (8, 0)], (10, 2, 1)).subs(x, t), 4, 2*x, Rational(5, 2)),
   "06003-18": lambda: definite_integral(graph_function([(0, 2), (2, -2), (4, 3), (6, 2), (8, 0)], (10, 2, 1)), 0, 12),
   "06003-19": lambda: definite_integral(graph_function([(0, -3), (2, -1), (4, 0), (6, 1), (8, 0)], (10, 2, 1)), 2, 12),
   "06003-20": lambda: definite_integral(graph_function([(0, -3), (2, -3), (4, 0), (6, -2), (8, 0)], (10, 2, 1)), 4, 12),
   "06003-21": lambda: definite_integral(graph_function([(0, -1), (2, -3), (4, 0), (6, -3), (8, 0)], (10, 2, -1)), 4, 12),
   "06005-00": lambda: amount_to_three_places(expression("sin(t**2/3) + 9"), 0, 55, Rational(7, 2)),
   "06005-01": lambda: amount_to_three_places(expression("2*sin(t**2/2) + 6"), 0, 60, 4),
   "06005-02": lambda: amount_to_three_places(expression("2*sin(t**2/4) + 3"), 0, 20, 2),
   "06005-03": lambda: amount_exact(expression("8 - 6*t"), 1, 50, 4),
   "06005-04": lambda: amount_to_three_places(expression("3*sin(t**2/5) + 7"), 0, 25, Rational(5, 2)),
   "06005-05": lambda: amount_exact(expression("4*t + 6"), 1, 85, 2),
   "06005-06": lambda: amount_to_three_places(expression("2*sin(t**2/4) + 6"), 0, 25, 4),
   "06005-07": lambda: amount_exact(expression("2*t + 2"), 3, 50, 6),
   "06005-08": lambda: amount_exact(expression("3*t**2 + 4*t + 5"), 2, 30, 1),
   "06005-09": lambda: amount_to_three_places(expression("sin(t**2/3) + 4"), 0, 30, 2),
   "06005-10": lambda: amount_to_three_places(expression("3*sin(t**2/2) + 3"), 0, 45, 2),
   "06005-11": lambda: amount_exact(expression("2 - 6*t"), 3, 35, 1),
   "06005-12": lambda: amount_to_three_places(expression("sin(t**2/5) + 6"), 0, 45, 2),
   "06005-13": lambda: amount_to_three_places(expression("sin(t**2/4) + 5"), 0, 45, 4),
   "06005-14": lambda: amount_exact(expression("2*t + 2"), 3, 65, 5),
   "06005-15": lambda: amount_exact(expression("3*t**2 - 6*t + 7"), 2, 25, 3),
   "06005-16": lambda: amount_to_three_places(expression("3*sin(t**2/2) + 9"), 0, 80, Rational(5, 2)),
   "06005-17": lambda: amount_to_three_places(expression("3*sin(t**2/5) + 8"), 0, 60, 2),
   "06005-18": lambda: amount_to_three_places(expression("3*sin(t**2/2) + 4"), 0, 30, 3),
   "06005-19": lambda: amount_exact(expression("-6*t**2 - 6*t + 4"), 3, 70, 1),
   "06005-20": lambda: amount_exact(expression("7 - 6*t"), 3, 45, 5),
   "06005-21": lambda: amount_to_three_places(expression("2*sin(t**2/3) + 8"), 0, 30, 3),
   "06006-00": lambda: amount_to_three_places(expression("2*sin(t**2/2) - cos(t/2) + 3"), 0, 25, Rational(5, 2)),
   "06006-01": lambda: amount_to_three_places(expression("2*sin(t**2/3) - cos(t/2) + 4"), 0, 0, 4),
   "06006-02": lambda: amount_to_three_places(expression("2*sin(t**2/2) - cos(t/2) + 5"), 0, 85, 4),
   "06006-03": lambda: amount_to_three_places(expression("3*sin(t**2/2) - 2*cos(t/2) + 3"), 0, 65, 3),
   "06006-04": lambda: amount_to_three_places(expression("sin(t**2/3) - 3*cos(t/2) + 5"), 0, 0, Rational(5, 2)),
   "06006-05": lambda: amount_to_three_places(expression("3*sin(t**2/4) - cos(t/2) + 5"), 0, 75, 4),
   "06006-06": lambda: amount_to_three_places(expression("3*sin(t**2/2) - 3*cos(t/2) + 1"), 0, 45, 3),
   "06006-07": lambda: amount_to_three_places(expression("sin(t**2/4) - 3*cos(t/2) + 2"), 0, 20, 2),
   "06006-08": lambda: amount_to_three_places(expression("3*sin(t**2/3) - cos(t/2) + 4"), 0, 0, 3),
   "06006-09": lambda: amount_to_three_places(expression("2*sin(t**2/4) - 2*cos(t/2) + 6"), 0, 0, Rational(7, 2)),
   "06006-10": lambda: amount_to_three_places(expression("sin(t**2/2) - 3*cos(t/2) + 1"), 0, 0, Rational(7, 2)),
   "06006-11": lambda: amount_to_three_places(expression("3*sin(t**2/4) - cos(t/2) + 2"), 0, 30, 2),
   "06006-12": lambda: amount_to_three_places(expression("3*sin(t**2/2) - 2*cos(t/2)"), 0, 60, Rational(7, 2)),
   "06006-13": lambda: amount_to_three_places(expression("2*sin(t**2/3) - 2*cos(t/2) + 2"), 0, 85, Rational(5, 2)),
   "06006-14": lambda: amount_to_three_places(expression("3*sin(t**2/3) - cos(t/2)"), 0, 0, Rational(7, 2)),
   "06006-15": lambda: amount_to_three_places(expression("2*sin(t**2/3) - 2*cos(t/2) + 6"), 0, 75, Rational(5, 2)),
   "06006-16": lambda: amount_to_three_places(expression("3*sin(t**2/2) - 2*cos(t/2) + 3"), 0, 40, 3),
   "06006-17": lambda: amount_to_three_places(expression("3*sin(t**2/4) - 2*cos(t/2) + 4"), 0, 0, 3),
   "06006-18": lambda: amount_to_three_places(expression("sin(t**2/2) - cos(t/2) + 3"), 0, 0, 3),
   "06006-19": lambda: amount_to_three_places(expression("2*sin(t**2/3) - 2*cos(t/2) + 1"), 0, 0, 2),
   "06006-20": lambda: amount_to_three_places(expression("3*sin(t**2/4) - cos(t/2) + 2"), 0, 0, 4),
   "06006-21": lambda: amount_to_three_places(expression("sin(t**2/4) - 2*cos(t/2) + 4"), 0, 50, Rational(7, 2)),
   "06008-00": lambda: definite_integral(expression("3*x*cos(x**2 + 4)"), 0, 2),
   "06008-01": lambda: antiderivative(expression("3*x**2*cos(2*x**3 + 2)"), x),
   "06008-02": lambda: definite_integral(expression("9*x**2*exp(2*x**3 + 2)"), 0, 1),
   "06008-03": lambda: antiderivative(expression("x*cos(2*x**2 + 1)"), x),
   "06008-04": lambda: antiderivative(expression("x**2*exp(2*x**3 + 1)"), x),
   "06009-00": lambda: antiderivative(expression("5*x*sin(2*x)"), x),
   "06009-01": lambda: antiderivative(expression("5*s*sin(5*s)"), s),
   "06009-02": lambda: antiderivative(expression("-x*cos(2*x)"), x),
   "06009-03": lambda: definite_integral(expression("x*cos(4*x)"), 0, expression("pi/12")),
   "06009-04": lambda: definite_integral(expression("-x*exp(3*x)"), 0, 2),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
