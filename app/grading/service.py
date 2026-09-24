"""The free-response path from photograph to graded points, over the database.

The order is fixed and each step refuses to run out of it:

1. start_attempt opens a free-response attempt inside one of the four modes per-point grading may
   run in (R10: unit check, part drill, mock, six-week checkpoint). Anywhere else it refuses.
2. add_image runs the quality gate (app/capture/quality.py) and stores the photograph with its
   verdict. A rejected photograph never reaches a provider.
3. read_back sends the accepted photographs to the transcriber and stores the read-back, which
   stays unconfirmed.
4. confirm_read_back stores the student's confirmed or corrected read-back and sets
   transcription_confirmed. A correction after grading invalidates the grading and reverses its
   credit (03, "Transcription errors").
5. grade refuses unless the read-back is confirmed (test_readback_gate), then decides every point
   (app/grading/point.py), writes one gradings row per point and a grading_split review_queue row
   per escalated point, runs the diagnostician when a point was lost, and applies engine credit
   from the non-provisional points only.
6. reread is the student's one-click dispute on a point: a dispute review_queue row visible to the
   student, a fresh three-sample judgement of that point, and the credit recomputed.

Typed entry (submit_typed) is the secondary mode: the student's typed lines are the read-back,
confirmed by construction, and grading proceeds from step 5.

Every write is flushed, never committed: the route owns the transaction.
"""
import json
import uuid
from datetime import date, timedelta

from sqlalchemy import select

from app.auth.service import write_audit
from app.capture import quality
from app.db import models
from app.diagnosis import diagnose as diagnosis_module
from app.diagnosis.observe import ObservationFailed, observe
from app.engine import constants
from app.engine.state import Confidence, FadingStage, MasteryState, ResponseFormat
from app.engine.strength import probability
from app.engine.update import Observation as EngineObservation, apply_observation
from app.frq.items import FRQ_FORMAT
from app.grading import point as grader
from app.grading import transcribe
from app.session import repository

GRADED_MODES = ("unit_check", "part_drill", "mock", "checkpoint")
MASTERY_MODES = ("unit_check",)
CAPTURE_MODES = ("photo", "typed")

CAPTURING = "capturing"
AWAITING_CONFIRMATION = "awaiting_confirmation"
CONFIRMED = "confirmed"
GRADED = "graded"
PARTLY_GRADED = "partly_graded"

GRADING_SPLIT = "grading_split"
DISPUTE = "dispute"
DIAGNOSED_BY_MODEL = "diagnostician_v1"
DIAGNOSED_BY_RULE_ONLY = "diagnostician_v1_rule_only"


class GradingRefused(Exception):
   """A step asked for out of order or outside the modes it may run in. The message is shown."""


class ReadBackNotConfirmed(GradingRefused):
   pass


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def stamp(now):
   return now.isoformat()


def is_graded_mode(session_row):
   return session_row.mode in GRADED_MODES


