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
GROWTH_AI_BACKEND     the primary switch for what backs the AI roles, the tutor included:
                      subscription (the default), api, replay or none. subscription runs the
                      official Claude Code CLI headless on the operator's own Claude subscription
                      (app/providers/subscription.py), so runtime calls are not billed to an API
                      key. It refuses to start when the database holds more than one user
                      account. api wires app/providers/anthropic.py AnthropicProvider and is the
                      only value that ever uses ANTHROPIC_API_KEY, which is a fallback chosen
                      explicitly and never picked up because it happens to be set. api without
                      a key wires no tutor. replay reads GROWTH_TUTOR_CASSETTE. none wires no tutor,
                      and app/feedback/tutor.py returns the deterministic payload with no
                      sentence. No backend makes a call at build time, and the choice is logged.
GROWTH_TUTOR_PROVIDER the older switch: none or replay, read only when GROWTH_AI_BACKEND is
                      unset. Its old value anthropic stops the process at startup unless
                      GROWTH_AI_BACKEND=api is also set, because the paid API is used only
                      when GROWTH_AI_BACKEND says so.
GROWTH_TUTOR_CASSETTE path to a recorded cassette JSON file, read only by the replay backend.
GROWTH_GRADING_CASSETTES path to a cassette book (app/providers/cassette_book.py) the replay
                      backend answers the transcriber, grader and diagnostician from. Unset, the
                      replay backend grades deterministic points only and leaves judged points
                      pending.
GROWTH_FRQ_DIR        the directory of free-response records. Default content/frq_items.
GROWTH_<ROLE>_CAP_USD and GROWTH_<ROLE>_CAP_TOKENS for grader, transcriber and diagnostician
                      the daily caps those roles carry on the api backend, where a role with no
                      cap is refused. Defaults in DEFAULT_GRADING_CAPS. The subscription backend
                      paces them by call counts instead.
GROWTH_CLAUDE_BIN     the claude CLI the subscription backend runs. Default the claude on PATH.
GROWTH_SUBSCRIPTION_<ROLE>_CALLS_PER_DAY and GROWTH_SUBSCRIPTION_CALLS_PER_MINUTE
                      the subscription backend's pacing guard (app/providers/guard.py
                      SubscriptionPacingCaps), which replaces the per-role dollar and token caps
                      for a role on the subscription. Defaults: tutor 60 calls a day, every other
                      role 20, and 4 calls a minute per role (docs/plan/14-token-economy.md,
                      "Subscription pacing"). Read only when the backend is subscription.
GROWTH_TUTOR_CAP_USD  the tutor role's daily dollar cap, enforced by app/providers/guard.py
                      before every call on the api backend (the subscription backend is paced
                      by call counts instead). Default 1.00, the tutor daily cap row of
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
GROWTH_ITEMS_DIR      the directories of item records the bank ingests through app/items/ingest.py
                      on its first query, skipping ids already in the items table, separated by
                      the platform path separator (":" on macOS and Linux). Unset, it is every
                      content/items_* directory under the repo root, in name order: the P1 bank
                      content/items_p1_agent and the per-unit banks content/items_unitNN_agent
                      (agent drafts the operator ruled servable on 2026-09-23 and signed off on
                      the operator's delegation; provenance model operator once signed off, their
                      authored_by before). none disables it. A set path that is not a directory
                      stops the process at startup, and an item id found in two directories stops
                      the first ingestion rather than serving whichever came first.
GROWTH_EXPERIMENTS_DEFAULT the state both A/B switches of app/experiments/switches.py start in
                      for a student: off, on or randomised. Unset, retrieval_entry starts
                      randomised and feedback_elaboration starts off (RUNNING_EXPERIMENT_DEFAULTS).
                      A switch the student has already set keeps its state.

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
import logging
import os
import sqlite3
from pathlib import Path

from fastapi import Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, PlainTextResponse

from app.api.app import Settings, create_app
from app.experiments import switches
from app.frq.bank import DEFAULT_FRQ_DIR, build_frq_context
from app.providers.anthropic import AnthropicProvider
from app.providers.cassette_book import CassetteBookProvider
from app.providers.guard import BudgetCaps, pacing_caps_from_environment
from app.providers.replay import ReplayProvider
from app.providers.subscription import SubscriptionProvider
from app.runtime.context import build_session_context
from app.settings.budgets import validated_cap

logger = logging.getLogger(__name__)

