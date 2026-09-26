"""The fallback chain and its cooldowns, app/providers/router.py (11 P6 scope item 5, cut to one
student). Every link wraps a double behind the real GuardedProvider, so nothing here starts a
process or opens a socket.
"""
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SqlSession

from app.db import models
from app.providers.base import Message, Provider, ProviderRequest, RefusedBeforeWire
from app.providers.guard import (
   ROLES,
   BudgetCaps,
   BudgetStopped,
   DevSpendLedger,
   ProviderCallFailed,
   SubscriptionPacingCaps,
   SubscriptionPacingLedger,
)
from app.providers.replay import ReplayProvider
from app.providers.router import (
   API_LINK,
   FAILURE_COOLDOWN,
   FAILURES_BEFORE_COOLDOWN,
   LIMIT_COOLDOWN,
   SUBSCRIPTION_LINK,
   ChainLink,
   CooldownBoard,
   CoolingDown,
   FallbackChain,
)
from app.providers.subscription import SubscriptionLimitReached, SubscriptionTransportError

CASSETTE = {
   "text": "Rewrite before cancelling.",
   "finish_reason": "success",
   "usage": {"input_tokens": 1400, "output_tokens": 120, "cached_read_tokens": 0, "cached_write_tokens": 0},
}
ROOMY_CAPS = BudgetCaps(cap_usd=5.0, cap_tokens=5_000_000)
DOLLAR_CAP_BELOW_ONE_CALL = BudgetCaps(cap_usd=0.000001, cap_tokens=10)
START = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)


class Clock:
   def __init__(self, moment):
      self.moment = moment

   def __call__(self):
      return self.moment

   def advance(self, **delta):
      self.moment = self.moment + timedelta(**delta)


class ScriptedProvider(Provider):
   """Answers from the cassette, or raises what raises names, and counts every call that reached it."""

   def __init__(self, raises=None):
      self.calls = 0
      self.raises = raises
      self.inner = ReplayProvider(cassette=CASSETTE)

   def generate(self, request):
      self.calls = self.calls + 1

      if self.raises is not None:
         raise self.raises("scripted failure")

      return self.inner.generate(request)

   def stream(self, request):
      return self.inner.stream(request)


def request_for(role):
   return ProviderRequest(
      role=role,
      model="claude-sonnet-5",
      system="You write one short paragraph.",
      messages=[Message(role="user", content="violated step: 2")],
      max_output_tokens=600,
   )


def database():
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)

   return SqlSession(engine)


def guard_options(tmp_path):
   return {
      "pacing_ledger": SubscriptionPacingLedger(path=tmp_path / "pacing.json"),
      "dev_spend_ledger": DevSpendLedger(path=tmp_path / "dev_spend.json"),
      "dev_spend_cap": 15.0,
   }


def chain_of(links, tmp_path, clock, board, caps=None):
   return FallbackChain(
      links,
      database(),
      "USER-1",
      caps=caps if caps is not None else {role: ROOMY_CAPS for role in ROLES},
      clock=clock,
      board=board,
      guard_options=guard_options(tmp_path),
   )


def subscription_and_api(subscription, api):
   return (
      ChainLink(SUBSCRIPTION_LINK, subscription, pacing=SubscriptionPacingCaps()),
      ChainLink(API_LINK, api, pays=True),
   )


def test_fallback_chain(tmp_path):
   """A usage limit on the subscription moves the call to the API link and cools the subscription:
   the next call skips it without starting anything, and once the cooldown ends it is tried first
   again."""
   subscription = ScriptedProvider(raises=SubscriptionLimitReached)
   api = ScriptedProvider()
   clock = Clock(START)
   board = CooldownBoard()
   chain = chain_of(subscription_and_api(subscription, api), tmp_path, clock, board)

   first = chain.generate(request_for("tutor"))

   assert first.text == CASSETTE["text"]
   assert chain.served_by == API_LINK
   assert (subscription.calls, api.calls) == (1, 1)
   assert board.snapshot(clock())[0]["because"] == SubscriptionLimitReached.__name__

   clock.advance(minutes=5)
   chain.generate(request_for("tutor"))

   assert (subscription.calls, api.calls) == (1, 2)

   subscription.raises = None
   clock.advance(seconds=LIMIT_COOLDOWN.total_seconds())
   chain.generate(request_for("tutor"))

   assert chain.served_by == SUBSCRIPTION_LINK
   assert (subscription.calls, api.calls) == (2, 2)
   assert board.snapshot(clock()) == []


