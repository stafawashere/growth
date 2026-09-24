"""Blind answers for the unit 9 generated items in stems_T.json.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, never from a key, a worked solution or a template. Values are computed at 30 digits
and returned unrounded.
"""
import sympy
from sympy import cos, sin

from tools.key_recheck import theta

DIGITS = 30


def polar_coordinate_rate(radius, at, coordinate):
   is_horizontal = coordinate == "x"
   position = radius * cos(theta) if is_horizontal else radius * sin(theta)
   rate = sympy.diff(position, theta).subs(theta, at)

   return sympy.N(rate, DIGITS)


def ray_distance_rate(first_radius, second_radius, at):
   """D is |r1 - r2| along the ray, so its rate carries the sign of r1 - r2 at the angle."""
   gap = first_radius - second_radius
   gap_sign = sympy.sign(sympy.N(gap.subs(theta, at), DIGITS))
   rate = gap_sign * sympy.diff(gap, theta).subs(theta, at)

   return sympy.N(rate, DIGITS)


BY_SUFFIX = {
   "99002-30": lambda: polar_coordinate_rate(2 * sin(2*theta) + 4, sympy.Float("0.9", DIGITS), "x"),
   "99002-31": lambda: polar_coordinate_rate(sin(2*theta) + 5, sympy.Float("1.1", DIGITS), "x"),
   "99002-32": lambda: polar_coordinate_rate(2 * sin(theta) + 1, sympy.Float("2.2", DIGITS), "x"),
   "99002-33": lambda: polar_coordinate_rate(3 * cos(2*theta) + 1, sympy.Float("0.9", DIGITS), "x"),
   "99002-34": lambda: polar_coordinate_rate(sin(2*theta) + 4, sympy.Float("0.9", DIGITS), "y"),
   "99002-35": lambda: polar_coordinate_rate(4 * cos(theta) + 5, sympy.Float("0.7", DIGITS), "x"),

   "99006-30": lambda: ray_distance_rate(2*theta * sin(theta) + 6, cos(theta) + 4, sympy.Float("1.2", DIGITS)),
   "99006-31": lambda: ray_distance_rate(theta * sin(theta) + 10, 3 * cos(theta) + 3, sympy.Float("1.2", DIGITS)),
   "99006-32": lambda: ray_distance_rate(-theta * sin(theta) + 10, 2 * sin(theta) + 2, sympy.Float("1.1", DIGITS)),
   "99006-33": lambda: ray_distance_rate(2*theta * sin(theta) + 6, 2 * sin(theta) + 1, sympy.Float("0.3", DIGITS)),
   "99006-34": lambda: ray_distance_rate(3*theta * sin(theta) + 12, 2 * sin(theta) + 3, sympy.Float("1.2", DIGITS)),
   "99006-35": lambda: ray_distance_rate(-2*theta * sin(theta) + 12, 3 * sin(theta) + 3, sympy.Float("0.5", DIGITS)),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
