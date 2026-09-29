"""The consolidation job and its drain (docs/agent/architecture.md, "The memory store", and
docs/agent/build-plan.md, Slice 6), against tests/fixtures/fake_claude/claude in its consolidate
mode, which returns the structured_output each test writes.

A job applies what passes apply_proposals and counts the rest, marks the conversation consolidated,
resolves a confusion whose skills are mastered and deletes turns older than 30 days. A limit
re-queues the job later and ends the pass; a pacing stop ends the pass and leaves the job as it
was; an output the schema refuses counts one attempt. The job's payload carries no text.
"""
import json
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.agent import consolidate, conversations, memory
from app.agent.drain import drain_agent_jobs, sweep_idle_conversations
from app.auth.service import as_iso
from app.db import models
from app.feedback.drain import LIMIT_RETRY_AFTER
from app.providers.guard import SubscriptionPacingCaps
from app.providers.router import SUBSCRIPTION_LINK, ChainLink, CooldownBoard, FallbackChain
from app.providers.subscription import SubscriptionProvider
from tests.providers.test_subscription import FakeCli

USER_ID = "USR-consolidate"
OTHER_USER_ID = "USR-elsewhere"
NOW = datetime(2026, 10, 1, 12, 0, tzinfo=timezone.utc)
SKILLS = ("BC-SKL-0601", "BC-SKL-0602", "BC-SKL-0301")
MASTERED_SKILL = "BC-SKL-0301"
STUDENT_TEXT = "I keep forgetting which part is the inside function"
AGENT_TEXT = "Which function is applied last when you evaluate it?"


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()
   fake = FakeCli(home)
   fake.mode("consolidate")

   return fake


@pytest.fixture
def db(tmp_path):
   engine = models.make_engine(tmp_path / "consolidate.db")
   stamp = as_iso(NOW)

   with OrmSession(engine) as session:
      for user_id in (USER_ID, OTHER_USER_ID):
         session.add(models.User(id=user_id, created_at=stamp, updated_at=stamp))

      for skill_id in SKILLS:
         session.add(
            models.SkillState(
               user_id=USER_ID,
               skill_id=skill_id,
               snapshot_id="SNP-test",
               beta=0.0,
               fading_stage="unsupported",
               mastered=1 if skill_id == MASTERED_SKILL else 0,
               created_at=stamp,
               updated_at=stamp,
            )
         )

      session.commit()

      yield session


def links_for(cli, pacing=None):
   provider = SubscriptionProvider(environ=cli.environ())

   return (ChainLink(SUBSCRIPTION_LINK, provider, pacing=pacing or SubscriptionPacingCaps()),)


def chain_for(db, cli, pacing=None):
   return FallbackChain(links_for(cli, pacing), db, USER_ID, clock=lambda: NOW, board=CooldownBoard())


def choose_output(cli, proposals, student_terms=(), stated_requests=()):
   document = {
      "proposals": list(proposals),
      "student_terms": list(student_terms),
      "stated_requests": list(stated_requests),
   }
   (cli.home / "fake_claude_structured_output.json").write_text(json.dumps(document))


def closed_conversation(db, user_id=USER_ID, at=NOW - timedelta(hours=1), attempt_id=None):
   conversation = conversations.open_conversation(db, user_id, "session_item", at)
   student = conversations.append_turn(db, conversation, "student", STUDENT_TEXT, at, attempt_id=attempt_id)
   agent = conversations.append_turn(db, conversation, "agent", AGENT_TEXT, at)
   conversations.close_conversation(db, conversation, at)
   db.commit()

   return conversation, [student.id, agent.id]


def stored_entry(db, kind, text, skill_ids=(), **extra):
   stamp = as_iso(NOW - timedelta(days=1))
   entry = models.TutorMemory(
      id=consolidate.new_id("MEM"),
      user_id=USER_ID,
      kind=kind,
      text=text,
      skill_ids=list(skill_ids),
      source=memory.SOURCE_CONVERSATION,
      evidence_count=1,
      last_confirmed_at=stamp,
      last_used_at=stamp,
      created_at=stamp,
      updated_at=stamp,
      edited_by_student=extra.pop("edited_by_student", 0),
      **extra,
   )
   db.add(entry)
   db.commit()

   return entry


def proposal(operation, kind, text, target_id=None, skill_ids=(), evidence_turn_ids=()):
   return {
      "operation": operation,
      "target_id": target_id,
      "kind": kind,
      "text": text,
      "skill_ids": list(skill_ids),
      "evidence_turn_ids": list(evidence_turn_ids),
   }


def drain(db, cli, pacing=None, limit=2):
   return drain_agent_jobs(db, NOW, links_for(cli, pacing), {}, CooldownBoard(), limit=limit)


def agent_jobs(db):
   return db.scalars(select(models.Job).where(models.Job.type == consolidate.JOB_TYPE).order_by(models.Job.created_at)).all()


