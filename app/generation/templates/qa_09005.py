"""BC-QA-09005, a coordinate of a particle at one time recovered from its position at another, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-09005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "x_amplitude", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "x_spread", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "y_rate", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "x_start", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "y_start", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "known_time", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "requested", "type": "label", "role": "safe", "domain": {"values": ["x", "y"]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["later", "earlier"]}},
      {"name": "given_as", "type": "label", "role": "difficulty", "domain": {"values": ["coordinates", "point"]}},
   ],
   "constraints": [
      "x_start != y_start",
      "x_start != 0",
      "y_start != 0",
      "direction == 'later' or known_time > offset",
   ],
   "derived": [
      {"name": "target_time", "expression": "known_time + offset if direction == 'later' else known_time - offset"},
   ],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-06", "settings": {"later": "off", "earlier": "low"}},
      {"parameter": "given_as", "difficulty_factor_id": "BC-DF-14", "settings": {"coordinates": "off", "point": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-14", "figure_kind": None, "requires": ["x_amplitude", "x_spread", "y_rate", "x_start", "y_start", "known_time", "offset", "requested", "direction", "given_as"]},
   ],
   "notes": "dx/dt = x_amplitude cos(t^2 / x_spread) and dy/dt = y_rate sqrt(t) e^(-t/2) have no elementary antiderivatives, so the change comes from the calculator. The two starting coordinates differ and are nonzero, so using the other coordinate's value, or none, gives a distinct option. When the requested time is earlier the integral runs backwards.",
}

t = sympy.Symbol("t")


def build(names):
   known_time = names["known_time"]
   target_time = names["target_time"]
   is_earlier = names["direction"] == "earlier"
   is_point = names["given_as"] == "point"
   wants_x = names["requested"] == "x"

   x_velocity = names["x_amplitude"] * sympy.cos(t**2 / names["x_spread"])
   y_velocity = names["y_rate"] * sympy.sqrt(t) * sympy.exp(-t / 2)
   x_start = names["x_start"]
   y_start = names["y_start"]

   if wants_x:
      component, start, other_start, letter = x_velocity, x_start, y_start, "x"
   else:
      component, start, other_start, letter = y_velocity, y_start, x_start, "y"

   change = numeric_integral(component, t, known_time, target_time)
   position = start + change

   velocity = rf"\left\langle {tex_f(x_velocity)}, {tex_f(y_velocity)} \right\rangle"

   if is_point:
      known = f"At time {math(f't = {known_time}')} the particle is at the point {math(f'({x_start}, {y_start})')}."
   else:
      known = f"At time {math(f't = {known_time}')}, {math(f'x({known_time}) = {x_start}')} and {math(f'y({known_time}) = {y_start}')}."

   stem = (
      f"A particle moves in the xy-plane with velocity vector {math('v(t) = ' + velocity)} for {math(r't \ge 0')}. "
      f"{known} Using a calculator, find the {letter}-coordinate of the particle's position at time "
      f"{math(f't = {target_time}')}. Show the setup for the calculations, and give the value correct to three decimal places."
   )

   rate_tex = tex_f(component)
   setup = rf"{letter}({target_time}) = {letter}({known_time}) + \int_{{{known_time}}}^{{{target_time}}} \left({rate_tex}\right)\,dt"
   steps = [
      Step(
         text=f"The {letter}-coordinate is the known value plus the accumulated change: {math(setup)}.",
         point_type_id="BC-PT-99033",
         rule="position from an initial condition",
      ),
      Step(
         text=(
            f"With a calculator the integral is about {decimal_text(change)}"
            + (" (the integral runs from the later time back to the earlier one)." if is_earlier else ".")
         ),
         value=change,
         point_type_id="BC-PT-99001",
         rule="numerical integration",
      ),
      Step(
         text=f"So {math(f'{letter}({target_time}) \\approx {start} + ({decimal_text(change)}) = {decimal_text(position)}')}.",
         value=position,
         point_type_id="BC-PT-99004",
         rule="add the initial value",
      ),
   ]

   distractors = [
      Distractor("BC-ERR-08011", "the integral reported alone, without the known coordinate", change, mechanism="forgot_constant"),
      Distractor("BC-ERR-09021", "the change subtracted from the known coordinate, accumulating in the wrong direction in time", start - change, mechanism="sign_error"),
      Distractor("BC-ERR-09019", f"the other coordinate's known value, {other_start}, used as the starting value", other_start + change, mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=position, decimals=3),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-14",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
