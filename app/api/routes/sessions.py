"""The session routes of 06's API surface, thin over app/session/service.py.

Every route resolves the session row by id and by the cookie's user id, so one user's id never
reaches another user's row, and a session belonging to nobody in this cookie reads as 404.
"""
import json
from datetime import date

from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import current_user, get_db, get_settings
from app.db import models
from app.feedback import render, tutor
from app.items.grade import grade
from app.providers.guard import BudgetStopped, GuardedProvider
from app.session import service

router = APIRouter(prefix="/sessions", tags=["sessions"])


def body_of(payload):
   return payload or {}


def known_scope_ids(context, scope):
   is_archetype_scope = scope == "archetype"

   if is_archetype_scope:
      return set(context.archetypes)

   return set(context.graph.skills)


def today_of(fields):
   raw = fields.get("today")
   is_given = isinstance(raw, str) and raw != ""

   if is_given:
      return date.fromisoformat(raw)

   return date.today()


def owned_session(db, session_id, user):
   row = db.get(models.Session, session_id)
   is_missing = row is None
   is_other_user = row is not None and row.user_id != user.id

   if is_missing or is_other_user:
      raise HTTPException(status_code=404, detail="no such session")

   return row


def owned_attempt(db, session_row, attempt_id):
   row = db.get(models.Attempt, attempt_id)
   is_missing = row is None
   is_other_session = row is not None and row.session_id != session_row.id

   if is_missing or is_other_session:
      raise HTTPException(status_code=404, detail="no such attempt")

   return row


def chosen_option(item, answer):
   options = item.options or []
   chosen_id = answer.get("option_id")
   names_an_option = chosen_id is not None

   if not names_an_option:
      return None

   for option in options:
      is_chosen = option.get("id") == chosen_id

      if is_chosen:
         return option

   return None


def session_payload(db, row):
   remaining = [
      item
      for block, position, item in service.served_positions(row)
      if (block, position) not in service.consumed_positions(db, row)
   ]

   return {
      "id": row.id,
      "mode": row.mode,
      "sub_mode": row.sub_mode,
      "started_at": row.started_at,
      "ended_at": row.ended_at,
      "updates_mastery": row.updates_mastery,
      "snapshot_id": row.snapshot_id,
      "queue": json.loads(row.queue),
      "remaining": remaining,
   }


