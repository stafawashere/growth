"""docs/plan/07-ai-provider-layer.md, Anthropic adapter section and Known traps.

Every call is driven through a fake transport or a patched opener, so these tests hold even
though no live API key exists in this environment. The one exception is the redirect test, which
opens two servers on 127.0.0.1 and nothing beyond it.
"""
import http.server
import json
import socket
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session as SqlSession

from app.db import models
from app.providers.base import CacheSettings, Message, ProviderRequest, RefusedBeforeWire
from app.providers import anthropic
from app.providers.anthropic import MESSAGES_URL, AnthropicProvider, ProviderTransportError
from app.providers.guard import BudgetCaps, GuardedProvider


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
   assert result.finish_reason == "end_turn"
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
      "finish_reason": "end_turn",
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
   assert result.finish_reason == "end_turn"
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


def test_reasoning_tokens_reads_the_thinking_token_field_when_reported():
   """13-ai-engineering.md: usage.output_tokens_details.thinking_tokens is the field 13 names."""
   response = {
      "content": [{"type": "text", "text": "ok"}],
      "stop_reason": "end_turn",
      "usage": {
         "input_tokens": 1200,
         "output_tokens": 340,
         "output_tokens_details": {"thinking_tokens": 250},
      },
   }
   provider, _transport = _provider(response)

   result = provider.generate(_request())

   assert result.usage.reasoning_tokens == 250


def test_reasoning_tokens_is_a_real_zero_when_reported_as_zero():
   response = {
      "content": [{"type": "text", "text": "ok"}],
      "stop_reason": "end_turn",
      "usage": {
         "input_tokens": 1200,
         "output_tokens": 40,
         "output_tokens_details": {"thinking_tokens": 0},
      },
   }
   provider, _transport = _provider(response)

   result = provider.generate(_request())

   assert result.usage.reasoning_tokens == 0
   assert result.usage.reasoning_tokens is not None


def test_the_plaintext_key_is_never_a_named_local_on_a_raising_frame():
   """13, 'Where app/providers/guard.py is wrong', item 8: the key must not sit in f_locals
   on any frame that can raise, and must never be an attribute retained on the adapter."""
   secret = "sk-ant-do-not-print-this-value-anywhere"

   def _raising_transport(url, headers, body):
      raise ConnectionError("network is down")

   provider = AnthropicProvider(transport=_raising_transport, environ={"ANTHROPIC_API_KEY": secret})

   assert not hasattr(provider, "api_key")
   assert not hasattr(provider, "_api_key")

   with pytest.raises(ProviderTransportError) as excinfo:
      provider.generate(_request())

   offending_frames = []
   traceback_obj = excinfo.tb

   while traceback_obj is not None:
      frame = traceback_obj.tb_frame
      is_adapter_frame = frame.f_code.co_filename.endswith("app/providers/anthropic.py")

      if is_adapter_frame:
         for local_name, local_value in frame.f_locals.items():
            if local_value == secret:
               offending_frames.append((frame.f_code.co_name, local_name))

      traceback_obj = traceback_obj.tb_next

   assert offending_frames == []
   assert not hasattr(provider, "api_key")
   assert not hasattr(provider, "_api_key")


def test_thinking_disabled_and_effort_reach_the_wire_body():
   """I4: provider_options.thinking of type disabled and output_config.effort both reach
   the wire body untouched."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   provider.generate(_request(provider_options={
      "thinking": {"type": "disabled"},
      "output_config": {"effort": "low"},
   }))

   body = transport.calls[0]["body"]

   assert body["thinking"] == {"type": "disabled"}
   assert body["output_config"]["effort"] == "low"


def test_thinking_form_selection_is_by_model_family():
   """07 line 145: 'The adapter selects the thinking form by model family and a golden test
   asserts the selection.' Sonnet 5 accepts thinking disabled at any effort; 13 corrects that
   Opus 5 accepts it only at effort high or below."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}

   provider, transport = _provider(response)
   provider.generate(_request(
      model="claude-sonnet-5",
      provider_options={"thinking": {"type": "disabled"}, "output_config": {"effort": "max"}},
   ))
   assert transport.calls[0]["body"]["thinking"] == {"type": "disabled"}

   provider, transport = _provider(response)
   provider.generate(_request(
      model="claude-opus-5",
      provider_options={"thinking": {"type": "disabled"}, "output_config": {"effort": "high"}},
   ))
   assert transport.calls[0]["body"]["thinking"] == {"type": "disabled"}

   provider, transport = _provider(response)
   with pytest.raises(ValueError):
      provider.generate(_request(
         model="claude-opus-5",
         provider_options={"thinking": {"type": "disabled"}, "output_config": {"effort": "xhigh"}},
      ))
   assert transport.calls == []


