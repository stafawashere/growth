"""Blind re-solve of generated unit 5 items, batch D, each answer computed from its stem alone.

Written from var/p4/resolve/items_gen_unit05/stems_D.json and nothing else about these items by a blind
solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. The file is self-contained: each
statement item's choices and each graph's plotted points are copied into it from the stems. A statement
item returns the text of the choice the mathematics selects; when no choice or more than one choice
states the computed result, the list of matches comes back so the recheck reports the item.
"""
import re

import sympy
from sympy import Rational, oo

from tools.key_recheck import horizontal_tangent_points, x, y

POINT_IN_CHOICE = r"\\\( \((-?\d+), (-?\d+)\) \\\)"
PLOT_TOLERANCE = 0.01
SLOPE_TOLERANCE = 0.05


def expression(text):
   return sympy.sympify(text, locals={"x": x, "y": y})


def derivative_of(text):
   return sympy.diff(expression(text), x)


def choice_stating(suffix, wanted):
   matches = [choice for choice in CHOICES[suffix] if choice == wanted]

   return matches[0] if len(matches) == 1 else matches


def choices_where(suffix, holds):
   matches = [choice for choice in CHOICES[suffix] if holds(choice)]

   return matches[0] if len(matches) == 1 else matches


def real_roots(expression_in_x):
   return sorted({root for root in sympy.solve(expression_in_x, x) if root.is_real})


def sign_word(value):
   return "positive" if value > 0 else "negative"


def critical_point_choice(suffix, sign_part, low, high, name):
   """sign_part is the derivative with its always-positive factor (y^2 + 1, or the given positive
   function) dropped, so it has the derivative's sign everywhere."""
   inside = [root for root in real_roots(sign_part) if low < root < high]
   has_one_critical_point = len(inside) == 1

   if not has_one_critical_point:
      return []

   point = inside[0]
   left_edge = max([low] + [root for root in real_roots(sign_part) if root < point])
   right_edge = min([high] + [root for root in real_roots(sign_part) if root > point])
   before = sign_part.subs(x, (left_edge + point) / 2)
   after = sign_part.subs(x, (point + right_edge) / 2)
   changes_sign = before * after < 0

   if not changes_sign:
      return []

   kind = "maximum" if before > 0 else "minimum"
   wanted = (
      f"At x = {point} only; {name} has a relative {kind} there because {name}' changes from "
      f"{sign_word(before)} to {sign_word(after)} at x = {point}."
   )

   return choice_stating(suffix, wanted)


def interval_text(left, right):
   return f"\\( ({sympy.latex(left)}, {sympy.latex(right)}) \\)"


def listed(parts):
   if len(parts) == 1:
      return parts[0]

   return ", ".join(parts[:-1]) + " and " + parts[-1]


def monotonic_intervals(rate, direction):
   numerator, denominator = sympy.fraction(sympy.together(rate))
   breaks = sorted(set(real_roots(numerator)) | set(real_roots(denominator)))
   edges = [-oo] + breaks + [oo]
   wanted_sign = 1 if direction == "increasing" else -1
   intervals = []

   for left, right in zip(edges, edges[1:]):
      is_left_unbounded = left == -oo
      is_right_unbounded = right == oo

      if is_left_unbounded:
         probe = right - 1
      elif is_right_unbounded:
         probe = left + 1
      else:
         probe = (left + right) / 2

      has_wanted_sign = sympy.sign(rate.subs(x, probe)) == wanted_sign

      if has_wanted_sign:
         intervals.append((left, right))

   return intervals


def monotonic_choice(suffix, rate, direction):
   intervals = monotonic_intervals(rate, direction)
   comparison = ">" if direction == "increasing" else "<"
   parts = [interval_text(left, right) for left, right in intervals]

   if len(parts) == 1:
      wanted = f"f is {direction} on the interval {parts[0]}, because \\( f'(x) {comparison} 0 \\) on that interval."
   else:
      wanted = (
         f"f is {direction} on the intervals {listed(parts)}, because \\( f'(x) {comparison} 0 \\) "
         f"on each of those intervals."
      )

   return choice_stating(suffix, wanted)


