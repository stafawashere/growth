"""The tutor writes the sentence that carries the deterministically selected feedback (R35).

docs/plan/03-diagnosis-and-feedback.md, "Who composes the string in P1": the application picks
the violated step, the observed behavior and scoring consequence of the option's BC-ERR record,
and the item's stored worked solution, and passes exactly those four fields into
prompts/feedback/elaborated_v2.md. Nothing else about the item reaches the model, and no call is
made before the student has submitted.
"""
import dataclasses
from pathlib import Path

from sqlalchemy import func, select

from app.auth.service import utc_now
from app.db import models
from app.feedback.render import FeedbackKind
from app.providers.base import (
   CacheSettings,
   Message,
   ProviderRequest,
   RefusedBeforeWire,
   render_template,
   split_template,
)
from app.providers.call_queue import queue_call
from app.providers.guard import BudgetStopped, ProviderCallFailed
from app.providers.model_routing import model_for
from app.providers.subscription import SubscriptionAuthFailed, SubscriptionLimitReached

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"
TEMPLATE_PATH = PROMPTS_DIR / "feedback" / "elaborated_v2.md"
ELABORATED = "elaborated"
FRQ_POINTS = "frq_points"
CORRECT_REINFORCEMENT = "correct_reinforcement"
TEMPLATES = {
   ELABORATED: TEMPLATE_PATH,
   FRQ_POINTS: PROMPTS_DIR / "tutor" / "frq_points_v1.md",
   CORRECT_REINFORCEMENT: PROMPTS_DIR / "tutor" / "correct_reinforcement_v1.md",
}
LOW_CONFIDENCE_RATINGS = ("guess", "unsure")
TUTOR_MODEL = model_for("tutor")
MAX_OUTPUT_TOKENS = 600
PREFIX_CACHE_TTL = "1h"
TUTOR_PROVIDER_OPTIONS = {
   "thinking": {"type": "disabled"},
   "output_config": {"effort": "low"},
}
TUTOR_CALLS_PER_SESSION = 20
TUTOR_CALLS_PER_ITEM = 3
LIMIT_QUEUE_REASON = "subscription_limit_reached"


def template_text(template=ELABORATED):
   is_elaborated = template == ELABORATED
   path = TEMPLATE_PATH if is_elaborated else TEMPLATES[template]

   return path.read_text()


def request_for(fields, template=ELABORATED):
   text = template_text(template)
   rendered = render_template(text, fields)

   return request_from_messages([Message(role="user", content=rendered)], template=template)


def request_from_messages(messages, model=None, template=ELABORATED):
   """A queued call stores only its rendered messages and the name of its template, so a later
   drain rebuilds the rest of the request from the same template and options the live call used.
   TUTOR_MODEL is read at call time, never bound as a default."""
   system, _variable_section = split_template(template_text(template))
   request = ProviderRequest(
      role="tutor",
      model=TUTOR_MODEL,
      system=system,
      messages=list(messages),
      max_output_tokens=MAX_OUTPUT_TOKENS,
      cache=CacheSettings(prefix_breakpoints=1, ttl=PREFIX_CACHE_TTL),
      provider_options={key: dict(value) for key, value in TUTOR_PROVIDER_OPTIONS.items()},
   )
   has_model = model is not None and model != ""

   if has_model:
      return dataclasses.replace(request, model=model)

   return request


def session_tutor_calls(db, session_id):
   spent = db.scalar(
      select(func.sum(models.Attempt.tutor_calls)).where(models.Attempt.session_id == session_id)
   )

   return spent or 0


def ceiling_reached(db, attempt):
   """13's "A per-session ceiling" gives 09's two inferred tunables their numbers, 20 per session
   and 3 per item. Both are counted from the attempts table and the constants are read at call
   time, so neither a new process nor a changed number lets a call through that the table refuses.
   """
   item_calls = attempt.tutor_calls or 0
   item_is_full = item_calls >= TUTOR_CALLS_PER_ITEM
   session_is_full = session_tutor_calls(db, attempt.session_id) >= TUTOR_CALLS_PER_SESSION

   return item_is_full or session_is_full


def added(total, amount):
   has_amount = amount is not None

   if not has_amount:
      return total

   has_total = total is not None

   if not has_total:
      return amount

   return total + amount


