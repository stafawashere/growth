"""Ingestion of lesson records, on app/items/ingest.py (docs/plan/15-lessons.md, Storage and
versioning through content snapshots; docs/lessons/BUILD-PLAN.md Slice L1).

Every content/lessons/*.json is validated and linted by tools/check_lessons.py check_lesson, and
one lesson_verifications row is written per lint with its outcome, so an operator can read why a
record is not served. The row's status is the record's own status, with three exceptions that
keep invariants L8 and L9 true of whatever the repository calls servable:

- stale, when the record's source_digest differs from the authoring bundle's current digest or a
  BC-* id it cites is not active in the snapshot (15, Storage and versioning). The audit action
  lesson_stale is written the first time a version goes stale.
- draft, when any lint finds something: a record that fails the checker has not passed BUILD-PLAN's
  step 2, whatever status it claims.
- draft, when docs/lessons/verification/<id>.json exists and a worked example or check lacks an
  agreeing verdict in its resolve block (L9, the blind re-solve half).

A record that fails the schema is not stored at all, since its fields cannot be trusted to fill a
row; its verification rows are written so the refusal is on record. lesson_signed_off is written
when a version is first stored, or moves, at signed_off.

Ingest is repeatable: a version already stored is rewritten in place and its verification rows
replaced, because a lesson record, unlike an item, may be edited under the same version while it
is a draft.
"""
import json
import os
import re
import uuid
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import delete

from app.auth.service import write_audit
from app.db import models
from app.lessons.source import authoring_bundle

ROOT = Path(__file__).resolve().parents[2]
VERIFICATION_DIR = ROOT / "docs" / "lessons" / "verification"
LESSONS_DIR = ROOT / "content" / "lessons"

PASS = "pass"
FAIL = "fail"
DRAFT = "draft"
STALE = "stale"
SIGNED_OFF = "signed_off"
RESOLVE_CHECK = "resolve"
STALE_CHECK = "stale"
SCHEMA_LINT = "schema"
PARALLEL_LINT_MIN_RECORDS = 16
PARALLEL_LINT_WORKERS_MAX = 8
ACTOR = "system"
KIND_CODES = {"concept": "con", "prerequisite": "prq", "decision": "dec"}
SECTION_ID = re.compile(r"LSN-[A-Z]+-[0-9-]+#[A-Za-z0-9-]+")
BC_ID = re.compile(r"\bBC-[A-Z]{2,4}-[A-Z0-9]{2,}(?:-[A-Z0-9]+)*\b")


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def default_context(snapshot):
   from tools.check_lessons import Context

   return Context(snapshot)


def lint_record(record, context):
   from tools.check_lessons import LINTS, check_lesson

   findings = check_lesson(record, context)
   fails_schema = SCHEMA_LINT in findings

   if fails_schema:
      return {SCHEMA_LINT: findings[SCHEMA_LINT]}, (SCHEMA_LINT,)

   return findings, tuple(LINTS)


def inactive_ids(record, snapshot):
   cited = sorted(set(BC_ID.findall(json.dumps(record))))
   inactive = []

   for identifier in cited:
      entry = snapshot.ids.get(identifier)
      is_active = entry is not None and entry.get("status") == "active"

      if not is_active:
         inactive.append(identifier)

   return inactive


def digest_moved(record, snapshot, context):
   is_concept = record["kind"] == "concept"

   if not is_concept:
      return False

   target = record["target_id"]
   target_is_known = target in snapshot.concepts

   if not target_is_known:
      return True

   has_context = context is not None

   if has_context:
      current = context.bundle(target)["source_digest"]
   else:
      current = authoring_bundle(target, snapshot)["source_digest"]

   return record["source_digest"] != current


def stale_reasons(record, snapshot, context=None):
   reasons = []

   if digest_moved(record, snapshot, context):
      reasons.append("source_digest differs from the authoring bundle's current digest")

   for identifier in inactive_ids(record, snapshot):
      reasons.append(f"{identifier} is not active in the snapshot")

   return reasons


def solved_records(record):
   examples = [section for section in record["sections"] if section["type"] == "worked_example"]

   return examples, list(record.get("checks") or [])


def design_block_ids(record):
   """Record section id to the design's block id, the ids the resolve verdicts carry: worked
   examples are ex-1, ex-2 in order and checks keep their chk-n suffix."""
   examples, checks = solved_records(record)
   mapping = {}

   for index, example in enumerate(examples, start=1):
      mapping[example["id"]] = f"{record['id']}#ex-{index}"

   for check in checks:
      mapping[check["id"]] = check["id"]

   return mapping


def resolve_messages(record, verification_dir):
   """L9, the blind re-solve half: every worked example and check has an agreeing verdict, when
   the design's verification file exists (BUILD-PLAN, design to record path, step 3)."""
   path = Path(verification_dir) / f"{record['id']}.json"

   if not path.is_file():
      return None

   resolve = json.loads(path.read_text()).get("resolve") or {}
   agreed = {verdict["id"] for verdict in resolve.get("verdicts") or [] if verdict.get("agree") is True}
   messages = []

   for section_id, design_id in design_block_ids(record).items():
      has_agreeing_verdict = design_id in agreed

      if not has_agreeing_verdict:
         messages.append(f"{section_id} has no agreeing blind re-solve verdict ({design_id})")

   return messages


