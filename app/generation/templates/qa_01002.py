"""BC-QA-01002, what a table of values near an input suggests about the limit there."""
import sympy

from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure

ARCHETYPE_ID = "BC-QA-01002"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 5, "step": 1}},
      {"name": "left_value", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 6, "step": 1}},
      {"name": "right_value", "type": "integer", "role": "safe", "domain": {"min": -4, "max": 6, "step": 1}},
      {"name": "left_slope", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "right_slope", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1, "exclude": [0]}},
      {"name": "curvature", "type": "integer", "role": "safe", "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "behaviour", "type": "label", "role": "difficulty", "domain": {"values": ["agree", "jump", "oscillate"]}},
   ],
   "constraints": [
      "left_value != right_value",
      "left_slope != right_slope",
   ],
   "derived": [],
   "invariants": [
      "behaviour != 'agree' or 'suggests that the limit is' in key",
      "behaviour == 'agree' or 'suggests that the limit does not exist' in key",
   ],
   "dial_bindings": [
      {"parameter": "behaviour", "difficulty_factor_id": "BC-DF-03", "settings": {"agree": "off", "jump": "low", "oscillate": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["target", "left_value", "right_value", "behaviour"]},
   ],
   "notes": "Rows sit at distances 0.1, 0.01, 0.001 and 0.0001 on each side of the target. Agreeing tables approach left_value from both sides; jump tables approach left_value on the left and right_value on the right; oscillating tables alternate between left_value and right_value on both sides. Each output is the approached value plus slope times the distance plus curvature times its square, shown to four decimal places.",
}

DISTANCES = [sympy.Rational(1, 10), sympy.Rational(1, 100), sympy.Rational(1, 1000), sympy.Rational(1, 10000)]


def _four_places(value):
   return f"{float(value):.4f}"


def _outputs(names):
   left_value = names["left_value"]
   right_value = names["right_value"]
   behaviour = names["behaviour"]
   curvature = names["curvature"]
   left_outputs = []
   right_outputs = []

   for index, distance in enumerate(DISTANCES):
      if behaviour == "agree":
         left_outputs.append(left_value + names["left_slope"] * distance + curvature * distance**2)
         right_outputs.append(left_value + names["right_slope"] * distance + curvature * distance**2)
      elif behaviour == "jump":
         left_outputs.append(left_value + names["left_slope"] * distance + curvature * distance**2)
         right_outputs.append(right_value + names["right_slope"] * distance + curvature * distance**2)
      else:
         is_even = index % 2 == 0
         left_outputs.append(left_value if is_even else right_value)
         right_outputs.append(right_value if is_even else left_value)

   return left_outputs, right_outputs


def build(names):
   target = names["target"]
   left_value = names["left_value"]
   right_value = names["right_value"]
   behaviour = names["behaviour"]
   left_outputs, right_outputs = _outputs(names)

   rows = []

   for distance, output in reversed(list(zip(DISTANCES, left_outputs))):
      rows.append([_four_places(target - distance), _four_places(output)])

   for distance, output in zip(DISTANCES, right_outputs):
      rows.append([_four_places(target + distance), _four_places(output)])

   table = table_figure(
      ["x", "f(x)"],
      rows,
      alt="A table of x and f(x): " + ", ".join(f"f({row[0]}) = {row[1]}" for row in rows) + ".",
   )

   limit_tex = rf"\lim_{{x \to {target}}} f(x)"
   stem = (
      f"Selected values of a function f are given in the table. The function f is not defined at "
      f"{math(f'x = {target}')}. What does the table suggest about {math(limit_tex)}?"
   )

   nearest_left = _four_places(left_outputs[-1])
   undefined_reason = Distractor(
      error_path="BC-ERR-01003",
      derivation="nonexistence concluded from f being undefined at the target rather than from the outputs",
      label=f"The table suggests that the limit does not exist, because no limit can exist where f is not defined, as at x = {target}.",
      mechanism="conceptual_confusion",
   )

   if behaviour == "agree":
      key_label = (
         f"The table suggests that the limit is {left_value}, because the outputs approach {left_value} "
         f"from both sides of x = {target}."
      )
      steps = [
         Step(text=f"From the left, the outputs {', '.join(_four_places(value) for value in left_outputs)} approach {left_value}.", rule="reading a table from one side"),
         Step(text=f"From the right, the outputs {', '.join(_four_places(value) for value in right_outputs)} also approach {left_value}.", rule="reading a table from one side"),
         Step(text=f"Both sides approach the same value, so the table suggests the limit is {left_value}. A table can suggest a limit but cannot prove it.", rule="two sided limit from agreeing one sided behaviour"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-01005",
            derivation="the agreement of the outputs with the value taken as proof of the limit",
            label=f"The table proves that the limit is {left_value}, because the outputs nearest x = {target} are within 0.01 of {left_value}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01005",
            derivation="the output in the row nearest the target taken as the limit itself, as if the table settled it",
            label=f"The table suggests that the limit is {nearest_left}, because that output is the one nearest x = {target}.",
            mechanism="conceptual_confusion",
         ),
         undefined_reason,
      ]
   elif behaviour == "jump":
      key_label = (
         f"The table suggests that the limit does not exist, because the outputs approach different values "
         f"on the two sides of x = {target}."
      )
      steps = [
         Step(text=f"From the left, the outputs {', '.join(_four_places(value) for value in left_outputs)} approach {left_value}.", rule="reading a table from one side"),
         Step(text=f"From the right, the outputs {', '.join(_four_places(value) for value in right_outputs)} approach {right_value}.", rule="reading a table from one side"),
         Step(text="The two sides approach different values, so the table suggests the two sided limit does not exist.", rule="two sided limit exists only when the one sided limits agree"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-01002",
            derivation="the value the left hand rows approach reported as the two sided limit",
            label=f"The table suggests that the limit is {left_value}, because the outputs approach {left_value} from the left of x = {target}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01002",
            derivation="the value the right hand rows approach reported as the two sided limit",
            label=f"The table suggests that the limit is {right_value}, because the outputs approach {right_value} from the right of x = {target}.",
            mechanism="conceptual_confusion",
         ),
         undefined_reason,
      ]
   else:
      key_label = (
         f"The table suggests that the limit does not exist, because the outputs keep alternating as x "
         f"approaches {target}."
      )
      steps = [
         Step(text=f"On each side the outputs switch between {left_value} and {right_value} however close x comes to {target}.", rule="reading a table from one side"),
         Step(text="The outputs do not settle toward any single value, so the table suggests the limit does not exist.", rule="limit requires the outputs to settle"),
      ]
      distractors = [
         Distractor(
            error_path="BC-ERR-01004",
            derivation="one of the two values the outputs alternate between reported as the limit",
            label=f"The table suggests that the limit is {left_value}, because the outputs keep returning to {left_value}.",
            mechanism="conceptual_confusion",
         ),
         Distractor(
            error_path="BC-ERR-01004",
            derivation="the other of the two values the outputs alternate between reported as the limit",
            label=f"The table suggests that the limit is {right_value}, because the outputs keep returning to {right_value}.",
            mechanism="conceptual_confusion",
         ),
         undefined_reason,
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="estimate",
   )