def record_call(db, attempt, accounting):
   attempt.tutor_calls = (attempt.tutor_calls or 0) + 1
   has_accounting = accounting is not None

   if has_accounting:
      attempt.tutor_tokens_in = added(attempt.tutor_tokens_in, accounting.tokens_in)
      attempt.tutor_tokens_cached_read = added(
         attempt.tutor_tokens_cached_read, accounting.tokens_cached_read
      )
      attempt.tutor_cost_usd = added(attempt.tutor_cost_usd, accounting.cost_usd)
      reported_a_cached_read = accounting.tokens_cached_read is not None

      if reported_a_cached_read:
         attempt.tutor_cached_read_reported_calls = (attempt.tutor_cached_read_reported_calls or 0) + 1

   db.add(attempt)
   db.flush()


def compose_sentence(provider, feedback, db=None, attempt=None, user_id=None):
   payload = feedback.elaborated
   fields = payload.as_prompt_fields() if payload is not None else None

   return compose(provider, fields, ELABORATED, db=db, attempt=attempt, user_id=user_id)


def reinforcement_fields(feedback, archetype, worked_solution):
   """A correct answer rated a guess or unsure gets two sentences naming the rule that made it
   right, since that is the answer most likely to be forgotten or reversed. A confident correct
   answer gets none, which keeps the tutor's calls on the answers that gain from one."""
   is_correct = feedback.kind == FeedbackKind.CORRECT
   rating = feedback.confidence.value if feedback.confidence is not None else None
   is_low_confidence = rating in LOW_CONFIDENCE_RATINGS
   has_solution = worked_solution is not None and str(worked_solution).strip() != ""
   reinforces = is_correct and is_low_confidence and has_solution

   if not reinforces:
      return None

   path = archetype.get("expected_solution_path") or []

   return {
      "solution_path": "; ".join(str(step) for step in path),
      "worked_solution": worked_solution,
   }


def compose_reinforcement(provider, feedback, archetype, worked_solution, db=None, attempt=None, user_id=None):
   fields = reinforcement_fields(feedback, archetype, worked_solution)

   return compose(provider, fields, CORRECT_REINFORCEMENT, db=db, attempt=attempt, user_id=user_id)


def point_line(part_id, criterion, row):
   quote = (row.evidence_quote or "").strip()
   rubric_field = (row.rule_field or "").strip()

   return (
      f"Part ({part_id}). The point needed: {criterion}. Rubric field applied: {rubric_field}. "
      f"Rule the grader cited: {row.rationale}. Quote from the work: {quote}."
   )


def frq_points_fields(record, rows, observed_errors, errors):
   """The points a graded question did not earn, each with its criterion, the rubric field and
   rule the grader cited and the quote the grader took from the work, plus, for each error the
   diagnostician observed, its recorded behavior and the evidence it quoted. The criterion and the
   grader's words are already on the result screen. No worked solution and no other rubric text
   is passed. A question with a point still provisional, or with no point lost, gets no call."""
   criteria = {point["point_id"]: point["criterion"] for part in record["parts"] for point in part["points"]}
   has_provisional = any(row.provisional for row in rows)
   lost_rows = [row for row in rows if row.earned == 0]
   has_lost = len(lost_rows) > 0
   explains = has_lost and not has_provisional

   if not explains:
      return None

   lines = [point_line(row.part_id, criteria.get(row.point_id, ""), row) for row in lost_rows]
   behaviors = []

   for observed in observed_errors:
      error_id = observed.get("error_id")
      behavior = (errors.get(error_id) or {}).get("observed_behavior") or ""
      evidence = (observed.get("evidence") or "").strip()
      has_evidence = evidence != ""

      if has_evidence:
         behaviors.append(f"{behavior} Seen in the work: {evidence}.")
      elif behavior:
         behaviors.append(behavior)

   return {
      "points_not_earned": " ".join(lines),
      "observed_errors": " ".join(behaviors),
   }


def compose_frq_explanation(provider, record, rows, observed_errors, errors, db=None, attempt=None, user_id=None):
   fields = frq_points_fields(record, rows, observed_errors, errors)

   return compose(provider, fields, FRQ_POINTS, db=db, attempt=attempt, user_id=user_id)


