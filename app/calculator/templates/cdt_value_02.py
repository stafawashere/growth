"""CDT-value-02, an amount found from its starting value and the integral of its rate to a stated time."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, draw_record, drill_spec, first_clear, first_reason, has_trig, key_exclusion,
   linear_integrand, math, number_text, numeric_integral, tex,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-value-02"
CAPABILITY = "value"
CARD_ID = "CCD-value-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 25, "max": 70, "step": 5}},
      {"name": "size", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "moment", "type": "real", "role": "safe", "domain": {"values": [2, 2.5, 3, 3.5, 4, 4.5, 5]}},
      {"name": "form", "type": "label", "role": "safe", "domain": {"values": ["sine", "root"]}},
   ],
   notes=(
      "S(0) = start kilograms and S'(t) = size sin(t^2 / stretch) or size - sqrt(t^2 + stretch) kilograms per hour, "
      "which change sign, so the amount rises and falls. A start of at least 25 keeps the amount positive, since the "
      "root rate is never below -3.9 on [0, 5.4]. The moment is nudged by tenths when the key's rounded and truncated "
      "forms agree."
   ),
)

UNIT = "kilograms"
NUDGES = (0, sympy.Rational(1, 10), sympy.Rational(2, 10), sympy.Rational(3, 10), sympy.Rational(4, 10))

t = sympy.Symbol("t")


def rate(names):
   if names["form"] == "sine":
      return names["size"] * sympy.sin(t**2 / names["stretch"])

   return names["size"] - sympy.sqrt(t**2 + names["stretch"])


def build(names):
   rate_expression = rate(names)
   start = names["start"]

   def build_variant(nudge):
      moment = sympy.nsimplify(names["moment"] + nudge)
      setup = sympy.Add(start, sympy.Integral(rate_expression, (t, 0, moment)), evaluate=False)
      value_key = sympy.Float(start + numeric_integral(rate_expression, t, 0, moment), 20)
      exclusion = first_reason(linear_integrand(rate_expression, t), key_exclusion(value_key))
      moment_text = number_text(moment)
      prompt = (
         f"A vat holds {math('S(t)')} kilograms of salt {math('t')} hours after it is filled, with "
         f"{math(f'S(0) = {start}')} and {math(f"S'(t) = {tex(rate_expression)}")}. Find "
         f"{math(f'S({moment_text})')}, in kilograms, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"S'(t) = {tex(rate_expression)}",
         setup_key=from_sympy(setup),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=UNIT,
         radian_sensitive=has_trig(rate_expression),
         draw=draw_record(names, {}, used_moment=moment),
         exclusion=exclusion,
      )

   return first_clear(NUDGES, build_variant)
