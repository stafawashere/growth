"""BC-QA-99003, the slope of the tangent line to a polar curve at a stated angle, exact value without a calculator."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-99003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

ANGLE_NAMES = ["1/6", "1/3", "2/3", "5/6", "7/6", "4/3", "5/3", "11/6"]

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 12, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 7, "step": 1}},
      {"name": "sign", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "angle_turns", "type": "rational", "role": "safe", "domain": {"values": ANGLE_NAMES}},
   ],
   "constraints": [
      "not (trig == 'cos' and amplitude == 2 * constant)",
      "not (trig == 'cos' and amplitude == 1 and 6 * angle_turns in [1, 5, 7, 11] and (sign == 1 or constant == 1))",
      "not (trig == 'cos' and sign == -1 and 6 * angle_turns in [1, 5, 7, 11] and (constant == 2 * amplitude or (constant == 7 and amplitude == 2)))",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "horizontal_rate != 0",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {
         "representation": "BC-REP-13",
         "figure_kind": None,
         "requires": ["constant", "amplitude", "sign", "trig", "angle_turns"],
      },
   ],
   "notes": "The curve is r = constant + sign amplitude trig(2 theta), so the radius itself needs the chain rule; the angle is a multiple of pi/6 that is not a multiple of pi/4, so dr/dtheta is never 0 there. The constraints remove, from a full enumeration of the domain, every draw where the tangent is vertical or two options coincide: all are cosine curves (amplitude twice the constant; amplitude 1 at odd multiples of pi/6 with sign 1, where dr/dtheta equals -cot(theta), or with r = 1 - cos(2 theta), where the product-rule and chain-rule distractors coincide; and sign -1 at odd multiples of pi/6 with constant twice the amplitude or r = 7 - 2 cos(2 theta), where dx/dtheta is 0).",
}

theta = sympy.Symbol("theta")


def _slope(radius, radius_rate, angle):
   vertical_rate = radius_rate * sympy.sin(theta) + radius * sympy.cos(theta)
   horizontal_rate = radius_rate * sympy.cos(theta) - radius * sympy.sin(theta)
   vertical_value = sympy.nsimplify(sympy.simplify(vertical_rate.subs(theta, angle)))
   horizontal_value = sympy.nsimplify(sympy.simplify(horizontal_rate.subs(theta, angle)))

   return vertical_value, horizontal_value


def build(names):
   constant = names["constant"]
   amplitude = names["amplitude"]
   sign = names["sign"]
   trig_function = sympy.sin if names["trig"] == "sin" else sympy.cos
   angle = names["angle_turns"] * sympy.pi

   radius = constant + sign * amplitude * trig_function(2 * theta)
   radius_rate = sympy.diff(radius, theta)
   vertical_value, horizontal_value = _slope(radius, radius_rate, angle)
   key_value = sympy.radsimp(vertical_value / horizontal_value) if horizontal_value != 0 else sympy.zoo

   radius_rate_value = sympy.simplify(radius_rate.subs(theta, angle))
   product_of_derivatives = sympy.simplify(-sympy.cos(angle) / sympy.sin(angle))
   no_chain_rate = sign * amplitude * sympy.diff(trig_function(theta), theta).subs(theta, 2 * theta)
   no_chain_vertical, no_chain_horizontal = _slope(radius, no_chain_rate, angle)
   no_chain_value = sympy.radsimp(no_chain_vertical / no_chain_horizontal) if no_chain_horizontal != 0 else sympy.zoo

   angle_tex = tex(angle)
   stem = (
      f"Find the exact slope of the line tangent to the polar curve {math('r = ' + tex(radius))} at the point where "
      f"{math(r'\theta = ' + angle_tex)}."
   )

   steps = [
      Step(
         text=(
            f"Write {math(r'x = r\cos\theta')} and {math(r'y = r\sin\theta')}, and differentiate r by the chain rule: "
            f"{math(r'\frac{dr}{d\theta} = ' + tex(radius_rate))}, which is {math(tex(radius_rate_value))} at "
            f"{math(r'\theta = ' + angle_tex)}."
         ),
         value=radius_rate_value,
         rule="chain rule",
      ),
      Step(
         text=(
            f"By the product rule, {math(r'\frac{dy}{d\theta} = \frac{dr}{d\theta}\sin\theta + r\cos\theta')} and "
            f"{math(r'\frac{dx}{d\theta} = \frac{dr}{d\theta}\cos\theta - r\sin\theta')}. At "
            f"{math(r'\theta = ' + angle_tex)} these are {math(tex(vertical_value))} and {math(tex(horizontal_value))}."
         ),
         rule="product rule",
      ),
      Step(
         text=(
            f"The slope is {math(r'\frac{dy/d\theta}{dx/d\theta} = ' + tex(key_value))}."
         ),
         value=key_value,
         rule="slope of a polar curve",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09031",
         derivation="dr/dtheta at the angle reported as the slope of the tangent line",
         value=radius_rate_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-09032",
         derivation="r sin(theta) and r cos(theta) each differentiated as the product of the two derivatives, which gives -cot(theta)",
         value=product_of_derivatives,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="the radius differentiated without the factor 2 from the chain rule, then the slope formed correctly",
         value=no_chain_value,
         mechanism="chain_rule_omitted",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-13",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"horizontal_rate": horizontal_value},
   )
