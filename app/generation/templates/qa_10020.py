"""BC-QA-10020, whether a Taylor series converges to its function at an endpoint input, with the position as the reason."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import x

ARCHETYPE_ID = "BC-QA-10020"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "case", "type": "label", "role": "difficulty", "domain": {"values": ["geometric_left", "log_right", "log_left"]}},
      {"name": "framing", "type": "label", "role": "difficulty", "domain": {"values": ["radius_given", "radius_found"]}},
      {"name": "centre", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "radius", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "answer in ['yes', 'no']",
   ],
   "dial_bindings": [
      {"parameter": "case", "difficulty_factor_id": "BC-DF-10", "settings": {"geometric_left": "low", "log_right": "medium", "log_left": "medium"}},
      {"parameter": "framing", "difficulty_factor_id": "BC-DF-14", "settings": {"radius_given": "off", "radius_found": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["case", "centre", "radius", "coefficient"]},
   ],
   "notes": "Geometric: f(x) = k b / (a + b - x), whose series about a converges on a - b < x < a + b; the input is the left endpoint. Logarithmic: f(x) = k ln(1 + (x - a)/b), whose series converges on a - b < x <= a + b; the input is either endpoint.",
}


def build(names):
   case = names["case"]
   centre = names["centre"]
   radius = names["radius"]
   coefficient = names["coefficient"]
   low = centre - radius
   high = centre + radius
   is_geometric = case == "geometric_left"
   displacement = x - centre
   lead = "" if coefficient == 1 else f"{coefficient} "

   if is_geometric:
      function_tex = tex(coefficient * radius / (centre + radius - x))
      general = rf"{lead}\left(\frac{{{tex(displacement)}}}{{{radius}}}\right)^{{n}}"
      series = rf"\sum_{{n=0}}^{{\infty}} {general}"
      includes_low = False
      includes_high = False
   else:
      function_tex = rf"{lead}\ln\left(1 + \frac{{{tex(displacement)}}}{{{radius}}}\right)"
      power_base = "x" if centre == 0 else rf"\left({tex(displacement)}\right)"
      general = rf"\frac{{{lead}(-1)^{{n+1}} {power_base}^{{n}}}}{{n \cdot {radius}^{{n}}}}"
      series = rf"\sum_{{n=1}}^{{\infty}} {general}"
      includes_low = False
      includes_high = True

   is_right = case == "log_right"
   point = high if is_right else low
   converges_at_point = includes_high if is_right else includes_low
   answer = "yes" if converges_at_point else "no"
   point_tex = math(f"x = {point}")

   def bounds(left_closed, right_closed):
      left = r"\le" if left_closed else "<"
      right = r"\le" if right_closed else "<"

      return math(f"{low} {left} x {right} {high}")

   interval = bounds(includes_low, includes_high)
   open_interval = bounds(False, False)

   stem = f"Let {math('f(x) = ' + function_tex)}. The Taylor series for f about {math(f'x = {centre}')} is {math(series)}."

   if names["framing"] == "radius_given":
      stem += f" Its radius of convergence is {math(str(radius))}."

   stem += f" Does the series converge to f at {point_tex}? Give a reason for the answer."

   if converges_at_point:
      key = f"Yes, because {point_tex} is an endpoint that the interval of convergence {interval} includes."
   else:
      key = f"No, because {point_tex} is an endpoint that the interval of convergence {interval} excludes."

   endpoint_numerator = f"{lead}(-1)^{{n}}".strip() if is_geometric else None
   steps = [
      Step(text=f"The ratio test gives convergence for {math(rf'\left|{tex(displacement)}\right| < {radius}')}, the interior {open_interval}, and {point_tex} is an endpoint.", rule="interval in play"),
   ]

   if is_geometric:
      steps.append(Step(text=f"At {point_tex} the series is {math(rf'\sum_{{n=0}}^{{\infty}} {endpoint_numerator}')}, whose terms do not approach 0, so it diverges there. The interval of convergence is {interval}.", rule="endpoint test"))
   elif is_right:
      steps.append(Step(text=f"At {point_tex} the series is {math(rf'\sum_{{n=1}}^{{\infty}} \frac{{{lead}(-1)^{{n+1}}}}{{n}}')}, which converges by the alternating series test, so the interval of convergence is {interval}.", rule="endpoint test"))
   else:
      steps.append(Step(text=f"At {point_tex} the series is {math(rf'\sum_{{n=1}}^{{\infty}} \frac{{-{coefficient}}}{{n}}')}, a multiple of the harmonic series, which diverges, so the interval of convergence is {interval}.", rule="endpoint test"))

   steps.append(Step(text=key, point_type_id="BC-PT-99005", rule="position of the input"))

   circular = Distractor(
      "BC-ERR-10043",
      "the verdict asserted with no reason that places the input relative to the interval",
      label="Yes, because the series converges to f at every point where f is defined." if is_geometric else f"Yes, because the series converges to f at {point_tex}.",
   )

   if is_geometric:
      value_at_point = sympy.Rational(coefficient, 2)
      distractors = [
         Distractor(
            "BC-ERR-10005",
            "the geometric sum formula applied with ratio -1, whose size is not less than 1",
            label=f"Yes, because the geometric sum {math(rf'\frac{{{coefficient}}}{{1 - (-1)}} = {tex(value_at_point)}')} equals {math(f'f({point})')}.",
         ),
         Distractor(
            "BC-ERR-10038",
            "the excluded left endpoint written into the interval with a closed bracket",
            label=f"Yes, because {point_tex} lies in the interval of convergence {bounds(True, False)}.",
         ),
         circular,
      ]
   elif is_right:
      distractors = [
         Distractor(
            "BC-ERR-10037",
            "the endpoint never examined, so the open interval from the ratio test was used to decide",
            label=f"No, because {point_tex} lies outside the open interval {open_interval}.",
         ),
         Distractor(
            "BC-ERR-10038",
            "the brackets written the other way round from the endpoint analysis, the convergent right end excluded and the divergent left end included",
            label=f"No, because {point_tex} is an endpoint that the interval of convergence {bounds(True, False)} excludes.",
         ),
         circular,
      ]
   else:
      distractors = [
         Distractor(
            "BC-ERR-10038",
            "the brackets written the other way round from the endpoint analysis, the divergent left end included",
            label=f"Yes, because {point_tex} is an endpoint that the interval of convergence {bounds(True, False)} includes.",
         ),
         Distractor(
            "BC-ERR-10037",
            "the endpoint never examined, so the open interval from the ratio test was used to decide",
            label=f"No, because {point_tex} lies outside the open interval {open_interval}.",
         ),
         circular,
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
      command_verb="justify",
      notes={"answer": answer},
   )
