"""POST /agent/turns (docs/agent/architecture.md, Streaming end to end; docs/agent/design.md, The
empty state and the degraded states; docs/agent/build-plan.md, Slice 4).

The subscription provider runs the fake claude CLI in its stream modes, wired as the tutor
provider the agent's chain falls back to when no agent_links are configured. The world fixture's
bank ids do not match the screen schema's ITM pattern, so the practice item, its session and the
lesson are written straight into the database. Every stored row is read back from the database,
never from the response.
"""
import json
import logging
import time
from datetime import datetime, timedelta, timezone

import pytest
import sympy
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.agent import copy as agent_copy
from app.agent import turn
from app.agent.screen import decline_text
from app.auth.service import as_iso
from app.content.loader import load_snapshot
from app.db import models
from app.items.mathjson import to_sympy
from app.providers.anthropic import AnthropicProvider
from app.providers.guard import BudgetCaps, SubscriptionPacingCaps, SubscriptionSpendLedger
from app.providers.subscription import SubscriptionProvider
from tests.api.conftest import SNAPSHOT_ID, item_row
from tests.api.test_lessons_routes import RECORD as LESSON_RECORD
from tests.api.test_lessons_routes import store_lesson
from tests.providers.test_subscription import FAKE_CLAUDE, FakeCli

REPO_ROOT = FAKE_CLAUDE.parents[3]
ARCHETYPE_ID = "BC-QA-01004"
ARCHETYPE_NAME = "Limit by algebraic rewrite"
ITEM_ID = "ITM-AGTTURN-01004-00"
SESSION_ID = "SES-" + "0a" * 16
ATTEMPT_ID = "ATT-" + "0b" * 16
STAMP = "2026-09-29T09:00:00+00:00"
MARKER = "MARKER-7f3e"
INTRUDER_ID = "USR-intruder"
PRACTICE_LINE = "Can see: Today, practice item, not checked yet. Cannot see: your answer or the answer key."
FAKE_FIVE_HOUR_WINDOW_SECONDS = 3600
AGENT_CAPS = {"agent": BudgetCaps(cap_usd=1.50, cap_tokens=1_500_000)}
MISSING_BINARY = FAKE_CLAUDE.parent / "no_such_claude"


@pytest.fixture(scope="module")
def snapshot():
   return load_snapshot(REPO_ROOT / "data")


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


@pytest.fixture(autouse=True)
def no_paid_api(monkeypatch):
   def refuse(*args, **kwargs):
      raise AssertionError("the agent must never fall through to the paid API in these tests")

   monkeypatch.setattr(AnthropicProvider, "generate", refuse)
   monkeypatch.setattr(AnthropicProvider, "stream", refuse)


def wire_agent(world, cli, tmp_path, pacing=None, **environ):
   ledger = SubscriptionSpendLedger(path=tmp_path / "subscription_ledger.json")
   world.settings.tutor = SubscriptionProvider(environ=cli.environ(**environ), subscription_ledger=ledger)
   world.settings.subscription_pacing = pacing or SubscriptionPacingCaps()
   world.settings.agent_caps = dict(AGENT_CAPS)
   context = world.settings.session_context
   archetypes = dict(context.archetypes)
   archetypes[ARCHETYPE_ID] = dict(archetypes[ARCHETYPE_ID], name=ARCHETYPE_NAME)
   context.archetypes = archetypes


@pytest.fixture
def agent(world, cli, tmp_path):
   cli.mode("stream")
   wire_agent(world, cli, tmp_path)

   return world


def signed_in(world):
   client = world.client()
   world.register(client)

   with OrmSession(world.engine) as db:
      user_id = db.scalars(select(models.User.id)).one()

   return client, user_id


