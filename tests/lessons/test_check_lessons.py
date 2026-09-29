"""tools/check_lessons.py: every lint has a red fixture that fails it, and the hand-authored
lesson passes them all. The fixtures are the hand-authored lesson (or the decision lesson beside
it) with one defect planted, so a lint that stops firing turns its own test red."""
import json
from pathlib import Path

import pytest

from app.lessons.confusable import confusable_sets
from tests.lessons.conftest import FIXTURE_DIR, HAND_AUTHORED, load_fixture
from tools import check_lessons
from tools.check_lessons import Context, check_lesson

RED_FIXTURES = sorted(path.name for path in FIXTURE_DIR.glob("red_*.json"))
PLANTED_DRAW = {"structure": "planted collision", "first_factor": "x", "second_factor": "x"}


def lint_named_by(file_name):
   stem = file_name[len("red_"):-len(".json")]

   return stem.split("__")[0]


def planted_content_dir(tmp_path):
   bank = tmp_path / "items_planted"
   bank.mkdir()
   record = {"id": "ITM-PLANTED-00", "archetype_id": "BC-QA-02008", "parameter_draw": PLANTED_DRAW}
   (bank / "ITM-PLANTED-00.json").write_text(json.dumps(record))

   return tmp_path


def test_every_lint_has_a_red_fixture():
   named = {lint_named_by(name) for name in RED_FIXTURES}

   assert named == set(check_lessons.LINTS)


@pytest.mark.parametrize("file_name", RED_FIXTURES)
def test_red_fixture_fails_its_named_lint(file_name, snapshot, context, tmp_path):
   lint = lint_named_by(file_name)
   needs_a_published_twin = lint == "draw_exclusion"
   lesson = load_fixture(file_name)

   if needs_a_published_twin:
      lesson_context = Context(snapshot, content_dir=planted_content_dir(tmp_path))
   else:
      lesson_context = context

   findings = check_lesson(lesson, lesson_context)

   assert lint in findings, f"{file_name} did not fail {lint}: {sorted(findings)}"


def test_the_planted_twin_is_what_fails_draw_exclusion(snapshot, context, tmp_path):
   lesson = load_fixture("red_draw_exclusion.json")
   without_twin = check_lesson(lesson, context)
   with_twin = check_lesson(lesson, Context(snapshot, content_dir=planted_content_dir(tmp_path)))

   assert "draw_exclusion" not in without_twin
   assert "draw_exclusion" in with_twin


def test_hand_authored_lesson_passes_every_lint(context, hand_authored):
   findings = check_lesson(hand_authored, context)

   assert findings == {}


def test_decision_lesson_control_passes_every_lint(context):
   findings = check_lesson(load_fixture("decision_clean.json"), context)

   assert findings == {}


def test_cli_exits_zero_for_a_clean_directory(tmp_path, capsys):
   (tmp_path / HAND_AUTHORED.name).write_text(HAND_AUTHORED.read_text())

   exit_code = check_lessons.main(["check_lessons.py", str(tmp_path)])
   output = capsys.readouterr().out

   assert exit_code == 0
   assert "lessons read: 1" in output
   assert "with findings: 0" in output


def test_cli_exits_nonzero_when_a_lesson_has_findings(tmp_path, capsys):
   (tmp_path / "red_style.json").write_text((FIXTURE_DIR / "red_style.json").read_text())

   exit_code = check_lessons.main(["check_lessons.py", str(tmp_path)])
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "style:" in output


def test_cli_refuses_an_empty_directory(tmp_path, capsys):
   exit_code = check_lessons.main(["check_lessons.py", str(tmp_path)])

   assert exit_code == 1
   assert "no lesson files were read" in capsys.readouterr().err


def test_sets_mode_prints_the_count(snapshot, capsys):
   exit_code = check_lessons.main(["check_lessons.py", "--sets"])
   output = capsys.readouterr().out
   expected = len(confusable_sets(snapshot))

   assert exit_code == 0
   assert f"confusable sets: {expected}" in output
   assert expected > 0


DELIVERY_FINDINGS = {
   "red_delivery.json": "must be step_reveal",
   "red_delivery__fallback.json": "needs a fallback",
   "red_delivery__reduced_motion.json": "needs a reduced_motion line",
   "red_delivery__placement.json": "places a label",
   "red_delivery__count.json": "at most 2",
   "red_delivery__kind.json": "is not a known spec kind",
}


@pytest.mark.parametrize("file_name", sorted(DELIVERY_FINDINGS))
def test_delivery_fixture_fails_for_its_planted_rule(file_name, context):
   messages = check_lessons.lint_delivery(load_fixture(file_name), context)
   expected = DELIVERY_FINDINGS[file_name]

   assert any(expected in message for message in messages), messages


