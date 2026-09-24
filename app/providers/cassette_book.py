"""A book of recorded calls keyed by what was asked, for roles that make many different calls.

ReplayProvider plays one cassette for every request, which suits the tutor's single template. The
grader, the transcriber and the diagnostician make a different call per point, per page and per
attempt, so their recordings are a JSON object from request_digest to the recorded result. The
digest covers the role, the model, the system prompt, every message, the output schema and the
sha256 of every image, and the sample label, so the grader's two standard samples of one point
are two recordings rather than one answer played twice. A changed template, rubric or photograph
misses the book instead of replaying an answer to a different question.

A book is recorded once by a tool that wraps a live provider (tools/record_grading_cassettes.py
over the operator's subscription) and replayed by tests, which never reach a provider.
"""
import hashlib
import json
import threading
from pathlib import Path

from app.providers.base import Provider, ProviderResult, Usage


class CassetteMiss(LookupError):
   """The book holds no recording for this request. The message names the digest and the role."""


def image_digest(image):
   return hashlib.sha256(image.data).hexdigest()


def request_digest(request):
   described = {
      "role": request.role,
      "model": request.model,
      "system": request.system,
      "messages": [[message.role, message.content] for message in request.messages],
      "output_schema": request.output_schema,
      "images": [image_digest(image) for image in request.images],
      "sample_label": request.sample_label,
   }
   canonical = json.dumps(described, sort_keys=True, separators=(",", ":"))

   return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def recorded_entry(result):
   usage = result.usage

   return {
      "text": result.text,
      "finish_reason": result.finish_reason,
      "provider": result.provider,
      "model": result.model,
      "usage": {
         "input_tokens": usage.input_tokens,
         "output_tokens": usage.output_tokens,
         "cached_read_tokens": usage.cached_read_tokens,
         "cached_write_tokens": usage.cached_write_tokens,
      },
   }


def result_from_entry(entry, request):
   usage_block = entry.get("usage") or {}

   return ProviderResult(
      text=entry.get("text"),
      finish_reason=entry.get("finish_reason"),
      usage=Usage(
         input_tokens=usage_block.get("input_tokens"),
         output_tokens=usage_block.get("output_tokens"),
         cached_read_tokens=usage_block.get("cached_read_tokens"),
         cached_write_tokens=usage_block.get("cached_write_tokens"),
      ),
      provider=entry.get("provider", "replay"),
      model=entry.get("model", request.model),
      raw_usage=dict(usage_block),
   )


def read_book(path):
   book_path = Path(path)

   if not book_path.is_file():
      return {}

   return json.loads(book_path.read_text())


class CassetteBookProvider(Provider):
   """Replays from a book. With a live provider and record=True it calls the live provider on a
   miss, stores the answer and saves the book after every call, so an interrupted recording keeps
   what it already paid for."""

   name = "cassette_book"

   def __init__(self, path=None, book=None, live=None, record=False):
      self._path = Path(path) if path is not None else None
      self._book = dict(book) if book is not None else read_book(path) if path is not None else {}
      self._live = live
      self._record = bool(record) and live is not None
      self.calls = []
      self._lock = threading.Lock()

   @property
   def book(self):
      return self._book

   def generate(self, request):
      digest = request_digest(request)
      self.calls.append((request.role, digest))
      entry = self._book.get(digest)
      has_entry = entry is not None

      if has_entry:
         return result_from_entry(entry, request)

      if not self._record:
         raise CassetteMiss(f"no recorded {request.role} call for digest {digest}")

      result = self._live.generate(request)

      with self._lock:
         self._book[digest] = recorded_entry(result)
         self.save()

      return result

   def stream(self, request):
      result = self.generate(request)

      if result.text:
         yield {"type": "text", "delta": result.text}

      return result

   def save(self):
      has_path = self._path is not None

      if not has_path:
         return

      self._path.parent.mkdir(parents=True, exist_ok=True)
      self._path.write_text(json.dumps(self._book, indent=1, sort_keys=True) + "\n")
