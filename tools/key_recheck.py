"""Mechanical recheck of an item bank's keys against answers computed from the stems.

Usage: python3 tools/key_recheck.py <items_dir> <formulations.py> [--report out.md]

A formulations file maps each item id to a function that computes, in SymPy and from the stem
text alone, the answer the stem asks for. It is written by reading stems only, never the stored
key, so that a match is evidence. content/items_p1_agent/key_formulations.py is the P1 one.

Per item the recheck reports:

- key: whether the stored key equals the computed answer;
- options: whether exactly the option marked as the key equals the computed answer, so a
  distractor equal to the key (an ambiguous item) and a key marked on the wrong option both show;
- stem: whether the stem is worded as a choice ("Which of the following"), which reads wrongly
  whenever R29 serves the item as a short answer with no options shown.

Equivalence is symbolic simplification, then numeric evaluation at seeded points, and a check
that cannot evaluate enough points raises instead of calling the pair equal. Before trusting any
result the run perturbs a spread of computed answers and requires every perturbation to be
reported as different; if one is not, the comparator is blind and the run exits 2.

Exit 0 when every item is formulated and clean, 1 when anything is flagged, 2 when the control
fails.
"""
import argparse
import importlib.util
import json
import random
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sympy

from app.items.mathjson import to_sympy

x, y = sympy.symbols("x y")
t, theta = sympy.symbols("t theta")
increment = sympy.Symbol("h")

NUMERIC_SAMPLE_POINTS = 12
MINIMUM_EVALUATED_POINTS = 6
EQUALITY_TOLERANCE = 1e-9
CONTROL_SAMPLE_SIZE = 8
CHOICE_WORDING = re.compile(r"which (of the following|expression)", re.IGNORECASE)

KEY_MATCHES = "key_matches"
KEY_DIFFERS = "key_differs"
NOT_FORMULATED = "not_formulated"
NOT_UNIQUE = "computed_answer_not_unique"
FORMULATION_FAILED = "formulation_failed"
OPTION_MISMATCH = "option_mismatch"
CHOICE_WORDED_STEM = "choice_worded_stem"
COMPARISON_UNDECIDED = "comparison_undecided"


class ComparisonUndecided(ValueError):
   pass


def limit_at(expression, point, direction="+-"):
   return sympy.limit(expression, x, point, direction)


def derivative(expression, variable=x, order=1):
   return sympy.diff(expression, variable, order)


def derivative_by_definition(expression, variable=x):
   quotient = (expression.subs(variable, variable + increment) - expression) / increment

   return sympy.limit(quotient, increment, 0)


def implicit_slope(curve):
   """dy/dx on curve = 0, as -F_x / F_y."""
   return -sympy.diff(curve, x) / sympy.diff(curve, y)


def implicit_second_derivative(curve):
   slope = implicit_slope(curve)

   return sympy.diff(slope, x) + sympy.diff(slope, y) * slope


def second_derivative_along_solution(slope_field):
   """d2y/dx2 for dy/dx = f(x, y), as f_x + f_y f."""
   return sympy.diff(slope_field, x) + sympy.diff(slope_field, y) * slope_field


def tangent_line(expression, at):
   value = expression.subs(x, at)
   slope = derivative(expression).subs(x, at)

   return sympy.expand(value + slope * (x - at))


def continuity_solutions(unknowns, pieces, joints):
   """Solves for the unknowns that make consecutive pieces meet at each joint. A joint given as
   (x0, value) also pins the function's value there."""
   equations = []

   for index, joint in enumerate(joints):
      has_point_value = isinstance(joint, tuple)
      at = joint[0] if has_point_value else joint
      from_left = sympy.limit(pieces[index], x, at, "-")
      from_right = sympy.limit(pieces[index + 1], x, at, "+")

      if has_point_value:
         equations.extend([sympy.Eq(from_left, joint[1]), sympy.Eq(from_right, joint[1])])
      else:
         equations.append(sympy.Eq(from_left, from_right))

   return sympy.solve(equations, unknowns, dict=True)


def continuity_value(unknown, pieces, joints, all_unknowns=None):
   solutions = continuity_solutions(all_unknowns or [unknown], pieces, joints)

   return [solution[unknown] for solution in solutions]


def integer_sum_of_interval_containing(domain, anchor):
   pieces = domain.args if isinstance(domain, sympy.Union) else (domain,)

   for piece in pieces:
      holds_the_anchor = piece.contains(anchor) == sympy.true

      if not holds_the_anchor:
         continue

      is_bounded = piece.inf != -sympy.oo and piece.sup != sympy.oo

      if not is_bounded:
         raise ValueError(f"the interval holding {anchor} is unbounded: {piece}")

      integers = range(int(sympy.ceiling(piece.inf)), int(sympy.floor(piece.sup)) + 1)

      return sum(number for number in integers if piece.contains(number) == sympy.true)

   raise ValueError(f"no continuous interval holds {anchor}")


