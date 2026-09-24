"""BC-QA-10001, choosing a convergence test that fits the general term and applying it to a verdict."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import INFINITY_LIMIT, n, series_tex

ARCHETYPE_ID = "BC-QA-10001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["pseries", "nth_term", "geometric", "ratio_power", "ratio_factorial", "alternating"]}},
      {"name": "power", "type": "rational", "role": "difficulty", "domain": {"values": ["1/3", "1/2", "2/3", "1", "4/3", "3/2", "2", "3"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 9, "step": 1}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "lead_top", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "constant_top", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "lead_bottom", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "constant_bottom", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "ratio", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1/3", "2/3", "1/4", "3/4", "2/5", "3/5", "4/5", "5/6", "2/7", "3/7", "5/7"]}},
      {"name": "base", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 6, "step": 1}},
      {"name": "degree", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
   ],
   "constraints": [
      "form != 'alternating' or power <= 1",
      "form != 'nth_term' or constant_top * lead_bottom != lead_top * constant_bottom",
   ],
   "derived": [],
   "invariants": [
      "verdict in ['converges', 'diverges']",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-09", "settings": {"pseries": "off", "nth_term": "off", "geometric": "off", "ratio_power": "low", "ratio_factorial": "low", "alternating": "low"}},
      {"parameter": "power", "difficulty_factor_id": "BC-DF-02", "settings": {"1/3": "low", "1/2": "low", "2/3": "low", "1": "off", "4/3": "low", "3/2": "low", "2": "off", "3": "off"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-11", "figure_kind": None, "requires": ["form", "power", "coefficient", "start"]},
   ],
   "notes": "Six general-term shapes, each matched to one test: a multiple of a p-series, a rational term with a nonzero limit, a geometric term written as a quotient of powers, a polynomial over an exponential, an exponential over a factorial, and an alternating p-series with p at most 1.",
}

LIMIT_OF_TERMS = rf"{INFINITY_LIMIT} a_n"
LIMIT_OF_RATIO = rf"{INFINITY_LIMIT} \left|\frac{{a_{{n+1}}}}{{a_n}}\right|"
NTH_TERM = "the nth term test"
RATIO = "the ratio test"
P_SERIES = "the p-series test"
GEOMETRIC = "the geometric series test"
ALTERNATING = "the alternating series test"


def _option(verdict, test, reason):
   """Every option has the same shape: a verdict, the test it credits, and one line of mathematics."""
   return f"The series {verdict} by {test}, because {math(reason)}."


def _terms_to_zero():
   return Distractor(
      "BC-ERR-10008",
      "convergence concluded from the terms approaching 0, a condition that is necessary but never sufficient",
      label=_option("converges", NTH_TERM, f"{LIMIT_OF_TERMS} = 0"),
   )


def _alternating_misuse():
   return Distractor(
      "BC-ERR-10009",
      "the alternating series test named for a series of positive terms, its alternating hypothesis never checked",
      label=f"The series converges by {ALTERNATING}, because {math('a_n')} decreases to 0.",
   )


def _pseries(names):
   coefficient = names["coefficient"]
   power = names["power"]
   term = coefficient / n**power
   converges = power > 1
   power_tex = tex(power)

   if converges:
      key = _option("converges", P_SERIES, f"p = {power_tex} > 1")
      threshold = _option("diverges", P_SERIES, f"p = {power_tex} > 1")
      threshold_how = "the p-series threshold reversed, so p greater than 1 read as divergence"
   else:
      key = _option("diverges", P_SERIES, rf"p = {power_tex} \le 1")
      is_harmonic = power == 1

      if is_harmonic:
         threshold = _option("converges", P_SERIES, r"p = 1 \ge 1")
         threshold_how = "the p-series threshold taken as p at least 1, so the harmonic case read as convergent"
      else:
         threshold = _option("converges", P_SERIES, f"p = {power_tex} < 1")
         threshold_how = "the p-series threshold reversed, so p less than 1 read as convergence"

   steps = [
      Step(text=f"The general term is {math(tex(term))}, a constant multiple of {math(rf'\frac{{1}}{{n^{{{power_tex}}}}}')}, so the p-series test fits: the terms are positive and the series is a p-series times {math(tex(coefficient))}.", rule="match the form to a test"),
      Step(text=f"Here {math(f'p = {power_tex}')}, and a p-series converges exactly when p is greater than 1.", value=power, rule="p-series test"),
      Step(text=key, rule="verdict"),
   ]
   distractors = [
      Distractor("BC-ERR-10014", threshold_how, label=threshold),
      _terms_to_zero(),
      _alternating_misuse(),
   ]

   return tex(term), "converges" if converges else "diverges", key, steps, distractors


def _nth_term(names):
   lead_top = names["lead_top"]
   constant_top = names["constant_top"]
   lead_bottom = names["lead_bottom"]
   constant_bottom = names["constant_bottom"]
   term = (lead_top * n + constant_top) / (lead_bottom * n + constant_bottom)
   limit_value = sympy.Rational(lead_top, lead_bottom)
   at_zero = sympy.Rational(constant_top, constant_bottom)
   key = _option("diverges", NTH_TERM, rf"{LIMIT_OF_TERMS} = {tex(limit_value)} \ne 0")

   steps = [
      Step(text=f"The general term {math(tex(term))} is a quotient of two linear expressions, so check its limit first with the nth term test.", rule="match the form to a test"),
      Step(text=f"Dividing the numerator and denominator by n gives {math(rf'{INFINITY_LIMIT} {tex(term)} = {tex(limit_value)}')}.", value=limit_value, rule="limit of the terms"),
      Step(text=key, rule="nth term test"),
   ]
   distractors = [
      Distractor("BC-ERR-10001", "the limit of the sequence of terms reported as the sum of the series", label=f"The series converges to {math(tex(limit_value))}, because {math(f'{LIMIT_OF_TERMS} = {tex(limit_value)}')}."),
      Distractor("BC-ERR-10007", "the limit of the terms evaluated by setting n to 0 instead of letting n grow", label=_option("diverges", NTH_TERM, rf"{LIMIT_OF_TERMS} = {tex(at_zero)} \ne 0")),
      Distractor("BC-ERR-10009", "the ratio test named, but its requirement of a limit below 1 not checked when the ratio tends to 1", label=_option("converges", RATIO, f"{LIMIT_OF_RATIO} = 1")),
   ]

   return tex(term), "diverges", key, steps, distractors


def _geometric(names):
   coefficient = names["coefficient"]
   ratio = names["ratio"]
   top, bottom = sympy.fraction(ratio)
   top_power = "" if top == 1 else rf"{top}^{{n}}"
   factors = [str(coefficient)] if coefficient != 1 else []
   factors += [top_power] if top_power else []
   numerator = r" \cdot ".join(factors) if factors else "1"
   written = rf"\frac{{{numerator}}}{{{bottom}^{{n}}}}"
   inverted = 1 / ratio
   key = _option("converges", GEOMETRIC, f"r = {tex(ratio)} < 1")

   steps = [
      Step(text=f"Each term is {math(tex(ratio))} times the one before, so the series is geometric and the geometric series test fits.", value=ratio, rule="match the form to a test"),
      Step(text=f"A geometric series converges exactly when its common ratio has absolute value less than 1, and {math(rf'\left|{tex(ratio)}\right| < 1')}.", rule="geometric series test"),
      Step(text=key, rule="verdict"),
   ]
   distractors = [
      Distractor("BC-ERR-10004", "the common ratio read upside down, as the denominator's base over the numerator's", label=_option("diverges", GEOMETRIC, f"r = {tex(inverted)} > 1")),
      _terms_to_zero(),
      _alternating_misuse(),
   ]

   return written, "converges", key, steps, distractors


def _ratio_power(names):
   base = names["base"]
   degree = names["degree"]
   limit_value = sympy.Rational(1, base)
   written = rf"\frac{{n^{{{degree}}}}}{{{base}^{{n}}}}"
   ratio_tex = rf"{LIMIT_OF_RATIO} = {INFINITY_LIMIT} \left(\frac{{n+1}}{{n}}\right)^{{{degree}}} \cdot \frac{{1}}{{{base}}} = {tex(limit_value)}"
   key = _option("converges", RATIO, f"{LIMIT_OF_RATIO} = {tex(limit_value)} < 1")

   steps = [
      Step(text=f"The general term {math(written)} has an exponential in the denominator, so the ratio test fits.", rule="match the form to a test"),
      Step(text=f"{math(ratio_tex)}.", value=limit_value, rule="ratio test"),
      Step(text=key, rule="verdict"),
   ]
   distractors = [
      Distractor("BC-ERR-10004", "the geometric test used on a series whose ratio of consecutive terms is not constant, with the ratio taken from the exponential alone", label=_option("converges", GEOMETRIC, f"r = {tex(limit_value)} < 1")),
      Distractor("BC-ERR-10007", "the limit of the terms taken as infinite because the numerator grows without bound", label=_option("diverges", NTH_TERM, rf"{LIMIT_OF_TERMS} = \infty")),
      _terms_to_zero(),
   ]

   return written, "converges", key, steps, distractors


def _ratio_factorial(names):
   base = names["base"]
   term = sympy.Integer(base) ** n / sympy.factorial(n)
   ratio_tex = rf"{LIMIT_OF_RATIO} = {INFINITY_LIMIT} \frac{{{base}}}{{n+1}} = 0"
   key = _option("converges", RATIO, f"{LIMIT_OF_RATIO} = 0 < 1")

   steps = [
      Step(text=f"The general term {math(tex(term))} contains a factorial, so the ratio test fits.", rule="match the form to a test"),
      Step(text=f"{math(ratio_tex)}.", rule="ratio test"),
      Step(text=key, rule="verdict"),
   ]
   distractors = [
      Distractor("BC-ERR-10004", "the series treated as geometric with the exponential's base as its ratio, ignoring the factorial", label=_option("diverges", GEOMETRIC, f"r = {base} > 1")),
      Distractor("BC-ERR-10007", "the limit of the terms taken as infinite because the numerator grows without bound", label=_option("diverges", NTH_TERM, rf"{LIMIT_OF_TERMS} = \infty")),
      _terms_to_zero(),
   ]

   return tex(term), "converges", key, steps, distractors


def _alternating(names):
   coefficient = names["coefficient"]
   power = names["power"]
   magnitude = coefficient / n**power
   term = (-1) ** n * magnitude
   power_tex = tex(power)
   key = f"The series converges by {ALTERNATING}, because {math('|a_n|')} decreases to 0."

   steps = [
      Step(text=f"The factor {math('(-1)^n')} makes the terms alternate, so the alternating series test fits.", rule="match the form to a test"),
      Step(text=f"The absolute values {math(tex(magnitude))} decrease as n increases, and {math(rf'{INFINITY_LIMIT} {tex(magnitude)} = 0')}.", rule="alternating series test conditions"),
      Step(text=key, rule="verdict"),
   ]
   distractors = [
      Distractor("BC-ERR-10008", "the verdict drawn from the terms approaching 0 alone, with the alternation and the decrease never used", label=_option("converges", NTH_TERM, f"{LIMIT_OF_TERMS} = 0")),
      Distractor("BC-ERR-10009", "the p-series test named for an alternating series, whose terms are not all positive as that test requires", label=_option("diverges", P_SERIES, rf"p = {power_tex} \le 1")),
      Distractor("BC-ERR-10001", "the limit of the sequence of terms reported as the sum of the series", label=f"The series converges to 0, because {math(f'{LIMIT_OF_TERMS} = 0')}."),
   ]

   return tex(term), "converges", key, steps, distractors


BUILDERS = {
   "pseries": _pseries,
   "nth_term": _nth_term,
   "geometric": _geometric,
   "ratio_power": _ratio_power,
   "ratio_factorial": _ratio_factorial,
   "alternating": _alternating,
}


def build(names):
   start = int(names["start"])
   term_tex, verdict, key, steps, distractors = BUILDERS[names["form"]](names)
   stem = (
      f"Determine whether the series {math(series_tex('a_n', start))}, where {math(f'a_n = {term_tex}')}, converges or diverges. "
      "Name a test whose conditions the series meets and state the verdict it gives."
   )

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