@router.post("")
def open_session(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_of(payload)
   context = settings.session_context
   row = service.open_session(
      db,
      user.id,
      fields.get("mode") or "learning",
      context.graph,
      context.engine_graph,
      context.archetypes,
      context.bank,
      context.snapshot_id,
      today_of(fields),
      settings.rng,
      sub_mode=fields.get("sub_mode"),
   )

   return session_payload(db, row)


@router.get("/{session_id}")
def read_session(session_id: str, db=Depends(get_db), user=Depends(current_user)):
   return session_payload(db, owned_session(db, session_id, user))


@router.get("/{session_id}/next")
def read_next_item(session_id: str, db=Depends(get_db), user=Depends(current_user)):
   row = owned_session(db, session_id, user)

   return {"item": service.next_item(db, row.id)}


@router.post("/{session_id}/attempts")
def submit_attempt(
   session_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   context = settings.session_context

   def grade_against_the_stored_key(queue_item, answer):
      stored = db.get(models.Item, queue_item["id"])
      has_no_row = stored is None

      if has_no_row:
         raise ValueError(f"item {queue_item['id']} has no items row, so it cannot be graded")

      submission = {
         "selected_option_id": answer.get("option_id"),
         "mathjson": answer.get("mathjson"),
         "units": answer.get("units"),
      }

      return grade(stored, submission, context.errors, served_format=queue_item["format"])

   try:
      attempt = service.record_attempt(
         db,
         row.id,
         fields.get("item_id"),
         fields.get("answer") or {},
         fields.get("elapsed_ms"),
         today_of(fields),
         archetypes=context.archetypes,
         engine_graph=context.engine_graph,
         confidence=fields.get("confidence"),
         grader=grade_against_the_stored_key,
      )
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return {
      "id": attempt.id,
      "item_id": attempt.item_id,
      "correct": None if attempt.correct is None else bool(attempt.correct),
      "confidence": attempt.confidence,
      "served_stage": attempt.served_stage,
      "format": attempt.format,
      "p_split": attempt.p_split,
      "p_compensatory": attempt.p_compensatory,
   }


@router.get("/{session_id}/attempts/{attempt_id}/feedback")
def read_feedback(
   session_id: str,
   attempt_id: str,
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   row = owned_session(db, session_id, user)
   attempt = owned_attempt(db, row, attempt_id)
   context = settings.session_context
   item = db.get(models.Item, attempt.item_id)
   is_unpublished = item is None

   if is_unpublished:
      raise HTTPException(status_code=404, detail="no items row for this attempt")

   archetype = context.archetypes.get(item.archetype_id)
   is_unknown_archetype = archetype is None

   if is_unknown_archetype:
      raise HTTPException(status_code=404, detail="the item names no archetype in this snapshot")

   is_ungraded = attempt.correct is None
   awaits_grading = is_ungraded and attempt.submitted_at is not None

   if awaits_grading:
      raise HTTPException(
         status_code=409,
         detail="this attempt is ungraded, so no point was lost and no feedback is composed",
      )

   answer = json.loads(attempt.response) if attempt.response else {}
   chosen = chosen_option(item, answer)
   error_path = (chosen or {}).get("error_path")
   error_record = context.errors.get(error_path) if error_path else None

   try:
      feedback = render.render_feedback(
         attempt.served_stage,
         archetype,
         {"worked_solution": item.worked_solution},
         submitted=attempt.submitted_at is not None,
         correct=None if attempt.correct is None else bool(attempt.correct),
         step_outcomes=answer.get("step_outcomes"),
         chosen_option=chosen,
         error_record=error_record,
         confidence=attempt.confidence,
      )
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   sentence, tutor_unavailable = tutor_sentence_for(settings, db, user, attempt, feedback)

   return dict(render.as_dict(feedback), sentence=sentence, tutor_unavailable=tutor_unavailable)


def tutor_sentence_for(settings, db, user, attempt, feedback):
   """Every tutor call goes through the guard, which is where 07 puts the cap, the accounting
   and the audit trail, and a call that would cross the cap never reaches the provider.

   07's hard-stop table gives the tutor role Stop at the cap, with the practice queue unaffected
   and a line saying the tutor is unavailable for the rest of today. That line is what the second
   return value carries, so the session screen can say it where it happened rather than only in
   settings.
   """
   has_tutor = settings.tutor is not None

   if not has_tutor:
      return None, False

   guarded = GuardedProvider(settings.tutor, db, user.id, caps=settings.tutor_caps)

   try:
      sentence = tutor.compose_sentence(guarded, feedback, db=db, attempt=attempt)
   except BudgetStopped:
      return None, True

   return sentence, False


@router.post("/{session_id}/attempts/{attempt_id}/confidence")
def submit_confidence(
   session_id: str,
   attempt_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   owned_attempt(db, row, attempt_id)
   context = settings.session_context

   try:
      attempt = service.record_confidence(
         db,
         attempt_id,
         fields.get("confidence"),
         archetypes=context.archetypes,
         engine_graph=context.engine_graph,
         today=today_of(fields),
      )
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return {"id": attempt.id, "confidence": attempt.confidence}


@router.post("/{session_id}/attempts/{attempt_id}/error-note")
def submit_error_note(
   session_id: str,
   attempt_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   user=Depends(current_user),
):
   """One note per item corrected in this session, per 02's Session assembly block 4.

   An attempt that was right, or that never graded, carries no note, so 06's API surface gains
   this row rather than the attempts route gaining a field.
   """
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   attempted = owned_attempt(db, row, attempt_id)
   was_corrected = attempted.correct == 0

   if not was_corrected:
      raise HTTPException(
         status_code=409,
         detail="an error note belongs to an item corrected in this session",
      )

   note = fields.get("note")
   is_blank = not isinstance(note, str) or note.strip() == ""

   if is_blank:
      raise HTTPException(status_code=400, detail="the error note cannot be empty")

   try:
      attempt = service.record_error_note(db, attempt_id, note.strip())
   except service.ErrorNoteAlreadyWritten:
      raise HTTPException(
         status_code=409,
         detail="this attempt already carries its error note",
      )
   except service.ErrorNoteNotOneLine:
      raise HTTPException(status_code=400, detail="the error note is one line")

   return {"id": attempt.id, "error_note": attempt.error_note}


@router.post("/{session_id}/judgments")
def record_judgment(
   session_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   scope = fields.get("scope") or "skill"
   scope_id = fields.get("scope_id") or ""
   known = known_scope_ids(settings.session_context, scope)
   scope_id_is_known = scope_id in known

   if not scope_id_is_known:
      raise HTTPException(status_code=400, detail=f"{scope_id} is not a {scope} in the loaded snapshot")

   retention = fields.get("predicted_retention")
   retention_is_number = isinstance(retention, (int, float)) and not isinstance(retention, bool)
   retention_in_range = retention_is_number and 0.0 <= retention <= 1.0

   if not retention_in_range:
      raise HTTPException(status_code=400, detail="predicted_retention must be a number from 0 to 1")

   judgment = service.record_judgment(
      db, row.id, scope, scope_id, float(retention), service.utc_now()
   )

   return {"id": judgment.id, "scope": judgment.scope, "scope_id": judgment.scope_id}


@router.post("/{session_id}/close")
def close_session(
   session_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   context = settings.session_context

   try:
      closed = service.close_session(
         db,
         row.id,
         archetypes=context.archetypes,
         engine_graph=context.engine_graph,
         today=today_of(fields),
      )
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return {"id": closed.id, "ended_at": closed.ended_at}
