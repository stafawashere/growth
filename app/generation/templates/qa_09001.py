"""BC-QA-09001, the slope of the line tangent to a parametric path at a time, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-09001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "drift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "height", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "rate", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1/3", "1/4", "2/3", "3/4"]}},
      {"name": "vertical", "type": "label", "role": "safe", "domain": {"values": ["sine", "cosine", "exponential"]}},
      {"name": "time", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "3/2", "2", "5/2", "3"]}},
      {"name": "object", "type": "label", "role": "safe", "domain": {"values": ["particle", "drone", "bead"]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["positions", "rate_of_x"]}},
   ],
   "constraints": [
      "2 * rate * time != 1",
      "2 * rate * time * (drift + 2 * time / (1 + time**2)) != 1",
      "rate * time**2 >= 1/2",
      "abs(rate * time**2 - 157/100) >= 1/4",
      "rate * time**2 <= 3",
      "not (vertical == 'exponential' and drift == 2 and height == 6 and rate == 1/2 and time == 3/2)",
   ],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-08", "settings": {"positions": "off", "rate_of_x": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-12", "figure_kind": None, "requires": ["drift", "height", "rate", "vertical", "time", "given"]},
   ],
   "notes": "x(t) = drift t + ln(1 + t^2), so dx/dt is at least drift and never 0. The vertical component has a t^2 inside, so its derivative needs the chain rule, which the component-derivative distractor leaves out; the inner factor 2 rate t is kept away from 1, and from 1 over dx/dt, so that leaving it out gives a value apart from the slope and from dy/dt. The angle rate t^2 lies between 1/2 and 3 and is kept a quarter away from pi/2, so the rates are not close to 0 and the options stay apart at three decimals. One exponential tuple whose slope rounds to -1.000 is excluded by name. With rate_of_x the stem gives dx/dt directly and x(0), so only y must be differentiated.",
}

OBJECTS = {"particle": "A particle", "drone": "A drone", "bead": "A bead"}

t = sympy.Symbol("t")


def _vertical(form, height, rate):
   inner = rate * t**2

   if form == "sine":
      return height * sympy.sin(inner), height * sympy.cos(inner)

   if form == "cosine":
      return height * sympy.cos(inner), -height * sympy.sin(inner)

   return height * sympy.exp(-inner), -height * sympy.exp(-inner)


def build(names):
   drift = names["drift"]
   time = names["time"]
   is_rate_given = names["given"] == "rate_of_x"

   horizontal = drift * t + sympy.log(1 + t**2)
   vertical, outer_only = _vertical(names["vertical"], names["height"], names["rate"])
   horizontal_rate = sympy.diff(horizontal, t)
   vertical_rate = sympy.diff(vertical, t)

   x_rate_value = horizontal_rate.subs(t, time)
   y_rate_value = vertical_rate.subs(t, time)
   slope = (y_rate_value / x_rate_value).evalf(30)
   reciprocal = (x_rate_value / y_rate_value).evalf(30)
   chain_omitted = (outer_only.subs(t, time) / x_rate_value).evalf(30)

   subject = OBJECTS[names["object"]]
   time_tex = tex_f(time)

   if is_rate_given:
      path = (
         f"{subject} moves in the xy-plane so that {math(r'\frac{dx}{dt} = ' + tex_f(horizontal_rate))} "
         f"with {math('x(0) = 0')}, and {math('y(t) = ' + tex_f(vertical))}, for {math(r't \ge 0')}."
      )
   else:
      path = (
         f"{subject} moves in the xy-plane so that its position at time t is "
         f"{math('(x(t), y(t)) = ' + rf'\left({tex_f(horizontal)}, {tex_f(vertical)}\right)')} for {math(r't \ge 0')}."
      )

   stem = (
      f"{path} Using a calculator, find the slope of the line tangent to the path of the {names['object']} at "
      f"{math(f't = {time_tex}')}. Show the setup for the calculation, and give the value correct to three decimal places."
   )

   slope_setup = rf"\frac{{dy/dt}}{{dx/dt}} = \frac{{y'({time_tex})}}{{x'({time_tex})}}"
   steps = [
      Step(
         text=(
            f"{math(r'\frac{dx}{dt} = ' + tex_f(horizontal_rate))} and, by the chain rule, "
            f"{math(r'\frac{dy}{dt} = ' + tex_f(vertical_rate))}."
         ),
         point_type_id="BC-PT-99049",
         rule="component derivatives",
      ),
      Step(
         text=(
            f"At {math(f't = {time_tex}')}, {math(r'\frac{dx}{dt} = ' + tex_f(x_rate_value))} and "
            f"{math(r'\frac{dy}{dt} \approx ' + decimal_text(y_rate_value))} (more places kept)."
         ),
         value=y_rate_value.evalf(30),
         point_type_id="BC-PT-99005",
         rule="evaluate at the time",
      ),
      Step(
         text=f"The slope is {math(slope_setup + r' \approx ' + decimal_text(slope))}.",
         value=slope,
         point_type_id="BC-PT-99004",
         rule="dy/dx as a quotient of rates",
      ),
   ]

   distractors = [
      Distractor("BC-ERR-09002", "the quotient taken the other way, dx/dt divided by dy/dt", reciprocal, mechanism="reversed_quantities"),
      Distractor("BC-ERR-09003", "dy/dt at the time reported as the slope", y_rate_value.evalf(30), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-09001", "dy/dt found without the chain rule, the derivative of the outer function only", chain_omitted, mechanism="chain_rule_omitted"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=slope, decimals=3),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-12",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
