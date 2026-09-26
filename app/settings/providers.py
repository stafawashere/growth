"""What GET /settings/providers reports: per role, what the running composition wires.

P1 wires one role, the tutor on the model app/feedback/tutor.py sends, and only when a tutor
provider is configured (docs/plan/07-ai-provider-layer.md, "Roles and routing"). Every other role
is reported unwired with no provider and no model, because nothing in this process would answer
it. No key material and no sign of whether a key exists is read here.
"""
from app.auth.service import utc_now
from app.feedback.tutor import TUTOR_MODEL
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import ROLES
from app.providers.replay import ReplayProvider
from app.providers.router import links_from_settings
from app.providers.subscription import SubscriptionProvider

PROVIDER_NAMES = {
   AnthropicProvider: "anthropic",
   ReplayProvider: "replay",
   SubscriptionProvider: "subscription",
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


def chain_names(settings, links_field, provider_field):
   return [link.name for link in links_from_settings(settings, links_field, provider_field)]


def providers_view(settings, now=None):
   """roles as before; chains is each role group's fallback order, and cooling every link that is
   on cooldown now (app/providers/router.py)."""
   board = settings.provider_cooldowns

   return {
      "roles": [role_entry(role, settings) for role in ROLES],
      "chains": {
         "tutor": chain_names(settings, "tutor_links", "tutor"),
         "grading": chain_names(settings, "ai_links", "ai_provider"),
      },
      "cooling": board.snapshot(now or utc_now()),
   }
