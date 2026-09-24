"""BC-QA-06003, an accumulation function read from the graph of its integrand."""
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

ARCHETYPE_ID = "BC-QA-06003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "heights", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "lower", "type": "integer", "role": "safe", "domain": {"values": [0, 2, 4]}},
      {"name": "circle", "type": "label", "role": "safe", "domain": {"values": ["above", "below"]}},
      {"name": "half_point", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "3/2", "5/2", "7/2"]}},
      {"name": "letters", "type": "label", "role": "safe", "domain": {"values": ["fg", "fh", "hg"]}},
      {"name": "ask", "type": "label", "role": "difficulty", "domain": {"values": ["value", "chain"]}},
   ],
   "constraints": [
      "heights[3] != 0",
      "ask != 'value' or linear_total != 0",
      "ask != 'value' or circle == 'below' or min(vertices[lower / 2:]) < 0",
      "ask != 'chain' or distinct([chain_key, chain_key / 2, 2 * inner_value, inner_slope])",
   ],
   "derived": [
      {"name": "vertices", "expression": "heights + [0]"},
      {"name": "linear_total", "expression": "sum(vertices[lower / 2:4]) + sum(vertices[lower / 2 + 1:5])"},
      {"name": "upper_index", "expression": "half_point - 1 / 2"},
      {"name": "inner_index", "expression": "(half_point - 1 / 2) // 2"},
      {"name": "chain_key", "expression": "vertices[upper_index] + vertices[upper_index + 1]"},
      {"name": "inner_slope", "expression": "(vertices[inner_index + 1] - vertices[inner_index]) / 2"},
      {"name": "inner_value", "expression": "vertices[inner_index] + inner_slope * (half_point - 2 * inner_index)"},
   ],
   "invariants": [
      "exact(key)",
      "finite(key)",
   ],
   "dial_bindings": [
      {"parameter": "ask", "difficulty_factor_id": "BC-DF-04", "settings": {"value": "off", "chain": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["heights", "circle", "lower", "ask"]},
   ],
   "notes": (
      "Four line segments join (0, h0), (2, h1), (4, h2), (6, h3) and (8, 0); a semicircle of radius 2 centred at "
      "(10, 0) closes the graph on [8, 12]. The value ask evaluates g(12) = integral of f from lower to 12. The chain "
      "ask differentiates the integral of f from lower to 2x at x = half_point, so 2x sits at the midpoint of a segment."
   ),
}

t = sympy.Symbol("t")
RADIUS = 2
CENTRE = 10
SEGMENT_WIDTH = 2
RIGHT_END = 12


def _signed_piece(left, right):
   return sympy.Integer(left + right) * SEGMENT_WIDTH / 2


def _unsigned_piece(left, right):
   same_side = left * right >= 0

   if same_side:
      return sympy.Integer(abs(left) + abs(right)) * SEGMENT_WIDTH / 2

   return sympy.Rational(SEGMENT_WIDTH * (left * left + right * right), 2 * (abs(left) + abs(right)))


def _graph(vertices, circle_sign, circle_word, integrand_letter):
   segments = []

   for index in range(4):
      segments.append([[SEGMENT_WIDTH * index, vertices[index]], [SEGMENT_WIDTH * (index + 1), vertices[index + 1]]])

   semicircle = circle_sign * sympy.sqrt(RADIUS**2 - (t - CENTRE) ** 2)
   circle_segments = sample_curve(semicircle, t, CENTRE - RADIUS, CENTRE + RADIUS, samples=81)
   corner_text = ", ".join(f"({SEGMENT_WIDTH * index}, {vertices[index]})" for index in range(5))

   return figure(
      "function_graph",
      domain=(-0.5, 12.5),
      range_=(-4, 4),
      curves=[segments + circle_segments],
      marks=[point_mark(SEGMENT_WIDTH * index, vertices[index]) for index in range(5)] + [point_mark(RIGHT_END, 0)],
      labels=[label(f"y = {integrand_letter}(t)", 0.6, 3.6)],
      axis_titles=("t", "y"),
      alt=(
         f"Line segments through {corner_text}, then a semicircle of radius 2 centred at (10, 0) {circle_word} the "
         "t-axis ending at (12, 0)."
      ),
   )


def build(names):
   vertices = [int(value) for value in names["heights"]] + [0]
   lower = int(names["lower"])
   circle_word = names["circle"]
   circle_sign = 1 if circle_word == "above" else -1
   integrand_letter, accumulation_letter = list(names["letters"])
   graph = _graph(vertices, circle_sign, circle_word, integrand_letter)
   window_text = math(r"0 \le t \le 12")
   opening = (
      f"The graph of the continuous function {integrand_letter} shown consists of four line segments and a "
      f"semicircle, for {window_text}."
   )

   if names["ask"] == "value":
      return _value_item(names, vertices, lower, circle_sign, circle_word, integrand_letter, accumulation_letter, opening, graph)

   return _chain_item(names, vertices, lower, integrand_letter, accumulation_letter, opening, graph)


