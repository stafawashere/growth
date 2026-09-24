"""BC-QA-03002, the derivative of a composite evaluated from a table of values."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-03002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "f_values", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "f_slopes", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "g_values", "type": "integer", "role": "safe", "count": 4, "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "g_slopes", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "names", "type": "label", "role": "safe", "domain": {"values": ["f,g", "p,q", "u,v"]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["forward", "reversed"]}},
   ],
   "constraints": [
      "inner != at",
      "outer_slope != 0",
      "inner_slope != 0",
      "outer_value != 0",
      "f_slopes[at - 1] != 0",
      "distinct(options)",
   ],
   "derived": [
      {"name": "inner", "expression": "g_values[at - 1]"},
      {"name": "outer_slope", "expression": "f_slopes[inner - 1]"},
      {"name": "outer_value", "expression": "f_values[inner - 1]"},
      {"name": "inner_slope", "expression": "g_slopes[at - 1]"},
      {"name": "chain", "expression": "outer_slope * inner_slope"},
      {
         "name": "options",
         "expression": (
            "[chain, f_slopes[at - 1] * inner_slope, outer_slope + inner_slope, outer_value * inner_slope] "
            "if direction == 'forward' else "
            "[inner_slope, chain / f_slopes[at - 1], chain - outer_slope, chain / outer_value]"
         ),
      },
   ],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "key == options[0]",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-13", "settings": {"forward": "off", "reversed": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["f_values", "f_slopes", "g_values", "g_slopes", "at"]},
   ],
   "notes": (
      "The table lists x = 1 to 4 with the values and derivatives of two functions; the inner function "
      "takes values in 1 to 4 so its output at the requested input is always a row of the table, and never "
      "the same row. The reversed form gives the composite's derivative and blanks the inner derivative."
   ),
}


def _paren(value):
   text = tex(value)

   return rf"\left({text}\right)" if value < 0 else text


def build(names):
   f_values = [int(value) for value in names["f_values"]]
   f_slopes = [int(value) for value in names["f_slopes"]]
   g_values = [int(value) for value in names["g_values"]]
   g_slopes = [int(value) for value in names["g_slopes"]]
   at = int(names["at"])
   outer_name, inner_name = names["names"].split(",")
   is_reversed = names["direction"] == "reversed"

   inner = g_values[at - 1]
   outer_slope = sympy.Integer(f_slopes[inner - 1])
   outer_value = sympy.Integer(f_values[inner - 1])
   inner_slope = sympy.Integer(g_slopes[at - 1])
   wrong_row_slope = sympy.Integer(f_slopes[at - 1])
   chain = outer_slope * inner_slope

   inner_slope_cells = [str(value) for value in g_slopes]

   if is_reversed:
      inner_slope_cells[at - 1] = "?"

   rows = []

   for index in range(4):
      rows.append([
         str(index + 1),
         str(f_values[index]),
         str(f_slopes[index]),
         str(g_values[index]),
         inner_slope_cells[index],
      ])

   columns = [
      math("x"),
      math(f"{outer_name}(x)"),
      math(f"{outer_name}'(x)"),
      math(f"{inner_name}(x)"),
      math(f"{inner_name}'(x)"),
   ]
   alt_rows = "; ".join(
      f"at x = {row[0]}, {outer_name} = {row[1]}, {outer_name}' = {row[2]}, {inner_name} = {row[3]}, {inner_name}' = {row[4]}"
      for row in rows
   )
   table = table_figure(columns, rows, alt=f"A table of values: {alt_rows}.")

   composite = f"h(x) = {outer_name}({inner_name}(x))"
   intro = (
      f"The table gives values of the differentiable functions {outer_name} and {inner_name} and their "
      f"derivatives at selected values of x. Let {math(composite)}."
   )

   lookup = Step(
      text=(
         f"By the chain rule, {math(f"h'(x) = {outer_name}'({inner_name}(x)) \\cdot {inner_name}'(x)")}. "
         f"From the table, {math(f'{inner_name}({at}) = {inner}')}, so the outer derivative is read in the row "
         f"x = {inner}: {math(f"{outer_name}'({inner}) = {tex(outer_slope)}")}."
      ),
      rule="chain rule",
   )

   if is_reversed:
      stem = (
         f"{intro} The entry for {math(f"{inner_name}'({at})")} is missing, but {math(f"h'({at}) = {tex(chain)}")}. "
         f"Find {math(f"{inner_name}'({at})")}."
      )
      key_value = inner_slope
      steps = [
         lookup,
         Step(
            text=(
               f"So {math(f"{tex(chain)} = h'({at}) = {_paren(outer_slope)} \\cdot {inner_name}'({at})")}, and "
               f"{math(f"{inner_name}'({at}) = {tex(key_value)}")}."
            ),
            value=key_value,
            rule="solve for the missing factor",
         ),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-03003",
            derivation=f"the outer derivative read in the row x = {at} instead of at the inner output {inner}",
            value=chain / wrong_row_slope,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-03004",
            derivation="the chain rule taken as the sum of the two derivatives, so the missing entry is h' minus the outer derivative",
            value=chain - outer_slope,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-03002",
            derivation="the outer layer left undifferentiated, so h' is taken as the outer value times the inner derivative",
            value=chain / outer_value,
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      stem = f"{intro} Find the exact value of {math(f"h'({at})")}."
      key_value = chain
      steps = [
         lookup,
         Step(
            text=(
               f"With {math(f"{inner_name}'({at}) = {tex(inner_slope)}")}, "
               f"{math(f"h'({at}) = {_paren(outer_slope)} \\cdot {_paren(inner_slope)} = {tex(key_value)}")}."
            ),
            value=key_value,
            rule="multiply the two derivatives",
         ),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-03003",
            derivation=f"the outer derivative read in the row x = {at} instead of at the inner output {inner}",
            value=wrong_row_slope * inner_slope,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-03004",
            derivation="the two derivatives added instead of multiplied",
            value=outer_slope + inner_slope,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-03002",
            derivation="the outer layer left undifferentiated: the outer value at the inner output times the inner derivative",
            value=outer_value * inner_slope,
            mechanism="conceptual_confusion",
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
