"""The automatic drain, app/feedback/autodrain.py, against tests/fixtures/fake_claude/claude.

A queued tutor call is retried by the running app once the limit's cooldown has passed, never
before, at most JOBS_PER_PASS a pass, under the subscription pacing guard, and never on a replayed
backend. The drain shares the app's cooldown board, which is what holds it back after a limit.
"""
import time
from datetime import timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.agent import conversations
from app.agent.consolidate import JOB_TYPE
from app.auth.service import as_iso, utc_now
from app.db import models
from app.feedback.autodrain import AutoDrain, auto_drain_enabled, can_drain
from app.feedback.drain import DONE_STATE, LIMIT_RETRY_AFTER
from app.main import build_application
from app.providers.anthropic import AnthropicProvider
from app.providers.call_queue import QUEUED_CALL_STATE
from app.providers.guard import SubscriptionPacingCaps
from app.providers.replay import ReplayProvider
from app.providers.router import REPLAY_LINK, SUBSCRIPTION_LINK, ChainLink, CooldownBoard
from app.providers.subscription import SubscriptionProvider
from tests.api.test_fallback_route import second_wrong_answer
from tests.api.test_subscription_drain import attempt_sentence, limited_attempt, queued_jobs
from tests.providers.test_subscription import FakeCli

FAKE_SENTENCE = "The factor cancels only after the rewrite, so the answer point is lost."


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


@pytest.fixture
def no_paid_api(monkeypatch):
   def refuse(*args, **kwargs):
      raise AssertionError("the automatic drain must never reach the paid API")

   monkeypatch.setattr(AnthropicProvider, "generate", refuse)
   monkeypatch.setattr(AnthropicProvider, "stream", refuse)


class Clock:
   def __init__(self, moment):
      self.moment = moment

   def __call__(self):
      return self.moment


def subscription_links(cli, pacing=None):
   provider = SubscriptionProvider(environ=cli.environ())

   return (ChainLink(SUBSCRIPTION_LINK, provider, pacing=pacing or SubscriptionPacingCaps()),)


def auto_drain(world, cli, clock, pacing=None, jobs_per_pass=5, interval=timedelta(minutes=10), board=None):
   return AutoDrain(
      world.engine,
      subscription_links(cli, pacing),
      world.settings.tutor_caps,
      board if board is not None else world.settings.provider_cooldowns,
      clock=clock,
      interval=interval,
      jobs_per_pass=jobs_per_pass,
   )


def test_a_queued_call_is_answered_once_the_window_has_passed_and_not_before(world, cli, no_paid_api):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   cli.mode("success")
   (cli.home / "fake_claude_record.json").unlink()
   clock = Clock(utc_now())
   drain = auto_drain(world, cli, clock)

   too_soon = drain.run_pass()

   assert too_soon.done == 0
   assert too_soon.requeued == 1
   assert queued_jobs(world.engine)[0].state == QUEUED_CALL_STATE
   assert not (cli.home / "fake_claude_record.json").exists()

   clock.moment = clock.moment + timedelta(minutes=10)

   assert drain.run_pass().done == 0

   clock.moment = clock.moment + LIMIT_RETRY_AFTER
   after_the_window = drain.run_pass()

   assert after_the_window.done == 1
   assert queued_jobs(world.engine)[0].state == DONE_STATE
   assert attempt_sentence(world.engine, attempt_id) == FAKE_SENTENCE


def test_a_pass_retries_at_most_its_cap(world, cli, no_paid_api):
   client, session_id, _attempt_id = limited_attempt(world, cli)
   next_attempt_id = second_wrong_answer(client, session_id)
   second = client.get(f"/sessions/{session_id}/attempts/{next_attempt_id}/feedback")

   assert second.status_code == 200
   assert len(queued_jobs(world.engine)) == 2

   cli.mode("success")
   clock = Clock(utc_now())
   drain = auto_drain(world, cli, clock, jobs_per_pass=1, board=CooldownBoard())

   assert drain.run_pass().done == 1
   assert sorted(job.state for job in queued_jobs(world.engine)) == [DONE_STATE, QUEUED_CALL_STATE]
   assert drain.run_pass().done == 1
   assert [job.state for job in queued_jobs(world.engine)] == [DONE_STATE, DONE_STATE]


