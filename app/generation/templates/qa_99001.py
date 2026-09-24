"""BC-QA-99001, the polar tangent slope relation solved for the derivative of the horizontal coordinate."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-99001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "sign", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {
         "name": "angle_turns",
         "type": "rational",
         "role": "safe",
         "domain": {"values": ["1/6", "1/4", "1/3", "2/3", "3/4", "5/6", "7/6", "5/4", "4/3", "5/3", "7/4", "11/6"]},
      },
      {"name": "notation", "type": "label", "role": "difficulty", "domain": {"values": ["verbal", "leibniz"]}},
   ],
   "constraints": [
      "constant != amplitude",
      "not (abs(constant - amplitude) == 2 and ((trig == 'sin' and sign == 1 and 6 * angle_turns in [1, 5]) or (trig == 'sin' and sign == -1 and 6 * angle_turns in [7, 11]) or (trig == 'cos' and sign == 1 and 6 * angle_turns in [2, 10]) or (trig == 'cos' and sign == -1 and 6 * angle_turns in [4, 8])))",
      "not (trig == 'cos' and sign == -1 and 6 * angle_turns in [2, 10] and constant * amplitude == 8 and abs(constant - amplitude) == 2)",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "slope == curve_slope",
      "vertical_rate == curve_vertical_rate",
      "key == curve_horizontal_rate",
   ],
   "dial_bindings": [
      {"parameter": "notation", "difficulty_factor_id": "BC-DF-04", "settings": {"verbal": "off", "leibniz": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-13", "figure_kind": None, "requires": ["constant", "amplitude", "sign", "trig", "angle_turns"]},
   ],
   "notes": "P is the point of r = constant + sign amplitude trig(theta) at angle_turns times pi, which the stem does not name. The stated dy/dx and dy/dtheta are that point's exact values, and the invariants recompute the curve's slope, dy/dtheta and dx/dtheta from x = r cos(theta), y = r sin(theta) and check the premise and the key against them. The constraints remove, from a full enumeration of the domain, every draw where dx/dtheta or dy/dtheta is 0 (all on cardioids, constant equal to amplitude) or two options coincide (dy/dtheta equal to 1 or -1, or dy/dtheta equal to the square of the slope).",
}

theta = sympy.Symbol("theta")


def _exact(expression):
   return sympy.radsimp(sympy.simplify(expression))


def build(names):
   trig_function = sympy.sin if names["trig"] == "sin" else sympy.cos
   angle = names["angle_turns"] * sympy.pi
   is_leibniz = names["notation"] == "leibniz"

   radius = names["constant"] + names["sign"] * names["amplitude"] * trig_function(theta)
   radius_rate = sympy.diff(radius, theta)
   vertical_rate = _exact((radius_rate * sympy.sin(theta) + radius * sympy.cos(theta)).subs(theta, angle))
   horizontal_rate = _exact((radius_rate * sympy.cos(theta) - radius * sympy.sin(theta)).subs(theta, angle))
   slope = _exact(vertical_rate / horizontal_rate)

   curve_vertical_rate = sympy.diff(radius * sympy.sin(theta), theta).subs(theta, angle)
   curve_horizontal_rate = sympy.diff(radius * sympy.cos(theta), theta).subs(theta, angle)
   curve_slope = curve_vertical_rate / curve_horizontal_rate

   key_value = _exact(vertical_rate / slope)
   inverted_quotient = _exact(slope * vertical_rate)
   chain_product = _exact(slope / vertical_rate)

   slope_tex = tex(slope)
   rate_tex = tex(vertical_rate)

   if is_leibniz:
      given = (
         f"At a point P on the curve, {math(r'\frac{dy}{dx} = ' + slope_tex)} and "
         f"{math(r'\frac{dy}{d\theta} = ' + rate_tex)}."
      )
      request = f"find the exact value of {math(r'\frac{dx}{d\theta}')} at P"
   else:
      given = (
         f"At a point P on the curve, the slope of the line tangent to the curve is {math(slope_tex)}, and the rate of "
         f"change of y with respect to {math(r'\theta')} is {math(rate_tex)}."
      )
      request = f"find the exact rate of change of x with respect to {math(r'\theta')} at P"

   stem = (
      f"A curve is given in polar coordinates by {math('r = ' + tex(radius))}, where "
      f"{math(r'x = r\cos\theta')} and {math(r'y = r\sin\theta')}. {given} A calculator may be used. Without "
      f"differentiating the polar equation, {request}, and show the work that leads to your answer."
   )

   relation_tex = r"\frac{dy}{dx} = \frac{dy/d\theta}{dx/d\theta}"
   solved_tex = r"\frac{dx}{d\theta} = \frac{dy/d\theta}{dy/dx}"
   steps = [
      Step(
         text=f"For a curve described by the angle, {math(relation_tex)}, so {math(solved_tex)}.",
         point_type_id="BC-PT-99049",
         rule="chain rule for polar slope",
      ),
      Step(
         text=(
            f"Substituting, {math(r'\frac{dx}{d\theta} = \frac{' + rate_tex + '}{' + slope_tex + '} = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99005",
         rule="substitution",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09002",
         derivation="the slope written as dx/dtheta divided by dy/dtheta, so solving gives dx/dtheta = (dy/dx)(dy/dtheta)",
         value=inverted_quotient,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="the chain rule product formed as dy/dx = (dy/dtheta)(dx/dtheta), so dx/dtheta = (dy/dx)/(dy/dtheta)",
         value=chain_product,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-09003",
         derivation="the slope and a rate with respect to theta treated as the same quantity, so the supplied slope is reported",
         value=slope,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-13",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
      notes={
         "slope": slope,
         "vertical_rate": vertical_rate,
         "curve_slope": curve_slope,
         "curve_vertical_rate": curve_vertical_rate,
         "curve_horizontal_rate": curve_horizontal_rate,
      },
   )
