"""Prerequisite gating, the outer fringe and the candidate set.

Implements the Prerequisite gating and the outer fringe section of docs/plan/02-adaptive-engine.md
and the shared helpers of the Item selection algorithm pseudocode. BC-TOP nodes are inert (R13),
co_requisite edges are loaded into their own mapping that gating and propagation never read, and
seeded assumed-mastered parents count as mastered (R15).
"""
from dataclasses import dataclass, field
from typing import Protocol

from app.engine import constants
from app.engine.prior import p_knowledge, primary_skill
from app.engine.state import FadingStage


class ItemBank(Protocol):
   def has_published_item(self, archetype_id):
      ...

   def published_items(self, archetype_id):
      ...


class DictItemBank:
   """An item bank over plain item dicts. Published means status verified (R18)."""

   def __init__(self, items):
      self._by_archetype = {}

      for item in items:
         self._by_archetype.setdefault(item["archetype_id"], []).append(item)

   def published_items(self, archetype_id):
      return [
         item
         for item in self._by_archetype.get(archetype_id, ())
         if item["status"] == "verified"
      ]

   def has_published_item(self, archetype_id):
      return len(self.published_items(archetype_id)) > 0


@dataclass(frozen=True)
class Graph:
   archetypes: dict
   skills: dict
   hard_parents: dict
   supporting_parents: dict
   co_requisite_parents: dict
   inert_top: frozenset
   _skills_with_archetype: frozenset = field(default=frozenset())
   conversion_pairs: frozenset = field(default=frozenset())

   @classmethod
   def from_records(cls, archetypes, skills, edges, inert_top, conversion_pairs=frozenset()):
      inert = frozenset(inert_top)
      archetype_map = {record["id"]: record for record in archetypes}
      skill_map = {record["id"]: record for record in skills}
      hard_parents = {}
      supporting_parents = {}
      co_requisite_parents = {}

      for edge in edges:
         is_hard = edge["type"] == "hard_prerequisite"
         is_supporting = edge["type"] == "supporting"
         is_co_requisite = edge["type"] == "co_requisite"

         if is_hard:
            hard_parents.setdefault(edge["to"], set()).add(edge["from"])

         if is_supporting:
            supporting_parents.setdefault(edge["to"], set()).add(edge["from"])

         if is_co_requisite:
            co_requisite_parents.setdefault(edge["to"], set()).add(edge["from"])

      loaded = {
         skill
         for record in archetype_map.values()
         for skill in record["skills"]
      }

      return cls(
         archetypes=archetype_map,
         skills=skill_map,
         hard_parents=hard_parents,
         supporting_parents=supporting_parents,
         co_requisite_parents=co_requisite_parents,
         inert_top=inert,
         _skills_with_archetype=frozenset(loaded),
         conversion_pairs=frozenset(conversion_pairs),
      )

   def primary_skill(self, archetype_id):
      return primary_skill(self.archetypes[archetype_id])

   def gating_parents(self, skill_id):
      """Hard prerequisite parents that gate, so every parent but the inert BC-TOP nodes."""
      return [
         parent
         for parent in sorted(self.hard_parents.get(skill_id, ()))
         if parent not in self.inert_top
      ]

   def has_archetype(self, skill_id):
      return skill_id in self._skills_with_archetype

   def primary_unit(self, archetype_id):
      return self.archetypes[archetype_id]["primary_unit"]

   def family(self, archetype_id):
      return self.archetypes[archetype_id]["family"]


def is_mastered(skill_id, states):
   state = states.get(skill_id)

   if state is None:
      return False

   return bool(state.mastered)


def outer_fringe(states, graph):
   fringe = []

   for skill_id in graph.skills:
      is_inert = skill_id in graph.inert_top
      is_unteachable = not graph.has_archetype(skill_id)
      already_mastered = is_mastered(skill_id, states)

      if is_inert or is_unteachable or already_mastered:
         continue

      gating_clear = parents_mastered(skill_id, states, graph)

      if gating_clear:
         fringe.append(skill_id)

   return fringe


def parents_mastered(skill_id, states, graph):
   """Invariant 3: a row is servable only once every gating parent of its primary skill is mastered."""
   return all(
      is_mastered(parent, states)
      for parent in graph.gating_parents(skill_id)
   )


