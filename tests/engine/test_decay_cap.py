"""The decayed-support cap of docs/plan/02-adaptive-engine.md "Decay": a skill whose R_k has fallen
below 0.5 has its fading_stage capped at completion on its next encounter.

The cap is a served-stage override. fading_stage has one writer, the R7 counter pair, and R32 keeps
serve_stage from competing with it, so the stored stage must come through every case unchanged.
Block 3 is capped like blocks 1 and 2: 02 calls it interleaved mixed review, and the criterion
behaviour 02 keeps free of support is rehearsal's (05), not block 3's.
"""
import random
from datetime import date, datetime, timedelta

import pytest

from app.engine import constants
from app.engine.fringe import serve_stage
from app.engine.prior import primary_skill
from app.engine.retention import current_retrievability
from app.engine.select import next_item_retrieval
from app.engine.state import FadingStage
from app.session.build import assemble_session
from tests.engine.conftest_selection import build_bank, build_graph, build_states, load_fixture

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0)
ARCHETYPE_ID = "BC-QA-01004"


def archetype_of(fixture):
   return next(record for record in fixture["archetypes"] if record["id"] == ARCHETYPE_ID)


def seen_unsupported(state, last_practised_days_ago, stability=2.0):
   state.fading_stage = FadingStage.UNSUPPORTED
   state.credited_observation_count = 4
   state.observation_count = 4
   state.unaided_success_count = 3
   state.c = 40.0
   state.stability = stability
   state.difficulty = 5.0
   state.last_practised_at = NOW - timedelta(days=last_practised_days_ago)


def days_for_retrievability(state, target):
   """The first whole number of days at which the skill's R_k falls below target."""
   for days in range(0, 3650):
      state.last_practised_at = NOW - timedelta(days=days)
      value = current_retrievability({state.skill_id: state}, TODAY)[state.skill_id]

      if value < target:
         return days

   raise AssertionError("R_k never fell below the target")


@pytest.mark.parametrize(
   ("retrievability", "expected"),
   [(0.4, FadingStage.COMPLETION), (0.6, FadingStage.UNSUPPORTED)],
)
def test_the_cap_turns_on_below_one_half_and_leaves_the_stored_stage(retrievability, expected):
   fixture = load_fixture()
   graph = build_graph(fixture)
   archetype = archetype_of(fixture)
   states = build_states(fixture)
   primary = primary_skill(archetype)
   seen_unsupported(states[primary], 30)

   served = serve_stage(archetype, states, graph, {primary: retrievability})

   assert served == expected
   assert states[primary].fading_stage == FadingStage.UNSUPPORTED


def test_a_skill_with_no_credited_observation_is_left_to_the_bands():
   fixture = load_fixture()
   graph = build_graph(fixture)
   archetype = archetype_of(fixture)
   states = build_states(fixture)
   primary = primary_skill(archetype)
   states[primary].fading_stage = FadingStage.UNSUPPORTED
   states[primary].credited_observation_count = 0
   everything_decayed = {skill_id: 0.1 for skill_id in states}

   from_bands = serve_stage(archetype, states, graph)
   decayed = serve_stage(archetype, states, graph, everything_decayed)

   assert decayed == from_bands
   assert states[primary].fading_stage == FadingStage.UNSUPPORTED


def test_the_cap_below_completion_never_raises_the_stage():
   fixture = load_fixture()
   graph = build_graph(fixture)
   archetype = archetype_of(fixture)
   states = build_states(fixture)
   primary = primary_skill(archetype)
   seen_unsupported(states[primary], 30)
   states[primary].fading_stage = FadingStage.EXAMPLE

   assert serve_stage(archetype, states, graph, {primary: 0.1}) == FadingStage.EXAMPLE


def primary_slots(session, primary, graph):
   return [
      (block_index, item)
      for block_index, block in enumerate(session.blocks[:3])
      for item in block
      if graph.primary_skill(item["archetype_id"]) == primary
   ]


@pytest.mark.parametrize(
   ("target", "expected"),
   [(constants.DECAYED_SUPPORT_CAP_RETRIEVABILITY, FadingStage.COMPLETION), (0.8, FadingStage.UNSUPPORTED)],
)
def test_assembly_reads_todays_retrievability_for_the_cap(target, expected):
   """No map is passed in, so the cap fires only if assembly derives R_k itself and hands it on."""
   fixture = load_fixture()
   graph = build_graph(fixture)
   archetype = archetype_of(fixture)
   primary = primary_skill(archetype)
   everything = {record["id"] for record in fixture["skills"]}
   states = build_states(fixture, mastered=everything)
   seen_unsupported(states[primary], 0)
   states[primary].last_practised_at = NOW - timedelta(days=days_for_retrievability(states[primary], target))
   today_r = current_retrievability(states, TODAY)[primary]

   assert today_r < target
   assert today_r < constants.desired_retention(TODAY)
   assert (today_r < constants.DECAYED_SUPPORT_CAP_RETRIEVABILITY) == (expected == FadingStage.COMPLETION)

   session = assemble_session(states, graph, build_bank(fixture), None, [], random.Random(3), TODAY, now=NOW)
   slots = primary_slots(session, primary, graph)

   assert slots, "the decayed skill was never served, so the cap was not measured"
   assert {item["stage"] for _, item in slots} == {expected}
   assert states[primary].fading_stage == FadingStage.UNSUPPORTED


def test_block_three_retrieval_is_capped_too():
   fixture = load_fixture()
   graph = build_graph(fixture)
   archetype = archetype_of(fixture)
   primary = primary_skill(archetype)
   everything_else = {record["id"] for record in fixture["skills"]} - {primary}
   states = build_states(fixture, mastered=everything_else)
   seen_unsupported(states[primary], 0)
   states[primary].last_practised_at = NOW - timedelta(
      days=days_for_retrievability(states[primary], constants.DECAYED_SUPPORT_CAP_RETRIEVABILITY)
   )

   selection = next_item_retrieval([archetype], states, graph, build_bank(fixture), [], random.Random(1), TODAY)

   assert selection.item is not None
   assert selection.item["stage"] == FadingStage.COMPLETION
   assert states[primary].fading_stage == FadingStage.UNSUPPORTED
