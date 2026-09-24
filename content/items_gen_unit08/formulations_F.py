"""Blind formulations for the unit 8 generated items in stems_F.json.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24. No key, candidate, template or worked solution was read. Calculator answers are
returned at full precision, exact answers as SymPy expressions, and statement items return the
text of the choice the mathematics selects, copied from the stems file.
"""
import re

import mpmath
import sympy
from sympy import Integral, Rational, atan, exp, ln, pi, sqrt

from tools.key_recheck import t, x, y

mpmath.mp.dps = 30

PRECISION = 30
DISPLAY_TOLERANCE = 0.0005 + 1e-9
ROOT_SCAN_STEPS = 4000
INTEGRAND_SAMPLE_COUNT = 7

s = sympy.Symbol("s")

CHOICES = {
   "08006-00": [
      "The amount is greatest at t = 10, where A is 190 barrels, because A' is positive on the interval from t = 7.341 to t = 10.",
      "The amount is greatest at t = 10, where A is 190 barrels, the largest of the values of A at t = 0, at t = 7.341 and at t = 10.",
      "The amount is greatest at t = 2.659, where A is 18.495 barrels, the largest of the values of A at t = 0, at both critical points and at t = 10.",
      "The amount is greatest at t = 2.659, where A is 198.495 barrels, the largest of the values of A at t = 0, at both critical points and at t = 10.",
   ],
   "08006-01": [
      "The amount is greatest at t = 2.256, where A is 205.482 barrels, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 2.256, where A is 25.482 barrels, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 8, where A is 204 barrels, because A' is positive on the interval from t = 5.744 to t = 8.",
      "The amount is greatest at t = 8, where A is 204 barrels, the largest of the values of A at t = 0, at t = 5.744 and at t = 8.",
   ],
   "08006-02": [
      "The amount is greatest at t = 2.213, where A is 29.237 barrels, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 2.213, where A is 59.237 barrels, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 8, where A is 54 barrels, because A' is positive on the interval from t = 5.787 to t = 8.",
      "The amount is greatest at t = 8, where A is 54 barrels, the largest of the values of A at t = 0, at t = 5.787 and at t = 8.",
   ],
   "08006-03": [
      "The amount is greatest at t = 12, where A is 86 tons, because A' is positive on the interval from t = 8.809 to t = 12.",
      "The amount is greatest at t = 12, where A is 86 tons, the largest of the values of A at t = 0, at t = 8.809 and at t = 12.",
      "The amount is greatest at t = 3.191, where A is 116.582 tons, the largest of the values of A at t = 0, at both critical points and at t = 12.",
      "The amount is greatest at t = 3.191, where A is 66.582 tons, the largest of the values of A at t = 0, at both critical points and at t = 12.",
   ],
   "08006-04": [
      "The amount is greatest at t = 10, where A is 190 gallons, the largest of the values of A at t = 0, at both critical points and at t = 10.",
      "The amount is greatest at t = 10, where A is 50 gallons, the largest of the values of A at t = 0, at both critical points and at t = 10.",
      "The amount is greatest at t = 3.333, where A is 170.450 gallons, because A' changes from positive to negative there.",
      "The amount is greatest at t = 3.333, where A is 170.450 gallons, the larger of the values of A at the two critical points.",
   ],
   "08006-05": [
      "The amount is greatest at t = 16, where A is 146 barrels, the largest of the values of A at t = 0, at both critical points and at t = 16.",
      "The amount is greatest at t = 16, where A is 96 barrels, the largest of the values of A at t = 0, at both critical points and at t = 16.",
      "The amount is greatest at t = 4.865, where A is 122.408 barrels, because A' changes from positive to negative there.",
      "The amount is greatest at t = 4.865, where A is 122.408 barrels, the larger of the values of A at the two critical points.",
   ],
   "08006-06": [
      "The amount is greatest at t = 2.160, where A is 174.531 tons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 2.160, where A is 24.531 tons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 8, where A is 166 tons, because A' is positive on the interval from t = 5.840 to t = 8.",
      "The amount is greatest at t = 8, where A is 166 tons, the largest of the values of A at t = 0, at t = 5.840 and at t = 8.",
   ],
   "08006-07": [
      "The amount is greatest at t = 24, where A is 204 gallons, because A' is positive on the interval from t = 17.360 to t = 24.",
      "The amount is greatest at t = 24, where A is 204 gallons, the largest of the values of A at t = 0, at t = 17.360 and at t = 24.",
      "The amount is greatest at t = 6.640, where A is 175.424 gallons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 6.640, where A is 235.424 gallons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
   ],
   "08006-08": [
      "The amount is greatest at t = 24, where A is 24 barrels, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 24, where A is 94 barrels, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 8.000, where A is 84.616 barrels, because A' changes from positive to negative there.",
      "The amount is greatest at t = 8.000, where A is 84.616 barrels, the larger of the values of A at the two critical points.",
   ],
   "08006-09": [
      "The amount is greatest at t = 10, where A is 130 barrels, the largest of the values of A at t = 0, at both critical points and at t = 10.",
      "The amount is greatest at t = 10, where A is 20 barrels, the largest of the values of A at t = 0, at both critical points and at t = 10.",
      "The amount is greatest at t = 2.902, where A is 128.132 barrels, because A' changes from positive to negative there.",
      "The amount is greatest at t = 2.902, where A is 128.132 barrels, the larger of the values of A at the two critical points.",
   ],
   "08006-10": [
      "The amount is greatest at t = 16, where A is 62 barrels, because A' is positive on the interval from t = 11.487 to t = 16.",
      "The amount is greatest at t = 16, where A is 62 barrels, the largest of the values of A at t = 0, at t = 11.487 and at t = 16.",
      "The amount is greatest at t = 4.513, where A is 33.976 barrels, the largest of the values of A at t = 0, at both critical points and at t = 16.",
      "The amount is greatest at t = 4.513, where A is 63.976 barrels, the largest of the values of A at t = 0, at both critical points and at t = 16.",
   ],
   "08006-11": [
      "The amount is greatest at t = 20, where A is 100 tons, the largest of the values of A at t = 0, at both critical points and at t = 20.",
      "The amount is greatest at t = 20, where A is 270 tons, the largest of the values of A at t = 0, at both critical points and at t = 20.",
      "The amount is greatest at t = 6.667, where A is 230.900 tons, because A' changes from positive to negative there.",
      "The amount is greatest at t = 6.667, where A is 230.900 tons, the larger of the values of A at the two critical points.",
   ],
   "08006-12": [
      "The amount is greatest at t = 24, where A is 84 tons, because A' is positive on the interval from t = 17.360 to t = 24.",
      "The amount is greatest at t = 24, where A is 84 tons, the largest of the values of A at t = 0, at t = 17.360 and at t = 24.",
      "The amount is greatest at t = 6.640, where A is 29.237 tons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 6.640, where A is 89.237 tons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
   ],
   "08006-13": [
      "The amount is greatest at t = 24, where A is 104 tons, because A' is positive on the interval from t = 17.231 to t = 24.",
      "The amount is greatest at t = 24, where A is 104 tons, the largest of the values of A at t = 0, at t = 17.231 and at t = 24.",
      "The amount is greatest at t = 6.769, where A is 105.482 tons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 6.769, where A is 25.482 tons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
   ],
   "08006-14": [
      "The amount is greatest at t = 2.160, where A is 191.328 tons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 2.160, where A is 61.328 tons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 8, where A is 170 tons, because A' is positive on the interval from t = 5.840 to t = 8.",
      "The amount is greatest at t = 8, where A is 170 tons, the largest of the values of A at t = 0, at t = 5.840 and at t = 8.",
   ],
   "08006-15": [
      "The amount is greatest at t = 20, where A is 170 tons, the largest of the values of A at t = 0, at both critical points and at t = 20.",
      "The amount is greatest at t = 20, where A is 80 tons, the largest of the values of A at t = 0, at both critical points and at t = 20.",
      "The amount is greatest at t = 6.667, where A is 138.720 tons, because A' changes from positive to negative there.",
      "The amount is greatest at t = 6.667, where A is 138.720 tons, the larger of the values of A at the two critical points.",
   ],
   "08006-16": [
      "The amount is greatest at t = 24, where A is 98 tons, because A' is positive on the interval from t = 17.231 to t = 24.",
      "The amount is greatest at t = 24, where A is 98 tons, the largest of the values of A at t = 0, at t = 17.231 and at t = 24.",
      "The amount is greatest at t = 6.769, where A is 100.964 tons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 6.769, where A is 50.964 tons, the largest of the values of A at t = 0, at both critical points and at t = 24.",
   ],
   "08006-17": [
      "The amount is greatest at t = 2.667, where A is 69.232 gallons, because A' changes from positive to negative there.",
      "The amount is greatest at t = 2.667, where A is 69.232 gallons, the larger of the values of A at the two critical points.",
      "The amount is greatest at t = 8, where A is 48 gallons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 8, where A is 88 gallons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
   ],
   "08006-18": [
      "The amount is greatest at t = 12, where A is 192 gallons, the largest of the values of A at t = 0, at both critical points and at t = 12.",
      "The amount is greatest at t = 12, where A is 72 gallons, the largest of the values of A at t = 0, at both critical points and at t = 12.",
      "The amount is greatest at t = 4.394, where A is 159.174 gallons, because A' changes from positive to negative there.",
      "The amount is greatest at t = 4.394, where A is 159.174 gallons, the larger of the values of A at the two critical points.",
   ],
   "08006-19": [
      "The amount is greatest at t = 2.213, where A is 79.746 tons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 2.213, where A is 9.746 tons, the largest of the values of A at t = 0, at both critical points and at t = 8.",
      "The amount is greatest at t = 8, where A is 78 tons, because A' is positive on the interval from t = 5.787 to t = 8.",
      "The amount is greatest at t = 8, where A is 78 tons, the largest of the values of A at t = 0, at t = 5.787 and at t = 8.",
   ],
   "08006-20": [
      "The amount is greatest at t = 24, where A is 122 barrels, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 24, where A is 72 barrels, the largest of the values of A at t = 0, at both critical points and at t = 24.",
      "The amount is greatest at t = 9.239, where A is 87.824 barrels, because A' changes from positive to negative there.",
      "The amount is greatest at t = 9.239, where A is 87.824 barrels, the larger of the values of A at the two critical points.",
   ],
   "08006-21": [
      "The amount is greatest at t = 12, where A is 154 tons, because A' is positive on the interval from t = 8.680 to t = 12.",
      "The amount is greatest at t = 12, where A is 154 tons, the largest of the values of A at t = 0, at t = 8.680 and at t = 12.",
      "The amount is greatest at t = 3.320, where A is 159.237 tons, the largest of the values of A at t = 0, at both critical points and at t = 12.",
      "The amount is greatest at t = 3.320, where A is 29.237 tons, the largest of the values of A at t = 0, at both critical points and at t = 12.",
   ],
   "08014-02": [
      "\\( \\int_{0}^{6} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{2}^{6} \\left(1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{2}^{6} \\sqrt{1 + \\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{2}^{6} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
   "08014-05": [
      "\\( \\int_{0}^{7} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{3}^{7} \\left(1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{3}^{7} \\sqrt{1 + \\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{3}^{7} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
   "08014-08": [
      "\\( \\int_{0}^{2} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{1}^{2} \\left(1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{1}^{2} \\sqrt{1 + \\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{1}^{2} \\sqrt{1 + \\left(\\frac{3 \\left(3 x + 2\\right)}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
   "08014-09": [
      "\\( \\int_{0}^{3} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{2}^{3} \\left(1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{2}^{3} \\sqrt{1 + \\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{4}}\\,dx \\)",
      "\\( \\int_{2}^{3} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{4}\\right)^{2}}\\,dx \\)",
   ],
   "08014-10": [
      "\\( \\int_{0}^{5} \\sqrt{1 + \\left(2 \\ln{\\left(x \\right)} + 2\\right)^{2}}\\,dx \\)",
      "\\( \\int_{2}^{5} \\left(1 + \\left(2 \\ln{\\left(x \\right)} + 2\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{2}^{5} \\sqrt{1 + 2 \\ln{\\left(x \\right)} + 2}\\,dx \\)",
      "\\( \\int_{2}^{5} \\sqrt{1 + \\left(2 \\ln{\\left(x \\right)} + 2\\right)^{2}}\\,dx \\)",
   ],
   "08014-12": [
      "\\( \\int_{0}^{3} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{2}^{3} \\left(1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{2}^{3} \\sqrt{1 + \\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}}\\,dx \\)",
      "\\( \\int_{2}^{3} \\sqrt{1 + \\left(\\frac{3 \\left(x + 4\\right) e^{\\frac{x}{4}}}{8}\\right)^{2}}\\,dx \\)",
   ],
   "08014-14": [
      "\\( \\int_{0}^{4} \\sqrt{1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{2}^{4} \\left(1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{2}^{4} \\sqrt{1 + \\frac{3 x + 2}{2 \\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{2}^{4} \\sqrt{1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
   "08014-15": [
      "\\( \\int_{0}^{5} \\sqrt{1 + \\left(\\frac{3 x + 2}{\\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{3}^{5} \\left(1 + \\left(\\frac{3 x + 2}{\\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{3}^{5} \\sqrt{1 + \\frac{3 x + 2}{\\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{3}^{5} \\sqrt{1 + \\left(\\frac{3 x + 2}{\\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
   "08014-17": [
      "\\( \\int_{0}^{4} \\sqrt{1 + \\left(\\frac{5 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{2}^{4} \\left(1 + \\left(\\frac{5 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{2}^{4} \\sqrt{1 + \\frac{5 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{2}^{4} \\sqrt{1 + \\left(\\frac{5 \\left(3 x + 2\\right)}{4 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
   "08014-20": [
      "\\( \\int_{0}^{6} \\sqrt{1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
      "\\( \\int_{3}^{6} \\left(1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}\\right)\\,dx \\)",
      "\\( \\int_{3}^{6} \\sqrt{1 + \\frac{3 x + 2}{2 \\sqrt{x + 1}}}\\,dx \\)",
      "\\( \\int_{3}^{6} \\sqrt{1 + \\left(\\frac{3 x + 2}{2 \\sqrt{x + 1}}\\right)^{2}}\\,dx \\)",
   ],
}


def full_precision(value):
   return sympy.Float(sympy.N(value, PRECISION), PRECISION)


def shows_value(displayed, computed):
   return abs(float(displayed) - float(computed)) <= DISPLAY_TOLERANCE


def single_or_all(found):
   return found[0] if len(found) == 1 else found


def numeric_roots(expression, variable, left, right):
   """Every root of expression strictly inside (left, right), found by a sign scan then refined."""
   function = sympy.lambdify(variable, expression, "mpmath")
   step = (mpmath.mpf(right) - mpmath.mpf(left)) / ROOT_SCAN_STEPS
   roots = []
   previous_point = mpmath.mpf(left) + step / 10
   previous_value = function(previous_point)

   for index in range(1, ROOT_SCAN_STEPS + 1):
      current_point = mpmath.mpf(left) + step * index - (step / 10 if index == ROOT_SCAN_STEPS else 0)
      current_value = function(current_point)
      has_crossed = previous_value * current_value <= 0

      if has_crossed:
         root = mpmath.findroot(function, (previous_point, current_point), solver="anderson")
         is_new = all(abs(root - known) > 1e-12 for known in roots)

         if is_new:
            roots.append(root)

      previous_point, previous_value = current_point, current_value

   return roots


def mean_value_time_from_rate(rate, start, end):
   rate_function = sympy.lambdify(s, rate, "mpmath")
   average_rate = mpmath.quad(rate_function, [start, end]) / (mpmath.mpf(end) - mpmath.mpf(start))
   roots = numeric_roots(rate - sympy.Float(average_rate, PRECISION), s, start, end)

   return single_or_all([full_precision(root) for root in roots])


def mean_value_time_from_amount(amount, start, end):
   return mean_value_time_from_rate(sympy.diff(amount, t).subs(t, s), start, end)


def total_distance(velocity, end):
   turning_points = [root for root in sympy.solve(velocity, t) if root.is_real and 0 < root < end]
   breakpoints = [sympy.Integer(0)] + sorted(turning_points) + [sympy.nsimplify(end)]
   pieces = zip(breakpoints[:-1], breakpoints[1:])

   return sympy.nsimplify(sum(sympy.Abs(sympy.integrate(velocity, (t, left, right))) for left, right in pieces))


def crossings(upper, lower):
   return sorted(root for root in sympy.solve(sympy.Eq(upper, lower), x) if root.is_real)


def area_between(upper, lower, left, right):
   inner_crossings = [root for root in crossings(upper, lower) if left < root < right]
   breakpoints = [sympy.nsimplify(left)] + inner_crossings + [sympy.nsimplify(right)]
   pieces = zip(breakpoints[:-1], breakpoints[1:])

   return sympy.simplify(sum(sympy.Abs(sympy.integrate(upper - lower, (x, a, b))) for a, b in pieces))


def enclosed_area(upper, lower):
   meeting_points = crossings(upper, lower)

   return area_between(upper, lower, meeting_points[0], meeting_points[-1])


def area_by_horizontal_slices(curve, line):
   """Region above the x-axis, right of the curve y = curve(x) and left of the line y = line(x)."""
   curve_x = sympy.solve(sympy.Eq(y, curve), x)[0]
   line_x = sympy.solve(sympy.Eq(y, line), x)[0]
   top = max(root for root in sympy.solve(sympy.Eq(curve_x, line_x), y) if root.is_real and root > 0)

   return sympy.simplify(sympy.integrate(line_x - curve_x, (y, 0, top)))


def cross_section_factor(shape, ratio=None):
   factors = {
      "square": sympy.Integer(1),
      "semicircle": pi / 8,
      "equilateral": sqrt(3) / 4,
      "isosceles right, hypotenuse in base": Rational(1, 4),
      "rectangle": ratio,
   }

   return factors[shape]


def cross_section_volume(upper, lower, shape, ratio=None):
   meeting_points = crossings(upper, lower)
   left, right = meeting_points[0], meeting_points[-1]
   width = upper - lower

   return sympy.simplify(cross_section_factor(shape, ratio) * sympy.integrate(width ** 2, (x, left, right)))


def cross_section_volume_numeric(upper, lower, left, right, shape, ratio=None):
   width = upper - lower
   area = cross_section_factor(shape, ratio) * width ** 2
   area_function = sympy.lambdify(x, area, "mpmath")

   return full_precision(mpmath.quad(area_function, [left, right]))


def disk_volume(function, axis, left, right):
   if left is None:
      left = min(root for root in sympy.solve(sympy.Eq(function, axis), x) if root.is_real and root < right)

   return sympy.simplify(pi * sympy.integrate((function - axis) ** 2, (x, left, right)))


def washer_volume(upper, lower, axis):
   meeting_points = crossings(upper, lower)
   left, right = meeting_points[0], meeting_points[-1]
   cross_section = sympy.expand((upper - axis) ** 2 - (lower - axis) ** 2)

   return sympy.simplify(pi * sympy.Abs(sympy.integrate(cross_section, (x, left, right))))


def arc_length_integral(function, left, right):
   return Integral(sqrt(1 + sympy.diff(function, x) ** 2), (x, left, right))


def arc_length(function, left, right):
   integrand = sympy.lambdify(x, sqrt(1 + sympy.diff(function, x) ** 2), "mpmath")

   return full_precision(mpmath.quad(integrand, [left, right]))


def same_integral(candidate, reference):
   candidate_limits = candidate.limits[0]
   reference_limits = reference.limits[0]
   has_same_limits = candidate_limits[1] == reference_limits[1] and candidate_limits[2] == reference_limits[2]

   if not has_same_limits:
      return False

   difference = candidate.function - reference.function
   left, right = float(reference_limits[1]), float(reference_limits[2])
   sample_points = [left + (right - left) * index / (INTEGRAND_SAMPLE_COUNT - 1) for index in range(INTEGRAND_SAMPLE_COUNT)]

   return all(abs(float(difference.subs(x, point))) < 1e-9 for point in sample_points)


def arc_length_choice(function, left, right, suffix, choice_integrals):
   """choice_integrals lists, in the order of CHOICES[suffix], each choice transcribed as a SymPy Integral."""
   reference = arc_length_integral(function, left, right)
   found = [text for text, candidate in zip(CHOICES[suffix], choice_integrals) if same_integral(candidate, reference)]

   return single_or_all(found)


MAXIMUM_PATTERN = re.compile(r"greatest at t = ([\d.]+), where A is ([\d.]+)")
LISTED_CANDIDATES_PATTERN = re.compile(r"largest of the values of A at t = 0, at t = ([\d.]+) and at t = ([\d.]+)\.")
BOTH_CRITICAL_PATTERN = re.compile(r"largest of the values of A at t = 0, at both critical points and at t = ([\d.]+)\.")


def justified_candidates(text, end):
   """The critical points a closed-interval justification compares, or None when the reasoning is not a candidates test."""
   listed = LISTED_CANDIDATES_PATTERN.search(text)
   both = BOTH_CRITICAL_PATTERN.search(text)

   if listed and shows_value(listed.group(2), end):
      return ("listed", [float(listed.group(1))])

   if both and shows_value(both.group(1), end):
      return ("both", None)

   return None


def greatest_amount_choice(rate, initial_amount, end, suffix):
   critical_times = numeric_roots(rate, t, 0, end)
   amount = lambda at: initial_amount + mpmath.quad(sympy.lambdify(t, rate, "mpmath"), [0, at])
   candidates = [mpmath.mpf(0)] + critical_times + [mpmath.mpf(end)]
   best_time = max(candidates, key=amount)
   best_amount = amount(best_time)
   found = []

   for text in CHOICES[suffix]:
      claim = MAXIMUM_PATTERN.search(text)
      has_time = shows_value(claim.group(1), best_time)
      has_amount = shows_value(claim.group(2), best_amount)
      justification = justified_candidates(text, end)

      if justification is None:
         covers_every_critical_point = False
      elif justification[0] == "both":
         covers_every_critical_point = len(critical_times) == 2
      else:
         covers_every_critical_point = all(
            any(shows_value(listed, critical) for listed in justification[1]) for critical in critical_times
         )

      is_correct = has_time and has_amount and covers_every_critical_point

      if is_correct:
         found.append(text)

   return single_or_all(found)


def tank_rate(amplitude, period_divisor, inflow_constant, outflow=0):
   return amplitude * sympy.cos(pi * t / period_divisor) + inflow_constant - outflow


def root_ratio(numerator, shift):
   return numerator * s / sqrt(s ** 2 + shift)


SQRT_TERM = x * sqrt(x + 1)
ROOT_DERIVATIVE = (3 * x + 2) / (2 * sqrt(x + 1))
EXP_DERIVATIVE = (x + 4) * exp(x / 4) / 4


def displayed_forms(displayed_derivative, left, right):
   return [
      Integral(sqrt(1 + displayed_derivative ** 2), (x, 0, right)),
      Integral(1 + displayed_derivative ** 2, (x, left, right)),
      Integral(sqrt(1 + displayed_derivative), (x, left, right)),
      Integral(sqrt(1 + displayed_derivative ** 2), (x, left, right)),
   ]


BY_SUFFIX = {
   "08002-00": lambda: mean_value_time_from_rate(exp(s / 4) / 2 + 3, 3, 5),
   "08002-01": lambda: mean_value_time_from_rate(root_ratio(6, 4) + 1, 3, 7),
   "08002-02": lambda: mean_value_time_from_rate(root_ratio(7, 5) + 2, 2, 4),
   "08002-03": lambda: mean_value_time_from_rate(root_ratio(7, 3) + 2, 3, 5),
   "08002-04": lambda: mean_value_time_from_amount(2*t + 6 * sqrt(t**2 + 2), 3, Rational(11, 2)),
   "08002-05": lambda: mean_value_time_from_rate(1 + 48 / (4 * s**2 + 9), 3, 6),
   "08002-06": lambda: mean_value_time_from_amount(t + 4 * sqrt(t**2 + 4), 2, 4),
   "08002-07": lambda: mean_value_time_from_amount(4*t + 2 * sqrt(t**2 + 3), 2, Rational(9, 2)),
   "08002-08": lambda: mean_value_time_from_rate(exp(s / 4) / 2 + 2, 2, 5),
   "08002-09": lambda: mean_value_time_from_rate(root_ratio(4, 3) + 3, 2, 5),
   "08002-10": lambda: mean_value_time_from_amount(3*t + 5 * exp(t / 5), 3, 6),
   "08002-11": lambda: mean_value_time_from_rate(root_ratio(2, 5) + 2, 1, 3),
   "08002-12": lambda: mean_value_time_from_amount(t + 9 * atan(t), 1, 4),
   "08002-13": lambda: mean_value_time_from_rate(root_ratio(3, 3) + 2, 1, Rational(7, 2)),
   "08002-14": lambda: mean_value_time_from_rate(6 * exp(s / 5) / 5 + 3, 1, 5),
   "08002-15": lambda: mean_value_time_from_amount(4*t + 3 * sqrt(t**2 + 4), 2, 6),
   "08002-16": lambda: mean_value_time_from_rate(3 * exp(s / 3) + 3, 1, 3),
   "08002-17": lambda: mean_value_time_from_amount(4*t + 7 * exp(t / 2), 1, 3),
   "08002-18": lambda: mean_value_time_from_rate(root_ratio(4, 4) + 4, 3, 6),
   "08002-19": lambda: mean_value_time_from_amount(3*t + 8 * exp(t / 5), 1, 5),
   "08002-20": lambda: mean_value_time_from_amount(t + 8 * sqrt(t**2 + 3), 1, 3),
   "08002-21": lambda: mean_value_time_from_amount(t + 9 * atan(2*t / 3), 3, 6),

   "08003-00": lambda: total_distance(-2*t**2 + 26*t - 72, 11),
   "08003-01": lambda: total_distance(-3*t**2 + 24*t - 36, Rational(15, 2)),
   "08003-02": lambda: total_distance(4*t**2 - 24*t + 20, Rational(11, 2)),
   "08003-03": lambda: total_distance(2*t**2 - 14*t + 12, Rational(15, 2)),
   "08003-04": lambda: total_distance(3*t**2 - 15*t + 12, Rational(9, 2)),
   "08003-05": lambda: total_distance(-4*t**2 + 28*t - 40, Rational(11, 2)),
   "08003-06": lambda: total_distance(-t**2 + 11*t - 24, Rational(17, 2)),
   "08003-07": lambda: total_distance(-4*t**2 + 44*t - 96, 9),
   "08003-08": lambda: total_distance(-3*t**2 + 33*t - 72, 9),
   "08003-09": lambda: total_distance(-4*t**2 + 40*t - 84, Rational(17, 2)),
   "08003-10": lambda: total_distance(-2*t**2 + 22*t - 48, Rational(17, 2)),
   "08003-11": lambda: total_distance(-t**2 + 12*t - 32, Rational(19, 2)),
   "08003-12": lambda: total_distance(-3*t**2 + 39*t - 120, Rational(17, 2)),
   "08003-13": lambda: total_distance(-t**2 + 15*t - 50, 11),
   "08003-14": lambda: total_distance(-2*t**2 + 24*t - 64, 9),
   "08003-15": lambda: total_distance(-4*t**2 + 24*t - 32, Rational(9, 2)),
   "08003-16": lambda: total_distance(2*t**2 - 14*t + 12, Rational(13, 2)),
   "08003-17": lambda: total_distance(-3*t**2 + 36*t - 96, Rational(17, 2)),
   "08003-18": lambda: total_distance(-4*t**2 + 48*t - 140, Rational(15, 2)),
   "08003-19": lambda: total_distance(-3*t**2 + 33*t - 72, Rational(17, 2)),
   "08003-20": lambda: total_distance(-4*t**2 + 60*t - 200, Rational(21, 2)),
   "08003-21": lambda: total_distance(t**2 - 9*t + 14, Rational(17, 2)),

   "08006-00": lambda: greatest_amount_choice(tank_rate(10, 5, 1), 180, 10, "08006-00"),
   "08006-01": lambda: greatest_amount_choice(tank_rate(15, 4, 11, 8), 180, 8, "08006-01"),
   "08006-02": lambda: greatest_amount_choice(tank_rate(18, 4, 3), 30, 8, "08006-02"),
   "08006-03": lambda: greatest_amount_choice(tank_rate(30, 6, 3), 50, 12, "08006-03"),
   "08006-04": lambda: greatest_amount_choice(tank_rate(10, 5, 5), 140, 10, "08006-04"),
   "08006-05": lambda: greatest_amount_choice(tank_rate(18, 8, 6), 50, 16, "08006-05"),
   "08006-06": lambda: greatest_amount_choice(tank_rate(16, 4, 9, 7), 150, 8, "08006-06"),
   "08006-07": lambda: greatest_amount_choice(tank_rate(36, 12, 6), 60, 24, "08006-07"),
   "08006-08": lambda: greatest_amount_choice(tank_rate(2, 12, 8, 7), 70, 24, "08006-08"),
   "08006-09": lambda: greatest_amount_choice(tank_rate(8, 5, 11, 9), 110, 10, "08006-09"),
   "08006-10": lambda: greatest_amount_choice(tank_rate(10, 8, 8, 6), 30, 16, "08006-10"),
   "08006-11": lambda: greatest_amount_choice(tank_rate(10, 10, 5), 170, 20, "08006-11"),
   "08006-12": lambda: greatest_amount_choice(tank_rate(6, 12, 9, 8), 60, 24, "08006-12"),
   "08006-13": lambda: greatest_amount_choice(tank_rate(5, 12, 1), 80, 24, "08006-13"),
   "08006-14": lambda: greatest_amount_choice(tank_rate(40, 4, 5), 130, 8, "08006-14"),
   "08006-15": lambda: greatest_amount_choice(tank_rate(8, 10, 4), 90, 20, "08006-15"),
   "08006-16": lambda: greatest_amount_choice(tank_rate(10, 12, 9, 7), 50, 24, "08006-16"),
   "08006-17": lambda: greatest_amount_choice(tank_rate(12, 4, 15, 9), 40, 8, "08006-17"),
   "08006-18": lambda: greatest_amount_choice(tank_rate(9, 6, 9, 3), 120, 12, "08006-18"),
   "08006-19": lambda: greatest_amount_choice(tank_rate(6, 4, 9, 8), 70, 8, "08006-19"),
   "08006-20": lambda: greatest_amount_choice(tank_rate(4, 12, 7, 4), 50, 24, "08006-20"),
   "08006-21": lambda: greatest_amount_choice(tank_rate(12, 6, 10, 8), 130, 12, "08006-21"),

   "08008-00": lambda: enclosed_area(-x**2 + 4*x, x + 2),
   "08008-01": lambda: enclosed_area(-2*x**2 + 15*x - 22, 2 - x),
   "08008-02": lambda: area_between(-3*x**2 + 10*x - 1, x + 3, 1, 2),
   "08008-03": lambda: enclosed_area(-3*x**2 + 5*x + 2, 2*x + 2),
   "08008-04": lambda: enclosed_area(-x**2 + x - 2, -x - 2),
   "08008-05": lambda: enclosed_area(-x**2 + 6*x - 9, x - 3),
   "08008-06": lambda: area_between(-2*x**2 + 5*x + 3, 1 - x, 0, 3),
   "08008-07": lambda: enclosed_area(-3*x**2 + 5*x + 6, -x - 3),
   "08008-08": lambda: enclosed_area(-2*x**2 - 4, 2*x - 4),
   "08008-09": lambda: enclosed_area(-2*x**2 + 6*x - 8, -2*x - 2),
   "08008-10": lambda: area_between(-x**2 + 4*x + 1, x - 1, 0, 3),
   "08008-11": lambda: enclosed_area(-x**2 + 4*x - 6, x - 4),
   "08008-12": lambda: enclosed_area(-3*x**2 + 2*x + 10, 4 - x),
   "08008-13": lambda: area_between(-3*x**2 - x + 11, -x - 4, -2, 2),
   "08008-14": lambda: enclosed_area(-2*x**2 + 15*x - 26, -x - 2),
   "08008-15": lambda: enclosed_area(-3*x**2 + 16*x - 19, -2*x - 4),
   "08008-16": lambda: area_between(1 - x**2, -x - 1, 0, 1),
   "08008-17": lambda: enclosed_area(-3*x**2 + 2*x + 5, -x - 1),
   "08008-18": lambda: area_between(-3*x**2 + 16*x - 20, x - 3, 2, 3),
   "08008-19": lambda: area_between(-2*x**2 + 4*x + 2, 2*x - 3, -1, 2),
   "08008-20": lambda: enclosed_area(-2*x**2 + 5*x + 4, x + 4),
   "08008-21": lambda: area_between(-x**2 + 6*x + 4, 2*x + 3, 0, 4),

   "08009-00": lambda: area_by_horizontal_slices(sqrt((x + 4) / 4), 2*x - 22),
   "08009-01": lambda: area_by_horizontal_slices(sqrt(x / 2), 2*x/3 - Rational(10, 3)),
   "08009-02": lambda: area_by_horizontal_slices(sqrt(x / 3), x - 24),
   "08009-03": lambda: area_by_horizontal_slices(sqrt(x + 4), 2*x - 7),
   "08009-04": lambda: area_by_horizontal_slices(sqrt(x + 4), 2*x/7 - 1),
   "08009-05": lambda: area_by_horizontal_slices(sqrt((x + 4) / 3), 2*x/3 - Rational(10, 3)),
   "08009-06": lambda: area_by_horizontal_slices(sqrt(x / 3), 2*x/5 - Rational(1, 5)),
   "08009-07": lambda: area_by_horizontal_slices(sqrt(x / 3), 2*x/5 - Rational(14, 5)),
   "08009-08": lambda: area_by_horizontal_slices(sqrt((x + 1) / 2), x/3 - Rational(8, 3)),
   "08009-09": lambda: area_by_horizontal_slices(sqrt((x + 1) / 4), 2*x/7 + Rational(1, 7)),
   "08009-10": lambda: area_by_horizontal_slices(sqrt((x + 1) / 4), x/3 - 3),
   "08009-11": lambda: area_by_horizontal_slices(sqrt(x + 1), x/2 - 1),
   "08009-12": lambda: area_by_horizontal_slices(sqrt((x + 2) / 2), 2*x/3 - Rational(23, 3)),
   "08009-13": lambda: area_by_horizontal_slices(sqrt(x + 4), x/2 + Rational(1, 2)),
   "08009-14": lambda: area_by_horizontal_slices(sqrt((x + 4) / 2), x - 11),
   "08009-15": lambda: area_by_horizontal_slices(sqrt(x / 4), x - 3),
   "08009-16": lambda: area_by_horizontal_slices(sqrt((x + 1) / 3), x/4 - Rational(7, 2)),
   "08009-17": lambda: area_by_horizontal_slices(sqrt(x), x/4 - Rational(5, 4)),
   "08009-18": lambda: area_by_horizontal_slices(sqrt(x / 4), x - 14),
   "08009-19": lambda: area_by_horizontal_slices(sqrt((x + 4) / 2), x/5 + Rational(1, 5)),
   "08009-20": lambda: area_by_horizontal_slices(sqrt(x / 3), x/6 - Rational(3, 2)),
   "08009-21": lambda: area_by_horizontal_slices(sqrt((x + 1) / 4), x/2 - Rational(11, 2)),

   "08010-00": lambda: area_between(2*x**2 - 7*x - 3, -x - 3, -1, 4),
   "08010-01": lambda: area_between(2*x**2 - 12*x + Rational(27, 2), 2*x - 3, 0, Rational(13, 2)),
   "08010-02": lambda: area_between(3*x**2 - 18*x + Rational(93, 4), 3, 0, Rational(11, 2)),
   "08010-03": lambda: area_between(2*x**2 - 6*x + Rational(7, 2), 2*x, -1, 4),
   "08010-04": lambda: area_between(3*x**2 - 4*x + 3, 2*x + 3, -1, Rational(5, 2)),
   "08010-05": lambda: area_between(x**2 - 6*x + 4, -1, -1, 6),
   "08010-06": lambda: area_between(2*x**2 - 21*x + 43, 1 - x, 1, 8),
   "08010-07": lambda: area_between(2*x**2 - 11*x + Rational(27, 2), x, 0, 5),
   "08010-08": lambda: area_between(2*x**2 - 7*x + 1, 1 - x, -1, Rational(7, 2)),
   "08010-09": lambda: area_between(2*x**2 - 16*x + 24, 0, 1, Rational(13, 2)),
   "08010-10": lambda: area_between(x**2 - 10*x + Rational(67, 4), 3 - 2*x, 1, Rational(13, 2)),
   "08010-11": lambda: area_between(2*x**2 - 12*x + 21, 2*x + 1, 0, 6),
   "08010-12": lambda: area_between(3*x**2 - 14*x + 12, x, 0, 5),
   "08010-13": lambda: area_between(x**2 - 6*x + Rational(35, 4), 2, 0, 5),
   "08010-14": lambda: area_between(2*x**2 - 17*x + 26, 2 - x, 0, Rational(13, 2)),
   "08010-15": lambda: area_between(2*x**2 - 14*x + 11, 1 - 2*x, 0, 6),
   "08010-16": lambda: area_between(x**2 - 5*x + Rational(33, 4), 2*x, 0, Rational(13, 2)),
   "08010-17": lambda: area_between(3*x**2 - 5*x - Rational(1, 4), 2 - 2*x, -2, 2),
   "08010-18": lambda: area_between(3*x**2 - 11*x - 1, x - 1, -1, Rational(9, 2)),
   "08010-19": lambda: area_between(x**2 - 6*x + 14, 2*x - 1, 1, Rational(11, 2)),
   "08010-20": lambda: area_between(3*x**2 - 10*x + Rational(3, 4), -x - 3, -1, 3),
   "08010-21": lambda: area_between(x**2 - 9*x + 9, -2*x - 1, 1, Rational(11, 2)),

   "08011-00": lambda: cross_section_volume_numeric(3 * exp(-x**2 / 3), -3*x/2, 0, 2, "rectangle", 3),
   "08011-01": lambda: cross_section_volume_numeric(2 * exp(-x**2 / 4), -x, 0, Rational(3, 2), "square"),
   "08011-02": lambda: cross_section_volume(-2*x**2 + 2*x + 2, -2, "semicircle"),
   "08011-03": lambda: cross_section_volume(-2*x**2 + 8*x - 2, 2*x + 2, "rectangle", 3),
   "08011-04": lambda: cross_section_volume(-2*x**2 + 3*x - 2, -x - 2, "rectangle", 2),
   "08011-05": lambda: cross_section_volume(-2*x**2, -2*x, "rectangle", 3),
   "08011-06": lambda: cross_section_volume(-x**2 + 4*x, 2*x, "rectangle", 3),
   "08011-07": lambda: cross_section_volume_numeric(3 * exp(-x**2 / 2), -3*x/2, 0, Rational(5, 2), "semicircle"),
   "08011-08": lambda: cross_section_volume(-x**2 + x + 1, 1 - 2*x, "equilateral"),
   "08011-09": lambda: cross_section_volume_numeric(4 * exp(-x**2 / 4), -x, 0, Rational(5, 2), "semicircle"),
   "08011-10": lambda: cross_section_volume(-2*x**2 + 10*x - 9, -1, "square"),
   "08011-11": lambda: cross_section_volume_numeric(3 * exp(-x**2 / 2), -x, 0, Rational(3, 2), "semicircle"),
   "08011-12": lambda: cross_section_volume(-x**2 + 3*x - 4, -x - 1, "semicircle"),
   "08011-13": lambda: cross_section_volume(-x**2 - x - 1, -x - 2, "isosceles right, hypotenuse in base"),
   "08011-14": lambda: cross_section_volume_numeric(2 * exp(-x**2 / 4), -3*x/2, 0, Rational(3, 2), "semicircle"),
   "08011-15": lambda: cross_section_volume_numeric(4 * exp(-x**2 / 2), -3*x/2, 0, 2, "rectangle", 3),
   "08011-16": lambda: cross_section_volume_numeric(2 * exp(-x**2 / 3), -3*x/2, 0, 2, "equilateral"),
   "08011-17": lambda: cross_section_volume(-x**2 - x, -2*x - 2, "rectangle", 2),
   "08011-18": lambda: cross_section_volume(-x**2 + x - 1, -2*x - 1, "isosceles right, hypotenuse in base"),
   "08011-19": lambda: cross_section_volume(-2*x**2 + 5*x, -x, "equilateral"),
   "08011-20": lambda: cross_section_volume(-2*x**2 + 8*x - 9, -2*x - 1, "square"),
   "08011-21": lambda: cross_section_volume(-2*x**2 + 2*x + 1, 1, "rectangle", 2),

   "08012-00": lambda: disk_volume(4*x**2 + 3, 3, None, 3),
   "08012-01": lambda: disk_volume(4*x - 3, -3, 1, 4),
   "08012-02": lambda: disk_volume(4 * sqrt(x), 0, None, 3),
   "08012-03": lambda: disk_volume(3 * sqrt(x) - 2, -2, 1, 6),
   "08012-04": lambda: disk_volume(3*x**2 + 3, 3, None, 5),
   "08012-05": lambda: disk_volume(sqrt(x) + 3, 3, 1, 3),
   "08012-06": lambda: disk_volume(x, 0, None, 4),
   "08012-07": lambda: disk_volume(2 * sqrt(x), 0, 1, 5),
   "08012-08": lambda: disk_volume(3 * sqrt(x) + 3, 3, None, 1),
   "08012-09": lambda: disk_volume(3*x**2 - 2, -2, 1, 6),
   "08012-10": lambda: disk_volume(sqrt(x), 0, None, 4),
   "08012-11": lambda: disk_volume(x, 0, None, 1),
   "08012-12": lambda: disk_volume(4 * sqrt(x) + 1, 1, 1, 6),
   "08012-13": lambda: disk_volume(3*x**2, 0, 1, 5),
   "08012-14": lambda: disk_volume(3*x, 0, None, 3),
   "08012-15": lambda: disk_volume(2*x**2, 0, None, 4),
   "08012-16": lambda: disk_volume(sqrt(x) - 1, -1, 1, 3),
   "08012-17": lambda: disk_volume(4*x - 2, -2, None, 5),
   "08012-18": lambda: disk_volume(sqrt(x) - 1, -1, None, 4),
   "08012-19": lambda: disk_volume(x, 0, None, 2),
   "08012-20": lambda: disk_volume(4*x**2, 0, None, 4),
   "08012-21": lambda: disk_volume(4*x**2 - 1, -1, 1, 2),

   "08013-00": lambda: washer_volume(-x**2 + 7*x - 6, 4, 8),
   "08013-01": lambda: washer_volume(-3*x**2 + 9*x - 4, 2, -3),
   "08013-02": lambda: washer_volume(-3*x**2 + 10*x + 4, x + 4, -3),
   "08013-03": lambda: washer_volume(-3*x**2 + 15*x - 14, 4, -1),
   "08013-04": lambda: washer_volume(-3*x**2 + 16*x - 16, x + 2, 0),
   "08013-05": lambda: washer_volume(-3*x**2 + 3*x + 4, 4, 0),
   "08013-06": lambda: washer_volume(-2*x**2 + 14*x - 18, 2, 7),
   "08013-07": lambda: washer_volume(-2*x**2 + 4*x + 1, 1, 0),
   "08013-08": lambda: washer_volume(-x**2 + 4*x + 1, x + 1, 0),
   "08013-09": lambda: washer_volume(-3*x**2 + 16*x - 10, x + 2, -3),
   "08013-10": lambda: washer_volume(-x**2 + 5*x - 1, 3, -3),
   "08013-11": lambda: washer_volume(-x**2 + 5*x - 3, 1, 0),
   "08013-12": lambda: washer_volume(-2*x**2 + x + 4, 4 - x, -1),
   "08013-13": lambda: washer_volume(-2*x**2 + 9*x - 3, x + 3, -3),
   "08013-14": lambda: washer_volume(-3*x**2 + 21*x - 29, 1, 0),
   "08013-15": lambda: washer_volume(-x**2 + 3*x + 3, x + 3, 7),
   "08013-16": lambda: washer_volume(-3*x**2 + 2*x + 4, 4 - x, 0),
   "08013-17": lambda: washer_volume(-x**2 + 5*x, x + 3, 0),
   "08013-18": lambda: washer_volume(-x**2 + 2*x + 1, 1, -1),
   "08013-19": lambda: washer_volume(-x**2 + 2*x + 2, x + 2, -3),
   "08013-20": lambda: washer_volume(-3*x**2 + 10*x - 3, x + 3, -1),
   "08013-21": lambda: washer_volume(-x**2 + x + 1, 1, 4),

   "08014-00": lambda: arc_length(x * ln(x), 2, 6),
   "08014-01": lambda: arc_length(3 * SQRT_TERM, 2, 5),
   "08014-02": lambda: arc_length_choice(3 * SQRT_TERM, 2, 6, "08014-02", displayed_forms(3 * ROOT_DERIVATIVE, 2, 6)),
   "08014-03": lambda: arc_length(SQRT_TERM, 1, 5),
   "08014-04": lambda: arc_length(5 * SQRT_TERM / 2, 3, 6),
   "08014-05": lambda: arc_length_choice(3 * SQRT_TERM / 2, 3, 7, "08014-05", displayed_forms(3 * (3*x + 2) / (4 * sqrt(x + 1)), 3, 7)),
   "08014-06": lambda: arc_length(SQRT_TERM / 2, 1, 3),
   "08014-07": lambda: arc_length(2 * SQRT_TERM, 3, 7),
   "08014-08": lambda: arc_length_choice(3 * SQRT_TERM, 1, 2, "08014-08", displayed_forms(3 * ROOT_DERIVATIVE, 1, 2)),
   "08014-09": lambda: arc_length_choice(3 * x * exp(x / 4), 2, 3, "08014-09", displayed_forms(3 * EXP_DERIVATIVE, 2, 3)),
   "08014-10": lambda: arc_length_choice(2 * x * ln(x), 2, 5, "08014-10", displayed_forms(2 * ln(x) + 2, 2, 5)),
   "08014-11": lambda: arc_length(3 * SQRT_TERM, 1, 4),
   "08014-12": lambda: arc_length_choice(3 * x * exp(x / 4) / 2, 2, 3, "08014-12", displayed_forms(3 * (x + 4) * exp(x / 4) / 8, 2, 3)),
   "08014-13": lambda: arc_length(x * ln(x) / 2, 2, 4),
   "08014-14": lambda: arc_length_choice(SQRT_TERM, 2, 4, "08014-14", displayed_forms(ROOT_DERIVATIVE, 2, 4)),
   "08014-15": lambda: arc_length_choice(2 * SQRT_TERM, 3, 5, "08014-15", displayed_forms((3*x + 2) / sqrt(x + 1), 3, 5)),
   "08014-16": lambda: arc_length(SQRT_TERM, 3, 7),
   "08014-17": lambda: arc_length_choice(5 * SQRT_TERM / 2, 2, 4, "08014-17", displayed_forms(5 * (3*x + 2) / (4 * sqrt(x + 1)), 2, 4)),
   "08014-18": lambda: arc_length(5 * x * ln(x) / 2, 2, 5),
   "08014-19": lambda: arc_length(SQRT_TERM / 2, 1, 5),
   "08014-20": lambda: arc_length_choice(SQRT_TERM, 3, 6, "08014-20", displayed_forms(ROOT_DERIVATIVE, 3, 6)),
   "08014-21": lambda: arc_length(3 * x * ln(x), 1, 2),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