def test_a_missing_delivery_fails_the_schema(context):
   lesson = load_fixture("red_schema__delivery.json")
   findings = check_lesson(lesson, context)
   lesson["sections"][0]["delivery"] = {"mode": "text", "reason": "restored"}
   restored = check_lessons.lint_schema(lesson, context)

   assert "schema" in findings
   assert any(message.startswith("sections/0") for message in findings["schema"])
   assert restored == []


def test_a_strategy_block_carrying_delivery_fails_the_schema(context, hand_authored):
   strategy = next(section for section in hand_authored["sections"] if section["type"] == "strategy")
   strategy["delivery"] = {"mode": "text", "reason": "planted"}
   findings = check_lesson(hand_authored, context)

   assert "schema" in findings


def test_hand_authored_delivery_matches_its_design(hand_authored):
   modes = [section["delivery"]["mode"] for section in hand_authored["sections"] if "delivery" in section]

   assert modes == ["text", "text", "step_reveal", "step_reveal", "step_reveal", "step_reveal", "step_reveal"]


def test_cli_takes_a_file_path(tmp_path, capsys):
   record = tmp_path / HAND_AUTHORED.name
   record.write_text(HAND_AUTHORED.read_text())

   exit_code = check_lessons.main(["check_lessons.py", str(record)])

   assert exit_code == 0
   assert "lessons read: 1" in capsys.readouterr().out


def test_three_drawn_blocks_are_not_capped_per_lesson(context, hand_authored):
   spec = {"kind": "graph", "curves": [{"expr": "x**2"}], "labels": [{"text": "y", "placement": "inside"}]}

   for section in hand_authored["sections"][:2] + [hand_authored["sections"][2]]:
      if "delivery" in section:
         section["delivery"] = {"mode": "figure", "reason": "planted", "spec": spec, "fallback": "f", "keyboard": "k"}

   assert check_lessons.lint_delivery(hand_authored, context) == []


def example_with_steps(hand_authored, steps):
   example = next(section for section in hand_authored["sections"] if section["type"] == "worked_example")
   example["steps"] = [{"cue": "c", "why": "w", **step} for step in steps]
   example["answer"] = {"form": "symbolic", "mathjson": steps[-1]["expression"]}

   return example


def test_a_differentiate_relation_is_checked_as_a_derivative(context, hand_authored):
   example_with_steps(hand_authored, [
      {"expression": ["Power", "x", 3], "relation": "new"},
      {"expression": ["Multiply", 3, ["Power", "x", 2]], "relation": "differentiate", "variable": "x"},
   ])
   good = check_lessons.lint_step_equivalence(hand_authored, context)
   hand_authored["sections"][4]["steps"][1]["expression"] = ["Multiply", 2, ["Power", "x", 2]]
   bad = check_lessons.lint_step_equivalence(hand_authored, context)

   assert good == []
   assert any("is not the derivative" in message for message in bad)


def test_equation_steps_chain_without_crashing(context, hand_authored):
   example_with_steps(hand_authored, [
      {"expression": ["Equal", ["Add", "k", "m"], 2], "relation": "new"},
      {"expression": ["Equal", "k", ["Add", 2, ["Negate", "m"]]], "relation": "equivalent"},
   ])

   assert check_lessons.lint_step_equivalence(hand_authored, context) == []


def test_error_block_with_equations_compares(context, hand_authored):
   block = next(section for section in hand_authored["sections"] if section["type"] == "common_error")
   block["wrong_step"]["expression"] = ["Equal", ["Add", "k", "m"], 3]
   block["right_step"]["expression"] = ["Equal", ["Add", "k", "m"], 2]
   block["relation"] = "distinct"

   assert check_lessons.relation_messages(block) == []


def test_a_research_citation_is_held_when_its_heading_exists(context, hand_authored):
   good = "research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule"
   bad = "research/units/unit-02-differentiation-definition-properties.md#No Such Heading"
   hand_authored["sections"][0]["sources"] = [good]
   held = check_lessons.unknown_source_messages(hand_authored, context)
   hand_authored["sections"][0]["sources"] = [bad]
   missing = check_lessons.unknown_source_messages(hand_authored, context)

   assert held == []
   assert any("heading is not" in message for message in missing)


def test_a_numeric_key_on_a_no_calculator_check_is_allowed(context, hand_authored):
   check = hand_authored["checks"][2]
   check["answer_key"]["form"] = "numeric"
   check["calculator_status"] = "no_calculator"

   assert check_lessons.lint_calculator_boundary(hand_authored, context) == []
