"""The assessment routes: 06's /mocks rows, the part drills beside them, and the unit check.

06 names POST /mocks, GET /mocks/{id}, POST /mocks/{id}/sections/{n}/start, POST
/mocks/{id}/sections/{n}/submit and POST /mocks/{id}/finish. A part drill is a one-part timed
session and answers to the same subroutes under /drills, with n always 1. {n} is the part's
position in the session (1 to 4 for a mock), because the four timed shapes are parts, not
sections. Saving the student's work on a question, the result and the history are added beside
them; 06 does not list them.

The mock and the drills can be switched off by configuration (Settings.timed_assessments, set
from GROWTH_TIMED_ASSESSMENTS in app/main.py), which is 11 P5's rollback; the unit check does
not depend on the booklet shape and stays on.
"""
import random
from datetime import date

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select

from app.api.deps import current_user, get_db, get_settings
from app.assessment import assemble, shape, unit_check
from app.assessment import service as assessment
from app.db import models
from app.frq.bank import ensure_item_rows

router = APIRouter(tags=["assessment"])


def context_of(settings):
   session_context = settings.session_context
   snapshot = session_context.snapshot or settings.resolve_snapshot()
   bank = session_context.bank
   ensures = getattr(bank, "ensure_ingested", None)

   if ensures is not None:
      ensures()

   return assessment.AssessmentContext(
      archetypes=session_context.archetypes,
      errors=session_context.errors,
      engine_graph=session_context.engine_graph,
      frq=settings.frq,
      graph=session_context.graph,
      snapshot=snapshot,
   )


def refused(error):
   return HTTPException(status_code=409, detail=str(error))


def timed_enabled_or_404(settings):
   is_enabled = getattr(settings, "timed_assessments", True)

   if not is_enabled:
      raise HTTPException(status_code=404, detail="timed practice is switched off on this installation")


def owned(db, session_id, user, modes):
   row = db.get(models.Session, session_id)
   is_owned = row is not None and row.user_id == user.id and row.mode in modes

   if not is_owned:
      raise HTTPException(status_code=404, detail="no such assessment")

   return row


def rng_for(settings, user, now):
   return random.Random(f"{settings.rng_seed}:{user.id}:{now.isoformat()}")


@router.get("/assessments/shape")
def read_shape(settings=Depends(get_settings), user=Depends(current_user)):
   payload = shape.shape_payload()
   payload["timed_available"] = getattr(settings, "timed_assessments", True)

   return payload


def open_timed(db, settings, user, part_keys, capture_mode):
   timed_enabled_or_404(settings)
   now = assessment.utc_now()
   context = context_of(settings)
   snapshot_id = settings.session_context.snapshot_id

   if context.frq is not None:
      ensure_item_rows(db, context.frq, snapshot_id, now)

   try:
      row = assessment.open_timed(db, user.id, context, part_keys, snapshot_id, now, rng_for(settings, user, now), capture_mode=capture_mode)
   except (assessment.AssessmentRefused, assemble.AssessmentUnavailable) as refusal:
      raise refused(refusal) from refusal

   return assessment.session_payload(db, context, row, now)


