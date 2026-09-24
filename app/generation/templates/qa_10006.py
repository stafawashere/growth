"""BC-QA-10006, the limit comparison test used to classify a series of rational terms."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import INFINITY_LIMIT, n, series_tex

ARCHETYPE_ID = "BC-QA-10006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "claim", "type": "label", "role": "difficulty", "domain": {"values": ["converging", "diverging", "absolute"]}},
      {"name": "partner", "type": "label", "role": "difficulty", "domain": {"values": ["given", "chosen"]}},
      {"name": "gap", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3]}},
      {"name": "top_degree", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "lead_top", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "constant_top", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "lead_bottom", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "constant_bottom", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
   ],
   "constraints": [
      "lead_top != lead_bottom",
   ],
   "derived": [],
   "invariants": [
      "verdict in ['converges', 'diverges', 'converges absolutely']",
   ],
   "dial_bindings": [
      {"parameter": "claim", "difficulty_factor_id": "BC-DF-01", "settings": {"converging": "low", "diverging": "low", "absolute": "medium"}},
      {"parameter": "partner", "difficulty_factor_id": "BC-DF-01", "settings": {"given": "low", "chosen": "medium"}},
      {"parameter": "gap", "difficulty_factor_id": "BC-DF-01", "settings": {"2": "low", "3": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["claim", "gap", "top_degree", "lead_top", "lead_bottom"]},
   ],
   "notes": "The general term is a quotient of polynomials whose degrees differ by the gap, compared with the p-series of that power (1 for the diverging claim, the drawn gap otherwise); the limit of the quotient is the ratio of leading coefficients, never 1, so comparing it with 1 gives a distinct wrong reason.",
}


def build(names):
   claim = names["claim"]
   gap = 1 if claim == "diverging" else int(names["gap"])
   top_degree = int(names["top_degree"])
   lead_top = names["lead_top"]
   lead_bottom = names["lead_bottom"]
   start = int(names["start"])
   is_absolute = claim == "absolute"

   magnitude = (lead_top * n**top_degree + names["constant_top"]) / (lead_bottom * n ** (top_degree + gap) + names["constant_bottom"])
   term = (-1) ** n * magnitude if is_absolute else magnitude
   partner = 1 / n**gap
   partner_tex = tex(partner)
   limit_value = sympy.Rational(lead_top, lead_bottom)
   numerator, denominator = magnitude.as_numer_denom()
   quotient = sympy.expand(numerator * n**gap) / denominator
   partner_converges = gap > 1
   given = math(series_tex("a_n", start))
   partner_sum = math(series_tex(partner_tex, start))
   short_given = math(r"\sum a_n")
   short_partner = math(rf"\sum {partner_tex}")
   size = "|a_n|" if is_absolute else "a_n"
   quotient_tex = rf"\frac{{{size}}}{{1/n^{{{gap}}}}}"
   limit_tex = math(rf"{INFINITY_LIMIT} {quotient_tex} = {tex(limit_value)}")
   full_limit = rf"{INFINITY_LIMIT} \frac{{{tex(magnitude)}}}{{{partner_tex}}} = {INFINITY_LIMIT} {tex(quotient)} = {tex(limit_value)}"
   p_tex = f"p = {gap}"

   if partner_converges:
      partner_verdict = f"converges because {math(p_tex + ' > 1')}"
   else:
      partner_verdict = f"diverges because {math(p_tex + r' \le 1')}"

   if is_absolute:
      verdict = "converges absolutely"
      partner_word = "converges"
      target = f"the series of absolute values {math(series_tex(tex(magnitude), start))}"
   else:
      verdict = "converges" if partner_converges else "diverges"
      partner_word = verdict
      target = f"the series {given}"

   key = f"{short_given} {verdict}, because {limit_tex} is positive and finite and {short_partner} {partner_word}."
   series_text = f"{given}, where {math(f'a_n = {tex(term)}')}"

   if names["partner"] == "given":
      method = f"Use the limit comparison test with {partner_sum}"
   else:
      method = "Use the limit comparison test with a p-series you choose"

   if is_absolute:
      stem = f"{method} to show that the series {series_text}, converges absolutely. State the conclusion, naming the series it concerns."
   else:
      stem = f"{method} to determine whether the series {series_text}, converges or diverges. State the conclusion, naming the series it concerns."

   steps = [
      Step(text=f"Compare {target} with {partner_sum}, the p-series with {math(p_tex)}, since the degrees of the denominator and numerator of the terms differ by {gap}. Both have positive terms.", rule="choose the comparison series"),
      Step(text=f"{math(full_limit)}.", value=limit_value, rule="limit of the quotient"),
      Step(text=f"The limit {math(tex(limit_value))} is positive and finite, and {partner_sum} {partner_verdict}.", rule="p-series test"),
      Step(text=key, point_type_id="BC-PT-99005", rule="limit comparison test"),
   ]

   is_below_one = limit_value < 1
   compared_with_one = "less than 1" if is_below_one else "greater than 1"
   one_verdict = "converges" if is_below_one else "diverges"
   absolute_one_verdict = "converges absolutely" if is_below_one else "diverges"
   one_derivation = f"the limit of the quotient compared with 1, as in the ratio test, and found {compared_with_one}"

   if is_absolute:
      distractors = [
         Distractor("BC-ERR-10023", "the absolute and conditional labels exchanged after the series of absolute values was shown to converge", label=f"{short_given} converges conditionally, because {limit_tex} is positive and finite and {short_partner} converges."),
         Distractor("BC-ERR-10018", "absolute values never taken, so only the alternating series test was used and its result called absolute convergence", label=f"{short_given} converges absolutely by the alternating series test, because {math('|a_n|')} decreases to 0."),
         Distractor("BC-ERR-10019", one_derivation, label=f"{short_given} {absolute_one_verdict}, because {limit_tex} is {compared_with_one}."),
      ]
   else:
      bare_tex = math(rf"{quotient_tex} = {tex(limit_value)}")
      distractors = [
         Distractor("BC-ERR-10019", one_derivation, label=f"{short_given} {one_verdict}, because {limit_tex} is {compared_with_one}."),
         Distractor("BC-ERR-10017", "the quotient of the terms written equal to its limit, with the limit notation left off", label=f"{short_given} {verdict}, because {bare_tex} is positive and finite and {short_partner} {verdict}."),
         Distractor("BC-ERR-10003", "the conclusion left with no series named, so it could be read as a statement about the comparison series", label=f"It {verdict}, because {limit_tex} is positive and finite and {short_partner} {verdict}."),
      ]

   for distractor in distractors:
      distractor.mechanism = "conceptual_confusion"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="determine",
      notes={"verdict": verdict},
   )
