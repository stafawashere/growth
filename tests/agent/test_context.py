"""docs/agent/architecture.md, The screen context and The context composer.

Before submission the packet is built from an allow-list, so the proof is a grep over the whole
rendered prompt, prefix and variable section, for every form of the item's key, every option value,
every worked solution step and every error or misconception id. After submission the packet carries
the elaborated payload, exactly one error id and at most one scoring point. A browsing screen carries the
section's own text. The screen shape is refused when it names an unknown kind or an extra field,
and a timed part is flagged and refused. The context line is the one design.md's table gives.
"""
import dataclasses
import json
import re
from pathlib import Path
from types import SimpleNamespace

import pytest
import sympy

from app.agent import context as context_module
from app.agent.context import (
   TimedPartRefused,
   compose_packet,
   point_type_for_step,
   question_key_forms,
   render_prompt,
   screen_line,
   turn_anchors,
   validate_screen,
)
from app.agent.drawing.record import stored_figure
from app.content.loader import load_snapshot
from app.evals import agent_checks, golden
from app.feedback import render
from app.items.mathjson import to_sympy
from app.runtime.context import DEFAULT_CONTENT_ROOT

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DESIGN_PATH = REPOSITORY_ROOT / "docs" / "agent" / "design.md"
ITEM_PATH = REPOSITORY_ROOT / "content" / "items_unit06_agent" / "ITM-AGT-06002-00.json"
LESSON_ID = "LSN-CON-06003"
PREDICTION_LESSON_ID = "LSN-CON-01006"
SESSION_ID = "SES-" + "0a" * 16
ATTEMPT_ID = "ATT-" + "0b" * 16
EXCLUDED_KEYS = ("answer_key", "is_key", "worked_solution", "common_distractors", "error_path", "value")


@pytest.fixture(scope="module")
def context():
   return golden.agent_context(load_snapshot(DEFAULT_CONTENT_ROOT))


@pytest.fixture(scope="module")
def item():
   return json.loads(ITEM_PATH.read_text())


def item_screen(item, submitted=False, **extra):
   screen = {
      "kind": "session_item",
      "session_id": SESSION_ID,
      "attempt_id": ATTEMPT_ID,
      "item_id": item["id"],
      "format": "mcq",
      "served_stage": "unsupported",
      "submitted": submitted,
   }
   screen.update(extra)

   return screen


def practice_prompt(context, item):
   attempt = SimpleNamespace(submitted_at=None, served_stage="unsupported", format="mcq", correct=None)
   packet, _move = compose_packet(
      context,
      item_screen(item),
      item=item,
      attempt=attempt,
      lesson=golden.agent_lesson(LESSON_ID),
      misconception_names=["A Riemann sum is a sum of the listed values"],
   )
   rendered = render_prompt(packet, [], None, [], "which option is it")

   return packet, rendered.system + rendered.user


def keys_anywhere(value):
   if isinstance(value, dict):
      for key, inner in value.items():
         yield key
         yield from keys_anywhere(inner)

   if isinstance(value, list):
      for inner in value:
         yield from keys_anywhere(inner)


def test_the_practice_prompt_carries_no_key_form(context, item):
   packet, prompt = practice_prompt(context, item)
   forms_without_letters = dataclasses.replace(agent_checks.key_forms(item), letter_patterns=())
   verdict = agent_checks.no_answer_before_submission(prompt, {"mode": "practice"}, forms_without_letters)

   assert verdict.passed, verdict.reason
   assert "145/2" not in prompt
   assert "72.5" not in prompt
   assert "\\frac{145}{2}" not in prompt
   assert packet.body["item"]["options"] == ["A", "B", "C", "D"]


def test_the_practice_prompt_carries_no_option_value_solution_or_record_id(context, item):
   packet, prompt = practice_prompt(context, item)

   for option in item["options"]:
      value = option["value"]
      expression = to_sympy(value)

      is_structured = isinstance(value, list)

      assert json.dumps(value) not in prompt

      if is_structured:
         assert sympy.latex(expression) not in prompt

      assert re.search(r"(?<![\d.])" + re.escape(str(expression)) + r"(?![\d])", prompt) is None, option["id"]

   for step in item["worked_solution"]:
      assert step["text"] not in prompt

   assert "BC-ERR" not in prompt
   assert "BC-MIS" not in prompt

   for derivation in item["parameter_draw"]["distractor_derivations"].values():
      assert derivation not in prompt

   for distractor in context.archetypes[item["archetype_id"]]["common_distractors"]:
      assert distractor not in prompt

   present = set(keys_anywhere(packet.body))

   assert present.isdisjoint(EXCLUDED_KEYS), present & set(EXCLUDED_KEYS)


