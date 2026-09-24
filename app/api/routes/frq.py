"""The free-response routes of 06's API surface: capture, read-back, confirmation, gradings and the
dispute, plus the unit check that holds them and metric 9.

Grading runs after the response, as a background task with its own database session, because one
question can take a minute of grader calls; the client polls GET /attempts/{aid}/gradings, whose
grading_state says where the attempt is. Nothing here grades before POST
/attempts/{aid}/transcription/confirm (or the typed submission) has set transcription_confirmed.
"""
import base64
import binascii
import json
import time
from datetime import date, datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.api.deps import current_user, get_db, get_settings
from app.assessment import shape as assessment_shape
from app.auth.service import write_audit
from app.capture import booklet
from app.db import models
from app.frq import metrics, unit_check
from app.frq.bank import ensure_item_rows
from app.grading import service, transcribe
from app.grading.judge import ModelJudge
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import GuardedProvider, SubscriptionPacingCaps
from app.providers.subscription import SubscriptionProvider

router = APIRouter(tags=["free response"])


def utc_now():
   return datetime.now(timezone.utc)


def frq_context(settings):
   context = settings.frq

   if context is None:
      raise HTTPException(status_code=503, detail="the free-response bank is not loaded")

   return context


def owned_attempt(db, attempt_id, user):
   attempt = db.get(models.Attempt, attempt_id)
   session_row = db.get(models.Session, attempt.session_id) if attempt is not None else None
   is_owned = session_row is not None and session_row.user_id == user.id
   is_free_response = attempt is not None and attempt.format == "free_response"

   if not is_owned or not is_free_response:
      raise HTTPException(status_code=404, detail="no such free-response attempt")

   return attempt, session_row


def record_of(settings, attempt):
   record = frq_context(settings).record(attempt.item_id)

   if record is None:
      raise HTTPException(status_code=404, detail="this question is no longer in the bank")

   return record


def guarded_provider(settings, db, user_id):
   provider = settings.ai_provider

   if provider is None:
      return None

   is_live = isinstance(provider, AnthropicProvider)
   is_on_the_subscription = isinstance(provider, SubscriptionProvider)
   pacing = (settings.subscription_pacing or SubscriptionPacingCaps()) if is_on_the_subscription else None

   return GuardedProvider(
      provider,
      db,
      user_id,
      caps=settings.grading_caps,
      dev_spend_track=is_live,
      subscription_pacing=pacing,
   )


def grading_context(settings, db, user_id, today=None):
   context = frq_context(settings)
   guarded = guarded_provider(settings, db, user_id)
   sleep = settings.grading_sleep or time.sleep
   judge = ModelJudge(guarded, context.point_types, sleep=sleep) if guarded is not None else None
   session_context = settings.session_context

   return {
      "judge": judge,
      "labels": context.labels,
      "library": context.library,
      "diagnostician": guarded,
      "engine_graph": session_context.engine_graph if session_context is not None else None,
      "today": today or date.today(),
   }


def refused(error):
   return HTTPException(status_code=409, detail=str(error))


QUEUED_QUESTION_MODES = (unit_check.MODE, "part_drill", "mock")


def assessment_response_of(db, attempt):
   return db.scalar(select(models.AssessmentResponse).where(models.AssessmentResponse.attempt_id == attempt.id))


def refuse_while_part_open(db, attempt):
   """In a timed part the answer is written on paper during the part and captured after it, as on
   the exam, so no capture step runs while the part's clock is still going."""
   response = assessment_response_of(db, attempt)

   if response is None:
      return

   part = db.get(models.AssessmentPart, response.part_id)
   is_closed = part.closed_at is not None
   is_past_deadline = part.deadline_at is not None and utc_now() >= datetime.fromisoformat(part.deadline_at)

   if not is_closed and not is_past_deadline:
      raise HTTPException(status_code=409, detail="capture opens when the part closes; write in the booklet until then")


def booklet_addressing(db, attempt):
   """The mock's booklet page: the part's calculator header and the exam question number, from the
   form template (content/assessment/form_2027.json)."""
   response = assessment_response_of(db, attempt)

   if response is None:
      return {}

   part = db.get(models.AssessmentPart, response.part_id)
   booklet = assessment_shape.form_template()["booklet"]
   header = booklet["calculator_required_header"] if part.calculator else booklet["calculator_absent_header"]

   return {"header": header, "question": response.number}


