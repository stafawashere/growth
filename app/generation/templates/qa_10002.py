"""BC-QA-10002, the exact value of a convergent geometric or telescoping series."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import n, series_tex

ARCHETYPE_ID = "BC-QA-10002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["geometric", "telescoping"]}},
      {"name": "start", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2, 3]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "ratio", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "-1/2", "1/3", "-1/3", "2/3", "-2/3", "1/4", "-1/4", "3/4", "2/5", "-2/5", "3/5"]}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
      "finite(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-02", "settings": {"geometric": "low", "telescoping": "medium"}},
      {"parameter": "start", "difficulty_factor_id": "BC-DF-02", "settings": {"1": "low", "2": "low", "3": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "start", "coefficient", "ratio", "offset"]},
   ],
   "notes": "Geometric: the sum from n = start of coefficient times ratio^n. Telescoping: the sum from n = start of coefficient over (n + offset)(n + offset + 1). The start is never 0, so taking the index 0 term as the first term is a distinct error.",
}


def _geometric(names):
   coefficient = names["coefficient"]
   ratio = names["ratio"]
   start = int(names["start"])
   term_tex = rf"{coefficient if coefficient != 1 else ''} \left({tex(ratio)}\right)^{{n}}".strip()
   first = coefficient * ratio**start
   value = first / (1 - ratio)
   three_terms = sum((coefficient * ratio ** (start + index) for index in range(3)), sympy.Integer(0))

   steps = [
      Step(text=f"The series is geometric with common ratio {math(f'r = {tex(ratio)}')}, and {math(rf'|r| < 1')}, so it converges. Its first term is the term with {math(f'n = {start}')}: {math(f'a = {tex(first)}')}.", value=first, rule="first term and ratio"),
      Step(text=f"The sum is {math(rf'\frac{{a}}{{1 - r}} = \frac{{{tex(first)}}}{{1 - \left({tex(ratio)}\right)}} = {tex(value)}')}.", value=value, rule="geometric series sum"),
   ]
   distractors = [
      Distractor("BC-ERR-10006", f"the index 0 term, {coefficient}, used as the first term although the series starts at n = {start}", value=coefficient / (1 - ratio), mechanism="wrong_limits"),
      Distractor("BC-ERR-99038", "the first three terms added and their total reported as the value of the series", value=three_terms, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-10001", "the limit of the general term, 0, reported as the value of the series", value=sympy.Integer(0), mechanism="conceptual_confusion"),
   ]

   return term_tex, value, steps, distractors


def _telescoping(names):
   coefficient = names["coefficient"]
   offset = names["offset"]
   start = int(names["start"])
   term = coefficient / ((n + offset) * (n + offset + 1))
   lowest = start + offset
   value = sympy.Rational(coefficient, lowest)
   three_terms = coefficient * (sympy.Rational(1, lowest) - sympy.Rational(1, lowest + 3))
   split = rf"{tex(term)} = {coefficient if coefficient != 1 else ''}\left(\frac{{1}}{{{tex(n + offset)}}} - \frac{{1}}{{{tex(n + offset + 1)}}}\right)"
   partial = rf"S_N = {coefficient if coefficient != 1 else ''}\left(\frac{{1}}{{{lowest}}} - \frac{{1}}{{N + {offset + 1}}}\right)"

   steps = [
      Step(text=f"Split the term into partial fractions: {math(split)}.", rule="partial fractions"),
      Step(text=f"In the partial sum from {math(f'n = {start}')} to {math('n = N')} the middle terms cancel: {math(partial)}.", rule="telescoping partial sum"),
      Step(text=f"As {math(r'N \to \infty')}, the second fraction approaches 0, so the value of the series is {math(tex(value))}.", value=value, rule="limit of the partial sums"),
   ]
   distractors = [
      Distractor("BC-ERR-10006", f"the cancellation started from the index 0 term instead of n = {start}, leaving 1 over {offset} rather than 1 over {lowest}", value=sympy.Rational(coefficient, offset), mechanism="wrong_limits"),
      Distractor("BC-ERR-99038", "the first three terms added and their total reported as the value of the series", value=three_terms, mechanism="conceptual_confusion"),
      Distractor("BC-ERR-10001", "the limit of the general term, 0, reported as the value of the series", value=sympy.Integer(0), mechanism="conceptual_confusion"),
   ]

   return tex(term), value, steps, distractors


def build(names):
   start = int(names["start"])
   builder = _geometric if names["form"] == "geometric" else _telescoping
   term_tex, value, steps, distractors = builder(names)
   stem = f"Find the exact value of the series {math(series_tex(term_tex, start))}."

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
   )
