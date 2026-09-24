"""The subscription pacing guard in app/providers/guard.py.

A role on the operator's subscription is capped by call counts per day and per minute, never by
the per-role dollar and token caps, which price the call at API rates the subscription never
bills. The wrapped provider is a ReplayProvider behind a counting double, so nothing here starts
a process or opens a socket.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session as SqlSession

from app.db import models
from app.providers.base import Message, Provider, ProviderRequest, RefusedBeforeWire
from app.providers.guard import (
   BudgetCaps,
   BudgetStopped,
   GuardedProvider,
   SUBSCRIPTION_DAILY_CAP,
   SUBSCRIPTION_MINUTE_RATE,
   SubscriptionPaceExceeded,
   SubscriptionPacingCaps,
   SubscriptionPacingLedger,
)
from app.providers.replay import ReplayProvider

CASSETTE = {
   "text": "Rewrite before cancelling.",
   "finish_reason": "success",
   "usage": {"input_tokens": 1400, "output_tokens": 120, "cached_read_tokens": 0, "cached_write_tokens": 0},
}
DOLLAR_CAP_BELOW_ONE_CALL = BudgetCaps(cap_usd=0.000001, cap_tokens=10)


class Clock:
   def __init__(self, moment):
      self.moment = moment

   def __call__(self):
      return self.moment

   def advance(self, **delta):
      self.moment = self.moment + timedelta(**delta)


class CountingProvider(Provider):
   def __init__(self, refuse_before_wire=False):
      self.calls = 0
      self.refuse_before_wire = refuse_before_wire
      self.inner = ReplayProvider(cassette=CASSETTE)

   def generate(self, request):
      self.calls = self.calls + 1

      if self.refuse_before_wire:
         raise RefusedBeforeWire("no process started")

      return self.inner.generate(request)

   def stream(self, request):
      return self.inner.stream(request)


def tutor_request():
   return ProviderRequest(
      role="tutor",
      model="claude-sonnet-5",
      system="You write one short paragraph.",
      messages=[Message(role="user", content="violated step: 2")],
      max_output_tokens=600,
   )


def database():
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)

   return SqlSession(engine)


@pytest.fixture
def clock():
   return Clock(datetime(2026, 9, 23, 10, 0, tzinfo=timezone.utc))


@pytest.fixture
def pacing_ledger(tmp_path):
   return SubscriptionPacingLedger(path=tmp_path / "pacing.json")


def paced_guard(db, provider, clock, pacing_ledger, pacing):
   return GuardedProvider(
      provider,
      db,
      user_id="USR-1",
      clock=clock,
      caps={"tutor": DOLLAR_CAP_BELOW_ONE_CALL},
      provider_name="subscription",
      subscription_pacing=pacing,
      pacing_ledger=pacing_ledger,
   )


def budget_rows(db):
   return db.scalars(select(models.Budget)).all()


def pacing_refusals(db):
   statement = select(models.AuditLog).where(models.AuditLog.action == "budget_call_refused")

   return [row for row in db.scalars(statement).all() if row.subject.startswith("subscription_pacing")]


def test_a_subscription_call_is_never_stopped_or_charged_by_the_api_dollar_cap(clock, pacing_ledger):
   db = database()
   provider = CountingProvider()
   guard = paced_guard(db, provider, clock, pacing_ledger, SubscriptionPacingCaps())

   first = guard.generate(tutor_request())
   second = guard.generate(tutor_request())

   assert first.text == "Rewrite before cancelling."
   assert second.text == "Rewrite before cancelling."
   assert provider.calls == 2
   assert budget_rows(db) == []
   assert guard.last_accounting.tokens_in == 1400
   assert guard.last_accounting.cost_usd > DOLLAR_CAP_BELOW_ONE_CALL.cap_usd
   assert pacing_ledger.calls_today("tutor", clock()) == 2


def test_the_same_dollar_cap_still_stops_an_api_call(clock):
   db = database()
   provider = CountingProvider()
   guard = GuardedProvider(provider, db, user_id="USR-1", clock=clock, caps={"tutor": DOLLAR_CAP_BELOW_ONE_CALL})

   with pytest.raises(BudgetStopped):
      guard.generate(tutor_request())

   assert provider.calls == 0


def test_the_daily_call_cap_refuses_before_the_provider_and_resets_the_next_day(clock, pacing_ledger):
   db = database()
   provider = CountingProvider()
   pacing = SubscriptionPacingCaps(calls_per_day={"tutor": 2}, calls_per_minute=100)
   guard = paced_guard(db, provider, clock, pacing_ledger, pacing)

   guard.generate(tutor_request())
   clock.advance(minutes=5)
   guard.generate(tutor_request())
   clock.advance(minutes=5)

   with pytest.raises(SubscriptionPaceExceeded) as refused:
      guard.generate(tutor_request())

   with pytest.raises(SubscriptionPaceExceeded):
      guard.generate(tutor_request())

   assert refused.value.cap == SUBSCRIPTION_DAILY_CAP
   assert isinstance(refused.value, BudgetStopped)
   assert provider.calls == 2

   refusals = pacing_refusals(db)

   assert len(refusals) == 1
   assert json.loads(refusals[0].detail)["cap"] == SUBSCRIPTION_DAILY_CAP

   clock.advance(days=1)
   guard.generate(tutor_request())

   assert provider.calls == 3


def test_the_minute_rate_refuses_a_burst_and_lets_the_next_minute_through(clock, pacing_ledger):
   db = database()
   provider = CountingProvider()
   pacing = SubscriptionPacingCaps(calls_per_day={"tutor": 100}, calls_per_minute=2)
   guard = paced_guard(db, provider, clock, pacing_ledger, pacing)

   guard.generate(tutor_request())
   clock.advance(seconds=10)
   guard.generate(tutor_request())
   clock.advance(seconds=10)

   with pytest.raises(SubscriptionPaceExceeded) as refused:
      guard.generate(tutor_request())

   assert refused.value.cap == SUBSCRIPTION_MINUTE_RATE
   assert provider.calls == 2

   clock.advance(seconds=45)
   guard.generate(tutor_request())

   assert provider.calls == 3


def test_a_call_that_never_left_gives_its_pacing_slot_back(clock, pacing_ledger):
   db = database()
   pacing = SubscriptionPacingCaps(calls_per_day={"tutor": 1}, calls_per_minute=100)
   refusing = paced_guard(db, CountingProvider(refuse_before_wire=True), clock, pacing_ledger, pacing)

   with pytest.raises(RefusedBeforeWire):
      refusing.generate(tutor_request())

   assert pacing_ledger.calls_today("tutor", clock()) == 0

   answering = paced_guard(db, CountingProvider(), clock, pacing_ledger, pacing)
   answering.generate(tutor_request())

   assert pacing_ledger.calls_today("tutor", clock()) == 1
