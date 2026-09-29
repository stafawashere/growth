"""skills_state, attempts history and the item bank, between the ORM rows and the engine types.

The engine works on the dataclasses in app/engine/state.py and on plain dicts; the database
stores text columns, with JSON arrays for the two sets and ISO strings for every date and
datetime. Column names follow docs/plan/06-architecture.md, so c maps to credited_successes and
f maps to credited_failures.
"""
import json
from datetime import date, datetime

from sqlalchemy import select

from app.db import models
from app.engine.fringe import DictItemBank
from app.engine.state import FadingStage, SkillState

MILLISECONDS_PER_MINUTE = 60000.0
FREE_RESPONSE_FORMAT = "free_response"


def as_iso(value):
   if value is None:
      return None

   return value.isoformat()


def parse_datetime(value):
   """Reads both forms: the service writes timezone-aware UTC, the engine writes naive local dates."""
   if value is None:
      return None

   return datetime.fromisoformat(value)


def parse_date(value):
   if value is None:
      return None

   return date.fromisoformat(value)


def row_to_state(row):
   return SkillState(
      skill_id=row.skill_id,
      beta=row.beta,
      c=row.credited_successes,
      f=row.credited_failures,
      stability=row.stability,
      difficulty=row.difficulty,
      last_practised_at=parse_datetime(row.last_practised_at),
      fading_stage=FadingStage(row.fading_stage),
      observation_count=row.observation_count,
      credited_observation_count=row.credited_observation_count,
      unaided_success_count=row.unaided_success_count,
      distinct_archetypes_succeeded=set(json.loads(row.distinct_archetypes_succeeded)),
      success_days={date.fromisoformat(day) for day in json.loads(row.success_days)},
      mastered=bool(row.mastered),
      mastered_at=parse_datetime(row.mastered_at),
      hypercorrection_due=parse_date(row.hypercorrection_due),
      consecutive_successes=row.consecutive_successes,
      consecutive_failures=row.consecutive_failures,
      concept_opener_done=bool(row.concept_opener_done),
   )


def state_values(state, snapshot_id, now):
   return {
      "snapshot_id": snapshot_id,
      "beta": state.beta,
      "credited_successes": state.c,
      "credited_failures": state.f,
      "stability": state.stability,
      "difficulty": state.difficulty,
      "last_practised_at": as_iso(state.last_practised_at),
      "fading_stage": FadingStage(state.fading_stage).value,
      "observation_count": state.observation_count,
      "credited_observation_count": state.credited_observation_count,
      "unaided_success_count": state.unaided_success_count,
      "distinct_archetypes_succeeded": json.dumps(sorted(state.distinct_archetypes_succeeded)),
      "success_days": json.dumps([day.isoformat() for day in sorted(state.success_days)]),
      "mastered": int(bool(state.mastered)),
      "mastered_at": as_iso(state.mastered_at),
      "hypercorrection_due": as_iso(state.hypercorrection_due),
      "consecutive_successes": state.consecutive_successes,
      "consecutive_failures": state.consecutive_failures,
      "concept_opener_done": int(bool(state.concept_opener_done)),
      "updated_at": as_iso(now),
   }


def load_states(db, user_id):
   rows = db.scalars(
      select(models.SkillState).where(models.SkillState.user_id == user_id)
   ).all()

   return {row.skill_id: row_to_state(row) for row in rows}


def save_states(db, user_id, states, snapshot_id, now):
   """Upsert one row per skill. Rows are seeded at account creation, so an insert is the fallback."""
   existing = {
      row.skill_id: row
      for row in db.scalars(
         select(models.SkillState).where(models.SkillState.user_id == user_id)
      ).all()
   }

   for skill_id, state in states.items():
      values = state_values(state, snapshot_id, now)
      row = existing.get(skill_id)
      is_new = row is None

      if is_new:
         row = models.SkillState(
            user_id=user_id,
            skill_id=skill_id,
            created_at=as_iso(now),
            **values,
         )
         db.add(row)
         continue

      for column, value in values.items():
         setattr(row, column, value)

   db.flush()


def mark_openers_done(db, user_id, skill_ids, now):
   """Sets concept_opener_done on each concept's first skill and writes nothing else of the row,
   because placing the opener is not an observation (02, Session assembly)."""
   for skill_id in skill_ids:
      row = db.get(models.SkillState, (user_id, skill_id))
      has_row = row is not None

      if not has_row:
         continue

      row.concept_opener_done = 1
      row.updated_at = as_iso(now)

   db.flush()


def opener_item_ids(queue_text):
   """The block 2 slots session assembly placed as productive-failure openers."""
   has_queue = bool(queue_text)

   if not has_queue:
      return frozenset()

   queue = json.loads(queue_text)

   return frozenset(
      item["id"]
      for item in queue.get("block2", [])
      if item.get("is_opener") is True
   )


def load_attempts_history(db, user_id):
   """The attempt rows assemble_session reads: requeue, repeat window, forecast and format.

   A diagnostic miss is not marked corrected, because the diagnostic shows no correction, so it
   never comes back through the R5 requeue. A productive-failure opener's miss is not marked
   corrected either: the attempt is expected to fail and carries no credit (02, Session
   assembly), so it is neither requeued nor listed for an error note. A free-response attempt is
   left out altogether: its question is point-graded and may only be served in the four modes R10
   names, so the micro-session's requeue and repeat window must never see it.
   """
   archetype_of = dict(db.execute(select(models.Item.id, models.Item.archetype_id)).all())
   rows = db.execute(
      select(models.Attempt, models.Session.started_at, models.Session.mode, models.Session.queue)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.format != FREE_RESPONSE_FORMAT)
      .order_by(models.Attempt.started_at)
   ).all()
   history = []
   openers_by_session = {}

   for attempt, started_at, mode, queue_text in rows:
      submitted_at = attempt.submitted_at or started_at
      was_diagnostic = mode == "diagnostic"

      if attempt.session_id not in openers_by_session:
         openers_by_session[attempt.session_id] = opener_item_ids(queue_text)

      was_opener = attempt.item_id in openers_by_session[attempt.session_id]
      was_wrong = attempt.correct is not None and attempt.correct == 0
      is_incorrect = was_wrong and not was_diagnostic and not was_opener
      minutes = None
      has_elapsed = attempt.elapsed_ms is not None

      if has_elapsed:
         minutes = attempt.elapsed_ms / MILLISECONDS_PER_MINUTE

      history.append({
         "attempt_id": attempt.id,
         "item_id": attempt.item_id,
         "archetype_id": archetype_of.get(attempt.item_id),
         "attempted_on": datetime.fromisoformat(submitted_at).date(),
         "minutes": minutes,
         "corrected": is_incorrect,
         "stage": FadingStage(attempt.served_stage),
         "confidence": attempt.confidence,
      })

   return history


def load_bank(db, snapshot_id=None):
   query = select(models.Item)
   has_snapshot = snapshot_id is not None

   if has_snapshot:
      query = query.where(models.Item.snapshot_id == snapshot_id)

   items = [
      {
         "id": row.id,
         "archetype_id": row.archetype_id,
         "status": row.status,
      }
      for row in db.scalars(query).all()
   ]

   return DictItemBank(items)
