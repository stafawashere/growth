"""BC-QA-01010, end behaviour at negative infinity of a quotient with a radical, written as a limit and evaluated."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "root_coef", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "linear_coef", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "linear_const", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "inner_const", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "radical_place", "type": "label", "role": "difficulty", "domain": {"values": ["denominator", "numerator"]}},
   ],
   "constraints": [
      "abs(linear_coef) != root_coef",
      "abs(linear_coef) != root_coef**2",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "radical_place", "difficulty_factor_id": "BC-DF-11", "settings": {"denominator": "off", "numerator": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["root_coef", "linear_coef", "linear_const", "inner_const", "radical_place"]},
   ],
   "notes": "The quotient pairs a linear expression with the square root of root_coef^2 x^2 + inner_const, one in the numerator and one in the denominator, and the limit is taken as x decreases without bound, where the square root of x^2 is -x.",
}

x = sympy.Symbol("x")


def build(names):
   root_coef = names["root_coef"]
   linear_coef = names["linear_coef"]
   linear_const = names["linear_const"]
   inner_const = names["inner_const"]
   radical_on_bottom = names["radical_place"] == "denominator"

   linear = linear_coef * x + linear_const
   radical = sympy.sqrt(root_coef**2 * x**2 + inner_const)
   sign_of_linear = sympy.sign(linear_coef)
   reduced_linear_tex = tex(-linear_coef - sympy.Rational(linear_const) / x)
   reduced_radical_tex = tex(sympy.sqrt(root_coef**2 + inner_const / x**2))

   if radical_on_bottom:
      rule_tex = rf"\frac{{{tex(linear)}}}{{{tex(radical)}}}"
      key_value = sympy.Rational(-linear_coef, root_coef)
      unsigned_value = sympy.Rational(linear_coef, root_coef)
      undegreed_value = sympy.Rational(-linear_coef, root_coef**2)
      divided_tex = rf"\frac{{{reduced_linear_tex}}}{{{reduced_radical_tex}}}"
      degree_slip = f"the coefficient {root_coef**2} under the radical used in place of its square root {root_coef}"
   else:
      rule_tex = rf"\frac{{{tex(radical)}}}{{{tex(linear)}}}"
      key_value = sympy.Rational(-root_coef, linear_coef)
      unsigned_value = sympy.Rational(root_coef, linear_coef)
      undegreed_value = sympy.Rational(-root_coef**2, linear_coef)
      divided_tex = rf"\frac{{{reduced_radical_tex}}}{{{reduced_linear_tex}}}"
      degree_slip = f"the coefficient {root_coef**2} under the radical compared with the linear coefficient as if both terms had the same degree"

   substituted_value = -sign_of_linear
   limit_tex = r"\lim_{x \to -\infty} f(x)"
   stem = (
      f"Let {math('f(x) = ' + rule_tex)}. Write a limit expression that describes the behaviour of f as x "
      "decreases without bound, and find the exact value of that limit."
   )

   steps = [
      Step(
         text=f"The behaviour of f as x decreases without bound is described by {math(limit_tex)}.",
         point_type_id="BC-PT-99054",
         rule="limit expression for end behaviour",
      ),
      Step(
         text=(
            f"For x < 0, {math(r'\sqrt{x^{2}} = -x')}, so {math(tex(radical) + ' = -x ' + reduced_radical_tex)}. "
            f"Dividing the numerator and the denominator by {math('-x')} gives {math('f(x) = ' + divided_tex)}."
         ),
         rule="divide by the dominant power, with the sign of x",
      ),
      Step(
         text=(
            f"As x decreases without bound the terms with x in the denominator approach 0, so "
            f"{math(limit_tex + ' = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="limit of each term",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-01024",
         derivation="the square root of x squared taken as x rather than -x for negative x, so the sign of the limit is lost",
         value=unsigned_value,
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-01023",
         derivation=degree_slip,
         value=undegreed_value,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01021",
         derivation="negative infinity substituted into numerator and denominator and the quotient of the two infinities taken as plus or minus 1 by their signs",
         value=substituted_value,
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
