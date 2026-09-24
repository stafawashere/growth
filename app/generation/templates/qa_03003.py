"""BC-QA-03003, the derivative of a composite read from the graphs of its two pieces."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark, tex

ARCHETYPE_ID = "BC-QA-03003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "outer_heights", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "inner_heights", "type": "integer", "role": "safe", "count": 4, "domain": {"min": 0, "max": 6, "step": 1}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"values": [1, 3, 5]}},
      {"name": "names", "type": "label", "role": "safe", "domain": {"values": ["f,g", "p,q", "u,v"]}},
   ],
   "constraints": [
      "inner in [1, 3, 5]",
      "inner != at",
      "inner_slope != 0",
      "outer_slope != 0",
      "distinct([outer_slope * inner_slope, wrong_slope * inner_slope, outer_slope, outer_slope + inner_slope])",
   ],
   "derived": [
      {"name": "piece", "expression": "(at - 1) // 2"},
      {"name": "inner", "expression": "(inner_heights[piece] + inner_heights[piece + 1]) / 2"},
      {"name": "inner_slope", "expression": "(inner_heights[piece + 1] - inner_heights[piece]) / 2"},
      {"name": "outer_piece", "expression": "(inner - 1) // 2"},
      {"name": "outer_slope", "expression": "(outer_heights[outer_piece + 1] - outer_heights[outer_piece]) / 2"},
      {"name": "wrong_slope", "expression": "(outer_heights[piece + 1] - outer_heights[piece]) / 2"},
   ],
   "invariants": [
      "exact(key)",
      "key == outer_slope * inner_slope",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["outer_heights", "inner_heights", "at"]},
   ],
   "notes": (
      "Both graphs are polygonal with corners only at x = 0, 2, 4, 6. The input is odd, so it sits in the middle "
      "of a piece of the inner graph, and the inner output is an odd whole number, so it sits in the middle of a "
      "piece of the outer graph and both slopes exist."
   ),
}

CORNERS = [0, 2, 4, 6]


def _paren(value):
   text = tex(value)

   return rf"\left({text}\right)" if value < 0 else text


def _polyline(heights):
   return [[[CORNERS[index], heights[index]], [CORNERS[index + 1], heights[index + 1]]] for index in range(3)]


def _vertex_text(heights):
   return ", ".join(f"({corner}, {height})" for corner, height in zip(CORNERS, heights))


def build(names):
   outer_heights = [int(value) for value in names["outer_heights"]]
   inner_heights = [int(value) for value in names["inner_heights"]]
   at = int(names["at"])
   outer_name, inner_name = names["names"].split(",")

   piece = (at - 1) // 2
   inner = (inner_heights[piece] + inner_heights[piece + 1]) // 2
   inner_slope = sympy.Rational(inner_heights[piece + 1] - inner_heights[piece], 2)
   outer_piece = (inner - 1) // 2
   outer_slope = sympy.Rational(outer_heights[outer_piece + 1] - outer_heights[outer_piece], 2)
   wrong_slope = sympy.Rational(outer_heights[piece + 1] - outer_heights[piece], 2)
   key_value = outer_slope * inner_slope

   outer_label_y = outer_heights[0] + 0.6 if outer_heights[0] < 4 else outer_heights[0] - 0.6
   inner_label_y = inner_heights[3] + 0.6 if inner_heights[3] < 6 else inner_heights[3] - 0.6
   marks = [point_mark(corner, height) for corner, height in zip(CORNERS, outer_heights)]
   marks += [point_mark(corner, height) for corner, height in zip(CORNERS, inner_heights)]
   graph = figure(
      "function_graph",
      domain=(-0.5, 7.5),
      range_=(-5, 7.5),
      curves=[_polyline(outer_heights), _polyline(inner_heights)],
      marks=marks,
      labels=[
         label(f"y = {outer_name}(x)", 0.1, outer_label_y),
         label(f"y = {inner_name}(x)", 6.1, inner_label_y),
      ],
      alt=(
         f"Two polygonal graphs on 0 to 6. The graph of {outer_name} joins {_vertex_text(outer_heights)} with "
         f"line segments; the graph of {inner_name} joins {_vertex_text(inner_heights)} with line segments."
      ),
   )

   composite = f"h(x) = {outer_name}({inner_name}(x))"
   stem = (
      f"The graphs of the functions {outer_name} and {inner_name} shown each consist of three line segments on "
      f"{math(r'0 \le x \le 6')}. Let {math(composite)}. Find the exact value of {math(f"h'({at})")}."
   )

   steps = [
      Step(
         text=(
            f"By the chain rule, {math(f"h'({at}) = {outer_name}'({inner_name}({at})) \\cdot {inner_name}'({at})")}. "
            f"From the graph, {math(f'{inner_name}({at}) = {inner}')}, and the segment of {inner_name} through "
            f"x = {at} has slope {math(f"{inner_name}'({at}) = {tex(inner_slope)}")}."
         ),
         rule="read the inner value and slope",
      ),
      Step(
         text=(
            f"The outer slope is read at the inner output x = {inner}, not at x = {at}: the segment of "
            f"{outer_name} there has slope {math(f"{outer_name}'({inner}) = {tex(outer_slope)}")}."
         ),
         rule="read the outer slope at the inner output",
      ),
      Step(
         text=f"So {math(f"h'({at}) = {_paren(outer_slope)} \\cdot {_paren(inner_slope)} = {tex(key_value)}")}.",
         value=key_value,
         rule="chain rule",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03003",
         derivation=f"the slope of {outer_name} read at x = {at} instead of at the inner output x = {inner}",
         value=wrong_slope * inner_slope,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-03001",
         derivation=f"the outer slope at the inner output reported alone, the factor {inner_name}'({at}) omitted",
         value=outer_slope,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03004",
         derivation="the two slopes added instead of multiplied",
         value=outer_slope + inner_slope,
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-02",
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
