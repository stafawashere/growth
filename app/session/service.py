"""The persisted session service: open, serve, record, close.

One plain function per operation in the API surface rows of docs/plan/06-architecture.md, so the
FastAPI routes that arrive later are thin wrappers over these. The four assembled blocks and the
minute forecast go into the sessions queue column (R5), every attempt row carries both the split
and the compensatory prediction (invariant 23), and a rehearsal session writes no mastery state
(invariant 17).

Confidence is collected after the student commits and before feedback, at stages completion and
unsupported, and not at all at stage example (docs/plan/11-phased-delivery.md, convention 3).
apply_observation already reads the rating and sets hypercorrection_due itself, so the rating is
an input to the single update rather than a second pass over the state: an attempt served at a
stage that collects a rating defers its update until record_confidence supplies one, and an
attempt served at stage example updates immediately.
"""
import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import update

from app.db import models
from app.engine import constants
from app.engine.prior import p_compensatory, p_knowledge
from app.engine.select import format_for_attempt, retrievability_map
from app.engine.state import Confidence, FadingStage, MasteryState, ResponseFormat
from app.engine.update import Observation, apply_observation, rule_based_mastery_states
from app.runtime.bank import served_steps, supports_completion
from app.session import repository
from app.session.build import assemble_session

SERVING_BLOCKS = ("block1", "block2", "block3")

RESPONSE_FIELDS = ("mathjson", "units", "option_id")


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def as_datetime(moment):
   """Every timestamp this service writes is timezone-aware UTC, as app/content/persist.py writes."""
   is_datetime = isinstance(moment, datetime)

   if is_datetime:
      is_naive = moment.tzinfo is None

      if is_naive:
         return moment.replace(tzinfo=timezone.utc)

      return moment.astimezone(timezone.utc)

   return datetime(moment.year, moment.month, moment.day, tzinfo=timezone.utc)


def utc_now():
   return datetime.now(timezone.utc)


def interleaving_satisfied(served, graph):
   """The queue records the max-2-consecutive-same-primary-skill rule as met (06, sessions.queue)."""
   primaries = [graph.primary_skill(item["archetype_id"]) for item in served]
   limit = constants.MAX_CONSECUTIVE_SAME_SKILL

   for index in range(len(primaries) - limit):
      window = primaries[index:index + limit + 1]
      is_run = len(set(window)) == 1

      if is_run:
         return False

   return True


def queue_payload(session, graph):
   return {
      "block1": session.block1,
      "block2": session.block2,
      "block3": session.block3,
      "block4": session.block4,
      "forecasts": session.forecasts,
      "coverage_gaps": list(session.coverage_gaps),
      "interleaving_satisfied": interleaving_satisfied(session.served, graph),
   }


def open_session(
   db,
   user_id,
   mode,
   graph,
   engine_graph,
   archetypes,
   bank,
   snapshot_id,
   today,
   rng,
   probes=None,
   now=None,
   sub_mode=None,
):
   started_at = as_datetime(now or today)
   states = repository.load_states(db, user_id)
   history = repository.load_attempts_history(db, user_id)
   assembled = assemble_session(
      states, graph, bank, probes, history, rng, today, now=now, db=db, user_id=user_id
   )
   is_rehearsal = mode == "rehearsal"
   row = models.Session(
      id=new_id("SES"),
      user_id=user_id,
      mode=mode,
      sub_mode=sub_mode,
      started_at=started_at.isoformat(),
      ended_at=None,
      queue=json.dumps(queue_payload(assembled, graph)),
      updates_mastery=0 if is_rehearsal else 1,
      snapshot_id=snapshot_id,
      created_at=started_at.isoformat(),
      updated_at=started_at.isoformat(),
   )
   db.add(row)
   db.flush()

   return row


def served_positions(session_row):
   """Every servable queue slot as (block, position, item). Block 4 serves no items."""
   queue = json.loads(session_row.queue)

   return [
      (block, position, item)
      for block in SERVING_BLOCKS
      for position, item in enumerate(queue[block])
   ]


