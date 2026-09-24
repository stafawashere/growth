"""BC-QA-02011, the equation of the line tangent to a quadratic at a named point."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-02011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, author tpl-B"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "square", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1, "exclude": [0]}},
      {"name": "linear", "type": "integer", "role": "safe", "domain": {"min": -6, "max": 6, "step": 1, "exclude": [0]}},
      {"name": "constant", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "at", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "given", "type": "label", "role": "difficulty", "domain": {"values": ["point", "input"]}},
   ],
   "constraints": [
      "slope != 0",
      "height != 0",
      "height != slope",
      "wrong_slope != slope",
      "wrong_slope != height",
      "height - slope * at != 0",
   ],
   "derived": [
      {"name": "slope", "expression": "2 * square * at + linear"},
      {"name": "height", "expression": "square * at**2 + linear * at + constant"},
      {"name": "wrong_slope", "expression": "2 * square * height + linear"},
   ],
   "invariants": [
      "exact(key)",
   ],
   "dial_bindings": [
      {"parameter": "given", "difficulty_factor_id": "BC-DF-08", "settings": {"point": "off", "input": "low"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["square", "linear", "constant", "at", "given"]},
   ],
   "notes": (
      "f(x) = square x^2 + linear x + constant, tangent at x = at. The constraints keep the slope, the function "
      "value and the derivative at the wrong input (the y-coordinate) pairwise different and nonzero, so the "
      "four lines are distinct, and keep the tangent line's intercept nonzero."
   ),
}

x = sympy.Symbol("x")


def _shifted(variable, value):
   return f"{variable} - {value}" if value > 0 else f"{variable} + {-value}"


def build(names):
   square = int(names["square"])
   linear = int(names["linear"])
   constant = int(names["constant"])
   at = int(names["at"])
   point_given = names["given"] == "point"

   function = square * x**2 + linear * x + constant
   derivative = sympy.diff(function, x)
   slope = derivative.subs(x, at)
   height = function.subs(x, at)
   wrong_slope = derivative.subs(x, height)
   key_value = sympy.expand(slope * (x - at) + height)

   if point_given:
      where = f"at the point {math(f'({at}, {height})')}"
   else:
      where = f"at the point where {math(f'x = {at}')}"

   stem = (
      f"Let {math('f(x) = ' + tex(function))}. Find an equation of the line tangent to the graph of f {where}. "
      f"Write it in the form {math('y = mx + b')}."
   )

   steps = [
      Step(
         text=f"Differentiate: {math("f'(x) = " + tex(derivative))}.",
         value=derivative,
         rule="power rule",
      ),
      Step(
         text=f"The slope is {math(f"f'({at}) = {tex(slope)}")}.",
         value=slope,
         point_type_id="BC-PT-99082",
         rule="derivative at the point",
      ),
      Step(
         text=f"The point of tangency has {math(f'f({at}) = {tex(height)}')}, so it is {math(f'({at}, {height})')}.",
         value=height,
         rule="function value at the point",
      ),
      Step(
         text=(
            f"Point-slope form gives {math(f'{_shifted("y", height)} = {tex(slope)}\\left({_shifted("x", at)}\\right)')}, "
            f"that is {math('y = ' + tex(key_value))}."
         ),
         value=key_value,
         point_type_id="BC-PT-99082",
         rule="point-slope form",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-02027",
         derivation=f"the function value f({at}) = {height} used as the slope",
         value=sympy.expand(height * (x - at) + height),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-04023",
         derivation="the slope and the function value exchanged in point-slope form",
         value=sympy.expand(height * (x - at) + slope),
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-02028",
         derivation=f"the derivative evaluated at the y-coordinate {height} instead of at x = {at}",
         value=sympy.expand(wrong_slope * (x - at) + height),
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
