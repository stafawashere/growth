"""BC-QA-09004, the acceleration vector of a particle in the plane at a time, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-09004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "growth", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1/3", "1/4"]}},
      {"name": "log_scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "time", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "3/2", "2", "5/2"]}},
      {"name": "position_axis", "type": "label", "role": "safe", "domain": {"values": ["x", "y"]}},
      {"name": "notation", "type": "label", "role": "difficulty", "domain": {"values": ["components", "vector"]}},
   ],
   "constraints": [
      "2 * log_scale * time / (1 + time**2) + linear != 2 * log_scale * (1 - time**2) / (1 + time**2)**2",
   ],
   "derived": [],
   "invariants": [
      "key != ''",
   ],
   "dial_bindings": [
      {"parameter": "notation", "difficulty_factor_id": "BC-DF-04", "settings": {"components": "off", "vector": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-14", "figure_kind": None, "requires": ["amplitude", "growth", "log_scale", "linear", "time", "position_axis", "notation"]},
   ],
   "notes": "One component is given as a velocity, amplitude e^(growth t) sin t, and the other as a position, log_scale ln(1 + t^2) + linear t, so the acceleration needs one derivative of the first and two of the second. Which axis carries the position is a surface choice. The position component's velocity and acceleration are kept unequal, so differentiating it once gives a vector apart from the key.",
}

t = sympy.Symbol("t")


def _pair(first, second, is_vector, time_tex):
   if is_vector:
      return math(rf"\left\langle {decimal_text(first)}, {decimal_text(second)} \right\rangle")

   first_text = math(rf"x''({time_tex}) \approx {decimal_text(first)}")
   second_text = math(rf"y''({time_tex}) \approx {decimal_text(second)}")

   return f"{first_text} and {second_text}"


def build(names):
   time = names["time"]
   is_vector = names["notation"] == "vector"
   position_on_x = names["position_axis"] == "x"

   velocity_part = names["amplitude"] * sympy.exp(names["growth"] * t) * sympy.sin(t)
   position_part = names["log_scale"] * sympy.log(1 + t**2) + names["linear"] * t

   velocity_accel = sympy.diff(velocity_part, t).subs(t, time).evalf(30)
   position_velocity = sympy.diff(position_part, t).subs(t, time).evalf(30)
   position_accel = sympy.diff(position_part, t, 2).subs(t, time).evalf(30)
   velocity_value = velocity_part.subs(t, time).evalf(30)

   if position_on_x:
      given = (
         f"{math('x(t) = ' + tex_f(position_part))} and {math(r"y'(t) = " + tex_f(velocity_part))}"
      )
      acceleration = (position_accel, velocity_accel)
      velocity = (position_velocity, velocity_value)
      once_each = (position_velocity, velocity_accel)
   else:
      given = (
         f"{math(r"x'(t) = " + tex_f(velocity_part))} and {math('y(t) = ' + tex_f(position_part))}"
      )
      acceleration = (velocity_accel, position_accel)
      velocity = (velocity_value, position_velocity)
      once_each = (velocity_accel, position_velocity)

   time_tex = tex_f(time)
   first_request = math(rf"x''({time_tex})")
   second_request = math(rf"y''({time_tex})")
   request = "the acceleration vector" if is_vector else f"{first_request} and {second_request}, the components of the acceleration"
   stem = (
      f"A particle moves in the xy-plane so that {given} for {math(r't \ge 0')}. Using a calculator, find {request} "
      f"of the particle at {math(f't = {time_tex}')}. Show the setup for the calculations, and give each value correct "
      "to three decimal places."
   )

   steps = [
      Step(
         text=(
            f"The component given as a velocity is differentiated once, {math(tex_f(sympy.diff(velocity_part, t)))} at "
            f"{math(f't = {time_tex}')} gives about {decimal_text(velocity_accel)}."
         ),
         point_type_id="BC-PT-99005",
         rule="derivative of a velocity component",
      ),
      Step(
         text=(
            f"The component given as a position is differentiated twice, {math(tex_f(sympy.factor(sympy.simplify(sympy.diff(position_part, t, 2)))))} "
            f"at {math(f't = {time_tex}')} gives about {decimal_text(position_accel)}."
         ),
         point_type_id="BC-PT-99052",
         rule="second derivative of a position component",
      ),
      Step(
         text=f"The acceleration at {math(f't = {time_tex}')} is {_pair(acceleration[0], acceleration[1], is_vector, time_tex)}.",
         point_type_id="BC-PT-99064",
         rule="acceleration vector",
      ),
   ]

   distractors = [
      Distractor(
         "BC-ERR-09017",
         "the two components written in the wrong order",
         label=_pair(acceleration[1], acceleration[0], is_vector, time_tex),
         mechanism="reversed_quantities",
      ),
      Distractor(
         "BC-ERR-99029",
         "the velocity vector at the time reported as the acceleration",
         label=_pair(velocity[0], velocity[1], is_vector, time_tex),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         "BC-ERR-99029",
         "each given component differentiated once, so the position component yields its velocity, not its acceleration",
         label=_pair(once_each[0], once_each[1], is_vector, time_tex),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_pair(acceleration[0], acceleration[1], is_vector, time_tex)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-14",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
