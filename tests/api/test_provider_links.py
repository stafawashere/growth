"""The fallback chain app/main.py builds per backend: subscription first, the paid API only when
GROWTH_AI_BACKEND=api allows it, and no link at all when neither may run. Building settings starts
no process and opens no socket.
"""
import sqlite3
from datetime import datetime, timedelta, timezone

from app.main import settings_from_environment
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import BudgetCaps
from app.providers.router import API_LINK, REPLAY_LINK, SUBSCRIPTION_LINK
from app.providers.subscription import SubscriptionLimitReached, SubscriptionProvider
from app.settings.providers import providers_view

CASSETTE = "tests/fixtures/provider_cassettes/tutor_elaborated_v1.json"
BOOK = "tests/fixtures/grading_cassettes/grader_goldens.json"


def env_for(tmp_path, **overrides):
   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db"), "GROWTH_ITEMS_DIR": "none"}
   env.update(overrides)

   return env


def names(links):
   return [link.name for link in links]


def test_the_subscription_backend_runs_on_the_subscription_alone(tmp_path):
   settings = settings_from_environment(env_for(tmp_path))

   assert names(settings.tutor_links) == [SUBSCRIPTION_LINK]
   assert names(settings.ai_links) == [SUBSCRIPTION_LINK]
   assert settings.tutor_links[0].provider is settings.tutor
   assert settings.tutor_links[0].pacing is not None
   assert not any(link.pays for link in settings.tutor_links + settings.ai_links)


def test_the_api_backend_puts_the_subscription_first_and_the_paid_api_second(tmp_path):
   settings = settings_from_environment(env_for(tmp_path, GROWTH_AI_BACKEND="api", ANTHROPIC_API_KEY="test-key-not-real"))

   for links in (settings.tutor_links, settings.ai_links):
      assert names(links) == [SUBSCRIPTION_LINK, API_LINK]
      assert isinstance(links[0].provider, SubscriptionProvider)
      assert links[0].pacing is not None
      assert links[0].pays is False
      assert isinstance(links[1].provider, AnthropicProvider)
      assert links[1].pays is True
      assert links[1].pacing is None


def test_the_api_backend_without_a_key_keeps_only_the_subscription(tmp_path, monkeypatch):
   monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
   settings = settings_from_environment(env_for(tmp_path, GROWTH_AI_BACKEND="api"))

   assert names(settings.tutor_links) == [SUBSCRIPTION_LINK]


def test_a_second_user_account_takes_the_subscription_out_of_the_api_chain(tmp_path):
   database_path = tmp_path / "growth.db"
   connection = sqlite3.connect(database_path)
   connection.execute("CREATE TABLE users (id TEXT)")
   connection.execute("INSERT INTO users VALUES ('USER-a'), ('USER-b')")
   connection.commit()
   connection.close()

   settings = settings_from_environment(env_for(tmp_path, GROWTH_AI_BACKEND="api", ANTHROPIC_API_KEY="test-key-not-real"))

   assert names(settings.tutor_links) == [API_LINK]


def test_replay_and_none_never_reach_a_live_backend(tmp_path):
   replayed = settings_from_environment(
      env_for(tmp_path, GROWTH_AI_BACKEND="replay", GROWTH_TUTOR_CASSETTE=CASSETTE, GROWTH_GRADING_CASSETTES=BOOK)
   )
   switched_off = settings_from_environment(env_for(tmp_path, GROWTH_AI_BACKEND="none"))

   assert names(replayed.tutor_links) == [REPLAY_LINK]
   assert names(replayed.ai_links) == [REPLAY_LINK]
   assert switched_off.tutor_links == ()
   assert switched_off.ai_links == ()


def test_settings_shows_each_chain_and_what_is_cooling(tmp_path):
   settings = settings_from_environment(env_for(tmp_path, GROWTH_AI_BACKEND="api", ANTHROPIC_API_KEY="test-key-not-real"))
   now = datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc)
   settings.provider_cooldowns.failed("tutor", SUBSCRIPTION_LINK, SubscriptionLimitReached.__name__, now)
   view = providers_view(settings, now=now + timedelta(minutes=1))

   assert view["chains"] == {"tutor": [SUBSCRIPTION_LINK, API_LINK], "grading": [SUBSCRIPTION_LINK, API_LINK]}
   assert [(entry["role"], entry["link"], entry["because"]) for entry in view["cooling"]] == [
      ("tutor", SUBSCRIPTION_LINK, SubscriptionLimitReached.__name__)
   ]
   assert providers_view(settings, now=now + timedelta(hours=1))["cooling"] == []


def test_the_agent_runs_on_the_tutors_chain_with_caps_of_its_own(tmp_path):
   settings = settings_from_environment(env_for(tmp_path))
   on_the_api = settings_from_environment(env_for(tmp_path, GROWTH_AI_BACKEND="api", ANTHROPIC_API_KEY="test-key-not-real"))

   assert names(settings.agent_links) == names(settings.tutor_links) == [SUBSCRIPTION_LINK]
   assert settings.agent_links[0].provider is settings.tutor
   assert names(on_the_api.agent_links) == names(on_the_api.tutor_links) == [SUBSCRIPTION_LINK, API_LINK]
   assert on_the_api.agent_links[1].provider is on_the_api.tutor
   assert on_the_api.agent_links[1].pays is True
   assert settings.agent_caps == {
      "agent": BudgetCaps(cap_tokens=1500000, cap_usd=1.50),
      "memory": BudgetCaps(cap_tokens=300000, cap_usd=0.50),
   }


def test_the_agent_caps_read_the_four_variables(tmp_path):
   settings = settings_from_environment(
      env_for(
         tmp_path,
         GROWTH_AGENT_CAP_USD="2.25",
         GROWTH_AGENT_CAP_TOKENS="900000",
         GROWTH_MEMORY_CAP_USD="0.10",
         GROWTH_MEMORY_CAP_TOKENS="50000",
      )
   )

   assert settings.agent_caps == {
      "agent": BudgetCaps(cap_tokens=900000, cap_usd=2.25),
      "memory": BudgetCaps(cap_tokens=50000, cap_usd=0.10),
   }
