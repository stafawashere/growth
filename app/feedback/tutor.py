"""The tutor writes the sentence that carries the deterministically selected feedback (R35).

docs/plan/03-diagnosis-and-feedback.md, "Who composes the string in P1": the application picks
the violated step, the observed behavior and scoring consequence of the option's BC-ERR record,
and the item's stored worked solution, and passes exactly those four fields into
prompts/feedback/elaborated_v1.md. Nothing else about the item reaches the model, and no call is
made before the student has submitted.
"""
from pathlib import Path

from app.providers.base import (
   CacheSettings,
   Message,
   ProviderRequest,
   render_template,
   split_template,
)
from app.providers.guard import BudgetStopped

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "prompts" / "feedback" / "elaborated_v1.md"
TUTOR_MODEL = "claude-sonnet-5"
MAX_OUTPUT_TOKENS = 400
PREFIX_CACHE_TTL = "1h"


def template_text():
   return TEMPLATE_PATH.read_text()


def request_for(fields):
   text = template_text()
   system, _variable_section = split_template(text)
   rendered = render_template(text, fields)

   return ProviderRequest(
      role="tutor",
      model=TUTOR_MODEL,
      system=system,
      messages=[Message(role="user", content=rendered)],
      max_output_tokens=MAX_OUTPUT_TOKENS,
      cache=CacheSettings(prefix_breakpoints=1, ttl=PREFIX_CACHE_TTL),
   )


def compose_sentence(provider, feedback, db=None, attempt=None):
   """The selected payload becomes one paragraph. No provider means no sentence, not an error.

   With a session and an attempt row the sentence is cached on the attempt, so re-reading the
   feedback screen returns the wording the student already saw and spends no second tutor call
   against the role's daily cap. The write is flushed and not committed: the caller owns the
   transaction. An empty or blank sentence is a provider that said nothing, so it is not stored
   and the next read composes again.

   A budget stop is not a provider failure and is not swallowed. 07's hard-stop table says the
   student is told the tutor is unavailable for the rest of today, so the caller has to be able
   to tell a cap from a model that merely returned nothing.
   """
   caches = db is not None and attempt is not None

   if caches:
      stored = attempt.tutor_sentence
      has_stored_sentence = stored is not None and stored.strip() != ""

      if has_stored_sentence:
         return stored

   has_provider = provider is not None
   payload = feedback.elaborated
   has_payload = payload is not None
   composes = has_provider and has_payload

   if not composes:
      return None

   try:
      result = provider.generate(request_for(payload.as_prompt_fields()))
   except BudgetStopped:
      raise
   except Exception:
      return None

   sentence = result.text
   has_sentence = sentence is not None and sentence.strip() != ""

   if not has_sentence:
      return None

   if caches:
      attempt.tutor_sentence = sentence
      db.add(attempt)
      db.flush()

   return sentence