def continuous_domain(expression, over=sympy.S.Reals):
   return sympy.calculus.util.continuous_domain(expression, x, over)


def real_points(curve, condition, quadrant=None):
   signs_by_quadrant = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}
   points = []

   for solution in sympy.solve([curve, condition], [x, y], dict=True):
      point_x = complex(solution[x])
      point_y = complex(solution[y])
      is_real = abs(point_x.imag) < EQUALITY_TOLERANCE and abs(point_y.imag) < EQUALITY_TOLERANCE

      if not is_real:
         continue

      exact_x = sympy.nsimplify(solution[x]) if solution[x].is_real else sympy.nsimplify(point_x.real)
      exact_y = sympy.nsimplify(solution[y]) if solution[y].is_real else sympy.nsimplify(point_y.real)
      in_quadrant = quadrant is None or (sympy.sign(exact_x), sympy.sign(exact_y)) == signs_by_quadrant[quadrant]

      if in_quadrant:
         points.append((exact_x, exact_y))

   return points


def horizontal_tangent_points(curve, quadrant=None):
   candidates = real_points(curve, sympy.diff(curve, x), quadrant)

   return [point for point in candidates if sympy.diff(curve, y).subs({x: point[0], y: point[1]}) != 0]


def vertical_tangent_points(curve, quadrant=None):
   candidates = real_points(curve, sympy.diff(curve, y), quadrant)

   return [point for point in candidates if sympy.diff(curve, x).subs({x: point[0], y: point[1]}) != 0]


def definite_integral(integrand, lower, upper, variable=x):
   """Also the improper case: pass sympy.oo as a limit, or a limit where the integrand is unbounded."""
   return sympy.integrate(integrand, (variable, lower, upper))


def pinned_antiderivative_value(integrand, anchor, anchor_value, at, variable=x):
   """F(at) for the antiderivative F of integrand with F(anchor) = anchor_value."""
   return anchor_value + definite_integral(integrand, anchor, at, variable)


def accumulation_derivative(integrand, lower, upper, at, variable=t):
   """d/dx of the integral of integrand(t) dt from lower(x) to upper(x), at x = at, by the
   fundamental theorem and the chain rule, never by integrating first."""
   rate_through_upper = integrand.subs(variable, upper) * sympy.diff(upper, x)
   rate_through_lower = integrand.subs(variable, lower) * sympy.diff(lower, x)

   return sympy.simplify((rate_through_upper - rate_through_lower).subs(x, at))


def trapezoidal_sum(points):
   """points: (input, value) pairs in increasing input order, spacing allowed to vary."""
   total = sympy.Integer(0)

   for (left_input, left_value), (right_input, right_value) in zip(points, points[1:]):
      width = sympy.nsimplify(right_input) - sympy.nsimplify(left_input)
      total += width * (sympy.nsimplify(left_value) + sympy.nsimplify(right_value)) / 2

   return total


def riemann_sum_limit(term, index, count, first=1):
   """The limit as count grows of the sum of term over index = first .. count."""
   partial_sum = sympy.summation(term, (index, first, count))

   return sympy.limit(partial_sum, count, sympy.oo)


def series_value(term, index, first):
   return sympy.summation(term, (index, first, sympy.oo))


def first_omitted_term(term, index, last_index):
   """The alternating series error bound for the partial sum ending at last_index."""
   return sympy.Abs(term.subs(index, last_index + 1))


def least_terms_for_tolerance(term, index, first, tolerance, search_limit=10000):
   """The least number of terms whose alternating series error bound is below tolerance."""
   for last_index in range(first, first + search_limit):
      bound = first_omitted_term(term, index, last_index)
      is_within = bool(bound < tolerance)

      if is_within:
         return last_index - first + 1

   raise ValueError(f"no partial sum within {tolerance} in {search_limit} terms")


def limit_comparison_value(term, comparison_term, index):
   return sympy.limit(term / comparison_term, index, sympy.oo)


def lagrange_error_bound(derivative_bound, at, center, degree):
   return derivative_bound * sympy.Abs(sympy.nsimplify(at) - center) ** (degree + 1) / sympy.factorial(degree + 1)


def radius_of_convergence(term, index, center=0, variable=x):
   """From the ratio test on the general term, which carries the variable: the displacement at
   which the limit of the ratio of consecutive terms equals 1."""
   displacement = sympy.Symbol("displacement", positive=True)
   at_displacement = term.subs(variable, center + displacement)
   ratio = sympy.simplify(at_displacement.subs(index, index + 1) / at_displacement)
   limit = sympy.limit(sympy.Abs(ratio), index, sympy.oo)

   if limit.is_zero:
      raise ValueError("the ratio tends to 0, so the radius is infinite")

   return sympy.solve(sympy.Eq(limit, 1), displacement)


