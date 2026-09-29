"""CDT-plot-02, a zero that the default window does not show."""
import sympy

from app.calculator.kit import (
   EQUATION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   math, numeric_roots, tex, zero_at_half_integer,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-plot-02"
CAPABILITY = "plot"
CARD_ID = "CCD-plot-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "growth", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 4, "step": 1}},
      {"name": "weight", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
   ],
   notes=(
      "f(x) = e^(x / growth) - weight x^2 is negative from x = 2 until the exponential overtakes the square, well "
      "beyond x = 10, and positive after, so it has exactly one zero on 2 < x < 20 growth. The weight is stepped by "
      "one when the key's rounded and truncated forms agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)
LOW = 2

x = sympy.Symbol("x")


def build(names):
   growth = names["growth"]
   high = 20 * growth

   def build_variant(step):
      weight = names["weight"] + step
      f_expression = sympy.exp(x / growth) - weight * x**2
      roots = numeric_roots(f_expression, x, LOW, high, pieces=800)
      has_one_root = len(roots) == 1
      value_key = roots[0] if has_one_root else sympy.Float("nan")
      exclusion = "root_count" if not has_one_root else first_reason(zero_at_half_integer(value_key), key_exclusion(value_key))
      prompt = (
         f"The function {math(f'f(x) = {tex(f_expression)}')} has exactly one zero on the interval "
         f"{math(f'{LOW} < x < {high}')}. Find it, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}",
         setup_key=from_sympy(sympy.Eq(f_expression, 0)),
         setup_kind=EQUATION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression)}, used_weight=weight),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
