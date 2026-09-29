"""The persisted session service: open, serve, record, close.

One plain function per operation in the API surface rows of docs/plan/06-architecture.md, so the
FastAPI routes that arrive later are thin wrappers over these. The four assembled blocks and the
minute forecast go into the sessions queue column (R5), every attempt row carries both the split
and the compensatory prediction (invariant 23), and a rehearsal session writes no mastery state
(invariant 17).

Confidence is collected after the student commits and before feedback, at every stage including
example (BUILD-LEDGER.md, "Decisions taken on the operator's instruction, 2026-09-23", which
withdraws 11 implementer decision 3 now that example commits a graded answer of its own).
apply_observation already reads the rating and sets hypercorrection_due itself, so the rating is
an input to the single update rather than a second pass over the state: every attempt defers its
update until record_confidence supplies the rating.
"""
import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import update

from app.db import models
from app.experiments import switches
from app.engine import constants
from app.engine.interleave import window_violations
from app.engine.prior import p_compensatory, p_knowledge, primary_skill
from app.engine.select import format_for_item, retrievability_map
from app.engine.state import Confidence, FadingStage, MasteryState, ResponseFormat
from app.engine.update import Observation, apply_observation, rule_based_mastery_states
from app.lessons import gate as lesson_gate
from app.lessons import refresh as lesson_refresh
from app.lessons import repository as lesson_repository
from app.runtime.bank import served_steps, supports_completion
from app.session import diagnostic_session, repository
from app.session.build import assemble_session
from app.session.diagnoses import write_rule_diagnosis

SERVING_BLOCKS = ("block1", "block2", "block3", diagnostic_session.ITEMS_KEY)

LEARNING_MODE = "learning"

CONFIDENCE_FROM_STUDENT = "student"

CONFIDENCE_FROM_SESSION_CLOSE = "session_close"

RESPONSE_FIELDS = ("mathjson", "units", "option_id")

READING_KINDS = lesson_repository.READING_KINDS


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


def is_reading(entry):
   return entry.get("kind") in READING_KINDS


def unexplained_violations(served, graph, shortfalls):
   """Window violations that no logged shortfall accounts for.

   shortfalls are (position, rule) pairs. A shortfall is logged when no candidate at that position could meet the rule, which is the
   plan's own "once 2 units are open" reading applied to every soft rule; anything else the
   independent check in app/engine/interleave.py finds is a real violation.
   """
   records = [graph.archetypes[item["archetype_id"]] for item in served if not is_reading(item)]
   explained = {(entry[0], entry[1]) for entry in shortfalls}

   return [
      violation
      for violation in window_violations(records, graph.conversion_pairs)
      if violation not in explained
   ]


def interleaving_satisfied(served, graph, shortfalls=()):
   """06 sessions.queue: the interleaving constraints recorded as satisfied, now all of D3."""
   return len(unexplained_violations(served, graph, shortfalls)) == 0


def queue_payload(session, graph):
   return {
      "block1": session.block1,
      "block2": session.block2,
      "block3": session.block3,
      "block4": session.block4,
      "forecasts": session.forecasts,
      "coverage_gaps": list(session.coverage_gaps),
      "interleaving_satisfied": interleaving_satisfied(
         session.served,
         graph,
         [(entry["position"], entry["rule"]) for entry in session.shortfalls],
      ),
      "interleaving_shortfalls": [[entry["position"], entry["rule"]] for entry in session.shortfalls],
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
   process_seed=0,
   experiment_default=None,
):
   """experiment_default is the state a student's A/B switches start in (app/experiments); None
   leaves the switches unread, which is how every caller that predates P7 assembles."""
   started_at = as_datetime(now or today)
   opens_diagnostic = mode == diagnostic_session.MODE

   if opens_diagnostic:
      unfinished = diagnostic_session.unfinished_diagnostic(db, user_id)

      if unfinished is not None:
         return unfinished

      return diagnostic_session.open_diagnostic(
         db,
         user_id,
         graph,
         bank,
         snapshot_id,
         today,
         process_seed,
         started_at,
         new_id("SES"),
      )

   states = repository.load_states(db, user_id)
   history = repository.load_attempts_history(db, user_id)
   retrieval_entry = None

   if experiment_default is not None:
      retrieval_entry = switches.retrieval_entry_thresholds(
         db, user_id, entry_candidates(states), experiment_default, started_at
      )

   opens_learning = mode == LEARNING_MODE
   lesson_inputs = None

   if opens_learning:
      lesson_inputs = load_lesson_inputs(
         db, user_id, states, graph, history, today, experiment_default, started_at
      )

   assembled = assemble_session(
      states,
      graph,
      bank,
      probes,
      history,
      rng,
      today,
      now=now,
      db=db,
      user_id=user_id,
      retrieval_entry=retrieval_entry,
      openers=opens_learning,
      lessons=lesson_inputs,
   )
   opened_first_skills = [
      graph.concept_skills[concept_id][0] for concept_id in assembled.opener_concepts
   ]
   repository.mark_openers_done(db, user_id, opened_first_skills, started_at)
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
   lesson_repository.write_session_reading(
      db, user_id, row.id, assembled.lessons, assembled.lesson_deferrals, now=started_at
   )

   return row