def after_submission_packet(context, item):
   archetype = context.archetypes[item["archetype_id"]]
   chosen = next(option for option in item["options"] if option["id"] == "B")
   feedback = render.render_feedback(
      "unsupported",
      archetype,
      {"worked_solution": json.dumps(item["worked_solution"])},
      submitted=True,
      correct=False,
      chosen_option=chosen,
      error_record=context.errors[chosen["error_path"]],
      confidence="confident",
   )
   attempt = SimpleNamespace(submitted_at="2026-09-29T00:00:00+00:00", served_stage="unsupported", format="mcq", correct=0)
   packet, move = compose_packet(
      context,
      item_screen(item, submitted=True, feedback_kind="elaborated"),
      item=item,
      attempt=attempt,
      lesson=golden.agent_lesson(LESSON_ID),
      feedback=feedback,
   )

   return packet, move


def test_after_submission_the_packet_carries_the_elaborated_fields_one_error_and_no_two_word_point(context, item):
   """The violated step shares only "form" and "trapezoid" with BC-PT-99018, below the three words
   point_type_for_step asks for, so no point is named."""
   packet, move = after_submission_packet(context, item)
   rendered = render_prompt(packet, [], None, [], "why was B wrong")
   feedback = packet.body["feedback"]
   error_ids = set(re.findall(r"BC-ERR-\d{5}", rendered.user))
   point_ids = set(re.findall(r"BC-PT-\d{5}", json.dumps(feedback)))

   assert packet.mode == "after_submission"
   assert move == "discuss_step"
   assert feedback["violated_step"] == context.archetypes[item["archetype_id"]]["expected_solution_path"][0]
   assert feedback["observed_behavior"] == context.errors["BC-ERR-06001"]["observed_behavior"]
   assert feedback["scoring_consequence"] == context.errors["BC-ERR-06001"]["scoring_consequence"]
   assert feedback["worked_solution"] == [step["text"] for step in item["worked_solution"]]
   assert feedback["kind"] == "elaborated"
   assert feedback["correct"] is False
   assert error_ids == {"BC-ERR-06001"}
   assert point_ids == set()
   assert "point" not in feedback
   assert feedback["lesson_section"] == "LSN-CON-06003#err-BC-ERR-06001"


def test_a_browsing_lesson_screen_carries_the_section_text(context):
   lesson = golden.agent_lesson(LESSON_ID)
   section = next(entry for entry in lesson.body["sections"] if entry["id"] == f"{LESSON_ID}#s3")
   screen = {
      "kind": "lesson",
      "lesson_id": LESSON_ID,
      "version": lesson.version,
      "section_id": section["id"],
      "section_index": 2,
      "section_count": len(lesson.body["sections"]),
      "return_to": "/lessons",
   }
   packet, move = compose_packet(context, screen, lesson=lesson)
   rendered = render_prompt(packet, [], None, [], "say it another way")

   assert packet.mode == "browsing"
   assert move == "explain"
   assert section["text"] in rendered.user
   assert packet.body["lesson"]["concept"] == "Riemann sum approximation of a definite integral"


def test_validate_screen_refuses_an_unknown_kind_and_an_extra_field():
   with pytest.raises(ValueError):
      validate_screen({"kind": "dashboard"})

   with pytest.raises(ValueError):
      validate_screen({"kind": "review", "draft": "x = 3"})

   with pytest.raises(ValueError):
      validate_screen({"kind": "session_item", "session_id": SESSION_ID})

   assert validate_screen({"kind": "review"}).timed is False


def test_a_timed_part_is_flagged_and_refused(context):
   screen = {"kind": "assessments", "format": "mock", "timed": True}

   assert validate_screen(screen).timed is True

   with pytest.raises(TimedPartRefused):
      compose_packet(context, screen)


def design_lines():
   text = DESIGN_PATH.read_text()
   table = text.split("| Screen | Line |", 1)[1].split("\n\n", 1)[0]
   rows = {}

   for line in table.strip().splitlines()[1:]:
      cells = [cell.strip() for cell in line.strip("|").split("|")]
      rows[cells[0]] = cells[1]

   return rows


