"""BC-QA-99005, the velocity vector of a particle travelling a polar curve, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-99005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "angle_rate", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "3/4", "3/2", "2"]}},
      {"name": "instant", "type": "real", "role": "safe", "domain": {"values": [0.5, 0.8, 1.2, 1.5, 1.8, 2.5]}},
      {"name": "angle_form", "type": "label", "role": "difficulty", "domain": {"values": ["linear", "quadratic"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "finite(horizontal_velocity)",
      "finite(vertical_velocity)",
      "abs(horizontal_velocity - vertical_velocity) > 0.001",
   ],
   "dial_bindings": [
      {"parameter": "angle_form", "difficulty_factor_id": "BC-DF-08", "settings": {"linear": "off", "quadratic": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-14",
         "figure_kind": None,
         "requires": ["constant", "amplitude", "trig", "angle_rate", "instant", "angle_form"],
      },
   ],
   "notes": "The angle is angle_rate times t or angle_rate times t squared, so the velocity needs the chain rule through the angle as well as the product rule in each component.",
}

t = sympy.Symbol("t")
theta = sympy.Symbol("theta")
DEGREE = sympy.pi / 180


def _vector_label(horizontal, vertical, instant_text):
   return math(rf"v({instant_text}) \approx \left\langle {decimal_text(horizontal)},\ {decimal_text(vertical)} \right\rangle")


def build(names):
   constant = names["constant"]
   amplitude = names["amplitude"]
   angle_rate = names["angle_rate"]
   instant = sympy.nsimplify(names["instant"])
   trig_function = sympy.sin if names["trig"] == "sin" else sympy.cos
   is_quadratic = names["angle_form"] == "quadratic"

   radius = constant + amplitude * trig_function(theta)
   angle_of_time = angle_rate * t**2 if is_quadratic else angle_rate * t
   radius_of_time = radius.subs(theta, angle_of_time)
   horizontal = radius_of_time * sympy.cos(angle_of_time)
   vertical = radius_of_time * sympy.sin(angle_of_time)

   horizontal_velocity = sympy.N(sympy.diff(horizontal, t).subs(t, instant), 30)
   vertical_velocity = sympy.N(sympy.diff(vertical, t).subs(t, instant), 30)

   degree_horizontal = horizontal.replace(sympy.cos, lambda arg: sympy.cos(arg * DEGREE)).replace(sympy.sin, lambda arg: sympy.sin(arg * DEGREE))
   degree_vertical = vertical.replace(sympy.cos, lambda arg: sympy.cos(arg * DEGREE)).replace(sympy.sin, lambda arg: sympy.sin(arg * DEGREE))
   degree_pair = (
      sympy.N(sympy.diff(degree_horizontal, t).subs(t, instant), 30),
      sympy.N(sympy.diff(degree_vertical, t).subs(t, instant), 30),
   )
   polar_pair = (
      sympy.N(sympy.diff(radius_of_time, t).subs(t, instant), 30),
      sympy.N(sympy.diff(angle_of_time, t).subs(t, instant), 30),
   )

   instant_text = f"{float(instant):g}"
   stem = (
      f"A particle moves along the polar curve {math('r = ' + tex(radius))} so that at time t its angle is "
      f"{math(r'\theta(t) = ' + tex(angle_of_time))}. Using a calculator, find the velocity vector of the particle at "
      f"time {math('t = ' + instant_text)}. Show the setup, and give each component correct to three decimal places."
   )

   position_tex = rf"\left\langle {tex(horizontal)},\ {tex(vertical)} \right\rangle"
   steps = [
      Step(
         text=(
            f"With {math(r'x = r\cos\theta')} and {math(r'y = r\sin\theta')}, the position vector in terms of time is "
            f"{math(r'\left\langle x(t), y(t) \right\rangle = ' + position_tex)}."
         ),
         point_type_id="BC-PT-99005",
         rule="polar to rectangular conversion",
      ),
      Step(
         text=(
            f"Differentiate each component and evaluate at {math('t = ' + instant_text)} with the calculator in radian mode: "
            f"{math(rf"x'({instant_text}) \approx " + decimal_text(horizontal_velocity))} and "
            f"{math(rf"y'({instant_text}) \approx " + decimal_text(vertical_velocity))}."
         ),
         point_type_id="BC-PT-99004",
         rule="componentwise derivative",
      ),
      Step(
         text=f"So the velocity vector is {_vector_label(horizontal_velocity, vertical_velocity, instant_text)}.",
         point_type_id="BC-PT-99064",
         rule="labelled components",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09017",
         derivation="the two components written in the wrong order, the y-component first",
         label=_vector_label(vertical_velocity, horizontal_velocity, instant_text),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-09027",
         derivation="the polar pair taken as the position, so the velocity is reported as dr/dt and dtheta/dt",
         label=_vector_label(polar_pair[0], polar_pair[1], instant_text),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-09023",
         derivation="both component derivatives evaluated with the calculator in degree mode",
         label=_vector_label(degree_pair[0], degree_pair[1], instant_text),
         mechanism="algebra_slip",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_vector_label(horizontal_velocity, vertical_velocity, instant_text)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-14",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
      notes={"horizontal_velocity": horizontal_velocity, "vertical_velocity": vertical_velocity},
   )
