"""Answers to the unit 1 generated items in stems_A.json and stems_A2.json, each computed from its stem.

Written from the stems alone by a blind solver, claude-opus-5-5, on the operator's delegation of
2026-09-24, without sight of any key, worked solution or template. A statement item returns the
one choice its computed facts make true, read against the choices copied into CHOICES below; a
list in place of one string means no choice or more than one choice held, and the recheck reads
that as an ambiguous item.
"""
import re

import sympy
from sympy import Rational, S, oo
from sympy.parsing.sympy_parser import (
   convert_xor,
   implicit_multiplication_application,
   parse_expr,
   standard_transformations,
)

from tools.key_recheck import derivative, limit_at, x

ITEM_PREFIX = "ITM-GEN-"

PARSE_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
SQUEEZE_SAMPLE_OFFSETS = [Rational(7, 10), Rational(3, 10), Rational(1, 10), Rational(1, 30), Rational(1, 300), Rational(3, 7)]
BOUND_TOLERANCE = 1e-12
INLINE_MATH = re.compile(r"\\\( (.+?) \\\)")


def expression(text):
   return parse_expr(text, transformations=PARSE_TRANSFORMS, local_dict={"x": x})


def closing_brace(text, opening):
   depth = 0

   for index in range(opening, len(text)):
      character = text[index]

      if character == "{":
         depth += 1
      elif character == "}":
         depth -= 1

         if depth == 0:
            return index

   raise ValueError(f"unbalanced braces in {text}")


def expand_command(text, command, arity, template):
   while command in text:
      start = text.index(command)
      cursor = start + len(command)

      while text[cursor] == " ":
         cursor += 1

      arguments = []

      for _ in range(arity):
         end = closing_brace(text, cursor)
         arguments.append(text[cursor + 1:end])
         cursor = end + 1

      text = text[:start] + template.format(*arguments) + text[cursor:]

   return text


def latex_value(latex):
   """The SymPy value of the plain LaTeX used in these choices: fractions, roots, powers, absolute values."""
   text = latex.strip()
   text = text.replace(r"\left|", " Abs(").replace(r"\right|", ") ")
   text = text.replace(r"\left", "").replace(r"\right", "")
   text = text.replace(r"\infty", "oo")
   text = expand_command(text, r"\frac", 2, "(({0})/({1}))")
   text = expand_command(text, r"\sqrt", 1, "sqrt({0})")
   text = expand_command(text, r"\sin", 1, "sin({0})")
   text = expand_command(text, r"\cos", 1, "cos({0})")
   text = text.replace("{", "(").replace("}", ")").replace("^", "**")

   return expression(text)


def inline_math(text):
   return INLINE_MATH.findall(text)


def same_value(left, right):
   is_missing = left is None or right is None

   if is_missing:
      return False

   has_infinity = any(value in (oo, -oo, sympy.zoo) for value in (left, right))

   if has_infinity:
      return left == right

   return sympy.simplify(sympy.sympify(left) - sympy.sympify(right)) == 0


def matching(suffix, holds):
   """The one choice of the item for which holds is true, or the list of all of them when that is not exactly one."""
   holding = [choice for choice in CHOICES[suffix] if holds(choice)]
   is_unique = len(holding) == 1

   if is_unique:
      return holding[0]

   return holding


def one_sided_limits(function, at):
   return limit_at(function, at, "-"), limit_at(function, at, "+")


# BC-QA-01001: limit (and value) at a point read from a graph with open and filled points.

def graph_limit(suffix, at, left, right, value, asks_value):
   limit_exists = left == right

   if asks_value:
      if limit_exists:
         expected = f"\\( \\lim_{{x \\to {at}}} f(x) = {left} \\), and \\( f({at}) = {value} \\)."
      else:
         expected = f"The limit \\( \\lim_{{x \\to {at}}} f(x) \\) does not exist, and \\( f({at}) = {value} \\)."

      return matching(suffix, lambda choice: choice == expected)

   if limit_exists:
      return matching(suffix, lambda choice: choice.startswith(f"The limit is {left}, because f(x) approaches"))

   return matching(suffix, lambda choice: choice.startswith("The limit does not exist, because f(x) approaches different values from the left and from the right"))


# BC-QA-01002: what a table of values near a point suggests about the limit.

def side_estimate(pairs):
   """pairs sorted nearest first; None when the outputs do not settle as x nears the point."""
   values = [value for _, value in pairs]
   gaps = [abs(nearer - farther) for nearer, farther in zip(values, values[1:])]
   is_settling = all(nearer_gap < farther_gap for nearer_gap, farther_gap in zip(gaps, gaps[1:]))

   if not is_settling:
      return None

   return sympy.nsimplify(round(float(values[0]), 2))


def table_limit(suffix, at, rows):
   points = [(Rational(point), Rational(value)) for point, value in rows]
   left_pairs = sorted([pair for pair in points if pair[0] < at], key=lambda pair: at - pair[0])
   right_pairs = sorted([pair for pair in points if pair[0] > at], key=lambda pair: pair[0] - at)
   from_left = side_estimate(left_pairs)
   from_right = side_estimate(right_pairs)
   keeps_alternating = from_left is None or from_right is None

   if keeps_alternating:
      return matching(suffix, lambda choice: choice.startswith("The table suggests that the limit does not exist, because the outputs keep alternating"))

   sides_agree = from_left == from_right

   if sides_agree:
      claim = f"The table suggests that the limit is {from_left}, because the outputs approach {from_left} from both sides"

      return matching(suffix, lambda choice: choice.startswith(claim))

   return matching(suffix, lambda choice: choice.startswith("The table suggests that the limit does not exist, because the outputs approach different values on the two sides"))


# BC-QA-01003: limit of h(f(x)) / g(x) from the stated limits of f and g, h a polynomial.

def composite_quotient_limit(outer, limit_of_inner, limit_of_denominator):
   return sympy.nsimplify(expression(outer).subs(x, limit_of_inner) / limit_of_denominator)


# BC-QA-01004: a 0/0 rational limit resolved by cancelling the common factor.

def stated_limit(choice):
   match = re.match(r"The limit is \\\( (.+?) \\\)", choice)

   return None if match is None else latex_value(match.group(1))


def cancelled_limit(suffix, function, at):
   value = limit_at(expression(function), at)

   def holds(choice):
      argues_by_cancelling = "common factor" in choice

      return argues_by_cancelling and same_value(stated_limit(choice), value)

   return matching(suffix, holds)


# BC-QA-01005: squeeze theorem with a bounded trigonometric factor.

def lies_between(lower, function, upper, point):
   lower_value = float(lower.subs(x, point))
   function_value = float(function.subs(x, point))
   upper_value = float(upper.subs(x, point))
   above_lower = lower_value <= function_value + BOUND_TOLERANCE
   below_upper = function_value <= upper_value + BOUND_TOLERANCE

   return above_lower and below_upper


def squeeze_limit(suffix, function, at):
   function = expression(function)
   value = limit_at(function, at)
   samples = [at + offset for offset in SQUEEZE_SAMPLE_OFFSETS] + [at - offset for offset in SQUEEZE_SAMPLE_OFFSETS]

   def holds(choice):
      bounds = re.search(r"because \\\( (.+?) \\le f\(x\) \\le (.+?) \\\) for", choice)
      argues_by_limits = "both bounds approach" in choice
      is_squeeze_argument = bounds is not None and argues_by_limits

      if not is_squeeze_argument:
         return False

      lower = latex_value(bounds.group(1))
      upper = latex_value(bounds.group(2))
      encloses = all(lies_between(lower, function, upper, point) for point in samples)
      lower_meets = limit_at(lower, at) == value
      upper_meets = limit_at(upper, at) == value
      bounds_meet = lower_meets and upper_meets

      return encloses and bounds_meet

   return matching(suffix, holds)


# BC-QA-01006: continuity at a point of a two-part definition.

def continuity_at_point(suffix, left_piece, right_piece, at, value):
   from_left = limit_at(expression(left_piece), at, "-")
   from_right = limit_at(expression(right_piece), at, "+")
   value = sympy.nsimplify(value)
   limit_exists = from_left == from_right
   is_continuous = limit_exists and from_left == value

   if is_continuous:
      reason = f"because the limit of f(x) there is {from_left}, which equals f({at})"

      return matching(suffix, lambda choice: choice.startswith("f is continuous") and reason in choice)

   if limit_exists:
      reason = f"because the limit of f(x) there is {from_left} while f({at}) = {value}"

      return matching(suffix, lambda choice: choice.startswith("f is not continuous") and reason in choice)

   reason = f"because the limits from the left and from the right are {from_left} and {from_right}"

   return matching(suffix, lambda choice: choice.startswith("f is not continuous") and reason in choice)


# BC-QA-01007: classify the discontinuity of a rational function at a zero of its denominator.

def discontinuity_kind(suffix, numerator, denominator, at):
   numerator = expression(numerator)
   denominator = expression(denominator)
   is_undefined = denominator.subs(x, at) == 0

   if not is_undefined:
      return matching(suffix, lambda choice: choice.startswith("There is no discontinuity"))

   from_left, from_right = one_sided_limits(numerator / denominator, at)
   is_unbounded = any(side in (oo, -oo) for side in (from_left, from_right))
   is_removable = not is_unbounded and from_left == from_right

   if is_unbounded:
      kind = "a vertical asymptote"
   elif is_removable:
      kind = "removable"
   else:
      kind = "a jump"

   return matching(suffix, lambda choice: choice.startswith(f"The discontinuity at \\( x = {at} \\) is {kind},"))


# BC-QA-01008: constants k and m that make a three-part function continuous.

def continuity_constants(suffix, left_piece, right_piece, left_joint, right_joint):
   k, m = sympy.symbols("k m")
   middle = k * x + m
   left_meets = sympy.Eq(middle.subs(x, left_joint), limit_at(expression(left_piece), left_joint, "-"))
   right_meets = sympy.Eq(middle.subs(x, right_joint), limit_at(expression(right_piece), right_joint, "+"))
   solution = sympy.solve([left_meets, right_meets], [k, m], dict=True)
   has_one_solution = len(solution) == 1

   if not has_one_solution:
      return matching(suffix, lambda choice: choice.startswith("No values"))

   claim = f"\\( k = {sympy.latex(solution[0][k])} \\) and \\( m = {sympy.latex(solution[0][m])} \\),"

   return matching(suffix, lambda choice: choice.startswith(claim))


# BC-QA-01009: every vertical asymptote of a rational function and its one sided limits.

def asymptote_claims(choice):
   claimed = {int(point) for point in re.findall(r"\\\( x = (-?\d+) \\\)", choice)}
   one_sided = re.findall(r"\\lim_\{x \\to (-?\d+)\^\{([-+])\}\} f\(x\) = (-?\\infty)", choice)
   both_sides = re.findall(r"\\lim_\{x \\to (-?\d+)\} f\(x\) = (-?\\infty) \\\) from both sides", choice)
   limits = {}

   for point, side, value in one_sided:
      limits[(int(point), side)] = latex_value(value)

   for point, value in both_sides:
      limits[(int(point), "-")] = latex_value(value)
      limits[(int(point), "+")] = latex_value(value)

   return claimed, limits


def vertical_asymptotes(suffix, numerator, denominator):
   function = expression(numerator) / expression(denominator)
   zeros = sympy.solveset(expression(denominator), x, sympy.S.Reals)
   computed = {}

   for zero in zeros:
      from_left, from_right = one_sided_limits(function, zero)
      is_asymptote = from_left in (oo, -oo) or from_right in (oo, -oo)

      if is_asymptote:
         computed[(int(zero), "-")] = from_left
         computed[(int(zero), "+")] = from_right

   asymptotes = {point for point, _ in computed}

   def holds(choice):
      denies_all = choice.startswith("No line")

      if denies_all:
         return len(asymptotes) == 0

      claimed, limits = asymptote_claims(choice)
      limits_right = all(computed.get(key) == value for key, value in limits.items())

      return claimed == asymptotes and len(limits) > 0 and limits_right

   return matching(suffix, holds)


# BC-QA-01010: limit as x decreases without bound of a quotient with a square root.

def limit_at_negative_infinity(function):
   return limit_at(expression(function), -oo)


# BC-QA-01011: whether the Intermediate Value Theorem guarantees a value from a table.

def brackets_target(table, low, high, target):
   is_ordered = low < high
   smaller, larger = sorted([table[low], table[high]])
   is_strictly_between = smaller < target < larger

   return is_ordered and is_strictly_between


def ivt_guarantee(suffix, rows, left_end, right_end, target):
   table = {int(point): int(value) for point, value in rows}
   inside = sorted(point for point in table if left_end <= point <= right_end)
   brackets = {(low, high) for low in inside for high in inside if brackets_target(table, low, high, target)}

   if not brackets:
      all_above = all(table[point] > target for point in inside)
      all_below = all(table[point] < target for point in inside)
      side = "greater" if all_above else "less" if all_below else None
      claim = f"No. Every tabulated value of f is {side} than {target},"

      return matching(suffix, lambda choice: choice.startswith(claim))

   def holds(choice):
      stated = re.search(
         r"it is continuous on \\\( \[(-?\d+), (-?\d+)\] \\\), and \\\( f\((-?\d+)\) = (-?\d+) < (-?\d+) < f\((-?\d+)\) = (-?\d+) \\\), so the Intermediate Value Theorem gives at least one such c\.$",
         choice,
      )

      if stated is None:
         return False

      low, high, first_point, first_value, stated_target, second_point, second_value = [int(part) for part in stated.groups()]
      values_match = table.get(first_point) == first_value and table.get(second_point) == second_value
      points_match = {first_point, second_point} == {low, high}
      target_matches = stated_target == target

      return (low, high) in brackets and values_match and points_match and target_matches

   return matching(suffix, holds)


# BC-QA-01012: instantaneous rate of change as the limit of average rates.

def rate_at(function, at):
   return derivative(expression(function)).subs(x, at)


def rate_from_table(rows):
   """The difference quotients from the first row; a quadratic makes them linear in the step, so the
   line through the two smallest steps meets the axis at the derivative."""
   base_point, base_value = Rational(rows[0][0]), Rational(rows[0][1])
   quotients = sorted(
      ((Rational(point) - base_point, (Rational(value) - base_value) / (Rational(point) - base_point)) for point, value in rows[1:]),
      key=lambda pair: pair[0],
   )
   (small_step, small_quotient), (next_step, next_quotient) = quotients[0], quotients[1]
   slope = (next_quotient - small_quotient) / (next_step - small_step)

   return sympy.nsimplify(small_quotient - slope * small_step)


# BC-QA-01013: what a limit statement says about a function and its graph.

def limit_meaning(suffix, approach, side, target):
   """approach is oo or -oo for a limit at infinity, else a point; side is "left" or "right" for a one sided
   limit; target is the limit value."""
   at_infinity = approach in (oo, -oo)

   if at_infinity:
      motion = "increases" if approach == oo else "decreases"
      opening = f"As x {motion} without bound,"

      return matching(suffix, lambda choice: choice.startswith(opening) and "horizontal asymptote" in choice and "both ends" not in choice)

   trend = "increases" if target == oo else "decreases"
   claim = f"from the {side}, "
   conclusion = f"{trend} without bound, so the line \\( x ="

   return matching(suffix, lambda choice: choice.startswith("As x approaches") and claim in choice and conclusion in choice)


# BC-QA-01014: classify the form of a limit, name its procedure, and give the result.

def final_value(choice):
   parts = inline_math(choice)

   return None if not parts else latex_value(parts[-1])


def form_and_result(suffix, numerator, denominator, at):
   numerator = expression(numerator)
   denominator = expression(denominator)
   function = numerator / denominator

   if at == oo:
      value = limit_at(function, oo)

      return matching(suffix, lambda choice: "divide both parts by" in choice and same_value(final_value(choice), value))

   numerator_at = sympy.simplify(numerator.subs(x, at))
   denominator_at = sympy.simplify(denominator.subs(x, at))
   is_zero_over_zero = numerator_at == 0 and denominator_at == 0

   if is_zero_over_zero:
      value = limit_at(function, at)

      return matching(suffix, lambda choice: choice.startswith("Substitution gives 0/0, so") and same_value(final_value(choice), value))

   from_left, from_right = one_sided_limits(function, at)
   sides_agree = from_left == from_right

   if sides_agree:
      outcome = f"which gives \\( {sympy.latex(from_left)} \\) on both sides"
   else:
      outcome = f"which gives \\( {sympy.latex(from_left)} \\) and \\( {sympy.latex(from_right)} \\), so no limit exists"

   return matching(suffix, lambda choice: "check the sign on each side" in choice and outcome in choice)


# BC-QA-01015: intervals of continuity of a quotient, one part possibly a square root.

def interval_from_latex(text):
   left_closed = text.startswith("[")
   right_closed = text.endswith("]")
   low_text, high_text = text[1:-1].split(", ")

   return sympy.Interval(latex_value(low_text), latex_value(high_text), not left_closed, not right_closed)


def stated_intervals(choice):
   body = re.search(r"continuous on \\\( (.+) \\\)\.$", choice).group(1)

   return sympy.Union(*[interval_from_latex(part.strip()) for part in body.split(r"\cup")])


def continuity_intervals(suffix, numerator, denominator):
   numerator = expression(numerator)
   denominator = expression(denominator)
   numerator_domain = sympy.calculus.util.continuous_domain(numerator, x, sympy.S.Reals)
   denominator_zeros = sympy.solveset(denominator, x, sympy.S.Reals)
   domain = sympy.Complement(numerator_domain, denominator_zeros)

   return matching(suffix, lambda choice: stated_intervals(choice) == domain)


