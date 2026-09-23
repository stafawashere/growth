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
estimate for that field, which leaves the budget row conservative rather than optimistic.

The cached fields keep the distinction in the durable store as counts, because the budgets row is
a daily sum and SQLite cannot relax the NOT NULL on tokens_cached_read and tokens_cached_write in
place (app/db/migrate.py adds columns, it never rebuilds a table). settled_calls counts the calls
that reached the provider. cached_read_reported_calls and cached_write_reported_calls count the
ones whose usage reported that field, zero included. tokens_cached_read and tokens_cached_write
sum only what was reported, so a null adds nothing to them and nothing to the reported count. A
row whose reported count is 0 has never had that field reported, and its token sum is then not a
measurement; a reported count below settled_calls means the sum covers only part of the day. A row
written before the three counts existed reads 0 in all of them after app/db/migrate.py adds them,
with its old sums intact, so a row whose settled_calls is 0 is never a measurement of either
cached field, whatever its sums hold (06, table budgets). The guard adds to such a row as it finds
it and does not backfill the counts, because nothing records how many calls its sums covered.

Worst case rather than refund (13, "Budget, fallback and degradation", item 3). A call that
reached the provider is charged: when it returns, at the reconciled usage; when it raises, when
its result cannot be read, or when the consumer of a stream stops iterating, at the worst-case
reservation. The refund path is reserved for a call that never left, and the guard cannot see the
wire, so it takes the adapter's word: only RefusedBeforeWire from app/providers/base.py, which
an adapter raises for validation, a missing key or a connection never established, releases the
reservation, leaves settled_calls alone and re-raises as ProviderRefusedBeforeWire. Every other
exception, and a GeneratorExit from an abandoned stream, is charged, and the charge is taken in a
finally so the one that is not an Exception is charged too.

The cache write multiplier. 13 item 6 asks for the multiplier from what the result reports rather
than from the request's ttl. Usage reports cached_write_tokens as one number and ProviderResult
carries no ttl, so the result does not say which rate the write was made at, and the guard charges
every cache write at the 1-hour rate, the higher of the two 04 prices. For P1's one role, whose
template caches with the 1-hour ttl (11 P1 item 12), that is the rate actually paid.

The audit row rule. 09's "Audit log" lists a controlled vocabulary of consequential actions and
an ordinary provider call is not in it; one row per tutor call would flood a record 09 describes
as durable and queryable. So the guard writes an audit row when the role hard-stops and when a
call is refused by the cap, and never on an ordinary call. A result the guard cannot read is the
third, because the money is already spent and the accounting could not be settled, and it is rare
by construction rather than per call. Per-call usage accounting lives in budgets, which is the
table 07 names for it.

Where a cap comes from. Until the operator changes a role's cap through PUT /settings/budgets,
the caps the process was started with are in force, and a changed startup cap overwrites today's
row on the next call. Once a PUT has been made for a user and role, which the budget_cap_changed
audit entry flags, the caps stored on the budgets rows are in force: today's row, else the latest
earlier row carried forward. From then on, changing the environment cap no longer binds for that
role, and the settings route is the way to change it.