AI_BACKEND_ENV_VAR = "GROWTH_AI_BACKEND"
LEGACY_PROVIDER_ENV_VAR = "GROWTH_TUTOR_PROVIDER"
DEFAULT_AI_BACKEND = "subscription"
AI_BACKENDS = ("subscription", "api", "replay", "none")
LEGACY_PROVIDER_TO_BACKEND = {"none": "none", "replay": "replay"}
LEGACY_PAID_PROVIDER = "anthropic"
LEGACY_PAID_NAMES = (LEGACY_PAID_PROVIDER, "api")

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "var" / "growth.db"
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"
DEFAULT_TUTOR_CAP_USD = 1.00
DEFAULT_TUTOR_CAP_TOKENS = 250000
DEFAULT_WEB_DIST_DIR = REPO_ROOT / "app" / "web" / "dist"
DEFAULT_TOKENS_PATH = REPO_ROOT / "app" / "design" / "growth-tokens.json"
DEFAULT_CONTENT_DIR = REPO_ROOT / "content"
DEFAULT_ITEMS_DIR = DEFAULT_CONTENT_DIR / "items_p1_agent"
ITEM_BANK_PATTERN = "items_*"
NO_ITEMS_DIR = "none"
WEB_BUILD_COMMAND = "npm run build --prefix app/web"


def refuse_the_legacy_paid_switch(env, configured):
   """The operator's instruction of 2026-09-23: the paid API is used only when
   GROWTH_AI_BACKEND=api. The older GROWTH_TUTOR_PROVIDER=anthropic used to wire it on its own, and
   GROWTH_TUTOR_PROVIDER=api would pass straight through as the backend, so either one now stops
   the process unless GROWTH_AI_BACKEND=api says the same thing."""
   legacy = env.get(LEGACY_PROVIDER_ENV_VAR)
   names_the_paid_api = legacy in LEGACY_PAID_NAMES
   backend_is_api = configured == "api"
   is_refused = names_the_paid_api and not backend_is_api

   if is_refused:
      raise ValueError(
         f"{LEGACY_PROVIDER_ENV_VAR}={legacy} no longer turns on the paid Anthropic API by itself. "
         f"Set {AI_BACKEND_ENV_VAR}=api to use the API key, or remove {LEGACY_PROVIDER_ENV_VAR} to "
         f"run on the Claude subscription."
      )


def resolve_ai_backend(env):
   configured = env.get(AI_BACKEND_ENV_VAR)
   has_configured = configured is not None and configured != ""
   refuse_the_legacy_paid_switch(env, configured)

   if has_configured:
      logger.info("AI backend %s, from %s", configured, AI_BACKEND_ENV_VAR)

      return configured

   legacy = env.get(LEGACY_PROVIDER_ENV_VAR)
   has_legacy = legacy is not None and legacy != ""

   if has_legacy:
      backend = LEGACY_PROVIDER_TO_BACKEND.get(legacy, legacy)
      logger.info("AI backend %s, from %s=%s", backend, LEGACY_PROVIDER_ENV_VAR, legacy)

      return backend

   logger.info("AI backend %s, the default", DEFAULT_AI_BACKEND)

   return DEFAULT_AI_BACKEND


def installed_user_count(db_path):
   """Read-only, and never creates the database file: a first start sees zero users."""
   path = Path(db_path)

   if not path.is_file():
      return 0

   connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)

   try:
      return connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
   except sqlite3.OperationalError:
      return 0
   finally:
      connection.close()


def build_tutor(env):
   """P1 scope item 12: the tutor is the one wired role, and the deployment opts into a backend
   by name (resolve_ai_backend).

   docs/plan/07-ai-provider-layer.md puts the budget guard, the usage accounting and the audit
   trail at the provider seam, and app/providers/guard.py now holds all three, so the role is safe
   to turn on. Opting in stays explicit anyway, because a key in the environment is not a decision
   to spend. A backend of none, or an unreachable replay cassette, leaves no tutor, and
   app/feedback/tutor.py's no-provider degradation returns the deterministic payload with no
   sentence.
   """
   backend = resolve_ai_backend(env)

   if backend == "none":
      return None

   if backend == "replay":
      cassette_path = env.get("GROWTH_TUTOR_CASSETTE")
      has_cassette = cassette_path is not None and cassette_path != ""

      if not has_cassette:
         return None

      return ReplayProvider(cassette_path=cassette_path)

   if backend == "api":
      api_key = env.get("ANTHROPIC_API_KEY")
      has_key = api_key is not None and api_key != ""

      if not has_key:
         return None

      return AnthropicProvider(environ=env)

   if backend == "subscription":
      db_path = env.get("GROWTH_DB_PATH", str(DEFAULT_DB_PATH))
      user_count = installed_user_count(db_path)

      return SubscriptionProvider(environ=env, user_count=user_count)

   raise ValueError(f"{AI_BACKEND_ENV_VAR} must be one of {', '.join(AI_BACKENDS)}, got {backend!r}")


