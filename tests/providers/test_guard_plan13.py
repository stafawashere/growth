"""docs/plan/13-ai-engineering.md, "Budget, fallback and degradation": the guard items 3 to 7 and
the two missing rows of 07's hard-stop table, a role with no configured cap and a cap raised
after a stop.

Every assertion about spend reads the budgets columns back with a column select, so it sees what
the database holds rather than an attribute on a mapped object.
"""
import json
import traceback
from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.db import models
from app.providers.base import Provider, RefusedBeforeWire
from app.providers.guard import (
   CACHE_WRITE_1H_MULTIPLIER,
   CALL_REFUSED_ACTION,
   BudgetCaps,
   BudgetStopped,
   CallAccounting,
   GuardedProvider,
   ProviderCallFailed,
)
from app.providers.replay import ReplayProvider
from tests.providers.test_guard import (
   EXPECTED_ESTIMATE_USD,
   EXPECTED_PROMPT_TOKENS,
   MAX_OUTPUT_TOKENS,
   FakeClock,
   RecordingProvider,
   _audit_rows,
   _cassette,
   _db,
   _guard,
   _request,
)

MORNING = datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc)
FAKE_KEY = "sk-ant-api03-FAKE-KEY-DO-NOT-LOG"
FAKE_BODY = '{"error": {"message": "the student wrote d/dx of x squared is 2x"}}'


def budget_columns(db):
   return db.execute(select(models.Budget.__table__)).mappings().one()


def refusals(db):
   return [row for row in _audit_rows(db) if row.action == CALL_REFUSED_ACTION]


class RaisingProvider(Provider):
   """An adapter that fails after the request has left, the way an HTTP client stringifies a
   response body and the key it sent into its own error."""

   def __init__(self, chunks_before_failure=0):
      self.calls = 0
      self.chunks_before_failure = chunks_before_failure

   def generate(self, request):
      self.calls = self.calls + 1

      raise RuntimeError(f"401 from api with x-api-key {FAKE_KEY}: {FAKE_BODY}")

   def stream(self, request):
      self.calls = self.calls + 1

      for index in range(self.chunks_before_failure):
         yield f"chunk {index}"

      raise RuntimeError(f"401 from api with x-api-key {FAKE_KEY}: {FAKE_BODY}")


def test_an_exception_after_the_wire_keeps_the_worst_case_charge():
   db = _db()
   guard = _guard(db, RaisingProvider())

   with pytest.raises(ProviderCallFailed):
      guard.generate(_request())

   row = budget_columns(db)

   assert row["tokens_in"] == EXPECTED_PROMPT_TOKENS
   assert row["tokens_out"] == MAX_OUTPUT_TOKENS
   assert row["cost_usd"] == pytest.approx(EXPECTED_ESTIMATE_USD)
   assert row["settled_calls"] == 1


def test_a_stream_that_fails_mid_way_keeps_the_worst_case_charge():
   db = _db()
   guard = _guard(db, RaisingProvider(chunks_before_failure=1))
   generator = guard.stream(_request())

   assert next(generator) == "chunk 0"

   with pytest.raises(ProviderCallFailed):
      next(generator)

   row = budget_columns(db)

   assert row["tokens_in"] == EXPECTED_PROMPT_TOKENS
   assert row["cost_usd"] == pytest.approx(EXPECTED_ESTIMATE_USD)


def test_the_bounded_failure_carries_no_key_and_no_body():
   db = _db()
   guard = _guard(db, RaisingProvider())

   with pytest.raises(ProviderCallFailed) as failed:
      guard.generate(_request())

   failure = failed.value
   rendered = "".join(traceback.format_exception(failure))
   surfaces = (str(failure), repr(failure), rendered)

   for surface in surfaces:
      assert FAKE_KEY not in surface
      assert "the student wrote" not in surface

   assert failure.__cause__ is None
   assert failure.__context__ is None
   assert (failure.provider, failure.model, failure.role, failure.exception_type) == (
      "anthropic",
      "claude-sonnet-5",
      "tutor",
      "RuntimeError",
   )


