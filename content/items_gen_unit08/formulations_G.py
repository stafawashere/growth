"""Answers to the batch G unit 8 generated items, computed from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The solver
read only stems_G.json, never a key, a worked solution or a template, so a match with the stored
key is independent evidence that the key answers the stem.
"""
import mpmath
import sympy

mpmath.mp.dps = 30


def as_sympy(value):
   return sympy.Float(mpmath.nstr(value, 30), 30)


def log_model(coefficient, divisor, constant):
   """A(t) = constant + coefficient ln(t^2 / divisor + 1); a decreasing model has a negative coefficient."""
   return lambda time: constant + coefficient * mpmath.log(mpmath.mpf(time)**2 / divisor + 1)


def average_rate_of_change(coefficient, divisor, constant, start, end):
   model = log_model(coefficient, divisor, constant)

   return as_sympy((model(end) - model(start)) / (end - start))


def column_total(amplitude, divisor, offset, cross_section_area, top_depth, bottom_depth):
   density = lambda depth: amplitude * mpmath.sin(depth**2 / divisor) + offset

   return as_sympy(mpmath.mpf(cross_section_area) * mpmath.quad(density, [top_depth, bottom_depth]))


def square_side(side):
   return mpmath.mpf(side)**2


BY_SUFFIX = {
   "99007-00": lambda: average_rate_of_change(-5, 2, 50, 3, 5),
   "99007-01": lambda: average_rate_of_change(2, 2, 20, 3, 5),
   "99007-02": lambda: average_rate_of_change(-3, 4, 70, 2, 7),
   "99007-03": lambda: average_rate_of_change(-2, 3, 40, 3, 5),
   "99007-04": lambda: average_rate_of_change(2, 4, 75, 1, 6),
   "99007-05": lambda: average_rate_of_change(-2, 3, 35, 2, 7),
   "99007-06": lambda: average_rate_of_change(6, 4, 80, 1, 6),
   "99007-07": lambda: average_rate_of_change(8, 3, 20, 2, 6),
   "99007-08": lambda: average_rate_of_change(7, 2, 20, 2, 5),
   "99007-09": lambda: average_rate_of_change(2, 3, 35, 1, 3),
   "99007-10": lambda: average_rate_of_change(-3, 2, 55, 2, 6),
   "99007-11": lambda: average_rate_of_change(8, 1, 55, 2, 4),
   "99007-12": lambda: average_rate_of_change(-6, 4, 65, 3, 7),
   "99007-13": lambda: average_rate_of_change(6, 1, 70, 1, 5),
   "99007-14": lambda: average_rate_of_change(-6, 2, 65, 1, 5),
   "99007-15": lambda: average_rate_of_change(5, 1, 55, 3, 7),
   "99007-16": lambda: average_rate_of_change(5, 2, 25, 3, 8),
   "99007-17": lambda: average_rate_of_change(5, 4, 80, 3, 7),
   "99007-18": lambda: average_rate_of_change(-9, 2, 55, 3, 7),
   "99007-19": lambda: average_rate_of_change(-2, 1, 65, 3, 5),
   "99007-20": lambda: average_rate_of_change(8, 4, 65, 3, 5),
   "99007-21": lambda: average_rate_of_change(7, 1, 35, 1, 3),

   "99009-00": lambda: column_total(8, 4, 45, square_side("3.5"), 0, 3),
   "99009-01": lambda: column_total(4, 2, 35, square_side(2), 2, 5),
   "99009-02": lambda: column_total(8, 3, 30, square_side(3), 0, 6),
   "99009-03": lambda: column_total(10, 3, 60, "12.25", 1, 7),
   "99009-04": lambda: column_total(6, 2, 60, square_side(2), 2, 7),
   "99009-05": lambda: column_total(8, 4, 25, square_side("2.5"), 1, 6),
   "99009-06": lambda: column_total(4, 5, 20, square_side(3), 0, 5),
   "99009-07": lambda: column_total(4, 5, 25, 4, 0, 5),
   "99009-08": lambda: column_total(8, 4, 40, square_side("1.5"), 0, 4),
   "99009-09": lambda: column_total(12, 4, 60, 4, 1, 6),
   "99009-10": lambda: column_total(4, 2, 30, "12.25", 0, 4),
   "99009-11": lambda: column_total(10, 3, 25, "2.25", 1, 7),
   "99009-12": lambda: column_total(10, 3, 55, square_side("2.5"), 1, 6),
   "99009-13": lambda: column_total(4, 5, 20, 9, 0, 6),
   "99009-14": lambda: column_total(6, 5, 45, 9, 0, 3),
   "99009-15": lambda: column_total(12, 5, 45, square_side("3.5"), 0, 3),
   "99009-16": lambda: column_total(8, 4, 30, square_side(2), 0, 6),
   "99009-17": lambda: column_total(10, 5, 40, square_side("1.5"), 0, 4),
   "99009-18": lambda: column_total(12, 2, 30, 4, 1, 4),
   "99009-19": lambda: column_total(8, 4, 60, "6.25", 0, 5),
   "99009-20": lambda: column_total(8, 4, 55, "6.25", 2, 8),
   "99009-21": lambda: column_total(6, 4, 30, "6.25", 2, 6),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
