"""Blind answers for the unit 8 generated items in stems_T.json.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, never from a key, a worked solution or a template. Each item revolves the region
between f and a horizontal line about that line, so the solid is a stack of disks of radius f - k.
"""
import sympy
from sympy import sqrt

from tools.key_recheck import definite_integral, x


def meeting_point_left_of(function, axis_height, right):
   meetings = sympy.solve(sympy.Eq(function, axis_height), x)
   real_left = [point for point in meetings if point.is_real and bool(point < right)]

   return max(real_left)


def disk_volume_about_line(function, axis_height, right, left=None):
   has_given_left = left is not None
   lower = left if has_given_left else meeting_point_left_of(function, axis_height, right)

   return sympy.pi * definite_integral((function - axis_height)**2, lower, right)


BY_SUFFIX = {
   "08012-30": lambda: disk_volume_about_line(3 * sqrt(x) - 1, -1, 4, left=1),
   "08012-31": lambda: disk_volume_about_line(4*x**2 - 1, -1, 2),
   "08012-32": lambda: disk_volume_about_line(3*x + 3, 3, 1),
   "08012-33": lambda: disk_volume_about_line(x + 2, 2, 4),
   "08012-34": lambda: disk_volume_about_line(2*x**2 + 1, 1, 4),
   "08012-35": lambda: disk_volume_about_line(2*x**2 - 1, -1, 4),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