def build_grading_provider(env):
   """The backend the grader, the transcriber and the diagnostician run on: the same choice as the
   tutor's (resolve_ai_backend), except that replay reads a cassette book keyed by request,
   because those roles make a different call per point, page and attempt."""
   backend = resolve_ai_backend(env)

   if backend == "replay":
      book_path = env.get("GROWTH_GRADING_CASSETTES")
      has_book = book_path is not None and book_path != ""

      return CassetteBookProvider(path=book_path) if has_book else None

   return build_tutor(env)


# 12's tutor row sets the tutor's caps; the three P3 roles carry these [inferred] defaults on the
# api backend, set so a day of free-response practice fits: about eight questions of fifteen
# grader calls at the priced grader call, one read-back a question and one diagnosis a question.
DEFAULT_GRADING_CAPS = {
   "grader": (1.50, 600000),
   "transcriber": (0.40, 150000),
   "diagnostician": (0.40, 150000),
}


def build_grading_caps(env):
   caps = {}

   for role, (default_usd, default_tokens) in DEFAULT_GRADING_CAPS.items():
      cap_usd = startup_cap(env, f"GROWTH_{role.upper()}_CAP_USD", str(default_usd))
      cap_tokens = startup_cap(env, f"GROWTH_{role.upper()}_CAP_TOKENS", str(default_tokens))
      caps[role] = BudgetCaps(cap_tokens=cap_tokens, cap_usd=cap_usd)

   return caps


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


def build_subscription_pacing(env):
   on_the_subscription = resolve_ai_backend(env) == "subscription"

   if not on_the_subscription:
      return None

   return pacing_caps_from_environment(env)


def default_item_directories(content_dir=DEFAULT_CONTENT_DIR):
   has_content_dir = content_dir.is_dir()

   if not has_content_dir:
      return ()

   return tuple(sorted(path for path in content_dir.glob(ITEM_BANK_PATTERN) if path.is_dir()))


def items_directories(env):
   configured = env.get("GROWTH_ITEMS_DIR")
   is_unset = configured is None or configured == ""

   if is_unset:
      return default_item_directories()

   if configured == NO_ITEMS_DIR:
      return ()

   configured_paths = tuple(Path(part) for part in configured.split(os.pathsep) if part != "")

   for configured_path in configured_paths:
      is_a_directory = configured_path.is_dir()

      if not is_a_directory:
         raise ValueError(f"GROWTH_ITEMS_DIR must name directories of item records, got {configured!r}")

   return configured_paths


RUNNING_EXPERIMENT_DEFAULTS = {
   switches.FEEDBACK_ELABORATION: switches.OFF,
   switches.RETRIEVAL_ENTRY: switches.RANDOMISED,
}


def experiment_default_state(env):
   """The state each A/B switch starts in for a student. Unset, the retrieval_entry comparison
   starts randomised, so it accrues from the first session with nobody turning it on, and the
   feedback comparison starts off, because the evidence already favours elaborated feedback and
   withholding it from half the corrected items would cost the student more than the answer is
   worth. GROWTH_EXPERIMENTS_DEFAULT names one state for both."""
   configured = env.get("GROWTH_EXPERIMENTS_DEFAULT")

   if configured is None:
      return dict(RUNNING_EXPERIMENT_DEFAULTS)

   is_known = configured in switches.STATES

   if not is_known:
      raise ValueError(f"GROWTH_EXPERIMENTS_DEFAULT must be one of {', '.join(switches.STATES)}, got {configured!r}")

   return configured


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
      subscription_pacing=build_subscription_pacing(env),
      key_audit_sample_path=env.get("GROWTH_KEY_AUDIT_SAMPLE_PATH"),
      items_directories=items_directories(env),
      experiment_default_state=experiment_default_state(env),
      ai_provider=build_grading_provider(env),
      grading_caps=build_grading_caps(env),
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
      engine, settings.content_root, items_directories=settings.items_directories
   )
   settings.frq = build_frq_context(
      settings.session_context.snapshot,
      Path(env.get("GROWTH_FRQ_DIR", str(DEFAULT_FRQ_DIR))),
      unit_titles=settings.session_context.unit_titles,
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