def test_without_the_api_link_a_limit_reaches_the_caller_and_the_cooldown_starts_no_call(tmp_path):
   subscription = ScriptedProvider(raises=SubscriptionLimitReached)
   clock = Clock(START)
   chain = chain_of((ChainLink(SUBSCRIPTION_LINK, subscription, pacing=SubscriptionPacingCaps()),), tmp_path, clock, CooldownBoard())

   with pytest.raises(ProviderCallFailed) as first:
      chain.generate(request_for("tutor"))

   assert first.value.exception_type == SubscriptionLimitReached.__name__

   with pytest.raises(CoolingDown) as second:
      chain.generate(request_for("tutor"))

   assert second.value.exception_type == SubscriptionLimitReached.__name__
   assert subscription.calls == 1


def test_a_cooldown_belongs_to_one_role(tmp_path):
   subscription = ScriptedProvider(raises=SubscriptionLimitReached)
   clock = Clock(START)
   chain = chain_of((ChainLink(SUBSCRIPTION_LINK, subscription, pacing=SubscriptionPacingCaps()),), tmp_path, clock, CooldownBoard())

   with pytest.raises(ProviderCallFailed):
      chain.generate(request_for("tutor"))

   subscription.raises = None

   assert chain.generate(request_for("grader")).text == CASSETTE["text"]
   assert subscription.calls == 2


def test_repeated_transport_failures_cool_the_link_and_a_single_one_does_not(tmp_path):
   subscription = ScriptedProvider(raises=SubscriptionTransportError)
   api = ScriptedProvider()
   clock = Clock(START)
   board = CooldownBoard()
   chain = chain_of(subscription_and_api(subscription, api), tmp_path, clock, board)

   for _ in range(FAILURES_BEFORE_COOLDOWN - 1):
      chain.generate(request_for("grader"))

   assert board.snapshot(clock()) == []

   chain.generate(request_for("grader"))
   chain.generate(request_for("grader"))

   assert subscription.calls == FAILURES_BEFORE_COOLDOWN
   assert api.calls == FAILURES_BEFORE_COOLDOWN + 1

   clock.advance(seconds=FAILURE_COOLDOWN.total_seconds())
   subscription.raises = None
   chain.generate(request_for("grader"))

   assert chain.served_by == SUBSCRIPTION_LINK


def test_a_pacing_stop_moves_the_call_on_without_cooling_the_link(tmp_path):
   subscription = ScriptedProvider()
   api = ScriptedProvider()
   clock = Clock(START)
   board = CooldownBoard()
   one_a_day = SubscriptionPacingCaps(calls_per_day={"tutor": 1}, calls_per_minute=10)
   links = (ChainLink(SUBSCRIPTION_LINK, subscription, pacing=one_a_day), ChainLink(API_LINK, api, pays=True))
   chain = chain_of(links, tmp_path, clock, board)

   chain.generate(request_for("tutor"))
   chain.generate(request_for("tutor"))

   assert (subscription.calls, api.calls) == (1, 1)
   assert chain.served_by == API_LINK
   assert board.snapshot(clock()) == []


def test_a_link_that_cannot_run_does_not_hide_the_next_links_stop(tmp_path):
   """No CLI installed says nothing about the call; the API link's cap stop is what the caller must
   see, so it degrades as a cap and not as a call that silently returned nothing."""
   subscription = ScriptedProvider(raises=RefusedBeforeWire)
   api = ScriptedProvider()
   links = subscription_and_api(subscription, api)
   chain = chain_of(links, tmp_path, Clock(START), CooldownBoard(), caps={"tutor": DOLLAR_CAP_BELOW_ONE_CALL})

   with pytest.raises(BudgetStopped):
      chain.generate(request_for("tutor"))

   assert api.calls == 0


@pytest.mark.parametrize("role", ROLES)
def test_budget_blocks_before_call(role, tmp_path):
   """For every role: a subscription link past its daily count and an API link whose dollar cap is
   below one call are both refused by their guards, neither provider is reached, and the caller gets
   the budget stop it already degrades to static feedback."""
   subscription = ScriptedProvider()
   api = ScriptedProvider()
   clock = Clock(START)
   used_up = SubscriptionPacingCaps(calls_per_day={role: 1}, calls_per_minute=10)
   links = (ChainLink(SUBSCRIPTION_LINK, subscription, pacing=used_up), ChainLink(API_LINK, api, pays=True))
   chain = chain_of(links, tmp_path, clock, CooldownBoard(), caps={role: DOLLAR_CAP_BELOW_ONE_CALL})

   chain.generate(request_for(role))

   assert (subscription.calls, api.calls) == (1, 0)

   with pytest.raises(BudgetStopped):
      chain.generate(request_for(role))

   assert (subscription.calls, api.calls) == (1, 0)
   assert chain.last_accounting is None


@pytest.mark.parametrize("role", ROLES)
def test_a_role_with_no_cap_on_the_api_link_is_refused_there(role, tmp_path):
   api = ScriptedProvider()
   chain = chain_of((ChainLink(API_LINK, api, pays=True),), tmp_path, Clock(START), CooldownBoard(), caps={})

   with pytest.raises(BudgetStopped):
      chain.generate(request_for(role))

   assert api.calls == 0
