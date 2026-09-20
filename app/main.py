"""The ASGI entrypoint uvicorn serves as app.main:application.

docs/plan/11-phased-delivery.md P1 scope items 1, 12 and 14: this is the composition root that
builds a real Settings and SessionContext from the live library, rather than the fixture double
tests/api/conftest.py wires. Building it makes no network call: the database is a local SQLite
file, the content root is read off local disk, the passkey verifier only binds a library, and the
tutor provider (P1 scope item 12, docs/plan/07-ai-provider-layer.md's one wired role) is only
constructed, never called, so building it never dials out either way.

Environment variables, every one optional with a loopback-safe default:

GROWTH_DB_PATH        path to the SQLite database file. Default var/growth.db under the repo root.
GROWTH_CONTENT_ROOT   path to the data/ registries. Default data/ under the repo root.
GROWTH_RP_ID          the WebAuthn relying party id. Default localhost.
GROWTH_ORIGIN         the deployment origin passkey ceremonies are verified against.
                      Default http://127.0.0.1:8000.
GROWTH_BIND_HOST      the host uvicorn binds to. Default 127.0.0.1.
GROWTH_EXAM_DATE      the ISO exam date new users are seeded with. Default 2027-05-10.
GROWTH_RNG_SEED       the seed for the process-wide selection rng. Default 7.
GROWTH_TUTOR_PROVIDER which provider backs the tutor role: none (the default), replay or
                      anthropic. anthropic also needs ANTHROPIC_API_KEY in the same environment,
                      and a key without this variable wires nothing, so a billed role is never
                      wired by the accident of a key sitting in the environment. With no tutor
                      app/feedback/tutor.py returns the deterministic payload and no sentence.
                      replay reads GROWTH_TUTOR_CASSETTE. Neither replay nor anthropic makes a
                      call at build time; the provider object is only constructed.
GROWTH_TUTOR_CASSETTE path to a recorded cassette JSON file, read only when
                      GROWTH_TUTOR_PROVIDER=replay.
GROWTH_TUTOR_CAP_USD  the tutor role's daily dollar cap, enforced by app/providers/guard.py
                      before every call. Default 1.00. docs/plan/07-ai-provider-layer.md sets no
                      number, so the default is inferred and is a tunable for 12-open-questions.
GROWTH_TUTOR_CAP_TOKENS the tutor role's daily token cap. Unset by default, because 07 keeps both
                      units and the dollar cap is the one the operator cares about; a number here
                      binds as well, whichever is crossed first.
"""
import os
from pathlib import Path

from app.api.app import Settings, create_app
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import BudgetCaps
from app.providers.replay import ReplayProvider
from app.runtime.context import build_session_context

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "var" / "growth.db"
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"
DEFAULT_TUTOR_CAP_USD = 1.00


def build_tutor(env):
   """P1 scope item 12: the tutor is the one wired role, and the deployment opts into it by name.

   docs/plan/07-ai-provider-layer.md puts the budget guard, the usage accounting and the audit
   trail at the provider seam, and app/providers/guard.py now holds all three, so the role is safe
   to turn on. Opting in stays explicit anyway, because a key in the environment is not a decision
   to spend. Without GROWTH_TUTOR_PROVIDER there is no tutor, and app/feedback/tutor.py's
   no-provider degradation returns the deterministic payload with no sentence.
   """
   provider_name = env.get("GROWTH_TUTOR_PROVIDER", "none")

   if provider_name == "none":
      return None

   if provider_name == "replay":
      cassette_path = env.get("GROWTH_TUTOR_CASSETTE")
      has_cassette = cassette_path is not None and cassette_path != ""

      if not has_cassette:
         return None

      return ReplayProvider(cassette_path=cassette_path)

   api_key = env.get("ANTHROPIC_API_KEY")
   has_key = api_key is not None and api_key != ""

   if not has_key:
      return None

   return AnthropicProvider(environ=env)


def build_tutor_caps(env):
   """A guard with no cap guards nothing, so the tutor role always carries one.

   docs/plan/07-ai-provider-layer.md names the daily cap in both tokens and dollars but sets no
   number for either, so the dollar default here is inferred and the token cap stays unset until
   the operator names one.
   """
   raw_tokens = env.get("GROWTH_TUTOR_CAP_TOKENS")
   names_a_token_cap = raw_tokens is not None and raw_tokens != ""
   cap_tokens = float(raw_tokens) if names_a_token_cap else None
   cap_usd = float(env.get("GROWTH_TUTOR_CAP_USD", str(DEFAULT_TUTOR_CAP_USD)))

   return {"tutor": BudgetCaps(cap_tokens=cap_tokens, cap_usd=cap_usd)}


def settings_from_environment(env=None):
   env = env if env is not None else os.environ

   return Settings(
      db_path=Path(env.get("GROWTH_DB_PATH", str(DEFAULT_DB_PATH))),
      content_root=Path(env.get("GROWTH_CONTENT_ROOT", str(DEFAULT_CONTENT_ROOT))),
      rp_id=env.get("GROWTH_RP_ID", "localhost"),
      origin=env.get("GROWTH_ORIGIN", "http://127.0.0.1:8000"),
      bind_host=env.get("GROWTH_BIND_HOST", "127.0.0.1"),
      exam_date=env.get("GROWTH_EXAM_DATE", "2027-05-10"),
      rng_seed=int(env.get("GROWTH_RNG_SEED", "7")),
      tutor=build_tutor(env),
      tutor_caps=build_tutor_caps(env),
   )


def build_application(env=None):
   settings = settings_from_environment(env)
   settings.db_path.parent.mkdir(parents=True, exist_ok=True)
   engine = settings.resolve_engine()
   settings.session_context = build_session_context(engine, settings.content_root)

   return create_app(settings)


application = build_application()
