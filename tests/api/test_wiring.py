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
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.main import DEFAULT_TUTOR_CAP_USD, build_application
from app.providers.anthropic import AnthropicProvider
from app.providers.replay import ReplayProvider
from app.providers.subscription import SubscriptionProvider

CASSETTE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "provider_cassettes" / "tutor_elaborated_v1.json"


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

   application = build_application(env_for(tmp_path, GROWTH_AI_BACKEND="api"))

   assert application.state.settings.tutor is None


def test_main_respects_an_explicit_none_provider_even_with_a_key(tmp_path):
   application = build_application(
      env_for(tmp_path, ANTHROPIC_API_KEY="test-key-not-real", GROWTH_TUTOR_PROVIDER="none")
   )

   assert application.state.settings.tutor is None


def test_a_stray_key_alone_wires_no_paid_tutor(tmp_path):
   """A billed role is never wired by the accident of a key sitting in the environment. Only
   GROWTH_AI_BACKEND=api, or the older GROWTH_TUTOR_PROVIDER=anthropic, spends on the key. With
   neither set the default backend is the operator's subscription, which never reads the key.
   """
   application = build_application(env_for(tmp_path, ANTHROPIC_API_KEY="test-key-not-real"))
   tutor = application.state.settings.tutor

   assert not isinstance(tutor, AnthropicProvider)
   assert isinstance(tutor, SubscriptionProvider)


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
   without_key = build_application(env_for(tmp_path / "second", GROWTH_AI_BACKEND="api"))
   on_the_subscription = build_application(env_for(tmp_path / "third"))

   assert with_key.state.settings.tutor is not None
   assert without_key.state.settings.tutor is None
   assert isinstance(on_the_subscription.state.settings.tutor, SubscriptionProvider)


def test_the_default_backend_is_the_subscription(tmp_path):
   application = build_application(env_for(tmp_path))

   assert isinstance(application.state.settings.tutor, SubscriptionProvider)


def test_an_explicit_backend_wins_over_the_older_variable(tmp_path):
   application = build_application(
      env_for(
         tmp_path,
         ANTHROPIC_API_KEY="test-key-not-real",
         GROWTH_TUTOR_PROVIDER="anthropic",
         GROWTH_AI_BACKEND="subscription",
      )
   )

   assert isinstance(application.state.settings.tutor, SubscriptionProvider)


def test_the_api_backend_is_the_only_way_to_the_paid_adapter(tmp_path):
   application = build_application(
      env_for(tmp_path, ANTHROPIC_API_KEY="test-key-not-real", GROWTH_AI_BACKEND="api")
   )

   assert isinstance(application.state.settings.tutor, AnthropicProvider)


def test_the_replay_backend_reads_the_cassette(tmp_path):
   application = build_application(
      env_for(
         tmp_path,
         ANTHROPIC_API_KEY="test-key-not-real",
         GROWTH_AI_BACKEND="replay",
         GROWTH_TUTOR_CASSETTE=str(CASSETTE_PATH),
      )
   )

   assert isinstance(application.state.settings.tutor, ReplayProvider)


def test_an_unknown_backend_stops_the_process_at_startup(tmp_path):
   with pytest.raises(ValueError, match="GROWTH_AI_BACKEND"):
      build_application(env_for(tmp_path, GROWTH_AI_BACKEND="anthropic"))


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


def test_main_gives_the_tutor_role_a_daily_cap(tmp_path):
   """07's budget guard is only a guard if a cap exists, so the default is a real number and not
   None, and the operator raises or lowers it through the environment."""
   application = build_application(env_for(tmp_path))
   caps = application.state.settings.tutor_caps

   assert "tutor" in caps
   assert caps["tutor"].cap_usd == DEFAULT_TUTOR_CAP_USD


def test_the_tutor_cap_is_read_from_the_environment(tmp_path):
   application = build_application(env_for(tmp_path, GROWTH_TUTOR_CAP_USD="0.25"))

   assert application.state.settings.tutor_caps["tutor"].cap_usd == 0.25
