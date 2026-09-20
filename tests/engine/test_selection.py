"""P1 gating, selection and session assembly tests, named as in docs/plan/11-phased-delivery.md.

Every test but test_never_serve_unmastered_prereq ranges over tests/fixtures/graph_p1.json and its
25 seeded parents. That one test draws its states over the live 618 rows, because 11-phased-delivery
test 21 names the live row count. data/ is read, never written.
"""
import random
from datetime import date, datetime, time, timedelta

from app.engine import constants
from app.engine.fringe import (
   candidates,
   count_unsupported_successes,
   drain_probe_queue,
   enqueue_probe,
   outer_fringe,
   retrieval_eligible,
)
from app.engine.select import format_for_attempt, next_item_learning, next_item_review
from app.engine.state import FadingStage, PendingProbe, ResponseFormat, SkillState
from app.session.build import assemble_session, eligible_records
from tests.engine.conftest_selection import (
   ACCOUNT_CREATED_AT,
   build_bank,
   build_graph,
   build_live_states,
   build_states,
   live_state_rows,
   load_fixture,
   seeded_parent_ids,
)

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0)


def fixture_gating_parents(fixture, skill_id):
   inert = set(fixture["inert_top"])

   return [
      edge["from"]
      for edge in fixture["edges"]
      if edge["to"] == skill_id and edge["type"] == "hard_prerequisite" and edge["from"] not in inert
   ]


def expected_fringe(fixture, states, graph):
   expected = set()

   for record in fixture["skills"]:
      skill_id = record["id"]
      is_unmastered = not states[skill_id].mastered
      gating = [
         edge["from"]
         for edge in fixture["edges"]
         if edge["to"] == skill_id and edge["type"] == "hard_prerequisite"
      ]
      parents_ok = all(
         parent in graph.inert_top or states[parent].mastered
         for parent in gating
      )

      if is_unmastered and parents_ok:
         expected.add(skill_id)

   return expected


def test_fringe_membership():
   fixture = load_fixture()
   graph = build_graph(fixture)
   skill_ids = [record["id"] for record in fixture["skills"]]
   rng = random.Random(11)

   for _ in range(50):
      mastered = {skill for skill in skill_ids if rng.random() < 0.4}
      states = build_states(fixture, mastered=mastered)

      assert set(outer_fringe(states, graph)) == expected_fringe(fixture, states, graph)

   assert graph.inert_top.isdisjoint(set(graph.skills))
   assert all(skill not in graph.inert_top for skill in outer_fringe(build_states(fixture), graph))


def test_retrieval_entry():
   fixture = load_fixture()
   skill_id = fixture["skills"][0]["id"]
   state = SkillState(skill_id, fading_stage=FadingStage.UNSUPPORTED, observation_count=4)
   observations = [
      {"skill_id": skill_id, "stage": FadingStage.COMPLETION, "credited": True, "success": True},
      {"skill_id": skill_id, "stage": FadingStage.UNSUPPORTED, "credited": True, "success": False},
      {"skill_id": skill_id, "stage": FadingStage.UNSUPPORTED, "credited": False, "success": True},
   ]

   before = count_unsupported_successes(observations, skill_id)

   assert before == 0
   assert not retrieval_eligible(state, before)

   observations.append(
      {"skill_id": skill_id, "stage": FadingStage.UNSUPPORTED, "credited": True, "success": True}
   )
   after = count_unsupported_successes(observations, skill_id)

   assert after == constants.RETRIEVAL_ENTRY
   assert retrieval_eligible(state, after)

   stored = SkillState(skill_id, fading_stage=FadingStage.COMPLETION, observation_count=4)

   assert not retrieval_eligible(stored)

   stored.unaided_success_count = constants.RETRIEVAL_ENTRY

   assert retrieval_eligible(stored)


