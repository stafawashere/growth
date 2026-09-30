"""CDT-intersection-01, a definite integral whose upper bound is where two graphs cross."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   lattice_point, linear_integrand, math, numeric_integral, numeric_roots, tex, value_at,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-intersection-01"
CAPABILITY = "intersection"
CARD_ID = "CCD-intersection-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "height", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "narrow", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
   ],
   notes=(
      "f(x) = height cos(x / stretch) falls on [0, 3 stretch] and g(x) = x^2 / narrow rises there, with f(0) > g(0) and "
      "f(3 stretch) < 0 < g(3 stretch), so the graphs cross exactly once in (0, 3 stretch) at r; the task is the "
      "integral of f - g from 0 to r. The narrow parameter is stepped by one when the key's rounded and truncated "
      "forms agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)

x = sympy.Symbol("x")


def build(names):
   f_expression = names["height"] * sympy.cos(x / names["stretch"])
   window = 3 * names["stretch"]

   def build_variant(step):
      narrow = names["narrow"] + step
      g_expression = x**2 / narrow
      difference = f_expression - g_expression
      roots = numeric_roots(difference, x, 0, window)
      has_one_root = len(roots) == 1
      functions = {"f": function_entry(x, f_expression), "g": function_entry(x, g_expression)}
      prompt = (
         f"Let {math(f'f(x) = {tex(f_expression)}')} and {math(f'g(x) = {tex(g_expression)}')}. The graphs of "
         f"{math('f')} and {math('g')} cross at exactly one point with {math(f'0 < x < {window}')}. Call its "
         f"{math('x')} coordinate {math('r')}. Find {math(r'\int_{0}^{r} \left(f(x) - g(x)\right)\,dx')} to three "
         "decimal places."
      )

      crossing = roots[0] if has_one_root else sympy.Integer(window)
      setup = sympy.Integral(difference, (x, 0, crossing))
      value_key = numeric_integral(difference, x, 0, crossing)

      if has_one_root:
         exclusion = first_reason(
            linear_integrand(difference, x),
            lattice_point(crossing, value_at(f_expression, x, crossing)),
            key_exclusion(value_key),
         )
      else:
         exclusion = "root_count"

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}, \\quad g(x) = {tex(g_expression)}",
         setup_key=from_sympy(setup),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression, g_expression),
         draw=draw_record(names, functions, used_narrow=narrow, crossing=crossing),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
