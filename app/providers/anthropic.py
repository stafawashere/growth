"""Maps the neutral shape in app/providers/base.py onto the Anthropic Messages wire body.

docs/plan/07-ai-provider-layer.md, Anthropic adapter section and Known traps: the system
block carries the cache_control breakpoint, no tool definitions are ever sent on a tutor
call, and manual thinking: {type: "enabled"} is never sent because it returns 400 on Opus 5
and Sonnet 5. 13-ai-engineering.md corrects the older reading: thinking is already on by
default on those models and needs no configuration, and turning it off takes an explicit
thinking: {"type": "disabled"}, which Sonnet 5 accepts at any effort and Opus 5 accepts only
at effort high or below. No temperature is sent either: a non-default temperature, top_p or
top_k returns 400 on every request to Opus 5 and Sonnet 5, so the wire body carries none and
the neutral request shape has no such field.

provider_options is opaque to the router (07, the normalised result shape), but the adapter
does not forward it blindly. Every key the adapter builds itself (model, max_tokens, system,
messages, stream) would let a caller run a model the budget guard never priced or escape the
guard's output reservation, and temperature, top_p and top_k are a 400 on every routed model
(13, line 20). So the adapter forwards only what a plan line names: thinking of exactly
{"type": "disabled"} (07 Known traps, 13 'tutor, kept') and output_config carrying effort alone,
at one of the five levels 07 names. Everything else is refused before the wire.

A transport failure leaves the adapter as a ProviderTransportError that carries the original
exception type and nothing else, raised outside the except block and with no chain, so no frame
that held the request headers survives in the traceback (13, item 8).

A failure that provably never reached the provider is a RefusedBeforeWire (base.py), which the
guard may refund (13, item 3): an option refused by validation, a missing key, and a URLError whose
reason is a refused connection or a name that did not resolve. A timeout, an HTTP error, or any
failure after the first stream event may have left, and stays a plain ProviderTransportError. So
does a redirect, which the real transports refuse to follow: a server answered, and following it
would send the key to a host that is not the provider, which 07's key handling never allows.

The wire call sits behind an injectable transport callable so every test drives a fake
transport. The only real transports use urllib.request from the standard library, since
06-architecture.md names no HTTP client dependency, through an opener that refuses redirects.

Streaming maps Anthropic's SSE events onto the normalised event vocabulary in
06-architecture.md (the "Normalising provider streams" section): text_delta to text,
thinking_delta to reasoning, input_json_delta to json, ping dropped, message_start to start,
message_stop to a usage event and then end. message_start carries the input and cache counts
and message_delta the cumulative output count and the stop reason, which end carries. The
generator returns a ProviderResult so the budget guard settles what the provider reported.
Anthropic's wire field is stop_reason and 07's normalised result shape names it finish_reason,
so the rename happens here and nowhere downstream.
content_block_start, content_block_stop and signature_delta are outside the mapping and dropped.
"""
import json
import os
import socket
import urllib.error
import urllib.request

from app.providers.base import Provider, ProviderResult, RefusedBeforeWire, Usage

MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

class ProviderTransportError(RuntimeError):
   def __init__(self, exception_type):
      super().__init__(f"the Anthropic transport raised {exception_type}")
      self.exception_type = exception_type


class ConnectionNotEstablished(ProviderTransportError, RefusedBeforeWire):
   pass


class RefusedOption(RefusedBeforeWire, ValueError):
   pass


class MissingApiKey(RefusedBeforeWire, RuntimeError):
   pass


_CONNECTION_NEVER_ESTABLISHED_REASONS = (ConnectionRefusedError, socket.gaierror)


def _connection_was_never_established(raised):
   is_url_error = isinstance(raised, urllib.error.URLError)
   reason = getattr(raised, "reason", None)
   reason_proves_no_connection = isinstance(reason, _CONNECTION_NEVER_ESTABLISHED_REASONS)

   return is_url_error and reason_proves_no_connection


def _bounded_transport_error(failure_type, never_left):
   if never_left:
      return ConnectionNotEstablished(failure_type)

   return ProviderTransportError(failure_type)


_FORBIDDEN_PROVIDER_OPTION_KEYS = ("tools", "tool_choice")
_ALLOWED_PROVIDER_OPTION_KEYS = ("thinking", "output_config")
_DISABLED_THINKING = {"type": "disabled"}
_ALLOWED_OUTPUT_CONFIG_KEYS = ("effort",)

_EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
_EFFORT_RANK = {level: rank for rank, level in enumerate(_EFFORT_LEVELS)}
_OPUS_5_FAMILY = "claude-opus-5"
_OPUS_5_MAX_EFFORT_FOR_DISABLED_THINKING = "high"
_HAIKU_4_5_FAMILY = "claude-haiku-4-5"


