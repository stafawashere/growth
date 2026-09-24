"""Unit checks, timed part drills and the full mock over the database (05, 11 P5).

One lifecycle serves all three. A session row holds the parts; each part holds its questions as
assessment_responses rows, which keep the student's answer, the tools used and the time spent
while the part is open. When a part closes, by submission or when its time runs out, each answered
multiple-choice or short-answer question becomes an attempts row graded against the stored key.

The rules that make it an exam rehearsal rather than practice:

- A timed session is written with updates_mastery 0 and nothing here calls the engine update for
  it, so no skills_state row changes (invariant 17, 11 P5 scope item 6). Its graded errors still
  get the rule diagnosis (D4), except a flagged rapid guess, and a wrong answer re-enters the
  micro-session through the ordinary corrected-item requeue.
- The deadline is the server's. A save after the deadline is refused and the part is closed as it
  stood; a closed part never reopens, and a mock's parts open only in order (scope item 4).
- The unit check is untimed and updates_mastery 1: its observations are applied, with the
  student's ratings, only when the whole check is submitted, so no feedback reaches the student
  before then.

Free-response questions of a timed part get their attempts when the part starts, so the booklet
pages can be printed; capture, read-back and grading then run through app/grading/service.py,
which credits the engine only in a unit check.
"""
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import select

from app.assessment import assemble, band, pacing, shape
from app.checkpoint import published
from app.db import models
from app.engine.prior import p_compensatory, p_knowledge
from app.engine.select import retrievability_map
from app.engine.state import FadingStage, MasteryState, ResponseFormat
from app.engine.update import rule_based_mastery_states
from app.frq.items import FRQ_FORMAT, served_record
from app.grading import service as grading
from app.items.grade import grade
from app.runtime.bank import as_served_item
from app.session import repository
from app.session import service as session_service
from app.session.diagnoses import write_rule_diagnosis

MOCK = "mock"
PART_DRILL = "part_drill"
UNIT_CHECK = "unit_check"
TIMED_MODES = (MOCK, PART_DRILL)
FULL_MOCK_SUB_MODE = "full_mock"

MULTIPLE_CHOICE_KIND = "mcq"
FREE_RESPONSE_KIND = "frq"

CLOSED_BY_SUBMISSION = "submitted"
CLOSED_BY_TIME = "time"

NOT_STARTED = "not_started"
OPEN = "open"
CLOSED = "closed"

ANSWER_FIELDS = ("option_id", "mathjson", "units")

UNIT_CHECK_PART_KEY = "unit"


class AssessmentRefused(ValueError):
   """A step out of order, after the deadline, or on a closed part. The message is shown."""


@dataclass
class AssessmentContext:
   archetypes: dict
   errors: dict
   engine_graph: Any
   frq: Any = None
   graph: Any = None
   snapshot: Any = None
   extras: dict = field(default_factory=dict)


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def stamp(moment):
   return moment.isoformat()


def utc_now():
   return datetime.now(timezone.utc)


def parsed(moment_text):
   return datetime.fromisoformat(moment_text)


def is_timed(session_row):
   return session_row.mode in TIMED_MODES


def queue_of(session_row):
   return json.loads(session_row.queue)


def parts_of(db, session_id):
   return db.scalars(
      select(models.AssessmentPart)
      .where(models.AssessmentPart.session_id == session_id)
      .order_by(models.AssessmentPart.position)
   ).all()


def responses_of(db, part_id):
   return db.scalars(
      select(models.AssessmentResponse)
      .where(models.AssessmentResponse.part_id == part_id)
      .order_by(models.AssessmentResponse.number)
   ).all()


def part_status(part):
   if part.closed_at is not None:
      return CLOSED

   if part.started_at is not None:
      return OPEN

   return NOT_STARTED


