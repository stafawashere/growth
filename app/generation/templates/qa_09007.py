"""BC-QA-09007, total distance travelled by a particle moving in the plane, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-09007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "frequency", "type": "rational", "role": "safe", "domain": {"values": ["1", "3/2", "2"]}},
      {"name": "vertical_scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "turning_square", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "end_time", "type": "rational", "role": "safe", "domain": {"values": ["2", "5/2", "3"]}},
      {"name": "units", "type": "label", "role": "safe", "domain": {"values": ["meters", "feet", "centimeters"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "units"]}},
   ],
   "constraints": [
      "turning_square < end_time**2",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-16", "settings": {"bare": "off", "units": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-14",
         "figure_kind": None,
         "requires": ["amplitude", "frequency", "vertical_scale", "turning_square", "end_time"],
      },
   ],
   "notes": "The vertical component changes sign inside the interval (turning_square below end_time squared), so the path turns and the displacement is strictly shorter than the distance.",
}

t = sympy.Symbol("t")


def _sign_change_times(component, end_time):
   zeros = sympy.solveset(component, t, sympy.Interval.open(0, end_time))

   return sorted(zeros) if isinstance(zeros, sympy.FiniteSet) else []


def build(names):
   amplitude = names["amplitude"]
   frequency = names["frequency"]
   vertical_scale = names["vertical_scale"]
   turning_square = names["turning_square"]
   end_time = names["end_time"]
   is_units = names["framing"] == "units"
   units = names["units"]

   horizontal_velocity = amplitude * sympy.cos(frequency * t)
   vertical_velocity = vertical_scale * (t**2 - turning_square)
   speed_squared = horizontal_velocity**2 + vertical_velocity**2
   speed = sympy.sqrt(speed_squared)

   distance = numeric_integral(speed, t, 0, end_time)
   horizontal_change = numeric_integral(horizontal_velocity, t, 0, end_time)
   vertical_change = numeric_integral(vertical_velocity, t, 0, end_time)
   displacement = sympy.sqrt(horizontal_change**2 + vertical_change**2)

   horizontal_turns = _sign_change_times(horizontal_velocity, end_time)
   vertical_turns = _sign_change_times(vertical_velocity, end_time)
   horizontal_travel = numeric_integral(sympy.Abs(horizontal_velocity), t, 0, end_time, horizontal_turns)
   vertical_travel = numeric_integral(sympy.Abs(vertical_velocity), t, 0, end_time, vertical_turns)
   separate_components = horizontal_travel + vertical_travel
   missing_radical = numeric_integral(speed_squared, t, 0, end_time)

   velocity_tex = rf"\left\langle {tex(horizontal_velocity)},\ {tex(vertical_velocity)} \right\rangle"
   window = rf"0 \le t \le {tex(end_time)}"

   if is_units:
      opening = (
         f"A particle moves in the xy-plane so that its velocity vector at time t seconds is "
         f"{math('v(t) = ' + velocity_tex)}, with velocity measured in {units} per second."
      )
      request = (
         f"Using a calculator, find the total distance, in {units}, traveled by the particle over the time "
         f"interval {math(window)}."
      )
      key_units = units
   else:
      opening = (
         f"A particle moves in the xy-plane so that its velocity vector at time t is {math('v(t) = ' + velocity_tex)}."
      )
      request = (
         f"Using a calculator, find the total distance traveled by the particle over the time interval {math(window)}."
      )
      key_units = None

   stem = (
      f"{opening} {request} Show the setup for the calculation, and give the value correct to three decimal places."
   )

   speed_tex = rf"\sqrt{{\left({tex(horizontal_velocity)}\right)^2 + \left({tex(vertical_velocity)}\right)^2}}"
   integral_tex = rf"\int_{{0}}^{{{tex(end_time)}}} {speed_tex}\,dt"
   unit_phrase = f" {units}" if is_units else ""
   steps = [
      Step(
         text=f"The speed of the particle is the magnitude of its velocity, {math(r'\lVert v(t) \rVert = ' + speed_tex)}.",
         point_type_id="BC-PT-99051",
         rule="speed as the magnitude of velocity",
      ),
      Step(
         text=(
            f"The total distance is the integral of speed over the interval, {math(integral_tex)}, which a calculator "
            f"gives as about {decimal_text(distance)}{unit_phrase}."
         ),
         value=distance,
         point_type_id="BC-PT-99004",
         rule="total distance as the integral of speed",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-99010",
         derivation="the net change in position reported, the length of the displacement vector from the integrals of the two components",
         value=displacement,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99029",
         derivation="distance written as two separate one-dimensional distances added together, the integral of |x'(t)| plus the integral of |y'(t)|",
         value=separate_components,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-09024",
         derivation="the speed written without its square root, so the integrand is x'(t)^2 + y'(t)^2",
         value=missing_radical,
         mechanism="algebra_slip",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=distance, decimals=3, units=key_units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-14",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
