"""BC-QA-01004, a zero over zero limit of a quotient of quadratics resolved by factoring."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "top_root", "type": "integer", "role": "safe", "domain": {"min": -7, "max": 7, "step": 1}},
      {"name": "bottom_root", "type": "integer", "role": "safe", "domain": {"min": -7, "max": 7, "step": 1}},
      {"name": "state_form", "type": "label", "role": "difficulty", "domain": {"values": ["silent", "stated"]}},
   ],
   "constraints": [
      "top_root != target",
      "bottom_root != target",
      "top_root != bottom_root",
   ],
   "derived": [],
   "invariants": [
      "limit_value != 0",
      "limit_value != 1",
   ],
   "dial_bindings": [
      {"parameter": "state_form", "difficulty_factor_id": "BC-DF-10", "settings": {"silent": "off", "stated": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["target", "top_root", "bottom_root"]},
   ],
   "notes": "Numerator (x - target)(x - top_root) and denominator (x - target)(x - bottom_root), both expanded. Cancelling the two x squared terms as if they were factors leaves two linear expressions whose values at target are both minus target squared, so that slip always yields 1; the key is never 0 or 1.",
}

x = sympy.Symbol("x")


def build(names):
   target = names["target"]
   top_root = names["top_root"]
   bottom_root = names["bottom_root"]
   is_stated = names["state_form"] == "stated"

   numerator = sympy.expand((x - target) * (x - top_root))
   denominator = sympy.expand((x - target) * (x - bottom_root))
   limit_value = sympy.Rational(target - top_root, target - bottom_root)
   top_tex, bottom_tex = tex(numerator), tex(denominator)
   limit_tex = rf"\lim_{{x \to {target}}} \frac{{{top_tex}}}{{{bottom_tex}}}"
   request = " State the form that substitution produces, and show the work that leads to your answer." if is_stated else ""
   stem = f"Find the exact value of {math(limit_tex)}.{request}"

   reduced = (x - top_root) / (x - bottom_root)
   term_cancelled = rf"\frac{{{tex(numerator - x**2)}}}{{{tex(denominator - x**2)}}}"
   factored = rf"\frac{{{tex((x - target) * (x - top_root))}}}{{{tex((x - target) * (x - bottom_root))}}}"
   value_tex = tex(limit_value)

   steps = [
      Step(text=f"Substituting {math(f'x = {target}')} gives 0 in the numerator and in the denominator, the indeterminate form 0/0.", rule="classify by substitution"),
      Step(text=f"Factoring gives {math(factored)}, and for {math(rf'x \ne {target}')} the common factor cancels, leaving {math(tex(reduced))}.", rule="factor and cancel"),
      Step(text=f"Substituting into the reduced expression, the limit is {math(value_tex)}.", rule="substitution after rewriting"),
   ]

   key_label = f"The limit is {math(value_tex)}, because after the common factor {math(tex(x - target))} cancels, substitution into {math(tex(reduced))} gives that value."
   distractors = [
      Distractor(
         error_path="BC-ERR-01008",
         derivation="the numerator's limit of 0 taken as the value of the whole quotient",
         label=f"The limit is {math('0')}, because the numerator {math(top_tex)} approaches 0 as x approaches {target}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01010",
         derivation="the x squared terms cancelled as though they were common factors, leaving two linear expressions that are equal at the target",
         label=f"The limit is {math('1')}, because cancelling the {math('x^{2}')} terms leaves {math(term_cancelled)}, which equals 1 at {math(f'x = {target}')}.",
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-01009",
         derivation="the indeterminate form 0/0 read as a statement that the limit does not exist",
         label=f"The limit does not exist, because substituting {math(f'x = {target}')} into the quotient gives the form 0/0.",
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
      command_verb="find",
      notes={"limit_value": limit_value},
   )
