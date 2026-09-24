"""BC-QA-05002, the value the Mean Value Theorem provides, solved for exactly."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-05002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "cubic", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 6, "step": 1}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 12, "step": 1}},
      {"name": "low", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 3, "step": 1}},
      {"name": "width", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
   ],
   "constraints": [
      "distinct([key_square, endpoint_slope_square, endpoint_value_square])",
      "endpoint_value_square > 0",
   ],
   "derived": [
      {"name": "high", "expression": "low + width"},
      {"name": "key_square", "expression": "(low**2 + low*(low + width) + (low + width)**2) / 3"},
      {"name": "endpoint_slope_square", "expression": "(low**2 + (low + width)**2) / 2"},
      {"name": "endpoint_value_square", "expression": "((cubic*(low**3 + (low + width)**3) + linear*(2*low + width)) / 2 + constant - linear) / (3*cubic)"},
   ],
   "invariants": [
      "exact(key)",
      "low < key",
      "key < high",
   ],
   "dial_bindings": [],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["cubic", "linear", "constant", "low", "width"]},
   ],
   "notes": "f(x) = k x^3 + p x + d on [a, b] with 0 <= a < b; the average rate is k(a^2 + ab + b^2) + p, so c = sqrt((a^2 + ab + b^2)/3), and the negative root lies outside the interval. The endpoint-value slope stays positive because p, d >= 0 and a + b >= 1.",
}

x = sympy.Symbol("x")


def build(names):
   cubic = int(names["cubic"])
   linear = int(names["linear"])
   constant = int(names["constant"])
   low = int(names["low"])
   high = int(names["high"])
   function = cubic * x**3 + linear * x + constant
   derivative = sympy.diff(function, x)
   low_value = function.subs(x, low)
   high_value = function.subs(x, high)
   average_rate = sympy.Rational(high_value - low_value, high - low)
   key_square = sympy.Rational(names["key_square"])
   key_value = sympy.sqrt(key_square)

   stem = (
      f"Let {math('f(x) = ' + tex(function))}. Find the value of c in the open interval {math(f'({low}, {high})')} at which "
      f"the instantaneous rate of change of f equals the average rate of change of f over {math(rf'\left[{low}, {high}\right]')}. "
      "Give the exact value."
   )

   average_tex = rf"\frac{{f({high}) - f({low})}}{{{high} - {low}}} = \frac{{{high_value} - {low_value}}}{{{high - low}}} = {tex(average_rate)}"
   equation_tex = f"{tex(derivative.subs(x, sympy.Symbol('c')))} = {tex(average_rate)}"
   steps = [
      Step(
         text=f"The average rate of change is {math(average_tex)}.",
         value=average_rate,
         rule="average rate of change",
      ),
      Step(
         text=f"Set the derivative equal to it and solve {math(equation_tex)}, which gives {math('c^{2} = ' + tex(key_square))}.",
         value=key_square,
         rule="solve the derivative equation",
      ),
      Step(
         text=(
            f"The solutions are {math('c = \\pm ' + tex(key_value))}. Only {math('c = ' + tex(key_value))} lies in "
            f"{math(f'({low}, {high})')}, so that is the value."
         ),
         value=key_value,
         rule="keep the solution in the open interval",
      ),
   ]

   endpoint_slope = (derivative.subs(x, low) + derivative.subs(x, high)) / 2
   endpoint_slope_root = sympy.sqrt(sympy.Rational(names["endpoint_slope_square"]))
   endpoint_value_slope = (low_value + high_value) / sympy.Integer(2)
   endpoint_value_root = sympy.sqrt(sympy.Rational(names["endpoint_value_square"]))

   distractors = [
      Distractor(
         error_path="BC-ERR-05005",
         derivation="the negative solution of the derivative equation reported, which lies outside the open interval",
         value=-key_value,
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-05003",
         derivation=f"the average rate of change formed as the average of f'({low}) and f'({high}), {endpoint_slope}, and the positive root taken",
         value=endpoint_slope_root,
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-05003",
         derivation=f"the average rate of change formed by averaging the endpoint values f({low}) and f({high}), {endpoint_value_slope}, and the positive root taken",
         value=endpoint_value_root,
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
