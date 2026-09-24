"""Each agent-drafted Unit 6 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. An edited stem needs its entry
rewritten the same way before the recheck can pass again. app/items/ingest.py loads only .json
records, so this file never reaches the bank.
"""
import sympy
from sympy import E, Rational, cos, exp, ln, pi, sec, sin, sqrt

from tools.key_recheck import (
   accumulation_derivative,
   definite_integral,
   pinned_antiderivative_value,
   t,
   trapezoidal_sum,
   x,
)

ITEM_PREFIX = "ITM-AGT-"


def fundamental_theorem_from_values(stated_values, lower, upper, at):
   """d/dx of the integral of f from lower(x) to upper(x) at x = at, for f known only through
   stated_values; a constant limit contributes nothing."""
   upper_at = sympy.sympify(upper).subs(x, at)
   lower_at = sympy.sympify(lower).subs(x, at)
   upper_rate = sympy.diff(upper, x).subs(x, at)
   lower_rate = sympy.diff(lower, x).subs(x, at)

   upper_contribution = stated_values[upper_at] * upper_rate if upper_rate != 0 else 0
   lower_contribution = stated_values[lower_at] * lower_rate if lower_rate != 0 else 0

   return sympy.Integer(upper_contribution - lower_contribution)


def parts_of_x_times_derivative(left, right, value_at_left, value_at_right, integral_of_function):
   """The integral of x F'(x) from left to right, as [x F(x)] minus the integral of F."""
   boundary_term = right * value_at_right - left * value_at_left

   return sympy.Integer(boundary_term - integral_of_function)


def combination_integral(lower, upper, weighted_integrals, constant):
   """The integral from lower to upper of a weighted sum of functions plus a constant, where each
   pair is (weight, integral of that function from lower to upper)."""
   function_part = sum(weight * integral for weight, integral in weighted_integrals)

   return sympy.Integer(function_part + constant * (upper - lower))


