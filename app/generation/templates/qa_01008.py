"""BC-QA-01008, two constants chosen so that a three piece function is continuous at both boundaries."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, tex

ARCHETYPE_ID = "BC-QA-01008"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "left_end", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1, "exclude": [0]}},
      {"name": "right_end", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 6, "step": 1}},
      {"name": "curvature", "type": "integer", "role": "safe", "domain": {"values": [-2, -1, 1, 2, 3]}},
      {"name": "lift", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "check", "type": "label", "role": "difficulty", "domain": {"values": ["values", "values_and_reason"]}},
   ],
   "constraints": [
      "right_end > left_end",
      "(curvature * right_end**2 + lift - 2 * left_end) % (right_end - left_end) == 0",
      "curvature * right_end**2 + lift != left_end + right_end",
      "curvature * left_end**2 + lift != 2 * left_end",
   ],
   "derived": [],
   "invariants": [
      "'k =' in key",
   ],
   "dial_bindings": [
      {"parameter": "check", "difficulty_factor_id": "BC-DF-17", "settings": {"values": "low", "values_and_reason": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-01", "figure_kind": None, "requires": ["left_end", "right_end", "curvature", "lift"]},
   ],
   "notes": "f is (x^2 - left_end^2)/(x - left_end) for x < left_end, kx + m on [left_end, right_end], and curvature x^2 + lift for x > right_end. The first branch equals x + left_end away from left_end, so matching at the two boundaries gives two linear equations in k and m. The constraints make k a whole number and keep both wrong branch pairings different from the key.",
}

x = sympy.Symbol("x")


def _pair_label(slope, intercept, reason):
   return f"{math(f'k = {tex(slope)}')} and {math(f'm = {tex(intercept)}')}, because {reason}."


def build(names):
   left_end = names["left_end"]
   right_end = names["right_end"]
   curvature = names["curvature"]
   lift = names["lift"]
   asks_reason = names["check"] == "values_and_reason"

   first_branch = rf"\frac{{{tex(x**2 - left_end**2)}}}{{{tex(x - left_end)}}}"
   last_branch = curvature * x**2 + lift
   left_limit = 2 * left_end
   right_value = curvature * right_end**2 + lift
   width = right_end - left_end

   slope = sympy.Rational(right_value - left_limit, width)
   intercept = left_limit - slope * left_end
   first_wrong_slope = sympy.Integer(1)
   first_wrong_intercept = sympy.Integer(left_end)
   last_at_left = curvature * left_end**2 + lift
   second_wrong_slope = sympy.Rational(right_value - last_at_left, width)
   second_wrong_intercept = last_at_left - second_wrong_slope * left_end

   rows = [
      (first_branch, rf"x < {left_end}"),
      ("kx + m", rf"{left_end} \le x \le {right_end}"),
      (tex(last_branch), rf"x > {right_end}"),
   ]
   body = r" \\ ".join(rf"{expression}, & {condition}" for expression, condition in rows)
   cases_tex = rf"f(x) = \begin{{cases}} {body} \end{{cases}}"
   request = " Show that the function value at each boundary agrees with both one sided limits." if asks_reason else ""
   stem = f"Let {math(cases_tex)}, where k and m are constants. Find the values of k and m for which f is continuous for all real numbers.{request}"

   left_equation = f"{left_end}k + m = {left_limit}"
   right_equation = f"{right_end}k + m = {right_value}"
   steps = [
      Step(
         text=(
            f"For {math(rf'x < {left_end}')}, {math(first_branch + ' = ' + tex(x + left_end))}, so the limit from the left at "
            f"{math(f'x = {left_end}')} is {left_limit}. The middle branch gives {math(f'f({left_end}) = {left_end}k + m')}, so {math(left_equation)}."
         ),
         rule="match the branches at the first boundary",
      ),
      Step(
         text=(
            f"At {math(f'x = {right_end}')} the middle branch gives {math(f'f({right_end}) = {right_end}k + m')} and the last branch "
            f"approaches {right_value}, so {math(right_equation)}."
         ),
         rule="match the branches at the second boundary",
      ),
      Step(
         text=f"Subtracting the equations gives {math(f'k = {tex(slope)}')}, and then {math(f'm = {tex(intercept)}')}.",
         rule="solve the linear system",
      ),
   ]

   key_label = _pair_label(slope, intercept, f"the middle branch must equal {left_limit} at {math(f'x = {left_end}')} and {right_value} at {math(f'x = {right_end}')}")
   distractors = [
      Distractor(
         error_path="BC-ERR-01017",
         derivation=f"at x = {right_end} the first branch, which applies only for x < {left_end}, used in place of the last branch",
         label=_pair_label(first_wrong_slope, first_wrong_intercept, f"the middle branch must equal {left_limit} at {math(f'x = {left_end}')} and {left_end + right_end} at {math(f'x = {right_end}')}"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01017",
         derivation=f"at x = {left_end} the last branch, which applies only for x > {right_end}, used in place of the first branch",
         label=_pair_label(second_wrong_slope, second_wrong_intercept, f"the middle branch must equal {last_at_left} at {math(f'x = {left_end}')} and {right_value} at {math(f'x = {right_end}')}"),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01003",
         derivation=f"the first branch is undefined at x = {left_end}, and that was taken to mean its limit there does not exist",
         label=f"No values of k and m work, because {math(first_branch)} is undefined at {math(f'x = {left_end}')}, so f has no limit there.",
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
      command_verb="find",
   )
