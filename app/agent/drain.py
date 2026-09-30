"""The agent's share of the automatic drain (docs/agent/architecture.md, "The memory store" and
"Roles, models, caps and the chain"; docs/agent/build-plan.md, Slice 6).

sweep_idle_conversations closes every open conversation idle for 30 minutes and enqueues its
consolidation. A conversation the panel closed is enqueued by the same sweep if nothing enqueued it
yet, since enqueue finds the existing row by its idempotency key and never writes a second.

drain_agent_jobs mirrors app/feedback/drain.py drain_queued_calls: the due agent_consolidate jobs
in the order they were queued, at most AGENT_JOBS_PER_PASS of them, each on the memory role's chain
under the memory caps and the app's shared cooldown board, so a limit the tutor met holds the memory
role back too. Each job is committed on its own, and a stop ends the pass.

app/feedback/autodrain.py reaches the agent only through this module, which keeps the memory store
behind the line tests/agent/test_boundary.py draws.
"""
import json
from dataclasses import dataclass

from sqlalchemy import select

from app.agent import consolidate, conversations
from app.auth.service import as_iso
from app.db import models
from app.providers.router import FallbackChain

AGENT_JOBS_PER_PASS = 2


@dataclass
class AgentDrainReport:
   swept: int = 0
   done: int = 0
   requeued: int = 0
   failed: int = 0
   applied: int = 0
   rejected: int = 0
   stopped_by: str | None = None


def due_jobs(db, now):
   statement = (
      select(models.Job)
      .where(models.Job.type == consolidate.JOB_TYPE)
      .where(models.Job.state == consolidate.QUEUED_STATE)
      .where(models.Job.not_before <= as_iso(now))
      .order_by(models.Job.created_at, models.Job.id)
   )

   return db.scalars(statement).all()


def memory_caps(caps):
   has_memory_caps = consolidate.MEMORY_ROLE in caps

   return {consolidate.MEMORY_ROLE: caps[consolidate.MEMORY_ROLE]} if has_memory_caps else {}


def sweep_idle_conversations(db, now):
   """Closes and enqueues. Returns how many conversations this sweep closed."""
   unconsolidated = select(models.AgentConversation).where(models.AgentConversation.consolidated_at.is_(None))
   closed = 0

   for conversation in db.scalars(unconsolidated).all():
      is_open = conversation.closed_at is None
      is_open_and_idle = is_open and conversations.is_idle(conversation, now)

      if is_open_and_idle:
         consolidate.close_and_enqueue(db, conversation, now)
         closed += 1
         continue

      if not is_open:
         consolidate.enqueue(db, conversation.user_id, conversation, now)

   db.flush()

   return closed


def tally(report, outcome):
   if outcome.state == consolidate.DONE_STATE:
      report.done += 1

   if outcome.state == consolidate.REQUEUED:
      report.requeued += 1

   if outcome.state == consolidate.FAILED_STATE:
      report.failed += 1

   report.applied += outcome.applied
   report.rejected += outcome.rejected


def drain_agent_jobs(db, now, links, caps, board, limit=AGENT_JOBS_PER_PASS):
   report = AgentDrainReport()
   role_caps = memory_caps(caps or {})

   for job in due_jobs(db, now)[:limit]:
      user_id = json.loads(job.payload).get("user_id")
      chain = FallbackChain(links, db, user_id, caps=role_caps, clock=lambda: now, board=board)
      outcome = consolidate.run_job(db, job, chain, now)
      db.commit()
      tally(report, outcome)

      if outcome.stopped_by is not None:
         report.stopped_by = outcome.stopped_by
         break

   return report
