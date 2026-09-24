"""BC-QA-08010, the total area between a parabola and a line that cross twice inside the stated interval."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, sample_curve, segment_mark
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 1, "step": 1}},
      {"name": "lead", "type": "rational", "role": "safe", "domain": {"values": ["1", "3/2", "2"]}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 4, "step": 1}},
      {"name": "overrun", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1"]}},
      {"name": "bulge", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "intercept", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "presentation", "type": "label", "role": "difficulty", "domain": {"values": ["graph", "formula"]}},
   ],
   "constraints": [
      "gap**3 / 6 > overrun**3 / 3 + gap * overrun**2 / 2",
   ],
   "derived": [
      {"name": "first_cross", "expression": "start + lead"},
      {"name": "second_cross", "expression": "start + lead + gap"},
      {"name": "finish", "expression": "start + lead + gap + overrun"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "presentation", "difficulty_factor_id": "BC-DF-17", "settings": {"graph": "low", "formula": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["start", "lead", "gap", "overrun", "bulge", "slope", "intercept"]},
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["start", "lead", "gap", "overrun", "bulge", "slope", "intercept"]},
   ],
   "notes": "f - g = bulge (x - first_cross)(x - second_cross), so on [start, finish] the parabola is above, below, then above the line. The middle piece outweighs the last one (the constraint compares the monic areas), which keeps the missed-crossing distractor apart from the one-integral distractor.",
}

x = sympy.Symbol("x")


def _graph(upper, lower, start, finish, first_cross, second_cross):
   low_x = start - sympy.Rational(1, 2)
   high_x = finish + sympy.Rational(1, 2)
   probes = [start + (finish - start) * sympy.Rational(index, 12) for index in range(13)] + [low_x, high_x]
   values = [upper.subs(x, point) for point in probes] + [lower.subs(x, point) for point in probes]
   top = max(values) + 2
   bottom = min(values) - 2

   def band(low, high):
      points = []

      for index in range(21):
         x_value = low + (high - low) * sympy.Rational(index, 20)
         points.append([float(x_value), float(upper.subs(x, x_value))])

      for index in range(20, -1, -1):
         x_value = low + (high - low) * sympy.Rational(index, 20)
         points.append([float(x_value), float(lower.subs(x, x_value))])

      return points

   middle = sympy.Rational(first_cross + second_cross, 2)
   parabola_label_y = min(upper.subs(x, low_x + sympy.Rational(1, 4)) + 1, top - sympy.Rational(1, 2))
   line_label_y = max(min(lower.subs(x, middle) + 1, top - sympy.Rational(1, 2)), bottom + sympy.Rational(1, 2))

   return figure(
      "function_graph",
      domain=(low_x, high_x),
      range_=(bottom, top),
      curves=[sample_curve(upper, x, low_x, high_x), sample_curve(lower, x, low_x, high_x)],
      marks=[
         segment_mark((start, bottom), (start, top), style="dashed"),
         segment_mark((finish, bottom), (finish, top), style="dashed"),
      ],
      labels=[
         label("y = f(x)", low_x + sympy.Rational(1, 4), max(parabola_label_y, bottom + sympy.Rational(1, 2))),
         label("y = g(x)", middle, line_label_y),
      ],
      fills=[band(start, first_cross), band(first_cross, second_cross), band(second_cross, finish)],
      alt=(
         f"The graphs of y = f(x), a parabola opening upward, and y = g(x), a line, crossing at x = {first_cross} and "
         f"x = {second_cross}. The regions between them are shaded from x = {start} to x = {finish}, with f above g "
         "on the outer pieces and below g on the middle piece."
      ),
   )


def build(names):
   start = names["start"]
   finish = names["finish"]
   first_cross = names["first_cross"]
   second_cross = names["second_cross"]
   bulge = names["bulge"]
   is_graph = names["presentation"] == "graph"

   lower = names["slope"] * x + names["intercept"]
   difference = sympy.expand(bulge * (x - first_cross) * (x - second_cross))
   upper = sympy.expand(lower + difference)
   antiderivative = sympy.integrate(difference, x)

   def signed(low, high):
      return antiderivative.subs(x, high) - antiderivative.subs(x, low)

   first_piece = signed(start, first_cross)
   middle_piece = signed(first_cross, second_cross)
   last_piece = signed(second_cross, finish)
   total = first_piece - middle_piece + last_piece
   one_integral = first_piece + middle_piece + last_piece
   missed_crossing = first_piece + abs(middle_piece + last_piece)

   functions = f"{math('f(x) = ' + tex_f(upper))} and {math('g(x) = ' + tex_f(lower))}"
   interval = f"{math(f'x = {tex_f(start)}')} to {math(f'x = {tex_f(finish)}')}"

   if is_graph:
      stem = (
         f"Let {functions}. Find the exact total area of the shaded regions shown, which lie between the graphs of "
         f"f and g from {interval}."
      )
      graph = _graph(upper, lower, start, finish, first_cross, second_cross)
      representation = "BC-REP-02"
   else:
      stem = f"Let {functions}. Find the exact total area of the regions between the graphs of f and g from {interval}."
      graph = None
      representation = "BC-REP-01"

   factored = tex_f(bulge * sympy.Mul(x - first_cross, x - second_cross, evaluate=False))

   def piece(low, high, order, value):
      integral = rf"\int_{{{tex_f(low)}}}^{{{tex_f(high)}}} \left({order}\right)\,dx = {tex_f(value)}"

      return math(integral)

   steps = [
      Step(
         text=(
            f"{math('f(x) - g(x) = ' + factored)}, so the graphs cross at {math(f'x = {tex_f(first_cross)}')} and "
            f"{math(f'x = {tex_f(second_cross)}')}, both inside the interval. f is above g before the first crossing "
            "and after the second, and below g between them."
         ),
         rule="intersections and order of the curves",
      ),
      Step(
         text=(
            f"The pieces are {piece(start, first_cross, 'f(x) - g(x)', first_piece)}, "
            f"{piece(first_cross, second_cross, 'g(x) - f(x)', -middle_piece)} and "
            f"{piece(second_cross, finish, 'f(x) - g(x)', last_piece)}."
         ),
         value=-middle_piece,
         rule="area of each piece, upper minus lower",
      ),
      Step(
         text=f"The total area is the sum of the pieces, {math(tex_f(total))}.",
         value=total,
         rule="additivity of area",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-08026",
         derivation="f(x) - g(x) integrated once over the whole interval, across both crossings",
         value=one_integral,
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-08025",
         derivation=f"the crossing at x = {second_cross} missed, so the second integral runs from {first_cross} to {finish} across it",
         value=missed_crossing,
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-08020",
         derivation="the curves split correctly but each piece integrated as lower minus upper",
         value=-total,
         mechanism="reversed_quantities",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=total),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
