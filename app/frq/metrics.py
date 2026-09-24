"""Learning-outcome metric 9 (R11, 11 P3 exit criteria, 10 "Learning-outcome metrics"): free-response
items attempted per week, which must hold a non-zero floor in every trial week, and the read-back
abandonment rate, captures started where confirm was never pressed.

An item counts as attempted in the ISO week its read-back was confirmed, photographed or typed. A
capture is started when the student's first photograph of the page is uploaded, whether or not it
passed the quality gate; the typed mode has no read-back to abandon and is not a capture. A capture
still unconfirmed ABANDONED_AFTER_HOURS after it started is abandoned, and a younger one is still
open and counted in neither numerator nor denominator. Both come with their denominators, and a
week with no confirmed item is listed with 0 rather than left out, because the floor is about
empty weeks. app/progress/learning_metrics.py reads the same numbers for the metrics view.

The measurement needs weeks of real use to mean anything, so until then it reports what exists
and says pending_on_usage.
"""
from datetime import datetime, timedelta

from sqlalchemy import select

from app.db import models
from app.frq.items import FRQ_FORMAT

ABANDONED_AFTER_HOURS = 24
TRIAL_WEEKS_NEEDED = 4


def iso_week(moment):
   year, week, _day = moment.isocalendar()

   return f"{year}-W{week:02d}"


def captures(db, user_id):
   return db.execute(
      select(models.Attempt, models.Session.mode)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.format == FRQ_FORMAT)
   ).all()


def photographed_attempt_ids(db, user_id):
   return set(
      db.scalars(
         select(models.FrqImage.attempt_id).where(models.FrqImage.user_id == user_id)
      ).all()
   )


def confirmed_between(db, user_id, first_day, last_day):
   """Read-backs confirmed on the calendar days first_day to last_day, both included."""
   count = 0

   for attempt, _mode in captures(db, user_id):
      if not attempt.transcription_confirmed:
         continue

      confirmed_on = datetime.fromisoformat(attempt.submitted_at or attempt.updated_at).date()
      is_inside = first_day <= confirmed_on <= last_day

      if is_inside:
         count += 1

   return count


def week_span(first, last):
   weeks = []
   cursor = first - timedelta(days=first.weekday())

   while cursor.date() <= last.date():
      weeks.append(iso_week(cursor))
      cursor += timedelta(days=7)

   return weeks


def metric_nine(db, user_id, now):
   rows = captures(db, user_id)
   photographed = photographed_attempt_ids(db, user_id)
   confirmed_weeks = {}
   started = 0
   abandoned = 0
   still_open = 0
   first_capture = None

   for attempt, _mode in rows:
      begun = datetime.fromisoformat(attempt.started_at)
      first_capture = begun if first_capture is None or begun < first_capture else first_capture
      is_confirmed = bool(attempt.transcription_confirmed)

      is_a_capture = attempt.id in photographed

      if is_confirmed:
         confirmed_at = datetime.fromisoformat(attempt.submitted_at or attempt.updated_at)
         week = iso_week(confirmed_at)
         confirmed_weeks[week] = confirmed_weeks.get(week, 0) + 1
         started += int(is_a_capture)
         continue

      if not is_a_capture:
         continue

      age_hours = (now - begun).total_seconds() / 3600
      is_abandoned = age_hours >= ABANDONED_AFTER_HOURS

      if is_abandoned:
         abandoned += 1
         started += 1
      else:
         still_open += 1

   has_captures = first_capture is not None
   weeks = week_span(first_capture, now) if has_captures else []
   per_week = [{"week": week, "items_attempted": confirmed_weeks.get(week, 0)} for week in weeks]
   empty_weeks = [entry["week"] for entry in per_week if entry["items_attempted"] == 0]
   enough_weeks = len(weeks) >= TRIAL_WEEKS_NEEDED

   return {
      "items_attempted_per_week": per_week,
      "weeks_observed": len(weeks),
      "weeks_below_floor": empty_weeks,
      "abandonment": {
         "abandoned": abandoned,
         "captures_started": started,
         "rate": round(abandoned / started, 4) if started else None,
         "still_open": still_open,
      },
      "pending_on_usage": not enough_weeks,
      "definition": (
         "items attempted: read-backs confirmed in the ISO week; abandoned: captures unconfirmed "
         f"{ABANDONED_AFTER_HOURS} hours after they started, over captures started and settled"
      ),
   }