def placement_only(concept_id, states, graph):
   """A concept whose skills are all mastered with no credited observation was mastered by the
   diagnostic's placement or by seeding, not by practice (15, Cold start)."""
   skills = lesson_gate.concept_skill_map(graph).get(concept_id, ())

   return all(states[skill].credited_observation_count == 0 for skill in skills if skill in states)


def bypass_placement(db, user_id, states, graph, servable, lesson_states, now):
   """15 Cold start: bypassed_by_placement on every placed concept whose lesson has no state yet.
   The diagnostic's own module is not this slice's, so the write happens when the first learning
   session after placement opens, which is before any lesson could be inserted."""
   bypassed = []

   for concept_id in lesson_gate.bypass_placed_concepts(states, graph):
      found = servable.get(concept_id)
      has_no_state = found is not None and found[0] not in lesson_states

      if has_no_state and placement_only(concept_id, states, graph):
         bypassed.append(found[0])

   lesson_repository.write_bypassed(db, user_id, bypassed, now=now)

   for lesson_id in bypassed:
      lesson_states[lesson_id] = {"status": lesson_gate.BYPASSED}


def example_first_chooser(db, user_id, experiment_default, now):
   """The lesson_first_contact switch (15, Within-student A/B), unit concept, stratified by unit.
   The five productive-failure targets are excluded and stay in the control arm."""
   if experiment_default is None:
      return None

   treatment = switches.DEFINITIONS[switches.LESSON_FIRST_CONTACT].treatment_arm

   def serves_example_first(concept_id, archetype):
      is_excluded = concept_id in constants.PRODUCTIVE_FAILURE_TARGETS

      if is_excluded:
         return False

      arm = switches.arm_for(
         db,
         user_id,
         switches.LESSON_FIRST_CONTACT,
         concept_id,
         archetype.get("primary_unit") or concept_id,
         None,
         experiment_default,
         now,
      )

      return arm == treatment

   return serves_example_first


def gap_skills(db, user_id, graph):
   gaps = []

   for gap_id, archetype_id in lesson_repository.prerequisite_gaps(db, user_id):
      record = graph.archetypes.get(archetype_id)

      if record is not None:
         gaps.append((gap_id, tuple(record["skills"])))

   return gaps


def load_lesson_inputs(db, user_id, states, graph, history, today, experiment_default, now):
   servable = lesson_repository.servable_map(db)
   lesson_states = lesson_repository.lesson_states(db, user_id)
   bypass_placement(db, user_id, states, graph, servable, lesson_states, now)
   refreshers = lesson_refresh.refresher_targets(
      states,
      history,
      lesson_states,
      today,
      graph=graph,
      servable=servable,
      prerequisite_gaps=gap_skills(db, user_id, graph),
   )

   return lesson_gate.LessonInputs(
      servable=servable,
      bodies=lesson_repository.lesson_bodies(db, servable.values()),
      lesson_states=lesson_states,
      completion_ratios=lesson_repository.completion_ratios(db, user_id),
      example_first=example_first_chooser(db, user_id, experiment_default, now),
      refreshers=tuple(refreshers),
   )


def entry_candidates(states):
   """Skills whose RETRIEVAL_ENTRY arm now decides whether they are in the block 3 pool: at least
   one unaided success and short of the treatment arm's entry. A skill is assigned the first time
   it reaches this point, so assignment never depends on how the skill does afterwards."""
   highest_entry = max(switches.ENTRY_THRESHOLDS.values())

   return [
      skill_id
      for skill_id, state in states.items()
      if 1 <= state.unaided_success_count < highest_entry
   ]


