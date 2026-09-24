"""The six-week released-material checkpoint: start, score, finish, history.

The checkpoint is an instrument, so it touches nothing the engine reads (05 "What feeds the mastery
model": no D2, no D3). It writes only checkpoints and checkpoint_scores, never sessions, attempts,
skills_state or the review queue, and the forms it serves are released College Board material
named by reference, never items in the practice bank.

Scoring is recorded by the student against College Board's published scoring guidelines, per part,
so scored_by is "student_self_score". P3's per-point grader may take over once it exists (R10 puts
the six-week checkpoint among the four places per-point grading runs); until then the self score is
what the history reports, and it says so.

Cadence is every 6 weeks (01 "External checkpoint", parameter table, [inferred] and tunable). It is
a measurement cadence and not a schedule: the app says only whether a checkpoint is available.
"""
import uuid
from datetime import date, timedelta

from sqlalchemy import select

from app.checkpoint import forms, published
from app.db import models

CADENCE_DAYS = 42
SCORED_BY_STUDENT = "student_self_score"
EXPECTED_EFFECT_LOW = 0.4
EXPECTED_EFFECT_HIGH = 0.7


class CheckpointRefused(ValueError):
   pass


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def user_checkpoints(db, user_id):
   return db.execute(
      select(models.Checkpoint)
      .where(models.Checkpoint.user_id == user_id)
      .order_by(models.Checkpoint.started_at, models.Checkpoint.id)
   ).scalars().all()


def open_checkpoint(db, user_id):
   for row in user_checkpoints(db, user_id):
      if row.finished_at is None:
         return row

   return None


def last_finished_day(db, user_id):
   finished = [row for row in user_checkpoints(db, user_id) if row.finished_at is not None]

   if not finished:
      return None

   return max(date.fromisoformat(row.finished_at[:10]) for row in finished)


def availability(db, user_id, today):
   used_years = {row.form_year for row in user_checkpoints(db, user_id)}
   upcoming = forms.next_form(used_years)
   current = open_checkpoint(db, user_id)
   last_day = last_finished_day(db, user_id)
   opens_on = last_day + timedelta(days=CADENCE_DAYS) if last_day else None
   is_due = opens_on is None or today >= opens_on
   has_form = upcoming is not None

   return {
      "open_checkpoint_id": current.id if current else None,
      "available": current is None and is_due and has_form,
      "opens_on": opens_on.isoformat() if opens_on and not is_due else None,
      "forms_remaining": len([form for form in forms.forms() if form.year not in used_years]),
      "cadence_days": CADENCE_DAYS,
   }


def start(db, user_id, now):
   today = now.date()
   state = availability(db, user_id, today)

   if state["open_checkpoint_id"]:
      raise CheckpointRefused("a checkpoint is already open")

   if not state["available"]:
      raise CheckpointRefused("no checkpoint is available today")

   used_years = {row.form_year for row in user_checkpoints(db, user_id)}
   form = forms.next_form(used_years)
   stamp = now.isoformat()
   row = models.Checkpoint(
      id=new_id("CKP"),
      user_id=user_id,
      form_year=form.year,
      started_at=stamp,
      finished_at=None,
      scored_by=SCORED_BY_STUDENT,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()

   return row


def owned(db, user_id, checkpoint_id):
   row = db.get(models.Checkpoint, checkpoint_id)
   is_owned = row is not None and row.user_id == user_id

   if not is_owned:
      raise LookupError(checkpoint_id)

   return row


def scores_for(db, checkpoint_id):
   return db.execute(
      select(models.CheckpointScore)
      .where(models.CheckpointScore.checkpoint_id == checkpoint_id)
      .order_by(models.CheckpointScore.question, models.CheckpointScore.part)
   ).scalars().all()


def record_score(db, user_id, checkpoint_id, record_id, points_earned, now):
   row = owned(db, user_id, checkpoint_id)

   if row.finished_at is not None:
      raise CheckpointRefused("a finished checkpoint cannot be rescored")

   form = forms.form_for(row.form_year)
   part = next((candidate for candidate in form.parts if candidate.record_id == record_id), None)

   if part is None:
      raise CheckpointRefused(f"{record_id} is not a part of the {row.form_year} form")

   is_whole = isinstance(points_earned, int) and not isinstance(points_earned, bool)
   is_in_range = is_whole and 0 <= points_earned <= part.points

   if not is_in_range:
      raise CheckpointRefused(f"points earned on {record_id} must be a whole number from 0 to {part.points}")

   stamp = now.isoformat()
   existing = next((score for score in scores_for(db, checkpoint_id) if score.frq_record_id == record_id), None)

   if existing is not None:
      existing.points_earned = points_earned
      existing.updated_at = stamp
      db.flush()

      return existing

   score = models.CheckpointScore(
      id=new_id("CKS"),
      user_id=user_id,
      checkpoint_id=checkpoint_id,
      frq_record_id=record_id,
      question=part.question,
      part=part.part,
      points_possible=part.points,
      points_earned=points_earned,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(score)
   db.flush()

   return score


def finish(db, user_id, checkpoint_id, now):
   row = owned(db, user_id, checkpoint_id)
   form = forms.form_for(row.form_year)
   scored = {score.frq_record_id for score in scores_for(db, checkpoint_id)}
   unscored = [part.record_id for part in form.parts if part.record_id not in scored]

   if unscored:
      raise CheckpointRefused(f"{len(unscored)} parts are not scored yet")

   row.finished_at = now.isoformat()
   row.updated_at = now.isoformat()
   db.flush()

   return row


def question_results(form, scores):
   earned = {}

   for score in scores:
      earned[score.question] = earned.get(score.question, 0) + score.points_earned

   results = []

   for question in form.questions():
      mean, from_years = published.comparison_mean(form.year, question)
      results.append({
         "question": question,
         "earned": earned.get(question, 0),
         "possible": forms.POINTS_PER_QUESTION,
         "published_mean": mean,
         "published_mean_years": list(from_years),
      })

   return results


def checkpoint_view(db, row):
   form = forms.form_for(row.form_year)
   scores = scores_for(db, row.id)
   results = question_results(form, scores)

   return {
      "id": row.id,
      "form_year": row.form_year,
      "started_at": row.started_at,
      "finished_at": row.finished_at,
      "scored_by": row.scored_by,
      "free_response_url": form.free_response_url,
      "scoring_guidelines_url": form.scoring_guidelines_url,
      "sections": forms.section_plan(form),
      "scores": {score.frq_record_id: score.points_earned for score in scores},
      "questions": results,
      "total_earned": sum(result["earned"] for result in results),
      "total_possible": sum(result["possible"] for result in results),
      "published_total": sum(result["published_mean"] or 0.0 for result in results),
   }


def history(db, user_id):
   return [
      checkpoint_view(db, row)
      for row in user_checkpoints(db, user_id)
      if row.finished_at is not None
   ]
