"""BC-QA-04007, related rates for a particle on an implicitly defined curve."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-04007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "square_x", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 2, "step": 1}},
      {"name": "mixed", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "square_y", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "point_x", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "point_y", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "rate_x", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0, 1]}},
   ],
   "constraints": [
      "x_part != 0",
      "y_part != 0",
      "distinct([key_rate, frozen_rate, slope_only, 0])",
   ],
   "derived": [
      {"name": "x_part", "expression": "2 * square_x * point_x + mixed * point_y"},
      {"name": "y_part", "expression": "mixed * point_x + 2 * square_y * point_y"},
      {"name": "key_rate", "expression": "-x_part * rate_x / y_part"},
      {"name": "frozen_rate", "expression": "-x_part * rate_x / (2 * square_y * point_y)"},
      {"name": "slope_only", "expression": "-x_part / y_part"},
   ],
   "invariants": [
      "exact(key)",
      "key == key_rate",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["square_x", "mixed", "square_y", "point_x", "point_y", "rate_x"]},
   ],
   "notes": "The curve a x^2 + b x y + c y^2 = K passes through the integer point by construction; the mixed term b x y is never absent, so the product rule is always needed.",
}

x, y = sympy.symbols("x y")


def _signed_sum(terms):
   """Terms written as coefficient times body, joined with the signs a student would write."""
   pieces = []

   for coefficient, body in terms:
      if coefficient == 0:
         continue

      size = abs(coefficient)
      shown = f"{size}{body}" if size != 1 or not body else body
      is_first = not pieces

      if is_first:
         pieces.append(f"-{shown}" if coefficient < 0 else shown)
      else:
         pieces.append(f"{'-' if coefficient < 0 else '+'} {shown}")

   return " ".join(pieces) if pieces else "0"


def build(names):
   square_x = int(names["square_x"])
   mixed = int(names["mixed"])
   square_y = int(names["square_y"])
   point_x = int(names["point_x"])
   point_y = int(names["point_y"])
   rate_x = int(names["rate_x"])
   left_side = square_x * x**2 + mixed * x * y + square_y * y**2
   level = left_side.subs({x: point_x, y: point_y})
   x_part = 2 * square_x * point_x + mixed * point_y
   y_part = mixed * point_x + 2 * square_y * point_y
   key_value = sympy.Rational(-x_part * rate_x, y_part)

   curve_tex = f"{tex(left_side)} = {level}"
   rate_tex = rf"\frac{{dx}}{{dt}} = {rate_x}"
   stem = (
      f"A particle moves along the curve {math(curve_tex)}. At the instant when the particle is at the point "
      f"{math(f'({point_x}, {point_y})')}, its x-coordinate is changing at the rate {math(rate_tex)}. Find "
      f"{math(r'\frac{dy}{dt}')} at that instant."
   )

   dx = r"\frac{dx}{dt}"
   dy = r"\frac{dy}{dt}"
   differentiated = _signed_sum([
      (2 * square_x, rf"x{dx}"),
      (mixed, rf"\left({dx}\,y + x{dy}\right)"),
      (2 * square_y, rf"y{dy}"),
   ]) + " = 0"
   substituted = _signed_sum([
      (2 * square_x * point_x * rate_x, ""),
      (mixed * rate_x * point_y, ""),
      (mixed * point_x, dy),
      (2 * square_y * point_y, dy),
   ]) + " = 0"
   isolated = _signed_sum([(x_part * rate_x, ""), (y_part, dy)]) + " = 0"

   steps = [
      Step(
         text=(
            f"Differentiate both sides with respect to t, using the product rule on the mixed term: "
            f"{math(differentiated)}."
         ),
         rule="implicit differentiation with respect to time",
      ),
      Step(
         text=f"Substitute x = {point_x}, y = {point_y} and {math(rate_tex)}: {math(substituted)}, that is, {math(isolated)}.",
         rule="substitute after differentiating",
      ),
      Step(
         text=f"Solve for the requested rate: {math(r'\frac{dy}{dt} = ' + tex(key_value))}.",
         value=key_value,
         rule="isolate the requested rate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-04018",
         derivation=f"the mixed term {tex(mixed * x * y)} differentiated as though y were constant, giving only {tex(mixed * y)} dx/dt",
         value=sympy.Rational(-x_part * rate_x, 2 * square_y * point_y),
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-04017",
         derivation="the curve differentiated with respect to x, and dy/dx at the point reported with no factor dx/dt",
         value=sympy.Rational(-x_part, y_part),
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-04020",
         derivation=f"x replaced by {point_x} before differentiating, so the x terms become constants and the equation forces dy/dt = 0",
         value=sympy.Integer(0),
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