def compose(provider, fields, template, db=None, attempt=None, user_id=None):
   """The selected payload becomes one paragraph. No provider means no sentence, not an error.

   With a session and an attempt row the sentence is cached on the attempt, so re-reading the
   feedback screen returns the wording the student already saw and spends no second tutor call
   against the role's daily cap. The write is flushed and not committed: the caller owns the
   transaction. An empty or blank sentence is a provider that said nothing, so it is not stored
   and the next read composes again.

   Every call that reaches the provider is counted on the attempt, with that call's accounting,
   whether it returns a sentence, an empty one or an error. A provider that reports its charges,
   which the guard does through last_accounting, is believed: a call it neither returned from nor
   charged never reached the adapter, whether it was a budget stop, a RefusedBeforeWire the guard
   refunded, or an unpriced model or a failed audit write raised while reserving. The request is
   built before the provider is asked, so a missing template is no call at all. None of these is
   counted, so a misconfiguration cannot use up an item's ceiling. A provider without
   last_accounting cannot say, so everything it raised except a refusal is counted. tutor_cached_read_reported_calls counts the
   calls whose accounting reported a cached read, zero included, so a served item where only some
   calls reported can be told apart from one where all did (06, attempts). A call past either ceiling is refused before the provider and returns no
   sentence: 07's hard-stop line says the tutor is unavailable for the rest of today, which is
   the daily cap's meaning and would be false for a ceiling that lifts on the next item or session.

   A budget stop is not a provider failure and is not swallowed. 07's hard-stop table says the
   student is told the tutor is unavailable for the rest of today, so the caller has to be able
   to tell a cap from a model that merely returned nothing.

   A subscription usage limit (app/providers/subscription.py SubscriptionLimitReached) degrades
   the same way. The guard reports it as a ProviderCallFailed naming that exception type, so it is
   recognised by name. With a session and an attempt the call is queued in the jobs table
   (app/providers/call_queue.py), and SubscriptionLimitReached is raised for the caller to show
   the static feedback with the tutor marked unavailable. Nothing retries on the paid API.
   """
   caches = db is not None and attempt is not None

   if caches:
      stored = attempt.tutor_sentence
      has_stored_sentence = stored is not None and stored.strip() != ""

      if has_stored_sentence:
         return stored

   has_provider = provider is not None
   has_payload = fields is not None
   composes = has_provider and has_payload

   if not composes:
      return None

   is_refused_by_a_ceiling = caches and ceiling_reached(db, attempt)

   if is_refused_by_a_ceiling:
      return None

   try:
      request = request_for(fields, template=template)
   except (OSError, ValueError):
      return None

   reports_charges = hasattr(provider, "last_accounting")
   accounting_before = getattr(provider, "last_accounting", None)
   returned = False
   refused_before_the_wire = False
   limit_reached = False
   sign_in_failed = False
   result = None

   try:
      result = provider.generate(request)
      returned = True
   except BudgetStopped:
      refused_before_the_wire = True
      raise
   except RefusedBeforeWire:
      refused_before_the_wire = True
      return None
   except SubscriptionLimitReached:
      limit_reached = True
   except SubscriptionAuthFailed:
      sign_in_failed = True
   except ProviderCallFailed as failed:
      limit_reached = failed.exception_type == SubscriptionLimitReached.__name__
      sign_in_failed = failed.exception_type == SubscriptionAuthFailed.__name__
      is_other_failure = not limit_reached and not sign_in_failed

      if is_other_failure:
         return None
   except Exception:
      return None
   finally:
      accounting_after = getattr(provider, "last_accounting", None)
      has_this_calls_accounting = accounting_after is not None and accounting_after is not accounting_before

      if reports_charges:
         reached_provider = returned or has_this_calls_accounting
      else:
         reached_provider = not refused_before_the_wire

      records_the_call = caches and reached_provider

      if records_the_call:
         record_call(db, attempt, accounting_after if has_this_calls_accounting else None)

   if sign_in_failed:
      raise SubscriptionAuthFailed(f"the Claude sign-in expired, so the {request.role} is unavailable")

   if limit_reached:
      if caches:
         queued_template = None if template == ELABORATED else template
         queue_call(db, user_id, attempt.id, request, reason=LIMIT_QUEUE_REASON, now=utc_now(), template=queued_template)

      raise SubscriptionLimitReached(f"the {request.role} call was queued behind a subscription limit")

   sentence = result.text
   has_sentence = sentence is not None and sentence.strip() != ""

   if not has_sentence:
      return None

   if caches:
      attempt.tutor_sentence = sentence
      db.add(attempt)
      db.flush()

   return sentence
