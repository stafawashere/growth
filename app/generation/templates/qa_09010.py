"""BC-QA-09010, the rate at which a particle's distance from the origin changes on a polar curve, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-09010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 7, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "frequency", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {
         "name": "angle",
         "type": "real",
         "role": "safe",
         "domain": {"values": [0.3, 0.4, 0.6, 0.7, 0.9, 1.1, 1.3, 1.4, 1.8, 1.9]},
      },
      {"name": "angle_rate", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "3/2", "2", "5/2", "3"]}},
      {"name": "rate_form", "type": "label", "role": "difficulty", "domain": {"values": ["constant", "angle_function"]}},
   ],
   "constraints": [
      "constant > amplitude",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "rate_form", "difficulty_factor_id": "BC-DF-04", "settings": {"constant": "off", "angle_function": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-13",
         "figure_kind": None,
         "requires": ["constant", "amplitude", "frequency", "trig", "angle", "angle_rate"],
      },
   ],
   "notes": "The radius stays positive (constant above amplitude), the angle rate is never 1 so dr/dtheta alone differs from dr/dt, and the angle is a decimal in radians kept away from pi/2, where sin(theta) is so close to 1 that the key could round to a whole number; a full enumeration of the domain finds no degenerate key.",
}

theta = sympy.Symbol("theta")
t = sympy.Symbol("t")
DEGREE = sympy.pi / 180


def build(names):
   constant = names["constant"]
   amplitude = names["amplitude"]
   frequency = names["frequency"]
   angle = sympy.nsimplify(names["angle"])
   angle_rate = names["angle_rate"]
   trig_function = sympy.sin if names["trig"] == "sin" else sympy.cos
   is_angle_function = names["rate_form"] == "angle_function"

   radius = constant + amplitude * trig_function(frequency * theta)
   radius_rate = sympy.diff(radius, theta)
   radius_rate_value = sympy.N(radius_rate.subs(theta, angle), 30)
   key_value = radius_rate_value * angle_rate

   degree_radius = constant + amplitude * trig_function(frequency * theta * DEGREE)
   degree_value = sympy.N(sympy.diff(degree_radius, theta).subs(theta, angle), 30) * angle_rate
   radius_value = sympy.N(radius.subs(theta, angle), 30)
   radius_times_rate = radius_value * angle_rate

   curve_tex = "r = " + tex(radius)
   angle_text = f"{float(angle):g}"
   rate_tex = tex(angle_rate)

   if is_angle_function:
      motion = (
         f"A particle moves along the polar curve {math(curve_tex)} so that its angle at time t is "
         f"{math(r'\theta(t) = ' + tex(angle_rate * t))}."
      )
      rate_step = (
         f"Since {math(r'\theta(t) = ' + tex(angle_rate * t))}, {math(r'\frac{d\theta}{dt} = ' + rate_tex)}. "
      )
   else:
      motion = (
         f"A particle moves along the polar curve {math(curve_tex)} so that its angle changes at the constant rate "
         f"{math(r'\frac{d\theta}{dt} = ' + rate_tex)}."
      )
      rate_step = ""

   stem = (
      f"{motion} Using a calculator, find the rate at which the particle's distance from the origin is changing with "
      f"respect to time at the instant when {math(r'\theta = ' + angle_text)}. Show the setup for the calculation, "
      "and give the value correct to three decimal places."
   )

   chain_tex = r"\frac{dr}{dt} = \frac{dr}{d\theta}\cdot\frac{d\theta}{dt}"
   steps = [
      Step(
         text=(
            f"The distance from the origin is r, and by the chain rule {math(chain_tex)}, with "
            f"{math(r'\frac{dr}{d\theta} = ' + tex(radius_rate))}."
         ),
         point_type_id="BC-PT-99049",
         rule="chain rule",
      ),
      Step(
         text=(
            f"At {math(r'\theta = ' + angle_text)}, a calculator in radian mode gives "
            f"{math(r'\frac{dr}{d\theta} \approx ' + decimal_text(radius_rate_value))}."
         ),
         value=radius_rate_value,
         point_type_id="BC-PT-99005",
         rule="evaluation at the stated angle",
      ),
      Step(
         text=(
            f"{rate_step}So {math(r'\frac{dr}{dt} \approx ' + decimal_text(radius_rate_value) + r' \cdot ' + rate_tex)}, "
            f"which is about {decimal_text(key_value)}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="multiply by the rate of the angle",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09030",
         derivation="the rate of the angle left out of the chain rule product, so dr/dtheta alone is reported",
         value=radius_rate_value,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-09023",
         derivation="dr/dtheta evaluated with the calculator in degree mode and then multiplied by the rate of the angle",
         value=degree_value,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="the chain rule product formed with r in place of dr/dtheta, so r times dtheta/dt is reported",
         value=radius_times_rate,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-13",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
