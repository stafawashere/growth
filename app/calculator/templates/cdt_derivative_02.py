"""CDT-derivative-02, the rate of change of one velocity component of a particle at a stated time."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, derivative_at, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig,
   key_exclusion, linear_at_point, math, number_text, tex,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-derivative-02"
CAPABILITY = "derivative"
CARD_ID = "CCD-derivative-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "across", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "lift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "moment", "type": "real", "role": "safe", "domain": {"min": 0.5, "max": 3.5, "step": 0.5}},
   ],
   notes=(
      "Velocity components p(t) = across e^(-t / stretch) and q(t) = lift sin(t^2 / stretch) + ln(1 + t); the task "
      "asks for q'(moment). The moment is nudged by tenths when the key's rounded and truncated forms agree."
   ),
)

NUDGES = (0, sympy.Rational(1, 10), sympy.Rational(2, 10), sympy.Rational(3, 10), sympy.Rational(4, 10))

t = sympy.Symbol("t")


def build(names):
   horizontal = names["across"] * sympy.exp(-t / names["stretch"])
   vertical = names["lift"] * sympy.sin(t**2 / names["stretch"]) + sympy.log(1 + t)

   def build_variant(nudge):
      moment = sympy.nsimplify(names["moment"] + nudge)
      setup = sympy.Subs(sympy.Derivative(vertical, t), t, moment)
      value_key = derivative_at(vertical, t, moment)
      exclusion = first_reason(linear_at_point(vertical, t, moment), key_exclusion(value_key))
      moment_text = number_text(moment)
      prompt = (
         f"A particle moves in the plane with velocity vector {math(r'\langle p(t), q(t) \rangle')}, where "
         f"{math(f'p(t) = {tex(horizontal)}')} and {math(f'q(t) = {tex(vertical)}')}. Find "
         f"{math(f"q'({moment_text})")}, the rate at which the vertical component of velocity changes at "
         f"{math(f't = {moment_text}')}, to three decimal places."
      )
      functions = {"p": function_entry(t, horizontal), "q": function_entry(t, vertical)}

      return DrillTask(
         prompt=prompt,
         function_tex=f"p(t) = {tex(horizontal)}, \\quad q(t) = {tex(vertical)}",
         setup_key=from_sympy(setup),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=None,
         radian_sensitive=has_trig(horizontal, vertical),
         draw=draw_record(names, functions, used_moment=moment),
         exclusion=exclusion,
      )

   return first_clear(NUDGES, build_variant)
