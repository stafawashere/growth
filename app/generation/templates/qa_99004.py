"""BC-QA-99004, the time at which a Cartesian coordinate of a particle on a polar path reaches a value, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_roots, tex

ARCHETYPE_ID = "BC-QA-99004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "fraction", "type": "real", "role": "safe", "domain": {"values": [0.2, 0.4, 0.5, 0.6, 0.8]}},
      {"name": "duration", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "coordinate", "type": "label", "role": "safe", "domain": {"values": ["x", "y"]}},
      {"name": "angle_given", "type": "label", "role": "difficulty", "domain": {"values": ["function", "rate"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "target", "expression": "constant + amplitude * fraction"},
   ],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "0 < key < duration",
      "root_count == 1",
   ],
   "dial_bindings": [
      {"parameter": "angle_given", "difficulty_factor_id": "BC-DF-14", "settings": {"function": "off", "rate": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {
         "representation": "BC-REP-13",
         "figure_kind": None,
         "requires": ["constant", "amplitude", "fraction", "duration", "coordinate"],
      },
   ],
   "notes": "For y the curve is r = c + a sin(theta), for x it is r = c + a cos(theta), and theta runs from 0 to pi/2 over the time interval. The named coordinate and r are both monotone there and the target lies strictly between c and c + a, so the coordinate and r each reach it exactly once, at different times.",
}

theta = sympy.Symbol("theta")
t = sympy.Symbol("t")


def _rounded_angle_time(angle, time_per_radian, key):
   for places in (1, 2):
      early = sympy.Float(round(float(angle), places), 15) * time_per_radian
      coincides = round(float(early), 3) == round(float(key), 3)

      if not coincides:
         return early, places

   return sympy.Float(round(float(angle), 1) + 0.1, 15) * time_per_radian, 0


def build(names):
   constant = names["constant"]
   amplitude = names["amplitude"]
   target = sympy.nsimplify(names["target"])
   duration = names["duration"]
   is_vertical = names["coordinate"] == "y"
   is_rate = names["angle_given"] == "rate"

   if is_vertical:
      radius = constant + amplitude * sympy.sin(theta)
      coordinate = radius * sympy.sin(theta)
   else:
      radius = constant + amplitude * sympy.cos(theta)
      coordinate = radius * sympy.cos(theta)

   angle_rate = sympy.pi / (2 * duration)
   angle_of_time = angle_rate * t
   time_per_radian = sympy.N(1 / angle_rate, 30)

   coordinate_in_time = coordinate.subs(theta, angle_of_time)
   roots = numeric_roots(coordinate_in_time - target, t, 0, duration)
   key_value = roots[0]
   key_angle = sympy.N(angle_rate * key_value, 30)
   radius_time = numeric_roots(radius.subs(theta, angle_of_time) - target, t, 0, duration)[0]
   rounded_time, places = _rounded_angle_time(key_angle, time_per_radian, key_value)

   curve_tex = "r = " + tex(radius)
   window = rf"0 \le t \le {duration}"
   target_text = f"{float(target):g}"

   if is_rate:
      motion = (
         f"A particle moves along the polar curve {math(curve_tex)} for {math(window)}. At time t = 0 the particle is at "
         f"{math(r'\theta = 0')}, and its angle increases at the constant rate {math(r'\frac{d\theta}{dt} = ' + tex(angle_rate))}."
      )
      angle_step = (
         f"The angle starts at 0 and grows at a constant rate, so {math(r'\theta(t) = ' + tex(angle_of_time))}. "
      )
   else:
      motion = (
         f"A particle moves along the polar curve {math(curve_tex)} so that at time t its angle is "
         f"{math(r'\theta(t) = ' + tex(angle_of_time))}, for {math(window)}."
      )
      angle_step = ""

   stem = (
      f"{motion} Using a calculator, find the time t at which the {names['coordinate']}-coordinate of the particle's "
      f"position is {target_text}. Show the setup for the calculation, and give the value correct to three decimal places."
   )

   factor_tex = r"\sin\theta" if is_vertical else r"\cos\theta"
   letter = names["coordinate"]
   steps = [
      Step(
         text=(
            f"{angle_step}The coordinate is {math(letter + ' = r' + factor_tex + ' = ' + tex(coordinate))}, so in terms of time "
            f"{math(letter + '(t) = ' + tex(coordinate_in_time))}."
         ),
         point_type_id="BC-PT-99005",
         rule="polar to rectangular conversion",
      ),
      Step(
         text=(
            f"Solve {math(tex(coordinate_in_time) + ' = ' + target_text)} on {math(window)} with a calculator. The only "
            f"solution is {math(r't \approx ' + decimal_text(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="numerical solution",
      ),
   ]

   if places == 1:
      rounding = "the angle rounded to one decimal place before it was converted to a time"
   elif places == 2:
      rounding = "the angle rounded to two decimal places before it was converted to a time"
   else:
      rounding = "the angle rounded up to the next tenth before it was converted to a time"

   distractors = [
      Distractor(
         error_path="BC-ERR-09027",
         derivation=f"r treated as the {letter}-coordinate, so the time at which r equals the value is reported",
         value=radius_time,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99031",
         derivation="the equation solved in theta and the angle reported in place of the time",
         value=key_angle,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-99019",
         derivation=rounding,
         value=rounded_time,
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
      notes={"root_count": len(roots)},
   )
