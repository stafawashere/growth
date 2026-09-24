"""BC-QA-10004, a series shown to converge or diverge by a named test with its conditions checked."""

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import INFINITY_LIMIT, n, series_tex

ARCHETYPE_ID = "BC-QA-10004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["comparison_converges", "comparison_diverges", "alternating"]}},
      {"name": "naming", "type": "label", "role": "difficulty", "domain": {"values": ["named", "unnamed"]}},
      {"name": "large_power", "type": "rational", "role": "safe", "domain": {"values": ["3/2", "2", "3", "5/2", "4"]}},
      {"name": "small_power", "type": "rational", "role": "safe", "domain": {"values": ["1/3", "1/2", "2/3", "1"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "verdict in ['converges', 'diverges']",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-09", "settings": {"comparison_converges": "low", "comparison_diverges": "low", "alternating": "off"}},
      {"parameter": "naming", "difficulty_factor_id": "BC-DF-09", "settings": {"named": "off", "unnamed": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "coefficient", "shift", "start"]},
   ],
   "notes": "A term below a convergent p-series multiple, a term above a divergent p-series, or an alternating term whose size decreases to 0. The named variant tells the student which test to use; the unnamed one leaves the choice open.",
}

LIMIT_OF_TERMS = rf"{INFINITY_LIMIT} a_n"
COMPARISON = "the direct comparison test"
ALTERNATING = "the alternating series test"


def _option(verdict, test, reason):
   return f"The series {verdict} by {test}, because {math(reason)}."


def _terms_to_zero(derivation):
   return Distractor("BC-ERR-10008", derivation, label=_option("converges", "the nth term test", f"{LIMIT_OF_TERMS} = 0"))


def _converging_comparison(names):
   coefficient = names["coefficient"]
   shift = names["shift"]
   power = names["large_power"]
   term = coefficient / (n**power + shift)
   partner = coefficient / n**power
   partner_sum = rf"\sum {tex(partner)}"
   inequality = rf"0 < {tex(term)} < {tex(partner)}"
   p_part = f"p = {tex(power)} > 1"
   key = _option("converges", COMPARISON, rf"0 < a_n < {tex(partner)} \text{{ and }} {p_part}")

   steps = [
      Step(text=f"The terms are positive, so the direct comparison test applies. Compare with {math(partner_sum)}, a multiple of the p-series with {math(f'p = {tex(power)}')}.", rule="name the test"),
      Step(text=f"Adding {math(tex(shift))} to the denominator makes each term smaller, so {math(inequality)} for every n.", rule="comparison inequality"),
      Step(text=f"Since {math(p_part)}, {math(partner_sum)} converges.", rule="p-series test"),
      Step(text=f"{key[:-1]}, so {math(series_tex('a_n', names['start']))} converges.", point_type_id="BC-PT-99005", rule="direct comparison test"),
   ]
   distractors = [
      Distractor("BC-ERR-10016", "the comparison inequality written the other way round, which could only support divergence", label=_option("converges", COMPARISON, rf"a_n \ge {tex(partner)} \text{{ and }} {p_part}")),
      Distractor("BC-ERR-10014", "the p-series threshold reversed, so the comparison series with p greater than 1 read as divergent", label=_option("diverges", COMPARISON, rf"0 < a_n < {tex(partner)} \text{{ and }} {p_part}")),
      _terms_to_zero("the verdict drawn from the terms approaching 0, which no test supports"),
   ]

   return term, "converges", COMPARISON, steps, key, distractors


def _diverging_comparison(names):
   shift = names["shift"]
   power = names["small_power"]
   term = (n**power + shift) / n ** (2 * power)
   partner = 1 / n**power
   partner_sum = rf"\sum {tex(partner)}"
   inequality = rf"{tex(term)} \ge {tex(partner)} > 0"
   p_part = rf"p = {tex(power)} \le 1"
   key = _option("diverges", COMPARISON, rf"a_n \ge {tex(partner)} \text{{ and }} {p_part}")

   steps = [
      Step(text=f"The terms are positive, so the direct comparison test applies. Compare with {math(partner_sum)}, the p-series with {math(f'p = {tex(power)}')}.", rule="name the test"),
      Step(text=f"Splitting the fraction, {math(tex(term) + ' = ' + tex(partner) + ' + ' + tex(shift / n ** (2 * power)))}, so {math(inequality)} for every n.", rule="comparison inequality"),
      Step(text=f"Since {math(p_part)}, {math(partner_sum)} diverges.", rule="p-series test"),
      Step(text=f"{key[:-1]}, so {math(series_tex('a_n', names['start']))} diverges.", point_type_id="BC-PT-99005", rule="direct comparison test"),
   ]
   distractors = [
      Distractor("BC-ERR-10016", "the comparison inequality written the other way round, which cannot show divergence", label=_option("diverges", COMPARISON, rf"a_n \le {tex(partner)} \text{{ and }} {p_part}")),
      _terms_to_zero("convergence concluded because the terms approach 0"),
      Distractor("BC-ERR-10009", "the alternating series test named for a series of positive terms, its alternating hypothesis never checked", label=f"The series converges by {ALTERNATING}, because {math('a_n')} decreases to 0."),
   ]

   return term, "diverges", COMPARISON, steps, key, distractors


def _alternating(names):
   coefficient = names["coefficient"]
   shift = names["shift"]
   power = names["small_power"]
   magnitude = coefficient / (n**power + shift)
   term = (-1) ** (n + 1) * magnitude
   limit_text = rf"{INFINITY_LIMIT} {tex(magnitude)} = 0"
   key = f"The series converges by {ALTERNATING}, because {math('|a_n|')} decreases to 0."

   steps = [
      Step(text=f"The factor {math('(-1)^{n+1}')} makes the terms alternate, so the alternating series test applies once its two conditions hold.", rule="name the test"),
      Step(text=f"The sizes {math(tex(magnitude))} decrease because the denominator increases with n.", rule="decreasing condition"),
      Step(text=f"The sizes approach 0: {math(limit_text)}.", rule="limit condition"),
      Step(text=f"The terms alternate, their sizes decrease, and the sizes approach 0, so {math(series_tex('a_n', names['start']))} converges by the alternating series test.", point_type_id="BC-PT-99005", rule="alternating series test"),
   ]
   distractors = [
      Distractor("BC-ERR-10020", "the alternating series test applied with only the limit condition stated, the decrease left out", label=_option("converges", ALTERNATING, rf"{INFINITY_LIMIT} |a_n| = 0")),
      _terms_to_zero("convergence concluded from the terms approaching 0 alone, the alternation never used"),
      Distractor("BC-ERR-10009", "the p-series test named for a series whose terms are not all positive, its hypothesis never checked", label=_option("diverges", "the p-series test", rf"p = {tex(power)} \le 1")),
   ]

   return term, "converges", ALTERNATING, steps, key, distractors


BUILDERS = {
   "comparison_converges": _converging_comparison,
   "comparison_diverges": _diverging_comparison,
   "alternating": _alternating,
}


def build(names):
   start = int(names["start"])
   term, verdict, test_name, steps, key, distractors = BUILDERS[names["form"]](names)
   series = f"{math(series_tex('a_n', start))}, where {math(f'a_n = {tex(term)}')},"

   if names["naming"] == "named":
      stem = f"Use {test_name} to determine whether the series {series} converges or diverges. Verify the conditions of the test."
   else:
      stem = f"Determine whether the series {series} converges or diverges. Name the test used and verify its conditions."

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