def test_opus_5_accepts_disabled_thinking_at_the_default_effort():
   """13: output_config.effort defaults to high, and Opus 5 accepts disabled thinking at
   high or below, so leaving effort unset must not be refused."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   provider.generate(_request(
      model="claude-opus-5",
      provider_options={"thinking": {"type": "disabled"}},
   ))

   assert transport.calls[0]["body"]["thinking"] == {"type": "disabled"}


def test_effort_outside_the_five_named_levels_is_refused():
   """07: 'output_config.effort parameter with levels low, medium, high, xhigh and max'."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   with pytest.raises(ValueError):
      provider.generate(_request(provider_options={"output_config": {"effort": "ultra"}}))

   assert transport.calls == []


def test_stream_maps_anthropic_events_to_the_normalised_vocabulary():
   """06-architecture.md, 'Normalising provider streams': text_delta to text, thinking_delta
   to reasoning, input_json_delta to json, ping dropped. No message_delta reported a stop
   reason, so end carries none rather than an invented one."""
   events = [
      {"event": "message_start", "data": {"message": {"model": "claude-sonnet-5", "id": "msg_123"}}},
      {"event": "content_block_delta", "data": {"delta": {"type": "text_delta", "text": "Which"}}},
      {"event": "content_block_delta", "data": {"delta": {"type": "thinking_delta", "thinking": "checking the step"}}},
      {"event": "content_block_delta", "data": {"delta": {"type": "input_json_delta", "partial_json": "{\"a\":1"}}},
      {"event": "ping", "data": {}},
      {"event": "message_stop", "data": {}},
   ]

   def fake_stream_transport(url, headers, body):
      assert body["stream"] is True
      return iter(events)

   provider = AnthropicProvider(
      stream_transport=fake_stream_transport,
      environ={"ANTHROPIC_API_KEY": "test-key-not-real"},
   )

   normalised = list(provider.stream(_request(role="tutor")))

   assert normalised == [
      {"type": "start", "role": "tutor", "model": "claude-sonnet-5", "request_id": "msg_123"},
      {"type": "text", "delta": "Which"},
      {"type": "reasoning", "delta": "checking the step"},
      {"type": "json", "delta": "{\"a\":1"},
      {"type": "end", "reason": None},
   ]


def test_stream_maps_an_error_event():
   events = [{"event": "error", "data": {"error": {"type": "overloaded_error", "message": "busy"}}}]

   def fake_stream_transport(url, headers, body):
      return iter(events)

   provider = AnthropicProvider(
      stream_transport=fake_stream_transport,
      environ={"ANTHROPIC_API_KEY": "test-key-not-real"},
   )

   normalised = list(provider.stream(_request()))

   assert normalised == [{"type": "error", "code": "overloaded_error", "retryable": True}]


def test_stream_error_retryable_matches_the_error_type():
   from app.providers.anthropic import _RETRYABLE_STREAM_ERROR_TYPES

   retryable_types = ("overloaded_error", "api_error", "rate_limit_error")
   non_retryable_types = (
      "invalid_request_error",
      "authentication_error",
      "permission_error",
      "not_found_error",
      "request_too_large",
   )

   assert set(_RETRYABLE_STREAM_ERROR_TYPES) == set(retryable_types)

   for error_type in retryable_types + non_retryable_types:
      events = [{"event": "error", "data": {"error": {"type": error_type, "message": "x"}}}]

      def fake_stream_transport(url, headers, body, events=events):
         return iter(events)

      provider = AnthropicProvider(
         stream_transport=fake_stream_transport,
         environ={"ANTHROPIC_API_KEY": "test-key-not-real"},
      )

      normalised = list(provider.stream(_request()))
      expected_retryable = error_type in retryable_types

      assert normalised == [{"type": "error", "code": error_type, "retryable": expected_retryable}]


