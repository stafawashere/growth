"""Answers to the unit 5 generated items in stems_C.json, worked from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. Only the
stems file and the shared recheck helpers were read, never a key, a worked solution, a template or
a candidate record. Each statement item's four choices are copied into CHOICES below, and its
formulation returns the one choice the mathematics makes true, or a list of every such choice when
there is not exactly one.
"""
import sympy
from sympy import Rational, exp

from tools.key_recheck import derivative, x

SIDE_STEP = Rational(1, 1000)


def choice_where(suffix, is_correct):
   matching = [choice for choice in CHOICES[suffix] if is_correct(choice)]
   has_single_match = len(matching) == 1

   if has_single_match:
      return matching[0]

   return matching


def joined(parts):
   if len(parts) == 1:
      return parts[0]

   return ", ".join(parts[:-1]) + " and " + parts[-1]


def mean_value_statement(suffix, values, left, right, target, defect, at):
   """defect is None when f is differentiable everywhere, "corner" when f is continuous but not
   differentiable at the point at, and "jump" when f is not continuous there."""
   average = Rational(values[right] - values[left], right - left)
   average_text = f"\\frac{{f({right}) - f({left})}}{{{right} - {left}}} = {sympy.latex(average)}"

   if average != target:
      return []

   breaks_differentiability = defect == "corner" and left < at < right
   breaks_continuity = defect == "jump" and left <= at <= right
   hypotheses_fail = breaks_differentiability or breaks_continuity
   failure_phrase = "is not differentiable" if breaks_differentiability else "is not continuous"

   def is_correct(choice):
      states_average = average_text in choice

      if hypotheses_fail:
         says_no = choice.startswith("No. Although")
         names_failure = f"f {failure_phrase} at" in choice
         withholds_theorem = "the Mean Value Theorem does not apply" in choice

         return states_average and says_no and names_failure and withholds_theorem

      says_yes = choice.startswith("Yes.")
      applies_theorem = "the Mean Value Theorem guarantees such a c" in choice
      rests_on_definedness = "defined at every point" in choice

      return states_average and says_yes and applies_theorem and not rests_on_definedness

   return choice_where(suffix, is_correct)


def mean_value_point(function, left, right):
   average = (function.subs(x, right) - function.subs(x, left)) / (right - left)
   solutions = sympy.solve(sympy.Eq(derivative(function, x), average), x)
   inside = [point for point in solutions if point.is_real and left < point < right]
   has_single_point = len(inside) == 1

   if has_single_point:
      return inside[0]

   return inside


def sign_word(value):
   return "positive" if value > 0 else "negative"


def extremum_statement(suffix, slope, at):
   if sympy.simplify(slope.subs(x, at)) != 0:
      raise ValueError(f"f' is not 0 at x = {at}")

   left_value = slope.subs(x, at - SIDE_STEP)
   right_value = slope.subs(x, at + SIDE_STEP)
   left_sign = sign_word(left_value)
   right_sign = sign_word(right_value)
   changes_sign = left_sign != right_sign

   if changes_sign:
      kind = "minimum" if left_sign == "negative" else "maximum"
      expected = [
         f"f has a relative {kind} at x = {at}, because f' changes from {left_sign} to {right_sign} at x = {at}.",
      ]
   else:
      neither = f"f has neither a relative minimum nor a relative maximum at x = {at}, because"
      expected = [
         f"{neither} f' does not change sign at x = {at}.",
         f"{neither} f' is {left_sign} on both sides of x = {at}.",
      ]

   return choice_where(suffix, lambda choice: choice in expected)


def segment_slopes(vertices):
   return [
      (Rational(start[0]), Rational(end[0]), Rational(end[1] - start[1], end[0] - start[0]))
      for start, end in zip(vertices, vertices[1:])
   ]


def interval_text(left, right):
   return f"\\( \\left({sympy.latex(left)}, {sympy.latex(right)}\\right) \\)"


def concavity_statement(suffix, concavity, vertices):
   """f is concave up where the graph of f' rises and concave down where it falls."""
   wants_rising = concavity == "up"
   runs = []

   for left, right, slope in segment_slopes(vertices):
      if slope == 0:
         raise ValueError("a flat segment of f' needs its own reading")

      is_wanted = (slope > 0) == wants_rising
      continues_run = is_wanted and runs and runs[-1][1] == left

      if continues_run:
         runs[-1][1] = right
      elif is_wanted:
         runs.append([left, right])

   trend = "increasing" if wants_rising else "decreasing"
   intervals = joined([interval_text(left, right) for left, right in runs])
   expected = f"The graph of f is concave {concavity} on {intervals}, because f' is {trend} there."

   return choice_where(suffix, lambda choice: choice == expected)


def inflection_statement(suffix, vertices):
   """Inflection points of f are where f' switches between rising and falling."""
   slopes = segment_slopes(vertices)
   switch_points = []

   for (_, joint, before), (_, _, after) in zip(slopes, slopes[1:]):
      if before == 0 or after == 0:
         raise ValueError("a flat segment of f' needs its own reading")

      switches = (before > 0) != (after > 0)

      if switches:
         switch_points.append(joint)

   points = joined([f"\\( x = {sympy.latex(point)} \\)" for point in switch_points])
   opening = f"The graph of f has points of inflection at {points}, because"
   expected = [
      f"{opening} f' changes between increasing and decreasing at each of these values.",
      f"{opening} f'' changes sign at each of these values.",
   ]

   return choice_where(suffix, lambda choice: choice in expected)


def absolute_extreme(function, kind, left, right):
   stationary = sympy.solve(derivative(function, x), x)
   inside = [point for point in stationary if point.is_real and left < point < right]
   candidates = [left, right] + inside
   values = [sympy.simplify(function.subs(x, point)) for point in candidates]

   if kind == "maximum":
      return max(values)

   return min(values)


