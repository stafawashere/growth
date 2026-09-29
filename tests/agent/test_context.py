"""docs/agent/architecture.md, The screen context and The context composer.

Before submission the packet is built from an allow-list, so the proof is a grep over the whole
rendered prompt, prefix and variable section, for every form of the item's key, every option value,
every worked solution step and every error or misconception id. After submission the packet carries
the elaborated payload, exactly one error id and one scoring point. A browsing screen carries the
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

from app.agent.context import (
   TimedPartRefused,
   compose_packet,
   render_prompt,
   screen_line,
   validate_screen,
)
from app.content.loader import load_snapshot
from app.evals import agent_checks, golden
from app.feedback import render
from app.items.mathjson import to_sympy
from app.runtime.context import DEFAULT_CONTENT_ROOT

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DESIGN_PATH = REPOSITORY_ROOT / "docs" / "agent" / "design.md"
ITEM_PATH = REPOSITORY_ROOT / "content" / "items_unit06_agent" / "ITM-AGT-06002-00.json"
LESSON_ID = "LSN-CON-06003"
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


def test_after_submission_the_packet_carries_the_elaborated_fields_one_error_and_one_point(context, item):
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
   assert point_ids == {"BC-PT-99018"}
   assert set(feedback["point"]) == {"id", "name", "earns", "does_not_earn"}
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
