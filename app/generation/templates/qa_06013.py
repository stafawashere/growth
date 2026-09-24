"""BC-QA-06013, a definite integral found from given integral values with linearity, additivity, reversal and a jump."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-06013"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "direction", "type": "label", "role": "difficulty", "domain": {"values": ["forward", "reversed"]}},
      {"name": "start", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 1, "step": 1}},
      {"name": "gaps", "type": "integer", "role": "safe", "count": 3, "domain": {"min": 1, "max": 3, "step": 1}},
      {"name": "first_value", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "whole_value", "type": "integer", "role": "safe", "domain": {"min": -12, "max": 12, "step": 1}},
      {"name": "multiple", "type": "integer", "role": "safe", "domain": {"values": [-3, -2, 2, 3]}},
      {"name": "steps", "type": "integer", "role": "safe", "count": 2, "distinct": True, "domain": {"min": -4, "max": 4, "step": 1}},
   ],
   "constraints": [
      "key_value != 0",
      "distinct([key_value, jump_error, lower_error, limit_error])",
   ],
   "derived": [
      {"name": "lower", "expression": "start + gaps[0]"},
      {"name": "jump", "expression": "start + gaps[0] + gaps[1]"},
      {"name": "upper", "expression": "start + gaps[0] + gaps[1] + gaps[2]"},
      {"name": "step_part", "expression": "steps[0] * gaps[1] + steps[1] * gaps[2]"},
      {"name": "forward_value", "expression": "multiple * (whole_value - first_value) + step_part"},
      {"name": "orientation", "expression": "-1 if direction == 'reversed' else 1"},
      {"name": "key_value", "expression": "orientation * forward_value"},
      {"name": "jump_error", "expression": "orientation * (multiple * (whole_value - first_value) + steps[1] * (gaps[1] + gaps[2]))"},
      {"name": "lower_error", "expression": "forward_value if direction == 'reversed' else multiple * whole_value + step_part"},
      {"name": "limit_error", "expression": "orientation * (multiple * whole_value + step_part) if direction == 'reversed' else -key_value"},
   ],
   "invariants": [
      "exact(key)",
      "key != 0",
   ],
   "dial_bindings": [
      {"parameter": "direction", "difficulty_factor_id": "BC-DF-17", "settings": {"forward": "low", "reversed": "medium"}},
   ],
   "calculator_guard": "exact(key)",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["direction", "start", "gaps", "first_value", "whole_value", "multiple", "steps"]},
   ],
   "notes": "With a < b < d < c, the integral of f is given on [a, b] and [a, c], and h is m left of d and n from d on. The integral of k f + h over [b, c] is k (R - P) + m (d - b) + n (c - d), negated when the limits run from c to b. The derived key and error values are required to be pairwise different.",
}


def _signed(value):
   return f"+ {value}" if value >= 0 else f"- {-value}"


def build(names):
   start = int(names["start"])
   lower = int(names["lower"])
   jump = int(names["jump"])
   upper = int(names["upper"])
   first_value = int(names["first_value"])
   whole_value = int(names["whole_value"])
   multiple = int(names["multiple"])
   left_step, right_step = [int(value) for value in names["steps"]]
   is_reversed = names["direction"] == "reversed"
   orientation = -1 if is_reversed else 1

   middle_value = whole_value - first_value
   step_part = left_step * (jump - lower) + right_step * (upper - jump)
   forward_value = multiple * middle_value + step_part
   key_value = sympy.Integer(orientation * forward_value)

   limits = rf"\int_{{{upper}}}^{{{lower}}}" if is_reversed else rf"\int_{{{lower}}}^{{{upper}}}"
   stem = (
      f"Suppose {math(rf'\int_{{{start}}}^{{{lower}}} f(x)\,dx = {first_value}')} and "
      f"{math(rf'\int_{{{start}}}^{{{upper}}} f(x)\,dx = {whole_value}')}. The function h is defined by "
      f"{math(f'h(x) = {left_step}')} for {math(f'x < {jump}')} and {math(f'h(x) = {right_step}')} for "
      f"{math(rf'x \ge {jump}')}. Find {math(limits + rf' \left({multiple}f(x) + h(x)\right)\,dx')}."
   )

   steps = [
      Step(
         text=(
            f"Split the interval at x = {lower}: {math(rf'\int_{{{lower}}}^{{{upper}}} f(x)\,dx = {whole_value} {_signed(-first_value)} = {middle_value}')}."
         ),
         point_type_id="BC-PT-99005",
         rule="additivity over adjacent intervals",
      ),
      Step(
         text=(
            f"h jumps at x = {jump}, so split its integral there: {math(f'{left_step} \\cdot {jump - lower} {_signed(right_step)} \\cdot {upper - jump} = {step_part}')}."
         ),
         rule="integral of a step function split at the jump",
      ),
      Step(
         text=(
            f"By linearity, {math(rf'\int_{{{lower}}}^{{{upper}}} \left({multiple}f(x) + h(x)\right)\,dx = {multiple}({middle_value}) {_signed(step_part)} = {forward_value}')}."
         ),
         value=None if is_reversed else key_value,
         rule="constant multiple and sum properties",
      ),
   ]

   if is_reversed:
      steps.append(Step(
         text=f"The requested limits run from {upper} down to {lower}, which changes the sign: the value is {math(tex(key_value))}.",
         value=key_value,
         point_type_id="BC-PT-99004",
         rule="reversing the limits",
      ))
      lower_error = Distractor(
         error_path="BC-ERR-99012",
         derivation="the reversed pair of limits not handled, so the sign is never changed",
         value=sympy.Integer(forward_value),
         mechanism="sign_error",
      )
      limit_error = Distractor(
         error_path="BC-ERR-99032",
         derivation=f"the integral of f run from {start} instead of from {lower}, a lower limit the requested integral never has",
         value=sympy.Integer(orientation * (multiple * whole_value + step_part)),
         mechanism="wrong_limits",
      )
   else:
      steps[-1].point_type_id = "BC-PT-99004"
      lower_error = Distractor(
         error_path="BC-ERR-99012",
         derivation=f"the integral of f from {lower} to {upper} taken as the given integral from {start}, ignoring the part below {lower}",
         value=sympy.Integer(multiple * whole_value + step_part),
         mechanism="wrong_limits",
      )
      limit_error = Distractor(
         error_path="BC-ERR-99032",
         derivation="the limits written in reverse order, which changes the sign",
         value=-key_value,
         mechanism="sign_error",
      )

   distractors = [
      Distractor(
         error_path="BC-ERR-06031",
         derivation=f"h integrated as the single value {right_step} across the jump at x = {jump}",
         value=sympy.Integer(orientation * (multiple * middle_value + right_step * (upper - lower))),
         mechanism="theorem_condition_ignored",
      ),
      lower_error,
      limit_error,
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
