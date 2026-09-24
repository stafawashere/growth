"""Learning and review selection, the two-term score of docs/plan/02-adaptive-engine.md (R4).

Candidates are archetypes over the whole loaded graph with at least one published item, the score
is due coverage, and ties and the no-due case are resolved by uniform random choice. The full D3
window of app/engine/interleave.py and, in blocks 2 and 3, the exam-weight quota of
app/engine/exam_weights.py are hard constraints applied before the score, never terms in it.
The five deferred weights of 02 are read nowhere here.
"""
from dataclasses import dataclass
from datetime import datetime, time

from app.engine import constants
from app.engine.exam_weights import filter_exam_weight
from app.engine.fringe import (
   candidates,
   drain_probe_queue,
   due_coverage,
   gated_records,
   is_due,
   outer_fringe,
   serve_stage,
)
from app.engine.interleave import FULL_RULES, window_filter
from app.engine.prior import p_knowledge
from app.engine.retention import current_retrievability
from app.engine.state import FadingStage, ResponseFormat


@dataclass(frozen=True)
class Selection:
   item: dict | None
   coverage_gaps: tuple = ()
   shortfalls: tuple = ()


DEFAULT_RULES = FULL_RULES

REVIEW_RETRIEVAL_FLOOR = 0.5


def session_now(today, now=None):
   """Probe expiry needs a clock, so a caller that passes only a date gets the start of that day."""
   if now is not None:
      return now

   is_datetime = isinstance(today, datetime)

   if is_datetime:
      return today

   return datetime.combine(today, time.min)


def retrievability_map(states, today, retrievability=None):
   """R_k is derived on read, so a caller that passes no map gets the one today's decay implies."""
   if retrievability is not None:
      return retrievability

   return current_retrievability(states, today)


def format_for_attempt(user_attempts, archetype_id, stage):
   """R29: only stage unsupported alternates, and the first unsupported attempt is short answer."""
   at_unsupported = stage == FadingStage.UNSUPPORTED

   if not at_unsupported:
      return ResponseFormat.SHORT_ANSWER

   consumed = 0

   for attempt in user_attempts:
      is_archetype = attempt["archetype_id"] == archetype_id
      counts = attempt["stage"] == FadingStage.UNSUPPORTED

      if is_archetype and counts:
         consumed += 1

   is_even_turn = consumed % 2 == 0

   if is_even_turn:
      return ResponseFormat.SHORT_ANSWER

   return ResponseFormat.MCQ


def filter_interleaving(records, history, graph, rules=DEFAULT_RULES):
   return window_filter(records, history, graph, rules)[0]


def servable_records(records, bank, excluded_ids):
   """Records with an item left to serve, so the window and the quota see only real options."""
   excluded = set(excluded_ids)

   return [
      record
      for record in records
      if any(item["id"] not in excluded for item in bank.published_items(record["id"]))
   ]


def constrained_candidates(records, history, graph, bank, excluded_ids, rules, unit_counts):
   servable = servable_records(records, bank, excluded_ids)
   allowed, shortfalls = window_filter(servable, history, graph, rules)

   return filter_exam_weight(allowed, unit_counts), shortfalls


def dress_item(record, chosen, states, graph, user_attempts, is_probe=False):
   archetype_id = record["id"]
   stage = serve_stage(record, states, graph)
   served = dict(chosen)
   served["stage"] = stage
   served["format"] = format_for_attempt(user_attempts, archetype_id, stage)
   served["is_probe"] = is_probe

   return served


def pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts, is_probe=False):
   archetype_id = record["id"]
   options = [
      item
      for item in bank.published_items(archetype_id)
      if item["id"] not in excluded_ids
   ]

   if not options:
      return None

   chosen = rng.choice(sorted(options, key=lambda item: item["id"]))

   return dress_item(record, chosen, states, graph, user_attempts, is_probe)


def pick_named_item(item_id, archetype_id, states, graph, bank, user_attempts):
   """Serve one named item, the path the corrected-item requeue takes back into block 1."""
   record = graph.archetypes.get(archetype_id)

   if record is None:
      return None

   for item in bank.published_items(archetype_id):
      if item["id"] == item_id:
         return dress_item(record, item, states, graph, user_attempts)

   return None


def choose_by_due_coverage(records, states, graph, today, retrievability, rng):
   if not records:
      return []

   scored = [
      (due_coverage(record, states, graph, today, retrievability), record)
      for record in records
   ]
   best_cover = max(cover for cover, _ in scored)

   if best_cover == 0:
      pool = [record for _, record in scored]
   else:
      pool = [record for cover, record in scored if cover == best_cover]

   ordered = sorted(pool, key=lambda record: record["id"])
   rng.shuffle(ordered)

   return ordered


