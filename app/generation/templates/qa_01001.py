"""BC-QA-01001, a two sided limit read from a graph with a removable break and a jump."""
from app.generation.kit import Distractor, Instance, Key, Step, figure, label, math, point_mark

ARCHETYPE_ID = "BC-QA-01001"
TEMPLATE_VERSION = "1"
AUTHORED_BY = "claude-opus-5-5 offline template, stage 5 of 2026-09-24"

SPEC = {
   "spec_version": "1",
   "evidence_tag": "inferred",
   "parameters": [
      {"name": "hole_x", "type": "integer", "role": "safe", "domain": {"values": [1, 2, 3]}},
      {"name": "jump_x", "type": "integer", "role": "safe", "domain": {"values": [5, 6]}},
      {"name": "start_y", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "hole_y", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "hole_value", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "left_limit", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "right_limit", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "end_y", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "jump_value", "type": "integer", "role": "safe", "domain": {"min": -3, "max": 4, "step": 1}},
      {"name": "value_mark", "type": "label", "role": "difficulty", "domain": {"values": ["marked", "unmarked"]}},
      {"name": "justify", "type": "label", "role": "difficulty", "domain": {"values": ["bare", "justified"]}},
      {"name": "request", "type": "label", "role": "difficulty", "domain": {"values": ["jump", "hole"]}},
   ],
   "constraints": [
      "hole_value != hole_y",
      "left_limit != right_limit",
      "jump_value != left_limit and jump_value != right_limit",
      "abs(left_limit - right_limit) >= 2",
   ],
   "derived": [],
   "invariants": [
      "request == 'hole' or 'does not exist' in key",
      "request == 'jump' or 'does not exist' not in key",
   ],
   "dial_bindings": [
      {"parameter": "value_mark", "difficulty_factor_id": "BC-DF-03", "settings": {"marked": "off", "unmarked": "low"}},
      {"parameter": "justify", "difficulty_factor_id": "BC-DF-10", "settings": {"bare": "off", "justified": "low"}},
      {"parameter": "request", "difficulty_factor_id": "BC-DF-03", "settings": {"hole": "off", "jump": "low"}},
   ],
   "calculator_guard": "True",
   "representation_bindings": [
      {"representation": "BC-REP-02", "figure_kind": "function_graph", "requires": ["hole_x", "jump_x", "left_limit", "right_limit", "value_mark"]},
   ],
   "notes": "Line segments join (0, start_y), (hole_x, hole_y), (jump_x, left_limit) and then (jump_x, right_limit), (8, end_y). The graph has a removable break at hole_x with a filled point at hole_value and a jump at jump_x, filled at jump_value when marked and unfilled otherwise. Half the items ask for the two sided limit at the jump, which does not exist; the other half ask for the limit and the function value at the removable break, where the limit exists and differs from the value.",
}


OPENING = r"The graph of the function f shown is defined for \( 0 \le x \le 8 \), except where the graph shows no filled point."


def _hole_item(hole_x, hole_y, hole_value, is_justified):
   limit_tex = rf"\lim_{{x \to {hole_x}}} f(x)"
   value_tex = f"f({hole_x})"
   request = " Justify your answers." if is_justified else ""
   stem = f"{OPENING} Find {math(limit_tex)} and {math(value_tex)}.{request}"

   def pair(limit_text, value):
      return f"{limit_text}, and {math(f'{value_tex} = {value}')}."

   key_label = pair(math(f"{limit_tex} = {hole_y}"), hole_value)
   steps = [
      Step(
         text=f"From both sides the graph approaches the open circle at ({hole_x}, {hole_y}), so {math(f'{limit_tex} = {hole_y}')}.",
         rule="two sided limit read from a graph",
      ),
      Step(
         text=f"The filled point above or below the circle gives the function value, {math(f'{value_tex} = {hole_value}')}. The limit does not depend on it.",
         rule="function value read from a graph",
      ),
   ]
   distractors = [
      Distractor(
         error_path="BC-ERR-01001",
         derivation="the plotted value of f reported as the limit",
         label=pair(math(f"{limit_tex} = {hole_value}"), hole_value),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01001",
         derivation="the limit and the plotted value of f treated as the same number, here the height of the open circle",
         label=pair(math(f"{limit_tex} = {hole_y}"), hole_y),
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01003",
         derivation="the open circle read as the function having no value on the curve there, and nonexistence of the limit concluded from that",
         label=pair(f"The limit {math(limit_tex)} does not exist", hole_value),
         mechanism="conceptual_confusion",
      ),
   ]

   return key_label, steps, distractors, stem


