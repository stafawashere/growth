"""BC-QA-03006, the derivative of an inverse function at a value, from a table of the original."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-03006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "values", "type": "integer", "role": "safe", "count": 4, "distinct": True, "order": "increasing", "domain": {"min": -3, "max": 9, "step": 1}},
      {"name": "slopes", "type": "integer", "role": "safe", "count": 4, "domain": {"min": 1, "max": 7, "step": 1}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "names", "type": "label", "role": "safe", "domain": {"values": ["f,g", "p,q", "h,k"]}},
   ],
   "constraints": [
      "target in [1, 2, 3, 4]",
      "target != at",
      "distinct([1 / slopes[at - 1], 1 / slopes[target - 1], 1 / target, 1 / values[target - 1]])",
      "values[target - 1] != 0",
   ],
   "derived": [
      {"name": "target", "expression": "values[at - 1]"},
   ],
   "invariants": [
      "exact(key)",
      "key == 1 / slopes[at - 1]",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["values", "slopes", "at"]},
   ],
   "notes": (
      "The table lists x = 1 to 4 with increasing values and positive derivatives, so the function is one to one "
      "there. The requested value is one of the listed outputs and is also a different row's input, so the row "
      "read at the given value is always available as the tempting wrong row."
   ),
}


def build(names):
   values = [int(value) for value in names["values"]]
   slopes = [int(value) for value in names["slopes"]]
   at = int(names["at"])
   function, inverse = names["names"].split(",")
   target = values[at - 1]
   matching_slope = sympy.Integer(slopes[at - 1])
   key_value = 1 / matching_slope

   rows = [[str(index + 1), str(values[index]), str(slopes[index])] for index in range(4)]
   columns = [math("x"), math(f"{function}(x)"), math(f"{function}'(x)")]
   alt_rows = "; ".join(f"at x = {row[0]}, {function} = {row[1]} and {function}' = {row[2]}" for row in rows)
   table = table_figure(columns, rows, alt=f"A table of values: {alt_rows}.")

   stem = (
      f"The function {function} is differentiable and increasing, and {inverse} is the inverse function of "
      f"{function}. The table gives values of {function} and {function}' at selected values of x. "
      f"Find the exact value of {math(f"{inverse}'({target})")}."
   )

   steps = [
      Step(
         text=(
            f"The value {target} is an output of {function}: from the table, {math(f'{function}({at}) = {target}')}, "
            f"so {math(f'{inverse}({target}) = {at}')}."
         ),
         rule="find the matching input",
      ),
      Step(
         text=(
            f"At that input {math(f"{function}'({at}) = {slopes[at - 1]}")}, which is not zero, so the inverse is "
            f"differentiable at {target} and {math(rf"{inverse}'({target}) = \frac{{1}}{{{function}'({inverse}({target}))}} = \frac{{1}}{{{function}'({at})}} = {tex(key_value)}")}."
         ),
         value=key_value,
         rule="derivative of an inverse function",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03015",
         derivation=f"the reciprocal of {function}' taken in the row x = {target} instead of at the matching input {at}",
         value=sympy.Rational(1, slopes[target - 1]),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-03016",
         derivation=f"the reciprocal of the function value {function}({at}) = {target} instead of the reciprocal of the derivative",
         value=sympy.Rational(1, target),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-03016",
         derivation=(
            f"the reciprocal of a function value instead of a derivative, read in the row x = {target}: "
            f"1 / {function}({target})"
         ),
         value=sympy.Rational(1, values[target - 1]),
         mechanism="compound",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="find",
   )
