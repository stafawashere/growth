"""Pacing metrics, 05 "Pacing metrics and rapid-guessing detection".

Pacing is its own metric and never folds into a score. Every budget is computed from the part's
published count and minutes, which app/assessment/shape.py reads, so nothing here states one.

Rapid guessing is flagged per archetype. The threshold is [inferred] and tunable (carried into
docs/plan/12-open-questions.md): once the student has RAPID_GUESS_MIN_ATTEMPTS untimed attempts on
the archetype it is RAPID_GUESS_MEDIAN_SHARE of their median time there, and before that it is
RAPID_GUESS_BASE_SECONDS plus RAPID_GUESS_SECONDS_PER_FACTOR for each of the archetype's
difficulty_factors, 05's named fallback. A question is flagged only when it was answered that fast
and inside the part's final five minutes, because 05 defines the flag as fast answers clustered at
the end of a part. Flagged questions leave the pacing averages and D4 diagnosis.
"""
import statistics
from datetime import datetime

from sqlalchemy import select

from app.assessment.shape import FIVE_MINUTE_ALERT_SECONDS
from app.db import models
from app.frq.items import FRQ_FORMAT

RAPID_GUESS_MIN_ATTEMPTS = 10
RAPID_GUESS_MEDIAN_SHARE = 0.10
RAPID_GUESS_BASE_SECONDS = 4.0
RAPID_GUESS_SECONDS_PER_FACTOR = 2.0
RAPID_GUESS_FLOOR_SECONDS = 2.0


def untimed_latencies(db, user_id, archetype_id):
   rows = db.scalars(
      select(models.Attempt.elapsed_ms)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .join(models.Item, models.Item.id == models.Attempt.item_id)
      .where(models.Session.user_id == user_id)
      .where(models.Session.updates_mastery == 1)
      .where(models.Item.archetype_id == archetype_id)
      .where(models.Attempt.format != FRQ_FORMAT)
      .where(models.Attempt.elapsed_ms.is_not(None))
   ).all()

   return [value / 1000 for value in rows if value > 0]


def rapid_guess_threshold_seconds(archetype, latencies):
   has_enough = len(latencies) >= RAPID_GUESS_MIN_ATTEMPTS

   if has_enough:
      return max(RAPID_GUESS_FLOOR_SECONDS, RAPID_GUESS_MEDIAN_SHARE * statistics.median(latencies))

   factors = len(archetype.get("difficulty_factors") or [])

   return RAPID_GUESS_BASE_SECONDS + RAPID_GUESS_SECONDS_PER_FACTOR * factors


def answered_in_final_minutes(response, part):
   has_times = response.first_answered_at is not None and part.deadline_at is not None

   if not has_times:
      return False

   remaining = (datetime.fromisoformat(part.deadline_at) - datetime.fromisoformat(response.first_answered_at)).total_seconds()

   return remaining <= FIVE_MINUTE_ALERT_SECONDS


def is_rapid_guess(response, part, threshold_seconds):
   is_answered = response.answer is not None
   is_fast = response.time_ms / 1000 < threshold_seconds

   return is_answered and is_fast and answered_in_final_minutes(response, part)


def ratio(numerator, denominator):
   has_denominator = denominator > 0

   return {"numerator": numerator, "denominator": denominator, "value": numerator / denominator if has_denominator else None}


def part_pacing(part, shape, responses, captured_numbers=None):
   """What 05's table lists, per part, each count with its denominator. A free-response question
   is answered on paper, so it counts as answered once its capture is confirmed (captured_numbers)."""
   ordered = sorted(responses, key=lambda response: response.number)
   flagged = [response for response in ordered if response.rapid_guess]
   counted = [response for response in ordered if not response.rapid_guess and response.time_ms > 0]
   captured = set(captured_numbers or ())
   answered = [response for response in ordered if response.answer is not None or response.number in captured]
   revisited = [response for response in answered if response.visits_after_answer > 0]
   limit_seconds = shape.seconds
   remaining_seconds = (part.time_remaining_ms or 0) / 1000 if part.closed_at else None
   used_seconds = limit_seconds - remaining_seconds if remaining_seconds is not None else None
   mean_seconds = statistics.mean(response.time_ms / 1000 for response in counted) if counted else None

   return {
      "part_key": shape.key,
      "label": shape.label,
      "questions": shape.questions,
      "limit_seconds": limit_seconds,
      "budget_seconds_per_question": shape.budget_seconds_per_question,
      "time_used_seconds": used_seconds,
      "time_remaining_seconds": remaining_seconds,
      "closed_by": part.closed_by,
      "mean_seconds_per_question": mean_seconds,
      "mean_counts": ratio(len(counted), len(ordered)),
      "answered": ratio(len(answered), len(ordered)),
      "rapid_guess": ratio(len(flagged), len(ordered)),
      "revisit": ratio(len(revisited), len(answered)),
      "marked": ratio(sum(1 for response in ordered if response.marked), len(ordered)),
      "per_question": [
         {
            "number": response.number,
            "seconds": response.time_ms / 1000,
            "answered": response.answer is not None or response.number in captured,
            "rapid_guess": bool(response.rapid_guess),
            "revisited": response.visits_after_answer > 0,
            "marked": bool(response.marked),
            "eliminator_used": bool(response.eliminator_used),
         }
         for response in ordered
      ],
   }