def attempt_rows(db, session_id):
   return (
      db.query(models.Attempt)
      .filter(models.Attempt.session_id == session_id)
      .order_by(models.Attempt.started_at, models.Attempt.id)
      .all()
   )


def consumed_positions(db, session_row):
   """A queue slot is consumed by the earliest attempt on its item id that no earlier slot took.

   The queue can list one item twice, because the corrected-item requeue puts a named item back
   into block 1, so the served set is keyed on the slot rather than on the item id.
   """
   remaining = {}

   for row in attempt_rows(db, session_row.id):
      remaining[row.item_id] = remaining.get(row.item_id, 0) + 1

   consumed = set()

   for block, position, item in served_positions(session_row):
      item_id = item["id"]
      has_attempt_left = remaining.get(item_id, 0) > 0

      if has_attempt_left:
         remaining[item_id] -= 1
         consumed.add((block, position))

   return consumed


def resolve_served_format(db, session_row, block, position, item):
   """R29 is answered when the slot is served, not when the queue is assembled.

   The alternation is per user per archetype per stage-unsupported attempt, so a format frozen at
   assembly gives every slot of a fresh session the same answer. The stage stays frozen; only the
   format is re-read, against the attempts as they stand now, and it is written back onto the slot
   so record_attempt and a second read of the same slot see the format that was served.
   """
   history = repository.load_attempts_history(db, session_row.user_id)
   resolved = format_for_attempt(history, item["archetype_id"], FadingStage(item["stage"]))
   is_unchanged = item.get("format") == resolved.value

   if is_unchanged:
      return item

   queue = json.loads(session_row.queue)
   queue[block][position]["format"] = resolved.value
   session_row.queue = json.dumps(queue)
   db.flush()

   return queue[block][position]


def resolve_served_stage(db, session_row, block, position, item):
   """Q16 serves an item with fewer than 2 worked steps at stage unsupported only.

   Stages example and completion both blank the item's last worked step, so both need the 2-step
   minimum to have a step to blank (app/runtime/bank.py served_steps). A slot at either stage over
   an item under the minimum falls back to unsupported, and the fallback is written onto the slot
   so the attempt row records the stage that was served. Example used to be the servable fallback
   here, before the operator's ruling on how a skill leaves stage example (BUILD-LEDGER.md,
   "Decisions taken on the operator's instruction, 2026-09-23") made example collect a graded
   answer too, which took away the room a short item has to blank a step for it. A slot whose item
   has no items row, or no readable step list, is left as it is, and served_item refuses it.
   """
   needs_blank_room = FadingStage(item["stage"]) in (FadingStage.COMPLETION, FadingStage.EXAMPLE)

   if not needs_blank_room:
      return item

   stored = db.get(models.Item, item["id"])
   has_no_row = stored is None

   if has_no_row:
      return item

   try:
      has_blank_room = supports_completion(stored.worked_solution)
   except ValueError:
      return item

   if has_blank_room:
      return item

   queue = json.loads(session_row.queue)
   queue[block][position]["stage"] = FadingStage.UNSUPPORTED.value
   session_row.queue = json.dumps(queue)
   db.flush()

   return queue[block][position]


def resolve_slot(db, session_row, block, position, item):
   """The stage first, because R29's format is resolved per stage."""
   staged = resolve_served_stage(db, session_row, block, position, item)

   return resolve_served_format(db, session_row, block, position, staged)


def next_item(db, session_id):
   """The next unconsumed queue slot, in block order, with its format resolved at serve time.

   An item id that already carries an attempt in this session is skipped even in a later slot,
   because record_attempt refuses a second attempt on the same item in the same session.
   """
   session_row = db.get(models.Session, session_id)
   consumed = consumed_positions(db, session_row)
   attempted = {row.item_id for row in attempt_rows(db, session_row.id)}

   for block, position, item in served_positions(session_row):
      is_consumed = (block, position) in consumed
      is_attempted = item["id"] in attempted

      if not is_consumed and not is_attempted:
         return resolve_slot(db, session_row, block, position, item)

   return None


