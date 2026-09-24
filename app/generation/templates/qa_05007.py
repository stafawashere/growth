"""BC-QA-05007, a critical point of a function given by an accumulation integral or a differential equation."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_d import product_tex

ARCHETYPE_ID = "BC-QA-05007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inside_root", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "range_end", "type": "integer", "role": "safe", "domain": {"values": [5, 6, 7]}},
      {"name": "outside_root", "type": "integer", "role": "safe", "domain": {"values": [-5, -4, -3, -2, -1, 8, 9, 10, 11]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "leading_sign", "type": "integer", "role": "difficulty", "domain": {"values": [1, -1]}},
      {"name": "letters", "type": "label", "role": "safe", "domain": {"values": ["gh", "Fk", "Gp", "fq", "Hr"]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["accumulation", "differential"]}},
   ],
   "constraints": [
      "inside_root < range_end",
   ],
   "derived": [],
   "invariants": [
      "classification in ['relative minimum', 'relative maximum']",
      "outside_root < 0 or outside_root > range_end",
   ],
   "dial_bindings": [
      {"parameter": "leading_sign", "difficulty_factor_id": "BC-DF-12", "settings": {"1": "off", "-1": "low"}},
      {"parameter": "given", "difficulty_factor_id": "BC-DF-02", "settings": {"accumulation": "off", "differential": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["inside_root", "outside_root", "range_end", "leading_sign"]},
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["inside_root", "outside_root", "range_end", "leading_sign"]},
   ],
   "notes": (
      "The derivative is leading_sign * scale (x - inside_root)(x - outside_root) times a factor the stem says is positive, so "
      "on the stated range only inside_root is critical, and the fixed sign of (x - outside_root) there decides the "
      "direction of the sign change."
   ),
}

x = sympy.Symbol("x")
t = sympy.Symbol("t")


def _sign_word(value):
   return "positive" if value > 0 else "negative"


def _classification(left_sign):
   return "relative minimum" if left_sign < 0 else "relative maximum"


def _opposite(kind):
   return "relative maximum" if kind == "relative minimum" else "relative minimum"


def build(names):
   inside = names["inside_root"]
   outside = names["outside_root"]
   range_end = names["range_end"]
   sign = names["leading_sign"]
   function_letter, factor_letter = list(names["letters"])
   scale = names["scale"]
   polynomial = sign * scale * (x - inside) * (x - outside)
   coefficient = str(sign * scale)

   if scale == 1:
      coefficient = "" if sign == 1 else "-"
   factor_tex = coefficient + product_tex(x, [inside, outside])
   integrand_factor_tex = coefficient + product_tex(t, [inside, outside])
   range_text = math(f"0 < x < {range_end}")
   prime = function_letter + "'"

   if names["given"] == "differential":
      derivative_expression = math(r"\frac{dy}{dx} = " + factor_tex + r"\left(y^{2} + 1\right)")
      opening = (
         f"The function {function_letter} is the solution of the differential equation {derivative_expression} with "
         f"{math(f'{function_letter}(0) = 2')}, and {function_letter} is defined for {range_text}."
      )
      positive_factor = math(r"y^{2} + 1")
      representation = "BC-REP-06"
   else:
      integrand = integrand_factor_tex + f"{factor_letter}(t)"
      definition = math(rf"{function_letter}(x) = \int_{{0}}^{{x}} " + integrand + r"\,dt")
      opening = (
         f"The function {factor_letter} is continuous and {math(f'{factor_letter}(t) > 0')} for all t. Let "
         f"{definition} for {range_text}."
      )
      positive_factor = math(f"{factor_letter}(x)")
      representation = "BC-REP-01"

   stem = (
      f"{opening} Find the value of x in {range_text} at which {function_letter} has a critical point, and determine "
      f"whether {function_letter} has a relative minimum, a relative maximum, or neither there. Give a reason for the "
      "answer."
   )

   left_sign = polynomial.subs(x, inside - sympy.Rational(1, 2))
   right_sign = polynomial.subs(x, inside + sympy.Rational(1, 2))
   kind = _classification(left_sign)
   outside_left = polynomial.subs(x, outside - sympy.Rational(1, 2))
   outside_kind = _classification(outside_left)
   change_text = f"changes from {_sign_word(left_sign)} to {_sign_word(right_sign)}"
   outside_side = "less than" if outside < 0 else "greater than"

   key_label = f"At x = {inside} only; {function_letter} has a {kind} there because {prime} {change_text} at x = {inside}."
   steps = [
      Step(
         text=(
            f"{math(f'{prime}(x)')} is {math(factor_tex)} times {positive_factor}, which is positive, so "
            f"{math(f'{prime}(x) = 0')} only where {math(factor_tex + ' = 0')}, at x = {inside} and x = {outside}."
         ),
         point_type_id="BC-PT-99013",
         rule="critical points from the derivative",
      ),
      Step(
         text=f"Only x = {inside} lies in {range_text}; x = {outside} is {outside_side} every x in the range.",
         point_type_id="BC-PT-99005",
         rule="stated range",
      ),
      Step(
         text=(
            f"On the range the factor {math(product_tex(x, [outside]))} keeps one sign, so {prime} {change_text} at x = {inside}, "
            f"and {function_letter} has a {kind} there."
         ),
         point_type_id="BC-PT-99012",
         rule="first derivative test",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05021",
         derivation="the direction of the sign change read the wrong way round in the classification",
         label=f"At x = {inside} only; {function_letter} has a {_opposite(kind)} there because {prime} {change_text} at x = {inside}.",
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-05010",
         derivation=f"the zero x = {outside} of the derivative kept although it lies outside the stated range",
         label=(
            f"At x = {inside} and x = {outside}; {function_letter} has a {kind} at x = {inside} and a {outside_kind} at "
            f"x = {outside} because {prime} changes sign at each."
         ),
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05022",
         derivation="the point classified by the size of the derivative nearby rather than by whether its sign changes",
         label=f"At x = {inside} only; {function_letter} has neither there because {prime} stays close to 0 on both sides of x = {inside}.",
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation=representation,
      calculator_status="no_calculator",
      command_verb="determine",
      notes={"classification": kind},
   )
