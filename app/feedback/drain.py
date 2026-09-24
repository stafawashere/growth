"""Retries the tutor calls a subscription usage limit queued (app/providers/call_queue.py) and
stores each sentence on its attempt, where app/feedback/tutor.py compose_sentence already looks
first, so the student sees the elaborated feedback the next time the feedback screen is opened.

Every retry goes through GuardedProvider with the same caps the feedback route would apply: the
subscription pacing guard on the subscription backend, the per-role caps and the persistent
developer spend cap on the api backend. Which backend is the caller's choice
(tools/drain_subscription_queue.py builds it with app/main.py build_tutor), so nothing here can
reach the paid API unless GROWTH_AI_BACKEND=api chose it.

A limit that still holds re-queues the job with a later not_before and stops the drain, because
every later job would meet the same closed window; waiting behind a limit is not a failure, so it
leaves attempts_made alone. A pacing, budget or developer spend cap stop leaves the job as it was
and stops the drain. Any other failure counts one attempt and re-queues the job until
MAX_DRAIN_ATTEMPTS, then marks it failed. Each job is committed on its own, so a drain cut short keeps what it finished.

A retry is held to the same per-item and per-session tutor ceilings compose_sentence enforces
(tutor.ceiling_reached): a job whose attempt or session is already full is marked failed without a
call, because neither ceiling lifts for that attempt. The call that met the limit was counted when
compose_sentence queued the job, and a drain retry that meets the limit again is the same call
still waiting for the window, so it is not counted a second time. Counting it would let waiting fill
the item's ceiling and fail a job no model ever answered.
"""
import json
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import select

from app.auth.service import as_iso
from app.db import models
from app.feedback import tutor
from app.providers.anthropic import AnthropicProvider
from app.providers.base import Message, RefusedBeforeWire
from app.providers.call_queue import QUEUED_CALL_JOB_TYPE, QUEUED_CALL_STATE
from app.providers.guard import BudgetStopped, DevSpendCapExceeded, GuardedProvider, ProviderCallFailed
from app.providers.subscription import SubscriptionLimitReached

DONE_STATE = "done"
FAILED_STATE = "failed"
DEV_SPEND_STOP = "dev_spend_cap"
CEILING_REACHED_ERROR = "tutor_ceiling_reached"
LIMIT_RETRY_AFTER = timedelta(minutes=30)
FAILURE_RETRY_AFTER = timedelta(minutes=5)
MAX_DRAIN_ATTEMPTS = 3
DRAINABLE_ROLES = ("tutor",)


@dataclass
class DrainReport:
   done: int = 0
   requeued: int = 0
   failed: int = 0
   skipped: int = 0
   stopped_by: str | None = None


def due_jobs(db, now):
   statement = (
      select(models.Job)
      .where(models.Job.type == QUEUED_CALL_JOB_TYPE)
      .where(models.Job.state == QUEUED_CALL_STATE)
      .where(models.Job.not_before <= as_iso(now))
      .order_by(models.Job.created_at, models.Job.id)
   )

   return db.scalars(statement).all()


def is_limit_failure(raised):
   is_bare_limit = isinstance(raised, SubscriptionLimitReached)
   is_guarded_limit = isinstance(raised, ProviderCallFailed) and raised.exception_type == SubscriptionLimitReached.__name__

   return is_bare_limit or is_guarded_limit


def guarded_for(provider, db, user_id, tutor_caps, pacing, clock):
   is_live_api = isinstance(provider, AnthropicProvider)

   return GuardedProvider(
      provider,
      db,
      user_id,
      clock=clock,
      caps=tutor_caps,
      dev_spend_track=is_live_api,
      subscription_pacing=pacing,
   )


def settle_job(job, state, now, error=None):
   job.state = state
   job.last_error = error
   job.updated_at = as_iso(now)


def defer_job(job, now, retry_after, error):
   job.not_before = as_iso(now + retry_after)
   settle_job(job, QUEUED_CALL_STATE, now, error)


