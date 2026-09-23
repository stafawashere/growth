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
                      before every call. Default 1.00, the tutor daily cap row of
                      docs/plan/12-open-questions.md.
GROWTH_TUTOR_CAP_TOKENS the tutor role's daily token cap. Default 250,000, the same row of 12,
                      set by 13-ai-engineering.md so the two caps bind within a few calls of each
                      other. Whichever is crossed first binds.
GROWTH_TOKENS_PATH    path to a filled design-token file (the shape
                      docs/operator/design-tokens.template.json fixes). Ruled 2026-09-23:
                      unset by default, defaults to app/design/growth-tokens.json, the file
                      the implementer authored under entry criterion 5, so GET /growth-tokens.css
                      serves real tokens out of the box. Set this to override it with another
                      file; GET /growth-tokens.css answers 404 only when the configured or
                      default file is unreadable or fails app/design/css.py's checks. The path
                      is read again on every request, never cached at build time, so a changed
                      file or a newly set path is served without a restart.
GROWTH_KEY_AUDIT_SAMPLE_PATH path to the key-audit sample file tools/draw_key_audit_sample.py
                      writes (docs/operator/key-audit.md). Unset by default, in which case
                      POST /review-queue/{id}/resolve refuses every item_audit verdict rather
                      than guess at a sample. Read once and cached on the Settings object, since
                      the sample is drawn once per audit round rather than per request.
GROWTH_ITEMS_DIR      the directory of item records the bank ingests through app/items/ingest.py
                      on its first query, skipping ids already in the items table. Unset, it is
                      content/items_p1_agent under the repo root when that directory exists (the
                      agent drafts the operator ruled servable on 2026-09-23; their provenance
                      model is their authored_by, never operator), and no directory otherwise.
                      none disables it. A set path that is not a directory stops the process at
                      startup.

This module also mounts the built React client (app/web/dist, docs/plan/06-architecture.md's
system diagram: the browser speaks REST to one FastAPI process) at the same origin the API
answers on, which is what lets app/web/src/api/client.ts issue relative paths. Every route
create_app registers is added to the application before the client mount, and Starlette tries
routes in registration order, so none of them is ever shadowed by the client's static files.

The client mount answers exactly two shapes of request: a real file under app/web/dist/assets,
and GET / for index.html. It is not a catch-all. app/web/src/App.tsx routes screens with
useState, never a URL path, so nothing in the client needs a path served past "/", and giving
every unmatched GET path a 200 of index.html would also have made GET /export and GET /purge
(both POST-only) answer 200 with HTML instead of the 405 Starlette already gives a path that
matches a route by shape but not by method. An unmatched path now falls straight through to
Starlette's own 404 or 405, exactly as it would if this module mounted nothing at all.

