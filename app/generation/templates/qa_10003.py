"""BC-QA-10003, a geometric series in x summed in closed form with its convergence condition."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import x

ARCHETYPE_ID = "BC-QA-10003"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "power", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2]}},
      {"name": "start", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2]}},
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "alternating"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 7, "step": 1}},
      {"name": "centre", "type": "integer", "role": "difficulty", "domain": {"min": -3, "max": 3, "step": 1}},
   ],
   "constraints": [
      "coefficient != base ** start",
   ],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "power", "difficulty_factor_id": "BC-DF-06", "settings": {"1": "low", "2": "medium"}},
      {"parameter": "start", "difficulty_factor_id": "BC-DF-06", "settings": {"1": "low", "2": "medium"}},
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-06", "settings": {"positive": "low", "alternating": "medium"}},
      {"parameter": "centre", "difficulty_factor_id": "BC-DF-06", "settings": {"-3": "medium", "-2": "medium", "-1": "medium", "0": "low", "1": "medium", "2": "medium", "3": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["power", "start", "sign", "coefficient", "base"]},
   ],
   "notes": "The series is the sum from n = start of coefficient times (sign (x - centre)^power / base)^n. The start is 1 or 2, so the index 0 term is never the first term.",
}


def build(names):
   power = int(names["power"])
   start = int(names["start"])
   coefficient = names["coefficient"]
   base = names["base"]
   is_alternating = names["sign"] == "alternating"
   sign_value = -1 if is_alternating else 1

   centre = names["centre"]
   shifted = x - centre
   ratio = sign_value * shifted**power / base
   first = coefficient * ratio**start
   value = sympy.factor(sympy.together(first / (1 - ratio)))
   bare_ratio = sign_value * shifted**power
   three_terms = first + first * ratio + first * ratio**2

   sign_tex = "(-1)^{n} " if is_alternating else ""
   base_tex = "x" if centre == 0 else rf"\left({tex(shifted)}\right)"
   variable_power = f"{base_tex}^{{n}}" if power == 1 else f"{base_tex}^{{2n}}"
   term_tex = rf"\frac{{{coefficient} {sign_tex}{variable_power}}}{{{base}^{{n}}}}"
   size_bound = sympy.Integer(base) if power == 1 else sympy.sqrt(base)
   bound = math(rf"\left|{tex(shifted)}\right| < {tex(size_bound)}")
   stem = (
      f"Find the sum of the series {math(rf'\sum_{{n={start}}}^{{\infty}} {term_tex}')} as a closed-form expression in x, "
      f"for the values of x where the series converges."
   )

   steps = [
      Step(text=f"The quotient of consecutive terms is {math(f'r = {tex(ratio)}')}, the same for every n, so the series is geometric. Its first term is the {math(f'n = {start}')} term, {math(f'a = {tex(first)}')}.", value=first, point_type_id="BC-PT-99067", rule="first term and ratio"),
      Step(text=f"It converges when {math(f'|r| < 1')}, that is for {bound}.", rule="convergence condition"),
      Step(text=f"There the sum is {math(rf'\frac{{a}}{{1 - r}} = {tex(value)}')}.", value=value, point_type_id="BC-PT-99004", rule="geometric series sum"),
   ]
   distractors = [
      Distractor("BC-ERR-10006", f"the index 0 term, {coefficient}, used as the first term although the series starts at n = {start}", value=sympy.factor(sympy.together(coefficient / (1 - ratio))), mechanism="wrong_limits"),
      Distractor("BC-ERR-10004", f"the common ratio read as {bare_ratio}, with the {base} to the n in the denominator left out of it", value=sympy.factor(sympy.together(first / (1 - bare_ratio))), mechanism="algebra_slip"),
      Distractor("BC-ERR-99038", "the first three terms written out and their sum given in place of the closed form", value=three_terms, mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
   )
