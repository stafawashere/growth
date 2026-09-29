"""The FastAPI application factory for P1.

Settings carry everything the routes need from outside: the database, the loaded content snapshot,
the engine bundle the session service is called with, the password and sign-in limits, the hosts
this installation serves and the two hooks that other P1 modules own. Nothing in app/api reads a
global, so a test builds a whole application over a fixture graph, with scrypt parameters cheap
enough to hash in a few milliseconds and a rate limit high enough never to trip by accident.

The scrypt parameters, the per-IP limit, the lockout schedule and allowed_hosts are read on every
request, so a test may lower or raise them on a built application's settings.
"""
import random
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.auth.guard import DEFAULT_ALLOWED_HOSTS
from app.auth.limiter import DEFAULT_LIMIT_COUNT, DEFAULT_LIMIT_WINDOW_SECONDS, SlidingWindowLimiter
from app.auth.passwords import DEFAULT_SCRYPT_N, DEFAULT_SCRYPT_P, DEFAULT_SCRYPT_R, build_dummy_hash
from app.auth.service import (
   LOCKOUT_BASE_SECONDS,
   LOCKOUT_FREE_FAILURES,
   LOCKOUT_MAX_SECONDS,
   REAUTH_TTL_SECONDS,
   SESSION_TTL_SECONDS,
)
from app.providers.router import CooldownBoard

AUTH_PATH_PREFIX = "/auth"


@dataclass
class SessionContext:
   """The engine bundle app/session/service.py is called with, resolved once per process."""

   graph: Any
   engine_graph: Any
   archetypes: Any
   bank: Any
   snapshot_id: str
   errors: dict = field(default_factory=dict)
   unit_titles: dict = field(default_factory=dict)
   snapshot: Any = None


@dataclass
class Settings:
   engine: Any = None
   db_path: Any = None
   snapshot: Any = None
   content_root: Any = None
   session_context: SessionContext | None = None
   tutor: Any = None
   tutor_caps: dict = field(default_factory=dict)
   subscription_pacing: Any = None
   bind_host: str = "127.0.0.1"
   allowed_hosts: tuple = DEFAULT_ALLOWED_HOSTS
   password_scrypt_n: int = DEFAULT_SCRYPT_N
   password_scrypt_r: int = DEFAULT_SCRYPT_R
   password_scrypt_p: int = DEFAULT_SCRYPT_P
   auth_rate_limit_count: int = DEFAULT_LIMIT_COUNT
   auth_rate_limit_window_seconds: int = DEFAULT_LIMIT_WINDOW_SECONDS
   lockout_free_failures: int = LOCKOUT_FREE_FAILURES
   lockout_base_seconds: int = LOCKOUT_BASE_SECONDS
   lockout_max_seconds: int = LOCKOUT_MAX_SECONDS
   exam_date: str | None = None
   seed_hook: Any = None
   purge_hook: Any = None
   session_ttl_seconds: int = SESSION_TTL_SECONDS
   reauth_ttl_seconds: int = REAUTH_TTL_SECONDS
   rng_seed: int = 7
   rng: Any = None
   extras: dict = field(default_factory=dict)
   key_audit_sample_ids: Any = None
   key_audit_sample_path: Any = None
   items_directories: tuple = ()
   experiment_default_state: str | dict | None = None
   ai_provider: Any = None
   tutor_links: tuple = ()
   ai_links: tuple = ()
   provider_cooldowns: Any = field(default_factory=CooldownBoard)
   grading_caps: dict = field(default_factory=dict)
   frq: Any = None
   grading_sleep: Any = None
   timed_assessments: bool = True

   def resolve_key_audit_sample_ids(self):
      """docs/operator/key-audit.md: a separate JSON array of the sampled item ids is the sample
      file. The review-queue route (app/api/routes/review.py) reads it through this resolver
      exactly like tools/check_audit_verdicts.py reads its sample argument, so an item_audit
      verdict is refused the same way through either path once no sample is configured.

      A sample file that is missing, unparsable, or whose JSON is not a list fails closed with a
      ValueError, the same refusal the route gives when no sample is configured at all, rather
      than a 500 or a membership check run against a dict's keys or a string's characters.
      """
      has_sample = self.key_audit_sample_ids is not None

      if has_sample:
         return self.key_audit_sample_ids

      has_path = self.key_audit_sample_path is not None

      if not has_path:
         return None

      import json
      from pathlib import Path

      try:
         raw_text = Path(self.key_audit_sample_path).read_text()
      except OSError as missing:
         raise ValueError(
            f"the key-audit sample file {self.key_audit_sample_path!r} could not be read: {missing}"
         ) from missing

      try:
         parsed = json.loads(raw_text)
      except json.JSONDecodeError as malformed:
         raise ValueError(
            f"the key-audit sample file {self.key_audit_sample_path!r} is not valid JSON: {malformed}"
         ) from malformed

      is_a_list = isinstance(parsed, list)

      if not is_a_list:
         raise ValueError(
            f"the key-audit sample file {self.key_audit_sample_path!r} must hold a JSON array "
            f"of item ids, not {type(parsed).__name__}"
         )

      self.key_audit_sample_ids = parsed

      return self.key_audit_sample_ids

   def resolve_engine(self):
      has_engine = self.engine is not None

      if has_engine:
         return self.engine

      from app.db.models import make_engine

      self.engine = make_engine(self.db_path)

      return self.engine

   def resolve_snapshot(self):
      has_snapshot = self.snapshot is not None

      if has_snapshot:
         return self.snapshot

      from app.content.loader import load_snapshot

      self.snapshot = load_snapshot(self.content_root)

      return self.snapshot

   def resolve_seed_hook(self):
      has_hook = self.seed_hook is not None

      if has_hook:
         return self.seed_hook

      from app.session.seed import seed_skills_state

      return seed_skills_state

   def resolve_purge_hook(self):
      has_hook = self.purge_hook is not None

      if has_hook:
         return self.purge_hook

      from app.session.purge import purge_user

      return purge_user