def verification_rows(record, check_type, messages, now):
   version = record.get("version") or 0
   lesson_id = record.get("id") or "unknown"

   if not messages:
      return [models.LessonVerification(
         id=new_id("LVR"),
         lesson_id=lesson_id,
         version=version,
         section_id=None,
         check_type=check_type,
         outcome=PASS,
         detail=None,
         created_at=now,
         updated_at=now,
      )]

   rows = []

   for message in messages:
      named = SECTION_ID.search(message)
      rows.append(models.LessonVerification(
         id=new_id("LVR"),
         lesson_id=lesson_id,
         version=version,
         section_id=named.group(0) if named else None,
         check_type=check_type,
         outcome=FAIL,
         detail=message,
         created_at=now,
         updated_at=now,
      ))

   return rows


def row_status(record, findings, stale, resolve_failures):
   if stale:
      return STALE

   has_findings = len(findings) > 0
   lacks_resolve = resolve_failures is not None and len(resolve_failures) > 0

   if has_findings or lacks_resolve:
      return DRAFT

   return record["status"]


def replace_verifications(db, record, rows):
   db.execute(
      delete(models.LessonVerification)
      .where(models.LessonVerification.lesson_id == record.get("id"))
      .where(models.LessonVerification.version == (record.get("version") or 0))
   )

   for row in rows:
      db.add(row)


def store_lesson(db, record, status, snapshot_id, now):
   existing = db.get(models.Lesson, (record["id"], record["version"]))
   previous_status = existing.status if existing is not None else None
   fields = {
      "kind": KIND_CODES[record["kind"]],
      "target_id": record["target_id"],
      "snapshot_id": snapshot_id,
      "body": record,
      "read_minutes_full": record["read_minutes"]["full"],
      "read_minutes_brief": record["read_minutes"]["brief"],
      "status": status,
      "provenance": record["provenance"],
      "source_digest": record["source_digest"],
      "updated_at": now,
   }

   if existing is None:
      db.add(models.Lesson(id=record["id"], version=record["version"], created_at=now, **fields))
   else:
      for name, value in fields.items():
         setattr(existing, name, value)

   return previous_status


def write_transition_audit(db, record, status, previous_status, reasons, now_moment):
   subject = f"lessons:{record['id']}@{record['version']}"
   became_stale = status == STALE and previous_status != STALE
   became_signed_off = status == SIGNED_OFF and previous_status != SIGNED_OFF

   if became_stale:
      write_audit(db, ACTOR, "lesson_stale", subject, {"reasons": reasons}, now=now_moment)

   if became_signed_off:
      write_audit(db, ACTOR, "lesson_signed_off", subject, {"snapshot_digest": record["snapshot_digest"]}, now=now_moment)


def ingest_lesson(db, record, snapshot, snapshot_id, context, now_moment, verification_dir=VERIFICATION_DIR, linted=None):
   now = now_moment.isoformat()
   findings, lints_run = linted if linted is not None else lint_record(record, context)
   fails_schema = SCHEMA_LINT in findings
   rows = []

   for name in lints_run:
      rows.extend(verification_rows(record, name, findings.get(name, []), now))

   if fails_schema:
      replace_verifications(db, record, rows)
      db.flush()

      return {"lesson_id": record.get("id"), "version": record.get("version"), "status": None, "findings": findings}

   reasons = stale_reasons(record, snapshot, context)
   is_stale = len(reasons) > 0
   resolve_failures = resolve_messages(record, verification_dir)
   rows.extend(verification_rows(record, STALE_CHECK, reasons, now))

   if resolve_failures is not None:
      rows.extend(verification_rows(record, RESOLVE_CHECK, resolve_failures, now))

   status = row_status(record, findings, is_stale, resolve_failures)
   previous_status = store_lesson(db, record, status, snapshot_id, now)
   replace_verifications(db, record, rows)
   write_transition_audit(db, record, status, previous_status, reasons, now_moment)
   db.flush()

   return {"lesson_id": record["id"], "version": record["version"], "status": status, "findings": findings}


_worker_context = None


def start_lint_worker(snapshot):
   global _worker_context
   _worker_context = default_context(snapshot)


def lint_in_worker(record):
   return lint_record(record, _worker_context)


def lint_records(records, snapshot, context):
   """Every record's lints, in record order. The lints are CAS work of about half a second a record,
   so a directory of PARALLEL_LINT_MIN_RECORDS or more is linted across a process pool, each worker
   holding one checker context; the findings are the same either way, and every database write
   stays in this process. A caller that passes its own context keeps the serial path."""
   is_large = len(records) >= PARALLEL_LINT_MIN_RECORDS
   uses_default_context = context is None
   runs_in_pool = is_large and uses_default_context

   if not runs_in_pool:
      lesson_context = context if context is not None else default_context(snapshot)

      return [lint_record(record, lesson_context) for record in records]

   workers = min(PARALLEL_LINT_WORKERS_MAX, os.cpu_count() or 1)

   with ProcessPoolExecutor(max_workers=workers, initializer=start_lint_worker, initargs=(snapshot,)) as pool:
      return list(pool.map(lint_in_worker, records, chunksize=4))


def ingest_lessons(db, directory, snapshot, snapshot_id, now=None, context=None, verification_dir=VERIFICATION_DIR):
   """Ingests every *.json in directory and returns one result per record, in file name order.
   The caller commits."""
   now_moment = now or datetime.now(timezone.utc)
   lesson_context = context if context is not None else default_context(snapshot)
   paths = sorted(path for path in Path(directory).iterdir() if path.suffix == ".json")
   records = [json.loads(path.read_text()) for path in paths]
   linted = lint_records(records, snapshot, context)

   return [
      ingest_lesson(db, record, snapshot, snapshot_id, lesson_context, now_moment, verification_dir, linted=result)
      for record, result in zip(records, linted)
   ]
