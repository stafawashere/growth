"""BC-QA-03001, the chain rule on a power or root of a quadratic, inside a product with a power of x."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-03001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "family", "type": "label", "role": "difficulty", "domain": {"values": ["power", "root"]}},
      {"name": "exponent", "type": "integer", "role": "safe", "domain": {"values": [2, 3, 4]}},
      {"name": "inner_slope", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"values": [-3, -2, -1, 1, 2, 3]}},
      {"name": "outside_power", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 5, "step": 1}},
   ],
   "constraints": [
      "distinct(options)",
      "options[0] != 0",
      "shift != 0",
   ],
   "derived": [
      {"name": "inner_value", "expression": "target if family == 'power' else target**2"},
      {"name": "shift", "expression": "inner_value - inner_slope * at**2"},
      {"name": "inner_rate", "expression": "2 * inner_slope * at"},
      {"name": "outer_value", "expression": "inner_value**exponent if family == 'power' else target"},
      {"name": "outer_rate", "expression": "exponent * inner_value**(exponent - 1) if family == 'power' else 1 / (2 * target)"},
      {"name": "front", "expression": "scale * outside_power * at**(outside_power - 1) * outer_value"},
      {"name": "back", "expression": "scale * at**outside_power"},
      {
         "name": "options",
         "expression": (
            "[front + back * outer_rate * inner_rate, back * outer_rate * inner_rate, "
            "front + back * outer_rate, front + back * outer_value * inner_rate]"
         ),
      },
   ],
   "invariants": [
      "exact(key)",
      "key == options[0]",
   ],
   "dial_bindings": [
      {"parameter": "family", "difficulty_factor_id": "BC-DF-02", "settings": {"power": "off", "root": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["family", "exponent", "inner_slope", "at", "outside_power", "target", "scale"]},
   ],
   "notes": (
      "h(x) = scale x^outside_power F(inner_slope x^2 + shift), with F a power or a square root, and the shift chosen "
      "so the inner expression at the requested input equals target (power) or target squared (root). The "
      "constraints keep the four options distinct; for the power family they exclude an inner value equal to "
      "the exponent, where the undifferentiated outer layer would agree with the key."
   ),
}

x = sympy.Symbol("x")


def _paren(value):
   text = tex(value)

   return rf"\left({text}\right)" if value < 0 else text


def build(names):
   is_power = names["family"] == "power"
   exponent = int(names["exponent"])
   inner_slope = int(names["inner_slope"])
   at = int(names["at"])
   outside_power = int(names["outside_power"])
   target = int(names["target"])
   scale = int(names["scale"])

   inner_value = sympy.Integer(target if is_power else target**2)
   shift = inner_value - inner_slope * at**2
   inner = inner_slope * x**2 + shift
   inner_rate = sympy.Integer(2 * inner_slope * at)

   if is_power:
      outer = inner**exponent
      outer_value = inner_value**exponent
      outer_rate = exponent * inner_value ** (exponent - 1)
      outer_rule = rf"\frac{{d}}{{du}} u^{{{exponent}}} = {exponent} u^{{{exponent - 1}}}".replace("u^{1}", "u")
   else:
      outer = sympy.sqrt(inner)
      outer_value = sympy.Integer(target)
      outer_rate = sympy.Rational(1, 2 * target)
      outer_rule = r"\frac{d}{du} \sqrt{u} = \frac{1}{2\sqrt{u}}"

   front_power = scale * x**outside_power
   function = front_power * outer
   front = scale * outside_power * sympy.Integer(at) ** (outside_power - 1) * outer_value
   back_factor = scale * sympy.Integer(at) ** outside_power
   chain = outer_rate * inner_rate
   key_value = front + back_factor * chain

   stem = f"Let {math('h(x) = ' + tex(function))}. Find the exact value of {math(f"h'({at})")}."

   derivative = sympy.diff(front_power, x) * outer + front_power * sympy.diff(outer, x)
   steps = [
      Step(
         text=(
            f"The composite has outer function F with {math(outer_rule)} and inner function "
            f"{math('u = ' + tex(inner))}, whose derivative is {math(tex(sympy.diff(inner, x)))}."
         ),
         point_type_id="BC-PT-99023",
         rule="identify the layers",
      ),
      Step(
         text=f"By the product rule and the chain rule, {math("h'(x) = " + tex(derivative))}.",
         point_type_id="BC-PT-99023",
         rule="product rule with the chain rule",
      ),
      Step(
         text=(
            f"At x = {at} the inner value is {tex(inner_value)} and the inner derivative is {tex(inner_rate)}, so "
            f"{math(f"h'({at}) = {tex(front)} + {_paren(back_factor)} \\cdot {_paren(outer_rate)} \\cdot {_paren(inner_rate)} = {tex(key_value)}")}."
         ),
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="evaluate",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-03006",
         derivation=f"the factor {tex(front_power)} held constant, so only the composite is differentiated",
         value=back_factor * chain,
         mechanism="product_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03001",
         derivation=f"the inner derivative {tex(inner_rate)} left off the chain rule",
         value=front + back_factor * outer_rate,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03002",
         derivation="the outer layer left undifferentiated, so F(u) is multiplied by the inner derivative",
         value=front + back_factor * outer_value * inner_rate,
         mechanism="chain_rule_omitted",
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