def start_attempt(db, session_row, record, capture_mode, now):
   if not is_graded_mode(session_row):
      raise GradingRefused(
         f"free-response grading runs only in a unit check, part drill, mock or checkpoint, not in {session_row.mode}"
      )

   if capture_mode not in CAPTURE_MODES:
      raise GradingRefused(f"capture mode must be one of {CAPTURE_MODES}")

   existing = db.scalar(
      select(models.Attempt)
      .where(models.Attempt.session_id == session_row.id)
      .where(models.Attempt.item_id == record["id"])
   )

   if existing is not None:
      return existing

   attempt = models.Attempt(
      id=new_id("ATT"),
      session_id=session_row.id,
      item_id=record["id"],
      started_at=stamp(now),
      submitted_at=None,
      response=json.dumps({"capture_mode": capture_mode}),
      served_stage=FadingStage.UNSUPPORTED.value,
      format=FRQ_FORMAT,
      per_skill_states=json.dumps({skill_id: MasteryState.NOT_ATTEMPTED.value for skill_id in record["skills"]}),
      transcription_confirmed=0,
      capture_mode=capture_mode,
      grading_state=CAPTURING,
      snapshot_id=session_row.snapshot_id,
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(attempt)
   db.flush()

   return attempt


def live_images(db, attempt_id):
   return db.scalars(
      select(models.FrqImage)
      .where(models.FrqImage.attempt_id == attempt_id)
      .where(models.FrqImage.deleted_at.is_(None))
      .order_by(models.FrqImage.created_at)
   ).all()


def add_image(db, attempt, user_id, data, declared_media_type, now):
   if attempt.transcription_confirmed:
      raise GradingRefused("this answer has already been confirmed; start a new capture to change it")

   verdict = quality.check_image(data, declared_media_type)
   row = models.FrqImage(
      id=new_id("IMG"),
      attempt_id=attempt.id,
      user_id=user_id,
      media_type=verdict.media_type or declared_media_type or "application/octet-stream",
      data=data,
      width=verdict.width,
      height=verdict.height,
      sha256=verdict.sha256,
      quality=json.dumps(verdict.as_record()),
      accepted=int(verdict.accepted),
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(row)
   attempt.updated_at = stamp(now)
   db.flush()

   return row, verdict


def read_back(db, attempt, record, provider, now):
   """The transcriber reads the latest photograph that passed the gate, because the booklet is one
   page per question and an earlier accepted photograph is a retake the student replaced. Nothing
   here grades."""
   if attempt.transcription_confirmed:
      raise GradingRefused("this read-back is already confirmed")

   accepted = [image for image in live_images(db, attempt.id) if image.accepted]
   has_accepted = len(accepted) > 0

   if not has_accepted:
      raise GradingRefused("no photograph has passed the image check yet")

   if provider is None:
      raise GradingRefused("no transcriber is configured; the typed mode still works")

   latest = accepted[-1:]
   transcription = transcribe.transcribe(provider, record, [transcribe.image_input(image) for image in latest])
   attempt.transcription = json.dumps({"read": transcription, "confirmed": None})
   attempt.image_ids = json.dumps([image.id for image in latest])
   attempt.grading_state = AWAITING_CONFIRMATION
   attempt.updated_at = stamp(now)
   db.flush()

   return transcription


def stored_transcription(attempt):
   has_transcription = attempt.transcription is not None

   return json.loads(attempt.transcription) if has_transcription else {"read": None, "confirmed": None}


def confirmed_work(attempt):
   return stored_transcription(attempt).get("confirmed")


def confirm_read_back(db, attempt, record, submitted, now, engine_graph=None, user_id=None):
   stored = stored_transcription(attempt)
   original = stored.get("read")
   has_original = original is not None

   if not has_original:
      raise GradingRefused("there is no read-back to confirm yet")

   confirmed = original if submitted is None else transcribe.corrected_transcription(record, submitted)
   was_confirmed = bool(attempt.transcription_confirmed)
   previous_confirmed = stored.get("confirmed")
   changes_confirmed_work = was_confirmed and transcribe.transcription_differs(previous_confirmed or {}, confirmed)

   if changes_confirmed_work:
      invalidate_grading(db, attempt, engine_graph, user_id, now, "the read-back was corrected after grading")

   attempt.transcription = json.dumps({"read": original, "confirmed": confirmed})
   attempt.transcription_confirmed = 1
   attempt.transcription_corrected = int(transcribe.transcription_differs(original, confirmed))
   attempt.grading_state = CONFIRMED
   attempt.submitted_at = attempt.submitted_at or stamp(now)
   attempt.updated_at = stamp(now)
   db.flush()

   return confirmed


def submit_typed(db, attempt, record, submitted, now):
   """Typed entry: what the student typed is the read-back, confirmed by construction."""
   if attempt.capture_mode != "typed":
      raise GradingRefused("this answer is being captured by photograph")

   confirmed = transcribe.corrected_transcription(record, submitted)
   attempt.transcription = json.dumps({"read": confirmed, "confirmed": confirmed})
   attempt.transcription_confirmed = 1
   attempt.transcription_corrected = 0
   attempt.grading_state = CONFIRMED
   attempt.submitted_at = stamp(now)
   attempt.updated_at = stamp(now)
   db.flush()

   return confirmed


def gradings_of(db, attempt_id):
   return db.scalars(
      select(models.Grading).where(models.Grading.attempt_id == attempt_id).order_by(models.Grading.created_at, models.Grading.point_id)
   ).all()


def decision_row(attempt_id, decision, now, rereads=0):
   return models.Grading(
      id=new_id("GRD"),
      attempt_id=attempt_id,
      part_id=decision.part_id,
      point_id=decision.point_id,
      point_type_id=decision.point_type_id,
      decided_by=decision.decided_by,
      earned=decision.earned,
      samples=json.dumps(decision.samples),
      agreement=decision.agreement,
      provisional=int(bool(decision.provisional)),
      rationale=decision.rationale,
      rule_field=decision.rule_field,
      evidence_quote=decision.evidence_quote,
      eligibility_note=decision.eligibility_note,
      deterministic_check=json.dumps(decision.deterministic_check) if decision.deterministic_check else None,
      rereads=rereads,
      created_at=stamp(now),
      updated_at=stamp(now),
   )


def open_review(db, kind, ref_id, now, visible_to_student=False):
   row = models.ReviewQueue(
      id=new_id("RVQ"),
      kind=kind,
      ref_id=ref_id,
      opened_at=stamp(now),
      resolved_at=None,
      resolution=None,
      visible_to_student=int(visible_to_student),
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(row)

   return row


def write_decisions(db, attempt, grading, now, previous_rows=()):
   """Replaces the attempt's gradings rows. A row keeps its id and its re-read count across a
   re-grade, so the review screen's links stay good."""
   previous = {row.point_id: row for row in previous_rows}
   written = []

   for decision in grading.decisions:
      old = previous.get(decision.point_id)
      row = decision_row(attempt.id, decision, now, rereads=old.rereads if old is not None else 0)

      if old is not None:
         row.id = old.id
         row.created_at = old.created_at
         db.delete(old)
         db.flush()

      db.add(row)
      written.append(row)

      newly_escalated = decision.decided_by == grader.ESCALATED and (old is None or old.decided_by != grader.ESCALATED)

      if newly_escalated:
         open_review(db, GRADING_SPLIT, row.id, now)

   db.flush()

   return written


def decisions_from_rows(rows):
   return [
      grader.PointDecision(
         part_id=row.part_id,
         point_id=row.point_id,
         point_type_id=row.point_type_id,
         decided_by=row.decided_by,
         earned=row.earned,
         agreement=row.agreement,
         provisional=bool(row.provisional),
         rationale=row.rationale,
         samples=json.loads(row.samples or "[]"),
         rule_field=row.rule_field,
         evidence_quote=row.evidence_quote,
         eligibility_note=row.eligibility_note,
         deterministic_check=json.loads(row.deterministic_check) if row.deterministic_check else None,
      )
      for row in rows
   ]


def part_has_work(work):
   return {
      part_work["part_id"]: any(not line.get("crossed_out") for line in part_work.get("lines", [])) or bool((part_work.get("answer") or "").strip())
      for part_work in (work or {}).get("parts", [])
   }


def credited_decisions(decisions):
   """Provisional points move no engine credit until they are decided (03, "Provisional display")."""
   return [decision for decision in decisions if not decision.provisional]


def observe_lost_points(record, decisions, work, library, provider):
   """The diagnostician's model call, made before anything is written, so no write transaction is
   held open while it runs (SQLite admits one writer, and a capture of the next question must not
   wait on this call). Returns (observation, diagnosed_by)."""
   lost_ids = {decision.point_id for decision in decisions if decision.earned == 0}
   lost_points = [point for part in record["parts"] for point in part["points"] if point["point_id"] in lost_ids]
   lost_skills = {skill_id for point in lost_points for skill_id in point["skills"]}
   has_lost = len(lost_ids) > 0

   if has_lost and provider is not None:
      try:
         return observe(provider, record, decisions, work, library, lost_skills), DIAGNOSED_BY_MODEL
      except ObservationFailed:
         pass

   return diagnosis_module.Observation(), DIAGNOSED_BY_RULE_ONLY


def run_diagnosis(db, attempt, record, decisions, work, library, confidence, strengths, now, observed):
   observation, diagnosed_by = observed
   result = diagnosis_module.diagnose(
      record,
      credited_decisions(decisions),
      observation,
      library,
      confidence=confidence,
      strengths=strengths,
      part_has_work=part_has_work(work),
   )
   write_diagnosis(db, attempt, result, diagnosed_by, now)

   return result


def write_diagnosis(db, attempt, result, diagnosed_by, now):
   for old in db.scalars(select(models.Diagnosis).where(models.Diagnosis.attempt_id == attempt.id)).all():
      db.delete(old)

   gaps = result["prerequisite_gaps"]
   signals = [entry["signal_id"] for entry in result["per_skill_mastery_state"] if entry.get("signal_id")]
   probe = result["recommended_probe"]
   row = models.Diagnosis(
      id=new_id("DGN"),
      attempt_id=attempt.id,
      observed_errors=json.dumps(result["observed_errors"]),
      misconception_hypotheses=json.dumps(result["candidate_misconceptions"]),
      non_conceptual_causes=json.dumps(result["non_conceptual_causes"]),
      prerequisite_gap=gaps[0]["prerequisite_id"] if gaps else None,
      mastery_states=json.dumps({entry["skill_id"]: entry["mastery_state"] for entry in result["per_skill_mastery_state"]}),
      matched_signal=signals[0] if signals else None,
      probe_scheduled=probe["archetype_id"] if probe else None,
      diagnosed_by=diagnosed_by,
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(row)
   db.flush()
   has_probe = probe is not None

   if has_probe:
      schedule_probe(db, attempt, probe["archetype_id"], row.id, now)

   return row


def schedule_probe(db, attempt, archetype_id, diagnosis_id, now):
   """03 "Rival handling and the probe trigger": the probe goes to pending_probes, which the
   micro-session's selection drains before its own scoring (R6), and expires after
   PROBE_TTL_DAYS. The queue's depth cap is applied when a session loads it."""
   session_row = db.get(models.Session, attempt.session_id)
   probe = models.PendingProbe(
      id=new_id("PRB"),
      user_id=session_row.user_id,
      archetype_id=archetype_id,
      diagnosis_id=diagnosis_id,
      enqueued_at=stamp(now),
      expires_at=stamp(now + timedelta(days=constants.PROBE_TTL_DAYS)),
      served_at=None,
      created_at=stamp(now),
      updated_at=stamp(now),
   )
   db.add(probe)
   db.flush()

   return probe


def reverse_credit(db, attempt, user_id, now):
   """The explicit inverse of the credit this attempt applied (03, "What the student sees for a
   provisional grade"). A row nothing has touched since is restored whole. A row a later attempt
   moved keeps that later movement and loses only this attempt's c and f."""
   has_record = attempt.credit_record is not None

   if not has_record:
      return 0

   record = json.loads(attempt.credit_record)
   rows = {
      row.skill_id: row
      for row in db.scalars(select(models.SkillState).where(models.SkillState.user_id == user_id)).all()
   }
   partial = []

   for skill_id, before in record["before"].items():
      row = rows.get(skill_id)

      if row is None:
         continue

      after = record["after"][skill_id]
      untouched_since = all(getattr(row, column) == value for column, value in without_stamp(after).items())

      if untouched_since:
         for column, value in before.items():
            if column != "updated_at":
               setattr(row, column, value)
      else:
         row.credited_successes = max(0.0, row.credited_successes - (after["credited_successes"] - before["credited_successes"]))
         row.credited_failures = max(0.0, row.credited_failures - (after["credited_failures"] - before["credited_failures"]))
         partial.append(skill_id)

      row.updated_at = stamp(now)

   attempt.credit_record = None
   db.flush()

   if partial:
      write_audit(db, user_id, "grading_rerun", attempt.id, {"credit_reversed_in_part": sorted(partial)}, now=now)

   return len(record["before"])


def without_stamp(values):
   return {column: value for column, value in values.items() if column != "updated_at"}


def apply_credit(db, session_row, attempt, record, states_by_skill, engine_graph, today, now):
   if session_row.mode not in MASTERY_MODES or engine_graph is None:
      return

   states = repository.load_states(db, session_row.user_id)
   before = {skill_id: repository.state_values(state, session_row.snapshot_id, now) for skill_id, state in states.items()}
   observation = EngineObservation(
      archetype_id=record["archetype_id"],
      skills=list(record["skills"]),
      per_skill_states=states_by_skill,
      response_format=ResponseFormat.FREE_RESPONSE,
      confidence=Confidence(attempt.confidence) if attempt.confidence else Confidence.UNSURE,
      elapsed_ms=attempt.elapsed_ms,
      served_stage=FadingStage.UNSUPPORTED,
   )
   apply_observation(states, engine_graph, observation, today)
   after = {skill_id: repository.state_values(state, session_row.snapshot_id, now) for skill_id, state in states.items()}
   changed = [skill_id for skill_id in after if without_stamp(after[skill_id]) != without_stamp(before[skill_id])]
   repository.save_states(db, session_row.user_id, {skill_id: states[skill_id] for skill_id in changed}, session_row.snapshot_id, now)
   attempt.credit_record = json.dumps({
      "applied_at": stamp(now),
      "before": {skill_id: before[skill_id] for skill_id in changed},
      "after": {skill_id: after[skill_id] for skill_id in changed},
   })
   db.flush()


def invalidate_grading(db, attempt, engine_graph, user_id, now, reason):
   rows = gradings_of(db, attempt.id)

   for row in rows:
      db.delete(row)

   if user_id is not None:
      reverse_credit(db, attempt, user_id, now)

   attempt.grading_state = CONFIRMED
   db.flush()

   if rows and user_id is not None:
      write_audit(db, user_id, "grading_rerun", attempt.id, {"reason": reason, "points_cleared": len(rows)}, now=now)


def engine_strengths(db, user_id):
   states = repository.load_states(db, user_id)

   return {skill_id: probability(state) for skill_id, state in states.items()}


def finish(db, session_row, attempt, record, grading, work, context, now, previous_rows=()):
   observed = observe_lost_points(record, grading.decisions, work, context["library"], context.get("diagnostician"))
   rows = write_decisions(db, attempt, grading, now, previous_rows)
   reverse_credit(db, attempt, session_row.user_id, now)
   strengths = engine_strengths(db, session_row.user_id)
   result = run_diagnosis(
      db, attempt, record, grading.decisions, work, context["library"], attempt.confidence, strengths, now, observed,
   )
   states_by_skill = {entry["skill_id"]: entry["mastery_state"] for entry in result["per_skill_mastery_state"]}
   attempt.per_skill_states = json.dumps(states_by_skill)
   apply_credit(db, session_row, attempt, record, states_by_skill, context.get("engine_graph"), context.get("today") or date.today(), now)
   has_pending = any(decision.decided_by == grader.PENDING for decision in grading.decisions)
   attempt.grading_state = PARTLY_GRADED if has_pending else GRADED
   earned_all = all(decision.earned == 1 for decision in grading.decisions)
   attempt.correct = None if has_pending else int(earned_all)
   attempt.updated_at = stamp(now)
   db.flush()

   return rows, result


def grade(db, session_row, attempt, record, context, now):
   """context carries the judge, labels, library, diagnostician provider, engine graph and today."""
   is_confirmed = bool(attempt.transcription_confirmed)

   if not is_confirmed:
      raise ReadBackNotConfirmed("nothing is graded until the read-back is confirmed")

   work = confirmed_work(attempt)
   previous_rows = gradings_of(db, attempt.id)
   stored_samples = {row.point_id: json.loads(row.samples or "[]") for row in previous_rows if row.decided_by in (grader.MODEL, grader.ESCALATED)}
   has_previous = len(previous_rows) > 0

   if has_previous:
      grading = grader.grade_question(record, work, context["labels"], grader.remembering_judge(context.get("judge"), stored_samples, fresh_point_id=None))
   else:
      grading = grader.grade_question(record, work, context["labels"], context.get("judge"))

   return finish(db, session_row, attempt, record, grading, work, context, now, previous_rows)


def reread(db, session_row, attempt, record, grading_row, context, reason, now):
   """The one-click re-read: a dispute row the student can see, and that one point judged afresh.
   The row is resolved once the re-read has run, so a point that splits again can be re-read
   again rather than waiting on a review nobody will do."""
   dispute = open_review(db, DISPUTE, grading_row.id, now, visible_to_student=True)
   point_id = grading_row.point_id
   work = confirmed_work(attempt)
   previous_rows = gradings_of(db, attempt.id)
   stored_samples = {row.point_id: json.loads(row.samples or "[]") for row in previous_rows}
   grading = grader.regrade_point(record, work, context["labels"], context.get("judge"), stored_samples, grading_row.point_id)
   rereads = {row.point_id: row.rereads for row in previous_rows}
   rereads[grading_row.point_id] = rereads.get(grading_row.point_id, 0) + 1

   for row in previous_rows:
      row.rereads = rereads[row.point_id]

   rows, result = finish(db, session_row, attempt, record, grading, work, context, now, previous_rows)
   decided = grading.by_point()[point_id]
   dispute.resolved_at = stamp(now)
   dispute.resolution = "re-read: still provisional" if decided.provisional else f"re-read: decided, earned {decided.earned}"
   write_audit(db, session_row.user_id, "grading_rerun", dispute.ref_id, {"reason": (reason or "")[:200], "point": point_id}, now=now)
   db.flush()

   return rows, result