def test_screen_line_matches_the_design_table():
   rows = design_lines()
   item_fields = {"session_id": SESSION_ID, "attempt_id": ATTEMPT_ID, "item_id": "ITM-AGT-06002-00", "format": "mcq", "served_stage": "unsupported"}
   lesson_screen = {"kind": "lesson", "lesson_id": LESSON_ID, "version": 1, "section_id": f"{LESSON_ID}#s3", "section_index": 2, "section_count": 9, "return_to": None}
   names = {LESSON_ID: "Riemann sums", "BC-SKL-06008": "Compute a trapezoidal sum", "map": "the skill map", "mock": "mock", "tutor": "Tutor"}
   cases = {
      "Today, no session open": ({"kind": "today"}, {}),
      "A practice item before checking": (dict(item_fields, kind="session_item", submitted=False), {}),
      "The same item after checking": (dict(item_fields, kind="session_item", submitted=True, feedback_kind="elaborated"), {}),
      "A lesson in a session or the library": (lesson_screen, {"{concept name}": "Riemann sums", "{n}": "3", "{total}": "9"}),
      "Review": ({"kind": "review"}, {}),
      "Progress, a tab": ({"kind": "progress", "tab": "map"}, {"{tab name}": "the skill map"}),
      "Progress, a skill opened": ({"kind": "progress", "tab": "map", "skill_id": "BC-SKL-06008"}, {"{skill name}": "Compute a trapezoidal sum"}),
      "Assessments, before starting": ({"kind": "assessments", "format": "mock"}, {"{format}": "mock"}),
      "Settings": ({"kind": "settings", "tab": "tutor"}, {"{tab}": "Tutor"}),
   }

   assert set(cases) == set(rows)

   for description, (screen, placeholders) in cases.items():
      expected = rows[description]

      for placeholder, value in placeholders.items():
         expected = expected.replace(placeholder, value)

      validate_screen(screen)

      assert screen_line(screen, names) == expected, description


def test_a_step_sharing_two_words_with_a_point_names_no_point(context):
   """BC-QA-03008's fourth step substitutes the first derivative, and the only point it shares
   words with is the higher-derivative point, on "deriv" and "point" alone."""
   archetype = context.archetypes["BC-QA-03008"]
   scoring_points = context.snapshot.scoring_points

   assert archetype["expected_solution_path"][3] == "substitute the value of the first derivative at that point"
   assert "BC-PT-99027" in archetype["point_types"]
   assert point_type_for_step(archetype, 3, scoring_points) is None


def test_a_unique_three_word_match_is_still_named(context):
   archetype = context.archetypes["BC-QA-01011"]
   point = point_type_for_step(archetype, 3, context.snapshot.scoring_points)

   assert point is not None
   assert point["id"] == "BC-PT-99016"
   assert point["name"] == "Intermediate Value Theorem conclusion"


def lesson_screen_on(lesson, section_id, index):
   return {
      "kind": "lesson",
      "lesson_id": lesson.id,
      "version": lesson.version,
      "section_id": section_id,
      "section_index": index,
      "section_count": len(lesson.body["sections"]),
      "return_to": "/lessons",
   }


def test_a_prediction_section_is_practice_with_its_question_and_without_its_key(context):
   """LSN-CON-01006 opens with a prediction whose keyed option is B, labelled 2, resolved in
   words that state the limit."""
   lesson = golden.agent_lesson(PREDICTION_LESSON_ID)
   section = lesson.body["sections"][0]
   screen = lesson_screen_on(lesson, section["id"], 0)
   packet, move = compose_packet(context, screen, lesson=lesson)
   rendered = render_prompt(packet, [], None, [], "what is the limit here")
   prompt = rendered.system + rendered.user

   assert section["type"] == "prediction"
   assert packet.mode == "practice"
   assert move == "ask_what_tried"
   assert packet.body["item"]["stem"] == section["stem"]["text"]
   assert packet.body["item"]["options"] == ["A", "B", "C"]
   assert section["resolution"]["text"] not in prompt
   assert "is_key" not in list(keys_anywhere(packet.body))
   assert "It does not exist" not in prompt

   forms = question_key_forms(section)

   assert forms.expression == 2
   assert any(pattern.search("the limit is that height, 2") for pattern in forms.text_patterns)
   assert any(pattern.search("option B") for pattern in forms.letter_patterns)