def seed_practice_item(world, user_id):
   """An unchecked item in a session of this user's. No attempts row exists before submission."""
   archetype = world.settings.session_context.archetypes[ARCHETYPE_ID]
   queue = {"block1": [{"id": ITEM_ID, "archetype_id": ARCHETYPE_ID}], "block2": [], "block3": []}

   with OrmSession(world.engine) as db:
      db.add(item_row(ITEM_ID, ARCHETYPE_ID, archetype["skills"]))
      db.add(
         models.Session(
            id=SESSION_ID,
            user_id=user_id,
            mode="learning",
            sub_mode=None,
            started_at=STAMP,
            ended_at=None,
            queue=json.dumps(queue),
            updates_mastery=1,
            snapshot_id=SNAPSHOT_ID,
            created_at=STAMP,
            updated_at=STAMP,
         )
      )
      db.commit()

   return {
      "kind": "session_item",
      "session_id": SESSION_ID,
      "attempt_id": ATTEMPT_ID,
      "item_id": ITEM_ID,
      "format": "mcq",
      "served_stage": "unsupported",
      "submitted": False,
   }


def practice(world):
   client, user_id = signed_in(world)

   return client, user_id, seed_practice_item(world, user_id)


def post_turn(client, screen, message="I plugged in 3 and got 0/0.", conversation_id=None):
   response = client.post("/agent/turns", json={"conversation_id": conversation_id, "screen": screen, "message": message})

   assert response.status_code == 200

   return response, parsed_events(response.text)


def parsed_events(body):
   events = []

   for frame in body.split("\n\n"):
      is_blank = frame.strip() == ""

      if is_blank:
         continue

      name_line, data_line = frame.split("\n")

      assert name_line.startswith("event: ")
      assert data_line.startswith("data: ")

      events.append((name_line[len("event: "):], json.loads(data_line[len("data: "):])))

   return events


def names_of(events):
   return [name for name, _data in events]


def rows_of(world, model, **filters):
   with OrmSession(world.engine) as db:
      statement = select(model)

      for name, value in filters.items():
         statement = statement.where(getattr(model, name) == value)

      return db.scalars(statement).all()


def agent_turns(world, role):
   with OrmSession(world.engine) as db:
      statement = (
         select(models.AgentTurn)
         .where(models.AgentTurn.role == role)
         .order_by(models.AgentTurn.created_at, models.AgentTurn.id)
      )

      return db.scalars(statement).all()


def cli_was_started(cli):
   return (cli.home / "fake_claude_record.json").exists()


def the_error(events):
   errors = [data for name, data in events if name == "error"]

   assert len(errors) == 1

   return errors[0]


def test_a_practice_turn_streams_start_each_sentence_and_end_in_order(agent):
   client, _user_id, screen = practice(agent)
   response, events = post_turn(client, screen)

   assert response.headers["content-type"].startswith("text/event-stream")
   assert response.headers["cache-control"] == "no-store"
   assert response.headers["x-accel-buffering"] == "no"
   assert names_of(events) == ["start", "text", "text", "end"]

   start, first, second, end = (data for _name, data in events)

   assert start["screen_line"] == PRACTICE_LINE
   assert start["can_see"] == list(screen)
   assert start["conversation_id"].startswith("ACV-")
   assert start["turn_id"].startswith("ATN-")
   assert first == {"delta": "First sentence."}
   assert second == {"delta": " Second sentence?"}
   assert end["outcome"] == "complete"
   assert end["turns_on_item"] == 1
   assert end["turns_in_conversation"] == 1
   assert end["turn_id"] != start["turn_id"]


