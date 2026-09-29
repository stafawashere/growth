"""The pace verdict at the top of the progress screen: is the student mastering the exam's skills
fast enough to have all of them held before the exam, with a review reserve left over.

It reads the same records the rest of progress reads, the skills_state rows, the retrievability
app/engine/retention.py derives and the practice attempts of app/progress/attempt_log.py, and it
answers in one sentence with the numbers under it. It is a pace on skill mastery and never a
predicted AP score: 05 and 08 rule the score out because the composite weights and the cut points
are unpublished, and nothing here needs either.

Readings this module fixes, every one [inferred]:

- A skill counts as held when it is mastered, not due under today's retention target, and was
  earned with at least the mastery rule's 3 unaided successes. Rows seeded mastered at account
  creation demonstrated nothing, so they count as remaining work, and a fading skill counts as
  remaining because it needs review before it holds again.
- Each skill is weighted by its unit's share of the multiple-choice section (the BC band midpoints
  app/engine/exam_weights.py reads) spread over that unit's skills, scaled so the weights sum to the
  skill count. A weighted skill is therefore one skill's worth of an average unit.
- The mastery rate is the weighted skills newly earned over the last 28 days, or since the first
  practice day when that is more recent, per week.
- New mastery should finish 28 days before the exam, leaving that reserve for mocks and review.
- No verdict is given before 7 days of practice and 40 graded practice attempts exist.
- The pace ratio is the weekly rate over the weekly rate still required. At 1.25 or more the
  student is ahead, at 1.0 on pace, at 0.6 behind and below that well behind. A measured 30-day
  retention under 0.75 on at least 10 attempts caps the verdict at behind, because skills that do
  not hold will have to be mastered twice.
"""
from dataclasses import dataclass
from datetime import date, timedelta

from app.engine import constants
from app.engine.exam_weights import band_midpoints
from app.engine.fringe import is_due
from app.engine.retention import current_retrievability

RATE_WINDOW_DAYS = 28
REVIEW_RESERVE_DAYS = 28
MIN_PRACTICE_DAYS = 7
MIN_GRADED_ATTEMPTS = 40
AHEAD_RATIO = 1.25
ON_PACE_RATIO = 1.0
BEHIND_RATIO = 0.6
RETENTION_FLOOR = 0.75
MIN_RETENTION_ATTEMPTS = 10
RETENTION_LOW_DAYS = 25
RETENTION_HIGH_DAYS = 35
RECENT_ACCURACY_DAYS = 14
MS_PER_MINUTE = 60_000
DAYS_PER_WEEK = 7

COMPLETE = "complete"
AHEAD = "ahead"
ON_PACE = "on_pace"
BEHIND = "behind"
WELL_BEHIND = "well_behind"
TOO_EARLY = "too_early"
EXAM_PASSED = "exam_passed"

VERDICT_ORDER = (WELL_BEHIND, BEHIND, ON_PACE, AHEAD)


@dataclass(frozen=True)
class SkillStanding:
   skill_id: str
   unit_id: str
   held: bool
   fading: bool
   assumed: bool
   earned_on: date | None


@dataclass(frozen=True)
class Practice:
   day: date
   correct: bool | None
   elapsed_ms: int | None
   primary_skill: str | None


def skill_weights(unit_by_skill, midpoints):
   """Unit share spread over the unit's skills, scaled so the weights sum to the skill count. A unit
   the blueprint does not weight takes the mean midpoint, so it is neither free nor dominant."""
   skills_per_unit = {}

   for unit_id in unit_by_skill.values():
      skills_per_unit[unit_id] = skills_per_unit.get(unit_id, 0) + 1

   mean_midpoint = sum(midpoints.values()) / len(midpoints) if midpoints else 1
   unit_midpoint = {unit_id: midpoints.get(unit_id, mean_midpoint) for unit_id in skills_per_unit}
   midpoint_total = sum(unit_midpoint.values())
   skill_count = len(unit_by_skill)
   weights = {}

   for skill_id, unit_id in unit_by_skill.items():
      unit_share = unit_midpoint[unit_id] / midpoint_total
      weights[skill_id] = float(unit_share * skill_count / skills_per_unit[unit_id])

   return weights


