"""The learning-outcome metrics of docs/plan/10 "Learning-outcome metrics", each with its
denominator (11 P7 exit criterion: "a count without a denominator is not a claim").

Every value carries a numerator where one exists, a denominator and what the denominator counts.
A metric with nothing to count is still returned, with a zero denominator and status no_data, so
the absence is stated rather than hidden. The external checkpoint and the concept probe are
reported here too, beside the internal numbers and never merged with them.

Readings this module fixes, which no plan document does:

- Mastery growth counts a skill once it is mastered with at least the mastery rule's 3 unaided
  successes, so skills placed by the diagnostic or seeded at registration, which carry none, are
  not counted as growth. Study time is the sum of logged item time on practice attempts.
- Retention reads each practice attempt against the previous attempt on the same primary skill:
  when that one was a success 5 to 9 or 25 to 35 days earlier, the attempt is a first attempt
  after that interval and counts in the bucket.
- Calibration maps a rating to a probability before scoring, guess 0.25, unsure 0.60, confident
  0.90. The guess value is the four-option chance floor 02 uses; the other two are [inferred].
- Method selection against execution is read off multiple-choice attempts. A distractor whose
  violated_step is 0, the first step of the item's worked solution, is a method-selection error;
  any other distractor is an execution error made after a right choice of method. Method accuracy
  is the share of graded multiple-choice attempts without a step-0 error; execution accuracy is
  the share correct among those. Short answers carry no step and are not counted. [inferred]
- Error recurrence reads 10's "diagnosed at least twice" as at least once: for each BC-ERR, the
  later practice attempts within 30 days of its first diagnosis on items loading one of the skills
  that attempt loaded are the denominator, and those diagnosed with the same BC-ERR the numerator.
- Adherence counts a day when a practice session ended on it, over the days from the first
  practice day to today. Nothing stores the queue of a day the app was not opened, so every day in
  that span is taken to have had a due queue. [inferred]
"""
import json
import statistics
from datetime import date, timedelta

from sqlalchemy import select

from app.checkpoint import probe as probe_service
from app.checkpoint import service as checkpoint_service
from app.db import models
from app.engine import constants
from app.progress.attempt_log import load_attempts
from app.session.service import CONFIDENCE_FROM_STUDENT

GROWTH_WINDOW_DAYS = 14
CALIBRATION_WINDOW_DAYS = 30
RECURRENCE_WINDOW_DAYS = 30
PARTICIPATION_WINDOW_DAYS = 7
RETENTION_BUCKETS = (("7_day", 5, 9), ("30_day", 25, 35))
CONFIDENCE_PROBABILITY = {"guess": 0.25, "unsure": 0.60, "confident": 0.90}
METHOD_STEP = 0
REHEARSAL_MODE = "rehearsal"
FREE_RESPONSE_FORMAT = "free_response"
MS_PER_HOUR = 3_600_000


def value(label, numerator, denominator, denominator_label, measured=None):
   """measured defaults to numerator over denominator; None when the denominator is 0."""
   has_denominator = denominator > 0

   if measured is None and has_denominator and numerator is not None:
      measured = numerator / denominator

   return {
      "label": label,
      "value": measured if has_denominator else None,
      "numerator": numerator,
      "denominator": denominator,
      "denominator_label": denominator_label,
   }


def metric(key, name, values, definition, window=None):
   has_data = any(entry["denominator"] > 0 for entry in values)

   return {
      "key": key,
      "name": name,
      "status": "measured" if has_data else "no_data",
      "definition": definition,
      "window": window,
      "values": values,
   }


def in_window(record, first_day, last_day):
   return first_day <= record.day <= last_day


def practice(attempts):
   return [record for record in attempts if record.updates_mastery]


def mastery_growth(db, user_id, attempts, today):
   first_day = today - timedelta(days=GROWTH_WINDOW_DAYS - 1)
   rows = db.execute(
      select(models.SkillState.mastered_at, models.SkillState.unaided_success_count)
      .where(models.SkillState.user_id == user_id)
      .where(models.SkillState.mastered == 1)
      .where(models.SkillState.mastered_at.is_not(None))
   ).all()
   newly_mastered = 0

   for mastered_at, unaided in rows:
      mastered_day = date.fromisoformat(mastered_at[:10])
      is_in_window = first_day <= mastered_day <= today
      was_earned = unaided >= constants.MASTERY_MIN_UNAIDED_SUCCESSES

      if is_in_window and was_earned:
         newly_mastered += 1

   milliseconds = sum(
      record.elapsed_ms or 0
      for record in practice(attempts)
      if in_window(record, first_day, today)
   )
   hours = milliseconds / MS_PER_HOUR
   entry = value("skills newly mastered per study hour", newly_mastered, hours, "hours of logged item time")
   entry["denominator"] = round(hours, 4)

   return metric(
      "mastery_growth",
      "Mastery growth per study hour",
      [entry],
      "Skills newly meeting the mastery rule with its 3 unaided successes, over logged item time.",
      {"start": first_day.isoformat(), "end": today.isoformat()},
   )


