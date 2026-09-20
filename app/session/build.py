"""Four-block session assembly (docs/plan/02-adaptive-engine.md, Session assembly, R5).

Block 1 due reviews, block 2 fringe learning, block 3 interleaved mixed review, block 4 the
calibration and error-note list. The minute forecast is an assembly input only, never a target.
The productive-failure opener is out of P1 scope (R35), so block 2 opens with an ordinary item.

The pending-probe queue is handed to block 2 alone, which is where 11-phased-delivery.md test 15
puts the served probe. The drain path inside next_item_review stays wired for review-mode sessions.

Block 2's fail-closed coverage gaps (R18, docs/plan/06-architecture.md traceability row for the
job worker) are recorded twice: in the session's queue payload, which sessions.service already
writes, and in audit_log, naming the skill left unserved and the reason, which the queue payload
alone does not give an operator a durable, queryable record of. The write reuses app.auth.service's
write_audit rather than a second audit writer, and is a no-op when no db is supplied, so a caller
that only wants the in-memory Session, such as the engine unit tests, is unaffected.
"""
import statistics
from dataclasses import dataclass, field
from datetime import timedelta

from sqlalchemy import select

from app.auth.service import write_audit
from app.db import models
from app.engine import constants
from app.engine.fringe import retrieval_eligible
from app.engine.select import (
   DEFAULT_RULES,
   filter_interleaving,
   next_item_learning,
   next_item_retrieval,
   next_item_review,
   pick_named_item,
   retrievability_map,
   session_now,
)

COVERAGE_GAP_ACTION = "coverage_gap_fail_closed"


@dataclass
class Session:
   block1: list = field(default_factory=list)
   block2: list = field(default_factory=list)
   block3: list = field(default_factory=list)
   block4: list = field(default_factory=list)
   served: list = field(default_factory=list)
   coverage_gaps: tuple = ()
   forecasts: dict = field(default_factory=dict)

   @property
   def blocks(self):
      return [self.block1, self.block2, self.block3, self.block4]

   @property
   def is_empty(self):
      return all(len(block) == 0 for block in self.blocks)

   def forecast(self, item):
      return self.forecasts.get(item["archetype_id"], constants.FORECAST_DEFAULT_MINUTES)


def forecast_minutes(archetype_id, attempts_history):
   times = [
      attempt["minutes"]
      for attempt in attempts_history
      if attempt.get("archetype_id") == archetype_id and attempt.get("minutes") is not None
   ]
   has_enough = len(times) >= constants.FORECAST_MIN_ATTEMPTS

   if not has_enough:
      return constants.FORECAST_DEFAULT_MINUTES

   return statistics.median(times)


def recently_served(attempts_history, today):
   window = timedelta(days=constants.REPEAT_WINDOW_DAYS)
   recent = set()
   corrected = set()

   for attempt in attempts_history:
      attempted_on = attempt.get("attempted_on")
      item_id = attempt.get("item_id")
      has_date = attempted_on is not None and item_id is not None

      if not has_date:
         continue

      is_recent = today - attempted_on <= window

      if is_recent:
         recent.add(item_id)

      if attempt.get("corrected"):
         corrected.add(item_id)

   return recent, corrected


def requeue_ready(attempts_history, today):
   """R5: a corrected item comes back through block 1 once the REQUEUE gap has elapsed.

   The latest correction of an item opens a window from REQUEUE_GAP_DAYS_MIN to
   REQUEUE_GAP_DAYS_MAX days after it. Inside the window the item is served ahead of the FSRS
   order; a retry of the item after the correction, or the window closing, retires the requeue.
   """
   corrected_on = {}
   retried_on = {}

   for attempt in attempts_history:
      attempted_on = attempt.get("attempted_on")
      item_id = attempt.get("item_id")
      has_date = attempted_on is not None and item_id is not None

      if not has_date:
         continue

      is_correction = bool(attempt.get("corrected"))

      if is_correction:
         previous = corrected_on.get(item_id)
         is_later = previous is None or attempted_on > previous[0]

         if is_later:
            corrected_on[item_id] = (attempted_on, attempt.get("archetype_id"))
      else:
         previous_retry = retried_on.get(item_id)
         is_later_retry = previous_retry is None or attempted_on > previous_retry

         if is_later_retry:
            retried_on[item_id] = attempted_on

   ready = []

   for item_id, (date_corrected, archetype_id) in corrected_on.items():
      waited_days = (today - date_corrected).days
      in_window = constants.REQUEUE_GAP_DAYS_MIN <= waited_days <= constants.REQUEUE_GAP_DAYS_MAX
      is_known = archetype_id is not None
      last_retry = retried_on.get(item_id)
      was_retried = last_retry is not None and last_retry > date_corrected

      if in_window and is_known and not was_retried:
         ready.append((date_corrected, item_id, archetype_id))

   return [(item_id, archetype_id) for _, item_id, archetype_id in sorted(ready)]


def gap_already_recorded(db, user_id, archetype_id):
   statement = (
      select(models.AuditLog.id)
      .where(models.AuditLog.action == COVERAGE_GAP_ACTION)
      .where(models.AuditLog.actor == user_id)
      .where(models.AuditLog.subject == f"archetypes:{archetype_id}")
      .limit(1)
   )

   return db.scalars(statement).first() is not None


