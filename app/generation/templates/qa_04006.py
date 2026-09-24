"""BC-QA-04006, related rates in a geometric setting, with the requested rate found at an instant."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-04006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "shape", "type": "label", "role": "difficulty", "domain": {"values": ["circle", "cube", "sphere", "ladder", "cone"]}},
      {"name": "size", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 10, "step": 1}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "ratio", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "leg", "type": "label", "role": "safe", "domain": {"values": ["short", "long"]}},
      {"name": "length_unit", "type": "label", "role": "safe", "domain": {"values": ["centimeter", "inch", "foot", "meter"]}},
      {"name": "time_unit", "type": "label", "role": "safe", "domain": {"values": ["second", "minute"]}},
   ],
   "constraints": [
      "not (shape == 'cube' and size == 4)",
      "not (shape == 'sphere' and size == 2)",
      "not (shape == 'circle' and size == rate)",
      "not (shape == 'sphere' and size == 2 * rate)",
      "not (shape == 'cube' and size == 4 * rate)",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "shape", "difficulty_factor_id": "BC-DF-02", "settings": {"circle": "off", "cube": "off", "sphere": "low", "ladder": "low", "cone": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["shape", "size", "rate", "ratio", "leg", "length_unit", "time_unit"]},
   ],
   "notes": "Five configurations: a spreading circle, a growing cube and sphere, a sliding ladder on a 3-4-5 triangle scaled by ratio, and a conical tank whose height is ratio + 1 times its top radius, filled at a constant rate.",
}

PLURAL = {"centimeter": "centimeters", "inch": "inches", "foot": "feet", "meter": "meters"}

LADDER_UNITS = {"centimeter": "meters", "inch": "feet", "foot": "feet", "meter": "meters"}


def _circle(names, length, lengths, per):
   radius = names["size"]
   rate = names["rate"]
   key_value = 2 * sympy.pi * radius * rate
   stem = (
      f"A circular ripple spreads on the surface of a pond so that its radius increases at a constant rate of {rate} "
      f"{lengths} per {per}. At the instant when the radius is {radius} {lengths}, find the rate at which the area "
      "enclosed by the ripple is increasing. Give an exact answer with units."
   )
   steps = [
      Step(text=f"The area enclosed is {math('A = \\pi r^{2}')}, with r the radius, both depending on time.", rule="relating equation"),
      Step(
         text=f"Differentiate with respect to time: {math(r'\frac{dA}{dt} = 2\pi r \frac{dr}{dt}')}.",
         point_type_id="BC-PT-99023",
         rule="chain rule",
      ),
      Step(
         text=f"At the instant, r = {radius} and {math(rf'\frac{{dr}}{{dt}} = {rate}')}, so {math(r'\frac{dA}{dt} = ' + tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="substitute after differentiating",
      ),
   ]
   distractors = [
      Distractor("BC-ERR-04017", "the area differentiated with respect to the radius, dA/dr = 2 pi r, and the chain rule factor dr/dt never applied", value=2 * sympy.pi * radius, mechanism="chain_rule_omitted"),
      Distractor("BC-ERR-04016", "the circumference 2 pi r used as the relating equation for the area, giving 2 pi dr/dt", value=2 * sympy.pi * rate, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-04015", "the supplied rate dr/dt reported as the requested rate dA/dt", value=sympy.Integer(rate), mechanism="reversed_quantities"),
   ]

   return stem, steps, distractors, key_value, f"square {lengths} per {per}"


def _sphere(names, length, lengths, per):
   radius = names["size"]
   rate = names["rate"]
   key_value = 4 * sympy.pi * radius**2 * rate
   stem = (
      f"A spherical balloon is inflated so that its radius increases at a constant rate of {rate} {lengths} per {per}. "
      f"At the instant when the radius is {radius} {lengths}, find the rate at which the volume of the balloon is "
      "increasing. Give an exact answer with units."
   )
   steps = [
      Step(text=f"The volume is {math(r'V = \tfrac{4}{3}\pi r^{3}')}, with r the radius, both depending on time.", rule="relating equation"),
      Step(
         text=f"Differentiate with respect to time: {math(r'\frac{dV}{dt} = 4\pi r^{2} \frac{dr}{dt}')}.",
         point_type_id="BC-PT-99023",
         rule="chain rule",
      ),
      Step(
         text=f"At the instant, r = {radius} and {math(rf'\frac{{dr}}{{dt}} = {rate}')}, so {math(r'\frac{dV}{dt} = ' + tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="substitute after differentiating",
      ),
   ]
   distractors = [
      Distractor("BC-ERR-04017", "the volume differentiated with respect to the radius, dV/dr = 4 pi r squared, and the chain rule factor dr/dt never applied", value=4 * sympy.pi * radius**2, mechanism="chain_rule_omitted"),
      Distractor("BC-ERR-04016", "the surface area 4 pi r squared used as the relating equation for the volume, giving 8 pi r dr/dt", value=8 * sympy.pi * radius * rate, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-04015", "the supplied rate dr/dt reported as the requested rate dV/dt", value=sympy.Integer(rate), mechanism="reversed_quantities"),
   ]

   return stem, steps, distractors, key_value, f"cubic {lengths} per {per}"


def _cube(names, length, lengths, per):
   edge = names["size"]
   rate = names["rate"]
   key_value = sympy.Integer(3 * edge**2 * rate)
   stem = (
      f"A crystal grows in the shape of a cube, and each edge lengthens at a constant rate of {rate} {lengths} per {per}. "
      f"At the instant when each edge is {edge} {lengths} long, find the rate at which the volume of the crystal is "
      "increasing. Give an exact answer with units."
   )
   steps = [
      Step(text=f"The volume is {math('V = s^{3}')}, with s the edge length, both depending on time.", rule="relating equation"),
      Step(
         text=f"Differentiate with respect to time: {math(r'\frac{dV}{dt} = 3s^{2} \frac{ds}{dt}')}.",
         point_type_id="BC-PT-99023",
         rule="chain rule",
      ),
      Step(
         text=f"At the instant, s = {edge} and {math(rf'\frac{{ds}}{{dt}} = {rate}')}, so {math(r'\frac{dV}{dt} = ' + tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="substitute after differentiating",
      ),
   ]
   distractors = [
      Distractor("BC-ERR-04017", "the volume differentiated with respect to the edge, dV/ds = 3 s squared, and the chain rule factor ds/dt never applied", value=sympy.Integer(3 * edge**2), mechanism="chain_rule_omitted"),
      Distractor("BC-ERR-04016", "the surface area 6 s squared used as the relating equation for the volume, giving 12 s ds/dt", value=sympy.Integer(12 * edge * rate), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-04015", "the supplied rate ds/dt reported as the requested rate dV/dt", value=sympy.Integer(rate), mechanism="reversed_quantities"),
   ]

   return stem, steps, distractors, key_value, f"cubic {lengths} per {per}"


def _ladder(names, length, lengths, per):
   lengths = LADDER_UNITS[length]
   scale = names["ratio"]
   rate = names["rate"]
   is_short = names["leg"] == "short"
   foot = (3 if is_short else 4) * scale
   top = (4 if is_short else 3) * scale
   ladder = 5 * scale
   key_value = sympy.Rational(-foot * rate, top)
   stem = (
      f"A ladder {ladder} {lengths} long leans against a vertical wall. The bottom of the ladder slides away from the wall "
      f"along level ground at a constant rate of {rate} {lengths} per {per}. At the instant when the bottom of the ladder "
      f"is {foot} {lengths} from the wall, find the rate of change of the height of the top of the ladder. Give an exact "
      "answer with units."
   )
   steps = [
      Step(
         text=f"With x the distance from the wall to the bottom and y the height of the top, {math(f'x^{{2}} + y^{{2}} = {ladder**2}')}.",
         rule="relating equation",
      ),
      Step(
         text=f"At the instant x = {foot}, so {math(f'y = \\sqrt{{{ladder**2} - {foot**2}}} = {top}')}.",
         value=sympy.Integer(top),
         rule="missing instantaneous value from the relating equation",
      ),
      Step(
         text=f"Differentiate with respect to time: {math(r'2x\frac{dx}{dt} + 2y\frac{dy}{dt} = 0')}.",
         point_type_id="BC-PT-99023",
         rule="chain rule",
      ),
      Step(
         text=(
            f"Substitute x = {foot}, y = {top} and {math(rf'\frac{{dx}}{{dt}} = {rate}')}: "
            f"{math(r'\frac{dy}{dt} = -\frac{x}{y}\frac{dx}{dt} = ' + tex(key_value))}, negative because the top slides down."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="substitute after differentiating",
      ),
   ]
   distractors = [
      Distractor("BC-ERR-04005", "the rate reported as a positive size, so the downward motion of the top is lost", value=-key_value, mechanism="sign_error"),
      Distractor("BC-ERR-04017", "the relation differentiated with respect to x, dy/dx = -x/y, and the chain rule factor dx/dt never applied", value=sympy.Rational(-foot, top), mechanism="chain_rule_omitted"),
      Distractor("BC-ERR-04015", "the supplied rate dx/dt reported as the requested rate dy/dt", value=sympy.Integer(rate), mechanism="reversed_quantities"),
   ]

   return stem, steps, distractors, key_value, f"{lengths} per {per}"


def _cone(names, length, lengths, per):
   depth = names["size"]
   inflow = names["rate"]
   stretch = names["ratio"] + 1
   key_value = sympy.Rational(stretch**2 * inflow, depth**2) / sympy.pi
   stem = (
      f"Water is poured at a constant rate of {inflow} cubic {lengths} per {per} into a tank shaped like a cone with its "
      f"vertex pointing down. The height of the tank is {stretch} times the radius of its circular top. At the instant when "
      f"the water is {depth} {lengths} deep, find the rate at which the depth of the water is increasing. Give an exact "
      "answer with units."
   )
   volume_in_h = rf"V = \tfrac{{1}}{{3}}\pi \left(\tfrac{{h}}{{{stretch}}}\right)^{{2}} h = \tfrac{{\pi}}{{{3 * stretch**2}}} h^{{3}}"
   steps = [
      Step(
         text=(
            f"With h the depth and r the radius of the water surface, {math(r'V = \tfrac{1}{3}\pi r^{2} h')}, and by similar "
            f"triangles {math(f'r = \\tfrac{{h}}{{{stretch}}}')}, so {math(volume_in_h)}."
         ),
         rule="relating equation with the radius eliminated",
      ),
      Step(
         text=f"Differentiate with respect to time: {math(rf'\frac{{dV}}{{dt}} = \frac{{\pi}}{{{stretch**2}}} h^{{2}} \frac{{dh}}{{dt}}')}.",
         point_type_id="BC-PT-99023",
         rule="chain rule",
      ),
      Step(
         text=(
            f"Substitute h = {depth} and {math(rf'\frac{{dV}}{{dt}} = {inflow}')}: "
            f"{math(r'\frac{dh}{dt} = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="solve for the requested rate",
      ),
   ]
   frozen_radius = sympy.Rational(depth, stretch)
   distractors = [
      Distractor(
         "BC-ERR-04020",
         f"the radius replaced by its value {frozen_radius} at the instant before differentiating, so V = (1/3) pi r0^2 h gives dh/dt = 3 dV/dt / (pi r0^2)",
         value=3 * inflow / (sympy.pi * frozen_radius**2),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         "BC-ERR-04017",
         f"the volume differentiated with respect to the depth, dV/dh = pi h^2 / {stretch**2} at h = {depth}, and the rate dV/dt never brought in",
         value=sympy.pi * depth**2 / stretch**2,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         "BC-ERR-04016",
         "the cylinder formula V = pi r^2 h used for the cone, which drops the factor 1/3 from the relating equation",
         value=key_value / 3,
         mechanism="conceptual_confusion",
      ),
   ]

   return stem, steps, distractors, key_value, f"{lengths} per {per}"


BUILDERS = {"circle": _circle, "sphere": _sphere, "cube": _cube, "ladder": _ladder, "cone": _cone}


def build(names):
   length = names["length_unit"]
   lengths = PLURAL[length]
   per = names["time_unit"]
   stem, steps, distractors, key_value, units = BUILDERS[names["shape"]](names, length, lengths, per)

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value, units=units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-05",
      calculator_status="no_calculator",
      command_verb="find",
   )
