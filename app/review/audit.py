"""The item_audit writer and the key error rate of eval 29 in docs/plan/11-phased-delivery.md.

item_audit is the operator's hand-audit verdict on a published item and is the only review_queue
kind P1 writes (docs/plan/06-architecture.md, review_queue). A key error is an item whose stated
key is mathematically wrong or whose stem the operator judged ambiguous enough to admit a second
correct answer, and the ambiguous verdict carries that second answer so the judgement stays
auditable. No pass threshold is set in P1: what is checked is that every verdict exists over the
audited sample and that the rate is published.
"""
import json
import uuid

from sqlalchemy import select

from app.db import models

KIND = "item_audit"

VERDICT_KEY_WRONG = "key_wrong"
VERDICT_AMBIGUOUS = "ambiguous"
VERDICT_CLEAN = "clean"

VERDICTS = (VERDICT_KEY_WRONG, VERDICT_AMBIGUOUS, VERDICT_CLEAN)
KEY_ERROR_VERDICTS = (VERDICT_KEY_WRONG, VERDICT_AMBIGUOUS)


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def open_item_audit(db, item_id, now):
   row = models.ReviewQueue(
      id=new_id("RVQ"),
      kind=KIND,
      ref_id=item_id,
      opened_at=now,
      resolved_at=None,
      resolution=None,
      visible_to_student=0,
      created_at=now,
      updated_at=now,
   )
   db.add(row)
   db.flush()

   return row


def open_row_for(db, item_id):
   statement = (
      select(models.ReviewQueue)
      .where(models.ReviewQueue.kind == KIND)
      .where(models.ReviewQueue.ref_id == item_id)
      .where(models.ReviewQueue.resolved_at.is_(None))
   )

   return db.scalars(statement).first()


def write_resolution_audit_entry(db, row, verdict, now, actor):
   entry = models.AuditLog(
      id=new_id("AUD"),
      at=now,
      actor=actor,
      action="review_queue_item_resolved",
      subject=f"review_queue:{row.id}",
      detail=json.dumps({"kind": KIND, "ref_id": row.ref_id, "verdict": verdict}),
      created_at=now,
      updated_at=now,
   )
   db.add(entry)


def record_item_audit_verdict(db, item_id, verdict, now, second_answer=None, actor="operator"):
   is_known_verdict = verdict in VERDICTS

   if not is_known_verdict:
      raise ValueError(f"unknown item audit verdict: {verdict!r}")

   is_ambiguous = verdict == VERDICT_AMBIGUOUS
   has_second_answer = second_answer is not None
   missing_second_answer = is_ambiguous and not has_second_answer

   if missing_second_answer:
      raise ValueError(f"ambiguous verdict on {item_id} needs the second answer the operator found")

   row = open_row_for(db, item_id)
   has_open_row = row is not None

   if not has_open_row:
      row = open_item_audit(db, item_id, now)

   row.resolution = json.dumps({"verdict": verdict, "second_answer": second_answer})
   row.resolved_at = now
   row.updated_at = now

   write_resolution_audit_entry(db, row, verdict, now, actor)
   db.flush()

   return row


def recorded_verdicts(db):
   statement = (
      select(models.ReviewQueue)
      .where(models.ReviewQueue.kind == KIND)
      .where(models.ReviewQueue.resolution.is_not(None))
      .order_by(models.ReviewQueue.ref_id)
   )
   rows = db.scalars(statement).all()

   return [
      {"item_id": row.ref_id, **json.loads(row.resolution)} for row in rows
   ]


def key_error_rate(db, sample_size):
   verdicts = recorded_verdicts(db)
   recorded = len(verdicts)
   key_errors = len([
      verdict for verdict in verdicts if verdict["verdict"] in KEY_ERROR_VERDICTS
   ])
   is_complete = recorded >= sample_size
   rate = key_errors / recorded if recorded > 0 else None

   return {
      "sample_size": sample_size,
      "verdicts_recorded": recorded,
      "verdicts_complete": is_complete,
      "key_errors": key_errors,
      "key_error_rate": rate,
   }


def publish_key_error_rate(db, sample_size, now, report_path=None):
   measurement = key_error_rate(db, sample_size)
   measurement["measured_at"] = now

   has_report_path = report_path is not None

   if has_report_path:
      report_path.write_text(json.dumps(measurement, indent=2))

   return measurement
