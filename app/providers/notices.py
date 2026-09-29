"""Short notices telling a signed-in student each time the app talked to an AI model.

GuardedProvider (app/providers/guard.py) is the one seam every model call passes through, so it is
where a notice is recorded: one per call outcome, for the user the guard was built for. A notice
names the role, the provider and model, the outcome, a brief of what was asked and a brief of what
came back.

The asked brief is built per role from the template fields the caller filled in, recovered from
the rendered message against the variable section of the role's template, never from the prompt
text itself, whose first characters are template boilerplate. A structured answer is summarised
from its fields rather than shown. No brief carries image bytes, a key, a template or the student's
full work, and each is cut to BRIEF_LIMIT characters.

Notices live in a bounded per-user buffer in this process and are never written to the database.
Recording one must never change a call, so every entry point here swallows its own failures.
"""
import json
import re
import threading
from collections import deque
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path

from app.providers.base import PROMPT_MARKER

BRIEF_LIMIT = 160
NOTICES_PER_USER = 50
ELLIPSIS = "..."

ANSWERED = "answered"
FAILED = "failed"
REFUSED = "refused"
STOPPED = "stopped"
INTERRUPTED = "interrupted"
QUEUED = "queued"

REPLAY_MARKERS = ("replay", "cassette")

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")
_PART_ID_RE = re.compile(r"part \(([^)]*)\)")
_WHITESPACE_RE = re.compile(r"\s+")


class NoticeBoard:
   """Per-user notices for the life of the process, oldest dropped past NOTICES_PER_USER. Ids rise
   across every user, so a client asks for what is newer than the last id it saw."""

   def __init__(self, per_user=NOTICES_PER_USER):
      self._per_user = per_user
      self._lock = threading.Lock()
      self._next_id = 1
      self._by_user = {}

   def record(self, user_id, fields):
      with self._lock:
         notice = dict(fields, id=self._next_id)
         self._next_id = self._next_id + 1
         held = self._by_user.get(user_id)

         if held is None:
            held = deque(maxlen=self._per_user)
            self._by_user[user_id] = held

         held.append(notice)

         return notice

   def since(self, user_id, after_id):
      with self._lock:
         held = self._by_user.get(user_id, ())

         return [dict(notice) for notice in held if notice["id"] > after_id]

   def forget(self, user_id):
      with self._lock:
         self._by_user.pop(user_id, None)

   def reset(self):
      with self._lock:
         self._next_id = 1
         self._by_user = {}


BOARD = NoticeBoard()


def reset_notices():
   BOARD.reset()


def clipped(text, limit=BRIEF_LIMIT):
   """One line, at most limit characters, cut at a word where one is near."""
   flat = _WHITESPACE_RE.sub(" ", str(text or "")).strip()

   if len(flat) <= limit:
      return flat

   room = limit - len(ELLIPSIS)
   cut = flat[:room]
   last_space = cut.rfind(" ")
   has_word_break = last_space > room // 2

   if has_word_break:
      cut = cut[:last_space]

   return cut.rstrip(" ,;:.") + ELLIPSIS


def _role_templates(role):
   """The template files each runtime role renders, read from the callers' own constants so this
   module never names a template path twice. Imported here, at call time, because the callers
   import the provider package."""
   if role == "tutor":
      from app.feedback import tutor

      return (tutor.TEMPLATE_PATH,)

   if role == "grader":
      from app.grading import judge

      return (judge.STANDARD_TEMPLATE, judge.STRICT_TEMPLATE)

   if role == "transcriber":
      from app.grading import transcribe

      return (transcribe.TEMPLATE_PATH,)

   if role == "diagnostician":
      from app.diagnosis import observe

      return (observe.TEMPLATE_PATH,)

   return ()


@lru_cache(maxsize=16)
def _variable_pieces(path):
   """The variable section as alternating literal text and field names."""
   text = Path(path).read_text()
   _prefix, marker, section = text.partition(PROMPT_MARKER)

   if marker == "":
      return None

   return tuple(_PLACEHOLDER_RE.split(section))


