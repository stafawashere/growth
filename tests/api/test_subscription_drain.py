"""Draining the tutor calls a subscription usage limit queued (app/feedback/drain.py and
tools/drain_subscription_queue.py), against tests/fixtures/fake_claude/claude.

A call queued behind a limit is retried once the window has reset, through the configured
backend and never the paid API unless GROWTH_AI_BACKEND=api, and its sentence lands on the
attempt so the student sees it on the next read of the feedback screen.
"""
import json
from datetime import timedelta
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.auth.service import as_iso, utc_now
from app.db import models
from app.feedback import tutor
from app.feedback.drain import CEILING_REACHED_ERROR, DEV_SPEND_STOP, DONE_STATE, FAILED_STATE, LIMIT_RETRY_AFTER, MAX_DRAIN_ATTEMPTS, drain_queued_calls
from app.providers import guard
from app.providers.anthropic import AnthropicProvider
from app.providers.call_queue import QUEUED_CALL_JOB_TYPE, QUEUED_CALL_STATE
from app.providers.guard import DEV_SPEND_CAP_ENV_VAR, SubscriptionPacingCaps
from app.providers.subscription import SubscriptionProvider
from tests.api.test_tutor_budget import wrong_short_answer
from tests.providers.test_subscription import FakeCli
from tools import drain_subscription_queue

CASSETTE_PATH = Path(__file__).resolve().parents[1] / "fixtures" / "provider_cassettes" / "tutor_elaborated_v1.json"
FAKE_SENTENCE = "The factor cancels only after the rewrite, so the answer point is lost."


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


@pytest.fixture
def no_paid_api(monkeypatch):
   def refuse(*args, **kwargs):
      raise AssertionError("draining the queue must never reach the paid API")

   monkeypatch.setattr(AnthropicProvider, "generate", refuse)
   monkeypatch.setattr(AnthropicProvider, "stream", refuse)


def queued_jobs(engine):
   with OrmSession(engine) as db:
      return db.scalars(select(models.Job).where(models.Job.type == QUEUED_CALL_JOB_TYPE)).all()


def attempt_sentence(engine, attempt_id):
   with OrmSession(engine) as db:
      return db.get(models.Attempt, attempt_id).tutor_sentence


def attempt_tutor_calls(engine, attempt_id):
   with OrmSession(engine) as db:
      return db.get(models.Attempt, attempt_id).tutor_calls or 0


def set_attempt_tutor_calls(engine, attempt_id, calls):
   with OrmSession(engine) as db:
      db.get(models.Attempt, attempt_id).tutor_calls = calls
      db.commit()


def limited_attempt(world, cli):
   cli.mode("weekly_limit")
   world.settings.tutor = SubscriptionProvider(environ=cli.environ())
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   first = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert first["tutor_unavailable"] is True
   assert len(queued_jobs(world.engine)) == 1

   return client, session_id, attempt_id


def drain(world, cli, clock=utc_now):
   with OrmSession(world.engine) as db:
      return drain_queued_calls(
         db,
         SubscriptionProvider(environ=cli.environ()),
         clock,
         pacing=SubscriptionPacingCaps(),
      )


def test_a_drained_call_stores_the_sentence_the_student_then_sees(world, cli, no_paid_api):
   client, session_id, attempt_id = limited_attempt(world, cli)
   cli.mode("success")
   report = drain(world, cli)

   assert report.done == 1
   assert report.stopped_by is None

   job = queued_jobs(world.engine)[0]

   assert job.state == DONE_STATE
   assert attempt_sentence(world.engine, attempt_id) == FAKE_SENTENCE

   queued_prompt = json.loads(job.payload)["messages"][0]["content"]

   assert cli.record()["stdin"] == queued_prompt

   cli.mode("nonzero")
   returned = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert returned["sentence"] == FAKE_SENTENCE
   assert returned["tutor_unavailable"] is False


