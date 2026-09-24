"""BC-QA-05003, a named critical point classified from the sign change of the first derivative."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-05003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "named", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "other", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 6, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "sign", "type": "label", "role": "safe", "domain": {"values": ["positive", "negative"]}},
      {"name": "multiplicity", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2]}},
      {"name": "factor", "type": "label", "role": "difficulty", "domain": {"values": ["none", "exponential", "quadratic"]}},
   ],
   "constraints": [
      "named != other",
      "multiplicity == 1 or side_sign > 0",
   ],
   "derived": [
      {"name": "side_sign", "expression": "(named - other) * (1 if sign == 'positive' else -1)"},
   ],
   "invariants": [
      "side_sign != 0",
   ],
   "dial_bindings": [
      {"parameter": "multiplicity", "difficulty_factor_id": "BC-DF-13", "settings": {"1": "off", "2": "low"}},
      {"parameter": "factor", "difficulty_factor_id": "BC-DF-03", "settings": {"none": "off", "exponential": "low", "quadratic": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["named", "other", "scale", "sign", "multiplicity", "factor"]},
   ],
   "notes": "f'(x) = k (x - c)^m (x - d) times an always-positive factor. With m = 1 the sign of f' changes at c; with m = 2 it keeps the sign of k(c - d), which the constraint makes positive so the neither case has f' positive on both sides.",
}

x = sympy.Symbol("x")

FACTORS = {"none": sympy.Integer(1), "exponential": sympy.exp(x), "quadratic": x**2 + 1}


def _factor_tex(root, power):
   linear = x - root
   base = tex(linear) if root == 0 else rf"\left({tex(linear)}\right)"

   return base if power == 1 else f"{base}^{{{power}}}"


def _derivative_tex(leading, named, multiplicity, other, factor):
   coefficient = {1: "", -1: "-"}.get(leading, str(leading))
   pieces = [_factor_tex(named, multiplicity), _factor_tex(other, 1)]
   pieces.sort(key=lambda piece: not piece.startswith("x"))

   if factor != "none":
      extra = tex(FACTORS[factor])
      pieces.append(extra if factor == "exponential" else rf"\left({extra}\right)")

   return coefficient + " ".join(pieces)


def _label(classification, named, reason, place="at"):
   if classification == "neither":
      opening = f"f has neither a relative minimum nor a relative maximum at x = {named}"
   else:
      opening = f"f has a relative {classification} at x = {named}"

   return f"{opening}, because {reason} {place} x = {named}."


def build(names):
   named = int(names["named"])
   other = int(names["other"])
   sign = 1 if names["sign"] == "positive" else -1
   leading = sign * int(names["scale"])
   multiplicity = int(names["multiplicity"])
   right_positive = leading * (named - other) > 0
   changes_sign = multiplicity == 1

   derivative_statement = "f'(x) = " + _derivative_tex(leading, named, multiplicity, other, names["factor"])
   zero_statement = f"f'({named}) = 0"
   stem = (
      f"The derivative of a function f is given by {math(derivative_statement)} for all x. Does f have a relative "
      f"minimum, a relative maximum, or neither at x = {named}? Give a reason for the answer."
   )

   named_prime = "f'"
   steps = [
      Step(
         text=f"The factor {math(tex((x - named) ** multiplicity))} makes {math(zero_statement)}, so x = {named} is a critical point of f.",
         point_type_id="BC-PT-99013",
         rule="critical point",
      ),
   ]

   if changes_sign:
      before, after = ("negative", "positive") if right_positive else ("positive", "negative")
      classification = "minimum" if right_positive else "maximum"
      opposite = "maximum" if right_positive else "minimum"
      change_words = f"{before} to {after}"
      steps.append(Step(
         text=(
            f"Every other factor keeps one sign near x = {named}, and {math(tex(x - named))} changes sign there, so "
            f"{math(named_prime)} changes from {change_words} at x = {named}. By the first derivative test f has a relative "
            f"{classification} there."
         ),
         point_type_id="BC-PT-99012",
         rule="first derivative test",
      ))
      key_label = _label(classification, named, f"{named_prime} changes from {change_words}")
      distractors = [
         Distractor("BC-ERR-05021", f"the classification read backwards from a {change_words} change", label=_label(opposite, named, f"{named_prime} changes from {change_words}"), mechanism="reversed_quantities"),
         Distractor("BC-ERR-05021", f"the sign chart read in the reverse direction, as a change from {after} to {before}, and classified from that", label=_label(opposite, named, f"{named_prime} changes from {after} to {before}"), mechanism="reversed_quantities"),
         Distractor("BC-ERR-05022", "the classification taken from the size of f' near the input, which is close to 0, rather than from its change of sign", label=_label("neither", named, f"{named_prime} stays close to 0 on both sides", place="of")),
      ]
   else:
      steps.append(Step(
         text=(
            f"The factor {math(tex((x - named) ** 2))} is never negative and every other factor is positive near x = {named}, "
            f"so {math(named_prime)} does not change sign at x = {named}. By the first derivative test f has neither a "
            "relative minimum nor a relative maximum there."
         ),
         point_type_id="BC-PT-99012",
         rule="first derivative test",
      ))
      key_label = _label("neither", named, f"{named_prime} does not change sign")
      distractors = [
         Distractor("BC-ERR-05013", "a critical point with no sign change declared a relative minimum", label=_label("minimum", named, f"{named_prime} is equal to 0"), mechanism="theorem_condition_ignored"),
         Distractor("BC-ERR-05013", "a critical point with no sign change declared a relative maximum because f rises up to it", label=_label("maximum", named, f"{named_prime} is positive before and equal to 0"), mechanism="theorem_condition_ignored"),
         Distractor("BC-ERR-05022", "the classification taken from the value of f', which is smallest at the input, rather than from a change of sign", label=_label("minimum", named, f"{named_prime} takes its smallest nearby value")),
      ]

   for distractor in distractors:
      distractor.mechanism = distractor.mechanism or "conceptual_confusion"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="classify",
   )
