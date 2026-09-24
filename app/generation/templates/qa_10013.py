"""BC-QA-10013, the interval of convergence of a power series by the ratio test and two endpoint tests."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import INFINITY_LIMIT, series_tex, x

ARCHETYPE_ID = "BC-QA-10013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "power", "type": "rational", "role": "difficulty", "domain": {"values": ["0", "1/2", "1", "2"]}},
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "alternating"]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "radius", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "interval_kind in ['open', 'closed', 'left_closed', 'right_closed']",
   ],
   "dial_bindings": [
      {"parameter": "power", "difficulty_factor_id": "BC-DF-09", "settings": {"0": "low", "1/2": "medium", "1": "medium", "2": "low"}},
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-02", "settings": {"positive": "off", "alternating": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["power", "sign", "centre", "radius"]},
   ],
   "notes": "The series is the sum from n = 1 of (x - centre)^n over radius^n n^power, with an optional (-1)^n; the ratio test gives |x - centre| < radius, one endpoint yields a p-series and the other an alternating p-series.",
}


def _interval_tex(low, high, includes_low, includes_high):
   left = r"\le" if includes_low else "<"
   right = r"\le" if includes_high else "<"

   return math(f"{low} {left} x {right} {high}")


def _endpoint_analysis(power, alternates, coefficient, start):
   """What the endpoint series is, the test that settles it, and whether it converges."""
   is_constant = power == 0
   lead = "" if coefficient == 1 else f"{coefficient} "
   sign = "(-1)^n" if alternates else ""
   numerator = f"{lead}{sign}".strip() or "1"
   limits = rf"\sum_{{n={start}}}^{{\infty}}"

   if is_constant:
      series = f"{limits} {numerator}"
   else:
      series = rf"{limits} \frac{{{numerator}}}{{{_index_power_tex('n', power)}}}"

   if alternates and is_constant:
      return series, "diverges by the nth term test, since its terms do not approach 0", False

   if alternates:
      return series, "converges by the alternating series test, since its terms alternate and their sizes decrease to 0", True

   if is_constant:
      return series, f"diverges by the nth term test, since every term equals {coefficient}", False

   converges = power > 1
   verdict = "converges" if converges else "diverges"
   relation = ">" if converges else r"\le"

   return series, f"{verdict} by the p-series test, since it is a multiple of a p-series with {math(f'p = {tex(power)} {relation} 1')}", converges


def _index_power_tex(index, power):
   grouped = index if index == "n" else f"({index})"

   if power == 1:
      return grouped

   if power == sympy.Rational(1, 2):
      return rf"\sqrt{{{index}}}"

   return rf"{grouped}^{{{tex(power)}}}"


def _term_tex(index, coefficient, is_alternating, centre, radius, power):
   """The general term written as a single fraction, with the index given as text."""
   sign = rf"(-1)^{{{index}}} " if is_alternating else ""
   lead = "" if coefficient == 1 else f"{coefficient} "
   base = "x" if centre == 0 else rf"\left({tex(x - centre)}\right)"
   numerator = rf"{lead}{sign}{base}^{{{index}}}"

   index_power = "" if power == 0 else " " + _index_power_tex(index, power)

   return rf"\frac{{{numerator}}}{{{radius}^{{{index}}}{index_power}}}"


def build(names):
   power = names["power"]
   centre = names["centre"]
   radius = names["radius"]
   is_alternating = names["sign"] == "alternating"
   low = centre - radius
   high = centre + radius
   displacement_abs = rf"\left|{tex(x - centre)}\right|"
   coefficient = names["coefficient"]
   term_tex = _term_tex("n", coefficient, is_alternating, centre, radius, power)
   next_term_tex = _term_tex("n+1", coefficient, is_alternating, centre, radius, power)
   ratio_tex = rf"\left|\frac{{{next_term_tex}}}{{{term_tex}}}\right|"
   power_factor = "" if power == 0 else r" \cdot " + _index_power_tex(r"\frac{n}{n+1}", power).replace("(\\frac", "\\left(\\frac").replace("})", "}\\right)")
   limit_tex = rf"{INFINITY_LIMIT} {ratio_tex} = {INFINITY_LIMIT} \frac{{{displacement_abs}}}{{{radius}}}{power_factor} = \frac{{{displacement_abs}}}{{{radius}}}"

   # At x = high the factor (x - centre)^n / radius^n is 1, and at x = low it is (-1)^n.
   high_series, high_reason, high_included = _endpoint_analysis(power, is_alternating, coefficient, names["start"])
   low_series, low_reason, low_included = _endpoint_analysis(power, not is_alternating, coefficient, names["start"])

   key_tex = _interval_tex(low, high, low_included, high_included)
   both = low_included and high_included
   neither = not low_included and not high_included

   if both:
      interval_kind = "closed"
   elif neither:
      interval_kind = "open"
   elif low_included:
      interval_kind = "left_closed"
   else:
      interval_kind = "right_closed"

   stem = (
      f"Find the interval of convergence of the power series {math(series_tex(term_tex, names['start']))}. "
      "Use the ratio test for the interior and justify the behaviour at each endpoint."
   )
   steps = [
      Step(text=f"For the ratio test, form {math(ratio_tex)}.", point_type_id="BC-PT-99042", rule="ratio of consecutive terms"),
      Step(text=f"{math(limit_tex)}.", point_type_id="BC-PT-99043", rule="limit of the ratio"),
      Step(text=f"The series converges when {math(rf'\frac{{{displacement_abs}}}{{{radius}}} < 1')}, that is {math(rf'{displacement_abs} < {radius}')}, so {math(f'{low} < x < {high}')}.", point_type_id="BC-PT-99044", rule="interior of the interval"),
      Step(text=f"At {math(f'x = {high}')} the series is {math(high_series)}, which {high_reason}. At {math(f'x = {low}')} the series is {math(low_series)}, which {low_reason}.", point_type_id="BC-PT-99045", rule="endpoint tests"),
      Step(text=f"The interval of convergence is {key_tex}.", point_type_id="BC-PT-99046", rule="interval with matching endpoints"),
   ]

   high_relation = r"\le" if high_included else "<"
   half_line = math(f"x {high_relation} {high}")
   low_end_alternates = not is_alternating
   dropped_absolute = Distractor(
      "BC-ERR-99037",
      f"the absolute value dropped when solving, so {tex(x - centre)} < {radius} was kept as the whole solution and only the endpoint {high} tested",
      label=f"The interval of convergence is {half_line}.",
   )

   if neither:
      distractors = [
         Distractor("BC-ERR-10038", "both endpoints included although each endpoint series was shown to diverge", label=f"The interval of convergence is {_interval_tex(low, high, True, True)}."),
         Distractor("BC-ERR-99017", "the endpoint series with alternating signs tested with the alternating series test although its terms do not approach 0, and called convergent", label=f"The interval of convergence is {_interval_tex(low, high, low_end_alternates, is_alternating)}."),
         dropped_absolute,
      ]
   elif both:
      distractors = [
         Distractor("BC-ERR-10037", "the endpoints left untested, so the open interval from the ratio test reported as the answer", label=f"The interval of convergence is {_interval_tex(low, high, False, False)}."),
         Distractor("BC-ERR-10038", "the endpoint where the series is a positive p-series excluded, although the p-series test showed it converges", label=f"The interval of convergence is {_interval_tex(low, high, low_end_alternates, is_alternating)}."),
         dropped_absolute,
      ]
   else:
      distractors = [
         Distractor("BC-ERR-10037", "the endpoints left untested, so the open interval from the ratio test reported as the answer", label=f"The interval of convergence is {_interval_tex(low, high, False, False)}."),
         Distractor("BC-ERR-10038", "the brackets placed the other way round from the endpoint verdicts, the convergent end excluded and the divergent end included", label=f"The interval of convergence is {_interval_tex(low, high, high_included, low_included)}."),
         dropped_absolute,
      ]

   for distractor in distractors:
      distractor.mechanism = "conceptual_confusion"

   dropped_absolute.mechanism = "sign_error"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=f"The interval of convergence is {key_tex}."),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-11",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"interval_kind": interval_kind},
   )
