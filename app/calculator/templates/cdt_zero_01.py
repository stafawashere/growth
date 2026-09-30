"""CDT-zero-01, the x-intercept of a transcendental function."""
import sympy

from app.calculator.kit import (
   EQUATION, DrillTask, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig, key_exclusion,
   math, numeric_roots, tex, zero_at_half_integer,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-zero-01"
CAPABILITY = "zero"
CARD_ID = "CCD-zero-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "form", "type": "label", "role": "safe", "domain": {"values": ["exponential", "cosine"]}},
   ],
   notes=(
      "f is e^(x / rate) + x - offset or cos x + rate x - offset, both strictly increasing, so the graph crosses the "
      "x-axis exactly once, between -(offset + 5) and offset + 5. The offset is stepped by one when the key's rounded "
      "and truncated forms agree."
   ),
)

STEPS = (0, 1, 2, 3, 4)

x = sympy.Symbol("x")


def function(names, offset):
   if names["form"] == "exponential":
      return sympy.exp(x / names["rate"]) + x - offset

   return sympy.cos(x) + names["rate"] * x - offset


def build(names):
   def build_variant(step):
      offset = names["offset"] + step
      f_expression = function(names, offset)
      roots = numeric_roots(f_expression, x, -(offset + 5), offset + 5)
      has_one_root = len(roots) == 1
      value_key = roots[0] if has_one_root else sympy.Float("nan")
      exclusion = "root_count" if not has_one_root else first_reason(zero_at_half_integer(value_key), key_exclusion(value_key))
      prompt = (
         f"The graph of {math(f'f(x) = {tex(f_expression)}')} crosses the {math('x')} axis at exactly one point. "
         f"Find the {math('x')} coordinate of that point, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"f(x) = {tex(f_expression)}",
         setup_key=from_sympy(sympy.Eq(f_expression, 0)),
         setup_kind=EQUATION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(f_expression),
         draw=draw_record(names, {"f": function_entry(x, f_expression)}, used_offset=offset),
         exclusion=exclusion,
      )

   return first_clear(STEPS, build_variant)
