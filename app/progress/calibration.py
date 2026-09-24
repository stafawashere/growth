"""The item-level calibration curve on the progress screen (docs/plan/08-design-brief.md,
"Progress"; 11-phased-delivery.md P2 scope item 6).

An attempt counts when all of these hold:

- it belongs to the user and carries a verdict (attempts.correct is not null);
- its rating came from the student (attempts.confidence_source is student). The rating is
  collected after the commit and before feedback at every stage, and render_feedback refuses to
  build feedback for an unrated submitted attempt, so every student rating is a pre-feedback one.
  A rating close_session swept in as unsure is not the student's and is left out, and so is a
  legacy unsure the migration could not attribute;
- it was submitted inside the last WINDOW_DAYS calendar days ending on the requested day, the
  "Calibration, last 30 days" heading of 08's wireframe.

Every stage and every session mode counts, because 10-quality-and-evaluation.md defines
calibration over all items carrying a rating.

The curve reports, per confidence level, the attempt count, the count correct, the observed
accuracy and a Wilson 95 percent interval on it. No summary statistic is reported. 10 names two,
the Brier score and confidence minus accuracy, and both need each rating mapped to a
probability, which no plan document fixes, so the record carries counts and accuracies only.
"""
import math
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import select

from app.db import models
from app.engine.state import Confidence
from app.session.service import CONFIDENCE_FROM_STUDENT

MINIMUM_RATED_ATTEMPTS = 30

WINDOW_DAYS = 30

WILSON_Z_95 = 1.959963984540054

CONFIDENCE_ORDER = (Confidence.GUESS, Confidence.UNSURE, Confidence.CONFIDENT)


@dataclass(frozen=True)
class RatedAttempt:
   confidence: Confidence
   correct: bool


@dataclass(frozen=True)
class CalibrationBin:
   confidence: Confidence
   attempts: int
   correct: int
   accuracy: float | None
   interval_low: float | None
   interval_high: float | None


@dataclass(frozen=True)
class CalibrationRecord:
   rated_attempts: int
   bins: tuple[CalibrationBin, ...]

   @property
   def available(self):
      return self.rated_attempts >= MINIMUM_RATED_ATTEMPTS

   @property
   def attempts_needed(self):
      return max(0, MINIMUM_RATED_ATTEMPTS - self.rated_attempts)


def wilson_interval(successes, trials, z=WILSON_Z_95):
   has_trials = trials > 0

   if not has_trials:
      raise ValueError("a Wilson interval needs at least one trial")

   proportion = successes / trials
   z_squared = z * z
   denominator = 1 + z_squared / trials
   centre = (proportion + z_squared / (2 * trials)) / denominator
   spread = z * math.sqrt(proportion * (1 - proportion) / trials + z_squared / (4 * trials * trials))
   half_width = spread / denominator

   return max(0.0, centre - half_width), min(1.0, centre + half_width)


def calibration_bin(confidence, outcomes):
   attempts = len(outcomes)
   correct = sum(1 for outcome in outcomes if outcome)
   has_attempts = attempts > 0

   if not has_attempts:
      return CalibrationBin(confidence, 0, 0, None, None, None)

   low, high = wilson_interval(correct, attempts)

   return CalibrationBin(confidence, attempts, correct, correct / attempts, low, high)


def calibration_record(rated_attempts):
   outcomes_by_level = {level: [] for level in CONFIDENCE_ORDER}

   for rated in rated_attempts:
      outcomes_by_level[Confidence(rated.confidence)].append(bool(rated.correct))

   bins = tuple(calibration_bin(level, outcomes_by_level[level]) for level in CONFIDENCE_ORDER)
   total = sum(entry.attempts for entry in bins)

   return CalibrationRecord(rated_attempts=total, bins=bins)


def window_bounds(day):
   return day - timedelta(days=WINDOW_DAYS - 1), day


def counted_attempts(db, user_id, day):
   first_day, last_day = window_bounds(day)
   rows = db.execute(
      select(models.Attempt.confidence, models.Attempt.correct, models.Attempt.submitted_at)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.correct.is_not(None))
      .where(models.Attempt.confidence.is_not(None))
      .where(models.Attempt.confidence_source == CONFIDENCE_FROM_STUDENT)
      .where(models.Attempt.submitted_at.is_not(None))
   ).all()

   counted = []

   for confidence, correct, submitted_at in rows:
      submitted_day = submitted_at[:10]
      is_after_start = submitted_day >= first_day.isoformat()
      is_before_end = submitted_day <= last_day.isoformat()
      is_in_window = is_after_start and is_before_end

      if is_in_window:
         counted.append(RatedAttempt(Confidence(confidence), bool(correct)))

   return counted


def bin_view(entry):
   return {
      "confidence": entry.confidence.value,
      "attempts": entry.attempts,
      "correct": entry.correct,
      "accuracy": entry.accuracy,
      "interval_low": entry.interval_low,
      "interval_high": entry.interval_high,
   }


def calibration_view(record, day):
   """Below MINIMUM_RATED_ATTEMPTS the bins list is empty, so no client can draw a curve from
   too few attempts; the count and the shortfall are still stated."""
   first_day, last_day = window_bounds(day)
   bins = [bin_view(entry) for entry in record.bins] if record.available else []

   return {
      "available": record.available,
      "rated_attempts": record.rated_attempts,
      "minimum_rated_attempts": MINIMUM_RATED_ATTEMPTS,
      "attempts_needed": record.attempts_needed,
      "window_days": WINDOW_DAYS,
      "window_start": first_day.isoformat(),
      "window_end": last_day.isoformat(),
      "bins": bins,
   }


def user_calibration(db, user_id, day):
   return calibration_view(calibration_record(counted_attempts(db, user_id, day)), day)