def fields_from_rendered(pieces, rendered):
   """The fields a caller filled in, recovered by walking the literal text between placeholders
   left to right. Linear in the message length: no regular expression runs over student text."""
   literals = pieces[0::2]
   names = pieces[1::2]
   starts_right = rendered.startswith(literals[0])

   if not starts_right:
      return None

   position = len(literals[0])
   fields = {}

   for index, name in enumerate(names):
      following = literals[index + 1]
      is_last = index == len(names) - 1

      if is_last:
         ends_right = rendered.endswith(following) and len(rendered) - len(following) >= position

         if not ends_right:
            return None

         end = len(rendered) - len(following)
      else:
         end = rendered.find(following, position) if following != "" else position

         if end < 0:
            return None

      fields[name] = rendered[position:end]
      position = end + len(following)

   return fields


def supplied_fields(request):
   messages = tuple(request.messages or ())

   if not messages:
      return None

   rendered = messages[-1].content

   for path in _role_templates(request.role):
      pieces = _variable_pieces(str(path))

      if pieces is None:
         continue

      fields = fields_from_rendered(pieces, rendered)

      if fields is not None:
         return fields

   return None


def _field(fields, name):
   return _WHITESPACE_RE.sub(" ", str(fields.get(name) or "")).strip()


def _count_lines(text):
   lines = [line for line in str(text or "").splitlines() if line.strip() != ""]
   says_none = len(lines) == 1 and lines[0].strip() == "(none)"

   if says_none:
      return 0

   return len(lines)


def _plural(count, word):
   return f"{count} {word}" if count == 1 else f"{count} {word}s"


def asked_brief(request):
   role = request.role
   fields = supplied_fields(request) or {}

   if role == "tutor":
      step = _field(fields, "violated_step")

      if step:
         return clipped(f"Asked the tutor to explain the step you missed: {step}")

      return clipped("Asked the tutor for a feedback sentence on your answer.")

   if role == "grader":
      point_name = _field(fields, "point_type_name")
      part_id = _field(fields, "part_id")

      if point_name and part_id:
         return clipped(f"Asked whether your work on part ({part_id}) earns the point for {point_name}.")

      return clipped("Asked whether your work earns one scoring point.")

   if role == "transcriber":
      pages = _plural(len(request.images or ()), "photographed page")
      question = _field(fields, "question_label")
      part_ids = _PART_ID_RE.findall(str(fields.get("part_labels") or ""))

      if question and part_ids:
         parts = ", ".join(part_ids)

         return clipped(f"Asked to read {pages} for question {question}, parts {parts}.")

      return clipped(f"Asked to read {pages} of your work.")

   if role == "diagnostician":
      has_points_lost = "points_lost" in fields

      if has_points_lost:
         lost = _plural(_count_lines(fields["points_lost"]), "point")

         return clipped(f"Asked what might explain the {lost} you lost on this question.")

      return clipped("Asked what might explain the points you lost.")

   return clipped(f"Asked the {role} model for help.")


def _structured(result_text):
   try:
      payload = json.loads(result_text or "")
   except ValueError:
      return None

   is_object = isinstance(payload, dict)

   return payload if is_object else None


def _list_of(payload, key):
   value = payload.get(key)

   return value if isinstance(value, list) else []


def _structured_brief(role, payload):
   if role == "grader":
      decision = payload.get("decision")
      rule_field = payload.get("rule_field")
      verdicts = {"earned": "Judged the point earned", "not_earned": "Judged the point not earned"}
      verdict = verdicts.get(decision)

      if verdict is None:
         return "Returned a grading with no clear decision."

      has_rule = isinstance(rule_field, str) and rule_field.strip() != ""

      if has_rule:
         return f"{verdict}, citing the {rule_field.replace('_', ' ')} rule."

      return f"{verdict}."

   if role == "transcriber":
      parts = _plural(len(_list_of(payload, "parts")), "part")
      unreadable = len(_list_of(payload, "unreadable"))

      if unreadable:
         return f"Returned a transcription of {parts}, with {unreadable} marked unreadable."

      return f"Returned a transcription of {parts}."

   if role == "diagnostician":
      errors = _plural(len(_list_of(payload, "observed_errors")), "possible error")
      signals = _plural(len(_list_of(payload, "matched_signals")), "matched signal")
      readings = _plural(len(_list_of(payload, "skill_readings")), "skill reading")

      return f"Named {errors}, {signals} and {readings}."

   names = ", ".join(sorted(str(key) for key in payload))

   return f"Returned a structured answer with fields: {names}."


