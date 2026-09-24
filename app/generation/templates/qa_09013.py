"""BC-QA-09013, the area inside one polar curve and outside a circle, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral, tex

ARCHETYPE_ID = "BC-QA-09013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 8, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 8, "step": 1}},
      {"name": "circle", "type": "rational", "role": "safe", "domain": {"min": 1.5, "max": 9, "step": 0.5}},
      {"name": "orientation", "type": "label", "role": "safe", "domain": {"values": ["right", "up", "left", "down"]}},
      {"name": "intersections", "type": "label", "role": "difficulty", "domain": {"values": ["given", "found"]}},
   ],
   "constraints": [
      "constant < circle",
      "circle < constant + coefficient",
      "coefficient < constant + circle",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "intersections", "difficulty_factor_id": "BC-DF-07", "settings": {"given": "off", "found": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-13", "figure_kind": None, "requires": ["constant", "coefficient", "circle", "orientation"]},
   ],
   "notes": "The outer curve is a limacon r = constant plus or minus coefficient times cos or sin, crossing the circle r = circle twice, with the region symmetric about the ray through the limacon's farthest point. The inner loop, when present, stays inside the circle.",
}

theta = sympy.Symbol("theta")
ORIENTATIONS = {
   "right": (sympy.cos, 1, sympy.Integer(0)),
   "up": (sympy.sin, 1, sympy.pi / 2),
   "left": (sympy.cos, -1, sympy.pi),
   "down": (sympy.sin, -1, 3 * sympy.pi / 2),
}


def build(names):
   constant = names["constant"]
   coefficient = names["coefficient"]
   circle = names["circle"]
   is_given = names["intersections"] == "given"
   trig_function, sign, centre = ORIENTATIONS[names["orientation"]]

   outer = constant + sign * coefficient * trig_function(theta)
   half_width = sympy.acos((circle - constant) / coefficient)
   low_angle = centre - half_width
   high_angle = centre + half_width
   low_value = sympy.N(low_angle, 30)
   high_value = sympy.N(high_angle, 30)

   difference_of_squares = outer**2 - circle**2
   key_value = numeric_integral(difference_of_squares, theta, low_value, high_value) / 2
   no_half = 2 * key_value
   half_sweep = numeric_integral(difference_of_squares, theta, sympy.N(centre, 30), high_value) / 2
   square_of_difference = numeric_integral((outer - circle) ** 2, theta, low_value, high_value) / 2

   outer_tex = "r = " + tex(outer)
   circle_tex = "r = " + tex(circle)
   low_text = decimal_text(low_value)
   high_text = decimal_text(high_value)
   crossing_sentence = (
      f" The curves intersect at {math(rf'\theta = {low_text}')} and {math(rf'\theta = {high_text}')}, "
      f"correct to three decimal places."
      if is_given else ""
   )
   stem = (
      f"Let R be the region that lies inside the polar curve {math(outer_tex)} and outside the circle "
      f"{math(circle_tex)}.{crossing_sentence} Using a calculator, "
      "find the area of R. Show the setup for the calculation, and give the value correct to three decimal places."
   )

   if is_given:
      limits_text = f"The stated intersection angles are {math(low_text)} and {math(high_text)}"
   else:
      limits_text = (
         f"Setting {math(tex(outer) + ' = ' + tex(circle))} gives the intersection angles "
         f"{math(rf'\theta \approx {low_text}')} and {math(rf'\theta \approx {high_text}')}"
      )

   integral_tex = (
      rf"\frac{{1}}{{2}}\int_{{{low_text}}}^{{{high_text}}} \left(\left({tex(outer)}\right)^2 - {tex(circle**2)}\right)\,d\theta"
   )
   steps = [
      Step(
         text=f"{limits_text}, and between them the limacon is outside the circle, so it is the outer curve.",
         point_type_id="BC-PT-99001",
         rule="intersection angles",
      ),
      Step(
         text=f"The area is one half the integral of the difference of the squares of the radii: {math('A = ' + integral_tex)}.",
         point_type_id="BC-PT-99048",
         rule="area between polar curves",
      ),
      Step(
         text=f"A calculator gives {math(r'A \approx ' + decimal_text(key_value))}, using the unrounded intersection angles.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="numerical integration",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09035",
         derivation="the factor of one half left off the integral of the difference of the squares",
         value=no_half,
         mechanism="forgot_constant",
      ),
      Distractor(
         error_path="BC-ERR-09040",
         derivation="the square of the difference of the radii integrated in place of the difference of the squares",
         value=square_of_difference,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-09041",
         derivation="the integral taken over half the region, from the axis of symmetry to one intersection angle, without doubling",
         value=half_sweep,
         mechanism="forgot_constant",
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