def test_format_alternates():
   archetype_id = "BC-QA-01004"
   attempts = []
   seen = []

   for index in range(6):
      stage = FadingStage.UNSUPPORTED

      if index == 2:
         stage = FadingStage.EXAMPLE

      if index == 3:
         stage = FadingStage.COMPLETION

      served = format_for_attempt(attempts, archetype_id, stage)
      seen.append((stage, served))
      attempts.append({"archetype_id": archetype_id, "stage": stage, "format": served})

   supported = [served for stage, served in seen if stage != FadingStage.UNSUPPORTED]
   unsupported = [served for stage, served in seen if stage == FadingStage.UNSUPPORTED]

   assert supported == [ResponseFormat.SHORT_ANSWER, ResponseFormat.SHORT_ANSWER]
   assert unsupported == [
      ResponseFormat.SHORT_ANSWER,
      ResponseFormat.MCQ,
      ResponseFormat.SHORT_ANSWER,
      ResponseFormat.MCQ,
   ]

   other = format_for_attempt(attempts, "BC-QA-02002", FadingStage.UNSUPPORTED)

   assert other == ResponseFormat.SHORT_ANSWER


def run_trace(fixture, graph, steps):
   states = build_states(fixture)
   bank = build_bank(fixture)
   rng = random.Random(3)
   history = []

   for _ in range(steps):
      selection = next_item_learning(states, graph, bank, [], history, rng, TODAY, now=NOW)

      if selection.item is None:
         break

      history.append(selection.item)
      primary = graph.primary_skill(selection.item["archetype_id"])
      state = states[primary]
      state.observation_count += 1

      if state.observation_count >= 3:
         state.mastered = True

   return [item["id"] for item in history], states


def test_co_requisite_inert():
   fixture = load_fixture()
   loaded = build_graph(fixture, True)
   dropped = build_graph(fixture, False)

   assert loaded.co_requisite_parents == {"BC-SKL-02007": {"BC-SKL-02006"}}
   assert dropped.co_requisite_parents == {}
   assert loaded.hard_parents == dropped.hard_parents

   rng = random.Random(17)
   skill_ids = list(loaded.skills)

   for _ in range(100):
      mastered = {skill for skill in skill_ids if rng.random() < 0.5}
      states = build_states(fixture, mastered=mastered)

      assert outer_fringe(states, loaded) == outer_fringe(states, dropped)

   with_edge, states_with = run_trace(fixture, build_graph(fixture, True), 1000)
   without_edge, states_without = run_trace(fixture, build_graph(fixture, False), 1000)

   assert with_edge == without_edge
   assert states_with == states_without


def block_two_first(fixture, probes):
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture)
   session = assemble_session(states, graph, bank, probes, [], random.Random(5), TODAY, now=NOW)

   return session.block2[0]


def test_pending_probes_drained():
   fixture = load_fixture()
   probe_archetype = "BC-QA-01004"
   fresh = PendingProbe(probe_archetype, "BC-DGN-0001", NOW - timedelta(days=1))
   expired = PendingProbe(
      probe_archetype, "BC-DGN-0002", NOW - timedelta(days=constants.PROBE_TTL_DAYS + 1)
   )

   served = block_two_first(fixture, [fresh])

   assert served["archetype_id"] == probe_archetype
   assert served["is_probe"] is True

   ordinary = block_two_first(fixture, [])

   assert ordinary["archetype_id"] != probe_archetype or ordinary["is_probe"] is False
   assert ordinary["is_probe"] is False

   after_expiry = block_two_first(fixture, [expired])

   assert after_expiry["is_probe"] is False


def test_probe_queue_cap():
   probes = []
   depth = constants.PROBE_QUEUE_MAX

   for index in range(depth + 2):
      enqueue_probe(probes, PendingProbe("BC-QA-01004", f"BC-DGN-{index:04d}", NOW))

      assert len(probes) <= depth

   kept = [probe.diagnosis_id for probe in probes]

   assert kept == [f"BC-DGN-{index:04d}" for index in range(2, depth + 2)]


def test_fail_closed_no_item():
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   draft_archetype = "BC-QA-01008"
   bank = build_bank(fixture, draft_only={draft_archetype})
   fringe = outer_fringe(states, graph)
   available, gaps = candidates(fringe, graph, bank)

   assert draft_archetype not in [record["id"] for record in available]
   assert draft_archetype in gaps

   rng = random.Random(1)
   served = set()

   for _ in range(200):
      selection = next_item_learning(states, graph, bank, [], [], rng, TODAY, now=NOW)

      if selection.item is not None:
         served.add(selection.item["archetype_id"])

   assert draft_archetype not in served


