"""tools/lesson_sign_off.py: a record reaches signed_off only on evidence of a full agreeing re-solve
and an audit with no non-ok block (docs/plan/15-lessons.md, Pipeline step 4; invariant L9). The
record is LSN-CON-02013 transcribed from its design, with its design's verification copied as the
evidence file."""
import copy
import json
from datetime import date

from tests.lessons.conftest import FIXTURE_DIR, REPO_ROOT
from tools import lesson_sign_off

TRANSCRIBED = FIXTURE_DIR / "resolve" / "LSN-CON-02013.json"
VERIFICATION = REPO_ROOT / "docs" / "lessons" / "verification" / "LSN-CON-02013.json"
SIGNED_ON = date(2026, 9, 29)


def evidence():
   verification = json.loads(VERIFICATION.read_text())

   return {
      "lesson_id": "LSN-CON-02013",
      "version": 1,
      "compared_on": "2026-09-29",
      "auditor": "claude-opus-5-5",
      "resolve": verification["resolve"],
      "audit": verification["audit"],
   }


def sign(tmp_path, context, evidence_body):
   record_path = tmp_path / "LSN-CON-02013.json"
   record_path.write_text(TRANSCRIBED.read_text())
   audit_dir = tmp_path / "lesson-audit"
   audit_dir.mkdir()

   if evidence_body is not None:
      (audit_dir / "LSN-CON-02013.json").write_text(json.dumps(evidence_body))

   problems = lesson_sign_off.sign_off(record_path, context, audit_dir, SIGNED_ON)

   return problems, json.loads(record_path.read_text())


def test_full_evidence_signs_the_record_off(tmp_path, context):
   problems, record = sign(tmp_path, context, evidence())

   assert problems == []
   assert record["status"] == "signed_off"
   assert record["provenance"]["signed_off_by"] == "claude-opus-5-5"
   assert record["provenance"]["signed_off_at"] == "2026-09-29"


def test_a_wrong_audit_block_refuses(tmp_path, context):
   body = evidence()
   body["audit"] = copy.deepcopy(body["audit"])
   body["audit"]["blocks"][0]["verdict"] = "wrong"
   body["audit"]["counts"]["wrong"] = 1
   problems, record = sign(tmp_path, context, body)

   assert "the audit counts 1 wrong" in problems
   assert record["status"] == "draft"


def test_a_check_without_an_agreeing_verdict_refuses(tmp_path, context):
   body = evidence()
   body["resolve"] = copy.deepcopy(body["resolve"])
   body["resolve"]["verdicts"] = [verdict for verdict in body["resolve"]["verdicts"] if verdict["id"] != "LSN-CON-02013#chk-3"]
   problems, record = sign(tmp_path, context, body)

   assert "no agreeing re-solve verdict for LSN-CON-02013#chk-3" in problems
   assert record["status"] == "draft"


def test_no_evidence_refuses(tmp_path, context):
   problems, record = sign(tmp_path, context, None)

   assert problems[0].startswith("no sign-off evidence")
   assert record["status"] == "draft"