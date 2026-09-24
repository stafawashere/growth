"""BC-QA-10005, the integral test with its three conditions, an improper integral in limit notation and a verdict."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import series_tex, x

ARCHETYPE_ID = "BC-QA-10005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["squared", "gaussian", "plain", "cubic"]}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3, 4, 5]}},
      {"name": "shift", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 15, "step": 1}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 15, "step": 1}},
   ],
   "constraints": [
      "form != 'squared' or shift < 3 * start ** 2",
      "form != 'plain' or shift < start ** 2 + 1",
      "form != 'cubic' or 2 * shift < start ** 3 + 1",
   ],
   "derived": [],
   "invariants": [
      "verdict in ['converges', 'diverges']",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-09", "settings": {"squared": "low", "gaussian": "low", "plain": "low", "cubic": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "start", "shift", "coefficient"]},
   ],
   "notes": "f(x) = c x / (x^2 + k)^2 gives a convergent integral equal to c / (2 (s^2 + k)); f(x) = c x e^(-k x^2) gives c e^(-k s^2) / (2k); f(x) = c x / (x^2 + k) and f(x) = c x^2 / (x^3 + k) give divergent ones. The shift is small enough that f decreases on the whole interval from the starting index.",
}


def build(names):
   start = int(names["start"])
   shift = names["shift"]
   coefficient = names["coefficient"]
   form = names["form"]
   converges = form in ("squared", "gaussian")
   upper = sympy.Symbol("b", positive=True)

   if form == "squared":
      function = coefficient * x / (x**2 + shift) ** 2
      antiderivative = -coefficient / (2 * (x**2 + shift))
      value = sympy.Rational(coefficient, 2 * (start**2 + shift))
      early_value = sympy.Rational(coefficient, 2 * ((start - 1) ** 2 + shift))
      limit_of_bound = "0"
   elif form == "gaussian":
      function = coefficient * x * sympy.exp(-shift * x**2)
      antiderivative = -sympy.Rational(coefficient, 2 * shift) * sympy.exp(-shift * x**2)
      value = sympy.Rational(coefficient, 2 * shift) * sympy.exp(-shift * start**2)
      early_value = sympy.Rational(coefficient, 2 * shift) * sympy.exp(-shift * (start - 1) ** 2)
      limit_of_bound = "0"
   elif form == "cubic":
      function = coefficient * x**2 / (x**3 + shift)
      antiderivative = coefficient * sympy.log(x**3 + shift) / 3
      value = sympy.oo
      early_value = sympy.oo
      limit_of_bound = r"\infty"
   else:
      function = coefficient * x / (x**2 + shift)
      antiderivative = coefficient * sympy.log(x**2 + shift) / 2
      value = sympy.oo
      early_value = sympy.oo
      limit_of_bound = r"\infty"

   verdict = "converges" if converges else "diverges"
   series = math(series_tex("a_n", start))
   short_series = math(r"\sum a_n")
   interval = math(rf"[{start}, \infty)")
   conditions = f"f is positive, decreasing and continuous on {interval}"

   def improper(low, result):
      return math(rf"\lim_{{b\to\infty}} \int_{{{low}}}^{{b}} f(x)\,dx = {tex(result)}")

   key = f"{short_series} {verdict}, because {conditions} and {improper(start, value)}."
   stem = (
      f"Let {math('f(x) = ' + tex(function))} and {math('a_n = f(n)')}. State the conditions the integral test requires for "
      f"the series {series}, and use the test to determine whether the series converges or diverges."
   )

   denominator = sympy.denom(sympy.together(function))
   has_denominator = not function.has(sympy.exp)

   if has_denominator:
      continuity = f"continuous because {math(tex(denominator))} is positive there"
   else:
      continuity = "continuous as a product of continuous functions"

   evaluated = rf"\lim_{{b\to\infty}} \left[{tex(antiderivative)}\right]_{{{start}}}^{{b}} = \lim_{{b\to\infty}} \left({tex(antiderivative.subs(x, upper))} - \left({tex(antiderivative.subs(x, start))}\right)\right)"
   steps = [
      Step(text=f"On {interval}, f is positive, {continuity}, and decreasing because {math(rf'f^{{\prime}}(x) = {tex(sympy.factor(sympy.diff(function, x)))}')} is negative there.", point_type_id="BC-PT-99005", rule="integral test conditions"),
      Step(text=f"An antiderivative of f is {math(tex(antiderivative))}.", point_type_id="BC-PT-99003", rule="substitution"),
      Step(text=f"{math(evaluated)}, and the first term approaches {math(limit_of_bound)}, so {improper(start, value)}.", point_type_id="BC-PT-99053", rule="limit notation on an improper integral"),
      Step(text=f"The integral {verdict}, so by the integral test {series} {verdict}.", rule="integral test"),
   ]

   incomplete = Distractor("BC-ERR-10010", "the conditions listed incompletely, with only positivity checked", label=f"{short_series} {verdict}, because f is positive on {interval} and {improper(start, value)}.")
   wrong_start = Distractor("BC-ERR-10012", f"the improper integral started at {start - 1}, an index the series does not use", label=f"{short_series} {verdict}, because {conditions} and {improper(start - 1, early_value)}.")

   if converges:
      distractors = [
         Distractor("BC-ERR-10013", "the value of the improper integral reported as the sum of the series", label=f"{short_series} converges to {math(tex(value))}, because {conditions} and {improper(start, value)}."),
         incomplete,
         wrong_start,
      ]
   else:
      distractors = [
         incomplete,
         wrong_start,
         Distractor("BC-ERR-10003", "the conclusion stated with no series named, so it could be read as a statement about the integral", label=f"It diverges, because {conditions} and {improper(start, value)}."),
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
      command_verb="determine",
      notes={"verdict": verdict},
   )