def test_the_student_and_agent_turns_are_stored_with_the_screen_and_the_outcome(agent):
   client, user_id, screen = practice(agent)
   _response, events = post_turn(client, screen, message="Where do I start?")
   start = events[0][1]
   end = events[-1][1]
   student = agent_turns(agent, "student")
   reply = agent_turns(agent, "agent")

   assert [row.id for row in student] == [start["turn_id"]]
   assert [row.id for row in reply] == [end["turn_id"]]
   assert student[0].text == "Where do I start?"
   assert student[0].screen == screen
   assert student[0].mode == "practice"
   assert student[0].item_id == ITEM_ID
   assert student[0].conversation_id == start["conversation_id"]
   assert student[0].user_id == user_id
   assert reply[0].text == "First sentence. Second sentence?"
   assert reply[0].outcome == "complete"
   assert reply[0].mode == "practice"
   assert reply[0].move == "ask_what_tried"
   assert reply[0].model == "claude-sonnet-5-5"
   assert reply[0].link == "subscription"

   conversation = rows_of(agent, models.AgentConversation, id=start["conversation_id"])[0]

   assert conversation.turn_count == 2
   assert conversation.opened_on_screen == "session_item"


def test_the_screen_line_is_echoed_for_a_lesson_and_for_progress(agent, snapshot):
   agent.settings.session_context.snapshot = snapshot
   store_lesson(agent, "signed_off")
   client, _user_id = signed_in(agent)
   sections = LESSON_RECORD["sections"]
   lesson_screen = {
      "kind": "lesson",
      "lesson_id": LESSON_RECORD["id"],
      "version": 1,
      "section_id": sections[1]["id"],
      "section_index": 1,
      "section_count": len(sections),
      "return_to": "/lessons",
   }
   concept_name = snapshot.concepts[LESSON_RECORD["target_id"]]["name"]
   _response, lesson_events = post_turn(client, lesson_screen, message="Say this part another way.")
   conversation_id = lesson_events[0][1]["conversation_id"]
   _response, progress_events = post_turn(client, {"kind": "progress", "tab": "map"}, message="Where is my map?", conversation_id=conversation_id)

   assert sections[1]["type"] == "orientation"
   assert names_of(lesson_events)[0] == "start"
   assert lesson_events[0][1]["screen_line"] == f"Can see: Lesson, {concept_name}, part 2 of {len(sections)}."
   assert names_of(progress_events)[0] == "start"
   assert progress_events[0][1]["screen_line"] == "Can see: Progress, map."
   assert progress_events[0][1]["conversation_id"] == conversation_id
   assert progress_events[-1][1]["turns_in_conversation"] == 2
   assert [row.move for row in agent_turns(agent, "agent")] == ["explain", "navigate"]


def prediction_screen():
   sections = LESSON_RECORD["sections"]

   return {
      "kind": "lesson",
      "lesson_id": LESSON_RECORD["id"],
      "version": 1,
      "section_id": sections[0]["id"],
      "section_index": 0,
      "section_count": len(sections),
      "return_to": "/lessons",
   }


def test_a_prediction_section_is_practice_counted_per_section_and_its_key_is_withheld(agent, cli, snapshot):
   """LSN-CON-02013 opens with a prediction whose keyed option is B."""
   agent.settings.session_context.snapshot = snapshot
   store_lesson(agent, "signed_off")
   client, _user_id = signed_in(agent)
   screen = prediction_screen()
   _response, first = post_turn(client, screen, message="Which one is it?")
   conversation_id = first[0][1]["conversation_id"]
   cli.mode("stream_leak")
   (cli.home / "fake_claude_stream_text.txt").write_text("So the answer is B. ")
   _response, second = post_turn(client, screen, message="Just tell me.", conversation_id=conversation_id)

   assert LESSON_RECORD["sections"][0]["type"] == "prediction"
   assert first[-1][1]["turns_on_item"] == 1
   assert second[-1][1]["turns_on_item"] == 2
   assert second[-1][1]["outcome"] == "withheld"
   assert [row.mode for row in agent_turns(agent, "student")] == ["practice", "practice"]
   assert agent_turns(agent, "agent")[0].move == "ask_what_tried"