def fitted_cubic(points):
   """The polynomial of degree at most 3 through four plotted points spread across the curve,
   refused when the other plotted points stray from it."""
   chosen = [points[0], points[len(points) // 3], points[2 * len(points) // 3], points[-1]]
   exact_points = [(sympy.nsimplify(px), sympy.nsimplify(py)) for px, py in chosen]
   polynomial = sympy.expand(sympy.interpolate(exact_points, x))
   largest_residual = max(abs(float(polynomial.subs(x, px)) - py) for px, py in points)

   if largest_residual > PLOT_TOLERANCE:
      raise ValueError(f"plotted curve is not a cubic, residual {largest_residual}")

   return polynomial


def slope_mismatch(antiderivative, function, sample_xs):
   return max(abs(float((sympy.diff(antiderivative, x) - function).subs(x, at))) for at in sample_xs)


def antiderivative_chain_choice(suffix, names):
   """names: the function whose slope is no other curve, the middle one, and the one whose slope is
   the middle one, so (g, G, K) or (f'', f', f). Finds which curve's slope is which other curve from
   the plotted points, then names each curve by the label drawn closest above or below it."""
   plotted = PLOTTED[suffix]
   curves = [fitted_cubic(points) for points in plotted["curves"]]
   sample_xs = [px for px, _ in plotted["curves"][0]]
   fits = []

   for g_index, big_g_index, k_index in [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]:
      mismatch = max(
         slope_mismatch(curves[big_g_index], curves[g_index], sample_xs),
         slope_mismatch(curves[k_index], curves[big_g_index], sample_xs),
      )
      fits.append((mismatch, {g_index: names[0], big_g_index: names[1], k_index: names[2]}))

   fits.sort(key=lambda fit: fit[0])
   best_mismatch, roles = fits[0]
   is_clear_fit = best_mismatch < SLOPE_TOLERANCE and fits[1][0] > 10 * SLOPE_TOLERANCE

   if not is_clear_fit:
      return []

   role_by_label = {}

   for label, (anchor_x, anchor_y) in plotted["labels"].items():
      gaps = [abs(float(curve.subs(x, anchor_x)) - anchor_y) for curve in curves]
      nearest = gaps.index(min(gaps))
      role_by_label[label] = roles[nearest]

   labels_name_distinct_curves = len(set(role_by_label.values())) == 3

   if not labels_name_distinct_curves:
      return []

   wanted = (
      f"Curve A is the graph of \\( {role_by_label['A']} \\), curve B is the graph of "
      f"\\( {role_by_label['B']} \\), and curve C is the graph of \\( {role_by_label['C']} \\)."
   )

   return choice_stating(suffix, wanted)


def extreme_value_choice(suffix, name, hypothesis, asked):
   """hypothesis: "differentiable" (twice differentiable on the whole closed interval), "continuous"
   (stated continuous on the closed interval) or "jump" (a jump discontinuity inside it). asked: the
   kind of interval the stem asks about. Only continuity on a closed interval guarantees the extreme,
   by the Extreme Value Theorem; without it the extreme need not be attained."""
   if asked == "open":
      opening = "No, because \\( ("
      reason = "is not a closed interval, so the Extreme Value Theorem does not apply there."

      return choices_where(suffix, lambda choice: choice.startswith(opening) and choice.endswith(reason))

   openings = {
      "differentiable": f"Yes, because {name} is differentiable, so continuous, on the closed interval",
      "continuous": f"Yes, because {name} is continuous on the closed interval",
      "jump": f"No, because {name} is not continuous on the closed interval",
   }

   return choices_where(suffix, lambda choice: choice.startswith(openings[hypothesis]))


def open_box_largest_volume(side, height_cap):
   volume = x * (side - 2 * x) ** 2
   largest_cut = Rational(side, 2) if height_cap is None else min(Rational(side, 2), height_cap)
   stationary = [point for point in real_roots(sympy.diff(volume, x)) if 0 < point < largest_cut]
   cap_is_binding = height_cap is not None and height_cap < Rational(side, 2)
   candidates = stationary + ([height_cap] if cap_is_binding else [])

   return max(volume.subs(x, candidate) for candidate in candidates)


def horizontal_tangent_choice(suffix, curve):
   points = {(sympy.Integer(px), sympy.Integer(py)) for px, py in horizontal_tangent_points(sympy.expand(curve))}

   def lists_exactly_these(choice):
      listed_points = {(sympy.Integer(px), sympy.Integer(py)) for px, py in re.findall(POINT_IN_CHOICE, choice)}

      return choice.startswith("The tangent line is horizontal only at") and listed_points == points

   return choices_where(suffix, lists_exactly_these)


def test_clause(rate, point, name):
   slope = rate.subs(x, point)
   concavity = sympy.diff(rate, x).subs(x, point)
   is_critical = slope == 0

   if not is_critical:
      return f"{name} has no relative extremum because \\( {name}'({point}) = {slope} \\ne 0 \\)"

   if concavity == 0:
      return None

   kind = "minimum" if concavity > 0 else "maximum"
   comparison = ">" if concavity > 0 else "<"

   return (
      f"{name} has a relative {kind} because \\( {name}'({point}) = 0 \\) and "
      f"\\( {name}''({point}) = {concavity} {comparison} 0 \\)"
   )


def second_derivative_test_choice(suffix, rate, first, second, name):
   first_clause = test_clause(rate, first, name)
   second_clause = test_clause(rate, second, name)
   test_is_conclusive = first_clause is not None and second_clause is not None

   if not test_is_conclusive:
      return []

   wanted = f"At \\( x = {first} \\), {first_clause}; at \\( x = {second} \\), {second_clause}."

   return choice_stating(suffix, wanted)



CHOICES = {
   "05007-00": [
      "At x = 2 and x = -4; H has a relative maximum at x = 2 and a relative minimum at x = -4 because H' changes sign at each.",
      "At x = 2 only; H has a relative maximum there because H' changes from positive to negative at x = 2.",
      "At x = 2 only; H has a relative minimum there because H' changes from positive to negative at x = 2.",
      "At x = 2 only; H has neither there because H' stays close to 0 on both sides of x = 2.",
   ],
   "05007-01": [
      "At x = 1 and x = 8; g has a relative maximum at x = 1 and a relative minimum at x = 8 because g' changes sign at each.",
      "At x = 1 only; g has a relative maximum there because g' changes from positive to negative at x = 1.",
      "At x = 1 only; g has a relative minimum there because g' changes from positive to negative at x = 1.",
      "At x = 1 only; g has neither there because g' stays close to 0 on both sides of x = 1.",
   ],
   "05007-02": [
      "At x = 4 and x = 9; H has a relative maximum at x = 4 and a relative minimum at x = 9 because H' changes sign at each.",
      "At x = 4 only; H has a relative maximum there because H' changes from positive to negative at x = 4.",
      "At x = 4 only; H has a relative minimum there because H' changes from positive to negative at x = 4.",
      "At x = 4 only; H has neither there because H' stays close to 0 on both sides of x = 4.",
   ],
   "05007-03": [
      "At x = 3 and x = 10; G has a relative minimum at x = 3 and a relative maximum at x = 10 because G' changes sign at each.",
      "At x = 3 only; G has a relative maximum there because G' changes from negative to positive at x = 3.",
      "At x = 3 only; G has a relative minimum there because G' changes from negative to positive at x = 3.",
      "At x = 3 only; G has neither there because G' stays close to 0 on both sides of x = 3.",
   ],
   "05008-00": [
      "f is decreasing on the interval \\( (-4, 2) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-4, 0) \\) and \\( (2, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -4) \\) and \\( (0, 2) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -4) \\) and \\( (0, 2) \\), because it is negative there.",
   ],
   "05008-01": [
      "f is increasing on the interval \\( (0, 3) \\), because \\( f'(x) > 0 \\) on that interval.",
      "f is increasing on the interval \\( (\\frac{3}{2}, \\infty) \\), because f' is increasing there.",
      "f is increasing on the intervals \\( (-\\infty, 0) \\) and \\( (3, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, 0) \\) and \\( (3, \\infty) \\), because it is positive there.",
   ],
   "05008-02": [
      "f is increasing on the interval \\( (-5, -4) \\), because \\( f'(x) > 0 \\) on that interval.",
      "f is increasing on the intervals \\( (-\\infty, -5) \\) and \\( (-4, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, -5) \\), \\( (-4, 4) \\) and \\( (4, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, -5) \\), \\( (-4, 4) \\) and \\( (4, \\infty) \\), because it is positive there.",
   ],
   "05008-03": [
      "f is decreasing on the intervals \\( (-2, -1) \\) and \\( (1, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-2, -1) \\) and \\( (1, \\infty) \\), because it is negative there.",
      "f is decreasing on the intervals \\( (-\\infty, -1) \\) and \\( (1, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -2) \\) and \\( (-1, 1) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
   ],
   "05008-04": [
      "f is increasing on the intervals \\( (-5, -1) \\) and \\( (4, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-5, -1) \\) and \\( (4, \\infty) \\), because it is positive there.",
      "f is increasing on the intervals \\( (-\\infty, -5) \\) and \\( (-1, 4) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, -5) \\) and \\( (-1, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
   ],
   "05008-05": [
      "f is decreasing on the interval \\( (-2, \\infty) \\), because f' is decreasing there.",
      "f is decreasing on the interval \\( (-4, 0) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-\\infty, -4) \\) and \\( (0, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -4) \\) and \\( (0, \\infty) \\), because it is negative there.",
   ],
   "05008-06": [
      "f is increasing on the interval \\( (4, 5) \\), because \\( f'(x) > 0 \\) on that interval.",
      "f is increasing on the intervals \\( (-\\infty, 3) \\), \\( (3, 4) \\) and \\( (5, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, 3) \\), \\( (3, 4) \\) and \\( (5, \\infty) \\), because it is positive there.",
      "f is increasing on the intervals \\( (-\\infty, 4) \\) and \\( (5, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
   ],
   "05008-07": [
      "f is decreasing on the interval \\( (2, 3) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-3, 2) \\) and \\( (3, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (2, 3) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (2, 3) \\), because it is negative there.",
   ],
   "05008-08": [
      "f is decreasing on the interval \\( (-2, 1) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the interval \\( (-2, 1) \\), because it is negative there.",
      "f is decreasing on the interval \\( (-\\infty, - \\frac{1}{2}) \\), because f' is decreasing there.",
      "f is decreasing on the intervals \\( (-\\infty, -2) \\) and \\( (1, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
   ],
   "05008-09": [
      "f is decreasing on the interval \\( (-3, -2) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-3, -2) \\) and \\( (0, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (-2, 0) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (-2, 0) \\), because it is negative there.",
   ],
   "05008-10": [
      "f is increasing on the interval \\( (-4, 4) \\), because \\( f'(x) > 0 \\) on that interval.",
      "f is increasing on the intervals \\( (-4, 2) \\) and \\( (2, 4) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-4, 2) \\) and \\( (2, 4) \\), because it is positive there.",
      "f is increasing on the intervals \\( (-\\infty, -4) \\) and \\( (4, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
   ],
   "05008-11": [
      "f is decreasing on the interval \\( (-1, 2) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the interval \\( (\\frac{1}{2}, \\infty) \\), because f' is decreasing there.",
      "f is decreasing on the intervals \\( (-\\infty, -1) \\) and \\( (2, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -1) \\) and \\( (2, \\infty) \\), because it is negative there.",
   ],
   "05008-12": [
      "f is increasing on the intervals \\( (-\\infty, 0) \\) and \\( (1, 2) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, 1) \\) and \\( (2, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (0, 1) \\) and \\( (2, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (0, 1) \\) and \\( (2, \\infty) \\), because it is positive there.",
   ],
   "05008-13": [
      "f is decreasing on the interval \\( (2, 3) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-\\infty, -5) \\), \\( (-5, 2) \\) and \\( (3, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -5) \\), \\( (-5, 2) \\) and \\( (3, \\infty) \\), because it is negative there.",
      "f is decreasing on the intervals \\( (-\\infty, 2) \\) and \\( (3, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
   ],
   "05008-14": [
      "f is decreasing on the interval \\( (-2, 5) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the interval \\( (\\frac{3}{2}, \\infty) \\), because f' is decreasing there.",
      "f is decreasing on the intervals \\( (-\\infty, -2) \\) and \\( (5, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -2) \\) and \\( (5, \\infty) \\), because it is negative there.",
   ],
   "05008-15": [
      "f is decreasing on the interval \\( (-5, 5) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-5, 1) \\) and \\( (1, 5) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-5, 1) \\) and \\( (1, 5) \\), because it is negative there.",
      "f is decreasing on the intervals \\( (-\\infty, -5) \\) and \\( (5, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
   ],
   "05008-16": [
      "f is increasing on the interval \\( (1, 2) \\), because \\( f'(x) > 0 \\) on that interval.",
      "f is increasing on the intervals \\( (-\\infty, 0) \\), \\( (0, 1) \\) and \\( (2, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, 0) \\), \\( (0, 1) \\) and \\( (2, \\infty) \\), because it is positive there.",
      "f is increasing on the intervals \\( (-\\infty, 1) \\) and \\( (2, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
   ],
   "05008-17": [
      "f is decreasing on the interval \\( (-3, 4) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-3, 0) \\) and \\( (0, 4) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-3, 0) \\) and \\( (0, 4) \\), because it is negative there.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (4, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
   ],
   "05008-18": [
      "f is increasing on the interval \\( (-3, -1) \\), because \\( f'(x) > 0 \\) on that interval.",
      "f is increasing on the interval \\( (-3, -1) \\), because it is positive there.",
      "f is increasing on the interval \\( (-\\infty, -2) \\), because f' is increasing there.",
      "f is increasing on the intervals \\( (-\\infty, -3) \\) and \\( (-1, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
   ],
   "05008-19": [
      "f is decreasing on the interval \\( (-4, 0) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-4, -1) \\) and \\( (-1, 0) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-4, -1) \\) and \\( (-1, 0) \\), because it is negative there.",
      "f is decreasing on the intervals \\( (-\\infty, -4) \\) and \\( (0, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
   ],
   "05008-20": [
      "f is increasing on the intervals \\( (-1, 0) \\) and \\( (4, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-1, 0) \\) and \\( (4, \\infty) \\), because it is positive there.",
      "f is increasing on the intervals \\( (-\\infty, -1) \\) and \\( (0, 4) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
      "f is increasing on the intervals \\( (-\\infty, -1) \\) and \\( (0, \\infty) \\), because \\( f'(x) > 0 \\) on each of those intervals.",
   ],
   "05008-21": [
      "f is decreasing on the interval \\( (- \\frac{5}{2}, \\infty) \\), because f' is decreasing there.",
      "f is decreasing on the interval \\( (-3, -2) \\), because \\( f'(x) < 0 \\) on that interval.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (-2, \\infty) \\), because \\( f'(x) < 0 \\) on each of those intervals.",
      "f is decreasing on the intervals \\( (-\\infty, -3) \\) and \\( (-2, \\infty) \\), because it is negative there.",
   ],
   "05009-00": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
   ],
   "05009-01": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
   ],
   "05009-02": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
   ],
   "05009-03": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
   ],
   "05009-04": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-05": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
   ],
   "05009-06": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
   ],
   "05009-07": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-08": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-09": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
   ],
   "05009-10": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-11": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-12": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-13": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
   ],
   "05009-14": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-15": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
   ],
   "05009-16": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
   ],
   "05009-17": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
   ],
   "05009-18": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( G \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
   ],
   "05009-19": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f' \\).",
   ],
   "05009-20": [
      "Curve A is the graph of \\( f \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f \\), and curve C is the graph of \\( f'' \\).",
      "Curve A is the graph of \\( f' \\), curve B is the graph of \\( f'' \\), and curve C is the graph of \\( f \\).",
      "Curve A is the graph of \\( f'' \\), curve B is the graph of \\( f' \\), and curve C is the graph of \\( f \\).",
   ],
   "05009-21": [
      "Curve A is the graph of \\( G \\), curve B is the graph of \\( g \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( K \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( g \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( G \\), and curve C is the graph of \\( K \\).",
      "Curve A is the graph of \\( g \\), curve B is the graph of \\( K \\), and curve C is the graph of \\( G \\).",
   ],
   "05010-00": [
      "No, because f is not continuous on the closed interval \\( [-2, 5] \\), so the Extreme Value Theorem does not apply.",
      "Yes, because f has a relative minimum at \\( x = 2 \\), so its absolute minimum value is \\( f(2) \\).",
      "Yes, because f is continuous on \\( [-2, 5] \\) except at \\( x = 1 \\), so the Extreme Value Theorem applies.",
      "Yes, because f is defined at every x in the closed interval \\( [-2, 5] \\), so the Extreme Value Theorem applies.",
   ],
   "05010-01": [
      "Yes, because g has a relative maximum at \\( x = -3 \\), so its absolute maximum value is \\( g(-3) \\).",
      "Yes, because g is defined at every x in the closed interval \\( [-4, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is differentiable, so continuous, on the closed interval \\( [-4, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = -3 \\), where \\( g'(-3) = 0 \\).",
   ],
   "05010-02": [
      "Yes, because g has a relative maximum at \\( x = -2 \\), so its absolute maximum value is \\( g(-2) \\).",
      "Yes, because g is defined at every x in the closed interval \\( [-4, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is differentiable, so continuous, on the closed interval \\( [-4, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = -2 \\), where \\( g'(-2) = 0 \\).",
   ],
   "05010-03": [
      "No, because g is not continuous on the closed interval \\( [-2, 3] \\), so the Extreme Value Theorem does not apply.",
      "Yes, because g has a relative minimum at \\( x = 0 \\), so its absolute minimum value is \\( g(0) \\).",
      "Yes, because g is continuous on \\( [-2, 3] \\) except at \\( x = 2 \\), so the Extreme Value Theorem applies.",
      "Yes, because g is defined at every x in the closed interval \\( [-2, 3] \\), so the Extreme Value Theorem applies.",
   ],
   "05010-04": [
      "Yes, because g has a relative minimum at \\( x = 1 \\), so its absolute minimum value is \\( g(1) \\).",
      "Yes, because g is defined at every x in the closed interval \\( [-3, 3] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is differentiable, so continuous, on the closed interval \\( [-3, 3] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = 1 \\), where \\( g'(1) = 0 \\).",
   ],
   "05010-05": [
      "Yes, because f has a relative minimum at \\( x = 0 \\), so its absolute minimum value is \\( f(0) \\).",
      "Yes, because f is defined at every x in the closed interval \\( [-1, 6] \\), so the Extreme Value Theorem applies.",
      "Yes, because f is differentiable, so continuous, on the closed interval \\( [-1, 6] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = 0 \\), where \\( f'(0) = 0 \\).",
   ],
   "05010-06": [
      "No, because \\( (2, 9) \\) is not a closed interval, so the Extreme Value Theorem does not apply there.",
      "No, because the Extreme Value Theorem places the absolute minimum of g on \\( [2, 9] \\) at an endpoint.",
      "Yes, because g has a relative minimum at \\( x = 6 \\), so its absolute minimum value is \\( g(6) \\).",
      "Yes, because g is continuous on the interval \\( (2, 9) \\), so the Extreme Value Theorem applies.",
   ],
   "05010-07": [
      "Yes, because h has a relative maximum at \\( x = 3 \\), so its absolute maximum value is \\( h(3) \\).",
      "Yes, because h is continuous on the closed interval \\( [-1, 6] \\), so the Extreme Value Theorem applies.",
      "Yes, because h is defined at every x in the closed interval \\( [-1, 6] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = 3 \\), where \\( h'(3) = 0 \\).",
   ],
   "05010-08": [
      "Yes, because g has a relative minimum at \\( x = 5 \\), so its absolute minimum value is \\( g(5) \\).",
      "Yes, because g is continuous on the closed interval \\( [2, 8] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is defined at every x in the closed interval \\( [2, 8] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = 5 \\), where \\( g'(5) = 0 \\).",
   ],
   "05010-09": [
      "Yes, because h has a relative maximum at \\( x = 4 \\), so its absolute maximum value is \\( h(4) \\).",
      "Yes, because h is defined at every x in the closed interval \\( [-1, 5] \\), so the Extreme Value Theorem applies.",
      "Yes, because h is differentiable, so continuous, on the closed interval \\( [-1, 5] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = 4 \\), where \\( h'(4) = 0 \\).",
   ],
   "05010-10": [
      "Yes, because g has a relative minimum at \\( x = -2 \\), so its absolute minimum value is \\( g(-2) \\).",
      "Yes, because g is defined at every x in the closed interval \\( [-3, 4] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is differentiable, so continuous, on the closed interval \\( [-3, 4] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = -2 \\), where \\( g'(-2) = 0 \\).",
   ],
   "05010-11": [
      "No, because h is not continuous on the closed interval \\( [-2, 5] \\), so the Extreme Value Theorem does not apply.",
      "Yes, because h has a relative maximum at \\( x = 0 \\), so its absolute maximum value is \\( h(0) \\).",
      "Yes, because h is continuous on \\( [-2, 5] \\) except at \\( x = 3 \\), so the Extreme Value Theorem applies.",
      "Yes, because h is defined at every x in the closed interval \\( [-2, 5] \\), so the Extreme Value Theorem applies.",
   ],
   "05010-12": [
      "Yes, because h has a relative maximum at \\( x = 3 \\), so its absolute maximum value is \\( h(3) \\).",
      "Yes, because h is defined at every x in the closed interval \\( [-2, 5] \\), so the Extreme Value Theorem applies.",
      "Yes, because h is differentiable, so continuous, on the closed interval \\( [-2, 5] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = 3 \\), where \\( h'(3) = 0 \\).",
   ],
   "05010-13": [
      "Yes, because g has a relative minimum at \\( x = -1 \\), so its absolute minimum value is \\( g(-1) \\).",
      "Yes, because g is continuous on the closed interval \\( [-2, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is defined at every x in the closed interval \\( [-2, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = -1 \\), where \\( g'(-1) = 0 \\).",
   ],
   "05010-14": [
      "Yes, because h has a relative minimum at \\( x = -2 \\), so its absolute minimum value is \\( h(-2) \\).",
      "Yes, because h is defined at every x in the closed interval \\( [-5, 0] \\), so the Extreme Value Theorem applies.",
      "Yes, because h is differentiable, so continuous, on the closed interval \\( [-5, 0] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = -2 \\), where \\( h'(-2) = 0 \\).",
   ],
   "05010-15": [
      "No, because \\( (-4, 2) \\) is not a closed interval, so the Extreme Value Theorem does not apply there.",
      "No, because the Extreme Value Theorem places the absolute maximum of h on \\( [-4, 2] \\) at an endpoint.",
      "Yes, because h has a relative maximum at \\( x = 0 \\), so its absolute maximum value is \\( h(0) \\).",
      "Yes, because h is continuous on the interval \\( (-4, 2) \\), so the Extreme Value Theorem applies.",
   ],
   "05010-16": [
      "No, because h is not continuous on the closed interval \\( [-3, 4] \\), so the Extreme Value Theorem does not apply.",
      "Yes, because h has a relative minimum at \\( x = -2 \\), so its absolute minimum value is \\( h(-2) \\).",
      "Yes, because h is continuous on \\( [-3, 4] \\) except at \\( x = -1 \\), so the Extreme Value Theorem applies.",
      "Yes, because h is defined at every x in the closed interval \\( [-3, 4] \\), so the Extreme Value Theorem applies.",
   ],
   "05010-17": [
      "Yes, because g has a relative maximum at \\( x = 0 \\), so its absolute maximum value is \\( g(0) \\).",
      "Yes, because g is defined at every x in the closed interval \\( [-5, 1] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is differentiable, so continuous, on the closed interval \\( [-5, 1] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = 0 \\), where \\( g'(0) = 0 \\).",
   ],
   "05010-18": [
      "No, because h is not continuous on the closed interval \\( [-1, 4] \\), so the Extreme Value Theorem does not apply.",
      "Yes, because h has a relative minimum at \\( x = 1 \\), so its absolute minimum value is \\( h(1) \\).",
      "Yes, because h is continuous on \\( [-1, 4] \\) except at \\( x = 0 \\), so the Extreme Value Theorem applies.",
      "Yes, because h is defined at every x in the closed interval \\( [-1, 4] \\), so the Extreme Value Theorem applies.",
   ],
   "05010-19": [
      "Yes, because g has a relative minimum at \\( x = -2 \\), so its absolute minimum value is \\( g(-2) \\).",
      "Yes, because g is defined at every x in the closed interval \\( [-5, 1] \\), so the Extreme Value Theorem applies.",
      "Yes, because g is differentiable, so continuous, on the closed interval \\( [-5, 1] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute minimum at \\( x = -2 \\), where \\( g'(-2) = 0 \\).",
   ],
   "05010-20": [
      "No, because \\( (0, 7) \\) is not a closed interval, so the Extreme Value Theorem does not apply there.",
      "No, because the Extreme Value Theorem places the absolute maximum of f on \\( [0, 7] \\) at an endpoint.",
      "Yes, because f has a relative maximum at \\( x = 5 \\), so its absolute maximum value is \\( f(5) \\).",
      "Yes, because f is continuous on the interval \\( (0, 7) \\), so the Extreme Value Theorem applies.",
   ],
   "05010-21": [
      "Yes, because h has a relative maximum at \\( x = 1 \\), so its absolute maximum value is \\( h(1) \\).",
      "Yes, because h is defined at every x in the closed interval \\( [-5, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because h is differentiable, so continuous, on the closed interval \\( [-5, 2] \\), so the Extreme Value Theorem applies.",
      "Yes, because the Extreme Value Theorem places the absolute maximum at \\( x = 1 \\), where \\( h'(1) = 0 \\).",
   ],
   "05012-00": [
      "The tangent line is horizontal only at the point \\( (5, -1) \\).",
      "The tangent line is horizontal only at the points \\( (-1, -1) \\), \\( (3, 7) \\) and \\( (3, -9) \\).",
      "The tangent line is horizontal only at the points \\( (3, 7) \\) and \\( (3, -9) \\).",
      "The tangent line is horizontal only where \\( x = 3 \\).",
   ],
   "05012-01": [
      "The tangent line is horizontal only at the point \\( (-5, 3) \\).",
      "The tangent line is horizontal only at the points \\( (-6, 5) \\) and \\( (-6, 1) \\).",
      "The tangent line is horizontal only at the points \\( (-8, 3) \\), \\( (-6, 5) \\) and \\( (-6, 1) \\).",
      "The tangent line is horizontal only where \\( x = -6 \\).",
   ],
   "05012-02": [
      "The tangent line is horizontal only at the point \\( (10, 0) \\).",
      "The tangent line is horizontal only at the points \\( (7, 0) \\), \\( (9, 2) \\) and \\( (9, -2) \\).",
      "The tangent line is horizontal only at the points \\( (9, 2) \\) and \\( (9, -2) \\).",
      "The tangent line is horizontal only where \\( x = 9 \\).",
   ],
   "05012-03": [
      "The tangent line is horizontal only at the point \\( (8, 0) \\).",
      "The tangent line is horizontal only at the points \\( (5, 0) \\), \\( (7, 4) \\) and \\( (7, -4) \\).",
      "The tangent line is horizontal only at the points \\( (7, 4) \\) and \\( (7, -4) \\).",
      "The tangent line is horizontal only where \\( x = 7 \\).",
   ],
   "05012-04": [
      "The tangent line is horizontal only at the point \\( (6, 9) \\).",
      "The tangent line is horizontal only at the points \\( (3, 9) \\), \\( (5, 15) \\) and \\( (5, 3) \\).",
      "The tangent line is horizontal only at the points \\( (5, 15) \\) and \\( (5, 3) \\).",
      "The tangent line is horizontal only where \\( x = 5 \\).",
   ],
   "05013-00": [
      "At \\( x = 3 \\), f has a relative maximum because \\( f'(3) = 0 \\) and \\( f''(3) = -42 < 0 \\); at \\( x = 5 \\), f has a relative maximum because \\( f''(5) = -66 < 0 \\).",
      "At \\( x = 3 \\), f has a relative maximum because \\( f'(3) = 0 \\) and \\( f''(3) = -42 < 0 \\); at \\( x = 5 \\), f has no relative extremum because \\( f'(5) = -108 \\ne 0 \\).",
      "At \\( x = 3 \\), f has a relative minimum because \\( f'(3) = 0 \\) and \\( f''(3) = -42 < 0 \\); at \\( x = 5 \\), f has no relative extremum because \\( f'(5) = -108 \\ne 0 \\).",
      "At \\( x = 3 \\), f has an absolute maximum because \\( f'(3) = 0 \\) and \\( f''(3) = -42 < 0 \\); at \\( x = 5 \\), f has no relative extremum because \\( f'(5) = -108 \\ne 0 \\).",
   ],
   "05013-01": [
      "At \\( x = 2 \\), f has a relative maximum because \\( f'(2) = 0 \\) and \\( f''(2) = -24 < 0 \\); at \\( x = 3 \\), f has a relative maximum because \\( f''(3) = -36 < 0 \\).",
      "At \\( x = 2 \\), f has a relative maximum because \\( f'(2) = 0 \\) and \\( f''(2) = -24 < 0 \\); at \\( x = 3 \\), f has no relative extremum because \\( f'(3) = -30 \\ne 0 \\).",
      "At \\( x = 2 \\), f has a relative minimum because \\( f'(2) = 0 \\) and \\( f''(2) = -24 < 0 \\); at \\( x = 3 \\), f has no relative extremum because \\( f'(3) = -30 \\ne 0 \\).",
      "At \\( x = 2 \\), f has an absolute maximum because \\( f'(2) = 0 \\) and \\( f''(2) = -24 < 0 \\); at \\( x = 3 \\), f has no relative extremum because \\( f'(3) = -30 \\ne 0 \\).",
   ],
   "05013-02": [
      "At \\( x = 3 \\), g has a relative maximum because \\( g'(3) = 0 \\) and \\( g''(3) = 12 > 0 \\); at \\( x = -4 \\), g has no relative extremum because \\( g'(-4) = 210 \\ne 0 \\).",
      "At \\( x = 3 \\), g has a relative minimum because \\( g'(3) = 0 \\) and \\( g''(3) = 12 > 0 \\); at \\( x = -4 \\), g has a relative maximum because \\( g''(-4) = -72 < 0 \\).",
      "At \\( x = 3 \\), g has a relative minimum because \\( g'(3) = 0 \\) and \\( g''(3) = 12 > 0 \\); at \\( x = -4 \\), g has no relative extremum because \\( g'(-4) = 210 \\ne 0 \\).",
      "At \\( x = 3 \\), g has an absolute minimum because \\( g'(3) = 0 \\) and \\( g''(3) = 12 > 0 \\); at \\( x = -4 \\), g has no relative extremum because \\( g'(-4) = 210 \\ne 0 \\).",
   ],
   "05013-03": [
      "At \\( x = -1 \\), g has a relative maximum because \\( g'(-1) = 0 \\) and \\( g''(-1) = -6 < 0 \\); at \\( x = -2 \\), g has a relative maximum because \\( g''(-2) = -18 < 0 \\).",
      "At \\( x = -1 \\), g has a relative maximum because \\( g'(-1) = 0 \\) and \\( g''(-1) = -6 < 0 \\); at \\( x = -2 \\), g has no relative extremum because \\( g'(-2) = 12 \\ne 0 \\).",
      "At \\( x = -1 \\), g has a relative minimum because \\( g'(-1) = 0 \\) and \\( g''(-1) = -6 < 0 \\); at \\( x = -2 \\), g has no relative extremum because \\( g'(-2) = 12 \\ne 0 \\).",
      "At \\( x = -1 \\), g has an absolute maximum because \\( g'(-1) = 0 \\) and \\( g''(-1) = -6 < 0 \\); at \\( x = -2 \\), g has no relative extremum because \\( g'(-2) = 12 \\ne 0 \\).",
   ],
   "05013-04": [
      "At \\( x = 3 \\), g has a relative maximum because \\( g'(3) = 0 \\) and \\( g''(3) = -30 < 0 \\); at \\( x = -1 \\), g has a relative minimum because \\( g''(-1) = 18 > 0 \\).",
      "At \\( x = 3 \\), g has a relative maximum because \\( g'(3) = 0 \\) and \\( g''(3) = -30 < 0 \\); at \\( x = -1 \\), g has no relative extremum because \\( g'(-1) = 24 \\ne 0 \\).",
      "At \\( x = 3 \\), g has a relative minimum because \\( g'(3) = 0 \\) and \\( g''(3) = -30 < 0 \\); at \\( x = -1 \\), g has no relative extremum because \\( g'(-1) = 24 \\ne 0 \\).",
      "At \\( x = 3 \\), g has an absolute maximum because \\( g'(3) = 0 \\) and \\( g''(3) = -30 < 0 \\); at \\( x = -1 \\), g has no relative extremum because \\( g'(-1) = 24 \\ne 0 \\).",
   ],
   "05013-05": [
      "At \\( x = -2 \\), f has a relative maximum because \\( f'(-2) = 0 \\) and \\( f''(-2) = -6 < 0 \\); at \\( x = 4 \\), f has a relative minimum because \\( f''(4) = 66 > 0 \\).",
      "At \\( x = -2 \\), f has a relative maximum because \\( f'(-2) = 0 \\) and \\( f''(-2) = -6 < 0 \\); at \\( x = 4 \\), f has no relative extremum because \\( f'(4) = 180 \\ne 0 \\).",
      "At \\( x = -2 \\), f has a relative minimum because \\( f'(-2) = 0 \\) and \\( f''(-2) = -6 < 0 \\); at \\( x = 4 \\), f has no relative extremum because \\( f'(4) = 180 \\ne 0 \\).",
      "At \\( x = -2 \\), f has an absolute maximum because \\( f'(-2) = 0 \\) and \\( f''(-2) = -6 < 0 \\); at \\( x = 4 \\), f has no relative extremum because \\( f'(4) = 180 \\ne 0 \\).",
   ],
   "05013-06": [
      "At \\( x = -2 \\), h has a relative maximum because \\( h'(-2) = 0 \\) and \\( h''(-2) = 18 > 0 \\); at \\( x = 0 \\), h has no relative extremum because \\( h'(0) = 12 \\ne 0 \\).",
      "At \\( x = -2 \\), h has a relative minimum because \\( h'(-2) = 0 \\) and \\( h''(-2) = 18 > 0 \\); at \\( x = 0 \\), h has a relative maximum because \\( h''(0) = -6 < 0 \\).",
      "At \\( x = -2 \\), h has a relative minimum because \\( h'(-2) = 0 \\) and \\( h''(-2) = 18 > 0 \\); at \\( x = 0 \\), h has no relative extremum because \\( h'(0) = 12 \\ne 0 \\).",
      "At \\( x = -2 \\), h has an absolute minimum because \\( h'(-2) = 0 \\) and \\( h''(-2) = 18 > 0 \\); at \\( x = 0 \\), h has no relative extremum because \\( h'(0) = 12 \\ne 0 \\).",
   ],
   "05013-07": [
      "At \\( x = 4 \\), h has a relative maximum because \\( h'(4) = 0 \\) and \\( h''(4) = -48 < 0 \\); at \\( x = -1 \\), h has a relative minimum because \\( h''(-1) = 12 > 0 \\).",
      "At \\( x = 4 \\), h has a relative maximum because \\( h'(4) = 0 \\) and \\( h''(4) = -48 < 0 \\); at \\( x = -1 \\), h has no relative extremum because \\( h'(-1) = 90 \\ne 0 \\).",
      "At \\( x = 4 \\), h has a relative minimum because \\( h'(4) = 0 \\) and \\( h''(4) = -48 < 0 \\); at \\( x = -1 \\), h has no relative extremum because \\( h'(-1) = 90 \\ne 0 \\).",
      "At \\( x = 4 \\), h has an absolute maximum because \\( h'(4) = 0 \\) and \\( h''(4) = -48 < 0 \\); at \\( x = -1 \\), h has no relative extremum because \\( h'(-1) = 90 \\ne 0 \\).",
   ],
   "05013-08": [
      "At \\( x = -4 \\), h has a relative maximum because \\( h'(-4) = 0 \\) and \\( h''(-4) = -36 < 0 \\); at \\( x = -3 \\), h has a relative maximum because \\( h''(-3) = -24 < 0 \\).",
      "At \\( x = -4 \\), h has a relative maximum because \\( h'(-4) = 0 \\) and \\( h''(-4) = -36 < 0 \\); at \\( x = -3 \\), h has no relative extremum because \\( h'(-3) = -30 \\ne 0 \\).",
      "At \\( x = -4 \\), h has a relative minimum because \\( h'(-4) = 0 \\) and \\( h''(-4) = -36 < 0 \\); at \\( x = -3 \\), h has no relative extremum because \\( h'(-3) = -30 \\ne 0 \\).",
      "At \\( x = -4 \\), h has an absolute maximum because \\( h'(-4) = 0 \\) and \\( h''(-4) = -36 < 0 \\); at \\( x = -3 \\), h has no relative extremum because \\( h'(-3) = -30 \\ne 0 \\).",
   ],
   "05013-09": [
      "At \\( x = 3 \\), g has a relative maximum because \\( g'(3) = 0 \\) and \\( g''(3) = -42 < 0 \\); at \\( x = -2 \\), g has a relative minimum because \\( g''(-2) = 18 > 0 \\).",
      "At \\( x = 3 \\), g has a relative maximum because \\( g'(3) = 0 \\) and \\( g''(3) = -42 < 0 \\); at \\( x = -2 \\), g has no relative extremum because \\( g'(-2) = 60 \\ne 0 \\).",
      "At \\( x = 3 \\), g has a relative minimum because \\( g'(3) = 0 \\) and \\( g''(3) = -42 < 0 \\); at \\( x = -2 \\), g has no relative extremum because \\( g'(-2) = 60 \\ne 0 \\).",
      "At \\( x = 3 \\), g has an absolute maximum because \\( g'(3) = 0 \\) and \\( g''(3) = -42 < 0 \\); at \\( x = -2 \\), g has no relative extremum because \\( g'(-2) = 60 \\ne 0 \\).",
   ],
   "05013-10": [
      "At \\( x = -3 \\), h has a relative maximum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -18 < 0 \\); at \\( x = 5 \\), h has a relative minimum because \\( h''(5) = 78 > 0 \\).",
      "At \\( x = -3 \\), h has a relative maximum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -18 < 0 \\); at \\( x = 5 \\), h has no relative extremum because \\( h'(5) = 240 \\ne 0 \\).",
      "At \\( x = -3 \\), h has a relative minimum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -18 < 0 \\); at \\( x = 5 \\), h has no relative extremum because \\( h'(5) = 240 \\ne 0 \\).",
      "At \\( x = -3 \\), h has an absolute maximum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -18 < 0 \\); at \\( x = 5 \\), h has no relative extremum because \\( h'(5) = 240 \\ne 0 \\).",
   ],
   "05013-11": [
      "At \\( x = 4 \\), f has a relative maximum because \\( f'(4) = 0 \\) and \\( f''(4) = 42 > 0 \\); at \\( x = 2 \\), f has no relative extremum because \\( f'(2) = -60 \\ne 0 \\).",
      "At \\( x = 4 \\), f has a relative minimum because \\( f'(4) = 0 \\) and \\( f''(4) = 42 > 0 \\); at \\( x = 2 \\), f has a relative minimum because \\( f''(2) = 18 > 0 \\).",
      "At \\( x = 4 \\), f has a relative minimum because \\( f'(4) = 0 \\) and \\( f''(4) = 42 > 0 \\); at \\( x = 2 \\), f has no relative extremum because \\( f'(2) = -60 \\ne 0 \\).",
      "At \\( x = 4 \\), f has an absolute minimum because \\( f'(4) = 0 \\) and \\( f''(4) = 42 > 0 \\); at \\( x = 2 \\), f has no relative extremum because \\( f'(2) = -60 \\ne 0 \\).",
   ],
   "05013-12": [
      "At \\( x = -2 \\), f has a relative maximum because \\( f'(-2) = 0 \\) and \\( f''(-2) = 18 > 0 \\); at \\( x = 5 \\), f has no relative extremum because \\( f'(5) = -168 \\ne 0 \\).",
      "At \\( x = -2 \\), f has a relative minimum because \\( f'(-2) = 0 \\) and \\( f''(-2) = 18 > 0 \\); at \\( x = 5 \\), f has a relative maximum because \\( f''(5) = -66 < 0 \\).",
      "At \\( x = -2 \\), f has a relative minimum because \\( f'(-2) = 0 \\) and \\( f''(-2) = 18 > 0 \\); at \\( x = 5 \\), f has no relative extremum because \\( f'(5) = -168 \\ne 0 \\).",
      "At \\( x = -2 \\), f has an absolute minimum because \\( f'(-2) = 0 \\) and \\( f''(-2) = 18 > 0 \\); at \\( x = 5 \\), f has no relative extremum because \\( f'(5) = -168 \\ne 0 \\).",
   ],
   "05013-13": [
      "At \\( x = 3 \\), h has a relative maximum because \\( h'(3) = 0 \\) and \\( h''(3) = 18 > 0 \\); at \\( x = 1 \\), h has no relative extremum because \\( h'(1) = -12 \\ne 0 \\).",
      "At \\( x = 3 \\), h has a relative minimum because \\( h'(3) = 0 \\) and \\( h''(3) = 18 > 0 \\); at \\( x = 1 \\), h has a relative maximum because \\( h''(1) = -6 < 0 \\).",
      "At \\( x = 3 \\), h has a relative minimum because \\( h'(3) = 0 \\) and \\( h''(3) = 18 > 0 \\); at \\( x = 1 \\), h has no relative extremum because \\( h'(1) = -12 \\ne 0 \\).",
      "At \\( x = 3 \\), h has an absolute minimum because \\( h'(3) = 0 \\) and \\( h''(3) = 18 > 0 \\); at \\( x = 1 \\), h has no relative extremum because \\( h'(1) = -12 \\ne 0 \\).",
   ],
   "05013-14": [
      "At \\( x = 2 \\), h has a relative maximum because \\( h'(2) = 0 \\) and \\( h''(2) = 30 > 0 \\); at \\( x = 5 \\), h has no relative extremum because \\( h'(5) = 144 \\ne 0 \\).",
      "At \\( x = 2 \\), h has a relative minimum because \\( h'(2) = 0 \\) and \\( h''(2) = 30 > 0 \\); at \\( x = 5 \\), h has a relative minimum because \\( h''(5) = 66 > 0 \\).",
      "At \\( x = 2 \\), h has a relative minimum because \\( h'(2) = 0 \\) and \\( h''(2) = 30 > 0 \\); at \\( x = 5 \\), h has no relative extremum because \\( h'(5) = 144 \\ne 0 \\).",
      "At \\( x = 2 \\), h has an absolute minimum because \\( h'(2) = 0 \\) and \\( h''(2) = 30 > 0 \\); at \\( x = 5 \\), h has no relative extremum because \\( h'(5) = 144 \\ne 0 \\).",
   ],
   "05013-15": [
      "At \\( x = -4 \\), g has a relative maximum because \\( g'(-4) = 0 \\) and \\( g''(-4) = 18 > 0 \\); at \\( x = 5 \\), g has no relative extremum because \\( g'(5) = -324 \\ne 0 \\).",
      "At \\( x = -4 \\), g has a relative minimum because \\( g'(-4) = 0 \\) and \\( g''(-4) = 18 > 0 \\); at \\( x = 5 \\), g has a relative maximum because \\( g''(5) = -90 < 0 \\).",
      "At \\( x = -4 \\), g has a relative minimum because \\( g'(-4) = 0 \\) and \\( g''(-4) = 18 > 0 \\); at \\( x = 5 \\), g has no relative extremum because \\( g'(5) = -324 \\ne 0 \\).",
      "At \\( x = -4 \\), g has an absolute minimum because \\( g'(-4) = 0 \\) and \\( g''(-4) = 18 > 0 \\); at \\( x = 5 \\), g has no relative extremum because \\( g'(5) = -324 \\ne 0 \\).",
   ],
   "05013-16": [
      "At \\( x = -1 \\), f has a relative maximum because \\( f'(-1) = 0 \\) and \\( f''(-1) = -30 < 0 \\); at \\( x = 3 \\), f has a relative minimum because \\( f''(3) = 18 > 0 \\).",
      "At \\( x = -1 \\), f has a relative maximum because \\( f'(-1) = 0 \\) and \\( f''(-1) = -30 < 0 \\); at \\( x = 3 \\), f has no relative extremum because \\( f'(3) = -24 \\ne 0 \\).",
      "At \\( x = -1 \\), f has a relative minimum because \\( f'(-1) = 0 \\) and \\( f''(-1) = -30 < 0 \\); at \\( x = 3 \\), f has no relative extremum because \\( f'(3) = -24 \\ne 0 \\).",
      "At \\( x = -1 \\), f has an absolute maximum because \\( f'(-1) = 0 \\) and \\( f''(-1) = -30 < 0 \\); at \\( x = 3 \\), f has no relative extremum because \\( f'(3) = -24 \\ne 0 \\).",
   ],
   "05013-17": [
      "At \\( x = -2 \\), g has a relative maximum because \\( g'(-2) = 0 \\) and \\( g''(-2) = -24 < 0 \\); at \\( x = -5 \\), g has a relative maximum because \\( g''(-5) = -60 < 0 \\).",
      "At \\( x = -2 \\), g has a relative maximum because \\( g'(-2) = 0 \\) and \\( g''(-2) = -24 < 0 \\); at \\( x = -5 \\), g has no relative extremum because \\( g'(-5) = 126 \\ne 0 \\).",
      "At \\( x = -2 \\), g has a relative minimum because \\( g'(-2) = 0 \\) and \\( g''(-2) = -24 < 0 \\); at \\( x = -5 \\), g has no relative extremum because \\( g'(-5) = 126 \\ne 0 \\).",
      "At \\( x = -2 \\), g has an absolute maximum because \\( g'(-2) = 0 \\) and \\( g''(-2) = -24 < 0 \\); at \\( x = -5 \\), g has no relative extremum because \\( g'(-5) = 126 \\ne 0 \\).",
   ],
   "05013-18": [
      "At \\( x = -3 \\), g has a relative maximum because \\( g'(-3) = 0 \\) and \\( g''(-3) = -6 < 0 \\); at \\( x = 5 \\), g has a relative maximum because \\( g''(5) = -102 < 0 \\).",
      "At \\( x = -3 \\), g has a relative maximum because \\( g'(-3) = 0 \\) and \\( g''(-3) = -6 < 0 \\); at \\( x = 5 \\), g has no relative extremum because \\( g'(5) = -432 \\ne 0 \\).",
      "At \\( x = -3 \\), g has a relative minimum because \\( g'(-3) = 0 \\) and \\( g''(-3) = -6 < 0 \\); at \\( x = 5 \\), g has no relative extremum because \\( g'(5) = -432 \\ne 0 \\).",
      "At \\( x = -3 \\), g has an absolute maximum because \\( g'(-3) = 0 \\) and \\( g''(-3) = -6 < 0 \\); at \\( x = 5 \\), g has no relative extremum because \\( g'(5) = -432 \\ne 0 \\).",
   ],
   "05013-19": [
      "At \\( x = -1 \\), h has a relative maximum because \\( h'(-1) = 0 \\) and \\( h''(-1) = -18 < 0 \\); at \\( x = -3 \\), h has a relative minimum because \\( h''(-3) = 6 > 0 \\).",
      "At \\( x = -1 \\), h has a relative maximum because \\( h'(-1) = 0 \\) and \\( h''(-1) = -18 < 0 \\); at \\( x = -3 \\), h has no relative extremum because \\( h'(-3) = 12 \\ne 0 \\).",
      "At \\( x = -1 \\), h has a relative minimum because \\( h'(-1) = 0 \\) and \\( h''(-1) = -18 < 0 \\); at \\( x = -3 \\), h has no relative extremum because \\( h'(-3) = 12 \\ne 0 \\).",
      "At \\( x = -1 \\), h has an absolute maximum because \\( h'(-1) = 0 \\) and \\( h''(-1) = -18 < 0 \\); at \\( x = -3 \\), h has no relative extremum because \\( h'(-3) = 12 \\ne 0 \\).",
   ],
   "05013-20": [
      "At \\( x = 1 \\), g has a relative maximum because \\( g'(1) = 0 \\) and \\( g''(1) = 12 > 0 \\); at \\( x = -5 \\), g has no relative extremum because \\( g'(-5) = -288 \\ne 0 \\).",
      "At \\( x = 1 \\), g has a relative minimum because \\( g'(1) = 0 \\) and \\( g''(1) = 12 > 0 \\); at \\( x = -5 \\), g has a relative minimum because \\( g''(-5) = 84 > 0 \\).",
      "At \\( x = 1 \\), g has a relative minimum because \\( g'(1) = 0 \\) and \\( g''(1) = 12 > 0 \\); at \\( x = -5 \\), g has no relative extremum because \\( g'(-5) = -288 \\ne 0 \\).",
      "At \\( x = 1 \\), g has an absolute minimum because \\( g'(1) = 0 \\) and \\( g''(1) = 12 > 0 \\); at \\( x = -5 \\), g has no relative extremum because \\( g'(-5) = -288 \\ne 0 \\).",
   ],
   "05013-21": [
      "At \\( x = -3 \\), h has a relative maximum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -6 < 0 \\); at \\( x = 2 \\), h has a relative maximum because \\( h''(2) = -66 < 0 \\).",
      "At \\( x = -3 \\), h has a relative maximum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -6 < 0 \\); at \\( x = 2 \\), h has no relative extremum because \\( h'(2) = -180 \\ne 0 \\).",
      "At \\( x = -3 \\), h has a relative minimum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -6 < 0 \\); at \\( x = 2 \\), h has no relative extremum because \\( h'(2) = -180 \\ne 0 \\).",
      "At \\( x = -3 \\), h has an absolute maximum because \\( h'(-3) = 0 \\) and \\( h''(-3) = -6 < 0 \\); at \\( x = 2 \\), h has no relative extremum because \\( h'(2) = -180 \\ne 0 \\).",
   ],
}

