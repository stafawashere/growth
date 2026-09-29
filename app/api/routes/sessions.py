"""The session routes of 06's API surface, thin over app/session/service.py.

Every route resolves the session row by id and by the cookie's user id, so one user's id never
reaches another user's row, and a session belonging to nobody in this cookie reads as 404.
"""
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select

from app.api.deps import current_user, get_db, get_settings
from app.db import models
from app.experiments import switches
from app.feedback import render, tutor
from app.items.grade import grade
from app.items.verify import ChildDiedError
from app.lessons import repository as lesson_repository
from app.providers.guard import BudgetStopped
from app.providers.router import chain_for
from app.providers.subscription import SubscriptionAuthFailed, SubscriptionLimitReached
from app.session import diagnostic_session, preview, probes, service

router = APIRouter(prefix="/sessions", tags=["sessions"])


def body_of(payload):
   return payload or {}


def known_scope_ids(context, scope):
   is_archetype_scope = scope == "archetype"

   if is_archetype_scope:
      return set(context.archetypes)

   return set(context.graph.skills)


def today_of(fields):
   try:
      return preview.assembly_day(fields.get("today"))
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable


def assembly_inputs_of(settings, user, fields):
   try:
      return preview.user_assembly_inputs(settings.rng_seed, user.id, fields.get("today"))
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable


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


def stored_answer_key(item):
   try:
      return json.loads(item.answer_key)
   except (TypeError, ValueError):
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
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_of(payload)
   context = settings.session_context
   today, rng = assembly_inputs_of(settings, user, fields)
   probe_rows, probe_queue = probes.load_queue(db, user.id, datetime.now(timezone.utc))
   row = service.open_session(
      db,
      user.id,
      fields.get("mode") or "learning",
      context.graph,
      context.engine_graph,
      context.archetypes,
      context.bank,
      context.snapshot_id,
      today,
      rng,
      probes=probe_queue,
      sub_mode=fields.get("sub_mode"),
      process_seed=settings.rng_seed,
      experiment_default=settings.experiment_default_state,
   )
   probes.mark_drained(db, probe_rows, probe_queue, datetime.now(timezone.utc))

   return session_payload(db, row)