def next_item_learning(
   states,
   graph,
   bank,
   probes,
   history,
   rng,
   today,
   now=None,
   retrievability=None,
   excluded_ids=(),
   user_attempts=(),
   rules=DEFAULT_RULES,
   unit_counts=None,
   ordering=None,
):
   """unit_counts, when given, is the per-unit tally the exam-weight quota reads (blocks 2 and 3).
   ordering replaces the two-term ordering only in simulation (app/sim/five_term.py); the running
   app never passes one."""
   retrievability = retrievability_map(states, today, retrievability)
   probe_archetype = drain_probe_queue(probes, graph, bank, session_now(today, now))

   if probe_archetype is not None:
      record = graph.archetypes[probe_archetype]
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts, True)

      if served is not None:
         return Selection(served)

   fringe = outer_fringe(states, graph)
   available, coverage_gaps = candidates(fringe, graph, bank)
   allowed, shortfalls = constrained_candidates(
      available, history, graph, bank, excluded_ids, rules, unit_counts
   )
   has_ordering = ordering is not None

   if has_ordering:
      ordered = ordering(allowed, states, graph, today, retrievability, rng, history)
   else:
      ordered = choose_by_due_coverage(allowed, states, graph, today, retrievability, rng)

   for record in ordered:
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts)

      if served is not None:
         return Selection(served, tuple(coverage_gaps), shortfalls)

   return Selection(None, tuple(coverage_gaps))


def due_skills(states, graph, today, retrievability):
   target = constants.desired_retention(today)

   return {
      skill_id
      for skill_id in states
      if is_due(skill_id, states, retrievability, target)
   }


def hypercorrection_skills(states, today):
   return {
      skill_id
      for skill_id, state in states.items()
      if state.hypercorrection_due is not None and state.hypercorrection_due <= today
   }


def reached_skills(record, graph, include_parents):
   reached = set(record["skills"])

   if include_parents:
      for skill_id in record["skills"]:
         reached.update(graph.gating_parents(skill_id))

   return reached


def archetypes_touching(skill_ids, graph, include_parents=False):
   """include_parents widens the reach to 1-hop gating parents, the same reach
   covered_due_skills credits, so an archetype that retires a due skill only as an ancestor
   is still a candidate."""
   return [
      record
      for record in graph.archetypes.values()
      if reached_skills(record, graph, include_parents) & set(skill_ids)
   ]


def review_eligible(pool_skills, states, graph, bank, needs_retrieval=True):
   """Archetypes touching the pool that have a published item (R18) and clear gating.

   A due review is a retrieval opportunity, not a fringe probe, so it also needs p_A of at least
   REVIEW_RETRIEVAL_FLOOR, and it reaches the pool through 1-hop hard ancestors as repetition
   compression does. Hypercorrection overrides the floor, as it overrides the FSRS order, and
   is served only by archetypes loading the flagged skill directly.
   """
   touching = [
      record
      for record in archetypes_touching(pool_skills, graph, include_parents=needs_retrieval)
      if bank.has_published_item(record["id"])
   ]
   gated = gated_records(touching, states, graph)

   if not needs_retrieval:
      return gated

   return [
      record
      for record in gated
      if p_knowledge(record, states, graph.hard_parents) >= REVIEW_RETRIEVAL_FLOOR
   ]


def next_item_review(
   states,
   graph,
   bank,
   probes,
   history,
   rng,
   today,
   now=None,
   retrievability=None,
   excluded_ids=(),
   user_attempts=(),
   rules=DEFAULT_RULES,
):
   retrievability = retrievability_map(states, today, retrievability)
   probe_archetype = drain_probe_queue(probes, graph, bank, session_now(today, now))

   if probe_archetype is not None:
      record = graph.archetypes[probe_archetype]
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts, True)

      if served is not None:
         return Selection(served)

   hyper = hypercorrection_skills(states, today)
   due = due_skills(states, graph, today, retrievability)
   serves_hyper = len(hyper) > 0
   pool_skills = hyper if serves_hyper else due

   if not pool_skills:
      return Selection(None)

   eligible = review_eligible(pool_skills, states, graph, bank, needs_retrieval=not serves_hyper)
   allowed, shortfalls = constrained_candidates(
      eligible, history, graph, bank, excluded_ids, rules, None
   )
   ordered = choose_by_due_coverage(allowed, states, graph, today, retrievability, rng)

   for record in ordered:
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts)

      if served is not None:
         return Selection(served, shortfalls=shortfalls)

   return Selection(None)


def next_item_retrieval(
   pool,
   states,
   graph,
   bank,
   history,
   rng,
   today,
   retrievability=None,
   excluded_ids=(),
   user_attempts=(),
   rules=DEFAULT_RULES,
   unit_counts=None,
):
   """Block 3: the retrieval-eligible pool is the candidate set, not a filter over a wider pick."""
   retrievability = retrievability_map(states, today, retrievability)
   servable = [record for record in pool if bank.has_published_item(record["id"])]
   gated = gated_records(servable, states, graph)
   allowed, shortfalls = constrained_candidates(
      gated, history, graph, bank, excluded_ids, rules, unit_counts
   )
   ordered = choose_by_due_coverage(allowed, states, graph, today, retrievability, rng)

   for record in ordered:
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts)

      if served is not None:
         return Selection(served, shortfalls=shortfalls)

   return Selection(None)