class DummyHashes:
   """One hash of a random password per scrypt parameter set, built when the application is and
   again only if a test changes the parameters afterwards. app/auth/service.py verifies against it
   whenever there is no real hash to check, so an unknown username costs the same work as a known
   one."""

   def __init__(self):
      self.by_parameters = {}

   def for_settings(self, settings):
      parameters = (settings.password_scrypt_n, settings.password_scrypt_r, settings.password_scrypt_p)
      built = self.by_parameters.get(parameters)

      if built is None:
         built = build_dummy_hash(*parameters)
         self.by_parameters = {parameters: built}

      return built


def without_input(errors):
   """A 422 on an auth route never echoes what was sent, which may be a password."""
   return [
      {key: value for key, value in error.items() if key not in ("input", "ctx")}
      for error in errors
   ]


def create_app(settings):
   from app.api.routes import assessment, auth, content, evaluation, export, frq, health, me, notices, progress, purge, review, review_screen, sessions
   from app.api.routes import settings as settings_routes
   from app.api.security_headers import SecurityHeadersMiddleware
   from starlette.middleware.gzip import GZipMiddleware

   application = FastAPI(title="Growth", version="0.0.1")
   application.add_middleware(SecurityHeadersMiddleware)
   application.add_middleware(GZipMiddleware, minimum_size=1024)
   application.state.settings = settings
   application.state.engine = settings.resolve_engine()
   application.state.auth_limiter = SlidingWindowLimiter()
   application.state.dummy_hashes = DummyHashes()
   application.state.dummy_hashes.for_settings(settings)
   settings.rng = random.Random(settings.rng_seed)

   @application.exception_handler(RequestValidationError)
   async def validation_error_handler(request, exception):
      is_auth_path = request.url.path.startswith(AUTH_PATH_PREFIX)

      if not is_auth_path:
         return await request_validation_exception_handler(request, exception)

      return JSONResponse(status_code=422, content={"detail": jsonable_encoder(without_input(exception.errors()))})

   for module in (auth, me, notices, sessions, frq, assessment, purge, content, review, review_screen, progress, evaluation, settings_routes, export, health):
      application.include_router(module.router)

   return application
