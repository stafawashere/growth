"""What GET /settings/providers reports: per role, what the running composition wires.

P1 wires one role, the tutor on the model app/feedback/tutor.py sends, and only when a tutor
provider is configured (docs/plan/07-ai-provider-layer.md, "Roles and routing"). Every other role
is reported unwired with no provider and no model, because nothing in this process would answer
it. No key material and no sign of whether a key exists is read here.
"""
from app.feedback.tutor import TUTOR_MODEL
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import ROLES
from app.providers.replay import ReplayProvider

PROVIDER_NAMES = {
   AnthropicProvider: "anthropic",
   ReplayProvider: "replay",
}


def provider_name_of(provider):
   for provider_class, name in PROVIDER_NAMES.items():
      if isinstance(provider, provider_class):
         return name

   return type(provider).__name__


def unwired(role):
   return {"role": role, "provider": None, "model": None, "wired": False}


def role_entry(role, settings):
   is_tutor = role == "tutor"
   has_tutor = settings.tutor is not None
   is_wired = is_tutor and has_tutor

   if not is_wired:
      return unwired(role)

   return {"role": role, "provider": provider_name_of(settings.tutor), "model": TUTOR_MODEL, "wired": True}


def providers_view(settings):
   return {"roles": [role_entry(role, settings) for role in ROLES]}
