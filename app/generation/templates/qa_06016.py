"""BC-QA-06016, an antidifferentiation technique chosen from the structure of the integrand and applied."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06016"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "structure", "type": "label", "role": "difficulty", "domain": {"values": ["product", "improper_rational"]}},
      {"name": "multiplier", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "rate_sign", "type": "integer", "role": "safe", "domain": {"values": [-1, 1]}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
   ],
   "constraints": [],
   "derived": [
      {"name": "exponent_rate", "expression": "rate * rate_sign"},
      {"name": "remainder", "expression": "shift**2 + constant"},
   ],
   "invariants": [
      "exact(key)",
      "remainder > 0",
   ],
   "dial_bindings": [
      {"parameter": "structure", "difficulty_factor_id": "BC-DF-15", "settings": {"product": "low", "improper_rational": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["structure", "multiplier", "rate", "shift", "constant"]},
   ],
   "notes": "The product form m x e^(kx) has no inner derivative present and selects integration by parts; the rational form m (x^2 + c) / (x + a) has numerator degree above the denominator's and selects long division first. The remainder a^2 + c is never zero.",
}

x = sympy.Symbol("x")


def _product_instance(multiplier, exponent_rate):
   exponential = sympy.exp(exponent_rate * x)
   integrand = multiplier * x * exponential
   key_value = sympy.expand(multiplier * x * exponential / exponent_rate - multiplier * exponential / exponent_rate**2)
   parts_line = sympy.expand(multiplier * x * exponential / exponent_rate)
   differential = r"dx" if multiplier == 1 else rf"{multiplier}\,dx"
   remaining = multiplier * exponential / abs(exponent_rate)
   remaining_sign = " - " if exponent_rate > 0 else " + "
   stem = f"Find the indefinite integral {math(r'\int ' + tex(integrand) + r'\,dx')}."
   steps = [
      Step(
         text=(
            f"The integrand is a product of x and an exponential, and the derivative of the exponent, {math(tex(exponent_rate))}, "
            "does not account for the factor x, so substitution does not apply and the product calls for integration by parts."
         ),
         rule="technique selected by structure",
      ),
      Step(
         text=(
            f"Take {math('u = ' + tex(multiplier * x))} and {math(r'dv = ' + tex(exponential) + r'\,dx')}, so "
            f"{math(r'du = ' + differential)} and {math('v = ' + tex(exponential / exponent_rate))}. "
            f"Then the integral is {math(tex(parts_line) + remaining_sign + r'\int ' + tex(remaining) + r'\,dx')}."
         ),
         rule="integration by parts",
      ),
      Step(
         text=f"Antidifferentiate the remaining exponential: the integral is {math(tex(key_value) + ' + C')}.",
         value=key_value,
         rule="antiderivative of an exponential",
      ),
   ]
   distractors = [
      Distractor(
         error_path="BC-ERR-06022",
         derivation="x and the exponential antidifferentiated separately and the results multiplied",
         value=multiplier * x**2 / 2 * exponential / exponent_rate,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-06020",
         derivation=f"u = {exponent_rate}x substituted with the factor x treated as though it were part of du, so it disappears",
         value=multiplier * exponential / exponent_rate,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06020",
         derivation=f"u = {exponent_rate}x substituted with the factor x held fixed as a constant, although du does not contain it",
         value=multiplier * x * exponential / exponent_rate,
         mechanism="conceptual_confusion",
      ),
   ]

   return stem, steps, key_value, distractors


def _rational_instance(multiplier, shift, constant, remainder):
   denominator = x + shift
   numerator = multiplier * (x**2 + constant)
   integrand = numerator / denominator
   quotient = sympy.expand(multiplier * (x - shift))
   divided = quotient + multiplier * remainder / denominator
   logarithm = sympy.log(sympy.Abs(denominator))
   key_value = multiplier * x**2 / 2 - multiplier * shift * x + multiplier * remainder * logarithm
   stem = f"Find the indefinite integral {math(r'\int ' + tex(integrand) + r'\,dx')}."
   steps = [
      Step(
         text=(
            "The numerator has degree 2 and the denominator degree 1, so the rational function is improper and must be "
            "divided before any logarithm appears."
         ),
         rule="technique selected by structure",
      ),
      Step(
         text=f"Long division gives {math(tex(integrand) + ' = ' + tex(divided))}.",
         value=divided,
         rule="polynomial long division",
      ),
      Step(
         text=f"Antidifferentiate term by term: the integral is {math(tex(key_value) + ' + C')}.",
         value=key_value,
         rule="antiderivatives of a polynomial and of 1 over a linear factor",
      ),
   ]
   distractors = [
      Distractor(
         error_path="BC-ERR-06026",
         derivation=f"the improper fraction split directly, keeping only the constant {multiplier * remainder} over {tex(denominator)} and losing the polynomial part",
         value=multiplier * remainder * logarithm,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06022",
         derivation="the numerator and 1 over the denominator antidifferentiated separately and the results multiplied",
         value=multiplier * (x**3 / 3 + constant * x) * logarithm,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-06020",
         derivation="u taken as the denominator and the whole numerator treated as though it were du, so it is carried in front of the logarithm",
         value=numerator * logarithm,
         mechanism="conceptual_confusion",
      ),
   ]

   return stem, steps, key_value, distractors


def build(names):
   multiplier = int(names["multiplier"])

   if names["structure"] == "product":
      stem, steps, key_value, distractors = _product_instance(multiplier, int(names["exponent_rate"]))
   else:
      stem, steps, key_value, distractors = _rational_instance(
         multiplier, int(names["shift"]), int(names["constant"]), int(names["remainder"]),
      )

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
