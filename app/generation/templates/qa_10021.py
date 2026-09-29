"""BC-QA-10021, the sum of a series found from its partial sums before any convergence test is taught."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-10021"
TEMPLATE_VERSION = "2"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "2",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "family", "type": "label", "role": "difficulty", "domain": {"values": ["rational", "exponential", "telescoping"]}},
      {"name": "lead", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "ratio", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1/3", "2/3", "1/4", "3/4"]}},
      {"name": "numerator", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 6, "step": 1}},
   ],
   "constraints": [
      "family != 'rational' or distinct([0, lead / rate, (lead + shift) / (rate + offset), (2 * lead + shift) / (2 * rate + offset)])",
      "family != 'exponential' or distinct([0, lead, lead - offset * ratio, lead - offset * ratio**2])",
      "gcd(lead, rate) == 1",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "family", "difficulty_factor_id": "BC-DF-13", "settings": {"rational": "low", "exponential": "low", "telescoping": "off"}},
      {"parameter": "family", "difficulty_factor_id": "BC-DF-15", "settings": {"rational": "low", "exponential": "low", "telescoping": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["family", "lead", "shift", "rate", "offset", "ratio", "numerator", "start"]},
   ],
   "notes": "rational: S_n = (p n + q)/(r n + s), whose limit p/r is the sum. exponential: S_n = p - s c^n with 0 < c < 1, whose limit p is the sum. telescoping: the series of k/((n + m)(n + m + 1)) from n = 1, whose partial sums k/(m + 1) - k/(n + m + 1) approach k/(m + 1). No test is named and the answer is a value, so the item can be served as a short answer opener for BC-CON-10002; the canonical solution reads the sum as the limit of the partial sums. The distractors are 0, the limit of the terms, and the first and second partial sums; the constraints keep all four apart.",
}

n = sympy.Symbol("n", positive=True, integer=True)
SERIES = r"\sum_{n=1}^{\infty} a_n"


def _definition_step():
   return Step(
      text="A series converges exactly when its sequence of partial sums approaches a finite limit, and that limit is its sum.",
      rule="convergence as the limit of the partial sums",
   )


def build(names):
   family = names["family"]
   lead = int(names["lead"])
   shift = int(names["shift"])
   rate = int(names["rate"])
   offset = int(names["offset"])
   ratio = sympy.nsimplify(names["ratio"])
   numerator = int(names["numerator"])
   start = int(names["start"])

   if family == "telescoping":
      term = numerator / ((n + start) * (n + start + 1))
      partial = sympy.Rational(numerator, start + 1) - numerator / (n + start + 1)
      total = sympy.Rational(numerator, start + 1)
      series = rf"\sum_{{n=1}}^{{\infty}} {tex(term)}"
      stem = f"The series {math(series)} converges. Find its sum."
      steps = [
         _definition_step(),
         Step(
            text=(
               f"Each term splits as {math(tex(term) + ' = ' + tex(numerator / (n + start)) + ' - ' + tex(numerator / (n + start + 1)))}, "
               f"so in the nth partial sum every middle term cancels and {math('S_n = ' + tex(partial))}."
            ),
            rule="partial sums of a telescoping series",
         ),
         Step(
            text=f"As n increases, {math(tex(numerator / (n + start + 1)))} approaches 0, so the sum is {math(tex(total))}.",
            value=total,
            rule="limit of the partial sums",
         ),
      ]
      first = partial.subs(n, 1)
      second = partial.subs(n, 2)
   else:
      if family == "rational":
         partial = (lead * n + shift) / (rate * n + offset)
         total = sympy.Rational(lead, rate)
         reason = "Dividing numerator and denominator by n"
      else:
         partial = lead - offset * ratio**n
         total = sympy.Integer(lead)
         reason = f"Since {math(r'\left(' + tex(ratio) + r'\right)^{n}')} approaches 0,"

      stem = (
         f"The nth partial sum of the series {math(SERIES)} is {math('S_n = ' + tex(partial))} for {math(r'n \ge 1')}. "
         "The series converges. Find its sum."
      )
      steps = [
         _definition_step(),
         Step(
            text=f"{reason} {math(r'\lim_{n \to \infty} S_n = ' + tex(total))}, so the sum is {math(tex(total))}.",
            value=total,
            rule="limit of the partial sums",
         ),
      ]
      first = partial.subs(n, 1)
      second = partial.subs(n, 2)

   distractors = [
      Distractor("BC-ERR-10001", "the terms approach 0, and that limit was reported as the sum of the series", value=sympy.Integer(0), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-99038", "the first partial sum reported as the sum", value=sympy.nsimplify(first), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-99038", "the second partial sum reported as the sum", value=sympy.nsimplify(second), mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=total),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
   )