def test_a_failing_stream_is_bounded_too():
   db = _db()
   guard = _guard(db, RaisingProvider())

   with pytest.raises(ProviderCallFailed) as failed:
      list(guard.stream(_request()))

   rendered = "".join(traceback.format_exception(failed.value))

   assert FAKE_KEY not in rendered
   assert failed.value.__context__ is None


def test_simultaneous_crossings_name_both_caps():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=1.0, cap_usd=0.0))

   with pytest.raises(BudgetStopped) as stopped:
      guard.generate(_request())

   hard_stop = [row for row in _audit_rows(db) if row.action == "budget_hard_stop"][0]

   assert stopped.value.caps == ("tokens", "usd")
   assert json.loads(hard_stop.detail)["cap"] == "tokens,usd"


def test_a_second_distinct_crossing_is_named_after_a_stop():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0), clock=clock).generate(_request())

   token_cap_added = BudgetCaps(cap_tokens=1.0, cap_usd=0.0)

   with pytest.raises(BudgetStopped) as stopped:
      _guard(db, double, caps=token_cap_added, clock=clock).generate(_request())

   reasons = {json.loads(row.detail)["cap"] for row in refusals(db)}

   assert stopped.value.caps == ("tokens", "usd")
   assert reasons == {"usd", "tokens,usd"}
   assert budget_columns(db)["hard_stopped"] == 1
   assert double.calls == 0


def test_a_cap_raised_above_the_spend_that_a_new_cap_crosses_names_the_new_cap():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0), clock=clock).generate(_request())

   with pytest.raises(BudgetStopped) as stopped:
      _guard(db, double, caps=BudgetCaps(cap_tokens=1.0, cap_usd=1000.0), clock=clock).generate(_request())

   assert stopped.value.cap == "tokens"
   assert double.calls == 0


def test_a_stopped_role_stays_stopped_for_a_call_that_would_fit():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   caps = BudgetCaps(cap_tokens=None, cap_usd=EXPECTED_ESTIMATE_USD / 2)
   guard = _guard(db, double, caps=caps)

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   with pytest.raises(BudgetStopped) as stopped:
      guard.generate(_request(max_output_tokens=1))

   assert stopped.value.cap == "usd"
   assert double.calls == 0
   assert budget_columns(db)["hard_stopped"] == 1


def test_a_cap_raised_above_the_days_spend_clears_the_stop():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0), clock=clock).generate(_request())

   assert budget_columns(db)["hard_stopped"] == 1

   _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=1.0), clock=clock).generate(_request())

   assert double.calls == 1
   assert budget_columns(db)["hard_stopped"] == 0


def test_a_cap_raised_but_still_under_the_days_spend_keeps_the_stop():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)

   _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=1.0), clock=clock).generate(_request())
   spent = budget_columns(db)["cost_usd"]

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=spent / 4), clock=clock).generate(_request())

   with pytest.raises(BudgetStopped) as stopped:
      _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=spent / 2), clock=clock).generate(_request())

   hard_stops = [row for row in _audit_rows(db) if row.action == "budget_hard_stop"]

   assert stopped.value.cap == "usd"
   assert double.calls == 1
   assert budget_columns(db)["hard_stopped"] == 1
   assert len(hard_stops) == 1


def unconfigured_guard(db, double, clock):
   return GuardedProvider(double, db, user_id="USR-1", clock=clock, caps={}, provider_name="anthropic")


def test_an_unconfigured_role_is_refused_and_audited_once_per_day():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)
   guard = unconfigured_guard(db, double, clock)

   for _attempt in range(3):
      with pytest.raises(BudgetStopped) as stopped:
         guard.generate(_request())

   assert stopped.value.cap == "unconfigured"
   assert len(refusals(db)) == 1

   detail = json.loads(refusals(db)[0].detail)

   assert detail == {"provider": "anthropic", "model": "claude-sonnet-5", "role": "tutor", "cap": "unconfigured"}

   clock.advance_days(1)

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   assert len(refusals(db)) == 2
   assert double.calls == 0


