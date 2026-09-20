"""The ASGI entrypoint uvicorn serves as app.main:application.

docs/plan/11-phased-delivery.md P1 scope items 1, 12 and 14: this is the composition root that
builds a real Settings and SessionContext from the live library, rather than the fixture double
tests/api/conftest.py wires. Building it makes no network call: the database is a local SQLite
file, the content root is read off local disk, and the passkey verifier only binds a library, it
never dials out.

Environment variables, every one optional with a loopback default:

GROWTH_DB_PATH       path to the SQLite database file. Default var/growth.db under the repo root.
GROWTH_CONTENT_ROOT  path to the data/ registries. Default data/ under the repo root.
GROWTH_RP_ID         the WebAuthn relying party id. Default localhost.
GROWTH_ORIGIN        the deployment origin passkey ceremonies are verified against.
                     Default http://127.0.0.1:8000.
GROWTH_BIND_HOST     the host uvicorn binds to. Default 127.0.0.1.
GROWTH_EXAM_DATE     the ISO exam date new users are seeded with. Default 2027-05-10.
GROWTH_RNG_SEED      the seed for the process-wide selection rng. Default 7.
"""
import os
from pathlib import Path

from app.api.app import Settings, create_app
from app.runtime.context import build_session_context

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "var" / "growth.db"
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"


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
   )


def build_application(env=None):
   settings = settings_from_environment(env)
   settings.db_path.parent.mkdir(parents=True, exist_ok=True)
   engine = settings.resolve_engine()
   settings.session_context = build_session_context(engine, settings.content_root)

   return create_app(settings)


application = build_application()
