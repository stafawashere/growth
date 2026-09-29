"""CDT-derivative-01, the rate of change of a logistic model at a stated time."""
import sympy

from app.calculator.kit import (
   EXPRESSION, DrillTask, derivative_at, draw_record, drill_spec, first_clear, first_reason, function_entry, has_trig,
   key_exclusion, linear_at_point, math, number_text, tex,
)
from app.items.mathjson import from_sympy

TEMPLATE_ID = "CDT-derivative-01"
CAPABILITY = "derivative"
CARD_ID = "CCD-derivative-01"
TEMPLATE_VERSION = 1

SPEC = drill_spec(
   parameters=[
      {"name": "capacity", "type": "integer", "role": "safe", "domain": {"min": 200, "max": 900, "step": 100}},
      {"name": "spread", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 9, "step": 1}},
      {"name": "growth", "type": "rational", "role": "safe", "domain": {"values": ["3/10", "2/5", "1/2", "3/5", "7/10"]}},
      {"name": "moment", "type": "real", "role": "safe", "domain": {"min": 1.5, "max": 6, "step": 0.5}},
   ],
   notes=(
      "P(t) = capacity / (1 + spread e^(-growth t)) fish, asked for P'(moment) in fish per year. The moment is nudged "
      "by tenths when the key's rounded and truncated forms agree."
   ),
)

UNIT = "fish per year"
NUDGES = (0, sympy.Rational(1, 10), sympy.Rational(2, 10), sympy.Rational(3, 10), sympy.Rational(4, 10))

t = sympy.Symbol("t")


def build(names):
   growth = sympy.nsimplify(names["growth"])
   model = names["capacity"] / (1 + names["spread"] * sympy.exp(-growth * t))

   def build_variant(nudge):
      moment = sympy.nsimplify(names["moment"] + nudge)
      setup = sympy.Subs(sympy.Derivative(model, t), t, moment)
      value_key = derivative_at(model, t, moment)
      exclusion = first_reason(linear_at_point(model, t, moment), key_exclusion(value_key))
      moment_text = number_text(moment)
      prompt = (
         f"A lake is stocked with fish, and {math(f'P(t) = {tex(model)}')} models the number of fish "
         f"{math('t')} years later. Find {math(f"P'({moment_text})")}, in fish per year, to three decimal places."
      )

      return DrillTask(
         prompt=prompt,
         function_tex=f"P(t) = {tex(model)}",
         setup_key=from_sympy(setup),
         setup_kind=EXPRESSION,
         value_key=value_key,
         unit=UNIT,
         radian_sensitive=has_trig(model),
         draw=draw_record(names, {"P": function_entry(t, model)}, used_moment=moment),
         exclusion=exclusion,
      )

   return first_clear(NUDGES, build_variant)
