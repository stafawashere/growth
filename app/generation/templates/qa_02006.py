"""BC-QA-02006, a sum of powers, a radical or a reciprocal, and a constant differentiated term by term."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "leading", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "degree", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "second", "type": "label", "role": "difficulty", "domain": {"values": ["radical", "reciprocal"]}},
      {"name": "second_coefficient", "type": "integer", "role": "safe", "domain": {"min": -8, "max": 8, "step": 1, "exclude": [0]}},
      {"name": "root_index", "type": "integer", "role": "safe", "domain": {"values": [2, 3]}},
      {"name": "reciprocal_power", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "second", "difficulty_factor_id": "BC-DF-12", "settings": {"radical": "off", "reciprocal": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["leading", "degree", "second", "second_coefficient", "constant"]},
   ],
   "notes": (
      "f(x) = leading x^degree + second_coefficient R(x) + constant, where R is a square or cube root of x or "
      "a reciprocal power of x. The reciprocal form produces a negative exponent and so a sign to carry."
   ),
}

x = sympy.Symbol("x")


def _scaled_power(coefficient, exponent):
   power = rf"x^{{{tex(exponent)}}}"

   if coefficient == 1:
      return power

   if coefficient == -1:
      return f"-{power}"

   return f"{coefficient} {power}"


def build(names):
   leading = int(names["leading"])
   degree = int(names["degree"])
   second_coefficient = int(names["second_coefficient"])
   constant = int(names["constant"])
   is_radical = names["second"] == "radical"

   if is_radical:
      exponent = sympy.Rational(1, int(names["root_index"]))
      shape = "radical"
   else:
      exponent = -sympy.Integer(int(names["reciprocal_power"]))
      shape = "reciprocal"

   power_term = leading * x**degree
   second_term = second_coefficient * x**exponent
   function = power_term + second_term + constant

   power_slope = leading * degree * x ** (degree - 1)
   second_slope = second_coefficient * exponent * x ** (exponent - 1)
   key_value = power_slope + second_slope

   rewritten = f"{_scaled_power(leading, degree)} + {_scaled_power(second_coefficient, exponent)} + {constant}"
   rewritten = rewritten.replace("+ -", "- ")
   stem = f"Let {math('f(x) = ' + tex(function))} for {math('x > 0')}. Find {math("f'(x)")}."

   steps = [
      Step(
         text=f"Write every term as a power of x: {math('f(x) = ' + rewritten)}.",
         rule=f"rewrite the {shape} as a power",
      ),
      Step(
         text=(
            f"By the power rule, {math(tex(power_term))} has derivative {math(tex(power_slope))}, "
            f"{math(tex(second_term))} has derivative {math(tex(second_slope))}, and the constant has derivative 0."
         ),
         rule="power rule, term by term",
      ),
      Step(
         text=f"So {math("f'(x) = " + tex(key_value))}.",
         value=key_value,
         rule="sum rule",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-02015",
         derivation="each exponent lowered by 1 without multiplying by the old exponent",
         value=leading * x ** (degree - 1) + second_coefficient * x ** (exponent - 1),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02016",
         derivation=f"the constant {constant} carried into the derivative unchanged",
         value=key_value + constant,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02017",
         derivation=f"the {shape} term copied into the derivative undifferentiated",
         value=power_slope + second_term,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
