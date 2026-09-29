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


READING_KINDS = ("lesson", "refresher")
SLOT_EVENTS = ("completed", "skipped")
SLOT_BLOCKS = ("block1", "block2")
MILLISECONDS_PER_MINUTE = 60000


def reading_slots(queue):
   """Every lesson and refresher slot of a session queue as (block, position, entry). A queue
   that is not the four-block mapping holds none."""
   is_block_queue = isinstance(queue, dict)

   if not is_block_queue:
      return []

   return [
      (block, position, entry)
      for block in SLOT_BLOCKS
      for position, entry in enumerate(queue.get(block, []))
      if entry.get("kind") in READING_KINDS
   ]


def slot_event_counts(db, session_id):
   """(lesson_id, kind) to the number of completed or skipped events of this session."""
   rows = db.execute(
      select(models.LessonEvent.lesson_id, models.LessonEvent.kind)
      .where(models.LessonEvent.session_id == session_id)
      .where(models.LessonEvent.event.in_(SLOT_EVENTS))
   ).all()
   counts = {}

   for lesson_id, kind in rows:
      counts[(lesson_id, kind)] = counts.get((lesson_id, kind), 0) + 1

   return counts


def consumed_reading_slots(db, session_row):
   """15 Session assembly: a lesson slot is consumed by a completed or skipped event on
   POST /sessions/{id}/lessons/{lesson_id}/events, never by an attempt. Events are matched to the
   slots of their lesson and kind in queue order, as attempts are matched to item slots."""
   remaining = slot_event_counts(db, session_row.id)
   consumed = []

   for block, position, entry in reading_slots(json.loads(session_row.queue)):
      key = (entry["lesson_id"], entry["kind"])
      has_event_left = remaining.get(key, 0) > 0

      if has_event_left:
         remaining[key] -= 1
         consumed.append((block, position))

   return consumed


def consume_lesson_slot(db, session_row, lesson_id, event):
   """The slot a completed or skipped event consumes (15, Endpoints). The route has already
   written the event row, which is the record consumed_reading_slots reads, so this names the slot
   that row took: the last consumed slot of the lesson, or None when the session queue holds no
   slot of that lesson (a read the student opened some other way)."""
   is_slot_event = event in SLOT_EVENTS
   has_session = session_row is not None

   if not is_slot_event or not has_session:
      return None

   queue =json.loads(session_row.queue)
   consumed = consumed_reading_slots(db, session_row)
   of_lesson = [
      (block, position)
      for block, position in consumed
      if queue[block][position]["lesson_id"] == lesson_id
   ]

   if not of_lesson:
      return None

   return of_lesson[-1]


def lesson_bodies(db, pairs):
   bodies = {}

   for lesson_id, version in pairs:
      row = db.get(models.Lesson, (lesson_id, version))

      if row is not None:
         bodies[lesson_id] = row.body

   return bodies


def completion_ratios(db, user_id):
   """read_ms over the authored read_minutes of the band read, one per completed session lesson,
   in completion order (15, Forecast)."""
   rows = db.execute(
      select(models.LessonEvent, models.Lesson)
      .join(
         models.Lesson,
         (models.Lesson.id == models.LessonEvent.lesson_id) & (models.Lesson.version == models.LessonEvent.version),
      )
      .where(models.LessonEvent.user_id == user_id)
      .where(models.LessonEvent.kind == "lesson")
      .where(models.LessonEvent.event == "completed")
      .where(models.LessonEvent.elapsed_ms.is_not(None))
      .order_by(models.LessonEvent.created_at)
   ).all()
   ratios = []

   for event, lesson in rows:
      authored = lesson.read_minutes_brief if event.band == "mid" else lesson.read_minutes_full
      has_authored = authored is not None and authored > 0

      if has_authored:
         ratios.append(event.elapsed_ms / MILLISECONDS_PER_MINUTE / authored)

   return tuple(ratios)


def prerequisite_gaps(db, user_id):
   """(gap id, archetype id) for every diagnosis of this user naming a prerequisite_gap, which T3
   reads (15 Re-teaching). A gap column holds one id or a JSON list of ids."""
   rows = db.execute(
      select(models.Diagnosis.prerequisite_gap, models.Item.archetype_id)
      .join(models.Attempt, models.Attempt.id == models.Diagnosis.attempt_id)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .join(models.Item, models.Item.id == models.Attempt.item_id)
      .where(models.Session.user_id == user_id)
      .where(models.Diagnosis.prerequisite_gap.is_not(None))
   ).all()
   gaps = []

   for gap_text, archetype_id in rows:
      try:
         named = json.loads(gap_text)
      except ValueError:
         named = gap_text

      for gap_id in named if isinstance(named, list) else [named]:
         if isinstance(gap_id, str):
            gaps.append((gap_id, archetype_id))

   return gaps


def write_session_reading(db, user_id, session_id, lessons, deferrals, now=None):
   """What open_session persists after assembly (15, Session assembly and Telemetry): a served
   first-contact lesson writes lesson_state served and a served event with reason and band; a
   deferral writes deferred and a deferred event; a refresher writes its due reason and serving
   time, which the gap rule reads, and a served event of kind refresher."""
   stamp = now_iso(now)

   for entry in lessons:
      is_refresher = entry["kind"] == "refresher"
      kind = "refresher" if is_refresher else "lesson"
      write_event(db, user_id, entry["lesson_id"], entry["version"], kind, "served", session_id=session_id, reason=entry["reason"], band=entry["band"], now=now)

      if is_refresher:
         write_state(db, user_id, entry["lesson_id"], now=now, refresher_due_reason=entry["reason"], refresher_served_at=stamp)
         continue

      existing = lesson_state(db, user_id, entry["lesson_id"])
      first_served_at = existing.first_served_at if existing is not None and existing.first_served_at else stamp
      write_state(
         db,
         user_id,
         entry["lesson_id"],
         now=now,
         status="served",
         band_served=entry["band"],
         first_served_at=first_served_at,
         version_seen=entry["version"],
      )

   served_ids = {entry["lesson_id"] for entry in lessons if entry["kind"] == "lesson"}

   for deferral in deferrals:
      write_event(db, user_id, deferral["lesson_id"], deferral["version"], "lesson", "deferred", session_id=session_id, reason=deferral["reason"], band=deferral["band"], now=now)
      # A lesson deferred at one item and served at a later one in the same session was served.
      is_served_later = deferral["lesson_id"] in served_ids

      if not is_served_later:
         write_state(db, user_id, deferral["lesson_id"], now=now, status=DEFERRED)


def write_bypassed(db, user_id, lesson_ids, now=None):
   for lesson_id in lesson_ids:
      write_state(db, user_id, lesson_id, now=now, status="bypassed_by_placement")


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