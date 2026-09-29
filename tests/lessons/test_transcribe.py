"""tools/lesson_transcribe.py: a design's machine record becomes a lesson record deterministically,
and the record passes tools/check_lessons.py (docs/lessons/BUILD-PLAN.md, The design to record
path, step 2)."""
import json
from pathlib import Path

import pytest

from app.lessons import plan
from tools import lesson_transcribe
from tools.check_lessons import check_lesson
from tools.lesson_transcribe import TranscriptionError, render, transcribe

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PRODUCT_RULE = REPO_ROOT / "docs" / "lessons" / "unit-02" / "LSN-CON-02013.md"
DECISION = REPO_ROOT / "docs" / "lessons" / "decisions" / "LSN-DEC-06-01.md"
STATEMENT_KEYS = REPO_ROOT / "docs" / "lessons" / "unit-05" / "LSN-CON-05009.md"


@pytest.fixture(scope="module")
def product_rule(snapshot):
   return transcribe(PRODUCT_RULE, snapshot)


def test_the_same_design_gives_the_same_bytes(snapshot, product_rule):
   again = transcribe(PRODUCT_RULE, snapshot)

   assert render(again) == render(product_rule)


def test_sections_follow_the_content_model_order_with_their_anchors(product_rule):
   kinds = [(section["type"], section["id"].split("#")[1]) for section in product_rule["sections"]]

   assert kinds == [
      ("orientation", "s1"),
      ("key_ideas", "s2"),
      ("strategy", "s3"),
      ("strategy", "s4"),
      ("worked_example", "s5"),
      ("worked_example", "s6"),
      ("what_a_reader_scores", "s7"),
      ("what_a_reader_scores", "s8"),
      ("common_error", "err-BC-ERR-02020"),
      ("common_error", "err-BC-ERR-02023"),
      ("common_error", "err-BC-ERR-02024"),
   ]
   assert [check["id"] for check in product_rule["checks"]] == [f"LSN-CON-02013#chk-{n}" for n in (1, 2, 3)]
   assert product_rule["checks"][0]["completes"] == "LSN-CON-02013#s5"


def test_steps_carry_mathjson_and_the_relation_fields(product_rule):
   example = product_rule["sections"][4]
   rule_step = example["steps"][1]

   assert rule_step["relation"] == "new"
   assert rule_step["point_type_id"] == "BC-PT-99022"
   assert rule_step["expression"][0] == "Add"
   assert "expression" not in example["steps"][0]


def test_counts_provenance_and_status(product_rule):
   assert product_rule["status"] == "draft"
   assert product_rule["word_count"] == {
      "full": plan.band_words(product_rule, "low"),
      "brief": plan.band_words(product_rule, "mid"),
   }
   assert product_rule["provenance"] == {
      "author": "tools/lesson_transcribe.py",
      "prompt_version": "generator/lesson_v1",
      "design_path": "docs/lessons/unit-02/LSN-CON-02013.md",
      "signed_off_by": None,
      "signed_off_at": None,
      "not_human": True,
   }


def test_the_transcription_passes_the_record_checker(context, product_rule):
   assert check_lesson(product_rule, context) == {}


def test_a_statement_key_keeps_its_text(snapshot):
   lesson = transcribe(STATEMENT_KEYS, snapshot)

   assert lesson["checks"][0]["answer_key"] == {"form": "statement", "mathjson": "relative_minimum_at_2"}


def test_a_decision_record_builds_its_stems_spec(context, snapshot):
   lesson = transcribe(DECISION, snapshot)
   delivery = lesson["decision"]["delivery"]

   assert delivery["mode"] == "contrast"
   assert delivery["spec"] == {
      "kind": "stems",
      "stems": ["LSN-DEC-06-01#stem-1", "LSN-DEC-06-01#stem-2"],
      "selecting_feature": "task",
   }
   assert delivery["fallback"] and delivery["keyboard"]
   assert lesson["refresher"] == ["LSN-DEC-06-01#s2", "LSN-DEC-06-01#s3"]
   assert check_lesson(lesson, context) == {}


def test_an_expression_the_record_cannot_hold_is_refused_by_field(tmp_path, snapshot):
   text = PRODUCT_RULE.read_text().replace('"expr": "x/2"', '"expr": "Matrix([[1, 2]])"', 1)
   design = tmp_path / "LSN-CON-02013.md"
   design.write_text(text)

   with pytest.raises(TranscriptionError, match=r"err-BC-ERR-02023\.right_step\.expr"):
      transcribe(design, snapshot)


def test_the_command_writes_the_record(tmp_path, capsys):
   output = tmp_path / "LSN-CON-02013.json"

   exit_code = lesson_transcribe.main(["lesson_transcribe.py", str(PRODUCT_RULE), str(output)])

   assert exit_code == 0
   assert json.loads(output.read_text())["id"] == "LSN-CON-02013"