def taylor_polynomial(expression, center, degree, variable=x):
   return sympy.expand(sympy.series(expression, variable, center, degree + 1).removeO())


def taylor_from_derivatives(values, center, variable=x):
   """values[k] is the k-th derivative at center, values[0] the function value."""
   return sympy.expand(sum(
      sympy.nsimplify(value) * (variable - center) ** order / sympy.factorial(order)
      for order, value in enumerate(values)
   ))


def derivatives_along_solution(slope_field, center, value, count):
   """f(center), f'(center), ... up to count values, for y' = slope_field(x, y) and y(center) = value."""
   values = [sympy.nsimplify(value)]
   current = slope_field

   for _ in range(count - 1):
      values.append(sympy.simplify(current.subs({x: center, y: value})))
      current = sympy.diff(current, x) + sympy.diff(current, y) * slope_field

   return values


def taylor_from_relation(slope_field, center, value, degree):
   return taylor_from_derivatives(derivatives_along_solution(slope_field, center, value, degree + 1), center)


def euler_approximation(slope_field, start_x, start_y, step, steps):
   current_x = sympy.nsimplify(start_x)
   current_y = sympy.nsimplify(start_y)
   step = sympy.nsimplify(step)

   for _ in range(steps):
      current_y = current_y + step * slope_field.subs({x: current_x, y: current_y})
      current_x = current_x + step

   return sympy.simplify(current_y)


def particular_solutions(slope_field, start_x, start_y):
   """Every explicit solution of y' = slope_field(x, y) through (start_x, start_y)."""
   unknown = sympy.Function("solution")
   equation = sympy.Eq(unknown(x).diff(x), slope_field.subs(y, unknown(x)))
   found = sympy.dsolve(equation, unknown(x), ics={unknown(start_x): start_y})
   found = found if isinstance(found, list) else [found]

   return [solution.rhs for solution in found if sympy.simplify(solution.rhs.subs(x, start_x) - start_y) == 0]


def is_solution(candidate, slope_field):
   residual = sympy.diff(candidate, x) - slope_field.subs(y, candidate)

   return sympy.simplify(residual) == 0


def polar_slope(radius, at, variable=theta):
   horizontal = radius * sympy.cos(variable)
   vertical = radius * sympy.sin(variable)
   slope = sympy.diff(vertical, variable) / sympy.diff(horizontal, variable)

   return sympy.simplify(slope.subs(variable, at))


def related_rate(curve, point, known_rate, known="x"):
   """The rate of the other coordinate of a point moving on curve = 0, from F_x x' + F_y y' = 0."""
   at_point = {x: point[0], y: point[1]}
   on_curve = sympy.simplify(curve.subs(at_point)) == 0

   if not on_curve:
      raise ValueError(f"{point} is not on the curve")

   partial_x = sympy.diff(curve, x).subs(at_point)
   partial_y = sympy.diff(curve, y).subs(at_point)

   if known == "x":
      return sympy.simplify(-partial_x * known_rate / partial_y)

   return sympy.simplify(-partial_y * known_rate / partial_x)


def function_with_values(center, values, variable=x):
   """The polynomial whose value and derivatives at center are the given values, standing in for a
   function a stem describes only through those values."""
   return taylor_from_derivatives(values, center, variable)


def equivalent(left, right):
   difference = sympy.simplify(sympy.expand_trig(sympy.sympify(left) - sympy.sympify(right)))
   is_zero = difference == 0

   if is_zero:
      return True

   symbols = sorted(difference.free_symbols, key=str)
   rng = random.Random(1)
   evaluated = 0

   for _ in range(NUMERIC_SAMPLE_POINTS):
      point = {symbol: sympy.Rational(rng.randint(11, 29), 10) for symbol in symbols}

      try:
         value = complex(difference.subs(point).evalf())
      except (TypeError, ValueError):
         continue

      evaluated += 1
      differs = abs(value) > EQUALITY_TOLERANCE

      if differs:
         return False

   too_few_points = evaluated < MINIMUM_EVALUATED_POINTS

   if too_few_points:
      raise ComparisonUndecided(f"only {evaluated} of {NUMERIC_SAMPLE_POINTS} points evaluated for {difference}")

   return True


@dataclass
class ItemResult:
   item_id: str
   flags: list = field(default_factory=list)
   stored_key: str = ""
   computed: str = ""
   note: str = ""

   @property
   def is_clean(self):
      return self.flags == [KEY_MATCHES]


def single_answer(computed):
   is_list = isinstance(computed, (list, tuple, set))

   if not is_list:
      return computed

   distinct = list(dict.fromkeys(computed))
   is_unique = len(distinct) == 1

   if not is_unique:
      raise ValueError(f"{NOT_UNIQUE}: {distinct}")

   return distinct[0]


