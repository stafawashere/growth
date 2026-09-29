"""What a calculator drill template builds from one draw, and the helpers the templates share on
top of app/generation/kit.py (docs/calculator/architecture.md, Drill templates).

Every key is a numerical evaluation, the way the calculator gets it: quadrature for integrals,
root finding for zeros and intersections, differentiation evaluated at the point for derivatives.
"""
from dataclasses import dataclass
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal

import sympy

from app.generation.kit import math, numeric_integral, numeric_roots, tex
from app.generation.spec import serialise
from app.items.mathjson import from_sympy

__all__ = [
   "EQUATION",
   "EXPRESSION",
   "DrillTask",
   "derivative_at",
   "draw_record",
   "first_clear",
   "first_reason",
   "function_entry",
   "drill_spec",
   "has_trig",
   "is_trivial_key",
   "key_float",
   "key_exclusion",
   "linear_at_point",
   "linear_integrand",
   "lattice_point",
   "math",
   "number_text",
   "numeric_integral",
   "numeric_roots",
   "rounded_and_truncated",
   "setup_latex",
   "tex",
   "value_at",
   "zero_at_half_integer",
]

KEY_DIGITS = 20
EVALUATION_DIGITS = 30
THREE_PLACES = Decimal("0.001")
MIN_NONZERO_DECIMALS = 3
LATTICE_TOLERANCE = 1e-9

EXPRESSION = "expression"
EQUATION = "equation"


@dataclass(frozen=True)
class DrillTask:
   prompt: str
   function_tex: str
   setup_key: object
   setup_kind: str
   value_key: sympy.Float
   unit: str | None
   radian_sensitive: bool
   draw: dict
   exclusion: str | None


def drill_spec(parameters, notes, constraints=(), derived=()):
   """A spec dict in the shape app/generation/spec.py draws from and the archetype schema accepts.
   A drill has no dials and no figure, so those parts are empty or plain."""
   return {
      "spec_version": "1",
      "evidence_tag": "inferred",
      "parameters": parameters,
      "constraints": list(constraints),
      "derived": list(derived),
      "invariants": ["finite(key)", "nondegenerate_three_decimals(key)"],
      "dial_bindings": [],
      "calculator_guard": None,
      "representation_bindings": [
         {"representation": "BC-REP-01", "figure_kind": None, "requires": [parameter["name"] for parameter in parameters]},
      ],
      "notes": notes,
   }


def key_float(value):
   return sympy.Float(sympy.N(value, EVALUATION_DIGITS), KEY_DIGITS)


def derivative_at(expression, variable, point):
   slope = sympy.diff(expression, variable).subs(variable, point)

   return key_float(slope)


def value_at(expression, variable, point):
   return key_float(expression.subs(variable, point))


def _exact_decimal(key):
   return Decimal(str(sympy.Float(key, KEY_DIGITS)))


def _three_place_text(value):
   if value == 0:
      return "0.000"

   return format(value, "f")


def rounded_and_truncated(key):
   """The two three-place forms the scoring guideline accepts, from the 20-digit key's decimal
   text so no binary float ever decides a digit."""
   exact = _exact_decimal(key)
   rounded = exact.quantize(THREE_PLACES, rounding=ROUND_HALF_UP)
   truncated = exact.quantize(THREE_PLACES, rounding=ROUND_DOWN)

   return _three_place_text(rounded), _three_place_text(truncated)


def is_trivial_key(key):
   """True when the drill could not tell rounding from truncation for this key."""
   rounded, truncated = rounded_and_truncated(key)
   forms_coincide = rounded == truncated
   decimals = format(_exact_decimal(key), "f").partition(".")[2]
   nonzero_decimals = sum(1 for digit in decimals if digit != "0")
   too_few_decimals = nonzero_decimals < MIN_NONZERO_DECIMALS

   return forms_coincide or too_few_decimals


def key_exclusion(key):
   is_finite = sympy.Float(key).is_finite

   if not is_finite:
      return "key_not_finite"

   if is_trivial_key(key):
      return "key_trivial"

   return None


def linear_integrand(integrand, variable):
   is_polynomial = integrand.is_polynomial(variable)
   is_linear = is_polynomial and sympy.degree(integrand, variable) <= 1

   return "integrand_linear" if is_linear else None


def linear_at_point(expression, variable, point):
   is_polynomial = expression.is_polynomial(variable)
   is_linear = is_polynomial and sympy.degree(expression, variable) <= 1

   return "linear_at_point" if is_linear else None


def _near_integer(value):
   number = float(value)

   return abs(number - round(number)) < LATTICE_TOLERANCE


def zero_at_half_integer(root):
   return "zero_at_half_integer" if _near_integer(2 * root) else None


def lattice_point(x_value, y_value):
   on_lattice = _near_integer(x_value) and _near_integer(y_value)

   return "lattice_intersection" if on_lattice else None


def first_reason(*reasons):
   return next((reason for reason in reasons if reason is not None), None)


def first_clear(variants, build_variant):
   """The task for the first variant no exclusion rejects, or the last one tried.

   A template varies one parameter in small steps because about half of all real keys have a
   fourth decimal below 5, where rounding and truncation agree; trying a few neighbours keeps the
   template's rejection rate well under half without widening its draw.
   """
   task = None

   for variant in variants:
      task = build_variant(variant)

      if task.exclusion is None:
         return task

   return task


def function_entry(variable, expression):
   return {"variable": variable.name, "expression": from_sympy(expression)}


def draw_record(names, functions, **chosen):
   """The draw as JSON: the spec's names, the values a variant settled on, and the named
   functions the prompt defines, so a typed setup that uses f(x) can be read against them."""
   record = serialise(names)
   record.update(serialise(chosen))
   record["functions"] = functions

   return record


def has_trig(*expressions):
   trig_heads = (sympy.sin, sympy.cos, sympy.tan, sympy.sec, sympy.csc, sympy.cot)

   return any(expression.has(*trig_heads) for expression in expressions)


def _is_terminating(number):
   denominator = int(number.q)

   for factor in (2, 5):
      while denominator % factor == 0:
         denominator //= factor

   return number.is_Rational and not number.is_Integer and denominator == 1


def _bounds(expression):
   for integral in expression.atoms(sympy.Integral):
      for limit in integral.limits:
         yield from limit[1:]

   for substitution in expression.atoms(sympy.Subs):
      yield from substitution.point


def setup_latex(expression):
   """LaTeX for a setup with drawn bounds and points printed as decimals, t = 2.1 rather than
   21/10, while coefficients such as x/2 keep their fraction."""
   decimals = {
      bound: sympy.Float(number_text(bound), 15)
      for bound in _bounds(expression)
      if isinstance(bound, sympy.Rational) and _is_terminating(bound)
   }

   return tex(expression.xreplace(decimals))


def number_text(value):
   """A drawn number as the prompt prints it: 2.35 rather than 47/20."""
   number = sympy.nsimplify(value)

   if number.is_Integer:
      return str(int(number))

   return format(Decimal(str(sympy.Float(number, KEY_DIGITS))).normalize(), "f")