def mastered_review_states(fixture, mastered_skills):
   states = build_states(fixture, mastered=set(mastered_skills))

   for skill_id in states:
      state = states[skill_id]

      if state.mastered:
         state.c = 40
         state.fading_stage = FadingStage.UNSUPPORTED
         state.success_days = {date(2026, 2, 1)}

   return states


def unit_one_review_setup(fixture, retrievability_value=0.5):
   graph = build_graph(fixture)
   review_skills = [record["id"] for record in fixture["skills"] if record["unit"] == "BC-UNIT-01"]
   states = mastered_review_states(fixture, review_skills)
   bank = build_bank(fixture, items_per_archetype=10)
   retrievability = {skill: retrievability_value for skill in review_skills}
   successes = {skill: 1 for skill in review_skills}

   return graph, states, bank, retrievability, successes, review_skills


def block_forecast_total(session, block):
   return sum(session.forecast(item) for item in block)


def test_session_assembly_blocks():
   fixture = load_fixture()
   graph, states, bank, retrievability, successes, _ = unit_one_review_setup(fixture)
   attempts = [
      {
         "archetype_id": "BC-QA-01004",
         "item_id": "BC-QA-01004-V00",
         "minutes": 2.0,
         "corrected": True,
         "attempted_on": TODAY,
      }
   ]

   session = assemble_session(
      states,
      graph,
      bank,
      [],
      attempts,
      random.Random(9),
      TODAY,
      now=NOW,
      retrievability=retrievability,
      unsupported_successes=successes,
   )

   assert session.blocks == [session.block1, session.block2, session.block3, session.block4]
   assert session.served == session.block1 + session.block2 + session.block3
   assert len(session.block1) <= constants.BLOCK1_MAX_ITEMS
   assert block_forecast_total(session, session.block1) <= constants.BLOCK1_MAX_MINUTES
   assert block_forecast_total(session, session.block2) <= constants.BLOCK2_MAX_MINUTES
   assert block_forecast_total(session, session.block3) <= constants.BLOCK3_MAX_MINUTES

   pool = eligible_records(states, graph, bank, successes)

   assert len(pool) > 0
   assert len(session.block3) > 0
   assert all(
      item["archetype_id"] in {record["id"] for record in pool}
      for item in session.block3
   )
   assert session.block4 == ["BC-QA-01004-V00"]

   served_ids = [item["id"] for item in session.served]

   assert len(served_ids) == len(set(served_ids))

   empty = assemble_session(
      build_states(fixture, mastered={record["id"] for record in fixture["skills"]}),
      graph,
      build_bank(fixture),
      [],
      [],
      random.Random(9),
      TODAY,
      now=NOW,
   )

   assert empty.blocks == [[], [], [], []]
   assert empty.is_empty


def test_block3_draws_from_the_eligible_pool():
   """Block 3 must not be emptied by a whole-state pick that lands outside the eligible pool."""
   fixture = load_fixture()
   graph = build_graph(fixture)
   unit_one = [record["id"] for record in fixture["skills"] if record["unit"] == "BC-UNIT-01"]
   unit_two = [record["id"] for record in fixture["skills"] if record["unit"] == "BC-UNIT-02"]
   states = mastered_review_states(fixture, unit_one + unit_two)
   bank = build_bank(fixture, items_per_archetype=10)
   retrievability = {skill: 1.0 for skill in unit_one}
   retrievability.update({skill: 0.5 for skill in unit_two})
   successes = {skill: 1 for skill in unit_one}

   session = assemble_session(
      states,
      graph,
      bank,
      [],
      [],
      random.Random(9),
      TODAY,
      now=NOW,
      retrievability=retrievability,
      unsupported_successes=successes,
   )
   pool_ids = {record["id"] for record in eligible_records(states, graph, bank, successes)}

   assert len(pool_ids) > 0
   assert len(session.block3) > 0
   assert all(item["archetype_id"] in pool_ids for item in session.block3)


def test_session_assembly_serves_hypercorrection_first():
   fixture = load_fixture()
   graph, states, bank, _, successes, review_skills = unit_one_review_setup(fixture)
   nothing_due = {skill: 1.0 for skill in review_skills}

   for skill in review_skills:
      states[skill].c = 0
      states[skill].f = 40

   flagged = graph.primary_skill("BC-QA-01004")
   states[flagged].hypercorrection_due = TODAY
   touching = {
      record["id"]
      for record in graph.archetypes.values()
      if flagged in record["skills"]
   }

   session = assemble_session(
      states,
      graph,
      bank,
      [],
      [],
      random.Random(9),
      TODAY,
      now=NOW,
      retrievability=nothing_due,
      unsupported_successes=successes,
   )

   assert len(session.block1) > 0
   assert session.block1[0]["archetype_id"] in touching


