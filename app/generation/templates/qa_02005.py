"""BC-QA-02005, differentiability decided at a point where a fractional power makes a continuous function fail."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "point", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "exponent", "type": "rational", "role": "difficulty", "domain": {"values": ["1/3", "1/5", "3/5", "2/3", "2/5", "4/5", "4/3", "5/3", "7/5", "6/5"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exponent < 1 or 'is differentiable' in key",
      "exponent > 1 or 'is not differentiable' in key",
   ],
   "dial_bindings": [
      {"parameter": "exponent", "difficulty_factor_id": "BC-DF-17", "settings": {"1/3": "low", "1/5": "low", "3/5": "low", "2/3": "medium", "2/5": "medium", "4/5": "medium", "4/3": "low", "5/3": "low", "7/5": "low", "6/5": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["point", "shift", "coefficient", "exponent"]},
   ],
   "notes": "f(x) = coefficient (x - point)^exponent + shift, with the power read as the real odd root. An odd numerator gives a vertical tangent (difference quotients of one sign growing without bound); an even numerator gives a cusp (opposite signs). Exponents above 1 give a difference quotient that tends to 0, so f is differentiable there with a horizontal tangent. f is continuous at point in every draw.",
}

x = sympy.Symbol("x")


def _root_power_tex(base_tex, exponent):
   numerator, denominator = exponent.p, exponent.q
   root = rf"\sqrt[{denominator}]{{{base_tex}}}"

   if numerator == 1:
      return root

   return rf"\left({root}\right)^{{{numerator}}}"


def _differentiable(point, stem, at, quotient_tex, quotient_power, shift, coefficient, exponent):
   derivative_root = _root_power_tex(tex(x - point), sympy.Rational(exponent.p - exponent.q, exponent.q))
   derivative_tex = f"f'(x) = {tex(coefficient * exponent)}{derivative_root}"
   zero_slope = f"f'({point}) = 0"
   steps = [
      Step(text=f"f is continuous at {at}, since {math(f'f({point}) = {shift}')} and the root is continuous everywhere.", rule="continuity of root functions"),
      Step(text=f"The difference quotient is {math(quotient_tex)}, and the exponent {math(tex(quotient_power))} is positive.", rule="difference quotient"),
      Step(text=f"So the difference quotient approaches 0 from both sides, f is differentiable at {at}, and {math(zero_slope)}. The tangent line there is horizontal.", rule="derivative as a limit"),
   ]
   key_label = f"f is differentiable at {at} with {math(zero_slope)}, because the difference quotient approaches 0 from both sides."
   distractors = [
      Distractor(
         error_path="BC-ERR-02012",
         derivation="differentiability concluded from continuity, the implication run backwards, with no slope computed",
         label=f"f is differentiable at {at}, because f is continuous at {at}, and every continuous function is differentiable.",
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-03012",
         derivation="a zero derivative read as a vertical tangent instead of a horizontal one",
         label=f"f is not differentiable at {at}, because {math(derivative_tex)} is 0 there, so the tangent is vertical.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-02013",
         derivation="non-differentiability read off the look of a sketch near the root, with no difference quotient examined",
         label=f"f is not differentiable at {at}, because a sketch of the graph of f shows a sharp point at {at}, where the root is 0.",
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
   )


def build(names):
   point = names["point"]
   shift = names["shift"]
   coefficient = names["coefficient"]
   exponent = sympy.Rational(names["exponent"])
   is_cusp = exponent.p % 2 == 0

   base_tex = tex(x - point)
   power_tex = _root_power_tex(base_tex, exponent)
   leading = {1: "", -1: "-"}.get(coefficient, str(coefficient))
   shift_tex = f" + {shift}" if shift > 0 else (f" - {abs(shift)}" if shift < 0 else "")
   rule_tex = f"f(x) = {leading}{power_tex}{shift_tex}"
   at = math(f"x = {point}")
   stem = f"Let {math(rule_tex)}. Determine whether f is differentiable at {at}, and justify your answer."

   quotient_power = exponent - 1
   quotient_tex = rf"\frac{{f({point} + h) - f({point})}}{{h}} = {leading}h^{{{tex(quotient_power)}}}"
   sign_word = "positive" if coefficient > 0 else "negative"

   if exponent > 1:
      return _differentiable(point, stem, at, quotient_tex, quotient_power, shift, coefficient, exponent)

   if is_cusp:
      behaviour = "grows without bound with opposite signs on the two sides"
      shape = "the graph has a cusp there"
      detail = "Because the power of h has an odd numerator, the quotient has opposite signs for h < 0 and h > 0, and its size grows without bound as h approaches 0."
   else:
      behaviour = f"grows without bound, staying {sign_word}, on both sides"
      shape = "the graph has a vertical tangent there"
      detail = f"Because the power of h has an even numerator, the quotient keeps the sign of {coefficient} on both sides, and its size grows without bound as h approaches 0."

   steps = [
      Step(text=f"f is continuous at {at}, since {math(f'f({point}) = {shift}')} and the root is continuous everywhere.", rule="continuity of root functions"),
      Step(text=f"The difference quotient is {math(quotient_tex)}, and the exponent {math(tex(quotient_power))} is negative.", rule="difference quotient"),
      Step(text=detail, rule="one sided limits of the difference quotient"),
      Step(text=f"The difference quotient has no finite limit, so f is not differentiable at {at}, and {shape}.", rule="derivative as a limit"),
   ]

   key_label = f"f is not differentiable at {at}, because the difference quotient {behaviour}, so {shape}."
   zero_slope_tex = f"f'({point}) = 0"
   distractors = [
      Distractor(
         error_path="BC-ERR-02012",
         derivation="differentiability concluded from continuity, the implication run backwards",
         label=f"f is differentiable at {at}, because f is continuous at {at}, and every continuous function is differentiable.",
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-03012",
         derivation="the zero denominator of the derivative formula read as a horizontal tangent instead of a vertical one",
         label=f"f is differentiable at {at} with {math(zero_slope_tex)}, because the derivative formula has a zero denominator there, so the tangent is horizontal.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-02013",
         derivation="non-differentiability read off the look of a sketch, which suggests a corner, with no difference quotient examined",
         label=f"f is not differentiable at {at}, because a sketch of the graph of f shows a corner at {at}, where two straight pieces meet.",
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
   )
