"""BC-QA-02002, the derivative of a polynomial at a point computed from the limit of the difference quotient."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "leading", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "point", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "degree", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3]}},
   ],
   "constraints": [
      "degree * leading * point**(degree - 1) + linear != 0",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "degree", "difficulty_factor_id": "BC-DF-02", "settings": {"2": "low", "3": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["leading", "linear", "constant", "point", "degree"]},
   ],
   "notes": "f(x) = leading x^degree + linear x + constant. Expanding (point + h)^degree as point^degree + h^degree, the characteristic slip, leaves a quotient whose limit is the linear coefficient, which differs from the key because point is not 0.",
}

x = sympy.Symbol("x")
h = sympy.Symbol("h")


def build(names):
   leading = names["leading"]
   linear = names["linear"]
   constant = names["constant"]
   point = names["point"]
   degree = int(names["degree"])

   function = leading * x**degree + linear * x + constant
   derivative = sympy.diff(function, x)
   key_value = derivative.subs(x, point)
   shifted = sympy.expand(function.subs(x, point + h))
   base = function.subs(x, point)
   difference = sympy.expand(shifted - base)
   quotient = sympy.expand(difference / h)
   slipped_difference = sympy.expand(leading * (point**degree + h**degree) + linear * (point + h) + constant - base)

   quotient_tex = rf"\lim_{{h \to 0}} \frac{{f({point} + h) - f({point})}}{{h}}"
   stem = (
      f"Let {math('f(x) = ' + tex(function))}. Use the limit definition of the derivative to find the exact value "
      f"of the derivative of f at {math(f'x = {point}')}."
   )

   steps = [
      Step(
         text=f"Write the difference quotient: {math(quotient_tex)}, with {math(f'f({point} + h) = ' + tex(shifted))} and {math(f'f({point}) = {base}')}.",
         rule="difference quotient",
      ),
      Step(
         text=f"The numerator is {math(tex(difference))}, and every term has a factor of h, so for h not 0 the quotient is {math(tex(quotient))}.",
         value=quotient,
         rule="divide out the increment",
      ),
      Step(
         text=f"Taking the limit as h approaches 0 gives {math(tex(key_value))}.",
         value=key_value,
         rule="limit by substitution",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-02007",
         derivation=f"({point} + h)^{degree} expanded as {point}^{degree} + h^{degree}, so the numerator becomes {tex(slipped_difference)} and the quotient tends to {linear}",
         value=sympy.Integer(linear),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02005",
         derivation="h set to 0 in the numerator before dividing, so the numerator is 0 and the answer is reported as 0",
         value=sympy.Integer(0),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02030",
         derivation="the derivative function reported where its value at the point was asked for",
         value=derivative,
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
