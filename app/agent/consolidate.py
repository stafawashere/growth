"""The consolidation job: one closed conversation becomes proposals to the student's tutor memory
(docs/agent/architecture.md, "The memory store", the Consolidation paragraph, and "Roles, models,
caps and the chain").

enqueue writes one jobs row per conversation under the idempotency key
agent_consolidate:<conversation_id>, so a conversation closed twice is consolidated once. The
payload names the student and the conversation and carries no text, because the jobs table is read
by the export and the purge and a job outlives the turns it points at.

run_job renders prompts/memory/consolidate_v1.md with the conversation's turns, the student's
active entries, the error notes and self-explanations of attempts in the sessions those turns
touched, and the student's skill ids, all JSON-encoded below the marker, and calls the memory role
through the chain it is given, under schemas/agent/consolidation.schema.json. The output is
validated against the schema here as well, because a link that ignores the schema must not reach
apply_proposals with a shape it never promised. app/agent/memory.py apply_proposals then enforces
every content rule and writes the one agent_consolidation_applied audit row; expire_and_resolve
resolves a confusion whose skills are all mastered. The job then marks the conversation consolidated
and deletes the student's turns and conversations older than 30 days.

The retry discipline is app/feedback/drain.py's. A usage limit re-queues the job 30 minutes later
without counting an attempt and ends the pass. A pacing, budget or developer spend cap stop, and a
call refused before the wire, leave the job as it was and end the pass. Any other failure, an
unparseable output or one the schema refuses counts one attempt and re-queues, until
MAX_DRAIN_ATTEMPTS, then the job is failed.

While the student has paused memory no call is made: the job applies no proposals, which still
writes the audit row with zero counts, and finishes, so pausing never spends a subscription call.

The two profile extraction fields, student_terms and stated_requests, are returned on the
ConsolidationOutcome, and finish hands the outcome to app/agent/profile.py compute_profile, which
validates them, recomputes the code fields and writes a new tutor_profiles version only when a value
changed (docs/agent/architecture.md, The self-tuning loop).
"""
import json
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path

import jsonschema
from sqlalchemy import delete, select

from app.agent import conversations, memory, profile
from app.auth.service import as_iso, new_id, utc_now
from app.db import models
from app.feedback.drain import (
   DEV_SPEND_STOP,
   DONE_STATE,
   FAILED_STATE,
   FAILURE_RETRY_AFTER,
   LIMIT_RETRY_AFTER,
   MAX_DRAIN_ATTEMPTS,
   defer_job,
   is_limit_failure,
   requeue_job,
   settle_job,
)
from app.providers.base import CacheSettings, Message, ProviderRequest, RefusedBeforeWire, render_template, split_template
from app.providers.call_queue import QUEUED_CALL_STATE
from app.providers.guard import BudgetStopped, DevSpendCapExceeded, ProviderCallFailed
from app.providers.model_routing import model_for
from app.providers.subscription import SubscriptionLimitReached

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "prompts" / "memory" / "consolidate_v1.md"
SCHEMA_PATH = REPO_ROOT / "schemas" / "agent" / "consolidation.schema.json"

JOB_TYPE = "agent_consolidate"
QUEUED_STATE = QUEUED_CALL_STATE
MEMORY_ROLE = "memory"
MAX_OUTPUT_TOKENS = 1500
PREFIX_CACHE_TTL = "1h"
MEMORY_PROVIDER_OPTIONS = {
   "thinking": {"type": "disabled"},
   "output_config": {"effort": "low"},
}
TURNS_KEPT_FOR = timedelta(days=30)

REQUEUED = "requeued"
HELD = "held"
LIMIT_REASON = "subscription_limit_reached"
REFUSED_BEFORE_WIRE_STOP = "refused_before_wire"
CONVERSATION_MISSING_ERROR = "conversation_missing"
INVALID_OUTPUT_ERROR = "invalid_output"


@dataclass
class ConsolidationOutcome:
   """What one run of a job did. state is done, requeued, failed or held (left untouched);
   stopped_by names why the pass must end, if it must."""

   state: str
   stopped_by: str | None = None
   applied: int = 0
   rejected: int = 0
   student_terms: list = field(default_factory=list)
   stated_requests: list = field(default_factory=list)
   expired: int = 0
   resolved: int = 0
   turns_deleted: int = 0
   conversations_deleted: int = 0


