"""BC-QA-03009, choosing the rules for a power of x times an exponential of a polynomial, then evaluating."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-03009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "inner_degree", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2]}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
   ],
   "constraints": [
      "exponent_at != 0",
      "key_factor != 0",
      "distinct([key_factor, inner_rate * at**power, power * at**(power - 1) + at**power])",
   ],
   "derived": [
      {"name": "exponent_at", "expression": "rate * at**inner_degree + offset"},
      {"name": "inner_rate", "expression": "inner_degree * rate * at**(inner_degree - 1)"},
      {"name": "key_factor", "expression": "power * at**(power - 1) + at**power * inner_rate"},
   ],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "inner_degree", "difficulty_factor_id": "BC-DF-06", "settings": {"1": "off", "2": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["scale", "power", "rate", "offset", "inner_degree", "at"]},
   ],
   "notes": (
      "h(x) = scale x^power e^(rate x^d + offset). The outermost operation is a product, one factor of which is a "
      "composite, so the product rule opens and the chain rule follows; the exponential with a polynomial "
      "exponent looks like a power, which invites the power rule. The constraints keep the four options apart."
   ),
}

x = sympy.Symbol("x")


def build(names):
   scale = int(names["scale"])
   power = int(names["power"])
   rate = int(names["rate"])
   offset = int(names["offset"])
   inner_degree = int(names["inner_degree"])
   at = int(names["at"])

   exponent = rate * x**inner_degree + offset
   function = scale * x**power * sympy.exp(exponent)
   exponent_at = rate * at**inner_degree + offset
   inner_rate = inner_degree * rate * at ** (inner_degree - 1)
   growth = sympy.exp(exponent_at)

   front = scale * power * sympy.Integer(at) ** (power - 1)
   back = scale * sympy.Integer(at) ** power
   key_value = (front + back * inner_rate) * growth

   stem = f"Let {math('h(x) = ' + tex(function))}. Find the exact value of {math(f"h'({at})")}."

   derivative = sympy.diff(scale * x**power, x) * sympy.exp(exponent) + scale * x**power * sympy.diff(exponent, x) * sympy.exp(exponent)
   steps = [
      Step(
         text=(
            f"The outermost operation is a product of {math(tex(scale * x**power))} and {math(tex(sympy.exp(exponent)))}, "
            "so the product rule comes first; the second factor is a composite, so its derivative needs the chain "
            f"rule with inner function {math(tex(exponent))}."
         ),
         rule="classify the outermost operation",
      ),
      Step(
         text=f"So {math("h'(x) = " + tex(derivative))}.",
         rule="product rule, then chain rule",
      ),
      Step(
         text=(
            f"At x = {at} the exponent is {exponent_at} and its derivative is {inner_rate}, so "
            f"{math(f"h'({at}) = {tex(key_value)}")}."
         ),
         value=key_value,
         rule="evaluate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03006",
         derivation=f"the factor {tex(scale * x**power)} held constant, so the product rule is never applied",
         value=back * inner_rate * growth,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03002",
         derivation="the inner layer of the exponential left undifferentiated, so its derivative is taken as the exponential itself",
         value=(front + back) * growth,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-99036",
         derivation="the exponential read by its shape as a power and differentiated by the power rule, u e^(u - 1)",
         value=front * growth + back * exponent_at * sympy.exp(exponent_at - 1),
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
