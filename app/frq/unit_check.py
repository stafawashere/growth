"""The free-response part of a unit check, the one assessment mode P3 needs before P5 builds the
others (BUILD-LEDGER.md, decisions of 2026-09-24, stage 4).

05 "Unit check" is untimed and moves the mastery model, which is why P3 carries its free
response here: a unit check session holds the unit's free-response questions, feedback waits
until each question is confirmed and graded, and graded points credit the engine. The
multiple-choice sweep and the set-cover over the unit's skills arrive with P5; this module serves
only the free-response questions, the least-attempted first.
"""
import json
import uuid

from sqlalchemy import func, select

from app.db import models
from app.frq.items import FRQ_FORMAT, served_record

MODE = "unit_check"
QUESTIONS_PER_CHECK = 2


def new_session_id():
   return f"SES-{uuid.uuid4().hex}"


def attempt_counts(db, user_id):
   rows = db.execute(
      select(models.Attempt.item_id, func.count(models.Attempt.id))
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.format == FRQ_FORMAT)
      .group_by(models.Attempt.item_id)
   ).all()

   return dict(rows)


def chosen_questions(context, unit_id, counts, count=QUESTIONS_PER_CHECK, first_item_id=None):
   """The least-attempted questions of the unit, with the one the student asked for, if any, first."""
   candidates = context.records_for_unit(unit_id)
   ordered = sorted(candidates, key=lambda record: (record["id"] != first_item_id, counts.get(record["id"], 0), record["id"]))

   return ordered[:count]


def open_unit_check(db, user_id, context, unit_id, snapshot_id, now, first_item_id=None):
   has_questions = len(context.records_for_unit(unit_id)) > 0

   if not has_questions:
      raise ValueError(f"no free-response question is available for {unit_id}")

   questions = chosen_questions(context, unit_id, attempt_counts(db, user_id), first_item_id=first_item_id)
   stamp = now.isoformat()
   row = models.Session(
      id=new_session_id(),
      user_id=user_id,
      mode=MODE,
      sub_mode=unit_id,
      started_at=stamp,
      ended_at=None,
      queue=json.dumps({"unit_id": unit_id, "frq": [record["id"] for record in questions]}),
      updates_mastery=1,
      snapshot_id=snapshot_id,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()

   return row


def questions_of(session_row, context):
   queue = json.loads(session_row.queue)

   return [served_record(context.records[item_id]) for item_id in queue.get("frq", []) if item_id in context.records]


def holds_question(session_row, item_id):
   return item_id in json.loads(session_row.queue).get("frq", [])