def test_a_limit_that_still_holds_requeues_the_job_later_and_stops(world, cli, no_paid_api):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   now = utc_now()
   report = drain(world, cli, clock=lambda: now)

   assert report.done == 0
   assert report.requeued == 1
   assert report.stopped_by == "subscription_limit_reached"

   job = queued_jobs(world.engine)[0]

   assert job.state == QUEUED_CALL_STATE
   assert job.attempts_made == 0
   assert job.not_before == as_iso(now + LIMIT_RETRY_AFTER)
   assert attempt_sentence(world.engine, attempt_id) is None

   cli.mode("success")
   too_soon = drain(world, cli, clock=lambda: now + timedelta(minutes=1))

   assert too_soon.done == 0
   assert queued_jobs(world.engine)[0].state == QUEUED_CALL_STATE

   after_the_reset = drain(world, cli, clock=lambda: now + LIMIT_RETRY_AFTER + timedelta(minutes=1))

   assert after_the_reset.done == 1
   assert attempt_sentence(world.engine, attempt_id) == FAKE_SENTENCE


def test_the_pacing_guard_holds_the_drain_back_without_calling(world, cli, no_paid_api):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   cli.mode("success")
   (cli.home / "fake_claude_record.json").unlink()

   with OrmSession(world.engine) as db:
      report = drain_queued_calls(
         db,
         SubscriptionProvider(environ=cli.environ()),
         utc_now,
         pacing=SubscriptionPacingCaps(calls_per_day={"tutor": 1}, calls_per_minute=10),
      )

   assert report.stopped_by == "budget:subscription_calls_per_day"
   assert queued_jobs(world.engine)[0].state == QUEUED_CALL_STATE
   assert not (cli.home / "fake_claude_record.json").exists()
   assert attempt_sentence(world.engine, attempt_id) is None


def test_the_drain_tool_uses_the_configured_subscription_backend(world, cli, no_paid_api, capsys):
   """The API dollar cap is set below one call, so the drain only answers if the tool paces the
   subscription call instead of charging it to that cap."""
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   cli.mode("success")
   env = cli.environ(GROWTH_DB_PATH=str(world.engine.url.database), GROWTH_TUTOR_CAP_USD="0.000001")

   exit_code = drain_subscription_queue.main([], env=env)
   printed = capsys.readouterr().out

   assert exit_code == 0
   assert "backend = subscription" in printed
   assert "done = 1" in printed
   assert attempt_sentence(world.engine, attempt_id) == FAKE_SENTENCE


def test_the_drain_tool_never_stores_a_replayed_sentence_on_a_real_attempt(world, cli, no_paid_api):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   env = cli.environ(
      GROWTH_DB_PATH=str(world.engine.url.database),
      GROWTH_AI_BACKEND="replay",
      GROWTH_TUTOR_CASSETTE=str(CASSETTE_PATH),
   )

   assert drain_subscription_queue.main([], env=env) == 2
   assert queued_jobs(world.engine)[0].state == QUEUED_CALL_STATE
   assert attempt_sentence(world.engine, attempt_id) is None


def test_the_drain_tool_refuses_the_older_paid_switch(world, cli, no_paid_api):
   limited_attempt(world, cli)
   env = cli.environ(
      GROWTH_DB_PATH=str(world.engine.url.database),
      GROWTH_TUTOR_PROVIDER="anthropic",
      ANTHROPIC_API_KEY="test-key-not-real",
   )

   with pytest.raises(ValueError, match="GROWTH_AI_BACKEND=api"):
      drain_subscription_queue.main([], env=env)

   assert json.loads(queued_jobs(world.engine)[0].payload)["role"] == "tutor"
   assert queued_jobs(world.engine)[0].state == QUEUED_CALL_STATE


def test_waiting_behind_a_limit_does_not_use_up_the_failure_retries(world, cli, no_paid_api):
   """Limit waits outnumber MAX_DRAIN_ATTEMPTS, and the one real failure after them still
   re-queues the job instead of failing it."""
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   now = utc_now()

   for wait in range(MAX_DRAIN_ATTEMPTS + 1):
      moment = now + (LIMIT_RETRY_AFTER + timedelta(minutes=1)) * wait
      report = drain(world, cli, clock=lambda: moment)

      assert report.stopped_by == "subscription_limit_reached"

   assert queued_jobs(world.engine)[0].attempts_made == 0

   cli.mode("nonzero")
   after_the_reset = now + (LIMIT_RETRY_AFTER + timedelta(minutes=1)) * (MAX_DRAIN_ATTEMPTS + 1)
   report = drain(world, cli, clock=lambda: after_the_reset)
   job = queued_jobs(world.engine)[0]

   assert report.failed == 0
   assert report.requeued == 1
   assert job.state == QUEUED_CALL_STATE
   assert job.state != FAILED_STATE
   assert job.attempts_made == 1
   assert attempt_sentence(world.engine, attempt_id) is None


