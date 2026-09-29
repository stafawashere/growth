"""Moves a lesson record to signed_off when its sign-off evidence allows it (docs/plan/15-lessons.md,
Sourcing, Pipeline step 4, and docs/operator/lessons.md, The sign-off evidence file).

A record is signed off only when all of these hold:

- tools/check_lessons.py finds nothing in it;
- docs/operator/lesson-audit/<id>.json exists for the record's version, written by
  tools/lesson_resolve_compare.py after the record compared equal to its design;
- the evidence's resolve block agrees on every problem, has no pending judgment, and holds an
  agreeing verdict for every worked example and check of the record (invariant L9);
- the evidence's audit block counts zero unsourced, wrong, over_cap and lint blocks, and every
  block's verdict is ok.

The record's status becomes signed_off and its provenance names the auditor and the date. A record
that fails any condition is left as it is and the reasons are printed.

Usage: python3 tools/lesson_sign_off.py <record.json> [<record.json> ...]
"""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.content.loader import load_snapshot
from tools import check_lessons

AUDIT_DIR = ROOT / "docs" / "operator" / "lesson-audit"
FAILING_COUNTS = ("unsourced", "wrong", "over_cap", "lint")
SIGNED_OFF = "signed_off"


def solved_ids(record):
   examples = [section for section in record["sections"] if section["type"] == "worked_example"]
   example_ids = [f"{record['id']}#ex-{index + 1}" for index in range(len(examples))]
   check_ids = [check["id"] for check in record.get("checks") or []]

   return example_ids + check_ids


def resolve_problems(record, resolve):
   if resolve is None:
      return ["the evidence holds no resolve block"]

   problems = []
   is_agreed = resolve.get("all_agree") is True
   has_pending = (resolve.get("judgments_pending") or 0) > 0

   if not is_agreed:
      problems.append("the blind re-solve does not agree on every problem")

   if has_pending:
      problems.append("the blind re-solve has pending judgments")

   agreed = {verdict["id"] for verdict in resolve.get("verdicts") or [] if verdict.get("agree") is True}
   unresolved = [solved_id for solved_id in solved_ids(record) if solved_id not in agreed]

   if unresolved:
      problems.append(f"no agreeing re-solve verdict for {', '.join(unresolved)}")

   return problems


def audit_problems(audit):
   if audit is None:
      return ["the evidence holds no audit block"]

   problems = []
   counts = audit.get("counts") or {}

   for name in FAILING_COUNTS:
      count = counts.get(name, 0)

      if count != 0:
         problems.append(f"the audit counts {count} {name}")

   not_ok = [block.get("id") for block in audit.get("blocks") or [] if block.get("verdict") != "ok"]

   if not_ok:
      problems.append(f"audit blocks not ok: {', '.join(str(block_id) for block_id in not_ok)}")

   has_no_blocks = len(audit.get("blocks") or []) == 0

   if has_no_blocks:
      problems.append("the audit records no blocks")

   return problems


def evidence_problems(record, audit_dir):
   path = Path(audit_dir) / f"{record['id']}.json"

   if not path.is_file():
      return [f"no sign-off evidence at {path}"], None

   evidence = json.loads(path.read_text())
   is_other_version = evidence.get("version") != record["version"]

   if is_other_version:
      return [f"the evidence is for version {evidence.get('version')}, the record is {record['version']}"], evidence

   problems = resolve_problems(record, evidence.get("resolve")) + audit_problems(evidence.get("audit"))

   return problems, evidence


def sign_off(path, context, audit_dir, today):
   record = json.loads(Path(path).read_text())
   findings = check_lessons.check_lesson(record, context)
   problems = [f"check_lessons {name}: {messages[0]}" for name, messages in findings.items()]
   found, evidence = evidence_problems(record, audit_dir)
   problems.extend(found)

   if problems:
      return problems

   record["status"] = SIGNED_OFF
   record["provenance"]["signed_off_by"] = evidence["auditor"]
   record["provenance"]["signed_off_at"] = today.isoformat()
   Path(path).write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")

   return []


def main(argv, audit_dir=AUDIT_DIR, today=None):
   paths = argv[1:]

   if not paths:
      print("usage: python3 tools/lesson_sign_off.py <record.json> [...]", file=sys.stderr)

      return 1

   context = check_lessons.Context(load_snapshot(check_lessons.DATA_ROOT))
   refused = 0

   for path in paths:
      problems = sign_off(path, context, audit_dir, today or date.today())

      if problems:
         refused += 1
         print(f"REFUSED {path}")

         for problem in problems:
            print(f"  {problem}")

         continue

      print(f"SIGNED_OFF {path}")

   print()
   print(f"records: {len(paths)}")
   print(f"signed off: {len(paths) - refused}")
   print(f"refused: {refused}")

   return 0 if refused == 0 else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))