"""BC-QA-03004, dy/dx found by implicit differentiation and evaluated at a point on the curve."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-03004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "mixed", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "y_coefficient", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "right_slope", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "x_at", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "y_at", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "y_power", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3]}},
   ],
   "constraints": [
      "denominator != 0",
      "options[0] != 0",
      "right_side != 0",
      "distinct(options)",
   ],
   "derived": [
      {"name": "y_rate", "expression": "y_power * y_coefficient * y_at**(y_power - 1)"},
      {"name": "denominator", "expression": "mixed * x_at + y_rate"},
      {"name": "right_side", "expression": "x_at**2 + mixed * x_at * y_at + y_coefficient * y_at**y_power - right_slope * x_at"},
      {
         "name": "options",
         "expression": (
            "[(right_slope - 2 * x_at - mixed * y_at) / denominator, "
            "(right_slope - 2 * x_at - mixed * y_at - y_rate) / (mixed * x_at), "
            "(right_slope - 2 * x_at - mixed * y_at) / y_rate, "
            "(-2 * x_at - mixed * y_at) / denominator]"
         ),
      },
   ],
   "invariants": [
      "exact(key)",
      "key == options[0]",
   ],
   "dial_bindings": [
      {"parameter": "y_power", "difficulty_factor_id": "BC-DF-06", "settings": {"2": "off", "3": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["mixed", "y_coefficient", "right_slope", "x_at", "y_at", "y_power"]},
   ],
   "notes": (
      "The curve x^2 + mixed x y + y_coefficient y^n = right_slope x + c passes through (x_at, y_at), with c "
      "computed from that point and kept nonzero. The mixed term needs the product rule, the y term a dy/dx "
      "factor, and the right side has a nonzero derivative, so dropping it moves the answer."
   ),
}

x = sympy.Symbol("x")
y = sympy.Symbol("y")


def _multiplier(value):
   if value == 1:
      return ""

   if value == -1:
      return "-"

   return tex(value)


def build(names):
   mixed = int(names["mixed"])
   y_coefficient = int(names["y_coefficient"])
   right_slope = int(names["right_slope"])
   x_at = int(names["x_at"])
   y_at = int(names["y_at"])
   y_power = int(names["y_power"])

   right_constant = x_at**2 + mixed * x_at * y_at + y_coefficient * y_at**y_power - right_slope * x_at
   left = x**2 + mixed * x * y + y_coefficient * y**y_power
   right = right_slope * x + right_constant

   y_rate = y_power * y_coefficient * y_at ** (y_power - 1)
   denominator = mixed * x_at + y_rate
   key_value = sympy.Rational(right_slope - 2 * x_at - mixed * y_at, denominator)

   stem = (
      f"A curve is defined by {math(tex(left) + ' = ' + tex(right))}. The point {math(f'({x_at}, {y_at})')} lies on "
      f"the curve. Find the value of {math(r'\frac{dy}{dx}')} at this point."
   )

   y_term_rate = sympy.diff(y_coefficient * y**y_power, y)
   differentiated = (
      rf"2x + {_multiplier(mixed)}\left(y + x\frac{{dy}}{{dx}}\right) + {tex(y_term_rate)}\frac{{dy}}{{dx}} = {right_slope}"
   ).replace("+ - ", "- ").replace("+ -", "- ")
   collected = (
      rf"\frac{{dy}}{{dx}} = \frac{{{tex(right_slope - 2 * x - mixed * y)}}}{{{tex(mixed * x + y_term_rate)}}}"
   )

   top = right_slope - 2 * x_at - mixed * y_at

   if denominator < 0:
      top, shown_denominator = -top, -denominator
   else:
      shown_denominator = denominator

   is_reduced = sympy.gcd(top, shown_denominator) == 1 and shown_denominator != 1

   if is_reduced:
      substituted = tex(key_value)
   else:
      substituted = rf"\frac{{{top}}}{{{shown_denominator}}} = {tex(key_value)}"

   steps = [
      Step(
         text=(
            "Differentiate both sides with respect to x, using the product rule on the mixed term and a factor "
            f"{math(r'\frac{dy}{dx}')} on each term in y: {math(differentiated)}."
         ),
         rule="implicit differentiation",
      ),
      Step(
         text=f"Collect the terms with {math(r'\frac{dy}{dx}')} and divide: {math(collected)}.",
         rule="solve for dy/dx",
      ),
      Step(
         text=(
            f"At {math(f'({x_at}, {y_at})')}, "
            f"{math(rf'\frac{{dy}}{{dx}} = {substituted}')}."
         ),
         value=key_value,
         rule="substitute both coordinates",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03007",
         derivation=f"the term {tex(y_coefficient * y**y_power)} differentiated to {tex(y_term_rate)} with no dy/dx factor",
         value=sympy.Rational(right_slope - 2 * x_at - mixed * y_at - y_rate, mixed * x_at),
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03008",
         derivation=f"the mixed term {tex(mixed * x * y)} differentiated as though y were constant, giving {tex(mixed * y)}",
         value=sympy.Rational(right_slope - 2 * x_at - mixed * y_at, y_rate),
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03009",
         derivation=f"the right side dropped after differentiating, so its derivative {right_slope} is lost",
         value=sympy.Rational(-2 * x_at - mixed * y_at, denominator),
         mechanism="algebra_slip",
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
