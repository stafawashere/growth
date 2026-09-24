"""Home's view of today's queue (docs/plan/08-design-brief.md, "Home, today's queue").

The preview runs the Session assembly rule of docs/plan/02-adaptive-engine.md exactly as
open_session does, over the same stored states and attempt history, and persists nothing: no
sessions row, and no coverage gap audit row, because assemble_session writes one only when handed
a db. Every number below is read off that assembled Session, so the forecast on home is the
forecast the assembly rule computes and not a second estimate of it.

The wireframe counts skills on two lines and items on the third, while the queue is made of items.
The skill readings are kept, because each block's items are chosen for skills, and each count is
defined against the block that holds it:

skills_due_for_review, block 1 minus its corrected-item requeues: the distinct skills among those
items that next_item_review would pool, meaning due under the retention target or carrying a
hypercorrection due date. A block 1 item is picked for any skill it exercises, not only its primary.

frontier_skills, block 2: the distinct primary skills of its items, since fringe candidates are
admitted by primary skill (app/engine/fringe.py, candidates).

corrected_items_returning, block 1: the items served through the R5 requeue, counted as items
because the wireframe counts them as items and the requeue returns a named item.

forecast_minutes, blocks 1 to 3: Session.forecast_total. Block 4 serves no items and so adds none.

due_today_skills and due_today_minutes, the whole of today's due queue (Session.due_queue), which
block 1 serves only the first 5 items or 5 minutes of: the count of mastered skills below the
retention target, and the forecast over the archetypes that cover them, the archetypes serving a
hypercorrection that has come due and the corrected items returning. Both are finite for any day,
because the queue is built from a finite skill set.

The preview predicts POST /sessions only if both read the same assembly inputs, so the day and the
rng for both routes come from one place: the requested day, or the server's date when none is sent,
and an rng seeded by the process seed, the user and that day. Two reads on one day agree, and the session
opened that day assembles the queue the preview counted.

user_assembly_inputs adds the user id to that seed, so two students on one day do not share a
draw. The user id is minted at random on registration, so under it the process seed no longer
fixes which archetype a given run serves, and a test that needs a particular archetype has to
make it certain rather than rely on the seed.
"""
import random
from datetime import date, datetime

from sqlalchemy import select

from app.db import models
from app.engine import constants
from app.engine.select import due_skills, hypercorrection_skills, retrievability_map
from app.session import repository
from app.session.build import assemble_session


class UnreadableDay(ValueError):
   pass


def assembly_day(requested):
   is_given = isinstance(requested, str) and requested != ""

   if not is_given:
      return date.today()

   try:
      return date.fromisoformat(requested)
   except ValueError as unreadable:
      raise UnreadableDay("today is not an ISO 8601 calendar date") from unreadable


def user_assembly_rng(process_seed, user_id, today):
   return random.Random(f"{process_seed}:{user_id}:{today.isoformat()}")


def user_assembly_inputs(process_seed, user_id, requested_day):
   """The day and the rng that GET /progress and POST /sessions both assemble with."""
   today = assembly_day(requested_day)

   return today, user_assembly_rng(process_seed, user_id, today)


HOME_FIRST_LOGIN = "first_login"
HOME_LONG_GAP = "long_gap"
HOME_QUEUE = "queue"

DIAGNOSTIC_MODE = "diagnostic"

ASSESSMENT_MODES = ("unit_check", "part_drill", "mock")


def open_session_id(db, user_id, diagnostic=False):
   """The newest unfinished session of the one kind asked for: a diagnostic resumes on the
   onboarding screen, a micro-session on the session screen. A unit check, a part drill or a mock
   resumes from the mock exam screen's own list (GET /assessments/unfinished), never from home."""
   mode_matches = (
      models.Session.mode == DIAGNOSTIC_MODE
      if diagnostic
      else models.Session.mode.not_in((DIAGNOSTIC_MODE, *ASSESSMENT_MODES))
   )
   statement = (
      select(models.Session.id)
      .where(models.Session.user_id == user_id)
      .where(models.Session.ended_at.is_(None))
      .where(mode_matches)
      .order_by(models.Session.started_at.desc(), models.Session.id)
      .limit(1)
   )

   return db.scalars(statement).first()


def last_session_day(db, user_id):
   statement = (
      select(models.Session.started_at)
      .where(models.Session.user_id == user_id)
      .order_by(models.Session.started_at.desc())
      .limit(1)
   )
   started_at = db.scalars(statement).first()

   if started_at is None:
      return None

   return datetime.fromisoformat(started_at).date()


def home_state(db, user_id, today):
   """08 home: first login runs the onboarding diagnostic, a gap over GAP_DAYS_DIAGNOSTIC days since
   the last session offers a re-diagnostic instead of the queue (02, Decay), anything else is the
   queue. The gap counts calendar days from the day the last session started."""
   last_day = last_session_day(db, user_id)

   if last_day is None:
      return HOME_FIRST_LOGIN, None

   gap_days = (today - last_day).days
   is_long_gap = gap_days > constants.GAP_DAYS_DIAGNOSTIC

   if is_long_gap:
      return HOME_LONG_GAP, gap_days

   return HOME_QUEUE, gap_days


def reviewable_skills(states, graph, today):
   retrievability = retrievability_map(states, today, None)

   return due_skills(states, graph, today, retrievability) | hypercorrection_skills(states, today)


def queue_preview(db, user_id, graph, bank, today, rng):
   states = repository.load_states(db, user_id)
   history = repository.load_attempts_history(db, user_id)
   reviewable = reviewable_skills(states, graph, today)
   session = assemble_session(states, graph, bank, None, history, rng, today)

   requeued_ids = {item["id"] for item in session.requeued}
   reviewed_items = [item for item in session.block1 if item["id"] not in requeued_ids]
   due_touched = {
      skill_id
      for item in reviewed_items
      for skill_id in graph.archetypes[item["archetype_id"]]["skills"]
      if skill_id in reviewable
   }
   frontier = {graph.primary_skill(item["archetype_id"]) for item in session.block2}

   state, gap_days = home_state(db, user_id, today)

   return {
      "home_state": state,
      "days_since_last_session": gap_days,
      "diagnostic_in_progress": open_session_id(db, user_id, diagnostic=True),
      "skills_due_for_review": len(due_touched),
      "frontier_skills": len(frontier),
      "corrected_items_returning": len(session.requeued),
      "forecast_minutes": session.forecast_total,
      "due_today_skills": len(session.due_queue.skills),
      "due_today_minutes": session.due_queue.minutes,
      "session_in_progress": open_session_id(db, user_id),
   }