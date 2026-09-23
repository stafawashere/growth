"""The tutor writes the sentence that carries the deterministically selected feedback (R35).

docs/plan/03-diagnosis-and-feedback.md, "Who composes the string in P1": the application picks
the violated step, the observed behavior and scoring consequence of the option's BC-ERR record,
and the item's stored worked solution, and passes exactly those four fields into
prompts/feedback/elaborated_v2.md. Nothing else about the item reaches the model, and no call is
made before the student has submitted.
"""
from pathlib import Path

from sqlalchemy import func, select

from app.db import models
from app.providers.base import (
   CacheSettings,
   Message,
   ProviderRequest,
   RefusedBeforeWire,
   render_template,
   split_template,
)
from app.providers.guard import BudgetStopped
from app.providers.model_routing import model_for

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "prompts" / "feedback" / "elaborated_v2.md"
TUTOR_MODEL = model_for("tutor")
MAX_OUTPUT_TOKENS = 600
PREFIX_CACHE_TTL = "1h"
TUTOR_PROVIDER_OPTIONS = {
   "thinking": {"type": "disabled"},
   "output_config": {"effort": "low"},
}
TUTOR_CALLS_PER_SESSION = 20
TUTOR_CALLS_PER_ITEM = 3


def template_text():
   return TEMPLATE_PATH.read_text()


def request_for(fields):
   text = template_text()
   system, _variable_section = split_template(text)
   rendered = render_template(text, fields)

   return ProviderRequest(
      role="tutor",
      model=TUTOR_MODEL,
      system=system,
      messages=[Message(role="user", content=rendered)],
      max_output_tokens=MAX_OUTPUT_TOKENS,
      cache=CacheSettings(prefix_breakpoints=1, ttl=PREFIX_CACHE_TTL),
      provider_options={key: dict(value) for key, value in TUTOR_PROVIDER_OPTIONS.items()},
   )


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


def compose_sentence(provider, feedback, db=None, attempt=None):
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
   """
   caches = db is not None and attempt is not None

   if caches:
      stored = attempt.tutor_sentence
      has_stored_sentence = stored is not None and stored.strip() != ""

      if has_stored_sentence:
         return stored

   has_provider = provider is not None
   payload = feedback.elaborated
   has_payload = payload is not None
   composes = has_provider and has_payload

   if not composes:
      return None

   is_refused_by_a_ceiling = caches and ceiling_reached(db, attempt)

   if is_refused_by_a_ceiling:
      return None

   try:
      request = request_for(payload.as_prompt_fields())
   except (OSError, ValueError):
      return None

   reports_charges = hasattr(provider, "last_accounting")
   accounting_before = getattr(provider, "last_accounting", None)
   returned = False
   refused_before_the_wire = False
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

   sentence = result.text
   has_sentence = sentence is not None and sentence.strip() != ""

   if not has_sentence:
      return None

   if caches:
      attempt.tutor_sentence = sentence
      db.add(attempt)
      db.flush()

   return sentence
