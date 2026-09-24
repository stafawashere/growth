"""BC-QA-01003, a limit of a quotient built on a composite, found from given limits rather than from tabulated values."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure, tex

ARCHETYPE_ID = "BC-QA-01003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "point", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "limit_f", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "limit_g", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "table_f", "type": "integer", "role": "safe", "count": 6, "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "table_g", "type": "integer", "role": "safe", "count": 6, "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "justify", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "named"]}},
   ],
   "constraints": [
      "0 <= point**2 + shift and point**2 + shift <= 5",
      "point**2 + shift != point",
      "table_f[point] != limit_f",
      "table_g[point] != limit_g",
      "limit_f**2 + shift != 0",
      "distinct([key_value, both_values, denominator_value, wrong_order])",
   ],
   "derived": [
      {"name": "key_value", "expression": "(limit_f**2 + shift) / limit_g"},
      {"name": "both_values", "expression": "(table_f[point]**2 + shift) / table_g[point]"},
      {"name": "denominator_value", "expression": "(limit_f**2 + shift) / table_g[point]"},
      {"name": "wrong_order", "expression": "table_f[max(0, min(5, point**2 + shift))] / limit_g"},
   ],
   "invariants": [
      "exact(key)",
      "key == key_value",
   ],
   "dial_bindings": [
      {"parameter": "justify", "difficulty_factor_id": "BC-DF-10", "settings": {"bare": "off", "named": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["point", "shift", "limit_f", "limit_g", "table_f", "table_g"]},
   ],
   "notes": "h(x) = x^2 + shift. f and g are tabulated at x = 0 to 5 and both jump at point, where their limits (given in the stem) differ from their tabulated values. The limit of h(f(x)) / g(x) at point is h(limit_f) / limit_g because h is continuous and limit_g is not 0; h(point) is a tabulated input so the reversed composition f(h(point)) can be read from the table.",
}

x = sympy.Symbol("x")


def build(names):
   point = int(names["point"])
   shift = int(names["shift"])
   limit_f = int(names["limit_f"])
   limit_g = int(names["limit_g"])
   table_f = [int(value) for value in names["table_f"]]
   table_g = [int(value) for value in names["table_g"]]
   is_named = names["justify"] == "named"

   outer = x**2 + shift
   inner_limit_image = limit_f**2 + shift
   key_value = sympy.Rational(inner_limit_image, limit_g)
   inputs = list(range(6))

   table = table_figure(
      ["x", "f(x)", "g(x)"],
      [[value, table_f[value], table_g[value]] for value in inputs],
      alt="A table of x, f(x) and g(x): " + "; ".join(f"f({value}) = {table_f[value]}, g({value}) = {table_g[value]}" for value in inputs) + ".",
   )

   limit_tex = rf"\lim_{{x \to {point}}} \frac{{h(f(x))}}{{g(x)}}"
   given_f = rf"\lim_{{x \to {point}}} f(x) = {limit_f}"
   given_g = rf"\lim_{{x \to {point}}} g(x) = {limit_g}"
   request = " Name the limit theorems you use." if is_named else ""
   stem = (
      f"Let {math('h(x) = ' + tex(outer))}. The functions f and g satisfy {math(given_f)} and {math(given_g)}, "
      f"and selected values of f and g are given in the table. Find {math(limit_tex)}.{request}"
   )

   raw_quotient = rf"\frac{{{inner_limit_image}}}{{{limit_g}}}"
   is_reduced = sympy.gcd(inner_limit_image, limit_g) == 1 and limit_g > 0
   quotient_tex = tex(key_value) if is_reduced else f"{raw_quotient} = {tex(key_value)}"
   steps = [
      Step(
         text=f"Because h is a polynomial, it is continuous, so {math(rf'\lim_{{x \to {point}}} h(f(x)) = h({limit_f}) = {inner_limit_image}')}.",
         rule="limit of a composite with a continuous outer function",
      ),
      Step(
         text=f"The limit of the denominator is {limit_g}, which is not 0, so the quotient theorem applies.",
         rule="quotient limit theorem, denominator condition",
      ),
      Step(
         text=f"{math(limit_tex + ' = ' + quotient_tex)}. The tabulated values at x = {point} are not used, because f and g are not continuous there.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="quotient limit theorem",
      ),
   ]

   reversed_input = point**2 + shift
   distractors = [
      Distractor(
         error_path="BC-ERR-01001",
         derivation=f"the tabulated values f({point}) and g({point}) used in place of the limits",
         value=sympy.Rational(table_f[point] ** 2 + shift, table_g[point]),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01001",
         derivation=f"the tabulated value g({point}) used in place of the limit of the denominator",
         value=sympy.Rational(inner_limit_image, table_g[point]),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01007",
         derivation=f"the composition taken in the wrong order, f applied to the limit of h(x), so f({reversed_input}) read from the table",
         value=sympy.Rational(table_f[reversed_input], limit_g),
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
