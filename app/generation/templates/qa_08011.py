"""BC-QA-08011, the volume of a solid whose cross sections perpendicular to the x-axis are a named shape."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, figure, label, math, numeric_integral, sample_curve, segment_mark
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "shape", "type": "label", "role": "difficulty", "domain": {"values": ["square", "semicircle", "equilateral", "hypotenuse", "rectangle"]}},
      {"name": "tool", "type": "label", "role": "difficulty", "domain": {"values": ["by_hand", "technology"]}},
      {"name": "left", "type": "integer", "role": "safe", "domain": {"min": -1, "max": 1, "step": 1}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "bulge", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 2, "step": 1}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "intercept", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "height_ratio", "type": "integer", "role": "safe", "domain": {"values": [2, 3]}},
      {"name": "peak", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 4, "step": 1}},
      {"name": "spread", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "drop", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "3/2"]}},
      {"name": "reach", "type": "rational", "role": "safe", "domain": {"values": ["3/2", "2", "5/2"]}},
      {"name": "presentation", "type": "label", "role": "safe", "domain": {"values": ["figure", "formula"]}},
   ],
   "constraints": [
      "slope * (2 * left + width) + 2 * intercept != 0",
      "2 * cross_integral + lower_square_integral != 0",
   ],
   "derived": [
      {"name": "right", "expression": "left + width"},
      {"name": "cross_integral", "expression": "(slope * (2 * left + width) / 2 + intercept) * bulge * width**3 / 6"},
      {"name": "lower_square_integral", "expression": "slope**2 * (right**3 - left**3) / 3 + slope * intercept * (right**2 - left**2) + intercept**2 * width"},
   ],
   "invariants": [
      "finite(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "tool", "difficulty_factor_id": "BC-DF-07", "settings": {"by_hand": "off", "technology": "low"}},
      {"parameter": "shape", "difficulty_factor_id": "BC-DF-17", "settings": {"square": "off", "semicircle": "off", "equilateral": "off", "hypotenuse": "off", "rectangle": "off"}},
   ],
   "calculator_guard": "exact(key) or tool == 'technology'",
   "representation_bindings": [
      {"representation": "BC-REP-08", "figure_kind": "region", "requires": ["shape", "tool"]},
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["shape", "tool"]},
      {"representation": "BC-REP-09", "figure_kind": None, "requires": ["shape", "tool", "peak", "spread", "drop", "reach"]},
   ],
   "notes": "By hand, the base lies between the parabola g + bulge (x - left)(right - x) and the line g, which meet at x = left and x = right; the line's value at the midpoint is nonzero, so the difference of squares differs from the square of the difference, and the integral of f squared differs from both. With technology, the base lies between peak e^(-x^2 / spread) and the line y = -drop x from x = 0 to x = reach, whose squared gap has no elementary antiderivative. The shape changes only the constant of the area formula, and the archetype has no dial for it, so its binding leaves BC-DF-17 off.",
}

SHAPES = {
   "square": ("squares", sympy.Integer(1), r"s^{2}", "a square with side s has area s^2"),
   "semicircle": ("semicircles whose diameters lie in the base", sympy.pi / 8, r"\frac{\pi}{8}s^{2}", "a semicircle with diameter s has radius s/2 and area (1/2) pi (s/2)^2"),
   "equilateral": ("equilateral triangles", sympy.sqrt(3) / 4, r"\frac{\sqrt{3}}{4}s^{2}", "an equilateral triangle with side s has area (sqrt(3)/4) s^2"),
   "hypotenuse": ("isosceles right triangles whose hypotenuses lie in the base", sympy.Rational(1, 4), r"\frac{1}{4}s^{2}", "an isosceles right triangle with hypotenuse s has legs s/sqrt(2) and area s^2/4"),
   "rectangle": ("rectangles whose heights are {ratio} times their bases", None, r"{ratio}s^{{2}}", "a rectangle with base s and height {ratio}s has area {ratio}s^2"),
}

LENGTH_NAMES = {"square": "side", "semicircle": "diameter", "equilateral": "side", "hypotenuse": "hypotenuse", "rectangle": "base"}

x = sympy.Symbol("x")


def _region_figure(upper, lower, left, right, is_technology):
   low_x = left - sympy.Rational(1, 2)
   high_x = right + sympy.Rational(1, 2)
   probes = [left + (right - left) * sympy.Rational(index, 12) for index in range(13)]
   values = [upper.subs(x, point) for point in probes] + [lower.subs(x, point) for point in probes]
   top = sympy.ceiling(max(values)) + 1
   bottom = sympy.floor(min(min(values), 0)) - 1

   outline = []

   for index in range(41):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      outline.append([float(x_value), float(upper.subs(x, x_value))])

   for index in range(40, -1, -1):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      outline.append([float(x_value), float(lower.subs(x, x_value))])

   middle = sympy.Rational(1, 2) * (left + right)
   marks = []

   if is_technology:
      marks = [segment_mark((right, lower.subs(x, right)), (right, upper.subs(x, right)))]

   return figure(
      "region",
      domain=(low_x, high_x),
      range_=(bottom, top),
      curves=[sample_curve(upper, x, low_x, high_x, y_limit=float(max(abs(top), abs(bottom)))), sample_curve(lower, x, low_x, high_x)],
      marks=marks,
      labels=[
         label("y = f(x)", middle, min(float(upper.subs(x, middle)) + 0.5, float(top) - 0.3)),
         label("y = g(x)", middle, max(float(lower.subs(x, middle)) - 0.5, float(bottom) + 0.3)),
      ],
      fills=[outline],
      alt=f"The base region lies between the graph of y = f(x) above and y = g(x) below, from x = {left} to x = {right}.",
   )


def build(names):
   shape = names["shape"]
   is_technology = names["tool"] == "technology"
   is_figure = names["presentation"] == "figure"
   ratio = names["height_ratio"]
   plural, coefficient, area_tex, area_reason = SHAPES[shape]

   if shape == "rectangle":
      plural = plural.format(ratio=ratio)
      coefficient = sympy.Integer(ratio)
      area_tex = area_tex.format(ratio=ratio)
      area_reason = area_reason.format(ratio=ratio)

   if is_technology:
      left = sympy.Integer(0)
      right = names["reach"]
      upper = names["peak"] * sympy.exp(-x**2 / names["spread"])
      lower = -names["drop"] * x
      boundary = f"the graphs of f and g and the vertical lines {math('x = 0')} and {math(f'x = {tex_f(right)}')}"
   else:
      left = names["left"]
      right = names["right"]
      lower = names["slope"] * x + names["intercept"]
      upper = sympy.expand(lower + names["bulge"] * (x - left) * (right - x))
      boundary = "the graphs of f and g"

   gap = upper - lower

   if is_technology:
      gap_squared = numeric_integral(gap**2, x, left, right)
      upper_squared = numeric_integral(upper**2, x, left, right)
      lower_squared = numeric_integral(lower**2, x, left, right)
      base_area = numeric_integral(gap, x, left, right)
   else:
      gap_squared = sympy.integrate(sympy.expand(gap**2), (x, left, right))
      upper_squared = sympy.integrate(sympy.expand(upper**2), (x, left, right))
      lower_squared = sympy.integrate(sympy.expand(lower**2), (x, left, right))
      base_area = sympy.integrate(sympy.expand(gap), (x, left, right))

   squares_differ = upper_squared - lower_squared
   volume = coefficient * gap_squared

   functions = f"{math('f(x) = ' + tex_f(upper))} and {math('g(x) = ' + tex_f(lower))}"
   solid = f"cross sections perpendicular to the x-axis are {plural}"

   if is_figure:
      region_text = f"The region R shown is bounded by {boundary}."
      graph = _region_figure(upper, lower, left, right, is_technology)
   else:
      region_text = f"Let R be the region bounded by {boundary}."
      graph = None

   if is_technology:
      stem = (
         f"Let {functions}. {region_text} R is the base of a solid whose {solid}. Using a calculator, find the volume "
         "of the solid. Show the setup for the calculation, and give the value correct to three decimal places."
      )
      representation = "BC-REP-08" if is_figure else "BC-REP-09"
      calculator_status = "calculator"
   else:
      stem = f"Let {functions}. {region_text} R is the base of a solid whose {solid}. Find the exact volume of the solid."
      representation = "BC-REP-08" if is_figure else "BC-REP-01"
      calculator_status = "no_calculator"

   if is_technology and not is_figure:
      representation = "BC-REP-09"

   integral = rf"\int_{{{tex_f(left)}}}^{{{tex_f(right)}}} {tex_f(coefficient)}\left({tex_f(gap)}\right)^{{2}}\,dx"

   if is_technology:
      value_text = f"which a calculator gives as about {decimal_text(volume)}"
   else:
      value_text = f"which equals {math(tex_f(volume))}"

   steps = [
      Step(
         text=f"The {LENGTH_NAMES[shape]} of each cross section is the vertical distance across R, {math('s = f(x) - g(x) = ' + tex_f(gap))}.",
         rule="distance between the boundary curves",
      ),
      Step(
         text=f"Because {area_reason}, each cross section has area {math(area_tex)}.",
         rule="area of the named shape",
      ),
      Step(
         text=f"The volume is {math(integral)}, {value_text}.",
         value=volume,
         point_type_id="BC-PT-99001",
         rule="volume by cross sections",
      ),
   ]

   if shape == "square":
      distractors = [
         Distractor("BC-ERR-08029", "a factor of pi placed in front of the square's area", sympy.pi * gap_squared, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08030", "the side squared as f(x)^2 - g(x)^2 instead of (f(x) - g(x))^2", squares_differ, mechanism="algebra_slip"),
         Distractor("BC-ERR-08028", "the side taken as the value of f alone", upper_squared, mechanism="conceptual_confusion"),
      ]
   elif shape == "semicircle":
      distractors = [
         Distractor("BC-ERR-08034", "the distance s used as the radius, area (1/2) pi s^2", sympy.pi / 2 * gap_squared, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-06013", "the full circle with diameter s used, area pi s^2 / 4", sympy.pi / 4 * gap_squared, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08030", "the diameter squared as f(x)^2 - g(x)^2 instead of (f(x) - g(x))^2", sympy.pi / 8 * squares_differ, mechanism="algebra_slip"),
      ]
   elif shape == "equilateral":
      distractors = [
         Distractor("BC-ERR-08032", "the triangle's area written as (1/2) s^2, with the side used as the height", gap_squared / 2, mechanism="algebra_slip"),
         Distractor("BC-ERR-08029", "a factor of pi placed in the triangle's area", sympy.pi * sympy.sqrt(3) / 4 * gap_squared, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08030", "the side squared as f(x)^2 - g(x)^2 instead of (f(x) - g(x))^2", sympy.sqrt(3) / 4 * squares_differ, mechanism="algebra_slip"),
      ]
   elif shape == "hypotenuse":
      distractors = [
         Distractor("BC-ERR-08033", "the distance s used as a leg, area s^2 / 2", gap_squared / 2, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08032", "the constant of the area formula dropped, area s^2", gap_squared, mechanism="algebra_slip"),
         Distractor("BC-ERR-08030", "the hypotenuse squared as f(x)^2 - g(x)^2 instead of (f(x) - g(x))^2", squares_differ / 4, mechanism="algebra_slip"),
      ]
   else:
      distractors = [
         Distractor("BC-ERR-08031", f"the height {ratio}s left out, so only the base s is integrated", base_area, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08029", "a factor of pi placed in front of the rectangle's area", sympy.pi * ratio * gap_squared, mechanism="conceptual_confusion"),
         Distractor("BC-ERR-08030", "the base squared as f(x)^2 - g(x)^2 instead of (f(x) - g(x))^2", ratio * squares_differ, mechanism="algebra_slip"),
      ]

   if is_technology:
      key = Key(form="numeric", value=sympy.N(volume, 20), decimals=3)

      for distractor in distractors:
         distractor.value = sympy.N(distractor.value, 20)
   else:
      key = Key(form="symbolic", value=volume)

   return Instance(
      stem=stem,
      key=key,
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status=calculator_status,
      figure=graph,
      setup_required=is_technology,
      command_verb="find",
   )
