"""BC-QA-08009, the area of a region found by integrating with respect to y after rewriting both curves."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark, sample_curve
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-08009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "height", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "run", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "3/2", "2", "5/2", "3", "7/2", "4", "5", "6"]}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 0, "step": 1}},
      {"name": "letters", "type": "label", "role": "safe", "domain": {"values": ["fg", "hk", "pq"]}},
      {"name": "presentation", "type": "label", "role": "difficulty", "domain": {"values": ["graph", "formula"]}},
   ],
   "constraints": [
      "run < stretch * height",
      "stretch * height**2 <= 30",
      "x_limits_value != area_value",
      "x_limits_value != -area_value",
   ],
   "derived": [
      {"name": "offset", "expression": "stretch * height**2 - run * height"},
      {"name": "corner", "expression": "stretch * height**2 + shift"},
      {"name": "area_value", "expression": "run * height**2 / 2 + offset * height - stretch * height**3 / 3"},
      {"name": "x_limits_value", "expression": "run * (corner**2 - shift**2) / 2 + offset * (corner - shift) - stretch * (corner**3 - shift**3) / 3"},
   ],
   "invariants": [
      "exact(key)",
      "key > 0",
   ],
   "dial_bindings": [
      {"parameter": "presentation", "difficulty_factor_id": "BC-DF-14", "settings": {"graph": "off", "formula": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["stretch", "height", "run", "shift"]},
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["stretch", "height", "run", "shift"]},
   ],
   "notes": "The curves are x = stretch y^2 + shift (given as the upper half y = sqrt((x - shift)/stretch)) and x = run y + offset + shift (given as a line in x), meeting at y = height; with the x-axis they bound a region whose left edge is the parabola and right edge the line for 0 <= y <= height, which in x would need two integrals. The shift is at most 0 so the integrand in x stays real on the y-interval, which the dy-with-an-x-integrand distractor needs.",
}

LETTERS = {"fg": ("f", "g"), "hk": ("h", "k"), "pq": ("p", "q")}

x = sympy.Symbol("x")
y = sympy.Symbol("y")


def _graph(root_curve, line_curve, stretch, height, shift, offset, run, names_pair):
   corner_x = stretch * height**2 + shift
   low_x = min(shift, 0) - 1
   high_x = corner_x + 2
   top = height + 2
   bottom = -2
   line_low = shift + offset - 2 * run
   line_start = max(low_x, line_low)

   region = []

   for index in range(41):
      y_value = height * sympy.Rational(index, 40)
      region.append([float(stretch * y_value**2 + shift), float(y_value)])

   for index in range(40, -1, -1):
      y_value = height * sympy.Rational(index, 40)
      region.append([float(run * y_value + offset + shift), float(y_value)])

   root_label_x = shift + sympy.Rational(1, 2)
   root_label_y = sympy.sqrt(sympy.Rational(1, 2) / stretch) + sympy.Rational(3, 4)
   line_label_x = min(corner_x + 1, high_x - sympy.Rational(1, 2))
   line_label_y = sympy.Rational(1, 2) + (line_label_x - shift - offset) / run - 1

   return figure(
      "function_graph",
      domain=(low_x, high_x),
      range_=(bottom, top),
      curves=[
         sample_curve(root_curve, x, shift, high_x),
         sample_curve(line_curve, x, line_start, high_x, y_limit=top),
      ],
      marks=[point_mark(corner_x, height), point_mark(shift + offset, 0)],
      labels=[
         label(f"y = {names_pair[0]}(x)", root_label_x, min(root_label_y, top - sympy.Rational(1, 2))),
         label(f"y = {names_pair[1]}(x)", line_label_x, max(min(line_label_y, top - sympy.Rational(1, 2)), bottom + sympy.Rational(1, 2))),
      ],
      fills=[region],
      alt=(
         f"The graph of y = {names_pair[0]}(x), the upper half of a parabola opening to the right from ({shift}, 0), and "
         f"the line y = {names_pair[1]}(x) crossing the x-axis at ({shift + offset}, 0). The shaded region lies above "
         f"the x-axis, to the right of the parabola and to the left of the line, up to the point ({corner_x}, {height}) "
         "where they meet."
      ),
   )


def build(names):
   stretch = names["stretch"]
   height = names["height"]
   run = names["run"]
   shift = names["shift"]
   offset = names["offset"]
   is_graph = names["presentation"] == "graph"
   first_name, second_name = LETTERS[names["letters"]]

   root_curve = sympy.sqrt((x - shift) / stretch)
   line_curve = (x - shift - offset) / run
   left_edge = stretch * y**2 + shift
   right_edge = run * y + offset + shift
   width = sympy.expand(right_edge - left_edge)
   width_antiderivative = sympy.integrate(width, y)
   area = width_antiderivative.subs(y, height) - width_antiderivative.subs(y, 0)

   corner_x = stretch * height**2 + shift
   low_corner_x = shift
   x_limits_value = width_antiderivative.subs(y, corner_x) - width_antiderivative.subs(y, low_corner_x)
   t = sympy.Symbol("t", nonnegative=True)
   unrewritten = sympy.integrate(root_curve.subs(x, t) - line_curve.subs(x, t), (t, 0, height))
   unrewritten = sympy.simplify(unrewritten)

   if stretch == 1:
      root_tex = rf"\sqrt{{{tex_f(x - shift)}}}"
   else:
      root_tex = rf"\sqrt{{\frac{{{tex_f(x - shift)}}}{{{stretch}}}}}"

   functions = (
      f"{math(f'{first_name}(x) = ' + root_tex)} and {math(f'{second_name}(x) = ' + tex_f(line_curve))}"
   )

   if is_graph:
      stem = (
         f"Let {functions}. The shaded region R shown is bounded by the graphs of {first_name} and {second_name} "
         "and the x-axis. By integrating with respect to y, find the exact area of R."
      )
      graph = _graph(root_curve, line_curve, stretch, height, shift, offset, run, (first_name, second_name))
      representation = "BC-REP-02"
   else:
      stem = (
         f"Let {functions}. Let R be the region bounded by the graphs of {first_name} and {second_name} and the x-axis. "
         "By integrating with respect to y, find the exact area of R."
      )
      graph = None
      representation = "BC-REP-01"

   integral = rf"\int_{{0}}^{{{height}}} \left(\left({tex_f(right_edge)}\right) - \left({tex_f(left_edge)}\right)\right)\,dy"
   steps = [
      Step(
         text=(
            f"Solve each equation for x: {math('x = ' + tex_f(left_edge))} from the graph of {first_name}, with "
            f"{math(r'y \ge 0')}, and {math('x = ' + tex_f(right_edge))} from the graph of {second_name}."
         ),
         rule="rewrite each curve as a function of y",
      ),
      Step(
         text=(
            f"The curves meet where {math(f'{tex_f(left_edge)} = {tex_f(right_edge)}')}, at {math(f'y = {height}')}, "
            f"and the region runs from the x-axis, {math('y = 0')}, up to there. On that interval the line is to the "
            "right of the parabola."
         ),
         rule="limits in y and the right-hand curve",
      ),
      Step(text=f"The area is {math(integral + ' = ' + tex_f(area))}.", value=area, rule="area integral in y"),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-08020",
         derivation="the parabola's x taken minus the line's x, left minus right",
         value=-area,
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-08024",
         derivation=f"the correct integrand in y integrated between the x-coordinates of the region's ends, {low_corner_x} and {corner_x}",
         value=x_limits_value,
         mechanism="wrong_limits",
      ),
      Distractor(
         error_path="BC-ERR-08023",
         derivation=f"{first_name}(x) - {second_name}(x) integrated as written over the y-interval from 0 to {height}, without rewriting the curves in y",
         value=unrewritten,
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
