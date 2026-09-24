"""BC-QA-08013, the volume of a solid of revolution by washers, about the x-axis or a horizontal line below or above the region."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, sample_curve, segment_mark
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "left", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 2, "step": 1}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "bulge", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": -1, "max": 1, "step": 1}},
      {"name": "intercept", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "depth", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "presentation", "type": "label", "role": "safe", "domain": {"values": ["figure", "formula"]}},
      {"name": "axis", "type": "label", "role": "difficulty", "domain": {"values": ["x_axis", "below", "above"]}},
   ],
   "constraints": [
      "intercept + slope * left > 0",
      "intercept + slope * right > 0",
   ],
   "derived": [
      {"name": "right", "expression": "left + width"},
      {"name": "level", "expression": "0 if axis == 'x_axis' else (-depth if axis == 'below' else intercept + abs(slope) * right + (bulge * width**2) // 4 + depth)"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "axis", "difficulty_factor_id": "BC-DF-01", "settings": {"x_axis": "off", "below": "low", "above": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-08", "figure_kind": "region", "requires": ["left", "width", "bulge", "slope", "intercept", "axis"]},
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["left", "width", "bulge", "slope", "intercept", "axis"]},
   ],
   "notes": "The lower boundary is the line g, positive on the interval, and the upper boundary is g + bulge (x - left)(right - x), so they meet at x = left and x = right and the region sits above the x-axis. The axis is the x-axis, the line y = -depth below the region, or a line above the region's highest point (the level bounds the parabola's peak from above), so the region never touches it and every slice is a washer.",
}

x = sympy.Symbol("x")


def _region_figure(upper, lower, level, left, right):
   low_x = left - 1
   high_x = right + 1
   probes = [left + (right - left) * sympy.Rational(index, 12) for index in range(13)]
   highest = max(upper.subs(x, point) for point in probes)
   top = sympy.ceiling(max(highest, level)) + 1
   bottom = sympy.floor(min(level, 0)) - 1

   outline = []

   for index in range(41):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      outline.append([float(x_value), float(upper.subs(x, x_value))])

   for index in range(40, -1, -1):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      outline.append([float(x_value), float(lower.subs(x, x_value))])

   middle = sympy.Rational(left + right, 2)
   window_limit = float(max(abs(top), abs(bottom)))

   return figure(
      "region",
      domain=(low_x, high_x),
      range_=(bottom, top),
      curves=[sample_curve(upper, x, low_x, high_x, y_limit=window_limit), sample_curve(lower, x, low_x, high_x, y_limit=window_limit)],
      marks=[segment_mark((low_x, level), (high_x, level), style="dashed")],
      labels=[
         label("y = f(x)", middle, min(float(top) - 0.4, float(upper.subs(x, middle)) + 0.4)),
         label("y = g(x)", high_x - sympy.Rational(1, 2), max(float(bottom) + 0.4, min(float(top) - 0.4, float(lower.subs(x, high_x - sympy.Rational(1, 2))) + 0.5))),
         label(f"y = {level}", low_x + sympy.Rational(1, 2), float(level) + 0.3),
      ],
      fills=[outline],
      alt=(
         f"The region between y = f(x) above and y = g(x) below, from x = {left} to x = {right}, where the graphs meet, "
         f"with the line y = {level} drawn dashed as the axis of revolution."
      ),
   )


def build(names):
   left = names["left"]
   right = names["right"]
   level = names["level"]
   axis = names["axis"]
   is_figure = names["presentation"] == "figure"

   lower = names["slope"] * x + names["intercept"]
   upper = sympy.expand(lower + names["bulge"] * (x - left) * (right - x))

   if axis == "above":
      outer = level - lower
      inner = level - upper
   else:
      outer = upper - level
      inner = lower - level

   def integral_of(expression):
      return sympy.integrate(sympy.expand(expression), (x, left, right))

   difference_of_squares = integral_of(outer**2 - inner**2)
   volume = sympy.pi * difference_of_squares

   if axis == "x_axis":
      axis_text = "the x-axis"
   else:
      axis_text = f"the line {math(f'y = {level}')}"

   functions = f"{math('f(x) = ' + tex_f(upper))} and {math('g(x) = ' + tex_f(lower))}"

   if is_figure:
      region_sentence = "The region R shown is bounded by the graphs of f and g."
      graph = _region_figure(upper, lower, level, left, right)
      representation = "BC-REP-08"
   else:
      region_sentence = "Let R be the region bounded by the graphs of f and g."
      graph = None
      representation = "BC-REP-01"

   stem = (
      f"Let {functions}. {region_sentence} Find the exact volume of the solid generated when R is revolved about "
      f"{axis_text}."
   )

   if axis == "above":
      order_text = f"The axis lies above R, so g is farther from it: the outer radius is {math(f'R = {level} - g(x) = {tex_f(outer)}')} and the inner radius is {math(f'r = {level} - f(x) = {tex_f(sympy.expand(inner))}')}."
   elif axis == "below":
      order_text = f"The axis lies below R, so f is farther from it: the outer radius is {math(f'R = f(x) - ({level}) = {tex_f(sympy.expand(outer))}')} and the inner radius is {math(f'r = g(x) - ({level}) = {tex_f(inner)}')}."
   else:
      order_text = f"The axis is the x-axis, below R, so the outer radius is {math(f'R = f(x) = {tex_f(outer)}')} and the inner radius is {math(f'r = g(x) = {tex_f(inner)}')}."

   meet_text = f"The graphs meet where {math(f'f(x) - g(x) = ' + tex_f(sympy.expand(upper - lower)) + ' = 0')}, at {math(f'x = {left}')} and {math(f'x = {right}')}."
   integral = rf"\pi\int_{{{left}}}^{{{right}}} \left(R^{{2}} - r^{{2}}\right)\,dx"
   steps = [
      Step(text=f"{meet_text} {order_text}", point_type_id="BC-PT-99058", rule="washer radii"),
      Step(
         text=f"The volume is {math(integral)}, and {math(rf'\int_{{{left}}}^{{{right}}} \left(R^{{2}} - r^{{2}}\right)\,dx = {tex_f(difference_of_squares)}')}, so the volume is {math(tex_f(volume))}.",
         value=volume,
         point_type_id="BC-PT-99001",
         rule="washer method",
      ),
   ]

   square_of_difference = Distractor(
      error_path="BC-ERR-08030",
      derivation="the square of the difference of the radii, (R - r)^2, used in place of R^2 - r^2",
      value=sympy.pi * integral_of((outer - inner) ** 2),
      mechanism="algebra_slip",
   )
   exchanged = Distractor(
      error_path="BC-ERR-08040",
      derivation="the radii exchanged, r^2 - R^2" if axis != "above" else "the radii assigned by which curve is higher, (level - f)^2 - (level - g)^2",
      value=-volume,
      mechanism="reversed_quantities",
   )

   if axis == "x_axis":
      third = Distractor(
         error_path="BC-ERR-08037",
         derivation="the factor of pi left off",
         value=difference_of_squares,
         mechanism="forgot_constant",
      )
   else:
      third = Distractor(
         error_path="BC-ERR-08038",
         derivation=f"both radii measured from the x-axis, f(x) and g(x), instead of from the line y = {level}",
         value=sympy.pi * integral_of(upper**2 - lower**2),
         mechanism="conceptual_confusion",
      )

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=volume),
      steps=steps,
      distractors=[square_of_difference, exchanged, third],
      representation=representation,
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
