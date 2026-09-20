"""The budget guard, the usage accounting and the audit write at the provider seam.

docs/plan/07-ai-provider-layer.md, "Budget caps": the guard runs before the call, inside the
provider layer, as middleware outside the fallback chain so that a fallback cannot spend past
a cap. It estimates the call from the prompt token count and the configured max_output_tokens,
using the worst case rather than the expected case, refuses if the estimate would cross the cap,
and after the call reconciles the estimate against the provider's own usage block.

Three decisions here are [inferred] rather than read from the plan.

The character divisor. Token counting has no provider call available in P1 and no key, so the
prompt token count is estimated from characters by CHARACTERS_PER_TOKEN. That is an estimate and
nothing here should be read as exact. 07 line 62 is explicit that token accounting computed by
the client is an estimate and that the provider's own raw_usage block is the record, which is why
the estimate is a reservation that the reconciliation replaces rather than a number kept.

The null usage rule. 07 states that a null usage field means the provider did not report and a
zero means a real zero, and that conflating them would make the cache hit rate metric silently
wrong. So a null input or output count is never read as zero: the guard keeps its own worst-case
estimate for that field, which leaves the budget row conservative rather than optimistic. A null
cached read or cached write adds nothing to those counters, and the uncached base price the
estimate already used stands, which errs in the same direction.

The audit row rule. 09's "Audit log" lists a controlled vocabulary of consequential actions and
an ordinary provider call is not in it; one row per tutor call would flood a record 09 describes
as durable and queryable. So the guard writes an audit row when the role hard-stops and when a
call is refused by the cap, and never on an ordinary call. Per-call usage accounting lives in
budgets, which is the table 07 names for it.

A role with no configured cap is refused at construction of its budget row, before any call.
The guard exists to stop spending past a cap, and a role whose caps are both None crosses no cap
at all, so an unconfigured caller would otherwise get an unlimited provider with nothing to show
that it had.

No key material, no raw provider response body and no student response text reaches an audit
detail field or an exception message (09 "Key handling" and "Audit log"). The detail names the
provider, the model, the role and the cap that bound, and nothing else.

The price table holds only claude-sonnet-5, at the $2 and $10 per MTok that 07 cites against
Anthropic's own pricing page, because that is the one model P1 routes. Every other model raises
rather than being priced from a number no plan document carries, so a fallback to an unpriced
model is a refusal and not a silent wrong charge.
"""
import json
import math
from dataclasses import dataclass

from sqlalchemy import select

from app.auth.service import as_iso, new_id, utc_now, write_audit
from app.db import models
from app.providers.base import Provider

CHARACTERS_PER_TOKEN = 4

CACHE_READ_MULTIPLIER = 0.1
CACHE_WRITE_5M_MULTIPLIER = 1.25
CACHE_WRITE_1H_MULTIPLIER = 2.0

HARD_STOP_ACTION = "budget_hard_stop"
CALL_REFUSED_ACTION = "budget_call_refused"


@dataclass(frozen=True)
class ModelPrice:
   input_usd_per_mtok: float
   output_usd_per_mtok: float


MODEL_PRICES = {
   "claude-sonnet-5": ModelPrice(input_usd_per_mtok=2.0, output_usd_per_mtok=10.0),
}


@dataclass(frozen=True)
class BudgetCaps:
   cap_tokens: float | None = None
   cap_usd: float | None = None


@dataclass(frozen=True)
class CallEstimate:
   prompt_tokens: int
   output_tokens: int
   cost_usd: float

   @property
   def total_tokens(self):
      return self.prompt_tokens + self.output_tokens


class BudgetStopped(Exception):
   """Raised instead of calling the provider. Carries the role and the cap that bound, nothing else."""

   def __init__(self, role, cap):
      super().__init__(f"budget cap reached for role {role}: {cap}")
      self.role = role
      self.cap = cap


def price_for(model):
   price = MODEL_PRICES.get(model)

   if price is None:
      raise ValueError(f"no price recorded for model {model!r}")

   return price


def estimate_prompt_tokens(request):
   """An estimate from characters, never exact. See the module docstring."""
   message_characters = sum(len(message.content) for message in request.messages)
   total_characters = len(request.system or "") + message_characters

   return math.ceil(total_characters / CHARACTERS_PER_TOKEN)


def estimate_call(request):
   price = price_for(request.model)
   prompt_tokens = estimate_prompt_tokens(request)
   output_tokens = request.max_output_tokens

   input_cost = (prompt_tokens / 1_000_000) * price.input_usd_per_mtok
   output_cost = (output_tokens / 1_000_000) * price.output_usd_per_mtok

   return CallEstimate(
      prompt_tokens=prompt_tokens,
      output_tokens=output_tokens,
      cost_usd=input_cost + output_cost,
   )


