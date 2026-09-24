"""BC-QA-10017, a Maclaurin series found by substituting k x^p into a known series and multiplying by a constant."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math
from app.generation.templates._helpers_h import polynomial_tex, taylor_polynomial

ARCHETYPE_ID = "BC-QA-10017"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "base", "type": "label", "role": "difficulty", "domain": {"values": ["exp", "sin", "cos", "geometric"]}},
      {"name": "inner_power", "type": "integer", "role": "difficulty", "domain": {"values": [2, 3, 4]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"values": [-4, -3, -2, 2, 3, 4]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 15, "step": 1}},
      {"name": "count", "type": "integer", "role": "difficulty", "domain": {"values": [3, 4]}},
   ],
   "constraints": [],
   "derived": [],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "base", "difficulty_factor_id": "BC-DF-06", "settings": {"exp": "low", "sin": "medium", "cos": "medium", "geometric": "low"}},
      {"parameter": "inner_power", "difficulty_factor_id": "BC-DF-06", "settings": {"2": "low", "3": "medium", "4": "medium"}},
      {"parameter": "count", "difficulty_factor_id": "BC-DF-08", "settings": {"3": "low", "4": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["base", "inner_power", "scale", "coefficient", "count"]},
   ],
   "notes": "f(x) = c g(k x^p) with g one of e^x, sin x, cos x, 1/(1 - x) and p at least 2, so every power is raised by the substitution; the answer is the first three or four nonzero terms, a polynomial.",
}

# Each known series: the coefficient of u^j, and the same series as it is commonly misremembered.
KNOWN = {
   "exp": (lambda j: sympy.Integer(1) / sympy.factorial(j), lambda j: sympy.Integer(1), "e^{x}", "the factorials left out of the series for e^x"),
   "sin": (lambda j: sympy.Integer((-1) ** ((j - 1) // 2)) / sympy.factorial(j) if j % 2 else sympy.Integer(0), lambda j: sympy.Integer(1) / sympy.factorial(j) if j % 2 else sympy.Integer(0), r"\sin x", "the series for sin x recalled with every sign positive"),
   "cos": (lambda j: sympy.Integer(0) if j % 2 else sympy.Integer((-1) ** (j // 2)) / sympy.factorial(j), lambda j: sympy.Integer(0) if j % 2 else sympy.Integer(1) / sympy.factorial(j), r"\cos x", "the series for cos x recalled with every sign positive"),
   "geometric": (lambda j: sympy.Integer(1), lambda j: sympy.Integer((-1) ** j), r"\frac{1}{1 - x}", "the series for 1/(1 - x) recalled with alternating signs, as for 1/(1 + x)"),
}

FUNCTION_TEX = {
   "exp": lambda argument: f"e^{{{argument}}}",
   "sin": lambda argument: rf"\sin\left({argument}\right)",
   "cos": lambda argument: rf"\cos\left({argument}\right)",
}


def _orders(coefficient_of, count):
   """The first count orders j whose coefficient in the known series is nonzero."""
   orders = []
   order = 0

   while len(orders) < count:
      if coefficient_of(order) != 0:
         orders.append(order)

      order += 1

   return orders


def _terms(coefficient_of, orders, coefficient, scale, inner_power, mode="correct"):
   """Coefficients by power of x of c g(k x^p) over the given orders, or of a wrong substitution."""
   placed = {}

   for order in orders:
      if mode == "unraised_scale":
         factor = scale if order > 0 else 1
         exponent = inner_power * order
      elif mode == "added_power":
         factor = sympy.Integer(scale) ** order
         exponent = order + inner_power if order > 0 else 0
      else:
         factor = sympy.Integer(scale) ** order
         exponent = inner_power * order

      placed[exponent] = placed.get(exponent, 0) + coefficient * coefficient_of(order) * factor

   degree = max(placed)

   return [placed.get(power, sympy.Integer(0)) for power in range(degree + 1)]


def build(names):
   base = names["base"]
   inner_power = int(names["inner_power"])
   scale = int(names["scale"])
   coefficient = int(names["coefficient"])
   count = int(names["count"])
   coefficient_of, wrong_coefficient_of, known_tex, wrong_how = KNOWN[base]

   argument = f"{scale}x^{{{inner_power}}}"
   lead = "" if coefficient == 1 else f"{coefficient} "

   if base == "geometric":
      sign = "+" if scale < 0 else "-"
      function_tex = rf"\frac{{{coefficient}}}{{1 {sign} {abs(scale)}x^{{{inner_power}}}}}"
   else:
      function_tex = f"{lead}{FUNCTION_TEX[base](argument)}"

   orders = _orders(coefficient_of, count)
   key_coefficients = _terms(coefficient_of, orders, coefficient, scale, inner_power)
   value = taylor_polynomial(key_coefficients, 0)
   stem = (
      f"Let {math('f(x) = ' + function_tex)}. Use the Maclaurin series for {math(known_tex)} to find the first {count} "
      "nonzero terms of the Maclaurin series for f."
   )

   steps = [
      Step(text=f"Replace x by {math(argument)} in the series for {math(known_tex)}, raising the whole of {math(argument)} to each power, so the jth term carries {math(f'({scale})^j x^{{{inner_power}j}}')}.", point_type_id="BC-PT-99037", rule="substitution into a known series"),
      Step(text=f"Multiply by {math(str(coefficient))} and keep the first {count} nonzero terms: {math(polynomial_tex(key_coefficients, 0))}.", value=value, point_type_id="BC-PT-99035", rule="first nonzero terms"),
   ]

   wrong_orders = _orders(wrong_coefficient_of, count)
   distractors = [
      Distractor("BC-ERR-10040", wrong_how, value=taylor_polynomial(_terms(wrong_coefficient_of, wrong_orders, coefficient, scale, inner_power), 0), mechanism="conceptual_confusion"),
      Distractor("BC-ERR-10041", f"{scale} not raised to the power of each term, so every term after the first carries {scale} once", value=taylor_polynomial(_terms(coefficient_of, orders, coefficient, scale, inner_power, "unraised_scale"), 0), mechanism="algebra_slip"),
      Distractor("BC-ERR-10041", f"the power of x^{inner_power} added to the exponent instead of multiplying it, so x^j became x^(j + {inner_power})", value=taylor_polynomial(_terms(coefficient_of, orders, coefficient, scale, inner_power, "added_power"), 0), mechanism="algebra_slip"),
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
