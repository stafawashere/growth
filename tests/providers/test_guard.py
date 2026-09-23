"""docs/plan/07-ai-provider-layer.md, "Budget caps", and docs/plan/09-security-and-privacy.md, "Audit log".

No test here opens a socket. The wrapped provider is always a ReplayProvider behind a
recording double, so these tests hold with no key and no network.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session as SqlSession

from app.db import models
from app.providers.base import (
   CacheSettings,
   Message,
   Provider,
   ProviderRequest,
   ProviderResult,
   Usage,
)
from app.providers.guard import (
   BudgetCaps,
   BudgetStopped,
   CACHE_READ_MULTIPLIER,
   CHARACTERS_PER_TOKEN,
   GuardedProvider,
   estimate_call,
)
from app.providers.replay import ReplayProvider

SYSTEM_TEXT = "s" * 400
USER_TEXT = "u" * 400
EXPECTED_PROMPT_TOKENS = 800 // CHARACTERS_PER_TOKEN
MAX_OUTPUT_TOKENS = 1000
EXPECTED_ESTIMATE_USD = (EXPECTED_PROMPT_TOKENS / 1_000_000) * 2.0 + (MAX_OUTPUT_TOKENS / 1_000_000) * 10.0


def _request(**overrides):
   defaults = dict(
      role="tutor",
      model="claude-sonnet-5",
      system=SYSTEM_TEXT,
      messages=(Message(role="user", content=USER_TEXT),),
      max_output_tokens=MAX_OUTPUT_TOKENS,
      cache=CacheSettings(prefix_breakpoints=1, ttl="5m"),
   )
   defaults.update(overrides)

   return ProviderRequest(**defaults)


def _cassette(**overrides):
   usage = dict(input_tokens=50, output_tokens=20, cached_read_tokens=0, cached_write_tokens=0)
   usage.update(overrides)

   return {"text": "Try the chain rule on the inner factor.", "stop_reason": "end_turn", "usage": usage}


class FakeClock:
   def __init__(self, moment):
      self.moment = moment

   def __call__(self):
      return self.moment

   def advance_days(self, days):
      self.moment = self.moment + timedelta(days=days)


class RecordingProvider(Provider):
   """Counts calls and, when given a db, snapshots the budget row as the guard saw it at call time."""

   def __init__(self, inner, db=None):
      self.inner = inner
      self.db = db
      self.calls = 0
      self.snapshots = []

   def generate(self, request):
      self.calls = self.calls + 1

      if self.db is not None:
         row = _budget_rows(self.db)[0]
         self.snapshots.append((row.tokens_in, row.tokens_out, row.cost_usd))

      return self.inner.generate(request)

   def stream(self, request):
      return self.inner.stream(request)


def _db():
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)

   return SqlSession(engine)


def _budget_rows(db):
   return list(db.execute(select(models.Budget)).scalars().all())


def _audit_rows(db):
   return list(db.execute(select(models.AuditLog)).scalars().all())


DEFAULT_TEST_CAPS = BudgetCaps(cap_usd=1000.0)


def _guard(db, double, caps=None, clock=None):
   """A role with no cap is refused by the guard, so a test that is not about the cap still
   carries one, set high enough to be out of the way."""
   return GuardedProvider(
      double,
      db,
      user_id="USR-1",
      clock=clock or FakeClock(datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc)),
      caps={"tutor": caps if caps is not None else DEFAULT_TEST_CAPS},
      provider_name="anthropic",
   )


def test_guard_estimates_the_worst_case_before_the_call():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()), db=db)
   guard = _guard(db, double)

   estimate = estimate_call(_request())

   assert estimate.prompt_tokens == EXPECTED_PROMPT_TOKENS
   assert estimate.output_tokens == MAX_OUTPUT_TOKENS
   assert estimate.total_tokens == EXPECTED_PROMPT_TOKENS + MAX_OUTPUT_TOKENS
   assert estimate.cost_usd == pytest.approx(EXPECTED_ESTIMATE_USD)

   guard.generate(_request())

   reserved_at_call_time = double.snapshots[0]
   assert reserved_at_call_time == (EXPECTED_PROMPT_TOKENS, MAX_OUTPUT_TOKENS, pytest.approx(EXPECTED_ESTIMATE_USD))


def test_guard_refuses_when_the_estimate_crosses_the_dollar_cap():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=EXPECTED_ESTIMATE_USD / 2))

   with pytest.raises(BudgetStopped) as stopped:
      guard.generate(_request())

   assert stopped.value.role == "tutor"
   assert stopped.value.cap == "usd"
   assert double.calls == 0

   row = _budget_rows(db)[0]
   assert row.hard_stopped == 1
   assert row.cost_usd == 0.0
   assert row.tokens_in == 0
   assert row.tokens_out == 0


def test_guard_refuses_when_the_estimate_crosses_the_token_cap():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=EXPECTED_PROMPT_TOKENS + 10, cap_usd=None))

   with pytest.raises(BudgetStopped) as stopped:
      guard.generate(_request())

   assert stopped.value.cap == "tokens"
   assert double.calls == 0
   assert _budget_rows(db)[0].hard_stopped == 1


def test_guard_reconciles_the_estimate_against_raw_usage():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette(input_tokens=50, output_tokens=20)))
   guard = _guard(db, double)

   guard.generate(_request())

   row = _budget_rows(db)[0]
   reconciled_cost = (50 / 1_000_000) * 2.0 + (20 / 1_000_000) * 10.0

   assert row.tokens_in == 50
   assert row.tokens_out == 20
   assert row.cost_usd == pytest.approx(reconciled_cost)

   unreported_db = _db()
   unreported_double = RecordingProvider(
      ReplayProvider(cassette=_cassette(input_tokens=None, output_tokens=None))
   )
   unreported_guard = _guard(unreported_db, unreported_double)

   unreported_guard.generate(_request())

   unreported_row = _budget_rows(unreported_db)[0]

   assert unreported_row.tokens_in == EXPECTED_PROMPT_TOKENS
   assert unreported_row.tokens_out == MAX_OUTPUT_TOKENS
   assert unreported_row.cost_usd == pytest.approx(EXPECTED_ESTIMATE_USD)


def test_guard_keeps_one_budget_row_per_user_role_and_day():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc))
   guard = _guard(db, double, clock=clock)

   guard.generate(_request())
   guard.generate(_request())
   guard.generate(_request())

   rows = _budget_rows(db)
   assert len(rows) == 1
   assert rows[0].day == "2026-09-20"
   assert rows[0].tokens_in == 150

   clock.advance_days(1)
   guard.generate(_request())

   rows = sorted(_budget_rows(db), key=lambda row: row.day)
   assert [row.day for row in rows] == ["2026-09-20", "2026-09-21"]
   assert rows[1].tokens_in == 50


def test_guard_writes_an_audit_entry_when_the_cap_stops_the_role():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0))

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   actions = [row.action for row in _audit_rows(db)]
   assert "budget_hard_stop" in actions
   assert "budget_call_refused" in actions

   hard_stop = [row for row in _audit_rows(db) if row.action == "budget_hard_stop"][0]
   detail = json.loads(hard_stop.detail)

   assert detail == {"provider": "anthropic", "model": "claude-sonnet-5", "role": "tutor", "cap": "usd"}
   assert hard_stop.actor == "USR-1"
   assert hard_stop.subject.startswith("budgets:")


def test_guard_writes_no_key_material_into_the_audit_detail():
   secret_key = "sk-ant-api03-DO-NOT-LOG-THIS"
   student_text = "I think the integral diverges because of the endpoint"
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0))

   request = _request(
      system=SYSTEM_TEXT + secret_key,
      messages=(Message(role="user", content=student_text),),
      provider_options={"api_key": secret_key},
   )

   with pytest.raises(BudgetStopped) as stopped:
      guard.generate(request)

   audit_text = " ".join(f"{row.action} {row.subject} {row.detail}" for row in _audit_rows(db))

   assert secret_key not in audit_text
   assert student_text not in audit_text
   assert "Try the chain rule" not in audit_text
   assert secret_key not in str(stopped.value)
   assert student_text not in str(stopped.value)


def test_a_stopped_role_refuses_every_later_call_that_day():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0))

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   row = _budget_rows(db)[0]
   row.cap_usd = 1000.0
   row.cap_tokens = 10_000_000
   db.flush()

   with pytest.raises(BudgetStopped) as stopped:
      guard.generate(_request())

   assert stopped.value.role == "tutor"
   assert double.calls == 0

   hard_stops = [row for row in _audit_rows(db) if row.action == "budget_hard_stop"]
   refusals = [row for row in _audit_rows(db) if row.action == "budget_call_refused"]

   assert len(hard_stops) == 1
   assert len(refusals) == 2


def test_guard_prices_cached_reads_at_the_multiplier():
   db = _db()
   cassette = _cassette(
      input_tokens=0,
      output_tokens=0,
      cached_read_tokens=1_000_000,
      cached_write_tokens=0,
   )
   double = RecordingProvider(ReplayProvider(cassette=cassette))
   guard = _guard(db, double)

   guard.generate(_request())

   row = _budget_rows(db)[0]

   assert row.tokens_cached_read == 1_000_000
   assert row.cost_usd == pytest.approx(2.0 * CACHE_READ_MULTIPLIER)

   write_db = _db()
   write_cassette = _cassette(
      input_tokens=0,
      output_tokens=0,
      cached_read_tokens=0,
      cached_write_tokens=1_000_000,
   )
   write_double = RecordingProvider(ReplayProvider(cassette=write_cassette))
   write_guard = _guard(write_db, write_double)

   write_guard.generate(_request(cache=CacheSettings(prefix_breakpoints=1, ttl="1h")))

   write_row = _budget_rows(write_db)[0]

   assert write_row.tokens_cached_write == 1_000_000
   assert write_row.cost_usd == pytest.approx(2.0 * 2.0)

   with pytest.raises(ValueError):
      estimate_call(_request(model="claude-not-a-model"))


class StubProvider(Provider):
   """Returns a result built by the test, including shapes a real adapter should never produce."""

   def __init__(self, result):
      self.result = result
      self.calls = 0

   def generate(self, request):
      self.calls = self.calls + 1

      return self.result

   def stream(self, request):
      self.calls = self.calls + 1
      yield ""

      return self.result


def test_an_abandoned_stream_releases_the_reservation():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double)

   generator = guard.stream(_request())
   next(generator)
   generator.close()

   row = _budget_rows(db)[0]

   assert row.tokens_in == 0
   assert row.tokens_out == 0
   assert row.cost_usd == pytest.approx(0.0)


def test_a_completed_stream_reconciles_against_raw_usage():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette(input_tokens=50, output_tokens=20)))
   guard = _guard(db, double)

   chunks = list(guard.stream(_request()))

   assert chunks == ["Try the chain rule on the inner factor."]

   row = _budget_rows(db)[0]
   reconciled_cost = (50 / 1_000_000) * 2.0 + (20 / 1_000_000) * 10.0

   assert row.tokens_in == 50
   assert row.tokens_out == 20
   assert row.cost_usd == pytest.approx(reconciled_cost)


def test_a_stopped_role_records_the_refusal_once_and_still_refuses():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   guard = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0))

   for _attempt in range(39):
      with pytest.raises(BudgetStopped):
         guard.generate(_request())

   before_the_last_attempt = len([row for row in _audit_rows(db) if row.action == "budget_call_refused"])

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   refusals = [row for row in _audit_rows(db) if row.action == "budget_call_refused"]
   reasons = {json.loads(row.detail)["cap"] for row in refusals}

   assert len(refusals) == before_the_last_attempt
   assert len(refusals) == 2
   assert reasons == {"usd", "hard_stopped"}
   assert double.calls == 0


def test_a_lowered_cap_binds_on_the_existing_row():
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   clock = FakeClock(datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc))

   generous = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=1.0), clock=clock)
   generous.generate(_request())

   assert _budget_rows(db)[0].cap_usd == 1.0

   lowered = _guard(db, double, caps=BudgetCaps(cap_tokens=None, cap_usd=0.0), clock=clock)

   with pytest.raises(BudgetStopped) as stopped:
      lowered.generate(_request())

   assert stopped.value.cap == "usd"
   assert double.calls == 1
   assert _budget_rows(db)[0].cap_usd == 0.0


def test_an_unpriced_result_model_is_charged_at_the_requested_model_price():
   db = _db()
   result = ProviderResult(
      text="ok",
      stop_reason="end_turn",
      usage=Usage(input_tokens=50, output_tokens=20, cached_read_tokens=0, cached_write_tokens=0),
      provider="anthropic",
      model="claude-not-a-model",
   )
   double = StubProvider(result)
   guard = _guard(db, double)

   guard.generate(_request())

   row = _budget_rows(db)[0]
   requested_model_cost = (50 / 1_000_000) * 2.0 + (20 / 1_000_000) * 10.0

   assert row.tokens_in == 50
   assert row.tokens_out == 20
   assert row.cost_usd == pytest.approx(requested_model_cost)


def test_a_result_without_usage_keeps_the_worst_case_reservation():
   db = _db()
   result = ProviderResult(
      text="ok",
      stop_reason="end_turn",
      usage=None,
      provider="anthropic",
      model="claude-sonnet-5",
   )
   double = StubProvider(result)
   guard = _guard(db, double)

   returned = guard.generate(_request())

   assert returned is result

   row = _budget_rows(db)[0]

   assert row.tokens_in == EXPECTED_PROMPT_TOKENS
   assert row.tokens_out == MAX_OUTPUT_TOKENS
   assert row.cost_usd == pytest.approx(EXPECTED_ESTIMATE_USD)


def test_a_role_with_no_configured_cap_is_refused():
   """A guard with no cap guards nothing, and an unconfigured role silently spending is the
   failure the whole seam exists to prevent (07, Budget caps)."""
   db = _db()
   double = RecordingProvider(ReplayProvider(cassette=_cassette()), db=db)
   guard = GuardedProvider(
      double,
      db,
      user_id="USR-1",
      clock=FakeClock(datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc)),
      caps={},
      provider_name="anthropic",
   )

   with pytest.raises(BudgetStopped):
      guard.generate(_request())

   assert double.calls == 0
