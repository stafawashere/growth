"""Maps the neutral shape in app/providers/base.py onto the Anthropic Messages wire body.

docs/plan/07-ai-provider-layer.md, Anthropic adapter section and Known traps: the system
block carries the cache_control breakpoint, no tool definitions are ever sent on a tutor
call, and thinking is never requested because sending thinking: {type: "enabled"} to
Sonnet 5 or Opus 5 returns 400 and this project has no use for the adaptive form either.
No temperature is sent either: a non-default temperature, top_p or top_k returns 400 on
every request to Opus 5 and Sonnet 5, so the wire body carries none and the neutral request
shape has no such field.

The wire call sits behind an injectable transport callable so every test drives a fake
transport and no test opens a socket. The only real transport uses urllib.request from the
standard library, since 06-architecture.md names no HTTP client dependency.
"""
import json
import os
import urllib.request

from app.providers.base import Provider, ProviderResult, Usage

MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

_FORBIDDEN_PROVIDER_OPTION_KEYS = ("tools", "tool_choice", "thinking")


def default_transport(url, headers, body):
   payload = json.dumps(body).encode("utf-8")
   request = urllib.request.Request(url, data=payload, headers=headers, method="POST")

   with urllib.request.urlopen(request) as response:
      return json.loads(response.read().decode("utf-8"))


class AnthropicProvider(Provider):
   def __init__(self, api_key_env="ANTHROPIC_API_KEY", base_url=MESSAGES_URL, transport=None, environ=None):
      self._api_key_env = api_key_env
      self._base_url = base_url
      self._transport = transport if transport is not None else default_transport
      self._environ = environ if environ is not None else os.environ

   def generate(self, request):
      body = self._wire_body(request, stream=False)
      response = self._transport(self._base_url, self._headers(), body)

      return self._to_result(request, response)

   def stream(self, request):
      body = self._wire_body(request, stream=True)
      response = self._transport(self._base_url, self._headers(), body)
      result = self._to_result(request, response)

      if result.text:
         yield result.text

      return result

   def _headers(self):
      api_key = self._environ.get(self._api_key_env)
      has_key = api_key is not None and api_key != ""

      if not has_key:
         raise RuntimeError(f"{self._api_key_env} is not set")

      return {
         "x-api-key": api_key,
         "anthropic-version": ANTHROPIC_VERSION,
         "content-type": "application/json",
      }

   def _wire_body(self, request, stream):
      _guard_provider_options(request.provider_options)

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

      if request.output_schema is not None:
         body["output_config"] = {"format": {"type": "json_schema", "schema": request.output_schema}, "strict": True}

      return body

   def _to_result(self, request, response):
      blocks = response.get("content", [])
      text_blocks = [block.get("text", "") for block in blocks if block.get("type") == "text"]
      text = "".join(text_blocks) if text_blocks else None

      raw_usage = response.get("usage", {})
      usage = Usage(
         input_tokens=raw_usage.get("input_tokens"),
         output_tokens=raw_usage.get("output_tokens"),
         cached_read_tokens=raw_usage.get("cache_read_input_tokens"),
         cached_write_tokens=raw_usage.get("cache_creation_input_tokens"),
         reasoning_tokens=None,
      )

      return ProviderResult(
         text=text,
         stop_reason=response.get("stop_reason"),
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
      raise ValueError(f"the tutor call may never carry {present}, the adapter refuses to forward them")
