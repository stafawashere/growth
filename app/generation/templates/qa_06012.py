"""BC-QA-06012, the derivative of an accumulation function whose upper limit is a function of x, at a point."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06012"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "power", "type": "integer", "role": "difficulty", "domain": {"values": [1, 2, 3]}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "quadratic", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "lower", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "point", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2]}},
   ],
   "constraints": [
      "power > 1 or scale > 1",
      "value_at_top != 0",
      "value_at_lower != 0",
      "value_at_point != key_value",
      "value_at_point != value_at_top",
      "value_at_point != key_value - value_at_lower",
      "value_at_top != key_value - value_at_lower",
   ],
   "derived": [
      {"name": "top", "expression": "scale * point**power"},
      {"name": "chain_factor", "expression": "scale * power * point**(power - 1)"},
      {"name": "value_at_top", "expression": "quadratic * top**2 + constant"},
      {"name": "value_at_point", "expression": "quadratic * point**2 + constant"},
      {"name": "value_at_lower", "expression": "quadratic * lower**2 + constant"},
      {"name": "key_value", "expression": "value_at_top * chain_factor"},
   ],
   "invariants": [
      "exact(key)",
      "key == key_value",
   ],
   "dial_bindings": [
      {"parameter": "power", "difficulty_factor_id": "BC-DF-09", "settings": {"1": "low", "2": "medium", "3": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["power", "scale", "quadratic", "constant", "lower", "point"]},
   ],
   "notes": "h(x) is the integral from a to k x^n of (p t^2 + r) dt, and h'(c) = f(k c^n) times k n c^(n-1). The upper limit is never plain x, so the chain factor is never 1; the constraints keep the key and the three error values pairwise different.",
}

x = sympy.Symbol("x")
t = sympy.Symbol("t")


def build(names):
   power = int(names["power"])
   scale = int(names["scale"])
   lower = int(names["lower"])
   point = int(names["point"])
   integrand = int(names["quadratic"]) * t**2 + int(names["constant"])
   upper = scale * x**power
   top = int(names["top"])
   chain_factor = int(names["chain_factor"])
   value_at_top = sympy.Integer(names["value_at_top"])
   value_at_point = sympy.Integer(names["value_at_point"])
   value_at_lower = sympy.Integer(names["value_at_lower"])
   key_value = value_at_top * chain_factor
   chain_text = rf"\left({chain_factor}\right)" if chain_factor < 0 else str(chain_factor)

   definition = rf"h(x) = \int_{{{lower}}}^{{{tex(upper)}}} \left({tex(integrand)}\right)\,dt"
   stem = f"Let {math(definition)}. Find {math(f'h^{{\\prime}}({point})')}."

   derivative_form = rf"h^{{\prime}}(x) = \left({tex(integrand.subs(t, upper))}\right) \cdot {tex(sympy.diff(upper, x))}"

   steps = [
      Step(
         text=(
            f"By the Fundamental Theorem of Calculus with the chain rule, the derivative is the integrand evaluated at the "
            f"upper limit times the derivative of the upper limit: {math(derivative_form)}."
         ),
         point_type_id="BC-PT-99024",
         rule="Fundamental Theorem of Calculus with a composite upper limit",
      ),
      Step(
         text=(
            f"At x = {point} the upper limit is {top}, the integrand at {math(f't = {top}')} is {math(tex(value_at_top))}, "
            f"and the derivative of the upper limit is {chain_factor}, so {math(f'h^{{\\prime}}({point}) = {tex(value_at_top)} \\cdot {chain_text} = {tex(key_value)}')}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="evaluation",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-06027",
         derivation=f"the integrand evaluated at the upper limit with no factor for the derivative of {tex(upper)}",
         value=value_at_top,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-06028",
         derivation=f"t replaced by x itself instead of by the upper limit, so the integrand is evaluated at x = {point}",
         value=value_at_point,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99012",
         derivation=f"the integrand at the lower limit {lower} subtracted as though the constant lower limit contributed to the derivative",
         value=key_value - value_at_lower,
         mechanism="conceptual_confusion",
      ),
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
