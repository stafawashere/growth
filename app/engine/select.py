"""Learning and review selection, the two-term score of docs/plan/02-adaptive-engine.md (R4).

Candidates are fringe archetypes with at least one published item, the score is due coverage, and
ties and the no-due case are resolved by uniform random choice. Interleaving beyond the
max-2-consecutive-same-primary-skill rule is implemented but held off in P1 (scope item 6).
"""
from dataclasses import dataclass
from datetime import datetime, time

from app.engine import constants
from app.engine.fringe import (
   candidates,
   drain_probe_queue,
   due_coverage,
   gated_records,
   is_mastered,
   outer_fringe,
   retrievability_of,
   serve_stage,
)
from app.engine.prior import p_knowledge, primary_skill
from app.engine.retention import current_retrievability
from app.engine.state import FadingStage, ResponseFormat


@dataclass(frozen=True)
class Selection:
   item: dict | None
   coverage_gaps: tuple = ()


@dataclass(frozen=True)
class InterleaveRules:
   """P1 enforces the max-2 rule only. The rest are wired and default off (scope item 6)."""
   max_consecutive: bool = True
   block_skills: bool = False
   block_units: bool = False
   family_cap: bool = False


DEFAULT_RULES = InterleaveRules()



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
   primaries = [graph.primary_skill(item["archetype_id"]) for item in history]
   filtered = list(records)

   if rules.max_consecutive:
      last_two = primaries[-constants.MAX_CONSECUTIVE_SAME_SKILL:]
      is_run = len(last_two) == constants.MAX_CONSECUTIVE_SAME_SKILL and len(set(last_two)) == 1

      if is_run:
         filtered = [record for record in filtered if primary_skill(record) != last_two[0]]

   block = history[-9:]
   block_primaries = {graph.primary_skill(item["archetype_id"]) for item in block}

   if rules.block_skills:
      too_few_skills = len(block_primaries) < constants.MIN_SKILLS_PER_10 - 1

      if too_few_skills:
         filtered = [record for record in filtered if primary_skill(record) not in block_primaries]

   if rules.block_units:
      block_units = {graph.primary_unit(item["archetype_id"]) for item in block}
      too_few_units = len(block_units) < constants.MIN_UNITS_PER_10

      if too_few_units:
         filtered = [record for record in filtered if record["primary_unit"] not in block_units]

   if rules.family_cap:
      families = [graph.family(item["archetype_id"]) for item in block]
      filtered = [
         record
         for record in filtered
         if families.count(record["family"]) < constants.MAX_FAMILY_PER_10
      ]

   return filtered


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
):
   retrievability = retrievability_map(states, today, retrievability)
   probe_archetype = drain_probe_queue(probes, graph, bank, session_now(today, now))

   if probe_archetype is not None:
      record = graph.archetypes[probe_archetype]
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts, True)

      if served is not None:
         return Selection(served)

   fringe = outer_fringe(states, graph)
   available, coverage_gaps = candidates(fringe, graph, bank)
   allowed = filter_interleaving(available, history, graph, rules)
   ordered = choose_by_due_coverage(allowed, states, graph, today, retrievability, rng)

   for record in ordered:
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts)

      if served is not None:
         return Selection(served, tuple(coverage_gaps))

   return Selection(None, tuple(coverage_gaps))


def due_skills(states, graph, today, retrievability):
   target = constants.desired_retention(today)

   return {
      skill_id
      for skill_id in states
      if is_mastered(skill_id, states) and retrievability_of(skill_id, retrievability) < target
   }


def hypercorrection_skills(states, today):
   return {
      skill_id
      for skill_id, state in states.items()
      if state.hypercorrection_due is not None and state.hypercorrection_due <= today
   }


def archetypes_touching(skill_ids, graph):
   return [
      record
      for record in graph.archetypes.values()
      if any(skill in skill_ids for skill in record["skills"])
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

   touching = [
      record
      for record in archetypes_touching(pool_skills, graph)
      if bank.has_published_item(record["id"])
   ]
   gated = gated_records(touching, states, graph)
   allowed = filter_interleaving(gated, history, graph, rules)

   if serves_hyper:
      retrievable = allowed
   else:
      retrievable = [
         record
         for record in allowed
         if p_knowledge(record, states, graph.hard_parents) >= 0.5
      ]

   ordered = choose_by_due_coverage(retrievable, states, graph, today, retrievability, rng)

   for record in ordered:
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts)

      if served is not None:
         return Selection(served)

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
):
   """Block 3: the retrieval-eligible pool is the candidate set, not a filter over a wider pick."""
   retrievability = retrievability_map(states, today, retrievability)
   servable = [record for record in pool if bank.has_published_item(record["id"])]
   gated = gated_records(servable, states, graph)
   allowed = filter_interleaving(gated, history, graph, rules)
   ordered = choose_by_due_coverage(allowed, states, graph, today, retrievability, rng)

   for record in ordered:
      served = pick_item(record, states, graph, bank, rng, excluded_ids, user_attempts)

      if served is not None:
         return Selection(served)

   return Selection(None)