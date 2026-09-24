"""BC-QA-01006, continuity of a piecewise function at its boundary tested against the three conditions."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01006"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "boundary", "type": "integer", "role": "safe", "domain": {"min": -2, "max": 3, "step": 1}},
      {"name": "left_limit", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "right_limit", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "point_value", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 4, "step": 1}},
      {"name": "left_slope", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "right_slope", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 3, "step": 1, "exclude": [0]}},
      {"name": "closed_side", "type": "label", "role": "safe", "domain": {"values": ["left", "right"]}},
      {"name": "break_kind", "type": "label", "role": "difficulty", "domain": {"values": ["value", "jump", "none"]}},
   ],
   "constraints": [
      "break_kind == 'value' or left_limit != right_limit",
      "break_kind != 'value' or point_value != left_limit",
   ],
   "derived": [],
   "invariants": [
      "break_kind == 'none' or 'is not continuous' in key",
      "break_kind != 'none' or 'is not continuous' not in key",
   ],
   "dial_bindings": [
      {"parameter": "break_kind", "difficulty_factor_id": "BC-DF-17", "settings": {"value": "low", "jump": "medium", "none": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["boundary", "left_limit", "right_limit", "point_value", "break_kind"]},
   ],
   "notes": "Linear branches meet the boundary at left_limit and right_limit. A value break and the no break case both use a quotient that simplifies to the left branch away from the boundary, with point_value (value break) or left_limit (no break) defined at the boundary; a jump break assigns the boundary to the closed side's branch. With no break the rule is a quotient that simplifies to the left branch away from the boundary, with the boundary value defined separately to match, so f is continuous there; the other two kinds fail continuity for the reason the kind names.",
}

x = sympy.Symbol("x")


def _cases(rows):
   body = r" \\ ".join(rf"{expression}, & {condition}" for expression, condition in rows)

   return rf"f(x) = \begin{{cases}} {body} \end{{cases}}"


def build(names):
   boundary = names["boundary"]
   left_limit = names["left_limit"]
   left_slope = names["left_slope"]
   right_slope = names["right_slope"]
   is_jump = names["break_kind"] == "jump"
   is_continuous = names["break_kind"] == "none"
   right_limit = names["right_limit"] if is_jump else left_limit
   closes_left = names["closed_side"] == "left"

   left_branch = left_slope * (x - boundary) + left_limit
   right_branch = right_slope * (x - boundary) + right_limit
   left_tex = tex(sympy.expand(left_branch))
   right_tex = tex(sympy.expand(right_branch))

   if is_jump:
      point_value = left_limit if closes_left else right_limit
      left_condition = rf"x \le {boundary}" if closes_left else rf"x < {boundary}"
      right_condition = rf"x > {boundary}" if closes_left else rf"x \ge {boundary}"
      rows = [(left_tex, left_condition), (right_tex, right_condition)]
   else:
      point_value = left_limit if is_continuous else names["point_value"]
      quotient_tex = rf"\frac{{{tex(sympy.expand((x - boundary) * left_branch))}}}{{{tex(x - boundary)}}}"
      rows = [(quotient_tex, rf"x \ne {boundary}"), (tex(point_value), rf"x = {boundary}")]

   stem = (
      f"Let f be the function defined by {math(_cases(rows))}. Determine whether f is continuous at "
      f"{math(f'x = {boundary}')}, and justify your answer."
   )

   left_limit_tex = rf"\lim_{{x \to {boundary}^-}} f(x) = {left_limit}"
   right_limit_tex = rf"\lim_{{x \to {boundary}^+}} f(x) = {right_limit}"
   steps = [
      Step(text=f"The function value at the boundary is {math(f'f({boundary}) = {point_value}')}.", rule="evaluate the function at the input"),
      Step(text=f"Using the branch for x less than {boundary}, {math(left_limit_tex)}.", rule="left hand limit from the left branch"),
      Step(text=f"Using the branch for x greater than {boundary}, {math(right_limit_tex)}.", rule="right hand limit from the right branch"),
   ]
   at = f"x = {boundary}"

   if is_continuous:
      steps = [
         Step(text=f"The function value at the boundary is {math(f'f({boundary}) = {point_value}')}, from the second line of the rule.", rule="evaluate the function at the input"),
         Step(text=f"For {math(rf'x \ne {boundary}')} the quotient simplifies to {math(left_tex)}, so {math(rf'\lim_{{x \to {boundary}}} f(x) = {left_limit}')} from both sides.", rule="limit after cancelling"),
         Step(text=f"The limit equals the function value, so f is continuous at {math(at)}.", rule="the limit must equal the function value"),
      ]
      key_label = f"f is continuous at {math(at)}, because the limit of f(x) there is {left_limit}, which equals f({boundary})."
      distractors = [
         Distractor(
            error_path="BC-ERR-01017",
            derivation=f"x = {boundary} substituted into the quotient, which applies only for x not equal to {boundary}, giving 0/0",
            label=f"f is not continuous at {math(at)}, because the quotient gives 0/0 at {math(at)}, so f({boundary}) is undefined.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01015",
            derivation="continuity concluded from the agreement of the one sided limits, with the function value never compared",
            label=f"f is continuous at {math(at)}, because the limits from both sides are {left_limit}, and matching one sided limits alone make a function continuous.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01014",
            derivation="continuity concluded because the function has a value at the input",
            label=f"f is continuous at {math(at)}, because f({boundary}) = {point_value} is defined, and a function is continuous wherever it has a value.",
            mechanism="conceptual_confusion",
         ),
      ]
   elif is_jump:
      steps.append(Step(
         text=f"The one sided limits differ, so {math(rf'\lim_{{x \to {boundary}}} f(x)')} does not exist and f is not continuous at {math(at)}.",
         rule="the limit must exist",
      ))
      key_label = f"f is not continuous at {math(at)}, because the limits from the left and from the right are {left_limit} and {right_limit}."
      wrong_branch_value = point_value
      far_side = "right" if closes_left else "left"
      distractors = [
         Distractor(
            error_path="BC-ERR-01014",
            derivation="continuity concluded because the function has a value at the input",
            label=f"f is continuous at {math(at)}, because f({boundary}) = {point_value} is defined, so f has a value at {math(at)}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01017",
            derivation=f"the {far_side} hand limit taken from the branch on the other side, so both one sided limits come out equal to f({boundary})",
            label=f"f is continuous at {math(at)}, because the limits from the left and from the right are both {wrong_branch_value}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-99001",
            derivation="a justification about an unnamed it, which reads the missing function value on one branch as missing for f, so the reason given is false",
            label=f"f is not continuous at {math(at)}, because it has no value there, so it cannot be continuous at {math(at)}.",
            mechanism="conceptual_confusion",
         ),
      ]
   else:
      steps = [
         Step(text=f"The function value at the boundary is {math(f'f({boundary}) = {point_value}')}, from the second line of the rule.", rule="evaluate the function at the input"),
         Step(text=f"For {math(rf'x \ne {boundary}')} the quotient simplifies to {math(left_tex)}, so {math(rf'\lim_{{x \to {boundary}}} f(x) = {left_limit}')} from both sides.", rule="limit after cancelling"),
         Step(
            text=f"The limit exists and equals {left_limit}, but {math(f'f({boundary}) = {point_value}')}, so the limit does not equal the function value and f is not continuous at {math(at)}.",
            rule="the limit must equal the function value",
         ),
      ]
      key_label = f"f is not continuous at {math(at)}, because the limit of f(x) there is {left_limit} while f({boundary}) = {point_value}."
      distractors = [
         Distractor(
            error_path="BC-ERR-01017",
            derivation=f"x = {boundary} substituted into the quotient, which applies only for x not equal to {boundary}, giving 0/0",
            label=f"f is not continuous at {math(at)}, because the quotient gives 0/0 at {math(at)}, so f({boundary}) is undefined.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01015",
            derivation="continuity concluded from the agreement of the one sided limits, with the function value never compared",
            label=f"f is continuous at {math(at)}, because the limits from the left and from the right are both {left_limit}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01001",
            derivation="the function value at the input reported as the limit, so the limit and the value appear to agree",
            label=f"f is continuous at {math(at)}, because the limit of f(x) there is {point_value}, which equals f({boundary}).",
            mechanism="conceptual_confusion",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-01",
      calculator_status="no_calculator",
      command_verb="determine",
   )