def served_item(db, session_id):
   """next_item with the worked steps its stage shows, read from the items row at serve time.

   The steps are not written into sessions.queue, so GET /sessions/{id} never carries them.
   """
   item = next_item(db, session_id)
   is_exhausted = item is None

   if is_exhausted:
      return None

   stage = FadingStage(item["stage"])
   is_unsupported = stage == FadingStage.UNSUPPORTED
   steps = None

   if not is_unsupported:
      stored = db.get(models.Item, item["id"])
      has_no_row = stored is None

      if has_no_row:
         raise ValueError(f"item {item['id']} has no items row, so its worked steps cannot be shown")

      steps = served_steps(stored.worked_solution, stage)

   return dict(item, served_steps=steps)


def stored_response(answer):
   """06 attempts.response: MathJSON for typed input, with the units typed beside it, which
   app/items/grade.py reads, or the option id for MCQ. Anything else the body claims is dropped.
   """
   return {name: answer[name] for name in RESPONSE_FIELDS if name in answer}


def queue_slot(session_row, item_id):
   for block, position, item in served_positions(session_row):
      if item["id"] == item_id:
         return block, position, item

   raise ValueError(f"{item_id} is not in the queue of session {session_row.id}")


def queue_item(session_row, item_id):
   return queue_slot(session_row, item_id)[2]


def collects_confidence(stage):
   """A rating is collected before feedback on every stage (11 P1 scope 10), example included:
   the operator's ruling on how a skill leaves stage example (BUILD-LEDGER.md, "Decisions taken
   on the operator's instruction, 2026-09-23") withdraws 11 implementer decision 3, which had
   carved example out because it committed no answer. It now commits one, so it rates like any
   other stage.
   """
   FadingStage(stage)

   return True


def observation_for(attempt, archetype, confidence):
   return Observation(
      archetype_id=archetype["id"],
      skills=list(archetype["skills"]),
      per_skill_states=json.loads(attempt.per_skill_states),
      response_format=ResponseFormat(attempt.format),
      confidence=Confidence(confidence),
      elapsed_ms=attempt.elapsed_ms,
      served_stage=FadingStage(attempt.served_stage),
   )


def apply_attempt(db, session_row, attempt, archetype, confidence, today, engine_graph, now):
   """The single update per attempt. Rehearsal stops here, per invariant 17."""
   writes_mastery = session_row.updates_mastery == 1

   if not writes_mastery:
      return

   states = repository.load_states(db, session_row.user_id)
   apply_observation(states, engine_graph, observation_for(attempt, archetype, confidence), today)
   repository.save_states(db, session_row.user_id, states, session_row.snapshot_id, now)


def record_attempt(
   db,
   session_id,
   item_id,
   answer,
   elapsed_ms,
   today,
   archetypes=None,
   engine_graph=None,
   confidence=None,
   started_at=None,
   now=None,
   grader=None,
):
   """Write one attempt row and, once it is graded and rated, apply its single observation.

   A grader is a callable over the queue item and the submitted answer that returns the R12
   verdict, which overrides anything the submission claims about itself. Callers that pass no
   grader are trusted to have graded the answer already, which is why the HTTP layer always
   passes one.
   """
   session_row = db.get(models.Session, session_id)
   block, position, slot = queue_slot(session_row, item_id)
   item = resolve_slot(db, session_row, block, position, slot)
   already_attempted = any(row.item_id == item_id for row in attempt_rows(db, session_id))

   if already_attempted:
      raise ValueError(f"item {item_id} already has an attempt in session {session_id}")

   archetype = archetypes[item["archetype_id"]]
   submitted_at = as_datetime(now or today)
   states = repository.load_states(db, session_row.user_id)
   retrievability = retrievability_map(states, today)
   split = p_knowledge(archetype, states, engine_graph.hard_parents, retrievability)
   compensatory = p_compensatory(archetype, states, retrievability)
   grades_here = grader is not None
   verdict = grader(item, answer) if grades_here else {}
   graded_answer = {**answer, **verdict}
   is_graded = graded_answer.get("correct") is not None

   if is_graded:
      per_skill_states = rule_based_mastery_states(archetype, graded_answer)
   else:
      per_skill_states = {
         skill: MasteryState.NOT_ATTEMPTED for skill in archetype["skills"]
      }

   is_correct = bool(graded_answer.get("correct")) if is_graded else None
   stored_confidence = Confidence(confidence).value if confidence is not None else None
   attempt = models.Attempt(
      id=new_id("ATT"),
      session_id=session_id,
      item_id=item_id,
      started_at=(started_at or submitted_at).isoformat(),
      submitted_at=submitted_at.isoformat(),
      response=json.dumps(stored_response(answer)),
      confidence=stored_confidence,
      elapsed_ms=elapsed_ms,
      correct=int(is_correct) if is_graded else None,
      p_split=split,
      p_compensatory=compensatory,
      served_stage=FadingStage(item["stage"]).value,
      format=ResponseFormat(item["format"]).value,
      per_skill_states=json.dumps(
         {skill: state.value for skill, state in per_skill_states.items()}
      ),
      snapshot_id=session_row.snapshot_id,
      created_at=submitted_at.isoformat(),
      updated_at=submitted_at.isoformat(),
   )
   db.add(attempt)
   db.flush()

   has_rating = confidence is not None
   awaits_rating = collects_confidence(item["stage"]) and not has_rating
   is_held = awaits_rating or not is_graded

   if is_held:
      return attempt

   rating = confidence if has_rating else Confidence.UNSURE
   apply_attempt(
      db, session_row, attempt, archetype, rating, today, engine_graph, submitted_at
   )

   return attempt


