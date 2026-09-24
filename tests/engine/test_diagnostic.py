"""P2 scope item 1: the capped adaptive diagnostic of app/engine/diagnostic.py."""
import math
import random

import pytest

from app.engine import constants, diagnostic
from app.engine.retention import current_retrievability
from app.sim import whole_graph

STUDENTS = 60

LOGIT_SHIFT = {"not_started": -3.0, "partial": 0.0, "fluent": 3.0}


@pytest.fixture(scope="module")
def library():
   return whole_graph.library()


@pytest.fixture(scope="module")
def full_bank(library):
   return whole_graph.synthetic_bank(library.graph)


@pytest.fixture(scope="module")
def runs(full_bank):
   outcomes = []

   for index in range(STUDENTS):
      student = whole_graph.make_student(f"diag-{index}", random.Random(3000 + index))
      outcomes.append((student, whole_graph.run_diagnostic(student, full_bank, seed=3000 + index)))

   return outcomes


def independent_predictive(run, record):
   baseline = run.baseline[record["id"]]
   bounded = min(max(baseline, 1e-6), 1 - 1e-6)
   base_logit = math.log(bounded / (1 - bounded))
   distribution = run.posterior[record["primary_unit"]]
   states = ("not_started", "partial", "fluent")

   return sum(
      weight / (1 + math.exp(-(base_logit + LOGIT_SHIFT[state])))
      for weight, state in zip(distribution, states)
   )


def step_through(student, bank, seed, response_format, check):
   world = whole_graph.library()
   graph = world.graph
   states = whole_graph.fresh_states()
   rng = random.Random(seed)
   world_model = whole_graph.World(whole_graph.student_trajectory(student), random.Random(seed + 1))
   today = whole_graph.START_DAY
   run = diagnostic.start_run(states, graph, bank, current_retrievability(states, today), rng, response_format)

   while True:
      pool = diagnostic.adaptive_pool(run, graph, bank)
      record = diagnostic.next_archetype(run, graph, bank, rng)

      if record is None:
         return run

      check(run, run.pending, pool)
      outcome = whole_graph.diagnostic_outcome(world_model, record, response_format, today, rng)
      diagnostic.record_outcome(run, record, outcome)


@pytest.mark.parametrize("response_format,target", [("short_answer", 0.5), ("mcq", 0.625)])
def test_diagnostic_target_probability(library, full_bank, response_format, target):
   graph = library.graph
   checked = []

   def check(run, entry, pool):
      if entry["held_out"]:
         return

      is_mcq = response_format == "mcq"
      distances = {}

      for record in pool:
         knowledge = independent_predictive(run, record)
         raw = 0.25 + 0.75 * knowledge if is_mcq else knowledge
         distances[record["id"]] = abs(raw - target)

      chosen = entry["archetype_id"]

      assert chosen in distances
      assert distances[chosen] <= min(distances.values()) + constants.DIAG_TIE_BAND + 1e-12
      assert entry["target"] == target
      assert math.isclose(entry["p_a"], independent_predictive(run, graph.archetypes[chosen]), abs_tol=1e-9)
      checked.append(chosen)

   for index in range(10):
      student = whole_graph.make_student(f"target-{index}", random.Random(4000 + index))
      step_through(student, full_bank, 4000 + index, response_format, check)

   assert len(checked) > 100


def test_entropy_stopping(runs):
   stopped_early = 0

   for _, outcome in runs:
      run = outcome.run
      trace = run.entropy_trace
      asked = len(run.asked)

      assert asked <= constants.DIAG_CAP

      if run.stop_reason == diagnostic.STOP_ENTROPY:
         assert asked >= constants.DIAG_MIN
         assert trace[-4] - trace[-1] <= constants.DIAG_ENTROPY_STALL_BITS
         stopped_early += 1

      if run.stop_reason == diagnostic.STOP_CAP:
         assert asked == constants.DIAG_CAP

      assert run.stop_reason in (diagnostic.STOP_ENTROPY, diagnostic.STOP_CAP, diagnostic.STOP_EXHAUSTED)

   assert stopped_early > 0


def test_the_run_stops_as_soon_as_entropy_stalls_and_not_before():
   run = diagnostic.DiagnosticRun(
      units=["BC-UNIT-01"],
      posterior={"BC-UNIT-01": [1 / 3, 1 / 3, 1 / 3]},
      baseline={},
      held_out_position=None,
   )
   run.asked = [{"held_out": False, "outcome": "incorrect"} for _ in range(constants.DIAG_MIN)]
   run.entropy_trace = [5.0, 4.0, 3.0, 2.0, 1.5, 1.2, 1.0, 0.9, 0.80, 0.795, 0.79, 0.785]

   assert diagnostic.stop_reason_before_next(run) == diagnostic.STOP_ENTROPY

   run.entropy_trace[-4] = 0.9

   assert diagnostic.stop_reason_before_next(run) is None

   run.asked = run.asked[:constants.DIAG_MIN - 1]
   run.entropy_trace = [1.0, 1.0, 1.0, 1.0]

   assert diagnostic.stop_reason_before_next(run) is None

   run.asked = [{"held_out": False, "outcome": "incorrect"} for _ in range(constants.DIAG_CAP)]
   run.entropy_trace = [9.0, 6.0, 3.0, 0.0]

   assert diagnostic.stop_reason_before_next(run) == diagnostic.STOP_CAP


def test_exactly_one_held_out_item_and_it_never_moves_the_posterior(runs, library):
   for _, outcome in runs:
      run = outcome.run
      held_out = [entry for entry in run.asked if entry["held_out"]]

      assert len(held_out) == 1
      assert len(run.entropy_trace) == len(run.scored) + 1


