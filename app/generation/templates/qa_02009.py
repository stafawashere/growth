"""BC-QA-02009, the derivative of a product or quotient at a point from tabulated values."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-02009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "f_values", "type": "integer", "role": "safe", "count": 3, "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "f_slopes", "type": "integer", "role": "safe", "count": 3, "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "g_values", "type": "integer", "role": "safe", "count": 3, "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "g_slopes", "type": "integer", "role": "safe", "count": 3, "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "row", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 2, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": -1, "max": 2, "step": 1}},
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["product", "quotient"]}},
   ],
   "constraints": [
      "distinct(options)",
      "options[0] != 0",
   ],
   "derived": [
      {"name": "f_at", "expression": "f_values[row]"},
      {"name": "fp_at", "expression": "f_slopes[row]"},
      {"name": "g_at", "expression": "g_values[row]"},
      {"name": "gp_at", "expression": "g_slopes[row]"},
      {
         "name": "options",
         "expression": (
            "[fp_at * g_at + f_at * gp_at, fp_at * gp_at, f_at * g_at + f_at * gp_at, fp_at * g_at + f_at * g_at] "
            "if form == 'product' else "
            "[(fp_at * g_at - f_at * gp_at) / g_at**2, (f_at * gp_at - fp_at * g_at) / g_at**2, "
            "(fp_at * g_at - f_at * gp_at) / g_at, (f_at * g_at - f_at * gp_at) / g_at**2]"
         ),
      },
   ],
   "invariants": [
      "exact(key)",
      "key == options[0]",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-03", "settings": {"product": "off", "quotient": "off"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["f_values", "f_slopes", "g_values", "g_slopes", "row", "start"]},
   ],
   "notes": (
      "Three consecutive inputs are tabulated with the values and derivatives of f and g, all nonzero. The "
      "archetype's dials have no setting for product against quotient, so that parameter is bound to BC-DF-03 "
      "at off in both states and the dial is moved by nothing here."
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
   row = int(names["row"])
   inputs = [int(names["start"]) + index for index in range(3)]
   at = inputs[row]
   is_product = names["form"] == "product"

   f_at = sympy.Integer(f_values[row])
   fp_at = sympy.Integer(f_slopes[row])
   g_at = sympy.Integer(g_values[row])
   gp_at = sympy.Integer(g_slopes[row])

   rows = [[str(inputs[index]), str(f_values[index]), str(f_slopes[index]), str(g_values[index]), str(g_slopes[index])] for index in range(3)]
   columns = [math("x"), math("f(x)"), math("f'(x)"), math("g(x)"), math("g'(x)")]
   alt_rows = "; ".join(f"at x = {cells[0]}, f = {cells[1]}, f' = {cells[2]}, g = {cells[3]}, g' = {cells[4]}" for cells in rows)
   table = table_figure(columns, rows, alt=f"A table of values: {alt_rows}.")

   if is_product:
      definition = "h(x) = f(x)\\,g(x)"
      key_value = fp_at * g_at + f_at * gp_at
      rule_text = "h'(x) = f'(x)\\,g(x) + f(x)\\,g'(x)"
      substituted = f"{_paren(fp_at)} \\cdot {_paren(g_at)} + {_paren(f_at)} \\cdot {_paren(gp_at)}"
      rule_step = Step(
         text=f"By the product rule, {math(rule_text)}.",
         point_type_id="BC-PT-99022",
         rule="product rule",
      )
      distractors = [
         Distractor(
            error_path="BC-ERR-02020",
            derivation=f"the product of the two derivatives, f'({at}) g'({at})",
            value=fp_at * gp_at,
            mechanism="product_rule_omitted",
         ),
         Distractor(
            error_path="BC-ERR-02024",
            derivation=f"the value f({at}) read where f'({at}) belongs in the rule",
            value=f_at * g_at + f_at * gp_at,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-02024",
            derivation=f"the value g({at}) read where g'({at}) belongs in the rule",
            value=fp_at * g_at + f_at * g_at,
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      definition = r"h(x) = \frac{f(x)}{g(x)}"
      key_value = (fp_at * g_at - f_at * gp_at) / g_at**2
      rule_text = r"h'(x) = \frac{f'(x)\,g(x) - f(x)\,g'(x)}{\left(g(x)\right)^{2}}"
      substituted = rf"\frac{{{_paren(fp_at)} \cdot {_paren(g_at)} - {_paren(f_at)} \cdot {_paren(gp_at)}}}{{{_paren(g_at)}^{{2}}}}"
      rule_step = Step(
         text=f"By the quotient rule, {math(rule_text)}.",
         rule="quotient rule",
      )
      distractors = [
         Distractor(
            error_path="BC-ERR-02021",
            derivation="the two terms of the numerator taken in the reverse order",
            value=(f_at * gp_at - fp_at * g_at) / g_at**2,
            mechanism="reversed_quantities",
         ),
         Distractor(
            error_path="BC-ERR-02022",
            derivation=f"the numerator divided by g({at}) instead of by its square",
            value=(fp_at * g_at - f_at * gp_at) / g_at,
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-02024",
            derivation=f"the value f({at}) read where f'({at}) belongs in the rule",
            value=(f_at * g_at - f_at * gp_at) / g_at**2,
            mechanism="conceptual_confusion",
         ),
      ]

   stem = (
      "The table gives values of the differentiable functions f and g and their derivatives at selected values "
      f"of x. Let {math(definition)}. Find the exact value of {math(f"h'({at})")}."
   )

   steps = [
      Step(
         text=(
            f"From the row x = {at}: {math(f'f({at}) = {tex(f_at)}')}, {math(f"f'({at}) = {tex(fp_at)}")}, "
            f"{math(f'g({at}) = {tex(g_at)}')} and {math(f"g'({at}) = {tex(gp_at)}")}."
         ),
         rule="read the table",
      ),
      rule_step,
      Step(
         text=f"So {math(f"h'({at}) = {substituted} = {tex(key_value)}")}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="substitute and evaluate",
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
