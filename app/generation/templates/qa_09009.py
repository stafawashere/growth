"""BC-QA-09009, the derivative of r with respect to theta on a polar curve at a stated angle, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-09009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "frequency", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "2", "3"]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["cos", "sin"]}},
      {
         "name": "angle",
         "type": "real",
         "role": "safe",
         "domain": {"values": [0.4, 0.5, 0.7, 0.8, 1.1, 1.2, 1.3, 1.7, 1.9, 2.3]},
      },
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "distance"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "finite(slope)",
   ],
   "dial_bindings": [
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-05", "settings": {"bare": "off", "distance": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-13",
         "figure_kind": None,
         "requires": ["constant", "coefficient", "frequency", "trig", "angle"],
      },
   ],
   "notes": "The radius is a constant plus a multiple of theta times a sine or cosine, so the derivative needs the product rule; the angle is a decimal in radians so the value is found on a calculator.",
}

theta = sympy.Symbol("theta")
DEGREE = sympy.pi / 180


def build(names):
   constant = names["constant"]
   coefficient = names["coefficient"]
   frequency = names["frequency"]
   angle = sympy.nsimplify(names["angle"])
   trig_function = sympy.cos if names["trig"] == "cos" else sympy.sin
   is_distance = names["framing"] == "distance"

   radius = constant + coefficient * theta * trig_function(frequency * theta)
   radius_rate = sympy.diff(radius, theta)
   key_value = sympy.N(radius_rate.subs(theta, angle), 30)

   degree_radius = constant + coefficient * theta * trig_function(frequency * theta * DEGREE)
   degree_value = sympy.N(sympy.diff(degree_radius, theta).subs(theta, angle), 30)

   no_product_rule = coefficient * sympy.diff(trig_function(frequency * theta), theta)
   no_product_value = sympy.N(no_product_rule.subs(theta, angle), 30)

   radius_value = sympy.N(radius.subs(theta, angle), 30)
   horizontal_rate = key_value * sympy.cos(angle) - radius_value * sympy.sin(angle)
   vertical_rate = key_value * sympy.sin(angle) + radius_value * sympy.cos(angle)
   slope_value = sympy.N(vertical_rate / horizontal_rate, 30)

   curve_tex = "r = " + tex(radius)
   angle_tex = rf"\theta = {float(angle):g}"

   if is_distance:
      stem = (
         f"A particle moves along the polar curve {math(curve_tex)}. Using a calculator, find the rate at which the "
         f"particle's distance from the origin changes with respect to {math(r'\theta')} when {math(angle_tex)}. "
         "Show the setup for the calculation, and give the value correct to three decimal places."
      )
   else:
      stem = (
         f"A curve is given in polar coordinates by {math(curve_tex)}. Using a calculator, find the value of "
         f"{math(r'\frac{dr}{d\theta}')} at the point on the curve where {math(angle_tex)}. Show the setup for the "
         "calculation, and give the value correct to three decimal places."
      )

   opening = (
      f"The distance from the origin is r, so the rate asked for is {math(r'\frac{dr}{d\theta}')}. "
      if is_distance else ""
   )
   steps = [
      Step(
         text=(
            f"{opening}By the product rule, {math(r'\frac{dr}{d\theta} = ' + tex(radius_rate))}."
         ),
         point_type_id="BC-PT-99049",
         rule="product rule",
      ),
      Step(
         text=(
            f"With the calculator in radian mode, the derivative at {math(angle_tex)} is about {decimal_text(key_value)}."
         ),
         value=key_value,
         point_type_id="BC-PT-99005",
         rule="evaluation at the stated angle",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09023",
         derivation="the derivative evaluated with the calculator in degree mode, so the trigonometric factor reads its argument in degrees",
         value=degree_value,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-09031",
         derivation="dr/dtheta and the slope dy/dx of the curve confused, so the slope of the tangent line at the angle is reported",
         value=slope_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="the polar radius differentiated without the product rule, theta times the trigonometric factor differentiated as the product of the two derivatives",
         value=no_product_value,
         mechanism="product_rule_omitted",
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
      notes={"slope": slope_value},
   )
