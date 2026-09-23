"""Slice 10: the tutor role's real cassettes against claude-haiku-4-5.

tests/fixtures/provider_cassettes/tutor_haiku_live_*.json are eight calls recorded live against
api.anthropic.com on 2026-09-23, each request built from a real content/items_p1_agent item and
its BC-ERR record through app/feedback/render.elaborated_payload and app/feedback/tutor.request_for,
with the model swapped from the tutor role's assigned claude-sonnet-5 to claude-haiku-4-5 per this
slice's budget. No network call happens here: app/providers/replay.ReplayProvider plays each
cassette back, and the cost recorded on each file is recomputed from its own usage numbers through
app/providers/guard.usage_cost, the same function that priced the live call, so a change to
MODEL_PRICES or the pricing formula that would silently mis-price a Haiku call is caught here.
"""
import json
from pathlib import Path

import pytest

from app.providers.base import CacheSettings, Message, ProviderRequest
from app.providers.guard import usage_cost
from app.providers.replay import ReplayProvider

CASSETTES_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "provider_cassettes"
CASSETTE_PATHS = sorted(CASSETTES_DIR.glob("tutor_haiku_live_*.json"))


def _request():
   return ProviderRequest(
      role="tutor",
      model="claude-haiku-4-5",
      system="s",
      messages=(Message(role="user", content="u"),),
      max_output_tokens=600,
      cache=CacheSettings(prefix_breakpoints=1, ttl="1h"),
   )


@pytest.mark.parametrize("cassette_path", CASSETTE_PATHS, ids=lambda path: path.name)
def test_cassette_is_a_real_recording_not_synthetic(cassette_path):
   cassette = json.loads(cassette_path.read_text())

   assert cassette["recorded"] is True
   assert "synthetic" not in cassette
   assert cassette["model"] == "claude-haiku-4-5"
   assert cassette["role"] == "tutor"
   assert cassette["request_id"].startswith("msg_")
   assert cassette["text"].strip() != ""


@pytest.mark.parametrize("cassette_path", CASSETTE_PATHS, ids=lambda path: path.name)
def test_cassette_replays_with_no_network_call(cassette_path):
   provider = ReplayProvider(cassette_path=cassette_path)
   result = provider.generate(_request())
   cassette = json.loads(cassette_path.read_text())

   assert result.text == cassette["text"]
   assert result.model == "claude-haiku-4-5"
   assert result.provider == "anthropic"
   assert result.usage.input_tokens == cassette["usage"]["input_tokens"]
   assert result.usage.output_tokens == cassette["usage"]["output_tokens"]


@pytest.mark.parametrize("cassette_path", CASSETTE_PATHS, ids=lambda path: path.name)
def test_cassette_cost_matches_guard_pricing(cassette_path):
   cassette = json.loads(cassette_path.read_text())
   usage = cassette["usage"]

   recomputed = usage_cost(
      cassette["model"],
      usage["input_tokens"],
      usage["output_tokens"],
      usage["cached_read_tokens"] or 0,
      usage["cached_write_tokens"] or 0,
   )

   assert recomputed == pytest.approx(cassette["cost_usd"], rel=1e-9)


def test_none_of_the_eight_calls_cached_the_prefix():
   """Live evidence, not an assumption: the tutor template's static prefix measures roughly
   1,300 to 1,600 tokens per call (each cassette's own input_tokens), well under Haiku 4.5's
   4,096-token cache minimum (docs/plan/07-ai-provider-layer.md, Cache-prefix stability), so
   every one of these eight live calls processed its prefix uncached. This is what
   docs/plan/07-ai-provider-layer.md predicts and the live cassettes confirm it rather than
   merely assume it.
   """
   for path in CASSETTE_PATHS:
      cassette = json.loads(path.read_text())

      assert cassette["usage"]["cached_read_tokens"] == 0
      assert cassette["usage"]["cached_write_tokens"] == 0


def test_eight_cassettes_recorded():
   assert len(CASSETTE_PATHS) == 8