def cache_write_multiplier(cache):
   wants_one_hour = cache is not None and cache.ttl == "1h"

   if wants_one_hour:
      return CACHE_WRITE_1H_MULTIPLIER

   return CACHE_WRITE_5M_MULTIPLIER


def usage_cost(model, cache, tokens_in, tokens_out, tokens_cached_read, tokens_cached_write):
   price = price_for(model)
   write_multiplier = cache_write_multiplier(cache)

   base_input = (tokens_in / 1_000_000) * price.input_usd_per_mtok
   cached_read = (tokens_cached_read / 1_000_000) * price.input_usd_per_mtok * CACHE_READ_MULTIPLIER
   cached_write = (tokens_cached_write / 1_000_000) * price.input_usd_per_mtok * write_multiplier
   output = (tokens_out / 1_000_000) * price.output_usd_per_mtok

   return base_input + cached_read + cached_write + output


class GuardedProvider(Provider):
   """The only provider object a caller wires. A bypass would defeat the cap, the accounting and the audit."""

   def __init__(self, provider, db, user_id, clock=None, caps=None, provider_name=None):
      self._provider = provider
      self._db = db
      self._user_id = user_id
      self._clock = clock or utc_now
      self._caps = caps or {}
      self._provider_name = provider_name or getattr(provider, "name", type(provider).__name__)

   def generate(self, request):
      budget, estimate = self._reserve(request)
      settled = False

      try:
         result = self._provider.generate(request)
         self._settle(budget, estimate, request, result)
         settled = True
      finally:
         if not settled:
            self._release(budget, estimate)

      return result

   def stream(self, request):
      """A consumer that stops iterating raises GeneratorExit here, which is not an Exception, so
      the reservation is released in a finally rather than in an except clause."""
      budget, estimate = self._reserve(request)
      settled = False

      try:
         result = yield from self._provider.stream(request)
         self._settle(budget, estimate, request, result)
         settled = True
      finally:
         if not settled:
            self._release(budget, estimate)

      return result

   def session(self):
      is_factory = callable(self._db)

      if is_factory:
         return self._db()

      return self._db

   def _reserve(self, request):
      db = self.session()
      estimate = estimate_call(request)
      budget = self._budget_row(db, request.role)

      already_stopped = budget.hard_stopped == 1

      if already_stopped:
         self._refuse(db, budget, request, "hard_stopped")

      bound_cap = self._bound_cap(budget, estimate)

      if bound_cap is not None:
         budget.hard_stopped = 1
         self._stamp(budget)
         write_audit(
            db,
            self._user_id,
            HARD_STOP_ACTION,
            f"budgets:{budget.id}",
            self._detail(request, bound_cap),
            now=self._clock(),
         )
         self._refuse(db, budget, request, bound_cap)

      budget.tokens_in = budget.tokens_in + estimate.prompt_tokens
      budget.tokens_out = budget.tokens_out + estimate.output_tokens
      budget.cost_usd = budget.cost_usd + estimate.cost_usd
      self._stamp(budget)
      db.flush()

      return budget, estimate

   def _refuse(self, db, budget, request, cap):
      """One refusal row per user per role per day per reason, the way app/session/build.py's
      gap_already_recorded bounds the coverage gap row. A row per refused call would flood a
      record 09 calls durable and queryable, and the fortieth row says nothing the first did not."""
      already_recorded = self._refusal_already_recorded(db, budget, cap)

      if not already_recorded:
         write_audit(
            db,
            self._user_id,
            CALL_REFUSED_ACTION,
            f"budgets:{budget.id}",
            self._detail(request, cap),
            now=self._clock(),
         )
         db.flush()

      raise BudgetStopped(request.role, cap)

   def _refusal_already_recorded(self, db, budget, cap):
      statement = (
         select(models.AuditLog.detail)
         .where(models.AuditLog.action == CALL_REFUSED_ACTION)
         .where(models.AuditLog.actor == self._user_id)
         .where(models.AuditLog.subject == f"budgets:{budget.id}")
      )

      for detail in db.scalars(statement).all():
         recorded = json.loads(detail) if detail else {}
         same_reason = recorded.get("cap") == cap

         if same_reason:
            return True

      return False

   def _release(self, budget, estimate):
      budget.tokens_in = budget.tokens_in - estimate.prompt_tokens
      budget.tokens_out = budget.tokens_out - estimate.output_tokens
      budget.cost_usd = budget.cost_usd - estimate.cost_usd
      self._stamp(budget)
      self.session().flush()

   def _settle(self, budget, estimate, request, result):
      """The money is already spent by the time this runs, so an unreadable result must not leave
      the reservation dangling. An unpriced result model is charged at the requested model, which
      estimate_call already priced; anything else unreadable keeps the worst-case reservation,
      which leaves the row conservative rather than empty."""
      try:
         self._reconcile(budget, estimate, request, result)
      except (AttributeError, TypeError, ValueError):
         self._stamp(budget)
         self.session().flush()

   def _reconcile(self, budget, estimate, request, result):
      usage = result.usage

      reported_input = usage.input_tokens
      reported_output = usage.output_tokens

      tokens_in = estimate.prompt_tokens if reported_input is None else reported_input
      tokens_out = estimate.output_tokens if reported_output is None else reported_output
      tokens_cached_read = usage.cached_read_tokens or 0
      tokens_cached_write = usage.cached_write_tokens or 0

      cost = usage_cost(
         self._priced_model(result, request),
         request.cache,
         tokens_in,
         tokens_out,
         tokens_cached_read,
         tokens_cached_write,
      )

      budget.tokens_in = budget.tokens_in - estimate.prompt_tokens + tokens_in
      budget.tokens_out = budget.tokens_out - estimate.output_tokens + tokens_out
      budget.tokens_cached_read = budget.tokens_cached_read + tokens_cached_read
      budget.tokens_cached_write = budget.tokens_cached_write + tokens_cached_write
      budget.cost_usd = budget.cost_usd - estimate.cost_usd + cost

      self._stamp(budget)
      self.session().flush()

   def _priced_model(self, result, request):
      reported_model = result.model
      has_priced_report = reported_model is not None and reported_model in MODEL_PRICES

      if has_priced_report:
         return reported_model

      return request.model

   def _bound_cap(self, budget, estimate):
      spent_tokens = (
         budget.tokens_in
         + budget.tokens_out
         + budget.tokens_cached_read
         + budget.tokens_cached_write
      )
      projected_tokens = spent_tokens + estimate.total_tokens
      projected_usd = budget.cost_usd + estimate.cost_usd

      has_token_cap = budget.cap_tokens is not None
      crosses_token_cap = has_token_cap and projected_tokens > budget.cap_tokens

      has_usd_cap = budget.cap_usd is not None
      crosses_usd_cap = has_usd_cap and projected_usd > budget.cap_usd

      if crosses_token_cap:
         return "tokens"

      if crosses_usd_cap:
         return "usd"

      return None

   def _detail(self, request, cap):
      return {
         "provider": self._provider_name,
         "model": request.model,
         "role": request.role,
         "cap": cap,
      }

   def _budget_row(self, db, role):
      day = self._clock().date().isoformat()
      statement = select(models.Budget).where(
         models.Budget.user_id == self._user_id,
         models.Budget.role == role,
         models.Budget.day == day,
      )
      existing = db.execute(statement).scalars().first()
      caps = self._configured_caps(role)

      if existing is not None:
         self._apply_caps(existing, caps)

         return existing

      timestamp = as_iso(self._clock())
      row = models.Budget(
         id=new_id("BUD"),
         user_id=self._user_id,
         role=role,
         day=day,
         tokens_in=0,
         tokens_out=0,
         tokens_cached_read=0,
         tokens_cached_write=0,
         cost_usd=0.0,
         cap_tokens=caps.cap_tokens,
         cap_usd=caps.cap_usd,
         hard_stopped=0,
         created_at=timestamp,
         updated_at=timestamp,
      )
      db.add(row)
      db.flush()

      return row

   def _configured_caps(self, role):
      """A role with no cap is refused rather than run uncapped. 07 puts the guard before the
      call so that nothing spends past a cap, and a role whose cap is None crosses nothing, so
      an unconfigured caller would get an unlimited provider and no sign that it had."""
      caps = self._caps.get(role)
      has_caps = caps is not None
      names_a_cap = has_caps and (caps.cap_tokens is not None or caps.cap_usd is not None)

      if not names_a_cap:
         raise BudgetStopped(role, "unconfigured")

      return caps

   def _apply_caps(self, budget, caps):
      """The configured cap is the truth, not the copy written into the row this morning. An
      operator who lowers a cap has it bind on the next call rather than tomorrow."""
      token_cap_changed = budget.cap_tokens != caps.cap_tokens
      usd_cap_changed = budget.cap_usd != caps.cap_usd
      cap_changed = token_cap_changed or usd_cap_changed

      if cap_changed:
         budget.cap_tokens = caps.cap_tokens
         budget.cap_usd = caps.cap_usd
         self._stamp(budget)
         self.session().flush()

   def _stamp(self, budget):
      budget.updated_at = as_iso(self._clock())
