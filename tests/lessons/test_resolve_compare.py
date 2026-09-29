"""tools/lesson_resolve_compare.py: a record inherits its design's blind re-solve and audit only
when its stems, keys and served text equal the design's (docs/lessons/BUILD-PLAN.md, The design to
record path, steps 3 and 4). The equal record is LSN-CON-02013 transcribed from its design; the
mutated copies change one key and one stem."""
import json
from datetime import date

import pytest

from tests.lessons.conftest import FIXTURE_DIR, REPO_ROOT
from tools import lesson_resolve_compare

DESIGN = REPO_ROOT / "docs" / "lessons" / "unit-02" / "LSN-CON-02013.md"
TRANSCRIBED = FIXTURE_DIR / "resolve" / "LSN-CON-02013.json"
COMPARED_ON = date(2026, 9, 29)
CHANGED_KEY = ["Add", ["Multiply", 5, ["Power", "x", 4]], -3]


def transcribed():
   return json.loads(TRANSCRIBED.read_text())


def run(tmp_path, record, verification=None):
   record_path = tmp_path / "record.json"
   record_path.write_text(json.dumps(record))
   verification_dir = tmp_path / "verification"
   verification_dir.mkdir()

   if verification is not None:
      (verification_dir / f"{record['id']}.json").write_text(json.dumps(verification))

   audit_dir = tmp_path / "lesson-audit"
   exit_code = lesson_resolve_compare.main(
      ["lesson_resolve_compare.py", str(record_path), str(DESIGN)],
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
