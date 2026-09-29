"""tools/lesson_transcribe.py: a design's machine record becomes a lesson record deterministically,
and the record passes tools/check_lessons.py (docs/lessons/BUILD-PLAN.md, The design to record
path, step 2)."""
import json
import re
from pathlib import Path

import pytest

from app.lessons import plan
from tools import lesson_transcribe
from tools.check_lessons import check_lesson
from tools.lesson_transcribe import TranscriptionError, render, transcribe

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CLEAN_DESIGNS = REPO_ROOT / "tests" / "fixtures" / "lesson_designs" / "clean"
PRODUCT_RULE = CLEAN_DESIGNS / "LSN-CON-02013.md"
DECISION = CLEAN_DESIGNS / "LSN-DEC-06-01.md"
PRODUCT_RULE_LIBRARY_PATH = "docs/lessons/unit-02/LSN-CON-02013.md"
DECISION_LIBRARY_PATH = "docs/lessons/decisions/LSN-DEC-06-01.md"
STATEMENT_KEYS = REPO_ROOT / "docs" / "lessons" / "unit-05" / "LSN-CON-05009.md"


@pytest.fixture(scope="module")
def product_rule(snapshot):
   return transcribe(PRODUCT_RULE, snapshot, PRODUCT_RULE_LIBRARY_PATH)


def test_the_same_design_gives_the_same_bytes(snapshot, product_rule):
   again = transcribe(PRODUCT_RULE, snapshot, PRODUCT_RULE_LIBRARY_PATH)

   assert render(again) == render(product_rule)


def test_sections_follow_the_content_model_order_with_their_anchors(product_rule):
   kinds = [(section["type"], section["id"].split("#")[1]) for section in product_rule["sections"]]

   assert kinds == [
      ("prediction", "s1"),
      ("orientation", "s2"),
      ("key_ideas", "s3"),
      ("strategy", "s4"),
      ("strategy", "s5"),
      ("worked_example", "s6"),
      ("worked_example", "s7"),
      ("what_a_reader_scores", "s8"),
      ("what_a_reader_scores", "s9"),
      ("common_error", "err-BC-ERR-02020"),
      ("common_error", "err-BC-ERR-02023"),
      ("common_error", "err-BC-ERR-02024"),
   ]
   assert [check["id"] for check in product_rule["checks"]] == [f"LSN-CON-02013#chk-{n}" for n in (1, 2, 3)]
   assert product_rule["checks"][0]["completes"] == "LSN-CON-02013#s6"


def test_steps_carry_mathjson_and_the_relation_fields(product_rule):
   example = product_rule["sections"][5]
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
      "prompt_version": "generator/lesson_v2",
      "design_path": "docs/lessons/unit-02/LSN-CON-02013.md",
      "signed_off_by": None,
      "signed_off_at": None,
      "not_human": True,
   }


def test_the_transcription_passes_the_record_checker(context, product_rule):
   assert check_lesson(product_rule, context) == {}


def test_the_prediction_is_the_first_section_with_its_fields(product_rule):
   prediction = product_rule["sections"][0]

   assert prediction["type"] == "prediction"
   assert prediction["bands"] == ["low", "mid"]
   assert prediction["skills"] == product_rule["sections"][1]["skills"]
   assert prediction["sources"] == ["BC-CON-02013", "BC-ERR-02020"]
   assert prediction["evidence_tag"] == "inferred"
   assert prediction["stem"]["command_verb"] == "predict"
   assert prediction["stem"]["text"].startswith("Let \\(h(x)=(x^2+3)\\cos x\\)")
   assert prediction["format"] == "mcq"
   assert [(option["id"], option["is_key"]) for option in prediction["options"]] == [("A", False), ("B", True), ("C", False)]
   assert prediction["resolution"]["text"].startswith("The rule keeps two terms")
   assert prediction["delivery"] == {"mode": "text", "reason": "rule 6"}


