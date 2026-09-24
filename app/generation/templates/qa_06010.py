"""BC-QA-06010, an antiderivative of a rational function by decomposition into linear partial fractions."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "degree", "type": "label", "role": "difficulty", "domain": {"values": ["proper", "improper"]}},
      {"name": "leading", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4, 5]}},
      {"name": "first_shift", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "second_shift", "type": "integer", "role": "safe", "domain": {"values": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}},
      {"name": "weight", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
   ],
   "constraints": [
      "leading * second_shift != first_shift",
      "gcd(leading, first_shift) == 1",
      "(first_shift >= 0 and second_shift <= -1) or (first_shift <= -leading and second_shift >= 1)",
      "-second_shift >= 2 or -first_shift >= 2 * leading",
   ],
   "derived": [
      {"name": "numerator_constant", "expression": "weight * (leading * second_shift - first_shift)"},
   ],
   "invariants": [
      "exact(key)",
      "numerator_constant != 0",
   ],
   "dial_bindings": [
      {"parameter": "degree", "difficulty_factor_id": "BC-DF-08", "settings": {"proper": "off", "improper": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["degree", "leading", "first_shift", "second_shift", "weight"]},
   ],
   "notes": "The denominator is (p x + a)(x + b) with p from 2 to 5, p and a coprime, and distinct roots; the numerator constant N = m (p b - a) makes the decomposition m p / (p x + a) - m / (x + b), with integer constants. The improper form adds the denominator to the numerator, so division leaves 1 plus the same proper fraction. The leading coefficient p is never 1, so dropping the 1/p from the first logarithm always changes the answer. One root is at most 0 and the other at least 1, so the two linear factors have opposite signs on (0, 1) and the answer without absolute values is not the same real function there. The positive root is at least 2, so the dropped absolute value also shows between 1.1 and 2, where tools/key_recheck.py samples.",
}

x = sympy.Symbol("x")


def build(names):
   leading = int(names["leading"])
   first_shift = int(names["first_shift"])
   second_shift = int(names["second_shift"])
   weight = int(names["weight"])
   numerator_constant = int(names["numerator_constant"])
   is_improper = names["degree"] == "improper"

   first_factor = leading * x + first_shift
   second_factor = x + second_shift
   denominator = sympy.expand(first_factor * second_factor)
   first_constant = weight * leading
   second_constant = -weight
   decomposition = first_constant / first_factor + second_constant / second_factor

   first_log = sympy.log(sympy.Abs(first_factor))
   second_log = sympy.log(sympy.Abs(second_factor))
   bare_first_log = sympy.log(first_factor)
   bare_second_log = sympy.log(second_factor)
   polynomial_part = x if is_improper else sympy.Integer(0)

   key_value = polynomial_part + weight * first_log - weight * second_log
   numerator = denominator + numerator_constant if is_improper else sympy.Integer(numerator_constant)
   proper_part = numerator_constant / denominator
   integrand_tex = rf"\frac{{{tex(numerator)}}}{{{tex(denominator)}}}" if is_improper else tex(proper_part)
   stem = f"Find the indefinite integral {math(r'\int ' + integrand_tex + r'\,dx')}."

   steps = []

   if is_improper:
      steps.append(Step(
         text=(
            "The numerator and denominator both have degree 2, so divide first: "
            f"{math(integrand_tex + ' = ' + tex(1 + proper_part))}."
         ),
         rule="polynomial division before decomposition",
      ))

   steps.extend([
      Step(
         text=(
            f"Factor the denominator as {math(rf'\left({tex(first_factor)}\right)\left({tex(second_factor)}\right)')} and write "
            f"{math(tex(proper_part) + rf' = \frac{{A}}{{{tex(first_factor)}}} + \frac{{B}}{{{tex(second_factor)}}}')}. "
            f"Clearing denominators and substituting {math(f'x = {tex(sympy.Rational(-first_shift, leading))}')} and "
            f"{math(f'x = {-second_shift}')} gives {math(f'A = {first_constant}')} and {math(f'B = {second_constant}')}."
         ),
         value=polynomial_part + decomposition,
         point_type_id="BC-PT-99081",
         rule="partial fraction decomposition",
      ),
      Step(
         text=(
            f"Antidifferentiate each term, dividing by the leading coefficient {leading} for the first: the integral is "
            f"{math(tex(key_value) + ' + C')}."
         ),
         value=key_value,
         point_type_id="BC-PT-99003",
         rule="antiderivative of 1 over a linear factor",
      ),
   ])

   if is_improper:
      distractors = [
         Distractor(
            error_path="BC-ERR-06026",
            derivation="the improper fraction decomposed directly; the constants come out the same but the polynomial part x from the division is lost",
            value=weight * first_log - weight * second_log,
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the reciprocal 1/{leading} that d(u) = {leading} dx introduces dropped from the first logarithm",
            value=polynomial_part + first_constant * first_log - weight * second_log,
            mechanism="chain_rule_omitted",
         ),
         Distractor(
            error_path="BC-ERR-07030",
            derivation="the absolute values removed from both logarithms with no sign check",
            value=polynomial_part + weight * bare_first_log - weight * bare_second_log,
            mechanism="algebra_slip",
         ),
      ]
   else:
      distractors = [
         Distractor(
            error_path="BC-ERR-06019",
            derivation=f"the reciprocal 1/{leading} that d(u) = {leading} dx introduces dropped from the first logarithm",
            value=first_constant * first_log - weight * second_log,
            mechanism="chain_rule_omitted",
         ),
         Distractor(
            error_path="BC-ERR-07030",
            derivation="the absolute values removed from both logarithms with no sign check",
            value=weight * bare_first_log - weight * bare_second_log,
            mechanism="algebra_slip",
         ),
         Distractor(
            error_path="BC-ERR-06022",
            derivation="no decomposition: 1 over each linear factor antidifferentiated separately and the two logarithms multiplied",
            value=sympy.Rational(numerator_constant, leading) * first_log * second_log,
            mechanism="product_rule_omitted",
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