def requeue_session(fixture, graph, bank, retrievability, successes, states, attempts, today, seed):
   return assemble_session(
      states,
      graph,
      bank,
      [],
      attempts,
      random.Random(seed),
      today,
      now=NOW,
      retrievability=retrievability,
      unsupported_successes=successes,
   )


def test_requeue_gap():
   fixture = load_fixture()
   corrected_id = "BC-QA-01004-V00"
   attempts = [
      {
         "archetype_id": "BC-QA-01004",
         "item_id": corrected_id,
         "corrected": True,
         "attempted_on": TODAY,
      }
   ]

   for seed in range(20):
      graph, states, bank, retrievability, successes, _ = unit_one_review_setup(fixture)
      same_day = requeue_session(
         fixture, graph, bank, retrievability, successes, states, attempts, TODAY, seed
      )
      block1_ids = [item["id"] for item in same_day.block1]

      assert corrected_id not in block1_ids

   for gap in range(constants.REQUEUE_GAP_DAYS_MIN, constants.REQUEUE_GAP_DAYS_MAX + 1):
      graph, states, bank, retrievability, successes, _ = unit_one_review_setup(fixture)
      later = TODAY + timedelta(days=gap)
      session = requeue_session(
         fixture, graph, bank, retrievability, successes, states, attempts, later, 4
      )

      assert session.block1[0]["id"] == corrected_id

   graph, states, bank, retrievability, successes, _ = unit_one_review_setup(fixture)
   past_window = TODAY + timedelta(days=constants.REQUEUE_GAP_DAYS_MAX + 1)
   expired = requeue_session(
      fixture, graph, bank, retrievability, successes, states, attempts, past_window, 4
   )

   assert corrected_id not in [item["id"] for item in expired.block1]

   retried = attempts + [
      {
         "archetype_id": "BC-QA-01004",
         "item_id": corrected_id,
         "corrected": False,
         "attempted_on": TODAY + timedelta(days=constants.REQUEUE_GAP_DAYS_MIN),
      }
   ]
   graph, states, bank, retrievability, successes, _ = unit_one_review_setup(fixture)
   after_retry = requeue_session(
      fixture, graph, bank, retrievability, successes, states, retried,
      TODAY + timedelta(days=constants.REQUEUE_GAP_DAYS_MAX), 4
   )

   assert corrected_id not in [item["id"] for item in after_retry.block1]


def test_due_reviews_from_decay():
   """R_k is derived on read, so a decayed skill is due even when no retrievability map is passed."""
   fixture = load_fixture()
   graph, states, bank, _, successes, _ = unit_one_review_setup(fixture)
   flagged = graph.primary_skill("BC-QA-01004")
   touching = {
      record["id"]
      for record in graph.archetypes.values()
      if flagged in record["skills"]
   }
   states[flagged].stability = 5.0
   states[flagged].difficulty = 5.0
   states[flagged].last_practised_at = NOW - timedelta(days=60)

   decayed = assemble_session(
      states,
      graph,
      bank,
      [],
      [],
      random.Random(9),
      TODAY,
      now=NOW,
      unsupported_successes=successes,
   )

   assert len(decayed.block1) > 0
   assert decayed.block1[0]["archetype_id"] in touching

   graph, fresh_states, bank, _, successes, _ = unit_one_review_setup(fixture)
   fresh_states[flagged].stability = 5.0
   fresh_states[flagged].difficulty = 5.0
   fresh_states[flagged].last_practised_at = NOW

   fresh = assemble_session(
      fresh_states,
      graph,
      bank,
      [],
      [],
      random.Random(9),
      TODAY,
      now=NOW,
      unsupported_successes=successes,
   )

   assert fresh.block1 == []


