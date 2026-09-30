"""The six lesson endpoints of docs/plan/15-lessons.md, Endpoints, as the lessons framework
contract fixes them, thin over app/lessons/repository.py.

Every route resolves the lesson through repository.servable_lesson, so a draft, stale or unknown
lesson reads as 404 (15, invariant L8). A check answer is graded by app/items/grade.py against the
check's own key and written to lesson_check_responses alone; it never reaches attempts, the engine
or the diagnostician (15, invariant L2).
"""
from datetime import date, datetime, timezone
from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import current_user, get_db, get_settings
from app.db import models
from app.items.grade import grade
from app.lessons import plan, repository

router = APIRouter(tags=["lessons"])

LIBRARY = "library"
LESSON = "lesson"
REFRESHER = "refresher"
COMPLETED = "completed"
SKIPPED = "skipped"
OPENED = "opened"
PLAN_REASONS = (plan.FIRST_CONTACT, plan.READ_AGAIN) + plan.REFRESHER_REASONS
SLOT_EVENTS = (COMPLETED, SKIPPED)
CALCULATOR_ARCHETYPE = "calculator"


class LessonEventBody(BaseModel):
   event: Literal["opened", "section_viewed", "completed", "skipped"]
   section_id: str | None = None
   mode: Literal[
      "text", "step_reveal", "figure", "table", "motion", "interactive", "model", "contrast", "check", "prediction"
   ] | None = None
   elapsed_ms: int = Field(ge=0)
   band: Literal["low", "mid"] | None = None


class SessionLessonEventBody(LessonEventBody):
   reason: Literal["first_contact", "read_again", "feedback", "T1", "T2", "T3", "T4", "T5"] | None = None


class CheckAnswerBody(BaseModel):
   answer: Any = None
   option_id: str | None = None
   elapsed_ms: int = Field(ge=0)


class PromptAnswerBody(BaseModel):
   answer: Any = None
   option_id: str | None = None
   elapsed_ms: int = Field(ge=0)


def now_utc():
   return datetime.now(timezone.utc)


def lesson_snapshot(settings):
   context = settings.session_context
   has_context_snapshot = context is not None and context.snapshot is not None

   if has_context_snapshot:
      return context.snapshot

   return settings.resolve_snapshot()


def curriculum_of(settings):
   has_content_root = settings.content_root is not None

   if has_content_root:
      path = settings.content_root / "curriculum.json"

      if path.is_file():
         return repository.load_curriculum(path)

   return repository.load_curriculum()


def servable_or_404(db, lesson_id, version=None):
   row = repository.servable_lesson(db, lesson_id, version)

   if row is None:
      raise HTTPException(status_code=404, detail="no such lesson")

   return row


def user_state(db, user_id, lesson_id):
   return repository.state_as_dict(repository.lesson_state(db, user_id, lesson_id))


def has_calculator_work(lesson_body, settings):
   """True when a worked example belongs to a calculator archetype, so the reader can offer the
   Calculator destination beside it (docs/calculator/build-plan.md, Slice 3)."""
   context = settings.session_context
   archetypes = context.archetypes if context is not None else None

   if not archetypes:
      return False

   for section in lesson_body.get("sections") or []:
      is_worked_example = section.get("type") == plan.WORKED_EXAMPLE
      archetype = archetypes.get(section.get("archetype_id")) if is_worked_example else None
      is_calculator_archetype = archetype is not None and archetype.get("calculator_status") == CALCULATOR_ARCHETYPE

      if is_calculator_archetype:
         return True

   return False


