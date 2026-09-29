"""tools/lesson_resolve_compare.py: a record inherits its design's blind re-solve and audit only
when its stems, keys and served text equal the design's (docs/lessons/BUILD-PLAN.md, The design to
record path, steps 3 and 4). The equal record is LSN-CON-02013 transcribed from its design; the
mutated copies change one key and one stem."""
import json
import re
from datetime import date

import pytest

from tests.lessons.conftest import FIXTURE_DIR, REPO_ROOT
from tools import lesson_resolve_compare
from tools.lesson_transcribe import transcribe

DESIGN = REPO_ROOT / "tests" / "fixtures" / "lesson_designs" / "clean" / "LSN-CON-02013.md"
TRANSCRIBED = FIXTURE_DIR / "resolve" / "LSN-CON-02013.json"
COMPARED_ON = date(2026, 9, 29)
CHANGED_KEY = ["Add", ["Multiply", 5, ["Power", "x", 4]], -3]


def transcribed():
   return json.loads(TRANSCRIBED.read_text())


def run(tmp_path, record, verification=None, design=DESIGN):
   record_path = tmp_path / "record.json"
   record_path.write_text(json.dumps(record))
   verification_dir = tmp_path / "verification"
   verification_dir.mkdir()

   if verification is not None:
      (verification_dir / f"{record['id']}.json").write_text(json.dumps(verification))

   audit_dir = tmp_path / "lesson-audit"
   exit_code = lesson_resolve_compare.main(
      ["lesson_resolve_compare.py", str(record_path), str(design)],
      verification_dir=verification_dir,
      audit_dir=audit_dir,
      today=COMPARED_ON,
   )

   return exit_code, audit_dir / f"{record['id']}.json"


def test_the_transcribed_record_equals_its_design(tmp_path, capsys):
   exit_code, evidence = run(tmp_path, transcribed())
   output = capsys.readouterr().out

   assert exit_code == 0
   assert "differing: 0" in output
   assert "DIFFERS" not in output
   assert not evidence.exists()


def test_a_changed_key_differs(tmp_path, capsys):
   record = transcribed()
   record["checks"][1]["answer_key"]["mathjson"] = CHANGED_KEY
   exit_code, evidence = run(tmp_path, record, verification={"resolve": {"all_agree": True}})
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS check 2 key" in output
   assert not evidence.exists()


def test_a_changed_stem_differs(tmp_path, capsys):
   record = transcribed()
   record["checks"][0]["stem"]["text"] = record["checks"][0]["stem"]["text"] + " Show the work."
   exit_code, _ = run(tmp_path, record)
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS check 1 stem" in output


def test_whitespace_alone_is_not_a_difference(tmp_path):
   record = transcribed()
   record["checks"][0]["stem"]["text"] = "  " + record["checks"][0]["stem"]["text"].replace(" ", "   ")
   exit_code, _ = run(tmp_path, record)

   assert exit_code == 0


def test_an_equal_record_copies_its_design_evidence(tmp_path):
   verification = {"resolve": {"all_agree": True, "verdicts": []}, "audit": {"errors": 0}}
   exit_code, evidence = run(tmp_path, transcribed(), verification=verification)
   written = json.loads(evidence.read_text())

   assert exit_code == 0
   assert written == {
      "lesson_id": "LSN-CON-02013",
      "version": 1,
      "compared_on": "2026-09-29",
      "auditor": lesson_resolve_compare.AUDITOR,
      "resolve": verification["resolve"],
      "audit": verification["audit"],
   }


@pytest.mark.parametrize("argv", [["tool"], ["tool", "a.json"]])
def test_usage_is_refused(argv, capsys):
   assert lesson_resolve_compare.main(argv) == 2


def test_a_changed_distractor_differs(tmp_path, capsys):
   record = transcribed()
   record["checks"][2]["options"][0]["value"] = 9
   exit_code, _ = run(tmp_path, record)
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS check 3 option 1 value" in output


def section_of(record, section_type, position=0):
   return [section for section in record["sections"] if section["type"] == section_type][position]


def test_a_moved_prediction_key_differs(tmp_path, capsys):
   record = transcribed()
   options = section_of(record, "prediction")["options"]
   options[0]["is_key"] = True
   options[1]["is_key"] = False
   exit_code, _ = run(tmp_path, record)
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS prediction option 1" in output
   assert "DIFFERS prediction option 2" in output


def test_a_changed_short_answer_prediction_key_differs(tmp_path, capsys, snapshot):
   design = tmp_path / "LSN-CON-02013.md"
   design.write_text(re.sub(
      r'"format": "mcq",\s*"options": \[.*?\],',
      '"format": "short_answer", "key": {"form": "symbolic", "expr": "2*x*cos(x)"},',
      DESIGN.read_text(),
      count=1,
      flags=re.DOTALL,
   ))
   record = transcribe(design, snapshot)
   (tmp_path / "equal").mkdir()
   (tmp_path / "changed").mkdir()
   equal_exit, _ = run(tmp_path / "equal", record, design=design)
   section_of(record, "prediction")["answer_key"]["mathjson"] = ["Multiply", 2, ["Cos", "x"]]
   changed_exit, _ = run(tmp_path / "changed", record, design=design)
   output = capsys.readouterr().out

   assert equal_exit == 0
   assert changed_exit == 1
   assert "DIFFERS prediction key" in output


def test_a_changed_contrast_text_differs(tmp_path, capsys):
   record = transcribed()
   section_of(record, "strategy")["contrast"]["not_this"]["why_not"] = "The sine is applied last."
   exit_code, _ = run(tmp_path, record)
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS strategy 1 contrast why_not" in output


def test_a_changed_fade_from_differs(tmp_path, capsys):
   record = transcribed()
   section_of(record, "worked_example", 1)["fade_from"] = 2
   exit_code, _ = run(tmp_path, record)
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS worked_example 2 fade_from" in output


def test_a_flipped_fix_prompt_differs(tmp_path, capsys):
   record = transcribed()
   section_of(record, "common_error", 1)["fix_prompt"] = True
   exit_code, _ = run(tmp_path, record)
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "DIFFERS error BC-ERR-02023 fix_prompt" in output