def test_probe_served_without_explicit_now():
   fixture = load_fixture()
   graph = build_graph(fixture)
   states = build_states(fixture)
   bank = build_bank(fixture)
   probe_archetype = "BC-QA-01004"
   probes = [PendingProbe(probe_archetype, "BC-DGN-0003", datetime.combine(TODAY, time(9, 0)))]

   session = assemble_session(states, graph, bank, probes, [], random.Random(5), TODAY)

   assert session.block2[0]["archetype_id"] == probe_archetype
   assert session.block2[0]["is_probe"] is True


def test_interleave_max_two():
   fixture = load_fixture()
   graph = build_graph(fixture)
   bank = build_bank(fixture, items_per_archetype=10)
   single = build_bank(
      fixture,
      draft_only={record["id"] for record in fixture["archetypes"] if record["id"] != "BC-QA-02006"},
      items_per_archetype=10,
   )

   for seed in range(20):
      for supply in (bank, single):
         states = build_states(fixture)
         session = assemble_session(
            states, graph, supply, [], [], random.Random(seed), TODAY, now=NOW
         )
         served = session.block1 + session.block2 + session.block3
         primaries = [graph.primary_skill(item["archetype_id"]) for item in served]

         for index in range(len(primaries) - 2):
            window = primaries[index:index + 3]

            assert len(set(window)) > 1

      assert len(primaries) == constants.MAX_CONSECUTIVE_SAME_SKILL

   requeue_archetype = "BC-QA-02006"
   minute_rows = [
      {"archetype_id": record["id"], "minutes": 0.5}
      for record in fixture["archetypes"]
      for _ in range(constants.FORECAST_MIN_ATTEMPTS)
   ]
   corrected_ids = [f"{requeue_archetype}-V{index:02d}" for index in range(3)]
   corrected_rows = [
      {
         "archetype_id": requeue_archetype,
         "item_id": item_id,
         "minutes": 0.5,
         "corrected": True,
         "attempted_on": TODAY - timedelta(days=constants.REQUEUE_GAP_DAYS_MIN),
      }
      for item_id in corrected_ids
   ]
   graph, states, supply, retrievability, successes, _ = unit_one_review_setup(fixture)
   requeued = assemble_session(
      states,
      graph,
      supply,
      [],
      minute_rows + corrected_rows,
      random.Random(7),
      TODAY,
      now=NOW,
      retrievability=retrievability,
      unsupported_successes=successes,
   )
   block1_ids = [item["id"] for item in requeued.block1]
   block1_primaries = [graph.primary_skill(item["archetype_id"]) for item in requeued.block1]

   assert set(corrected_ids) <= set(block1_ids)

   for index in range(len(block1_primaries) - 2):
      window = block1_primaries[index:index + 3]

      assert len(set(window)) > 1


def assert_gating_held(item, fixture, graph, states):
   primary = graph.primary_skill(item["archetype_id"])

   for parent in fixture_gating_parents(fixture, primary):
      assert states[parent].mastered


def test_never_serve_unmastered_prereq():
   fixture = load_fixture()
   graph = build_graph(fixture)
   bank = build_bank(fixture, items_per_archetype=10)
   rows = live_state_rows()
   rng = random.Random(23)

   assert len(rows) == 618
   assert set(graph.skills) <= set(rows)
   assert set(seeded_parent_ids(fixture)) <= set(rows)

   retrievability = {row: 0.5 for row in rows}
   learning_served = 0
   review_served = 0
   session_served = 0

   for index in range(1000):
      states = build_live_states(rng, mastered_c=40.0)
      selection = next_item_learning(states, graph, bank, [], [], rng, TODAY, now=NOW)

      if selection.item is not None:
         learning_served += 1
         primary = graph.primary_skill(selection.item["archetype_id"])

         assert not states[primary].mastered

         assert_gating_held(selection.item, fixture, graph, states)

      review = next_item_review(
         states, graph, bank, [], [], rng, TODAY, now=NOW, retrievability=retrievability
      )

      if review.item is not None:
         review_served += 1

         assert_gating_held(review.item, fixture, graph, states)

      runs_session = index % 10 == 0

      if not runs_session:
         continue

      session = assemble_session(
         states, graph, bank, [], [], rng, TODAY,
         now=NOW,
         retrievability=retrievability,
      )

      for item in session.served:
         session_served += 1

         assert_gating_held(item, fixture, graph, states)

   assert learning_served > 0
   assert review_served > 0
   assert session_served > 0