def record_confidence(
   db,
   attempt_id,
   confidence,
   archetypes=None,
   engine_graph=None,
   today=None,
   now=None,
):
   """The P1 path that supplies the rating to the update, before feedback is shown.

   An ungraded attempt still takes the rating, because 11 collects one before feedback on every
   item, but it has no observation to apply, so the rating is stored and mastery is left alone.
   """
   attempt = db.get(models.Attempt, attempt_id)
   already_rated = attempt.confidence is not None

   if already_rated:
      raise ValueError(f"attempt {attempt_id} already carries a confidence rating")

   has_context = archetypes is not None and engine_graph is not None and today is not None

   if not has_context:
      raise ValueError("record_confidence applies the observation and needs the engine context")

   is_graded = attempt.correct is not None

   if not is_graded:
      attempt.confidence = Confidence(confidence).value
      attempt.updated_at = as_datetime(now or today).isoformat()
      db.flush()

      return attempt

   session_row = db.get(models.Session, attempt.session_id)
   item = queue_item(session_row, attempt.item_id)
   attempt.confidence = Confidence(confidence).value
   applied_at = as_datetime(now or today)
   attempt.updated_at = applied_at.isoformat()
   db.flush()
   apply_attempt(
      db,
      session_row,
      attempt,
      archetypes[item["archetype_id"]],
      confidence,
      today,
      engine_graph,
      applied_at,
   )

   return attempt


class ErrorNoteAlreadyWritten(ValueError):
   pass


class ErrorNoteNotOneLine(ValueError):
   pass


class ErrorNoteTooLong(ValueError):
   pass


ERROR_NOTE_MAX_CHARACTERS = 500


def record_error_note(db, attempt_id, note):
   """One line, once, per 03's "The student's one-line error note". The guard lives here rather
   than in the route so that every caller gets it, because a second note overwrites the record of
   what the student first thought. 03 and 06 set no length, so the cap is the operator's own
   decision (BUILD-LEDGER.md, "Decisions taken on the operator's instruction, 2026-09-20": the
   error note is capped at 500 characters), checked before anything is written.
   """
   attempt = db.get(models.Attempt, attempt_id)

   existing = attempt.error_note
   already_written = isinstance(existing, str) and existing.strip() != ""

   if already_written:
      raise ErrorNoteAlreadyWritten(f"attempt {attempt_id} already carries its error note")

   carries_newline = "\n" in note
   carries_carriage_return = "\r" in note
   spans_more_than_one_line = carries_newline or carries_carriage_return

   if spans_more_than_one_line:
      raise ErrorNoteNotOneLine(f"the error note for attempt {attempt_id} is not one line")

   is_too_long = len(note) > ERROR_NOTE_MAX_CHARACTERS

   if is_too_long:
      raise ErrorNoteTooLong(
         f"the error note for attempt {attempt_id} is over {ERROR_NOTE_MAX_CHARACTERS} characters"
      )

   attempt.error_note = note
   db.flush()

   return attempt