def new_part_row(user_id, session_id, position, part_shape, now, timed=True):
   return models.AssessmentPart(
      id=new_id("APT"),
      user_id=user_id,
      session_id=session_id,
      position=position,
      exam_part=part_shape.key,
      question_type=part_shape.question_type,
      calculator=int(part_shape.calculator_required),
      minutes=part_shape.minutes if timed else None,
      question_count=part_shape.questions,
      started_at=None,
      deadline_at=None,
      closed_at=None,
      closed_by=None,
      time_remaining_ms=None,
      created_at=stamp(now),
      updated_at=stamp(now),
   )


def new_response_row(user_id, session_id, part_id, number, item_id, kind, served_format, now):
   return models.AssessmentResponse(
      id=new_id("ARS"),
      user_id=user_id,
      session_id=session_id,
      part_id=part_id,
      number=number,
      item_id=item_id,
      kind=kind,
      served_format=served_format,
      answer=None,
      first_answered_at=None,
      answered_at=None,
      time_ms=0,
      visits=0,
      visits_after_answer=0,
      marked=0,
      eliminated="[]",
      eliminator_used=0,
      notes=None,
      highlights="[]",
      confidence=None,
      attempt_id=None,
      correct=None,
      rapid_guess=None,
      created_at=stamp(now),
      updated_at=stamp(now),
   )


