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
   "01014-00": [
      "Substitution gives 0/0, so factor both parts and cancel \\( x - 1 \\), and then substitute, which gives \\( -1 \\).",
      "Substitution makes the numerator \\( x^{2} - 3 x + 2 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = 1 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x^{2} - x \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-01": [
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), an indeterminate form, which means the limit does not exist.",
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\).",
      "As x grows the leading terms dominate, so take the ratio of the leading coefficients, which gives \\( \\frac{4}{3} \\).",
      "Substituting \\( x = \\infty \\) gives \\( \\frac{\\infty}{\\infty} \\), so the infinities cancel, which gives \\( 1 \\).",
   ],
   "01014-02": [
      "Substitution gives \\( \\frac{6}{0} \\), so check the sign on each side of \\( x = 1 \\), which gives \\( -\\infty \\) and \\( \\infty \\), so no limit exists.",
      "Substitution gives \\( \\frac{6}{0} \\), so the quotient grows without bound, which gives \\( \\infty \\) from both sides.",
      "The denominator \\( x - 1 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{6}{0} \\).",
      "The quotient is undefined at \\( x = 1 \\), so no sign check is needed, which means the limit does not exist.",
   ],
   "01014-03": [
      "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 12} + 3 \\) and cancel \\( x + 3 \\), and then substitute, which gives \\( \\frac{1}{6} \\).",
      "Substitution makes the numerator \\( \\sqrt{x + 12} - 3 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -3 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 3 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-04": [
      "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 7} + 2 \\) and cancel \\( x + 3 \\), and then substitute, which gives \\( \\frac{1}{4} \\).",
      "Substitution makes the numerator \\( \\sqrt{x + 7} - 2 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -3 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 3 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-05": [
      "Substitution gives 0/0, so combine the fractions over \\( -4 x \\) and cancel \\( x + 4 \\), and then substitute, which gives \\( - \\frac{1}{16} \\).",
      "Substitution makes the numerator \\( \\frac{1}{x} - \\frac{1}{-4} \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -4 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 4 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-06": [
      "Substitution gives 0/0, so combine the fractions over \\( -5 x \\) and cancel \\( x + 5 \\), and then substitute, which gives \\( - \\frac{1}{25} \\).",
      "Substitution makes the numerator \\( \\frac{1}{x} - \\frac{1}{-5} \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -5 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 5 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-07": [
      "Substitution gives 0/0, so factor both parts and cancel \\( x - 3 \\), and then substitute, which gives \\( \\frac{3}{4} \\).",
      "Substitution makes the numerator \\( x^{2} - 9 x + 18 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = 3 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x^{2} - 10 x + 21 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-08": [
      "Substitution gives 0/0, so combine the fractions over \\( 2 x \\) and cancel \\( x - 2 \\), and then substitute, which gives \\( - \\frac{1}{4} \\).",
      "Substitution makes the numerator \\( \\frac{1}{x} - \\frac{1}{2} \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = 2 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x - 2 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-09": [
      "Substitution gives 0/0, so combine the fractions over \\( -3 x \\) and cancel \\( x + 3 \\), and then substitute, which gives \\( - \\frac{1}{9} \\).",
      "Substitution makes the numerator \\( \\frac{1}{x} - \\frac{1}{-3} \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -3 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 3 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-10": [
      "Substitution gives 0/0, so combine the fractions over \\( -1 x \\) and cancel \\( x + 1 \\), and then substitute, which gives \\( -1 \\).",
      "Substitution makes the numerator \\( \\frac{1}{x} - \\frac{1}{-1} \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -1 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 1 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-11": [
      "Substitution gives 0/0, so combine the fractions over \\( 4 x \\) and cancel \\( x - 4 \\), and then substitute, which gives \\( - \\frac{1}{16} \\).",
      "Substitution makes the numerator \\( \\frac{1}{x} - \\frac{1}{4} \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = 4 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x - 4 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-12": [
      "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 10} + 3 \\) and cancel \\( x + 1 \\), and then substitute, which gives \\( \\frac{1}{6} \\).",
      "Substitution makes the numerator \\( \\sqrt{x + 10} - 3 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -1 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 1 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-13": [
      "Substitution gives \\( \\frac{3}{0} \\), so check the sign on each side of \\( x = 2 \\), which gives \\( \\infty \\) on both sides.",
      "Substitution gives \\( \\frac{3}{0} \\), so the quotient grows without bound, which means the limit exists and equals \\( \\infty \\).",
      "The denominator \\( \\left(x - 2\\right)^{2} \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{3}{0} \\).",
      "The quotient is undefined at \\( x = 2 \\), so no sign check is needed, which means the limit does not exist.",
   ],
   "01014-14": [
      "Substitution gives 0/0, so multiply both parts by the conjugate \\( \\sqrt{x + 6} + 2 \\) and cancel \\( x + 2 \\), and then substitute, which gives \\( \\frac{1}{4} \\).",
      "Substitution makes the numerator \\( \\sqrt{x + 6} - 2 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -2 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x + 2 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-15": [
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), an indeterminate form, which means the limit does not exist.",
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\).",
      "As x grows the leading terms dominate, so take the ratio of the leading coefficients, which gives \\( \\frac{1}{2} \\).",
      "Substituting \\( x = \\infty \\) gives \\( \\frac{\\infty}{\\infty} \\), so the infinities cancel, which gives \\( 1 \\).",
   ],
   "01014-16": [
      "Substitution gives \\( \\frac{9}{0} \\), so check the sign on each side of \\( x = 2 \\), which gives \\( -\\infty \\) and \\( \\infty \\), so no limit exists.",
      "Substitution gives \\( \\frac{9}{0} \\), so the quotient grows without bound, which gives \\( \\infty \\) from both sides.",
      "The denominator \\( x - 2 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{9}{0} \\).",
      "The quotient is undefined at \\( x = 2 \\), so no sign check is needed, which means the limit does not exist.",
   ],
   "01014-17": [
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), an indeterminate form, which means the limit does not exist.",
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\).",
      "As x grows the leading terms dominate, so take the ratio of the leading coefficients, which gives \\( 4 \\).",
      "Substituting \\( x = \\infty \\) gives \\( \\frac{\\infty}{\\infty} \\), so the infinities cancel, which gives \\( 1 \\).",
   ],
   "01014-18": [
      "Substitution gives 0/0, so factor both parts and cancel \\( x + 1 \\), and then substitute, which gives \\( - \\frac{3}{2} \\).",
      "Substitution makes the numerator \\( x^{2} - 4 x - 5 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -1 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x^{2} + 6 x + 5 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-19": [
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), an indeterminate form, which means the limit does not exist.",
      "As x grows the form is \\( \\frac{\\infty}{\\infty} \\), so divide both parts by \\( x^{2} \\), which gives \\( 0 \\).",
      "As x grows the leading terms dominate, so take the ratio of the leading coefficients, which gives \\( \\frac{1}{3} \\).",
      "Substituting \\( x = \\infty \\) gives \\( \\frac{\\infty}{\\infty} \\), so the infinities cancel, which gives \\( 1 \\).",
   ],
   "01014-20": [
      "Substitution gives 0/0, so factor both parts and cancel \\( x + 4 \\), and then substitute, which gives \\( \\frac{7}{3} \\).",
      "Substitution makes the numerator \\( x^{2} + x - 12 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -4 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x^{2} + 5 x + 4 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
   "01014-21": [
      "Substitution gives 0/0, so factor both parts and cancel \\( x + 1 \\), and then substitute, which gives \\( \\frac{7}{3} \\).",
      "Substitution makes the numerator \\( x^{2} - 5 x - 6 \\) equal to 0, so no rewriting is needed, which gives \\( 0 \\).",
      "Substitution of \\( x = -1 \\) gives 0/0, so no procedure applies, which means the limit does not exist.",
      "The denominator \\( x^{2} - x - 2 \\) has a limit, so divide the limit of the numerator by it, which gives \\( \\frac{0}{0} \\).",
   ],
}

BY_SUFFIX = {
   "01014-00": lambda: form_and_result("01014-00", "x**2 - 3*x + 2", "x**2 - x", 1),
   "01014-01": lambda: form_and_result("01014-01", "4*x + 5", "3*x**2 + 4", oo),
   "01014-02": lambda: form_and_result("01014-02", "x + 5", "x - 1", 1),
   "01014-03": lambda: form_and_result("01014-03", "sqrt(x + 12) - 3", "x + 3", -3),
   "01014-04": lambda: form_and_result("01014-04", "sqrt(x + 7) - 2", "x + 3", -3),
   "01014-05": lambda: form_and_result("01014-05", "1/4 + 1/x", "x + 4", -4),
   "01014-06": lambda: form_and_result("01014-06", "1/5 + 1/x", "x + 5", -5),
   "01014-07": lambda: form_and_result("01014-07", "x**2 - 9*x + 18", "x**2 - 10*x + 21", 3),
   "01014-08": lambda: form_and_result("01014-08", "-1/2 + 1/x", "x - 2", 2),
   "01014-09": lambda: form_and_result("01014-09", "1/3 + 1/x", "x + 3", -3),
   "01014-10": lambda: form_and_result("01014-10", "1 + 1/x", "x + 1", -1),
   "01014-11": lambda: form_and_result("01014-11", "-1/4 + 1/x", "x - 4", 4),
   "01014-12": lambda: form_and_result("01014-12", "sqrt(x + 10) - 3", "x + 1", -1),
   "01014-13": lambda: form_and_result("01014-13", "x + 1", "(x - 2)**2", 2),
   "01014-14": lambda: form_and_result("01014-14", "sqrt(x + 6) - 2", "x + 2", -2),
   "01014-15": lambda: form_and_result("01014-15", "2*x + 2", "4*x**2 + 3", oo),
   "01014-16": lambda: form_and_result("01014-16", "x + 7", "x - 2", 2),
   "01014-17": lambda: form_and_result("01014-17", "4*x + 5", "x**2 - 5", oo),
   "01014-18": lambda: form_and_result("01014-18", "x**2 - 4*x - 5", "x**2 + 6*x + 5", -1),
   "01014-19": lambda: form_and_result("01014-19", "2*x - 4", "6*x**2 + 2", oo),
   "01014-20": lambda: form_and_result("01014-20", "x**2 + x - 12", "x**2 + 5*x + 4", -4),
   "01014-21": lambda: form_and_result("01014-21", "x**2 - 5*x - 6", "x**2 - x - 2", -1),
}

FORMULATIONS = {f"{ITEM_PREFIX}{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