def test_sse_parsing_splits_events_on_blank_lines_and_drops_unmapped_deltas():
   from app.providers.anthropic import _parse_sse_events

   raw_lines = [
      b"event: message_start\n",
      b"data: {\"message\": {\"model\": \"claude-sonnet-5\", \"id\": \"msg_1\"}}\n",
      b"\n",
      b"event: content_block_delta\n",
      b"data: {\"delta\": {\"type\": \"text_delta\", \"text\": \"hi\"}}\n",
      b"\n",
      b"event: ping\n",
      b"data: {}\n",
      b"\n",
      b"event: message_stop\n",
      b"data: {}\n",
      b"\n",
   ]

   events = list(_parse_sse_events(raw_lines))

   assert events == [
      {"event": "message_start", "data": {"message": {"model": "claude-sonnet-5", "id": "msg_1"}}},
      {"event": "content_block_delta", "data": {"delta": {"type": "text_delta", "text": "hi"}}},
      {"event": "ping", "data": {}},
      {"event": "message_stop", "data": {}},
   ]


def _plain_wire_body():
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)
   provider.generate(_request(output_schema={"type": "object"}))

   return transport.calls[0]["body"]


SAMPLING_KEYS_THE_ROUTED_MODELS_REJECT = ("temperature", "top_p", "top_k")
REFUSED_OPTION_KEYS = tuple(
   sorted(set(_plain_wire_body()) - {"output_config"}) + list(SAMPLING_KEYS_THE_ROUTED_MODELS_REJECT)
) + ("metadata",)


@pytest.mark.parametrize("option_key", REFUSED_OPTION_KEYS)
def test_an_option_key_outside_the_allowlist_never_reaches_the_wire(option_key):
   """13 line 20: temperature, top_p and top_k are a 400 on every routed model. Every key the
   adapter builds itself would let a caller override it: model runs a model the guard did not
   price, max_tokens escapes the guard's reservation."""
   plain_body = _plain_wire_body()
   override_value = plain_body.get(option_key, 1)
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   with pytest.raises(ValueError):
      provider.generate(_request(provider_options={option_key: override_value}))

   assert transport.calls == []


