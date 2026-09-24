"""BC-QA-10007, a series classified as absolutely convergent, conditionally convergent or divergent."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-10007"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["power", "ratio"]}},
      {"name": "power", "type": "rational", "role": "difficulty", "domain": {"values": ["1/3", "1/2", "2/3", "1", "4/3", "3/2", "2", "3"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "sign_start", "type": "label", "role": "safe", "domain": {"values": ["n", "n+1"]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "classification in ['converges absolutely', 'converges conditionally', 'diverges']",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-09", "settings": {"power": "off", "ratio": "low"}},
      {"parameter": "power", "difficulty_factor_id": "BC-DF-09", "settings": {"1/3": "low", "1/2": "low", "2/3": "low", "1": "low", "4/3": "off", "3/2": "off", "2": "off", "3": "off"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "power", "coefficient", "offset"]},
   ],
   "notes": "The power form is coefficient over (n + offset) to the power, alternating; its absolute series is a p-series in disguise by limit comparison. The ratio form, coefficient n over (n + offset), fails the nth term test.",
}

n = sympy.Symbol("n", positive=True, integer=True)

ABSOLUTE = "converges absolutely"
CONDITIONAL = "converges conditionally"
DIVERGES = "diverges"


def _labelled(classification, reason):
   return f"The series {classification}, {reason}."


def build(names):
   coefficient = names["coefficient"]
   offset = names["offset"]
   power = names["power"]
   start = int(names["start"])
   exponent = n if names["sign_start"] == "n" else n + 1

   if names["form"] == "ratio":
      magnitude = coefficient * n / (n + offset)
   else:
      magnitude = coefficient / (n + offset) ** power

   term = (-1) ** exponent * magnitude
   series_tex = rf"\sum_{{n={start}}}^{{\infty}} {tex(term)}"
   stem = f"Classify the series {math(series_tex)} as absolutely convergent, conditionally convergent, or divergent."

   limit_of_magnitude = sympy.limit(magnitude, n, sympy.oo)
   terms_vanish = limit_of_magnitude == 0

   if not terms_vanish:
      classification = DIVERGES
      key_reason = "because its terms do not approach 0"
      steps = [
         Step(text=f"Look at the size of the terms: {math(r'\lim_{n\to\infty} ' + tex(magnitude) + ' = ' + tex(limit_of_magnitude))}.", value=limit_of_magnitude, rule="limit of the terms"),
         Step(text="Since the terms of the series do not approach 0, the series diverges by the nth term test, and neither kind of convergence applies.", rule="nth term test"),
      ]
      distractors = [
         Distractor("BC-ERR-10018", "absolute values never considered and the alternation taken as enough for convergence, then called absolute", label=_labelled(ABSOLUTE, "because its terms alternate in sign")),
         Distractor("BC-ERR-10023", "the absolute and conditional labels exchanged on an alternating-series reading", label=_labelled(CONDITIONAL, "because its terms alternate in sign while their sizes do not shrink")),
         Distractor("BC-ERR-10003", "a convergence conclusion drawn without saying which series it concerns", label=_labelled("converges", "because it is an alternating series")),
      ]
   elif power > 1:
      classification = ABSOLUTE
      key_reason = "because the series of absolute values converges by comparison with a p-series"
      steps = [
         Step(text=f"Test the series of absolute values, {math(rf'\sum {tex(magnitude)}')}. By limit comparison with {math(rf'\sum \frac{{1}}{{n^{{{tex(power)}}}}}')}, the ratio of terms tends to {math(tex(coefficient))}, a positive finite number.", value=sympy.Integer(coefficient), rule="limit comparison test"),
         Step(text=f"That p-series has p = {math(tex(power))} > 1 and converges, so the series of absolute values converges and the given series converges absolutely.", rule="p-series test"),
      ]
      distractors = [
         Distractor("BC-ERR-10023", "the absolute and conditional labels exchanged", label=_labelled(CONDITIONAL, key_reason)),
         Distractor("BC-ERR-10018", "absolute values omitted, so the absolute series was never tested and only the alternating series test was used", label=_labelled(CONDITIONAL, "because it passes the alternating series test")),
         Distractor("BC-ERR-10003", "the conclusion drawn about a series it does not name", label=_labelled(DIVERGES, "because the series of absolute values is compared with a p-series")),
      ]
   else:
      classification = CONDITIONAL
      key_reason = "because it passes the alternating series test while the series of absolute values diverges"
      steps = [
         Step(text=f"Test the series of absolute values, {math(rf'\sum {tex(magnitude)}')}. By limit comparison with {math(rf'\sum \frac{{1}}{{n^{{{tex(power)}}}}}')}, the ratio of terms tends to {math(tex(coefficient))}, so both series behave alike.", value=sympy.Integer(coefficient), rule="limit comparison test"),
         Step(text=f"That p-series has p = {math(tex(power))}, not more than 1, so the series of absolute values diverges.", rule="p-series test"),
         Step(text="The given series alternates, its terms decrease, and they approach 0, so it converges by the alternating series test. It converges conditionally.", rule="alternating series test"),
      ]
      distractors = [
         Distractor("BC-ERR-10023", "the absolute and conditional labels exchanged", label=_labelled(ABSOLUTE, key_reason)),
         Distractor("BC-ERR-10018", "absolute values omitted: the alternating series test result reported as absolute convergence", label=_labelled(ABSOLUTE, "because it passes the alternating series test, its terms decreasing in size to 0")),
         Distractor("BC-ERR-10003", "the divergence of the absolute series reported as the verdict on the given series", label=_labelled(DIVERGES, "because the series of absolute values diverges by comparison with a p-series")),
      ]

   for distractor in distractors:
      distractor.mechanism = "conceptual_confusion"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=_labelled(classification, key_reason)),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="classify",
      notes={"classification": classification},
   )
