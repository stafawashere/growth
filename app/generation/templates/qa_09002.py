"""BC-QA-09002, the second derivative of a parametric curve at a parameter value and the concavity it gives."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-09002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "x_square", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
      {"name": "x_linear", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "x_constant", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "y_cube", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
      {"name": "y_square", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "y_constant", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "time", "type": "integer", "role": "safe", "domain": {"values": [-1, 1, 2]}},
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["forward", "backward"]}},
   ],
   "constraints": [
      "x_rate > 0 if direction == 'forward' else x_rate < 0",
      "x_rate != 1",
      "second != 0",
      "y_accel * second < 0",
      "y_accel / x_accel != second",
      "y_accel / x_accel != second * x_rate",
   ],
   "derived": [
      {"name": "x_rate", "expression": "2 * x_square * time + x_linear"},
      {"name": "x_accel", "expression": "2 * x_square"},
      {"name": "y_rate", "expression": "3 * y_cube * time**2 + 2 * y_square * time"},
      {"name": "y_accel", "expression": "6 * y_cube * time + 2 * y_square"},
      {"name": "second", "expression": "(y_accel * x_rate - y_rate * x_accel) / x_rate**3"},
   ],
   "invariants": [
      "concavity in ['concave up', 'concave down']",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-12", "settings": {"forward": "off", "backward": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-12", "figure_kind": None, "requires": ["x_square", "x_linear", "y_cube", "y_square", "time", "direction"]},
   ],
   "notes": "x is quadratic and y cubic in t, so every quantity is exact. The constraints keep dx/dt away from 0 and 1 (at 1 the missing second division would change nothing), make d2y/dt2 opposite in sign to d2y/dx2 so the component reading gives the wrong verdict, and keep the quotient of second derivatives apart from the key. Up and down each occur on about half of the tuples, and dx/dt is negative on the backward half.",
}

t = sympy.Symbol("t")


def _verdict(value):
   return "concave up" if value > 0 else "concave down"


def _label(value, quantity, time):
   return f"The curve is {_verdict(value)} at t = {time}, because {math(quantity + ' = ' + tex_f(value))} there."


def build(names):
   time = names["time"]
   horizontal = names["x_square"] * t**2 + names["x_linear"] * t + names["x_constant"]
   vertical = names["y_cube"] * t**3 + names["y_square"] * t**2 + names["y_constant"]

   x_rate = sympy.diff(horizontal, t)
   y_rate = sympy.diff(vertical, t)
   slope = sympy.cancel(y_rate / x_rate)
   slope_rate = sympy.cancel(sympy.diff(slope, t))
   second = sympy.cancel(slope_rate / x_rate)

   second_value = second.subs(t, time)
   slope_rate_value = slope_rate.subs(t, time)
   quotient_value = sympy.diff(vertical, t, 2).subs(t, time) / sympy.diff(horizontal, t, 2).subs(t, time)
   y_accel_value = sympy.diff(vertical, t, 2).subs(t, time)
   concavity = _verdict(second_value)

   stem = (
      f"A curve is defined by {math('x = ' + tex_f(horizontal))} and {math('y = ' + tex_f(vertical))}. Find "
      rf"{math(r'\frac{d^{2}y}{dx^{2}}')} at {math(f't = {time}')}, and state whether the curve is concave up or "
      "concave down there."
   )

   steps = [
      Step(
         text=(
            f"{math(r'\frac{dy}{dx} = \frac{dy/dt}{dx/dt} = \frac{' + tex_f(y_rate) + '}{' + tex_f(x_rate) + '}')}, "
            f"which simplifies to {math(tex_f(slope))}."
         ),
         rule="slope of a parametric curve",
      ),
      Step(
         text=(
            f"Differentiate with respect to t: {math(r'\frac{d}{dt}\left(\frac{dy}{dx}\right) = ' + tex_f(slope_rate))}, "
            f"which is {math(tex_f(slope_rate_value))} at {math(f't = {time}')}."
         ),
         value=slope_rate_value,
         rule="quotient rule",
      ),
      Step(
         text=(
            f"Divide by {math(r'\frac{dx}{dt}')}, which is {math(tex_f(x_rate.subs(t, time)))} at {math(f't = {time}')}: "
            f"{math(r'\frac{d^{2}y}{dx^{2}} = ' + tex_f(second_value))}, so the curve is {concavity} there."
         ),
         value=second_value,
         rule="second derivative of a parametric curve",
      ),
   ]

   second_name = r"\frac{d^{2}y}{dx^{2}}"
   distractors = [
      Distractor(
         "BC-ERR-09009",
         "d2y/dx2 taken as the quotient of the second derivatives, (d2y/dt2)/(d2x/dt2)",
         label=_label(quotient_value, second_name, time),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         "BC-ERR-09010",
         "the derivative of dy/dx with respect to t, without the second division by dx/dt",
         label=_label(slope_rate_value, second_name, time),
         mechanism="algebra_slip",
      ),
      Distractor(
         "BC-ERR-09012",
         "concavity read from the sign of d2y/dt2",
         label=_label(y_accel_value, r"\frac{d^{2}y}{dt^{2}}", time),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_label(second_value, second_name, time)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-12",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"concavity": concavity},
   )
