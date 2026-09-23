"""Provider calls deferred by a hard stop, kept in the jobs table app/export/archive.py already
uses for deferred work, so a queued call needs no new table or migration.

docs/plan/07-ai-provider-layer.md degrades a hard stop by serving static feedback and queueing
the call for later. One attempt queues at most once: a student who reopens the feedback screen
while the limit still holds finds the existing row rather than a duplicate.
"""
import json

from sqlalchemy import select

from app.auth.service import as_iso, new_id
from app.db import models

QUEUED_CALL_JOB_TYPE = "provider_call_queued"
QUEUED_CALL_STATE = "queued"


def idempotency_key_for(role, attempt_id):
   return f"{QUEUED_CALL_JOB_TYPE}:{role}:{attempt_id}"


def queue_call(db, user_id, attempt_id, request, reason, now):
   key = idempotency_key_for(request.role, attempt_id)
   existing = db.scalar(select(models.Job).where(models.Job.idempotency_key == key))

   if existing is not None:
      return existing

   timestamp = as_iso(now)
   payload = {
      "user_id": user_id,
      "attempt_id": attempt_id,
      "reason": reason,
      "role": request.role,
      "model": request.model,
      "max_output_tokens": request.max_output_tokens,
      "messages": [{"role": message.role, "content": message.content} for message in request.messages],
   }
   job = models.Job(
      id=new_id("JOB"),
      type=QUEUED_CALL_JOB_TYPE,
      payload=json.dumps(payload, sort_keys=True),
      idempotency_key=key,
      state=QUEUED_CALL_STATE,
      not_before=timestamp,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(job)
   db.flush()

   return job
