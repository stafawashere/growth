"""Provider-neutral call and result shapes (docs/plan/07-ai-provider-layer.md, Provider abstraction).

Every number in usage is present or null, never omitted, because a null usage field is a
provider that does not report and a zero is a real zero, and the two mean different things
to the cache hit rate metric.

This module also holds the versioned prompt template contract that docs/plan/11-phased-delivery.md
P1 scope item 13 asks for: a template file carries a stable static prefix, a marker, then a
variable section that names the only fields a caller may substitute. render_template refuses
an unknown field and a missing one, so no rendering path can smuggle a field the template never
declared into a rendered prompt.
"""
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

PROMPT_MARKER = "<!-- prompt-variables -->"

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


@dataclass(frozen=True)
class Message:
   role: str
   content: str


@dataclass(frozen=True)
class CacheSettings:
   prefix_breakpoints: int = 1
   ttl: str = "5m"


@dataclass(frozen=True)
class ProviderRequest:
   role: str
   model: str
   system: str
   messages: tuple
   max_output_tokens: int
   temperature: float = 0.0
   output_schema: dict | None = None
   stream: bool = False
   cache: CacheSettings | None = None
   provider_options: dict | None = None
   idempotency_key: str | None = None
   correlation_id: str | None = None


@dataclass(frozen=True)
class Usage:
   input_tokens: int | None
   output_tokens: int | None
   cached_read_tokens: int | None
   cached_write_tokens: int | None
   reasoning_tokens: int | None = None


@dataclass(frozen=True)
class ProviderResult:
   text: str | None
   stop_reason: str | None
   usage: Usage
   provider: str
   model: str
   request_id: str | None = None
   raw_usage: dict | None = None


class Provider(ABC):
   """The seam every caller goes through. No caller builds a wire request directly."""

   @abstractmethod
   def generate(self, request: ProviderRequest) -> ProviderResult:
      raise NotImplementedError

   @abstractmethod
   def stream(self, request: ProviderRequest):
      raise NotImplementedError


def split_template(text):
   has_marker = PROMPT_MARKER in text

   if not has_marker:
      raise ValueError(f"template is missing the stable marker {PROMPT_MARKER!r}")

   prefix, _marker, variable_section = text.partition(PROMPT_MARKER)

   return prefix, variable_section


def template_placeholders(text):
   return set(_PLACEHOLDER_RE.findall(text))


def render_template(text, fields):
   _prefix, variable_section = split_template(text)

   declared = template_placeholders(variable_section)
   given = set(fields)

   has_unknown_field = not given <= declared
   has_missing_field = not declared <= given

   if has_unknown_field:
      raise ValueError(f"unknown template fields: {sorted(given - declared)}")

   if has_missing_field:
      raise ValueError(f"missing template fields: {sorted(declared - given)}")

   def _substitute(match):
      return str(fields[match.group(1)])

   return _PLACEHOLDER_RE.sub(_substitute, variable_section)
