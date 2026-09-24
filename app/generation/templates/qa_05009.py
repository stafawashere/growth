"""BC-QA-05009, three graphs matched to a function and its first two derivatives."""
import math as pymath

import sympy

from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, sample_curve

ARCHETYPE_ID = "BC-QA-05009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "first_root", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 1, "step": 1}},
      {"name": "root_gap", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4, 5, 6]}},
      {"name": "steepness", "type": "rational", "role": "safe", "domain": {"values": ["1/3", "1/2", "2/3", "1"]}},
      {"name": "orientation", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "lift", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 2, "step": 1}},
      {"name": "lettering", "type": "label", "role": "safe", "domain": {"values": ["ABC", "ACB", "BAC", "BCA", "CAB", "CBA"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["derivatives", "antiderivatives"]}},
   ],
   "constraints": [],
   "derived": [
      {"name": "second_root", "expression": "first_root + root_gap"},
   ],
   "invariants": [
      "second_root - first_root >= 2",
   ],
   "dial_bindings": [
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-13", "settings": {"derivatives": "off", "antiderivatives": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["first_root", "root_gap", "steepness", "orientation", "lettering"]},
   ],
   "notes": (
      "The top function is a cubic whose derivative, a quadratic, has zeros at first_root and second_root; the second "
      "derivative is a line through the midpoint. All three are drawn on one set of axes and lettered by the lettering "
      "permutation. The antiderivative framing names the line g and asks for its antiderivatives, which reverses the "
      "direction of the reasoning."
   ),
}

x = sympy.Symbol("x")
EDGE = sympy.Rational(3, 2)
ROLE_COUNT = 3
ANTIDERIVATIVE_LINKS = ("G' = g", "K' = G")


def _functions(names):
   first_root = names["first_root"]
   second_root = names["second_root"]
   scale = names["orientation"] * names["steepness"]
   first = scale * (x - first_root) * (x - second_root)
   top = sympy.integrate(first, x)
   centre = sympy.Rational(first_root + second_root, 2)
   top = sympy.expand(top - top.subs(x, centre) + names["lift"])
   second = sympy.diff(first, x)

   return [top, first, second]


def _window(curves):
   largest = 0.0

   for segments in curves:
      for segment in segments:
         for point in segment:
            largest = max(largest, abs(point[1]))

   return pymath.ceil(largest) + 1


def _value_at(function, x_value):
   return function(x_value)


def _label_spot(index, evaluators, placed, low, high, height):
   """A point on curve index that is as far as possible from the other two curves and from
   labels already placed, so each letter plainly names one curve."""
   best = None
   steps = 40

   for position in range(1, steps):
      x_value = low + 0.4 + (high - low - 0.8) * position / steps
      own = _value_at(evaluators[index], x_value)
      others = [_value_at(evaluators[other], x_value) for other in range(ROLE_COUNT) if other != index]
      clearance = min(abs(own - value) for value in others)
      crowded = any(abs(x_value - spot[0]) < 1.2 for spot in placed)
      fits = abs(own) + 0.9 < height

      if crowded or not fits:
         continue

      if best is None or clearance > best[0]:
         nearest = min(others, key=lambda value: abs(own - value))
         offset = 0.5 if own >= nearest else -0.5
         best = (clearance, x_value, own + offset)

   if best is None:
      return (low + 0.5 + index, 0.0)

   return (best[1], best[2])


def _point_text(expression, x_value):
   return f"({x_value}, {expression.subs(x, x_value)})"


def _feature_text(expression, kind):
   turning_points = sorted(sympy.solve(sympy.diff(expression, x), x))
   zeros = sorted(root for root in sympy.solve(expression, x) if root.is_real)

   if kind == "line":
      slope = sympy.diff(expression, x)
      return f"a line of slope {slope} crossing the x-axis at x = {zeros[0]}"

   if kind == "parabola":
      return (
         f"a parabola crossing the x-axis at x = {zeros[0]} and x = {zeros[1]} with its vertex at "
         f"{_point_text(expression, turning_points[0])}"
      )

   turning_text = " and ".join(_point_text(expression, point) for point in turning_points)

   return f"a cubic curve with horizontal tangents at {turning_text}"