@pytest.mark.parametrize(
   "provider_options",
   [
      {"thinking": {"type": "disabled", "budget_tokens": 1024}},
      {"thinking": "disabled"},
      {"output_config": {"format": {"type": "json_schema", "schema": {}}}},
      {"output_config": {"effort": "low", "strict": False}},
      {"output_config": "low"},
   ],
)
def test_an_allowed_option_key_with_an_unnamed_value_shape_is_refused(provider_options):
   """07 line 145 and 13 line 60 name thinking {"type": "disabled"} and output_config.effort.
   Anything else under those keys, such as a budget or a format replacing the schema, is refused."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   with pytest.raises(ValueError):
      provider.generate(_request(output_schema={"type": "object"}, provider_options=provider_options))

   assert transport.calls == []


def _locals_holding(traceback_obj, secret):
   offending = []

   while traceback_obj is not None:
      frame = traceback_obj.tb_frame

      for local_name, local_value in frame.f_locals.items():
         local_text = repr(local_value)

         if secret in local_text:
            offending.append((frame.f_code.co_filename, frame.f_code.co_name, local_name))

      traceback_obj = traceback_obj.tb_next

   return offending


def _chained_exceptions(exception):
   seen = []
   pending = [exception]

   while pending:
      current = pending.pop()
      already_seen = any(current is known for known in seen)

      if current is None or already_seen:
         continue

      seen.append(current)
      pending.append(current.__cause__)
      pending.append(current.__context__)

   return seen


def _escaping_exception(call):
   try:
      call()
   except BaseException as escaped:
      return escaped

   raise AssertionError("the call was expected to raise")


@pytest.mark.parametrize("call_shape", ["generate", "stream"])
def test_an_exception_escaping_the_real_transport_holds_the_key_in_no_frame(monkeypatch, call_shape):
   """13 item 8: no traceback renderer that prints locals may print the key. The opener raises
   inside the real default transport, and every frame of the escaping exception and of its
   whole chain is searched by repr."""
   secret = "sk-ant-do-not-print-this-value-anywhere"

   def _raising_opener(request, *args, **kwargs):
      raise urllib.error.URLError("network is down")

   monkeypatch.setattr(anthropic, "open_without_redirects", _raising_opener)
   provider = AnthropicProvider(environ={"ANTHROPIC_API_KEY": secret})
   request = _request()

   def _call():
      if call_shape == "generate":
         provider.generate(request)
      else:
         list(provider.stream(request))

   escaped = _escaping_exception(_call)
   offending = []

   for exception in _chained_exceptions(escaped):
      offending.extend(_locals_holding(exception.__traceback__, secret))

   retained_attributes = [name for name, value in vars(provider).items() if secret in repr(value)]

   assert offending == []
   assert retained_attributes == []
   assert isinstance(escaped, ProviderTransportError)
   assert secret not in str(escaped)


def _anthropic_stream_events():
   return [
      {"event": "message_start", "data": {"message": {
         "model": "claude-sonnet-5",
         "id": "msg_usage",
         "usage": {
            "input_tokens": 1200,
            "output_tokens": 1,
            "cache_read_input_tokens": 1024,
            "cache_creation_input_tokens": 0,
         },
      }}},
      {"event": "content_block_delta", "data": {"delta": {"type": "text_delta", "text": "Which rule?"}}},
      {"event": "message_delta", "data": {"delta": {"stop_reason": "end_turn"}, "usage": {"output_tokens": 40}}},
      {"event": "message_stop", "data": {}},
   ]


def _streaming_provider(events):
   def fake_stream_transport(url, headers, body):
      return iter(events)

   return AnthropicProvider(
      stream_transport=fake_stream_transport,
      environ={"ANTHROPIC_API_KEY": "test-key-not-real"},
   )


def test_stream_emits_the_usage_event_and_the_reported_stop_reason():
   """06 line 481 names the usage event; message_start carries input and cache usage and
   message_delta carries the cumulative output count and the stop reason."""
   provider = _streaming_provider(_anthropic_stream_events())

   normalised = list(provider.stream(_request()))

   assert normalised[-2:] == [
      {"type": "usage", "input": 1200, "output": 40, "cached_read": 1024, "cached_write": 0},
      {"type": "end", "reason": "end_turn"},
   ]


def test_a_stream_through_the_guard_settles_the_reported_usage():
   """The guard settles from the value the adapter's generator returns. Without it the row
   keeps an estimate rather than the 1200 in and 40 out the provider reported."""
   engine = create_engine("sqlite:///:memory:")
   models.Base.metadata.create_all(engine)
   db = SqlSession(engine)
   guard = GuardedProvider(
      _streaming_provider(_anthropic_stream_events()),
      db,
      user_id="USR-1",
      clock=lambda: datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc),
      caps={"tutor": BudgetCaps(cap_usd=1000.0)},
      provider_name="anthropic",
   )

   list(guard.stream(_request(max_output_tokens=600)))

   row = db.execute(select(models.Budget.__table__)).mappings().one()

   assert row["tokens_in"] == 1200
   assert row["tokens_out"] == 40
   assert row["tokens_cached_read"] == 1024
   assert guard.last_accounting is not None


@pytest.mark.parametrize(
   "opus_5_model_id",
   ["claude-opus-5", "claude-opus-5-20260901", "claude-opus-5-latest"],
)
def test_the_opus_5_effort_rule_matches_the_model_family(opus_5_model_id):
   """07 line 145: 'The adapter selects the thinking form by model family'."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   with pytest.raises(ValueError):
      provider.generate(_request(
         model=opus_5_model_id,
         provider_options={"thinking": {"type": "disabled"}, "output_config": {"effort": "xhigh"}},
      ))

   assert transport.calls == []


