"""CDT-value-01, a function evaluated at a point that is not an integer."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, draw_record, drill_spec, first_clear, function_entry, has_trig, key_exclusion, math,
   number_text, tex, value_at,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-value-01"
CAPABILITY = "value"
CARD_ID = "CCD-value-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "lift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "point", "type": "real", "role": "safe", "domain": {"min": 0.3, "max": 4.8, "step": 0.1, "exclude": [1, 2, 3, 4]}},
      {"name": "form", "type": "label", "role": "safe", "domain": {"values": ["exponential", "sine"]}},
   ],
   notes=(
      "f(x) = (x^2 + lift) e^(-x / stretch) or (x^2 + lift) sin(x / stretch), evaluated at a point with one decimal "
      "that is not a whole number. The point is nudged by hundredths when the key's rounded and truncated forms agree."
   ),
)

NUDGES = (0, sympy.Rational(1, 100), sympy.Rational(2, 100), sympy.Rational(3, 100), sympy.Rational(4, 100))

x = sympy.Symbol("x")


def function(names):
   if names["form"] == "exponential":
      return (x**2 + names["lift"]) * sympy.exp(-x / names["stretch"])

   return (x**2 + names["lift"]) * sympy.sin(x / names["stretch"])


def build(names):
   f_expression = function(names)

   def build_variant(nudge):
      point = sympy.nsimplify(names["point"] + nudge)
      value_key = value_at(f_expression, x, point)
      point_text = number_text(point)
      prompt = (
         f"Let {math(f'f(x) = {tex(f_expression)}')}. Find {math(f'f({point_text})')} to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}",
         setup_key=from_sympy(sympy.Subs(f_expression, x, point)),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression)}, used_point=point),
         exclusion=key_exclusion(value_key),
      )

   return first_clear(NUDGES, build_variant)