def answered_brief(request, result):
   text = getattr(result, "text", None)
   is_blank = text is None or str(text).strip() == ""

   if is_blank:
      return "Returned no text."

   payload = _structured(text)
   expects_structure = request.output_schema is not None

   if payload is not None:
      return clipped(_structured_brief(request.role, payload))

   if expects_structure:
      return "Returned an answer that could not be read as the expected structure."

   return clipped(text)


def _humanised(name):
   return str(name or "").replace("_", " ").strip()


def outcome_of(raised):
   """The outcome and the brief of what came back, for a call that raised. The exception classes
   are imported here so this module can be imported by the guard without a cycle."""
   from app.providers.base import RefusedBeforeWire
   from app.providers.guard import BudgetStopped, DevSpendCapExceeded, ProviderCallFailed
   from app.providers.subscription import SubscriptionAuthFailed

   if isinstance(raised, GeneratorExit):
      return INTERRUPTED, "The answer stream was closed before it finished."

   if isinstance(raised, BudgetStopped):
      caps = _humanised(getattr(raised, "cap", "")) or "usage"

      return STOPPED, clipped(f"Nothing was sent: the {raised.role} {caps} limit was reached.")

   if isinstance(raised, DevSpendCapExceeded):
      return STOPPED, "Nothing was sent: the developer spend cap was reached."

   if isinstance(raised, RefusedBeforeWire):
      kind = getattr(raised, "exception_type", type(raised).__name__)

      return REFUSED, clipped(f"Nothing was sent: the model could not take the call ({kind}).")

   is_sign_in_failure = getattr(raised, "exception_type", type(raised).__name__) == SubscriptionAuthFailed.__name__

   if is_sign_in_failure:
      return FAILED, clipped("Nothing came back: the Claude sign-in expired, so the model is unavailable until it is renewed.")

   if isinstance(raised, ProviderCallFailed):
      return FAILED, clipped(f"Nothing came back: the call failed ({raised.exception_type}).")

   return FAILED, clipped(f"Nothing came back: the app could not make the call ({type(raised).__name__}).")


def _is_replay(provider_name):
   lowered = str(provider_name or "").lower()

   return any(marker in lowered for marker in REPLAY_MARKERS)


def _now_iso(clock):
   try:
      moment = clock()
   except Exception:
      moment = datetime.now(timezone.utc)

   return moment.isoformat()


def record_call(user_id, provider_name, request, result=None, raised=None, clock=None):
   """Called by the guard once a call has an outcome. Returns the notice, or None when none was
   recorded. Never raises."""
   try:
      has_user = user_id is not None

      if not has_user:
         return None

      if raised is None:
         outcome = ANSWERED
         answered = answered_brief(request, result)
      else:
         outcome, answered = outcome_of(raised)

      result_model = getattr(result, "model", None)

      return BOARD.record(user_id, {
         "role": request.role,
         "provider": str(provider_name),
         "model": str(result_model or request.model),
         "outcome": outcome,
         "replayed": _is_replay(provider_name),
         "asked": asked_brief(request),
         "answered": answered,
         "created_at": _now_iso(clock or _utc_now),
      })
   except Exception:
      return None


def record_queued(user_id, request, reason, clock=None):
   """A call deferred by a limit, recorded when its job is first queued. Never raises."""
   try:
      has_user = user_id is not None

      if not has_user:
         return None

      because = _humanised(reason) or "a limit"

      return BOARD.record(user_id, {
         "role": request.role,
         "provider": "queue",
         "model": str(request.model),
         "outcome": QUEUED,
         "replayed": False,
         "asked": asked_brief(request),
         "answered": clipped(f"Nothing came back yet: the call was saved to try later ({because})."),
         "created_at": _now_iso(clock or _utc_now),
      })
   except Exception:
      return None


def notices_for(user_id, after_id):
   return BOARD.since(user_id, after_id)


def _utc_now():
   return datetime.now(timezone.utc)