A role with no configured cap is refused before any call. The guard exists to stop spending past
a cap, and a role whose caps are both None crosses no cap at all, so an unconfigured caller would
otherwise get an unlimited provider with nothing to show that it had. Its budget row is created
with both caps null and hard_stopped 0, so settings shows it as unconfigured rather than stopped,
and the refusal is audited once per user per role per day against that row (13, "A role with no
configured cap").

What a refusal names (13 item 4). A refusal names every cap that this call's projection crosses,
tokens before usd, so a simultaneous crossing names both. A stop still holds for the rest of the
day (07's table: "No further tutor calls today"), so a call that would fit under the caps of a
stopped row is refused too, naming stopped_by, the caps that stopped the row. Raising a cap above
the day's recorded spend clears the stop and stopped_by on the next call (13, "A cap that is
raised after a stop"). Only a raise does: every cap that stopped the row raised, none lowered, and
every cap in force above the spend. A lowered cap keeps the stop even when it still sits above the
spend, because 07 says no further calls today and 13 names only a raise as the way back.

No key material, no raw provider response body and no student response text reaches an audit
detail field or an exception message (09 "Key handling" and "Audit log"). The detail names the
provider, the model, the role and the cap that bound, and nothing else. An exception raised inside
the adapter is re-raised as ProviderCallFailed carrying the provider, the model, the role and the
exception's type name, raised outside the handler so neither __cause__ nor __context__ keeps the
original, whose message may hold a response body or a key (13 item 7).

The price table holds every model 13's routing names, at the interactive rates in 13's cost model
table, which cites Anthropic's and Google's pricing pages: claude-opus-5, claude-sonnet-5,
claude-haiku-4-5, gemini-3.5-flash-lite and gemini-3.8-flash. Gemini 3.8 Flash is promotional
through 2026-12-31 and doubles from 2027-01-01, so its entry carries that end date as data and
price_for takes the day of the call; the guard passes its own clock's day. A dated price asked for
without a day raises rather than guessing a side of the boundary. The cache read multiplier
reproduces every read price the table prints, Gemini's included; the table prints no cache write
price for Gemini, whose implicit caching bills storage by the hour instead, which the guard does not
model. Batch rates are not modelled either (13 item 2). Every other model raises rather than being
priced from a number no plan document carries, so a fallback to an unpriced model is a refusal and
not a silent wrong charge.
"""
import json
import math
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select

from app.auth.service import as_iso, new_id, utc_now, write_audit
from app.db import models
from app.providers.base import Provider, RefusedBeforeWire

CHARACTERS_PER_TOKEN = 4

CACHE_READ_MULTIPLIER = 0.1
CACHE_WRITE_1H_MULTIPLIER = 2.0

HARD_STOP_ACTION = "budget_hard_stop"
CALL_REFUSED_ACTION = "budget_call_refused"
UNREADABLE_RESULT_ACTION = "provider_result_unreadable"
CAP_CHANGED_ACTION = "budget_cap_changed"

ROLES = ("tutor", "generator", "verifier", "grader", "diagnostician", "transcriber")

UNCONFIGURED = "unconfigured"
CAP_SEPARATOR = ","
CAP_FIELDS = (("tokens", "cap_tokens"), ("usd", "cap_usd"))


@dataclass(frozen=True)
class ModelPrice:
   input_usd_per_mtok: float
   output_usd_per_mtok: float


@dataclass(frozen=True)
class DatedModelPrice:
   promotional: ModelPrice
   promotional_through: date
   standard: ModelPrice

   def on(self, day):
      is_promotional = day <= self.promotional_through

      return self.promotional if is_promotional else self.standard


MODEL_PRICES = {
   "claude-opus-5": ModelPrice(input_usd_per_mtok=5.0, output_usd_per_mtok=25.0),
   "claude-sonnet-5": ModelPrice(input_usd_per_mtok=2.0, output_usd_per_mtok=10.0),
   "claude-haiku-4-5": ModelPrice(input_usd_per_mtok=1.0, output_usd_per_mtok=5.0),
   "gemini-3.5-flash-lite": ModelPrice(input_usd_per_mtok=0.30, output_usd_per_mtok=2.50),
   "gemini-3.8-flash": DatedModelPrice(
      promotional=ModelPrice(input_usd_per_mtok=0.75, output_usd_per_mtok=3.75),
      promotional_through=date(2026, 12, 31),
      standard=ModelPrice(input_usd_per_mtok=1.50, output_usd_per_mtok=7.50),
   ),
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


@dataclass(frozen=True)
class CallAccounting:
   """What one call was charged. The cached fields are None when the provider did not report them."""

   model: str
   tokens_in: int
   tokens_out: int
   tokens_cached_read: int | None
   tokens_cached_write: int | None
   cost_usd: float


class ProviderCallFailed(Exception):
   """The adapter raised. Carries the provider, the model, the role and the type name, nothing else."""

   def __init__(self, provider, model, role, exception_type):
      super().__init__(
         f"provider call failed: provider={provider} model={model} role={role} exception={exception_type}"
      )
      self.provider = provider
      self.model = model
      self.role = role
      self.exception_type = exception_type


class ProviderRefusedBeforeWire(ProviderCallFailed, RefusedBeforeWire):
   """The adapter refused before the request left, so the reservation was released rather than
   charged. Bounded like ProviderCallFailed, and still a RefusedBeforeWire so a caller can tell a
   call that cost nothing from one that did."""


class BudgetStopped(Exception):
   """Raised instead of calling the provider. Carries the role and the caps that bound, nothing else.
   cap is the caps joined by a comma, so a single crossing reads as its one name."""

   def __init__(self, role, caps):
      named = (caps,) if isinstance(caps, str) else tuple(caps)
      joined = CAP_SEPARATOR.join(named)

      super().__init__(f"budget cap reached for role {role}: {joined}")
      self.role = role
      self.caps = named
      self.cap = joined


def price_for(model, day=None):
   price = MODEL_PRICES.get(model)

   if price is None:
      raise ValueError(f"no price recorded for model {model!r}")

   is_dated = isinstance(price, DatedModelPrice)

   if not is_dated:
      return price

   if day is None:
      raise ValueError(f"the price of model {model!r} depends on the day and no day was given")

   return price.on(day)


def estimate_prompt_tokens(request):
   """An estimate from characters, never exact. See the module docstring."""
   message_characters = sum(len(message.content) for message in request.messages)
   total_characters = len(request.system or "") + message_characters

   return math.ceil(total_characters / CHARACTERS_PER_TOKEN)


def estimate_call(request, day=None):
   price = price_for(request.model, day)
   prompt_tokens = estimate_prompt_tokens(request)
   output_tokens = request.max_output_tokens

   input_cost = (prompt_tokens / 1_000_000) * price.input_usd_per_mtok
   output_cost = (output_tokens / 1_000_000) * price.output_usd_per_mtok

   return CallEstimate(
      prompt_tokens=prompt_tokens,
      output_tokens=output_tokens,
      cost_usd=input_cost + output_cost,
   )


def usage_cost(model, tokens_in, tokens_out, tokens_cached_read, tokens_cached_write, day=None):
   """Cache writes at the 1-hour rate whatever the request asked for. See the module docstring."""
   price = price_for(model, day)

   base_input = (tokens_in / 1_000_000) * price.input_usd_per_mtok
   cached_read = (tokens_cached_read / 1_000_000) * price.input_usd_per_mtok * CACHE_READ_MULTIPLIER
   cached_write = (tokens_cached_write / 1_000_000) * price.input_usd_per_mtok * CACHE_WRITE_1H_MULTIPLIER
   output = (tokens_out / 1_000_000) * price.output_usd_per_mtok

   return base_input + cached_read + cached_write + output


def find_budget_row(db, user_id, role, day):
   statement = select(models.Budget).where(
      models.Budget.user_id == user_id,
      models.Budget.role == role,
      models.Budget.day == day,
   )

   return db.execute(statement).scalars().first()


def create_budget_row(db, user_id, role, day, caps, timestamp):
   row = models.Budget(
      id=new_id("BUD"),
      user_id=user_id,
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
      settled_calls=0,
      cached_read_reported_calls=0,
      cached_write_reported_calls=0,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(row)
   db.flush()

   return row


def spent_tokens(budget):
   return budget.tokens_in + budget.tokens_out + budget.tokens_cached_read + budget.tokens_cached_write


def reported(value):
   return 0 if value is None else value


def caps_of_row(row):
   return BudgetCaps(cap_tokens=row.cap_tokens, cap_usd=row.cap_usd)


def stopping_caps(budget):
   """The caps that stopped the row. A row stopped before stopped_by existed names the caps it
   carries, which are the only caps that could have stopped it."""
   recorded = budget.stopped_by

   if recorded:
      return tuple(recorded.split(CAP_SEPARATOR))

   carried = (("tokens", budget.cap_tokens), ("usd", budget.cap_usd))

   return tuple(name for name, value in carried if value is not None)


def cap_rises(before, after):
   """None is no cap, so dropping a cap is the largest raise and adding one is a lowering."""
   is_uncapped_after = after is None

   if is_uncapped_after:
      return before is not None

   was_uncapped_before = before is None

   if was_uncapped_before:
      return False

   return after > before


def cap_falls(before, after):
   was_uncapped_before = before is None

   if was_uncapped_before:
      return after is not None

   is_uncapped_after = after is None

   if is_uncapped_after:
      return False

   return after < before


def spend_is_under(budget, caps):
   tokens_under_cap = caps.cap_tokens is None or spent_tokens(budget) < caps.cap_tokens
   usd_under_cap = caps.cap_usd is None or budget.cost_usd < caps.cap_usd

   return tokens_under_cap and usd_under_cap


def change_clears_the_stop(budget, after):
   """13 clears a stop only for a raise above the day's recorded spend, and 07's table says no
   further tutor calls today, so a lowered cap never reopens a role even when it still sits above
   the spend. A raise here is: every cap that stopped the row raised, no cap lowered, and every
   cap in force above the day's spend."""
   is_stopped = budget.hard_stopped == 1

   if not is_stopped:
      return False

   before = caps_of_row(budget)
   stopped_by_names = stopping_caps(budget)
   stopping_fields = [field for name, field in CAP_FIELDS if name in stopped_by_names]
   every_stopping_cap_rises = all(
      cap_rises(getattr(before, field), getattr(after, field)) for field in stopping_fields
   )
   any_cap_falls = any(cap_falls(getattr(before, field), getattr(after, field)) for _name, field in CAP_FIELDS)
   is_a_raise = every_stopping_cap_rises and not any_cap_falls

   return is_a_raise and spend_is_under(budget, after)


def apply_cap_change(budget, after):
   """Writes the caps in force onto the row and clears the stop and its cause together when the
   change is a raise. The guard and PUT /settings/budgets both come through here, so the two
   cannot disagree on what reopens a role. Returns whether anything changed."""
   token_cap_changed = budget.cap_tokens != after.cap_tokens
   usd_cap_changed = budget.cap_usd != after.cap_usd
   cap_changed = token_cap_changed or usd_cap_changed

   if not cap_changed:
      return False

   clears = change_clears_the_stop(budget, after)
   budget.cap_tokens = after.cap_tokens
   budget.cap_usd = after.cap_usd

   if clears:
      budget.hard_stopped = 0
      budget.stopped_by = None

   return True


def latest_earlier_row(db, user_id, role, day):
   statement = (
      select(models.Budget)
      .where(models.Budget.user_id == user_id)
      .where(models.Budget.role == role)
      .where(models.Budget.day < day)
      .order_by(models.Budget.day.desc())
   )

   return db.execute(statement).scalars().first()


def cap_changed_by_operator(db, user_id, role):
   """A flag only. The budget_cap_changed entry says a PUT was made for the role; the values it
   records are never read back as the cap."""
   statement = (
      select(models.AuditLog.detail)
      .where(models.AuditLog.action == CAP_CHANGED_ACTION)
      .where(models.AuditLog.actor == user_id)
   )

   for detail in db.scalars(statement).all():
      recorded = json.loads(detail) if detail else {}
      names_this_role = recorded.get("role") == role

      if names_this_role:
         return True

   return False


def stored_caps(db, user_id, role, day):
   today = find_budget_row(db, user_id, role, day)

   if today is not None:
      return caps_of_row(today)

   earlier = latest_earlier_row(db, user_id, role, day)

   if earlier is not None:
      return caps_of_row(earlier)

   return None


def caps_in_force(db, user_id, role, day, configured):
   """Until the operator changes a role's cap through PUT /settings/budgets, the startup caps are
   in force. After that, the caps stored on the budgets rows are: today's row, else the latest
   earlier row carried forward."""
   is_operator_set = cap_changed_by_operator(db, user_id, role)

   if is_operator_set:
      stored = stored_caps(db, user_id, role, day)

      if stored is not None:
         return stored

   return configured.get(role)


class GuardedProvider(Provider):
   """The only provider object a caller wires. A bypass would defeat the cap, the accounting and the audit.

   last_accounting is None until a call settles and is reset to None when the next call starts, so
   a refused call never leaves the previous call's accounting behind for its caller to read."""

   def __init__(self, provider, db, user_id, clock=None, caps=None, provider_name=None):
      self._provider = provider
      self._db = db
      self._user_id = user_id
      self._clock = clock or utc_now
      self._caps = caps or {}
      self._provider_name = provider_name or getattr(provider, "name", type(provider).__name__)
      self.last_accounting = None

   def generate(self, request):
      self.last_accounting = None
      budget, estimate = self._reserve(request)
      failure = None
      settled = False
      never_left = False

      try:
         try:
            result = self._provider.generate(request)
         except RefusedBeforeWire as refused:
            never_left = True
            failure = self._bounded_refusal(request, refused)
         except Exception as raised:
            failure = self._bounded_failure(request, raised)
         else:
            self._settle(budget, estimate, request, result)
            settled = True
      finally:
         self._close_reservation(budget, estimate, request, settled, never_left)

      if failure is not None:
         raise failure

      return result

   def stream(self, request):
      """A consumer that stops iterating raises GeneratorExit here, which is not an Exception, so
      the worst-case charge is taken in a finally rather than in an except clause."""
      self.last_accounting = None
      budget, estimate = self._reserve(request)
      failure = None
      settled = False
      never_left = False

      try:
         try:
            result = yield from self._provider.stream(request)
         except RefusedBeforeWire as refused:
            never_left = True
            failure = self._bounded_refusal(request, refused)
         except Exception as raised:
            failure = self._bounded_failure(request, raised)
         else:
            self._settle(budget, estimate, request, result)
            settled = True
      finally:
         self._close_reservation(budget, estimate, request, settled, never_left)

      if failure is not None:
         raise failure

      return result

   def session(self):
      is_factory = callable(self._db)

      if is_factory:
         return self._db()

      return self._db

   def _bounded_failure(self, request, raised):
      return ProviderCallFailed(self._provider_name, request.model, request.role, type(raised).__name__)

   def _bounded_refusal(self, request, refused):
      return ProviderRefusedBeforeWire(self._provider_name, request.model, request.role, type(refused).__name__)

   def _close_reservation(self, budget, estimate, request, settled, never_left):
      """Runs from a finally, so a consumer that abandons a stream, whose GeneratorExit is not an
      Exception, still leaves the worst-case charge. Only the adapter's own RefusedBeforeWire
      releases the reservation."""
      if settled:
         return

      if never_left:
         self._release(budget, estimate)
         return

      self._charge_worst_case(budget, estimate, request)

   def _release(self, budget, estimate):
      """The request never left, so the reservation comes off the row and settled_calls is not
      touched: no call reached the provider."""
      budget.tokens_in = budget.tokens_in - estimate.prompt_tokens
      budget.tokens_out = budget.tokens_out - estimate.output_tokens
      budget.cost_usd = budget.cost_usd - estimate.cost_usd
      self._stamp(budget)
      self.session().flush()

   def _reserve(self, request):
      db = self.session()
      estimate = estimate_call(request, self._clock().date())
      budget = self._budget_row(db, request.role)

      is_configured = budget.cap_tokens is not None or budget.cap_usd is not None

      if not is_configured:
         self._refuse(db, budget, request, (UNCONFIGURED,))

      binding = self._binding_caps(budget, estimate)
      already_stopped = budget.hard_stopped == 1
      stops_now = len(binding) > 0 and not already_stopped

      if stops_now:
         budget.hard_stopped = 1
         budget.stopped_by = CAP_SEPARATOR.join(binding)
         self._stamp(budget)
         write_audit(
            db,
            self._user_id,
            HARD_STOP_ACTION,
            f"budgets:{budget.id}",
            self._detail(request, binding),
            now=self._clock(),
         )

      if binding:
         self._refuse(db, budget, request, binding)

      if already_stopped:
         self._refuse(db, budget, request, stopping_caps(budget))

      budget.tokens_in = budget.tokens_in + estimate.prompt_tokens
      budget.tokens_out = budget.tokens_out + estimate.output_tokens
      budget.cost_usd = budget.cost_usd + estimate.cost_usd
      self._stamp(budget)
      db.flush()

      return budget, estimate

   def _refuse(self, db, budget, request, caps):
      """One refusal row per user per role per day per reason, the way app/session/build.py's
      gap_already_recorded bounds the coverage gap row. A row per refused call would flood a
      record 09 calls durable and queryable, and the fortieth row says nothing the first did not."""
      cap = CAP_SEPARATOR.join(caps)
      already_recorded = self._refusal_already_recorded(db, budget, cap)

      if not already_recorded:
         write_audit(
            db,
            self._user_id,
            CALL_REFUSED_ACTION,
            f"budgets:{budget.id}",
            self._detail(request, caps),
            now=self._clock(),
         )
         db.flush()

      raise BudgetStopped(request.role, caps)

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

   def _charge_worst_case(self, budget, estimate, request):
      """The call reached the provider and nothing readable came back, so the reservation stands
      as the charge and neither cached field was reported."""
      budget.settled_calls = budget.settled_calls + 1
      self._stamp(budget)
      self.session().flush()

      self.last_accounting = CallAccounting(
         model=request.model,
         tokens_in=estimate.prompt_tokens,
         tokens_out=estimate.output_tokens,
         tokens_cached_read=None,
         tokens_cached_write=None,
         cost_usd=estimate.cost_usd,
      )

   def _settle(self, budget, estimate, request, result):
      """The money is already spent by the time this runs, so an unreadable result must not leave
      the reservation dangling. An unpriced result model is charged at the requested model, which
      estimate_call already priced; anything else unreadable keeps the worst-case reservation,
      which leaves the row conservative rather than empty."""
      try:
         self._reconcile(budget, estimate, request, result)
      except (AttributeError, TypeError, ValueError) as unreadable:
         self._record_unreadable(budget, request, unreadable)
         self._charge_worst_case(budget, estimate, request)

   def _record_unreadable(self, budget, request, unreadable):
      """One row per user per role per day, which is the bound the budgets row already carries,
      because the subject names that row. A second unreadable result the same day for the same
      role tells an operator nothing the first did not, and 09 calls the log durable and
      queryable. The detail carries what an operator can act on and nothing else: no key material
      and no part of the provider's payload reaches it."""
      db = self.session()
      already_recorded = self._unreadable_already_recorded(db, budget)

      if already_recorded:
         return

      write_audit(
         db,
         self._user_id,
         UNREADABLE_RESULT_ACTION,
         f"budgets:{budget.id}",
         {
            "role": request.role,
            "model": request.model,
            "exception": type(unreadable).__name__,
         },
         now=self._clock(),
      )

   def _unreadable_already_recorded(self, db, budget):
      statement = (
         select(models.AuditLog.id)
         .where(models.AuditLog.action == UNREADABLE_RESULT_ACTION)
         .where(models.AuditLog.actor == self._user_id)
         .where(models.AuditLog.subject == f"budgets:{budget.id}")
      )

      return db.scalars(statement).first() is not None

   def _reconcile(self, budget, estimate, request, result):
      """Everything is computed before the row is touched, so a result that turns out unreadable
      half way leaves the reservation whole for _settle to charge."""
      usage = result.usage

      reported_input = usage.input_tokens
      reported_output = usage.output_tokens
      reported_cached_read = usage.cached_read_tokens
      reported_cached_write = usage.cached_write_tokens

      tokens_in = estimate.prompt_tokens if reported_input is None else reported_input
      tokens_out = estimate.output_tokens if reported_output is None else reported_output
      read_was_reported = reported_cached_read is not None
      write_was_reported = reported_cached_write is not None
      priced_model = self._priced_model(result, request)

      cost = usage_cost(
         priced_model,
         tokens_in,
         tokens_out,
         reported(reported_cached_read),
         reported(reported_cached_write),
         self._clock().date(),
      )

      budget.tokens_in = budget.tokens_in - estimate.prompt_tokens + tokens_in
      budget.tokens_out = budget.tokens_out - estimate.output_tokens + tokens_out
      budget.cost_usd = budget.cost_usd - estimate.cost_usd + cost
      budget.settled_calls = budget.settled_calls + 1

      if read_was_reported:
         budget.tokens_cached_read = budget.tokens_cached_read + reported_cached_read
         budget.cached_read_reported_calls = budget.cached_read_reported_calls + 1

      if write_was_reported:
         budget.tokens_cached_write = budget.tokens_cached_write + reported_cached_write
         budget.cached_write_reported_calls = budget.cached_write_reported_calls + 1

      self._stamp(budget)
      self.session().flush()

      self.last_accounting = CallAccounting(
         model=priced_model,
         tokens_in=tokens_in,
         tokens_out=tokens_out,
         tokens_cached_read=reported_cached_read,
         tokens_cached_write=reported_cached_write,
         cost_usd=cost,
      )

   def _priced_model(self, result, request):
      reported_model = result.model
      has_priced_report = reported_model is not None and reported_model in MODEL_PRICES

      if has_priced_report:
         return reported_model

      return request.model

   def _binding_caps(self, budget, estimate):
      """Every cap this call's projection crosses, tokens before usd, so a simultaneous crossing
      names both rather than whichever is tested first."""
      projected_tokens = spent_tokens(budget) + estimate.total_tokens
      projected_usd = budget.cost_usd + estimate.cost_usd

      has_token_cap = budget.cap_tokens is not None
      crosses_token_cap = has_token_cap and projected_tokens > budget.cap_tokens

      has_usd_cap = budget.cap_usd is not None
      crosses_usd_cap = has_usd_cap and projected_usd > budget.cap_usd

      crossings = (("tokens", crosses_token_cap), ("usd", crosses_usd_cap))

      return tuple(name for name, crosses in crossings if crosses)

   def _detail(self, request, caps):
      return {
         "provider": self._provider_name,
         "model": request.model,
         "role": request.role,
         "cap": CAP_SEPARATOR.join(caps),
      }

   def _budget_row(self, db, role):
      day = self._clock().date().isoformat()
      caps = caps_in_force(db, self._user_id, role, day, self._caps) or BudgetCaps()
      existing = find_budget_row(db, self._user_id, role, day)

      if existing is not None:
         self._apply_caps(existing, caps)

         return existing

      return create_budget_row(db, self._user_id, role, day, caps, as_iso(self._clock()))

   def _apply_caps(self, budget, caps):
      """The cap in force is the truth, not the copy written into the row this morning. A startup
      cap lowered and the process restarted binds on the next call rather than tomorrow, and a
      raise above the day's recorded spend clears the stop on that call (13, "A cap that is raised
      after a stop"). See apply_cap_change for what counts as a raise."""
      changed = apply_cap_change(budget, caps)

      if not changed:
         return

      self._stamp(budget)
      self.session().flush()

   def _stamp(self, budget):
      budget.updated_at = as_iso(self._clock())