def test_a_timed_part_is_refused_with_kind_timed_and_nothing_stored(agent, cli):
   client, _user_id = signed_in(agent)
   _response, events = post_turn(client, {"kind": "assessments", "format": "mock", "timed": True})

   assert names_of(events) == ["error"]
   assert the_error(events)["kind"] == "timed"
   assert the_error(events)["copy"] == "Not available during a timed part."
   assert agent_turns(agent, "student") == []
   assert not cli_was_started(cli)


def test_the_fourth_practice_turn_on_one_item_reaches_the_ceiling(agent, cli):
   client, _user_id, screen = practice(agent)
   conversation_id = None

   for turn_number in range(1, 4):
      _response, events = post_turn(client, screen, message=f"Attempt number {turn_number}.", conversation_id=conversation_id)
      conversation_id = events[0][1]["conversation_id"]

      assert events[-1][1]["turns_on_item"] == turn_number

   _response, events = post_turn(client, screen, message="And again.", conversation_id=conversation_id)

   assert names_of(events) == ["error"]
   assert the_error(events)["kind"] == "ceiling"
   assert the_error(events)["copy"] == (
      "That is the third question on this item. Check your answer when you are ready, and we can go through it after."
   )
   assert len(agent_turns(agent, "student")) == 3


def add_conversation(world, user_id, conversation_id, student_turns=0, last_turn_at=None):
   stamp = last_turn_at or as_iso(datetime.now(timezone.utc))

   with OrmSession(world.engine) as db:
      db.add(
         models.AgentConversation(
            id=conversation_id,
            user_id=user_id,
            opened_at=stamp,
            last_turn_at=stamp,
            closed_at=None,
            consolidated_at=None,
            opened_on_screen="review",
            turn_count=student_turns * 2,
            created_at=stamp,
            updated_at=stamp,
         )
      )

      for index in range(student_turns):
         for role in ("student", "agent"):
            db.add(
               models.AgentTurn(
                  id=f"ATN-{role}-{index:02d}",
                  conversation_id=conversation_id,
                  user_id=user_id,
                  role=role,
                  text=f"{role} turn {index}",
                  screen={"kind": "review"},
                  mode="browsing",
                  created_at=stamp,
                  updated_at=stamp,
               )
            )

      db.commit()


def test_the_twenty_first_turn_in_one_conversation_reaches_the_ceiling(agent, cli):
   client, user_id = signed_in(agent)
   add_conversation(agent, user_id, "ACV-twenty", student_turns=20)
   _response, events = post_turn(client, {"kind": "review"}, conversation_id="ACV-twenty")

   assert names_of(events) == ["error"]
   assert the_error(events)["kind"] == "ceiling"
   assert the_error(events)["copy"] == agent_copy.CONVERSATION_CEILING
   assert len(agent_turns(agent, "student")) == 20
   assert not cli_was_started(cli)


def test_a_usage_limit_is_an_error_event_with_the_reset_time_from_the_rate_limit_event(agent, cli):
   """The fake stamps the five-hour window's reset an hour past its own clock."""
   cli.mode("stream_limit")
   client, _user_id, screen = practice(agent)
   before = int(time.time())
   _response, events = post_turn(client, screen)
   after = int(time.time())

   assert names_of(events) == ["start", "error"]

   error = the_error(events)
   resets = datetime.fromisoformat(error["resets_at"])

   assert error["kind"] == "usage_limit"
   assert resets.tzinfo is not None
   assert resets.utcoffset() == timedelta(0)
   assert before + FAKE_FIVE_HOUR_WINDOW_SECONDS <= resets.timestamp() <= after + FAKE_FIVE_HOUR_WINDOW_SECONDS
   assert error["resets_at"] == datetime.fromtimestamp(int(resets.timestamp()), timezone.utc).isoformat()
   assert error["copy"] == agent_copy.usage_limit_copy(f"{resets:%H:%M} UTC on {resets.day} {resets:%B}")
   assert "It will answer again after " in error["copy"]
   assert len(agent_turns(agent, "student")) == 1
   assert agent_turns(agent, "agent") == []