def test_a_model_outside_the_opus_5_family_is_not_held_to_its_effort_rule():
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   provider.generate(_request(
      model="claude-opus-50",
      provider_options={"thinking": {"type": "disabled"}, "output_config": {"effort": "xhigh"}},
   ))

   assert transport.calls[0]["body"]["thinking"] == {"type": "disabled"}


REFUSAL_SECRET = "sk-ant-refused-before-the-wire-value"


def _raising_opener_for(error):
   def _raising_opener(request, *args, **kwargs):
      raise error

   return _raising_opener


def _refusal_cases():
   return {
      "unnamed option": dict(provider_options={"temperature": 0.3}),
      "thinking shape": dict(provider_options={"thinking": {"type": "enabled"}}),
      "effort level": dict(provider_options={"output_config": {"effort": "ultra"}}),
      "opus 5 effort": dict(
         model="claude-opus-5",
         provider_options={"thinking": {"type": "disabled"}, "output_config": {"effort": "max"}},
      ),
      "forbidden tools": dict(provider_options={"tools": [{"name": "lookup"}]}),
   }


@pytest.mark.parametrize("call_shape", ["generate", "stream"])
@pytest.mark.parametrize("case_name", sorted(_refusal_cases()))
def test_a_request_refused_by_validation_never_left(case_name, call_shape):
   """13 item 3: the refund path is reserved for a call that never left."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response, environ={"ANTHROPIC_API_KEY": REFUSAL_SECRET})
   request = _request(**_refusal_cases()[case_name])

   def _call():
      if call_shape == "generate":
         provider.generate(request)
      else:
         list(provider.stream(request))

   escaped = _escaping_exception(_call)

   assert isinstance(escaped, RefusedBeforeWire)
   assert isinstance(escaped, ValueError)
   assert REFUSAL_SECRET not in str(escaped)
   assert transport.calls == []


@pytest.mark.parametrize("call_shape", ["generate", "stream"])
def test_a_missing_key_never_left(call_shape):
   provider = AnthropicProvider(environ={})

   def _call():
      if call_shape == "generate":
         provider.generate(_request())
      else:
         list(provider.stream(_request()))

   escaped = _escaping_exception(_call)

   assert isinstance(escaped, RefusedBeforeWire)


def _connection_failures():
   return {
      "connection refused": urllib.error.URLError(ConnectionRefusedError(61, "Connection refused")),
      "name did not resolve": urllib.error.URLError(socket.gaierror(8, "nodename nor servname provided")),
   }


def _failures_after_the_request_may_have_left():
   return {
      "timeout": urllib.error.URLError(TimeoutError("timed out")),
      "socket timeout": urllib.error.URLError(socket.timeout("timed out")),
      "http error": urllib.error.HTTPError(MESSAGES_URL, 500, REFUSAL_SECRET, {}, None),
      "reset": ConnectionResetError(54, "Connection reset by peer"),
   }


@pytest.mark.parametrize("call_shape", ["generate", "stream"])
@pytest.mark.parametrize("failure_name", sorted(_connection_failures()))
def test_a_connection_that_was_never_established_never_left(monkeypatch, failure_name, call_shape):
   monkeypatch.setattr(anthropic, "open_without_redirects", _raising_opener_for(_connection_failures()[failure_name]))
   provider = AnthropicProvider(environ={"ANTHROPIC_API_KEY": REFUSAL_SECRET})

   def _call():
      if call_shape == "generate":
         provider.generate(_request())
      else:
         list(provider.stream(_request()))

   escaped = _escaping_exception(_call)

   assert isinstance(escaped, RefusedBeforeWire)
   assert isinstance(escaped, ProviderTransportError)
   assert REFUSAL_SECRET not in str(escaped)


@pytest.mark.parametrize("call_shape", ["generate", "stream"])
@pytest.mark.parametrize("failure_name", sorted(_failures_after_the_request_may_have_left()))
def test_a_failure_after_the_request_may_have_left_is_not_a_refusal(monkeypatch, failure_name, call_shape):
   failure = _failures_after_the_request_may_have_left()[failure_name]
   monkeypatch.setattr(anthropic, "open_without_redirects", _raising_opener_for(failure))
   provider = AnthropicProvider(environ={"ANTHROPIC_API_KEY": REFUSAL_SECRET})

   def _call():
      if call_shape == "generate":
         provider.generate(_request())
      else:
         list(provider.stream(_request()))

   escaped = _escaping_exception(_call)

   assert isinstance(escaped, ProviderTransportError)
   assert not isinstance(escaped, RefusedBeforeWire)
   assert REFUSAL_SECRET not in str(escaped)


def test_a_refused_connection_after_the_stream_started_is_not_a_refusal():
   """Once an event has arrived the request left, whatever the later error says."""
   def fake_stream_transport(url, headers, body):
      yield {"event": "message_start", "data": {"message": {"model": "claude-sonnet-5", "id": "msg_1"}}}
      raise urllib.error.URLError(ConnectionRefusedError(61, "Connection refused"))

   provider = AnthropicProvider(
      stream_transport=fake_stream_transport,
      environ={"ANTHROPIC_API_KEY": "test-key-not-real"},
   )

   escaped = _escaping_exception(lambda: list(provider.stream(_request())))

   assert isinstance(escaped, ProviderTransportError)
   assert not isinstance(escaped, RefusedBeforeWire)


REDIRECT_SECRET = "sk-ant-must-never-reach-a-redirect-target"


class _RecordingHandler(http.server.BaseHTTPRequestHandler):
   def log_message(self, *args):
      return None

   def _record(self):
      length = int(self.headers.get("content-length") or 0)
      body = self.rfile.read(length) if length else b""
      headers = {name.lower(): value for name, value in self.headers.items()}
      self.server.seen.append({"method": self.command, "headers": headers, "body": body})


class _RedirectingHandler(_RecordingHandler):
   def do_POST(self):
      self._record()
      self.send_response(302)
      self.send_header("Location", self.server.redirect_to)
      self.send_header("Content-Length", "0")
      self.end_headers()


class _AnsweringHandler(_RecordingHandler):
   def _answer(self):
      self._record()
      payload = json.dumps({
         "content": [{"type": "text", "text": "answered by the redirect target"}],
         "stop_reason": "end_turn",
         "usage": {},
      }).encode("utf-8")
      self.send_response(200)
      self.send_header("Content-Type", "application/json")
      self.send_header("Content-Length", str(len(payload)))
      self.end_headers()
      self.wfile.write(payload)

   do_GET = _answer
   do_POST = _answer


def _local_server(handler):
   server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
   server.seen = []
   thread = threading.Thread(target=server.serve_forever, daemon=True)
   thread.start()

   return server


@pytest.mark.parametrize("call_shape", ["generate", "stream"])
def test_the_real_transport_never_follows_a_redirect_with_the_key(call_shape):
   """07's key handling sends the key to the provider and nowhere else. urllib follows a 302 on a
   POST and copies the x-api-key header to the new host, so a redirect is refused and not
   followed. A redirect is an answer from a server, so it is not a refusal before the wire."""
   target = _local_server(_AnsweringHandler)
   redirector = _local_server(_RedirectingHandler)
   redirector.redirect_to = f"http://127.0.0.1:{target.server_address[1]}/v1/messages"
   provider = AnthropicProvider(
      base_url=f"http://127.0.0.1:{redirector.server_address[1]}/v1/messages",
      environ={"ANTHROPIC_API_KEY": REDIRECT_SECRET},
   )

   def _call():
      if call_shape == "generate":
         provider.generate(_request())
      else:
         list(provider.stream(_request()))

   try:
      escaped = _escaping_exception(_call)
   finally:
      redirector.shutdown()
      target.shutdown()

   assert len(redirector.seen) == 1
   assert redirector.seen[0]["headers"].get("x-api-key") == REDIRECT_SECRET
   assert target.seen == []
   assert isinstance(escaped, ProviderTransportError)
   assert not isinstance(escaped, RefusedBeforeWire)
   assert REDIRECT_SECRET not in str(escaped)
   assert REDIRECT_SECRET not in repr(escaped)
   assert escaped.__cause__ is None
   assert escaped.__suppress_context__


def _drain_stream(generator):
   while True:
      try:
         next(generator)
      except StopIteration as finished:
         return finished.value


def test_result_names_finish_reason():
   """07 line 51, the normalised result shape: 'finish_reason'. Anthropic's wire field is
   stop_reason, and the adapter renames it on the way out of both call shapes."""
   from dataclasses import fields

   from app.providers.base import ProviderResult

   result_field_names = {field.name for field in fields(ProviderResult)}

   assert "finish_reason" in result_field_names
   assert "stop_reason" not in result_field_names

   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, _transport = _provider(response)
   generated = provider.generate(_request())
   streamed = _drain_stream(_streaming_provider(_anthropic_stream_events()).stream(_request()))

   assert generated.finish_reason == "end_turn"
   assert streamed.finish_reason == "end_turn"


def test_a_cassette_carrying_stop_reason_instead_of_finish_reason_is_refused():
   from app.providers.replay import ReplayProvider

   stale_cassette = {"text": "ok", "stop_reason": "end_turn", "usage": {}}

   with pytest.raises(ValueError):
      ReplayProvider(cassette=stale_cassette)


def test_every_committed_cassette_replays_its_finish_reason():
   from pathlib import Path

   from app.providers.replay import ReplayProvider

   cassette_dir = Path(__file__).resolve().parents[1] / "fixtures" / "provider_cassettes"
   cassette_paths = sorted(cassette_dir.glob("*.json"))

   assert cassette_paths

   for cassette_path in cassette_paths:
      recorded = json.loads(cassette_path.read_text())
      result = ReplayProvider(cassette_path=cassette_path).generate(_request())

      assert "stop_reason" not in recorded
      assert result.finish_reason == recorded["finish_reason"]


HAIKU_4_5_MODEL_IDS = ["claude-haiku-4-5", "claude-haiku-4-5-20251001"]


@pytest.mark.parametrize("haiku_model_id", HAIKU_4_5_MODEL_IDS)
def test_effort_is_refused_on_haiku_4_5(haiku_model_id):
   """07 Known traps: output_config.effort 'is not supported on Haiku 4.5'."""
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   with pytest.raises(anthropic.RefusedOption):
      provider.generate(_request(model=haiku_model_id, provider_options={"output_config": {"effort": "low"}}))

   assert transport.calls == []


@pytest.mark.parametrize("haiku_model_id", HAIKU_4_5_MODEL_IDS)
def test_haiku_4_5_without_effort_reaches_the_wire(haiku_model_id):
   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)

   provider.generate(_request(model=haiku_model_id))

   assert transport.calls[0]["body"]["model"] == haiku_model_id
   assert "output_config" not in transport.calls[0]["body"]


def test_an_image_reaches_the_wire_as_a_base64_block_before_the_text():
   """The transcriber's photograph goes as an image content block on the last user message
   (https://platform.claude.com/docs/en/build-with-claude/vision), never inside the prompt text."""
   import base64

   from app.providers.base import ImageInput

   response = {"content": [{"type": "text", "text": "ok"}], "stop_reason": "end_turn", "usage": {}}
   provider, transport = _provider(response)
   page = ImageInput(media_type="image/jpeg", data=b"jpeg bytes", width=10, height=10)

   provider.generate(_request(images=(page,)))

   content = transport.calls[0]["body"]["messages"][-1]["content"]

   assert [block["type"] for block in content] == ["image", "text"]
   assert content[0]["source"]["media_type"] == "image/jpeg"
   assert base64.b64decode(content[0]["source"]["data"]) == b"jpeg bytes"
   assert content[1]["text"] == "I am stuck on step two."
