"""Reads and writes of the lesson tables for the routes and, later, the session layer
(docs/lessons/BUILD-PLAN.md Slice L1; docs/plan/15-lessons.md, State, and API, migrations,
telemetry).

Only a signed_off, non stale row is servable (15, invariant L8; the ingest has already refused
signed_off to any record with a lint finding or a missing re-solve verdict). A missing
lesson_state row reads as unseen, so nothing here writes one on a read.
"""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from app.db import models

ROOT = Path(__file__).resolve().parents[2]
CURRICULUM_PATH = ROOT / "data" / "curriculum.json"

SIGNED_OFF = "signed_off"
UNSEEN = "unseen"
DEFERRED = "deferred"
COMING_UP = "coming_up"
NOT_AVAILABLE = "not_available"
NOT_YET_READ = (UNSEEN, DEFERRED)
STATE_FIELDS = (
   "status",
   "version_seen",
   "band_served",
   "first_served_at",
   "read_at",
   "read_source",
   "refresher_due_reason",
   "refresher_served_at",
   "refresher_count",
)


def now_iso(now=None):
   return (now or datetime.now(timezone.utc)).isoformat()


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def servable_rows(db):
   rows = db.scalars(
      select(models.Lesson)
      .where(models.Lesson.status == SIGNED_OFF)
      .order_by(models.Lesson.id, models.Lesson.version)
   ).all()
   latest = {}

   for row in rows:
      latest[row.id] = row

   return list(latest.values())


def servable_map(db):
   """Target id (a BC-CON, BC-PRQ or BC-UNIT id) to (lesson_id, version) of its servable lesson,
   the highest signed_off version of each lesson."""
   return {row.target_id: (row.id, row.version) for row in servable_rows(db)}


def servable(db, concept_id):
   found = servable_map(db).get(concept_id)

   if found is None:
      return None

   return db.get(models.Lesson, found)


def servable_lesson(db, lesson_id, version=None):
   """The lesson row a reader may open: the latest signed_off version, or the named version when
   it is signed_off. None for an unknown lesson or one with no signed_off version."""
   is_named_version = version is not None

   if is_named_version:
      row = db.get(models.Lesson, (lesson_id, version))
      is_servable = row is not None and row.status == SIGNED_OFF

      return row if is_servable else None

   for row in servable_rows(db):
      if row.id == lesson_id:
         return row

   return None


def state_as_dict(row):
   if row is None:
      return None

   state = {"lesson_id": row.lesson_id}

   for name in STATE_FIELDS:
      state[name] = getattr(row, name)

   state["updated_at"] = row.updated_at

   return state


def lesson_state(db, user_id, lesson_id):
   return db.get(models.LessonState, (user_id, lesson_id))


def lesson_states(db, user_id):
   rows = db.scalars(select(models.LessonState).where(models.LessonState.user_id == user_id)).all()

   return {row.lesson_id: state_as_dict(row) for row in rows}


def write_state(db, user_id, lesson_id, now=None, **fields):
   unknown = set(fields) - set(STATE_FIELDS)

   if unknown:
      raise ValueError(f"not lesson_state fields: {sorted(unknown)}")

   timestamp = now_iso(now)
   row = lesson_state(db, user_id, lesson_id)
   is_new = row is None

   if is_new:
      row = models.LessonState(
         user_id=user_id,
         lesson_id=lesson_id,
         status=fields.get("status", UNSEEN),
         refresher_count=0,
         created_at=timestamp,
         updated_at=timestamp,
      )
      db.add(row)

   for name, value in fields.items():
      setattr(row, name, value)

   row.updated_at = timestamp
   db.flush()

   return row


def write_event(db, user_id, lesson_id, version, kind, event, session_id=None, section_id=None, mode=None, reason=None, band=None, elapsed_ms=None, now=None):
   timestamp = now_iso(now)
   row = models.LessonEvent(
      id=new_id("LEV"),
      user_id=user_id,
      session_id=session_id,
      lesson_id=lesson_id,
      version=version,
      kind=kind,
      event=event,
      section_id=section_id,
      mode=mode,
      reason=reason,
      band=band,
      elapsed_ms=elapsed_ms,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(row)
   db.flush()

   return row


def write_check_response(db, user_id, lesson_id, version, check_id, response, correct, error_id, elapsed_ms, now=None):
   timestamp = now_iso(now)
   is_graded = correct is not None
   row = models.LessonCheckResponse(
      id=new_id("LCR"),
      user_id=user_id,
      lesson_id=lesson_id,
      version=version,
      check_id=check_id,
      response=json.dumps(response),
      correct=int(correct) if is_graded else None,
      error_id=error_id,
      elapsed_ms=elapsed_ms,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(row)
   db.flush()

   return row


def consume_lesson_slot(db, session_row, lesson_id, event):
   """The session's lesson slot is consumed on completed or skipped (15, Endpoints). The session
   queue belongs to app/session, which wires this in a later slice; until then the event row the
   route writes is the only record, and nothing in the queue moves."""
   return None


def load_curriculum(path=CURRICULUM_PATH):
   return json.loads(Path(path).read_text())


def concepts_in_unit(unit, snapshot):
   topic_order = {topic_id: index for index, topic_id in enumerate(unit.get("topics") or [])}
   last = len(topic_order)
   concepts = [concept for concept in snapshot.concepts.values() if concept.get("unit") == unit["id"]]

   def position(concept):
      topics = concept.get("topics") or []
      first = min((topic_order.get(topic_id, last) for topic_id in topics), default=last)

      return (first, concept["id"])

   return sorted(concepts, key=position)


def listing_state(found, state):
   has_lesson = found is not None

   if not has_lesson:
      return NOT_AVAILABLE

   status = state["status"] if state is not None else UNSEEN
   is_not_yet_read = status in NOT_YET_READ

   return COMING_UP if is_not_yet_read else status


def concept_entry(concept, servable_targets, states):
   found = servable_targets.get(concept["id"])
   lesson_id, version = found if found is not None else (None, None)
   state = states.get(lesson_id) if lesson_id is not None else None

   return {
      "concept_id": concept["id"],
      "name": concept.get("name"),
      "lesson_id": lesson_id,
      "version": version,
      "servable": found is not None,
      "state": listing_state(found, state),
      "read_at": state["read_at"] if state is not None else None,
   }


def library_listing(db, user_id, snapshot, unit_id=None, curriculum=None):
   """The GET /lessons payload: units in data/curriculum.json order, each unit's concepts in the
   order of their first topic, each with its servable lesson and the user's state."""
   curriculum = curriculum if curriculum is not None else load_curriculum()
   servable_targets = servable_map(db)
   states = lesson_states(db, user_id)
   units = []

   for order, unit in enumerate(curriculum["units"], start=1):
      is_other_unit = unit_id is not None and unit["id"] != unit_id

      if is_other_unit:
         continue

      units.append({
         "id": unit["id"],
         "name": unit.get("name"),
         "order": unit.get("number", order),
         "concepts": [concept_entry(concept, servable_targets, states) for concept in concepts_in_unit(unit, snapshot)],
      })

   return {"units": units}