def test_the_subscription_daily_cap_is_a_daily_cap_event(world, cli, tmp_path):
   cli.mode("stream")
   wire_agent(world, cli, tmp_path, pacing=SubscriptionPacingCaps(calls_per_day={"agent": 0}))
   client, _user_id, screen = practice(world)
   _response, events = post_turn(client, screen)

   assert names_of(events) == ["start", "error"]
   assert the_error(events)["kind"] == "daily_cap"
   assert the_error(events)["copy"] == (
      "The tutor has used today's allowance and is unavailable for the rest of today. Practice is not affected."
   )
   assert not cli_was_started(cli)


def test_the_subscription_minute_rate_is_a_minute_cap_event(world, cli, tmp_path):
   cli.mode("stream")
   wire_agent(world, cli, tmp_path, pacing=SubscriptionPacingCaps(calls_per_minute_by_role={"agent": 0}))
   client, _user_id, screen = practice(world)
   _response, events = post_turn(client, screen)

   assert names_of(events) == ["start", "error"]
   assert the_error(events)["kind"] == "minute_cap"
   assert the_error(events)["copy"] == "The tutor is answering too many questions at once. Wait a moment and send again."
   assert not cli_was_started(cli)


def test_an_expired_sign_in_is_a_sign_in_event(agent, cli):
   cli.mode("stream_auth")
   client, _user_id, screen = practice(agent)
   _response, events = post_turn(client, screen)

   assert names_of(events) == ["start", "error"]
   assert the_error(events)["kind"] == "sign_in"
   assert the_error(events)["copy"] == (
      "The tutor cannot answer because the Claude sign-in on this computer has expired. Practice is not affected."
   )


def test_a_missing_cli_is_an_unavailable_event(world, cli, tmp_path):
   wire_agent(world, cli, tmp_path, GROWTH_CLAUDE_BIN=str(MISSING_BINARY))
   client, _user_id, screen = practice(world)
   _response, events = post_turn(client, screen)

   assert names_of(events) == ["start", "error"]
   assert the_error(events)["kind"] == "unavailable"
   assert the_error(events)["copy"] == "No connection to the tutor right now. What you typed is kept here."


def test_a_first_text_later_than_the_bound_is_an_unavailable_event(agent, monkeypatch):
   ticks = iter(range(0, 10_000, turn.FIRST_TEXT_BOUND_SECONDS + 1))
   monkeypatch.setattr(turn, "monotonic", lambda: next(ticks))
   client, _user_id, screen = practice(agent)
   _response, events = post_turn(client, screen)

   assert names_of(events) == ["start", "error"]
   assert the_error(events)["kind"] == "unavailable"
   assert agent_turns(agent, "agent") == []


def key_latex(world):
   with OrmSession(world.engine) as db:
      answer_key = json.loads(db.get(models.Item, ITEM_ID).answer_key)

   return sympy.latex(to_sympy(answer_key["mathjson"]))


def leak_the_key(world, cli):
   cli.mode("stream_leak")
   leaking = f"The limit is \\({key_latex(world)}\\) once the factor is gone. "
   (cli.home / "fake_claude_stream_text.txt").write_text(leaking)

   return leaking


def withheld_rows(world):
   return rows_of(world, models.AuditLog, action="agent_reply_withheld")


