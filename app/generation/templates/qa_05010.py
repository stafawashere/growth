"""BC-QA-05010, whether the Extreme Value Theorem assures an absolute extreme value on an interval."""
from app.generation.kit import Distractor, Instance, Key, Step, math

ARCHETYPE_ID = "BC-QA-05010"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24, run D"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "left_end", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 2, "step": 1}},
      {"name": "length", "type": "integer", "role": "safe", "domain": {"min": 3, "max": 7, "step": 1}},
      {"name": "jump_offset", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "critical_offset", "type": "integer", "role": "safe", "domain": {"min": 1, "max": 6, "step": 1}},
      {"name": "letter", "type": "label", "role": "safe", "domain": {"values": ["f", "g", "h"]}},
      {"name": "extreme", "type": "label", "role": "safe", "domain": {"values": ["maximum", "minimum"]}},
      {"name": "situation", "type": "label", "role": "difficulty", "domain": {"values": ["continuous", "differentiable", "jump", "open"]}},
   ],
   "constraints": [
      "jump_offset < length",
      "critical_offset < length",
      "jump_offset != critical_offset",
   ],
   "derived": [
      {"name": "right_end", "expression": "left_end + length"},
      {"name": "jump_point", "expression": "left_end + jump_offset"},
      {"name": "critical_point", "expression": "left_end + critical_offset"},
   ],
   "invariants": [
      "left_end < critical_point and critical_point < right_end",
      "left_end < jump_point and jump_point < right_end",
      "(verdict == 'yes') == (situation in ['continuous', 'differentiable'])",
   ],
   "dial_bindings": [
      {"parameter": "situation", "difficulty_factor_id": "BC-DF-01", "settings": {"continuous": "off", "differentiable": "low", "jump": "low", "open": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-04", "figure_kind": None, "requires": ["left_end", "length", "situation", "extreme"]},
   ],
   "notes": (
      "Every stem also gives a relative extremum of the requested kind at critical_point, so a response that reports it "
      "as the absolute extremum, or that uses the theorem to place the extremum, has something concrete to name."
   ),
}


def _closed(low, high):
   return math(f"[{low}, {high}]")


def _open(low, high):
   return math(f"({low}, {high})")


def build(names):
   letter = names["letter"]
   low = names["left_end"]
   high = names["right_end"]
   jump = names["jump_point"]
   critical = names["critical_point"]
   extreme = names["extreme"]
   situation = names["situation"]
   is_maximum = extreme == "maximum"
   concavity = "<" if is_maximum else ">"
   relative = f"relative {extreme}"
   closed_text = _closed(low, high)
   open_text = _open(low, high)
   first_derivative_zero = math(f"{letter}'({critical}) = 0")
   second_derivative_sign = math(f"{letter}''({critical}) {concavity} 0")
   second_derivative_fact = f"{first_derivative_zero} and {second_derivative_sign}"

   if situation == "continuous":
      description = (
         f"The function {letter} is continuous on the closed interval {closed_text} and twice differentiable on "
         f"{open_text}, with {second_derivative_fact}."
      )
   elif situation == "differentiable":
      description = (
         f"The function {letter} is twice differentiable at every x in the closed interval {closed_text}, with "
         f"{second_derivative_fact}."
      )
   elif situation == "jump":
      description = (
         f"The function {letter} is defined on the closed interval {closed_text} and is twice differentiable at every "
         f"x in that interval except {math(f'x = {jump}')}, where {letter} has a jump discontinuity. Also "
         f"{second_derivative_fact}."
      )
   else:
      description = (
         f"The function {letter} is twice differentiable at every x in the closed interval {closed_text}, with "
         f"{second_derivative_fact}."
      )

   is_open_question = situation == "open"
   asked_interval = f"the open interval {open_text}" if is_open_question else f"the closed interval {closed_text}"
   stem = f"{description} Must {letter} attain an absolute {extreme} value on {asked_interval}? Justify the answer."

   theorem = "the Extreme Value Theorem"
   applies = f"so {theorem} applies"
   relative_claim = (
      f"Yes, because {letter} has a {relative} at {math(f'x = {critical}')}, so its absolute {extreme} value is "
      f"{math(f'{letter}({critical})')}."
   )

   if situation in ("continuous", "differentiable"):
      verdict = "yes"

      if situation == "differentiable":
         continuity_reason = f"{letter} is differentiable, so continuous, on the closed interval {closed_text}"
      else:
         continuity_reason = f"{letter} is continuous on the closed interval {closed_text}"

      key_label = f"Yes, because {continuity_reason}, {applies}."
      steps = [
         Step(text=f"The interval {closed_text} is closed and bounded.", rule="closed interval hypothesis"),
         Step(text=f"The function {continuity_reason}.", rule="differentiability implies continuity" if situation == "differentiable" else "continuity hypothesis"),
         Step(text=f"Both hypotheses of {theorem} hold, so {letter} attains an absolute {extreme} value on {closed_text}. The theorem gives existence only, not where the value occurs.", rule="Extreme Value Theorem"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-05007",
            derivation="the theorem applied because the interval is closed, with continuity never checked",
            label=f"Yes, because {letter} is defined at every x in the closed interval {closed_text}, {applies}.",
         ),
         Distractor(
            error_path="BC-ERR-05008",
            derivation="the existence theorem used to say where the extreme value is, at the critical point given",
            label=f"Yes, because {theorem} places the absolute {extreme} at {math(f'x = {critical}')}, where {first_derivative_zero}.",
         ),
         Distractor(
            error_path="BC-ERR-05012",
            derivation="the relative extremum found by the second derivative test reported as the absolute one",
            label=relative_claim,
         ),
      ]
   elif situation == "jump":
      verdict = "no"
      key_label = f"No, because {letter} is not continuous on the closed interval {closed_text}, so {theorem} does not apply."
      steps = [
         Step(text=f"The interval {closed_text} is closed.", rule="closed interval hypothesis"),
         Step(text=f"{letter} has a jump discontinuity at {math(f'x = {jump}')}, inside the interval, so {letter} is not continuous on {closed_text}.", rule="continuity hypothesis"),
         Step(text=f"A hypothesis of {theorem} fails, so the theorem gives no conclusion and {letter} need not attain an absolute {extreme} value.", rule="Extreme Value Theorem"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-05007",
            derivation="the theorem cited on a closed interval for a function with a jump inside it",
            label=f"Yes, because {letter} is defined at every x in the closed interval {closed_text}, {applies}.",
         ),
         Distractor(
            error_path="BC-ERR-99008",
            derivation="continuity checked only away from the jump, so the hypothesis was never verified on the whole interval",
            label=f"Yes, because {letter} is continuous on {closed_text} except at {math(f'x = {jump}')}, {applies}.",
         ),
         Distractor(
            error_path="BC-ERR-05012",
            derivation="the relative extremum found by the second derivative test reported as the absolute one",
            label=relative_claim,
         ),
      ]
   else:
      verdict = "no"
      key_label = f"No, because {open_text} is not a closed interval, so {theorem} does not apply there."
      steps = [
         Step(text=f"{letter} is differentiable, and so continuous, on {closed_text}, but the question asks about the open interval {open_text}.", rule="closed interval hypothesis"),
         Step(text=f"{theorem[0].upper() + theorem[1:]} needs a closed interval, so it gives no conclusion on {open_text}.", rule="Extreme Value Theorem"),
         Step(text=f"The absolute {extreme} of {letter} on {closed_text} may occur only at an endpoint, which the open interval leaves out, so {letter} need not attain an absolute {extreme} value on {open_text}.", rule="endpoint candidates"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-05007",
            derivation="the theorem applied on an open interval because the function is continuous there",
            label=f"Yes, because {letter} is continuous on the interval {open_text}, {applies}.",
         ),
         Distractor(
            error_path="BC-ERR-05008",
            derivation="the existence theorem used to place the extreme value at an endpoint, which is then read as a verdict",
            label=f"No, because {theorem} places the absolute {extreme} of {letter} on {closed_text} at an endpoint.",
         ),
         Distractor(
            error_path="BC-ERR-05012",
            derivation="the relative extremum found by the second derivative test reported as the absolute one",
            label=relative_claim,
         ),
      ]

   for distractor in distractors:
      distractor.mechanism = "theorem_condition_ignored" if distractor.error_path in ("BC-ERR-05007", "BC-ERR-99008") else "conceptual_confusion"

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-04",
      calculator_status="no_calculator",
      command_verb="justify",
      notes={"verdict": verdict},
   )
