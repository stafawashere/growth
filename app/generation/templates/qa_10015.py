"""BC-QA-10015, one endpoint of a power series substituted, the numerical series identified and tested."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import x

ARCHETYPE_ID = "BC-QA-10015"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["power", "shifted"]}},
      {"name": "power", "type": "rational", "role": "difficulty", "domain": {"values": ["1/3", "1/2", "1", "3/2", "2"]}},
      {"name": "sign", "type": "label", "role": "difficulty", "domain": {"values": ["positive", "alternating"]}},
      {"name": "end", "type": "label", "role": "difficulty", "domain": {"values": ["right", "left"]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["value", "implicit"]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "radius", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
   ],
   "constraints": [
      "abs(centre) != 2 * radius",
   ],
   "derived": [],
   "invariants": [
      "verdict in ['converges', 'diverges']",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-14", "settings": {"value": "off", "implicit": "low"}},
      {"parameter": "form", "difficulty_factor_id": "BC-DF-14", "settings": {"power": "off", "shifted": "low"}},
      {"parameter": "power", "difficulty_factor_id": "BC-DF-14", "settings": {"1/3": "off", "1/2": "off", "1": "off", "3/2": "off", "2": "off"}},
      {"parameter": "sign", "difficulty_factor_id": "BC-DF-14", "settings": {"positive": "off", "alternating": "off"}},
      {"parameter": "end", "difficulty_factor_id": "BC-DF-14", "settings": {"right": "off", "left": "off"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "power", "sign", "end", "centre", "radius"]},
   ],
   "notes": "The power series is the sum from n = 1 of (x - centre)^n over radius^n times n^power (or n^power + shift). At an endpoint the factor (x - centre)^n / radius^n becomes 1 or (-1)^n, so the endpoint series is a p-series, a shifted p-series, or an alternating version of either. The centre is never 0 or twice the radius, so putting the endpoint itself in place of x - centre gives a series whose ratio is not 1.",
}


def _size_tex(form, power, shift, index="n"):
   if power == 1:
      base = index
   elif power == sympy.Rational(1, 2):
      base = rf"\sqrt{{{index}}}"
   else:
      base = rf"{index}^{{{tex(power)}}}"

   return f"{base} + {shift}" if form == "shifted" else base


def build(names):
   form = names["form"]
   power = names["power"]
   shift = names["shift"]
   centre = names["centre"]
   radius = names["radius"]
   is_right = names["end"] == "right"
   power_alternates = names["sign"] == "alternating"

   endpoint = centre + radius if is_right else centre - radius
   is_left = not is_right
   endpoint_alternates = power_alternates != is_left
   size = _size_tex(form, power, shift)
   sign_tex = "(-1)^{n} " if power_alternates else ""
   displacement = rf"\left({tex(x - centre)}\right)"
   size_factor = rf"\left({size}\right)" if form == "shifted" else size
   series = rf"\sum_{{n=1}}^{{\infty}} \frac{{{sign_tex}{displacement}^{{n}}}}{{{radius}^{{n}} {size_factor}}}"
   endpoint_numerator = "(-1)^{n}" if endpoint_alternates else "1"
   endpoint_series = rf"\sum_{{n=1}}^{{\infty}} \frac{{{endpoint_numerator}}}{{{size}}}"
   end_word = "right" if is_right else "left"

   if names["given"] == "value":
      stem = (
         f"The power series {math(series)} has radius of convergence {math(str(radius))}. Determine whether the series "
         f"converges or diverges at {math(f'x = {endpoint}')}, naming the test used."
      )
   else:
      stem = (
         f"Determine whether the power series {math(series)} converges or diverges at the {end_word} endpoint of its "
         "interval of convergence, naming the test used."
      )

   factor_value = rf"\left(\frac{{{endpoint - centre}}}{{{radius}}}\right)^{{n}}"
   factor_result = "(-1)^{n}" if (endpoint - centre) < 0 else "1"
   steps = [
      Step(text=f"The ratio test gives convergence for {math(rf'\left|{tex(x - centre)}\right| < {radius}')}, so the {end_word} endpoint is {math(f'x = {endpoint}')}.", rule="locate the endpoint"),
      Step(text=f"At {math(f'x = {endpoint}')}, {math(rf'\frac{{{displacement}^{{n}}}}{{{radius}^{{n}}}} = {factor_value} = {factor_result}')}, so the series becomes {math(endpoint_series)}.", rule="substitute the endpoint"),
   ]

   converges_absolutely = power > 1
   is_shifted = form == "shifted"
   plain_size = _size_tex("power", power, shift)
   partner = math(rf"\sum \frac{{1}}{{{plain_size}}}")
   sizes = math(rf"\frac{{1}}{{{size}}}")
   above_one = math(f"p = {tex(power)} > 1")
   at_most_one = math(rf"p = {tex(power)} \le 1")
   at_endpoint = f"At {math(f'x = {endpoint}')}"

   def option(verdict, test, reason):
      return f"{at_endpoint} the series {verdict} by {test}, because {reason}."

   if endpoint_alternates:
      verdict = "converges"
      key = option(verdict, "the alternating series test", f"the sizes {sizes} decrease to 0")
      steps.append(Step(text=f"The terms alternate in sign, their sizes {sizes} decrease as n increases, and {math(rf'\lim_{{n\to\infty}} \frac{{1}}{{{size}}} = 0')}.", rule="alternating series test"))
   elif converges_absolutely and is_shifted:
      verdict = "converges"
      key = option(verdict, f"direct comparison with {partner}", above_one)
      steps.append(Step(text=f"The terms are positive and {math(rf'\frac{{1}}{{{size}}} < \frac{{1}}{{{plain_size}}}')}, the terms of a convergent p-series with {above_one}.", rule="direct comparison test"))
   elif converges_absolutely:
      verdict = "converges"
      key = option(verdict, "the p-series test", above_one)
      steps.append(Step(text=f"It is a p-series with {above_one}.", rule="p-series test"))
   elif is_shifted:
      verdict = "diverges"
      key = option(verdict, f"limit comparison with {partner}", at_most_one)
      steps.append(Step(text=f"The terms are positive and {math(rf'\lim_{{n\to\infty}} \frac{{{plain_size}}}{{{size}}} = 1')}, which is positive and finite, and the p-series with {at_most_one} diverges.", rule="limit comparison test"))
   else:
      verdict = "diverges"
      key = option(verdict, "the p-series test", at_most_one)
      steps.append(Step(text=f"It is a p-series with {at_most_one}.", rule="p-series test"))

   belongs = "belongs" if verdict == "converges" else "does not belong"
   steps.append(Step(text=f"{key[:-1]}, so {math(f'x = {endpoint}')} {belongs} to the interval of convergence.", rule="verdict at the endpoint"))

   open_interval = Distractor(
      "BC-ERR-10037",
      "the endpoint never examined: the open interval from the ratio test taken as the whole answer",
      label=option("diverges", "the ratio test", f"{math(f'{centre - radius} < x < {centre + radius}')} leaves it out"),
   )

   if is_left:
      dropped_alternates = power_alternates

      if dropped_alternates:
         dropped_verdict, dropped_test, dropped_reason = "converges", "the alternating series test", f"the terms {math(rf'\frac{{(-1)^n}}{{{size}}}')} alternate and shrink"
      elif converges_absolutely:
         dropped_verdict, dropped_test, dropped_reason = "converges", "the p-series test", f"{math(rf'\sum \frac{{1}}{{{size}}}')} has {above_one}"
      else:
         dropped_verdict, dropped_test, dropped_reason = "diverges", "the p-series test", f"{math(rf'\sum \frac{{1}}{{{size}}}')} has {at_most_one}"

      first = Distractor(
         "BC-ERR-10034",
         f"the factor (-1)^n produced by substituting the negative displacement {endpoint - centre} dropped, so the endpoint series was tested with the wrong sign pattern",
         label=option(dropped_verdict, dropped_test, dropped_reason),
         mechanism="sign_error",
      )
   else:
      first = open_interval

   # A dropped (-1)^n that leaves a convergent p-series still reaches a true conclusion, so it is no distractor.
   dropped_is_true = is_left and endpoint_alternates and converges_absolutely
   distractors = [] if dropped_is_true else [first]
   limit_only = Distractor("BC-ERR-10020", "the alternating series test applied with only the limit condition, the decrease of the sizes never stated", label=option("converges", "the alternating series test", math(rf"\lim_{{n\to\infty}} \frac{{1}}{{{size}}} = 0")))

   if endpoint_alternates and converges_absolutely:
      distractors.append(limit_only)
      distractors.append(open_interval)
      distractors.append(Distractor("BC-ERR-10017", "the limit of the sizes written as an equation without limit notation, so the term itself is set equal to 0", label=option("converges", "the alternating series test", math(rf"\frac{{1}}{{{size}}} = 0"))))
   elif endpoint_alternates:
      distractors.append(Distractor("BC-ERR-10015", "the p-series test used on the alternating endpoint series, whose terms are not all positive", label=option("diverges", "the p-series test", at_most_one)))
      distractors.append(limit_only)
   else:
      distractors.append(Distractor("BC-ERR-10015", "the alternating series test used on the endpoint series although its terms are all positive", label=option("converges", "the alternating series test", f"the sizes {sizes} decrease to 0")))

      if is_shifted and not converges_absolutely:
         distractors.append(Distractor("BC-ERR-10016", "the comparison inequality in the direction that cannot show divergence: terms smaller than those of a divergent series", label=option("diverges", f"direct comparison with {partner}", math(rf"\frac{{1}}{{{size}}} < \frac{{1}}{{{plain_size}}}"))))
      elif converges_absolutely:
         distractors.append(Distractor("BC-ERR-10014", "the p-series threshold reversed, so p greater than 1 read as divergence", label=option("diverges", "the p-series test", above_one)))
      else:
         is_harmonic = power == 1
         threshold = math(r"p = 1 \ge 1") if is_harmonic else math(f"p = {tex(power)} < 1")
         threshold_word = "at least 1" if is_harmonic else "less than 1"
         distractors.append(Distractor("BC-ERR-10014", f"the p-series threshold misapplied, p {threshold_word} read as convergence", label=option("converges", "the p-series test", threshold)))

   distractors.append(open_interval)
   seen = {key}
   chosen = []

   for distractor in distractors:
      is_new = distractor.label not in seen

      if is_new:
         chosen.append(distractor)
         seen.add(distractor.label)

   distractors = chosen[:3]

   for distractor in distractors:
      distractor.mechanism = distractor.mechanism or "conceptual_confusion"

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
