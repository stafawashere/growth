"""The FastAPI application factory for P1.

Settings carry everything the routes need from outside: the database, the loaded content snapshot,
the engine bundle the session service is called with, the passkey verifier, the deployment origin
and the two hooks that other P1 modules own. Nothing in app/api reads a global, so a test builds a
whole application over a fixture graph and a verifier double.
"""
import random
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.auth.service import REAUTH_TTL_SECONDS, SESSION_TTL_SECONDS, AuthError, ChallengeStore
from app.auth.webauthn import LibraryVerifier

WEBAUTHN_LIBRARY_ERROR_DETAIL = "the passkey ceremony did not verify"


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
   verifier: Any = None
   tutor: Any = None
   tutor_caps: dict = field(default_factory=dict)
   subscription_pacing: Any = None
   rp_id: str = "localhost"
   origin: str = "http://127.0.0.1:8000"
   bind_host: str = "127.0.0.1"
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

   def resolve_verifier(self):
      has_verifier = self.verifier is not None

      if has_verifier:
         return self.verifier

      self.verifier = LibraryVerifier(rp_id=self.rp_id, origin=self.origin)

      return self.verifier

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


def create_app(settings):
   from app.api.routes import assessment, auth, content, evaluation, export, frq, health, me, progress, purge, review, review_screen, sessions
   from app.api.routes import settings as settings_routes
   from app.api.security_headers import SecurityHeadersMiddleware

   application = FastAPI(title="Growth", version="0.0.1")
   application.add_middleware(SecurityHeadersMiddleware)
   application.state.settings = settings
   application.state.engine = settings.resolve_engine()
   application.state.challenges = ChallengeStore()
   settings.resolve_verifier()
   settings.rng = random.Random(settings.rng_seed)

   @application.exception_handler(AuthError)
   async def auth_error_handler(request, exception):
      return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})

   from webauthn.helpers.exceptions import (
      InvalidAuthenticationResponse,
      InvalidJSONStructure,
      InvalidRegistrationResponse,
   )

   @application.exception_handler(InvalidRegistrationResponse)
   @application.exception_handler(InvalidAuthenticationResponse)
   @application.exception_handler(InvalidJSONStructure)
   async def webauthn_library_error_handler(request, exception):
      return JSONResponse(status_code=400, content={"detail": WEBAUTHN_LIBRARY_ERROR_DETAIL})

   for module in (auth, me, sessions, frq, assessment, purge, content, review, review_screen, progress, evaluation, settings_routes, export, health):
      application.include_router(module.router)

   return application
