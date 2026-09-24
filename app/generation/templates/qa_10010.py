"""BC-QA-10010, a Taylor polynomial built by differentiating a relation that defines f prime."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_h import polynomial_tex, taylor_polynomial

ARCHETYPE_ID = "BC-QA-10010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "degree", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"values": [-1, 0, 1]}},
      {"name": "alpha", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1, "exclude": [0]}},
      {"name": "beta", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "start_value", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
   ],
   "constraints": [
      "first != 0",
      "second != 0",
      "third != 0",
      "fourth != 0",
      "first != second",
      "second != third",
      "alpha * centre * first != 2 * second",
      "alpha * centre * first != second",
   ],
   "derived": [
      {"name": "first", "expression": "alpha * centre * start_value + beta"},
      {"name": "second", "expression": "alpha * start_value + alpha * centre * first"},
      {"name": "third", "expression": "2 * alpha * first + alpha * centre * second"},
      {"name": "fourth", "expression": "3 * alpha * second + alpha * centre * third"},
   ],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "degree", "difficulty_factor_id": "BC-DF-01", "settings": {"2": "low", "3": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["degree", "centre", "alpha", "beta", "start_value"]},
   ],
   "notes": "f'(x) = alpha x f(x) + beta, so f'' = alpha f + alpha x f' and f''' = 2 alpha f' + alpha x f''; every derivative through the fourth is nonzero at the centre, so the polynomial keeps every term and the extra-term distractor is real.",
}


def _linear_text(terms):
   """A sum of coefficient-times-symbol terms written with its signs, zero terms left out."""
   pieces = []

   for coefficient, symbol in terms:
      if coefficient == 0:
         continue

      magnitude = abs(coefficient)
      shown = symbol if magnitude == 1 and symbol else f"{magnitude} {symbol}".strip()
      is_negative = coefficient < 0

      if not pieces:
         pieces.append(f"-{shown}" if is_negative else shown)
      else:
         pieces.append(f"- {shown}" if is_negative else f"+ {shown}")

   return " ".join(pieces)


def build(names):
   degree = int(names["degree"])
   centre = names["centre"]
   alpha = names["alpha"]
   beta = names["beta"]
   start_value = names["start_value"]
   derivatives = [start_value, names["first"], names["second"], names["third"], names["fourth"]]

   coefficients = [derivatives[order] / sympy.factorial(order) for order in range(degree + 1)]
   value = taylor_polynomial(coefficients, centre)

   relation = _linear_text([(alpha, "x f(x)"), (beta, "")])
   stem = (
      f"Let f be the function with {math(f'f({centre}) = {start_value}')} whose derivative satisfies "
      f"{math(f'f^{{\\prime}}(x) = {relation}')}. Find the Taylor polynomial of degree {degree} for f about {math(f'x = {centre}')}."
   )

   steps = [
      Step(text=f"Substituting {math(f'x = {centre}')} and {math(f'f({centre}) = {start_value}')} into the relation gives {math(rf'f^{{\prime}}({centre}) = {derivatives[1]}')}.", value=sympy.Integer(derivatives[1]), point_type_id="BC-PT-99027", rule="evaluate the relation"),
      Step(text=f"By the product rule, {math(r'f^{\prime\prime}(x) = ' + _linear_text([(alpha, 'f(x)'), (alpha, r'x f^{\prime}(x)')]))}, so {math(rf'f^{{\prime\prime}}({centre}) = {derivatives[2]}')}.", value=sympy.Integer(derivatives[2]), point_type_id="BC-PT-99022", rule="product rule"),
   ]

   if degree == 3:
      steps.append(Step(text=f"Differentiating again, {math(r'f^{\prime\prime\prime}(x) = ' + _linear_text([(2 * alpha, r'f^{\prime}(x)'), (alpha, r'x f^{\prime\prime}(x)')]))}, so {math(rf'f^{{\prime\prime\prime}}({centre}) = {derivatives[3]}')}.", value=sympy.Integer(derivatives[3]), point_type_id="BC-PT-99027", rule="product rule"))

   steps.append(Step(
      text=f"Dividing each value by the matching factorial, the polynomial is {math(polynomial_tex(coefficients, centre))}.",
      value=value,
      point_type_id="BC-PT-99035",
      rule="Taylor polynomial",
   ))

   # Differentiating alpha x f(x) as alpha x f'(x) alone drops the alpha f(x) term at every order.
   no_product = [start_value, derivatives[1], alpha * centre * derivatives[1]]
   no_product.append(alpha * centre * no_product[2])
   no_product_coefficients = [no_product[order] / sympy.factorial(order) for order in range(degree + 1)]
   raw_coefficients = [sympy.Integer(derivatives[order]) for order in range(degree + 1)]
   extra_coefficients = coefficients + [derivatives[degree + 1] / sympy.factorial(degree + 1)]

   distractors = [
      Distractor("BC-ERR-10028", "the product rule skipped on alpha x f(x), so each new derivative kept only the alpha x times the previous derivative", value=taylor_polynomial(no_product_coefficients, centre), mechanism="product_rule_omitted"),
      Distractor("BC-ERR-10029", "each derivative value placed as the coefficient with no factorial in the denominator", value=taylor_polynomial(raw_coefficients, centre), mechanism="algebra_slip"),
      Distractor("BC-ERR-10030", f"the polynomial carried one degree past {degree}", value=taylor_polynomial(extra_coefficients, centre), mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