@router.get("/lessons")
def read_library(
   unit: str | None = None,
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   curriculum = curriculum_of(settings)
   known_units = {entry["id"] for entry in curriculum["units"]}
   is_unknown_unit = unit is not None and unit not in known_units

   if is_unknown_unit:
      raise HTTPException(status_code=404, detail="no such unit")

   return repository.library_listing(db, user.id, lesson_snapshot(settings), unit_id=unit, curriculum=curriculum)


@router.get("/lessons/{lesson_id}")
def read_lesson(
   lesson_id: str,
   version: int | None = None,
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   row = servable_or_404(db, lesson_id, version)

   return {
      **row.body,
      "state": user_state(db, user.id, lesson_id),
      "calculator_work": has_calculator_work(row.body, settings),
   }


def days_between(earlier_iso, today):
   if earlier_iso is None:
      return None

   return (today - datetime.fromisoformat(earlier_iso).date()).days


def plan_state(state, today):
   """The two facts plan_lesson reads for T4 (app/lessons/plan.py is_repeat_t4)."""
   if state is None:
      return None

   return {
      "refresher_reason": state["refresher_due_reason"],
      "days_since_refresher": days_between(state["refresher_served_at"], today),
   }


@router.get("/lessons/{lesson_id}/plan")
def read_plan(
   lesson_id: str,
   band: Literal["low", "mid"],
   reason: Literal["first_contact", "read_again", "T1", "T2", "T3", "T4", "T5"] = "read_again",
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   row = servable_or_404(db, lesson_id)
   state = user_state(db, user.id, lesson_id)
   lesson_plan = plan.plan_lesson(row.body, band, reason, lesson_state=plan_state(state, date.today()))

   return {
      "lesson": row.body,
      "plan": lesson_plan.as_dict(),
      "band": band,
      "state": state,
      "calculator_work": has_calculator_work(row.body, settings),
   }


def library_state_fields(row, body, now):
   is_completed = body.event == COMPLETED

   if not is_completed:
      return None

   return {"status": "read", "read_source": LIBRARY, "read_at": now.isoformat(), "version_seen": row.version}


def session_state_fields(row, body, existing, now):
   stamp = now.isoformat()

   if body.event == OPENED:
      first_served_at = existing.first_served_at if existing is not None and existing.first_served_at else stamp
      fields = {"status": "served", "first_served_at": first_served_at, "version_seen": row.version}

      if body.band is not None:
         fields["band_served"] = body.band

      return fields

   if body.event == COMPLETED:
      return {"status": "read", "read_source": "session", "read_at": stamp, "version_seen": row.version}

   if body.event == SKIPPED:
      return {"status": "skipped", "version_seen": row.version}

   return None


def refresher_state_fields(body, existing, now):
   is_completed = body.event == COMPLETED

   if not is_completed:
      return None

   count = existing.refresher_count if existing is not None else 0
   fields = {"refresher_served_at": now.isoformat(), "refresher_count": count + 1, "refresher_due_reason": None}

   if existing is None:
      fields["status"] = "read"

   return fields


def record_event(db, user, row, body, kind, fields, now, session_id=None, reason=None):
   repository.write_event(
      db,
      user.id,
      row.id,
      row.version,
      kind,
      body.event,
      session_id=session_id,
      section_id=body.section_id,
      mode=body.mode,
      reason=reason,
      band=body.band,
      elapsed_ms=body.elapsed_ms,
      now=now,
   )

   if fields is not None:
      repository.write_state(db, user.id, row.id, now=now, **fields)

   return {"ok": True, "state": user_state(db, user.id, row.id)}


@router.post("/lessons/{lesson_id}/events")
def post_library_event(
   lesson_id: str,
   body: LessonEventBody,
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   row = servable_or_404(db, lesson_id)
   now = now_utc()

   return record_event(db, user, row, body, LIBRARY, library_state_fields(row, body, now), now)


def owned_session_or_404(db, session_id, user):
   session_row = db.get(models.Session, session_id)
   is_owned = session_row is not None and session_row.user_id == user.id

   if not is_owned:
      raise HTTPException(status_code=404, detail="no such session")

   return session_row


@router.post("/sessions/{session_id}/lessons/{lesson_id}/events")
def post_session_event(
   session_id: str,
   lesson_id: str,
   body: SessionLessonEventBody,
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   session_row = owned_session_or_404(db, session_id, user)
   row = servable_or_404(db, lesson_id)
   now = now_utc()
   existing = repository.lesson_state(db, user.id, lesson_id)
   is_refresher = body.reason in plan.REFRESHER_REASONS

   if is_refresher:
      kind = REFRESHER
      fields = refresher_state_fields(body, existing, now)
   else:
      kind = LESSON
      fields = session_state_fields(row, body, existing, now)

   response = record_event(db, user, row, body, kind, fields, now, session_id=session_id, reason=body.reason)
   consumes_slot = body.event in SLOT_EVENTS

   if consumes_slot:
      repository.consume_lesson_slot(db, session_row, lesson_id, body.event)

   return response


def is_named(record_id, requested_id):
   return record_id == requested_id or record_id.endswith(f"#{requested_id}")


def find_check(lesson_body, check_id):
   """A check is named by its full id or by its #chk-n suffix, since a client may not carry the
   # through a path."""
   for check in lesson_body.get("checks") or []:
      if is_named(check["id"], check_id):
         return check

   return None


def as_gradable_item(check):
   options = [
      {"id": option["id"], "is_key": option["is_key"], "error_path": option.get("error_path")}
      for option in check.get("options") or []
   ]

   return {"answer_key": check["answer_key"], "options": options, "skills": check.get("skills") or []}


def error_block(lesson_body, error_id):
   if error_id is None:
      return None

   anchor = f"{lesson_body['id']}#err-{error_id}"

   for section in lesson_body["sections"]:
      if section["id"] == anchor:
         return section

   return None


def error_anchor(lesson_body, error_id):
   if error_id is None:
      return None

   anchor = f"{lesson_body['id']}#err-{error_id}"
   section_ids = {section["id"] for section in lesson_body["sections"]}

   return anchor if anchor in section_ids else None


def explanation_anchor(lesson_body, check):
   """The worked example that shows the check's method: the one it completes, else the first on
   the same archetype."""
   completes = check.get("completes")

   if completes is not None:
      return completes

   for section in lesson_body["sections"]:
      is_same_archetype = section["type"] == plan.WORKED_EXAMPLE and section.get("archetype_id") == check["archetype_id"]

      if is_same_archetype:
         return section["id"]

   return None


@router.post("/lessons/{lesson_id}/checks/{check_id}/answers")
def post_check_answer(
   lesson_id: str,
   check_id: str,
   body: CheckAnswerBody,
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   row = servable_or_404(db, lesson_id)
   check = find_check(row.body, check_id)

   if check is None:
      raise HTTPException(status_code=404, detail="no such check")

   submission = {"mathjson": body.answer, "selected_option_id": body.option_id}
   result = grade(as_gradable_item(check), submission, {}, check["format"])
   is_correct = result["correct"] is True
   error_id = None if is_correct else result["error_path"]
   repository.write_check_response(
      db,
      user.id,
      row.id,
      row.version,
      check["id"],
      {"answer": body.answer, "option_id": body.option_id},
      result["correct"],
      error_id,
      body.elapsed_ms,
   )

   block = error_block(row.body, error_id)
   right_step = block.get("right_step") if block is not None else None

   return {
      "correct": is_correct,
      "error_id": error_id,
      "anchor": error_anchor(row.body, error_id),
      "explanation_anchor": None if is_correct else explanation_anchor(row.body, check),
      "right_step": right_step["text"] if right_step is not None else None,
      "scoring_consequence": block.get("scoring_consequence") if block is not None else None,
   }


PREDICTION_PROMPT = "prediction"
FIX_PROMPT = "fix"
FADE_PROMPT = "fade"


def prompt_kind(section):
   """The kind of answer a section asks for before it reveals itself, or None when it asks for
   none."""
   is_prediction = section["type"] == plan.PREDICTION
   asks_for_a_fix = section["type"] == plan.COMMON_ERROR and section.get("fix_prompt") is True
   is_faded = section["type"] == plan.WORKED_EXAMPLE and section.get("fade_from") is not None

   if is_prediction:
      return PREDICTION_PROMPT

   if asks_for_a_fix:
      return FIX_PROMPT

   if is_faded:
      return FADE_PROMPT

   return None


def find_prompt(lesson_body, section_id):
   for section in lesson_body["sections"]:
      if is_named(section["id"], section_id):
         return section

   return None


def prompt_as_gradable_item(section, kind):
   options = []

   if kind == PREDICTION_PROMPT:
      answer_key = section.get("answer_key")
      options = [{"id": option["id"], "is_key": option["is_key"], "error_path": None} for option in section.get("options") or []]
   elif kind == FIX_PROMPT:
      answer_key = {"form": "symbolic", "mathjson": section["right_step"]["expression"]}
   else:
      answer_key = section["answer"]

   return {"answer_key": answer_key, "options": options, "skills": section.get("skills") or []}


def prompt_format(section, kind):
   if kind == PREDICTION_PROMPT:
      return section["format"]

   return "short_answer"


@router.post("/lessons/{lesson_id}/prompts/{section_id}/answers")
def post_prompt_answer(
   lesson_id: str,
   section_id: str,
   body: PromptAnswerBody,
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   row = servable_or_404(db, lesson_id)
   section = find_prompt(row.body, section_id)
   kind = prompt_kind(section) if section is not None else None

   if kind is None:
      raise HTTPException(status_code=404, detail="no such prompt")

   submission = {"mathjson": body.answer, "selected_option_id": body.option_id}
   result = grade(prompt_as_gradable_item(section, kind), submission, {}, prompt_format(section, kind))
   repository.write_check_response(
      db,
      user.id,
      row.id,
      row.version,
      section["id"],
      {"answer": body.answer, "option_id": body.option_id},
      result["correct"],
      None,
      body.elapsed_ms,
   )
   is_prediction = kind == PREDICTION_PROMPT

   return {
      "correct": result["correct"] is True,
      "section_id": section["id"],
      "kind": kind,
      "resolution": section["resolution"]["text"] if is_prediction else None,
   }