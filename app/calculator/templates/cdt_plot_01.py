"""CDT-plot-01, the maximum value of a function whose peak lies outside the default window."""
import sympy

from app.calculator.kit import (
   EQUATION, DrillTask, draw_record, drill_spec, first_clear, function_entry, has_trig, key_exclusion,
   math, numeric_roots, tex, value_at,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-plot-01"
CAPABILITY = "plot"
CARD_ID = "CCD-plot-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "reach", "type": "integer", "role": "safe", "domain": {"min": 4, "max": 8, "step": 1}},
      {"name": "drift", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
   ],
   notes=(
      "f(x) = scale x^2 e^(-x / reach) + x / drift rises to one local maximum on 0 < x < 6 reach, beyond the default "
      "window, and the task is its value. The drift term moves the peak off 2 reach. The reach is stepped by one when "
      "the key's rounded and truncated forms agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)

x = sympy.Symbol("x")


def build(names):
   def build_variant(step):
      reach = names["reach"] + step
      f_expression = names["scale"] * x**2 * sympy.exp(-x / reach) + x / names["drift"]
      window = 6 * reach
      slope = sympy.diff(f_expression, x)
      curvature = sympy.diff(slope, x)
      critical = [root for root in numeric_roots(slope, x, 1, window) if curvature.subs(x, root) < 0]
      has_one_peak = len(critical) == 1
      peak = critical[0] if has_one_peak else sympy.Integer(window)
      value_key = value_at(f_expression, x, peak) if has_one_peak else sympy.Float("nan")
      exclusion = key_exclusion(value_key) if has_one_peak else "root_count"
      prompt = (
         f"Let {math(f'f(x) = {tex(f_expression)}')}. On the interval {math(f'0 < x < {window}')}, {math('f')} has "
         "exactly one local maximum. Find the value of that maximum, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}",
         setup_key=from_sympy(sympy.Eq(slope, 0)),
         setup_kind=EQUATION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression)}, used_reach=reach, peak=peak),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
