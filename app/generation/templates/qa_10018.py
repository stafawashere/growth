"""BC-QA-10018, a power series differentiated term by term, with the radius kept and the endpoints rechecked."""

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import x

ARCHETYPE_ID = "BC-QA-10018"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "alternating"]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["interval", "none"]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 12, "step": 1}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "interval_kind in ['left_closed', 'right_closed']",
   ],
   "dial_bindings": [
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-04", "settings": {"positive": "low", "alternating": "medium"}},
      {"parameter": "given", "difficulty_factor_id": "BC-DF-14", "settings": {"interval": "off", "none": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["sign", "centre", "base", "coefficient"]},
   ],
   "notes": "f(x) is the sum from n = 1 of c (x - a)^n / (n^2 b^n), optionally with (-1)^n; it converges on the closed interval of radius b. Its derivative, the sum of c (x - a)^(n-1) / (n b^n), keeps the radius but loses one endpoint, where it becomes a multiple of the harmonic series.",
}


def _interval(low, high, left_closed, right_closed):
   left = r"\le" if left_closed else "<"
   right = r"\le" if right_closed else "<"

   return f"{low} {left} x {right} {high}"


def build(names):
   is_alternating = names["sign"] == "alternating"
   centre = names["centre"]
   base = names["base"]
   coefficient = names["coefficient"]
   low = centre - base
   high = centre + base
   lead = "" if coefficient == 1 else f"{coefficient} "
   sign = "(-1)^{n} " if is_alternating else ""
   displacement = "x" if centre == 0 else rf"\left({tex(x - centre)}\right)"

   original = rf"\sum_{{n=1}}^{{\infty}} \frac{{{lead}{sign}{displacement}^{{n}}}}{{n^{{2}} {base}^{{n}}}}"
   derived = rf"\sum_{{n=1}}^{{\infty}} \frac{{{lead}{sign}{displacement}^{{n-1}}}}{{n \cdot {base}^{{n}}}}"
   unlowered = rf"\sum_{{n=1}}^{{\infty}} \frac{{{lead}{sign}{displacement}^{{n}}}}{{n \cdot {base}^{{n}}}}"

   # At x = high the factor (x - a)^(n-1) / b^n is 1/b; at x = low it is (-1)^(n-1)/b.
   high_alternates = is_alternating
   high_included = high_alternates
   low_included = not high_alternates
   interval_kind = "left_closed" if low_included else "right_closed"
   key_interval = _interval(low, high, low_included, high_included)
   original_interval = _interval(low, high, True, True)

   stem = f"Let {math('f(x) = ' + original)}"

   if names["given"] == "interval":
      stem += f", whose interval of convergence is {math(original_interval)}"

   stem += ". Find the series for f prime obtained by term-by-term differentiation, and give the interval on which it converges."

   def option(series, interval):
      return f"{math(r'f^{\prime}(x) = ' + series)}, converging for {math(interval)}."

   key = option(derived, key_interval)
   endpoint_harmonic = rf"\sum \frac{{{lead}}}{{{base} n}}" if lead else rf"\sum \frac{{1}}{{{base} n}}"
   steps = [
      Step(text=f"Differentiate each term: the derivative of {math(rf'\frac{{{lead}{sign}{displacement}^{{n}}}}{{n^{{2}} {base}^{{n}}}}')} is {math(rf'\frac{{{lead}{sign}{displacement}^{{n-1}}}}{{n \cdot {base}^{{n}}}}')}, so {math(r'f^{\prime}(x) = ' + derived)}.", point_type_id="BC-PT-99038", rule="term-by-term differentiation"),
      Step(text=f"Term-by-term differentiation keeps the radius of convergence, so the radius is still {math(str(base))} and the series converges for {math(rf'\left|{tex(x - centre)}\right| < {base}')}.", point_type_id="BC-PT-99047", rule="radius unchanged"),
      Step(text=f"The endpoints must be checked again. At the endpoint where the terms keep one sign, the series is {math(endpoint_harmonic)}, a multiple of the harmonic series, which diverges. At the other endpoint the terms alternate and decrease to 0, so it converges by the alternating series test.", rule="endpoint tests"),
      Step(text=f"The series for f prime converges for {math(key_interval)}.", rule="interval of convergence"),
   ]
   distractors = [
      Distractor("BC-ERR-10037", "the interval of f carried over with both endpoints, the endpoints of the new series never tested", label=option(derived, original_interval)),
      Distractor("BC-ERR-10015", "the alternating endpoint series tested with the p-series test, whose positive-terms condition it fails, and so excluded", label=option(derived, _interval(low, high, False, False))),
      Distractor("BC-ERR-99018", "each coefficient divided by n but the power of the displacement left at n instead of lowered to n - 1", label=option(unlowered, key_interval)),
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
      command_verb="find",
      notes={"interval_kind": interval_kind},
   )
