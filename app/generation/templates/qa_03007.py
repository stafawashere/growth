"""BC-QA-03007, the derivative of a power times an inverse trigonometric function of an inner expression."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-03007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "family", "type": "label", "role": "safe", "domain": {"values": ["arctan", "arcsin"]}},
      {"name": "inner", "type": "label", "role": "difficulty", "domain": {"values": ["linear", "quadratic"]}},
      {"name": "slope", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "sign", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
   ],
   "constraints": [
      "family == 'arcsin' or abs(at) != 1",
      "inner == 'linear' or abs(at) <= 2",
   ],
   "derived": [
      {"name": "inner_value", "expression": "sign if family == 'arctan' else sign / 2"},
   ],
   "invariants": [
      "exact(key)",
      "finite(key)",
   ],
   "dial_bindings": [
      {"parameter": "inner", "difficulty_factor_id": "BC-DF-02", "settings": {"linear": "off", "quadratic": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["family", "inner", "slope", "at", "coefficient", "power", "sign"]},
   ],
   "notes": (
      "h(x) = coefficient x^power F(u(x)), where F is the inverse tangent or inverse sine and the inner "
      "expression u is slope x + b or slope x^2 + b, with b chosen so that u equals plus or minus 1 (inverse "
      "tangent) or plus or minus one half (inverse sine) at the requested input. The inverse tangent excludes "
      "inputs of size 1, where the unsubstituted formula would agree with the correct one."
   ),
}

x = sympy.Symbol("x")


def _tex(expression):
   return sympy.latex(expression, inv_trig_style="full", ln_notation=True)


def _arctan_slope(u):
   return 1 / (1 + u**2)


def _arcsin_slope(u):
   return 1 / sympy.sqrt(1 - u**2)


def build(names):
   is_arctan = names["family"] == "arctan"
   is_quadratic = names["inner"] == "quadratic"
   slope = int(names["slope"])
   at = int(names["at"])
   coefficient = int(names["coefficient"])
   power = int(names["power"])
   sign = int(names["sign"])

   inner_value = sympy.Integer(sign) if is_arctan else sympy.Rational(sign, 2)
   inner_degree = 2 if is_quadratic else 1
   shift = inner_value - slope * at**inner_degree
   inner = slope * x**inner_degree + shift
   inner_slope = sympy.diff(inner, x).subs(x, at)

   if is_arctan:
      outer = sympy.atan
      formula = _arctan_slope
      unsubstituted = 1 / (1 + sympy.Integer(at) ** 2)
      unsubstituted_text = "the formula written with x in place of the inner expression, 1 / (1 + x^2)"
      formula_tex = r"\frac{d}{du}\arctan u = \frac{1}{1 + u^{2}}"
   else:
      outer = sympy.asin
      formula = _arcsin_slope
      unsubstituted = 1 / sympy.sqrt(1 - inner_value)
      unsubstituted_text = "the inner expression left unsquared under the radical, 1 / sqrt(1 - u)"
      formula_tex = r"\frac{d}{du}\arcsin u = \frac{1}{\sqrt{1 - u^{2}}}"

   power_factor = sympy.Integer(at) ** power
   power_slope = power * sympy.Integer(at) ** (power - 1)
   outer_value = outer(inner_value)
   outer_slope = formula(inner_value)

   shown_outer = outer(inner, evaluate=False)
   function = coefficient * x**power * shown_outer
   product_term = coefficient * power_slope * outer_value
   chain_term = coefficient * power_factor * outer_slope * inner_slope
   key_value = sympy.expand(product_term + chain_term)

   stem = f"Let {math('h(x) = ' + _tex(function))}. Find the exact value of {math(f"h'({at})")}."

   derivative = coefficient * sympy.diff(x**power, x) * shown_outer + coefficient * x**power * formula(inner) * sympy.diff(inner, x)
   if chain_term.could_extract_minus_sign():
      unsimplified = f"{_tex(product_term)} - {_tex(-chain_term)}"
   else:
      unsimplified = f"{_tex(product_term)} + {_tex(chain_term)}"

   simplified = _tex(key_value)
   evaluation = unsimplified if unsimplified == simplified else f"{unsimplified} = {simplified}"

   steps = [
      Step(
         text=(
            f"The inner expression is {math('u = ' + _tex(inner))}, with {math(f"u' = {_tex(sympy.diff(inner, x))}")}, "
            f"and {math(formula_tex)}."
         ),
         rule="inverse trigonometric derivative with the chain rule",
      ),
      Step(
         text=(
            f"By the product rule and the chain rule, {math("h'(x) = " + _tex(derivative))}."
         ),
         rule="product rule",
      ),
      Step(
         text=(
            f"At x = {at}, {math(f'u = {_tex(inner_value)}')} and {math(f"u' = {_tex(inner_slope)}")}, so "
            f"{math(f"h'({at}) = {evaluation}")}."
         ),
         value=key_value,
         rule="evaluate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03006",
         derivation="the power factor held constant, so only the inverse trigonometric factor is differentiated",
         value=sympy.expand(chain_term),
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03017",
         derivation="the derivative formula recalled with the wrong sign, the cofunction's formula in its place",
         value=sympy.expand(product_term + coefficient * power_factor * (-formula(inner_value)) * inner_slope),
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-03018",
         derivation=unsubstituted_text,
         value=sympy.expand(product_term + coefficient * power_factor * unsubstituted * inner_slope),
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