def test_an_option_expression_becomes_its_mathjson_value(tmp_path, snapshot):
   text = PRODUCT_RULE.read_text().replace('"is_key": false}\n  ],', '"is_key": false, "expr": "2*x*cos(x)"}\n  ],', 1)
   design = tmp_path / "LSN-CON-02013.md"
   design.write_text(text)

   options = transcribe(design, snapshot)["sections"][0]["options"]

   assert options[2]["value"] == ["Multiply", 2, "x", ["Cos", "x"]]
   assert "value" not in options[0]


def test_a_short_answer_prediction_carries_its_key(tmp_path, snapshot):
   text = re.sub(
      r'"format": "mcq",\s*"options": \[.*?\],',
      '"format": "short_answer", "key": {"form": "symbolic", "expr": "2*x*cos(x)"},',
      PRODUCT_RULE.read_text(),
      count=1,
      flags=re.DOTALL,
   )
   design = tmp_path / "LSN-CON-02013.md"
   design.write_text(text)

   prediction = transcribe(design, snapshot)["sections"][0]

   assert prediction["format"] == "short_answer"
   assert prediction["answer_key"] == {"form": "symbolic", "mathjson": ["Multiply", 2, "x", ["Cos", "x"]]}
   assert "options" not in prediction


def test_contrast_fade_fix_prompt_and_no_figure_reason_are_carried(product_rule):
   strategies = [section for section in product_rule["sections"] if section["type"] == "strategy"]
   examples = [section for section in product_rule["sections"] if section["type"] == "worked_example"]
   errors = [section for section in product_rule["sections"] if section["type"] == "common_error"]

   assert strategies[0]["contrast"] == {
      "this": {"text": "Let \\(h(x)=x^3\\sin x\\). Find \\(h'(x)\\).", "archetype_id": "BC-QA-02008"},
      "not_this": {"text": "Let \\(h(x)=\\sin(x^3)\\). Find \\(h'(x)\\).", "why_not": "The cube sits inside the sine, so the chain rule applies."},
      "feature": "Two factors multiplied, not one function inside another.",
   }
   assert "contrast" not in strategies[1]
   assert "fade_from" not in examples[0]
   assert examples[1]["fade_from"] == 3
   assert [(section["error_id"], section["fix_prompt"]) for section in errors] == [
      ("BC-ERR-02020", True),
      ("BC-ERR-02023", False),
      ("BC-ERR-02024", True),
   ]
   assert product_rule["no_figure_reason"].startswith("The concept is a symbolic rule")


def test_a_concept_error_block_without_fix_prompt_is_refused_by_field(tmp_path, snapshot):
   text = PRODUCT_RULE.read_text()
   design = tmp_path / "LSN-CON-02013.md"
   design.write_text(text.replace('"fix_prompt": false,', "", 1))

   with pytest.raises(TranscriptionError, match=r"err-BC-ERR-02023\.fix_prompt is missing"):
      transcribe(design, snapshot)


def test_a_prediction_field_the_record_cannot_hold_is_refused_by_field(tmp_path, snapshot):
   text = PRODUCT_RULE.read_text().replace('"id": "pr-1",', '"id": "pr-1", "hint": "Think of two factors.",', 1)
   design = tmp_path / "LSN-CON-02013.md"
   design.write_text(text)

   with pytest.raises(TranscriptionError, match=r"prediction\.hint is a field the record cannot express"):
      transcribe(design, snapshot)


def test_a_statement_key_keeps_its_text(tmp_path, snapshot):
   # The library design predates fix_prompt; every one of its error blocks is distinct.
   design = tmp_path / "LSN-CON-05009.md"
   design.write_text(STATEMENT_KEYS.read_text().replace('   "relation": "distinct",', '   "relation": "distinct", "fix_prompt": true,'))
   lesson = transcribe(design, snapshot)

   assert lesson["checks"][0]["answer_key"] == {"form": "statement", "mathjson": "relative_minimum_at_2"}


def test_a_decision_record_builds_its_stems_spec(context, snapshot):
   lesson = transcribe(DECISION, snapshot, DECISION_LIBRARY_PATH)
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