def test_a_check_section_is_practice_and_its_key_and_worked_solution_stay_out(context):
   lesson = golden.agent_lesson(PREDICTION_LESSON_ID)
   check = lesson.body["checks"][0]
   screen = lesson_screen_on(lesson, check["id"], 3)
   packet, _move = compose_packet(context, screen, lesson=lesson)
   rendered = render_prompt(packet, [], None, [], "how do I start")
   prompt = rendered.system + rendered.user

   assert packet.mode == "practice"
   assert packet.body["item"]["stem"] == check["stem"]["text"]

   for step in check["worked_solution"]:
      assert step["text"] not in prompt

   assert question_key_forms(check).expression == check["answer_key"]["mathjson"]


def test_a_fix_prompt_is_practice_and_its_right_step_stays_out(context):
   lesson = golden.agent_lesson(PREDICTION_LESSON_ID)
   index, section = next(
      (index, entry) for index, entry in enumerate(lesson.body["sections"]) if entry.get("fix_prompt") is True
   )
   packet, _move = compose_packet(context, lesson_screen_on(lesson, section["id"], index), lesson=lesson)
   rendered = render_prompt(packet, [], None, [], "what should it be")

   assert packet.mode == "practice"
   assert section["right_step"]["text"] not in rendered.user
   assert section["wrong_step"]["text"] in packet.body["item"]["stem"]


def test_a_faded_example_is_practice_and_holds_back_its_later_steps(context):
   lesson = golden.agent_lesson(PREDICTION_LESSON_ID)
   index, section = next(
      (index, entry) for index, entry in enumerate(lesson.body["sections"]) if entry.get("fade_from") is not None
   )
   packet, _move = compose_packet(context, lesson_screen_on(lesson, section["id"], index), lesson=lesson)
   rendered = render_prompt(packet, [], None, [], "what comes next")
   held_back = section["steps"][section["fade_from"] - 1:]

   assert packet.mode == "practice"
   assert section["problem"]["text"] in packet.body["item"]["stem"]

   for step in held_back:
      assert step["cue"] not in rendered.user
      assert step["why"] not in rendered.user


def test_an_orientation_section_stays_browsing(context):
   lesson = golden.agent_lesson(PREDICTION_LESSON_ID)
   section = lesson.body["sections"][1]
   packet, move = compose_packet(context, lesson_screen_on(lesson, section["id"], 1), lesson=lesson)

   assert section["type"] == "orientation"
   assert packet.mode == "browsing"
   assert move == "explain"
   assert packet.body["lesson"]["section"]["text"].startswith(section["text"])


def test_the_packet_carries_drawing_from_the_move_and_the_switch(context, item):
   first_on_item, move = compose_packet(context, item_screen(item), item=item)
   today, today_move = compose_packet(context, {"kind": "today"})
   switched_off, _move = compose_packet(context, {"kind": "today"}, drawing_enabled=False)

   assert (move, first_on_item.drawing) == ("ask_what_tried", "closed")
   assert (today_move, today.drawing) == ("navigate", "open")
   assert switched_off.drawing == "closed"


def test_render_prompt_fills_drawing_only_for_a_template_that_asks_for_it(context, monkeypatch, tmp_path):
   packet, _move = compose_packet(context, {"kind": "today"})
   drawing_template = tmp_path / "live_drawing.md"
   drawing_template.write_text(context_module.LIVE_V1_TEMPLATE_PATH.read_text() + "\nDrawing: {{ drawing }}\n")

   monkeypatch.setattr(context_module, "LIVE_TEMPLATE_PATH", context_module.LIVE_V1_TEMPLATE_PATH)
   without_field = render_prompt(packet, [], None, [], "hello")
   monkeypatch.setattr(context_module, "LIVE_TEMPLATE_PATH", drawing_template)
   with_field = render_prompt(packet, [], None, [], "hello")
   closed = render_prompt(dataclasses.replace(packet, drawing="closed"), [], None, [], "hello")

   assert "Drawing:" not in without_field.user
   assert "Drawing: open" in with_field.user
   assert "Drawing: closed" in closed.user