class SelfExplanationNotInvited(ValueError):
   pass


class SelfExplanationAlreadyWritten(ValueError):
   pass


class SelfExplanationEmpty(ValueError):
   pass


def invites_self_explanation(attempt):
   """11 P1 scope 10: the prompt is attached to worked examples and corrected errors only."""
   is_worked_example = attempt.served_stage == FadingStage.EXAMPLE.value
   was_corrected = attempt.correct == 0

   return is_worked_example or was_corrected


def record_self_explanation(db, attempt_id, answer):
   """One answer per attempt. The write is conditional on the column still being empty, so two
   racing requests cannot both land.
   """
   is_text = isinstance(answer, str)
   is_empty = not is_text or answer.strip() == ""

   if is_empty:
      raise SelfExplanationEmpty(f"the self-explanation for attempt {attempt_id} is empty")

   attempt = db.get(models.Attempt, attempt_id)

   if not invites_self_explanation(attempt):
      raise SelfExplanationNotInvited(
         f"attempt {attempt_id} is neither a worked example nor a corrected error"
      )

   written = db.execute(
      update(models.Attempt)
      .where(models.Attempt.id == attempt_id, models.Attempt.self_explanation.is_(None))
      .values(self_explanation=answer.strip())
   )
   was_written = written.rowcount == 1

   if not was_written:
      raise SelfExplanationAlreadyWritten(f"attempt {attempt_id} already carries its self-explanation")

   db.flush()

   return attempt


def record_judgment(db, session_id, scope, scope_id, predicted_retention, now):
   """A metacognitive judgment of learning. It is a measurement, never a credit-assignment input
   (docs/plan/02-adaptive-engine.md line 723), so this writes only the judgments row.
   """
   made_at = as_datetime(now)
   row = models.Judgment(
      id=new_id("JDG"),
      user_id=db.get(models.Session, session_id).user_id,
      session_id=session_id,
      scope=scope,
      scope_id=scope_id,
      predicted_retention=predicted_retention,
      made_at=made_at.isoformat(),
      outcome_attempt_id=None,
      outcome_correct=None,
      created_at=made_at.isoformat(),
      updated_at=made_at.isoformat(),
   )
   db.add(row)
   db.flush()

   return row


def unrated_graded_attempts(db, session_row):
   """Every attempt still without a rating at a stage that collects one, correct or not."""
   result = []

   for attempt in attempt_rows(db, session_row.id):
      is_graded = attempt.correct is not None
      awaits_rating = collects_confidence(attempt.served_stage) and attempt.confidence is None
      needs_update = is_graded and awaits_rating

      if needs_update:
         result.append(attempt)

   return result


def close_session(db, session_id, now=None, archetypes=None, engine_graph=None, today=None):
   """Sweeps unrated attempts in as Confidence.UNSURE before stamping ended_at.

   No hypercorrection can fire from unsure (BUILD-LEDGER.md, "Decisions taken on the operator's
   instruction"), so a student who never rates loses no observation and gains no false alarm.
   """
   session_row = db.get(models.Session, session_id)
   pending = unrated_graded_attempts(db, session_row)
   has_pending = len(pending) > 0

   if has_pending:
      has_context = archetypes is not None and engine_graph is not None and today is not None

      if not has_context:
         raise ValueError("close_session needs archetypes, engine_graph and today to apply unrated attempts")

      applied_at = as_datetime(now or utc_now())

      for attempt in pending:
         item = queue_item(session_row, attempt.item_id)
         attempt.confidence = Confidence.UNSURE.value
         attempt.updated_at = applied_at.isoformat()
         apply_attempt(
            db,
            session_row,
            attempt,
            archetypes[item["archetype_id"]],
            Confidence.UNSURE,
            today,
            engine_graph,
            applied_at,
         )

      db.flush()

   session_row.ended_at = as_datetime(now or utc_now()).isoformat()
   session_row.updated_at = session_row.ended_at
   db.flush()

   return session_row