def test_an_unconfigured_role_is_not_shown_as_stopped():
   db = _db()
   guard = unconfigured_guard(db, RecordingProvider(ReplayProvider(cassette=_cassette())), FakeClock(MORNING))

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   row = budget_columns(db)

   assert row["hard_stopped"] == 0
   assert (row["cap_tokens"], row["cap_usd"]) == (None, None)


def test_a_null_cached_usage_is_not_stored_as_a_reported_zero():
   db = _db()
   unreported = RecordingProvider(ReplayProvider(cassette=_cassette(cached_read_tokens=None, cached_write_tokens=None)))
   clock = FakeClock(MORNING)

   _guard(db, unreported, clock=clock).generate(_request())

   row = budget_columns(db)

   assert row["settled_calls"] == 1
   assert row["cached_read_reported_calls"] == 0
   assert row["cached_write_reported_calls"] == 0

   reported_zero = RecordingProvider(ReplayProvider(cassette=_cassette(cached_read_tokens=0, cached_write_tokens=0)))
   _guard(db, reported_zero, clock=clock).generate(_request())

   row = budget_columns(db)

   assert row["settled_calls"] == 2
   assert row["cached_read_reported_calls"] == 1
   assert row["cached_write_reported_calls"] == 1
   assert row["tokens_cached_read"] == 0


def test_a_cache_write_on_a_request_that_set_no_cache_is_charged_at_the_worst_case():
   db = _db()
   cassette = _cassette(input_tokens=0, output_tokens=0, cached_read_tokens=0, cached_write_tokens=1_000_000)
   guard = _guard(db, RecordingProvider(ReplayProvider(cassette=cassette)))

   guard.generate(_request(cache=None))

   assert budget_columns(db)["cost_usd"] == pytest.approx(2.0 * CACHE_WRITE_1H_MULTIPLIER)


def test_last_accounting_is_the_settled_calls_accounting():
   db = _db()
   cassette = _cassette(input_tokens=50, output_tokens=20, cached_read_tokens=None, cached_write_tokens=0)
   guard = _guard(db, RecordingProvider(ReplayProvider(cassette=cassette)))

   assert guard.last_accounting is None

   guard.generate(_request())

   expected_cost = (50 / 1_000_000) * 2.0 + (20 / 1_000_000) * 10.0

   assert guard.last_accounting == CallAccounting(
      model="claude-sonnet-5",
      tokens_in=50,
      tokens_out=20,
      tokens_cached_read=None,
      tokens_cached_write=0,
      cost_usd=pytest.approx(expected_cost),
   )


def test_a_refused_call_leaves_no_stale_accounting():
   db = _db()
   caps = {"tutor": BudgetCaps(cap_tokens=None, cap_usd=1.0)}
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = GuardedProvider(double, db, user_id="USR-1", clock=FakeClock(MORNING), caps=caps, provider_name="anthropic")

   guard.generate(_request())

   assert guard.last_accounting is not None

   caps["tutor"] = BudgetCaps(cap_tokens=None, cap_usd=0.0)

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   assert guard.last_accounting is None


def test_a_cap_lowered_after_a_stop_keeps_the_stop_while_the_cap_still_sits_above_the_spend():
   """07's table says no further tutor calls today, and 13 clears the stop only for a raise. A cap
   lowered to a value still above the day's spend is not a raise, so a smaller call that would fit
   under it stays refused."""
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)
   stopping_cap = EXPECTED_ESTIMATE_USD / 2

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=stopping_cap), clock=clock).generate(_request())

   lowered = BudgetCaps(cap_tokens=None, cap_usd=stopping_cap / 2)

   with pytest.raises(BudgetStopped) as stopped:
      _guard(db, double, caps=lowered, clock=clock).generate(_request(max_output_tokens=1))

   row = budget_columns(db)

   assert stopped.value.cap == "usd"
   assert double.calls == 0
   assert row["cost_usd"] < lowered.cap_usd
   assert (row["hard_stopped"], row["stopped_by"]) == (1, "usd")


