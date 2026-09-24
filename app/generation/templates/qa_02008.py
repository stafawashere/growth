"""BC-QA-02008, a quotient of a polynomial and a sine or cosine differentiated by the quotient rule."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "numerator", "type": "label", "role": "difficulty", "domain": {"values": ["linear", "quadratic"]}},
      {"name": "leading", "type": "integer", "role": "safe", "domain": {"min": -7, "max": 7, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -12, "max": 12, "step": 1, "exclude": [0]}},
      {"name": "trig", "type": "label", "role": "safe", "domain": {"values": ["sin", "cos"]}},
      {"name": "angle", "type": "rational", "role": "safe", "domain": {"values": ["1/6", "1/4", "1/3"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "numerator", "difficulty_factor_id": "BC-DF-06", "settings": {"linear": "off", "quadratic": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["numerator", "leading", "constant", "trig", "angle"]},
   ],
   "notes": (
      "h(x) = (leading x^n + constant) / (sine or cosine of x), n = 1 or 2, differentiated and evaluated at pi/6, "
      "pi/4 or pi/3, where the denominator and its derivative are both nonzero. Neither piece is constant and the "
      "quotient does not reduce to a sum of powers. Because pi is transcendental the numerator u'v - uv' is never "
      "0 there, so no option coincides with the key."
   ),
}

x = sympy.Symbol("x")


def _clean(value):
   return sympy.expand(sympy.radsimp(sympy.expand(value)))


def build(names):
   degree = 1 if names["numerator"] == "linear" else 2
   leading = int(names["leading"])
   constant = int(names["constant"])
   trig = sympy.sin if names["trig"] == "sin" else sympy.cos
   point = sympy.pi * sympy.Rational(names["angle"])

   top = leading * x**degree + constant
   bottom = trig(x)
   top_slope = sympy.diff(top, x)
   bottom_slope = sympy.diff(bottom, x)

   u_at = top.subs(x, point)
   v_at = bottom.subs(x, point)
   up_at = top_slope.subs(x, point)
   vp_at = bottom_slope.subs(x, point)
   key_value = _clean((up_at * v_at - u_at * vp_at) / v_at**2)

   point_tex = tex(point)
   stem = (
      f"Let {math(r'h(x) = \frac{' + tex(top) + '}{' + tex(bottom) + '}')}. "
      f"Find the exact value of {math(rf"h'\left({point_tex}\right)")}."
   )

   steps = [
      Step(
         text=(
            f"The numerator is {math('u = ' + tex(top))} with {math("u' = " + tex(top_slope))}, and the denominator is "
            f"{math('v = ' + tex(bottom))} with {math("v' = " + tex(bottom_slope))}."
         ),
         rule="identify the two pieces",
      ),
      Step(
         text=f"By the quotient rule, {math(r"h'(x) = \frac{u'v - uv'}{v^{2}}")}, with u'v first in the numerator.",
         point_type_id="BC-PT-99080",
         rule="quotient rule",
      ),
      Step(
         text=(
            f"At {math('x = ' + point_tex)}: {math(f'u = {tex(u_at)}')}, {math(f"u' = {tex(up_at)}")}, "
            f"{math(f'v = {tex(v_at)}')} and {math(f"v' = {tex(vp_at)}")}, so "
            f"{math(rf"h'\left({point_tex}\right) = {tex(key_value)}")}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="substitute and simplify",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-02021",
         derivation="the numerator written as u v' - u' v, the two terms in reverse order",
         value=_clean((u_at * vp_at - up_at * v_at) / v_at**2),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-02022",
         derivation="the numerator divided by v instead of by v squared",
         value=_clean((up_at * v_at - u_at * vp_at) / v_at),
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-02026",
         derivation="numerator and denominator differentiated separately, u' / v'",
         value=_clean(up_at / vp_at),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
