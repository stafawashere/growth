"""BC-QA-10019, a function represented by integrating a geometric series term by term, with the constant from f(0)."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_h import polynomial_tex, taylor_polynomial

ARCHETYPE_ID = "BC-QA-10019"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inner_power", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2]}},
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["minus", "plus"]}},
      {"name": "count", "type": "integer", "role": "difficulty", "domain": {"values": [4, 5]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start_value", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "inner_power", "difficulty_factor_id": "BC-DF-06", "settings": {"1": "low", "2": "medium"}},
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-06", "settings": {"minus": "low", "plus": "medium"}},
      {"parameter": "count", "difficulty_factor_id": "BC-DF-06", "settings": {"4": "low", "5": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["inner_power", "sign", "count", "scale", "coefficient", "start_value"]},
   ],
   "notes": "f'(x) = c / (1 - s k x^p) with s = 1 or -1, expanded as c times the sum of (s k)^n x^(pn); integrating gives the constant f(0) plus c (s k)^n x^(pn+1) / (pn+1). f(0) is never 0, so dropping the constant is a distinct error.",
}


def _coefficients(start_value, coefficient, ratio, inner_power, count, mode="correct"):
   """f's coefficients by power of x: the constant, then count - 1 integrated terms."""
   degree = inner_power * (count - 2) + 1
   values = [sympy.Integer(0)] * (degree + 1)
   values[0] = sympy.Integer(0) if mode == "no_constant" else sympy.Integer(start_value)

   for index in range(count - 1):
      power = inner_power * index + 1

      if mode == "unraised":
         factor = ratio if index > 0 else 1
      else:
         factor = ratio**index

      divisor = 1 if mode == "undivided" else power
      values[power] = sympy.Rational(coefficient * factor, divisor)

   return values


def build(names):
   inner_power = int(names["inner_power"])
   is_plus = names["sign"] == "plus"
   count = int(names["count"])
   scale = int(names["scale"])
   coefficient = int(names["coefficient"])
   start_value = int(names["start_value"])
   ratio = -scale if is_plus else scale

   variable = "x" if inner_power == 1 else f"x^{{{inner_power}}}"
   operator = "+" if is_plus else "-"
   derivative_tex = rf"\frac{{{coefficient}}}{{1 {operator} {scale}{variable}}}"
   stem = (
      f"The function f satisfies {math(f'f(0) = {start_value}')} and {math(r'f^{\prime}(x) = ' + derivative_tex)}. Use the "
      f"geometric series to find the first {count} nonzero terms of the Maclaurin series for f."
   )

   key_coefficients = _coefficients(start_value, coefficient, ratio, inner_power, count)
   value = taylor_polynomial(key_coefficients, 0)
   integrand_coefficients = [sympy.Integer(0)] * (inner_power * (count - 2) + 1)

   for index in range(count - 1):
      integrand_coefficients[inner_power * index] = sympy.Integer(coefficient * ratio**index)

   ratio_tex = f"{ratio}{variable}"
   steps = [
      Step(text=f"With common ratio {math(ratio_tex)}, the geometric series gives {math(r'f^{\prime}(x) = ' + polynomial_tex(integrand_coefficients, 0) + r' + \cdots')}.", point_type_id="BC-PT-99067", rule="geometric series"),
      Step(text=f"Integrate term by term, raising each power by 1 and dividing by the new power, and add the constant {math(f'f(0) = {start_value}')}.", point_type_id="BC-PT-99003", rule="term-by-term antiderivative"),
      Step(text=f"The first {count} nonzero terms are {math(polynomial_tex(key_coefficients, 0))}.", value=value, point_type_id="BC-PT-99004", rule="first nonzero terms"),
   ]
   distractors = [
      Distractor("BC-ERR-07026", f"the constant of integration dropped, so the value f(0) = {start_value} was never used", value=taylor_polynomial(_coefficients(start_value, coefficient, ratio, inner_power, count, "no_constant"), 0), mechanism="forgot_constant"),
      Distractor("BC-ERR-99018", "each power raised by 1 but the coefficient not divided by the new power", value=taylor_polynomial(_coefficients(start_value, coefficient, ratio, inner_power, count, "undivided"), 0), mechanism="algebra_slip"),
      Distractor("BC-ERR-10041", f"{ratio} not raised to the power of each term when substituted into the geometric series", value=taylor_polynomial(_coefficients(start_value, coefficient, ratio, inner_power, count, "unraised"), 0), mechanism="algebra_slip"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
   )