def requeue_job(job, now, retry_after, error):
   job.attempts_made = (job.attempts_made or 0) + 1
   defer_job(job, now, retry_after, error)


def fail_or_requeue(job, now, error, report):
   attempts_after_this = (job.attempts_made or 0) + 1
   is_out_of_attempts = attempts_after_this >= MAX_DRAIN_ATTEMPTS

   if is_out_of_attempts:
      job.attempts_made = attempts_after_this
      settle_job(job, FAILED_STATE, now, error)
      report.failed = report.failed + 1

      return

   requeue_job(job, now, FAILURE_RETRY_AFTER, error)
   report.requeued = report.requeued + 1


def drain_queued_calls(db, provider, clock, tutor_caps=None, pacing=None, limit=None):
   """Drains the due jobs in the order they were queued, at most limit of them. Returns a
   DrainReport; stopped_by names why the drain ended early, if it did."""
   report = DrainReport()
   now = clock()
   jobs = due_jobs(db, now)
   has_limit = limit is not None

   if has_limit:
      jobs = jobs[:limit]

   for job in jobs:
      now = clock()
      stop = drain_one(db, job, provider, clock, now, tutor_caps or {}, pacing, report)
      db.commit()

      if stop is not None:
         report.stopped_by = stop
         break

   return report


def drain_one(db, job, provider, clock, now, tutor_caps, pacing, report):
   payload = json.loads(job.payload)
   role = payload.get("role")
   is_drainable = role in DRAINABLE_ROLES

   if not is_drainable:
      report.skipped = report.skipped + 1

      return None

   attempt = db.get(models.Attempt, payload.get("attempt_id"))

   if attempt is None:
      settle_job(job, FAILED_STATE, now, "attempt_missing")
      report.failed = report.failed + 1

      return None

   stored = attempt.tutor_sentence
   already_answered = stored is not None and stored.strip() != ""

   if already_answered:
      settle_job(job, DONE_STATE, now)
      report.done = report.done + 1

      return None

   is_refused_by_a_ceiling = tutor.ceiling_reached(db, attempt)

   if is_refused_by_a_ceiling:
      settle_job(job, FAILED_STATE, now, CEILING_REACHED_ERROR)
      report.failed = report.failed + 1

      return None

   messages = [Message(role=message["role"], content=message["content"]) for message in payload["messages"]]
   request = tutor.request_from_messages(messages, model=payload.get("model"))
   guarded = guarded_for(provider, db, payload.get("user_id"), tutor_caps, pacing, clock)

   try:
      result = guarded.generate(request)
   except BudgetStopped as stopped:
      return f"budget:{stopped.cap}"
   except DevSpendCapExceeded:
      return DEV_SPEND_STOP
   except (ProviderCallFailed, SubscriptionLimitReached, RefusedBeforeWire) as raised:
      if is_limit_failure(raised):
         defer_job(job, now, LIMIT_RETRY_AFTER, tutor.LIMIT_QUEUE_REASON)
         report.requeued = report.requeued + 1

         return tutor.LIMIT_QUEUE_REASON

      record_reached_call(db, attempt, guarded)
      error = getattr(raised, "exception_type", type(raised).__name__)
      fail_or_requeue(job, now, error, report)

      return None

   record_reached_call(db, attempt, guarded)
   sentence = result.text
   has_sentence = sentence is not None and sentence.strip() != ""

   if not has_sentence:
      fail_or_requeue(job, now, "empty_sentence", report)

      return None

   attempt.tutor_sentence = sentence
   db.add(attempt)
   settle_job(job, DONE_STATE, now)
   report.done = report.done + 1

   return None


def record_reached_call(db, attempt, guarded):
   """The guard sets last_accounting only for a call that reached the provider, the rule
   compose_sentence counts calls by."""
   accounting = guarded.last_accounting
   reached_provider = accounting is not None

   if reached_provider:
      tutor.record_call(db, attempt, accounting)