def gated_records(records, states, graph):
   return [
      record
      for record in records
      if parents_mastered(primary_skill(record), states, graph)
   ]


def candidates(fringe, graph, bank):
   """Fringe archetypes with at least one published item, plus the coverage gaps (R18)."""
   on_fringe = set(fringe)
   available = []
   coverage_gaps = []

   for archetype_id, record in graph.archetypes.items():
      is_on_fringe = primary_skill(record) in on_fringe

      if not is_on_fringe:
         continue

      if bank.has_published_item(archetype_id):
         available.append(record)
      else:
         coverage_gaps.append(archetype_id)

   return available, coverage_gaps


def enqueue_probe(probes, probe):
   """R6: the depth cap is enforced here, so an overflowing enqueue drops the oldest probe."""
   probes.append(probe)
   overflow = len(probes) - constants.PROBE_QUEUE_MAX

   if overflow > 0:
      del probes[:overflow]

   return probes


def drain_probe_queue(probes, graph, bank, now):
   """R6: expire, then pop the front probe. Returns the archetype id or None."""
   if probes is None:
      return None

   cutoff_days = constants.PROBE_TTL_DAYS
   live = [
      probe
      for probe in probes
      if (now - probe.enqueued_at).days < cutoff_days
   ]
   del probes[:]
   probes.extend(live)

   if not probes:
      return None

   probe = probes.pop(0)
   archetype_id = probe.archetype_id
   is_servable = archetype_id in graph.archetypes and bank.has_published_item(archetype_id)

   if not is_servable:
      return None

   return archetype_id


def retrievability_of(skill_id, retrievability):
   if retrievability is None:
      return 1.0

   return retrievability.get(skill_id, 1.0)


def is_due(skill_id, states, retrievability, target):
   """Due for review means mastered and below the retention target; nothing unmastered is due."""
   mastered = is_mastered(skill_id, states)
   below_target = retrievability_of(skill_id, retrievability) < target

   return mastered and below_target


def covered_due_skills(archetype, states, graph, today, retrievability=None):
   """The due skills one archetype retires: its loaded skills and their 1-hop hard ancestors."""
   target = constants.desired_retention(today)
   covered = set()

   for skill_id in archetype["skills"]:
      reached = [skill_id] + graph.gating_parents(skill_id)

      for candidate in reached:
         if is_due(candidate, states, retrievability, target):
            covered.add(candidate)

   return covered


def due_coverage(archetype, states, graph, today, retrievability=None):
   return len(covered_due_skills(archetype, states, graph, today, retrievability))


def serve_stage(archetype, states, graph):
   """R32: the bands pick the initial stage only, the stored stage wins once a credited
   observation exists. An uncredited attempt (NOT_ATTEMPTED, a prerequisite gap with no credit)
   moves observation_count but never fading_stage, so the bands stay live until credit lands.
   """
   primary = primary_skill(archetype)
   state = states[primary]
   has_history = state.credited_observation_count > 0

   if has_history:
      return state.fading_stage

   knowledge = p_knowledge(archetype, states, graph.hard_parents)

   if knowledge < constants.STAGE_LOW:
      return FadingStage.EXAMPLE

   if knowledge > constants.STAGE_HIGH:
      return FadingStage.UNSUPPORTED

   return FadingStage.COMPLETION


def count_unsupported_successes(observations, skill_id):
   """Credited successes recorded at stage unsupported, the R33 reading of RETRIEVAL_ENTRY."""
   total = 0

   for record in observations:
      is_skill = record["skill_id"] == skill_id
      at_unsupported = record["stage"] == FadingStage.UNSUPPORTED
      is_credited_success = record.get("credited", True) and record.get("success", False)

      if is_skill and at_unsupported and is_credited_success:
         total += 1

   return total


def retrieval_eligible(state, unsupported_success_count=None):
   """R8, R33: a skill joins the block 3 pool on its first credited success at stage unsupported.

   The stored counter already records only successes credited at stage unsupported, so the current
   fading stage does not enter the test: a skill dropped back to completion after entry stays in
   the pool. The explicit count argument is still accepted for callers that recount observations.
   """
   if unsupported_success_count is not None:
      return unsupported_success_count >= constants.RETRIEVAL_ENTRY

   return state.unaided_success_count >= constants.RETRIEVAL_ENTRY