def test_the_pacing_guard_holds_a_pass_back_without_starting_the_cli(world, cli, no_paid_api):
   limited_attempt(world, cli)
   cli.mode("success")
   (cli.home / "fake_claude_record.json").unlink()
   spent_for_today = SubscriptionPacingCaps(calls_per_day={"tutor": 1}, calls_per_minute=10)
   report = auto_drain(world, cli, utc_now, pacing=spent_for_today, board=CooldownBoard()).run_pass()

   assert report.stopped_by == "budget:subscription_calls_per_day"
   assert queued_jobs(world.engine)[0].state == QUEUED_CALL_STATE
   assert not (cli.home / "fake_claude_record.json").exists()


def test_the_running_thread_drains_without_anyone_starting_a_tool(world, cli, no_paid_api):
   _client, _session_id, attempt_id = limited_attempt(world, cli)
   cli.mode("success")
   drain = auto_drain(world, cli, utc_now, interval=timedelta(milliseconds=20), board=CooldownBoard())

   assert drain.start() is True

   deadline = time.monotonic() + 10

   try:
      while attempt_sentence(world.engine, attempt_id) is None and time.monotonic() < deadline:
         time.sleep(0.02)
   finally:
      drain.stop()

   assert attempt_sentence(world.engine, attempt_id) == FAKE_SENTENCE


def test_a_replayed_or_empty_chain_never_drains():
   replayed = (ChainLink(REPLAY_LINK, ReplayProvider(cassette={"text": "canned"})),)
   drain = AutoDrain(None, replayed, {}, CooldownBoard())

   assert can_drain(()) is False
   assert can_drain(replayed) is False
   assert drain.start() is False
   assert drain.run_pass() is None


def test_the_server_starts_the_drain_with_itself_unless_it_is_switched_off(tmp_path):
   env = {"GROWTH_DB_PATH": str(tmp_path / "growth.db"), "GROWTH_ITEMS_DIR": "none"}
   switched_on = build_application(env)
   switched_off = build_application(dict(env, GROWTH_AUTO_DRAIN="off"))

   assert switched_on.state.auto_drain.start in switched_on.router.on_startup
   assert switched_on.state.auto_drain.stop in switched_on.router.on_shutdown
   assert switched_off.router.on_startup == []
   assert auto_drain_enabled({}) is True

   with pytest.raises(ValueError):
      auto_drain_enabled({"GROWTH_AUTO_DRAIN": "sometimes"})


def test_a_pass_sweeps_idle_conversations_and_runs_the_agent_drain(world, cli, no_paid_api):
   cli.mode("consolidate")
   now = utc_now()
   user_id = "USR-agent-drain"

   with OrmSession(world.engine) as db:
      db.add(models.User(id=user_id, created_at=as_iso(now), updated_at=as_iso(now)))
      idle = conversations.open_conversation(db, user_id, "session_item", now - timedelta(minutes=31))
      conversations.append_turn(db, idle, "student", "Where did I stop last time", now - timedelta(minutes=31))
      db.commit()
      idle_id = idle.id

   drain = auto_drain(world, cli, Clock(now), board=CooldownBoard())
   drain.run_pass()
   agent_report = drain.last_agent_report

   assert (agent_report.swept, agent_report.done, agent_report.stopped_by) == (1, 1, None)

   with OrmSession(world.engine) as db:
      conversation = db.get(models.AgentConversation, idle_id)
      job = db.scalars(select(models.Job).where(models.Job.type == JOB_TYPE)).one()

      assert conversation.closed_at is not None
      assert conversation.consolidated_at is not None
      assert job.state == DONE_STATE

   assert "--json-schema" in " ".join(cli.record()["argv"])
