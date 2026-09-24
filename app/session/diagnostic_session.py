"""The diagnostic as a persisted session: open, serve the next item, record an answer, finish.

docs/plan/02 "Cold-start diagnostic design" over app/engine/diagnostic.py. A diagnostic cannot be
assembled ahead of time, because each item depends on the answer before it, so the session row's
queue holds the run itself under "diagnostic" and the items served so far under
"diagnostic_items", and the next item is chosen when the previous one has been answered.

What 08 draws for the diagnostic item decides three things here. Items are served at stage
unsupported, with no worked steps, as short answer, the MathLive field of the wireframe. No
confidence rating and no feedback is collected, because the diagnostic item's states are
unanswered, answered and submitted and nothing else, so each scored answer is applied at once
with the rating recorded as unsure and its source as "diagnostic", which the calibration curve
does not count. "I have not learned this yet" is an answer: no grading, no credit to any skill,
and strong evidence in the posterior that the unit has not been started.

The run finishes when the engine stops it. The placement is then written to skills_state and the
session is closed, so a first login and a long-gap return both land on home with the queue the
placed state implies.
"""
import json
import random

from app.db import models
from app.engine import constants, diagnostic
from app.engine.retention import current_retrievability
from app.engine.select import dress_item, requires_choice
from app.engine.state import Confidence, FadingStage, MasteryState, ResponseFormat
from app.engine.update import Observation, apply_observation, rule_based_mastery_states
from app.session import repository
from app.session.build import recently_served
from app.session.diagnoses import write_rule_diagnosis

MODE = "diagnostic"

CONFIDENCE_FROM_DIAGNOSTIC = "diagnostic"

RUN_KEY = "diagnostic"

ITEMS_KEY = "diagnostic_items"


def is_diagnostic(session_row):
   return session_row.mode == MODE


def load_run(session_row):
   return diagnostic.DiagnosticRun.from_dict(json.loads(session_row.queue)[RUN_KEY])


def save_run(db, session_row, run, served_items=None):
   queue = json.loads(session_row.queue)
   queue[RUN_KEY] = run.as_dict()

   if served_items is not None:
      queue[ITEMS_KEY] = served_items

   session_row.queue = json.dumps(queue)
   db.flush()


def empty_queue(run):
   return {
      "block1": [],
      "block2": [],
      "block3": [],
      "block4": [],
      "forecasts": {},
      "coverage_gaps": list(run.coverage_gaps),
      "interleaving_satisfied": True,
      "interleaving_shortfalls": [],
      RUN_KEY: run.as_dict(),
      ITEMS_KEY: [],
   }


def unfinished_diagnostic(db, user_id):
   """A diagnostic left open is resumed rather than started again beside it."""
   return (
      db.query(models.Session)
      .filter(
         models.Session.user_id == user_id,
         models.Session.mode == MODE,
         models.Session.ended_at.is_(None),
      )
      .order_by(models.Session.started_at.desc())
      .first()
   )


def run_rng(process_seed, session_id, position):
   return random.Random(f"{process_seed}:{session_id}:{position}")


class ShortAnswerBank:
   """The bank as the diagnostic sees it. The diagnostic asks every item as a short answer (P2),
   and a statement-keyed item has nothing to type, so it is left out; an archetype whose items are
   all statements is a coverage gap for the diagnostic, as it was before it had any items."""

   def __init__(self, bank):
      self.bank = bank

   def published_items(self, archetype_id):
      return [item for item in self.bank.published_items(archetype_id) if not requires_choice(item)]

   def has_published_item(self, archetype_id):
      return len(self.published_items(archetype_id)) > 0

   def __getattr__(self, name):
      return getattr(self.bank, name)


