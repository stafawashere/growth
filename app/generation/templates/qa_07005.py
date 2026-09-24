"""BC-QA-07005, whether a tangent line or Euler approximation to a solution over- or underestimates, from concavity."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-07005"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "form", "type": "label", "role": "difficulty", "domain": {"values": ["autonomous", "with_x"]}},
      {"name": "method", "type": "label", "role": "difficulty", "domain": {"values": ["tangent", "euler"]}},
      {"name": "rate", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "rate_sign", "type": "integer", "role": "safe", "domain": {"values": [-1, 1]}},
      {"name": "level", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"values": [-3, -2, -1, 1, 2, 3]}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": 0, "max": 2, "step": 1}},
      {"name": "step", "type": "rational", "role": "safe", "domain": {"values": ["1/2", "1"]}},
   ],
   "constraints": [
      "form == 'autonomous' or rate_sign == 1",
      "form == 'autonomous' or start >= 1",
   ],
   "derived": [
      {"name": "initial", "expression": "level + offset"},
      {"name": "coefficient", "expression": "rate * rate_sign"},
   ],
   "invariants": [
      "initial != level",
      "len(key) > 60",
   ],
   "dial_bindings": [
      {"parameter": "form", "difficulty_factor_id": "BC-DF-12", "settings": {"autonomous": "off", "with_x": "low"}},
      {"parameter": "method", "difficulty_factor_id": "BC-DF-12", "settings": {"tangent": "off", "euler": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-06", "figure_kind": None, "requires": ["form", "method", "rate", "level", "offset", "start", "step"]},
   ],
   "notes": "The equation is dy/dx = c(y - L), or c x (y - L) with c > 0 and x >= 1. Differentiating and substituting gives y'' = c^2 (y - L) or c (y - L)(1 + c x^2), whose sign is the sign of y - L, which the stated bound fixes on the whole interval.",
}

x = sympy.Symbol("x")
y = sympy.Symbol("y")


def _answer(conclusion, reason):
   return f"{conclusion}, because {reason}."


def build(names):
   coefficient = int(names["coefficient"])
   level = int(names["level"])
   initial = int(names["initial"])
   start = int(names["start"])
   step = sympy.Rational(names["step"])
   target = start + step
   is_autonomous = names["form"] == "autonomous"
   uses_euler = names["method"] == "euler"

   if is_autonomous:
      right_side = coefficient * (y - level)
   else:
      right_side = coefficient * x * (y - level)

   second_derivative = sympy.factor(sympy.diff(right_side, x) + sympy.diff(right_side, y) * right_side)
   above = initial > level
   bound_text = math(f"f(x) {'>' if above else '<'} {level}")
   concave_up = above
   first_positive = coefficient * (initial - level) > 0

   conclusion = "An underestimate" if concave_up else "An overestimate"
   opposite = "An overestimate" if concave_up else "An underestimate"
   second_sign = "positive" if concave_up else "negative"
   concavity = "up" if concave_up else "down"
   first_sign = "positive" if first_positive else "negative"
   monotone = "increasing" if first_positive else "decreasing"

   equation = rf"\frac{{dy}}{{dx}} = {tex(right_side)}"
   target_tex = tex(target)

   if uses_euler:
      half = tex(step / 2)
      approximation = f"Euler's method, starting at {math(f'x = {start}')} with two steps of equal size {math(half)}, is used to approximate {math(f'f({target_tex})')}"
      method_reason = "each Euler step follows the tangent line at the start of the step"
   else:
      approximation = f"The line tangent to the graph of f at {math(f'x = {start}')} is used to approximate {math(f'f({target_tex})')}"
      method_reason = "a tangent line approximation follows the slope at the point of tangency"

   stem = (
      f"Let y = f(x) be the solution to the differential equation {math(equation)} with {math(f'f({start}) = {initial}')}. "
      f"It is known that {bound_text} for all x. {approximation}. Is the approximation an overestimate or an "
      "underestimate of the value of the solution? Give a reason for your answer."
   )

   key_label = _answer(conclusion, f"the second derivative of f is {second_sign} for all x in the interval, so the graph of f is concave {concavity} there")

   steps = [
      Step(
         text=(
            f"Differentiate the right side with respect to x and replace dy/dx by the equation: "
            f"{math(r'\frac{d^2y}{dx^2} = ' + tex(second_derivative))}."
         ),
         point_type_id="BC-PT-99027",
         rule="implicit differentiation of the differential equation",
      ),
      Step(
         text=(
            f"Because {bound_text} for every x, the factor {math(tex(y - level))} is {second_sign} "
            f"{'and every other factor is positive ' if not is_autonomous else ''}throughout, so the second derivative is "
            f"{second_sign} on the whole interval from {math(f'x = {start}')} to {math(f'x = {target_tex}')}."
         ),
         rule="sign of the second derivative over the interval",
      ),
      Step(
         text=(
            f"The graph of f is concave {concavity} there, so it lies {'above' if concave_up else 'below'} its tangent lines, "
            f"and the approximation is {conclusion.lower()}."
         ),
         point_type_id="BC-PT-99026",
         rule="direction of the error from concavity",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-07018",
         derivation="the direction decided from whether the solution increases or decreases, with no reference to concavity",
         label=_answer(opposite, f"the first derivative of f is {first_sign} for all x in the interval, so f is {monotone} there"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-99004",
         derivation="the sign of the second derivative checked only at the starting point, a local fact offered where the interval is needed",
         label=_answer(conclusion, f"the second derivative of f is {second_sign} at the starting point, so the graph of f is concave {concavity} at that point"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-07023",
         derivation="a direction asserted from how the method works, with no concavity statement",
         label=_answer(opposite, f"{method_reason}, and that slope is too steep for the rest of the interval"),
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-06",
      calculator_status="no_calculator",
      command_verb="determine",
   )