def open_timed(db, user_id, context, part_keys, snapshot_id, now, rng, capture_mode="photo"):
   """A full mock when part_keys is every part, a part drill when it is one."""
   is_full_mock = tuple(part_keys) == shape.part_keys()
   is_single_part = len(part_keys) == 1

   if not is_full_mock and not is_single_part:
      raise AssessmentRefused("a timed session is one part or the whole exam in order")

   if capture_mode not in grading.CAPTURE_MODES:
      raise AssessmentRefused(f"capture mode must be one of {grading.CAPTURE_MODES}")

   mode = MOCK if is_full_mock else PART_DRILL
   shapes = [shape.part_shape(key) for key in part_keys]
   session_row = models.Session(
      id=new_id("SES"),
      user_id=user_id,
      mode=mode,
      sub_mode=FULL_MOCK_SUB_MODE if is_full_mock else part_keys[0],
      started_at=stamp(now),
      ended_at=None,
      queue="{}",
      updates_mastery=0,
      snapshot_id=snapshot_id,
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(session_row)
   frq_ids = []
   taken_items = []

   for position, part_shape in enumerate(shapes, start=1):
      part = new_part_row(user_id, session_row.id, position, part_shape, now)
      db.add(part)
      number = shape.first_number(part_shape)

      if part_shape.is_multiple_choice:
         rows = assemble.multiple_choice_items(
            db, user_id, context.archetypes, part_shape.calculator_required, part_shape.questions, rng, excluded_ids=taken_items
         )
         taken_items.extend(row.id for row in rows)

         for offset, row in enumerate(rows):
            db.add(new_response_row(user_id, session_row.id, part.id, number + offset, row.id, MULTIPLE_CHOICE_KIND, ResponseFormat.MCQ.value, now))
      else:
         has_bank = context.frq is not None

         if not has_bank:
            raise assemble.AssessmentUnavailable("the free-response bank is not loaded")

         records = assemble.free_response_questions(
            db, user_id, context.frq, part_shape.calculator_required, part_shape.questions, rng, excluded_ids=frq_ids
         )
         frq_ids.extend(record["id"] for record in records)

         for offset, record in enumerate(records):
            db.add(new_response_row(user_id, session_row.id, part.id, number + offset, record["id"], FREE_RESPONSE_KIND, FRQ_FORMAT, now))

   session_row.queue = json.dumps({"kind": mode, "parts": list(part_keys), "frq": frq_ids, "capture_mode": capture_mode})
   db.flush()

   return session_row


def expire_if_due(db, context, session_row, part, now):
   """Closes an open timed part whose deadline has passed, as the student left it."""
   is_open = part_status(part) == OPEN
   has_deadline = part.deadline_at is not None
   is_past = has_deadline and now >= parsed(part.deadline_at)

   if is_open and is_past:
      close_part(db, context, session_row, part, CLOSED_BY_TIME, now)

   return part


def expire_all(db, context, session_row, now):
   for part in parts_of(db, session_row.id):
      expire_if_due(db, context, session_row, part, now)


def part_at(db, session_row, position):
   for part in parts_of(db, session_row.id):
      if part.position == position:
         return part

   raise AssessmentRefused(f"this session has no part {position}")


def start_part(db, context, session_row, position, now):
   expire_all(db, context, session_row, now)
   parts = parts_of(db, session_row.id)
   part = part_at(db, session_row, position)
   status = part_status(part)

   if status == CLOSED:
      raise AssessmentRefused("this part is closed and cannot be reopened")

   if status == OPEN:
      return part

   earlier_open = [other for other in parts if other.position < position and part_status(other) != CLOSED]

   if earlier_open:
      raise AssessmentRefused("the parts run in order; finish the earlier part first")

   another_open = [other for other in parts if other.id != part.id and part_status(other) == OPEN]

   if another_open:
      raise AssessmentRefused("another part is open")

   part.started_at = stamp(now)
   has_timer = part.minutes is not None

   if has_timer:
      part.deadline_at = stamp(now + timedelta(minutes=part.minutes))

   part.updated_at = stamp(now)
   start_free_response_attempts(db, context, session_row, part, now)
   db.flush()

   return part


def start_free_response_attempts(db, context, session_row, part, now):
   capture_mode = queue_of(session_row).get("capture_mode") or "photo"

   for response in responses_of(db, part.id):
      is_free_response = response.kind == FREE_RESPONSE_KIND

      if not is_free_response:
         continue

      record = context.frq.record(response.item_id)
      attempt = grading.start_attempt(db, session_row, record, capture_mode, now)
      response.attempt_id = attempt.id


def open_part_or_refuse(db, context, session_row, position, now):
   part = part_at(db, session_row, position)
   expire_if_due(db, context, session_row, part, now)
   status = part_status(part)

   if status == CLOSED:
      closed_by_time = part.closed_by == CLOSED_BY_TIME
      reason = "time ran out on this part, so it closed as you left it" if closed_by_time else "this part is closed and cannot be reopened"
      raise AssessmentRefused(reason)

   if status == NOT_STARTED:
      raise AssessmentRefused("this part has not started")

   return part


def stored_answer(answer):
   is_mapping = isinstance(answer, dict)

   if not is_mapping:
      return None

   kept = {name: answer[name] for name in ANSWER_FIELDS if name in answer and answer[name] is not None}

   return kept or None


def save_response(db, context, session_row, position, number, fields, now):
   """Records what the student did on one question: the answer, a visit's time, the flag, the
   eliminated options, notes and highlights, and for a unit check the confidence rating."""
   part = open_part_or_refuse(db, context, session_row, position, now)
   response = db.scalar(
      select(models.AssessmentResponse)
      .where(models.AssessmentResponse.part_id == part.id)
      .where(models.AssessmentResponse.number == number)
   )

   if response is None:
      raise AssessmentRefused(f"this part has no question {number}")

   visit_ms = fields.get("visit_ms")
   has_visit = isinstance(visit_ms, int) and visit_ms >= 0

   if has_visit:
      visit_started = now - timedelta(milliseconds=visit_ms)
      answered_before_the_visit = response.first_answered_at is not None and parsed(response.first_answered_at) <= visit_started
      response.time_ms += visit_ms
      response.visits += 1

      if answered_before_the_visit:
         response.visits_after_answer += 1

   if "answer" in fields:
      is_free_response = response.kind == FREE_RESPONSE_KIND

      if is_free_response:
         raise AssessmentRefused("a free-response answer is written in the booklet and captured after the part")

      answer = stored_answer(fields.get("answer"))
      response.answer = json.dumps(answer) if answer is not None else None

      if answer is not None:
         response.answered_at = stamp(now)
         response.first_answered_at = response.first_answered_at or stamp(now)

   if "marked" in fields:
      response.marked = int(bool(fields.get("marked")))

   if "eliminated" in fields:
      eliminated = [str(option_id) for option_id in (fields.get("eliminated") or [])]
      response.eliminated = json.dumps(sorted(set(eliminated)))

      if eliminated:
         response.eliminator_used = 1

   if "notes" in fields:
      response.notes = str(fields.get("notes") or "")[:2000] or None

   if "highlights" in fields:
      response.highlights = json.dumps(list(fields.get("highlights") or [])[:50])

   if "confidence" in fields:
      confidence = fields.get("confidence")
      is_rating = confidence in (None, "guess", "unsure", "confident")

      if not is_rating:
         raise AssessmentRefused("confidence is guess, unsure or confident")

      response.confidence = confidence

   response.updated_at = stamp(now)
   db.flush()

   return response


def submit_part(db, context, session_row, position, now):
   part = open_part_or_refuse(db, context, session_row, position, now)
   close_part(db, context, session_row, part, CLOSED_BY_SUBMISSION, now)

   return part


def close_part(db, context, session_row, part, closed_by, now):
   has_deadline = part.deadline_at is not None
   remaining_ms = 0

   if has_deadline:
      remaining_ms = max(0, int((parsed(part.deadline_at) - now).total_seconds() * 1000))

   part.closed_at = stamp(min(now, parsed(part.deadline_at)) if has_deadline else now)
   part.closed_by = closed_by
   part.time_remaining_ms = remaining_ms if has_deadline else None
   part.updated_at = stamp(now)
   grade_part(db, context, session_row, part, now)
   db.flush()


def grade_part(db, context, session_row, part, now):
   for response in responses_of(db, part.id):
      is_free_response = response.kind == FREE_RESPONSE_KIND
      is_answered = response.answer is not None

      if is_free_response or not is_answered:
         continue

      archetype = context.archetypes[db.get(models.Item, response.item_id).archetype_id]

      if is_timed(session_row):
         latencies = pacing.untimed_latencies(db, session_row.user_id, archetype["id"])
         threshold = pacing.rapid_guess_threshold_seconds(archetype, latencies)
         response.rapid_guess = int(pacing.is_rapid_guess(response, part, threshold))

      attempt = write_attempt(db, context, session_row, response, archetype, now)
      response.attempt_id = attempt.id
      response.correct = attempt.correct
      response.updated_at = stamp(now)


def write_attempt(db, context, session_row, response, archetype, now):
   """The attempts row for one answered question, as the micro-session writes it, with the rule
   diagnosis unless the answer was a flagged rapid guess (05: a guess tells no story)."""
   item_row = db.get(models.Item, response.item_id)
   answer = json.loads(response.answer)
   submission = {
      "selected_option_id": answer.get("option_id"),
      "mathjson": answer.get("mathjson"),
      "units": answer.get("units"),
   }
   verdict = grade(item_row, submission, context.errors, served_format=response.served_format)
   graded_answer = {**answer, **verdict}
   is_graded = verdict.get("correct") is not None

   if is_graded:
      per_skill_states = rule_based_mastery_states(archetype, graded_answer)
   else:
      per_skill_states = {skill: MasteryState.NOT_ATTEMPTED for skill in archetype["skills"]}

   states = repository.load_states(db, session_row.user_id)
   retrievability = retrievability_map(states, now.date())
   first_seen = parsed(response.created_at)
   confidence = response.confidence if session_row.mode == UNIT_CHECK else None
   attempt = models.Attempt(
      id=new_id("ATT"),
      session_id=session_row.id,
      item_id=response.item_id,
      started_at=stamp(first_seen),
      submitted_at=stamp(now),
      response=json.dumps(answer),
      confidence=confidence,
      confidence_source=session_service.CONFIDENCE_FROM_STUDENT if confidence else None,
      elapsed_ms=response.time_ms or None,
      correct=int(bool(verdict["correct"])) if is_graded else None,
      p_split=p_knowledge(archetype, states, context.engine_graph.hard_parents, retrievability),
      p_compensatory=p_compensatory(archetype, states, retrievability),
      served_stage=FadingStage.UNSUPPORTED.value,
      format=response.served_format,
      per_skill_states=json.dumps({skill: state.value for skill, state in per_skill_states.items()}),
      snapshot_id=session_row.snapshot_id,
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(attempt)
   db.flush()
   is_guess = bool(response.rapid_guess)

   if is_graded and not is_guess:
      write_rule_diagnosis(db, attempt.id, per_skill_states, graded_answer, now)

   return attempt


def item_for_response(db, context, response, part):
   if response.kind == FREE_RESPONSE_KIND:
      record = context.frq.record(response.item_id)
      served = served_record(record)
      served["radian_note"] = assemble.radian_note_applies(
         " ".join([record["stem"]["text"]] + [part_entry["prompt"] for part_entry in record["parts"]]),
         bool(part.calculator),
      )

      return served

   row = db.get(models.Item, response.item_id)

   return assemble.served_multiple_choice(row, bool(part.calculator)) if response.kind == MULTIPLE_CHOICE_KIND else dict(as_served_item(row), radian_note=False)


def response_payload(db, context, response, part, with_item):
   payload = {
      "number": response.number,
      "kind": response.kind,
      "format": response.served_format,
      "answer": json.loads(response.answer) if response.answer else None,
      "marked": bool(response.marked),
      "eliminated": json.loads(response.eliminated),
      "notes": response.notes,
      "highlights": json.loads(response.highlights),
      "confidence": response.confidence,
      "time_ms": response.time_ms,
      "attempt_id": response.attempt_id,
   }

   if with_item:
      payload["item"] = item_for_response(db, context, response, part)

   return payload


def free_response_capture(db, context, response, part):
   """What the capture step needs for one question: the attempt, and the question itself, which
   the student may read again once the part is closed because nothing more is written."""
   attempt = db.get(models.Attempt, response.attempt_id) if response.attempt_id else None

   return {
      "number": response.number,
      "item_id": response.item_id,
      "attempt_id": response.attempt_id,
      "grading_state": attempt.grading_state if attempt is not None else None,
      "item": item_for_response(db, context, response, part),
   }


def untimed_part_payload(part):
   return {
      "key": part.exam_part,
      "label": "Unit check",
      "multiple_choice": True,
      "question_count": part.question_count,
      "minutes": None,
      "calculator": False,
      "calculator_label": None,
      "calculator_note": None,
      "first_number": 1,
      "budget_seconds_per_question": None,
      "tools": [],
   }


def part_payload(db, context, session_row, part, now):
   is_unit_check = part.exam_part == UNIT_CHECK_PART_KEY
   status = part_status(part)
   responses = responses_of(db, part.id)

   if is_unit_check:
      return dict(
         untimed_part_payload(part),
         position=part.position,
         status=status,
         timed=False,
         started_at=part.started_at,
         deadline_at=None,
         closed_at=part.closed_at,
         closed_by=part.closed_by,
         time_remaining_ms=None,
         answered=sum(1 for response in responses if response.answer is not None),
         questions=[response_payload(db, context, response, part, with_item=True) for response in responses] if status == OPEN else [],
      )

   part_shape = shape.part_shape(part.exam_part)
   responses = responses_of(db, part.id)
   shows_questions = status == OPEN
   remaining_ms = None

   if status == OPEN and part.deadline_at is not None:
      remaining_ms = max(0, int((parsed(part.deadline_at) - now).total_seconds() * 1000))

   payload = dict(
      shape.part_payload(part_shape),
      position=part.position,
      status=status,
      timed=part.minutes is not None,
      started_at=part.started_at,
      deadline_at=part.deadline_at,
      closed_at=part.closed_at,
      closed_by=part.closed_by,
      time_remaining_ms=remaining_ms if status == OPEN else part.time_remaining_ms,
      answered=sum(1 for response in responses if response.answer is not None),
      questions=[response_payload(db, context, response, part, with_item=True) for response in responses] if shows_questions else [],
   )
   is_free_response_part = not part_shape.is_multiple_choice

   if is_free_response_part and status != NOT_STARTED:
      payload["capture"] = [free_response_capture(db, context, response, part) for response in responses]

   return payload


def session_payload(db, context, session_row, now):
   expire_all(db, context, session_row, now)
   parts = parts_of(db, session_row.id)
   template = shape.form_template()
   payload = {
      "id": session_row.id,
      "mode": session_row.mode,
      "sub_mode": session_row.sub_mode,
      "updates_mastery": bool(session_row.updates_mastery),
      "started_at": session_row.started_at,
      "ended_at": session_row.ended_at,
      "capture_mode": queue_of(session_row).get("capture_mode"),
      "parts": [part_payload(db, context, session_row, part, now) for part in parts],
      "closed_part_note": template["closed_part_note"],
      "break_note": template["break_note"],
      "reference_sheet": template["reference_sheet"],
      "radian_note": template["radian_note"],
   }
   db.flush()

   return payload


def free_response_points(db, context, responses):
   """Per exam question number: points earned, points still pending and points possible."""
   points = {}

   for response in responses:
      record = context.frq.record(response.item_id)
      possible = assemble.question_points(record)
      earned = 0
      decided = 0

      if response.attempt_id is not None:
         for row in grading.gradings_of(db, response.attempt_id):
            is_decided = not row.provisional and row.earned is not None

            if is_decided:
               decided += 1
               earned += int(row.earned == 1)

      points[response.number] = {"earned": earned, "pending": possible - decided, "possible": possible}

   return points


def captured_numbers(db, responses):
   captured = []

   for response in responses:
      attempt = db.get(models.Attempt, response.attempt_id) if response.kind == FREE_RESPONSE_KIND and response.attempt_id else None
      is_captured = attempt is not None and bool(attempt.transcription_confirmed)

      if is_captured:
         captured.append(response.number)

   return captured


def results(db, context, session_row, now):
   """Pacing per part for every timed session; for a full mock, the band and the per-question
   comparison as well."""
   expire_all(db, context, session_row, now)
   parts = parts_of(db, session_row.id)
   every_part_closed = all(part_status(part) == CLOSED for part in parts)
   pacing_rows = []
   mcq_correct = 0
   mcq_total = 0
   frq_responses = []

   for part in parts:
      part_shape = shape.part_shape(part.exam_part)
      responses = responses_of(db, part.id)
      pacing_rows.append(pacing.part_pacing(part, part_shape, responses, captured_numbers(db, responses)))

      if part_shape.is_multiple_choice:
         mcq_total += len(responses)
         mcq_correct += sum(1 for response in responses if response.correct == 1)
      else:
         frq_responses.extend(responses)

   payload = {
      "id": session_row.id,
      "mode": session_row.mode,
      "complete": every_part_closed,
      "pacing": pacing_rows,
      "multiple_choice": {"correct": mcq_correct, "total": mcq_total} if mcq_total else None,
   }
   points = free_response_points(db, context, frq_responses) if frq_responses else {}

   if points:
      payload["free_response"] = {
         "earned": sum(entry["earned"] for entry in points.values()),
         "pending": sum(entry["pending"] for entry in points.values()),
         "total": sum(entry["possible"] for entry in points.values()),
      }
      payload["questions"] = band.question_comparison(points)

   is_full_mock = session_row.mode == MOCK

   if is_full_mock and every_part_closed:
      frq_total = shape.free_response_total() * published.points_per_free_response_question()
      estimate = band.result_payload(
         mcq_correct,
         shape.multiple_choice_total(),
         payload["free_response"]["earned"],
         payload["free_response"]["pending"],
         frq_total,
         points,
      )
      payload.update(estimate)

   return payload


def finish_mock(db, context, session_row, now):
   if session_row.mode != MOCK:
      raise AssessmentRefused("only a full mock is finished with a band")

   payload = results(db, context, session_row, now)

   if not payload["complete"]:
      raise AssessmentRefused("every part must be closed before the mock is finished")

   row = db.scalar(select(models.MockResult).where(models.MockResult.session_id == session_row.id))
   is_new = row is None

   if is_new:
      row = models.MockResult(id=new_id("MKR"), user_id=session_row.user_id, session_id=session_row.id, created_at=stamp(now))
      db.add(row)

   row.taken_at = session_row.started_at
   row.mcq_correct = payload["multiple_choice"]["correct"]
   row.mcq_total = payload["multiple_choice"]["total"]
   row.frq_points = payload["free_response"]["earned"]
   row.frq_pending = payload["free_response"]["pending"]
   row.frq_total = payload["free_response"]["total"]
   row.band_low = payload["band"]["low"]
   row.band_high = payload["band"]["high"]
   row.payload = json.dumps(payload)
   row.updated_at = stamp(now)
   session_row.ended_at = session_row.ended_at or stamp(now)
   session_row.updated_at = stamp(now)
   db.flush()

   return payload


def mock_history(db, user_id):
   rows = db.scalars(
      select(models.MockResult).where(models.MockResult.user_id == user_id).order_by(models.MockResult.taken_at)
   ).all()

   return [
      {
         "session_id": row.session_id,
         "taken_at": row.taken_at,
         "band": {"low": row.band_low, "high": row.band_high},
         "multiple_choice": {"correct": row.mcq_correct, "total": row.mcq_total},
         "free_response": {"earned": row.frq_points, "pending": row.frq_pending, "total": row.frq_total},
      }
      for row in rows
   ]


def captures_done(db, parts):
   """Every free-response question of the parts has been captured and graded."""
   for part in parts:
      for response in responses_of(db, part.id):
         is_free_response = response.kind == FREE_RESPONSE_KIND
         attempt = db.get(models.Attempt, response.attempt_id) if response.attempt_id else None
         is_graded = attempt is not None and attempt.grading_state in (grading.GRADED, grading.PARTLY_GRADED)

         if is_free_response and not is_graded:
            return False

   return True


def unfinished(db, user_id):
   """Every assessment the student started and has not finished, newest first, so a reload or a
   closed tab can resume it. A mock is finished once its result is stored; a drill or a unit check
   once every part is closed and every free-response question in it is graded."""
   rows = db.scalars(
      select(models.Session)
      .where(models.Session.user_id == user_id)
      .where(models.Session.mode.in_((MOCK, PART_DRILL, UNIT_CHECK)))
      .order_by(models.Session.started_at.desc())
   ).all()
   finished_mocks = set(db.scalars(select(models.MockResult.session_id).where(models.MockResult.user_id == user_id)).all())
   listed = []

   for session_row in rows:
      parts = parts_of(db, session_row.id)
      has_parts = len(parts) > 0

      if not has_parts:
         continue

      closed = sum(1 for part in parts if part_status(part) == CLOSED)
      is_mock = session_row.mode == MOCK
      every_part_closed = closed == len(parts)
      is_finished = session_row.id in finished_mocks if is_mock else every_part_closed and captures_done(db, parts)

      if is_finished:
         continue

      listed.append({
         "id": session_row.id,
         "mode": session_row.mode,
         "sub_mode": session_row.sub_mode,
         "started_at": session_row.started_at,
         "parts_closed": closed,
         "parts_total": len(parts),
      })

   return listed
