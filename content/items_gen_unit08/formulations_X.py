"""Blind re-solve of generated unit 8 items, batch X, each answer computed from its stem alone.

Written from var/p4/resolve/items_gen_unit08/stems_X.json and nothing else about these items by a blind
solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The file is self-contained. Each
average value, asked correct to three decimal places, comes back at 30 significant digits, unrounded.
"""
import mpmath
import sympy
from sympy import Rational

from tools.key_recheck import t

WORKING_DIGITS = 30


def expression(text):
   return sympy.sympify(text, locals={"t": t})


def average_value_to_three_places(rate, start, end):
   """The integral of rate over [start, end] divided by the interval's length, by quadrature."""
   rate_function = sympy.lambdify(t, rate, "mpmath")

   with mpmath.workdps(WORKING_DIGITS + 10):
      left = mpmath.mpf(sympy.Rational(start))
      right = mpmath.mpf(sympy.Rational(end))
      average = mpmath.quad(rate_function, [left, right]) / (right - left)

      return sympy.Float(mpmath.nstr(average, WORKING_DIGITS), WORKING_DIGITS)


BY_SUFFIX = {
   "08001-00": lambda: average_value_to_three_places(expression("5*cos(t**2/4) - 1"), 0, 4),
   "08001-01": lambda: average_value_to_three_places(expression("5*cos(t**2/2) - 2"), 0, 4),
   "08001-02": lambda: average_value_to_three_places(expression("2*cos(t**2/3)"), 0, 4),
   "08001-03": lambda: average_value_to_three_places(expression("5*cos(t**2/3) + 2"), 0, Rational(7, 2)),
   "08001-04": lambda: average_value_to_three_places(expression("8*cos(t**2) + 2"), 0, 3),
   "08001-05": lambda: average_value_to_three_places(expression("7*cos(t**2/2) + 1"), 0, Rational(7, 2)),
   "08001-06": lambda: average_value_to_three_places(expression("7*cos(t**2) + 1"), 0, Rational(7, 2)),
   "08001-07": lambda: average_value_to_three_places(expression("4*cos(t**2/2) - 2"), 0, Rational(7, 2)),
   "08001-08": lambda: average_value_to_three_places(expression("8*cos(t**2/2) + 2"), 0, 4),
   "08001-09": lambda: average_value_to_three_places(expression("8*cos(t**2) - 1"), 0, 3),
   "08001-10": lambda: average_value_to_three_places(expression("7*cos(t**2) - 1"), 0, 2),
   "08001-11": lambda: average_value_to_three_places(expression("9*cos(t**2) + 3"), 0, 2),
   "08001-12": lambda: average_value_to_three_places(expression("3*cos(t**2)"), 0, Rational(7, 2)),
   "08001-13": lambda: average_value_to_three_places(expression("6*cos(t**2) + 3"), 0, 3),
   "08001-14": lambda: average_value_to_three_places(expression("6*cos(t**2) - 2"), 0, 3),
   "08001-15": lambda: average_value_to_three_places(expression("8*cos(t**2/2)"), 0, Rational(7, 2)),
   "08001-16": lambda: average_value_to_three_places(expression("6*cos(t**2/3) + 3"), 0, Rational(7, 2)),
   "08001-17": lambda: average_value_to_three_places(expression("6*cos(t**2/2) - 2"), 0, 3),
   "08001-18": lambda: average_value_to_three_places(expression("6*cos(t**2/3) - 1"), 0, 4),
   "08001-19": lambda: average_value_to_three_places(expression("2*cos(t**2) - 1"), 0, Rational(7, 2)),
   "08001-20": lambda: average_value_to_three_places(expression("7*cos(t**2/2) + 2"), 0, Rational(7, 2)),
   "08001-21": lambda: average_value_to_three_places(expression("4*cos(t**2)"), 0, 2),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