CHOICES = {
   "05001-00": [
      "No. Although \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (1, 9) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[1, 9\\right] \\), \\( \\frac{f(1) - f(9)}{9 - 1} = \\frac{1}{4} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[1, 9\\right] \\).",
      "Yes. Since \\( \\frac{f(9) - f(1)}{9 - 1} = - \\frac{1}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 9) \\).",
   ],
   "05001-01": [
      "No. Although \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), f is not differentiable at \\( x = 3 \\), which lies in \\( (0, 6) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[0, 6\\right] \\), \\( \\frac{f(0) - f(6)}{6 - 0} = - \\frac{3}{2} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = \\frac{3}{2} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 6) \\).",
   ],
   "05001-02": [
      "No. Although \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), f is not differentiable at \\( x = 7 \\), which lies in \\( (4, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[4, 10\\right] \\), \\( \\frac{f(4) - f(10)}{10 - 4} = 3 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[4, 10\\right] \\).",
      "Yes. Since \\( \\frac{f(10) - f(4)}{10 - 4} = -3 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 10) \\).",
   ],
   "05001-03": [
      "No. Although \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), f is not differentiable at \\( x = \\frac{9}{2} \\), which lies in \\( (2, 7) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[2, 7\\right] \\), \\( \\frac{f(2) - f(7)}{7 - 2} = - \\frac{19}{5} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[2, 7\\right] \\).",
      "Yes. Since \\( \\frac{f(7) - f(2)}{7 - 2} = \\frac{19}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 7) \\).",
   ],
   "05001-04": [
      "No. Although \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), f is not continuous at \\( x = 8 \\), which lies in \\( \\left[7, 9\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[7, 9\\right] \\), \\( \\frac{f(7) - f(9)}{9 - 7} = 4 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[7, 9\\right] \\).",
      "Yes. Since \\( \\frac{f(9) - f(7)}{9 - 7} = -4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (7, 9) \\).",
   ],
   "05001-05": [
      "No. Although \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), f is not differentiable at \\( x = 8 \\), which lies in \\( (4, 12) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[4, 12\\right] \\), \\( \\frac{f(4) - f(12)}{12 - 4} = \\frac{19}{8} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[4, 12\\right] \\).",
      "Yes. Since \\( \\frac{f(12) - f(4)}{12 - 4} = - \\frac{19}{8} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 12) \\).",
   ],
   "05001-06": [
      "No. Although \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), f is not continuous at \\( x = \\frac{9}{2} \\), which lies in \\( \\left[0, 9\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[0, 9\\right] \\), \\( \\frac{f(0) - f(9)}{9 - 0} = \\frac{2}{9} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 9\\right] \\).",
      "Yes. Since \\( \\frac{f(9) - f(0)}{9 - 0} = - \\frac{2}{9} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 9) \\).",
   ],
   "05001-07": [
      "No. Although \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), f is not differentiable at \\( x = \\frac{11}{2} \\), which lies in \\( (3, 8) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[3, 8\\right] \\), \\( \\frac{f(3) - f(8)}{8 - 3} = - \\frac{1}{5} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 8\\right] \\).",
      "Yes. Since \\( \\frac{f(8) - f(3)}{8 - 3} = \\frac{1}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 8) \\).",
   ],
   "05001-08": [
      "No. Although \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (0, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[0, 10\\right] \\), \\( \\frac{f(0) - f(10)}{10 - 0} = - \\frac{1}{5} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 10\\right] \\).",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = \\frac{1}{5} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 10) \\).",
   ],
   "05001-09": [
      "No. Although \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), f is not continuous at \\( x = \\frac{13}{2} \\), which lies in \\( \\left[1, 12\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[1, 12\\right] \\), \\( \\frac{f(1) - f(12)}{12 - 1} = - \\frac{24}{11} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[1, 12\\right] \\).",
      "Yes. Since \\( \\frac{f(12) - f(1)}{12 - 1} = \\frac{24}{11} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 12) \\).",
   ],
   "05001-10": [
      "No. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), but \\( \\frac{f(6) - f(12)}{12 - 6} = -1 \\), so the Mean Value Theorem does not give such a c.",
      "Yes. Since f is defined at every point of \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), the Mean Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), so the Intermediate Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[6, 12\\right] \\), and \\( \\frac{f(12) - f(6)}{12 - 6} = 1 \\), so the Mean Value Theorem guarantees such a c.",
   ],
   "05001-11": [
      "No. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), but \\( \\frac{f(2) - f(10)}{10 - 2} = - \\frac{5}{4} \\), so the Mean Value Theorem does not give such a c.",
      "Yes. Since f is defined at every point of \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), the Mean Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), so the Intermediate Value Theorem guarantees such a c.",
      "Yes. Since f is differentiable, it is continuous on \\( \\left[2, 10\\right] \\), and \\( \\frac{f(10) - f(2)}{10 - 2} = \\frac{5}{4} \\), so the Mean Value Theorem guarantees such a c.",
   ],
   "05001-12": [
      "No. Although \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), f is not continuous at \\( x = \\frac{9}{2} \\), which lies in \\( \\left[3, 6\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[3, 6\\right] \\), \\( \\frac{f(3) - f(6)}{6 - 3} = -4 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(3)}{6 - 3} = 4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 6) \\).",
   ],
   "05001-13": [
      "No. Although \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), f is not differentiable at \\( x = \\frac{15}{2} \\), which lies in \\( (3, 12) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[3, 12\\right] \\), \\( \\frac{f(3) - f(12)}{12 - 3} = \\frac{1}{9} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 12\\right] \\).",
      "Yes. Since \\( \\frac{f(12) - f(3)}{12 - 3} = - \\frac{1}{9} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 12) \\).",
   ],
   "05001-14": [
      "No. Although \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (2, 8) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[2, 8\\right] \\), \\( \\frac{f(2) - f(8)}{8 - 2} = -1 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[2, 8\\right] \\).",
      "Yes. Since \\( \\frac{f(8) - f(2)}{8 - 2} = 1 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 8) \\).",
   ],
   "05001-15": [
      "No. Although \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), f is not continuous at \\( x = 4 \\), which lies in \\( \\left[1, 7\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[1, 7\\right] \\), \\( \\frac{f(1) - f(7)}{7 - 1} = -4 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[1, 7\\right] \\).",
      "Yes. Since \\( \\frac{f(7) - f(1)}{7 - 1} = 4 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (1, 7) \\).",
   ],
   "05001-16": [
      "No. Although \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), f is not differentiable at \\( x = 5 \\), which lies in \\( (0, 10) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[0, 10\\right] \\), \\( \\frac{f(0) - f(10)}{10 - 0} = 2 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 10\\right] \\).",
      "Yes. Since \\( \\frac{f(10) - f(0)}{10 - 0} = -2 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 10) \\).",
   ],
   "05001-17": [
      "No. Although \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), f is not differentiable at \\( x = 3 \\), which lies in \\( (0, 6) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[0, 6\\right] \\), \\( \\frac{f(0) - f(6)}{6 - 0} = -2 \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[0, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(0)}{6 - 0} = 2 \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (0, 6) \\).",
   ],
   "05001-18": [
      "No. Although \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), f is not differentiable at \\( x = \\frac{19}{2} \\), which lies in \\( (8, 11) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[8, 11\\right] \\), \\( \\frac{f(8) - f(11)}{11 - 8} = \\frac{8}{3} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[8, 11\\right] \\).",
      "Yes. Since \\( \\frac{f(11) - f(8)}{11 - 8} = - \\frac{8}{3} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (8, 11) \\).",
   ],
   "05001-19": [
      "No. Although \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), f is not differentiable at \\( x = 4 \\), which lies in \\( (3, 5) \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[3, 5\\right] \\), \\( \\frac{f(3) - f(5)}{5 - 3} = - \\frac{15}{2} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[3, 5\\right] \\).",
      "Yes. Since \\( \\frac{f(5) - f(3)}{5 - 3} = \\frac{15}{2} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (3, 5) \\).",
   ],
   "05001-20": [
      "No. Although \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), f is not continuous at \\( x = 4 \\), which lies in \\( \\left[2, 6\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[2, 6\\right] \\), \\( \\frac{f(2) - f(6)}{6 - 2} = \\frac{15}{4} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[2, 6\\right] \\).",
      "Yes. Since \\( \\frac{f(6) - f(2)}{6 - 2} = - \\frac{15}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (2, 6) \\).",
   ],
   "05001-21": [
      "No. Although \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), f is not continuous at \\( x = 6 \\), which lies in \\( \\left[4, 8\\right] \\), so the Mean Value Theorem does not apply and such a c is not guaranteed.",
      "No. Although f is defined on \\( \\left[4, 8\\right] \\), \\( \\frac{f(4) - f(8)}{8 - 4} = - \\frac{3}{4} \\), which is not the named value, so such a c is not guaranteed.",
      "Yes. Since \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), the Intermediate Value Theorem guarantees such a c, with f taken to be continuous on \\( \\left[4, 8\\right] \\).",
      "Yes. Since \\( \\frac{f(8) - f(4)}{8 - 4} = \\frac{3}{4} \\), the Mean Value Theorem guarantees such a c, with f taken to be differentiable on \\( (4, 8) \\).",
   ],
   "05003-00": [
      "f has a relative maximum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from negative to positive at x = 2.",
      "f has a relative minimum at x = 2, because it changes from negative to positive at x = 2.",
      "f has a relative minimum at x = 2, because the function changes from negative to positive at x = 2.",
   ],
   "05003-01": [
      "f has a relative maximum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has a relative maximum at x = -3, because it changes from positive to negative at x = -3.",
      "f has a relative maximum at x = -3, because the function changes from positive to negative at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from positive to negative at x = -3.",
   ],
   "05003-02": [
      "f has a relative maximum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because it changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because the function changes from negative to positive at x = 0.",
   ],
   "05003-03": [
      "f has a relative maximum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has a relative maximum at x = 2, because it changes from positive to negative at x = 2.",
      "f has a relative maximum at x = 2, because the function changes from positive to negative at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from positive to negative at x = 2.",
   ],
   "05003-04": [
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative maximum at x = 1, because it changes from positive to negative at x = 1.",
      "f has a relative maximum at x = 1, because the function changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from positive to negative at x = 1.",
   ],
   "05003-05": [
      "f has a relative maximum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative minimum at x = -1, because f' changes from negative to positive at x = -1.",
      "f has a relative minimum at x = -1, because it changes from negative to positive at x = -1.",
      "f has a relative minimum at x = -1, because the function changes from negative to positive at x = -1.",
   ],
   "05003-06": [
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' is positive on both sides of x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because it does not change sign at x = 2.",
   ],
   "05003-07": [
      "f has a relative maximum at x = -2, because f' changes from positive to negative at x = -2.",
      "f has a relative maximum at x = -2, because it changes from positive to negative at x = -2.",
      "f has a relative maximum at x = -2, because the function changes from positive to negative at x = -2.",
      "f has a relative minimum at x = -2, because f' changes from positive to negative at x = -2.",
   ],
   "05003-08": [
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative maximum at x = 1, because it changes from positive to negative at x = 1.",
      "f has a relative maximum at x = 1, because the function changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from positive to negative at x = 1.",
   ],
   "05003-09": [
      "f has a relative maximum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has a relative minimum at x = 4, because f' changes from negative to positive at x = 4.",
      "f has a relative minimum at x = 4, because it changes from negative to positive at x = 4.",
      "f has a relative minimum at x = 4, because the function changes from negative to positive at x = 4.",
   ],
   "05003-10": [
      "f has a relative maximum at x = 2, because f' changes from positive to negative at x = 2.",
      "f has a relative maximum at x = 2, because it changes from positive to negative at x = 2.",
      "f has a relative maximum at x = 2, because the function changes from positive to negative at x = 2.",
      "f has a relative minimum at x = 2, because f' changes from positive to negative at x = 2.",
   ],
   "05003-11": [
      "f has a relative maximum at x = 1, because f' changes from positive to negative at x = 1.",
      "f has a relative maximum at x = 1, because it changes from positive to negative at x = 1.",
      "f has a relative maximum at x = 1, because the function changes from positive to negative at x = 1.",
      "f has a relative minimum at x = 1, because f' changes from positive to negative at x = 1.",
   ],
   "05003-12": [
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' is positive on both sides of x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because it does not change sign at x = 2.",
   ],
   "05003-13": [
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' is positive on both sides of x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because it does not change sign at x = 2.",
   ],
   "05003-14": [
      "f has a relative maximum at x = 0, because f' changes from positive to negative at x = 0.",
      "f has a relative maximum at x = 0, because it changes from positive to negative at x = 0.",
      "f has a relative maximum at x = 0, because the function changes from positive to negative at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from positive to negative at x = 0.",
   ],
   "05003-15": [
      "f has a relative minimum at x = 4, because f' is equal to 0 at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' does not change sign at x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because f' is positive on both sides of x = 4.",
      "f has neither a relative minimum nor a relative maximum at x = 4, because it does not change sign at x = 4.",
   ],
   "05003-16": [
      "f has a relative maximum at x = -3, because f' changes from negative to positive at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from negative to positive at x = -3.",
      "f has a relative minimum at x = -3, because it changes from negative to positive at x = -3.",
      "f has a relative minimum at x = -3, because the function changes from negative to positive at x = -3.",
   ],
   "05003-17": [
      "f has a relative maximum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because f' changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because it changes from negative to positive at x = 0.",
      "f has a relative minimum at x = 0, because the function changes from negative to positive at x = 0.",
   ],
   "05003-18": [
      "f has a relative minimum at x = -2, because f' is equal to 0 at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' does not change sign at x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because f' is positive on both sides of x = -2.",
      "f has neither a relative minimum nor a relative maximum at x = -2, because it does not change sign at x = -2.",
   ],
   "05003-19": [
      "f has a relative minimum at x = 2, because f' is equal to 0 at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' does not change sign at x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because f' is positive on both sides of x = 2.",
      "f has neither a relative minimum nor a relative maximum at x = 2, because it does not change sign at x = 2.",
   ],
   "05003-20": [
      "f has a relative maximum at x = -3, because f' changes from positive to negative at x = -3.",
      "f has a relative maximum at x = -3, because it changes from positive to negative at x = -3.",
      "f has a relative maximum at x = -3, because the function changes from positive to negative at x = -3.",
      "f has a relative minimum at x = -3, because f' changes from positive to negative at x = -3.",
   ],
   "05003-21": [
      "f has a relative maximum at x = 3, because f' changes from positive to negative at x = 3.",
      "f has a relative maximum at x = 3, because it changes from positive to negative at x = 3.",
      "f has a relative maximum at x = 3, because the function changes from positive to negative at x = 3.",
      "f has a relative minimum at x = 3, because f' changes from positive to negative at x = 3.",
   ],
   "05004-00": [
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(2, 5\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(\\frac{7}{2}, \\frac{23}{4}\\right) \\), because f' is negative there.",
   ],
   "05004-01": [
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(1, \\frac{9}{4}\\right) \\) and \\( \\left(\\frac{22}{5}, \\frac{23}{4}\\right) \\), because f' is positive there.",
      "The graph of f is concave up on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because it is increasing there.",
   ],
   "05004-02": [
      "The graph of f is concave down on \\( \\left(0, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, \\frac{3}{4}\\right) \\), because f' is negative there.",
      "The graph of f is concave down on \\( \\left(1, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(1, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
   ],
   "05004-03": [
      "The graph of f is concave up on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{22}{5}, \\frac{28}{5}\\right) \\), because f' is positive there.",
   ],
   "05004-04": [
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(\\frac{13}{5}, \\frac{17}{4}\\right) \\), because f' is negative there.",
   ],
   "05004-05": [
      "The graph of f is concave up on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, \\frac{1}{4}\\right) \\) and \\( \\left(\\frac{11}{2}, 6\\right) \\), because f' is positive there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because it is increasing there.",
   ],
   "05004-06": [
      "The graph of f is concave down on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 4\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(\\frac{4}{3}, 3\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is negative there.",
   ],
   "05004-07": [
      "The graph of f is concave down on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(2, \\frac{7}{2}\\right) \\) and \\( \\left(\\frac{19}{4}, 6\\right) \\), because f' is negative there.",
   ],
   "05004-08": [
      "The graph of f is concave up on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, \\frac{1}{4}\\right) \\) and \\( \\left(2, \\frac{10}{3}\\right) \\), because f' is positive there.",
      "The graph of f is concave up on \\( \\left(1, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because it is increasing there.",
   ],
   "05004-09": [
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(\\frac{27}{5}, 6\\right) \\), because f' is negative there.",
   ],
   "05004-10": [
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\) and \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, \\frac{3}{5}\\right) \\) and \\( \\left(\\frac{11}{3}, 6\\right) \\), because f' is negative there.",
      "The graph of f is concave down on \\( \\left(2, 5\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(2, 5\\right) \\), because it is decreasing there.",
   ],
   "05004-11": [
      "The graph of f is concave down on \\( \\left(0, 2\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 2\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(\\frac{7}{5}, \\frac{7}{2}\\right) \\) and \\( \\left(\\frac{17}{3}, 6\\right) \\), because f' is negative there.",
   ],
   "05004-12": [
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{1}{4}, \\frac{3}{2}\\right) \\) and \\( \\left(\\frac{22}{5}, \\frac{11}{2}\\right) \\), because f' is positive there.",
   ],
   "05004-13": [
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\) and \\( \\left(3, 6\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, \\frac{7}{4}\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is positive there.",
   ],
   "05004-14": [
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{2}{5}, \\frac{18}{5}\\right) \\) and \\( \\left(\\frac{21}{4}, 6\\right) \\), because f' is positive there.",
   ],
   "05004-15": [
      "The graph of f is concave down on \\( \\left(0, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, \\frac{1}{4}\\right) \\), \\( \\left(\\frac{9}{4}, \\frac{14}{3}\\right) \\) and \\( \\left(\\frac{11}{2}, 6\\right) \\), because f' is negative there.",
      "The graph of f is concave down on \\( \\left(1, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(1, 3\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
   ],
   "05004-16": [
      "The graph of f is concave up on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 4\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{7}{2}, \\frac{11}{2}\\right) \\), because f' is positive there.",
   ],
   "05004-17": [
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 3\\right) \\) and \\( \\left(4, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{1}{2}, \\frac{8}{5}\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is positive there.",
   ],
   "05004-18": [
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 2\\right) \\), \\( \\left(3, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, 3\\right) \\) and \\( \\left(3, \\frac{9}{2}\\right) \\), because f' is negative there.",
   ],
   "05004-19": [
      "The graph of f is concave up on \\( \\left(0, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(1, 2\\right) \\) and \\( \\left(3, 5\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{3}{2}, \\frac{9}{4}\\right) \\), because f' is positive there.",
   ],
   "05004-20": [
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 1\\right) \\), \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because it is increasing there.",
      "The graph of f is concave up on \\( \\left(0, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is increasing there.",
      "The graph of f is concave up on \\( \\left(\\frac{11}{3}, \\frac{13}{3}\\right) \\), because f' is positive there.",
   ],
   "05004-21": [
      "The graph of f is concave down on \\( \\left(0, 1\\right) \\), \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(0, \\frac{2}{3}\\right) \\) and \\( \\left(3, \\frac{9}{2}\\right) \\), because f' is negative there.",
      "The graph of f is concave down on \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because f' is decreasing there.",
      "The graph of f is concave down on \\( \\left(2, 4\\right) \\) and \\( \\left(5, 6\\right) \\), because it is decreasing there.",
   ],
   "05005-00": [
      "The graph of f has points of inflection at \\( x = 2 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\) and \\( x = 4 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{10}{3} \\) and \\( x = \\frac{14}{3} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-01": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{3}{4} \\), \\( x = \\frac{8}{3} \\), \\( x = \\frac{7}{2} \\) and \\( x = \\frac{28}{5} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-02": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = \\frac{5}{2} \\), \\( x = \\frac{17}{4} \\) and \\( x = \\frac{23}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-03": [
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 3 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\) and \\( x = \\frac{14}{3} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-04": [
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 3 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 3 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 4 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{9}{4} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-05": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{1}{2} \\), \\( x = 2 \\) and \\( x = 4 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-06": [
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{1}{2} \\) and \\( x = \\frac{5}{2} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-07": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = \\frac{10}{3} \\), \\( x = \\frac{22}{5} \\) and \\( x = \\frac{23}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-08": [
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 4 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{3}{5} \\), \\( x = \\frac{5}{2} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-09": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{2}{5} \\), \\( x = 2 \\), \\( x = \\frac{11}{3} \\) and \\( x = \\frac{17}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-10": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{7}{5} \\), \\( x = \\frac{5}{2} \\) and \\( x = 4 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-11": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{2}{3} \\), \\( x = \\frac{9}{2} \\) and \\( x = \\frac{17}{3} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-12": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{2}{5} \\), \\( x = \\frac{3}{2} \\), \\( x = \\frac{13}{4} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-13": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{3}{4} \\), \\( x = \\frac{3}{2} \\), \\( x = 3 \\) and \\( x = \\frac{11}{2} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-14": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 4 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{2}{3} \\), \\( x = \\frac{3}{2} \\), \\( x = 3 \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-15": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 4 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 4 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{3}{4} \\), \\( x = \\frac{5}{2} \\), \\( x = \\frac{7}{2} \\) and \\( x = \\frac{19}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-16": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 4 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{10}{3} \\) and \\( x = \\frac{22}{5} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-17": [
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 2 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\) and \\( x = 2 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{7}{5} \\) and \\( x = 5 \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-18": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{7}{5} \\), \\( x = \\frac{5}{2} \\) and \\( x = \\frac{15}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-19": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{1}{4} \\), \\( x = \\frac{12}{5} \\), \\( x = \\frac{7}{2} \\) and \\( x = \\frac{23}{5} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-20": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\), \\( x = 4 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{1}{2} \\), \\( x = \\frac{8}{5} \\), \\( x = \\frac{12}{5} \\) and \\( x = \\frac{17}{4} \\), because f' is equal to 0 at each of these values.",
   ],
   "05005-21": [
      "The graph of f has points of inflection at \\( x = 1 \\), \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because the slope of the graph of f' changes at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f' changes between increasing and decreasing at each of these values.",
      "The graph of f has points of inflection at \\( x = 2 \\), \\( x = 3 \\) and \\( x = 5 \\), because f'' changes sign at each of these values.",
      "The graph of f has points of inflection at \\( x = \\frac{13}{5} \\), \\( x = 4 \\) and \\( x = \\frac{11}{2} \\), because f' is equal to 0 at each of these values.",
   ],
}


BY_SUFFIX = {
   "05001-00": lambda: mean_value_statement("05001-00", {1: 12, 2: -5, 4: 19, 9: 10, 10: -9}, 1, 9, Rational(-1, 4), defect="corner", at=5),
   "05001-01": lambda: mean_value_statement("05001-01", {0: 9, 1: 0, 3: 14, 6: 18, 8: 18}, 0, 6, Rational(3, 2), defect="corner", at=3),
   "05001-02": lambda: mean_value_statement("05001-02", {3: 17, 4: 20, 5: -1, 7: 3, 10: 2}, 4, 10, -3, defect="corner", at=7),
   "05001-03": lambda: mean_value_statement("05001-03", {0: 20, 2: -1, 4: 20, 7: 18, 9: 18}, 2, 7, Rational(19, 5), defect="corner", at=Rational(9, 2)),
   "05001-04": lambda: mean_value_statement("05001-04", {2: -5, 6: -3, 7: 17, 8: 2, 9: 9}, 7, 9, -4, defect="jump", at=8),
   "05001-05": lambda: mean_value_statement("05001-05", {3: 7, 4: 17, 5: 18, 7: 8, 12: -2}, 4, 12, Rational(-19, 8), defect="corner", at=8),
   "05001-06": lambda: mean_value_statement("05001-06", {0: 15, 6: -8, 8: -9, 9: 13, 10: 17}, 0, 9, Rational(-2, 9), defect="jump", at=Rational(9, 2)),
   "05001-07": lambda: mean_value_statement("05001-07", {2: 6, 3: 2, 5: 5, 7: -1, 8: 3}, 3, 8, Rational(1, 5), defect="corner", at=Rational(11, 2)),
   "05001-08": lambda: mean_value_statement("05001-08", {0: 10, 1: 17, 3: 20, 10: 12, 11: -9}, 0, 10, Rational(1, 5), defect="corner", at=5),
   "05001-09": lambda: mean_value_statement("05001-09", {1: -8, 5: -8, 10: 14, 11: 13, 12: 16}, 1, 12, Rational(24, 11), defect="jump", at=Rational(13, 2)),
   "05001-10": lambda: mean_value_statement("05001-10", {0: 13, 6: 10, 9: 1, 10: 13, 12: 16}, 6, 12, 1, defect=None, at=None),
   "05001-11": lambda: mean_value_statement("05001-11", {1: 3, 2: 9, 3: -8, 5: 16, 10: 19}, 2, 10, Rational(5, 4), defect=None, at=None),
   "05001-12": lambda: mean_value_statement("05001-12", {3: -8, 4: 19, 6: 4, 7: 13, 10: 14}, 3, 6, 4, defect="jump", at=Rational(9, 2)),
   "05001-13": lambda: mean_value_statement("05001-13", {1: -8, 3: 7, 5: 5, 9: 17, 12: 6}, 3, 12, Rational(-1, 9), defect="corner", at=Rational(15, 2)),
   "05001-14": lambda: mean_value_statement("05001-14", {1: 12, 2: 6, 4: -7, 6: -7, 8: 12}, 2, 8, 1, defect="corner", at=5),
   "05001-15": lambda: mean_value_statement("05001-15", {1: -4, 4: 7, 6: 16, 7: 20, 11: 0}, 1, 7, 4, defect="jump", at=4),
   "05001-16": lambda: mean_value_statement("05001-16", {0: 20, 1: 6, 6: 18, 9: -3, 10: 0}, 0, 10, -2, defect="corner", at=5),
   "05001-17": lambda: mean_value_statement("05001-17", {0: 7, 1: -7, 4: -8, 6: 19, 10: 4}, 0, 6, 2, defect="corner", at=3),
   "05001-18": lambda: mean_value_statement("05001-18", {3: 5, 6: 12, 8: 5, 9: 9, 11: -3}, 8, 11, Rational(-8, 3), defect="corner", at=Rational(19, 2)),
   "05001-19": lambda: mean_value_statement("05001-19", {3: -8, 4: 2, 5: 7, 10: 9, 12: 7}, 3, 5, Rational(15, 2), defect="corner", at=4),
   "05001-20": lambda: mean_value_statement("05001-20", {2: 14, 5: 6, 6: -1, 8: -3, 11: 7}, 2, 6, Rational(-15, 4), defect="jump", at=4),
   "05001-21": lambda: mean_value_statement("05001-21", {0: -8, 2: 3, 4: 0, 7: -7, 8: 3}, 4, 8, Rational(3, 4), defect="jump", at=6),
   "05002-00": lambda: mean_value_point(2*x**3 + 6*x + 12, 0, 2),
   "05002-01": lambda: mean_value_point(2*x**3 + x + 9, 0, 4),
   "05002-02": lambda: mean_value_point(3*x**3 + 5*x + 12, 1, 2),
   "05002-03": lambda: mean_value_point(x**3 + 4*x + 12, 3, 6),
   "05002-04": lambda: mean_value_point(2*x**3 + 4*x + 2, 1, 2),
   "05002-05": lambda: mean_value_point(x**3 + 3*x + 7, 1, 4),
   "05002-06": lambda: mean_value_point(2*x**3 + 2*x + 3, 0, 4),
   "05002-07": lambda: mean_value_point(2*x**3 + 2*x, 2, 6),
   "05002-08": lambda: mean_value_point(3*x**3 + 3, 3, 5),
   "05002-09": lambda: mean_value_point(3*x**3 + 2*x + 10, 1, 4),
   "05002-10": lambda: mean_value_point(3*x**3 + 3*x + 7, 1, 3),
   "05002-11": lambda: mean_value_point(3*x**3 + 2*x + 3, 2, 4),
   "05002-12": lambda: mean_value_point(x**3 + 3*x + 5, 2, 3),
   "05002-13": lambda: mean_value_point(3*x**3 + 3*x + 9, 2, 3),
   "05002-14": lambda: mean_value_point(2*x**3 + 12, 1, 2),
   "05002-15": lambda: mean_value_point(3*x**3 + 5*x + 6, 0, 4),
   "05002-16": lambda: mean_value_point(2*x**3 + 8, 0, 4),
   "05002-17": lambda: mean_value_point(3*x**3 + 5*x + 3, 0, 3),
   "05002-18": lambda: mean_value_point(3*x**3 + 6*x + 3, 1, 5),
   "05002-19": lambda: mean_value_point(2*x**3 + 3, 0, 3),
   "05002-20": lambda: mean_value_point(3*x**3 + x + 1, 1, 5),
   "05002-21": lambda: mean_value_point(2*x**3 + 5*x + 12, 0, 4),
   "05003-00": lambda: extremum_statement("05003-00", (x + 4)*(4*x - 8)*(x**2 + 1), 2),
   "05003-01": lambda: extremum_statement("05003-01", (-2*x - 6)*(x + 4)*exp(x), -3),
   "05003-02": lambda: extremum_statement("05003-02", -3*x*(x - 2), 0),
   "05003-03": lambda: extremum_statement("05003-03", (6 - 3*x)*(x + 2)*(x**2 + 1), 2),
   "05003-04": lambda: extremum_statement("05003-04", -x*(x - 1)*exp(x), 1),
   "05003-05": lambda: extremum_statement("05003-05", (x + 4)*(4*x + 4)*(x**2 + 1), -1),
   "05003-06": lambda: extremum_statement("05003-06", 4*(x - 2)**2*(x + 1)*exp(x), 2),
   "05003-07": lambda: extremum_statement("05003-07", (-4*x - 8)*(x + 5)*(x**2 + 1), -2),
   "05003-08": lambda: extremum_statement("05003-08", (1 - x)*(x + 1)*(x**2 + 1), 1),
   "05003-09": lambda: extremum_statement("05003-09", (16 - 4*x)*(x - 5)*(x**2 + 1), 4),
   "05003-10": lambda: extremum_statement("05003-10", (x - 4)*(2*x - 4)*exp(x), 2),
   "05003-11": lambda: extremum_statement("05003-11", (x - 6)*(x - 1)*(x**2 + 1), 1),
   "05003-12": lambda: extremum_statement("05003-12", (x - 2)**2*(x + 5)*exp(x), 2),
   "05003-13": lambda: extremum_statement("05003-13", 4*x*(x - 2)**2, 2),
   "05003-14": lambda: extremum_statement("05003-14", 2*x*(x - 3)*exp(x), 0),
   "05003-15": lambda: extremum_statement("05003-15", 2*(x - 4)**2*(x - 3)*(x**2 + 1), 4),
   "05003-16": lambda: extremum_statement("05003-16", (x + 4)*(2*x + 6), -3),
   "05003-17": lambda: extremum_statement("05003-17", 4*x*(x + 4)*(x**2 + 1), 0),
   "05003-18": lambda: extremum_statement("05003-18", -(x - 3)*(x + 2)**2*(x**2 + 1), -2),
   "05003-19": lambda: extremum_statement("05003-19", 4*(x - 2)**2*(x + 5)*exp(x), 2),
   "05003-20": lambda: extremum_statement("05003-20", (x - 3)*(2*x + 6), -3),
   "05003-21": lambda: extremum_statement("05003-21", (3 - x)*(x - 2)*exp(x), 3),
   "05004-00": lambda: concavity_statement("05004-00", "down", [(0, 1), (1, 2), (2, 3), (3, 2), (4, -2), (5, -3), (6, 1)]),
   "05004-01": lambda: concavity_statement("05004-01", "up", [(0, 2), (1, 0), (2, 1), (3, -3), (4, -2), (5, 3), (6, -1)]),
   "05004-02": lambda: concavity_statement("05004-02", "down", [(0, -3), (1, 1), (2, 0), (3, 3), (4, 2), (5, 3), (6, 1)]),
   "05004-03": lambda: concavity_statement("05004-03", "up", [(0, 0), (1, -3), (2, -1), (3, -3), (4, -2), (5, 3), (6, -2)]),
   "05004-04": lambda: concavity_statement("05004-04", "down", [(0, 3), (1, 1), (2, 3), (3, -2), (4, -1), (5, 3), (6, 1)]),
   "05004-05": lambda: concavity_statement("05004-05", "up", [(0, 1), (1, -3), (2, -2), (3, -3), (4, -2), (5, -1), (6, 1)]),
   "05004-06": lambda: concavity_statement("05004-06", "down", [(0, 3), (1, 1), (2, -2), (3, 0), (4, -3), (5, 0), (6, 3)]),
   "05004-07": lambda: concavity_statement("05004-07", "down", [(0, 2), (1, 1), (2, 0), (3, -3), (4, 3), (5, -1), (6, -3)]),
   "05004-08": lambda: concavity_statement("05004-08", "up", [(0, 1), (1, -3), (2, 0), (3, 1), (4, -2), (5, -3), (6, -1)]),
   "05004-09": lambda: concavity_statement("05004-09", "down", [(0, 0), (1, 1), (2, 2), (3, 3), (4, 1), (5, 2), (6, -3)]),
   "05004-10": lambda: concavity_statement("05004-10", "down", [(0, -3), (1, 2), (2, 3), (3, 2), (4, -1), (5, -3), (6, 0)]),
   "05004-11": lambda: concavity_statement("05004-11", "down", [(0, 3), (1, 2), (2, -3), (3, -1), (4, 1), (5, 2), (6, -1)]),
   "05004-12": lambda: concavity_statement("05004-12", "up", [(0, -1), (1, 3), (2, -3), (3, -1), (4, -2), (5, 3), (6, -3)]),
   "05004-13": lambda: concavity_statement("05004-13", "up", [(0, 2), (1, 3), (2, -1), (3, -3), (4, -2), (5, 0), (6, 3)]),
   "05004-14": lambda: concavity_statement("05004-14", "up", [(0, -2), (1, 3), (2, 1), (3, 3), (4, -2), (5, -1), (6, 3)]),
   "05004-15": lambda: concavity_statement("05004-15", "down", [(0, -1), (1, 3), (2, 1), (3, -3), (4, -2), (5, 1), (6, -1)]),
   "05004-16": lambda: concavity_statement("05004-16", "up", [(0, 0), (1, -2), (2, -1), (3, -3), (4, 3), (5, 2), (6, -2)]),
   "05004-17": lambda: concavity_statement("05004-17", "up", [(0, -3), (1, 3), (2, -2), (3, -1), (4, -3), (5, 0), (6, 1)]),
   "05004-18": lambda: concavity_statement("05004-18", "down", [(0, -2), (1, -3), (2, -1), (3, 0), (4, -3), (5, 3), (6, 1)]),
   "05004-19": lambda: concavity_statement("05004-19", "up", [(0, 0), (1, -1), (2, 1), (3, -3), (4, -1), (5, 0), (6, -2)]),
   "05004-20": lambda: concavity_statement("05004-20", "up", [(0, -1), (1, 0), (2, -3), (3, -2), (4, 1), (5, -2), (6, -1)]),
   "05004-21": lambda: concavity_statement("05004-21", "down", [(0, -2), (1, 1), (2, 3), (3, 0), (4, -3), (5, 3), (6, 1)]),
   "05005-00": lambda: inflection_statement("05005-00", [(0, 0), (1, -1), (2, -2), (3, -1), (4, 2), (5, -1), (6, -2)]),
   "05005-01": lambda: inflection_statement("05005-01", [(0, -3), (1, 1), (2, 2), (3, -1), (4, 1), (5, 3), (6, -2)]),
   "05005-02": lambda: inflection_statement("05005-02", [(0, -1), (1, 0), (2, -2), (3, 2), (4, 1), (5, -3), (6, 1)]),
   "05005-03": lambda: inflection_statement("05005-03", [(0, 0), (1, 1), (2, 0), (3, -3), (4, -2), (5, 1), (6, 2)]),
   "05005-04": lambda: inflection_statement("05005-04", [(0, -2), (1, -3), (2, -1), (3, 3), (4, 1), (5, 0), (6, -1)]),
   "05005-05": lambda: inflection_statement("05005-05", [(0, -1), (1, 1), (2, 0), (3, -1), (4, 0), (5, 2), (6, 1)]),
   "05005-06": lambda: inflection_statement("05005-06", [(0, -2), (1, 2), (2, 1), (3, -1), (4, -2), (5, -3), (6, 0)]),
   "05005-07": lambda: inflection_statement("05005-07", [(0, 3), (1, 0), (2, 3), (3, 1), (4, -2), (5, 3), (6, -1)]),
   "05005-08": lambda: inflection_statement("05005-08", [(0, 3), (1, -2), (2, -1), (3, 1), (4, 3), (5, 0), (6, -1)]),
   "05005-09": lambda: inflection_statement("05005-09", [(0, 2), (1, -3), (2, 0), (3, 2), (4, -1), (5, 3), (6, 2)]),
   "05005-10": lambda: inflection_statement("05005-10", [(0, 1), (1, 2), (2, -3), (3, 3), (4, 0), (5, -2), (6, 0)]),
   "05005-11": lambda: inflection_statement("05005-11", [(0, -2), (1, 1), (2, 2), (3, 1), (4, 2), (5, -2), (6, 1)]),
   "05005-12": lambda: inflection_statement("05005-12", [(0, -2), (1, 3), (2, -3), (3, -1), (4, 3), (5, 0), (6, 1)]),
   "05005-13": lambda: inflection_statement("05005-13", [(0, 3), (1, -1), (2, 1), (3, 0), (4, 1), (5, 3), (6, -3)]),
   "05005-14": lambda: inflection_statement("05005-14", [(0, -2), (1, 1), (2, -1), (3, 0), (4, 1), (5, 0), (6, -2)]),
   "05005-15": lambda: inflection_statement("05005-15", [(0, 3), (1, -1), (2, -3), (3, 3), (4, -3), (5, 1), (6, 2)]),
   "05005-16": lambda: inflection_statement("05005-16", [(0, 1), (1, 3), (2, 2), (3, 1), (4, -2), (5, 3), (6, 2)]),
   "05005-17": lambda: inflection_statement("05005-17", [(0, 1), (1, 2), (2, -3), (3, -2), (4, -1), (5, 0), (6, 2)]),
   "05005-18": lambda: inflection_statement("05005-18", [(0, -1), (1, -2), (2, 3), (3, -3), (4, 1), (5, 2), (6, 1)]),
   "05005-19": lambda: inflection_statement("05005-19", [(0, 1), (1, -3), (2, -2), (3, 3), (4, -3), (5, 2), (6, 1)]),
   "05005-20": lambda: inflection_statement("05005-20", [(0, 3), (1, -3), (2, 2), (3, -3), (4, -1), (5, 3), (6, 0)]),
   "05005-21": lambda: inflection_statement("05005-21", [(0, 0), (1, 1), (2, 3), (3, -2), (4, 0), (5, 2), (6, -2)]),
   "05006-00": lambda: absolute_extreme(-x - 2 - 16/x, "maximum", 2, 6),
   "05006-01": lambda: absolute_extreme(-3*x - 4 - 27/x, "maximum", 2, 4),
   "05006-02": lambda: absolute_extreme(3*x - 11 + 12/x, "minimum", 1, 4),
   "05006-03": lambda: absolute_extreme(-x**3 + 3*x**2 - 7, "minimum", -1, 5),
   "05006-04": lambda: absolute_extreme(x**3 + 3*x**2 - 10, "minimum", -5, 1),
   "05006-05": lambda: absolute_extreme(3*x - 3 + 48/x, "minimum", 2, 7),
   "05006-06": lambda: absolute_extreme(-x - 11 - 16/x, "maximum", 2, 6),
   "05006-07": lambda: absolute_extreme(-x + 7 - 9/x, "maximum", 2, 5),
   "05006-08": lambda: absolute_extreme(-2*x - 8/x, "maximum", 1, 3),
   "05006-09": lambda: absolute_extreme(3*x + 8 + 48/x, "minimum", 2, 7),
   "05006-10": lambda: absolute_extreme(x - 11 + 16/x, "minimum", 1, 5),
   "05006-11": lambda: absolute_extreme(-x**3 + 3*x**2 + 7, "minimum", -1, 4),
   "05006-12": lambda: absolute_extreme(-x - 4 - 9/x, "maximum", 2, 6),
   "05006-13": lambda: absolute_extreme(-x - 6 - 16/x, "maximum", 3, 5),
   "05006-14": lambda: absolute_extreme(2*x - 5 + 32/x, "minimum", 3, 7),
   "05006-15": lambda: absolute_extreme(-x + 1 - 4/x, "maximum", 1, 5),
   "05006-16": lambda: absolute_extreme(2*x + 11 + 8/x, "minimum", 1, 4),
   "05006-17": lambda: absolute_extreme(-x**3 + 6*x**2 - 9*x - 3, "minimum", -2, 6),
   "05006-18": lambda: absolute_extreme(-x - 1 - 9/x, "maximum", 1, 5),
   "05006-19": lambda: absolute_extreme(-x - 11 - 9/x, "maximum", 2, 6),
   "05006-20": lambda: absolute_extreme(-3*x + 3 - 48/x, "maximum", 2, 6),
   "05006-21": lambda: absolute_extreme(-x**3 + 12*x - 5, "maximum", -5, 5),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
