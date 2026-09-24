"""BC-QA-10012, the Taylor polynomial of x^m f(kx) built from a known Maclaurin series."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_h import polynomial_tex, taylor_polynomial, x

ARCHETYPE_ID = "BC-QA-10012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "base", "type": "label", "role": "difficulty", "domain": {"values": ["exp", "sin", "cos", "geometric"]}},
      {"name": "power", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2, 3]}},
      {"name": "terms", "type": "integer", "role": "difficulty", "domain": {"values": [3, 4]}},
      {"name": "scale", "type": "rational", "role": "safe", "domain": {"values": ["-3", "-2", "2", "3", "1/4", "-1/2", "1/3", "-1/3"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 12, "step": 1}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "base", "difficulty_factor_id": "BC-DF-01", "settings": {"exp": "low", "sin": "medium", "cos": "medium", "geometric": "low"}},
      {"parameter": "power", "difficulty_factor_id": "BC-DF-01", "settings": {"1": "low", "2": "low", "3": "medium"}},
      {"parameter": "terms", "difficulty_factor_id": "BC-DF-01", "settings": {"3": "low", "4": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["base", "power", "terms", "scale", "coefficient"]},
   ],
   "notes": "g(x) = c x^m f(kx) for f one of e^x, sin x, cos x, 1/(1 - x); the requested degree is the one that keeps exactly the drawn number of nonzero terms (three or four), so a term with the scale raised to at least the second power is always present and a later nonzero term is left for the extra-term distractor.",
}

BASES = {
   "exp": (lambda order: sympy.Integer(1) / sympy.factorial(order), lambda order: sympy.Integer(1), "e^{x}", "the factorials dropped from the series for e^x"),
   "sin": (lambda order: (-1) ** ((order - 1) // 2) / sympy.factorial(order) if order % 2 else sympy.Integer(0), lambda order: sympy.Integer(1) / sympy.factorial(order) if order % 2 else sympy.Integer(0), r"\sin x", "the series for sin x recalled with every sign positive"),
   "cos": (lambda order: sympy.Integer(0) if order % 2 else (-1) ** (order // 2) / sympy.factorial(order), lambda order: sympy.Integer(0) if order % 2 else sympy.Integer(1) / sympy.factorial(order), r"\cos x", "the series for cos x recalled with every sign positive"),
   "geometric": (lambda order: sympy.Integer(1), lambda order: sympy.Integer(-1) ** order, r"\frac{1}{1 - x}", "the series for 1/(1 - x) recalled with alternating signs, as for 1/(1 + x)"),
}


LAST_ORDER = {
   "exp": lambda terms: terms - 1,
   "geometric": lambda terms: terms - 1,
   "sin": lambda terms: 2 * terms - 1,
   "cos": lambda terms: 2 * terms - 2,
}

ARGUMENT_FORMS = {
   "exp": lambda argument: f"e^{{{argument}}}",
   "sin": lambda argument: rf"\sin\left({argument}\right)",
   "cos": lambda argument: rf"\cos\left({argument}\right)",
}


def _function_tex(base, scale):
   return ARGUMENT_FORMS[base](tex(scale * x))


def _polynomial(coefficient_of, coefficient, power, scale, degree, raise_scale=True):
   """Coefficients of c x^m f(kx) through the given degree, from the coefficients of f."""
   coefficients = [sympy.Integer(0)] * (degree + 1)

   for order in range(degree - power + 1):
      factor = scale**order if raise_scale or order == 0 else scale
      coefficients[order + power] = coefficient * coefficient_of(order) * factor

   return coefficients


def build(names):
   base = names["base"]
   power = int(names["power"])
   last_order = LAST_ORDER[base](int(names["terms"]))
   degree = power + last_order
   scale = names["scale"]
   coefficient = names["coefficient"]
   coefficient_of, wrong_coefficient_of, known_tex, wrong_how = BASES[base]

   lead = "" if coefficient == 1 else f"{coefficient} "
   power_part = "x" if power == 1 else f"x^{{{power}}}"
   is_geometric = base == "geometric"

   if is_geometric:
      sign = "+" if scale < 0 else "-"
      g_tex = rf"\frac{{{lead}{power_part}}}{{1 {sign} {tex(abs(scale) * x)}}}"
   else:
      g_tex = f"{lead}{power_part} {_function_tex(base, scale)}"
   coefficients = _polynomial(coefficient_of, coefficient, power, scale, degree)
   value = taylor_polynomial(coefficients, 0)

   next_degree = degree + 1

   while _polynomial(coefficient_of, coefficient, power, scale, next_degree)[next_degree] == 0:
      next_degree += 1

   extra = _polynomial(coefficient_of, coefficient, power, scale, next_degree)
   stem = (
      f"Let {math('g(x) = ' + g_tex)}. Use the Maclaurin series for {math(known_tex)} to find the Taylor polynomial of "
      f"degree {degree} for g about {math('x = 0')}."
   )

   substituted = _polynomial(coefficient_of, 1, 0, scale, degree - power)
   steps = [
      Step(text=f"Replace x by {math(tex(scale * x))} in the series for {math(known_tex)}: its terms through degree {degree - power} are {math(polynomial_tex(substituted, 0))}.", point_type_id="BC-PT-99037", rule="substitution into a known series"),
      Step(text=f"Multiply every term by {math(tex(coefficient * x**power))} and keep the terms of degree at most {degree}: {math(polynomial_tex(coefficients, 0))}.", value=value, point_type_id="BC-PT-99035", rule="multiply and truncate"),
   ]
   distractors = [
      Distractor("BC-ERR-10040", wrong_how, value=taylor_polynomial(_polynomial(wrong_coefficient_of, coefficient, power, scale, degree), 0), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-10041", f"x replaced by {scale * x} but the factor {scale} not raised to the power of each term", value=taylor_polynomial(_polynomial(coefficient_of, coefficient, power, scale, degree, raise_scale=False), 0), mechanism="algebra_slip"),
      Distractor("BC-ERR-10030", f"the next nonzero term, of degree {next_degree}, kept beyond the requested degree {degree}", value=taylor_polynomial(extra, 0), mechanism="conceptual_confusion"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