def idempotency_key_for(conversation_id):
   return f"{JOB_TYPE}:{conversation_id}"


def enqueue(db, user_id, conversation, now):
   key = idempotency_key_for(conversation.id)
   existing = db.scalar(select(models.Job).where(models.Job.idempotency_key == key))

   if existing is not None:
      return existing

   stamp = as_iso(now)
   payload = {"user_id": user_id, "conversation_id": conversation.id}
   job = models.Job(
      id=new_id("JOB"),
      type=JOB_TYPE,
      payload=json.dumps(payload, sort_keys=True),
      idempotency_key=key,
      state=QUEUED_STATE,
      not_before=stamp,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(job)
   db.flush()

   return job


def template_text():
   return TEMPLATE_PATH.read_text()


def output_schema():
   return json.loads(SCHEMA_PATH.read_text())


def conversation_turns(db, conversation):
   statement = (
      select(models.AgentTurn)
      .where(models.AgentTurn.conversation_id == conversation.id)
      .where(models.AgentTurn.user_id == conversation.user_id)
      .order_by(models.AgentTurn.created_at, models.AgentTurn.id)
   )

   return db.scalars(statement).all()


def own_notes(db, user_id, turns):
   """The error notes and self-explanations of every attempt in the sessions the conversation's
   turns point at, and only the student's own sessions."""
   attempt_ids = {turn.attempt_id for turn in turns if turn.attempt_id is not None}

   if not attempt_ids:
      return []

   touched_sessions = select(models.Attempt.session_id).where(models.Attempt.id.in_(attempt_ids))
   owned_sessions = (
      select(models.Session.id)
      .where(models.Session.id.in_(touched_sessions))
      .where(models.Session.user_id == user_id)
   )
   attempts = db.scalars(
      select(models.Attempt)
      .where(models.Attempt.session_id.in_(owned_sessions))
      .order_by(models.Attempt.started_at, models.Attempt.id)
   ).all()
   notes = []

   for attempt in attempts:
      for kind in ("error_note", "self_explanation"):
         text = getattr(attempt, kind)
         has_text = text is not None and text.strip() != ""

         if has_text:
            notes.append({"kind": kind, "text": text})

   return notes


def active_skill_ids(db, user_id):
   return sorted(memory.user_skill_ids(db, user_id))


def mastered_skill_ids(db, user_id):
   statement = (
      select(models.SkillState.skill_id)
      .where(models.SkillState.user_id == user_id)
      .where(models.SkillState.mastered == 1)
   )

   return set(db.scalars(statement).all())


def build_request(db, conversation, template, now=None):
   """The memory role's request for one conversation. Every field below the marker is
   JSON-encoded, because every one of them was written by or derived from the student."""
   now = now or utc_now()
   user_id = conversation.user_id
   turns = conversation_turns(db, conversation)
   entries = memory.active_entries(db, user_id, now)
   fields = {
      "turns": json.dumps([{"id": turn.id, "role": turn.role, "text": turn.text} for turn in turns]),
      "active_entries": json.dumps([memory.entry_payload(entry) for entry in entries]),
      "own_notes": json.dumps(own_notes(db, user_id, turns)),
      "active_skill_ids": json.dumps(active_skill_ids(db, user_id)),
   }
   system, _variable_section = split_template(template)
   rendered = render_template(template, fields)

   return ProviderRequest(
      role=MEMORY_ROLE,
      model=model_for(MEMORY_ROLE),
      system=system,
      messages=[Message(role="user", content=rendered)],
      max_output_tokens=MAX_OUTPUT_TOKENS,
      output_schema=output_schema(),
      cache=CacheSettings(prefix_breakpoints=1, ttl=PREFIX_CACHE_TTL),
      provider_options={key: dict(value) for key, value in MEMORY_PROVIDER_OPTIONS.items()},
   )


def parsed_output(text):
   """The output when it parses and the schema accepts it, else None."""
   has_text = text is not None and text.strip() != ""

   if not has_text:
      return None

   try:
      document = json.loads(text)
      jsonschema.validate(document, output_schema())
   except (ValueError, jsonschema.ValidationError):
      return None

   return document


def fail_or_requeue(job, now, error):
   attempts_after_this = (job.attempts_made or 0) + 1
   is_out_of_attempts = attempts_after_this >= MAX_DRAIN_ATTEMPTS

   if is_out_of_attempts:
      job.attempts_made = attempts_after_this
      settle_job(job, FAILED_STATE, now, error)

      return ConsolidationOutcome(FAILED_STATE)

   requeue_job(job, now, FAILURE_RETRY_AFTER, error)

   return ConsolidationOutcome(REQUEUED)


def delete_old_turns(db, user_id, now):
   cutoff = as_iso(now - TURNS_KEPT_FOR)
   old_turns = (models.AgentTurn.user_id == user_id) & (models.AgentTurn.created_at < cutoff)
   old_conversations = (models.AgentConversation.user_id == user_id) & (models.AgentConversation.last_turn_at < cutoff)
   turns_deleted = db.execute(delete(models.AgentTurn).where(old_turns)).rowcount
   conversations_deleted = db.execute(delete(models.AgentConversation).where(old_conversations)).rowcount
   db.flush()

   return turns_deleted, conversations_deleted


def finish(db, job, conversation, proposals, extraction, now):
   user_id = conversation.user_id
   counts = memory.apply_proposals(db, user_id, conversation, proposals, now)
   upkeep = memory.expire_and_resolve(db, user_id, now, mastered_skill_ids(db, user_id))
   stamp = as_iso(now)
   conversation.consolidated_at = stamp
   conversation.updated_at = stamp
   db.flush()

   turns_deleted, conversations_deleted = delete_old_turns(db, user_id, now)
   settle_job(job, DONE_STATE, now)

   outcome = ConsolidationOutcome(
      DONE_STATE,
      applied=counts["applied"],
      rejected=counts["rejected"],
      student_terms=list(extraction.get("student_terms", [])),
      stated_requests=list(extraction.get("stated_requests", [])),
      expired=upkeep["expired"],
      resolved=upkeep["resolved"],
      turns_deleted=turns_deleted,
      conversations_deleted=conversations_deleted,
   )
   profile.compute_profile(db, user_id, now, None, outcome)

   return outcome


def job_conversation(db, job):
   payload = json.loads(job.payload)
   conversation = db.get(models.AgentConversation, payload.get("conversation_id"))
   is_owned = conversation is not None and conversation.user_id == payload.get("user_id")

   return conversation if is_owned else None


def run_job(db, job, chain, now):
   conversation = job_conversation(db, job)

   if conversation is None:
      settle_job(job, FAILED_STATE, now, CONVERSATION_MISSING_ERROR)

      return ConsolidationOutcome(FAILED_STATE)

   is_already_consolidated = conversation.consolidated_at is not None

   if is_already_consolidated:
      settle_job(job, DONE_STATE, now)

      return ConsolidationOutcome(DONE_STATE)

   if memory.is_memory_paused(db, conversation.user_id):
      return finish(db, job, conversation, [], {}, now)

   request = build_request(db, conversation, template_text(), now)

   try:
      result = chain.generate(request)
   except BudgetStopped as stopped:
      return ConsolidationOutcome(HELD, stopped_by=f"budget:{stopped.cap}")
   except DevSpendCapExceeded:
      return ConsolidationOutcome(HELD, stopped_by=DEV_SPEND_STOP)
   except RefusedBeforeWire:
      return ConsolidationOutcome(HELD, stopped_by=REFUSED_BEFORE_WIRE_STOP)
   except (ProviderCallFailed, SubscriptionLimitReached) as raised:
      if is_limit_failure(raised):
         defer_job(job, now, LIMIT_RETRY_AFTER, LIMIT_REASON)

         return ConsolidationOutcome(REQUEUED, stopped_by=LIMIT_REASON)

      return fail_or_requeue(job, now, getattr(raised, "exception_type", type(raised).__name__))

   document = parsed_output(result.text)

   if document is None:
      return fail_or_requeue(job, now, INVALID_OUTPUT_ERROR)

   return finish(db, job, conversation, document["proposals"], document, now)


def close_and_enqueue(db, conversation, now):
   conversations.close_conversation(db, conversation, now)

   return enqueue(db, conversation.user_id, conversation, now)
