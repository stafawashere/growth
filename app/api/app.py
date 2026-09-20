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


@dataclass
class SessionContext:
   """The engine bundle app/session/service.py is called with, resolved once per process."""

   graph: Any
   engine_graph: Any
   archetypes: Any
   bank: Any
   snapshot_id: str
   errors: dict = field(default_factory=dict)


@dataclass
class Settings:
   engine: Any = None
   db_path: Any = None
   snapshot: Any = None
   content_root: Any = None
   session_context: SessionContext | None = None
   verifier: Any = None
   tutor: Any = None
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
   from app.api.routes import auth, content, health, me, purge, review, sessions

   application = FastAPI(title="Growth", version="0.0.1")
   application.state.settings = settings
   application.state.engine = settings.resolve_engine()
   application.state.challenges = ChallengeStore()
   settings.resolve_verifier()
   settings.rng = random.Random(settings.rng_seed)

   @application.exception_handler(AuthError)
   async def auth_error_handler(request, exception):
      return JSONResponse(status_code=exception.status_code, content={"detail": exception.detail})

   for module in (auth, me, sessions, purge, content, review, health):
      application.include_router(module.router)

   return application
