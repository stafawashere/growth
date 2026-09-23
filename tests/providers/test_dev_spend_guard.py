"""The persistent developer spend cap: app/providers/guard.py DevSpendLedger and DevSpendCapExceeded.

Distinct from tests/providers/test_guard.py's BudgetCaps, which are per-user, per-role and reset
every day. This cap is one running total, global across every role and every process run, meant
to stand between the operator's own Anthropic key and the credit on it.

GuardedProvider only tracks a call against the ledger when the caller passes
dev_spend_track=True, and the only real caller that does is app/api/routes/sessions.py, which
sets it from isinstance(settings.tutor, AnthropicProvider). Tracking is never guessed from the
wrapped provider's class inside the guard itself: tests/providers/test_anthropic.py wires a real
AnthropicProvider to a fake transport, and that must never start writing to the real developer
ledger file just because it looks like the live adapter.
"""
import threading
import time
from datetime import datetime, timezone

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
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import (
   BudgetCaps,
   CHARACTERS_PER_TOKEN,
   DevSpendCapExceeded,
   DevSpendLedger,
   GuardedProvider,
   dev_price_row,
)
from app.providers.replay import ReplayProvider

SYSTEM_TEXT = "s" * 400
USER_TEXT = "u" * 400
MAX_OUTPUT_TOKENS = 1000
EXPECTED_PROMPT_TOKENS = 800 // CHARACTERS_PER_TOKEN
GENEROUS_CAPS = BudgetCaps(cap_tokens=10_000_000, cap_usd=1000.0)


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


class FakeClock:
   def __init__(self, moment):
      self.moment = moment

   def __call__(self):
      return self.moment


class LiveDouble(Provider):
   """Stands in for a real adapter, never ReplayProvider, so the dev-spend ledger tracks it."""

   def __init__(self, tokens_in=50, tokens_out=20, cached_read=0, cached_write=0):
      self.calls = 0
      self.tokens_in = tokens_in
      self.tokens_out = tokens_out
      self.cached_read = cached_read
      self.cached_write = cached_write

   def generate(self, request):
      self.calls = self.calls + 1
      usage = Usage(
         input_tokens=self.tokens_in,
         output_tokens=self.tokens_out,
         cached_read_tokens=self.cached_read,
         cached_write_tokens=self.cached_write,
      )

      return ProviderResult(text="ok", finish_reason="end_turn", usage=usage,
                             provider="anthropic", model=request.model)

   def stream(self, request):
      raise NotImplementedError


def _db():
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)

   return SqlSession(engine)


def _guard(db, provider, ledger, cap, clock=None, dev_spend_track=True):
   return GuardedProvider(
      provider,
      db,
      user_id="USR-1",
      clock=clock or FakeClock(datetime(2026, 9, 23, 10, 0, tzinfo=timezone.utc)),
      caps={"tutor": GENEROUS_CAPS},
      provider_name="anthropic",
      dev_spend_cap=cap,
      dev_spend_ledger=ledger,
      dev_spend_track=dev_spend_track,
   )


def test_dev_spend_cap_refuses_a_call_whose_worst_case_would_cross_it(tmp_path):
   db = _db()
   ledger = DevSpendLedger(path=tmp_path / "dev_spend_ledger.json")
   double = LiveDouble()
   guard = _guard(db, double, ledger, cap=0.0001)

   with pytest.raises(DevSpendCapExceeded) as excinfo:
      guard.generate(_request())

   assert double.calls == 0
   assert excinfo.value.role == "tutor"
   assert excinfo.value.cap_usd == 0.0001
   assert ledger.spent() == 0.0

   rows = list(db.execute(select(models.AuditLog)).scalars().all())
   refusals = [row for row in rows if row.action == "dev_spend_cap_refused"]
   assert len(refusals) == 1
   assert refusals[0].actor == "USR-1"


def test_dev_spend_cap_persists_across_a_fresh_guard_instance(tmp_path):
   ledger_path = tmp_path / "dev_spend_ledger.json"

   db1 = _db()
   ledger1 = DevSpendLedger(path=ledger_path)
   double1 = LiveDouble(tokens_in=50, tokens_out=20)
   guard1 = _guard(db1, double1, ledger1, cap=1000.0)
   guard1.generate(_request())

   spent_after_first_call = ledger1.spent()
   assert spent_after_first_call > 0.0

   db2 = _db()
   ledger2 = DevSpendLedger(path=ledger_path)
   assert ledger2.spent() == pytest.approx(spent_after_first_call)

   double2 = LiveDouble()
   tight_cap = spent_after_first_call + 0.0000001
   guard2 = _guard(db2, double2, ledger2, cap=tight_cap)

   with pytest.raises(DevSpendCapExceeded):
      guard2.generate(_request())

   assert double2.calls == 0


def test_dev_spend_reconciles_the_worst_case_reservation_to_actual_usage(tmp_path):
   db = _db()
   ledger = DevSpendLedger(path=tmp_path / "dev_spend_ledger.json")
   double = LiveDouble(tokens_in=50, tokens_out=20, cached_read=0, cached_write=0)
   guard = _guard(db, double, ledger, cap=1000.0)

   sonnet = dev_price_row("claude-sonnet-5", batch=False)
   worst_case = (EXPECTED_PROMPT_TOKENS / 1_000_000) * sonnet["input"] + (MAX_OUTPUT_TOKENS / 1_000_000) * sonnet["output"]
   reconciled = (50 / 1_000_000) * sonnet["input"] + (20 / 1_000_000) * sonnet["output"]

   assert reconciled != pytest.approx(worst_case)

   guard.generate(_request())

   assert ledger.spent() == pytest.approx(reconciled)


