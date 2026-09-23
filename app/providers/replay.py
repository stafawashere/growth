"""A recorded-cassette player for the Anthropic adapter's wire shape.

docs/plan/07-ai-provider-layer.md names no cassette format, so this reads the same result
shape app/providers/anthropic.py already produces: text, finish_reason, usage with its four
token fields, provider and model. The cassettes themselves are recorded by the operator
against a live key and do not exist yet in this repository, so this player works from a
cassette dict passed in directly or read from a JSON file path, and every test in
tests/providers/ supplies its own small cassette rather than a recorded one.

Never opens a socket. There is no transport here for a request to reach.
"""
import json
from pathlib import Path

from app.providers.base import Provider, ProviderResult, Usage


class ReplayProvider(Provider):
   def __init__(self, cassette=None, cassette_path=None):
      has_cassette = cassette is not None
      has_path = cassette_path is not None

      if not has_cassette and not has_path:
         raise ValueError("ReplayProvider needs either a cassette dict or a cassette_path")

      self._cassette = cassette if has_cassette else _read_cassette(cassette_path)
      _refuse_stale_finish_reason_key(self._cassette)

   def generate(self, request):
      return self._to_result(request)

   def stream(self, request):
      result = self._to_result(request)

      if result.text:
         yield result.text

      return result

   def _to_result(self, request):
      cassette = self._cassette
      raw_usage = cassette.get("usage", {})

      usage = Usage(
         input_tokens=raw_usage.get("input_tokens"),
         output_tokens=raw_usage.get("output_tokens"),
         cached_read_tokens=raw_usage.get("cached_read_tokens"),
         cached_write_tokens=raw_usage.get("cached_write_tokens"),
         reasoning_tokens=raw_usage.get("reasoning_tokens"),
      )

      return ProviderResult(
         text=cassette.get("text"),
         finish_reason=cassette.get("finish_reason"),
         usage=usage,
         provider=cassette.get("provider", "anthropic"),
         model=cassette.get("model", request.model),
         request_id=cassette.get("request_id"),
         raw_usage=raw_usage,
      )


def _refuse_stale_finish_reason_key(cassette):
   """07's result shape names finish_reason. A cassette written under the older stop_reason key
   would otherwise replay a null finish reason with no error."""
   has_stale_key = "stop_reason" in cassette

   if has_stale_key:
      raise ValueError("cassette carries stop_reason; 07's result shape names it finish_reason")


def _read_cassette(cassette_path):
   path = Path(cassette_path)

   return json.loads(path.read_text())
