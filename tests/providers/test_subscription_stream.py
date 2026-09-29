"""The incremental stream of app/providers/subscription.py (docs/agent/architecture.md, Streaming end
to end) against the stream modes of tests/fixtures/fake_claude/claude, which print stream-json lines
the way the installed CLI did on 2026-09-29 (docs/agent/research/providers.md, Measured on
2026-09-29 by the orchestrator).
"""
import time
from pathlib import Path

import pytest

from app.providers.base import Message, ProviderRequest
from app.providers.guard import SubscriptionSpendLedger
from app.providers.subscription import (
   DISALLOWED_TOOLS,
   SubscriptionAuthFailed,
   SubscriptionLimitReached,
   SubscriptionProvider,
   SubscriptionTransportError,
)
from tests.providers.test_subscription import FakeCli, option_value

STREAMED_DELTAS = ("First sentence. ", "Second ", "sentence?")
SCHEMA = {"type": "object", "properties": {"sentence": {"type": "string"}}}
FIRST_DELTA_BOUND_SECONDS = 5
INTERRUPT_BOUND_SECONDS = 5


def request_for(role, stream=True, output_schema=None):
   return ProviderRequest(
      role=role,
      model="claude-sonnet-5-5",
      system="You ask one question at a time.",
      messages=[Message(role="user", content="is my chain rule step right")],
      max_output_tokens=800,
      output_schema=output_schema,
      stream=stream,
   )


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


@pytest.fixture
def ledger(tmp_path):
   return SubscriptionSpendLedger(path=tmp_path / "subscription_ledger.json")


def provider_for(cli, ledger, timeout_seconds=30, **extra_env):
   return SubscriptionProvider(
      environ=cli.environ(**extra_env),
      subscription_ledger=ledger,
      timeout_seconds=timeout_seconds,
   )


def drain(generator):
   events = []

   with pytest.raises(StopIteration) as finished:
      while True:
         events.append(next(generator))

   return events, finished.value.value


def test_deltas_arrive_in_order_and_the_result_carries_the_usage_and_the_joined_text(cli, ledger):
   cli.mode("stream")
   events, result = drain(provider_for(cli, ledger).stream(request_for("agent")))

   assert events == [{"type": "text", "delta": delta} for delta in STREAMED_DELTAS]
   assert result.text == "".join(STREAMED_DELTAS)
   assert result.usage.input_tokens == 1200
   assert result.usage.output_tokens == 40
   assert result.usage.cached_read_tokens == 900
   assert result.usage.cached_write_tokens == 300
   assert result.raw_usage["total_cost_usd"] == 0.0123
   assert result.raw_usage["duration_ms"] == 2345
   assert ledger.spent() == pytest.approx(0.0123)


def test_the_first_delta_reaches_the_caller_while_the_process_still_runs(cli, ledger):
   """The fake holds after its first delta until the test releases it, so a stream that shows
   nothing before the process exits waits the fake's whole hold and misses the bound."""
   cli.mode("stream")
   (cli.home / "fake_claude_hold").write_text("hold")
   generator = provider_for(cli, ledger).stream(request_for("agent"))
   started = time.monotonic()
   first_event = next(generator)
   elapsed = time.monotonic() - started
   (cli.home / "fake_claude_release").write_text("release")
   rest, result = drain(generator)

   assert elapsed < FIRST_DELTA_BOUND_SECONDS
   assert first_event == {"type": "text", "delta": STREAMED_DELTAS[0]}
   assert [event["delta"] for event in rest] == list(STREAMED_DELTAS[1:])
   assert result.text == "".join(STREAMED_DELTAS)


def test_the_rate_limit_event_keeps_both_windows_with_their_reset_times(cli, ledger):
   """The fake stamps its reset times from the clock, an hour and a day ahead, so the windows are
   checked against the moments around the call."""
   cli.mode("stream")
   provider = provider_for(cli, ledger)
   before = int(time.time())
   drain(provider.stream(request_for("agent")))
   after = int(time.time())
   windows = provider.last_rate_limit["unifiedWindows"]
   five_hour_reset = windows["five_hour"]["resetsAt"]
   seven_day_reset = windows["seven_day"]["resetsAt"]

   assert provider.last_rate_limit["status"] == "allowed"
   assert provider.last_rate_limit["rateLimitType"] == "five_hour"
   assert provider.last_rate_limit["resetsAt"] == five_hour_reset
   assert windows["five_hour"] == {"utilization": 0.18, "resetsAt": five_hour_reset}
   assert windows["seven_day"] == {"utilization": 0.29, "resetsAt": seven_day_reset}
   assert before + 3600 <= five_hour_reset <= after + 3600
   assert before + 86400 <= seven_day_reset <= after + 86400