def retention(attempts):
   last_by_skill = {}
   buckets = {name: [] for name, _, _ in RETENTION_BUCKETS}

   for record in practice(attempts):
      is_graded = record.correct is not None
      has_skill = record.primary_skill is not None

      if not (is_graded and has_skill):
         continue

      previous = last_by_skill.get(record.primary_skill)
      last_by_skill[record.primary_skill] = record
      follows_a_success = previous is not None and previous.correct is True

      if not follows_a_success:
         continue

      gap = (record.day - previous.day).days

      for name, low, high in RETENTION_BUCKETS:
         if low <= gap <= high:
            buckets[name].append(1 if record.correct else 0)

   values = [
      value(
         f"first-attempt accuracy {low} to {high} days after a success",
         sum(buckets[name]),
         len(buckets[name]),
         "first attempts in the interval",
      )
      for name, low, high in RETENTION_BUCKETS
   ]

   return metric(
      "retention_7_30",
      "Retention at 7 and 30 days",
      values,
      "First-attempt accuracy on a skill after an interval since its last success, against the desired retention that scheduled it.",
   )


def calibration(attempts, today):
   first_day = today - timedelta(days=CALIBRATION_WINDOW_DAYS - 1)
   rated = [
      record
      for record in attempts
      if record.confidence_source == CONFIDENCE_FROM_STUDENT
      and record.confidence in CONFIDENCE_PROBABILITY
      and record.correct is not None
      and in_window(record, first_day, today)
   ]
   count = len(rated)
   squared = sum((CONFIDENCE_PROBABILITY[record.confidence] - (1.0 if record.correct else 0.0)) ** 2 for record in rated)
   confidence_total = sum(CONFIDENCE_PROBABILITY[record.confidence] for record in rated)
   correct_total = sum(1 for record in rated if record.correct)
   gap = (confidence_total - correct_total) / count if count else None

   return metric(
      "calibration",
      "Calibration",
      [
         value("Brier score", None, count, "rated attempts", squared / count if count else None),
         value("confidence minus accuracy", None, count, "rated attempts", gap),
      ],
      "Ratings mapped to guess 0.25, unsure 0.60, confident 0.90. Brier is the mean squared gap to the outcome; confidence minus accuracy gives its sign.",
      {"start": first_day.isoformat(), "end": today.isoformat()},
   )


def option_steps(db, item_ids):
   rows = db.execute(select(models.Item.id, models.Item.options).where(models.Item.id.in_(sorted(item_ids)))).all()
   steps = {}

   for item_id, options in rows:
      for option in options or []:
         steps[(item_id, option.get("id"))] = option.get("violated_step")

   return steps


def method_and_execution(db, attempts):
   multiple_choice = [
      record
      for record in practice(attempts)
      if record.format == "mcq" and record.correct is not None and record.response.get("option_id")
   ]
   steps = option_steps(db, {record.item_id for record in multiple_choice})
   method_right = []

   for record in multiple_choice:
      chosen_step = steps.get((record.item_id, record.response.get("option_id")))
      chose_wrong_method = record.correct is False and chosen_step == METHOD_STEP

      if not chose_wrong_method:
         method_right.append(record)

   executed = sum(1 for record in method_right if record.correct)

   return metric(
      "method_selection",
      "Method selection against execution",
      [
         value("method-selection accuracy", len(method_right), len(multiple_choice), "graded multiple-choice attempts"),
         value("execution accuracy", executed, len(method_right), "attempts with the method chosen right"),
      ],
      "A distractor whose violated step is the first worked-solution step is a method error; any other distractor is an execution error.",
   )


def error_recurrence(db, attempts):
   by_attempt = {record.id: record for record in practice(attempts)}
   rows = db.execute(
      select(models.Diagnosis.attempt_id, models.Diagnosis.observed_errors)
      .where(models.Diagnosis.attempt_id.in_(sorted(by_attempt)))
   ).all()
   errors_by_attempt = {attempt_id: set(json.loads(observed or "[]")) for attempt_id, observed in rows}
   ordered = [record for record in practice(attempts) if record.correct is not None]
   first_seen = {}

   for record in ordered:
      for error_id in sorted(errors_by_attempt.get(record.id, ())):
         first_seen.setdefault(error_id, record)

   exposures = 0
   recurrences = 0

   for error_id, first in sorted(first_seen.items()):
      loaded = set(first.skills)
      last_day = first.day + timedelta(days=RECURRENCE_WINDOW_DAYS)

      for record in ordered:
         is_later = record.submitted_at > first.submitted_at and record.day <= last_day
         shares_a_skill = len(loaded & set(record.skills)) > 0

         if is_later and shares_a_skill:
            exposures += 1
            recurrences += error_id in errors_by_attempt.get(record.id, ())

   return metric(
      "error_recurrence",
      "Error-type recurrence",
      [
         value("recurrence rate", recurrences, exposures, "later attempts loading the same skills within 30 days"),
         value("error types diagnosed", len(first_seen), len(ordered), "graded practice attempts"),
      ],
      "For each diagnosed BC-ERR, the share of later attempts on the same skills in the next 30 days that show it again.",
   )


