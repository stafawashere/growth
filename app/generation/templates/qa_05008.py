"""BC-QA-05008, open intervals of increase or decrease justified by the sign of the derivative."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex
from app.generation.templates._helpers_d import interval_list_text, merge_touching, pieces_between, sign_on

ARCHETYPE_ID = "BC-QA-05008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "first_zero", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 4, "step": 1}},
      {"name": "second_zero", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 5, "step": 1}},
      {"name": "gap", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 4, "step": 1}},
      {"name": "direction", "type": "label", "role": "safe", "domain": {"values": ["increasing", "decreasing"]}},
      {"name": "leading_sign", "type": "integer", "role": "difficulty", "domain": {"values": [1, -1]}},
      {"name": "domain_break", "type": "label", "role": "difficulty", "domain": {"values": ["none", "even", "odd"]}},
   ],
   "constraints": [
      "first_zero < second_zero",
      "gap != first_zero and gap != second_zero",
      "domain_break != 'even' or leading_sign * direction_sign * (gap - first_zero) * (gap - second_zero) > 0",
   ],
   "derived": [
      {"name": "direction_sign", "expression": "1 if direction == 'increasing' else -1"},
   ],
   "invariants": [
      "interval_count >= 1",
      "interval_count <= 3",
   ],
   "dial_bindings": [
      {"parameter": "leading_sign", "difficulty_factor_id": "BC-DF-12", "settings": {"1": "off", "-1": "low"}},
      {"parameter": "domain_break", "difficulty_factor_id": "BC-DF-17", "settings": {"none": "off", "even": "low", "odd": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["first_zero", "second_zero", "gap", "leading_sign", "domain_break"]},
   ],
   "notes": (
      "The derivative is leading_sign * scale * (x - first_zero)(x - second_zero), divided by (x - gap) squared when the "
      "domain break is even and by (x - gap) when it is odd. An even break sits inside a piece of the requested sign, "
      "so the answer has two intervals that meet at the excluded point and must not be merged."
   ),
}

x = sympy.Symbol("x")


def _derivative(names):
   numerator = names["leading_sign"] * names["scale"] * (x - names["first_zero"]) * (x - names["second_zero"])
   domain_break = names["domain_break"]

   if domain_break == "even":
      return numerator / (x - names["gap"]) ** 2

   if domain_break == "odd":
      return numerator / (x - names["gap"])

   return numerator


def _factor_tex(root):
   return tex(x - root)


def _product_tex(first_root, second_root):
   if first_root == 0:
      return rf"x\left({_factor_tex(second_root)}\right)"

   if second_root == 0:
      return rf"x\left({_factor_tex(first_root)}\right)"

   return rf"\left({_factor_tex(first_root)}\right)\left({_factor_tex(second_root)}\right)"


def _derivative_tex(names):
   coefficient = names["leading_sign"] * names["scale"]
   factors = _product_tex(names["first_zero"], names["second_zero"])
   sign_text = "-" if coefficient < 0 else ""
   size_text = "" if abs(coefficient) == 1 else f"{abs(coefficient)}"
   numerator = size_text + factors
   domain_break = names["domain_break"]

   if domain_break == "none":
      return sign_text + numerator

   gap = names["gap"]
   denominator = _factor_tex(gap)

   if domain_break == "even":
      denominator = "x^{2}" if gap == 0 else rf"\left({denominator}\right)^{{2}}"

   return sign_text + rf"\frac{{{numerator}}}{{{denominator}}}"


def _reason(inequality, intervals):
   where = "on that interval" if len(intervals) == 1 else "on each of those intervals"

   sign_text = math("f'(x) " + inequality + " 0")

   return f"because {sign_text} {where}"


def _pieces_of_sign(expression, points, wanted_sign):
   pieces = pieces_between(points)

   return [(low, high) for low, high in pieces if sign_on(expression, x, low, high) == wanted_sign]


def _statement(direction, intervals, reason):
   return f"f is {direction} on {interval_list_text(intervals)}, {reason}."


def build(names):
   first_zero = names["first_zero"]
   second_zero = names["second_zero"]
   gap = names["gap"]
   direction = names["direction"]
   direction_sign = 1 if direction == "increasing" else -1
   domain_break = names["domain_break"]
   has_break = domain_break != "none"
   inequality = ">" if direction_sign == 1 else "<"
   opposite = "<" if direction_sign == 1 else ">"

   derivative = _derivative(names)
   points = [first_zero, second_zero] + ([gap] if has_break else [])
   removed = [gap] if has_break else []
   key_intervals = merge_touching(_pieces_of_sign(derivative, points, direction_sign), removed)
   other_intervals = merge_touching(_pieces_of_sign(derivative, points, -direction_sign), removed)

   derivative_tex = _derivative_tex(names)

   if has_break:
      excluded_text = math(r"x \ne " + tex(gap))
      domain_text = f"for all {excluded_text}, where f is not defined at {math(f'x = {tex(gap)}')}"
   else:
      domain_text = "for all real x"

   derivative_text = math("f'(x) = " + derivative_tex)
   stem = (
      f"A function f has derivative {derivative_text} {domain_text}. On what open intervals "
      f"is f {direction}? Give a reason for the answer."
   )

   key_reason = _reason(inequality, key_intervals)
   key_label = _statement(direction, key_intervals, key_reason)

   zero_text = math("f'(x) = 0")
   critical_text = f"{zero_text} at {math(f'x = {tex(first_zero)}')} and {math(f'x = {tex(second_zero)}')}"

   if has_break:
      critical_text += f", and f' is undefined at {math(f'x = {tex(gap)}')}, which is not in the domain of f"

   same_sign_text = math("f'(x) " + inequality + " 0")
   opposite_sign_text = math("f'(x) " + opposite + " 0")
   steps = [
      Step(
         text=f"The sign of f' can change only where {critical_text}.",
         point_type_id="BC-PT-99005",
         rule="partition points of the sign chart",
      ),
      Step(
         text=(
            f"Testing one point in each piece gives {same_sign_text} on {interval_list_text(key_intervals)} "
            f"and {opposite_sign_text} on {interval_list_text(other_intervals)}."
         ),
         point_type_id="BC-PT-99010",
         rule="sign chart of the derivative",
      ),
      Step(
         text=f"So f is {direction} on {interval_list_text(key_intervals)}, {key_reason}.",
         point_type_id="BC-PT-99063",
         rule="sign of the derivative gives the direction of the function",
      ),
   ]

   distractors = [
      Distractor(
         error_path="BC-ERR-05014",
         derivation="the sign of f' read backwards, so the pieces where f' has the opposite sign are reported",
         label=_statement(direction, other_intervals, _reason(inequality, other_intervals)),
         mechanism="sign_error",
      ),
      Distractor(
         error_path="BC-ERR-05018",
         derivation="the right intervals, justified by a pronoun that never says which function is positive or negative",
         label=_statement(direction, key_intervals, "because it is " + ("positive" if direction_sign == 1 else "negative") + " there"),
         mechanism="conceptual_confusion",
      ),
   ]

   if domain_break == "even":
      merged = merge_touching(key_intervals)
      distractors.append(Distractor(
         error_path="BC-ERR-05019",
         derivation=f"the two intervals on either side of the excluded point x = {gap} joined into one interval across the gap",
         label=_statement(direction, merged, _reason(inequality, merged)),
         mechanism="conceptual_confusion",
      ))
   elif domain_break == "odd":
      numerator_only = derivative * (x - gap)
      omitted = merge_touching(_pieces_of_sign(numerator_only, [first_zero, second_zero], direction_sign))
      distractors.append(Distractor(
         error_path="BC-ERR-05017",
         derivation=f"the sign chart built on the zeros of f' only, leaving out x = {gap} where f' is undefined",
         label=_statement(direction, omitted, _reason(inequality, omitted)),
         mechanism="conceptual_confusion",
      ))
   else:
      second_derivative = sympy.diff(derivative, x)
      turning = sympy.solve(second_derivative, x)[0]
      rising = merge_touching(_pieces_of_sign(second_derivative, [turning], direction_sign))
      rising_word = "increasing" if direction_sign == 1 else "decreasing"
      distractors.append(Distractor(
         error_path="BC-ERR-05016",
         derivation=f"f taken to be {direction} where f' is {rising_word}, on the side of x = {turning} where f'' has that sign",
         label=_statement(direction, rising, f"because f' is {rising_word} there"),
         mechanism="conceptual_confusion",
      ))

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="find",
      notes={"interval_count": len(key_intervals)},
   )