def test_raising_only_a_cap_that_did_not_stop_the_role_keeps_the_stop():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)
   stopping_cap = EXPECTED_ESTIMATE_USD / 2
   token_cap = 1_000_000.0

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=token_cap, cap_usd=stopping_cap), clock=clock).generate(_request())

   tokens_raised = BudgetCaps(cap_tokens=token_cap * 2, cap_usd=stopping_cap)

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=tokens_raised, clock=clock).generate(_request(max_output_tokens=1))

   assert double.calls == 0
   assert (budget_columns(db)["hard_stopped"], budget_columns(db)["stopped_by"]) == (1, "usd")



def test_raising_the_stopping_cap_while_lowering_the_other_keeps_the_stop():
   """13 clears a stop only for a raise above the day's spend, and 07's table says no further
   tutor calls today. Raising the cap that stopped the role while lowering the other is not a
   raise, even when both still sit above the spend and the next call fits under both."""
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(MORNING)
   stopping_cap = EXPECTED_ESTIMATE_USD / 2
   token_cap = 1_000_000.0

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=BudgetCaps(cap_tokens=token_cap, cap_usd=stopping_cap), clock=clock).generate(_request())

   usd_raised_tokens_lowered = BudgetCaps(cap_tokens=token_cap / 2, cap_usd=EXPECTED_ESTIMATE_USD * 100)

   with pytest.raises(BudgetStopped) as stopped:
      _guard(db, double, caps=usd_raised_tokens_lowered, clock=clock).generate(_request(max_output_tokens=1))

   row = budget_columns(db)
   spent_tokens = row["tokens_in"] + row["tokens_out"]

   assert stopped.value.cap == "usd"
   assert double.calls == 0
   assert row["cost_usd"] < usd_raised_tokens_lowered.cap_usd
   assert spent_tokens < usd_raised_tokens_lowered.cap_tokens
   assert (row["cap_usd"], row["cap_tokens"]) == (usd_raised_tokens_lowered.cap_usd, token_cap / 2)
   assert (row["hard_stopped"], row["stopped_by"]) == (1, "usd")

class RefusingAdapter(Provider):
   """An adapter whose request provably never left: RefusedBeforeWire is the adapter's own word
   for validation, a missing key or a connection that was never established."""

   def __init__(self):
      self.calls = 0

   def generate(self, request):
      self.calls = self.calls + 1

      raise RefusedBeforeWire(f"no key configured, would have sent {FAKE_KEY}")

   def stream(self, request):
      self.calls = self.calls + 1

      raise RefusedBeforeWire(f"no key configured, would have sent {FAKE_KEY}")
      yield ""


def test_a_call_refused_before_the_wire_is_refunded():
   db = _db()
   adapter = RefusingAdapter()
   guard = _guard(db, adapter)

   with pytest.raises(ProviderCallFailed) as failed:
      guard.generate(_request())

   row = budget_columns(db)

   assert adapter.calls == 1
   assert isinstance(failed.value, RefusedBeforeWire)
   assert FAKE_KEY not in str(failed.value)
   assert (row["tokens_in"], row["tokens_out"], row["cost_usd"]) == (0, 0, 0.0)
   assert row["settled_calls"] == 0
   assert guard.last_accounting is None


def test_a_stream_refused_before_the_wire_is_refunded():
   db = _db()
   guard = _guard(db, RefusingAdapter())

   with pytest.raises(RefusedBeforeWire):
      next(guard.stream(_request()))

   row = budget_columns(db)

   assert (row["tokens_in"], row["tokens_out"], row["cost_usd"]) == (0, 0, 0.0)
   assert row["settled_calls"] == 0
