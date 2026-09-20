"""app/main.py's composition root: the tutor role it wires onto Settings (docs/plan/11-phased-
delivery.md P1 scope item 12, docs/plan/07-ai-provider-layer.md's one wired role), plus
app/api/routes/auth.py's reauth_finish audit entry (docs/plan/09-security-and-privacy.md's Audit
log section names "a session established from a new authenticator" as recorded).

Every build_application test here builds a real application against the live data/ registries,
exactly as the module-level `application` object does, with only the database pointed at a tmp
path. No test supplies a real Anthropic key and no test opens a socket; the tutor's own
construction never calls a provider, so a fake key string is enough to prove the provider was
wired without proving anything about the key's validity.

The reauth test drives a full passkey ceremony through the `world` fixture tests/api/conftest.py
already builds for the other route tests, over a FakeVerifier that never opens a socket either.
"""
import socket

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.main import build_application
from app.providers.anthropic import AnthropicProvider


def env_for(tmp_path, **overrides):
   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db")}
   env.update(overrides)
   return env


def test_main_wires_a_tutor_when_a_key_is_configured(tmp_path, monkeypatch):
   def _forbidden_socket(*args, **kwargs):
      raise AssertionError("building the application must never open a socket")

   monkeypatch.setattr("socket.socket", _forbidden_socket)

   application = build_application(
      env_for(
         tmp_path,
         ANTHROPIC_API_KEY="test-key-not-real",
         GROWTH_TUTOR_PROVIDER="anthropic",
      )
   )

   assert isinstance(application.state.settings.tutor, AnthropicProvider)


def test_main_builds_without_a_tutor_when_no_key_is_configured(tmp_path, monkeypatch):
   monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

   application = build_application(env_for(tmp_path))

   assert application.state.settings.tutor is None


def test_main_respects_an_explicit_none_provider_even_with_a_key(tmp_path):
   application = build_application(
      env_for(tmp_path, ANTHROPIC_API_KEY="test-key-not-real", GROWTH_TUTOR_PROVIDER="none")
   )

   assert application.state.settings.tutor is None


def test_a_stray_key_alone_wires_no_tutor(tmp_path):
   """07 puts the budget guard, the usage accounting and the audit trail at the provider seam,
   none of which P1 has built, so a billed role is never wired by the accident of a key sitting
   in the environment. The deployment names the provider or gets none.
   """
   application = build_application(env_for(tmp_path, ANTHROPIC_API_KEY="test-key-not-real"))

   assert application.state.settings.tutor is None


def test_building_the_application_opens_no_socket(tmp_path, monkeypatch):
   def _forbidden_socket(*args, **kwargs):
      raise AssertionError("building the application must never open a socket")

   monkeypatch.setattr("socket.socket", _forbidden_socket)

   with_key = build_application(
      env_for(
         tmp_path,
         ANTHROPIC_API_KEY="test-key-not-real",
         GROWTH_TUTOR_PROVIDER="anthropic",
      )
   )
   without_key = build_application(env_for(tmp_path / "second"))

   assert with_key.state.settings.tutor is not None
   assert without_key.state.settings.tutor is None


def test_reauth_finish_writes_an_audit_entry(world):
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200

   reauthed = world.reauth(client)

   assert reauthed.status_code == 200

   with OrmSession(world.engine) as db:
      rows = db.scalars(
         select(models.AuditLog).where(models.AuditLog.action == "reauth_established")
      ).all()

   assert len(rows) == 1
   assert rows[0].actor == registered.json()["user"]["id"]