GRAPH_FIGURE = {
   "kind": "function_graph",
   "domain": [-1, 4],
   "range": [-2, 6],
   "curves": [{"segments": [[[0, 0], [1, 1]]], "style": "solid"}],
   "marks": [{"type": "point", "at": [2, 5]}],
   "labels": [{"text": "LABEL-9d1c", "anchor": [1, 1]}],
   "gridlines": True,
   "axis_titles": ["x", "y"],
   "alt": "A line through the origin.",
}
TABLE_FIGURE = {"kind": "table", "columns": ["x", "f(x)"], "rows": [["0", "1"], ["2", "5"]], "labels": [], "alt": "Two rows."}


@pytest.mark.parametrize(
   "figure_spec, expected",
   [
      (GRAPH_FIGURE, {"kind": "function_graph", "alt": "A line through the origin.", "window": {"x": [-1, 4], "y": [-2, 6]}}),
      (TABLE_FIGURE, {"kind": "table", "alt": "Two rows.", "columns": ["x", "f(x)"], "rows": [["0", "1"], ["2", "5"]]}),
   ],
   ids=["graph", "table"],
)
def test_an_item_figure_reaches_the_packet_as_its_kind_window_alt_and_table_only(context, item, figure_spec, expected):
   with_figure = dict(item, figure_spec=json.dumps(figure_spec))
   packet, _move = compose_packet(context, item_screen(item), item=with_figure)
   plain, _move = compose_packet(context, item_screen(item), item=dict(item, figure_spec=None))

   assert packet.body["figure"] == expected
   assert "LABEL-9d1c" not in json.dumps(packet.body)
   assert "figure" not in plain.body


def history_sent(rendered):
   line = next(line for line in rendered.user.splitlines() if line.startswith("Conversation so far: "))

   return json.loads(line[len("Conversation so far: "):])


def test_a_shown_figure_adds_its_title_and_description_to_the_history_and_nothing_else(context):
   packet, _move = compose_packet(context, {"kind": "today"})
   source = {"kind": "graph", "title": "Secant to tangent", "description": "A secant moves toward P.", "steps": []}
   history = [
      {"role": "agent", "text": "Look at the curve.", "figure": stored_figure("shown", source, 2)},
      {"role": "agent", "text": "Again.", "figure": stored_figure("refused:closed", source)},
      {"role": "student", "text": "Why?", "figure": None},
   ]
   sent = history_sent(render_prompt(packet, [], None, history, "hello"))

   assert [turn["text"] for turn in sent] == [
      "Look at the curve.\n[Figure shown: Secant to tangent. A secant moves toward P.]",
      "Again.",
      "Why?",
   ]


def anchor_ids(packet):
   return [anchor["id"] for anchor in packet.body["anchors"]]


def test_a_practice_item_lists_its_stem_and_graph_and_never_an_option(context, item):
   packet, _move = compose_packet(context, item_screen(item), item=dict(item, figure_spec=json.dumps(GRAPH_FIGURE)))
   texts = {anchor["id"]: anchor.get("text") for anchor in turn_anchors(packet.body)}

   assert packet.body["anchors"] == [
      {"id": "stem", "kind": "text"},
      {"id": "item_figure", "kind": "graph", "window": {"x": [-1, 4], "y": [-2, 6]}},
   ]
   assert texts["stem"] == packet.body["item"]["stem"]


def test_the_anchors_never_name_an_option_before_or_after_checking(context, item):
   """Before checking, ringing an option names an answer; after checking, the session screen shows
   the feedback in place of the item and no options."""
   practice, _move = compose_packet(context, item_screen(item), item=item)
   checked, _move = after_submission_packet(context, item)

   for packet in (practice, checked):
      option_anchors = [anchor_id for anchor_id in anchor_ids(packet) if anchor_id.startswith("option_")]

      assert packet.body["item"]["options"] == ["A", "B", "C", "D"]
      assert option_anchors == []


def test_a_table_item_lists_its_row_and_column_counts(context, item):
   packet, _move = compose_packet(context, item_screen(item), item=dict(item, figure_spec=json.dumps(TABLE_FIGURE)))

   assert packet.body["anchors"][1] == {"id": "item_table", "kind": "table", "rows": 2, "columns": 2}