@router.get("/{session_id}")
def read_session(session_id: str, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   return session_payload(db, owned_session(db, session_id, user))


@router.get("/{session_id}/next")
def read_next_item(
   session_id: str,
   today: str | None = None,
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   """The stage example prompt is the one the feedback screen repeats, from one function in
   app/feedback/render.py, so the student is asked about the same visible step before and after.

   A diagnostic session chooses its next item here, after the last answer, and finishes itself
   when the engine stops the run; the reply then carries diagnostic_finished.
   """
   row = owned_session(db, session_id, user)

   if diagnostic_session.is_diagnostic(row):
      return next_diagnostic_item(db, settings, row, today_of({"today": today}))

   try:
      item = service.served_item(db, row.id)
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   is_exhausted = item is None

   if is_exhausted:
      return {"item": None}

   if service.is_reading(item):
      return {"item": dict(item, concept_name=concept_name(settings, item.get("concept_id")))}

   prompt = render.pre_submission_prompt(item["stage"], item["served_steps"])

   return {"item": dict(item, self_explanation_prompt=prompt)}


def concept_name(settings, concept_id):
   """The name the lesson top bar reads (15 UI); None when the context carries no snapshot."""
   snapshot = settings.session_context.snapshot
   concepts = getattr(snapshot, "concepts", None) or {}
   record = concepts.get(concept_id) or {}

   return record.get("name")


def diagnostic_advancer(db, settings, row, today):
   context = settings.session_context

   def advance():
      return diagnostic_session.advance(
         db,
         row,
         context.graph,
         context.engine_graph,
         context.bank,
         today,
         settings.rng_seed,
         service.utc_now(),
      )

   return advance


def next_diagnostic_item(db, settings, row, today):
   context = settings.session_context
   advance = diagnostic_advancer(db, settings, row, today)
   item = service.answer_skipped_units(db, row, advance(), today, context.archetypes, context.engine_graph, advance)
   is_finished = item is None

   if is_finished:
      return {"item": None, "diagnostic_finished": True}

   return {"item": dict(item, served_steps=None, self_explanation_prompt=None), "diagnostic_finished": False}


@router.post("/{session_id}/diagnostic/skip-unit")
def skip_diagnostic_unit(
   session_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   """The operator's ruling in the stage 11 brief: "I have not learned this yet" for every
   remaining item of the unit being asked, recorded as that answer is, and nothing else. Replies
   as GET next does."""
   fields = body_of(payload)
   row = owned_session(db, session_id, user)

   if not diagnostic_session.is_diagnostic(row):
      raise HTTPException(status_code=404, detail="this session is not a diagnostic")

   context = settings.session_context
   today = today_of(fields)
   advance = diagnostic_advancer(db, settings, row, today)

   try:
      service.skip_diagnostic_unit(
         db,
         row,
         fields.get("item_id"),
         fields.get("elapsed_ms"),
         today,
         context.archetypes,
         context.engine_graph,
         advance,
      )
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return next_diagnostic_item(db, settings, row, today)


@router.get("/{session_id}/diagnostic")
def read_diagnostic(session_id: str, db=Depends(get_db, scope="function"), settings=Depends(get_settings), user=Depends(current_user)):
   """08 diagnostic result: unit-level states, never a percentage and never a score."""
   row = owned_session(db, session_id, user)

   if not diagnostic_session.is_diagnostic(row):
      raise HTTPException(status_code=404, detail="this session is not a diagnostic")

   return diagnostic_session.result_payload(row, settings.session_context.unit_titles)


@router.post("/{session_id}/attempts")
def submit_attempt(
   session_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
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
         experiment_default=settings.experiment_default_state,
      )
   except ChildDiedError as failure:
      raise HTTPException(
         status_code=503,
         detail="the answer could not be graded just now and was not recorded, so it can be sent again",
      ) from failure
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   shows_correctness = not diagnostic_session.is_diagnostic(row)
   correct = None if attempt.correct is None else bool(attempt.correct)

   return {
      "id": attempt.id,
      "item_id": attempt.item_id,
      "correct": correct if shows_correctness else None,
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
   db=Depends(get_db, scope="function"),
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

   answer = json.loads(attempt.response) if attempt.response else {}
   chosen = chosen_option(item, answer)
   error_path = (chosen or {}).get("error_path")
   error_record = context.errors.get(error_path) if error_path else None
   is_opener = service.served_as_opener(row, attempt)

   graded_item = {
      "worked_solution": item.worked_solution,
      "answer_key": stored_answer_key(item),
      "options": item.options or [],
   }

   try:
      feedback = render.render_feedback(
         attempt.served_stage,
         archetype,
         graded_item,
         submitted=attempt.submitted_at is not None,
         correct=None if attempt.correct is None else bool(attempt.correct),
         chosen_option=chosen,
         error_record=error_record,
         confidence=attempt.confidence,
         is_opener=is_opener,
         answer=answer,
      )
   except ValueError as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   is_comparison = feedback.kind == render.FeedbackKind.COMPARISON

   if is_comparison:
      return dict(render.as_dict(feedback), sentence=None, tutor_unavailable=False, lesson_link=None)

   feedback_arm = switches.recorded_arms(attempt).get(switches.FEEDBACK_ELABORATION)
   is_verification_only = feedback_arm == switches.DEFINITIONS[switches.FEEDBACK_ELABORATION].treatment_arm

   if is_verification_only:
      feedback = render.verification_only(feedback)

   is_correct = feedback.kind == render.FeedbackKind.CORRECT
   reinforces = is_correct and not is_verification_only

   if reinforces:
      sentence, tutor_unavailable = reinforcement_for(settings, db, user, attempt, feedback, archetype, item.worked_solution)
   else:
      sentence, tutor_unavailable = tutor_sentence_for(settings, db, user, attempt, feedback)

   link = None if is_verification_only else lesson_link_for(db, attempt, archetype, error_path, context.graph)

   return dict(render.as_dict(feedback), sentence=sentence, tutor_unavailable=tutor_unavailable, lesson_link=link)


def attempt_diagnoses(db, attempt):
   return db.scalars(select(models.Diagnosis).where(models.Diagnosis.attempt_id == attempt.id)).all()


def is_probe_tied(db, diagnoses):
   """15 By misconception candidate: a top-two tie that writes a probe carries no lesson link, so
   the probe stays uncontaminated (03, Rival handling)."""
   for diagnosis in diagnoses:
      has_scheduled_probe = diagnosis.probe_scheduled is not None
      pending = db.scalars(select(models.PendingProbe.id).where(models.PendingProbe.diagnosis_id == diagnosis.id)).first()

      if has_scheduled_probe or pending is not None:
         return True

   return False


def named_errors(error_path, diagnoses):
   named = [error_path] if error_path else []

   for diagnosis in diagnoses:
      observed = json.loads(diagnosis.observed_errors) if diagnosis.observed_errors else []
      named.extend(error_id for error_id in observed if isinstance(error_id, str))

   return list(dict.fromkeys(named))


def lesson_link_for(db, attempt, archetype, error_path, graph):
   """15 Diagnosis links: the graded option's error_path, or an observed error of the diagnosis,
   names a BC-ERR the item's concept lesson anchors as #err-<id>. The concepts are read in the
   archetype's skills order, primary first, as the first-contact gate reads them."""
   diagnoses = attempt_diagnoses(db, attempt)
   error_ids = named_errors(error_path, diagnoses)
   has_errors = len(error_ids) > 0

   if not has_errors or is_probe_tied(db, diagnoses):
      return None

   servable = lesson_repository.servable_map(db)
   concepts = []

   for skill_id in archetype["skills"]:
      concept_id = (graph.skills.get(skill_id) or {}).get("concept")

      if concept_id is not None and concept_id not in concepts:
         concepts.append(concept_id)

   for concept_id in concepts:
      found = servable.get(concept_id)

      if found is None:
         continue

      row = db.get(models.Lesson, found)
      section_ids = {section["id"] for section in row.body.get("sections", [])}

      for error_id in error_ids:
         anchor = f"{row.id}#err-{error_id}"

         if anchor in section_ids:
            return {"lesson_id": row.id, "version": row.version, "anchor": anchor}

   return None


def tutor_sentence_for(settings, db, user, attempt, feedback):
   """Every tutor call goes through the guard, which is where 07 puts the cap, the accounting
   and the audit trail, and a call that would cross the cap never reaches the provider.

   07's hard-stop table gives the tutor role Stop at the cap, with the practice queue unaffected
   and a line saying the tutor is unavailable for the rest of today. That line is what the second
   return value carries, so the session screen can say it where it happened rather than only in
   settings.

   A subscription usage limit is the same stop from the student's side: static feedback, the
   tutor marked unavailable, and the call queued by app/feedback/tutor.py.

   The tutor runs down its fallback chain (app/providers/router.py): the subscription, paced by
   call counts, then the paid API only when GROWTH_AI_BACKEND=api put it in the chain, each link
   behind its own guard. Only the API link is tracked against the persistent developer spend cap.
   """
   def compose(guarded):
      return tutor.compose_sentence(guarded, feedback, db=db, attempt=attempt, user_id=user.id)

   return tutor_call(settings, db, user, compose)


def reinforcement_for(settings, db, user, attempt, feedback, archetype, worked_solution):
   def compose(guarded):
      return tutor.compose_reinforcement(
         guarded, feedback, archetype, worked_solution, db=db, attempt=attempt, user_id=user.id
      )

   return tutor_call(settings, db, user, compose)


def tutor_call(settings, db, user, compose):
   """One tutor call down the tutor's chain, whichever template composes it. The second value says
   the tutor is unavailable, for the line 07's hard-stop table puts where it happened."""
   guarded = chain_for(settings, db, user.id, "tutor_links", "tutor", settings.tutor_caps)

   if guarded is None:
      return None, False

   try:
      sentence = compose(guarded)
   except BudgetStopped:
      return None, True
   except SubscriptionLimitReached:
      return None, True
   except SubscriptionAuthFailed:
      return None, True

   return sentence, False


@router.post("/{session_id}/attempts/{attempt_id}/confidence")
def submit_confidence(
   session_id: str,
   attempt_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
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
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   """One note per item corrected in this session, per 02's Session assembly block 4.

   An attempt that was right, or that never graded, carries no note, so 06's API surface gains
   this row rather than the attempts route gaining a field.
   """
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   attempted = owned_attempt(db, row, attempt_id)
   is_opener = service.served_as_opener(row, attempted)
   was_corrected = attempted.correct == 0 and not is_opener

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
   except service.ErrorNoteNotOneLine:
      raise HTTPException(status_code=400, detail="the error note is one line")
   except service.ErrorNoteTooLong:
      raise HTTPException(
         status_code=422,
         detail=f"the error note is capped at {service.ERROR_NOTE_MAX_CHARACTERS} characters",
      )

   return {"id": attempt.id, "error_note": attempt.error_note}


@router.post("/{session_id}/attempts/{attempt_id}/self-explanation")
def submit_self_explanation(
   session_id: str,
   attempt_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   """The answer to the one structured prompt of 11 P1 scope 10, written once per attempt."""
   fields = body_of(payload)
   row = owned_session(db, session_id, user)
   owned_attempt(db, row, attempt_id)

   try:
      service.record_self_explanation(db, attempt_id, fields.get("answer"))
   except service.SelfExplanationEmpty as refused:
      raise HTTPException(status_code=422, detail=str(refused)) from refused
   except service.SelfExplanationNotInvited as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused
   except service.SelfExplanationAlreadyWritten as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   stored = db.execute(
      select(models.Attempt.self_explanation).where(models.Attempt.id == attempt_id)
   ).scalar_one()

   return {"attempt_id": attempt_id, "self_explanation": stored}


@router.post("/{session_id}/judgments")
def record_judgment(
   session_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
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
   db=Depends(get_db, scope="function"),
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