def test_replay_calls_cost_nothing_and_never_touch_the_dev_spend_ledger(tmp_path):
   ledger_path = tmp_path / "dev_spend_ledger.json"
   ledger = DevSpendLedger(path=ledger_path)
   db = _db()
   cassette = {
      "text": "Try the chain rule on the inner factor.",
      "finish_reason": "end_turn",
      "usage": {"input_tokens": 50, "output_tokens": 20, "cached_read_tokens": 0, "cached_write_tokens": 0},
   }
   double = ReplayProvider(cassette=cassette)
   guard = _guard(db, double, ledger, cap=0.0000001, dev_spend_track=False)

   guard.generate(_request())
   guard.generate(_request())

   assert ledger.spent() == 0.0
   assert not ledger_path.exists()


def test_dev_spend_tracking_is_off_unless_the_caller_opts_in(tmp_path):
   """The regression this guards against: a double that looks exactly like a live adapter (it
   even reports real usage) must not touch the ledger when dev_spend_track is left at its
   default. Every other test in this file passes dev_spend_track explicitly; this is the one
   that proves the default is off."""
   db = _db()
   ledger = DevSpendLedger(path=tmp_path / "dev_spend_ledger.json")
   double = LiveDouble()
   guard = GuardedProvider(
      double,
      db,
      user_id="USR-1",
      clock=FakeClock(datetime(2026, 9, 23, 10, 0, tzinfo=timezone.utc)),
      caps={"tutor": GENEROUS_CAPS},
      provider_name="anthropic",
      dev_spend_cap=0.0000001,
      dev_spend_ledger=ledger,
   )

   guard.generate(_request())

   assert double.calls == 1
   assert ledger.spent() == 0.0


def test_the_real_anthropic_provider_is_tracked_when_the_caller_opts_in(tmp_path):
   """The composition root's own choice, exercised over the real adapter class rather than a
   double: dev_spend_track=True over a real AnthropicProvider built with no key. The cap is set
   so tight that the reservation refuses the call before the adapter ever reads the missing key,
   so this proves the ledger engaged without opening a socket."""
   db = _db()
   ledger = DevSpendLedger(path=tmp_path / "dev_spend_ledger.json")
   provider = AnthropicProvider(environ={})
   guard = _guard(db, provider, ledger, cap=0.0000001, dev_spend_track=True)

   with pytest.raises(DevSpendCapExceeded):
      guard.generate(_request())

   assert ledger.spent() == 0.0


def test_dev_spend_ledger_add_is_safe_under_concurrent_writers(tmp_path, monkeypatch):
   """Reproduces the unlocked check-then-reserve race the review named: two writers each read the
   same starting total before either has written back, and the slower writer's update is lost.
   The slow_read patch widens the read-to-write window so two threads racing through add() are
   certain to overlap there if nothing serializes them; with the file lock in place, ledger_b's
   add() cannot even start reading until ledger_a's add() (read, sleep, then write) has completed
   and released the lock, so the widened window changes nothing about the result."""
   ledger_path = tmp_path / "dev_spend_ledger.json"
   ledger_a = DevSpendLedger(path=ledger_path)
   ledger_b = DevSpendLedger(path=ledger_path)
   original_read = DevSpendLedger._read

   def slow_read(self):
      value = original_read(self)
      time.sleep(0.05)

      return value

   monkeypatch.setattr(DevSpendLedger, "_read", slow_read)

   barrier = threading.Barrier(2)

   def call(ledger, delta):
      barrier.wait()
      ledger.add(delta)

   thread_a = threading.Thread(target=call, args=(ledger_a, 1.0))
   thread_b = threading.Thread(target=call, args=(ledger_b, 2.0))
   thread_a.start()
   thread_b.start()
   thread_a.join(timeout=5)
   thread_b.join(timeout=5)

   assert not thread_a.is_alive()
   assert not thread_b.is_alive()
   assert ledger_a.spent() == pytest.approx(3.0)


def test_dev_spend_reservation_prices_a_cached_request_at_the_write_rate(tmp_path):
   """A tutor call always sends cache=CacheSettings, which _request() defaults to above.
   dev_actual_usd charges a reported cache write at write_1h, double sonnet's base input rate, so
   a reservation that assumed every prompt token at 1x input can sit below what a cold-cache call
   actually costs. The cap is set just above the uncached worst case: a reservation that still
   priced at input-only would fit under it and let the call through, so this only passes if the
   reservation is priced at the higher, cache-aware rate."""
   sonnet = dev_price_row("claude-sonnet-5", batch=False)
   uncached_worst_case = ((EXPECTED_PROMPT_TOKENS / 1_000_000) * sonnet["input"]
                          + (MAX_OUTPUT_TOKENS / 1_000_000) * sonnet["output"])
   cap_above_uncached_only = uncached_worst_case + 0.000001

   db = _db()
   ledger = DevSpendLedger(path=tmp_path / "dev_spend_ledger.json")
   double = LiveDouble()
   guard = _guard(db, double, ledger, cap=cap_above_uncached_only)

   with pytest.raises(DevSpendCapExceeded):
      guard.generate(_request())

   assert double.calls == 0
   assert ledger.spent() == 0.0


def test_claude_opus_5_5_price_is_present_in_the_dev_spend_price_table():
   interactive = dev_price_row("claude-opus-5-5", batch=False)

   assert interactive == {"input": 4.00, "write_5m": 5.00, "write_1h": 8.00, "read": 0.20, "output": 20.00}

   batch = dev_price_row("claude-opus-5-5", batch=True)

   assert batch["input"] == pytest.approx(2.00)
   assert batch["output"] == pytest.approx(10.00)
