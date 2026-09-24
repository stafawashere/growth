"""BC-QA-08012, the volume of a solid of revolution by discs, about the x-axis or a horizontal line."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, sample_curve, segment_mark
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "safe", "domain": {"values": ["root", "linear", "square"]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "left", "type": "integer", "role": "safe", "domain": {"values": [0, 1]}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "presentation", "type": "label", "role": "safe", "domain": {"values": ["figure", "formula"]}},
      {"name": "axis", "type": "label", "role": "difficulty", "domain": {"values": ["x_axis", "shifted"]}},
   ],
   "constraints": [
      "form != 'linear' or scale != 2",
      "level * width + 2 * profile_integral != 0",
   ],
   "derived": [
      {"name": "right", "expression": "left + width"},
      {"name": "profile_integral", "expression": "scale * 2 * (sqrt(right)**3 - sqrt(left)**3) / 3 if form == 'root' else (scale * (right**2 - left**2) / 2 if form == 'linear' else scale * (right**3 - left**3) / 3)"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "axis", "difficulty_factor_id": "BC-DF-08", "settings": {"x_axis": "off", "shifted": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-08", "figure_kind": "region", "requires": ["form", "scale", "left", "width", "level", "axis"]},
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["form", "scale", "left", "width", "level", "axis"]},
   ],
   "notes": "The curve is y = level + p(x) with p one of scale sqrt(x), scale x, scale x^2, nonnegative on the interval; the region lies between the curve and the line y = level (y = 0 when the axis is the x-axis), from x = left to x = right, so every slice is a disc of radius p(x). The level is kept away from minus twice the mean of p, where measuring from the x-axis would give the same volume, and a linear profile with scale 2 is excluded because its shell volume about the y-axis equals the disc volume.",
}

x = sympy.Symbol("x")


def _profile(form, scale):
   if form == "root":
      return scale * sympy.sqrt(x)

   if form == "linear":
      return scale * x

   return scale * x**2


def _region_figure(curve, level, left, right):
   low_x = left - 1
   high_x = right + 1
   top_value = curve.subs(x, right)
   top = sympy.ceiling(max(top_value, level, 0)) + 1
   bottom = sympy.floor(min(level, 0)) - 1

   outline = []

   for index in range(41):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      outline.append([float(x_value), float(curve.subs(x, x_value))])

   outline.append([float(right), float(level)])
   outline.append([float(left), float(level)])

   return figure(
      "region",
      domain=(low_x, high_x),
      range_=(bottom, top),
      curves=[sample_curve(curve, x, max(low_x, 0), high_x, y_limit=float(max(abs(top), abs(bottom))))],
      marks=[
         segment_mark((low_x, level), (high_x, level), style="dashed"),
         segment_mark((right, level), (right, curve.subs(x, right))),
      ],
      labels=[label("y = f(x)", left + sympy.Rational(1, 2) * (right - left), min(float(top) - 0.4, float(curve.subs(x, sympy.Rational(1, 2) * (left + right))) + 0.8))],
      fills=[outline],
      alt=(
         f"The region between the graph of y = f(x) and the line y = {level}, from x = {left} to x = {right}, "
         f"with the line y = {level} drawn dashed as the axis of revolution."
      ),
   )


def build(names):
   form = names["form"]
   scale = names["scale"]
   left = names["left"]
   right = names["right"]
   is_shifted = names["axis"] == "shifted"
   is_figure = names["presentation"] == "figure"
   level = names["level"] if is_shifted else sympy.Integer(0)

   profile = _profile(form, scale)
   curve = level + profile

   def integral_of(expression):
      return sympy.integrate(sympy.expand(expression), (x, left, right))

   radius_squared = integral_of(profile**2)
   volume = sympy.pi * radius_squared

   if left == 0:
      vertical_lines = f"the vertical line {math(f'x = {right}')}"
   else:
      vertical_lines = f"the vertical lines {math(f'x = {left}')} and {math(f'x = {right}')}"

   if is_shifted:
      axis_text = f"the line {math(f'y = {level}')}"
      region_text = f"the graph of f, the line {math(f'y = {level}')}, and {vertical_lines}"
   else:
      axis_text = "the x-axis"
      region_text = f"the graph of f, the x-axis, and {vertical_lines}"

   if is_figure:
      region_sentence = f"The region R shown is bounded by {region_text}."
      graph = _region_figure(curve, level, left, right)
      representation = "BC-REP-08"
   else:
      region_sentence = f"Let R be the region bounded by {region_text}."
      graph = None
      representation = "BC-REP-01"

   stem = (
      f"Let {math('f(x) = ' + tex_f(curve))}. {region_sentence} Find the exact volume of the solid generated when R "
      f"is revolved about {axis_text}."
   )

   radius_text = tex_f(profile)
   shift_text = f"({level})" if level < 0 else f"{level}"

   if is_shifted:
      radius_step = f"Each slice perpendicular to the x-axis is a disc whose radius is the distance from the curve to the axis, {math(f'r = f(x) - {shift_text} = {radius_text}')}."
   else:
      radius_step = f"Each slice perpendicular to the x-axis is a disc of radius {math(f'r = f(x) = {radius_text}')}."

   integral = rf"\pi\int_{{{left}}}^{{{right}}} \left({radius_text}\right)^{{2}}\,dx"
   steps = [
      Step(text=radius_step, point_type_id="BC-PT-99058", rule="disc radius"),
      Step(text=f"The volume is {math(integral)}.", point_type_id="BC-PT-99001", rule="disc method"),
      Step(
         text=f"Since {math(rf'\int_{{{left}}}^{{{right}}} {tex_f(sympy.expand(profile**2))}\,dx = {tex_f(radius_squared)}')}, the volume is {math(tex_f(volume))}.",
         value=volume,
         point_type_id="BC-PT-99004",
         rule="power rule",
      ),
   ]

   unsquared = Distractor(
      error_path="BC-ERR-08036",
      derivation="the radius left unsquared, pi times the integral of r",
      value=sympy.pi * integral_of(profile),
      mechanism="algebra_slip",
   )
   no_pi = Distractor(
      error_path="BC-ERR-08037",
      derivation="the factor of pi left off, the integral of r squared",
      value=radius_squared,
      mechanism="forgot_constant",
   )

   if is_shifted:
      third = Distractor(
         error_path="BC-ERR-08038",
         derivation=f"the radius measured from the x-axis, f(x), instead of from the line y = {level}",
         value=sympy.pi * integral_of(curve**2),
         mechanism="conceptual_confusion",
      )
   else:
      third = Distractor(
         error_path="BC-ERR-99011",
         derivation="the region revolved about the y-axis instead, by shells: 2 pi times the integral of x f(x)",
         value=2 * sympy.pi * integral_of(x * profile),
         mechanism="conceptual_confusion",
      )

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=volume),
      steps=steps,
      distractors=[unsquared, no_pi, third],
      representation=representation,
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
