"""BC-QA-04004, the intervals on which a particle moves in a stated direction, from the sign of velocity."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_c import first_integer_inside, intervals_text, where_sign

ARCHETYPE_ID = "BC-QA-04004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "double_root", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "single_root", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 7, "step": 1}},
      {"name": "size", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "leading", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "negative"]}},
      {"name": "horizon", "type": "integer", "role": "safe", "domain": {"min": 5, "max": 10, "step": 1}},
      {"name": "direction", "type": "label", "role": "safe", "domain": {"values": ["left", "right"]}},
      {"name": "time_units", "type": "label", "role": "safe", "domain": {"values": ["seconds", "minutes", "hours"]}},
   ],
   "constraints": [
      "double_root != single_root",
      "(double_root + 2*single_root) % 3 != 0",
      "horizon > double_root",
      "horizon > single_root",
   ],
   "derived": [
      {"name": "turning_time", "expression": "(double_root + 2*single_root) / 3"},
   ],
   "invariants": [
      "not is_integer(turning_time)",
      "0 < turning_time",
      "turning_time < horizon",
   ],
   "dial_bindings": [
      {"parameter": "leading", "difficulty_factor_id": "BC-DF-12", "settings": {"positive": "off", "negative": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["double_root", "single_root", "size", "leading", "horizon", "direction"]},
   ],
   "notes": "Position k(t - p)^2 (t - q) has velocity k(t - p)(3t - p - 2q), with one integer zero p and one zero (p + 2q)/3 that is never an integer, so sampling integer times misses it.",
}

t = sympy.Symbol("t")


def _statement(direction, intervals, horizon, reason):
   if not intervals:
      return f"The particle is never moving to the {direction} for {math(f'0 < t < {horizon}')}, because {reason} at no time in that interval."

   return f"The particle is moving to the {direction} exactly on {intervals_text(intervals)}, because {reason} there."


def build(names):
   double_root = int(names["double_root"])
   single_root = int(names["single_root"])
   horizon = int(names["horizon"])
   sign = 1 if names["leading"] == "positive" else -1
   leading = sign * int(names["size"])
   moving_right = names["direction"] == "right"
   direction = names["direction"]
   inequality = ">" if moving_right else "<"
   decreasing_word = "increasing" if moving_right else "decreasing"

   position = leading * (t - double_root) ** 2 * (t - single_root)
   velocity = sympy.factor(sympy.diff(position, t))
   turning_time = sympy.Rational(double_root + 2 * single_root, 3)
   velocity_zeros = sorted([sympy.Integer(double_root), turning_time])

   key_intervals = where_sign(velocity, t, velocity_zeros, 0, horizon, moving_right)
   position_intervals = where_sign(position, t, [double_root, single_root], 0, horizon, moving_right)
   sampled_intervals = where_sign(velocity, t, [double_root], 0, horizon, moving_right, sample=first_integer_inside)
   acceleration = sympy.diff(velocity, t)
   acceleration_zero = sympy.solve(acceleration, t)[0]
   monotone_intervals = where_sign(acceleration, t, [acceleration_zero], 0, horizon, moving_right)

   units = names["time_units"]
   stem = (
      f"A particle moves along the x-axis so that its position at time t {units} is "
      f"{math('x(t) = ' + tex(position))}, for {math(f'0 \\le t \\le {horizon}')}. Find all open intervals of time in "
      f"{math(f'0 < t < {horizon}')} during which the particle is moving to the {direction}. Give a reason for the answer."
   )

   velocity_tex = "v(t) = x'(t) = " + tex(velocity)
   zeros_tex = ", ".join(tex(zero) for zero in velocity_zeros)
   steps = [
      Step(
         text=f"Differentiate the position with the product rule: {math(velocity_tex)}.",
         rule="velocity is the derivative of position",
      ),
      Step(
         text=f"Solving {math('v(t) = 0')} gives {math('t = ' + zeros_tex)}, which split {math(f'0 < t < {horizon}')} into pieces on which v keeps one sign.",
         rule="zeros of velocity",
      ),
      Step(
         text=(
            f"Testing a time in each piece shows {math(f'v(t) {inequality} 0')} exactly on {intervals_text(key_intervals)}. "
            f"The particle moves to the {direction} when its velocity is {'positive' if moving_right else 'negative'}, so it "
            f"moves to the {direction} on {intervals_text(key_intervals)}."
         ),
         rule="sign of velocity gives the direction of motion",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-04008",
         derivation=f"the direction read from the sign of the position x(t) rather than of the velocity",
         label=_statement(direction, position_intervals, horizon, math(f"x(t) {inequality} 0")),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-04010",
         derivation=(
            f"only the integer zero t = {double_root} found by trying whole-number times, so the zero at t = "
            f"{turning_time} is missed and each remaining piece is judged at one whole-number time"
         ),
         label=_statement(direction, sampled_intervals, horizon, math(f"v(t) {inequality} 0")),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-99030",
         derivation=f"the direction read from whether the velocity is {decreasing_word}, the sign of its change, rather than from its sign",
         label=_statement(direction, monotone_intervals, horizon, f"v(t) is {decreasing_word}"),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_statement(direction, key_intervals, horizon, math(f"v(t) {inequality} 0"))),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
