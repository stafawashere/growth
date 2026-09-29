"""BC-QA-06019, an antiderivative found after splitting a fraction or expanding a product, and confirmed by differentiating it."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06019"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 15 of 2026-09-28"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "structure", "type": "label", "role": "difficulty", "domain": {"values": ["product", "fraction", "root"]}},
      {"name": "coefficient", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "first", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "second", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "power", "type": "integer", "role": "safe", "domain": {"values": [2, 3]}},
   ],
   "constraints": [
      "second + coefficient * first != 0",
   ],
   "derived": [
      {"name": "middle", "expression": "second + coefficient * first"},
   ],
   "invariants": [
      "exact(key)",
      "middle != 0",
   ],
   "dial_bindings": [
      {"parameter": "structure", "difficulty_factor_id": "BC-DF-06", "settings": {"product": "low", "fraction": "medium", "root": "medium"}},
      {"parameter": "structure", "difficulty_factor_id": "BC-DF-13", "settings": {"product": "low", "fraction": "low", "root": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["structure", "coefficient", "first", "second", "power"]},
   ],
   "notes": "Product (x + p)(c x + q), expanded to c x^2 + (q + c p) x + p q with the middle coefficient kept nonzero; fraction (c x^(k+1) + p)/x^k = c x + p x^(-k) with k = 2 or 3, so no logarithm arises; root (c x + p)/sqrt(x) = c x^(1/2) + p x^(-1/2). The options are candidate antiderivatives and the check is that the derivative of the chosen one returns the integrand.",
}

x = sympy.Symbol("x")


def _power_rule_slips(terms):
   """The two wrong-divisor versions of the power rule, term by term: no division at all, and
   division by the old exponent where it is not zero."""
   undivided = 0
   old_divisor = 0

   for coefficient, exponent in terms:
      raised = coefficient * x ** (exponent + 1)
      undivided += raised
      old_divisor += raised / exponent if exponent != 0 else raised

   return sympy.expand(undivided), sympy.expand(old_divisor)


def _antiderivative(expression):
   return sympy.expand(sympy.integrate(expression, x))


def build(names):
   structure = names["structure"]
   coefficient = int(names["coefficient"])
   first = int(names["first"])
   second = int(names["second"])
   power = int(names["power"])

   if structure == "product":
      left_factor = x + first
      right_factor = coefficient * x + second
      integrand = left_factor * right_factor
      rewritten = sympy.expand(integrand)
      terms = [(coefficient, 2), (second + coefficient * first, 1), (first * second, 0)]
      separate = _antiderivative(left_factor) * _antiderivative(right_factor)
      rewrite_words = "Expand the product"
      separate_words = "each factor antidifferentiated on its own and the two results multiplied"
   elif structure == "fraction":
      numerator = coefficient * x ** (power + 1) + first
      denominator = x**power
      integrand = numerator / denominator
      rewritten = coefficient * x + first * x ** (-power)
      terms = [(coefficient, 1), (first, -power)]
      separate = _antiderivative(numerator) / _antiderivative(denominator)
      rewrite_words = "Split the fraction term by term"
      separate_words = "the numerator and the denominator antidifferentiated separately and the results divided"
   else:
      numerator = coefficient * x + first
      denominator = sympy.sqrt(x)
      integrand = numerator / denominator
      rewritten = coefficient * sympy.sqrt(x) + first / sympy.sqrt(x)
      terms = [(coefficient, sympy.Rational(1, 2)), (first, sympy.Rational(-1, 2))]
      separate = _antiderivative(numerator) / _antiderivative(denominator)
      rewrite_words = "Split the fraction term by term"
      separate_words = "the numerator and the denominator antidifferentiated separately and the results divided"

   key_value = _antiderivative(rewritten)
   undivided, old_divisor = _power_rule_slips(terms)

   stem = f"Find the indefinite integral {math(r'\int ' + tex(integrand) + r'\,dx')}."
   steps = [
      Step(
         text=f"{rewrite_words} so that every term is a power of x: {math(tex(integrand) + ' = ' + tex(rewritten))}.",
         value=rewritten,
         rule="rearrangement into an equivalent form",
      ),
      Step(
         text=f"Apply the power rule for antiderivatives to each term: the integral is {math(tex(key_value) + ' + C')}.",
         value=key_value,
         rule="power rule for antiderivatives",
      ),
      Step(
         text=f"Check: the derivative of {math(tex(key_value))} is {math(tex(rewritten))}, which is the integrand.",
         rule="antiderivative verified by differentiating",
      ),
   ]
   distractors = [
      Distractor("BC-ERR-06022", separate_words, value=sympy.simplify(separate), mechanism="product_rule_omitted"),
      Distractor("BC-ERR-06033", "each exponent raised by one with no division by the new exponent", value=undivided, mechanism="algebra_slip"),
      Distractor("BC-ERR-06033", "each exponent raised by one and the term divided by the old exponent instead of the new one", value=old_divisor, mechanism="algebra_slip"),
   ]

   return Instance(
      stem=stem,
      key=Key(form="symbolic", value=key_value),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
   )
