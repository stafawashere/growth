"""CDT-integral-02, the average value of a function on an interval."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   linear_integrand, math, numeric_integral, tex,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-integral-02"
CAPABILITY = "integral"
CARD_ID = "CCD-integral-02"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "low", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 2, "step": 1}},
      {"name": "span", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "form", "type": "label", "role": "safe", "domain": {"values": ["log", "root", "sine"]}},
   ],
   notes=(
      "f is scale ln(x^2 + shift), scale sqrt(x^3 + shift) or scale + sin(x^2 / shift) on [low, low + span]; the "
      "average value is the integral divided by span. The shift is stepped by one when the key's rounded and truncated "
      "forms agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)

x = sympy.Symbol("x")


def function(names, shift):
   scale = names["scale"]

   if names["form"] == "log":
      return scale * sympy.log(x**2 + shift)

   if names["form"] == "root":
      return scale * sympy.sqrt(x**3 + shift)

   return scale + sympy.sin(x**2 / shift)


def build(names):
   low = names["low"]
   span = names["span"]
   high = low + span

   def build_variant(step):
      shift = names["shift"] + step
      f_expression = function(names, shift)
      setup = sympy.Mul(sympy.Rational(1, span), sympy.Integral(f_expression, (x, low, high)), evaluate=False)
      value_key = sympy.Float(numeric_integral(f_expression, x, low, high) / span, 20)
      exclusion = first_reason(linear_integrand(f_expression, x), key_exclusion(value_key))
      prompt = (
         f"Let {math(f'f(x) = {tex(f_expression)}')}. Find the average value of {math('f')} on the interval "
         f"{math(f'{low} \\le x \\le {high}')}, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}",
         setup_key=from_sympy(setup),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression)}, used_shift=shift),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