class RedirectRefused(Exception):
   pass


class _RefuseRedirects(urllib.request.HTTPRedirectHandler):
   """urllib follows a redirect on a POST and copies every header but the body's to the new
   location, the key among them, and 07's key handling sends the key to the provider and nowhere
   else, so no redirect is followed. The reply is closed and named by its status alone."""

   def redirect_request(self, request, response, code, message, headers, new_url):
      response.close()

      raise RedirectRefused(f"the provider answered {code} and redirects are not followed")


_REDIRECT_REFUSING_OPENER = urllib.request.build_opener(_RefuseRedirects)


def open_without_redirects(request):
   return _REDIRECT_REFUSING_OPENER.open(request)


def default_transport(url, headers, body):
   payload = json.dumps(body).encode("utf-8")
   request = urllib.request.Request(url, data=payload, headers=headers, method="POST")

   with open_without_redirects(request) as response:
      return json.loads(response.read().decode("utf-8"))


def default_stream_transport(url, headers, body):
   payload = json.dumps(body).encode("utf-8")
   request = urllib.request.Request(url, data=payload, headers=headers, method="POST")

   with open_without_redirects(request) as response:
      yield from _parse_sse_events(response)


def _parse_sse_events(lines):
   event_name = None
   data_lines = []

   for raw_line in lines:
      line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
      line = line.rstrip("\r\n")
      is_blank_line = line == ""

      if is_blank_line:
         has_pending_event = event_name is not None or data_lines

         if has_pending_event:
            data_text = "\n".join(data_lines)
            data = json.loads(data_text) if data_text else {}
            yield {"event": event_name, "data": data}

         event_name = None
         data_lines = []
         continue

      if line.startswith("event:"):
         event_name = line[len("event:"):].strip()
         continue

      if line.startswith("data:"):
         data_lines.append(line[len("data:"):].strip())


class _StreamState:
   def __init__(self):
      self.raw_usage = {}
      self.finish_reason = None
      self.request_id = None
      self.text_parts = []

   def usage(self):
      return _usage_from_raw(self.raw_usage)


def _normalise_stream_event(request, provider_event, state):
   event_type = provider_event.get("event")
   data = provider_event.get("data") or {}

   if event_type == "message_start":
      message = data.get("message") or {}
      state.request_id = message.get("id")
      state.raw_usage.update(message.get("usage") or {})

      return [{
         "type": "start",
         "role": request.role,
         "model": message.get("model"),
         "request_id": message.get("id"),
      }]

   if event_type == "content_block_delta":
      normalised = _normalise_content_block_delta(data.get("delta") or {})

      if normalised is None:
         return []

      is_text = normalised["type"] == "text"

      if is_text:
         state.text_parts.append(normalised["delta"])

      return [normalised]

   if event_type == "message_delta":
      delta = data.get("delta") or {}
      state.finish_reason = delta.get("stop_reason", state.finish_reason)
      state.raw_usage.update(data.get("usage") or {})

      return []

   if event_type == "message_stop":
      return _closing_events(state)

   if event_type == "error":
      error = data.get("error") or {}

      return [{"type": "error", "code": error.get("type"), "retryable": False}]

   return []


def _closing_events(state):
   events = []
   usage_was_reported = len(state.raw_usage) > 0

   if usage_was_reported:
      usage = state.usage()
      events.append({
         "type": "usage",
         "input": usage.input_tokens,
         "output": usage.output_tokens,
         "cached_read": usage.cached_read_tokens,
         "cached_write": usage.cached_write_tokens,
      })

   events.append({"type": "end", "reason": state.finish_reason})

   return events


def _usage_from_raw(raw_usage):
   thinking_details = raw_usage.get("output_tokens_details")
   reasoning_tokens = thinking_details.get("thinking_tokens") if thinking_details is not None else None

   return Usage(
      input_tokens=raw_usage.get("input_tokens"),
      output_tokens=raw_usage.get("output_tokens"),
      cached_read_tokens=raw_usage.get("cache_read_input_tokens"),
      cached_write_tokens=raw_usage.get("cache_creation_input_tokens"),
      reasoning_tokens=reasoning_tokens,
   )


def _normalise_content_block_delta(delta):
   delta_type = delta.get("type")

   if delta_type == "text_delta":
      return {"type": "text", "delta": delta.get("text", "")}

   if delta_type == "thinking_delta":
      return {"type": "reasoning", "delta": delta.get("thinking", "")}

   if delta_type == "input_json_delta":
      return {"type": "json", "delta": delta.get("partial_json", "")}

   return None


