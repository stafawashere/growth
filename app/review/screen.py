"""The student's review screen (docs/plan/08-design-brief.md, Information architecture "review" and
the Review wireframe). Distinct from GET /review-queue, which is the operator's queue of item audits.

coming_back is the R5 requeue as block 1 serves it (app/session/build.py requeue_pending): every
item corrected within the last REQUEUE_GAP_DAYS_MAX days and not retried since. An item the
student had rated confident is in the hypercorrection lane, which comes first and returns after
HYPERCORRECTION_GAP_DAYS; the rest return after REQUEUE_GAP_DAYS_MIN.

error_notes are the student's own one-line notes, newest first. Editing one goes through the
existing POST /sessions/{sid}/attempts/{aid}/error-note, which replaces the note, so the payload
carries each note's session id.

provisional_points is the grading-disputes section, and the seam P3 fills. Until gradings exist
it is empty and grading_available is false. P3 appends one entry per provisional point with the
keys named in PROVISIONAL_POINT_KEYS: grading_id (the id POST /gradings/{gid}/dispute takes),
attempt_id, label (the question and part, such as the wireframe's "2026 Q3 part b"), point_label
(the scoring point), reason (the plain-words disagreement 08's provisional-grade copy prints) and
disputed (true once the student has asked for a re-read). The client renders whatever this list
holds, so P3 changes this module and nothing on the screen.
"""
from datetime import datetime, timedelta

from sqlalchemy import select

from app.db import models
from app.engine import constants
from app.session.build import requeue_pending

HYPERCORRECTION = "hypercorrection"
REQUEUE = "requeue"

PROVISIONAL_POINT_KEYS = ("grading_id", "attempt_id", "label", "point_label", "reason", "disputed")


def archetype_label(archetypes, archetype_id):
   record = archetypes.get(archetype_id) or {}

   return record.get("name") or archetype_id


def coming_back_entry(correction, archetypes, today):
   lane = HYPERCORRECTION if correction.was_confident else REQUEUE
   is_hypercorrection = lane == HYPERCORRECTION
   gap_days = constants.HYPERCORRECTION_GAP_DAYS if is_hypercorrection else constants.REQUEUE_GAP_DAYS_MIN
   returns_on = correction.corrected_on + timedelta(days=gap_days)
   days_until = max(0, (returns_on - today).days)

   return {
      "item_id": correction.item_id,
      "attempt_id": correction.attempt_id,
      "label": archetype_label(archetypes, correction.archetype_id),
      "lane": lane,
      "confidence": correction.confidence,
      "corrected_on": correction.corrected_on.isoformat(),
      "returns_on": max(returns_on, today).isoformat(),
      "days_until": days_until,
   }


def written_day(attempt, started_at):
   stamp = attempt.submitted_at or started_at

   return datetime.fromisoformat(stamp).date().isoformat()


def error_notes(db, user_id, archetypes):
   rows = db.execute(
      select(models.Attempt, models.Session.started_at, models.Item.archetype_id)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .outerjoin(models.Item, models.Item.id == models.Attempt.item_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.error_note.is_not(None))
      .order_by(models.Attempt.submitted_at.desc(), models.Attempt.id.desc())
   ).all()

   return [
      {
         "attempt_id": attempt.id,
         "session_id": attempt.session_id,
         "note": attempt.error_note,
         "written_on": written_day(attempt, started_at),
         "label": archetype_label(archetypes, archetype_id),
      }
      for attempt, started_at, archetype_id in rows
   ]


def review_screen(db, user_id, archetypes, attempts_history, today):
   pending = requeue_pending(attempts_history, today)

   return {
      "today": today.isoformat(),
      "coming_back": [coming_back_entry(correction, archetypes, today) for correction in pending],
      "error_notes": error_notes(db, user_id, archetypes),
      "grading_available": False,
      "provisional_points": [],
   }
