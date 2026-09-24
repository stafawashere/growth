"""BC-QA-06004, a definite integral evaluated from a graph by geometry."""
import sympy

from app.generation.kit import (
   Distractor,
   Instance,
   Key,
   Step,
   figure,
   label,
   math,
   point_mark,
   sample_curve,
   tex,
)

ARCHETYPE_ID = "BC-QA-06004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "heights", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "lower", "type": "integer", "role": "safe", "domain": {"values": [0, 1, 2]}},
      {"name": "circle", "type": "label", "role": "difficulty", "domain": {"values": ["above", "below"]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["forward", "reversed"]}},
   ],
   "constraints": [
      "linear_area != 0",
      "min(heights[lower:]) < 0 or circle == 'below'",
      "heights[3] != 0",
   ],
   "derived": [
      {"name": "linear_area", "expression": "(2 * sum(heights[lower:]) - heights[lower]) / 2"},
   ],
   "invariants": [
      "exact(key)",
      "finite(key)",
   ],
   "dial_bindings": [
      {"parameter": "circle", "difficulty_factor_id": "BC-DF-01", "settings": {"above": "low", "below": "medium"}},
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-13", "settings": {"forward": "off", "reversed": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["heights", "circle"]},
   ],
   "notes": "Four line segments join (0, h0), (1, h1), (2, h2), (3, h3) and (4, 0); a semicircle of radius 2 centred at (6, 0) closes the graph on [4, 8], above or below the axis.",
}

x = sympy.Symbol("x")
RADIUS = 2
CENTRE = 6


def _signed_piece(left, right):
   return sympy.Rational(left + right, 2)


def _unsigned_piece(left, right):
   same_side = left * right >= 0

   if same_side:
      return sympy.Rational(abs(left) + abs(right), 2)

   return sympy.Rational(left * left + right * right, 2 * (abs(left) + abs(right)))


def build(names):
   heights = [int(value) for value in names["heights"]]
   lower = int(names["lower"])
   vertices = heights + [0]
   circle_sign = 1 if names["circle"] == "above" else -1
   is_reversed = names["direction"] == "reversed"
   orientation = -1 if is_reversed else 1

   pieces = [(vertices[index], vertices[index + 1]) for index in range(lower, 4)]
   linear_signed = sum((_signed_piece(left, right) for left, right in pieces), sympy.Integer(0))
   linear_unsigned = sum((_unsigned_piece(left, right) for left, right in pieces), sympy.Integer(0))
   half_disc = sympy.pi * RADIUS**2 / 2
   key_value = orientation * (linear_signed + circle_sign * half_disc)

   limits = rf"\int_{{8}}^{{{lower}}}" if is_reversed else rf"\int_{{{lower}}}^{{8}}"
   stem = (
      "The graph of the continuous function f shown consists of four line segments and a semicircle, "
      f"for {math(r'0 \le x \le 8')}. Find {math(limits + r' f(x)\,dx')}."
   )

   segments = []

   for index in range(4):
      segments.append([[index, vertices[index]], [index + 1, vertices[index + 1]]])

   semicircle = circle_sign * sympy.sqrt(RADIUS**2 - (x - CENTRE) ** 2)
   circle_segments = sample_curve(semicircle, x, CENTRE - RADIUS, CENTRE + RADIUS, samples=81)
   graph = figure(
      "function_graph",
      domain=(-0.5, 8.5),
      range_=(-4, 4),
      curves=[segments + circle_segments],
      marks=[point_mark(index, vertices[index]) for index in range(5)] + [point_mark(8, 0)],
      labels=[label("y = f(x)", 0.4, 3.6)],
      alt=(
         f"Line segments through (0, {vertices[0]}), (1, {vertices[1]}), (2, {vertices[2]}), "
         f"(3, {vertices[3]}) and (4, 0), then a semicircle of radius 2 centred at (6, 0) "
         f"{names['circle']} the x-axis ending at (8, 0)."
      ),
   )

   piece_texts = ", ".join(tex(_signed_piece(left, right)) for left, right in pieces)
   steps = [
      Step(
         text=(
            f"Between x = {lower} and x = 4 the graph is made of line segments, so each unit strip is a "
            f"trapezoid or a pair of triangles with signed area {math(piece_texts)}, totalling "
            f"{math(tex(linear_signed))}."
         ),
         value=linear_signed,
         rule="area of a trapezoid, negative below the axis",
      ),
      Step(
         text=(
            f"On [4, 8] the semicircle has radius 2, so its area is {math(r'\tfrac{1}{2}\pi (2)^2 = 2\pi')}, "
            f"counted as {math(tex(circle_sign * half_disc))} because it lies {names['circle']} the axis."
         ),
         value=circle_sign * half_disc,
         rule="area of a semicircle",
      ),
      Step(
         text=(
            f"Adding the signed pieces gives {math(rf'\int_{{{lower}}}^{{8}} f(x)\,dx = ' + tex(linear_signed + circle_sign * half_disc))}."
         ),
         value=linear_signed + circle_sign * half_disc,
         point_type_id="BC-PT-99069",
         rule="additivity over adjacent intervals",
      ),
   ]

   if is_reversed:
      steps.append(Step(
         text=f"Reversing the limits changes the sign, so the value is {math(tex(key_value))}.",
         value=key_value,
         rule="reversed limits",
      ))

   distractors = [
      Distractor(
         error_path="BC-ERR-06014",
         derivation="every piece counted as positive area, including those below the axis",
         value=orientation * (linear_unsigned + half_disc),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06013",
         derivation="the semicircle given the area of the full circle, 4 pi",
         value=orientation * (linear_signed + circle_sign * 2 * half_disc),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99012",
         derivation="the integral of f read as f evaluated at the upper limit minus f at the lower limit",
         value=orientation * (0 - vertices[lower]),
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
