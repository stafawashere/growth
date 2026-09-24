"""BC-QA-04009, a zero over zero limit with an unknown function in the numerator, by L'Hospital's rule."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-04009"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "anchor", "type": "integer", "role": "safe", "domain": {"values": [1, 2]}},
      {"name": "stretch", "type": "integer", "role": "safe", "domain": {"values": [2, 3]}},
      {"name": "far_value", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "far_slope", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "near_value", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1}},
      {"name": "near_slope", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "denominator", "type": "label", "role": "safe", "domain": {"values": ["linear", "square", "cube", "exponential", "sine"]}},
   ],
   "constraints": [
      "near_slope != far_slope",
      "stretch * near_slope != far_slope",
      "near_value != far_value",
   ],
   "derived": [
      {"name": "inner_point", "expression": "anchor * stretch"},
   ],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["anchor", "stretch", "far_value", "far_slope", "near_value", "near_slope", "denominator"]},
   ],
   "notes": "The numerator is f(kx) - f(ka), known only through f and f' at a and at ka, and the denominator vanishes at a with a nonzero derivative, so one application of the rule settles the limit at k f'(ka) / D'(a).",
}

x = sympy.Symbol("x")


def _denominator(kind, anchor):
   if kind == "linear":
      return x - anchor

   if kind == "square":
      return x**2 - anchor**2

   if kind == "cube":
      return x**3 - anchor**3

   if kind == "exponential":
      return sympy.exp(x - anchor) - 1

   return sympy.sin(x - anchor)


def build(names):
   anchor = int(names["anchor"])
   stretch = int(names["stretch"])
   inner = int(names["inner_point"])
   far_value = int(names["far_value"])
   far_slope = int(names["far_slope"])
   near_value = int(names["near_value"])
   near_slope = int(names["near_slope"])
   denominator = _denominator(names["denominator"], anchor)
   denominator_slope = sympy.diff(denominator, x).subs(x, anchor)
   key_value = sympy.Rational(stretch * far_slope, 1) / denominator_slope

   numerator_tex = f"f({stretch}x) - {far_value}" if far_value >= 0 else f"f({stretch}x) + {-far_value}"
   limit_tex = rf"\lim_{{x \to {anchor}}} \frac{{{numerator_tex}}}{{{tex(denominator)}}}"
   facts = [(anchor, near_value, near_slope), (inner, far_value, far_slope)]
   fact_pieces = []

   for point, value, slope in facts:
      value_statement = f"f({point}) = {value}"
      slope_statement = f"f'({point}) = {slope}"
      fact_pieces.append(f"{math(value_statement)}, {math(slope_statement)}")

   facts_text = ", ".join(fact_pieces[:-1]) + " and " + fact_pieces[-1]
   stem = (
      f"Let f be a function with a continuous derivative for all real x, where {facts_text}. Find {math(limit_tex)}, "
      "showing the work that justifies the method."
   )

   if far_value >= 0:
      at_anchor = f"f({inner}) - {far_value} = {far_value} - {far_value}"
   else:
      at_anchor = f"f({inner}) + {-far_value} = {far_value} + {-far_value}"

   numerator_limit = rf"\lim_{{x \to {anchor}}} \left({numerator_tex}\right) = {at_anchor} = 0"
   denominator_limit = rf"\lim_{{x \to {anchor}}} \left({tex(denominator)}\right) = 0"
   derivative_ratio = rf"\lim_{{x \to {anchor}}} \frac{{{stretch} f'({stretch}x)}}{{{tex(sympy.diff(denominator, x))}}} = \frac{{{stretch}({far_slope})}}{{{tex(denominator_slope)}}} = {tex(key_value)}"
   steps = [
      Step(
         text=f"Check the form first: {math(numerator_limit)} and {math(denominator_limit)}, so the limit has the form 0/0.",
         point_type_id="BC-PT-99005",
         rule="verify the indeterminate form",
      ),
      Step(
         text=(
            f"By L'Hospital's rule, differentiate the numerator and the denominator separately, using the chain rule on "
            f"{math(f'f({stretch}x)')}: {math(derivative_ratio)}."
         ),
         value=key_value,
         point_type_id="BC-PT-99055",
         rule="L'Hospital's rule",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-04031",
         derivation=f"the derivative of f({stretch}x) taken as f'({stretch}x), with the chain rule factor {stretch} dropped",
         value=sympy.Rational(far_slope, 1) / denominator_slope,
         mechanism="chain_rule_omitted",
      ),
      Distractor(
         error_path="BC-ERR-03003",
         derivation=f"the derivative of f({stretch}x) at x = {anchor} read as {stretch} f'({anchor}) instead of {stretch} f'({inner})",
         value=sympy.Rational(stretch * near_slope, 1) / denominator_slope,
         mechanism="algebra_slip",
      ),
      Distractor(
         error_path="BC-ERR-01008",
         derivation="the numerator seen to tend to 0 and the limit reported as 0, with the denominator ignored",
         value=sympy.Integer(0),
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