def test_a_job_applies_what_passes_counts_the_rest_and_marks_the_conversation(db, cli):
   conversation, turn_ids = closed_conversation(db)
   tombstone = stored_entry(db, memory.PREFERENCE, None, deleted_at=as_iso(NOW - timedelta(days=2)))
   edited = stored_entry(db, memory.CONFUSION, "Unsure what the inner function is", ["BC-SKL-0601"], edited_by_student=1)
   mastered_confusion = stored_entry(db, memory.CONFUSION, "Mixes up the two limits", [MASTERED_SKILL])
   choose_output(
      cli,
      [
         proposal("ADD", "preference", "Likes a sketch of the graph first", evidence_turn_ids=turn_ids[:1]),
         proposal("ADD", "preference", "Always give the full working", evidence_turn_ids=turn_ids[:1]),
         proposal("UPDATE", "preference", "Likes a sketch first", target_id=tombstone.id, evidence_turn_ids=turn_ids[:1]),
         proposal("UPDATE", "confusion", "Unsure about the inside part", target_id=edited.id, evidence_turn_ids=turn_ids[:1]),
         proposal("ADD", "episode", "Talked about the chain rule", evidence_turn_ids=["ATN-not-this-conversation"]),
      ],
      student_terms=[{"term": "inside function", "concept_id": "BC-SKL-0601"}],
      stated_requests=["wants_graph_first"],
   )
   job = consolidate.enqueue(db, USER_ID, conversation, NOW)
   db.commit()

   outcome = consolidate.run_job(db, job, chain_for(db, cli), NOW)
   db.commit()

   assert (outcome.state, outcome.applied, outcome.rejected) == ("done", 1, 4)
   assert outcome.student_terms == [{"term": "inside function", "concept_id": "BC-SKL-0601"}]
   assert outcome.stated_requests == ["wants_graph_first"]
   assert outcome.resolved == 1
   assert job.state == "done"
   assert db.get(models.AgentConversation, conversation.id).consolidated_at == as_iso(NOW)

   stored_texts = sorted(entry.text for entry in memory.active_entries(db, USER_ID, NOW))

   assert stored_texts == ["Likes a sketch of the graph first", "Unsure what the inner function is"]
   assert db.get(models.TutorMemory, tombstone.id).text is None
   assert db.get(models.TutorMemory, mastered_confusion.id).resolved_at == as_iso(NOW)

   audit_rows = db.scalars(select(models.AuditLog).where(models.AuditLog.action == memory.CONSOLIDATION_ACTION)).all()

   assert len(audit_rows) == 1
   assert json.loads(audit_rows[0].detail) == {"conversation_id": conversation.id, "applied": 1, "rejected": 4}

   record = cli.record()
   schema_flags = [argument for argument in record["argv"] if argument.startswith("--json-schema=")]

   assert len(schema_flags) == 1
   assert json.loads(schema_flags[0].split("=", 1)[1]) == consolidate.output_schema()
   assert STUDENT_TEXT in record["stdin"]


def test_the_request_carries_notes_only_from_the_conversations_own_sessions(db):
   stamp = as_iso(NOW)

   for session_id, user_id in (("SES-own", USER_ID), ("SES-other", USER_ID), ("SES-foreign", OTHER_USER_ID)):
      db.add(
         models.Session(
            id=session_id,
            user_id=user_id,
            mode="practice",
            started_at=stamp,
            queue="[]",
            snapshot_id="SNP-test",
            created_at=stamp,
            updated_at=stamp,
         )
      )

   notes = (
      ("ATT-own-1", "SES-own", "own note on the pointed attempt"),
      ("ATT-own-2", "SES-own", "own note on a sibling attempt"),
      ("ATT-other", "SES-other", "note from another session"),
      ("ATT-foreign", "SES-foreign", "note from another student"),
   )

   for attempt_id, session_id, note in notes:
      db.add(
         models.Attempt(
            id=attempt_id,
            session_id=session_id,
            item_id="ITM-test",
            started_at=stamp,
            served_stage="unsupported",
            format="mcq",
            per_skill_states="{}",
            error_note=note,
            snapshot_id="SNP-test",
            created_at=stamp,
            updated_at=stamp,
         )
      )

   db.commit()
   conversation, _turn_ids = closed_conversation(db, attempt_id="ATT-own-1")
   conversations.append_turn(db, conversation, "student", "a turn naming a foreign attempt", NOW, attempt_id="ATT-foreign")

   request = consolidate.build_request(db, conversation, consolidate.template_text(), NOW)
   rendered = request.messages[0].content

   assert "own note on the pointed attempt" in rendered
   assert "own note on a sibling attempt" in rendered
   assert "note from another session" not in rendered
   assert "note from another student" not in rendered
   assert (request.role, request.max_output_tokens) == ("memory", 1500)
   assert STUDENT_TEXT not in request.system


