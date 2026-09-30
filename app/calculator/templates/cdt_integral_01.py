"""CDT-integral-01, the total a rate with a cosine or exponential factor accumulates over an interval."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   linear_integrand, math, number_text, numeric_integral, tex,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-integral-01"
CAPABILITY = "integral"
CARD_ID = "CCD-integral-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 8, "step": 1}},
      {"name": "swing", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "horizon", "type": "real", "role": "safe", "domain": {"values": [2, 2.5, 3, 3.5, 4, 4.5]}},
      {"name": "factor", "type": "label", "role": "safe", "domain": {"values": ["cosine", "exponential"]}},
   ],
   notes=(
      "The rate is base + swing cos(t^2 / stretch) or base + swing t e^(-t / stretch) litres per minute, positive "
      "because base exceeds swing times the largest value of the factor. The horizon is nudged by tenths when the key's "
      "rounded and truncated forms agree."
   ),
)

UNIT = "litres"
NUDGES = (0, sympy.Rational(1, 10), sympy.Rational(2, 10), sympy.Rational(3, 10), sympy.Rational(4, 10))

t = sympy.Symbol("t")


def rate(names):
   if names["factor"] == "cosine":
      return names["base"] + names["swing"] * sympy.cos(t**2 / names["stretch"])

   return names["base"] + names["swing"] * t * sympy.exp(-t / names["stretch"])


def build(names):
   rate_expression = rate(names)
   start = names["horizon"]

   def build_variant(nudge):
      horizon = sympy.nsimplify(start + nudge)
      setup = sympy.Integral(rate_expression, (t, 0, horizon))
      value_key = numeric_integral(rate_expression, t, 0, horizon)
      exclusion = first_reason(linear_integrand(rate_expression, t), key_exclusion(value_key))
      horizon_text = number_text(horizon)
      prompt = (
         f"Water runs into a cistern at {math(f'R(t) = {tex(rate_expression)}')} litres per minute, where "
         f"{math('t')} is the time in minutes. Find how many litres run in from {math('t = 0')} to "
         f"{math(f't = {horizon_text}')}, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"R(t) = {tex(rate_expression)}",
         setup_key=from_sympy(setup),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=UNIT,
         radian_sensitive=has_trig(rate_expression),
         draw=draw_record(names, {"R": function_entry(t, rate_expression)}, used_horizon=horizon),
         exclusion=exclusion,
      )

   return first_clear(NUDGES, build_variant)