def write_coverage_gap_audit(db, user_id, archetype_ids, graph):
   """R18: an archetype excluded from block 2 for want of a published item is named by its
   skill, not just its archetype id, because the skill is what an operator needs to go fill.

   One row per user per archetype. The gap persists until the operator authors the item, so a
   row per session opened would grow without bound and would say nothing the first row did not.

   The row is stamped by write_audit with the wall clock rather than with the engine's session
   clock, which is local midnight of `today` whenever the caller supplies no time.
   """
   for archetype_id in archetype_ids:
      if gap_already_recorded(db, user_id, archetype_id):
         continue

      record = graph.archetypes.get(archetype_id)
      skill_id = graph.primary_skill(archetype_id) if record is not None else None
      detail = {
         "archetype_id": archetype_id,
         "skill": skill_id,
         "reason": "no published item for this fringe archetype",
      }
      write_audit(db, user_id, COVERAGE_GAP_ACTION, f"archetypes:{archetype_id}", detail)


def corrected_today(attempts_history, today):
   return [
      attempt["item_id"]
      for attempt in attempts_history
      if attempt.get("corrected") and attempt.get("attempted_on") == today
   ]


def eligible_records(states, graph, bank, unsupported_successes):
   pool = []

   for archetype_id, record in graph.archetypes.items():
      if not bank.has_published_item(archetype_id):
         continue

      primary = graph.primary_skill(archetype_id)
      state = states.get(primary)

      if state is None:
         continue

      count = None

      if unsupported_successes is not None:
         count = unsupported_successes.get(primary, 0)

      if retrieval_eligible(state, count):
         pool.append(record)

   return pool


def assemble_session(
   states,
   graph,
   bank,
   probes,
   attempts_history,
   rng,
   today,
   now=None,
   retrievability=None,
   unsupported_successes=None,
   rules=DEFAULT_RULES,
   db=None,
   user_id=None,
):
   retrievability = retrievability_map(states, today, retrievability)
   now = session_now(today, now)
   history = []
   session = Session()
   recent = recently_served(attempts_history, today)[0]
   requeue = requeue_ready(attempts_history, today)
   ready_ids = {item_id for item_id, _ in requeue}
   blocked_later = set(recent)
   blocked_block1 = set(recent) - ready_ids

   def forecast_for(item):
      archetype_id = item["archetype_id"]

      if archetype_id not in session.forecasts:
         session.forecasts[archetype_id] = forecast_minutes(archetype_id, attempts_history)

      return session.forecasts[archetype_id]

   def serve(block, item):
      block.append(item)
      session.served.append(item)
      history.append(item)
      blocked_later.add(item["id"])
      blocked_block1.add(item["id"])

      return forecast_for(item)

   assembled = 0.0

   def fits(current, item, cap):
      return current + forecast_for(item) <= cap

   pending_requeue = list(requeue)

   def next_requeue_index():
      """R5 keeps the corrected item ahead of the FSRS order, but never past the max-2 rule."""
      for index, (item_id, archetype_id) in enumerate(pending_requeue):
         record = graph.archetypes.get(archetype_id)
         is_served_already = item_id in blocked_block1
         is_unknown = record is None

         if is_served_already or is_unknown:
            continue

         interleaves = len(filter_interleaving([record], history, graph, rules)) > 0

         if interleaves:
            return index

      return None

   while len(session.block1) < constants.BLOCK1_MAX_ITEMS:
      index = next_requeue_index()
      is_requeue_turn = index is not None

      if is_requeue_turn:
         item_id, archetype_id = pending_requeue.pop(index)
         served = pick_named_item(item_id, archetype_id, states, graph, bank, attempts_history)
      else:
         selection = next_item_review(
            states, graph, bank, None, history, rng, today,
            now=now,
            retrievability=retrievability,
            excluded_ids=blocked_block1,
            user_attempts=attempts_history,
            rules=rules,
         )
         served = selection.item

      if served is None:
         if is_requeue_turn:
            continue

         break

      if not fits(assembled, served, constants.BLOCK1_MAX_MINUTES):
         break

      assembled += serve(session.block1, served)

   assembled = 0.0
   gaps = ()

   while True:
      selection = next_item_learning(
         states, graph, bank, probes, history, rng, today,
         now=now,
         retrievability=retrievability,
         excluded_ids=blocked_later,
         user_attempts=attempts_history,
         rules=rules,
      )
      gaps = gaps or selection.coverage_gaps

      if selection.item is None:
         break

      if not fits(assembled, selection.item, constants.BLOCK2_MAX_MINUTES):
         break

      assembled += serve(session.block2, selection.item)

   session.coverage_gaps = gaps
   has_gaps = len(gaps) > 0
   has_audit_target = db is not None and user_id is not None

   if has_gaps and has_audit_target:
      write_coverage_gap_audit(db, user_id, gaps, graph)

   pool = eligible_records(states, graph, bank, unsupported_successes)
   assembled = 0.0

   while assembled < constants.BLOCK3_MIN_MINUTES:
      selection = next_item_retrieval(
         pool, states, graph, bank, history, rng, today,
         retrievability=retrievability,
         excluded_ids=blocked_later,
         user_attempts=attempts_history,
         rules=rules,
      )

      if selection.item is None:
         break

      if not fits(assembled, selection.item, constants.BLOCK3_MAX_MINUTES):
         break

      assembled += serve(session.block3, selection.item)

   session.block4 = corrected_today(attempts_history, today)

   return session
