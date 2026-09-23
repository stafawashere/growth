"""app/providers/subscription.py against tests/fixtures/fake_claude/claude, which records the argv,
stdin, environment and working directory it was started with and answers with a canned result.
No test here starts the real claude CLI (tests/conftest.py fails any that tries).
"""
import json
import os
from pathlib import Path

import pytest

from app.providers import guard
from app.providers.base import Message, ProviderRequest, RefusedBeforeWire
from app.providers.guard import DevSpendLedger, GuardedProvider, SubscriptionSpendLedger
from app.providers.subscription import (
   SubscriptionBinaryMissing,
   SubscriptionLimitReached,
   SubscriptionProvider,
   SubscriptionTransportError,
   max_budget_for,
)

FAKE_CLAUDE = Path(__file__).resolve().parents[1] / "fixtures" / "fake_claude" / "claude"
SYSTEM_PROMPT = "---\ntitle: Elaborated feedback\n---\n\nYou write one short paragraph."
USER_PROMPT = "violated step: 2\nobserved behavior: the factor is cancelled early"


def tutor_request(output_schema=None):
   return ProviderRequest(
      role="tutor",
      model="claude-sonnet-5",
      system=SYSTEM_PROMPT,
      messages=[Message(role="user", content=USER_PROMPT)],
      max_output_tokens=600,
      output_schema=output_schema,
   )


class FakeCli:
   def __init__(self, home):
      self.home = home

   def mode(self, name):
      (self.home / "fake_claude_mode").write_text(name)

   def record(self):
      return json.loads((self.home / "fake_claude_record.json").read_text())

   def environ(self, **extra):
      environ = {
         "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
         "HOME": str(self.home),
         "GROWTH_CLAUDE_BIN": str(FAKE_CLAUDE),
      }
      environ.update(extra)

      return environ


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


@pytest.fixture
def ledger(tmp_path):
   return SubscriptionSpendLedger(path=tmp_path / "subscription_ledger.json")


def provider_for(cli, ledger, **extra_env):
   return SubscriptionProvider(environ=cli.environ(**extra_env), subscription_ledger=ledger)


def option_value(argv, flag):
   return argv[argv.index(flag) + 1]


def test_the_cli_runs_headless_with_the_requested_model_and_the_system_prompt(cli, ledger):
   cli.mode("success")
   provider_for(cli, ledger).generate(tutor_request())
   argv = cli.record()["argv"]

   assert argv[0] == str(FAKE_CLAUDE)
   assert "-p" in argv
   assert option_value(argv, "--model") == "claude-sonnet-5"
   assert f"--system-prompt={SYSTEM_PROMPT}" in argv
   assert option_value(argv, "--output-format") == "json"
   assert option_value(argv, "--max-budget-usd") == f"{max_budget_for('tutor'):.2f}"
   assert "--no-session-persistence" in argv
   assert "--bare" not in argv
   assert "--max-turns" not in argv
   assert "--json-schema" not in " ".join(argv)


def test_the_cli_loads_no_settings_mcp_server_or_project_context(cli, ledger):
   cli.mode("success")
   provider_for(cli, ledger).generate(tutor_request())
   record = cli.record()
   argv = record["argv"]

   assert option_value(argv, "--setting-sources") == ""
   assert "--strict-mcp-config" in argv
   assert json.loads(option_value(argv, "--mcp-config")) == {"mcpServers": {}}
   assert "--disable-slash-commands" in argv
   assert record["cwd_entries"] == []
   assert not Path(record["cwd"]).exists()
   assert Path(record["cwd"]).resolve() != Path.cwd().resolve()


def test_the_user_prompt_goes_on_stdin_and_never_on_the_command_line(cli, ledger):
   cli.mode("success")
   provider_for(cli, ledger).generate(tutor_request())
   record = cli.record()

   assert record["stdin"] == USER_PROMPT
   assert all(USER_PROMPT not in argument for argument in record["argv"])


def test_usage_and_result_map_onto_the_provider_result(cli, ledger):
   cli.mode("success")
   result = provider_for(cli, ledger).generate(tutor_request())

   assert result.text == "The factor cancels only after the rewrite, so the answer point is lost."
   assert result.finish_reason == "success"
   assert result.provider == "subscription"
   assert result.model == "claude-sonnet-5"
   assert result.usage.input_tokens == 1200
   assert result.usage.output_tokens == 40
   assert result.usage.cached_read_tokens == 900
   assert result.usage.cached_write_tokens == 300
   assert result.raw_usage["total_cost_usd"] == 0.0123
   assert result.raw_usage["duration_ms"] == 2345