def checked_packet(context, item, served_stage, chosen_id):
   archetype = context.archetypes[item["archetype_id"]]
   chosen = next(option for option in item["options"] if option["id"] == chosen_id)
   error_path = chosen.get("error_path")
   feedback = render.render_feedback(
      served_stage,
      archetype,
      {"worked_solution": json.dumps(item["worked_solution"])},
      submitted=True,
      correct=chosen["is_key"],
      chosen_option=chosen,
      error_record=context.errors[error_path] if error_path else None,
      confidence="confident",
   )
   attempt = SimpleNamespace(
      submitted_at="2026-09-29T00:00:00+00:00",
      served_stage=served_stage,
      format="mcq",
      correct=int(chosen["is_key"]),
   )
   screen = item_screen(item, submitted=True, served_stage=served_stage, feedback_kind=feedback.kind.value)
   packet, _move = compose_packet(context, screen, item=item, attempt=attempt, feedback=feedback)

   return packet


def test_after_a_wrong_answer_at_the_unsupported_stage_the_feedback_is_an_anchor_and_no_solution_step(context, item):
   """The session screen shows the elaborated panel at the unsupported stage and no worked steps."""
   packet, _move = after_submission_packet(context, item)
   texts = {anchor["id"]: anchor.get("text") for anchor in turn_anchors(packet.body)}

   assert packet.body["feedback"]["worked_solution"] != []
   assert anchor_ids(packet) == ["stem", "feedback"]
   assert packet.body["feedback"]["observed_behavior"] in texts["feedback"]


def test_after_a_right_answer_at_the_unsupported_stage_neither_the_feedback_nor_a_step_is_an_anchor(context, item):
   """A right answer at the unsupported stage has no elaborated panel, and that stage shows no
   worked steps."""
   packet = checked_packet(context, item, "unsupported", "A")

   assert packet.body["feedback"]["kind"] == "correct"
   assert packet.body["feedback"]["worked_solution"] != []
   assert anchor_ids(packet) == ["stem"]


def test_at_a_supported_stage_each_marked_step_is_an_anchor_and_the_feedback_is_not(context, item):
   """Below the unsupported stage the session screen marks every worked step and shows no
   elaborated panel."""
   packet = checked_packet(context, item, "completion", "B")
   steps = packet.body["feedback"]["worked_solution"]
   texts = {anchor["id"]: anchor.get("text") for anchor in turn_anchors(packet.body)}

   assert packet.body["feedback"]["kind"] == "step_verification"
   assert len(steps) == len(item["worked_solution"])
   assert anchor_ids(packet) == ["stem"] + [f"solution_step_{number}" for number in range(1, len(steps) + 1)]
   assert texts["solution_step_1"] == steps[0]


def is_drawn(section):
   delivery = section.get("delivery") or {}
   is_drawn_mode = delivery.get("mode") in ("figure", "table", "motion", "interactive", "model")

   return is_drawn_mode and delivery.get("spec") is not None


def test_a_lesson_section_lists_the_section_and_its_drawn_figure(context):
   lesson = golden.agent_lesson(LESSON_ID)
   drawn = [(index, section) for index, section in enumerate(lesson.body["sections"]) if is_drawn(section)]
   index, section = drawn[0]
   packet, _move = compose_packet(context, lesson_screen_on(lesson, section["id"], index), lesson=lesson)
   texts = {anchor["id"]: anchor.get("text") for anchor in turn_anchors(packet.body)}

   assert packet.mode == "browsing"
   assert anchor_ids(packet) == ["section", "section_figure"]
   assert texts["section"] == packet.body["lesson"]["section"]["text"]


def test_a_lesson_question_anchors_its_section_to_the_question_as_served(context):
   lesson = golden.agent_lesson(PREDICTION_LESSON_ID)
   section = lesson.body["sections"][0]
   packet, _move = compose_packet(context, lesson_screen_on(lesson, section["id"], 0), lesson=lesson)
   texts = {anchor["id"]: anchor.get("text") for anchor in turn_anchors(packet.body)}

   assert packet.mode == "practice"
   assert anchor_ids(packet)[0] == "section"
   assert texts["section"] == section["stem"]["text"]
   assert not any(anchor_id.startswith("option_") for anchor_id in anchor_ids(packet))


def test_a_screen_with_nothing_to_mark_lists_no_anchors(context):
   packet, _move = compose_packet(context, {"kind": "today"})

   assert packet.body["anchors"] == []