PLOTTED = {
   "05009-00": {
      "curves": [
         [(-1.5, 0.2222), (-0.1667, 2.4486), (1.1667, 1.5144), (2.5, -1.0), (3.8333, -3.5144), (5.1667, -4.4486), (6.5, -2.2222)],
         [(-1.5, 3.25), (-0.1667, 0.287), (1.1667, -1.4907), (2.5, -2.0833), (3.8333, -1.4907), (5.1667, 0.287), (6.5, 3.25)],
         [(-1.5, -2.6667), (-0.1667, -1.7778), (1.1667, -0.8889), (2.5, -0.0), (3.8333, 0.8889), (5.1667, 1.7778), (6.5, 2.6667)],
      ],
      "labels": {"A": [-0.92, -2.78], "B": [4.12, -1.7085], "C": [5.92, -4.1804]},
   },
   "05009-01": {
      "curves": [
         [(-2.5, 1.8333), (-1.1667, 5.1728), (0.1667, 3.7716), (1.5, 0.0), (2.8333, -3.7716), (4.1667, -5.1728), (5.5, -1.8333)],
         [(-2.5, 4.875), (-1.1667, 0.4306), (0.1667, -2.2361), (1.5, -3.125), (2.8333, -2.2361), (4.1667, 0.4306), (5.5, 4.875)],
         [(-2.5, -4.0), (-1.1667, -2.6667), (0.1667, -1.3333), (1.5, 0.0), (2.8333, 1.3333), (4.1667, 2.6667), (5.5, 4.0)],
      ],
      "labels": {"A": [2.58, 1.58], "B": [-1.38, 1.5222], "C": [4.92, -4.5206]},
   },
   "05009-02": {
      "curves": [
         [(-1.5, 4.6667), (-0.1667, 11.3457), (1.1667, 8.5432), (2.5, 1.0), (3.8333, -6.5432), (5.1667, -9.3457), (6.5, -2.6667)],
         [(-1.5, 9.75), (-0.1667, 0.8611), (1.1667, -4.4722), (2.5, -6.25), (3.8333, -4.4722), (5.1667, 0.8611), (6.5, 9.75)],
         [(-1.5, -8.0), (-0.1667, -5.3333), (1.1667, -2.6667), (2.5, 0.0), (3.8333, 2.6667), (5.1667, 5.3333), (6.5, 8.0)],
      ],
      "labels": {"A": [0.7, 10.806], "B": [3.58, 2.66], "C": [-0.56, 2.6136]},
   },
   "05009-03": {
      "curves": [
         [(-4.5, -0.2917), (-3.3333, 5.0988), (-2.1667, 4.1373), (-1.0, 0.0), (0.1667, -4.1373), (1.3333, -5.0988), (2.5, 0.2917)],
         [(-4.5, 8.25), (-3.3333, 1.4444), (-2.1667, -2.6389), (-1.0, -4.0), (0.1667, -2.6389), (1.3333, 1.4444), (2.5, 8.25)],
         [(-4.5, -7.0), (-3.3333, -4.6667), (-2.1667, -2.3333), (-1.0, 0.0), (0.1667, 2.3333), (1.3333, 4.6667), (2.5, 7.0)],
      ],
      "labels": {"A": [-3.17, 0.2089], "B": [-0.07, 2.36], "C": [1.945, -3.766]},
   },
   "05009-04": {
      "curves": [
         [(-4.5, 1.9028), (-3.3333, 3.6996), (-2.1667, 3.3791), (-1.0, 2.0), (0.1667, 0.6209), (1.3333, 0.3004), (2.5, 2.0972)],
         [(-4.5, 2.75), (-3.3333, 0.4815), (-2.1667, -0.8796), (-1.0, -1.3333), (0.1667, -0.8796), (1.3333, 0.4815), (2.5, 2.75)],
         [(-4.5, -2.3333), (-3.3333, -1.5556), (-2.1667, -0.7778), (-1.0, 0.0), (0.1667, 0.7778), (1.3333, 1.5556), (2.5, 2.3333)],
      ],
      "labels": {"A": [-2.24, 3.9415], "B": [-3.635, 0.4811], "C": [-0.845, 0.6033]},
   },
   "05009-05": {
      "curves": [
         [(-2.5, 0.125), (-1.5, -1.9167), (-0.5, -1.9583), (0.5, -1.0), (1.5, -0.0417), (2.5, -0.0833), (3.5, -2.125)],
         [(-2.5, -3.375), (-1.5, -0.875), (-0.5, 0.625), (0.5, 1.125), (1.5, 0.625), (2.5, -0.875), (3.5, -3.375)],
         [(-2.5, 3.0), (-1.5, 2.0), (-0.5, 1.0), (0.5, 0.0), (1.5, -1.0), (2.5, -2.0), (3.5, -3.0)],
      ],
      "labels": {"A": [-0.41, -2.3982], "B": [0.89, 1.549], "C": [-1.84, 2.84]},
   },
   "05009-06": {
      "curves": [
         [(-2.5, -0.2222), (-1.1667, -2.4486), (0.1667, -1.5144), (1.5, 1.0), (2.8333, 3.5144), (4.1667, 4.4486), (5.5, 2.2222)],
         [(-2.5, -3.25), (-1.1667, -0.287), (0.1667, 1.4907), (1.5, 2.0833), (2.8333, 1.4907), (4.1667, -0.287), (5.5, -3.25)],
         [(-2.5, 2.6667), (-1.1667, 1.7778), (0.1667, 0.8889), (1.5, 0.0), (2.8333, -0.8889), (4.1667, -1.7778), (5.5, -2.6667)],
      ],
      "labels": {"A": [3.12, 1.7085], "B": [4.92, 4.1804], "C": [-1.92, 2.78]},
   },
   "05009-07": {
      "curves": [
         [(-4.5, 0.5), (-3.5, -2.2222), (-2.5, -2.2778), (-1.5, -1.0), (-0.5, 0.2778), (0.5, 0.2222), (1.5, -2.5)],
         [(-4.5, -4.5), (-3.5, -1.1667), (-2.5, 0.8333), (-1.5, 1.5), (-0.5, 0.8333), (0.5, -1.1667), (1.5, -4.5)],
         [(-4.5, 4.0), (-3.5, 2.6667), (-2.5, 1.3333), (-1.5, 0.0), (-0.5, -1.3333), (0.5, -2.6667), (1.5, -4.0)],
      ],
      "labels": {"A": [-2.41, -2.6975], "B": [-1.11, 1.8986], "C": [-3.84, 3.62]},
   },
   "05009-08": {
      "curves": [
         [(-3.5, 2.8333), (-2.1667, 6.1728), (-0.8333, 4.7716), (0.5, 1.0), (1.8333, -2.7716), (3.1667, -4.1728), (4.5, -0.8333)],
         [(-3.5, 4.875), (-2.1667, 0.4306), (-0.8333, -2.2361), (0.5, -3.125), (1.8333, -2.2361), (3.1667, 0.4306), (4.5, 4.875)],
         [(-3.5, -4.0), (-2.1667, -2.6667), (-0.8333, -1.3333), (0.5, 0.0), (1.8333, 1.3333), (3.1667, 2.6667), (4.5, 4.0)],
      ],
      "labels": {"A": [1.76, 1.76], "B": [-2.56, 1.0568], "C": [-1.3, 6.153]},
   },
   "05009-09": {
      "curves": [
         [(-4.5, -2.2917), (-3.3333, 3.0988), (-2.1667, 2.1373), (-1.0, -2.0), (0.1667, -6.1373), (1.3333, -7.0988), (2.5, -1.7083)],
         [(-4.5, 8.25), (-3.3333, 1.4444), (-2.1667, -2.6389), (-1.0, -4.0), (0.1667, -2.6389), (1.3333, 1.4444), (2.5, 8.25)],
         [(-4.5, -7.0), (-3.3333, -4.6667), (-2.1667, -2.3333), (-1.0, 0.0), (0.1667, 2.3333), (1.3333, 4.6667), (2.5, 7.0)],
      ],
      "labels": {"A": [-3.635, -5.77], "B": [0.55, -2.0975], "C": [1.945, -5.766]},
   },
   "05009-10": {
      "curves": [
         [(-3.5, 1.4444), (-2.1667, 5.8971), (-0.8333, 4.0288), (0.5, -1.0), (1.8333, -6.0288), (3.1667, -7.8971), (4.5, -3.4444)],
         [(-3.5, 6.5), (-2.1667, 0.5741), (-0.8333, -2.9815), (0.5, -4.1667), (1.8333, -2.9815), (3.1667, 0.5741), (4.5, 6.5)],
         [(-3.5, -5.3333), (-2.1667, -3.5556), (-0.8333, -1.7778), (0.5, 0.0), (1.8333, 1.7778), (3.1667, 3.5556), (4.5, 5.3333)],
      ],
      "labels": {"A": [-2.92, -5.06], "B": [2.3, -2.5067], "C": [3.92, -6.8607]},
   },
   "05009-11": {
      "curves": [
         [(-3.5, -1.0972), (-2.3333, 0.6996), (-1.1667, 0.3791), (0.0, -1.0), (1.1667, -2.3791), (2.3333, -2.6996), (3.5, -0.9028)],
         [(-3.5, 2.75), (-2.3333, 0.4815), (-1.1667, -0.8796), (0.0, -1.3333), (1.1667, -0.8796), (2.3333, 0.4815), (3.5, 2.75)],
         [(-3.5, -2.3333), (-2.3333, -1.5556), (-1.1667, -0.7778), (0.0, 0.0), (1.1667, 0.7778), (2.3333, 1.5556), (3.5, 2.3333)],
      ],
      "labels": {"A": [-2.48, -2.1533], "B": [1.24, -0.3208], "C": [2.945, -2.5887]},
   },
   "05009-12": {
      "curves": [
         [(-3.5, 0.125), (-2.5, -1.9167), (-1.5, -1.9583), (-0.5, -1.0), (0.5, -0.0417), (1.5, -0.0833), (2.5, -2.125)],
         [(-3.5, -3.375), (-2.5, -0.875), (-1.5, 0.625), (-0.5, 1.125), (0.5, 0.625), (1.5, -0.875), (2.5, -3.375)],
         [(-3.5, 3.0), (-2.5, 2.0), (-1.5, 1.0), (-0.5, 0.0), (0.5, -1.0), (1.5, -2.0), (2.5, -3.0)],
      ],
      "labels": {"A": [-1.41, -2.3982], "B": [-0.11, 1.549], "C": [-2.84, 2.84]},
   },
   "05009-13": {
      "curves": [
         [(-2.5, 0.8333), (-1.1667, 4.1728), (0.1667, 2.7716), (1.5, -1.0), (2.8333, -4.7716), (4.1667, -6.1728), (5.5, -2.8333)],
         [(-2.5, 4.875), (-1.1667, 0.4306), (0.1667, -2.2361), (1.5, -3.125), (2.8333, -2.2361), (4.1667, 0.4306), (5.5, 4.875)],
         [(-2.5, -4.0), (-1.1667, -2.6667), (0.1667, -1.3333), (1.5, 0.0), (2.8333, 1.3333), (4.1667, 2.6667), (5.5, 4.0)],
      ],
      "labels": {"A": [4.92, -5.5206], "B": [-1.92, -3.92], "C": [3.12, -2.3128]},
   },
   "05009-14": {
      "curves": [
         [(-2.5, 1.125), (-1.5, -0.9167), (-0.5, -0.9583), (0.5, 0.0), (1.5, 0.9583), (2.5, 0.9167), (3.5, -1.125)],
         [(-2.5, -3.375), (-1.5, -0.875), (-0.5, 0.625), (0.5, 1.125), (1.5, 0.625), (2.5, -0.875), (3.5, -3.375)],
         [(-2.5, 3.0), (-1.5, 2.0), (-0.5, 1.0), (0.5, 0.0), (1.5, -1.0), (2.5, -2.0), (3.5, -3.0)],
      ],
      "labels": {"A": [2.97, 0.7672], "B": [-1.97, -2.4255], "C": [1.54, -1.54]},
   },
   "05009-15": {
      "curves": [
         [(-1.5, 1.1458), (-0.3333, -1.5494), (0.8333, -1.0687), (2.0, 1.0), (3.1667, 3.0687), (4.3333, 3.5494), (5.5, 0.8542)],
         [(-1.5, -4.125), (-0.3333, -0.7222), (0.8333, 1.3194), (2.0, 2.0), (3.1667, 1.3194), (4.3333, -0.7222), (5.5, -4.125)],
         [(-1.5, 3.5), (-0.3333, 2.3333), (0.8333, 1.1667), (2.0, 0.0), (3.1667, -1.1667), (4.3333, -2.3333), (5.5, -3.5)],
      ],
      "labels": {"A": [3.55, 1.2987], "B": [4.945, 3.133], "C": [-0.635, 3.135]},
   },
   "05009-16": {
      "curves": [
         [(-1.5, -3.5), (-0.5, -0.7778), (0.5, -0.7222), (1.5, -2.0), (2.5, -3.2778), (3.5, -3.2222), (4.5, -0.5)],
         [(-1.5, 4.5), (-0.5, 1.1667), (0.5, -0.8333), (1.5, -1.5), (2.5, -0.8333), (3.5, 1.1667), (4.5, 4.5)],
         [(-1.5, -4.0), (-0.5, -2.6667), (0.5, -1.3333), (1.5, 0.0), (2.5, 1.3333), (3.5, 2.6667), (4.5, 4.0)],
      ],
      "labels": {"A": [3.97, -2.8563], "B": [-0.97, 3.0673], "C": [2.54, 1.8867]},
   },
   "05009-17": {
      "curves": [
         [(-1.5, -2.125), (-0.5, -0.0833), (0.5, -0.0417), (1.5, -1.0), (2.5, -1.9583), (3.5, -1.9167), (4.5, 0.125)],
         [(-1.5, 3.375), (-0.5, 0.875), (0.5, -0.625), (1.5, -1.125), (2.5, -0.625), (3.5, 0.875), (4.5, 3.375)],
         [(-1.5, -3.0), (-0.5, -2.0), (0.5, -1.0), (1.5, 0.0), (2.5, 1.0), (3.5, 2.0), (4.5, 3.0)],
      ],
      "labels": {"A": [-0.97, 2.4255], "B": [2.54, 1.54], "C": [3.97, -1.7672]},
   },
   "05009-18": {
      "curves": [
         [(-4.5, -0.8056), (-3.3333, -4.3992), (-2.1667, -3.7582), (-1.0, -1.0), (0.1667, 1.7582), (1.3333, 2.3992), (2.5, -1.1944)],
         [(-4.5, -5.5), (-3.3333, -0.963), (-2.1667, 1.7593), (-1.0, 2.6667), (0.1667, 1.7593), (1.3333, -0.963), (2.5, -5.5)],
         [(-4.5, 4.6667), (-3.3333, 3.1111), (-2.1667, 1.5556), (-1.0, 0.0), (0.1667, -1.5556), (1.3333, -3.1111), (2.5, -4.6667)],
      ],
      "labels": {"A": [-0.845, 3.1507], "B": [-3.945, 4.4267], "C": [-2.24, -4.383]},
   },
   "05009-19": {
      "curves": [
         [(-4.5, -3.4444), (-3.1667, -7.8971), (-1.8333, -6.0288), (-0.5, -1.0), (0.8333, 4.0288), (2.1667, 5.8971), (3.5, 1.4444)],
         [(-4.5, -6.5), (-3.1667, -0.5741), (-1.8333, 2.9815), (-0.5, 4.1667), (0.8333, 2.9815), (2.1667, -0.5741), (3.5, -6.5)],
         [(-4.5, 5.3333), (-3.1667, 3.5556), (-1.8333, 1.7778), (-0.5, 0.0), (0.8333, -1.7778), (2.1667, -3.5556), (3.5, -5.3333)],
      ],
      "labels": {"A": [-3.56, -1.5757], "B": [-2.3, -7.704], "C": [0.76, -2.18]},
   },
   "05009-20": {
      "curves": [
         [(-3.5, -1.25), (-2.5, 2.8333), (-1.5, 2.9167), (-0.5, 1.0), (0.5, -0.9167), (1.5, -0.8333), (2.5, 3.25)],
         [(-3.5, 6.75), (-2.5, 1.75), (-1.5, -1.25), (-0.5, -2.25), (0.5, -1.25), (1.5, 1.75), (2.5, 6.75)],
         [(-3.5, -6.0), (-2.5, -4.0), (-1.5, -2.0), (-0.5, 0.0), (0.5, 2.0), (1.5, 4.0), (2.5, 6.0)],
      ],
      "labels": {"A": [1.45, 1.0525], "B": [-2.71, -4.92], "C": [-1.41, 3.2963]},
   },
   "05009-21": {
      "curves": [
         [(-2.5, -1.5), (-1.5, 1.2222), (-0.5, 1.2778), (0.5, 0.0), (1.5, -1.2778), (2.5, -1.2222), (3.5, 1.5)],
         [(-2.5, 4.5), (-1.5, 1.1667), (-0.5, -0.8333), (0.5, -1.5), (1.5, -0.8333), (2.5, 1.1667), (3.5, 4.5)],
         [(-2.5, -4.0), (-1.5, -2.6667), (-0.5, -1.3333), (0.5, 0.0), (1.5, 1.3333), (2.5, 2.6667), (3.5, 4.0)],
      ],
      "labels": {"A": [1.54, 1.8867], "B": [-1.97, 3.0673], "C": [2.97, -0.8563]},
   },
}


