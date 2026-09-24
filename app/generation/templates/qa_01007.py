"""BC-QA-01007, a discontinuity of a rational function classified from its one sided limits."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01007"
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
      {"name": "target", "type": "label", "role": "difficulty", "domain": {"values": ["removable", "asymptote"]}},
   ],
   "constraints": [
      "cancelled_root != pole",
      "zero != pole",
      "zero != cancelled_root",
   ],
   "derived": [],
   "invariants": [
      "classification in ['removable', 'vertical asymptote']",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-02", "settings": {"factored": "off", "expanded": "medium"}},
      {"parameter": "target", "difficulty_factor_id": "BC-DF-10", "settings": {"removable": "low", "asymptote": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["coefficient", "cancelled_root", "pole", "zero", "form", "target"]},
   ],
   "notes": "f(x) = coefficient (x - cancelled_root)(x - zero) / ((x - cancelled_root)(x - pole)^2). The break at cancelled_root is removable; the squared factor makes f tend to the same infinity on both sides of pole, which is what a student who reads an infinite limit as an existing one relies on.",
}

x = sympy.Symbol("x")


def build(names):
   coefficient = names["coefficient"]
   cancelled_root = names["cancelled_root"]
   pole = names["pole"]
   zero = names["zero"]
   is_removable = names["target"] == "removable"

   numerator = coefficient * (x - cancelled_root) * (x - zero)
   denominator = (x - cancelled_root) * (x - pole) ** 2

   if names["form"] == "expanded":
      rule_tex = rf"\frac{{{tex(sympy.expand(numerator))}}}{{{tex(sympy.expand(denominator))}}}"
   else:
      rule_tex = rf"\frac{{{tex(numerator)}}}{{{tex(denominator)}}}"

   point = cancelled_root if is_removable else pole
   at = math(f"x = {point}")
   stem = (
      f"Let {math('f(x) = ' + rule_tex)}. Determine whether f is continuous at {at}. If it is not, classify the "
      "discontinuity as removable, a jump, or a vertical asymptote. Justify your answer."
   )

   reduced = coefficient * (x - zero) / (x - pole) ** 2
   steps = [
      Step(
         text=f"Factor and divide out the common factor: for {math(rf'x \ne {cancelled_root}')}, {math('f(x) = ' + tex(reduced))}.",
         rule="factor and cancel",
      ),
   ]

   if is_removable:
      limit_value = reduced.subs(x, cancelled_root)
      steps.append(Step(
         text=f"The reduced expression is continuous at {at}, so {math(rf'\lim_{{x \to {point}}} f(x) = {tex(limit_value)}')}, a finite number, while f({point}) is undefined.",
         rule="limit of the reduced expression",
      ))
      steps.append(Step(text="The limit exists but f has no value there, so the discontinuity is removable.", rule="classification from the limit"))
      classification = "removable"
      key_label = f"The discontinuity at {at} is removable, because the limit of f(x) there is a finite number."
      distractors = [
         Distractor(
            error_path="BC-ERR-01018",
            derivation="the zero of the original denominator named an asymptote although its factor divides out",
            label=f"The discontinuity at {at} is a vertical asymptote, because the denominator of f is 0 there.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01003",
            derivation="the limit declared nonexistent because f is undefined at the input, so the break called a jump",
            label=f"The discontinuity at {at} is a jump, because f is undefined there so the limit does not exist.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01015",
            derivation="agreeing one sided limits taken as continuity, with the missing value ignored",
            label=f"There is no discontinuity at {at}, because the limits from the left and from the right are equal.",
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      numerator_sign = sympy.sign(coefficient * (pole - zero))
      infinity_tex = r"\infty" if numerator_sign > 0 else r"-\infty"
      steps.append(Step(
         text=(
            f"Near {at} the numerator of the reduced expression approaches {coefficient * (pole - zero)} and "
            f"the denominator approaches 0 through positive values, so {math(rf'\lim_{{x \to {point}}} f(x) = {infinity_tex}')}."
         ),
         rule="sign analysis of the reduced quotient",
      ))
      steps.append(Step(text="f is unbounded near the input, so the discontinuity is a vertical asymptote.", rule="classification from the limit"))
      classification = "vertical asymptote"
      key_label = f"The discontinuity at {at} is a vertical asymptote, because f(x) is unbounded as x approaches {point}."
      distractors = [
         Distractor(
            error_path="BC-ERR-01020",
            derivation="the statement that the limit is infinite read as saying the limit exists, so the break called removable",
            label=f"The discontinuity at {at} is removable, because the limit of f(x) there exists and equals {math(infinity_tex)}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01003",
            derivation="the limit declared nonexistent because f is undefined at the input, so the break called a jump",
            label=f"The discontinuity at {at} is a jump, because f is undefined there so the limit does not exist.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01015",
            derivation="agreeing one sided limits, both infinite, taken as continuity",
            label=f"There is no discontinuity at {at}, because the limits from the left and from the right are equal.",
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
      command_verb="classify",
      notes={"classification": classification},
   )
