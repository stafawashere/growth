"""BC-QA-05005, the points of inflection of f read from the graph of f', with a reason tied to that graph."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark
from app.generation.templates._helpers_c import label_spot, points_text

ARCHETYPE_ID = "BC-QA-05005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SEGMENTS = 6

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "heights", "type": "integer", "role": "safe", "count": 7, "domain": {"min": -3, "max": 3, "step": 1}},
   ],
   "constraints": [
      "all([slopes[0] != 0, slopes[1] != 0, slopes[2] != 0, slopes[3] != 0, slopes[4] != 0, slopes[5] != 0])",
      "any([slopes[0] * slopes[1] < 0, slopes[1] * slopes[2] < 0, slopes[2] * slopes[3] < 0, slopes[3] * slopes[4] < 0, slopes[4] * slopes[5] < 0])",
      "any([slopes[0] * slopes[1] > 0 and slopes[0] != slopes[1], slopes[1] * slopes[2] > 0 and slopes[1] != slopes[2], slopes[2] * slopes[3] > 0 and slopes[2] != slopes[3], slopes[3] * slopes[4] > 0 and slopes[3] != slopes[4], slopes[4] * slopes[5] > 0 and slopes[4] != slopes[5]])",
      "any([heights[0] * heights[1] < 0, heights[1] * heights[2] < 0, heights[2] * heights[3] < 0, heights[3] * heights[4] < 0, heights[4] * heights[5] < 0, heights[5] * heights[6] < 0])",
   ],
   "derived": [
      {"name": "slopes", "expression": "differences(heights)"},
   ],
   "invariants": [
      "len(slopes) == 6",
   ],
   "dial_bindings": [],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["heights"]},
   ],
   "notes": "The graph of f' is six non-horizontal line segments on 0 <= x <= 6. It has a corner where f' switches between increasing and decreasing (the answer), a corner where only the steepness changes, and a crossing of the axis strictly inside a segment, so listing corners or zeros of f' gives a different, wrong list.",
}


def _zeros(heights):
   zeros = []

   for index in range(SEGMENTS):
      left, right = heights[index], heights[index + 1]
      is_interior_vertex = left == 0 and index > 0

      if is_interior_vertex:
         zeros.append(sympy.Integer(index))

      crosses = left * right < 0

      if crosses:
         zeros.append(index + sympy.Rational(left, left - right))

   return zeros


def _statement(points, reason):
   if not points:
      return f"The graph of f has no point of inflection in {math('0 < x < 6')}, because {reason} at no value there."

   if len(points) == 1:
      return f"The graph of f has exactly one point of inflection, at {points_text(points)}, because {reason} there."

   return f"The graph of f has points of inflection exactly at {points_text(points)}, because {reason} at each of these values."


def build(names):
   heights = [int(value) for value in names["heights"]]
   slopes = [heights[index + 1] - heights[index] for index in range(SEGMENTS)]
   turning = [sympy.Integer(index) for index in range(1, SEGMENTS) if slopes[index - 1] * slopes[index] < 0]
   corners = [sympy.Integer(index) for index in range(1, SEGMENTS) if slopes[index - 1] != slopes[index]]
   zeros = _zeros(heights)

   vertices = [[index, heights[index]] for index in range(SEGMENTS + 1)]
   graph = figure(
      "function_graph",
      domain=(-0.5, 6.5),
      range_=(-4, 4),
      curves=[[[vertices[index], vertices[index + 1]] for index in range(SEGMENTS)]],
      marks=[point_mark(index, heights[index]) for index in range(SEGMENTS + 1)],
      labels=[label("y = f'(x)", *label_spot(heights))],
      alt=(
         "The graph of f' is made of line segments joining "
         + ", ".join(f"({index}, {heights[index]})" for index in range(SEGMENTS + 1))
         + "."
      ),
   )

   stem = (
      f"The graph of f', the derivative of a function f, is shown for {math(r'0 \le x \le 6')} and consists of six line "
      f"segments. Find all values of x in the open interval {math('0 < x < 6')} at which the graph of f has a point of "
      "inflection. Give a reason for the answer."
   )

   change_reason = "f' changes between increasing and decreasing"
   steps = [
      Step(
         text=(
            "The graph of f changes concavity exactly where f' changes between increasing and decreasing, which on this "
            "graph happens at a corner where a rising segment meets a falling one."
         ),
         point_type_id="BC-PT-99061",
         rule="inflection where the derivative changes monotonicity",
      ),
      Step(
         text=f"Those corners are at {points_text(turning)}, so the graph of f has a point of inflection there and nowhere else in {math('0 < x < 6')}.",
         point_type_id="BC-PT-99060",
         rule="read the corners from the graph",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05033",
         derivation="every zero of the plotted curve f' listed as a point of inflection, with no change in concavity checked",
         label=_statement(zeros, "f' is equal to 0"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99023",
         derivation="every corner of the graph of f' listed, including one where f' keeps rising or keeps falling and only its steepness changes",
         label=_statement(corners, "the slope of the graph of f' changes"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99023",
         derivation=f"the corner at x = {turning[-1]}, where f' changes between increasing and decreasing, omitted from the list",
         label=_statement(turning[:-1], change_reason),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_statement(turning, change_reason)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-02",
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
