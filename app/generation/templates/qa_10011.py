"""BC-QA-10011, a Taylor polynomial assembled from a table of derivative values."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure
from app.generation.templates._helpers_h import polynomial_tex, taylor_polynomial

ARCHETYPE_ID = "BC-QA-10011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "degree", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3]}},
      {"name": "centre", "type": "integer", "role": "difficulty", "domain": {"values": [0, 1, 2, -1]}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "centre_row", "type": "integer", "role": "safe", "count": 5, "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "other_row", "type": "integer", "role": "safe", "count": 5, "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "centre_first", "type": "label", "role": "safe", "domain": {"values": ["yes", "no"]}},
   ],
   "constraints": [
      "centre_row[0] != other_row[0] or centre_row[1] != other_row[1]",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "degree", "difficulty_factor_id": "BC-DF-01", "settings": {"2": "low", "3": "medium"}},
      {"parameter": "centre", "difficulty_factor_id": "BC-DF-01", "settings": {"0": "low", "1": "medium", "2": "medium", "-1": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["degree", "centre", "gap", "centre_row", "other_row"]},
   ],
   "notes": "The table lists f and its first four derivatives at the centre and at a second point gap units to the right; every value is a nonzero integer, so each term of the polynomial is present.",
}

HEADERS = ["x", r"\( f(x) \)", r"\( f^{\prime}(x) \)", r"\( f^{\prime\prime}(x) \)", r"\( f^{\prime\prime\prime}(x) \)", r"\( f^{(4)}(x) \)"]


def _coefficients(values, degree):
   return [sympy.Integer(values[order]) / sympy.factorial(order) for order in range(degree + 1)]


def build(names):
   degree = int(names["degree"])
   centre = names["centre"]
   other = centre + names["gap"]
   centre_values = [int(value) for value in names["centre_row"]]
   other_values = [int(value) for value in names["other_row"]]

   centre_line = [str(centre)] + [str(value) for value in centre_values]
   other_line = [str(other)] + [str(value) for value in other_values]
   rows = [centre_line, other_line] if names["centre_first"] == "yes" else [other_line, centre_line]
   table = table_figure(
      HEADERS,
      rows,
      alt=(
         f"At x = {centre}: f = {centre_values[0]}, f' = {centre_values[1]}, f'' = {centre_values[2]}, f''' = {centre_values[3]}, "
         f"fourth derivative = {centre_values[4]}. At x = {other}: f = {other_values[0]}, f' = {other_values[1]}, "
         f"f'' = {other_values[2]}, f''' = {other_values[3]}, fourth derivative = {other_values[4]}."
      ),
   )

   coefficients = _coefficients(centre_values, degree)
   value = taylor_polynomial(coefficients, centre)
   stem = (
      f"The function f has derivatives of all orders. Values of f and its first four derivatives at two inputs are given in "
      f"the table. Find the Taylor polynomial of degree {degree} for f about {math(f'x = {centre}')}."
   )

   divided = ", ".join(
      math(rf"\frac{{{centre_values[order]}}}{{{order}!}}") for order in range(degree + 1)
   )
   steps = [
      Step(text=f"Read the row for {math(f'x = {centre}')}: the values of f and its first {degree} derivatives there are {', '.join(str(centre_values[order]) for order in range(degree + 1))}.", rule="read the table"),
      Step(text=f"Divide the kth derivative value by k! to get the coefficients {divided}.", rule="Taylor coefficients"),
      Step(text=f"Attach the powers of the displacement from {centre}: {math(f'P_{degree}(x) = ' + polynomial_tex(coefficients, centre))}.", value=value, point_type_id="BC-PT-99035", rule="Taylor polynomial"),
   ]

   raw = [sympy.Integer(centre_values[order]) for order in range(degree + 1)]
   extra = _coefficients(centre_values, degree + 1)
   distractors = [
      Distractor("BC-ERR-10029", "each derivative value used as the coefficient with no factorial in the denominator", value=taylor_polynomial(raw, centre), mechanism="algebra_slip"),
      Distractor("BC-ERR-10030", f"the next derivative in the table used as well, so the polynomial runs one degree past {degree}", value=taylor_polynomial(extra, centre), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-10031", f"the derivative values read from the row for x = {other} instead of x = {centre}", value=taylor_polynomial(_coefficients(other_values, degree), centre), mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="find",
   )
