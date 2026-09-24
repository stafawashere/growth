"""BC-QA-01014, the procedure a limit calls for, chosen from the form the drawn expression takes."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "top_root", "type": "integer", "role": "safe", "domain": {"min": -7, "max": 7, "step": 1}},
      {"name": "bottom_root", "type": "integer", "role": "safe", "domain": {"min": -7, "max": 7, "step": 1}},
      {"name": "root_value", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "lead_top", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "lead_bottom", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["factor", "conjugate", "complex_fraction", "infinite", "at_infinity"]}},
      {"name": "pole_power", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2]}},
   ],
   "constraints": [
      "top_root != bottom_root",
      "bottom_root != target",
      "top_root != target",
      "form != 'at_infinity' or lead_top != lead_bottom",
   ],
   "derived": [],
   "invariants": [
      "', which ' in key",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-01", "settings": {"factor": "off", "conjugate": "low", "complex_fraction": "low", "infinite": "low", "at_infinity": "low"}},
      {"parameter": "pole_power", "difficulty_factor_id": "BC-DF-01", "settings": {"1": "low", "2": "off"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["target", "top_root", "bottom_root", "root_value", "lead_top", "lead_bottom", "form", "pole_power"]},
   ],
   "notes": "The form decides the procedure. factor, conjugate and complex_fraction give 0/0 at the target and call for the named rewriting. infinite is (x - top_root) over (x - target)^pole_power, a nonzero number over 0 that calls for a sign check on each side, giving an infinite limit when the power is 2 and no limit when it is 1. at_infinity is (lead_top x + top_root) over (lead_bottom x^2 + bottom_root) as x grows, which calls for dividing by x^2. The distractors are the procedures the held errors lead to on each form.",
}

x = sympy.Symbol("x")


def _zero_over_zero(names):
   target = names["target"]
   top_root = names["top_root"]
   bottom_root = names["bottom_root"]
   root_value = names["root_value"]
   form = names["form"]

   if form == "factor":
      numerator = sympy.expand((x - target) * (x - top_root))
      denominator = sympy.expand((x - target) * (x - bottom_root))
      top_tex, bottom_tex = tex(numerator), tex(denominator)
      reduced = (x - top_root) / (x - bottom_root)
      procedure = f"factor both parts and cancel {math(tex(x - target))}"
      rewrite_text = f"Factoring gives {math(rf'\frac{{{tex((x - target) * (x - top_root))}}}{{{tex((x - target) * (x - bottom_root))}}}')}"
   elif form == "conjugate":
      radical = sympy.sqrt(x + root_value**2 - target)
      top_tex, bottom_tex = f"{tex(radical)} - {root_value}", tex(x - target)
      reduced = 1 / (radical + root_value)
      conjugate_tex = f"{tex(radical)} + {root_value}"
      procedure = f"multiply both parts by the conjugate {math(conjugate_tex)} and cancel {math(tex(x - target))}"
      rewrite_text = f"Multiplying by {math(conjugate_tex)} over itself turns the numerator into {math(tex(x - target))}"
   else:
      top_tex, bottom_tex = rf"\frac{{1}}{{x}} - \frac{{1}}{{{target}}}", tex(x - target)
      reduced = sympy.Rational(-1, target) / x
      procedure = f"combine the fractions over {math(f'{target} x')} and cancel {math(tex(x - target))}"
      rewrite_text = f"Combining gives a numerator of {math(rf'\frac{{{tex(target - x)}}}{{{target} x}}')}"

   limit_value = sympy.simplify(reduced.subs(x, target))
   value_text = math(tex(limit_value))
   limit_tex = rf"\lim_{{x \to {target}}} \frac{{{top_tex}}}{{{bottom_tex}}}"
   steps = [
      Step(text=f"Substituting {math(f'x = {target}')} makes the numerator and the denominator both 0, the indeterminate form 0/0.", rule="classify by substitution"),
      Step(text=f"{rewrite_text}, and the factor {math(tex(x - target))} cancels, leaving {math(tex(reduced))}.", rule="algebraic rewriting"),
      Step(text=f"Substituting into the rewritten expression gives the limit {value_text}.", rule="substitution after rewriting"),
   ]
   key_label = f"Substitution gives 0/0, so {procedure}, and then substitute, which gives {value_text}."
   distractors = [
      Distractor(
         error_path="BC-ERR-01006",
         derivation="the quotient limit theorem chosen although the denominator's limit is 0",
         label=f"The denominator {math(bottom_tex)} has a limit, so divide the limit of the numerator by it, which gives {math(r'\frac{0}{0}')}.",
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-01008",
         derivation="the form read from the numerator alone, so the limit reported as 0",
         label=f"Substitution makes the numerator {math(top_tex)} equal to 0, so no rewriting is needed, which gives {math('0')}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01009",
         derivation="the indeterminate form 0/0 read as a statement that the limit does not exist",
         label=f"Substitution of {math(f'x = {target}')} gives 0/0, so no procedure applies, which means the limit does not exist.",
         mechanism="conceptual_confusion",
      ),
   ]

   return limit_tex, steps, key_label, distractors


def _nonzero_over_zero(names):
   target = names["target"]
   top_root = names["top_root"]
   power = int(names["pole_power"])

   top_tex = tex(x - top_root)
   bottom_tex = tex((x - target) ** power)
   limit_tex = rf"\lim_{{x \to {target}}} \frac{{{top_tex}}}{{{bottom_tex}}}"
   numerator_value = target - top_root
   right_tex = r"\infty" if numerator_value > 0 else r"-\infty"
   opposite_tex = r"-\infty" if numerator_value > 0 else r"\infty"
   left_tex = right_tex if power == 2 else opposite_tex
   left_sign = "positive" if power == 2 else "negative"
   quotient_text = math(rf"\frac{{{numerator_value}}}{{0}}")
   at = math(f"x = {target}")

   steps = [
      Step(text=f"Substituting {at} gives {quotient_text}, a nonzero number over 0. This is not an indeterminate form, and the quotient is unbounded near {at}.", rule="classify by substitution"),
      Step(
         text=(
            f"The numerator is near {numerator_value}. The denominator {math(bottom_tex)} is positive on the right of {target} "
            f"and {left_sign} on the left, so the quotient approaches {math(left_tex)} from the left and {math(right_tex)} from the right."
         ),
         rule="sign on each side",
      ),
   ]

   if power == 2:
      result = f"which gives {math(right_tex)} on both sides"
      steps.append(Step(text=f"Both sides agree, so the limit is {math(right_tex)}, an infinite limit, and no real limit exists.", rule="infinite limit"))
      third = Distractor(
         error_path="BC-ERR-01020",
         derivation="the infinite limit read as an existing real limit",
         label=f"Substitution gives {quotient_text}, so the quotient grows without bound, which means the limit exists and equals {math(right_tex)}.",
         mechanism="conceptual_confusion",
      )
   else:
      result = f"which gives {math(left_tex)} and {math(right_tex)}, so no limit exists"
      steps.append(Step(text="The two sides disagree, so the limit does not exist.", rule="one sided infinite limits"))
      third = Distractor(
         error_path="BC-ERR-01019",
         derivation="one two sided infinite limit written without checking the sign on each side",
         label=f"Substitution gives {quotient_text}, so the quotient grows without bound, which gives {math(right_tex)} from both sides.",
         mechanism="sign_error",
      )

   key_label = f"Substitution gives {quotient_text}, so check the sign on each side of {at}, {result}."
   distractors = [
      Distractor(
         error_path="BC-ERR-01006",
         derivation="the quotient limit theorem chosen although the denominator's limit is 0",
         label=f"The denominator {math(bottom_tex)} has a limit, so divide the limit of the numerator by it, which gives {quotient_text}.",
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-01003",
         derivation="nonexistence concluded because the expression is undefined at the point, with no sign check",
         label=f"The quotient is undefined at {at}, and no limit of any kind exists where a quotient is undefined, which means no sign check is needed.",
         mechanism="conceptual_confusion",
      ),
      third,
   ]

   return limit_tex, steps, key_label, distractors


def _at_infinity(names):
   lead_top = names["lead_top"]
   lead_bottom = names["lead_bottom"]
   numerator = lead_top * x + names["top_root"]
   denominator = lead_bottom * x**2 + names["bottom_root"]
   limit_tex = rf"\lim_{{x \to \infty}} \frac{{{tex(numerator)}}}{{{tex(denominator)}}}"
   divided = rf"\frac{{{tex(sympy.expand(numerator / x**2))}}}{{{tex(sympy.expand(denominator / x**2))}}}"
   ratio = sympy.Rational(lead_top, lead_bottom)
   infinity_form = math(r"\frac{\infty}{\infty}")

   steps = [
      Step(text=f"As x grows, both the numerator and the denominator grow without bound, the form {infinity_form}.", rule="classify the form at infinity"),
      Step(text=f"Divide the numerator and the denominator by {math('x^{2}')}, the highest power in the denominator, and the expression becomes {math(divided)}.", rule="divide by the highest power"),
      Step(text=f"Every term with x in a denominator approaches 0, and the denominator approaches {lead_bottom}, so the limit is {math('0')}.", rule="limits of the terms"),
   ]
   key_label = f"As x grows the form is {infinity_form}, so divide both parts by {math('x^{2}')}, which gives {math('0')}."
   distractors = [
      Distractor(
         error_path="BC-ERR-01021",
         derivation="infinity substituted as a number and infinity over infinity simplified to 1",
         label=f"Substituting {math(r'x = \infty')} gives {infinity_form}, so the infinities cancel, which gives {math('1')}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01023",
         derivation="the ratio of the leading coefficients taken without comparing the degrees",
         label=f"As x grows the leading terms dominate, so take the ratio of the leading coefficients, which gives {math(tex(ratio))}.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01009",
         derivation="the indeterminate form infinity over infinity read as a statement that the limit does not exist",
         label=f"As x grows the form is {infinity_form}, an indeterminate form, which means the limit does not exist.",
         mechanism="conceptual_confusion",
      ),
   ]

   return limit_tex, steps, key_label, distractors


def build(names):
   form = names["form"]

   if form == "infinite":
      limit_tex, steps, key_label, distractors = _nonzero_over_zero(names)
   elif form == "at_infinity":
      limit_tex, steps, key_label, distractors = _at_infinity(names)
   else:
      limit_tex, steps, key_label, distractors = _zero_over_zero(names)

   stem = (
      f"Consider {math(limit_tex)}. Classify the form of this limit, name the procedure that resolves it, and "
      "give the result."
   )

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="determine",
      notes={"form": form},
   )