def standings(graph, states, today):
   retrievability = current_retrievability(states, today)
   target = constants.desired_retention(today)
   rows = []

   for skill_id, record in graph.skills.items():
      state = states.get(skill_id)
      is_mastered = state is not None and state.mastered
      was_earned = is_mastered and state.unaided_success_count >= constants.MASTERY_MIN_UNAIDED_SUCCESSES
      is_fading = is_mastered and is_due(skill_id, states, retrievability, target)
      is_assumed = is_mastered and state.observation_count == 0
      has_earned_day = was_earned and state.mastered_at is not None

      rows.append(
         SkillStanding(
            skill_id=skill_id,
            unit_id=record.get("unit") or "BC-UNIT-00",
            held=was_earned and not is_fading,
            fading=is_fading,
            assumed=is_assumed,
            earned_on=state.mastered_at.date() if has_earned_day else None,
         )
      )

   return rows


def practice_records(attempts):
   return [
      Practice(record.day, record.correct, record.elapsed_ms, record.primary_skill)
      for record in attempts
      if record.updates_mastery
   ]


def thirty_day_retention(practice):
   """First-attempt accuracy on a skill 25 to 35 days after a success on it, the 30-day bucket of
   the retention metric in app/progress/learning_metrics.py."""
   last_by_skill = {}
   outcomes = []

   for record in practice:
      is_counted = record.correct is not None and record.primary_skill is not None

      if not is_counted:
         continue

      previous = last_by_skill.get(record.primary_skill)
      last_by_skill[record.primary_skill] = record
      follows_a_success = previous is not None and previous.correct is True

      if not follows_a_success:
         continue

      gap = (record.day - previous.day).days
      is_in_bucket = RETENTION_LOW_DAYS <= gap <= RETENTION_HIGH_DAYS

      if is_in_bucket:
         outcomes.append(1 if record.correct else 0)

   return sum(outcomes), len(outcomes)


def study_time(practice, first_day, today):
   """Minutes are None, not 0, when no attempt in the window carries a logged time. A window shorter
   than a week is read as a week, so two days of practice are not stretched into a weekly habit."""
   in_window = [record for record in practice if first_day <= record.day <= today]
   active_days = {record.day for record in in_window}
   timed = [record.elapsed_ms for record in in_window if record.elapsed_ms]
   window_days = (today - first_day).days + 1
   weeks = max(window_days, MIN_PRACTICE_DAYS) / DAYS_PER_WEEK
   minutes = sum(timed) / MS_PER_MINUTE if timed else None
   has_minutes = minutes is not None and len(active_days) > 0

   return {
      "window_start": first_day.isoformat(),
      "window_days": window_days,
      "active_days": len(active_days),
      "timed_attempts": len(timed),
      "attempts": len(in_window),
      "minutes": round(minutes, 1) if minutes is not None else None,
      "minutes_per_active_day": round(minutes / len(active_days), 1) if has_minutes else None,
      "active_days_per_week": round(len(active_days) / weeks, 1),
      "minutes_per_week": round(minutes / weeks, 1) if minutes is not None else None,
   }


def recent_accuracy(practice, today):
   first_day = today - timedelta(days=RECENT_ACCURACY_DAYS - 1)
   graded = [record for record in practice if record.correct is not None and first_day <= record.day <= today]
   correct = sum(1 for record in graded if record.correct)

   return correct, len(graded)


def rate_window_start(practice, today):
   window_start = today - timedelta(days=RATE_WINDOW_DAYS - 1)
   first_practice_day = min((record.day for record in practice), default=today)

   return max(window_start, first_practice_day)


def classify(pace_ratio, retention_failing):
   if pace_ratio >= AHEAD_RATIO:
      verdict = AHEAD
   elif pace_ratio >= ON_PACE_RATIO:
      verdict = ON_PACE
   elif pace_ratio >= BEHIND_RATIO:
      verdict = BEHIND
   else:
      verdict = WELL_BEHIND

   is_above_behind = VERDICT_ORDER.index(verdict) > VERDICT_ORDER.index(BEHIND)
   should_cap = retention_failing and is_above_behind

   return BEHIND if should_cap else verdict