`application`, the object uvicorn resolves from `app.main:application`, is built lazily on first
attribute access rather than at import time. Importing this module only defines functions; it
opens no database and reads no content root, which matters because tests import build_application
and mount_client directly and must never touch the repository's own var/growth.db as a side
effect of that import.
"""
import os
from pathlib import Path

from fastapi import Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, PlainTextResponse

from app.api.app import Settings, create_app
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import BudgetCaps
from app.providers.replay import ReplayProvider
from app.runtime.context import build_session_context
from app.settings.budgets import validated_cap

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "var" / "growth.db"
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"
DEFAULT_TUTOR_CAP_USD = 1.00
DEFAULT_TUTOR_CAP_TOKENS = 250000
DEFAULT_WEB_DIST_DIR = REPO_ROOT / "app" / "web" / "dist"
DEFAULT_TOKENS_PATH = REPO_ROOT / "app" / "design" / "growth-tokens.json"
DEFAULT_ITEMS_DIR = REPO_ROOT / "content" / "items_p1_agent"
NO_ITEMS_DIR = "none"
WEB_BUILD_COMMAND = "npm run build --prefix app/web"


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


def startup_cap(env, variable, default=None):
   """One rule for a cap wherever it comes from, so the environment cannot set one that
   PUT /settings/budgets would refuse: a finite number, not negative. The error names the
   variable, because it stops the process at startup."""
   named_value = env.get(variable)
   is_unset = named_value is None or named_value == ""
   raw_value = default if is_unset else named_value

   if raw_value is None:
      return None

   try:
      return validated_cap(variable, float(raw_value))
   except ValueError as refused:
      raise ValueError(f"{variable} must be a finite, non-negative number, got {raw_value!r}") from refused


def build_tutor_caps(env):
   """A guard with no cap guards nothing, so the tutor role always carries one.

   docs/plan/07-ai-provider-layer.md names the daily cap in both tokens and dollars, and the
   tutor daily cap row of docs/plan/12-open-questions.md sets both defaults.
   """
   cap_tokens = startup_cap(env, "GROWTH_TUTOR_CAP_TOKENS", str(DEFAULT_TUTOR_CAP_TOKENS))
   cap_usd = startup_cap(env, "GROWTH_TUTOR_CAP_USD", str(DEFAULT_TUTOR_CAP_USD))

   return {"tutor": BudgetCaps(cap_tokens=cap_tokens, cap_usd=cap_usd)}


def items_directory(env):
   configured = env.get("GROWTH_ITEMS_DIR")
   is_unset = configured is None or configured == ""

   if is_unset:
      has_default = DEFAULT_ITEMS_DIR.is_dir()

      return DEFAULT_ITEMS_DIR if has_default else None

   if configured == NO_ITEMS_DIR:
      return None

   configured_path = Path(configured)
   is_a_directory = configured_path.is_dir()

   if not is_a_directory:
      raise ValueError(f"GROWTH_ITEMS_DIR must name a directory of item records, got {configured!r}")

   return configured_path


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
      key_audit_sample_path=env.get("GROWTH_KEY_AUDIT_SAMPLE_PATH"),
      items_directory=items_directory(env),
   )


def _tokens_css_response(env):
   """Ruled 2026-09-23: an unset GROWTH_TOKENS_PATH defaults to the repository's own checked-in
   token file (DEFAULT_TOKENS_PATH) rather than 404ing, so the served page carries real colour,
   type and spacing tokens out of the box; an explicitly set but unreadable or malformed path
   still 404s, which is what lets an operator override with a bad path notice the mistake."""
   configured_path = env.get("GROWTH_TOKENS_PATH")
   is_configured = configured_path is not None and configured_path != ""
   tokens_path = configured_path if is_configured else str(DEFAULT_TOKENS_PATH)

   from app.design.css import stylesheet_from_token_file

   try:
      stylesheet = stylesheet_from_token_file(tokens_path)
   except Exception:
      return Response(status_code=404)

   return Response(content=stylesheet, media_type="text/css")


def mount_client(application, env, dist_dir=DEFAULT_WEB_DIST_DIR):
   """Serves the operator's token stylesheet and the built React client from the same
   application, added after every router create_app already registered so none of those routes
   is ever shadowed.

   env is kept as a live reference, not read once here, because GROWTH_TOKENS_PATH is meant to
   bind on the next request rather than freeze at build time (checklist 7).

   Only two paths are ever claimed here: a real file under dist_dir/assets, served through
   Starlette's own StaticFiles, whose lookup_path already rejects an absolute path and anything
   that resolves outside the mounted directory; and GET / for index.html. Nothing else is
   registered, so a path that is not one of those two, including one that merely looks like an
   API path, falls straight through to Starlette's own routing: a 405 when some other route
   matches its shape but not its method, a plain 404 otherwise. A catch-all here would instead
   intercept both, because Starlette's router treats an unconditional path match as full even
   when an earlier route only partially matched on method.
   """
   dist_dir = Path(dist_dir)
   index_path = dist_dir / "index.html"
   assets_dir = dist_dir / "assets"

   @application.get("/growth-tokens.css")
   def growth_tokens_css():
      return _tokens_css_response(env)

   if assets_dir.is_dir():
      application.mount("/assets", StaticFiles(directory=str(assets_dir)), name="web-assets")

   @application.get("/")
   def serve_client_index():
      dist_is_built = index_path.is_file()

      if not dist_is_built:
         message = "the client is not built; run {0} to produce {1}".format(
            WEB_BUILD_COMMAND, dist_dir
         )

         return PlainTextResponse(message, status_code=404)

      return FileResponse(index_path)

   return application


def build_application(env=None):
   env = env if env is not None else os.environ
   settings = settings_from_environment(env)
   settings.db_path.parent.mkdir(parents=True, exist_ok=True)
   engine = settings.resolve_engine()
   settings.session_context = build_session_context(
      engine, settings.content_root, items_directory=settings.items_directory
   )

   application = create_app(settings)
   mount_client(application, env)

   return application


_application = None


def __getattr__(name):
   """PEP 562 lazy module attribute: `uvicorn app.main:application` resolves this module then
   reads its `application` attribute, and that attribute access is the only thing allowed to
   build the real application. A plain `import app.main`, or `from app.main import
   build_application`, must never open var/growth.db as a side effect, because tests import
   this module's functions constantly and must stay free to build against a tmp_path instead.
   """
   global _application

   if name != "application":
      raise AttributeError("module {0!r} has no attribute {1!r}".format(__name__, name))

   if _application is None:
      _application = build_application()

   return _application
