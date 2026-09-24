"""The two P5 evals of docs/plan/11, over a student's stored timed work.

mock_against_published_means: the student's mean points on each free-response position, over their
finished mocks, beside the published 2023 to 2025 means for that position. Only decided points
count; provisional ones are reported beside them, so the comparison never counts a point a grader
has not settled.

pacing_against_budgets: time per question by part against the per-question budget the part's
published count and minutes imply, over every closed timed part. Flagged rapid guesses are left
out of the means, as 05 requires, and every figure carries its denominator.
"""
import statistics

from sqlalchemy import select

from app.assessment import shape
from app.assessment import service as assessment
from app.checkpoint import published
from app.db import models


def finished_mocks(db, user_id):
   return db.scalars(
      select(models.Session)
      .join(models.MockResult, models.MockResult.session_id == models.Session.id)
      .where(models.Session.user_id == user_id)
      .order_by(models.Session.started_at)
   ).all()


def mock_against_published_means(db, user_id, frq_context):
   by_question = {}
   mocks = finished_mocks(db, user_id)

   for session_row in mocks:
      responses = [
         response
         for part in assessment.parts_of(db, session_row.id)
         for response in assessment.responses_of(db, part.id)
         if response.kind == assessment.FREE_RESPONSE_KIND
      ]
      points = assessment.free_response_points(db, assessment.AssessmentContext(archetypes={}, errors={}, engine_graph=None, frq=frq_context), responses)

      for question, entry in points.items():
         by_question.setdefault(question, []).append(entry)

   means = published.question_means()
   rows = []

   for question in sorted(by_question):
      entries = by_question[question]
      rows.append({
         "question": question,
         "mocks": len(entries),
         "mean_earned": statistics.mean(entry["earned"] for entry in entries),
         "pending_points": sum(entry["pending"] for entry in entries),
         "possible": entries[0]["possible"],
         "published": {
            year: means[(year, question)].mean
            for year in published.published_years()
            if (year, question) in means
         },
      })

   return {"available": len(mocks) > 0, "mocks": len(mocks), "questions": rows}


def pacing_against_budgets(db, user_id):
   closed = db.scalars(
      select(models.AssessmentPart)
      .join(models.Session, models.Session.id == models.AssessmentPart.session_id)
      .where(models.AssessmentPart.user_id == user_id)
      .where(models.AssessmentPart.closed_at.is_not(None))
      .where(models.Session.mode.in_(assessment.TIMED_MODES))
   ).all()
   rows = []

   for part_shape in shape.part_shapes():
      parts = [part for part in closed if part.exam_part == part_shape.key]
      seconds = []
      flagged = 0
      questions = 0
      finished_in_time = 0

      for part in parts:
         finished_in_time += int(part.closed_by == assessment.CLOSED_BY_SUBMISSION)

         for response in assessment.responses_of(db, part.id):
            questions += 1

            if response.rapid_guess:
               flagged += 1
               continue

            if response.time_ms > 0:
               seconds.append(response.time_ms / 1000)

      rows.append({
         "part_key": part_shape.key,
         "parts": len(parts),
         "budget_seconds_per_question": part_shape.budget_seconds_per_question,
         "mean_seconds_per_question": statistics.mean(seconds) if seconds else None,
         "questions_timed": {"numerator": len(seconds), "denominator": questions},
         "rapid_guesses": {"numerator": flagged, "denominator": questions},
         "submitted_before_time": {"numerator": finished_in_time, "denominator": len(parts)},
      })

   return {"parts": rows}
