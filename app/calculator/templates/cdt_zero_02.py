"""CDT-zero-02, the input at which a function takes a stated value."""
import sympy

from app.calculator.kit import (
   EQUATION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   math, numeric_roots, tex, zero_at_half_integer,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-zero-02"
CAPABILITY = "zero"
CARD_ID = "CCD-zero-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "cubic", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "growth", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 15, "step": 1}},
   ],
   notes=(
      "f(x) = x^3 / cubic + e^(x / growth) is strictly increasing, so f(x) = level has exactly one solution, which lies "
      "between -20 and 20 for these levels. The level is stepped by one when the key's rounded and truncated forms "
      "agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)
SEARCH = (-20, 20)

x = sympy.Symbol("x")


def build(names):
   f_expression = x**3 / names["cubic"] + sympy.exp(x / names["growth"])

   def build_variant(step):
      level = names["level"] + step
      roots = numeric_roots(f_expression - level, x, *SEARCH)
      has_one_root = len(roots) == 1
      value_key = roots[0] if has_one_root else sympy.Float("nan")
      exclusion = "root_count" if not has_one_root else first_reason(zero_at_half_integer(value_key), key_exclusion(value_key))
      prompt = (
         f"Let {math(f'f(x) = {tex(f_expression)}')}. Find the value of {math('x')} for which "
         f"{math(f'f(x) = {level}')}, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}",
         setup_key=from_sympy(sympy.Eq(f_expression, level)),
         setup_kind=EQUATION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression)}, used_level=level),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
