"""P2 scope item 4: the full D3 window and the translation floor, over the whole graph.

test_interleave_full_constraints is the gate 11 names: 1,000 simulated sessions, every window
checked by app/engine/interleave.py window_violations, which reads only the served sequence.
"""
import random
from collections import Counter

import pytest

from app.engine.interleave import (
   InterleaveRules,
   is_translation,
   required_translations,
   window_filter,
   window_violations,
)
from app.sim import whole_graph

STUDENTS = 25
DAYS = 40


def unexplained(day_record, pairs):
   explained = {(entry["position"], entry["rule"]) for entry in day_record.session.shortfalls}

   return [
      violation
      for violation in window_violations(day_record.records, pairs)
      if violation not in explained
   ]


def simulate(bank, students, days, seed_base, rules=None):
   sessions = []

   for index in range(students):
      seed = seed_base + index
      student = whole_graph.make_student(f"student-{index}", random.Random(seed))
      placed = whole_graph.run_diagnostic(student, bank, seed=seed)
      history, _, _, _ = whole_graph.run_days(
         student, bank, seed=seed, days=days, states=placed.states, rules=rules
      )
      sessions.extend(history)

   return sessions


@pytest.fixture(scope="module")
def library():
   return whole_graph.library()


def test_interleave_full_constraints(library):
   bank = whole_graph.synthetic_bank(library.graph)
   pairs = library.graph.conversion_pairs
   sessions = simulate(bank, STUDENTS, DAYS, seed_base=500)
   violations = Counter()
   shortfalls = Counter()
   block_items = [0, 0, 0]
   units_seen = set()

   for day_record in sessions:
      for violation in unexplained(day_record, pairs):
         violations[violation[1]] += 1

      for entry in day_record.session.shortfalls:
         shortfalls[entry["rule"]] += 1

      for index in range(3):
         block_items[index] += len(day_record.session.blocks[index])

      units_seen.update(record["primary_unit"] for record in day_record.records)

   assert len(sessions) == STUDENTS * DAYS == 1000
   assert all(count > 0 for count in block_items), block_items
   assert len(units_seen) == 10
   assert dict(violations) == {}
   assert dict(shortfalls) == {}


def test_translation_floor_binds_on_a_bank_where_translations_are_scarce(library):
   graph = library.graph
   pairs = graph.conversion_pairs
   plain = [archetype_id for archetype_id, record in graph.archetypes.items() if not is_translation(record, pairs)]
   translations = sorted(archetype_id for archetype_id, record in graph.archetypes.items() if is_translation(record, pairs))
   bank = whole_graph.synthetic_bank(graph, archetype_ids=plain + translations[::10])
   without_floor = InterleaveRules(translation_floor=False)

   floored = simulate(bank, 10, 20, seed_base=700)
   unfloored = simulate(bank, 10, 20, seed_base=700, rules=without_floor)

   floored_violations = [violation for record in floored for violation in unexplained(record, pairs)]
   unfloored_floor_breaks = [
      violation
      for record in unfloored
      for violation in window_violations(record.records, pairs)
      if violation[1] == "translation_floor"
   ]

   assert floored_violations == []
   assert len(unfloored_floor_breaks) > 0


def test_window_violations_catches_each_rule(library):
   graph = library.graph
   pairs = graph.conversion_pairs
   records = sorted(graph.archetypes.values(), key=lambda record: record["id"])
   plain = [record for record in records if not is_translation(record, pairs)]
   one_record = plain[0]

   repeated = [one_record, one_record, one_record]
   caught = {rule for _, rule in window_violations(repeated, pairs)}

   assert "max_consecutive" in caught

   same_unit = [record for record in plain if record["primary_unit"] == one_record["primary_unit"]][:2]
   alternating = [same_unit[index % 2] for index in range(10)]
   caught = {rule for _, rule in window_violations(alternating, pairs)}

   assert caught == {"block_skills", "block_units", "family_cap", "translation_floor"}


def test_required_translations_is_the_20_percent_floor_of_each_window():
   assert [required_translations(length) for length in range(1, 11)] == [0, 0, 0, 0, 1, 1, 1, 1, 1, 2]


def test_a_soft_rule_no_candidate_can_meet_is_reported_not_silently_dropped(library):
   graph = library.graph
   pairs = graph.conversion_pairs
   plain = sorted(
      (record for record in graph.archetypes.values() if not is_translation(record, pairs)),
      key=lambda record: record["id"],
   )
   history = [{"archetype_id": record["id"]} for record in plain[:4]]
   allowed, shortfalls = window_filter(plain[4:8], history, graph)

   assert allowed
   assert "translation_floor" in shortfalls