def adherence_and_effort(db, user_id, attempts, today):
   rows = db.execute(
      select(models.Session.id, models.Session.started_at, models.Session.ended_at)
      .where(models.Session.user_id == user_id)
      .where(models.Session.updates_mastery == 1)
      .where(models.Session.mode != "diagnostic")
   ).all()
   started_days = [date.fromisoformat(started_at[:10]) for _, started_at, _ in rows]
   ended_days = {date.fromisoformat(ended_at[:10]) for _, _, ended_at in rows if ended_at}
   first_day = min(started_days) if started_days else None
   span = (today - first_day).days + 1 if first_day else 0
   items_per_session = {}

   for record in practice(attempts):
      items_per_session[record.session_id] = items_per_session.get(record.session_id, 0) + 1

   counts = sorted(items_per_session.values())
   seconds = [record.elapsed_ms / 1000 for record in practice(attempts) if record.elapsed_ms]

   return metric(
      "adherence_effort",
      "Adherence against effort",
      [
         value("days with a completed session", len(ended_days), span, "days since the first practice day"),
         value("median items per session", None, len(counts), "sessions with an attempt", statistics.median(counts) if counts else None),
         value("median seconds per item", None, len(seconds), "timed attempts", statistics.median(seconds) if seconds else None),
      ],
      "Adherence holding while items per session falls is the token-session signature to watch.",
   )


def free_response_participation(attempts, today):
   first_day = today - timedelta(days=PARTICIPATION_WINDOW_DAYS - 1)
   free_response = [
      record
      for record in attempts
      if record.format == FREE_RESPONSE_FORMAT and in_window(record, first_day, today)
   ]
   captures = [record for record in attempts if record.image_ids]
   abandoned = sum(1 for record in captures if not record.transcription_confirmed)

   return metric(
      "free_response_participation",
      "Free-response participation and read-back abandonment",
      [
         value("free-response items attempted", len(free_response), PARTICIPATION_WINDOW_DAYS, "days"),
         value("read-back abandonment", abandoned, len(captures), "captures that passed the quality gate"),
      ],
      "Weekly free-response attempts, and the share of captures whose read-back was never confirmed.",
      {"start": first_day.isoformat(), "end": today.isoformat()},
   )


def mock_trajectory(db, user_id):
   mocks = db.execute(
      select(models.Session.id)
      .where(models.Session.user_id == user_id)
      .where(models.Session.mode == REHEARSAL_MODE)
      .where(models.Session.ended_at.is_not(None))
   ).scalars().all()

   return metric(
      "mock_trajectory",
      "Mock-exam trajectory",
      [value("full mocks finished", len(mocks), len(mocks), "finished mocks", None)],
      "Free-response points out of 54 and multiple-choice correct on each full mock, against the published means. Mocks arrive with P5.",
   )


def internal_numbers(attempts, first_day, last_day):
   period = [record for record in practice(attempts) if record.correct is not None and in_window(record, first_day, last_day)]

   return value(
      "practice accuracy in the same period",
      sum(1 for record in period if record.correct),
      len(period),
      "graded practice attempts",
   )


def external_checkpoint(db, user_id, attempts):
   history = checkpoint_service.history(db, user_id)
   values = []

   for entry in history:
      finished_day = date.fromisoformat(entry["finished_at"][:10])
      period_start = finished_day - timedelta(days=checkpoint_service.CADENCE_DAYS - 1)
      earned = value(
         f"{entry['form_year']} released form, points earned",
         entry["total_earned"],
         entry["total_possible"],
         "points possible",
      )
      earned["published_total"] = entry["published_total"]
      earned["scored_by"] = entry["scored_by"]
      values.append(earned)
      values.append(internal_numbers(attempts, period_start, finished_day))

   if not values:
      values.append(value("released-form points earned", 0, 0, "points possible"))

   return metric(
      "external_checkpoint",
      "External checkpoint",
      values,
      "Released AP free-response forms every 6 weeks, beside the internal numbers for the same period. The expectation recorded against it is d = 0.4 to 0.7 against a standardized criterion, not two sigma.",
   )


def concept_probe(db, user_id):
   history = probe_service.history(db, user_id)
   values = [
      value(f"probe of {entry['finished_at'][:10]}, correct", entry["correct"], entry["graded"], "graded probe items")
      for entry in history
   ]

   if not values:
      values.append(value("probe items correct", 0, 0, "graded probe items"))

   return metric(
      "concept_probe",
      "Stable concept probe",
      values,
      "A fixed item set never used for practice, every 8 weeks, reported apart from practice accuracy.",
   )


def learning_metrics(db, user_id, archetypes, today):
   attempts = load_attempts(db, user_id, archetypes)

   return [
      mastery_growth(db, user_id, attempts, today),
      retention(attempts),
      mock_trajectory(db, user_id),
      calibration(attempts, today),
      method_and_execution(db, attempts),
      error_recurrence(db, attempts),
      adherence_and_effort(db, user_id, attempts, today),
      free_response_participation(attempts, today),
      external_checkpoint(db, user_id, attempts),
      concept_probe(db, user_id),
   ]