def long_date(day):
   return f"{day:%B} {day.day}, {day.year}"


def weeks_text(weeks):
   rounded = round(weeks)

   return "1 week" if rounded == 1 else f"{rounded} weeks"


def statement_for(verdict, numbers):
   exam = long_date(numbers["exam_date"])
   deadline = long_date(numbers["deadline"])
   remaining = numbers["remaining_skills"]
   total = numbers["total_skills"]
   rate = numbers["weekly_rate"]
   required = numbers["required_weekly_rate"]
   finish = numbers["projected_finish"]

   if verdict == EXAM_PASSED:
      return f"The exam date, {exam}, has passed. Change it in settings if the exam is still ahead."

   if verdict == COMPLETE:
      return f"Every one of the {total} exam skills is mastered and holding. What is left before {exam} is keeping them from fading."

   if verdict == TOO_EARLY:
      return (
         f"Too early to call. A verdict needs {MIN_PRACTICE_DAYS} days of practice and {MIN_GRADED_ATTEMPTS} graded "
         f"attempts; you have {numbers['practice_days']} and {numbers['graded_attempts']}. To finish by {deadline} "
         f"you will need about {required:.1f} weighted skills a week."
      )

   if rate == 0:
      return (
         f"Not on pace. No skill reached mastery in the last {numbers['rate_window_days']} days, and {remaining} of "
         f"{total} skills remain with {weeks_text(numbers['weeks_to_deadline'])} left before {deadline}."
      )

   finish_text = long_date(finish)
   margin_weeks = (numbers["deadline"] - finish).days / DAYS_PER_WEEK

   if verdict == AHEAD:
      return (
         f"Ahead of pace. At your rate over the last {numbers['rate_window_days']} days every exam skill is mastered "
         f"by {finish_text}, {weeks_text(margin_weeks)} before the {deadline} target and {weeks_text((numbers['exam_date'] - finish).days / DAYS_PER_WEEK)} before the exam."
      )

   if verdict == ON_PACE:
      return (
         f"On pace. At your rate over the last {numbers['rate_window_days']} days every exam skill is mastered by "
         f"{finish_text}, in time for the {deadline} target that leaves {REVIEW_RESERVE_DAYS} days for review before {exam}."
      )

   is_capped_by_retention = numbers["retention_failing"] and rate >= required

   if is_capped_by_retention:
      return (
         f"Behind pace. New skills arrive fast enough to finish by {finish_text}, but only "
         f"{numbers['retention_value']:.0%} of skills held a month after a success, so many will need mastering twice."
      )

   if verdict == BEHIND:
      return (
         f"Behind pace. At your current rate the last skill is mastered on {finish_text}, after the {deadline} target. "
         f"You are mastering {rate:.1f} weighted skills a week and need {required:.1f}."
      )

   return (
      f"Well behind pace. You are mastering {rate:.1f} weighted skills a week and need {required:.1f}; at this rate "
      f"the last skill is mastered on {finish_text}, and the exam is {exam}."
   )


