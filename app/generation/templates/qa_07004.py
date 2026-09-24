"""BC-QA-07004, Euler's method with two steps of equal size from a given initial point."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["x_only", "both"]}},
      {"name": "x_coefficient", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "y_coefficient", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "start_x", "type": "integer", "role": "safe", "domain": {"min": -1, "max": 2, "step": 1}},
      {"name": "start_y", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "span", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "2"]}},
   ],
   "constraints": [
      "key_value != 0",
      "distinct([key_value, one_step, full_steps, target_slope_first])",
   ],
   "derived": [
      {"name": "used_y", "expression": "0 if form == 'x_only' else y_coefficient"},
      {"name": "step", "expression": "span / 2"},
      {"name": "slope_start", "expression": "x_coefficient * start_x + used_y * start_y + constant"},
      {"name": "middle_y", "expression": "start_y + step * slope_start"},
      {"name": "slope_middle", "expression": "x_coefficient * (start_x + step) + used_y * middle_y + constant"},
      {"name": "key_value", "expression": "middle_y + step * slope_middle"},
      {"name": "one_step", "expression": "start_y + span * slope_start"},
      {"name": "full_steps", "expression": "one_step + span * (x_coefficient * (start_x + span) + used_y * one_step + constant)"},
      {"name": "target_middle", "expression": "start_y + step * (x_coefficient * (start_x + span) + used_y * start_y + constant)"},
      {"name": "target_slope_first", "expression": "target_middle + step * (x_coefficient * (start_x + step) + used_y * target_middle + constant)"},
   ],
   "invariants": [
      "exact(key)",
      "key == key_value",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-01", "settings": {"x_only": "off", "both": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["form", "x_coefficient", "y_coefficient", "constant", "start_x", "start_y", "span"]},
   ],
   "notes": "dy/dx = a x + b y + c, with b = 0 on the x-only form. Two equal steps of size span/2 run from x0 to x0 + span. The key and the three error values (one full step, two steps of the full size, the first slope taken at the target input) are derived here and required to differ, and the key is never 0.",
}

x = sympy.Symbol("x")
y = sympy.Symbol("y")


def _signed(value):
   text = tex(value)

   return f"+ {text}" if value >= 0 else f"- {tex(-value)}"


def build(names):
   x_coefficient = int(names["x_coefficient"])
   used_y = int(names["used_y"])
   constant = int(names["constant"])
   start_x = int(names["start_x"])
   start_y = int(names["start_y"])
   span = sympy.Rational(names["span"])
   step = sympy.Rational(names["step"])
   middle_x = start_x + step
   target_x = start_x + span

   right_side = x_coefficient * x + used_y * y + constant
   slope_start = sympy.Rational(names["slope_start"])
   middle_y = sympy.Rational(names["middle_y"])
   slope_middle = sympy.Rational(names["slope_middle"])
   key_value = sympy.Rational(names["key_value"])

   stem = (
      f"Let {math('y = f(x)')} be the solution to the differential equation {math(rf'\frac{{dy}}{{dx}} = {tex(right_side)}')} "
      f"with {math(f'f({start_x}) = {start_y}')}. Use Euler's method, starting at {math(f'x = {start_x}')} with two steps "
      f"of equal size, to approximate {math(f'f({tex(target_x)})')}. Show the computations that lead to your answer."
   )

   steps = [
      Step(
         text=(
            f"Two equal steps from {math(f'x = {start_x}')} to {math(f'x = {tex(target_x)}')} have size "
            f"{math(r'\Delta x = ' + tex(step))}. The slope at {math(f'({start_x}, {start_y})')} is {math(tex(slope_start))}, so "
            f"{math(f'f({tex(middle_x)}) \\approx {start_y} {_signed(step * slope_start)} = {tex(middle_y)}')}."
         ),
         point_type_id="BC-PT-99034",
         rule="first Euler step",
      ),
      Step(
         text=(
            f"The slope at {math(f'({tex(middle_x)}, {tex(middle_y)})')} is {math(tex(slope_middle))}, so "
            f"{math(f'f({tex(target_x)}) \\approx {tex(middle_y)} {_signed(step * slope_middle)} = {tex(key_value)}')}."
         ),
         value=key_value,
         point_type_id="BC-PT-99005",
         rule="second Euler step from the first step's result",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07019",
         derivation=f"a single step of size {tex(span)}, the whole interval, using only the slope at the starting point",
         value=sympy.Rational(names["one_step"]),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99026",
         derivation=f"two steps taken with step size {tex(span)} instead of {tex(step)}, so the method overshoots the target",
         value=sympy.Rational(names["full_steps"]),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-07020",
         derivation=f"the first slope evaluated at the target input x = {tex(target_x)} instead of at the starting point",
         value=sympy.Rational(names["target_slope_first"]),
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
      command_verb="approximate",
   )
