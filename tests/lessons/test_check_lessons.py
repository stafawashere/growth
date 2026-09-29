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
