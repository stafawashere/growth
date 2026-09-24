"""Blind answers for the unit 5 generated items in stems_T.json.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, never from a key, a worked solution or a template. Each statement answer is the choice
text whose verdict matches the sign of f' on either side of the critical point.
"""
import sympy
from sympy import Rational

from tools.key_recheck import x

SIDE_OFFSET = Rational(1, 1000)

MAXIMUM_BY_SIGN_CHANGE = "f has a relative maximum at x = {point}, because f' changes from positive to negative at x = {point}."
MINIMUM_BY_SIGN_CHANGE = "f has a relative minimum at x = {point}, because f' changes from negative to positive at x = {point}."
NEITHER_NO_SIGN_CHANGE = "f has neither a relative minimum nor a relative maximum at x = {point}, because f' does not change sign at x = {point}."


def extremum_choice(derivative_expression, point):
   left_sign = sympy.sign(derivative_expression.subs(x, point - SIDE_OFFSET))
   right_sign = sympy.sign(derivative_expression.subs(x, point + SIDE_OFFSET))
   is_critical = derivative_expression.subs(x, point) == 0

   if not is_critical:
      raise ValueError(f"x = {point} is not a critical point")

   rises_then_falls = left_sign > 0 and right_sign < 0
   falls_then_rises = left_sign < 0 and right_sign > 0

   if rises_then_falls:
      return MAXIMUM_BY_SIGN_CHANGE.format(point=point)

   if falls_then_rises:
      return MINIMUM_BY_SIGN_CHANGE.format(point=point)

   return NEITHER_NO_SIGN_CHANGE.format(point=point)


BY_SUFFIX = {
   "05003-30": lambda: extremum_choice(-2*x * (x + 1)**2 * (x**2 + 1), -1),
   "05003-31": lambda: extremum_choice(2 * (x - 1) * (x - 5) * (x**2 + 1), 1),
   "05003-32": lambda: extremum_choice(-(x + 1) * (x - 3), -1),
   "05003-33": lambda: extremum_choice(-2 * (x + 1)**2 * (x - 3) * (x**2 + 1), -1),
   "05003-34": lambda: extremum_choice((x - 1) * (x - 3), 1),
   "05003-35": lambda: extremum_choice((x + 1)**2 * (x + 2), -1),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
