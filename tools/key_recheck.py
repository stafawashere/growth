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


def perturbed(value):
   return sympy.sympify(value) * 2 + 1


def control_holds(records, formulations):
   """Every perturbed computed answer must be reported as different from its stored key."""
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

      if equivalent(perturbed(computed), key):
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