def test_a_reply_stating_the_key_is_withheld_and_replaced_by_the_decline(agent, cli):
   client, user_id, screen = practice(agent)
   leaking = leak_the_key(agent, cli)
   _response, events = post_turn(client, screen)
   decline = decline_text()

   assert names_of(events) == ["start", "text", "end"]
   assert events[1][1] == {"delta": decline}
   assert events[2][1]["outcome"] == "withheld"

   reply = agent_turns(agent, "agent")

   assert [row.text for row in reply] == [decline]
   assert reply[0].outcome == "withheld"

   audit = withheld_rows(agent)

   assert len(audit) == 1
   assert audit[0].actor == user_id

   detail = json.loads(audit[0].detail)

   assert detail["check"] == "no_answer_before_submission"
   assert detail["turn_id"] == reply[0].id
   assert key_latex(agent) not in audit[0].detail
   assert leaking.strip() not in json.dumps([row.text for row in agent_turns(agent, "student") + reply])

   conversation_id = events[0][1]["conversation_id"]
   _response, again = post_turn(client, screen, message="Why not?", conversation_id=conversation_id)

   assert again[-1][1]["outcome"] == "withheld"
   assert len(withheld_rows(agent)) == 1


def test_a_marked_student_message_reaches_no_log_record_and_no_audit_detail(agent, cli, caplog):
   caplog.set_level(logging.DEBUG)
   client, _user_id, screen = practice(agent)
   message = f"{MARKER} I think the answer is 5/6."
   _response, answered = post_turn(client, screen, message=message)
   conversation_id = answered[0][1]["conversation_id"]
   leak_the_key(agent, cli)
   _response, withheld = post_turn(client, screen, message=message, conversation_id=conversation_id)

   assert answered[-1][1]["outcome"] == "complete"
   assert withheld[-1][1]["outcome"] == "withheld"
   assert len(withheld_rows(agent)) == 1

   for record in caplog.records:
      assert MARKER not in record.getMessage()
      assert MARKER not in repr(record.args)

   for row in rows_of(agent, models.AuditLog):
      assert MARKER not in (row.detail or "")
      assert MARKER not in (row.subject or "")

   turn_lines = [record.getMessage() for record in caplog.records if record.name == "app.agent.turn"]

   assert any(answered[-1][1]["turn_id"] in line and "outcome=complete" in line for line in turn_lines)


def test_a_student_cannot_post_into_another_users_conversation(agent, cli):
   client, _user_id = signed_in(agent)
   add_conversation(agent, INTRUDER_ID, "ACV-intruder", student_turns=1)
   _response, events = post_turn(client, {"kind": "review"}, conversation_id="ACV-intruder")

   assert names_of(events) == ["error"]
   assert the_error(events)["kind"] == "refused"
   assert the_error(events)["status"] == 404
   assert [row.user_id for row in agent_turns(agent, "student")] == [INTRUDER_ID]
   assert rows_of(agent, models.AgentConversation, id="ACV-intruder")[0].turn_count == 2
   assert not cli_was_started(cli)


def test_an_idle_conversation_is_closed_and_enqueued_and_the_turn_opens_a_new_one(agent):
   client, user_id = signed_in(agent)
   idle_since = as_iso(datetime.now(timezone.utc) - timedelta(minutes=31))
   add_conversation(agent, user_id, "ACV-idle", student_turns=1, last_turn_at=idle_since)
   _response, events = post_turn(client, {"kind": "review"}, conversation_id="ACV-idle")
   idle = rows_of(agent, models.AgentConversation, id="ACV-idle")[0]
   jobs = rows_of(agent, models.Job, idempotency_key="agent_consolidate:ACV-idle")

   assert events[0][1]["conversation_id"] != "ACV-idle"
   assert idle.closed_at is not None
   assert len(jobs) == 1


def test_the_panel_closes_a_conversation_and_enqueues_it(agent):
   client, user_id = signed_in(agent)
   add_conversation(agent, user_id, "ACV-open", student_turns=1)
   closed = client.post("/agent/conversations/ACV-open/close")

   assert closed.status_code == 200
   assert rows_of(agent, models.AgentConversation, id="ACV-open")[0].closed_at is not None
   assert len(rows_of(agent, models.Job, idempotency_key="agent_consolidate:ACV-open")) == 1
   assert client.post("/agent/conversations/ACV-missing/close").status_code == 404


