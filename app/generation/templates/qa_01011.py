"""BC-QA-01011, existence of an input with a given output argued from the Intermediate Value Theorem and a table."""
from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure

ARCHETYPE_ID = "BC-QA-01011"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inputs", "type": "integer", "role": "safe", "count": 4, "distinct": True, "order": "increasing", "domain": {"min": 0, "max": 9, "step": 1}},
      {"name": "outputs", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": -8, "max": 8, "step": 1}},
      {"name": "pair", "type": "label", "role": "difficulty", "domain": {"values": ["outer", "inner", "none"]}},
   ],
   "constraints": [
      "pair != 'outer' or (outputs[0] - target) * (outputs[3] - target) < 0",
      "pair != 'inner' or (outputs[0] - target) * (outputs[3] - target) > 0",
      "pair != 'inner' or (outputs[1] - target) * (outputs[2] - target) < 0",
      "pair != 'none' or min(outputs) > target or max(outputs) < target",
   ],
   "derived": [],
   "invariants": [
      "pair == 'none' or 'Intermediate Value Theorem gives at least one' in key",
      "pair != 'none' or 'No.' in key",
   ],
   "dial_bindings": [
      {"parameter": "pair", "difficulty_factor_id": "BC-DF-14", "settings": {"outer": "off", "inner": "low", "none": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["inputs", "outputs", "target", "pair"]},
   ],
   "notes": "A differentiable f is tabulated at four increasing inputs. The target lies strictly between the outputs at the two outer inputs, or, for the inner pair, only between the outputs at the two middle inputs, so the student has to choose the straddling pair. In the none case every tabulated value lies on one side of the target, the theorem guarantees nothing and the answer is no.",
}


def _unguaranteed(inputs, outputs, target, table, stem):
   whole = math(rf"[{inputs[0]}, {inputs[3]}]")
   side = "less" if max(outputs) < target else "greater"
   steps = [
      Step(text=f"Because f is differentiable, f is continuous on {whole}.", point_type_id="BC-PT-99015", rule="differentiability implies continuity"),
      Step(text=f"Every tabulated value of f is {side} than {target}, so no two of them have {target} between them.", rule="straddling values"),
      Step(
         text=f"The Intermediate Value Theorem needs {target} to lie between two values of f, so it guarantees nothing here, and a differentiable f with these values can stay {side} than {target} throughout. So no such c must exist.",
         point_type_id="BC-PT-99016",
         rule="Intermediate Value Theorem hypotheses",
      ),
   ]
   key_label = f"No. Every tabulated value of f is {side} than {target}, so the Intermediate Value Theorem does not apply on {whole}."
   distractors = [
      Distractor(
         error_path="BC-ERR-01026",
         derivation="the theorem applied with the straddling inequality never checked",
         label=f"Yes. Since f is differentiable, it is continuous on {whole}, so the Intermediate Value Theorem gives at least one such c.",
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-01028",
         derivation="the Mean Value Theorem named as the source of a point with a given function value",
         label=f"Yes. Since f is differentiable on {whole}, the Mean Value Theorem gives at least one such c.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01016",
         derivation="the general statement of the theorem restated in place of checking it against the table",
         label=f"Yes. A continuous function on {whole} takes every value between its values, so f takes the value {target}.",
         mechanism="conceptual_confusion",
      ),
   ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="justify",
   )


def build(names):
   inputs = [int(value) for value in names["inputs"]]
   outputs = [int(value) for value in names["outputs"]]
   target = int(names["target"])
   is_inner = names["pair"] == "inner"
   first, second = (1, 2) if is_inner else (0, 3)
   left_x, right_x = inputs[first], inputs[second]
   left_y, right_y = outputs[first], outputs[second]

   table = table_figure(
      ["x", "f(x)"],
      [[value, output] for value, output in zip(inputs, outputs)],
      alt="A table of x and f(x): " + ", ".join(f"f({value}) = {output}" for value, output in zip(inputs, outputs)) + ".",
   )

   window = rf"{inputs[0]} < c < {inputs[3]}"
   stem = (
      "The function f is differentiable for all real numbers, and selected values of f are given in the table. "
      f"Must there be a value c, with {math(window)}, for which {math(f'f(c) = {target}')}? Justify your answer."
   )

   if names["pair"] == "none":
      return _unguaranteed(inputs, outputs, target, table, stem)

   low, high = sorted([left_y, right_y])
   straddle = rf"f({left_x}) = {left_y}" if left_y == low else rf"f({right_x}) = {right_y}"
   straddle_top = rf"f({right_x}) = {right_y}" if left_y == low else rf"f({left_x}) = {left_y}"
   between = math(rf"{straddle} < {target} < {straddle_top}")
   interval = math(rf"[{left_x}, {right_x}]")

   inside = f", and that c also satisfies {math(window)}" if is_inner else ""
   steps = [
      Step(
         text=f"Because f is differentiable, f is continuous, in particular on {interval}.",
         point_type_id="BC-PT-99015",
         rule="differentiability implies continuity",
      ),
      Step(
         text=f"From the table, {between}, so {target} lies between the values of f at the ends of {interval}.",
         rule="straddling values",
      ),
      Step(
         text=(
            f"By the Intermediate Value Theorem there is at least one c with {math(rf'{left_x} < c < {right_x}')} "
            f"and {math(f'f(c) = {target}')}{inside}. So yes, such a c must exist."
         ),
         point_type_id="BC-PT-99016",
         rule="Intermediate Value Theorem",
      ),
   ]

   key_label = (
      f"Yes. Since f is differentiable, it is continuous on {interval}, and {between}, "
      "so the Intermediate Value Theorem gives at least one such c."
   )
   no_continuity = Distractor(
      error_path="BC-ERR-01025",
      derivation="the theorem applied with the continuity hypothesis never established",
      label=f"Yes. The Intermediate Value Theorem needs no hypothesis beyond {between}, so it gives at least one such c.",
      mechanism="theorem_condition_ignored",
   )
   uniqueness = Distractor(
      error_path="BC-ERR-01027",
      derivation="the existence conclusion of the theorem stated as uniqueness",
      label=(
         f"Yes. Since f is differentiable, it is continuous on {interval}, and {between}, "
         "so the Intermediate Value Theorem gives exactly one such c."
      ),
      mechanism="conceptual_confusion",
   )

   if is_inner:
      distractors = [
         Distractor(
            error_path="BC-ERR-01026",
            derivation="the straddling check made on the outer pair only, where it fails, and the failure read as a no",
            label=(
               f"No. Although f is continuous on {math(rf'[{inputs[0]}, {inputs[3]}]')}, {target} is not between "
               f"{math(rf'f({inputs[0]}) = {outputs[0]}')} and {math(rf'f({inputs[3]}) = {outputs[3]}')}, so no such c must exist."
            ),
            mechanism="conceptual_confusion",
         ),
         no_continuity,
         uniqueness,
      ]
   else:
      distractors = [
         no_continuity,
         uniqueness,
         Distractor(
            error_path="BC-ERR-01028",
            derivation="the Mean Value Theorem named in place of the Intermediate Value Theorem",
            label=(
               f"Yes. Since f is differentiable on {interval}, and {between}, "
               "the Mean Value Theorem gives at least one such c."
            ),
            mechanism="conceptual_confusion",
         ),
      ]

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-03",
      calculator_status="no_calculator",
      figure=table,
      command_verb="justify",
   )
