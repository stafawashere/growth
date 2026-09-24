"""Administering the stable concept probe (app/runtime/probe_set.py) every 8 weeks.

Like the checkpoint, the probe is an instrument: responses go to probe_responses only, graded by
the same deterministic grader practice uses, and nothing reaches sessions, attempts, skills_state
or the review queue. The items are served in the set's fixed order with no feedback, and an item
with options is served as multiple choice, so the format never changes between administrations.

Cadence is every 8 weeks (01 parameter table, [inferred] and tunable), stated as availability only.
"""
import json
import uuid
from datetime import date, timedelta

from sqlalchemy import select

from app.db import models
from app.items.grade import grade
from app.runtime.bank import _as_item_dict
from app.runtime.probe_set import PROBE_SET_NAME, probe_item_ids

CADENCE_DAYS = 56


class ProbeRefused(ValueError):
   pass


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def administrations(db, user_id):
   return db.execute(
      select(models.ProbeAdministration)
      .where(models.ProbeAdministration.user_id == user_id)
      .order_by(models.ProbeAdministration.started_at, models.ProbeAdministration.id)
   ).scalars().all()


def responses_for(db, administration_id):
   return db.execute(
      select(models.ProbeResponse)
      .where(models.ProbeResponse.administration_id == administration_id)
      .order_by(models.ProbeResponse.created_at, models.ProbeResponse.id)
   ).scalars().all()


def ordered_item_ids():
   return sorted(probe_item_ids())


def availability(db, user_id, today):
   rows = administrations(db, user_id)
   current = next((row for row in rows if row.finished_at is None), None)
   finished_days = [date.fromisoformat(row.finished_at[:10]) for row in rows if row.finished_at]
   last_day = max(finished_days) if finished_days else None
   opens_on = last_day + timedelta(days=CADENCE_DAYS) if last_day else None
   is_due = opens_on is None or today >= opens_on
   has_items = len(ordered_item_ids()) > 0

   return {
      "open_administration_id": current.id if current else None,
      "available": current is None and is_due and has_items,
      "opens_on": opens_on.isoformat() if opens_on and not is_due else None,
      "items": len(ordered_item_ids()),
      "cadence_days": CADENCE_DAYS,
   }


def start(db, user_id, now):
   state = availability(db, user_id, now.date())

   if state["open_administration_id"] or not state["available"]:
      raise ProbeRefused("no concept probe is available today")

   stamp = now.isoformat()
   row = models.ProbeAdministration(
      id=new_id("PRB"),
      user_id=user_id,
      probe_set=PROBE_SET_NAME,
      started_at=stamp,
      finished_at=None,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()

   return row


def owned(db, user_id, administration_id):
   row = db.get(models.ProbeAdministration, administration_id)
   is_owned = row is not None and row.user_id == user_id

   if not is_owned:
      raise LookupError(administration_id)

   return row


def served_format(item_row):
   return "mcq" if item_row.options else "short_answer"


def next_item(db, user_id, administration_id):
   row = owned(db, user_id, administration_id)
   answered = {response.item_id for response in responses_for(db, row.id)}

   for item_id in ordered_item_ids():
      if item_id in answered:
         continue

      item_row = db.get(models.Item, item_id)

      if item_row is None:
         raise ProbeRefused(f"probe item {item_id} has no items row")

      return dict(_as_item_dict(item_row), format=served_format(item_row))

   return None


def answer(db, user_id, administration_id, item_id, submitted, elapsed_ms, errors, now):
   row = owned(db, user_id, administration_id)

   if row.finished_at is not None:
      raise ProbeRefused("this probe is finished")

   expected = next_item(db, user_id, administration_id)
   is_expected = expected is not None and expected["id"] == item_id

   if not is_expected:
      raise ProbeRefused("answer the probe items in order")

   item_row = db.get(models.Item, item_id)
   submission = {
      "selected_option_id": submitted.get("option_id"),
      "mathjson": submitted.get("mathjson"),
      "units": submitted.get("units"),
   }
   verdict = grade(item_row, submission, errors, served_format=served_format(item_row))
   correct = verdict.get("correct")
   stamp = now.isoformat()
   response = models.ProbeResponse(
      id=new_id("PRR"),
      user_id=user_id,
      administration_id=row.id,
      item_id=item_id,
      response=json.dumps({name: submitted[name] for name in ("option_id", "mathjson", "units") if name in submitted}),
      correct=None if correct is None else int(bool(correct)),
      elapsed_ms=elapsed_ms,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(response)

   finished_all = next_item(db, user_id, administration_id) is None

   if finished_all:
      row.finished_at = stamp
      row.updated_at = stamp

   db.flush()

   return response


def administration_view(db, row):
   responses = responses_for(db, row.id)
   graded = [response for response in responses if response.correct is not None]

   return {
      "id": row.id,
      "probe_set": row.probe_set,
      "started_at": row.started_at,
      "finished_at": row.finished_at,
      "answered": len(responses),
      "graded": len(graded),
      "correct": sum(response.correct for response in graded),
      "items": len(ordered_item_ids()),
   }


def history(db, user_id):
   return [administration_view(db, row) for row in administrations(db, user_id) if row.finished_at]
