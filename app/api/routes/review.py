"""GET /review-queue and POST /review-queue/{id}/resolve, the operator's queue per 06's API surface.

This installation is single user, so the operator is the session's own user, the same one
app/auth/service.require_sole_user names, and there is no second notion of an operator role. P1
re-runs no grading and retires no item, so the "may re-run a grading or retire an item" trigger
named for this route in 06-architecture.md has no P1 effect and nothing is implemented for it here.

Ruled 2026-09-23: an item_audit verdict now goes through the same sample check and one-verdict
rule tools/check_audit_verdicts.py and app/review/audit.record_item_audit_verdict already enforce
for the CLI path, so a verdict outside the drawn sample or a second verdict on an already-audited
item is refused here too, rather than only there. The sample itself comes from
settings.resolve_key_audit_sample_ids() (docs/operator/key-audit.md's sample file); until the
operator configures one, no item_audit verdict can be resolved through this route, which is the
fail-closed reading of "outside the sample" when there is no sample yet.
"""
import json

from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import current_user, get_db, get_settings
from app.auth.service import as_iso, utc_now
from app.db import models
from app.review import audit

router = APIRouter(prefix="/review-queue", tags=["review-queue"])


def body_of(payload):
   return payload or {}


def open_row_payload(row):
   return {
      "id": row.id,
      "kind": row.kind,
      "ref_id": row.ref_id,
      "opened_at": row.opened_at,
      "visible_to_student": row.visible_to_student,
   }


def resolved_row_payload(row):
   return {
      "id": row.id,
      "kind": row.kind,
      "ref_id": row.ref_id,
      "opened_at": row.opened_at,
      "resolved_at": row.resolved_at,
      "resolution": json.loads(row.resolution) if row.resolution is not None else None,
   }


def owned_row(db, row_id):
   row = db.get(models.ReviewQueue, row_id)
   is_missing = row is None

   if is_missing:
      raise HTTPException(status_code=404, detail="no such review queue row")

   return row


@router.get("")
def list_open_rows(db=Depends(get_db), user=Depends(current_user)):
   rows = (
      db.query(models.ReviewQueue)
      .filter(models.ReviewQueue.resolved_at.is_(None))
      .order_by(models.ReviewQueue.opened_at.asc(), models.ReviewQueue.id.asc())
      .all()
   )

   return [open_row_payload(row) for row in rows]


class NoKeyAuditSample(ValueError):
   pass


def resolve_item_audit(db, row, fields, now, sample_ids):
   no_sample_is_configured = sample_ids is None

   if no_sample_is_configured:
      raise NoKeyAuditSample("no key-audit sample is configured; the operator has not drawn one yet")

   audit.refuse_outside_sample(row.ref_id, sample_ids)
   audit.refuse_second_verdict(db, row.ref_id)

   verdict = fields.get("verdict")

   return audit.resolve_item_audit_row(
      db, row, verdict, now, second_answer=fields.get("second_answer")
   )


def resolve_generic_row(db, row, fields, now):
   resolution_label = fields.get("resolution") or "resolved"
   row.resolution = json.dumps({"resolution": resolution_label})
   row.resolved_at = now
   row.updated_at = now
   audit.write_resolution_audit_entry(db, row, resolution_label, now, "operator")
   db.flush()

   return row


@router.post("/{row_id}/resolve")
def resolve_row(
   row_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   row = owned_row(db, row_id)
   is_already_resolved = row.resolved_at is not None

   if is_already_resolved:
      raise HTTPException(status_code=409, detail="this review queue row is already resolved")

   fields = body_of(payload)
   now = as_iso(utc_now())
   is_item_audit = row.kind == audit.KIND

   try:
      if is_item_audit:
         sample_ids = settings.resolve_key_audit_sample_ids()
         resolved = resolve_item_audit(db, row, fields, now, sample_ids)
      else:
         resolved = resolve_generic_row(db, row, fields, now)
   except ValueError as refused:
      raise HTTPException(status_code=400, detail=str(refused)) from refused

   return resolved_row_payload(resolved)