_STREAM_EXHAUSTED = object()


def _api_key_reader(environ, api_key_env):
   """A closure rather than an attribute holding the mapping, so no attribute on the adapter
   has a repr that prints the key."""
   def read_api_key():
      return environ.get(api_key_env)

   return read_api_key


class AnthropicProvider(Provider):
   def __init__(
      self,
      api_key_env="ANTHROPIC_API_KEY",
      base_url=MESSAGES_URL,
      transport=None,
      stream_transport=None,
      environ=None,
   ):
      self._api_key_env = api_key_env
      self._base_url = base_url
      self._transport = transport if transport is not None else default_transport
      self._stream_transport = stream_transport if stream_transport is not None else default_stream_transport
      self._read_api_key = _api_key_reader(environ if environ is not None else os.environ, api_key_env)

   def generate(self, request):
      body = self._wire_body(request, stream=False)
      self._require_api_key()
      failure_type = None
      never_left = False

      try:
         response = self._transport(self._base_url, self._headers(), body)
      except Exception as raised:
         failure_type = type(raised).__name__
         never_left = _connection_was_never_established(raised)

      transport_failed = failure_type is not None

      if transport_failed:
         raise _bounded_transport_error(failure_type, never_left) from None

      return self._to_result(request, response)

   def stream(self, request):
      body = self._wire_body(request, stream=True)
      self._require_api_key()
      state = _StreamState()
      provider_events = self._open_stream(body)
      nothing_received = True

      while True:
         provider_event = self._next_provider_event(provider_events, nothing_received)
         nothing_received = False

         if provider_event is _STREAM_EXHAUSTED:
            break

         yield from _normalise_stream_event(request, provider_event, state)

      text = "".join(state.text_parts) if state.text_parts else None

      return ProviderResult(
         text=text,
         finish_reason=state.finish_reason,
         usage=state.usage(),
         provider="anthropic",
         model=request.model,
         request_id=state.request_id,
         raw_usage=dict(state.raw_usage),
      )

   def _open_stream(self, body):
      failure_type = None

      never_left = False

      try:
         provider_events = iter(self._stream_transport(self._base_url, self._headers(), body))
      except Exception as raised:
         failure_type = type(raised).__name__
         never_left = _connection_was_never_established(raised)

      transport_failed = failure_type is not None

      if transport_failed:
         raise _bounded_transport_error(failure_type, never_left) from None

      return provider_events

   def _next_provider_event(self, provider_events, nothing_received):
      """Once any event has arrived the request left, so only a failure before the first event
      can prove the connection was never established."""
      failure_type = None
      never_left = False

      try:
         provider_event = next(provider_events, _STREAM_EXHAUSTED)
      except Exception as raised:
         failure_type = type(raised).__name__
         never_left = nothing_received and _connection_was_never_established(raised)

      transport_failed = failure_type is not None

      if transport_failed:
         raise _bounded_transport_error(failure_type, never_left) from None

      return provider_event

   def _require_api_key(self):
      has_key = bool(self._read_api_key())

      if not has_key:
         raise MissingApiKey(f"{self._api_key_env} is not set")

   def _headers(self):
      return {
         "x-api-key": self._read_api_key(),
         "anthropic-version": ANTHROPIC_VERSION,
         "content-type": "application/json",
      }

   def _wire_body(self, request, stream):
      provider_options = request.provider_options or {}

      _guard_provider_options(provider_options)
      _guard_thinking_effort_for_model(request.model, provider_options)
      _guard_effort_supported_by_model(request.model, provider_options)

      system_block = {"type": "text", "text": request.system}

      if request.cache is not None:
         system_block["cache_control"] = {"type": "ephemeral", "ttl": request.cache.ttl}

      body = {
         "model": request.model,
         "max_tokens": request.max_output_tokens,
         "system": [system_block],
         "messages": [{"role": message.role, "content": message.content} for message in request.messages],
         "stream": stream,
      }

      output_config = {}

      if request.output_schema is not None:
         output_config["format"] = {"type": "json_schema", "schema": request.output_schema}
         output_config["strict"] = True

      effort = (provider_options.get("output_config") or {}).get("effort")

      if effort is not None:
         output_config["effort"] = effort

      if output_config:
         body["output_config"] = output_config

      thinking = provider_options.get("thinking")

      if thinking is not None:
         body["thinking"] = dict(thinking)

      return body

   def _to_result(self, request, response):
      blocks = response.get("content", [])
      text_blocks = [block.get("text", "") for block in blocks if block.get("type") == "text"]
      text = "".join(text_blocks) if text_blocks else None

      raw_usage = response.get("usage", {})
      usage = _usage_from_raw(raw_usage)

      return ProviderResult(
         text=text,
         finish_reason=response.get("stop_reason"),
         usage=usage,
         provider="anthropic",
         model=request.model,
         request_id=response.get("id"),
         raw_usage=raw_usage,
      )


