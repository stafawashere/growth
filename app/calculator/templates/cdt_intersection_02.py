"""CDT-intersection-02, the x coordinate where two graphs cross."""
import sympy

from app.calculator.kit import (
   EQUATION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   lattice_point, math, numeric_roots, tex, value_at,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-intersection-02"
CAPABILITY = "intersection"
CARD_ID = "CCD-intersection-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "growth", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "top", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "narrow", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
   ],
   notes=(
      "f(x) = e^(x / growth) rises from 1 and g(x) = top - x^2 / narrow falls from top for x > 0, so the graphs cross "
      "exactly once with x > 0, below sqrt(top narrow). The top is stepped by one when the key's rounded and "
      "truncated forms agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)

x = sympy.Symbol("x")


def build(names):
   f_expression = sympy.exp(x / names["growth"])

   def build_variant(step):
      top = names["top"] + step
      g_expression = top - x**2 / names["narrow"]
      search_end = sympy.sqrt(top * names["narrow"]) + 1
      roots = numeric_roots(f_expression - g_expression, x, 0, search_end)
      has_one_root = len(roots) == 1
      value_key = roots[0] if has_one_root else sympy.Float("nan")

      if has_one_root:
         exclusion = first_reason(lattice_point(value_key, value_at(f_expression, x, value_key)), key_exclusion(value_key))
      else:
         exclusion = "root_count"

      prompt = (
         f"Let {math(f'f(x) = {tex(f_expression)}')} and {math(f'g(x) = {tex(g_expression)}')}. The graphs of "
         f"{math('f')} and {math('g')} cross at exactly one point with {math('x > 0')}. Find the {math('x')} "
         "coordinate of that point, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}, \\quad g(x) = {tex(g_expression)}",
         setup_key=from_sympy(sympy.Eq(f_expression, g_expression)),
         setup_kind=EQUATION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression, g_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression), "g": function_entry(x, g_expression)}, used_top=top),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