def _jump_item(jump_x, left_limit, right_limit, jump_value, is_marked, is_justified):
   limit_tex = rf"\lim_{{x \to {jump_x}}} f(x)"
   request = "Justify your answer." if is_justified else "If the limit does not exist, say why."
   stem = f"{OPENING} Find {math(limit_tex)}. {request}"

   key_label = f"The limit does not exist, because f(x) approaches different values from the left and from the right of x = {jump_x}."
   steps = [
      Step(
         text=f"As x approaches {jump_x} from the left, the graph approaches the open circle at ({jump_x}, {left_limit}), so the left hand limit is {left_limit}.",
         rule="one sided limit read from a graph",
      ),
      Step(
         text=f"As x approaches {jump_x} from the right, the graph approaches the open circle at ({jump_x}, {right_limit}), so the right hand limit is {right_limit}.",
         rule="one sided limit read from a graph",
      ),
      Step(
         text=f"The one sided limits differ, so {math(limit_tex)} does not exist, whatever the value of f at {jump_x}.",
         rule="two sided limit exists only when the one sided limits agree",
      ),
   ]

   if is_marked:
      third = Distractor(
         error_path="BC-ERR-01001",
         derivation="the plotted value of f at the jump reported as the limit",
         label=f"The limit is {jump_value}, because the graph has a filled point at ({jump_x}, {jump_value}).",
         mechanism="conceptual_confusion",
      )
   else:
      third = Distractor(
         error_path="BC-ERR-01003",
         derivation="nonexistence argued from the missing function value rather than from the one sided limits",
         label=f"The limit does not exist, because a limit can never exist where the graph has no filled point, as at x = {jump_x}.",
         mechanism="conceptual_confusion",
      )

   distractors = [
      Distractor(
         error_path="BC-ERR-01002",
         derivation="the value approached from the left reported as the two sided limit",
         label=f"The limit is {left_limit}, because f(x) approaches {left_limit} as x approaches {jump_x} from the left.",
         mechanism="conceptual_confusion",
      ),
      Distractor(
         error_path="BC-ERR-01002",
         derivation="the value approached from the right reported as the two sided limit",
         label=f"The limit is {right_limit}, because f(x) approaches {right_limit} as x approaches {jump_x} from the right.",
         mechanism="conceptual_confusion",
      ),
      third,
   ]

   return key_label, steps, distractors, stem


def build(names):
   hole_x = int(names["hole_x"])
   jump_x = int(names["jump_x"])
   start_y = int(names["start_y"])
   hole_y = int(names["hole_y"])
   hole_value = int(names["hole_value"])
   left_limit = int(names["left_limit"])
   right_limit = int(names["right_limit"])
   end_y = int(names["end_y"])
   jump_value = int(names["jump_value"])
   is_marked = names["value_mark"] == "marked"
   is_justified = names["justify"] == "justified"

   curves = [
      [[0, start_y], [hole_x, hole_y]],
      [[hole_x, hole_y], [jump_x, left_limit]],
      [[jump_x, right_limit], [8, end_y]],
   ]
   marks = [
      point_mark(0, start_y),
      point_mark(hole_x, hole_y, is_open=True),
      point_mark(hole_x, hole_value),
      point_mark(jump_x, left_limit, is_open=True),
      point_mark(jump_x, right_limit, is_open=True),
      point_mark(8, end_y),
   ]

   if is_marked:
      marks.append(point_mark(jump_x, jump_value))
      value_alt = f"a filled point at ({jump_x}, {jump_value})"
   else:
      value_alt = f"no point plotted at x = {jump_x}"

   graph = figure(
      "function_graph",
      domain=(-0.5, 8.5),
      range_=(-4.5, 5.5),
      curves=[curves],
      marks=marks,
      labels=[label("y = f(x)", 7.2, 5.0)],
      alt=(
         f"Line segments from (0, {start_y}) to ({hole_x}, {hole_y}) and on to ({jump_x}, {left_limit}), "
         f"with an open circle at ({hole_x}, {hole_y}) and a filled point at ({hole_x}, {hole_value}). "
         f"At x = {jump_x} there are open circles at ({jump_x}, {left_limit}) and ({jump_x}, {right_limit}) "
         f"and {value_alt}, and a segment runs from ({jump_x}, {right_limit}) to (8, {end_y})."
      ),
   )

   if names["request"] == "hole":
      key_label, steps, distractors, stem = _hole_item(hole_x, hole_y, hole_value, is_justified)
   else:
      key_label, steps, distractors, stem = _jump_item(jump_x, left_limit, right_limit, jump_value, is_marked, is_justified)

   return Instance(
      stem=stem,
      key=Key(form="statement", label=key_label),
      steps=steps,
      distractors=distractors,
      representation="BC-REP-02",
      calculator_status="no_calculator",
      figure=graph,
      command_verb="find",
   )