def test_structured_output_asks_for_the_schema_and_returns_the_structured_json(cli, ledger):
   schema = {"type": "object", "properties": {"sentence": {"type": "string"}}, "required": ["sentence"]}
   cli.mode("structured")
   result = provider_for(cli, ledger).generate(tutor_request(output_schema=schema))
   argv = cli.record()["argv"]

   assert f"--json-schema={json.dumps(schema)}" in argv
   assert json.loads(result.text) == {"sentence": "Rewrite first."}


def test_the_reported_cost_lands_on_the_subscription_counter_and_never_on_the_api_cap(
   cli, ledger, tmp_path, monkeypatch
):
   api_cap_path = tmp_path / "dev_spend_ledger.json"
   monkeypatch.setattr(guard, "DEV_SPEND_LEDGER_PATH", api_cap_path)

   assert DevSpendLedger().path == api_cap_path

   cli.mode("success")
   provider_for(cli, ledger).generate(tutor_request())
   provider_for(cli, ledger).generate(tutor_request())

   assert ledger.spent() == pytest.approx(0.0246)
   assert DevSpendLedger().spent() == 0.0
   assert not api_cap_path.exists()


def test_the_default_subscription_counter_is_a_different_file_from_the_api_cap_ledger():
   assert SubscriptionSpendLedger().path != DevSpendLedger().path


def test_stream_yields_the_whole_result_as_one_text_delta(cli, ledger):
   cli.mode("success")
   generator = provider_for(cli, ledger).stream(tutor_request())
   events = []

   with pytest.raises(StopIteration) as finished:
      while True:
         events.append(next(generator))

   assert events == [{"type": "text", "delta": finished.value.value.text}]
   assert finished.value.value.usage.input_tokens == 1200


def test_a_weekly_limit_answer_raises_the_limit_error(cli, ledger):
   cli.mode("weekly_limit")

   with pytest.raises(SubscriptionLimitReached):
      provider_for(cli, ledger).generate(tutor_request())


def test_a_five_hour_limit_on_stderr_with_a_failed_exit_raises_the_limit_error(cli, ledger):
   cli.mode("five_hour_limit_stderr")

   with pytest.raises(SubscriptionLimitReached):
      provider_for(cli, ledger).generate(tutor_request())


def test_output_that_is_not_json_is_a_transport_error(cli, ledger):
   cli.mode("malformed")

   with pytest.raises(SubscriptionTransportError) as raised:
      provider_for(cli, ledger).generate(tutor_request())

   assert not isinstance(raised.value, SubscriptionLimitReached)


def test_a_non_zero_exit_without_a_limit_message_is_a_transport_error(cli, ledger):
   cli.mode("nonzero")

   with pytest.raises(SubscriptionTransportError) as raised:
      provider_for(cli, ledger).generate(tutor_request())

   assert not isinstance(raised.value, RefusedBeforeWire)


def test_a_missing_binary_never_left_so_it_is_refused_before_the_wire(cli, ledger, tmp_path):
   environ = cli.environ(GROWTH_CLAUDE_BIN=str(tmp_path / "no-such-claude"))
   provider = SubscriptionProvider(environ=environ, subscription_ledger=ledger)

   with pytest.raises(SubscriptionBinaryMissing) as raised:
      provider.generate(tutor_request())

   assert isinstance(raised.value, RefusedBeforeWire)


def test_through_the_guard_a_limit_is_reported_by_its_type_name(cli, ledger, tmp_path):
   from app.db import models
   from app.providers.guard import BudgetCaps, ProviderCallFailed
   from sqlalchemy.orm import Session as OrmSession

   engine = models.make_engine(tmp_path / "growth.db")
   cli.mode("weekly_limit")

   with OrmSession(engine) as db:
      guarded = GuardedProvider(
         provider_for(cli, ledger), db, "USR-1", caps={"tutor": BudgetCaps(cap_usd=1.0)}
      )

      with pytest.raises(ProviderCallFailed) as raised:
         guarded.generate(tutor_request())

   assert raised.value.exception_type == SubscriptionLimitReached.__name__
   assert raised.value.provider == "subscription"


def test_the_conftest_guard_fails_a_test_that_resolves_a_binary_outside_the_fixtures(cli, ledger, tmp_path):
   stray_binary = tmp_path / "claude"
   stray_binary.write_text("#!/bin/sh\nexit 0\n")
   stray_binary.chmod(0o755)
   provider = SubscriptionProvider(
      environ=cli.environ(GROWTH_CLAUDE_BIN=str(stray_binary)), subscription_ledger=ledger
   )

   with pytest.raises(pytest.fail.Exception):
      provider.generate(tutor_request())

   assert not (cli.home / "fake_claude_record.json").exists()
