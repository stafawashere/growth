"""Each generated unit 9 item in batch s15, written as the SymPy computation of the answer its stem asks for.

Written from the stems alone, never from a stored key.
"""
import sympy
from sympy import cos, pi, sin

from tools.key_recheck import definite_integral, theta

FULL_TURN = 2 * pi


def polar_area(radius, lower, upper):
   return sympy.simplify(definite_integral(radius**2 / 2, lower, upper, variable=theta))


def enclosed_area(radius):
   # every curve in this batch keeps r > 0, so one full turn traces the boundary exactly once
   smallest_radius = sympy.minimum(radius, theta, sympy.Interval(0, FULL_TURN))
   is_positive_everywhere = smallest_radius > 0

   if not is_positive_everywhere:
      raise ValueError(f"radius {radius} reaches zero, the full-turn integral is not the enclosed area")

   return polar_area(radius, 0, FULL_TURN)


BY_SUFFIX = {
   "09014-00": lambda: enclosed_area(5 * sin(theta) + 6),
   "09014-01": lambda: polar_area(3 * sin(theta) + 13, 0, pi),
   "09014-02": lambda: enclosed_area(13 - 12 * cos(theta)),
   "09014-03": lambda: polar_area(6 * sin(2 * theta) + 11, 0, pi),
   "09014-04": lambda: enclosed_area(12 - 3 * sin(theta)),
   "09014-05": lambda: enclosed_area(13 * sin(2 * theta) + 15),
   "09014-06": lambda: polar_area(13 - 11 * cos(2 * theta), 0, pi / 2),
   "09014-07": lambda: polar_area(5 * sin(2 * theta) + 6, 0, pi),
   "09014-08": lambda: polar_area(sin(2 * theta) + 8, 0, pi / 2),
   "09014-09": lambda: polar_area(11 * cos(2 * theta) + 15, 0, pi / 2),
   "09014-10": lambda: enclosed_area(11 - 4 * cos(theta)),
   "09014-11": lambda: polar_area(11 - 2 * cos(theta), 0, pi / 2),
   "09014-12": lambda: enclosed_area(12 - 4 * cos(theta)),
   "09014-13": lambda: polar_area(sin(theta) + 2, 0, pi),
   "09014-14": lambda: enclosed_area(7 * sin(theta) + 8),
   "09014-15": lambda: enclosed_area(6 * sin(2 * theta) + 15),
   "09014-16": lambda: polar_area(6 * sin(theta) + 12, 0, pi),
   "09014-17": lambda: enclosed_area(12 * cos(theta) + 15),
   "09014-18": lambda: enclosed_area(11 - 10 * cos(2 * theta)),
   "09014-19": lambda: polar_area(7 - 6 * cos(theta), 0, pi),
   "09014-20": lambda: enclosed_area(12 - 9 * sin(2 * theta)),
   "09014-21": lambda: polar_area(7 * sin(2 * theta) + 8, 0, pi / 2),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