def test_the_turn_route_needs_a_session(agent):
   client = agent.client()
   response = client.post("/agent/turns", json={"conversation_id": None, "screen": {"kind": "review"}, "message": "hello"})

   assert response.status_code == 401


PROFILE_TERM = "the undo the zero thing"
PROFILE_CONCEPT = "BC-CON-01008"


def store_profile(world, user_id):
   stamp = STAMP
   body = {
      "opening_move": {},
      "nudge_depth_start": "rule_named",
      "representation_lead": {},
      "student_terms": [{"term": PROFILE_TERM, "concept_id": PROFILE_CONCEPT}],
      "turn_length": "short",
      "help_pattern": {"click_throughs": 0, "requests_before_work": 2, "errors_without_request": 0},
      "stated_requests": ["wants_answer"],
      "provenance": {"turn_length": {"source": "code", "evidence_n": 24, "updated_at": stamp}},
      "profile_version": 1,
   }

   with OrmSession(world.engine) as db:
      db.add(models.TutorProfile(user_id=user_id, version=1, body=body, evidence={}, created_at=stamp, updated_at=stamp))
      db.commit()


def primary_skill_of(world):
   return world.settings.session_context.archetypes[ARCHETYPE_ID]["skills"][0]


def assign_tutor_profile_arm(world, user_id, arm):
   skill_id = primary_skill_of(world)

   with OrmSession(world.engine) as db:
      db.add(
         models.ExperimentAssignment(
            user_id=user_id,
            experiment="tutor_profile",
            unit_id=skill_id,
            arm=arm,
            stratum=skill_id[len("BC-SKL-"):][:2],
            assigned_at=STAMP,
            created_at=STAMP,
            updated_at=STAMP,
         )
      )
      db.commit()


def profile_line(stdin):
   return next(line for line in stdin.splitlines() if line.startswith("Profile: "))


def test_the_profile_is_rendered_into_the_prompt_only_in_the_profile_applied_arm(agent, cli):
   agent.settings.experiment_default_state = {"tutor_profile": "on"}
   client, user_id, screen = practice(agent)
   store_profile(agent, user_id)
   post_turn(client, screen)
   stdin = cli.record()["stdin"]
   rendered = json.loads(profile_line(stdin)[len("Profile: "):])
   student = agent_turns(agent, "student")

   assert rendered["student_terms"] == [{"term": PROFILE_TERM, "concept_id": PROFILE_CONCEPT}]
   assert rendered["turn_length"] == "short"
   assert rendered["nudge_depth_start"] == "concept_only"
   assert "stated_requests" not in stdin
   assert "wants_answer" not in stdin
   assert "provenance" not in stdin
   assert student[0].screen == dict(screen, tutor_profile_arm="profile_applied", tutor_profile_clipped=1)


def test_the_withheld_arm_sends_a_null_profile_and_records_its_arm(agent, cli):
   agent.settings.experiment_default_state = {"tutor_profile": "randomised"}
   client, user_id, screen = practice(agent)
   store_profile(agent, user_id)
   assign_tutor_profile_arm(agent, user_id, "profile_withheld")
   post_turn(client, screen)
   stdin = cli.record()["stdin"]
   student = agent_turns(agent, "student")

   assert profile_line(stdin) == "Profile: null"
   assert PROFILE_TERM not in stdin
   assert "wants_answer" not in stdin
   assert student[0].screen == dict(screen, tutor_profile_arm="profile_withheld")


def test_with_the_switch_off_the_profile_is_null_and_the_screen_is_stored_as_sent(agent, cli):
   client, user_id, screen = practice(agent)
   store_profile(agent, user_id)
   post_turn(client, screen)
   stdin = cli.record()["stdin"]
   student = agent_turns(agent, "student")

   assert profile_line(stdin) == "Profile: null"
   assert PROFILE_TERM not in stdin
   assert "wants_answer" not in stdin
   assert student[0].screen == screen