def pace_verdict(graph, states, attempts, exam_date, today, midpoints=None):
   rows = standings(graph, states, today)
   weights = skill_weights({row.skill_id: row.unit_id for row in rows}, band_midpoints() if midpoints is None else midpoints)
   practice = practice_records(attempts)

   total_weight = sum(weights.values())
   held_weight = sum(weights[row.skill_id] for row in rows if row.held)
   remaining_weight = total_weight - held_weight

   window_start = rate_window_start(practice, today)
   window_days = (today - window_start).days + 1
   earned_weight = sum(
      weights[row.skill_id]
      for row in rows
      if row.earned_on is not None and window_start <= row.earned_on <= today
   )
   weekly_rate = earned_weight / (max(window_days, MIN_PRACTICE_DAYS) / DAYS_PER_WEEK)

   deadline = exam_date - timedelta(days=REVIEW_RESERVE_DAYS)
   is_past_deadline = deadline <= today
   target_day = exam_date if is_past_deadline else deadline
   weeks_to_deadline = max((target_day - today).days, 1) / DAYS_PER_WEEK
   required_weekly_rate = remaining_weight / weeks_to_deadline

   has_rate = weekly_rate > 0
   projected_finish = today + timedelta(days=round(remaining_weight / weekly_rate * DAYS_PER_WEEK)) if has_rate else None

   retention_correct, retention_count = thirty_day_retention(practice)
   retention_value = retention_correct / retention_count if retention_count else None
   has_retention_evidence = retention_count >= MIN_RETENTION_ATTEMPTS
   retention_failing = has_retention_evidence and retention_value < RETENTION_FLOOR

   graded_attempts = sum(1 for record in practice if record.correct is not None)
   practice_days = len({record.day for record in practice})
   first_practice_day = min((record.day for record in practice), default=None)
   days_practising = (today - first_practice_day).days + 1 if first_practice_day else 0
   has_enough_data = days_practising >= MIN_PRACTICE_DAYS and graded_attempts >= MIN_GRADED_ATTEMPTS

   is_exam_passed = exam_date < today
   is_complete = remaining_weight <= 0
   pace_ratio = weekly_rate / required_weekly_rate if required_weekly_rate > 0 else None

   if is_exam_passed:
      verdict = EXAM_PASSED
   elif is_complete:
      verdict = COMPLETE
   elif not has_enough_data:
      verdict = TOO_EARLY
   else:
      verdict = classify(pace_ratio, retention_failing)

   accuracy_correct, accuracy_count = recent_accuracy(practice, today)
   numbers = {
      "exam_date": exam_date,
      "deadline": target_day,
      "total_skills": len(rows),
      "remaining_skills": sum(1 for row in rows if not row.held),
      "weekly_rate": weekly_rate,
      "required_weekly_rate": required_weekly_rate,
      "projected_finish": projected_finish,
      "rate_window_days": window_days,
      "weeks_to_deadline": weeks_to_deadline,
      "practice_days": practice_days,
      "graded_attempts": graded_attempts,
      "retention_failing": retention_failing,
      "retention_value": retention_value,
   }

   return {
      "as_of": today.isoformat(),
      "verdict": verdict,
      "statement": statement_for(verdict, numbers),
      "exam_date": exam_date.isoformat(),
      "days_to_exam": (exam_date - today).days,
      "review_reserve_days": REVIEW_RESERVE_DAYS,
      "new_mastery_deadline": target_day.isoformat(),
      "skills": {
         "total": len(rows),
         "held": sum(1 for row in rows if row.held),
         "fading": sum(1 for row in rows if row.fading),
         "assumed": sum(1 for row in rows if row.assumed),
         "remaining": numbers["remaining_skills"],
         "remaining_weighted": round(remaining_weight, 2),
      },
      "rate": {
         "window_start": window_start.isoformat(),
         "window_days": window_days,
         "earned_weighted": round(earned_weight, 2),
         "weekly": round(weekly_rate, 2),
         "required_weekly": round(required_weekly_rate, 2),
         "pace_ratio": round(pace_ratio, 2) if pace_ratio is not None else None,
         "projected_finish": projected_finish.isoformat() if projected_finish else None,
      },
      "study_time": study_time(practice, window_start, today),
      "evidence": {
         "graded_attempts": graded_attempts,
         "practice_days": practice_days,
         "recent_accuracy": {
            "correct": accuracy_correct,
            "graded": accuracy_count,
            "days": RECENT_ACCURACY_DAYS,
            "value": round(accuracy_correct / accuracy_count, 3) if accuracy_count else None,
         },
         "retention_30_day": {
            "correct": retention_correct,
            "attempts": retention_count,
            "value": round(retention_value, 3) if retention_value is not None else None,
            "floor": RETENTION_FLOOR,
         },
      },
      "caveat": "A pace on mastering the exam's skills, not a predicted AP score: the score weights and cut points are unpublished.",
   }