def served_positions(session_row):
   """Every servable queue slot as (block, position, item). Block 4 serves no items."""
   queue = json.loads(session_row.queue)

   return [
      (block, position, item)
      for block in SERVING_BLOCKS
      for position, item in enumerate(queue.get(block, []))
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

   consumed = set(lesson_repository.consumed_reading_slots(db, session_row))

   for block, position, item in served_positions(session_row):
      if is_reading(item):
         continue

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
   resolved = format_for_item(history, item, FadingStage(item["stage"]))
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
   """The stage first, because R29's format is resolved per stage. A lesson or refresher slot has
   no stage; it is served with the stored record body the reader renders."""
   if is_reading(item):
      return reading_slot(db, item)

   staged = resolve_served_stage(db, session_row, block, position, item)

   return resolve_served_format(db, session_row, block, position, staged)


def reading_slot(db, entry):
   stored = db.get(models.Lesson, (entry["lesson_id"], entry["version"]))
   body = stored.body if stored is not None else None

   return dict(entry, lesson=body)


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
      # A lesson whose item was answered anyway has been passed over, so it is not served late.
      is_attempted = item.get("before_item_id" if is_reading(item) else "id") in attempted

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

   if is_reading(item):
      return item

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
      if item.get("id") == item_id:
         return block, position, item

   raise ValueError(f"{item_id} is not in the queue of session {session_row.id}")


def queue_item(session_row, item_id):
   return queue_slot(session_row, item_id)[2]


def is_opener_slot(item):
   return item.get("is_opener") is True


def is_opener_attempt(session_row, attempt):
   return is_opener_slot(queue_item(session_row, attempt.item_id))


def served_as_opener(session_row, attempt):
   """is_opener_attempt for the routes after submission, where an attempt whose item no serving
   slot holds (a diagnostic queue, a slot rewritten since) is simply not an opener."""
   for _block, _position, item in served_positions(session_row):
      if item.get("id") == attempt.item_id:
         return is_opener_slot(item)

   return False


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


def answer_skipped_units(db, session_row, item, today, archetypes, engine_graph, advance):
   """Answer "I have not learned this yet" to each served diagnostic item whose unit the student
   skipped, through the same record_attempt path as the button, until an item of another unit is
   waiting or the run finishes. advance serves the waiting or next item, or None once finished."""
   while item is not None and diagnostic_session.waits_in_skipped_unit(session_row):
      record_attempt(
         db,
         session_row.id,
         item["id"],
         dict(diagnostic_session.NOT_LEARNED_ANSWER),
         None,
         today,
         archetypes=archetypes,
         engine_graph=engine_graph,
      )
      item = advance()

   return item


def skip_diagnostic_unit(db, session_row, item_id, elapsed_ms, today, archetypes, engine_graph, advance):
   """Skip the unit of the diagnostic item on screen: record the unit as skipped and answer the item
   not learned. answer_skipped_units then answers each later item of the unit as it is served."""
   waiting = advance()
   is_on_screen = waiting is not None and waiting["id"] == item_id

   if not is_on_screen:
      raise ValueError(f"item {item_id} is not the diagnostic item waiting for an answer")

   diagnostic_session.mark_unit_skipped(db, session_row, diagnostic_session.waiting_unit(session_row))
   record_attempt(
      db,
      session_row.id,
      item_id,
      dict(diagnostic_session.NOT_LEARNED_ANSWER),
      elapsed_ms,
      today,
      archetypes=archetypes,
      engine_graph=engine_graph,
   )


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
   experiment_default=None,
):
   """Write one attempt row and, once it is graded and rated, apply its single observation.

   A productive-failure opener (02, Session assembly) is recorded as graded, so the comparison
   with the canonical method has the student's answer to work from, but its observation is
   applied at once as not_attempted on every loaded skill: observation_count moves, as 02's
   schema table says an uncredited observation does, and nothing else in skills_state does.

   A grader is a callable over the queue item and the submitted answer that returns the R12
   verdict, which overrides anything the submission claims about itself. Callers that pass no
   grader are trusted to have graded the answer already, which is why the HTTP layer always
   passes one.
   """
   session_row = db.get(models.Session, session_id)
   block, position, slot = queue_slot(session_row, item_id)

   if diagnostic_session.is_diagnostic(session_row):
      return diagnostic_session.record_answer(
         db,
         session_row,
         slot,
         answer,
         elapsed_ms,
         today,
         archetypes,
         engine_graph,
         grader,
         as_datetime(now or today),
         started_at,
         new_id,
      )

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
   is_opener = is_opener_slot(item)
   is_credited = is_graded and not is_opener

   if is_credited:
      per_skill_states = rule_based_mastery_states(archetype, graded_answer)
   else:
      per_skill_states = {
         skill: MasteryState.NOT_ATTEMPTED for skill in archetype["skills"]
      }

   is_correct = bool(graded_answer.get("correct")) if is_graded else None
   stored_confidence = Confidence(confidence).value if confidence is not None else None
   confidence_source = CONFIDENCE_FROM_STUDENT if confidence is not None else None
   attempt = models.Attempt(
      id=new_id("ATT"),
      session_id=session_id,
      item_id=item_id,
      started_at=(started_at or submitted_at).isoformat(),
      submitted_at=submitted_at.isoformat(),
      response=json.dumps(stored_response(answer)),
      confidence=stored_confidence,
      confidence_source=confidence_source,
      elapsed_ms=elapsed_ms,
      correct=int(is_correct) if is_graded else None,
      p_split=split,
      p_compensatory=compensatory,
      served_stage=FadingStage(item["stage"]).value,
      format=ResponseFormat(item["format"]).value,
      per_skill_states=json.dumps(
         {skill: state.value for skill, state in per_skill_states.items()}
      ),
      preceded_by_lesson_id=item.get("preceded_by_lesson_id"),
      preceded_by_lesson_version=item.get("preceded_by_lesson_version"),
      snapshot_id=session_row.snapshot_id,
      created_at=submitted_at.isoformat(),
      updated_at=submitted_at.isoformat(),
   )
   is_unsupported = FadingStage(item["stage"]) == FadingStage.UNSUPPORTED
   reads_the_feedback_switch = experiment_default is not None and is_unsupported and not is_opener

   if reads_the_feedback_switch:
      arm = switches.arm_for(
         db,
         session_row.user_id,
         switches.FEEDBACK_ELABORATION,
         item_id,
         primary_skill(archetype),
         split,
         experiment_default,
         submitted_at,
      )
      switches.record_arm(attempt, switches.FEEDBACK_ELABORATION, arm)

   db.add(attempt)
   db.flush()

   if is_graded:
      write_rule_diagnosis(db, attempt.id, per_skill_states, graded_answer, submitted_at)

   applies_uncredited = is_opener and is_graded

   if applies_uncredited:
      apply_attempt(
         db, session_row, attempt, archetype, Confidence.UNSURE, today, engine_graph, submitted_at
      )

   if is_opener:
      return attempt

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
   A productive-failure opener is the same: its uncredited observation was applied when it was
   submitted, and the rating never reaches the update (02, Session assembly).
   """
   attempt = db.get(models.Attempt, attempt_id)
   already_rated = attempt.confidence is not None

   if already_rated:
      raise ValueError(f"attempt {attempt_id} already carries a confidence rating")

   has_context = archetypes is not None and engine_graph is not None and today is not None

   if not has_context:
      raise ValueError("record_confidence applies the observation and needs the engine context")

   is_graded = attempt.correct is not None
   session_row = db.get(models.Session, attempt.session_id)
   stores_rating_only = not is_graded or is_opener_attempt(session_row, attempt)

   if stores_rating_only:
      attempt.confidence = Confidence(confidence).value
      attempt.confidence_source = CONFIDENCE_FROM_STUDENT
      attempt.updated_at = as_datetime(now or today).isoformat()
      db.flush()

      return attempt

   item = queue_item(session_row, attempt.item_id)
   attempt.confidence = Confidence(confidence).value
   attempt.confidence_source = CONFIDENCE_FROM_STUDENT
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


class ErrorNoteNotOneLine(ValueError):
   pass


class ErrorNoteTooLong(ValueError):
   pass


ERROR_NOTE_MAX_CHARACTERS = 500


def record_error_note(db, attempt_id, note):
   """One line, per 03's "The student's one-line error note". Ruled 2026-09-23, confirming the
   operator's 2026-09-20 decision (BUILD-LEDGER.md, "Decisions taken on the operator's
   instruction, 2026-09-20"): a second POST replaces the first, because replacing a note is
   editing it, not adding a second one; a second call to this function overwrites rather than
   refuses. 03 and 06 set no length, so the cap is the operator's own decision from the same
   ruling, checked before anything is written.
   """
   attempt = db.get(models.Attempt, attempt_id)

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
   session_row = db.get(models.Session, attempt.session_id)

   if served_as_opener(session_row, attempt):
      raise SelfExplanationNotInvited(
         f"attempt {attempt_id} is a productive-failure opener, whose feedback is the comparison"
      )

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
      was_applied_at_submission = is_opener_attempt(session_row, attempt)
      needs_update = is_graded and awaits_rating and not was_applied_at_submission

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
         attempt.confidence_source = CONFIDENCE_FROM_SESSION_CLOSE
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