def test_the_stream_asks_for_partial_messages_and_keeps_every_lockdown_flag(cli, ledger):
   cli.mode("stream")
   drain(provider_for(cli, ledger).stream(request_for("agent")))
   record = cli.record()
   argv = record["argv"]

   assert option_value(argv, "--output-format") == "stream-json"
   assert "--include-partial-messages" in argv
   assert "--verbose" in argv
   assert "--input-format" not in argv
   assert "--no-session-persistence" in argv
   assert option_value(argv, "--tools") == ""
   assert option_value(argv, "--disallowedTools") == ",".join(DISALLOWED_TOOLS)
   assert option_value(argv, "--setting-sources") == ""
   assert record["stdin"] == "is my chain rule step right"
   assert record["cwd_entries"] == []
   assert not Path(record["cwd"]).exists()


@pytest.mark.parametrize("role", ["agent", "memory"])
def test_the_agent_and_memory_roles_get_the_fixed_retry_bounds_and_never_the_hosts(cli, ledger, role):
   cli.mode("stream")
   provider = provider_for(cli, ledger, CLAUDE_CODE_MAX_RETRIES="10", API_TIMEOUT_MS="600000")
   drain(provider.stream(request_for(role)))
   env = cli.record()["env"]

   assert env["CLAUDE_CODE_MAX_RETRIES"] == "1"
   assert env["API_TIMEOUT_MS"] == "20000"


def test_the_agent_role_gets_the_retry_bounds_on_generate_too(cli, ledger):
   cli.mode("success")
   provider_for(cli, ledger).generate(request_for("agent", stream=False))
   env = cli.record()["env"]

   assert env["CLAUDE_CODE_MAX_RETRIES"] == "1"
   assert env["API_TIMEOUT_MS"] == "20000"


def test_the_tutor_role_gets_no_retry_bounds_and_nothing_copied_from_the_host(cli, ledger):
   cli.mode("stream")
   provider = provider_for(cli, ledger, CLAUDE_CODE_MAX_RETRIES="10", API_TIMEOUT_MS="600000")
   drain(provider.stream(request_for("tutor")))
   env = cli.record()["env"]

   assert "CLAUDE_CODE_MAX_RETRIES" not in env
   assert "API_TIMEOUT_MS" not in env


def test_a_rate_limit_retry_interrupts_the_process_and_raises_the_limit_error(cli, ledger):
   """The fake sleeps 30 s after the retry line, so only the interrupt ends it inside the bound."""
   cli.mode("stream_limit")
   generator = provider_for(cli, ledger).stream(request_for("agent"))
   started = time.monotonic()

   with pytest.raises(SubscriptionLimitReached) as raised:
      next(generator)

   elapsed = time.monotonic() - started

   assert elapsed < INTERRUPT_BOUND_SECONDS
   assert "agent" in str(raised.value)


def test_an_authentication_retry_interrupts_the_process_and_raises_the_auth_error(cli, ledger):
   cli.mode("stream_auth")
   generator = provider_for(cli, ledger).stream(request_for("agent"))
   started = time.monotonic()

   with pytest.raises(SubscriptionAuthFailed):
      next(generator)

   assert time.monotonic() - started < INTERRUPT_BOUND_SECONDS


def test_a_stream_past_the_timeout_is_killed_and_raises_a_transport_error(cli, ledger):
   cli.mode("stream")
   (cli.home / "fake_claude_hold").write_text("hold")
   generator = provider_for(cli, ledger, timeout_seconds=1).stream(request_for("agent"))
   started = time.monotonic()

   with pytest.raises(SubscriptionTransportError) as raised:
      drain(generator)

   assert time.monotonic() - started < INTERRUPT_BOUND_SECONDS
   assert "timed out" in str(raised.value)


def test_a_request_with_a_schema_keeps_the_json_format_and_one_delta(cli, ledger):
   cli.mode("structured")
   events, result = drain(provider_for(cli, ledger).stream(request_for("agent", output_schema=SCHEMA)))
   argv = cli.record()["argv"]

   assert option_value(argv, "--output-format") == "json"
   assert "--include-partial-messages" not in argv
   assert events == [{"type": "text", "delta": result.text}]


def test_a_request_that_does_not_stream_keeps_the_json_format_and_one_delta(cli, ledger):
   cli.mode("stream")
   events, result = drain(provider_for(cli, ledger).stream(request_for("agent", stream=False)))
   argv = cli.record()["argv"]

   assert option_value(argv, "--output-format") == "json"
   assert "--include-partial-messages" not in argv
   assert events == [{"type": "text", "delta": "".join(STREAMED_DELTAS)}]
   assert result.text == "".join(STREAMED_DELTAS)