def test_an_output_the_schema_refuses_counts_one_attempt_and_requeues(db, cli):
   conversation, _turn_ids = closed_conversation(db)
   (cli.home / "fake_claude_structured_output.json").write_text(json.dumps({"proposals": "none"}))
   consolidate.enqueue(db, USER_ID, conversation, NOW)
   db.commit()

   report = drain(db, cli)
   job = agent_jobs(db)[0]

   assert (report.done, report.requeued, report.stopped_by) == (0, 1, None)
   assert (job.state, job.attempts_made, job.last_error) == ("queued", 1, "invalid_output")
   assert job.not_before > as_iso(NOW)
   assert db.get(models.AgentConversation, conversation.id).consolidated_at is None


def test_a_limit_requeues_later_and_ends_the_pass(db, cli):
   first, _ = closed_conversation(db)
   second, _ = closed_conversation(db)
   consolidate.enqueue(db, USER_ID, first, NOW - timedelta(seconds=1))
   consolidate.enqueue(db, USER_ID, second, NOW)
   db.commit()
   cli.mode("weekly_limit")

   report = drain(db, cli, limit=2)
   limited, untouched = agent_jobs(db)

   assert (report.requeued, report.stopped_by) == (1, "subscription_limit_reached")
   assert (limited.state, limited.attempts_made) == ("queued", 0)
   assert limited.not_before == as_iso(NOW + LIMIT_RETRY_AFTER)
   assert untouched.not_before == as_iso(NOW)
   assert untouched.last_error is None


def test_a_pacing_stop_ends_the_pass_without_touching_the_job(db, cli):
   conversation, _turn_ids = closed_conversation(db)
   consolidate.enqueue(db, USER_ID, conversation, NOW)
   db.commit()
   before = agent_jobs(db)[0]
   snapshot = (before.state, before.attempts_made, before.not_before, before.updated_at, before.last_error)
   spent_for_today = SubscriptionPacingCaps(calls_per_day={"memory": 0}, calls_per_minute=10)

   report = drain(db, cli, pacing=spent_for_today)
   after = agent_jobs(db)[0]

   assert report.stopped_by == "budget:subscription_calls_per_day"
   assert (after.state, after.attempts_made, after.not_before, after.updated_at, after.last_error) == snapshot
   assert not (cli.home / "fake_claude_record.json").exists()


def test_the_job_deletes_turns_and_conversations_older_than_thirty_days(db, cli):
   long_ago = NOW - timedelta(days=31)
   old, _ = closed_conversation(db, at=long_ago)
   recent, _ = closed_conversation(db, at=NOW - timedelta(days=29))
   elsewhere, _ = closed_conversation(db, user_id=OTHER_USER_ID, at=long_ago)
   old_id, recent_id, elsewhere_id = old.id, recent.id, elsewhere.id
   choose_output(cli, [])
   consolidate.enqueue(db, USER_ID, recent, NOW)
   db.commit()

   report = drain(db, cli)
   remaining = set(db.scalars(select(models.AgentConversation.id)).all())
   remaining_turn_owners = set(db.scalars(select(models.AgentTurn.conversation_id)).all())

   assert report.done == 1
   assert remaining == {recent_id, elsewhere_id}
   assert remaining_turn_owners == {recent_id, elsewhere_id}
   assert old_id not in remaining


def test_the_sweep_closes_and_enqueues_only_idle_conversations(db):
   idle = conversations.open_conversation(db, USER_ID, "session_item", NOW - timedelta(minutes=31))
   fresh = conversations.open_conversation(db, USER_ID, "session_item", NOW - timedelta(minutes=5))
   db.commit()

   closed = sweep_idle_conversations(db, NOW)
   db.commit()

   assert closed == 1
   assert db.get(models.AgentConversation, idle.id).closed_at == as_iso(NOW)
   assert db.get(models.AgentConversation, fresh.id).closed_at is None
   assert [json.loads(job.payload)["conversation_id"] for job in agent_jobs(db)] == [idle.id]

   assert sweep_idle_conversations(db, NOW) == 0
   assert len(agent_jobs(db)) == 1


def test_the_job_payload_carries_ids_and_no_text(db):
   conversation, _turn_ids = closed_conversation(db)

   job = consolidate.enqueue(db, USER_ID, conversation, NOW)
   again = consolidate.enqueue(db, USER_ID, conversation, NOW)

   assert again.id == job.id
   assert job.idempotency_key == f"agent_consolidate:{conversation.id}"
   assert json.loads(job.payload) == {"user_id": USER_ID, "conversation_id": conversation.id}
   assert STUDENT_TEXT not in job.payload
   assert AGENT_TEXT not in job.payload


def test_a_paused_memory_consolidates_without_a_call(db, cli):
   conversation, turn_ids = closed_conversation(db)
   memory.set_paused(db, USER_ID, True, NOW)
   choose_output(cli, [proposal("ADD", "preference", "Likes a sketch of the graph first", evidence_turn_ids=turn_ids)])
   consolidate.enqueue(db, USER_ID, conversation, NOW)
   db.commit()

   report = drain(db, cli)

   assert (report.done, report.applied) == (1, 0)
   assert memory.active_entries(db, USER_ID, NOW) == []
   assert not (cli.home / "fake_claude_record.json").exists()