def test_record_outcome_leaves_the_posterior_alone_on_the_held_out_item(library, full_bank):
   graph = library.graph
   states = whole_graph.fresh_states()
   rng = random.Random(1)
   run = diagnostic.start_run(states, graph, full_bank, None, rng)
   run.held_out_position = 0
   record = diagnostic.next_archetype(run, graph, full_bank, rng)
   before = {unit: list(values) for unit, values in run.posterior.items()}

   assert run.pending["held_out"]

   diagnostic.record_outcome(run, record, diagnostic.OUTCOME_CORRECT)

   assert run.posterior == before

   record = diagnostic.next_archetype(run, graph, full_bank, rng)
   diagnostic.record_outcome(run, record, diagnostic.OUTCOME_CORRECT)

   assert run.posterior[record["primary_unit"]] != before[record["primary_unit"]]


def test_every_capped_diagnostic_asks_every_unit(runs):
   capped = [outcome.run for _, outcome in runs if outcome.run.stop_reason == diagnostic.STOP_CAP]

   assert capped

   for run in capped:
      assert {entry["unit"] for entry in run.scored} == set(run.units)


def test_no_family_is_asked_twice_and_gating_is_suspended(runs, library):
   graph = library.graph
   gated_somewhere = 0

   for _, outcome in runs:
      families = [entry["family"] for entry in outcome.run.scored]

      assert len(families) == len(set(families))

      fresh = whole_graph.fresh_states()

      for entry in outcome.run.scored:
         primary = graph.primary_skill(entry["archetype_id"])
         parents = graph.gating_parents(primary)
         gated_somewhere += any(not fresh[parent].mastered for parent in parents)

   assert gated_somewhere > 0


def test_placement_masters_only_gated_in_state_skills_it_did_not_see_failed(runs, library):
   graph = library.graph
   placed_total = 0

   for _, outcome in runs:
      run = outcome.run
      states = outcome.states
      failed = diagnostic.failed_in_run(run, graph)

      for skill_id in run.placement["newly_mastered"]:
         assert skill_id not in failed
         assert states[skill_id].mastered
         assert all(states[parent].mastered for parent in graph.gating_parents(skill_id))
         placed_total += 1

   assert placed_total > 0


def test_unresolved_skills_are_left_not_attempted(runs, library):
   graph = library.graph

   for _, outcome in runs:
      run = outcome.run
      placed = set(run.placement["newly_mastered"])
      asked_skills = {
         skill_id
         for entry in run.scored
         for skill_id in graph.archetypes[entry["archetype_id"]]["skills"]
      }
      fresh = whole_graph.fresh_states()

      for skill_id, state in outcome.states.items():
         untouched = skill_id not in placed and skill_id not in asked_skills and skill_id in graph.skills
         was_unmastered = not fresh[skill_id].mastered

         if untouched and was_unmastered:
            assert not state.mastered
            assert state.observation_count == 0


def test_a_re_diagnostic_updates_and_never_resets(library, full_bank):
   student = whole_graph.make_student("returning", random.Random(51))
   first = whole_graph.run_diagnostic(student, full_bank, seed=51)
   before = {
      skill_id: (state.mastered, state.c, state.f, state.observation_count)
      for skill_id, state in first.states.items()
   }
   later = whole_graph.START_DAY.replace(month=whole_graph.START_DAY.month + 1)
   second = whole_graph.run_diagnostic(student, full_bank, seed=52, states=first.states, today=later)
   asked_again = {
      skill_id
      for entry in second.run.scored
      for skill_id in library.graph.archetypes[entry["archetype_id"]]["skills"]
   }

   for skill_id, (was_mastered, c, f, observations) in before.items():
      state = second.states[skill_id]

      assert state.observation_count >= observations
      assert state.c >= c and state.f >= f

      kept_mastery = state.mastered or not was_mastered
      was_seen_again = skill_id in asked_again

      assert kept_mastery or was_seen_again


def test_only_published_archetypes_are_asked_and_the_rest_are_coverage_gaps(library):
   graph = library.graph
   published = sorted(graph.archetypes)[:25]
   bank = whole_graph.synthetic_bank(graph, archetype_ids=published)
   student = whole_graph.make_student("partial-bank", random.Random(8))
   run = whole_graph.run_diagnostic(student, bank, seed=8).run

   assert {entry["archetype_id"] for entry in run.asked} <= set(published)
   assert set(run.coverage_gaps) == set(graph.archetypes) - set(published)
   assert set(run.unprobeable_units) == set(run.units) - {graph.primary_unit(a) for a in published}


def test_no_unit_takes_a_fifth_item_while_a_servable_unit_is_unprobed(library, full_bank):
   graph = library.graph
   states = whole_graph.fresh_states()
   run = diagnostic.start_run(states, graph, full_bank, None, random.Random(2))
   unit_one = sorted(
      (record for record in graph.archetypes.values() if record["primary_unit"] == "BC-UNIT-01"),
      key=lambda record: record["id"],
   )
   distinct_families = []

   for record in unit_one:
      if record["family"] not in {chosen["family"] for chosen in distinct_families}:
         distinct_families.append(record)

   for record in distinct_families[:constants.DIAG_UNIT_POOL_CAP]:
      run.asked.append(diagnostic.entry_for(run, record, 0.5, held_out=False, ties=1))
      diagnostic.record_outcome(run, record, diagnostic.OUTCOME_CORRECT)

   pool_units = {record["primary_unit"] for record in diagnostic.adaptive_pool(run, graph, full_bank)}

   assert "BC-UNIT-01" not in pool_units
   assert len(pool_units) == 9
