"""BC-QA-09003, the length of a parametric curve, or the distance a particle travels along it, calculator active."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, decimal_text, math, numeric_integral
from app.generation.templates._helpers_f import tex_f

ARCHETYPE_ID = "BC-QA-09003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run F"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "stretch", "type": "rational", "role": "safe", "domain": {"values": ["1", "3/2", "2", "5/2", "3", "4"]}},
      {"name": "height", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "frequency", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1", "2"]}},
      {"name": "end", "type": "rational", "role": "safe", "domain": {"values": ["1", "3/2", "2", "5/2", "3"]}},
      {"name": "units", "type": "label", "role": "safe", "domain": {"values": ["meters", "feet", "centimeters"]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["curve", "velocity"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "finite(key)",
      "nondegenerate_three_decimals(key)",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-08", "settings": {"velocity": "off", "curve": "low"}},
   ],
   "calculator_guard": None,
   "representation_bindings": [
      {"representation": "BC-REP-12", "figure_kind": None, "requires": ["stretch", "height", "frequency", "end", "given"]},
   ],
   "notes": "x = stretch t^2 and y = height sin(frequency t) on [0, end]; x increases on the interval, so the curve is traced once. The x-rate 2 stretch t has a coefficient other than 1, so squaring it without parentheses changes the integrand.",
}

t = sympy.Symbol("t")


def build(names):
   stretch = names["stretch"]
   height = names["height"]
   frequency = names["frequency"]
   end = names["end"]
   units = names["units"]
   is_curve = names["given"] == "curve"

   horizontal = stretch * t**2
   vertical = height * sympy.sin(frequency * t)
   x_rate = sympy.diff(horizontal, t)
   y_rate = sympy.diff(vertical, t)
   x_coefficient = 2 * stretch

   length = numeric_integral(sympy.sqrt(x_rate**2 + y_rate**2), t, 0, end)
   summed_rates = numeric_integral(x_rate + y_rate, t, 0, end)
   lost_parentheses = numeric_integral(sympy.sqrt(x_coefficient * t**2 + y_rate**2), t, 0, end)
   displacement = sympy.sqrt(horizontal.subs(t, end) ** 2 + vertical.subs(t, end) ** 2).evalf(30)

   end_tex = tex_f(end)
   window = rf"0 \le t \le {end_tex}"

   if is_curve:
      stem = (
         f"A curve is defined by {math('x = ' + tex_f(horizontal))} and {math('y = ' + tex_f(vertical))}. Using a "
         f"calculator, find the length of the curve for {math(window)}. Show the setup for the calculation, and give "
         "the value correct to three decimal places."
      )
      key_units = None
      rate_text = f"{math(r'\frac{dx}{dt} = ' + tex_f(x_rate))} and {math(r'\frac{dy}{dt} = ' + tex_f(y_rate))}"
   else:
      velocity = rf"\left\langle {tex_f(x_rate)}, {tex_f(y_rate)} \right\rangle"
      stem = (
         f"A particle moves in the plane with velocity vector {math('v(t) = ' + velocity)}, with t in seconds and "
         f"distance in {units}, and it is at the origin at {math('t = 0')}. Using a calculator, find the total distance "
         f"the particle travels over {math(window)}. Show the setup for the calculation, and give the value correct "
         "to three decimal places."
      )
      key_units = units
      rate_text = f"the components are {math(r'\frac{dx}{dt} = ' + tex_f(x_rate))} and {math(r'\frac{dy}{dt} = ' + tex_f(y_rate))}"

   integral = rf"\int_{{0}}^{{{end_tex}}} \sqrt{{\left({tex_f(x_rate)}\right)^{{2}} + \left({tex_f(y_rate)}\right)^{{2}}}}\,dt"
   steps = [
      Step(text=f"The rates are {rate_text}." if is_curve else f"From the velocity, {rate_text}.", rule="component rates"),
      Step(
         text=f"The length is {math(integral)}, the integral of the speed.",
         rule="arc length of a parametric curve",
      ),
      Step(
         text=f"A calculator gives {decimal_text(length)}" + (f" {units}." if not is_curve else "."),
         value=length,
         rule="numerical integration",
      ),
   ]

   distractors = [
      Distractor("BC-ERR-09013", "the two rates added, the integral of dx/dt + dy/dt", summed_rates, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-09014", f"(dx/dt)^2 written as {tex_f(x_coefficient)} t^2, the coefficient left unsquared", lost_parentheses, mechanism="algebra_slip"),
      Distractor("BC-ERR-99010", "the straight-line distance from the start to the end, the magnitude of the displacement", displacement, mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="numeric", value=length, decimals=3, units=key_units),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-12",
      calculator_status="calculator",
      setup_required=True,
      command_verb="find",
   )
