"""BC-QA-09011, the point on a polar curve farthest from a coordinate axis, calculator active."""
import math as pymath

import sympy

from app.generation.kit import (
   Distractor,
   Instance,
   Key,
   Step,
   decimal_text,
   figure,
   label,
   math,
   numeric_roots,
   point_mark,
   sample_polar,
   tex,
)

ARCHETYPE_ID = "BC-QA-09011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "amplitude", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 8, "step": 1}},
      {"name": "start", "type": "real", "role": "safe", "domain": {"values": [0, 0.1, 0.15, 0.2, 0.25, 0.3]}},
      {"name": "end", "type": "real", "role": "safe", "domain": {"values": [1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2, 2.05, 2.1]}},
      {"name": "axis", "type": "label", "role": "safe", "domain": {"values": ["y-axis", "x-axis"]}},
      {"name": "presentation", "type": "label", "role": "difficulty", "domain": {"values": ["equation", "graph"]}},
   ],
   "constraints": [
      "amplitude < constant",
      "constant <= 2 * amplitude",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "low_angle < key < high_angle",
      "critical_count == 1",
   ],
   "dial_bindings": [
      {"parameter": "presentation", "difficulty_factor_id": "BC-DF-03", "settings": {"equation": "off", "graph": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-13", "figure_kind": None, "requires": ["constant", "amplitude", "start", "end", "axis"]},
      {"representation": "BC-REP-02", "figure_kind": "polar_curve", "requires": ["constant", "amplitude", "start", "end", "axis"]},
   ],
   "notes": "For the y-axis the curve is r = c + a sin(theta) on [start, end]; for the x-axis it is r = c - a cos(theta) on [start + 1.6, end + 1.6]. With a < c <= 2a the one critical angle of the coordinate lies inside the interval, the radius is largest at an interior angle that differs from it, and the coordinate changes sign before the upper end.",
}

theta = sympy.Symbol("theta")
AXIS_SHIFT = sympy.Rational(8, 5)


def _angle_text(value):
   return f"{float(value):g}"


def build(names):
   constant = names["constant"]
   amplitude = names["amplitude"]
   is_y_axis = names["axis"] == "y-axis"
   has_graph = names["presentation"] == "graph"

   if is_y_axis:
      radius = constant + amplitude * sympy.sin(theta)
      coordinate = radius * sympy.cos(theta)
      low_angle = sympy.nsimplify(names["start"])
      high_angle = sympy.nsimplify(names["end"])
      radius_peak = sympy.pi / 2
      letter = "x"
   else:
      radius = constant - amplitude * sympy.cos(theta)
      coordinate = radius * sympy.sin(theta)
      low_angle = sympy.nsimplify(names["start"]) + AXIS_SHIFT
      high_angle = sympy.nsimplify(names["end"]) + AXIS_SHIFT
      radius_peak = sympy.pi
      letter = "y"

   coordinate_rate = sympy.diff(coordinate, theta)
   critical_angles = numeric_roots(coordinate_rate, theta, low_angle, high_angle)
   critical_angle = critical_angles[0]

   def distance_at(angle):
      return abs(sympy.N(coordinate.subs(theta, angle), 30))

   candidates = [(low_angle, distance_at(low_angle)), (critical_angle, distance_at(critical_angle)), (high_angle, distance_at(high_angle))]
   farthest_angle = max(candidates, key=lambda pair: pair[1])[0]
   nearest_angle = min(candidates, key=lambda pair: pair[1])[0]
   endpoint_pairs = [candidates[0], candidates[2]]
   farther_endpoint = max(endpoint_pairs, key=lambda pair: pair[1])[0]

   curve_tex = "r = " + tex(radius)
   window_tex = rf"{_angle_text(low_angle)} \le \theta \le {_angle_text(high_angle)}"

   if has_graph:
      opening = f"The graph of the polar curve {math(curve_tex)} for {math(window_tex)} is shown."
      samples = sample_polar(radius, theta, low_angle, high_angle)
      xs = [point[0] for point in samples[0]]
      ys = [point[1] for point in samples[0]]
      x_window = (pymath.floor(min(min(xs), 0)) - 1, pymath.ceil(max(max(xs), 0)) + 1)
      y_window = (pymath.floor(min(min(ys), 0)) - 1, pymath.ceil(max(max(ys), 0)) + 1)
      graph = figure(
         "polar_curve",
         domain=x_window,
         range_=y_window,
         curves=[samples],
         marks=[point_mark(0, 0)],
         labels=[label("O", 0, 0)],
         alt=(
            f"The polar curve r = {constant} {'+' if is_y_axis else '-'} {amplitude} "
            f"{'sin' if is_y_axis else 'cos'}(theta) drawn for theta from {_angle_text(low_angle)} to "
            f"{_angle_text(high_angle)}, with the origin O marked."
         ),
      )
      representation = "BC-REP-02"
   else:
      opening = f"Consider the polar curve {math(curve_tex)} for {math(window_tex)}."
      graph = None
      representation = "BC-REP-13"

   stem = (
      f"{opening} Using a calculator, find the value of {math(r'\theta')} that corresponds to the point on the curve "
      f"farthest from the {names['axis']}. Justify your answer, show the setup, and give the value correct to three "
      "decimal places."
   )

   coordinate_tex = f"{letter} = r" + (r"\cos\theta" if is_y_axis else r"\sin\theta") + " = " + tex(coordinate)
   candidate_text = ", ".join(
      f"{math(f'|{letter}({_angle_text(angle) if angle != critical_angle else decimal_text(angle)})| \\approx {decimal_text(distance)}')}"
      for angle, distance in candidates
   )
   steps = [
      Step(
         text=f"The distance from the {names['axis']} is {math('|' + letter + '|')}, where {math(coordinate_tex)}.",
         point_type_id="BC-PT-99005",
         rule="polar to rectangular conversion",
      ),
      Step(
         text=(
            f"Set {math(rf'\frac{{d{letter}}}{{d\theta}} = ' + tex(coordinate_rate) + ' = 0')}. On the interval a calculator "
            f"gives one solution, {math(r'\theta \approx ' + decimal_text(critical_angle))}."
         ),
         value=critical_angle,
         point_type_id="BC-PT-99013",
         rule="critical angle",
      ),
      Step(
         text=(
            f"Compare the candidates, the critical angle and both endpoints: {candidate_text}. The largest distance is at "
            f"{math(r'\theta \approx ' + decimal_text(farthest_angle))}, so that is the farthest point."
         ),
         point_type_id="BC-PT-99011",
         rule="candidates test",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-09027",
         derivation="r treated as the distance from the axis, so the angle where r is largest is reported",
         value=radius_peak,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99004",
         derivation="the candidates comparison run without the interior critical angle, so the farther endpoint is reported",
         value=farther_endpoint,
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05028",
         derivation="the candidates compared correctly but the one nearest the axis reported",
         value=nearest_angle,
         mechanism="reversed_quantities",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=farthest_angle, decimals=3),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="calculator",
      figure=graph,
      setup_required=True,
      command_verb="find",
      notes={
         "low_angle": low_angle,
         "high_angle": high_angle,
         "critical_count": len(critical_angles),
      },
   )