def _assignment_clause(letters, role_names):
   pairs = sorted(zip(letters, role_names))
   parts = [f"curve {letter} is the graph of {math(name)}" for letter, name in pairs]

   return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def _assignment_label(letters, role_names):
   clause = _assignment_clause(letters, role_names)

   return clause[0].upper() + clause[1:] + "."


def build(names):
   first_root = names["first_root"]
   second_root = names["second_root"]
   letters = list(names["lettering"])
   functions = _functions(names)
   low = first_root - EDGE
   high = second_root + EDGE

   curves = [sample_curve(function, x, low, high, samples=121) for function in functions]
   height = _window(curves)
   evaluators = [sympy.lambdify(x, function, modules="math") for function in functions]
   placed = []

   for index in range(ROLE_COUNT):
      placed.append(_label_spot(index, evaluators, placed, float(low), float(high), height))

   kinds = ["cubic", "parabola", "line"]
   features = [_feature_text(functions[index], kinds[index]) for index in range(ROLE_COUNT)]
   alt = "Three curves on one set of axes: " + "; ".join(
      f"curve {letters[index]} is {features[index]}" for index in range(ROLE_COUNT)
   ) + "."

   graph = figure(
      "function_graph",
      domain=(low, high),
      range_=(-height, height),
      curves=curves,
      labels=[label(letters[index], placed[index][0], placed[index][1]) for index in range(ROLE_COUNT)],
      alt=alt,
   )

   if names["framing"] == "antiderivatives":
      role_names = ["K", "G", "g"]
      stem = (
         "The three curves A, B and C shown are the graphs of a function g, an antiderivative G of g, and an "
         f"antiderivative K of G, so that {math(ANTIDERIVATIVE_LINKS[0])} and {math(ANTIDERIVATIVE_LINKS[1])}. Identify which curve is the graph "
         "of each function."
      )
   else:
      role_names = ["f", "f'", "f''"]
      stem = (
         "The three curves A, B and C shown are the graphs of a function f and its derivatives f' and f''. Identify "
         "which curve is the graph of each function."
      )

   top_letter, first_letter, second_letter = letters
   centre = sympy.Rational(first_root + second_root, 2)
   steps = [
      Step(
         text=(
            f"Curve {top_letter} has horizontal tangents at x = {first_root} and x = {second_root}, and curve "
            f"{first_letter} crosses the x-axis at exactly those inputs, changing sign there. So curve {first_letter} "
            f"is the derivative of curve {top_letter}."
         ),
         rule="zeros of a derivative sit at the turning points of the function",
      ),
      Step(
         text=(
            f"Curve {first_letter} has its only turning point at x = {centre}, where curve {second_letter} crosses "
            f"the x-axis. So curve {second_letter} is the derivative of curve {first_letter}."
         ),
         rule="zeros of a derivative sit at the turning points of the function",
      ),
      Step(
         text=f"The chain runs {top_letter}, then {first_letter}, then {second_letter}, so {_assignment_clause(letters, role_names)}.",
         rule="order of differentiation",
      ),
   ]

   reversed_letters = [second_letter, first_letter, top_letter]
   inflection_letters = [top_letter, second_letter, first_letter]
   turning_letters = [first_letter, top_letter, second_letter]

   distractors = [
      Distractor(
         error_path="BC-ERR-05046",
         derivation="the three curves ordered in the reverse derivative direction, so the line is taken as the top function and the cubic as the bottom one",
         label=_assignment_label(reversed_letters, role_names),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-05043",
         derivation="the inflection point of the cubic paired with a zero of the next derivative, so the line is taken as the first derivative and the parabola as the second",
         label=_assignment_label(inflection_letters, role_names),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-05041",
         derivation="the derivative taken to have its turning points at the zeros of the function, so the cubic, whose turning points sit at the parabola's zeros, is called the derivative of the parabola",
         label=_assignment_label(turning_letters, role_names),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_assignment_label(letters, role_names)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-02",
      calculator_status="no_calculator",
      figure=graph,
      command_verb="identify",
   )