def _guard_provider_options(provider_options):
   if not provider_options:
      return

   present = [key for key in _FORBIDDEN_PROVIDER_OPTION_KEYS if key in provider_options]
   has_forbidden_key = len(present) > 0

   if has_forbidden_key:
      raise RefusedOption(f"the tutor call may never carry {present}, the adapter refuses to forward them")

   unnamed_keys = sorted(set(provider_options) - set(_ALLOWED_PROVIDER_OPTION_KEYS))
   has_unnamed_key = len(unnamed_keys) > 0

   if has_unnamed_key:
      raise RefusedOption(
         f"provider_options {unnamed_keys} are refused before the wire; only "
         f"{_ALLOWED_PROVIDER_OPTION_KEYS} are named by the plan"
      )

   _guard_thinking_type(provider_options.get("thinking"))
   _guard_effort_level(provider_options.get("output_config"))


def _guard_thinking_type(thinking):
   if thinking is None:
      return

   is_disabled_thinking = thinking == _DISABLED_THINKING

   if not is_disabled_thinking:
      raise RefusedOption(
         f"thinking {thinking!r} is refused before the wire; sending "
         "thinking: {\"type\": \"enabled\"} to Opus 5 or Sonnet 5 returns 400 "
         "(docs/plan/07-ai-provider-layer.md, Known traps) and only "
         f"{_DISABLED_THINKING} is supported"
      )


def _guard_effort_level(output_config):
   if output_config is None:
      return

   is_mapping = isinstance(output_config, dict)
   unnamed_keys = sorted(set(output_config) - set(_ALLOWED_OUTPUT_CONFIG_KEYS)) if is_mapping else None
   is_effort_only = is_mapping and unnamed_keys == []

   if not is_effort_only:
      raise RefusedOption(
         f"output_config may carry only {_ALLOWED_OUTPUT_CONFIG_KEYS}; the format comes from "
         "output_schema and nothing else is named by the plan"
      )

   effort = output_config.get("effort")

   if effort is None:
      return

   is_named_level = effort in _EFFORT_LEVELS

   if not is_named_level:
      raise RefusedOption(
         f"effort {effort!r} is outside the five levels 07 names: {_EFFORT_LEVELS}"
      )


def _guard_thinking_effort_for_model(model, provider_options):
   thinking = provider_options.get("thinking")
   is_thinking_disabled = isinstance(thinking, dict) and thinking.get("type") == "disabled"

   if not is_thinking_disabled:
      return

   is_opus_5 = _is_opus_5_family(model)

   if not is_opus_5:
      return

   output_config = provider_options.get("output_config") or {}
   effort = output_config.get("effort", _OPUS_5_MAX_EFFORT_FOR_DISABLED_THINKING)
   effort_rank = _EFFORT_RANK[effort]
   max_allowed_rank = _EFFORT_RANK[_OPUS_5_MAX_EFFORT_FOR_DISABLED_THINKING]
   effort_too_high = effort_rank > max_allowed_rank

   if effort_too_high:
      raise RefusedOption(
         "Opus 5 accepts thinking: disabled only at effort high or below "
         "(docs/plan/13-ai-engineering.md, 'tutor, kept' / the Opus 5 thinking correction)"
      )


def _guard_effort_supported_by_model(model, provider_options):
   output_config = provider_options.get("output_config") or {}
   carries_effort = output_config.get("effort") is not None
   is_haiku_4_5 = _is_model_family(model, _HAIKU_4_5_FAMILY)
   effort_is_unsupported = carries_effort and is_haiku_4_5

   if effort_is_unsupported:
      raise RefusedOption(
         "output_config.effort is not supported on Haiku 4.5 "
         "(docs/plan/07-ai-provider-layer.md, Known traps)"
      )


def _is_opus_5_family(model):
   return _is_model_family(model, _OPUS_5_FAMILY)


def _is_model_family(model, family):
   """The plan names bare model ids such as claude-opus-5 and claude-haiku-4-5. A dated or
   aliased id in the same family extends it after a hyphen, so the family is that id alone or
   that id followed by a hyphen."""
   is_bare_id = model == family
   is_extended_id = model.startswith(family + "-")

   return is_bare_id or is_extended_id
