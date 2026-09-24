"""BC-QA-02013, the value of a derivative at a named input found with a calculator."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, tex

ARCHETYPE_ID = "BC-QA-02013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": 20, "max": 30, "step": 1}},
      {"name": "swing", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "at", "type": "real", "role": "safe", "domain": {"values": [0.5, 1, 1.5, 2, 2.5, 3]}},
      {"name": "context", "type": "label", "role": "safe", "domain": {"values": ["reservoir", "traffic", "tank"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "context"]}},
   ],
   "constraints": [
      "abs(slope - degree_slope) > 1",
   ],
   "derived": [
      {"name": "slope", "expression": "form('2*swing*at/scale*cos(at^2/scale) + 1/(1 + at)')"},
      {"name": "degree_slope", "expression": "form('2*swing*at*pi/(180*scale)*cos(pi*at^2/(180*scale)) + 1/(1 + at)')"},
      {"name": "height", "expression": "form('level + swing*sin(at^2/scale) + log(1 + at)')"},
   ],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
      "abs(key - slope) < 1/1000",
      "abs(height - key) > 1",
   ],
   "dial_bindings": [
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-05", "settings": {"bare": "off", "context": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-09", "figure_kind": None, "requires": ["level", "swing", "scale", "at"]},
      {"representation": "BC-REP-05", "figure_kind": None, "requires": ["level", "swing", "scale", "at", "context"]},
   ],
   "notes": (
      "W(t) = level + swing sin(t^2 / scale) + ln(1 + t). The level keeps W above 16 while the derivative stays "
      "below 13 in size, so the function value never meets the derivative; the constraint keeps the radian and "
      "degree derivatives more than 1 apart, which also clears the early-rounded value."
   ),
}

CONTEXTS = {
   "reservoir": ("The volume of water in a reservoir", "million gallons", "days", "million gallons per day"),
   "traffic": ("The number of cars on a stretch of highway", "hundred cars", "hours", "hundred cars per hour"),
   "tank": ("The amount of fuel in a storage tank", "thousand liters", "weeks", "thousand liters per week"),
}

t = sympy.Symbol("t")


def _rounded_short(value):
   """The derivative reported to two places, or to one or none when fewer places still match the key."""
   key_three = round(float(value), 3)

   for places in (2, 1, 0):
      short = round(float(value), places)

      if round(short, 3) != key_three:
         return sympy.Rational(str(short)), places

   return sympy.Rational(str(round(float(value)) + 1)), -1


def build(names):
   level = int(names["level"])
   swing = int(names["swing"])
   scale = int(names["scale"])
   at = sympy.nsimplify(names["at"])
   function = level + swing * sympy.sin(t**2 / scale) + sympy.log(1 + t)
   derivative = sympy.diff(function, t)
   key_value = sympy.Float(derivative.subs(t, at).evalf(30), 20)
   function_value = sympy.Float(function.subs(t, at).evalf(30), 20)
   degree_function = function.subs(sympy.sin(t**2 / scale), sympy.sin(sympy.pi * t**2 / (180 * scale)))
   degree_value = sympy.Float(sympy.diff(degree_function, t).subs(t, at).evalf(30), 20)
   short_value, places = _rounded_short(key_value)

   function_tex = tex(function)
   at_tex = f"{float(at):g}"
   setup = rf"W'({at_tex}) = \left. \frac{{d}}{{dt}}\left({function_tex}\right) \right|_{{t={at_tex}}}"

   if names["framing"] == "context":
      subject, amount_units, time_units, rate_units = CONTEXTS[names["context"]]
      stem = (
         f"{subject} is modeled by {math('W(t) = ' + function_tex)} {amount_units}, where t is measured in "
         f"{time_units} for {math(r'0 \le t \le 4')}. Using a calculator, find {math(f"W'({at_tex})")}, the rate at "
         f"which the amount is changing at time t = {at_tex}. Show the setup for the calculation, give the value "
         "correct to three decimal places, and include units."
      )
      representation = "BC-REP-05"
      units = rate_units
      closing = f" {rate_units}"
   else:
      stem = (
         f"Let {math('W(t) = ' + function_tex)}. Using a calculator, find the value of {math(f"W'({at_tex})")}. "
         "Show the setup for the calculation, and give the value correct to three decimal places."
      )
      representation = "BC-REP-09"
      units = None
      closing = ""

   steps = [
      Step(
         text=f"The quantity asked for is the derivative of W at t = {at_tex}: {math(setup)}.",
         rule="derivative at a point",
      ),
      Step(
         text=(
            f"With the calculator in radian mode, the numerical derivative at t = {at_tex} gives "
            f"{math(f"W'({at_tex})")} approximately {decimal_text(key_value)}{closing}."
         ),
         value=key_value,
         rule="numerical derivative",
      ),
   ]

   if places > 0:
      rounding = f"the derivative reported to {'two places' if places == 2 else 'one place'} instead of three"
   else:
      rounding = "the derivative reported as a whole number instead of to three places"

   distractors = [
      Distractor(
         error_path="BC-ERR-02024",
         derivation=f"the function value W({at_tex}) reported in place of the derivative value",
         value=function_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-09023",
         derivation="the numerical derivative taken with the calculator in degree mode, so the sine reads its argument in degrees",
         value=degree_value,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02032",
         derivation=rounding,
         value=short_value,
         mechanism="algebra_slip",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=key_value, decimals=3, units=units),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
