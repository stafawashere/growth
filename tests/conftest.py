"""Suite-wide guards for the subscription backend.

No test may run the operator's real claude CLI, which would spend the operator's subscription
and could reach the network. Every binary app/providers/subscription.py resolves must sit under
tests/fixtures, and anything else fails the test before a process starts. The notional
subscription ledger is pointed at a per-test file so no test writes var/.
"""
from pathlib import Path

import pytest

from app.providers import guard, subscription

FIXTURES_DIR = (Path(__file__).resolve().parent / "fixtures").resolve()


def is_fixture_binary(resolved_path):
   return FIXTURES_DIR in Path(resolved_path).resolve().parents


@pytest.fixture(autouse=True)
def forbid_the_real_claude_binary(monkeypatch, tmp_path_factory):
   original_resolve_binary = subscription.resolve_binary

   def resolve_fixture_binary_only(binary, search_path):
      resolved = original_resolve_binary(binary, search_path)

      if not is_fixture_binary(resolved):
         pytest.fail(f"a test resolved a claude binary outside tests/fixtures: {resolved}")

      return resolved

   monkeypatch.setattr(subscription, "resolve_binary", resolve_fixture_binary_only)
   ledger_dir = tmp_path_factory.mktemp("subscription_ledger")
   monkeypatch.setattr(guard, "SUBSCRIPTION_SPEND_LEDGER_PATH", ledger_dir / "ledger.json")
