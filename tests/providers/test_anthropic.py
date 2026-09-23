"""docs/plan/07-ai-provider-layer.md, Anthropic adapter section and Known traps.

No test here opens a socket. Every call is driven through a fake transport, so these
tests hold even though no live API key exists in this environment.
"""
import pytest

from app.providers.base import CacheSettings, Message, ProviderRequest
from app.providers.anthropic import AnthropicProvider


def _request(**overrides):
   defaults = dict(
      role="tutor",
      model="claude-sonnet-5",
      system="You are a guardrailed calculus tutor. " * 50,
      messages=(Message(role="user", content="I am stuck on step two."),),
      max_output_tokens=400,
      cache=CacheSettings(prefix_breakpoints=1, ttl="1h"),
   )
   defaults.update(overrides)
   return ProviderRequest(**defaults)


class RecordingTransport:
   def __init__(self, response):
      self.response = response
      self.calls = []

   def __call__(self, url, headers, body):
      self.calls.append({"url": url, "headers": headers, "body": body})
      return self.response


def _provider(response, environ=None):
   transport = RecordingTransport(response)
   env = environ if environ is not None else {"ANTHROPIC_API_KEY": "test-key-not-real"}
   provider = AnthropicProvider(transport=transport, environ=env)
   return provider, transport


def test_call_maps_to_the_messages_wire_shape():
   response = {
      "content": [{"type": "text", "text": "Which rule did you apply on that step?"}],
      "stop_reason": "end_turn",
      "usage": {"input_tokens": 1200, "output_tokens": 40},
   }
   provider, transport = _provider(response)

   result = provider.generate(_request())

   assert len(transport.calls) == 1

   body = transport.calls[0]["body"]

   assert body["model"] == "claude-sonnet-5"
   assert body["max_tokens"] == 400
   assert "temperature" not in body
   assert body["messages"] == [{"role": "user", "content": "I am stuck on step two."}]
   assert body["system"][0]["text"].startswith("You are a guardrailed calculus tutor.")
   assert body["system"][0]["cache_control"] == {"type": "ephemeral", "ttl": "1h"}

   assert result.text == "Which rule did you apply on that step?"
   assert result.stop_reason == "end_turn"
   assert result.provider == "anthropic"
   assert result.model == "claude-sonnet-5"


def test_usage_reports_all_four_token_fields():
   response_without_cache = {
      "content": [{"type": "text", "text": "ok"}],
      "stop_reason": "end_turn",
      "usage": {"input_tokens": 1200, "output_tokens": 40},
   }
   provider, _transport = _provider(response_without_cache)

   result = provider.generate(_request())

   assert result.usage.input_tokens == 1200
   assert result.usage.output_tokens == 40
   assert result.usage.cached_read_tokens is None
   assert result.usage.cached_write_tokens is None

   response_with_cache = {
      "content": [{"type": "text", "text": "ok"}],
      "stop_reason": "end_turn",
      "usage": {
         "input_tokens": 1200,
         "output_tokens": 40,
         "cache_read_input_tokens": 1024,
         "cache_creation_input_tokens": 0,
      },
   }
   provider, _transport = _provider(response_with_cache)

   result = provider.generate(_request())

   assert result.usage.input_tokens == 1200
   assert result.usage.output_tokens == 40
   assert result.usage.cached_read_tokens == 1024
   assert result.usage.cached_write_tokens == 0


def test_no_tool_definitions_are_ever_sent():
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   provider.generate(_request())

   assert "tools" not in transport.calls[0]["body"]
   assert "tool_choice" not in transport.calls[0]["body"]

   with pytest.raises(ValueError):
      provider.generate(_request(provider_options={"tools": [{"name": "lookup"}]}))

   with pytest.raises(ValueError):
      provider.generate(_request(provider_options={"tool_choice": "auto"}))


def test_adaptive_thinking_is_never_requested():
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   provider.generate(_request())

   assert "thinking" not in transport.calls[0]["body"]

   with pytest.raises(ValueError):
      provider.generate(_request(provider_options={"thinking": {"type": "adaptive"}}))

   with pytest.raises(ValueError):
      provider.generate(_request(provider_options={"thinking": {"type": "enabled"}}))


def test_replay_provider_makes_no_network_call(monkeypatch):
   from app.providers.replay import ReplayProvider

   def _forbidden_socket(*args, **kwargs):
      raise AssertionError("replay provider must never open a socket")

   monkeypatch.setattr("socket.socket", _forbidden_socket)

   cassette = {
      "text": "Which rule did you apply on that step?",
      "stop_reason": "end_turn",
      "usage": {
         "input_tokens": 1200,
         "output_tokens": 40,
         "cached_read_tokens": 1024,
         "cached_write_tokens": 0,
      },
      "provider": "anthropic",
      "model": "claude-sonnet-5",
   }
   provider = ReplayProvider(cassette=cassette)

   result = provider.generate(_request())

   assert result.text == cassette["text"]
   assert result.stop_reason == "end_turn"
   assert result.usage.cached_read_tokens == 1024
   assert result.usage.cached_write_tokens == 0


def test_usage_carries_the_reasoning_token_field():
   """07's usage block has five fields, and the Messages API reports no reasoning count."""
   response = {
      "content": [{"type": "text", "text": "ok"}],
      "stop_reason": "end_turn",
      "usage": {"input_tokens": 1200, "output_tokens": 40},
   }
   provider, _transport = _provider(response)

   result = provider.generate(_request())

   assert result.usage.reasoning_tokens is None
