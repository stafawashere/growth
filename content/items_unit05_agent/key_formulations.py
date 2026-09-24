"""Each agent-drafted Unit 5 item's stem, written as the SymPy computation of the answer it asks for.

Read by tools/key_recheck.py. Every entry was written from the stem text alone, never from the
stored key, so a match is evidence that the key answers the stem. A relative extremum is found
from the derivative (the integrand at t = x, or the stated dy/dx) by its sign change across each
zero inside the stated open interval, and every qualifying point is returned so that a stem with
two answers shows up as ambiguous. For the horizontal tangent items, the singular point where both
partials vanish is excluded and d2y/dx2 is the implicit second derivative at each remaining point.
An edited stem needs its entry rewritten the same way before the recheck can pass again.
app/items/ingest.py loads only .json records, so this file never reaches the bank.
"""
import sympy
from sympy import Interval, cos, exp, pi, sin, sqrt

from tools.key_recheck import horizontal_tangent_points, implicit_second_derivative, t, x, y

ITEM_PREFIX = "ITM-AGT-"


def relative_extrema(rate, lower, upper, kind):
   """Points in (lower, upper) where rate, the derivative in x, changes sign: from negative to
   positive for a minimum, positive to negative for a maximum."""
   domain = Interval.open(lower, upper)
   zeros = sympy.solveset(rate, x, domain)

   if not isinstance(zeros, sympy.FiniteSet):
      raise ValueError(f"zeros of {rate} on {domain} are not a finite set: {zeros}")

   ordered_zeros = sorted(zeros, key=lambda zero: float(zero))
   boundaries = [sympy.sympify(lower)] + ordered_zeros + [sympy.sympify(upper)]
   signs = [sympy.sign(rate.subs(x, (left + right) / 2).evalf()) for left, right in zip(boundaries, boundaries[1:])]
   extrema = []

   for index, zero in enumerate(ordered_zeros):
      sign_before = signs[index]
      sign_after = signs[index + 1]
      is_minimum = sign_before < 0 and sign_after > 0
      is_maximum = sign_before > 0 and sign_after < 0
      matches = is_minimum if kind == "min" else is_maximum

      if matches:
         extrema.append(zero)

   return extrema


def accumulation_extrema(integrand, lower, upper, kind):
   return relative_extrema(integrand.subs(t, x), lower, upper, kind)


def implicit_concavity_at(curve, point):
   return sympy.simplify(implicit_second_derivative(curve).subs({x: point[0], y: point[1]}))


def horizontal_tangent_height(curve, concavity):
   heights = []

   for point in horizontal_tangent_points(curve):
      second = implicit_concavity_at(curve, point)
      matches = second > 0 if concavity == "up" else second < 0

      if matches:
         heights.append(point[1])

   return heights


BY_SUFFIX = {
   "05007-00": lambda: accumulation_extrema((t + 1)*(t - 2)*(t - 7), 0, 9, "min"),
   "05007-01": lambda: accumulation_extrema(t**3 - 6*t**2 + 3*t + 10, 0, 6, "min"),
   "05007-02": lambda: accumulation_extrema(-(t - 1)*(t - 6)*(t - 9), 0, 8, "max"),
   "05007-03": lambda: accumulation_extrema(t**3 - 5*t**2 - 8*t + 12, -4, 5, "min"),
   "05007-04": lambda: accumulation_extrema(t*(t - 3)*(t - 8), 1, 10, "min"),
   "05007-05": lambda: accumulation_extrema(-t**3 + 7*t**2 - 36, 0, 8, "max"),
   "05007-06": lambda: accumulation_extrema(-t*(t + 3)*(t - 5), -1, 7, "max"),
   "05007-07": lambda: accumulation_extrema(t**3 - t**2 - 16*t + 16, -3, 6, "min"),
   "05007-08": lambda: accumulation_extrema(t**3 - 9*t, -1, 4, "min"),
   "05007-09": lambda: accumulation_extrema(-(t + 2)*(t - 1)*(t - 4), 0, 5, "max"),

   "05007-10": lambda: relative_extrema(-(x - 1)*(x - 4)*(x - 9), 2, 10, "max"),
   "05007-11": lambda: relative_extrema(x**3 + 2*x**2 - 15*x, -1, 4, "min"),
   "05007-12": lambda: relative_extrema(x**3 - 17*x**2 + 80*x - 100, 0, 9, "min"),

   "05007-13": lambda: accumulation_extrema(2*cos(t) - 1, 0, 2*pi, "min"),
   "05007-14": lambda: accumulation_extrema(2*sin(t) - 1, 0, 2*pi, "max"),
   "05007-15": lambda: accumulation_extrema(sqrt(2)*cos(t) - 1, 0, 2*pi, "min"),
   "05007-16": lambda: accumulation_extrema(cos(t) - sin(t), 0, 2*pi, "min"),
   "05007-17": lambda: accumulation_extrema(sin(t) + cos(t), 0, 2*pi, "max"),

   "05012-00": lambda: implicit_concavity_at(x**2 + x*y + y**2 - 7, (1, 2)),
   "05012-01": lambda: implicit_concavity_at(x**2 - x*y + y**2 - 7, (2, 3)),
   "05012-02": lambda: implicit_concavity_at(x*y + y**2 - 6, (1, 2)),
   "05012-03": lambda: implicit_concavity_at(x**2*y + y**2 - 6, (1, 2)),
   "05012-04": lambda: implicit_concavity_at(x*y**2 + x**2 - 5, (1, 2)),
   "05012-05": lambda: implicit_concavity_at(x**3 + x*y + y**2 - 7, (1, 2)),
   "05012-06": lambda: implicit_concavity_at(2*x*y - y**2 - 3, (2, 1)),
   "05012-07": lambda: implicit_concavity_at(x**2 + 3*x*y + y**2 - 5, (1, 1)),
   "05012-08": lambda: implicit_concavity_at(y**2 + x*y - 2*x**2 - 4, (1, 2)),
   "05012-09": lambda: implicit_concavity_at(x*y**2 - x**3 - 10, (2, 3)),
   "05012-10": lambda: implicit_concavity_at(x*exp(y) + y - 2, (2, 0)),

   "05012-11": lambda: horizontal_tangent_height(y**2 - x**2*(x + 12), "up"),
   "05012-12": lambda: horizontal_tangent_height(y**2 - x**2*(12 - x), "down"),
   "05012-13": lambda: horizontal_tangent_height(y**2 - 3*x**2*(x + 3), "down"),
   "05012-14": lambda: horizontal_tangent_height(y**2 - x**2*(x + 27), "up"),
   "05012-15": lambda: horizontal_tangent_height(y**2 - 4*x**2*(3 - x), "up"),
   "05012-16": lambda: horizontal_tangent_height(y**2 - 2*x**2*(x + 6), "down"),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
