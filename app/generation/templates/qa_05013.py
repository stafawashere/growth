"""BC-QA-05013, the second derivative test at a critical point, beside an input that is not critical."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_d import product_tex

ARCHETYPE_ID = "BC-QA-05013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "first_root", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 3, "step": 1}},
      {"name": "second_root", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "other_input", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "tested_root", "type": "label", "role": "safe", "domain": {"values": ["first", "second"]}},
      {"name": "leading_sign", "type": "integer", "role": "safe", "domain": {"values": [1, -1]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "letter", "type": "label", "role": "safe", "domain": {"values": ["f", "g", "h"]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["derivative", "function"]}},
   ],
   "constraints": [
      "first_root < second_root",
      "other_input != first_root and other_input != second_root",
      "2 * other_input != first_root + second_root",
   ],
   "derived": [],
   "invariants": [
      "classification in ['relative maximum', 'relative minimum']",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-01", "settings": {"derivative": "off", "function": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["first_root", "second_root", "other_input", "given"]},
   ],
   "notes": (
      "The derivative is 6 * leading_sign * (x - first_root)(x - second_root), so one root is a relative maximum and the "
      "other a relative minimum. other_input is neither a root nor the zero of the second derivative, so the second "
      "derivative has a sign there that a response applying the test at a non-critical input would read."
   ),
}

x = sympy.Symbol("x")


def _kind(second_value):
   return "relative minimum" if second_value > 0 else "relative maximum"


def _opposite(kind):
   return "relative maximum" if kind == "relative minimum" else "relative minimum"


def _sign_text(value):
   return ">" if value > 0 else "<"


def build(names):
   letter = names["letter"]
   first_root = names["first_root"]
   second_root = names["second_root"]
   other = names["other_input"]
   critical = first_root if names["tested_root"] == "first" else second_root
   sign = names["leading_sign"]

   derivative = 6 * sign * (x - first_root) * (x - second_root)
   function = sympy.expand(sympy.integrate(derivative, x) + names["constant"])
   second = sympy.diff(derivative, x)
   second_at_critical = second.subs(x, critical)
   second_at_other = second.subs(x, other)
   first_at_other = derivative.subs(x, other)
   kind = _kind(second_at_critical)
   absolute_kind = kind.replace("relative", "absolute")

   prime = letter + "'"
   double_prime = letter + "''"
   first_zero = math(f"{prime}({critical}) = 0")
   critical_sign = math(f"{double_prime}({critical}) = {second_at_critical} {_sign_text(second_at_critical)} 0")
   other_nonzero = math(f"{prime}({other}) = {first_at_other}" + r" \ne 0")
   other_sign = math(f"{double_prime}({other}) = {second_at_other} {_sign_text(second_at_other)} 0")

   if names["given"] == "function":
      opening = f"Let {math(f'{letter}(x) = {tex(function)}')}."
   else:
      factors = product_tex(x, [first_root, second_root])
      coefficient = "6" if sign == 1 else "-6"
      opening = f"A function {letter} has derivative {math(f'{prime}(x) = {coefficient}' + factors)}."

   stem = (
      f"{opening} Using the second derivative test where it applies, determine whether {letter} has a relative "
      f"maximum, a relative minimum, or neither at {math(f'x = {critical}')} and at {math(f'x = {other}')}."
   )

   def statement(critical_claim, other_claim):
      return f"At {math(f'x = {critical}')}, {letter} has {critical_claim}; at {math(f'x = {other}')}, {letter} has {other_claim}."

   key_label = statement(f"a {kind} because {first_zero} and {critical_sign}", f"no relative extremum because {other_nonzero}")

   steps = []

   if names["given"] == "function":
      steps.append(Step(
         text=f"Differentiate: {math(f'{prime}(x) = {tex(sympy.expand(derivative))}')}, which factors as {math(f'{prime}(x) = {tex(sympy.factor(derivative))}')}.",
         rule="power rule",
      ))

   steps += [
      Step(
         text=f"{first_zero}, so {math(f'x = {critical}')} is a critical point, while {other_nonzero}, so {math(f'x = {other}')} is not.",
         rule="critical points are zeros of the first derivative",
      ),
      Step(
         text=f"{math(f'{double_prime}(x) = {tex(second)}')}, and {critical_sign}.",
         value=second_at_critical,
         rule="second derivative evaluated at the critical point",
      ),
      Step(
         text=(
            f"By the second derivative test {letter} has a {kind} at {math(f'x = {critical}')}. At {math(f'x = {other}')} "
            f"the first derivative is not zero, so {letter} has no relative extremum there and the test does not apply."
         ),
         rule="second derivative test",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05036",
         derivation=f"the second derivative test also applied at x = {other}, where the first derivative is not zero, and the sign of the second derivative there read as a classification",
         label=statement(f"a {kind} because {first_zero} and {critical_sign}", f"a {_kind(second_at_other)} because {other_sign}"),
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05037",
         derivation="the sign convention of the test reversed, so a negative second derivative is read as a minimum and a positive one as a maximum",
         label=statement(f"a {_opposite(kind)} because {first_zero} and {critical_sign}", f"no relative extremum because {other_nonzero}"),
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-05039",
         derivation="the relative extremum from the second derivative test extended to an absolute one with no argument that it is the only critical point, which it is not",
         label=statement(f"an {absolute_kind} because {first_zero} and {critical_sign}", f"no relative extremum because {other_nonzero}"),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="determine",
      notes={"classification": kind},
   )