def _value_item(names, vertices, lower, circle_sign, circle_word, integrand_letter, accumulation_letter, opening, graph):
   first_piece = lower // SEGMENT_WIDTH
   pieces = [(vertices[index], vertices[index + 1]) for index in range(first_piece, 4)]
   linear_signed = sum((_signed_piece(left, right) for left, right in pieces), sympy.Integer(0))
   linear_unsigned = sum((_unsigned_piece(left, right) for left, right in pieces), sympy.Integer(0))
   half_disc = sympy.pi * RADIUS**2 / 2
   key_value = linear_signed + circle_sign * half_disc

   definition = math(rf"{accumulation_letter}(x) = \int_{{{lower}}}^{{x}} {integrand_letter}(t)\,dt")
   stem = f"{opening} Let {definition}. Find the exact value of {math(f'{accumulation_letter}(12)')}."

   half_disc_text = math(r"\tfrac{1}{2}\pi (2)^2 = 2\pi")
   piece_texts = ", ".join(tex(_signed_piece(left, right)) for left, right in pieces)
   steps = [
      Step(
         text=(
            f"{math(f'{accumulation_letter}(12)')} is the signed area between the graph of {integrand_letter} and the "
            f"t-axis from t = {lower} to t = 12."
         ),
         rule="accumulation function as signed area",
      ),
      Step(
         text=(
            f"From t = {lower} to t = 8 the graph is made of line segments, with signed areas {math(piece_texts)}, "
            f"totalling {math(tex(linear_signed))}."
         ),
         value=linear_signed,
         rule="area of a trapezoid, negative below the axis",
      ),
      Step(
         text=(
            f"On [8, 12] the semicircle has area {half_disc_text}, counted as "
            f"{math(tex(circle_sign * half_disc))} because it lies {circle_word} the axis."
         ),
         value=circle_sign * half_disc,
         rule="area of a semicircle",
      ),
      Step(
         text=f"So {math(f'{accumulation_letter}(12) = ' + tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99069",
         rule="additivity over adjacent intervals",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-06014",
         derivation="every piece counted as positive area, including those below the axis",
         value=linear_unsigned + half_disc,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06013",
         derivation="the semicircle given the area of the full circle, 4 pi",
         value=linear_signed + circle_sign * 2 * half_disc,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99012",
         derivation=f"the accumulation function evaluated as {integrand_letter}(12) - {integrand_letter}({lower}), the integrand read at the two limits",
         value=sympy.Integer(0 - vertices[first_piece]),
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


def _chain_item(names, vertices, lower, integrand_letter, accumulation_letter, opening, graph):
   point = names["half_point"]
   upper_index = int(names["upper_index"])
   inner_index = int(names["inner_index"])
   upper_input = 2 * point
   integrand_at_upper = sympy.Rational(vertices[upper_index] + vertices[upper_index + 1], 2)
   key_value = 2 * integrand_at_upper
   inner_slope = sympy.Rational(vertices[inner_index + 1] - vertices[inner_index], 2)
   inner_value = vertices[inner_index] + inner_slope * (point - SEGMENT_WIDTH * inner_index)

   definition = math(rf"{accumulation_letter}(x) = \int_{{{lower}}}^{{2x}} {integrand_letter}(t)\,dt")
   derivative_name = math(f"{accumulation_letter}'({tex(point)})")
   stem = f"{opening} Let {definition}. Find {derivative_name}."

   ftc_text = math(f"{accumulation_letter}'(x) = {integrand_letter}(2x)" + r" \cdot 2")
   factor_text = tex(integrand_at_upper)

   if integrand_at_upper < 0:
      factor_text = r"\left(" + factor_text + r"\right)"

   derivative_tex = f"{accumulation_letter}'({tex(point)})"
   product_text = math(derivative_tex + r" = 2 \cdot " + f"{factor_text} = {tex(key_value)}")
   steps = [
      Step(
         text=(
            f"By the Fundamental Theorem of Calculus and the chain rule, {ftc_text}, since the upper limit 2x has "
            "derivative 2."
         ),
         point_type_id="BC-PT-99024",
         rule="Fundamental Theorem of Calculus with a composite upper limit",
      ),
      Step(
         text=(
            f"At x = {point} the upper limit is t = {upper_input}, the midpoint of the segment from "
            f"({SEGMENT_WIDTH * upper_index}, {vertices[upper_index]}) to ({SEGMENT_WIDTH * (upper_index + 1)}, "
            f"{vertices[upper_index + 1]}), so {math(f'{integrand_letter}({upper_input}) = {tex(integrand_at_upper)}')}."
         ),
         value=integrand_at_upper,
         rule="value read from the graph",
      ),
      Step(
         text=f"So {product_text}.",
         value=key_value,
         rule="chain rule factor",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-06027",
         derivation=f"the integrand at the upper limit, {integrand_letter}({upper_input}), with the factor 2 from the chain rule left off",
         value=integrand_at_upper,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-06028",
         derivation=f"the integrand evaluated at x = {point} itself instead of at the upper limit 2x, then doubled",
         value=2 * inner_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-06008",
         derivation=f"the graph shown taken as the graph of {accumulation_letter}, so its slope at x = {point} is reported",
         value=inner_slope,
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