CHOICES = {
   "01001-00": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit does not exist, because the graph has no filled point where x = 5.",
      "The limit is -3, because f(x) approaches -3 as x approaches 5 from the right.",
      "The limit is 1, because f(x) approaches 1 as x approaches 5 from the left.",
   ],
   "01001-01": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit is -2, because the graph has a filled point at (5, -2).",
      "The limit is 0, because f(x) approaches 0 as x approaches 5 from the right.",
      "The limit is 4, because f(x) approaches 4 as x approaches 5 from the left.",
   ],
   "01001-02": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit is -1, because the graph has a filled point at (6, -1).",
      "The limit is 2, because f(x) approaches 2 as x approaches 6 from the left.",
      "The limit is 4, because f(x) approaches 4 as x approaches 6 from the right.",
   ],
   "01001-03": [
      "The limit \\( \\lim_{x \\to 3} f(x) \\) does not exist, and \\( f(3) = 1 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 0 \\), and \\( f(3) = 0 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 0 \\), and \\( f(3) = 1 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 1 \\), and \\( f(3) = 1 \\).",
   ],
   "01001-04": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit is -2, because the graph has a filled point at (6, -2).",
      "The limit is 2, because f(x) approaches 2 as x approaches 6 from the right.",
      "The limit is 4, because f(x) approaches 4 as x approaches 6 from the left.",
   ],
   "01001-05": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit does not exist, because the graph has no filled point where x = 6.",
      "The limit is 2, because f(x) approaches 2 as x approaches 6 from the right.",
      "The limit is 4, because f(x) approaches 4 as x approaches 6 from the left.",
   ],
   "01001-06": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit does not exist, because the graph has no filled point where x = 6.",
      "The limit is -1, because f(x) approaches -1 as x approaches 6 from the left.",
      "The limit is 3, because f(x) approaches 3 as x approaches 6 from the right.",
   ],
   "01001-07": [
      "The limit \\( \\lim_{x \\to 2} f(x) \\) does not exist, and \\( f(2) = 3 \\).",
      "\\( \\lim_{x \\to 2} f(x) = -2 \\), and \\( f(2) = -2 \\).",
      "\\( \\lim_{x \\to 2} f(x) = -2 \\), and \\( f(2) = 3 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 3 \\), and \\( f(2) = 3 \\).",
   ],
   "01001-08": [
      "The limit \\( \\lim_{x \\to 3} f(x) \\) does not exist, and \\( f(3) = 3 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 1 \\), and \\( f(3) = 1 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 1 \\), and \\( f(3) = 3 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 3 \\), and \\( f(3) = 3 \\).",
   ],
   "01001-09": [
      "The limit \\( \\lim_{x \\to 1} f(x) \\) does not exist, and \\( f(1) = -1 \\).",
      "\\( \\lim_{x \\to 1} f(x) = -1 \\), and \\( f(1) = -1 \\).",
      "\\( \\lim_{x \\to 1} f(x) = 4 \\), and \\( f(1) = -1 \\).",
      "\\( \\lim_{x \\to 1} f(x) = 4 \\), and \\( f(1) = 4 \\).",
   ],
   "01001-10": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit is -2, because f(x) approaches -2 as x approaches 6 from the left.",
      "The limit is 0, because the graph has a filled point at (6, 0).",
      "The limit is 3, because f(x) approaches 3 as x approaches 6 from the right.",
   ],
   "01001-11": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit is -3, because f(x) approaches -3 as x approaches 5 from the right.",
      "The limit is 0, because the graph has a filled point at (5, 0).",
      "The limit is 1, because f(x) approaches 1 as x approaches 5 from the left.",
   ],
   "01001-12": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit is -1, because f(x) approaches -1 as x approaches 6 from the right.",
      "The limit is -3, because the graph has a filled point at (6, -3).",
      "The limit is 2, because f(x) approaches 2 as x approaches 6 from the left.",
   ],
   "01001-13": [
      "The limit \\( \\lim_{x \\to 2} f(x) \\) does not exist, and \\( f(2) = -1 \\).",
      "\\( \\lim_{x \\to 2} f(x) = -1 \\), and \\( f(2) = -1 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 3 \\), and \\( f(2) = -1 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 3 \\), and \\( f(2) = 3 \\).",
   ],
   "01001-14": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit does not exist, because the graph has no filled point where x = 5.",
      "The limit is -3, because f(x) approaches -3 as x approaches 5 from the right.",
      "The limit is 0, because f(x) approaches 0 as x approaches 5 from the left.",
   ],
   "01001-15": [
      "The limit \\( \\lim_{x \\to 3} f(x) \\) does not exist, and \\( f(3) = 3 \\).",
      "\\( \\lim_{x \\to 3} f(x) = -3 \\), and \\( f(3) = -3 \\).",
      "\\( \\lim_{x \\to 3} f(x) = -3 \\), and \\( f(3) = 3 \\).",
      "\\( \\lim_{x \\to 3} f(x) = 3 \\), and \\( f(3) = 3 \\).",
   ],
   "01001-16": [
      "The limit \\( \\lim_{x \\to 2} f(x) \\) does not exist, and \\( f(2) = -3 \\).",
      "\\( \\lim_{x \\to 2} f(x) = -3 \\), and \\( f(2) = -3 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 4 \\), and \\( f(2) = -3 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 4 \\), and \\( f(2) = 4 \\).",
   ],
   "01001-17": [
      "The limit \\( \\lim_{x \\to 2} f(x) \\) does not exist, and \\( f(2) = 4 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 2 \\), and \\( f(2) = 2 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 2 \\), and \\( f(2) = 4 \\).",
      "\\( \\lim_{x \\to 2} f(x) = 4 \\), and \\( f(2) = 4 \\).",
   ],
   "01001-18": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit does not exist, because the graph has no filled point where x = 5.",
      "The limit is -3, because f(x) approaches -3 as x approaches 5 from the left.",
      "The limit is 3, because f(x) approaches 3 as x approaches 5 from the right.",
   ],
   "01001-19": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit is -1, because f(x) approaches -1 as x approaches 5 from the left.",
      "The limit is 0, because the graph has a filled point at (5, 0).",
      "The limit is 3, because f(x) approaches 3 as x approaches 5 from the right.",
   ],
   "01001-20": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 5.",
      "The limit does not exist, because the graph has no filled point where x = 5.",
      "The limit is -3, because f(x) approaches -3 as x approaches 5 from the right.",
      "The limit is 1, because f(x) approaches 1 as x approaches 5 from the left.",
   ],
   "01001-21": [
      "The limit does not exist, because f(x) approaches different values from the left and from the right of x = 6.",
      "The limit is -2, because f(x) approaches -2 as x approaches 6 from the right.",
      "The limit is 2, because f(x) approaches 2 as x approaches 6 from the left.",
      "The limit is 4, because the graph has a filled point at (6, 4).",
   ],
   "01002-00": [
      "The table suggests that the limit does not exist, because f is not defined at x = 1.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1.",
      "The table suggests that the limit is -4, because the outputs keep returning to -4.",
      "The table suggests that the limit is 0, because the outputs keep returning to 0.",
   ],
   "01002-01": [
      "The table suggests that the limit does not exist, because f is not defined at x = 4.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 4.",
      "The table suggests that the limit is 3, because the outputs keep returning to 3.",
      "The table suggests that the limit is 6, because the outputs keep returning to 6.",
   ],
   "01002-02": [
      "The table proves that the limit is -4, because the outputs nearest x = 5 are within 0.01 of -4.",
      "The table suggests that the limit does not exist, because f is not defined at x = 5.",
      "The table suggests that the limit is -3.9996, because that output is the one nearest x = 5.",
      "The table suggests that the limit is -4, because the outputs approach -4 from both sides of x = 5.",
   ],
   "01002-03": [
      "The table suggests that the limit does not exist, because f is not defined at x = 1.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1.",
      "The table suggests that the limit is -3, because the outputs keep returning to -3.",
      "The table suggests that the limit is 0, because the outputs keep returning to 0.",
   ],
   "01002-04": [
      "The table suggests that the limit does not exist, because f is not defined at x = 1.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1.",
      "The table suggests that the limit is -3, because the outputs keep returning to -3.",
      "The table suggests that the limit is 6, because the outputs keep returning to 6.",
   ],
   "01002-05": [
      "The table proves that the limit is 0, because the outputs nearest x = -2 are within 0.01 of 0.",
      "The table suggests that the limit does not exist, because f is not defined at x = -2.",
      "The table suggests that the limit is 0, because the outputs approach 0 from both sides of x = -2.",
      "The table suggests that the limit is 0.0005, because that output is the one nearest x = -2.",
   ],
   "01002-06": [
      "The table suggests that the limit does not exist, because f is not defined at x = 4.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 4.",
      "The table suggests that the limit is -2, because the outputs keep returning to -2.",
      "The table suggests that the limit is 5, because the outputs keep returning to 5.",
   ],
   "01002-07": [
      "The table proves that the limit is 4, because the outputs nearest x = -1 are within 0.01 of 4.",
      "The table suggests that the limit does not exist, because f is not defined at x = -1.",
      "The table suggests that the limit is 3.9993, because that output is the one nearest x = -1.",
      "The table suggests that the limit is 4, because the outputs approach 4 from both sides of x = -1.",
   ],
   "01002-08": [
      "The table suggests that the limit does not exist, because f is not defined at x = 3.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 3.",
      "The table suggests that the limit is 1, because the outputs approach 1 from the left of x = 3.",
      "The table suggests that the limit is 2, because the outputs approach 2 from the right of x = 3.",
   ],
   "01002-09": [
      "The table suggests that the limit does not exist, because f is not defined at x = 1.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 1.",
      "The table suggests that the limit is -2, because the outputs keep returning to -2.",
      "The table suggests that the limit is 2, because the outputs keep returning to 2.",
   ],
   "01002-10": [
      "The table suggests that the limit does not exist, because f is not defined at x = -3.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches -3.",
      "The table suggests that the limit is -1, because the outputs keep returning to -1.",
      "The table suggests that the limit is 6, because the outputs keep returning to 6.",
   ],
   "01002-11": [
      "The table suggests that the limit does not exist, because f is not defined at x = 0.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 0.",
      "The table suggests that the limit is -2, because the outputs approach -2 from the left of x = 0.",
      "The table suggests that the limit is -3, because the outputs approach -3 from the right of x = 0.",
   ],
   "01002-12": [
      "The table suggests that the limit does not exist, because f is not defined at x = -1.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches -1.",
      "The table suggests that the limit is 2, because the outputs keep returning to 2.",
      "The table suggests that the limit is 4, because the outputs keep returning to 4.",
   ],
   "01002-13": [
      "The table suggests that the limit does not exist, because f is not defined at x = 5.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 5.",
      "The table suggests that the limit is -2, because the outputs keep returning to -2.",
      "The table suggests that the limit is 5, because the outputs keep returning to 5.",
   ],
   "01002-14": [
      "The table suggests that the limit does not exist, because f is not defined at x = 3.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 3.",
      "The table suggests that the limit is -4, because the outputs approach -4 from the right of x = 3.",
      "The table suggests that the limit is 4, because the outputs approach 4 from the left of x = 3.",
   ],
   "01002-15": [
      "The table suggests that the limit does not exist, because f is not defined at x = 1.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 1.",
      "The table suggests that the limit is 1, because the outputs approach 1 from the right of x = 1.",
      "The table suggests that the limit is 2, because the outputs approach 2 from the left of x = 1.",
   ],
   "01002-16": [
      "The table proves that the limit is 3, because the outputs nearest x = 3 are within 0.01 of 3.",
      "The table suggests that the limit does not exist, because f is not defined at x = 3.",
      "The table suggests that the limit is 3, because the outputs approach 3 from both sides of x = 3.",
      "The table suggests that the limit is 3.0003, because that output is the one nearest x = 3.",
   ],
   "01002-17": [
      "The table suggests that the limit does not exist, because f is not defined at x = 3.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 3.",
      "The table suggests that the limit is 0, because the outputs approach 0 from the right of x = 3.",
      "The table suggests that the limit is 4, because the outputs approach 4 from the left of x = 3.",
   ],
   "01002-18": [
      "The table suggests that the limit does not exist, because f is not defined at x = 5.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = 5.",
      "The table suggests that the limit is -2, because the outputs approach -2 from the right of x = 5.",
      "The table suggests that the limit is 5, because the outputs approach 5 from the left of x = 5.",
   ],
   "01002-19": [
      "The table suggests that the limit does not exist, because f is not defined at x = -1.",
      "The table suggests that the limit does not exist, because the outputs approach different values on the two sides of x = -1.",
      "The table suggests that the limit is 0, because the outputs approach 0 from the right of x = -1.",
      "The table suggests that the limit is 1, because the outputs approach 1 from the left of x = -1.",
   ],
   "01002-20": [
      "The table proves that the limit is 1, because the outputs nearest x = -2 are within 0.01 of 1.",
      "The table suggests that the limit does not exist, because f is not defined at x = -2.",
      "The table suggests that the limit is 1, because the outputs approach 1 from both sides of x = -2.",
      "The table suggests that the limit is 1.0004, because that output is the one nearest x = -2.",
   ],
   "01002-21": [
      "The table suggests that the limit does not exist, because f is not defined at x = 0.",
      "The table suggests that the limit does not exist, because the outputs keep alternating as x approaches 0.",
      "The table suggests that the limit is -2, because the outputs keep returning to -2.",
      "The table suggests that the limit is 2, because the outputs keep returning to 2.",
   ],
   "01004-00": [
      "The limit does not exist, because substituting \\( x = -5 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} + 2 x - 15 \\) approaches 0 as x approaches -5.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{2 x - 15}{8 x + 15} \\), which equals 1 at \\( x = -5 \\).",
      "The limit is \\( 4 \\), because after the common factor \\( x + 5 \\) cancels, substitution into \\( \\frac{x - 3}{x + 3} \\) gives that value.",
   ],
   "01004-01": [
      "The limit does not exist, because substituting \\( x = 2 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} + 5 x - 14 \\) approaches 0 as x approaches 2.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{5 x - 14}{- 2 x} \\), which equals 1 at \\( x = 2 \\).",
      "The limit is \\( \\frac{9}{2} \\), because after the common factor \\( x - 2 \\) cancels, substitution into \\( \\frac{x + 7}{x} \\) gives that value.",
   ],
   "01004-02": [
      "The limit does not exist, because substituting \\( x = -2 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} + x - 2 \\) approaches 0 as x approaches -2.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{x - 2}{- 3 x - 10} \\), which equals 1 at \\( x = -2 \\).",
      "The limit is \\( \\frac{3}{7} \\), because after the common factor \\( x + 2 \\) cancels, substitution into \\( \\frac{x - 1}{x - 5} \\) gives that value.",
   ],
   "01004-03": [
      "The limit does not exist, because substituting \\( x = -4 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 2 x - 24 \\) approaches 0 as x approaches -4.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{- 2 x - 24}{7 x + 12} \\), which equals 1 at \\( x = -4 \\).",
      "The limit is \\( 10 \\), because after the common factor \\( x + 4 \\) cancels, substitution into \\( \\frac{x - 6}{x + 3} \\) gives that value.",
   ],
   "01004-04": [
      "The limit does not exist, because substituting \\( x = 2 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 9 x + 14 \\) approaches 0 as x approaches 2.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{14 - 9 x}{6 - 5 x} \\), which equals 1 at \\( x = 2 \\).",
      "The limit is \\( 5 \\), because after the common factor \\( x - 2 \\) cancels, substitution into \\( \\frac{x - 7}{x - 3} \\) gives that value.",
   ],
   "01004-05": [
      "The limit does not exist, because substituting \\( x = 4 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 4 x \\) approaches 0 as x approaches 4.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{- 4 x}{12 - 7 x} \\), which equals 1 at \\( x = 4 \\).",
      "The limit is \\( 4 \\), because after the common factor \\( x - 4 \\) cancels, substitution into \\( \\frac{x}{x - 3} \\) gives that value.",
   ],
   "01004-06": [
      "The limit does not exist, because substituting \\( x = 1 \\) into the quotient gives the form 0/0.",
      "The limit is \\( - \\frac{4}{5} \\), because after the common factor \\( x - 1 \\) cancels, substitution into \\( \\frac{x - 5}{x + 4} \\) gives that value.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 6 x + 5 \\) approaches 0 as x approaches 1.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{5 - 6 x}{3 x - 4} \\), which equals 1 at \\( x = 1 \\).",
   ],
   "01004-07": [
      "The limit does not exist, because substituting \\( x = 1 \\) into the quotient gives the form 0/0.",
      "The limit is \\( -4 \\), because after the common factor \\( x - 1 \\) cancels, substitution into \\( \\frac{x - 5}{x} \\) gives that value.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 6 x + 5 \\) approaches 0 as x approaches 1.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{5 - 6 x}{- x} \\), which equals 1 at \\( x = 1 \\).",
   ],
   "01004-08": [
      "The limit does not exist, because substituting \\( x = -3 \\) into the quotient gives the form 0/0.",
      "The limit is \\( - \\frac{5}{2} \\), because after the common factor \\( x + 3 \\) cancels, substitution into \\( \\frac{x - 2}{x + 5} \\) gives that value.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} + x - 6 \\) approaches 0 as x approaches -3.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{x - 6}{8 x + 15} \\), which equals 1 at \\( x = -3 \\).",
   ],
   "01004-09": [
      "The limit does not exist, because substituting \\( x = -1 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 3 x - 4 \\) approaches 0 as x approaches -1.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{- 3 x - 4}{- 4 x - 5} \\), which equals 1 at \\( x = -1 \\).",
      "The limit is \\( \\frac{5}{6} \\), because after the common factor \\( x + 1 \\) cancels, substitution into \\( \\frac{x - 4}{x - 5} \\) gives that value.",
   ],
   "01004-10": [
      "The limit does not exist, because substituting \\( x = 3 \\) into the quotient gives the form 0/0.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} - 9 x + 18 \\) approaches 0 as x approaches 3.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{18 - 9 x}{15 - 8 x} \\), which equals 1 at \\( x = 3 \\).",
      "The limit is \\( \\frac{3}{2} \\), because after the common factor \\( x - 3 \\) cancels, substitution into \\( \\frac{x - 6}{x - 5} \\) gives that value.",
   ],
   "01004-11": [
      "The limit does not exist, because substituting \\( x = 1 \\) into the quotient gives the form 0/0.",
      "The limit is \\( -1 \\), because after the common factor \\( x - 1 \\) cancels, substitution into \\( \\frac{x + 2}{x - 4} \\) gives that value.",
      "The limit is \\( 0 \\), because the numerator \\( x^{2} + x - 2 \\) approaches 0 as x approaches 1.",
      "The limit is \\( 1 \\), because cancelling the \\( x^{2} \\) terms leaves \\( \\frac{x - 2}{4 - 5 x} \\), which equals 1 at \\( x = 1 \\).",
   ],
   "01005-00": [
      "The limit is -2, because \\( - 3 \\left(x - 2\\right)^{3} \\) approaches 0 as x approaches 2 and the limit of a product is the product of the limits.",
      "The limit is -2, because \\( -2 - 3 \\left|{x - 2}\\right|^{3} \\le f(x) \\le 3 \\left|{x - 2}\\right|^{3} - 2 \\) for \\( x \\ne 2 \\) and both bounds approach -2 as x approaches 2.",
      "The limit is -2, because \\( -2 - 3 \\left|{x - 2}\\right|^{3} \\le f(x) \\le 3 \\left|{x - 2}\\right|^{3} - 2 \\) for \\( x \\ne 2 \\) and both bounds equal -2 when x is 2.",
      "The limit is -2, because \\( 3 \\left(x - 2\\right)^{3} - 2 \\le f(x) \\le - 3 \\left(x - 2\\right)^{3} - 2 \\) for \\( x \\ne 2 \\) and both bounds approach -2 as x approaches 2.",
   ],
   "01005-01": [
      "The limit is 3, because \\( - 3 x^{3} \\) approaches 0 as x approaches 0 and the limit of a product is the product of the limits.",
      "The limit is 3, because \\( 3 - 3 \\left|{x}\\right|^{3} \\le f(x) \\le 3 \\left|{x}\\right|^{3} + 3 \\) for \\( x \\ne 0 \\) and both bounds approach 3 as x approaches 0.",
      "The limit is 3, because \\( 3 - 3 \\left|{x}\\right|^{3} \\le f(x) \\le 3 \\left|{x}\\right|^{3} + 3 \\) for \\( x \\ne 0 \\) and both bounds equal 3 when x is 0.",
      "The limit is 3, because \\( 3 x^{3} + 3 \\le f(x) \\le - 3 x^{3} + 3 \\) for \\( x \\ne 0 \\) and both bounds approach 3 as x approaches 0.",
   ],
   "01005-02": [
      "The limit is 0, because \\( - 2 \\left(x + 3\\right)^{3} \\le f(x) \\le 2 \\left(x + 3\\right)^{3} \\) for \\( x \\ne -3 \\) and both bounds approach 0 as x approaches -3.",
      "The limit is 0, because \\( -2 \\left|{x + 3}\\right|^{3} \\le f(x) \\le 2 \\left|{x + 3}\\right|^{3} \\) for \\( x \\ne -3 \\) and both bounds approach 0 as x approaches -3.",
      "The limit is 0, because \\( -2 \\left|{x + 3}\\right|^{3} \\le f(x) \\le 2 \\left|{x + 3}\\right|^{3} \\) for \\( x \\ne -3 \\) and both bounds equal 0 when x is -3.",
      "The limit is 0, because \\( 2 \\left(x + 3\\right)^{3} \\) approaches 0 as x approaches -3 and the limit of a product is the product of the limits.",
   ],
   "01005-03": [
      "The limit is 1, because \\( - 4 \\left(x - 2\\right) \\) approaches 0 as x approaches 2 and the limit of a product is the product of the limits.",
      "The limit is 1, because \\( 1 - 4 \\left|{x - 2}\\right| \\le f(x) \\le 4 \\left|{x - 2}\\right| + 1 \\) for \\( x \\ne 2 \\) and both bounds approach 1 as x approaches 2.",
      "The limit is 1, because \\( 1 - 4 \\left|{x - 2}\\right| \\le f(x) \\le 4 \\left|{x - 2}\\right| + 1 \\) for \\( x \\ne 2 \\) and both bounds equal 1 when x is 2.",
      "The limit is 1, because \\( 4 \\left(x - 2\\right) + 1 \\le f(x) \\le - 4 \\left(x - 2\\right) + 1 \\) for \\( x \\ne 2 \\) and both bounds approach 1 as x approaches 2.",
   ],
   "01005-04": [
      "The limit is -1, because \\( - (x + 3) - 1 \\le f(x) \\le 1 \\left(x + 3\\right) - 1 \\) for \\( x \\ne -3 \\) and both bounds approach -1 as x approaches -3.",
      "The limit is -1, because \\( -1 - \\left|{x + 3}\\right| \\le f(x) \\le \\left|{x + 3}\\right| - 1 \\) for \\( x \\ne -3 \\) and both bounds approach -1 as x approaches -3.",
      "The limit is -1, because \\( -1 - \\left|{x + 3}\\right| \\le f(x) \\le \\left|{x + 3}\\right| - 1 \\) for \\( x \\ne -3 \\) and both bounds equal -1 when x is -3.",
      "The limit is -1, because \\( 1 \\left(x + 3\\right) \\) approaches 0 as x approaches -3 and the limit of a product is the product of the limits.",
   ],
   "01005-05": [
      "The limit is 1, because \\( - 4 \\left(x + 3\\right) + 1 \\le f(x) \\le 4 \\left(x + 3\\right) + 1 \\) for \\( x \\ne -3 \\) and both bounds approach 1 as x approaches -3.",
      "The limit is 1, because \\( 1 - 4 \\left|{x + 3}\\right| \\le f(x) \\le 4 \\left|{x + 3}\\right| + 1 \\) for \\( x \\ne -3 \\) and both bounds approach 1 as x approaches -3.",
      "The limit is 1, because \\( 1 - 4 \\left|{x + 3}\\right| \\le f(x) \\le 4 \\left|{x + 3}\\right| + 1 \\) for \\( x \\ne -3 \\) and both bounds equal 1 when x is -3.",
      "The limit is 1, because \\( 4 \\left(x + 3\\right) \\) approaches 0 as x approaches -3 and the limit of a product is the product of the limits.",
   ],
   "01005-06": [
      "The limit is 5, because \\( - 2 \\left(x + 1\\right)^{3} + 5 \\le f(x) \\le 2 \\left(x + 1\\right)^{3} + 5 \\) for \\( x \\ne -1 \\) and both bounds approach 5 as x approaches -1.",
      "The limit is 5, because \\( 2 \\left(x + 1\\right)^{3} \\) approaches 0 as x approaches -1 and the limit of a product is the product of the limits.",
      "The limit is 5, because \\( 5 - 2 \\left|{x + 1}\\right|^{3} \\le f(x) \\le 2 \\left|{x + 1}\\right|^{3} + 5 \\) for \\( x \\ne -1 \\) and both bounds approach 5 as x approaches -1.",
      "The limit is 5, because \\( 5 - 2 \\left|{x + 1}\\right|^{3} \\le f(x) \\le 2 \\left|{x + 1}\\right|^{3} + 5 \\) for \\( x \\ne -1 \\) and both bounds equal 5 when x is -1.",
   ],
   "01005-07": [
      "The limit is 2, because \\( - 4 \\left(x + 2\\right)^{3} \\) approaches 0 as x approaches -2 and the limit of a product is the product of the limits.",
      "The limit is 2, because \\( 2 - 4 \\left|{x + 2}\\right|^{3} \\le f(x) \\le 4 \\left|{x + 2}\\right|^{3} + 2 \\) for \\( x \\ne -2 \\) and both bounds approach 2 as x approaches -2.",
      "The limit is 2, because \\( 2 - 4 \\left|{x + 2}\\right|^{3} \\le f(x) \\le 4 \\left|{x + 2}\\right|^{3} + 2 \\) for \\( x \\ne -2 \\) and both bounds equal 2 when x is -2.",
      "The limit is 2, because \\( 4 \\left(x + 2\\right)^{3} + 2 \\le f(x) \\le - 4 \\left(x + 2\\right)^{3} + 2 \\) for \\( x \\ne -2 \\) and both bounds approach 2 as x approaches -2.",
   ],
   "01005-08": [
      "The limit is 2, because \\( - 4 \\left(x + 3\\right) \\) approaches 0 as x approaches -3 and the limit of a product is the product of the limits.",
      "The limit is 2, because \\( 2 - 4 \\left|{x + 3}\\right| \\le f(x) \\le 4 \\left|{x + 3}\\right| + 2 \\) for \\( x \\ne -3 \\) and both bounds approach 2 as x approaches -3.",
      "The limit is 2, because \\( 2 - 4 \\left|{x + 3}\\right| \\le f(x) \\le 4 \\left|{x + 3}\\right| + 2 \\) for \\( x \\ne -3 \\) and both bounds equal 2 when x is -3.",
      "The limit is 2, because \\( 4 \\left(x + 3\\right) + 2 \\le f(x) \\le - 4 \\left(x + 3\\right) + 2 \\) for \\( x \\ne -3 \\) and both bounds approach 2 as x approaches -3.",
   ],
   "01005-09": [
      "The limit is -3, because \\( - \\left(x + 3\\right)^{3} \\) approaches 0 as x approaches -3 and the limit of a product is the product of the limits.",
      "The limit is -3, because \\( -3 - \\left|{x + 3}\\right|^{3} \\le f(x) \\le \\left|{x + 3}\\right|^{3} - 3 \\) for \\( x \\ne -3 \\) and both bounds approach -3 as x approaches -3.",
      "The limit is -3, because \\( -3 - \\left|{x + 3}\\right|^{3} \\le f(x) \\le \\left|{x + 3}\\right|^{3} - 3 \\) for \\( x \\ne -3 \\) and both bounds equal -3 when x is -3.",
      "The limit is -3, because \\( 1 \\left(x + 3\\right)^{3} - 3 \\le f(x) \\le - \\left(x + 3\\right)^{3} - 3 \\) for \\( x \\ne -3 \\) and both bounds approach -3 as x approaches -3.",
   ],
   "01005-10": [
      "The limit is 2, because \\( - \\left(x - 2\\right)^{3} + 2 \\le f(x) \\le 1 \\left(x - 2\\right)^{3} + 2 \\) for \\( x \\ne 2 \\) and both bounds approach 2 as x approaches 2.",
      "The limit is 2, because \\( 1 \\left(x - 2\\right)^{3} \\) approaches 0 as x approaches 2 and the limit of a product is the product of the limits.",
      "The limit is 2, because \\( 2 - \\left|{x - 2}\\right|^{3} \\le f(x) \\le \\left|{x - 2}\\right|^{3} + 2 \\) for \\( x \\ne 2 \\) and both bounds approach 2 as x approaches 2.",
      "The limit is 2, because \\( 2 - \\left|{x - 2}\\right|^{3} \\le f(x) \\le \\left|{x - 2}\\right|^{3} + 2 \\) for \\( x \\ne 2 \\) and both bounds equal 2 when x is 2.",
   ],
   "01005-11": [
      "The limit is -1, because \\( - 2 x^{3} - 1 \\le f(x) \\le 2 x^{3} - 1 \\) for \\( x \\ne 0 \\) and both bounds approach -1 as x approaches 0.",
      "The limit is -1, because \\( -1 - 2 \\left|{x}\\right|^{3} \\le f(x) \\le 2 \\left|{x}\\right|^{3} - 1 \\) for \\( x \\ne 0 \\) and both bounds approach -1 as x approaches 0.",
      "The limit is -1, because \\( -1 - 2 \\left|{x}\\right|^{3} \\le f(x) \\le 2 \\left|{x}\\right|^{3} - 1 \\) for \\( x \\ne 0 \\) and both bounds equal -1 when x is 0.",
      "The limit is -1, because \\( 2 x^{3} \\) approaches 0 as x approaches 0 and the limit of a product is the product of the limits.",
   ],
   "01005-12": [
      "The limit is 2, because \\( - 3 \\left(x + 1\\right)^{3} \\) approaches 0 as x approaches -1 and the limit of a product is the product of the limits.",
      "The limit is 2, because \\( 2 - 3 \\left|{x + 1}\\right|^{3} \\le f(x) \\le 3 \\left|{x + 1}\\right|^{3} + 2 \\) for \\( x \\ne -1 \\) and both bounds approach 2 as x approaches -1.",
      "The limit is 2, because \\( 2 - 3 \\left|{x + 1}\\right|^{3} \\le f(x) \\le 3 \\left|{x + 1}\\right|^{3} + 2 \\) for \\( x \\ne -1 \\) and both bounds equal 2 when x is -1.",
      "The limit is 2, because \\( 3 \\left(x + 1\\right)^{3} + 2 \\le f(x) \\le - 3 \\left(x + 1\\right)^{3} + 2 \\) for \\( x \\ne -1 \\) and both bounds approach 2 as x approaches -1.",
   ],
   "01005-13": [
      "The limit is 1, because \\( - 3 \\left(x + 3\\right)^{2} \\) approaches 0 as x approaches -3 and the limit of a product is the product of the limits.",
      "The limit is 1, because \\( 1 - 3 \\left(x + 3\\right)^{2} \\le f(x) \\le 3 \\left(x + 3\\right)^{2} + 1 \\) for \\( x \\ne -3 \\) and both bounds approach 1 as x approaches -3.",
      "The limit is 1, because \\( 1 - 3 \\left(x + 3\\right)^{2} \\le f(x) \\le 3 \\left(x + 3\\right)^{2} + 1 \\) for \\( x \\ne -3 \\) and both bounds equal 1 when x is -3.",
      "The limit is 1, because \\( 3 \\left(x + 3\\right)^{2} + 1 \\le f(x) \\le - 3 \\left(x + 3\\right)^{2} + 1 \\) for \\( x \\ne -3 \\) and both bounds approach 1 as x approaches -3.",
   ],
   "01005-14": [
      "The limit is -1, because \\( - 2 \\left(x - 1\\right) \\) approaches 0 as x approaches 1 and the limit of a product is the product of the limits.",
      "The limit is -1, because \\( -1 - 2 \\left|{x - 1}\\right| \\le f(x) \\le 2 \\left|{x - 1}\\right| - 1 \\) for \\( x \\ne 1 \\) and both bounds approach -1 as x approaches 1.",
      "The limit is -1, because \\( -1 - 2 \\left|{x - 1}\\right| \\le f(x) \\le 2 \\left|{x - 1}\\right| - 1 \\) for \\( x \\ne 1 \\) and both bounds equal -1 when x is 1.",
      "The limit is -1, because \\( 2 \\left(x - 1\\right) - 1 \\le f(x) \\le - 2 \\left(x - 1\\right) - 1 \\) for \\( x \\ne 1 \\) and both bounds approach -1 as x approaches 1.",
   ],
   "01005-15": [
      "The limit is -3, because \\( - 4 \\left(x - 1\\right)^{3} - 3 \\le f(x) \\le 4 \\left(x - 1\\right)^{3} - 3 \\) for \\( x \\ne 1 \\) and both bounds approach -3 as x approaches 1.",
      "The limit is -3, because \\( -3 - 4 \\left|{x - 1}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 1}\\right|^{3} - 3 \\) for \\( x \\ne 1 \\) and both bounds approach -3 as x approaches 1.",
      "The limit is -3, because \\( -3 - 4 \\left|{x - 1}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 1}\\right|^{3} - 3 \\) for \\( x \\ne 1 \\) and both bounds equal -3 when x is 1.",
      "The limit is -3, because \\( 4 \\left(x - 1\\right)^{3} \\) approaches 0 as x approaches 1 and the limit of a product is the product of the limits.",
   ],
   "01005-16": [
      "The limit is 4, because \\( - 2 \\left(x - 1\\right)^{3} \\) approaches 0 as x approaches 1 and the limit of a product is the product of the limits.",
      "The limit is 4, because \\( 2 \\left(x - 1\\right)^{3} + 4 \\le f(x) \\le - 2 \\left(x - 1\\right)^{3} + 4 \\) for \\( x \\ne 1 \\) and both bounds approach 4 as x approaches 1.",
      "The limit is 4, because \\( 4 - 2 \\left|{x - 1}\\right|^{3} \\le f(x) \\le 2 \\left|{x - 1}\\right|^{3} + 4 \\) for \\( x \\ne 1 \\) and both bounds approach 4 as x approaches 1.",
      "The limit is 4, because \\( 4 - 2 \\left|{x - 1}\\right|^{3} \\le f(x) \\le 2 \\left|{x - 1}\\right|^{3} + 4 \\) for \\( x \\ne 1 \\) and both bounds equal 4 when x is 1.",
   ],
   "01005-17": [
      "The limit is -1, because \\( - x^{2} \\) approaches 0 as x approaches 0 and the limit of a product is the product of the limits.",
      "The limit is -1, because \\( -1 - x^{2} \\le f(x) \\le x^{2} - 1 \\) for \\( x \\ne 0 \\) and both bounds approach -1 as x approaches 0.",
      "The limit is -1, because \\( -1 - x^{2} \\le f(x) \\le x^{2} - 1 \\) for \\( x \\ne 0 \\) and both bounds equal -1 when x is 0.",
      "The limit is -1, because \\( 1 x^{2} - 1 \\le f(x) \\le - x^{2} - 1 \\) for \\( x \\ne 0 \\) and both bounds approach -1 as x approaches 0.",
   ],
   "01005-18": [
      "The limit is 2, because \\( - 3 \\left(x - 2\\right) + 2 \\le f(x) \\le 3 \\left(x - 2\\right) + 2 \\) for \\( x \\ne 2 \\) and both bounds approach 2 as x approaches 2.",
      "The limit is 2, because \\( 2 - 3 \\left|{x - 2}\\right| \\le f(x) \\le 3 \\left|{x - 2}\\right| + 2 \\) for \\( x \\ne 2 \\) and both bounds approach 2 as x approaches 2.",
      "The limit is 2, because \\( 2 - 3 \\left|{x - 2}\\right| \\le f(x) \\le 3 \\left|{x - 2}\\right| + 2 \\) for \\( x \\ne 2 \\) and both bounds equal 2 when x is 2.",
      "The limit is 2, because \\( 3 \\left(x - 2\\right) \\) approaches 0 as x approaches 2 and the limit of a product is the product of the limits.",
   ],
   "01005-19": [
      "The limit is 2, because \\( - 2 \\left(x - 3\\right)^{3} \\) approaches 0 as x approaches 3 and the limit of a product is the product of the limits.",
      "The limit is 2, because \\( 2 - 2 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 2 \\left|{x - 3}\\right|^{3} + 2 \\) for \\( x \\ne 3 \\) and both bounds approach 2 as x approaches 3.",
      "The limit is 2, because \\( 2 - 2 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 2 \\left|{x - 3}\\right|^{3} + 2 \\) for \\( x \\ne 3 \\) and both bounds equal 2 when x is 3.",
      "The limit is 2, because \\( 2 \\left(x - 3\\right)^{3} + 2 \\le f(x) \\le - 2 \\left(x - 3\\right)^{3} + 2 \\) for \\( x \\ne 3 \\) and both bounds approach 2 as x approaches 3.",
   ],
   "01005-20": [
      "The limit is 0, because \\( - 4 \\left(x - 3\\right)^{3} \\) approaches 0 as x approaches 3 and the limit of a product is the product of the limits.",
      "The limit is 0, because \\( -4 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 3}\\right|^{3} \\) for \\( x \\ne 3 \\) and both bounds approach 0 as x approaches 3.",
      "The limit is 0, because \\( -4 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 3}\\right|^{3} \\) for \\( x \\ne 3 \\) and both bounds equal 0 when x is 3.",
      "The limit is 0, because \\( 4 \\left(x - 3\\right)^{3} \\le f(x) \\le - 4 \\left(x - 3\\right)^{3} \\) for \\( x \\ne 3 \\) and both bounds approach 0 as x approaches 3.",
   ],
   "01005-21": [
      "The limit is 4, because \\( - 4 \\left(x - 3\\right)^{3} + 4 \\le f(x) \\le 4 \\left(x - 3\\right)^{3} + 4 \\) for \\( x \\ne 3 \\) and both bounds approach 4 as x approaches 3.",
      "The limit is 4, because \\( 4 - 4 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 3}\\right|^{3} + 4 \\) for \\( x \\ne 3 \\) and both bounds approach 4 as x approaches 3.",
      "The limit is 4, because \\( 4 - 4 \\left|{x - 3}\\right|^{3} \\le f(x) \\le 4 \\left|{x - 3}\\right|^{3} + 4 \\) for \\( x \\ne 3 \\) and both bounds equal 4 when x is 3.",
      "The limit is 4, because \\( 4 \\left(x - 3\\right)^{3} \\) approaches 0 as x approaches 3 and the limit of a product is the product of the limits.",
   ],
   "01006-00": [
      "f is continuous at \\( x = 3 \\), because the limit of f(x) there is 4, which equals f(3).",
      "f is continuous at \\( x = 3 \\), because the limits from the left and from the right are both -4.",
      "f is not continuous at \\( x = 3 \\), because the limit of f(x) there is -4 while f(3) = 4.",
      "f is not continuous at \\( x = 3 \\), because the quotient gives 0/0 at \\( x = 3 \\), so f(3) is undefined.",
   ],
   "01006-01": [
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is 4, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both -3.",
      "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is -3 while f(1) = 4.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-02": [
      "f is continuous at \\( x = 1 \\), because f(1) = 4 is defined, so f has a value at \\( x = 1 \\).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both 4.",
      "f is not continuous at \\( x = 1 \\), because it does not equal it there, so it cannot be continuous at \\( x = 1 \\).",
      "f is not continuous at \\( x = 1 \\), because the limits from the left and from the right are 4 and 3.",
   ],
   "01006-03": [
      "f is continuous at \\( x = -2 \\), because the limit of f(x) there is 1, which equals f(-2).",
      "f is continuous at \\( x = -2 \\), because the limits from the left and from the right are both 4.",
      "f is not continuous at \\( x = -2 \\), because the limit of f(x) there is 4 while f(-2) = 1.",
      "f is not continuous at \\( x = -2 \\), because the quotient gives 0/0 at \\( x = -2 \\), so f(-2) is undefined.",
   ],
   "01006-04": [
      "f is continuous at \\( x = -1 \\), because the limit of f(x) there is 3, which equals f(-1).",
      "f is continuous at \\( x = -1 \\), because the limits from the left and from the right are both 2.",
      "f is not continuous at \\( x = -1 \\), because the limit of f(x) there is 2 while f(-1) = 3.",
      "f is not continuous at \\( x = -1 \\), because the quotient gives 0/0 at \\( x = -1 \\), so f(-1) is undefined.",
   ],
   "01006-05": [
      "f is continuous at \\( x = 3 \\), because the limit of f(x) there is 3, which equals f(3).",
      "f is continuous at \\( x = 3 \\), because the limits from the left and from the right are both -4.",
      "f is not continuous at \\( x = 3 \\), because the limit of f(x) there is -4 while f(3) = 3.",
      "f is not continuous at \\( x = 3 \\), because the quotient gives 0/0 at \\( x = 3 \\), so f(3) is undefined.",
   ],
   "01006-06": [
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is 0, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both 3.",
      "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is 3 while f(1) = 0.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-07": [
      "f is continuous at \\( x = -1 \\), because f(-1) = 0 is defined, so f has a value at \\( x = -1 \\).",
      "f is continuous at \\( x = -1 \\), because the limit of f(x) there is 0, which equals f(-1).",
      "f is continuous at \\( x = -1 \\), because the limits from the left and from the right are both 0.",
      "f is not continuous at \\( x = -1 \\), because the quotient gives 0/0 at \\( x = -1 \\), so f(-1) is undefined.",
   ],
   "01006-08": [
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is -4, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both 0.",
      "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is 0 while f(1) = -4.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-09": [
      "f is continuous at \\( x = -1 \\), because f(-1) = 4 is defined, so f has a value at \\( x = -1 \\).",
      "f is continuous at \\( x = -1 \\), because the limit of f(x) there is 4, which equals f(-1).",
      "f is continuous at \\( x = -1 \\), because the limits from the left and from the right are both 4.",
      "f is not continuous at \\( x = -1 \\), because the quotient gives 0/0 at \\( x = -1 \\), so f(-1) is undefined.",
   ],
   "01006-10": [
      "f is continuous at \\( x = 0 \\), because the limit of f(x) there is 0, which equals f(0).",
      "f is continuous at \\( x = 0 \\), because the limits from the left and from the right are both 1.",
      "f is not continuous at \\( x = 0 \\), because the limit of f(x) there is 1 while f(0) = 0.",
      "f is not continuous at \\( x = 0 \\), because the quotient gives 0/0 at \\( x = 0 \\), so f(0) is undefined.",
   ],
   "01006-11": [
      "f is continuous at \\( x = 3 \\), because f(3) = 3 is defined, so f has a value at \\( x = 3 \\).",
      "f is continuous at \\( x = 3 \\), because the limit of f(x) there is 3, which equals f(3).",
      "f is continuous at \\( x = 3 \\), because the limits from the left and from the right are both 3.",
      "f is not continuous at \\( x = 3 \\), because the quotient gives 0/0 at \\( x = 3 \\), so f(3) is undefined.",
   ],
   "01006-12": [
      "f is continuous at \\( x = 1 \\), because f(1) = -2 is defined, so f has a value at \\( x = 1 \\).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both -2.",
      "f is not continuous at \\( x = 1 \\), because it does not equal it there, so it cannot be continuous at \\( x = 1 \\).",
      "f is not continuous at \\( x = 1 \\), because the limits from the left and from the right are 2 and -2.",
   ],
   "01006-13": [
      "f is continuous at \\( x = -2 \\), because the limit of f(x) there is -4, which equals f(-2).",
      "f is continuous at \\( x = -2 \\), because the limits from the left and from the right are both 4.",
      "f is not continuous at \\( x = -2 \\), because the limit of f(x) there is 4 while f(-2) = -4.",
      "f is not continuous at \\( x = -2 \\), because the quotient gives 0/0 at \\( x = -2 \\), so f(-2) is undefined.",
   ],
   "01006-14": [
      "f is continuous at \\( x = 0 \\), because the limit of f(x) there is -2, which equals f(0).",
      "f is continuous at \\( x = 0 \\), because the limits from the left and from the right are both -3.",
      "f is not continuous at \\( x = 0 \\), because the limit of f(x) there is -3 while f(0) = -2.",
      "f is not continuous at \\( x = 0 \\), because the quotient gives 0/0 at \\( x = 0 \\), so f(0) is undefined.",
   ],
   "01006-15": [
      "f is continuous at \\( x = 3 \\), because the limit of f(x) there is 1, which equals f(3).",
      "f is continuous at \\( x = 3 \\), because the limits from the left and from the right are both 3.",
      "f is not continuous at \\( x = 3 \\), because the limit of f(x) there is 3 while f(3) = 1.",
      "f is not continuous at \\( x = 3 \\), because the quotient gives 0/0 at \\( x = 3 \\), so f(3) is undefined.",
   ],
   "01006-16": [
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is -2, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both 3.",
      "f is not continuous at \\( x = 1 \\), because the limit of f(x) there is 3 while f(1) = -2.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-17": [
      "f is continuous at \\( x = -1 \\), because f(-1) = -1 is defined, so f has a value at \\( x = -1 \\).",
      "f is continuous at \\( x = -1 \\), because the limits from the left and from the right are both -1.",
      "f is not continuous at \\( x = -1 \\), because it does not equal it there, so it cannot be continuous at \\( x = -1 \\).",
      "f is not continuous at \\( x = -1 \\), because the limits from the left and from the right are 1 and -1.",
   ],
   "01006-18": [
      "f is continuous at \\( x = 1 \\), because f(1) = 0 is defined, so f has a value at \\( x = 1 \\).",
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is 0, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both 0.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-19": [
      "f is continuous at \\( x = 1 \\), because f(1) = -1 is defined, so f has a value at \\( x = 1 \\).",
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is -1, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both -1.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-20": [
      "f is continuous at \\( x = 1 \\), because f(1) = -3 is defined, so f has a value at \\( x = 1 \\).",
      "f is continuous at \\( x = 1 \\), because the limit of f(x) there is -3, which equals f(1).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both -3.",
      "f is not continuous at \\( x = 1 \\), because the quotient gives 0/0 at \\( x = 1 \\), so f(1) is undefined.",
   ],
   "01006-21": [
      "f is continuous at \\( x = 1 \\), because f(1) = 2 is defined, so f has a value at \\( x = 1 \\).",
      "f is continuous at \\( x = 1 \\), because the limits from the left and from the right are both 2.",
      "f is not continuous at \\( x = 1 \\), because it does not equal it there, so it cannot be continuous at \\( x = 1 \\).",
      "f is not continuous at \\( x = 1 \\), because the limits from the left and from the right are 2 and -4.",
   ],
   "01007-00": [
      "The discontinuity at \\( x = 3 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 3 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = 3 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = 3 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-01": [
      "The discontinuity at \\( x = 0 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 0 \\) is a vertical asymptote, because f(x) is unbounded as x approaches 0.",
      "The discontinuity at \\( x = 0 \\) is removable, because the limit of f(x) there exists and equals \\( \\infty \\).",
      "There is no discontinuity at \\( x = 0 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-02": [
      "The discontinuity at \\( x = 1 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 1 \\) is a vertical asymptote, because f(x) is unbounded as x approaches 1.",
      "The discontinuity at \\( x = 1 \\) is removable, because the limit of f(x) there exists and equals \\( -\\infty \\).",
      "There is no discontinuity at \\( x = 1 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-03": [
      "The discontinuity at \\( x = -3 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -3 \\) is a vertical asymptote, because f(x) is unbounded as x approaches -3.",
      "The discontinuity at \\( x = -3 \\) is removable, because the limit of f(x) there exists and equals \\( -\\infty \\).",
      "There is no discontinuity at \\( x = -3 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-04": [
      "The discontinuity at \\( x = -3 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -3 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = -3 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = -3 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-05": [
      "The discontinuity at \\( x = -1 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -1 \\) is a vertical asymptote, because f(x) is unbounded as x approaches -1.",
      "The discontinuity at \\( x = -1 \\) is removable, because the limit of f(x) there exists and equals \\( -\\infty \\).",
      "There is no discontinuity at \\( x = -1 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-06": [
      "The discontinuity at \\( x = 4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 4 \\) is a vertical asymptote, because f(x) is unbounded as x approaches 4.",
      "The discontinuity at \\( x = 4 \\) is removable, because the limit of f(x) there exists and equals \\( \\infty \\).",
      "There is no discontinuity at \\( x = 4 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-07": [
      "The discontinuity at \\( x = -4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -4 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = -4 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = -4 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-08": [
      "The discontinuity at \\( x = -2 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -2 \\) is a vertical asymptote, because f(x) is unbounded as x approaches -2.",
      "The discontinuity at \\( x = -2 \\) is removable, because the limit of f(x) there exists and equals \\( -\\infty \\).",
      "There is no discontinuity at \\( x = -2 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-09": [
      "The discontinuity at \\( x = 4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 4 \\) is a vertical asymptote, because f(x) is unbounded as x approaches 4.",
      "The discontinuity at \\( x = 4 \\) is removable, because the limit of f(x) there exists and equals \\( -\\infty \\).",
      "There is no discontinuity at \\( x = 4 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-10": [
      "The discontinuity at \\( x = -3 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -3 \\) is a vertical asymptote, because f(x) is unbounded as x approaches -3.",
      "The discontinuity at \\( x = -3 \\) is removable, because the limit of f(x) there exists and equals \\( \\infty \\).",
      "There is no discontinuity at \\( x = -3 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-11": [
      "The discontinuity at \\( x = -4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -4 \\) is a vertical asymptote, because f(x) is unbounded as x approaches -4.",
      "The discontinuity at \\( x = -4 \\) is removable, because the limit of f(x) there exists and equals \\( -\\infty \\).",
      "There is no discontinuity at \\( x = -4 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-12": [
      "The discontinuity at \\( x = -4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -4 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = -4 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = -4 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-13": [
      "The discontinuity at \\( x = 4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 4 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = 4 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = 4 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-14": [
      "The discontinuity at \\( x = 1 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 1 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = 1 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = 1 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-15": [
      "The discontinuity at \\( x = 2 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 2 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = 2 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = 2 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-16": [
      "The discontinuity at \\( x = -1 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -1 \\) is a vertical asymptote, because f(x) is unbounded as x approaches -1.",
      "The discontinuity at \\( x = -1 \\) is removable, because the limit of f(x) there exists and equals \\( \\infty \\).",
      "There is no discontinuity at \\( x = -1 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-17": [
      "The discontinuity at \\( x = 1 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 1 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = 1 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = 1 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-18": [
      "The discontinuity at \\( x = -1 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -1 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = -1 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = -1 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-19": [
      "The discontinuity at \\( x = 0 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = 0 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = 0 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = 0 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-20": [
      "The discontinuity at \\( x = -3 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -3 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = -3 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = -3 \\), because the limits from the left and from the right are equal.",
   ],
   "01007-21": [
      "The discontinuity at \\( x = -4 \\) is a jump, because f is undefined there so the limit does not exist.",
      "The discontinuity at \\( x = -4 \\) is a vertical asymptote, because the denominator of f is 0 there.",
      "The discontinuity at \\( x = -4 \\) is removable, because the limit of f(x) there is a finite number.",
      "There is no discontinuity at \\( x = -4 \\), because the limits from the left and from the right are equal.",
   ],
   "01008-00": [
      "No values of k and m work, because \\( \\frac{x^{2} - 9}{x - 3} \\) is undefined at \\( x = 3 \\), so f has no limit there.",
      "\\( k = -14 \\) and \\( m = 16 \\), because the middle branch must equal -26 at \\( x = 3 \\) and -40 at \\( x = 4 \\).",
      "\\( k = -46 \\) and \\( m = 144 \\), because the middle branch must equal 6 at \\( x = 3 \\) and -40 at \\( x = 4 \\).",
      "\\( k = 1 \\) and \\( m = 3 \\), because the middle branch must equal 6 at \\( x = 3 \\) and 7 at \\( x = 4 \\).",
   ],
   "01008-01": [
      "No values of k and m work, because \\( \\frac{x^{2} - 4}{x - 2} \\) is undefined at \\( x = 2 \\), so f has no limit there.",
      "\\( k = -13 \\) and \\( m = 30 \\), because the middle branch must equal 4 at \\( x = 2 \\) and -9 at \\( x = 3 \\).",
      "\\( k = -5 \\) and \\( m = 6 \\), because the middle branch must equal -4 at \\( x = 2 \\) and -9 at \\( x = 3 \\).",
      "\\( k = 1 \\) and \\( m = 2 \\), because the middle branch must equal 4 at \\( x = 2 \\) and 5 at \\( x = 3 \\).",
   ],
   "01008-02": [
      "No values of k and m work, because \\( \\frac{x^{2} - 9}{x + 3} \\) is undefined at \\( x = -3 \\), so f has no limit there.",
      "\\( k = -12 \\) and \\( m = 0 \\), because the middle branch must equal 36 at \\( x = -3 \\) and 12 at \\( x = -1 \\).",
      "\\( k = 1 \\) and \\( m = -3 \\), because the middle branch must equal -6 at \\( x = -3 \\) and -4 at \\( x = -1 \\).",
      "\\( k = 9 \\) and \\( m = 21 \\), because the middle branch must equal -6 at \\( x = -3 \\) and 12 at \\( x = -1 \\).",
   ],
   "01008-03": [
      "No values of k and m work, because \\( \\frac{x^{2} - 4}{x + 2} \\) is undefined at \\( x = -2 \\), so f has no limit there.",
      "\\( k = -3 \\) and \\( m = -7 \\), because the middle branch must equal -1 at \\( x = -2 \\) and -4 at \\( x = -1 \\).",
      "\\( k = 0 \\) and \\( m = -4 \\), because the middle branch must equal -4 at \\( x = -2 \\) and -4 at \\( x = -1 \\).",
      "\\( k = 1 \\) and \\( m = -2 \\), because the middle branch must equal -4 at \\( x = -2 \\) and -3 at \\( x = -1 \\).",
   ],
   "01008-04": [
      "No values of k and m work, because \\( \\frac{x^{2} - 9}{x + 3} \\) is undefined at \\( x = -3 \\), so f has no limit there.",
      "\\( k = 1 \\) and \\( m = -3 \\), because the middle branch must equal -6 at \\( x = -3 \\) and 2 at \\( x = 5 \\).",
      "\\( k = 6 \\) and \\( m = 36 \\), because the middle branch must equal 18 at \\( x = -3 \\) and 66 at \\( x = 5 \\).",
      "\\( k = 9 \\) and \\( m = 21 \\), because the middle branch must equal -6 at \\( x = -3 \\) and 66 at \\( x = 5 \\).",
   ],
   "01008-05": [
      "No values of k and m work, because \\( \\frac{x^{2} - 16}{x + 4} \\) is undefined at \\( x = -4 \\), so f has no limit there.",
      "\\( k = -12 \\) and \\( m = -14 \\), because the middle branch must equal 34 at \\( x = -4 \\) and 10 at \\( x = -2 \\).",
      "\\( k = 1 \\) and \\( m = -4 \\), because the middle branch must equal -8 at \\( x = -4 \\) and -6 at \\( x = -2 \\).",
      "\\( k = 9 \\) and \\( m = 28 \\), because the middle branch must equal -8 at \\( x = -4 \\) and 10 at \\( x = -2 \\).",
   ],
   "01008-06": [
      "No values of k and m work, because \\( \\frac{x^{2} - 16}{x + 4} \\) is undefined at \\( x = -4 \\), so f has no limit there.",
      "\\( k = -14 \\) and \\( m = -32 \\), because the middle branch must equal 24 at \\( x = -4 \\) and 10 at \\( x = -3 \\).",
      "\\( k = 1 \\) and \\( m = -4 \\), because the middle branch must equal -8 at \\( x = -4 \\) and -7 at \\( x = -3 \\).",
      "\\( k = 18 \\) and \\( m = 64 \\), because the middle branch must equal -8 at \\( x = -4 \\) and 10 at \\( x = -3 \\).",
   ],
   "01008-07": [
      "No values of k and m work, because \\( \\frac{x^{2} - 1}{x - 1} \\) is undefined at \\( x = 1 \\), so f has no limit there.",
      "\\( k = -10 \\) and \\( m = 12 \\), because the middle branch must equal 2 at \\( x = 1 \\) and -8 at \\( x = 2 \\).",
      "\\( k = -6 \\) and \\( m = 4 \\), because the middle branch must equal -2 at \\( x = 1 \\) and -8 at \\( x = 2 \\).",
      "\\( k = 1 \\) and \\( m = 1 \\), because the middle branch must equal 2 at \\( x = 1 \\) and 3 at \\( x = 2 \\).",
   ],
   "01008-08": [
      "No values of k and m work, because \\( \\frac{x^{2} - 25}{x + 5} \\) is undefined at \\( x = -5 \\), so f has no limit there.",
      "\\( k = -9 \\) and \\( m = -26 \\), because the middle branch must equal 19 at \\( x = -5 \\) and 10 at \\( x = -4 \\).",
      "\\( k = 1 \\) and \\( m = -5 \\), because the middle branch must equal -10 at \\( x = -5 \\) and -9 at \\( x = -4 \\).",
      "\\( k = 20 \\) and \\( m = 90 \\), because the middle branch must equal -10 at \\( x = -5 \\) and 10 at \\( x = -4 \\).",
   ],
   "01008-09": [
      "No values of k and m work, because \\( \\frac{x^{2} - 25}{x - 5} \\) is undefined at \\( x = 5 \\), so f has no limit there.",
      "\\( k = -22 \\) and \\( m = 56 \\), because the middle branch must equal -54 at \\( x = 5 \\) and -76 at \\( x = 6 \\).",
      "\\( k = -86 \\) and \\( m = 440 \\), because the middle branch must equal 10 at \\( x = 5 \\) and -76 at \\( x = 6 \\).",
      "\\( k = 1 \\) and \\( m = 5 \\), because the middle branch must equal 10 at \\( x = 5 \\) and 11 at \\( x = 6 \\).",
   ],
   "01008-10": [
      "No values of k and m work, because \\( \\frac{x^{2} - 25}{x + 5} \\) is undefined at \\( x = -5 \\), so f has no limit there.",
      "\\( k = -27 \\) and \\( m = -53 \\), because the middle branch must equal 82 at \\( x = -5 \\) and 55 at \\( x = -4 \\).",
      "\\( k = 1 \\) and \\( m = -5 \\), because the middle branch must equal -10 at \\( x = -5 \\) and -9 at \\( x = -4 \\).",
      "\\( k = 65 \\) and \\( m = 315 \\), because the middle branch must equal -10 at \\( x = -5 \\) and 55 at \\( x = -4 \\).",
   ],
   "01008-11": [
      "No values of k and m work, because \\( \\frac{x^{2} - 9}{x - 3} \\) is undefined at \\( x = 3 \\), so f has no limit there.",
      "\\( k = -14 \\) and \\( m = 21 \\), because the middle branch must equal -21 at \\( x = 3 \\) and -35 at \\( x = 4 \\).",
      "\\( k = -41 \\) and \\( m = 129 \\), because the middle branch must equal 6 at \\( x = 3 \\) and -35 at \\( x = 4 \\).",
      "\\( k = 1 \\) and \\( m = 3 \\), because the middle branch must equal 6 at \\( x = 3 \\) and 7 at \\( x = 4 \\).",
   ],
   "01009-00": [
      "Both \\( x = 0 \\) and \\( x = -1 \\) are vertical asymptotes, with \\( \\lim_{x \\to -1^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to -1^{+}} f(x) = \\infty \\).",
      "No line is a vertical asymptote, because \\( \\lim_{x \\to -1^{+}} f(x) = \\infty \\) is a limit that exists at \\( x = -1 \\).",
      "Only \\( x = -1 \\) is a vertical asymptote, with \\( \\lim_{x \\to -1^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to -1^{+}} f(x) = \\infty \\).",
      "Only \\( x = -1 \\) is a vertical asymptote, with \\( \\lim_{x \\to -1} f(x) = \\infty \\) from both sides.",
   ],
   "01009-01": [
      "Both \\( x = -1 \\) and \\( x = -4 \\) are vertical asymptotes, with \\( \\lim_{x \\to -4^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to -4^{+}} f(x) = \\infty \\).",
      "No line is a vertical asymptote, because \\( \\lim_{x \\to -4^{+}} f(x) = \\infty \\) is a limit that exists at \\( x = -4 \\).",
      "Only \\( x = -4 \\) is a vertical asymptote, with \\( \\lim_{x \\to -4^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to -4^{+}} f(x) = \\infty \\).",
      "Only \\( x = -4 \\) is a vertical asymptote, with \\( \\lim_{x \\to -4} f(x) = \\infty \\) from both sides.",
   ],
   "01009-02": [
      "Both \\( x = 3 \\) and \\( x = 1 \\) are vertical asymptotes, with \\( \\lim_{x \\to 1^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to 1^{+}} f(x) = \\infty \\).",
      "No line is a vertical asymptote, because \\( \\lim_{x \\to 1^{+}} f(x) = \\infty \\) is a limit that exists at \\( x = 1 \\).",
      "Only \\( x = 1 \\) is a vertical asymptote, with \\( \\lim_{x \\to 1^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to 1^{+}} f(x) = \\infty \\).",
      "Only \\( x = 1 \\) is a vertical asymptote, with \\( \\lim_{x \\to 1} f(x) = \\infty \\) from both sides.",
   ],
   "01009-03": [
      "Both \\( x = 3 \\) and \\( x = -3 \\) are vertical asymptotes, with \\( \\lim_{x \\to -3^{-}} f(x) = \\infty \\) and \\( \\lim_{x \\to -3^{+}} f(x) = -\\infty \\).",
      "No line is a vertical asymptote, because \\( \\lim_{x \\to -3^{+}} f(x) = -\\infty \\) is a limit that exists at \\( x = -3 \\).",
      "Only \\( x = -3 \\) is a vertical asymptote, with \\( \\lim_{x \\to -3^{-}} f(x) = \\infty \\) and \\( \\lim_{x \\to -3^{+}} f(x) = -\\infty \\).",
      "Only \\( x = -3 \\) is a vertical asymptote, with \\( \\lim_{x \\to -3} f(x) = -\\infty \\) from both sides.",
   ],
   "01009-04": [
      "Both \\( x = 0 \\) and \\( x = 4 \\) are vertical asymptotes, with \\( \\lim_{x \\to 4^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to 4^{+}} f(x) = \\infty \\).",
      "No line is a vertical asymptote, because \\( \\lim_{x \\to 4^{+}} f(x) = \\infty \\) is a limit that exists at \\( x = 4 \\).",
      "Only \\( x = 4 \\) is a vertical asymptote, with \\( \\lim_{x \\to 4^{-}} f(x) = -\\infty \\) and \\( \\lim_{x \\to 4^{+}} f(x) = \\infty \\).",
      "Only \\( x = 4 \\) is a vertical asymptote, with \\( \\lim_{x \\to 4} f(x) = \\infty \\) from both sides.",
   ],
   "01011-00": [
      "Yes. Since \\( f(2) = -6 < -2 < f(9) = 6 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [2, 9] \\), and \\( f(2) = -6 < -2 < f(9) = 6 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 9] \\), and \\( f(2) = -6 < -2 < f(9) = 6 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 9] \\), and \\( f(2) = -6 < -2 < f(9) = 6 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-01": [
      "No. Every tabulated value of f is greater than -2, so the Intermediate Value Theorem does not apply on \\( [1, 7] \\).",
      "Yes. A continuous function on \\( [1, 7] \\) takes every value between its values, so f takes the value -2.",
      "Yes. Since f is differentiable on \\( [1, 7] \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [1, 7] \\), so the Intermediate Value Theorem gives at least one such c.",
   ],
   "01011-02": [
      "Yes. Since \\( f(0) = -9 < -2 < f(7) = 5 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [0, 7] \\), and \\( f(0) = -9 < -2 < f(7) = 5 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), and \\( f(0) = -9 < -2 < f(7) = 5 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), and \\( f(0) = -9 < -2 < f(7) = 5 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-03": [
      "No. Although f is continuous on \\( [1, 8] \\), -4 is not between \\( f(1) = -7 \\) and \\( f(8) = -8 \\), so no such c must exist.",
      "Yes. Since \\( f(3) = -7 < -4 < f(6) = 0 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 6] \\), and \\( f(3) = -7 < -4 < f(6) = 0 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 6] \\), and \\( f(3) = -7 < -4 < f(6) = 0 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-04": [
      "Yes. Since \\( f(9) = -7 < 3 < f(4) = 4 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [4, 9] \\), and \\( f(9) = -7 < 3 < f(4) = 4 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [4, 9] \\), and \\( f(9) = -7 < 3 < f(4) = 4 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [4, 9] \\), and \\( f(9) = -7 < 3 < f(4) = 4 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-05": [
      "No. Every tabulated value of f is greater than -4, so the Intermediate Value Theorem does not apply on \\( [2, 9] \\).",
      "Yes. A continuous function on \\( [2, 9] \\) takes every value between its values, so f takes the value -4.",
      "Yes. Since f is differentiable on \\( [2, 9] \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 9] \\), so the Intermediate Value Theorem gives at least one such c.",
   ],
   "01011-06": [
      "No. Every tabulated value of f is greater than -3, so the Intermediate Value Theorem does not apply on \\( [0, 9] \\).",
      "Yes. A continuous function on \\( [0, 9] \\) takes every value between its values, so f takes the value -3.",
      "Yes. Since f is differentiable on \\( [0, 9] \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 9] \\), so the Intermediate Value Theorem gives at least one such c.",
   ],
   "01011-07": [
      "Yes. Since \\( f(1) = 2 < 7 < f(7) = 8 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [1, 7] \\), and \\( f(1) = 2 < 7 < f(7) = 8 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [1, 7] \\), and \\( f(1) = 2 < 7 < f(7) = 8 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [1, 7] \\), and \\( f(1) = 2 < 7 < f(7) = 8 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-08": [
      "Yes. Since \\( f(6) = 2 < 3 < f(0) = 7 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [0, 6] \\), and \\( f(6) = 2 < 3 < f(0) = 7 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 6] \\), and \\( f(6) = 2 < 3 < f(0) = 7 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 6] \\), and \\( f(6) = 2 < 3 < f(0) = 7 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-09": [
      "No. Although f is continuous on \\( [3, 9] \\), -3 is not between \\( f(3) = 0 \\) and \\( f(9) = 4 \\), so no such c must exist.",
      "Yes. Since \\( f(4) = -4 < -3 < f(8) = 4 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [4, 8] \\), and \\( f(4) = -4 < -3 < f(8) = 4 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [4, 8] \\), and \\( f(4) = -4 < -3 < f(8) = 4 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-10": [
      "No. Every tabulated value of f is greater than -7, so the Intermediate Value Theorem does not apply on \\( [0, 7] \\).",
      "Yes. A continuous function on \\( [0, 7] \\) takes every value between its values, so f takes the value -7.",
      "Yes. Since f is differentiable on \\( [0, 7] \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), so the Intermediate Value Theorem gives at least one such c.",
   ],
   "01011-11": [
      "Yes. Since \\( f(9) = -9 < 0 < f(3) = 5 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [3, 9] \\), and \\( f(9) = -9 < 0 < f(3) = 5 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 9] \\), and \\( f(9) = -9 < 0 < f(3) = 5 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 9] \\), and \\( f(9) = -9 < 0 < f(3) = 5 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-12": [
      "No. Every tabulated value of f is greater than -8, so the Intermediate Value Theorem does not apply on \\( [0, 9] \\).",
      "Yes. A continuous function on \\( [0, 9] \\) takes every value between its values, so f takes the value -8.",
      "Yes. Since f is differentiable on \\( [0, 9] \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 9] \\), so the Intermediate Value Theorem gives at least one such c.",
   ],
   "01011-13": [
      "Yes. Since \\( f(2) = -6 < -4 < f(5) = 2 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [2, 5] \\), and \\( f(2) = -6 < -4 < f(5) = 2 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 5] \\), and \\( f(2) = -6 < -4 < f(5) = 2 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 5] \\), and \\( f(2) = -6 < -4 < f(5) = 2 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-14": [
      "Yes. Since \\( f(3) = -9 < -5 < f(9) = 3 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [3, 9] \\), and \\( f(3) = -9 < -5 < f(9) = 3 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 9] \\), and \\( f(3) = -9 < -5 < f(9) = 3 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 9] \\), and \\( f(3) = -9 < -5 < f(9) = 3 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-15": [
      "Yes. Since \\( f(9) = 2 < 3 < f(1) = 6 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [1, 9] \\), and \\( f(9) = 2 < 3 < f(1) = 6 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [1, 9] \\), and \\( f(9) = 2 < 3 < f(1) = 6 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [1, 9] \\), and \\( f(9) = 2 < 3 < f(1) = 6 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-16": [
      "No. Every tabulated value of f is less than 5, so the Intermediate Value Theorem does not apply on \\( [1, 9] \\).",
      "Yes. A continuous function on \\( [1, 9] \\) takes every value between its values, so f takes the value 5.",
      "Yes. Since f is differentiable on \\( [1, 9] \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [1, 9] \\), so the Intermediate Value Theorem gives at least one such c.",
   ],
   "01011-17": [
      "Yes. Since \\( f(6) = -5 < 5 < f(0) = 7 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [0, 6] \\), and \\( f(6) = -5 < 5 < f(0) = 7 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 6] \\), and \\( f(6) = -5 < 5 < f(0) = 7 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 6] \\), and \\( f(6) = -5 < 5 < f(0) = 7 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-18": [
      "No. Although f is continuous on \\( [2, 6] \\), -6 is not between \\( f(2) = 9 \\) and \\( f(6) = -1 \\), so no such c must exist.",
      "Yes. Since \\( f(3) = -7 < -6 < f(4) = -5 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 4] \\), and \\( f(3) = -7 < -6 < f(4) = -5 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [3, 4] \\), and \\( f(3) = -7 < -6 < f(4) = -5 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-19": [
      "No. Although f is continuous on \\( [1, 5] \\), -1 is not between \\( f(1) = 9 \\) and \\( f(5) = 7 \\), so no such c must exist.",
      "Yes. Since \\( f(2) = -9 < -1 < f(3) = 3 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 3] \\), and \\( f(2) = -9 < -1 < f(3) = 3 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [2, 3] \\), and \\( f(2) = -9 < -1 < f(3) = 3 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-20": [
      "Yes. Since \\( f(7) = -8 < -4 < f(0) = 6 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable on \\( [0, 7] \\), and \\( f(7) = -8 < -4 < f(0) = 6 \\), the Mean Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), and \\( f(7) = -8 < -4 < f(0) = 6 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [0, 7] \\), and \\( f(7) = -8 < -4 < f(0) = 6 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01011-21": [
      "No. Although f is continuous on \\( [3, 9] \\), 2 is not between \\( f(3) = 5 \\) and \\( f(9) = 3 \\), so no such c must exist.",
      "Yes. Since \\( f(4) = 0 < 2 < f(7) = 3 \\), the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [4, 7] \\), and \\( f(4) = 0 < 2 < f(7) = 3 \\), so the Intermediate Value Theorem gives at least one such c.",
      "Yes. Since f is differentiable, it is continuous on \\( [4, 7] \\), and \\( f(4) = 0 < 2 < f(7) = 3 \\), so the Intermediate Value Theorem gives exactly one such c.",
   ],
   "01013-00": [
      "As x approaches \\( \\frac{19}{2} \\), h(x) increases without bound, so the line \\( x = \\frac{19}{2} \\) is a vertical asymptote.",
      "As x increases or decreases without bound, h(x) approaches \\( \\frac{19}{2} \\), so the line \\( y = \\frac{19}{2} \\) is a horizontal asymptote at both ends.",
      "As x increases without bound, h(x) approaches \\( \\frac{19}{2} \\), so the line \\( y = \\frac{19}{2} \\) is a horizontal asymptote.",
      "The value of h at the input \\( \\infty \\) is \\( \\frac{19}{2} \\), so the graph of h contains the point \\( (\\infty, \\frac{19}{2}) \\).",
   ],
   "01013-01": [
      "As x approaches \\( \\frac{19}{2} \\) from either side, f(x) decreases without bound, so the line \\( x = \\frac{19}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{19}{2} \\) from the left, f(x) decreases without bound, so the line \\( x = \\frac{19}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{19}{2} \\) from the left, the limit of f(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = \\frac{19}{2} \\).",
      "As x decreases without bound, f(x) approaches \\( \\frac{19}{2} \\), so the line \\( y = \\frac{19}{2} \\) is a horizontal asymptote.",
   ],
   "01013-02": [
      "As x approaches \\( \\frac{13}{2} \\) from either side, k(x) decreases without bound, so the line \\( x = \\frac{13}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{13}{2} \\) from the right, k(x) decreases without bound, so the line \\( x = \\frac{13}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{13}{2} \\) from the right, the limit of k(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = \\frac{13}{2} \\).",
      "As x decreases without bound, k(x) approaches \\( \\frac{13}{2} \\), so the line \\( y = \\frac{13}{2} \\) is a horizontal asymptote.",
   ],
   "01013-03": [
      "As x approaches \\( 7 \\) from either side, k(x) increases without bound, so the line \\( x = 7 \\) is a vertical asymptote.",
      "As x approaches \\( 7 \\) from the left, k(x) increases without bound, so the line \\( x = 7 \\) is a vertical asymptote.",
      "As x approaches \\( 7 \\) from the left, the limit of k(x) exists and equals \\( \\infty \\), so there is no asymptote at \\( x = 7 \\).",
      "As x increases without bound, k(x) approaches \\( 7 \\), so the line \\( y = 7 \\) is a horizontal asymptote.",
   ],
   "01013-04": [
      "As x approaches \\( - \\frac{17}{2} \\) from either side, h(x) increases without bound, so the line \\( x = - \\frac{17}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{17}{2} \\) from the right, h(x) increases without bound, so the line \\( x = - \\frac{17}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{17}{2} \\) from the right, the limit of h(x) exists and equals \\( \\infty \\), so there is no asymptote at \\( x = - \\frac{17}{2} \\).",
      "As x increases without bound, h(x) approaches \\( - \\frac{17}{2} \\), so the line \\( y = - \\frac{17}{2} \\) is a horizontal asymptote.",
   ],
   "01013-05": [
      "As x approaches \\( \\frac{5}{2} \\), h(x) decreases without bound, so the line \\( x = \\frac{5}{2} \\) is a vertical asymptote.",
      "As x decreases without bound, h(x) approaches \\( \\frac{5}{2} \\), so the line \\( y = \\frac{5}{2} \\) is a horizontal asymptote.",
      "As x increases or decreases without bound, h(x) approaches \\( \\frac{5}{2} \\), so the line \\( y = \\frac{5}{2} \\) is a horizontal asymptote at both ends.",
      "The value of h at the input \\( -\\infty \\) is \\( \\frac{5}{2} \\), so the graph of h contains the point \\( (-\\infty, \\frac{5}{2}) \\).",
   ],
   "01013-06": [
      "As x approaches \\( 3 \\) from either side, f(x) decreases without bound, so the line \\( x = 3 \\) is a vertical asymptote.",
      "As x approaches \\( 3 \\) from the right, f(x) decreases without bound, so the line \\( x = 3 \\) is a vertical asymptote.",
      "As x approaches \\( 3 \\) from the right, the limit of f(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = 3 \\).",
      "As x decreases without bound, f(x) approaches \\( 3 \\), so the line \\( y = 3 \\) is a horizontal asymptote.",
   ],
   "01013-07": [
      "As x approaches \\( - \\frac{7}{2} \\) from either side, k(x) increases without bound, so the line \\( x = - \\frac{7}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{7}{2} \\) from the right, k(x) increases without bound, so the line \\( x = - \\frac{7}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{7}{2} \\) from the right, the limit of k(x) exists and equals \\( \\infty \\), so there is no asymptote at \\( x = - \\frac{7}{2} \\).",
      "As x increases without bound, k(x) approaches \\( - \\frac{7}{2} \\), so the line \\( y = - \\frac{7}{2} \\) is a horizontal asymptote.",
   ],
   "01013-08": [
      "As x approaches \\( \\frac{7}{2} \\) from either side, f(x) decreases without bound, so the line \\( x = \\frac{7}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{7}{2} \\) from the left, f(x) decreases without bound, so the line \\( x = \\frac{7}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{7}{2} \\) from the left, the limit of f(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = \\frac{7}{2} \\).",
      "As x decreases without bound, f(x) approaches \\( \\frac{7}{2} \\), so the line \\( y = \\frac{7}{2} \\) is a horizontal asymptote.",
   ],
   "01013-09": [
      "As x approaches \\( - \\frac{19}{2} \\), h(x) increases without bound, so the line \\( x = - \\frac{19}{2} \\) is a vertical asymptote.",
      "As x increases or decreases without bound, h(x) approaches \\( - \\frac{19}{2} \\), so the line \\( y = - \\frac{19}{2} \\) is a horizontal asymptote at both ends.",
      "As x increases without bound, h(x) approaches \\( - \\frac{19}{2} \\), so the line \\( y = - \\frac{19}{2} \\) is a horizontal asymptote.",
      "The value of h at the input \\( \\infty \\) is \\( - \\frac{19}{2} \\), so the graph of h contains the point \\( (\\infty, - \\frac{19}{2}) \\).",
   ],
   "01013-10": [
      "As x approaches \\( \\frac{17}{2} \\), k(x) decreases without bound, so the line \\( x = \\frac{17}{2} \\) is a vertical asymptote.",
      "As x decreases without bound, k(x) approaches \\( \\frac{17}{2} \\), so the line \\( y = \\frac{17}{2} \\) is a horizontal asymptote.",
      "As x increases or decreases without bound, k(x) approaches \\( \\frac{17}{2} \\), so the line \\( y = \\frac{17}{2} \\) is a horizontal asymptote at both ends.",
      "The value of k at the input \\( -\\infty \\) is \\( \\frac{17}{2} \\), so the graph of k contains the point \\( (-\\infty, \\frac{17}{2}) \\).",
   ],
   "01013-11": [
      "As x approaches \\( \\frac{11}{2} \\), h(x) decreases without bound, so the line \\( x = \\frac{11}{2} \\) is a vertical asymptote.",
      "As x decreases without bound, h(x) approaches \\( \\frac{11}{2} \\), so the line \\( y = \\frac{11}{2} \\) is a horizontal asymptote.",
      "As x increases or decreases without bound, h(x) approaches \\( \\frac{11}{2} \\), so the line \\( y = \\frac{11}{2} \\) is a horizontal asymptote at both ends.",
      "The value of h at the input \\( -\\infty \\) is \\( \\frac{11}{2} \\), so the graph of h contains the point \\( (-\\infty, \\frac{11}{2}) \\).",
   ],
   "01013-12": [
      "As x approaches \\( -4 \\) from either side, h(x) increases without bound, so the line \\( x = -4 \\) is a vertical asymptote.",
      "As x approaches \\( -4 \\) from the left, h(x) increases without bound, so the line \\( x = -4 \\) is a vertical asymptote.",
      "As x approaches \\( -4 \\) from the left, the limit of h(x) exists and equals \\( \\infty \\), so there is no asymptote at \\( x = -4 \\).",
      "As x increases without bound, h(x) approaches \\( -4 \\), so the line \\( y = -4 \\) is a horizontal asymptote.",
   ],
   "01013-13": [
      "As x approaches \\( \\frac{19}{2} \\) from either side, h(x) increases without bound, so the line \\( x = \\frac{19}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{19}{2} \\) from the left, h(x) increases without bound, so the line \\( x = \\frac{19}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{19}{2} \\) from the left, the limit of h(x) exists and equals \\( \\infty \\), so there is no asymptote at \\( x = \\frac{19}{2} \\).",
      "As x increases without bound, h(x) approaches \\( \\frac{19}{2} \\), so the line \\( y = \\frac{19}{2} \\) is a horizontal asymptote.",
   ],
   "01013-14": [
      "As x approaches \\( -6 \\) from either side, g(x) decreases without bound, so the line \\( x = -6 \\) is a vertical asymptote.",
      "As x approaches \\( -6 \\) from the left, g(x) decreases without bound, so the line \\( x = -6 \\) is a vertical asymptote.",
      "As x approaches \\( -6 \\) from the left, the limit of g(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = -6 \\).",
      "As x decreases without bound, g(x) approaches \\( -6 \\), so the line \\( y = -6 \\) is a horizontal asymptote.",
   ],
   "01013-15": [
      "As x approaches \\( 10 \\) from either side, h(x) decreases without bound, so the line \\( x = 10 \\) is a vertical asymptote.",
      "As x approaches \\( 10 \\) from the left, h(x) decreases without bound, so the line \\( x = 10 \\) is a vertical asymptote.",
      "As x approaches \\( 10 \\) from the left, the limit of h(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = 10 \\).",
      "As x decreases without bound, h(x) approaches \\( 10 \\), so the line \\( y = 10 \\) is a horizontal asymptote.",
   ],
   "01013-16": [
      "As x approaches \\( -9 \\), h(x) increases without bound, so the line \\( x = -9 \\) is a vertical asymptote.",
      "As x increases or decreases without bound, h(x) approaches \\( -9 \\), so the line \\( y = -9 \\) is a horizontal asymptote at both ends.",
      "As x increases without bound, h(x) approaches \\( -9 \\), so the line \\( y = -9 \\) is a horizontal asymptote.",
      "The value of h at the input \\( \\infty \\) is \\( -9 \\), so the graph of h contains the point \\( (\\infty, -9) \\).",
   ],
   "01013-17": [
      "As x approaches \\( - \\frac{15}{2} \\) from either side, f(x) increases without bound, so the line \\( x = - \\frac{15}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{15}{2} \\) from the right, f(x) increases without bound, so the line \\( x = - \\frac{15}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{15}{2} \\) from the right, the limit of f(x) exists and equals \\( \\infty \\), so there is no asymptote at \\( x = - \\frac{15}{2} \\).",
      "As x increases without bound, f(x) approaches \\( - \\frac{15}{2} \\), so the line \\( y = - \\frac{15}{2} \\) is a horizontal asymptote.",
   ],
   "01013-18": [
      "As x approaches \\( \\frac{13}{2} \\) from either side, k(x) decreases without bound, so the line \\( x = \\frac{13}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{13}{2} \\) from the left, k(x) decreases without bound, so the line \\( x = \\frac{13}{2} \\) is a vertical asymptote.",
      "As x approaches \\( \\frac{13}{2} \\) from the left, the limit of k(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = \\frac{13}{2} \\).",
      "As x decreases without bound, k(x) approaches \\( \\frac{13}{2} \\), so the line \\( y = \\frac{13}{2} \\) is a horizontal asymptote.",
   ],
   "01013-19": [
      "As x approaches \\( - \\frac{3}{2} \\) from either side, g(x) decreases without bound, so the line \\( x = - \\frac{3}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{3}{2} \\) from the right, g(x) decreases without bound, so the line \\( x = - \\frac{3}{2} \\) is a vertical asymptote.",
      "As x approaches \\( - \\frac{3}{2} \\) from the right, the limit of g(x) exists and equals \\( -\\infty \\), so there is no asymptote at \\( x = - \\frac{3}{2} \\).",
      "As x decreases without bound, g(x) approaches \\( - \\frac{3}{2} \\), so the line \\( y = - \\frac{3}{2} \\) is a horizontal asymptote.",
   ],
   "01013-20": [
      "As x approaches \\( \\frac{5}{2} \\), k(x) decreases without bound, so the line \\( x = \\frac{5}{2} \\) is a vertical asymptote.",
      "As x decreases without bound, k(x) approaches \\( \\frac{5}{2} \\), so the line \\( y = \\frac{5}{2} \\) is a horizontal asymptote.",
      "As x increases or decreases without bound, k(x) approaches \\( \\frac{5}{2} \\), so the line \\( y = \\frac{5}{2} \\) is a horizontal asymptote at both ends.",
      "The value of k at the input \\( -\\infty \\) is \\( \\frac{5}{2} \\), so the graph of k contains the point \\( (-\\infty, \\frac{5}{2}) \\).",
   ],
   "01013-21": [
      "As x approaches \\( 5 \\), g(x) increases without bound, so the line \\( x = 5 \\) is a vertical asymptote.",
      "As x increases or decreases without bound, g(x) approaches \\( 5 \\), so the line \\( y = 5 \\) is a horizontal asymptote at both ends.",
      "As x increases without bound, g(x) approaches \\( 5 \\), so the line \\( y = 5 \\) is a horizontal asymptote.",
      "The value of g at the input \\( \\infty \\) is \\( 5 \\), so the graph of g contains the point \\( (\\infty, 5) \\).",
   ],
   "01015-00": [
      "f is continuous on \\( (-\\infty, 6) \\cup (6, \\infty) \\).",
      "f is continuous on \\( [0, 6) \\cup (6, \\infty) \\).",
      "f is continuous on \\( [0, 6] \\cup [6, \\infty) \\).",
      "f is continuous on \\( [0, \\infty) \\).",
   ],
   "01015-01": [
      "f is continuous on \\( (-\\infty, 0) \\cup (0, 4) \\cup (4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 0) \\cup (0, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 0] \\cup [0, 4] \\cup [4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 4) \\cup (4, \\infty) \\).",
   ],
   "01015-02": [
      "f is continuous on \\( (-\\infty, 3) \\cup (3, \\infty) \\).",
      "f is continuous on \\( [2, 3) \\cup (3, \\infty) \\).",
      "f is continuous on \\( [2, 3] \\cup [3, \\infty) \\).",
      "f is continuous on \\( [2, \\infty) \\).",
   ],
   "01015-03": [
      "f is continuous on \\( (-\\infty, 1) \\cup (1, \\infty) \\).",
      "f is continuous on \\( [-4, 1) \\cup (1, \\infty) \\).",
      "f is continuous on \\( [-4, 1] \\cup [1, \\infty) \\).",
      "f is continuous on \\( [-4, \\infty) \\).",
   ],
   "01015-04": [
      "f is continuous on \\( (-\\infty, -4) \\cup (-4, 4) \\cup (4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -4) \\cup (-4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -4] \\cup [-4, 4] \\cup [4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 4) \\cup (4, \\infty) \\).",
   ],
   "01015-05": [
      "f is continuous on \\( (-\\infty, 6) \\cup (6, \\infty) \\).",
      "f is continuous on \\( [5, 6) \\cup (6, \\infty) \\).",
      "f is continuous on \\( [5, 6] \\cup [6, \\infty) \\).",
      "f is continuous on \\( [5, \\infty) \\).",
   ],
   "01015-06": [
      "f is continuous on \\( (-\\infty, 3) \\cup (3, 4) \\cup (4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 3) \\cup (3, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 3] \\cup [3, 4] \\cup [4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 4) \\cup (4, \\infty) \\).",
   ],
   "01015-07": [
      "f is continuous on \\( (-\\infty, -1) \\cup (-1, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -5) \\cup (-5, -1) \\cup (-1, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -5) \\cup (-5, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -5] \\cup [-5, -1] \\cup [-1, \\infty) \\).",
   ],
   "01015-08": [
      "f is continuous on \\( (-\\infty, 2) \\cup (2, \\infty) \\).",
      "f is continuous on \\( [-6, 2) \\cup (2, \\infty) \\).",
      "f is continuous on \\( [-6, 2] \\cup [2, \\infty) \\).",
      "f is continuous on \\( [-6, \\infty) \\).",
   ],
   "01015-09": [
      "f is continuous on \\( (-\\infty, 3) \\cup (3, \\infty) \\).",
      "f is continuous on \\( [-4, 3) \\cup (3, \\infty) \\).",
      "f is continuous on \\( [-4, 3] \\cup [3, \\infty) \\).",
      "f is continuous on \\( [-4, \\infty) \\).",
   ],
   "01015-10": [
      "f is continuous on \\( (-\\infty, -1) \\cup (-1, 4) \\cup (4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -1) \\cup (-1, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -1] \\cup [-1, 4] \\cup [4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 4) \\cup (4, \\infty) \\).",
   ],
   "01015-11": [
      "f is continuous on \\( (-\\infty, -5) \\cup (-5, 4) \\cup (4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -5) \\cup (-5, \\infty) \\).",
      "f is continuous on \\( (-\\infty, -5] \\cup [-5, 4] \\cup [4, \\infty) \\).",
      "f is continuous on \\( (-\\infty, 4) \\cup (4, \\infty) \\).",
   ],
}

BY_SUFFIX = {
   "01001-00": lambda: graph_limit("01001-00", at=5, left=1, right=-3, value=None, asks_value=False),
   "01001-01": lambda: graph_limit("01001-01", at=5, left=4, right=0, value=-2, asks_value=False),
   "01001-02": lambda: graph_limit("01001-02", at=6, left=2, right=4, value=-1, asks_value=False),
   "01001-03": lambda: graph_limit("01001-03", at=3, left=0, right=0, value=1, asks_value=True),
   "01001-04": lambda: graph_limit("01001-04", at=6, left=4, right=2, value=-2, asks_value=False),
   "01001-05": lambda: graph_limit("01001-05", at=6, left=4, right=2, value=None, asks_value=False),
   "01001-06": lambda: graph_limit("01001-06", at=6, left=-1, right=3, value=None, asks_value=False),
   "01001-07": lambda: graph_limit("01001-07", at=2, left=-2, right=-2, value=3, asks_value=True),
   "01001-08": lambda: graph_limit("01001-08", at=3, left=1, right=1, value=3, asks_value=True),
   "01001-09": lambda: graph_limit("01001-09", at=1, left=4, right=4, value=-1, asks_value=True),
   "01001-10": lambda: graph_limit("01001-10", at=6, left=-2, right=3, value=0, asks_value=False),
   "01001-11": lambda: graph_limit("01001-11", at=5, left=1, right=-3, value=0, asks_value=False),
   "01001-12": lambda: graph_limit("01001-12", at=6, left=2, right=-1, value=-3, asks_value=False),
   "01001-13": lambda: graph_limit("01001-13", at=2, left=3, right=3, value=-1, asks_value=True),
   "01001-14": lambda: graph_limit("01001-14", at=5, left=0, right=-3, value=None, asks_value=False),
   "01001-15": lambda: graph_limit("01001-15", at=3, left=-3, right=-3, value=3, asks_value=True),
   "01001-16": lambda: graph_limit("01001-16", at=2, left=4, right=4, value=-3, asks_value=True),
   "01001-17": lambda: graph_limit("01001-17", at=2, left=2, right=2, value=4, asks_value=True),
   "01001-18": lambda: graph_limit("01001-18", at=5, left=-3, right=3, value=None, asks_value=False),
   "01001-19": lambda: graph_limit("01001-19", at=5, left=-1, right=3, value=0, asks_value=False),
   "01001-20": lambda: graph_limit("01001-20", at=5, left=1, right=-3, value=None, asks_value=False),
   "01001-21": lambda: graph_limit("01001-21", at=6, left=2, right=-2, value=4, asks_value=False),

   "01002-00": lambda: table_limit("01002-00", 1, [("0.9999", "-4.0000"), ("0.9990", "0.0000"), ("0.9900", "-4.0000"), ("0.9000", "0.0000"), ("1.1000", "-4.0000"), ("1.0100", "0.0000"), ("1.0010", "-4.0000"), ("1.0001", "0.0000")]),
   "01002-01": lambda: table_limit("01002-01", 4, [("3.9999", "3.0000"), ("3.9990", "6.0000"), ("3.9900", "3.0000"), ("3.9000", "6.0000"), ("4.1000", "3.0000"), ("4.0100", "6.0000"), ("4.0010", "3.0000"), ("4.0001", "6.0000")]),
   "01002-02": lambda: table_limit("01002-02", 5, [("4.9999", "-3.9996"), ("4.9990", "-3.9960"), ("4.9900", "-3.9605"), ("4.9000", "-3.6500"), ("5.1000", "-3.3500"), ("5.0100", "-3.9305"), ("5.0010", "-3.9930"), ("5.0001", "-3.9993")]),
   "01002-03": lambda: table_limit("01002-03", 1, [("0.9999", "-3.0000"), ("0.9990", "0.0000"), ("0.9900", "-3.0000"), ("0.9000", "0.0000"), ("1.1000", "-3.0000"), ("1.0100", "0.0000"), ("1.0010", "-3.0000"), ("1.0001", "0.0000")]),
   "01002-04": lambda: table_limit("01002-04", 1, [("0.9999", "-3.0000"), ("0.9990", "6.0000"), ("0.9900", "-3.0000"), ("0.9000", "6.0000"), ("1.1000", "-3.0000"), ("1.0100", "6.0000"), ("1.0010", "-3.0000"), ("1.0001", "6.0000")]),
   "01002-05": lambda: table_limit("01002-05", -2, [("-2.0001", "0.0005"), ("-2.0010", "0.0050"), ("-2.0100", "0.0498"), ("-2.1000", "0.4800"), ("-1.9000", "-0.2200"), ("-1.9900", "-0.0202"), ("-1.9990", "-0.0020"), ("-1.9999", "-0.0002")]),
   "01002-06": lambda: table_limit("01002-06", 4, [("3.9999", "5.0000"), ("3.9990", "-2.0000"), ("3.9900", "5.0000"), ("3.9000", "-2.0000"), ("4.1000", "5.0000"), ("4.0100", "-2.0000"), ("4.0010", "5.0000"), ("4.0001", "-2.0000")]),
   "01002-07": lambda: table_limit("01002-07", -1, [("-1.0001", "3.9993"), ("-1.0010", "3.9930"), ("-1.0100", "3.9295"), ("-1.1000", "3.2500"), ("-0.9000", "3.6500"), ("-0.9900", "3.9695"), ("-0.9990", "3.9970"), ("-0.9999", "3.9997")]),
   "01002-08": lambda: table_limit("01002-08", 3, [("2.9999", "1.0005"), ("2.9990", "1.0050"), ("2.9900", "1.0497"), ("2.9000", "1.4700"), ("3.1000", "1.6700"), ("3.0100", "1.9697"), ("3.0010", "1.9970"), ("3.0001", "1.9997")]),
   "01002-09": lambda: table_limit("01002-09", 1, [("0.9999", "-2.0000"), ("0.9990", "2.0000"), ("0.9900", "-2.0000"), ("0.9000", "2.0000"), ("1.1000", "-2.0000"), ("1.0100", "2.0000"), ("1.0010", "-2.0000"), ("1.0001", "2.0000")]),
   "01002-10": lambda: table_limit("01002-10", -3, [("-3.0001", "-1.0000"), ("-3.0010", "6.0000"), ("-3.0100", "-1.0000"), ("-3.1000", "6.0000"), ("-2.9000", "-1.0000"), ("-2.9900", "6.0000"), ("-2.9990", "-1.0000"), ("-2.9999", "6.0000")]),
   "01002-11": lambda: table_limit("01002-11", 0, [("-0.0001", "-2.0009"), ("-0.0010", "-2.0090"), ("-0.0100", "-2.0905"), ("-0.1000", "-2.9500"), ("0.1000", "-3.2500"), ("0.0100", "-3.0205"), ("0.0010", "-3.0020"), ("0.0001", "-3.0002")]),
   "01002-12": lambda: table_limit("01002-12", -1, [("-1.0001", "4.0000"), ("-1.0010", "2.0000"), ("-1.0100", "4.0000"), ("-1.1000", "2.0000"), ("-0.9000", "4.0000"), ("-0.9900", "2.0000"), ("-0.9990", "4.0000"), ("-0.9999", "2.0000")]),
   "01002-13": lambda: table_limit("01002-13", 5, [("4.9999", "-2.0000"), ("4.9990", "5.0000"), ("4.9900", "-2.0000"), ("4.9000", "5.0000"), ("5.1000", "-2.0000"), ("5.0100", "5.0000"), ("5.0010", "-2.0000"), ("5.0001", "5.0000")]),
   "01002-14": lambda: table_limit("01002-14", 3, [("2.9999", "4.0001"), ("2.9990", "4.0010"), ("2.9900", "4.0101"), ("2.9000", "4.1100"), ("3.1000", "-4.3900"), ("3.0100", "-4.0399"), ("3.0010", "-4.0040"), ("3.0001", "-4.0004")]),
   "01002-15": lambda: table_limit("01002-15", 1, [("0.9999", "1.9994"), ("0.9990", "1.9940"), ("0.9900", "1.9402"), ("0.9000", "1.4200"), ("1.1000", "1.8200"), ("1.0100", "1.0802"), ("1.0010", "1.0080"), ("1.0001", "1.0008")]),
   "01002-16": lambda: table_limit("01002-16", 3, [("2.9999", "3.0003"), ("2.9990", "3.0030"), ("2.9900", "3.0296"), ("2.9000", "3.2600"), ("3.1000", "3.7600"), ("3.0100", "3.0796"), ("3.0010", "3.0080"), ("3.0001", "3.0008")]),
   "01002-17": lambda: table_limit("01002-17", 3, [("2.9999", "3.9992"), ("2.9990", "3.9920"), ("2.9900", "3.9195"), ("2.9000", "3.1500"), ("3.1000", "-0.4500"), ("3.0100", "-0.0405"), ("3.0010", "-0.0040"), ("3.0001", "-0.0004")]),
   "01002-18": lambda: table_limit("01002-18", 5, [("4.9999", "5.0002"), ("4.9990", "5.0020"), ("4.9900", "5.0200"), ("4.9000", "5.2000"), ("5.1000", "-2.2000"), ("5.0100", "-2.0200"), ("5.0010", "-2.0020"), ("5.0001", "-2.0002")]),
   "01002-19": lambda: table_limit("01002-19", -1, [("-1.0001", "0.9996"), ("-1.0010", "0.9960"), ("-1.0100", "0.9595"), ("-1.1000", "0.5500"), ("-0.9000", "-0.3500"), ("-0.9900", "-0.0305"), ("-0.9990", "-0.0030"), ("-0.9999", "-0.0003")]),
   "01002-20": lambda: table_limit("01002-20", -2, [("-2.0001", "1.0004"), ("-2.0010", "1.0040"), ("-2.0100", "1.0404"), ("-2.1000", "1.4400"), ("-1.9000", "0.7400"), ("-1.9900", "0.9704"), ("-1.9990", "0.9970"), ("-1.9999", "0.9997")]),
   "01002-21": lambda: table_limit("01002-21", 0, [("-0.0001", "-2.0000"), ("-0.0010", "2.0000"), ("-0.0100", "-2.0000"), ("-0.1000", "2.0000"), ("0.1000", "-2.0000"), ("0.0100", "2.0000"), ("0.0010", "-2.0000"), ("0.0001", "2.0000")]),

   "01003-00": lambda: composite_quotient_limit("x**2 + 3", 4, -1),
   "01003-01": lambda: composite_quotient_limit("x**2 - 1", 3, -2),
   "01003-02": lambda: composite_quotient_limit("x**2 + 1", -1, -1),
   "01003-03": lambda: composite_quotient_limit("x**2 + 1", 2, -4),
   "01003-04": lambda: composite_quotient_limit("x**2", 2, -1),

   "01004-00": lambda: cancelled_limit("01004-00", "(x**2 + 2*x - 15) / (x**2 + 8*x + 15)", -5),
   "01004-01": lambda: cancelled_limit("01004-01", "(x**2 + 5*x - 14) / (x**2 - 2*x)", 2),
   "01004-02": lambda: cancelled_limit("01004-02", "(x**2 + x - 2) / (x**2 - 3*x - 10)", -2),
   "01004-03": lambda: cancelled_limit("01004-03", "(x**2 - 2*x - 24) / (x**2 + 7*x + 12)", -4),
   "01004-04": lambda: cancelled_limit("01004-04", "(x**2 - 9*x + 14) / (x**2 - 5*x + 6)", 2),
   "01004-05": lambda: cancelled_limit("01004-05", "(x**2 - 4*x) / (x**2 - 7*x + 12)", 4),
   "01004-06": lambda: cancelled_limit("01004-06", "(x**2 - 6*x + 5) / (x**2 + 3*x - 4)", 1),
   "01004-07": lambda: cancelled_limit("01004-07", "(x**2 - 6*x + 5) / (x**2 - x)", 1),
   "01004-08": lambda: cancelled_limit("01004-08", "(x**2 + x - 6) / (x**2 + 8*x + 15)", -3),
   "01004-09": lambda: cancelled_limit("01004-09", "(x**2 - 3*x - 4) / (x**2 - 4*x - 5)", -1),
   "01004-10": lambda: cancelled_limit("01004-10", "(x**2 - 9*x + 18) / (x**2 - 8*x + 15)", 3),
   "01004-11": lambda: cancelled_limit("01004-11", "(x**2 + x - 2) / (x**2 - 5*x + 4)", 1),

   "01005-00": lambda: squeeze_limit("01005-00", "-3*(x - 2)**3*sin(1/(x - 2)) - 2", 2),
   "01005-01": lambda: squeeze_limit("01005-01", "-3*x**3*sin(1/x) + 3", 0),
   "01005-02": lambda: squeeze_limit("01005-02", "2*(x + 3)**3*sin(1/(x + 3))", -3),
   "01005-03": lambda: squeeze_limit("01005-03", "(8 - 4*x)*cos(1/(x - 2)) + 1", 2),
   "01005-04": lambda: squeeze_limit("01005-04", "(x + 3)*sin(1/(x + 3)) - 1", -3),
   "01005-05": lambda: squeeze_limit("01005-05", "(4*x + 12)*sin(1/(x + 3)) + 1", -3),
   "01005-06": lambda: squeeze_limit("01005-06", "2*(x + 1)**3*sin(1/(x + 1)) + 5", -1),
   "01005-07": lambda: squeeze_limit("01005-07", "-4*(x + 2)**3*sin(1/(x + 2)) + 2", -2),
   "01005-08": lambda: squeeze_limit("01005-08", "(-4*x - 12)*sin(1/(x + 3)) + 2", -3),
   "01005-09": lambda: squeeze_limit("01005-09", "-(x + 3)**3*sin(1/(x + 3)) - 3", -3),
   "01005-10": lambda: squeeze_limit("01005-10", "(x - 2)**3*cos(1/(x - 2)) + 2", 2),
   "01005-11": lambda: squeeze_limit("01005-11", "2*x**3*sin(1/x) - 1", 0),
   "01005-12": lambda: squeeze_limit("01005-12", "-3*(x + 1)**3*sin(1/(x + 1)) + 2", -1),
   "01005-13": lambda: squeeze_limit("01005-13", "-3*(x + 3)**2*cos(1/(x + 3)) + 1", -3),
   "01005-14": lambda: squeeze_limit("01005-14", "(2 - 2*x)*cos(1/(x - 1)) - 1", 1),
   "01005-15": lambda: squeeze_limit("01005-15", "4*(x - 1)**3*cos(1/(x - 1)) - 3", 1),
   "01005-16": lambda: squeeze_limit("01005-16", "-2*(x - 1)**3*sin(1/(x - 1)) + 4", 1),
   "01005-17": lambda: squeeze_limit("01005-17", "-x**2*cos(1/x) - 1", 0),
   "01005-18": lambda: squeeze_limit("01005-18", "(3*x - 6)*cos(1/(x - 2)) + 2", 2),
   "01005-19": lambda: squeeze_limit("01005-19", "-2*(x - 3)**3*sin(1/(x - 3)) + 2", 3),
   "01005-20": lambda: squeeze_limit("01005-20", "-4*(x - 3)**3*sin(1/(x - 3))", 3),
   "01005-21": lambda: squeeze_limit("01005-21", "4*(x - 3)**3*sin(1/(x - 3)) + 4", 3),

   "01006-00": lambda: continuity_at_point("01006-00", "(2*x**2 - 16*x + 30)/(x - 3)", "(2*x**2 - 16*x + 30)/(x - 3)", 3, 4),
   "01006-01": lambda: continuity_at_point("01006-01", "(2*x**2 - 7*x + 5)/(x - 1)", "(2*x**2 - 7*x + 5)/(x - 1)", 1, 4),
   "01006-02": lambda: continuity_at_point("01006-02", "6 - 2*x", "6 - 3*x", 1, expression("6 - 2*x").subs(x, 1)),
   "01006-03": lambda: continuity_at_point("01006-03", "(3*x**2 + 16*x + 20)/(x + 2)", "(3*x**2 + 16*x + 20)/(x + 2)", -2, 1),
   "01006-04": lambda: continuity_at_point("01006-04", "(-2*x**2 - 2*x)/(x + 1)", "(-2*x**2 - 2*x)/(x + 1)", -1, 3),
   "01006-05": lambda: continuity_at_point("01006-05", "(2*x**2 - 16*x + 30)/(x - 3)", "(2*x**2 - 16*x + 30)/(x - 3)", 3, 3),
   "01006-06": lambda: continuity_at_point("01006-06", "(-x**2 + 5*x - 4)/(x - 1)", "(-x**2 + 5*x - 4)/(x - 1)", 1, 0),
   "01006-07": lambda: continuity_at_point("01006-07", "(x**2 + 2*x + 1)/(x + 1)", "(x**2 + 2*x + 1)/(x + 1)", -1, 0),
   "01006-08": lambda: continuity_at_point("01006-08", "(x**2 - 2*x + 1)/(x - 1)", "(x**2 - 2*x + 1)/(x - 1)", 1, -4),
   "01006-09": lambda: continuity_at_point("01006-09", "(2*x**2 + 8*x + 6)/(x + 1)", "(2*x**2 + 8*x + 6)/(x + 1)", -1, 4),
   "01006-10": lambda: continuity_at_point("01006-10", "(-2*x**2 + x)/x", "(-2*x**2 + x)/x", 0, 0),
   "01006-11": lambda: continuity_at_point("01006-11", "(-2*x**2 + 15*x - 27)/(x - 3)", "(-2*x**2 + 15*x - 27)/(x - 3)", 3, 3),
   "01006-12": lambda: continuity_at_point("01006-12", "x + 1", "1 - 3*x", 1, expression("1 - 3*x").subs(x, 1)),
   "01006-13": lambda: continuity_at_point("01006-13", "(x**2 + 8*x + 12)/(x + 2)", "(x**2 + 8*x + 12)/(x + 2)", -2, -4),
   "01006-14": lambda: continuity_at_point("01006-14", "(3*x**2 - 3*x)/x", "(3*x**2 - 3*x)/x", 0, -2),
   "01006-15": lambda: continuity_at_point("01006-15", "(-2*x**2 + 15*x - 27)/(x - 3)", "(-2*x**2 + 15*x - 27)/(x - 3)", 3, 1),
   "01006-16": lambda: continuity_at_point("01006-16", "(-3*x**2 + 9*x - 6)/(x - 1)", "(-3*x**2 + 9*x - 6)/(x - 1)", 1, -2),
   "01006-17": lambda: continuity_at_point("01006-17", "-2*x - 1", "-3*x - 4", -1, expression("-3*x - 4").subs(x, -1)),
   "01006-18": lambda: continuity_at_point("01006-18", "(-3*x**2 + 6*x - 3)/(x - 1)", "(-3*x**2 + 6*x - 3)/(x - 1)", 1, 0),
   "01006-19": lambda: continuity_at_point("01006-19", "(2*x**2 - 5*x + 3)/(x - 1)", "(2*x**2 - 5*x + 3)/(x - 1)", 1, -1),
   "01006-20": lambda: continuity_at_point("01006-20", "(-3*x**2 + 3*x)/(x - 1)", "(-3*x**2 + 3*x)/(x - 1)", 1, -3),
   "01006-21": lambda: continuity_at_point("01006-21", "4 - 2*x", "-2*x - 2", 1, expression("4 - 2*x").subs(x, 1)),

   "01007-00": lambda: discontinuity_kind("01007-00", "2*x**2 - 4*x - 6", "x**3 + x**2 - 8*x - 12", 3),
   "01007-01": lambda: discontinuity_kind("01007-01", "(-3*x - 12)*(x - 3)", "x**2*(x + 4)", 0),
   "01007-02": lambda: discontinuity_kind("01007-02", "3*x**2 - 18*x + 24", "x**3 - 6*x**2 + 9*x - 4", 1),
   "01007-03": lambda: discontinuity_kind("01007-03", "(x - 4)*(x - 2)", "(x - 4)*(x + 3)**2", -3),
   "01007-04": lambda: discontinuity_kind("01007-04", "x*(-x - 3)", "(x - 4)**2*(x + 3)", -3),
   "01007-05": lambda: discontinuity_kind("01007-05", "2*x*(x - 4)", "x*(x + 1)**2", -1),
   "01007-06": lambda: discontinuity_kind("01007-06", "2*x**2 + 4*x - 16", "x**3 - 4*x**2 - 16*x + 64", 4),
   "01007-07": lambda: discontinuity_kind("01007-07", "2*x**2 + 14*x + 24", "x**3 + 2*x**2 - 7*x + 4", -4),
   "01007-08": lambda: discontinuity_kind("01007-08", "3*x**2 - 9*x - 12", "x**3 - 12*x - 16", -2),
   "01007-09": lambda: discontinuity_kind("01007-09", "-x**2 - x", "x**3 - 7*x**2 + 8*x + 16", 4),
   "01007-10": lambda: discontinuity_kind("01007-10", "(2 - 2*x)*(x - 4)", "(x - 1)*(x + 3)**2", -3),
   "01007-11": lambda: discontinuity_kind("01007-11", "3*x**2 + 3*x - 6", "x**3 + 7*x**2 + 8*x - 16", -4),
   "01007-12": lambda: discontinuity_kind("01007-12", "x**2 - 16", "x**3 - 12*x + 16", -4),
   "01007-13": lambda: discontinuity_kind("01007-13", "3*x**2 - 48", "x**3 + 2*x**2 - 15*x - 36", 4),
   "01007-14": lambda: discontinuity_kind("01007-14", "(x - 2)*(2*x - 2)", "(x - 1)*(x + 2)**2", 1),
   "01007-15": lambda: discontinuity_kind("01007-15", "(2 - x)*(x - 1)", "(x - 2)*(x + 1)**2", 2),
   "01007-16": lambda: discontinuity_kind("01007-16", "(-2*x - 4)*(x - 4)", "(x + 1)**2*(x + 2)", -1),
   "01007-17": lambda: discontinuity_kind("01007-17", "-3*x**2 - 9*x + 12", "x**3 + 3*x**2 - 4", 1),
   "01007-18": lambda: discontinuity_kind("01007-18", "3*x**2 + 12*x + 9", "x**3 - 3*x**2 + 4", -1),
   "01007-19": lambda: discontinuity_kind("01007-19", "x*(x - 1)", "x*(x - 2)**2", 0),
   "01007-20": lambda: discontinuity_kind("01007-20", "(-2*x - 6)*(x - 2)", "(x - 4)**2*(x + 3)", -3),
   "01007-21": lambda: discontinuity_kind("01007-21", "(-2*x - 8)*(x + 1)", "(x + 2)**2*(x + 4)", -4),

   "01008-00": lambda: continuity_constants("01008-00", "(x**2 - 9) / (x - 3)", "-2*x**2 - 8", 3, 4),
   "01008-01": lambda: continuity_constants("01008-01", "(x**2 - 4) / (x - 2)", "-x**2", 2, 3),
   "01008-02": lambda: continuity_constants("01008-02", "(x**2 - 9) / (x + 3)", "3*x**2 + 9", -3, -1),
   "01008-03": lambda: continuity_constants("01008-03", "(x**2 - 4) / (x + 2)", "x**2 - 5", -2, -1),
   "01008-04": lambda: continuity_constants("01008-04", "(x**2 - 9) / (x + 3)", "3*x**2 - 9", -3, 5),
   "01008-05": lambda: continuity_constants("01008-05", "(x**2 - 16) / (x + 4)", "2*x**2 + 2", -4, -2),
   "01008-06": lambda: continuity_constants("01008-06", "(x**2 - 16) / (x + 4)", "2*x**2 - 8", -4, -3),
   "01008-07": lambda: continuity_constants("01008-07", "(x**2 - 1) / (x - 1)", "-2*x**2", 1, 2),
   "01008-08": lambda: continuity_constants("01008-08", "(x**2 - 25) / (x + 5)", "x**2 - 6", -5, -4),
   "01008-09": lambda: continuity_constants("01008-09", "(x**2 - 25) / (x - 5)", "-2*x**2 - 4", 5, 6),
   "01008-10": lambda: continuity_constants("01008-10", "(x**2 - 25) / (x + 5)", "3*x**2 + 7", -5, -4),
   "01008-11": lambda: continuity_constants("01008-11", "(x**2 - 9) / (x - 3)", "-2*x**2 - 3", 3, 4),

   "01009-00": lambda: vertical_asymptotes("01009-00", "3*x*(x + 3)", "x*(x + 1)"),
   "01009-01": lambda: vertical_asymptotes("01009-01", "(-x - 1)*(x - 1)", "(x + 1)*(x + 4)"),
   "01009-02": lambda: vertical_asymptotes("01009-02", "-2*x**2 + 10*x - 12", "x**2 - 4*x + 3"),
   "01009-03": lambda: vertical_asymptotes("01009-03", "(9 - 3*x)*(x + 4)", "(x - 3)*(x + 3)"),
   "01009-04": lambda: vertical_asymptotes("01009-04", "3*x*(x - 3)", "x*(x - 4)"),

   "01010-00": lambda: limit_at_negative_infinity("(5*x - 9)/sqrt(16*x**2 + 4)"),
   "01010-01": lambda: limit_at_negative_infinity("(2*x + 6)/sqrt(16*x**2 + 2)"),
   "01010-02": lambda: limit_at_negative_infinity("sqrt(4*x**2 + 4)/(-3*x - 2)"),
   "01010-03": lambda: limit_at_negative_infinity("sqrt(25*x**2 + 5)/(8 - 3*x)"),
   "01010-04": lambda: limit_at_negative_infinity("(6 - 5*x)/sqrt(16*x**2 + 1)"),
   "01010-05": lambda: limit_at_negative_infinity("sqrt(16*x**2 + 5)/(6*x - 7)"),
   "01010-06": lambda: limit_at_negative_infinity("(x + 9)/sqrt(9*x**2 + 4)"),
   "01010-07": lambda: limit_at_negative_infinity("sqrt(25*x**2 + 1)/(x + 2)"),
   "01010-08": lambda: limit_at_negative_infinity("sqrt(25*x**2 + 8)/(4 - 2*x)"),
   "01010-09": lambda: limit_at_negative_infinity("(9 - 2*x)/sqrt(36*x**2 + 1)"),
   "01010-10": lambda: limit_at_negative_infinity("sqrt(9*x**2 + 3)/(2*x)"),
   "01010-11": lambda: limit_at_negative_infinity("(3*x + 1)/sqrt(36*x**2 + 4)"),
   "01010-12": lambda: limit_at_negative_infinity("sqrt(9*x**2 + 4)/(6 - x)"),
   "01010-13": lambda: limit_at_negative_infinity("(4*x + 7)/sqrt(9*x**2 + 8)"),
   "01010-14": lambda: limit_at_negative_infinity("(x + 5)/sqrt(36*x**2 + 8)"),
   "01010-15": lambda: limit_at_negative_infinity("sqrt(9*x**2 + 1)/(-x - 1)"),
   "01010-16": lambda: limit_at_negative_infinity("(5*x + 8)/sqrt(9*x**2 + 9)"),
   "01010-17": lambda: limit_at_negative_infinity("(x - 5)/sqrt(4*x**2 + 4)"),
   "01010-18": lambda: limit_at_negative_infinity("sqrt(36*x**2 + 3)/x"),
   "01010-19": lambda: limit_at_negative_infinity("sqrt(25*x**2 + 8)/(2*x - 2)"),
   "01010-20": lambda: limit_at_negative_infinity("(4*x + 8)/sqrt(9*x**2 + 5)"),
   "01010-21": lambda: limit_at_negative_infinity("sqrt(9*x**2 + 4)/(4*x + 8)"),

   "01011-00": lambda: ivt_guarantee("01011-00", [("2", "-6"), ("3", "-1"), ("4", "-4"), ("9", "6")], 2, 9, -2),
   "01011-01": lambda: ivt_guarantee("01011-01", [("1", "-1"), ("4", "0"), ("6", "-1"), ("7", "2")], 1, 7, -2),
   "01011-02": lambda: ivt_guarantee("01011-02", [("0", "-9"), ("2", "-8"), ("6", "-1"), ("7", "5")], 0, 7, -2),
   "01011-03": lambda: ivt_guarantee("01011-03", [("1", "-7"), ("3", "-7"), ("6", "0"), ("8", "-8")], 1, 8, -4),
   "01011-04": lambda: ivt_guarantee("01011-04", [("4", "4"), ("5", "-1"), ("8", "-7"), ("9", "-7")], 4, 9, 3),
   "01011-05": lambda: ivt_guarantee("01011-05", [("2", "7"), ("3", "-3"), ("5", "6"), ("9", "-2")], 2, 9, -4),
   "01011-06": lambda: ivt_guarantee("01011-06", [("0", "0"), ("2", "7"), ("5", "6"), ("9", "4")], 0, 9, -3),
   "01011-07": lambda: ivt_guarantee("01011-07", [("1", "2"), ("2", "-1"), ("5", "6"), ("7", "8")], 1, 7, 7),
   "01011-08": lambda: ivt_guarantee("01011-08", [("0", "7"), ("2", "8"), ("3", "-6"), ("6", "2")], 0, 6, 3),
   "01011-09": lambda: ivt_guarantee("01011-09", [("3", "0"), ("4", "-4"), ("8", "4"), ("9", "4")], 3, 9, -3),
   "01011-10": lambda: ivt_guarantee("01011-10", [("0", "5"), ("4", "9"), ("6", "-4"), ("7", "5")], 0, 7, -7),
   "01011-11": lambda: ivt_guarantee("01011-11", [("3", "5"), ("4", "4"), ("8", "-5"), ("9", "-9")], 3, 9, 0),
   "01011-12": lambda: ivt_guarantee("01011-12", [("0", "-2"), ("1", "3"), ("4", "0"), ("9", "2")], 0, 9, -8),
   "01011-13": lambda: ivt_guarantee("01011-13", [("2", "-6"), ("3", "-1"), ("4", "1"), ("5", "2")], 2, 5, -4),
   "01011-14": lambda: ivt_guarantee("01011-14", [("3", "-9"), ("5", "-4"), ("6", "8"), ("9", "3")], 3, 9, -5),
   "01011-15": lambda: ivt_guarantee("01011-15", [("1", "6"), ("2", "4"), ("8", "2"), ("9", "2")], 1, 9, 3),
   "01011-16": lambda: ivt_guarantee("01011-16", [("1", "-1"), ("5", "0"), ("7", "-1"), ("9", "2")], 1, 9, 5),
   "01011-17": lambda: ivt_guarantee("01011-17", [("0", "7"), ("2", "-2"), ("3", "1"), ("6", "-5")], 0, 6, 5),
   "01011-18": lambda: ivt_guarantee("01011-18", [("2", "9"), ("3", "-7"), ("4", "-5"), ("6", "-1")], 2, 6, -6),
   "01011-19": lambda: ivt_guarantee("01011-19", [("1", "9"), ("2", "-9"), ("3", "3"), ("5", "7")], 1, 5, -1),
   "01011-20": lambda: ivt_guarantee("01011-20", [("0", "6"), ("3", "-3"), ("6", "-9"), ("7", "-8")], 0, 7, -4),
   "01011-21": lambda: ivt_guarantee("01011-21", [("3", "5"), ("4", "0"), ("7", "3"), ("9", "3")], 3, 9, 2),

   "01012-00": lambda: rate_from_table([("3.000", "24.000000"), ("3.100", "24.710000"), ("3.010", "24.070100"), ("3.001", "24.007001")]),
   "01012-01": lambda: rate_at("-4*x**2 + 4*x + 17", 5),
   "01012-02": lambda: rate_at("2*x**2 + 5*x + 10", 5),
   "01012-03": lambda: rate_at("2*x**2 + 5*x + 13", 3),
   "01012-04": lambda: rate_at("3*x**2 - 2*x + 7", 3),
   "01012-05": lambda: rate_at("-4*x**2 - 7*x + 20", 5),
   "01012-06": lambda: rate_from_table([("1.000", "10.000000"), ("1.100", "10.930000"), ("1.010", "10.090300"), ("1.001", "10.009003")]),
   "01012-07": lambda: rate_from_table([("3.000", "16.000000"), ("3.100", "16.710000"), ("3.010", "16.070100"), ("3.001", "16.007001")]),
   "01012-08": lambda: rate_at("4*x**2 + 3*x", 4),
   "01012-09": lambda: rate_at("4*x**2 + 4*x + 2", 4),
   "01012-10": lambda: rate_at("-4*x**2 + x + 12", 4),
   "01012-11": lambda: rate_at("-3*x**2 + 8*x + 3", 3),
   "01012-12": lambda: rate_from_table([("5.000", "-69.000000"), ("5.100", "-72.130000"), ("5.010", "-69.310300"), ("5.001", "-69.031003")]),
   "01012-13": lambda: rate_at("-2*x**2 + 4*x + 17", 4),
   "01012-14": lambda: rate_at("-x**2 - 6*x + 2", 5),
   "01012-15": lambda: rate_at("2*x**2 + x", 2),
   "01012-16": lambda: rate_at("2*x**2 + 9*x + 15", 3),
   "01012-17": lambda: rate_at("-3*x**2 + 8*x + 8", 5),
   "01012-18": lambda: rate_at("x**2 + 4", 2),
   "01012-19": lambda: rate_at("4*x**2 - x + 13", 5),
   "01012-20": lambda: rate_at("3*x**2 - 6*x + 4", 4),
   "01012-21": lambda: rate_at("-4*x**2 - x", 2),

   "01013-00": lambda: limit_meaning("01013-00", oo, None, S("19/2")),
   "01013-01": lambda: limit_meaning("01013-01", S("19/2"), "left", -oo),
   "01013-02": lambda: limit_meaning("01013-02", S("13/2"), "right", -oo),
   "01013-03": lambda: limit_meaning("01013-03", S("7"), "left", oo),
   "01013-04": lambda: limit_meaning("01013-04", S("-17/2"), "right", oo),
   "01013-05": lambda: limit_meaning("01013-05", -oo, None, S("5/2")),
   "01013-06": lambda: limit_meaning("01013-06", S("3"), "right", -oo),
   "01013-07": lambda: limit_meaning("01013-07", S("-7/2"), "right", oo),
   "01013-08": lambda: limit_meaning("01013-08", S("7/2"), "left", -oo),
   "01013-09": lambda: limit_meaning("01013-09", oo, None, S("-19/2")),
   "01013-10": lambda: limit_meaning("01013-10", -oo, None, S("17/2")),
   "01013-11": lambda: limit_meaning("01013-11", -oo, None, S("11/2")),
   "01013-12": lambda: limit_meaning("01013-12", S("-4"), "left", oo),
   "01013-13": lambda: limit_meaning("01013-13", S("19/2"), "left", oo),
   "01013-14": lambda: limit_meaning("01013-14", S("-6"), "left", -oo),
   "01013-15": lambda: limit_meaning("01013-15", S("10"), "left", -oo),
   "01013-16": lambda: limit_meaning("01013-16", oo, None, S("-9")),
   "01013-17": lambda: limit_meaning("01013-17", S("-15/2"), "right", oo),
   "01013-18": lambda: limit_meaning("01013-18", S("13/2"), "left", -oo),
   "01013-19": lambda: limit_meaning("01013-19", S("-3/2"), "right", -oo),
   "01013-20": lambda: limit_meaning("01013-20", -oo, None, S("5/2")),
   "01013-21": lambda: limit_meaning("01013-21", oo, None, S("5")),

   "01015-00": lambda: continuity_intervals("01015-00", "-3*sqrt(x)", "x - 6"),
   "01015-01": lambda: continuity_intervals("01015-01", "2 - 2*x", "x**2 - 4*x"),
   "01015-02": lambda: continuity_intervals("01015-02", "-3*sqrt(x - 2)", "x - 3"),
   "01015-03": lambda: continuity_intervals("01015-03", "-3*sqrt(x + 4)", "x - 1"),
   "01015-04": lambda: continuity_intervals("01015-04", "2 - 2*x", "x**2 - 16"),
   "01015-05": lambda: continuity_intervals("01015-05", "3*sqrt(x - 5)", "x - 6"),
   "01015-06": lambda: continuity_intervals("01015-06", "3*x - 15", "x**2 - 7*x + 12"),
   "01015-07": lambda: continuity_intervals("01015-07", "18 - 3*x", "x**2 + 6*x + 5"),
   "01015-08": lambda: continuity_intervals("01015-08", "4*sqrt(x + 6)", "x - 2"),
   "01015-09": lambda: continuity_intervals("01015-09", "sqrt(x + 4)", "x - 3"),
   "01015-10": lambda: continuity_intervals("01015-10", "6 - 2*x", "x**2 - 3*x - 4"),
   "01015-11": lambda: continuity_intervals("01015-11", "4*x + 8", "x**2 + x - 20"),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
