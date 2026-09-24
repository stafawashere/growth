"""BC-QA-09006, the speed of a particle in the plane at a time, or the first time it reaches a given speed, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_roots
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-09006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "frequency", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1"]}},
      {"name": "growth", "type": "rational", "role": "safe", "domain": {"values": ["3/2", "2", "5/2", "3", "4"]}},
      {"name": "time", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "3/4", "5/4", "3/2"]}},
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 8, "step": 1}},
      {"name": "units", "type": "label", "role": "safe", "domain": {"values": ["meters", "feet"]}},
      {"name": "request", "type": "label", "role": "difficulty", "domain": {"values": ["value", "time"]}},
   ],
   "constraints": [
      "request == 'value' or target >= amplitude + 2",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "request", "difficulty_factor_id": "BC-DF-08", "settings": {"value": "off", "time": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-14", "figure_kind": None, "requires": ["amplitude", "frequency", "growth", "time", "target", "request"]},
   ],
   "notes": "The velocity is <amplitude cos(frequency t), growth t^2>. The speed starts at the amplitude, below every target, and the t^2 term makes it, and every distractor's version of it, pass any target speed by t = 6, so each first time exists on the search window. For the time request the target exceeds the cosine amplitude by at least 2, so the t^2 component matters where the target is reached; with growth at least 3/2 that happens before t = 2.4, while frequency t stays below pi, so the squared cosine in degree mode (near 1) differs from the squared cosine in radian mode. The coefficient growth is never 1, so squaring growth t^2 without parentheses changes the speed.",
}

t = sympy.Symbol("t")
SEARCH_END = 6
DEGREE = sympy.pi / 180


def _first_root(expression, target):
   roots = numeric_roots(expression - target, t, sympy.Rational(1, 1000), SEARCH_END, pieces=797)

   return roots[0] if roots else None


def build(names):
   amplitude = names["amplitude"]
   frequency = names["frequency"]
   growth = names["growth"]
   units = names["units"]
   is_time = names["request"] == "time"

   x_rate = amplitude * sympy.cos(frequency * t)
   y_rate = growth * t**2
   speed = sympy.sqrt(x_rate**2 + y_rate**2)
   summed = x_rate + y_rate
   lost_parentheses = sympy.sqrt(x_rate**2 + growth * t**4)
   degree_speed = sympy.sqrt((amplitude * sympy.cos(frequency * t * DEGREE)) ** 2 + y_rate**2)

   velocity = rf"\left\langle {tex_f(x_rate)}, {tex_f(y_rate)} \right\rangle"
   opening = (
      f"A particle moves in the xy-plane with velocity vector {math('v(t) = ' + velocity)} for {math(r't \ge 0')}, "
      f"with t in seconds and distances in {units}."
   )
   speed_tex = rf"\sqrt{{\left({tex_f(x_rate)}\right)^{{2}} + \left({tex_f(y_rate)}\right)^{{2}}}}"

   if is_time:
      target = names["target"]
      key_value = _first_root(speed, target)
      stem = (
         f"{opening} Using a calculator, find the first time {math('t > 0')} at which the speed of the particle is "
         f"{target} {units} per second. Show the setup for the calculation, and give the value correct to three decimal places."
      )
      steps = [
         Step(text=f"The speed is {math('|v(t)| = ' + speed_tex)}.", point_type_id="BC-PT-99050", rule="speed as the magnitude of velocity"),
         Step(
            text=f"Set {math(speed_tex + f' = {target}')} and solve with a calculator, in radian mode; the smallest positive solution is {math('t = ' + decimal_text(key_value))}.",
            value=key_value,
            point_type_id="BC-PT-99004",
            rule="numerical solve",
         ),
      ]
      distractors = [
         Distractor("BC-ERR-09013", "the two components added instead of combined as a magnitude, x'(t) + y'(t) set equal to the target", _first_root(summed, target), mechanism="conceptual_confusion"),
         Distractor("BC-ERR-09014", f"(y'(t))^2 written as {tex_f(growth)} t^4, the coefficient left unsquared", _first_root(lost_parentheses, target), mechanism="algebra_slip"),
         Distractor("BC-ERR-09023", "the equation solved with the calculator in degree mode", _first_root(degree_speed, target), mechanism="algebra_slip"),
      ]
      key_units = "seconds"
   else:
      time = names["time"]
      key_value = speed.subs(t, time).evalf(30)
      stem = (
         f"{opening} Using a calculator, find the speed of the particle at {math(f't = {tex_f(time)}')}. Show the setup "
         "for the calculation, and give the value correct to three decimal places."
      )
      steps = [
         Step(text=f"The speed is {math('|v(t)| = ' + speed_tex)}.", point_type_id="BC-PT-99050", rule="speed as the magnitude of velocity"),
         Step(
            text=f"At {math(f't = {tex_f(time)}')}, with the calculator in radian mode, the speed is about {decimal_text(key_value)} {units} per second.",
            value=key_value,
            point_type_id="BC-PT-99004",
            rule="evaluate at the time",
         ),
      ]
      distractors = [
         Distractor("BC-ERR-09013", "the two components added instead of combined as a magnitude", summed.subs(t, time).evalf(30), mechanism="conceptual_confusion"),
         Distractor("BC-ERR-09014", f"(y'(t))^2 written as {tex_f(growth)} t^4, the coefficient left unsquared", lost_parentheses.subs(t, time).evalf(30), mechanism="algebra_slip"),
         Distractor("BC-ERR-09023", "the cosine evaluated with the calculator in degree mode", degree_speed.subs(t, time).evalf(30), mechanism="algebra_slip"),
      ]
      key_units = f"{units} per second"

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3, units=key_units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-14",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
