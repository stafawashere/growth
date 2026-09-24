"""BC-QA-02004, continuity deduced from differentiability as the step that lets a limit or an existence argument go through."""
from app.generation.kit import Distractor, Instance, Key, Step, math, table_figure

ARCHETYPE_ID = "BC-QA-02004"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "inputs", "type": "integer", "role": "safe", "count": 4, "distinct": True, "order": "increasing", "domain": {"min": 0, "max": 9, "step": 1}},
      {"name": "values", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "slopes", "type": "integer", "role": "safe", "count": 4, "domain": {"min": -5, "max": 5, "step": 1}},
      {"name": "scale", "type": "integer", "role": "safe", "domain": {"min": 2, "max": 5, "step": 1}},
      {"name": "offset", "type": "integer", "role": "safe", "domain": {"min": -9, "max": 9, "step": 1}},
      {"name": "target", "type": "integer", "role": "safe", "domain": {"min": -8, "max": 8, "step": 1}},
      {"name": "argument", "type": "label", "role": "difficulty", "domain": {"values": ["limit", "existence", "no_existence"]}},
   ],
   "constraints": [
      "argument != 'existence' or (values[0] - target) * (values[3] - target) < 0",
      "argument != 'no_existence' or min(values) > target or max(values) < target",
   ],
   "derived": [],
   "invariants": [
      "'differentiable' in key or argument == 'no_existence'",
      "'so it is continuous' in key or argument == 'no_existence'",
      "argument != 'no_existence' or 'No' in key",
   ],
   "dial_bindings": [
      {"parameter": "argument", "difficulty_factor_id": "BC-DF-10", "settings": {"limit": "low", "existence": "medium", "no_existence": "medium"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-03", "figure_kind": "table", "requires": ["inputs", "values", "slopes", "argument"]},
   ],
   "notes": "The stem states that g is differentiable and tabulates g and g prime. The limit argument evaluates the limit of scale times g plus offset at the second tabulated input by continuity; the existence argument applies the Intermediate Value Theorem on the outer interval. Either way continuity comes from differentiability. In the no_existence case every tabulated value of g lies on one side of the target, so the theorem guarantees nothing and the answer is no.",
}


def _no_existence(inputs, values, target, table, opening):
   low_x, high_x = inputs[0], inputs[3]
   where = "on " + math(rf"[{low_x}, {high_x}]")
   side = "less" if max(values) < target else "greater"
   stem = (
      f"{opening} Must there be a value c, with {math(rf'{low_x} < c < {high_x}')}, for which "
      f"{math(f'g(c) = {target}')}? Justify your answer."
   )
   steps = [
      Step(text=f"g is differentiable {where}, so it is continuous there.", rule="differentiability implies continuity"),
      Step(text=f"Every tabulated value of g is {side} than {target}, so no two of them have {target} between them.", rule="straddling values"),
      Step(text=f"The Intermediate Value Theorem guarantees nothing here, and g could stay {side} than {target} on the whole interval, so no such c must exist.", rule="Intermediate Value Theorem hypotheses"),
   ]
   key_label = f"No, because although g is differentiable {where}, so it is continuous there, every tabulated value of g is {side} than {target}."
   distractors = [
      Distractor(
         error_path="BC-ERR-99008",
         derivation="the Intermediate Value Theorem used without checking that the target lies between two values of g",
         label=f"Yes, such a c must exist, because g is differentiable {where}, so it is continuous there, and the Intermediate Value Theorem applies.",
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-02011",
         derivation="continuity asserted on a false basis, having tabulated values, and the theorem then applied without its straddling condition",
         label=f"Yes, such a c must exist, because the table gives a value of g at every listed input, so g is continuous {where}, and the Intermediate Value Theorem applies.",
         mechanism="compound",
      ),
      Distractor(
         error_path="BC-ERR-02012",
         derivation="the implication run backwards, continuity offered as the reason for differentiability, and the theorem then applied without its straddling condition",
         label=f"Yes, such a c must exist, because g is continuous {where}, so it is differentiable there, and the Intermediate Value Theorem applies.",
         mechanism="compound",
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
   values = [int(value) for value in names["values"]]
   slopes = [int(value) for value in names["slopes"]]
   scale = int(names["scale"])
   offset = int(names["offset"])
   target = int(names["target"])
   is_limit = names["argument"] == "limit"

   table = table_figure(
      ["x", "g(x)", "g'(x)"],
      [[point, value, slope] for point, value, slope in zip(inputs, values, slopes)],
      alt="A table of x, g(x) and g'(x): " + "; ".join(
         f"at x = {point}, g = {value} and g' = {slope}" for point, value, slope in zip(inputs, values, slopes)
      ) + ".",
   )
   opening = "The function g is differentiable for all real numbers, and selected values of g and its derivative are given in the table."

   if names["argument"] == "no_existence":
      return _no_existence(inputs, values, target, table, opening)

   if is_limit:
      point = inputs[1]
      result = scale * values[1] + offset
      offset_tex = f" + {offset}" if offset > 0 else (f" - {abs(offset)}" if offset < 0 else "")
      limit_tex = rf"\lim_{{x \to {point}}} \left({scale} g(x){offset_tex}\right)"
      stem = f"{opening} Find {math(limit_tex)}, and justify your answer."
      where = "at " + math(f"x = {point}")
      conclusion = math(rf"\lim_{{x \to {point}}} g(x) = g({point}) = {values[1]}")
      claim = f"The limit is {result}"
      steps = [
         Step(text=f"g is differentiable {where}, so it is continuous there.", rule="differentiability implies continuity"),
         Step(text=f"Continuity gives {conclusion}.", rule="limit of a continuous function"),
         Step(text=f"By the limit laws the limit is {scale}({values[1]}){offset_tex} = {result}.", rule="sum and constant multiple limit laws"),
      ]
   else:
      low_x, high_x = inputs[0], inputs[3]
      where = "on " + math(rf"[{low_x}, {high_x}]")
      ordered = sorted([(values[0], low_x), (values[3], high_x)])
      conclusion = math(rf"g({ordered[0][1]}) = {ordered[0][0]} < {target} < g({ordered[1][1]}) = {ordered[1][0]}")
      stem = (
         f"{opening} Must there be a value c, with {math(rf'{low_x} < c < {high_x}')}, for which "
         f"{math(f'g(c) = {target}')}? Justify your answer."
      )
      claim = "Yes, such a c must exist"
      steps = [
         Step(text=f"g is differentiable {where}, so it is continuous there.", rule="differentiability implies continuity"),
         Step(text=f"From the table, {conclusion}.", rule="straddling values"),
         Step(text="By the Intermediate Value Theorem there is at least one such c.", rule="Intermediate Value Theorem"),
      ]

   key_label = f"{claim}, because g is differentiable {where}, so it is continuous there, and {conclusion}."
   distractors = [
      Distractor(
         error_path="BC-ERR-02011",
         derivation="continuity asserted on a false basis, having tabulated values, instead of on the differentiability the stem supplies",
         label=f"{claim}, because the table gives a value of g at every listed input, so g is continuous {where}, and {conclusion}.",
         mechanism="theorem_condition_ignored",
      ),
      Distractor(
         error_path="BC-ERR-02012",
         derivation="the implication run backwards, with continuity offered as the reason for differentiability",
         label=f"{claim}, because g is continuous {where}, so it is differentiable there, and {conclusion}.",
         mechanism="reversed_quantities",
      ),
      Distractor(
         error_path="BC-ERR-99008",
         derivation="the conclusion used as if it held for every function, with no hypothesis about g checked",
         label=f"{claim}, because every function has its limit equal to its value at each input, and {conclusion}.",
         mechanism="theorem_condition_ignored",
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
