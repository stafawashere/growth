"""BC-QA-08008, the area of a region between a parabola and a line, integrated in x."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, sample_curve, segment_mark
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "left", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "bulge", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1, "exclude": [0]}},
      {"name": "intercept", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "lift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "presentation", "type": "label", "role": "safe", "domain": {"values": ["graph", "formula"]}},
      {"name": "limits", "type": "label", "role": "difficulty", "domain": {"values": ["stated", "intersections"]}},
   ],
   "constraints": [
      "lower_value != 0",
      "lower_value != 2 * intercept * width",
      "area_value + intercept * width != 0",
      "2 * area_value + lower_value != 0",
   ],
   "derived": [
      {"name": "right", "expression": "left + width"},
      {"name": "area_value", "expression": "bulge * width**3 / 6 + (lift if limits == 'stated' else 0) * width"},
      {"name": "lower_value", "expression": "slope * width * (2 * left + width) / 2 + intercept * width"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "limits", "difficulty_factor_id": "BC-DF-14", "settings": {"stated": "off", "intersections": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["left", "width", "bulge", "slope", "intercept", "limits"]},
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["left", "width", "bulge", "slope", "intercept", "limits"]},
   ],
   "notes": "The upper curve is the line plus bulge times (x - left)(right - x), raised by lift when the limits are stated vertical lines, so the curves meet exactly at x = left and x = right in the intersections case and never meet on the interval in the stated case. The line has a nonzero slope and intercept so the lost-parentheses distractor moves, and the constraints keep the three distractors apart from the key and from each other.",
}

x = sympy.Symbol("x")


def _graph(upper, lower, left, right, is_stated):
   low_x = left - 1
   high_x = right + 1
   samples = [upper.subs(x, left + (right - left) * sympy.Rational(index, 8)) for index in range(9)]
   samples += [lower.subs(x, low_x), lower.subs(x, high_x), upper.subs(x, low_x), upper.subs(x, high_x)]
   top = max(samples) + 2
   bottom = min(min(samples), 0) - 2
   upper_segments = sample_curve(upper, x, low_x, high_x, y_limit=None)
   lower_segments = sample_curve(lower, x, low_x, high_x)
   clipped_upper = [[point for point in segment if bottom <= point[1] <= top] for segment in upper_segments]
   clipped_upper = [segment for segment in clipped_upper if len(segment) > 1]

   region = []

   for index in range(41):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      region.append([float(x_value), float(upper.subs(x, x_value))])

   for index in range(40, -1, -1):
      x_value = left + (right - left) * sympy.Rational(index, 40)
      region.append([float(x_value), float(lower.subs(x, x_value))])

   middle = sympy.Rational(left + right, 2)
   upper_label_y = min(upper.subs(x, middle) + 1, top - sympy.Rational(1, 2))
   lower_label_y = max(lower.subs(x, high_x - sympy.Rational(1, 2)) - 1, bottom + sympy.Rational(1, 2))
   marks = []

   if is_stated:
      marks = [
         segment_mark((left, bottom), (left, top), style="dashed"),
         segment_mark((right, bottom), (right, top), style="dashed"),
      ]

   return figure(
      "function_graph",
      domain=(low_x, high_x),
      range_=(bottom, top),
      curves=[clipped_upper, lower_segments],
      marks=marks,
      labels=[
         label("y = f(x)", middle, upper_label_y),
         label("y = g(x)", high_x - sympy.Rational(1, 2), lower_label_y),
      ],
      fills=[region],
      alt=(
         f"The graphs of y = f(x), a parabola opening downward, and y = g(x), a line, with the region between "
         f"them shaded from x = {left} to x = {right}, where f lies above g."
      ),
   )


def build(names):
   left = names["left"]
   right = names["right"]
   width = names["width"]
   bulge = names["bulge"]
   slope = names["slope"]
   intercept = names["intercept"]
   is_stated = names["limits"] == "stated"
   is_graph = names["presentation"] == "graph"
   lift = names["lift"] if is_stated else 0

   lower = slope * x + intercept
   gap = bulge * (x - left) * (right - x) + lift
   upper = sympy.expand(lower + gap)
   gap_antiderivative = sympy.integrate(sympy.expand(gap), x)
   area = gap_antiderivative.subs(x, right) - gap_antiderivative.subs(x, left)
   lower_area = sympy.integrate(lower, (x, left, right))

   functions = f"{math('f(x) = ' + tex_f(upper))} and {math('g(x) = ' + tex_f(lower))}"

   if is_stated:
      boundary = f"the graphs of f and g and the vertical lines {math(f'x = {left}')} and {math(f'x = {right}')}"
   else:
      boundary = "the graphs of f and g"

   if is_graph:
      stem = (
         f"Let {functions}. The shaded region R shown is bounded by {boundary}. Find the exact area of R."
      )
      graph = _graph(upper, lower, left, right, is_stated)
      representation = "BC-REP-02"
   else:
      stem = f"Let {functions}. Let R be the region bounded by {boundary}. Find the exact area of R."
      graph = None
      representation = "BC-REP-01"

   if is_stated:
      limits_text = (
         f"On {math(f'[{left}, {right}]')}, {math('f(x) - g(x) = ' + tex_f(sympy.expand(gap)))}, which is positive, "
         "so f is the upper curve and the limits are the given vertical lines."
      )
   else:
      limits_text = (
         f"Setting {math('f(x) = g(x)')} gives {math(tex_f(sympy.expand(gap)) + ' = 0')}, so the curves meet at "
         f"{math(f'x = {left}')} and {math(f'x = {right}')}, and f is above g between them."
      )

   integral = rf"\int_{{{left}}}^{{{right}}} \left({tex_f(sympy.expand(gap))}\right)\,dx"
   steps = [
      Step(text=limits_text, point_type_id="BC-PT-99059", rule="upper minus lower"),
      Step(text=f"The area is {math(integral)}.", point_type_id="BC-PT-99001", rule="area between curves"),
      Step(
         text=f"An antiderivative of the integrand is {math(tex_f(gap_antiderivative))}.",
         point_type_id="BC-PT-99003",
         rule="power rule",
      ),
      Step(
         text=f"Evaluating from {math(str(left))} to {math(str(right))}, the area is {math(tex_f(area))}.",
         value=area,
         point_type_id="BC-PT-99004",
         rule="Fundamental Theorem of Calculus",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-08020",
         derivation="the integrand written as g(x) - f(x), lower minus upper",
         value=-area,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-99009",
         derivation="g substituted into f(x) - g(x) without parentheses, so the constant term of g is added instead of subtracted",
         value=area + 2 * intercept * width,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99011",
         derivation="the area under the upper curve alone, the integral of f from the left limit to the right limit",
         value=area + lower_area,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=area),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
