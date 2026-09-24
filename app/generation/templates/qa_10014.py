"""BC-QA-10014, the radius of convergence of a power series from the ratio test."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import INFINITY_LIMIT, x

ARCHETYPE_ID = "BC-QA-10014"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["divided", "even", "multiplied"]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 9, "step": 1}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"values": [0, 1, 2, 3]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
   ],
   "constraints": [
      "form != 'even' or not is_square(base)",
   ],
   "derived": [],
   "invariants": [
      "radius > 0",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-02", "settings": {"divided": "low", "even": "medium", "multiplied": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "centre", "base", "power", "coefficient"]},
   ],
   "notes": "Divided: c n^p (x - a)^n / b^n, radius b. Even: c (x - a)^(2n) / (b^n n^p), radius the square root of b, never whole. Multiplied: c b^n (x - a)^n / n^p, radius 1/b. The centre is a positive whole number, so reading the bound of the one-sided inequality x < a + R as the radius gives a different positive number.",
}


def _index_power_tex(power, index="n"):
   if power == 0:
      return ""

   grouped = index if index == "n" else f"({index})"

   return grouped if power == 1 else f"{grouped}^{{{power}}}"


def build(names):
   form = names["form"]
   centre = names["centre"]
   base = names["base"]
   power = int(names["power"])
   start = int(names["start"])
   coefficient = names["coefficient"]
   lead = "" if coefficient == 1 else f"{coefficient} "
   displacement = rf"\left({tex(x - centre)}\right)"
   absolute = rf"\left|{tex(x - centre)}\right|"
   index_power = _index_power_tex(power)
   exponent = "" if power == 1 else f"^{{{power}}}"
   below = "" if not index_power else " " + index_power

   if form == "divided":
      radius = sympy.Integer(base)
      power_factor = "" if power == 0 else rf"\left(\frac{{n+1}}{{n}}\right){exponent} "
      term = rf"\frac{{{lead}{index_power + ' ' if index_power else ''}{displacement}^{{n}}}}{{{base}^{{n}}}}"
      limit = rf"{INFINITY_LIMIT} {power_factor}\frac{{{absolute}}}{{{base}}} = \frac{{{absolute}}}{{{base}}}"
      solved = rf"{absolute} < {base}"
      incomplete = sympy.Integer(1)
      incomplete_how = f"n replaced by n + 1 in the power of the displacement but not in {base}^n, so the ratio tends to the bare displacement and the radius comes out as 1"
   elif form == "even":
      radius = sympy.sqrt(base)
      power_factor = "" if power == 0 else rf"\left(\frac{{n}}{{n+1}}\right){exponent} "
      term = rf"\frac{{{lead}{displacement}^{{2n}}}}{{{base}^{{n}}{below}}}"
      limit = rf"{INFINITY_LIMIT} {power_factor}\frac{{{absolute}^{{2}}}}{{{base}}} = \frac{{{absolute}^{{2}}}}{{{base}}}"
      solved = rf"{absolute}^{{2}} < {base}"
      incomplete = sympy.Integer(base)
      incomplete_how = "the exponent 2n advanced to 2n + 1 instead of 2n + 2, so the ratio carries the displacement to the first power only"
   else:
      radius = sympy.Rational(1, base)
      power_factor = "" if power == 0 else rf"\left(\frac{{n}}{{n+1}}\right){exponent} "
      multiplier = "" if coefficient == 1 else rf"{coefficient} \cdot "
      numerator = rf"{multiplier}{base}^{{n}} {displacement}^{{n}}"
      term = rf"\frac{{{numerator}}}{{{index_power}}}" if index_power else numerator
      limit = rf"{INFINITY_LIMIT} {power_factor}{base} {absolute} = {base} {absolute}"
      solved = rf"{base} {absolute} < 1"
      incomplete = sympy.Integer(1)
      incomplete_how = f"n replaced by n + 1 in the power of the displacement but not in {base}^n, so the ratio tends to the bare displacement and the radius comes out as 1"

   bound_text = rf"{absolute} < {tex(radius)}"
   restated = solved == bound_text
   solved_text = math(solved) if restated else f"{math(solved)}, that is {math(bound_text)}"
   stem = f"Find the radius of convergence of the power series {math(rf'\sum_{{n={start}}}^{{\infty}} {term}')}."
   steps = [
      Step(text=f"For the ratio test, form {math(rf'\left|\frac{{a_{{n+1}}}}{{a_n}}\right|')} from consecutive terms of {math(term)}.", point_type_id="BC-PT-99042", rule="ratio of consecutive terms"),
      Step(text=f"Its limit is {math(limit)}.", point_type_id="BC-PT-99043", rule="limit of the ratio"),
      Step(text=f"The series converges when this limit is less than 1: {solved_text}, so the radius of convergence is {math(f'R = {tex(radius)}')}.", value=radius, point_type_id="BC-PT-99047", rule="radius stated"),
   ]

   low = centre - radius
   high = centre + radius
   one_sided = centre + radius
   distractors = [
      Distractor("BC-ERR-10036", "the interval of convergence written where the radius was asked for", label=math(rf"{tex(low)} < x < {tex(high)}")),
      Distractor("BC-ERR-10021", incomplete_how, label=math(f"R = {tex(incomplete)}")),
      Distractor("BC-ERR-10022", f"the ratio test done without absolute values, so the inequality became x < {one_sided} and that bound was reported as the radius", label=math(f"R = {tex(one_sided)}")),
   ]

   for distractor in distractors:
      distractor.mechanism = "conceptual_confusion"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=math(f"R = {tex(radius)}")),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"radius": radius},
   )