def compare_with_key_and_options(result, record, computed, key):
   result.flags.append(KEY_MATCHES if equivalent(computed, key) else KEY_DIFFERS)
   options = record.get("options") or []
   equal_options = [option["id"] for option in options if equivalent(computed, to_sympy(option["value"]))]
   marked_keys = [option["id"] for option in options if option["is_key"]]
   has_options = len(options) > 0
   options_disagree = has_options and equal_options != marked_keys

   if options_disagree:
      result.flags.append(OPTION_MISMATCH)
      result.note = f"options equal to the computed answer {equal_options}, marked key {marked_keys}"


def check_item(record, formulation):
   result = ItemResult(item_id=record["id"])
   key = to_sympy(record["answer_key"]["mathjson"])
   result.stored_key = sympy.sstr(key)
   is_choice_worded = CHOICE_WORDING.search(record["stem"]["text"]) is not None

   if formulation is None:
      result.flags.append(NOT_FORMULATED)
   else:
      try:
         computed = single_answer(formulation())
      except ValueError as refused:
         is_not_unique = str(refused).startswith(NOT_UNIQUE)
         result.flags.append(NOT_UNIQUE if is_not_unique else FORMULATION_FAILED)
         result.note = str(refused)
      else:
         result.computed = sympy.sstr(sympy.simplify(computed))

         try:
            compare_with_key_and_options(result, record, computed, key)
         except ComparisonUndecided as undecided:
            result.flags.append(COMPARISON_UNDECIDED)
            result.note = str(undecided)

   if is_choice_worded:
      result.flags.append(CHOICE_WORDED_STEM)

   return result


def perturbations(value):
   """2v + 1 changes scale and offset; it leaves -1 fixed, so a translation by an offset no key is
   plausibly wrong by also runs. A perturbation identical to the value is dropped, never counted."""
   value = sympy.sympify(value)
   candidates = [value * 2 + 1, value + sympy.sqrt(2) / 7]

   return [candidate for candidate in candidates if sympy.simplify(candidate - value) != 0]


def control_holds(records, formulations):
   """Every perturbation of a computed answer must be reported as different from its stored key."""
   formulated = [record for record in records if record["id"] in formulations]
   rng = random.Random(7)
   chosen = rng.sample(formulated, min(CONTROL_SAMPLE_SIZE, len(formulated)))
   blind_on = []

   for record in chosen:
      try:
         computed = single_answer(formulations[record["id"]]())
      except ValueError:
         continue

      key = to_sympy(record["answer_key"]["mathjson"])

      compares_equal = [equivalent(changed, key) for changed in perturbations(computed)]

      if any(compares_equal):
         blind_on.append(record["id"])

   return blind_on


def load_formulations(path):
   spec = importlib.util.spec_from_file_location("key_formulations", path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

   return module.FORMULATIONS


def recheck(items_dir, formulations):
   records = [json.loads(path.read_text()) for path in sorted(Path(items_dir).glob("ITM-*.json"))]
   blind_on = control_holds(records, formulations)
   results = [check_item(record, formulations.get(record["id"])) for record in records]

   return results, blind_on


def report_lines(results):
   lines = ["| Item | Stored key | Computed from the stem | Flags | Note |", "| --- | --- | --- | --- | --- |"]

   for result in results:
      stored = result.stored_key.replace("|", "\\|")
      computed = result.computed.replace("|", "\\|")
      lines.append(f"| {result.item_id} | `{stored}` | `{computed}` | {', '.join(result.flags)} | {result.note} |")

   return lines


def main(argv):
   parser = argparse.ArgumentParser(description="Recheck an item bank's keys against answers computed from its stems.")
   parser.add_argument("items_dir")
   parser.add_argument("formulations")
   parser.add_argument("--report")
   arguments = parser.parse_args(argv[1:])

   results, blind_on = recheck(arguments.items_dir, load_formulations(arguments.formulations))
   comparator_is_blind = len(blind_on) > 0

   if comparator_is_blind:
      print(f"control failed: a perturbed answer compared equal on {', '.join(blind_on)}", file=sys.stderr)

      return 2

   flagged = [result for result in results if not result.is_clean]
   print(f"control: {CONTROL_SAMPLE_SIZE} perturbed answers all reported as different")
   print(f"items: {len(results)}, clean: {len(results) - len(flagged)}, flagged: {len(flagged)}")

   for result in flagged:
      print(f"  {result.item_id}: {', '.join(result.flags)} {result.note}".rstrip())

   if arguments.report:
      Path(arguments.report).write_text("\n".join(report_lines(results)) + "\n")

   return 1 if flagged else 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
