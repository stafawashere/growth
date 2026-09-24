"""BC-QA-03008, the second derivative at a point of a solution to a differential equation in x and y."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-03008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "mixed", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "y_part", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "x_part", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "x_at", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "y_at", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "notation", "type": "label", "role": "safe", "domain": {"values": ["leibniz", "prime"]}},
   ],
   "constraints": [
      "slope != 0",
      "options[0] != 0",
      "distinct(options)",
   ],
   "derived": [
      {"name": "slope", "expression": "mixed * x_at * y_at + y_part * y_at + x_part * x_at"},
      {
         "name": "options",
         "expression": (
            "[mixed * y_at + (mixed * x_at + y_part) * slope + x_part, "
            "(mixed * x_at + y_part) * slope + x_part, mixed * y_at + x_part, slope]"
         ),
      },
   ],
   "invariants": [
      "exact(key)",
      "key == options[0]",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["mixed", "y_part", "x_part", "x_at", "y_at"]},
   ],
   "notes": (
      "dy/dx = mixed x y + y_part y + x_part x, so the second derivative needs the product rule on the mixed term, "
      "the chain rule on every y, and the value of dy/dx at the point."
   ),
}

x = sympy.Symbol("x")
y = sympy.Symbol("y")


def _paren(value):
   text = tex(value)

   return rf"\left({text}\right)" if value < 0 else text


def build(names):
   mixed = int(names["mixed"])
   y_part = int(names["y_part"])
   x_part = int(names["x_part"])
   x_at = int(names["x_at"])
   y_at = int(names["y_at"])
   uses_prime = names["notation"] == "prime"

   rate = mixed * x * y + y_part * y + x_part * x
   slope = sympy.Integer(mixed * x_at * y_at + y_part * y_at + x_part * x_at)
   slope_factor = mixed * x_at + y_part
   key_value = mixed * y_at + slope_factor * slope + x_part

   if uses_prime:
      first, second = "y'", "y''"
   else:
      first, second = r"\frac{dy}{dx}", r"\frac{d^{2}y}{dx^{2}}"

   stem = (
      f"Let {math('y = f(x)')} be the solution of the differential equation {math(first + ' = ' + tex(rate))} whose "
      f"graph passes through the point {math(f'({x_at}, {y_at})')}. Find the value of {math(second)} at this point."
   )

   general = rf"{second} = {tex(mixed * y)} + \left({tex(mixed * x + y_part)}\right){first} + {x_part}"
   general = general.replace("+ -", "- ")
   steps = [
      Step(
         text=(
            "Differentiate the equation with respect to x, using the product rule on the mixed term and the chain "
            f"rule on each y: {math(general)}."
         ),
         point_type_id="BC-PT-99022",
         rule="product rule and chain rule",
      ),
      Step(
         text=f"At {math(f'({x_at}, {y_at})')}, {math(f'{first} = {tex(slope)}')}.",
         value=slope,
         rule="first derivative at the point",
      ),
      Step(
         text=(
            f"So {math(f'{second} = {_paren(sympy.Integer(mixed * y_at))} + {_paren(sympy.Integer(slope_factor))} \\cdot {_paren(slope)} + {_paren(sympy.Integer(x_part))} = {tex(key_value)}')}."
         ),
         value=key_value,
         point_type_id="BC-PT-99027",
         rule="substitute the point and the first derivative",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03008",
         derivation=f"the mixed term differentiated as though x were constant, so its {tex(mixed * y)} part is lost",
         value=slope_factor * slope + x_part,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-05060",
         derivation="y treated as a constant when differentiating, so every dy/dx term is lost",
         value=sympy.Integer(mixed * y_at + x_part),
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03021",
         derivation="the first derivative at the point reported in place of the second",
         value=slope,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="find",
   )
