"""BC-QA-01009, the vertical asymptote of a rational function located after cancelling, with its one sided infinite limits."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "cancelled_root", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "pole", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "zero", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["factored", "expanded"]}},
   ],
   "constraints": [
      "cancelled_root != pole",
      "zero != pole",
      "zero != cancelled_root",
   ],
   "derived": [],
   "invariants": [
      "'Only' in key",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-02", "settings": {"factored": "low", "expanded": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["coefficient", "cancelled_root", "pole", "zero", "form"]},
   ],
   "notes": "f(x) = coefficient (x - cancelled_root)(x - zero) / ((x - cancelled_root)(x - pole)). The factor at cancelled_root divides out, leaving one simple pole, so the one sided limits there are infinite with opposite signs.",
}

x = sympy.Symbol("x")


def build(names):
   coefficient = names["coefficient"]
   cancelled_root = names["cancelled_root"]
   pole = names["pole"]
   zero = names["zero"]

   numerator = coefficient * (x - cancelled_root) * (x - zero)
   denominator = (x - cancelled_root) * (x - pole)

   if names["form"] == "expanded":
      rule_tex = rf"\frac{{{tex(sympy.expand(numerator))}}}{{{tex(sympy.expand(denominator))}}}"
   else:
      rule_tex = rf"\frac{{{tex(numerator)}}}{{{tex(denominator)}}}"

   reduced = coefficient * (x - zero) / (x - pole)
   numerator_at_pole = coefficient * (pole - zero)
   right_tex = r"\infty" if numerator_at_pole > 0 else r"-\infty"
   left_tex = r"-\infty" if numerator_at_pole > 0 else r"\infty"
   left_limit = rf"\lim_{{x \to {pole}^{{-}}}} f(x) = {left_tex}"
   right_limit = rf"\lim_{{x \to {pole}^{{+}}}} f(x) = {right_tex}"
   pole_line = math(f"x = {pole}")
   cancelled_line = math(f"x = {cancelled_root}")

   stem = (
      f"Let {math('f(x) = ' + rule_tex)}. Find every vertical asymptote of the graph of f, and state the one sided "
      "limits of f at each one."
   )

   steps = [
      Step(
         text=f"Factor and cancel: for {math(rf'x \ne {cancelled_root}')}, {math('f(x) = ' + tex(reduced))}. The factor at {cancelled_line} divides out, so that break is removable, with no asymptote.",
         rule="factor and cancel",
      ),
      Step(
         text=f"The remaining denominator is 0 only at {pole_line}, where the numerator of the reduced expression is {numerator_at_pole}, not 0.",
         rule="zeros of the reduced denominator",
      ),
      Step(
         text=f"The denominator {math(tex(x - pole))} is negative just left of {pole} and positive just right of it, so {math(left_limit)} and {math(right_limit)}.",
         rule="sign of the quotient on each side",
      ),
   ]

   both_sides = f"{math(left_limit)} and {math(right_limit)}"
   key_label = f"Only {pole_line} is a vertical asymptote, with {both_sides}."
   distractors = [
      Distractor(
         error_path="BC-ERR-01018",
         derivation="a vertical asymptote named at the zero of the denominator whose factor divides out",
         label=f"Both {cancelled_line} and {pole_line} are vertical asymptotes, with {both_sides}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01019",
         derivation="one two sided infinite limit written although the two sides have opposite signs",
         label=f"Only {pole_line} is a vertical asymptote, with {math(rf'\lim_{{x \to {pole}}} f(x) = {right_tex}')} from both sides.",
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-01020",
         derivation="the infinite one sided limit read as an existing limit, so no asymptote is recognised",
         label=f"No line is a vertical asymptote, because {math(right_limit)} is a limit that exists at {pole_line}.",
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
   )