def test_the_developer_spend_cap_stops_an_api_drain_cleanly(world, cli, no_paid_api, monkeypatch, tmp_path, capsys):
   """DevSpendCapExceeded is not a BudgetStopped, so it needs its own clean stop: the tool reports
   and exits 0, and the job is left exactly as it was."""
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   monkeypatch.setattr(guard, "DEV_SPEND_LEDGER_PATH", tmp_path / "dev_spend_ledger.json")
   monkeypatch.setenv(DEV_SPEND_CAP_ENV_VAR, "0.000001")
   env = cli.environ(
      GROWTH_DB_PATH=str(world.engine.url.database),
      GROWTH_AI_BACKEND="api",
      ANTHROPIC_API_KEY="test-key-not-real",
   )

   exit_code = drain_subscription_queue.main([], env=env)
   printed = capsys.readouterr().out
   job = queued_jobs(world.engine)[0]

   assert exit_code == 0
   assert "backend = api" in printed
   assert f"stopped_by = {DEV_SPEND_STOP}" in printed
   assert job.state == QUEUED_CALL_STATE
   assert job.attempts_made == 0
   assert attempt_sentence(world.engine, attempt_id) is None


def test_a_job_whose_item_ceiling_is_full_fails_without_calling(world, cli, no_paid_api):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   set_attempt_tutor_calls(world.engine, attempt_id, tutor.TUTOR_CALLS_PER_ITEM)
   cli.mode("success")
   (cli.home / "fake_claude_record.json").unlink()
   report = drain(world, cli)
   job = queued_jobs(world.engine)[0]

   assert report.failed == 1
   assert report.done == 0
   assert job.state == FAILED_STATE
   assert job.last_error == CEILING_REACHED_ERROR
   assert not (cli.home / "fake_claude_record.json").exists()
   assert attempt_sentence(world.engine, attempt_id) is None
   assert attempt_tutor_calls(world.engine, attempt_id) == tutor.TUTOR_CALLS_PER_ITEM


def test_a_job_whose_session_ceiling_is_full_fails_without_calling(world, cli, no_paid_api, monkeypatch):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   calls_so_far = attempt_tutor_calls(world.engine, attempt_id)
   item_has_room = calls_so_far < tutor.TUTOR_CALLS_PER_ITEM

   assert item_has_room

   monkeypatch.setattr(tutor, "TUTOR_CALLS_PER_SESSION", calls_so_far)
   cli.mode("success")
   (cli.home / "fake_claude_record.json").unlink()
   report = drain(world, cli)
   job = queued_jobs(world.engine)[0]

   assert report.failed == 1
   assert job.state == FAILED_STATE
   assert job.last_error == CEILING_REACHED_ERROR
   assert not (cli.home / "fake_claude_record.json").exists()
   assert attempt_sentence(world.engine, attempt_id) is None


def test_waiting_behind_a_limit_does_not_fill_the_item_ceiling(world, cli, no_paid_api):
   """More limit waits than the item ceiling allows calls, and the job is still answered once
   the window resets."""
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   calls_when_queued = attempt_tutor_calls(world.engine, attempt_id)
   now = utc_now()
   waits = tutor.TUTOR_CALLS_PER_ITEM + 1

   for wait in range(waits):
      moment = now + (LIMIT_RETRY_AFTER + timedelta(minutes=1)) * wait
      report = drain(world, cli, clock=lambda: moment)

      assert report.stopped_by == "subscription_limit_reached"

   assert attempt_tutor_calls(world.engine, attempt_id) == calls_when_queued

   cli.mode("success")
   after_the_reset = now + (LIMIT_RETRY_AFTER + timedelta(minutes=1)) * waits
   report = drain(world, cli, clock=lambda: after_the_reset)

   assert report.done == 1
   assert attempt_sentence(world.engine, attempt_id) == FAKE_SENTENCE
   assert attempt_tutor_calls(world.engine, attempt_id) == calls_when_queued + 1
