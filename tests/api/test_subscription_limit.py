"""A subscription usage limit on the feedback route degrades like 07's hard stop.

The student gets the static feedback with the tutor marked unavailable, the call is queued in the
jobs table, and nothing is retried on the paid API.
"""
import json

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.providers.anthropic import AnthropicProvider
from app.providers.call_queue import QUEUED_CALL_JOB_TYPE, QUEUED_CALL_STATE
from app.providers import guard
from app.providers.guard import DevSpendLedger, SubscriptionSpendLedger
from app.providers.subscription import SubscriptionProvider
from tests.api.test_tutor_budget import wrong_short_answer
from tests.providers.test_subscription import FakeCli


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


@pytest.fixture
def no_paid_api(monkeypatch):
   def refuse(*args, **kwargs):
      raise AssertionError("a subscription limit must never fall through to the paid API")

   monkeypatch.setattr(AnthropicProvider, "generate", refuse)
   monkeypatch.setattr(AnthropicProvider, "stream", refuse)


def queued_jobs(engine):
   with OrmSession(engine) as db:
      return db.scalars(select(models.Job).where(models.Job.type == QUEUED_CALL_JOB_TYPE)).all()


def subscription_tutor(cli, tmp_path):
   ledger = SubscriptionSpendLedger(path=tmp_path / "subscription_ledger.json")

   return SubscriptionProvider(environ=cli.environ(), subscription_ledger=ledger)


def test_a_weekly_limit_serves_static_feedback_and_queues_the_call(world, cli, tmp_path, no_paid_api):
   cli.mode("weekly_limit")
   world.settings.tutor = subscription_tutor(cli, tmp_path)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["sentence"] is None
   assert body["tutor_unavailable"] is True
   assert body["kind"] == "elaborated"

   jobs = queued_jobs(world.engine)

   assert len(jobs) == 1
   assert jobs[0].state == QUEUED_CALL_STATE

   payload = json.loads(jobs[0].payload)

   assert payload["attempt_id"] == attempt_id
   assert payload["role"] == "tutor"
   assert payload["reason"] == "subscription_limit_reached"
   assert payload["user_id"] is not None


def test_a_second_read_under_the_limit_does_not_queue_the_call_twice(world, cli, tmp_path, no_paid_api):
   cli.mode("weekly_limit")
   world.settings.tutor = subscription_tutor(cli, tmp_path)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")
   second = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert second.status_code == 200
   assert second.json()["tutor_unavailable"] is True
   assert len(queued_jobs(world.engine)) == 1


def test_an_ordinary_cli_failure_is_not_a_limit_and_queues_nothing(world, cli, tmp_path, no_paid_api):
   cli.mode("nonzero")
   world.settings.tutor = subscription_tutor(cli, tmp_path)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["sentence"] is None
   assert body["tutor_unavailable"] is False
   assert queued_jobs(world.engine) == []


def test_the_subscription_tutor_writes_its_sentence_on_success(world, cli, tmp_path, no_paid_api):
   cli.mode("success")
   world.settings.tutor = subscription_tutor(cli, tmp_path)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["sentence"] == "The factor cancels only after the rewrite, so the answer point is lost."
   assert body["tutor_unavailable"] is False
   assert queued_jobs(world.engine) == []


def test_a_served_subscription_sentence_is_counted_off_the_api_dev_cap(
   world, cli, tmp_path, no_paid_api, monkeypatch
):
   api_cap_path = tmp_path / "dev_spend_ledger.json"
   monkeypatch.setattr(guard, "DEV_SPEND_LEDGER_PATH", api_cap_path)

   assert DevSpendLedger().path == api_cap_path

   cli.mode("success")
   subscription_ledger = SubscriptionSpendLedger(path=tmp_path / "subscription_ledger.json")
   world.settings.tutor = SubscriptionProvider(environ=cli.environ(), subscription_ledger=subscription_ledger)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["sentence"] is not None
   assert subscription_ledger.spent() == pytest.approx(0.0123)
   assert DevSpendLedger().spent() == 0.0
   assert not api_cap_path.exists()


def test_a_subscription_tutor_is_not_stopped_by_the_api_dollar_cap(world, cli, tmp_path, no_paid_api):
   """The default $1.00 tutor cap prices a call at API rates. Set far below one call, it would
   stop the tutor at once if subscription calls were charged to it; they are paced instead."""
   cli.mode("success")
   world.settings.tutor = subscription_tutor(cli, tmp_path)
   world.settings.tutor_caps = {"tutor": guard.BudgetCaps(cap_usd=0.000001, cap_tokens=10)}
   world.settings.subscription_pacing = guard.SubscriptionPacingCaps()
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["sentence"] == "The factor cancels only after the rewrite, so the answer point is lost."
   assert body["tutor_unavailable"] is False

   with OrmSession(world.engine) as db:
      tutor_rows = db.scalars(select(models.Budget).where(models.Budget.role == "tutor")).all()
      attempt = db.get(models.Attempt, attempt_id)

   assert tutor_rows == []
   assert attempt.tutor_calls == 1
   assert attempt.tutor_cost_usd > 0.000001


def test_the_pacing_cap_marks_the_subscription_tutor_unavailable(world, cli, tmp_path, no_paid_api):
   cli.mode("success")
   world.settings.tutor = subscription_tutor(cli, tmp_path)
   world.settings.subscription_pacing = guard.SubscriptionPacingCaps(calls_per_day={"tutor": 1}, calls_per_minute=10)
   guard.SubscriptionPacingLedger().reserve("tutor", guard.utc_now(), world.settings.subscription_pacing)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["sentence"] is None
   assert body["tutor_unavailable"] is True
   assert not (cli.home / "fake_claude_record.json").exists()