def open_diagnostic(db, user_id, graph, bank, snapshot_id, today, process_seed, started_at, session_id):
   states = repository.load_states(db, user_id)
   retrievability = current_retrievability(states, today)
   rng = run_rng(process_seed, session_id, "start")
   run = diagnostic.start_run(states, graph, ShortAnswerBank(bank), retrievability, rng)
   stamp = started_at.isoformat()
   row = models.Session(
      id=session_id,
      user_id=user_id,
      mode=MODE,
      sub_mode=None,
      started_at=stamp,
      ended_at=None,
      queue=json.dumps(empty_queue(run)),
      updates_mastery=1,
      snapshot_id=snapshot_id,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()

   return row


def attempted_item_ids(db, session_id):
   rows = db.query(models.Attempt.item_id).filter(models.Attempt.session_id == session_id).all()

   return {row[0] for row in rows}


def pick_item(record, bank, rng, blocked):
   published = sorted(bank.published_items(record["id"]), key=lambda item: item["id"])
   fresh = [item for item in published if item["id"] not in blocked]
   choices = fresh or published

   return rng.choice(choices)


def advance(db, session_row, graph, engine_graph, bank, today, process_seed, finished_at):
   """The item waiting for an answer, a newly chosen one, or None once the run has finished."""
   if session_row.ended_at is not None:
      return None

   queue = json.loads(session_row.queue)
   served_items = queue[ITEMS_KEY]
   answered = attempted_item_ids(db, session_row.id)

   for item in served_items:
      if item["id"] not in answered:
         return item

   run = load_run(session_row)
   rng = run_rng(process_seed, session_row.id, len(run.asked))
   record = diagnostic.next_archetype(run, graph, ShortAnswerBank(bank), rng)
   has_finished = record is None

   if has_finished:
      finish(db, session_row, run, graph, today, finished_at)

      return None

   history = repository.load_attempts_history(db, session_row.user_id)
   blocked = recently_served(history, today)[0] | answered
   chosen = pick_item(record, ShortAnswerBank(bank), rng, blocked)
   states = repository.load_states(db, session_row.user_id)
   served = dress_item(record, chosen, states, graph, history)
   served["stage"] = FadingStage.UNSUPPORTED
   served["format"] = ResponseFormat(run.response_format)
   served["diagnostic_position"] = len(run.asked)
   served["diagnostic_cap"] = constants.DIAG_CAP
   run.pending["item_id"] = chosen["id"]
   served_items.append(json.loads(json.dumps(served, default=enum_value)))
   save_run(db, session_row, run, served_items)

   return served_items[-1]


def enum_value(value):
   return getattr(value, "value", str(value))


def finish(db, session_row, run, graph, today, finished_at):
   states = repository.load_states(db, session_row.user_id)
   diagnostic.place(run, states, graph, today)
   repository.save_states(db, session_row.user_id, states, session_row.snapshot_id, finished_at)
   save_run(db, session_row, run)
   session_row.ended_at = finished_at.isoformat()
   session_row.updated_at = session_row.ended_at
   db.flush()


def outcome_of(graded_answer, not_learned):
   if not_learned:
      return diagnostic.OUTCOME_NOT_LEARNED

   is_correct = bool(graded_answer.get("correct"))

   return diagnostic.OUTCOME_CORRECT if is_correct else diagnostic.OUTCOME_INCORRECT


def record_answer(db, session_row, item, answer, elapsed_ms, today, archetypes, engine_graph, grader, submitted_at, started_at, new_id):
   """One diagnostic answer: the attempt row, its diagnosis, the update and the posterior step."""
   run = load_run(session_row)
   entry = run.pending
   is_waiting_item = entry is not None and entry.get("item_id") == item["id"]

   if not is_waiting_item:
      raise ValueError(f"item {item['id']} is not the diagnostic item waiting for an answer")

   archetype = archetypes[item["archetype_id"]]
   not_learned = bool(answer.get("not_learned"))
   graded_answer = {} if not_learned else {**answer, **grader(item, answer)}
   is_graded = graded_answer.get("correct") is not None
   cannot_grade = not not_learned and not is_graded

   if cannot_grade:
      raise ValueError(f"item {item['id']} could not be graded, so the diagnostic cannot score it")

   if not_learned:
      per_skill_states = {skill: MasteryState.NOT_ATTEMPTED for skill in archetype["skills"]}
   else:
      per_skill_states = rule_based_mastery_states(archetype, graded_answer)

   stored_response = {"not_learned": True} if not_learned else {
      name: answer[name] for name in ("mathjson", "units", "option_id") if name in answer
   }
   attempt = models.Attempt(
      id=new_id("ATT"),
      session_id=session_row.id,
      item_id=item["id"],
      started_at=(started_at or submitted_at).isoformat(),
      submitted_at=submitted_at.isoformat(),
      response=json.dumps(stored_response),
      confidence=Confidence.UNSURE.value,
      confidence_source=CONFIDENCE_FROM_DIAGNOSTIC,
      elapsed_ms=elapsed_ms,
      correct=int(bool(graded_answer["correct"])) if is_graded else None,
      p_split=entry["p_a"],
      p_compensatory=None,
      served_stage=FadingStage.UNSUPPORTED.value,
      format=ResponseFormat(item["format"]).value,
      per_skill_states=json.dumps({skill: MasteryState(state).value for skill, state in per_skill_states.items()}),
      snapshot_id=session_row.snapshot_id,
      created_at=submitted_at.isoformat(),
      updated_at=submitted_at.isoformat(),
   )
   db.add(attempt)
   db.flush()
   write_rule_diagnosis(db, attempt.id, per_skill_states, graded_answer, submitted_at)

   is_scored = not entry["held_out"]

   if is_scored:
      states = repository.load_states(db, session_row.user_id)
      observation = Observation(
         archetype_id=archetype["id"],
         skills=list(archetype["skills"]),
         per_skill_states=per_skill_states,
         response_format=ResponseFormat(item["format"]),
         confidence=Confidence.UNSURE,
         elapsed_ms=elapsed_ms,
         served_stage=FadingStage.UNSUPPORTED,
      )
      apply_observation(states, engine_graph, observation, today)
      repository.save_states(db, session_row.user_id, states, session_row.snapshot_id, submitted_at)

   diagnostic.record_outcome(run, archetype, outcome_of(graded_answer, not_learned), item_id=item["id"])
   save_run(db, session_row, run)

   return attempt


def result_payload(session_row, unit_titles):
   """08 diagnostic result: unit-level states, never a percentage, and no score."""
   run = load_run(session_row)
   placement = run.placement or {}
   states_by_unit = placement.get("units", {})

   return {
      "session_id": session_row.id,
      "finished": session_row.ended_at is not None,
      "asked": len(run.asked),
      "cap": constants.DIAG_CAP,
      "stop_reason": run.stop_reason,
      "units": [
         {"unit": unit, "title": unit_titles.get(unit, unit), "state": states_by_unit.get(unit, "not_probed")}
         for unit in run.units
      ],
      "unprobeable_units": list(run.unprobeable_units),
   }
