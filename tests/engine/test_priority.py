"""Retrievability priority in the engine (docs/pedagogy/today/design.md D1), on the P1 fixture graph."""
import random
from datetime import date, timedelta

from hypothesis import given, settings
from hypothesis import strategies as st

from app.engine.fringe import due_coverage
from app.engine.priority import retrievability_need, retrievability_priority_ordering
from app.engine.retention import current_retrievability
from app.engine.select import choose_by_due_coverage
from tests.engine.conftest_selection import build_graph, build_states, load_fixture

TODAY = date(2026, 10, 1)
FIXTURE = load_fixture()
GRAPH = build_graph(FIXTURE)
SKILL_IDS = sorted({record["id"] for record in FIXTURE["skills"]})
SHUFFLE_SEEDS = range(30)

DECAYED_PARENT = "BC-SKL-01044"
REACHES_DECAYED_PARENT = "BC-QA-01008"
REACHES_ONLY_FRESH = "BC-QA-02007"


def remembered_states(stability=10.0):
   states = build_states(FIXTURE)

   for state in states.values():
      state.stability = stability
      state.last_practised_at = TODAY

   return states


def ordered_ids(records, states, retrievability, seed):
   ordered = retrievability_priority_ordering(
      records, states, GRAPH, TODAY, retrievability, random.Random(seed), []
   )

   return [record["id"] for record in ordered]


memory = st.one_of(
   st.none(),
   st.tuples(st.floats(min_value=0.1, max_value=400.0), st.integers(min_value=0, max_value=365)),
)


@settings(max_examples=150, deadline=None)
@given(
   memories=st.lists(memory, min_size=len(SKILL_IDS), max_size=len(SKILL_IDS)),
   seed=st.integers(0, 10**6),
)
def test_the_ordering_is_sorted_by_need_descending(memories, seed):
   states = build_states(FIXTURE)

   for skill_id, remembered in zip(SKILL_IDS, memories):
      has_memory = remembered is not None

      if has_memory:
         stability, gap_days = remembered
         states[skill_id].stability = stability
         states[skill_id].last_practised_at = TODAY - timedelta(days=gap_days)

   retrievability = current_retrievability(states, TODAY)
   records = list(GRAPH.archetypes.values())
   ordered = retrievability_priority_ordering(
      records, states, GRAPH, TODAY, retrievability, random.Random(seed), []
   )
   needs = [retrievability_need(record, states, GRAPH, retrievability) for record in ordered]

   for earlier, later in zip(needs, needs[1:]):
      assert earlier >= later


def test_a_skill_with_no_stability_contributes_nothing():
   states = build_states(FIXTURE)
   record = GRAPH.archetypes[REACHES_ONLY_FRESH]
   retrievability = {skill_id: 0.2 for skill_id in SKILL_IDS}

   for skill_id in record["skills"]:
      assert states[skill_id].stability is None

   assert retrievability_need(record, states, GRAPH, retrievability) == 0.0


def test_a_decayed_parent_outranks_only_fresh_skills():
   """The parent is left unmastered so it is not due, and due coverage cannot rank it first."""
   states = remembered_states()
   retrievability = {skill_id: 1.0 for skill_id in states}
   retrievability[DECAYED_PARENT] = 0.2
   states[DECAYED_PARENT].mastered = False
   loaded = GRAPH.archetypes[REACHES_DECAYED_PARENT]["skills"]
   records = [GRAPH.archetypes[REACHES_ONLY_FRESH], GRAPH.archetypes[REACHES_DECAYED_PARENT]]

   assert DECAYED_PARENT not in loaded

   for record in records:
      assert due_coverage(record, states, GRAPH, TODAY, retrievability) == 0

   for seed in SHUFFLE_SEEDS:
      order = ordered_ids(records, states, retrievability, seed)

      assert order == [REACHES_DECAYED_PARENT, REACHES_ONLY_FRESH]


def test_with_nothing_decayed_the_order_is_two_terms():
   states = remembered_states()
   retrievability = {skill_id: 1.0 for skill_id in states}
   records = list(reversed(list(GRAPH.archetypes.values())))

   for seed in SHUFFLE_SEEDS:
      two_term = choose_by_due_coverage(records, states, GRAPH, TODAY, retrievability, random.Random(seed))
      priority = retrievability_priority_ordering(
         records, states, GRAPH, TODAY, retrievability, random.Random(seed), []
      )

      assert [record["id"] for record in priority] == [record["id"] for record in two_term]
