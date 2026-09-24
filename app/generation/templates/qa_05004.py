"""BC-QA-05004, intervals of concavity read from the graph of the derivative, with a reason."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark
from app.generation.templates._helpers_c import intervals_text, label_spot, merge_touching, midpoint, pieces

ARCHETYPE_ID = "BC-QA-05004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SEGMENTS = 6

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "heights", "type": "integer", "role": "safe", "count": 7, "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "asked", "type": "label", "role": "safe", "domain": {"values": ["down", "up"]}},
   ],
   "constraints": [
      "all([heights[0] != heights[1], heights[1] != heights[2], heights[2] != heights[3], heights[3] != heights[4], heights[4] != heights[5], heights[5] != heights[6]])",
      "(asked == 'down' and falls_above and has_rise) or (asked == 'up' and rises_below and has_fall)",
   ],
   "derived": [
      {"name": "falls_above", "expression": "(heights[0] > heights[1] and heights[1] > 0) or (heights[1] > heights[2] and heights[2] > 0) or (heights[2] > heights[3] and heights[3] > 0) or (heights[3] > heights[4] and heights[4] > 0) or (heights[4] > heights[5] and heights[5] > 0) or (heights[5] > heights[6] and heights[6] > 0)"},
      {"name": "rises_below", "expression": "(heights[0] < heights[1] and heights[1] < 0) or (heights[1] < heights[2] and heights[2] < 0) or (heights[2] < heights[3] and heights[3] < 0) or (heights[3] < heights[4] and heights[4] < 0) or (heights[4] < heights[5] and heights[5] < 0) or (heights[5] < heights[6] and heights[6] < 0)"},
      {"name": "has_rise", "expression": "any([heights[0] < heights[1], heights[1] < heights[2], heights[2] < heights[3], heights[3] < heights[4], heights[4] < heights[5], heights[5] < heights[6]])"},
      {"name": "has_fall", "expression": "any([heights[0] > heights[1], heights[1] > heights[2], heights[2] > heights[3], heights[3] > heights[4], heights[4] > heights[5], heights[5] > heights[6]])"},
   ],
   "invariants": [
      "has_rise or has_fall",
   ],
   "dial_bindings": [],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["heights", "asked"]},
   ],
   "notes": "The graph of f' is six line segments joining integer points on 0 <= x <= 6 with no horizontal segment. A segment that falls while above the axis (for concave down) or rises while below it (for concave up) guarantees that reading concavity from the sign of f' gives a different answer.",
}


def _value_at(heights, point):
   index = min(int(sympy.floor(point)), SEGMENTS - 1)
   fraction = point - index

   return heights[index] + (heights[index + 1] - heights[index]) * fraction


def _zeros(heights):
   zeros = []

   for index in range(SEGMENTS):
      left, right = heights[index], heights[index + 1]

      if left == 0:
         zeros.append(sympy.Integer(index))

      crosses = left * right < 0

      if crosses:
         zeros.append(index + sympy.Rational(left, left - right))

   return zeros


def _statement(concavity, intervals, reason):
   if not intervals:
      return f"The graph of f is concave {concavity} on no open interval in {math('0 < x < 6')}, because {reason} nowhere there."

   return f"The graph of f is concave {concavity} exactly on {intervals_text(intervals)}, because {reason} there."


def build(names):
   heights = [int(value) for value in names["heights"]]
   concave_down = names["asked"] == "down"
   concavity = names["asked"]
   monotone_word = "decreasing" if concave_down else "increasing"
   sign_word = "negative" if concave_down else "positive"

   def wanted(left, right):
      return right < left if concave_down else right > left

   key_segments = [(sympy.Integer(index), sympy.Integer(index + 1)) for index in range(SEGMENTS) if wanted(heights[index], heights[index + 1])]
   other_segments = [(sympy.Integer(index), sympy.Integer(index + 1)) for index in range(SEGMENTS) if not wanted(heights[index], heights[index + 1])]
   key_intervals = merge_touching(key_segments)
   misread_intervals = merge_touching(sorted(key_segments + [other_segments[0]]))

   sign_intervals = []

   for piece in pieces(_zeros(heights), 0, SEGMENTS):
      value = _value_at(heights, midpoint(piece))
      has_sign = value < 0 if concave_down else value > 0

      if has_sign:
         sign_intervals.append(piece)

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
      f"The graph of f', the derivative of a function f, is shown for {math(r'0 \le x \le 6')} and consists of six "
      f"line segments. On what open intervals in {math('0 < x < 6')} is the graph of f concave {concavity}? Give a reason for "
      "the answer."
   )

   steps = [
      Step(
         text=f"The graph of f is concave {concavity} exactly where f' is {monotone_word}, that is, where the given graph {'falls' if concave_down else 'rises'} from left to right.",
         point_type_id="BC-PT-99063",
         rule="concavity from the monotonicity of the derivative",
      ),
      Step(
         text=f"Reading the segments, f' is {monotone_word} on {intervals_text(key_intervals)}, so the graph of f is concave {concavity} on {intervals_text(key_intervals)}.",
         point_type_id="BC-PT-99062",
         rule="read the intervals from the graph",
      ),
   ]

   flipped = other_segments[0]
   dropped = key_segments[-1]
   dropped_intervals = merge_touching(key_segments[:-1])

   for candidate in reversed(key_segments):
      remaining = merge_touching([segment for segment in key_segments if segment != candidate])
      differs = remaining != sign_intervals

      if differs:
         dropped = candidate
         dropped_intervals = remaining
         break

   distractors = [
      Distractor(
         error_path="BC-ERR-05031",
         derivation=f"concavity read from where the plotted derivative is {sign_word} rather than where it is {monotone_word}",
         label=_statement(concavity, sign_intervals, f"f' is {sign_word}"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-05030",
         derivation=f"the sign of f'' misread on ({flipped[0]}, {flipped[1]}), so that interval is wrongly included",
         label=_statement(concavity, misread_intervals, f"f' is {monotone_word}"),
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-05030",
         derivation=f"the sign of f'' misread on ({dropped[0]}, {dropped[1]}), so that interval is wrongly left out",
         label=_statement(concavity, dropped_intervals, f"f' is {monotone_word}"),
         mechanism="sign_error",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_statement(concavity, key_intervals, f"f' is {monotone_word}")),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-02",
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