BY_SUFFIX = {
   "06002-00": lambda: trapezoidal_sum([(0, 4), (2, 7), (5, 9), (10, 6)]),
   "06002-01": lambda: trapezoidal_sum([(0, 10), (3, 14), (6, 20), (9, 18)]),
   "06002-02": lambda: trapezoidal_sum([(0, 30), (1, 50), (3, 60), (4, 40)]),
   "06002-03": lambda: trapezoidal_sum([(0, 5), (2, 8), (4, 6), (6, 3)]),
   "06002-04": lambda: trapezoidal_sum([(0, 2), (1, 3), (4, 5), (6, 1)]),
   "06002-05": lambda: trapezoidal_sum([(0, 12), (5, 16), (10, 10), (15, 8)]),
   "06002-06": lambda: trapezoidal_sum([(1, 6), (2, 9), (5, 11), (7, 4)]),
   "06002-07": lambda: trapezoidal_sum([(0, 3), (2, 5), (4, 4), (6, 2)]),
   "06002-08": lambda: trapezoidal_sum([(0, 3), (4, 5), (6, 8), (12, 4)]),
   "06002-09": lambda: trapezoidal_sum([(0, 15), (10, 22), (20, 18), (30, 12)]),
   "06002-10": lambda: trapezoidal_sum([(0, 6), (Rational(1, 2), 7), (2, 10), (4, 5)]),
   "06002-11": lambda: trapezoidal_sum([(0, 4), (2, 12), (3, 16), (7, 8)]),
   "06002-12": lambda: trapezoidal_sum([(0, 25), (2, 45), (4, 70), (6, 50)]),
   "06002-13": lambda: trapezoidal_sum([(0, 9), (3, 7), (5, 6), (8, 2)]),
   "06002-14": lambda: trapezoidal_sum([(0, Rational(3, 2)), (2, Rational(5, 2)), (4, 3), (6, 2)]),
   "06002-15": lambda: trapezoidal_sum([(0, 20), (2, 24), (3, 30), (8, 14)]),
   "06002-16": lambda: trapezoidal_sum([(0, 5), (4, 9), (8, 12), (12, 7)]),
   "06002-17": lambda: trapezoidal_sum([(0, 2), (1, 6), (Rational(3, 2), 8), (3, 4)]),
   "06002-18": lambda: trapezoidal_sum([(0, 2), (6, 6), (12, 7), (18, 3)]),
   "06002-19": lambda: trapezoidal_sum([(0, 8), (5, 14), (15, 20), (20, 10)]),

   "06008-00": lambda: definite_integral(x * (x**2 + 1)**3, 0, 1),
   "06008-01": lambda: pinned_antiderivative_value(x * exp(x**2), 0, 3, 2),
   "06008-02": lambda: definite_integral(x**2 * sqrt(x**3 + 1), 0, 2),
   "06008-03": lambda: pinned_antiderivative_value(sin(x) * cos(x)**2, 0, 1, pi / 2),
   "06008-04": lambda: pinned_antiderivative_value(x / (x**2 + 1), 1, 1, 2),
   "06008-05": lambda: definite_integral(exp(2*x + 1), 0, 1),
   "06008-06": lambda: pinned_antiderivative_value(cos(3*x), 0, 2, pi / 6),
   "06008-07": lambda: pinned_antiderivative_value(x / (x**2 + 1)**2, 1, 1, 2),
   "06008-08": lambda: definite_integral(x**3 * (x**4 + 1)**2, 0, 1),
   "06008-09": lambda: pinned_antiderivative_value(x * sin(x**2), 0, 2, sqrt(pi)),
   "06008-10": lambda: definite_integral((2*x + 1)**3, 0, 1),
   "06008-11": lambda: definite_integral(1 / sqrt(2*x + 1), 0, 12),
   "06008-12": lambda: pinned_antiderivative_value(1 / (3*x + 1), 1, 2, 5),
   "06008-13": lambda: pinned_antiderivative_value(exp(cos(x)) * sin(x), 0, 1, pi / 2),
   "06008-14": lambda: pinned_antiderivative_value(x**2 / (x**3 + 1), 1, 1, 2),
   "06008-15": lambda: definite_integral(x * sqrt(x**2 + 16), 0, 3),
   "06008-16": lambda: pinned_antiderivative_value((x + 1) / (x**2 + 2*x + 2), 1, 2, 3),
   "06008-17": lambda: pinned_antiderivative_value((exp(x) + 1)**2 * exp(x), 0, 1, ln(3)),
   "06008-18": lambda: pinned_antiderivative_value(x * (1 - x**2)**4, 0, 1, 1),
   "06008-19": lambda: pinned_antiderivative_value(sec(2*x)**2, 0, 1, pi / 8),

   "06009-00": lambda: definite_integral(x * exp(x), 0, 1),
   "06009-01": lambda: definite_integral(x * cos(x), 0, pi / 2),
   "06009-02": lambda: definite_integral(x * ln(x), 1, E),
   "06009-03": lambda: definite_integral(x * exp(2*x), 0, 1),
   "06009-04": lambda: definite_integral((2*x + 1) * sin(x), 0, pi / 2),
   "06009-05": lambda: definite_integral(x**2 * ln(x), 1, E),
   "06009-06": lambda: definite_integral(x**2 * exp(x), 0, 1),
   "06009-07": lambda: definite_integral(x**2 * cos(x), 0, pi / 2),
   "06009-08": lambda: parts_of_x_times_derivative(1, 3, 2, 5, 4),
   "06009-09": lambda: definite_integral(x * exp(x), 0, ln(2)),
   "06009-10": lambda: definite_integral(ln(x) / x**2, 1, E),
   "06009-11": lambda: definite_integral(x * exp(-x), 0, 1),
   "06009-12": lambda: parts_of_x_times_derivative(0, 2, 3, 5, 4 - 1),
   "06009-13": lambda: definite_integral(x * cos(2*x), 0, pi / 4),
   "06009-14": lambda: definite_integral(x * ln(x), 1, 2),
   "06009-15": lambda: definite_integral((x + 1) * exp(x), 0, 1),
   "06009-16": lambda: parts_of_x_times_derivative(2, 4, 3, 7, 9),
   "06009-17": lambda: definite_integral(x**2 * sin(x), 0, pi),
   "06009-18": lambda: definite_integral(x * sec(x)**2, 0, pi / 3),
   "06009-19": lambda: parts_of_x_times_derivative(0, 2, 4, 1, 5),

   "06010-00": lambda: definite_integral((x**2 + 1) / (x**2 - 1), 2, 3),
   "06010-01": lambda: definite_integral(x**2 / (x**2 - 4), 3, 4),
   "06010-02": lambda: definite_integral((x**2 + x) / (x**2 - 3*x + 2), 3, 4),
   "06010-03": lambda: definite_integral((2*x**2 - 3) / (x**2 - 3*x + 2), 3, 5),
   "06010-04": lambda: definite_integral(x**3 / (x**2 - 1), 2, 3),
   "06010-05": lambda: definite_integral((x**3 + 2) / (x**2 - x), 2, 3),
   "06010-06": lambda: definite_integral((x**2 + 3*x) / (x**2 + 3*x + 2), 0, 1),
   "06010-07": lambda: definite_integral(3*x**2 / (x**2 - x - 2), 3, 4),
   "06010-08": lambda: definite_integral((x**2 - 2) / (x**2 + 2*x), 1, 2),
   "06010-09": lambda: definite_integral((x**2 + 4) / (x**2 - 4*x + 3), 4, 5),
   "06010-10": lambda: definite_integral((2*x**2 + x) / (x**2 + 4*x + 3), 0, 2),
   "06010-11": lambda: definite_integral((x**3 - 1) / (x**2 + 3*x + 2), 0, 1),
   "06010-12": lambda: definite_integral(x**2 / (x**2 + 4*x + 3), 0, 1),
   "06010-13": lambda: definite_integral((x**2 + 2*x + 3) / (x**2 - 1), 2, 4),
   "06010-14": lambda: definite_integral(x**2 / (2*x**2 + 3*x + 1), 0, 1),
   "06010-15": lambda: definite_integral(x**3 / (x**2 - 3*x + 2), 3, 4),
   "06010-16": lambda: pinned_antiderivative_value((x**2 - x + 1) / (x**2 - x - 6), 4, 1, 5),
   "06010-17": lambda: pinned_antiderivative_value(3*x**2 / (x**2 + 3*x + 2), 0, 2, 1),
   "06010-18": lambda: pinned_antiderivative_value((x**2 + 1) / (x**2 + 3*x + 2), 0, 3, 1),
   "06010-19": lambda: pinned_antiderivative_value((x**3 + x) / (x**2 + 3*x + 2), 0, 1, 1),

   "06012-00": lambda: accumulation_derivative(sqrt(t + 5), 0, x**2, 2),
   "06012-01": lambda: accumulation_derivative(sqrt(t**3 + 1), 2*x, 5, 1),
   "06012-02": lambda: accumulation_derivative(1 / t, x**2, x, 2),
   "06012-03": lambda: fundamental_theorem_from_values({1: 4, 3: 5, 9: -2}, x**2, 10, 3),
   "06012-04": lambda: accumulation_derivative(1 / (t + 1), 0, x**3, 2),
   "06012-05": lambda: fundamental_theorem_from_values({3: 1, 6: -2, 9: 4}, 2*x, x**2, 3),
   "06012-06": lambda: accumulation_derivative(4*t**2, sin(x), 3, pi / 6),
   "06012-07": lambda: accumulation_derivative(exp(t**2), 0, 2*x, Rational(1, 2)),
   "06012-08": lambda: accumulation_derivative(1 / (t**2 + 1), x, 3*x, 1),
   "06012-09": lambda: fundamental_theorem_from_values({1: -1, 3: 4}, 2*x + 1, 0, 1),
   "06012-10": lambda: accumulation_derivative(sin(t), 0, 2*x, pi / 4),
   "06012-11": lambda: fundamental_theorem_from_values({2: 3, 4: -1, 8: 2}, x**2, x**3, 2),
   "06012-12": lambda: accumulation_derivative(sqrt(t + 1), x**3, 2, 2),
   "06012-13": lambda: accumulation_derivative(1 / (t**2 + 1), 1, x**2 + 1, 1),
   "06012-14": lambda: accumulation_derivative(sqrt(1 - t**2), cos(x), sin(x), pi / 4),
   "06012-15": lambda: fundamental_theorem_from_values({1: -2, 2: 5}, x**2 - 3, 4, 2),
   "06012-16": lambda: accumulation_derivative(ln(t), 1, x**3, 2),
   "06012-17": lambda: accumulation_derivative(ln(t), x, 2*x, E),
   "06012-18": lambda: accumulation_derivative(t**3 + 1, sqrt(x), 3, 4),
   "06012-19": lambda: fundamental_theorem_from_values({0: 3, 1: -2, 2: 5}, 1 - x, x**2 + 1, 1),

   "06013-00": lambda: combination_integral(4, 0, [(2, -(10 - 3))], 5),
   "06013-01": lambda: combination_integral(1, 3, [(1, 12 - 5), (2, -4)], 0),
   "06013-02": lambda: combination_integral(5, 0, [(3, -(6 - (-4)))], 1),
   "06013-03": lambda: combination_integral(1, -2, [(1, -(8 - (-2)))], -3),
   "06013-04": lambda: combination_integral(0, 2, [(3, 9 - 4), (-1, -(-5))], 0),
   "06013-05": lambda: combination_integral(7, 1, [(2, -(-3 + (-5)))], 2),
   "06013-06": lambda: combination_integral(5, 1, [(2, -(14 - 6))], 3),
   "06013-07": lambda: combination_integral(-1, 2, [(2, 7 - (-3)), (3, -6)], 0),
   "06013-08": lambda: combination_integral(4, -3, [(-1, -(5 + (-2)))], 4),
   "06013-09": lambda: combination_integral(3, 0, [(3, -(-5 - 4))], -2),
   "06013-10": lambda: combination_integral(2, 4, [(-2, 11 - 6), (1, -3)], 0),
   "06013-11": lambda: combination_integral(8, 2, [(2, -(7 + 6))], -1),
   "06013-12": lambda: combination_integral(-1, -4, [(-1, -(9 - (-3)))], 2),
   "06013-13": lambda: combination_integral(0, 5, [(4, -6 - 2), (-3, -2)], 0),
   "06013-14": lambda: combination_integral(3, 0, [(3, -(4 - 9))], 2),
   "06013-15": lambda: combination_integral(6, 2, [(4, -(15 - 5))], 1),
   "06013-16": lambda: combination_integral(3, 6, [(1, 20 - 8), (4, -(-7))], 0),
   "06013-17": lambda: combination_integral(4, -1, [(2, -(-2 + 8))], -3),
   "06013-18": lambda: combination_integral(2, 0, [(2, -(12 - 20))], 3),
   "06013-19": lambda: combination_integral(-2, 0, [(-3, 5 - (-4)), (2, -1)], 0),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