@router.post("/mocks")
def open_mock(payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   capture_mode = (payload or {}).get("capture_mode") or "photo"

   return open_timed(db, settings, user, list(shape.part_keys()), capture_mode)


@router.get("/mocks")
def list_mocks(db=Depends(get_db), user=Depends(current_user)):
   return {"mocks": assessment.mock_history(db, user.id)}


@router.get("/assessments/unfinished")
def list_unfinished(db=Depends(get_db), user=Depends(current_user)):
   return {"unfinished": assessment.unfinished(db, user.id)}


@router.post("/drills")
def open_drill(payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   fields = payload or {}
   part_key = fields.get("part")
   is_known = part_key in shape.part_keys()

   if not is_known:
      raise HTTPException(status_code=422, detail=f"part must be one of {', '.join(shape.part_keys())}")

   return open_timed(db, settings, user, [part_key], fields.get("capture_mode") or "photo")


TIMED_PREFIXES = {"mocks": (assessment.MOCK,), "drills": (assessment.PART_DRILL,)}


def timed_session(db, settings, user, kind, session_id):
   timed_enabled_or_404(settings)

   return owned(db, session_id, user, TIMED_PREFIXES[kind])


def read_timed(db, settings, user, kind, session_id):
   row = timed_session(db, settings, user, kind, session_id)

   return assessment.session_payload(db, context_of(settings), row, assessment.utc_now())


def start_timed_part(db, settings, user, kind, session_id, position):
   row = timed_session(db, settings, user, kind, session_id)
   context = context_of(settings)
   now = assessment.utc_now()

   try:
      assessment.start_part(db, context, row, position, now)
   except assessment.AssessmentRefused as refusal:
      db.commit()
      raise refused(refusal) from refusal

   return assessment.session_payload(db, context, row, now)


def save_timed_question(db, settings, user, kind, session_id, position, number, payload):
   row = timed_session(db, settings, user, kind, session_id)

   try:
      response = assessment.save_response(db, context_of(settings), row, position, number, payload or {}, assessment.utc_now())
   except assessment.AssessmentRefused as refusal:
      db.commit()
      raise refused(refusal) from refusal

   return {"number": response.number, "saved": True}


def submit_timed_part(db, settings, user, kind, session_id, position):
   row = timed_session(db, settings, user, kind, session_id)
   context = context_of(settings)
   now = assessment.utc_now()

   try:
      assessment.submit_part(db, context, row, position, now)
   except assessment.AssessmentRefused as refusal:
      db.commit()
      raise refused(refusal) from refusal

   return assessment.session_payload(db, context, row, now)


def read_timed_result(db, settings, user, kind, session_id):
   row = timed_session(db, settings, user, kind, session_id)

   return assessment.results(db, context_of(settings), row, assessment.utc_now())


@router.get("/mocks/{session_id}")
def read_mock(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return read_timed(db, settings, user, "mocks", session_id)


@router.post("/mocks/{session_id}/sections/{position}/start")
def start_mock_part(session_id: str, position: int, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return start_timed_part(db, settings, user, "mocks", session_id, position)


@router.put("/mocks/{session_id}/sections/{position}/questions/{number}")
def save_mock_question(session_id: str, position: int, number: int, payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return save_timed_question(db, settings, user, "mocks", session_id, position, number, payload)


@router.post("/mocks/{session_id}/sections/{position}/submit")
def submit_mock_part(session_id: str, position: int, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return submit_timed_part(db, settings, user, "mocks", session_id, position)


@router.get("/mocks/{session_id}/result")
def read_mock_result(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return read_timed_result(db, settings, user, "mocks", session_id)


@router.get("/drills/{session_id}")
def read_drill(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return read_timed(db, settings, user, "drills", session_id)


@router.post("/drills/{session_id}/sections/{position}/start")
def start_drill_part(session_id: str, position: int, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return start_timed_part(db, settings, user, "drills", session_id, position)


@router.put("/drills/{session_id}/sections/{position}/questions/{number}")
def save_drill_question(session_id: str, position: int, number: int, payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return save_timed_question(db, settings, user, "drills", session_id, position, number, payload)


@router.post("/drills/{session_id}/sections/{position}/submit")
def submit_drill_part(session_id: str, position: int, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return submit_timed_part(db, settings, user, "drills", session_id, position)


@router.get("/drills/{session_id}/result")
def read_drill_result(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return read_timed_result(db, settings, user, "drills", session_id)


@router.post("/mocks/{session_id}/finish")
def finish_mock(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   row = timed_session(db, settings, user, "mocks", session_id)

   try:
      return assessment.finish_mock(db, context_of(settings), row, assessment.utc_now())
   except assessment.AssessmentRefused as refusal:
      raise refused(refusal) from refusal


@router.get("/unit-checks/units")
def unit_check_units(db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   context = context_of(settings)
   titles = settings.session_context.unit_titles or {}
   rows = unit_check.available_units(db, context, user.id)

   return {"units": [dict(entry, title=titles.get(entry["unit_id"], entry["unit_id"])) for entry in rows]}


@router.post("/unit-checks")
def open_unit_check(payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   unit_id = (payload or {}).get("unit_id")
   context = context_of(settings)
   now = assessment.utc_now()

   try:
      row = unit_check.open_unit_check(db, user.id, context, unit_id, settings.session_context.snapshot_id, now)
   except assessment.AssessmentRefused as refusal:
      raise refused(refusal) from refusal

   return assessment.session_payload(db, context, row, now)


def owned_unit_check(db, session_id, user):
   row = owned(db, session_id, user, (assessment.UNIT_CHECK,))
   has_parts = db.scalar(select(models.AssessmentPart.id).where(models.AssessmentPart.session_id == row.id)) is not None

   if not has_parts:
      raise HTTPException(status_code=404, detail="no such unit check")

   return row


@router.get("/unit-checks/{session_id}")
def read_unit_check(session_id: str, db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   row = owned_unit_check(db, session_id, user)

   return assessment.session_payload(db, context_of(settings), row, assessment.utc_now())


@router.put("/unit-checks/{session_id}/questions/{number}")
def save_unit_check_question(session_id: str, number: int, payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   row = owned_unit_check(db, session_id, user)

   try:
      assessment.save_response(db, context_of(settings), row, 1, number, payload or {}, assessment.utc_now())
   except assessment.AssessmentRefused as refusal:
      raise refused(refusal) from refusal

   return {"number": number, "saved": True}


@router.post("/unit-checks/{session_id}/submit")
def submit_unit_check(session_id: str, payload: dict = Body(default=None), db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   row = owned_unit_check(db, session_id, user)
   today_text = (payload or {}).get("today")

   try:
      today = date.fromisoformat(today_text) if today_text else None
   except ValueError as unreadable:
      raise HTTPException(status_code=422, detail="today is an ISO date") from unreadable

   try:
      return unit_check.submit_unit_check(db, context_of(settings), row, assessment.utc_now(), today=today)
   except assessment.AssessmentRefused as refusal:
      raise refused(refusal) from refusal