@router.get("/frq/units")
def list_units(settings=Depends(get_settings), user=Depends(current_user)):
   context = frq_context(settings)

   return {
      "units": [
         {
            "unit_id": unit_id,
            "title": context.unit_titles.get(unit_id, unit_id),
            "questions": len(context.records_for_unit(unit_id)),
         }
         for unit_id in context.units()
      ]
   }


@router.post("/frq/unit-checks")
def open_unit_check(payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   context = frq_context(settings)
   unit_id = (payload or {}).get("unit_id")
   first_item_id = (payload or {}).get("item_id")
   now = utc_now()
   snapshot_id = settings.session_context.snapshot_id
   ensure_item_rows(db, context, snapshot_id, now)

   try:
      row = unit_check.open_unit_check(db, user.id, context, unit_id, snapshot_id, now, first_item_id=first_item_id)
   except ValueError as missing:
      raise HTTPException(status_code=404, detail=str(missing)) from missing

   return {"session_id": row.id, "mode": row.mode, "unit_id": unit_id, "questions": unit_check.questions_of(row, context)}


@router.get("/frq/unit-checks/{session_id}")
def read_unit_check(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   row = db.get(models.Session, session_id)
   is_owned = row is not None and row.user_id == user.id and row.mode == unit_check.MODE

   if not is_owned:
      raise HTTPException(status_code=404, detail="no such unit check")

   context = frq_context(settings)
   attempts = {
      attempt.item_id: attempt
      for attempt in db.scalars(select(models.Attempt).where(models.Attempt.session_id == row.id)).all()
   }
   questions = []

   for question in unit_check.questions_of(row, context):
      attempt = attempts.get(question["id"])
      questions.append(dict(question, attempt_id=attempt.id if attempt else None, grading_state=attempt.grading_state if attempt else None))

   return {"session_id": row.id, "mode": row.mode, "unit_id": json.loads(row.queue).get("unit_id"), "questions": questions}


@router.post("/sessions/{session_id}/frq/{item_id}/attempts")
def start_attempt(session_id: str, item_id: str, payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   session_row = db.get(models.Session, session_id)
   is_owned = session_row is not None and session_row.user_id == user.id

   if not is_owned:
      raise HTTPException(status_code=404, detail="no such session")

   record = frq_context(settings).record(item_id)
   is_known = record is not None
   holds_a_list = session_row.mode in QUEUED_QUESTION_MODES
   is_outside_the_check = holds_a_list and not unit_check.holds_question(session_row, item_id)

   if not is_known or is_outside_the_check:
      raise HTTPException(status_code=404, detail="this question is not in the session")

   capture_mode = (payload or {}).get("capture_mode") or "photo"

   try:
      attempt = service.start_attempt(db, session_row, record, capture_mode, utc_now())
   except service.GradingRefused as refusal:
      raise refused(refusal) from refusal

   return attempt_payload(db, attempt)


@router.get("/attempts/{attempt_id}/booklet.png")
def booklet_page(attempt_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   png = booklet.page_png(record_of(settings, attempt), page_code=attempt.id[-8:], **booklet_addressing(db, attempt))

   return Response(content=png, media_type="image/png", headers={"Cache-Control": "no-store"})


@router.post("/attempts/{attempt_id}/images")
def upload_image(attempt_id: str, payload: dict = Body(...), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   refuse_while_part_open(db, attempt)
   encoded = payload.get("data_base64") or ""

   try:
      data = base64.b64decode(encoded, validate=True)
   except (binascii.Error, ValueError) as undecodable:
      raise HTTPException(status_code=422, detail="the photo did not arrive as base64") from undecodable

   try:
      image, verdict = service.add_image(db, attempt, user.id, data, payload.get("media_type"), utc_now())
   except service.GradingRefused as refusal:
      raise refused(refusal) from refusal

   return {"image_id": image.id, "accepted": verdict.accepted, "reasons": verdict.reasons, "measurements": verdict.measurements}


@router.get("/attempts/{attempt_id}/images/{image_id}")
def read_image(attempt_id: str, image_id: str, db=Depends(get_db), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   image = db.get(models.FrqImage, image_id)
   is_present = image is not None and image.attempt_id == attempt.id and image.deleted_at is None and image.data is not None

   if not is_present:
      raise HTTPException(status_code=404, detail="no such photo")

   return Response(content=image.data, media_type=image.media_type, headers={"Cache-Control": "no-store"})


@router.delete("/attempts/{attempt_id}/images/{image_id}")
def delete_image(attempt_id: str, image_id: str, db=Depends(get_db), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   image = db.get(models.FrqImage, image_id)
   is_present = image is not None and image.attempt_id == attempt.id and image.deleted_at is None

   if not is_present:
      raise HTTPException(status_code=404, detail="no such photo")

   now = utc_now()
   image.data = None
   image.deleted_at = now.isoformat()
   image.updated_at = now.isoformat()
   write_audit(db, user.id, "frq_image_deleted", image.id, {"attempt_id": attempt.id}, now=now)

   return {"deleted": image.id}


@router.post("/attempts/{attempt_id}/transcription")
def run_read_back(attempt_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   record = record_of(settings, attempt)
   provider = guarded_provider(settings, db, user.id)

   try:
      service.read_back(db, attempt, record, provider, utc_now())
   except service.GradingRefused as refusal:
      raise refused(refusal) from refusal
   except transcribe.TranscriptionFailed as failed:
      raise HTTPException(status_code=502, detail=str(failed)) from failed

   return attempt_payload(db, attempt)


@router.get("/attempts/{attempt_id}/transcription")
def read_transcription(attempt_id: str, db=Depends(get_db), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)

   return attempt_payload(db, attempt)


def grade_in_background(engine, settings, attempt_id, user_id, today):
   with OrmSession(engine) as db:
      attempt = db.get(models.Attempt, attempt_id)
      session_row = db.get(models.Session, attempt.session_id)
      record = frq_context(settings).record(attempt.item_id)
      context = grading_context(settings, db, user_id, today)

      try:
         service.grade(db, session_row, attempt, record, context, utc_now())
         db.commit()
      except Exception:
         db.rollback()
         raise


def reread_in_background(engine, settings, grading_id, user_id, reason, today):
   with OrmSession(engine) as db:
      grading_row = db.get(models.Grading, grading_id)
      attempt = db.get(models.Attempt, grading_row.attempt_id)
      session_row = db.get(models.Session, attempt.session_id)
      record = frq_context(settings).record(attempt.item_id)
      context = grading_context(settings, db, user_id, today)

      try:
         service.reread(db, session_row, attempt, record, grading_row, context, reason, utc_now())
         db.commit()
      except Exception:
         db.rollback()
         raise


def confidence_of(payload):
   confidence = (payload or {}).get("confidence")
   is_known = confidence in (None, "guess", "unsure", "confident")

   if not is_known:
      raise HTTPException(status_code=422, detail="confidence is guess, unsure or confident")

   return confidence


@router.post("/attempts/{attempt_id}/transcription/confirm")
def confirm_transcription(
   attempt_id: str,
   request: Request,
   background: BackgroundTasks,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   record = record_of(settings, attempt)
   corrected = (payload or {}).get("read_back")
   confidence = confidence_of(payload)
   engine_graph = settings.session_context.engine_graph if settings.session_context else None

   try:
      service.confirm_read_back(db, attempt, record, corrected, utc_now(), engine_graph=engine_graph, user_id=user.id)
   except service.GradingRefused as refusal:
      raise refused(refusal) from refusal
   except ValueError as malformed:
      raise HTTPException(status_code=422, detail=str(malformed)) from malformed

   if confidence is not None:
      attempt.confidence = confidence
      attempt.confidence_source = "student"

   db.commit()
   background.add_task(grade_in_background, request.app.state.engine, settings, attempt.id, user.id, date.today())

   return attempt_payload(db, attempt)


@router.post("/attempts/{attempt_id}/typed")
def submit_typed(
   attempt_id: str,
   request: Request,
   background: BackgroundTasks,
   payload: dict = Body(...),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   refuse_while_part_open(db, attempt)
   record = record_of(settings, attempt)
   confidence = confidence_of(payload)

   try:
      service.submit_typed(db, attempt, record, payload.get("read_back"), utc_now())
   except service.GradingRefused as refusal:
      raise refused(refusal) from refusal
   except ValueError as malformed:
      raise HTTPException(status_code=422, detail=str(malformed)) from malformed

   if confidence is not None:
      attempt.confidence = confidence
      attempt.confidence_source = "student"

   db.commit()
   background.add_task(grade_in_background, request.app.state.engine, settings, attempt.id, user.id, date.today())

   return attempt_payload(db, attempt)


@router.get("/attempts/{attempt_id}/gradings")
def read_gradings(attempt_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   attempt, _session_row = owned_attempt(db, attempt_id, user)
   record = record_of(settings, attempt)

   return gradings_payload(db, attempt, record, frq_context(settings))


@router.post("/gradings/{grading_id}/dispute")
def dispute(
   grading_id: str,
   request: Request,
   background: BackgroundTasks,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   grading_row = db.get(models.Grading, grading_id)

   if grading_row is None:
      raise HTTPException(status_code=404, detail="no such point")

   attempt, _session_row = owned_attempt(db, grading_row.attempt_id, user)
   reason = str((payload or {}).get("reason") or "")[:500]
   background.add_task(reread_in_background, request.app.state.engine, settings, grading_id, user.id, reason, date.today())

   return {"grading_id": grading_id, "attempt_id": attempt.id, "rereading": True}


@router.get("/frq/metrics")
def read_metrics(db=Depends(get_db), user=Depends(current_user)):
   return metrics.metric_nine(db, user.id, utc_now())


def image_payload(image):
   return {
      "image_id": image.id,
      "accepted": bool(image.accepted),
      "quality": json.loads(image.quality),
      "created_at": image.created_at,
   }


def attempt_payload(db, attempt):
   stored = service.stored_transcription(attempt)

   return {
      "attempt_id": attempt.id,
      "item_id": attempt.item_id,
      "capture_mode": attempt.capture_mode,
      "grading_state": attempt.grading_state,
      "transcription_confirmed": bool(attempt.transcription_confirmed),
      "read_back": stored.get("read"),
      "confirmed": stored.get("confirmed"),
      "images": [image_payload(image) for image in service.live_images(db, attempt.id)],
   }


def gradings_payload(db, attempt, record, context):
   rows = service.gradings_of(db, attempt.id)
   points = {point["point_id"]: (part, point) for part in record["parts"] for point in part["points"]}
   ordered = sorted(rows, key=lambda row: list(points).index(row.point_id) if row.point_id in points else 0)
   entries = []

   for row in ordered:
      part, point = points.get(row.point_id, ({"id": row.part_id}, {"criterion": ""}))
      point_type = context.point_types.get(row.point_type_id, {})
      entries.append({
         "grading_id": row.id,
         "part_id": row.part_id,
         "point_id": row.point_id,
         "point_type_id": row.point_type_id,
         "point_label": point_type.get("name", row.point_type_id),
         "criterion": point.get("criterion", ""),
         "decided_by": row.decided_by,
         "earned": row.earned,
         "provisional": bool(row.provisional),
         "rationale": row.rationale,
         "evidence_quote": row.evidence_quote,
         "eligibility_note": row.eligibility_note,
         "rereads": row.rereads,
      })

   decided = [entry for entry in entries if not entry["provisional"]]
   diagnosis = db.scalar(select(models.Diagnosis).where(models.Diagnosis.attempt_id == attempt.id))

   return {
      "attempt_id": attempt.id,
      "item_id": attempt.item_id,
      "grading_state": attempt.grading_state,
      "points": entries,
      "earned": sum(1 for entry in decided if entry["earned"] == 1),
      "decided": len(decided),
      "total": len(points),
      "provisional": len(entries) - len(decided),
      "worked_solution": [
         {"part_id": part["id"], "answer_latex": part["answer_latex"], "steps": part["worked_solution"]}
         for part in record["parts"]
      ] if entries else [],
      "probe_scheduled": diagnosis.probe_scheduled if diagnosis is not None else None,
   }