BY_SUFFIX = {
   "05007-00": lambda: critical_point_choice("05007-00", expression("(4 - 2*x)*(x + 4)"), 0, 6, "H"),
   "05007-01": lambda: critical_point_choice("05007-01", expression("(x - 8)*(3*x - 3)"), 0, 7, "g"),
   "05007-02": lambda: critical_point_choice("05007-02", expression("(x - 9)*(2*x - 8)"), 0, 5, "H"),
   "05007-03": lambda: critical_point_choice("05007-03", expression("(3 - x)*(x - 10)"), 0, 6, "G"),
   "05008-00": lambda: monotonic_choice("05008-00", expression("(x - 2)*(2*x + 8)/x"), "decreasing"),
   "05008-01": lambda: monotonic_choice("05008-01", expression("4*x*(x - 3)"), "increasing"),
   "05008-02": lambda: monotonic_choice("05008-02", expression("(x + 4)*(2*x + 10)/(x - 4)**2"), "increasing"),
   "05008-03": lambda: monotonic_choice("05008-03", expression("-(x - 1)*(4*x + 4)/(x + 2)"), "decreasing"),
   "05008-04": lambda: monotonic_choice("05008-04", expression("(x + 1)*(3*x + 15)/(x - 4)"), "increasing"),
   "05008-05": lambda: monotonic_choice("05008-05", expression("-2*x*(x + 4)"), "decreasing"),
   "05008-06": lambda: monotonic_choice("05008-06", expression("(x - 5)*(3*x - 12)/(x - 3)**2"), "increasing"),
   "05008-07": lambda: monotonic_choice("05008-07", expression("(x - 3)*(3*x - 6)/(x + 3)"), "decreasing"),
   "05008-08": lambda: monotonic_choice("05008-08", expression("(x - 1)*(4*x + 8)"), "decreasing"),
   "05008-09": lambda: monotonic_choice("05008-09", expression("(x + 2)*(4*x + 12)/x"), "decreasing"),
   "05008-10": lambda: monotonic_choice("05008-10", expression("-(x - 4)*(3*x + 12)/(x - 2)**2"), "increasing"),
   "05008-11": lambda: monotonic_choice("05008-11", expression("(-2*x - 2)*(x - 2)"), "decreasing"),
   "05008-12": lambda: monotonic_choice("05008-12", expression("(x - 2)*(3*x - 3)/x"), "increasing"),
   "05008-13": lambda: monotonic_choice("05008-13", expression("-(x - 3)*(4*x - 8)/(x + 5)**2"), "decreasing"),
   "05008-14": lambda: monotonic_choice("05008-14", expression("(-3*x - 6)*(x - 5)"), "decreasing"),
   "05008-15": lambda: monotonic_choice("05008-15", expression("(x - 5)*(2*x + 10)/(x - 1)**2"), "decreasing"),
   "05008-16": lambda: monotonic_choice("05008-16", expression("(x - 2)*(2*x - 2)/x**2"), "increasing"),
   "05008-17": lambda: monotonic_choice("05008-17", expression("(x - 4)*(x + 3)/x**2"), "decreasing"),
   "05008-18": lambda: monotonic_choice("05008-18", expression("(-x - 3)*(x + 1)"), "increasing"),
   "05008-19": lambda: monotonic_choice("05008-19", expression("3*x*(x + 4)/(x + 1)**2"), "decreasing"),
   "05008-20": lambda: monotonic_choice("05008-20", expression("x*(x + 1)/(x - 4)"), "increasing"),
   "05008-21": lambda: monotonic_choice("05008-21", expression("(-3*x - 9)*(x + 2)"), "decreasing"),
   "05009-00": lambda: antiderivative_chain_choice("05009-00", ("g", "G", "K")),
   "05009-01": lambda: antiderivative_chain_choice("05009-01", ("g", "G", "K")),
   "05009-02": lambda: antiderivative_chain_choice("05009-02", ("g", "G", "K")),
   "05009-03": lambda: antiderivative_chain_choice("05009-03", ("g", "G", "K")),
   "05009-04": lambda: antiderivative_chain_choice("05009-04", ("f''", "f'", "f")),
   "05009-05": lambda: antiderivative_chain_choice("05009-05", ("g", "G", "K")),
   "05009-06": lambda: antiderivative_chain_choice("05009-06", ("f''", "f'", "f")),
   "05009-07": lambda: antiderivative_chain_choice("05009-07", ("f''", "f'", "f")),
   "05009-08": lambda: antiderivative_chain_choice("05009-08", ("f''", "f'", "f")),
   "05009-09": lambda: antiderivative_chain_choice("05009-09", ("g", "G", "K")),
   "05009-10": lambda: antiderivative_chain_choice("05009-10", ("f''", "f'", "f")),
   "05009-11": lambda: antiderivative_chain_choice("05009-11", ("f''", "f'", "f")),
   "05009-12": lambda: antiderivative_chain_choice("05009-12", ("f''", "f'", "f")),
   "05009-13": lambda: antiderivative_chain_choice("05009-13", ("g", "G", "K")),
   "05009-14": lambda: antiderivative_chain_choice("05009-14", ("f''", "f'", "f")),
   "05009-15": lambda: antiderivative_chain_choice("05009-15", ("f''", "f'", "f")),
   "05009-16": lambda: antiderivative_chain_choice("05009-16", ("g", "G", "K")),
   "05009-17": lambda: antiderivative_chain_choice("05009-17", ("g", "G", "K")),
   "05009-18": lambda: antiderivative_chain_choice("05009-18", ("g", "G", "K")),
   "05009-19": lambda: antiderivative_chain_choice("05009-19", ("f''", "f'", "f")),
   "05009-20": lambda: antiderivative_chain_choice("05009-20", ("f''", "f'", "f")),
   "05009-21": lambda: antiderivative_chain_choice("05009-21", ("g", "G", "K")),
   "05010-00": lambda: extreme_value_choice("05010-00", "f", "jump", "closed"),
   "05010-01": lambda: extreme_value_choice("05010-01", "g", "differentiable", "closed"),
   "05010-02": lambda: extreme_value_choice("05010-02", "g", "differentiable", "closed"),
   "05010-03": lambda: extreme_value_choice("05010-03", "g", "jump", "closed"),
   "05010-04": lambda: extreme_value_choice("05010-04", "g", "differentiable", "closed"),
   "05010-05": lambda: extreme_value_choice("05010-05", "f", "differentiable", "closed"),
   "05010-06": lambda: extreme_value_choice("05010-06", "g", "differentiable", "open"),
   "05010-07": lambda: extreme_value_choice("05010-07", "h", "continuous", "closed"),
   "05010-08": lambda: extreme_value_choice("05010-08", "g", "continuous", "closed"),
   "05010-09": lambda: extreme_value_choice("05010-09", "h", "differentiable", "closed"),
   "05010-10": lambda: extreme_value_choice("05010-10", "g", "differentiable", "closed"),
   "05010-11": lambda: extreme_value_choice("05010-11", "h", "jump", "closed"),
   "05010-12": lambda: extreme_value_choice("05010-12", "h", "differentiable", "closed"),
   "05010-13": lambda: extreme_value_choice("05010-13", "g", "continuous", "closed"),
   "05010-14": lambda: extreme_value_choice("05010-14", "h", "differentiable", "closed"),
   "05010-15": lambda: extreme_value_choice("05010-15", "h", "differentiable", "open"),
   "05010-16": lambda: extreme_value_choice("05010-16", "h", "jump", "closed"),
   "05010-17": lambda: extreme_value_choice("05010-17", "g", "differentiable", "closed"),
   "05010-18": lambda: extreme_value_choice("05010-18", "h", "jump", "closed"),
   "05010-19": lambda: extreme_value_choice("05010-19", "g", "differentiable", "closed"),
   "05010-20": lambda: extreme_value_choice("05010-20", "f", "differentiable", "open"),
   "05010-21": lambda: extreme_value_choice("05010-21", "h", "differentiable", "closed"),
   "05011-00": lambda: open_box_largest_volume(48, 6),
   "05011-01": lambda: open_box_largest_volume(48, None),
   "05011-02": lambda: open_box_largest_volume(48, None),
   "05011-03": lambda: open_box_largest_volume(42, 2),
   "05011-04": lambda: open_box_largest_volume(42, None),
   "05011-05": lambda: open_box_largest_volume(48, 4),
   "05011-06": lambda: open_box_largest_volume(30, None),
   "05011-07": lambda: open_box_largest_volume(36, None),
   "05011-08": lambda: open_box_largest_volume(30, 2),
   "05011-09": lambda: open_box_largest_volume(42, 6),
   "05011-10": lambda: open_box_largest_volume(42, None),
   "05011-11": lambda: open_box_largest_volume(36, 3),
   "05011-12": lambda: open_box_largest_volume(30, 4),
   "05011-13": lambda: open_box_largest_volume(48, None),
   "05011-14": lambda: open_box_largest_volume(18, 2),
   "05011-15": lambda: open_box_largest_volume(36, 3),
   "05011-16": lambda: open_box_largest_volume(48, 6),
   "05011-17": lambda: open_box_largest_volume(12, 1),
   "05011-18": lambda: open_box_largest_volume(24, 2),
   "05011-19": lambda: open_box_largest_volume(36, None),
   "05011-20": lambda: open_box_largest_volume(42, None),
   "05011-21": lambda: open_box_largest_volume(24, None),
   "05012-00": lambda: horizontal_tangent_choice("05012-00", expression("-2*(5 - x)*(-x - 1)**2 + (y + 1)**2")),
   "05012-01": lambda: horizontal_tangent_choice("05012-01", expression("-(-x - 8)**2*(-x - 5) + (y - 3)**2")),
   "05012-02": lambda: horizontal_tangent_choice("05012-02", expression("y**2 - (7 - x)**2*(10 - x)")),
   "05012-03": lambda: horizontal_tangent_choice("05012-03", expression("y**2 - 4*(5 - x)**2*(8 - x)")),
   "05012-04": lambda: horizontal_tangent_choice("05012-04", expression("-9*(3 - x)**2*(6 - x) + (y - 9)**2")),
   "05013-00": lambda: second_derivative_test_choice("05013-00", expression("(-6*x - 24)*(x - 3)"), 3, 5, "f"),
   "05013-01": lambda: second_derivative_test_choice("05013-01", expression("(-6*x - 12)*(x - 2)"), 2, 3, "f"),
   "05013-02": lambda: second_derivative_test_choice("05013-02", derivative_of(expression("2*x**3 - 12*x**2 + 18*x")), 3, -4, "g"),
   "05013-03": lambda: second_derivative_test_choice("05013-03", expression("6*x*(x + 1)"), -1, -2, "g"),
   "05013-04": lambda: second_derivative_test_choice("05013-04", expression("(-6*x - 12)*(x - 3)"), 3, -1, "g"),
   "05013-05": lambda: second_derivative_test_choice("05013-05", derivative_of(expression("2*x**3 + 9*x**2 + 12*x + 4")), -2, 4, "f"),
   "05013-06": lambda: second_derivative_test_choice("05013-06", derivative_of(expression("-2*x**3 - 3*x**2 + 12*x + 3")), -2, 0, "h"),
   "05013-07": lambda: second_derivative_test_choice("05013-07", expression("(-6*x - 24)*(x - 4)"), 4, -1, "h"),
   "05013-08": lambda: second_derivative_test_choice("05013-08", expression("(x - 2)*(6*x + 24)"), -4, -3, "h"),
   "05013-09": lambda: second_derivative_test_choice("05013-09", derivative_of(expression("-2*x**3 - 3*x**2 + 72*x + 3")), 3, -2, "g"),
   "05013-10": lambda: second_derivative_test_choice("05013-10", expression("6*x*(x + 3)"), -3, 5, "h"),
   "05013-11": lambda: second_derivative_test_choice("05013-11", derivative_of(expression("2*x**3 - 3*x**2 - 72*x - 1")), 4, 2, "f"),
   "05013-12": lambda: second_derivative_test_choice("05013-12", derivative_of(expression("-2*x**3 - 3*x**2 + 12*x + 3")), -2, 5, "f"),
   "05013-13": lambda: second_derivative_test_choice("05013-13", derivative_of(expression("2*x**3 - 9*x**2 - 5")), 3, 1, "h"),
   "05013-14": lambda: second_derivative_test_choice("05013-14", derivative_of(expression("2*x**3 + 3*x**2 - 36*x")), 2, 5, "h"),
   "05013-15": lambda: second_derivative_test_choice("05013-15", expression("(-6*x - 24)*(x + 1)"), -4, 5, "g"),
   "05013-16": lambda: second_derivative_test_choice("05013-16", derivative_of(expression("2*x**3 - 9*x**2 - 24*x + 3")), -1, 3, "f"),
   "05013-17": lambda: second_derivative_test_choice("05013-17", expression("(x - 2)*(6*x + 12)"), -2, -5, "g"),
   "05013-18": lambda: second_derivative_test_choice("05013-18", derivative_of(expression("-2*x**3 - 21*x**2 - 72*x - 5")), -3, 5, "g"),
   "05013-19": lambda: second_derivative_test_choice("05013-19", expression("(-6*x - 24)*(x + 1)"), -1, -3, "h"),
   "05013-20": lambda: second_derivative_test_choice("05013-20", derivative_of(expression("-2*x**3 + 12*x**2 - 18*x - 3")), 1, -5, "g"),
   "05013-21": lambda: second_derivative_test_choice("05013-21", expression("(-6*x - 24)*(x + 3)"), -3, 2, "h"),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
