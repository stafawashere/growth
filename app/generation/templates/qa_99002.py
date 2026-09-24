"""BC-QA-99002, the derivative of a Cartesian coordinate with respect to theta on a polar curve, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-99002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "frequency", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2, 3]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "coordinate", "type": "label", "role": "safe", "domain": {"values": ["x", "y"]}},
      {
         "name": "angle",
         "type": "real",
         "role": "safe",
         "domain": {"values": [0.3, 0.4, 0.6, 0.7, 0.9, 1.1, 1.3, 1.4, 1.7, 2.2]},
      },
   ],
   "constraints": [
      "not (constant == 5 and amplitude == 1 and frequency == 3 and trig == 'cos' and coordinate == 'x' and angle == 7/5)",
      "not (constant == 5 and amplitude == 4 and frequency == 3 and trig == 'sin' and coordinate == 'x' and angle == 9/10)",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "frequency", "difficulty_factor_id": "BC-DF-06", "settings": {"1": "off", "2": "low", "3": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-13",
         "figure_kind": None,
         "requires": ["constant", "amplitude", "frequency", "trig", "coordinate", "angle"],
      },
   ],
   "notes": "The radius is constant plus amplitude times sin or cos of frequency theta; a frequency above 1 puts a chain rule inside the product rule. The angle is a decimal in radians. A full enumeration of the domain finds two draws whose value rounds to a whole number at three places, and the constraints remove them.",
}

theta = sympy.Symbol("theta")
DEGREE = sympy.pi / 180


def build(names):
   constant = names["constant"]
   amplitude = names["amplitude"]
   frequency = names["frequency"]
   angle = sympy.nsimplify(names["angle"])
   trig_function = sympy.sin if names["trig"] == "sin" else sympy.cos
   is_horizontal = names["coordinate"] == "x"

   radius = constant + amplitude * trig_function(frequency * theta)
   angle_factor = sympy.cos(theta) if is_horizontal else sympy.sin(theta)
   coordinate = radius * angle_factor
   coordinate_rate = sympy.diff(coordinate, theta)
   key_value = sympy.N(coordinate_rate.subs(theta, angle), 30)

   radius_rate = sympy.diff(radius, theta)
   radius_rate_value = sympy.N(radius_rate.subs(theta, angle), 30)
   derivative_product = sympy.N((radius_rate * sympy.diff(angle_factor, theta)).subs(theta, angle), 30)

   degree_coordinate = coordinate.subs(theta, theta * DEGREE)
   degree_value = sympy.N(sympy.diff(degree_coordinate, theta).subs(theta, angle), 30)

   letter = names["coordinate"]
   factor_tex = r"\cos\theta" if is_horizontal else r"\sin\theta"
   angle_text = f"{float(angle):g}"
   stem = (
      f"A curve is given in polar coordinates by {math('r = ' + tex(radius))}. Using a calculator, find the value of "
      f"{math(rf'\frac{{d{letter}}}{{d\theta}}')} at {math(r'\theta = ' + angle_text)}, where "
      f"{math(letter + ' = r' + factor_tex)}. Show the setup for the calculation, and give the value correct to three "
      "decimal places."
   )

   steps = [
      Step(
         text=f"Write the coordinate in terms of the angle: {math(letter + ' = ' + tex(coordinate))}.",
         point_type_id="BC-PT-99049",
         rule="polar to rectangular conversion",
      ),
      Step(
         text=(
            f"By the product rule, {math(rf'\frac{{d{letter}}}{{d\theta}} = ' + tex(coordinate_rate))}."
         ),
         point_type_id="BC-PT-99049",
         rule="product rule",
      ),
      Step(
         text=(
            f"With the calculator in radian mode, the value at {math(r'\theta = ' + angle_text)} is about "
            f"{decimal_text(key_value)}."
         ),
         value=key_value,
         point_type_id="BC-PT-99005",
         rule="evaluation at the stated angle",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09032",
         derivation=f"the product r {'cos' if is_horizontal else 'sin'}(theta) differentiated as the product of the two derivatives, dr/dtheta times the derivative of the angle factor",
         value=derivative_product,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-09027",
         derivation=f"r taken to be the coordinate {letter} itself, so dr/dtheta is reported",
         value=radius_rate_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-09023",
         derivation="the derivative of the coordinate evaluated with the calculator in degree mode",
         value=degree_value,
         mechanism="algebra_slip",
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
