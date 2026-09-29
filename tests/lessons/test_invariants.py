"""The lesson invariants of Slice L2 and L3 as property tests over the live graph, 1,000 cases each
(docs/plan/15-lessons.md, Quality and evaluation; docs/lessons/BUILD-PLAN.md Slices L2 and L3).

Numbering follows the worker brief: L0 no engine state moves, L1 the per-session lesson count, L2
the reading share, L3 a lesson precedes only an item of its concept, L4 band none never inserts,
L5 a deferred concept's next item gets the lesson first, L7 block 3 has no lesson, L11 the
refresher gap, L12 the windows, L14 an LSN-PRQ only after a flipped BC-PRQ. L13 is
tests/lessons/test_plan.py's.

Each case draws a student from the fresh live states (mastery, priors, observations, stuck and
decayed skills), a lesson library over the live concepts and prerequisites, lesson states, the
switch arm and the forecast history, all from one seeded generator.
"""
import copy
import os
import random
from datetime import datetime, timedelta

import pytest
from hypothesis import HealthCheck, Phase, given, settings, strategies as st

from app.engine.state import FadingStage
from app.lessons import constants, gate, refresh
from app.session.build import assemble_session
from app.session.service import interleaving_satisfied
from app.sim import whole_graph
from tests.session.test_lesson_gate import lesson_body

PROPERTY_EXAMPLES = 1000
# A red demonstration may run fewer cases without shrinking; the standing gate never sets it.
DEMONSTRATION_EXAMPLES = os.environ.get("LESSON_INVARIANT_DEMO_EXAMPLES")
TODAY = whole_graph.START_DAY
STATUSES = (None, "unseen", "deferred", "served", "read", "skipped")
PROPERTY = settings(
   max_examples=int(DEMONSTRATION_EXAMPLES) if DEMONSTRATION_EXAMPLES else PROPERTY_EXAMPLES,
   phases=(Phase.generate,) if DEMONSTRATION_EXAMPLES else tuple(Phase),
   deadline=None,
   suppress_health_check=[HealthCheck.function_scoped_fixture, HealthCheck.too_slow],
)


@pytest.fixture(scope="module")
def library():
   return whole_graph.library()


@pytest.fixture(scope="module")
def bank(library):
   return whole_graph.synthetic_bank(library.graph)


@pytest.fixture(scope="module")
def template(library):
   """One body per target, copied from the hand-authored record; plan_lesson reads only its
   structure, so the copies differ in id, target and minutes."""
   graph = library.graph
   concepts = sorted({record["concept"] for record in graph.skills.values()})
   prerequisites = sorted({prerequisite for record in graph.archetypes.values() for prerequisite in record.get("prerequisites") or ()})

   return concepts, prerequisites, lesson_body(concepts[0])


case_parameters = st.fixed_dictionaries({
   "seed": st.integers(min_value=0, max_value=2 ** 31),
   "mastered": st.floats(min_value=0.0, max_value=0.6),
   "observed": st.floats(min_value=0.0, max_value=0.6),
   "beta": st.floats(min_value=-4.0, max_value=4.0),
   "coverage": st.floats(min_value=0.1, max_value=1.0),
   "flipped": st.floats(min_value=0.0, max_value=0.3),
   "stuck": st.floats(min_value=0.0, max_value=0.2),
   "example_first": st.booleans(),
   "ratio": st.one_of(st.none(), st.floats(min_value=0.3, max_value=4.0)),
   "full": st.floats(min_value=0.5, max_value=6.0),
})


def body_for(template_body, target_id, full):
   body = copy.deepcopy(template_body)
   prefix = "LSN-PRQ" if target_id.startswith("BC-PRQ") else "LSN-CON"
   body["id"] = f"{prefix}-{target_id[7:]}"
   body["target_id"] = target_id
   body["read_minutes"] = {"full": full, "brief": full / 2}

   return body


def draw_states(library, rng, parameters):
   states = whole_graph.fresh_states()

   for skill_id, state in states.items():
      is_prerequisite = skill_id.startswith("BC-PRQ")

      if is_prerequisite:
         state.mastered = rng.random() >= parameters["flipped"]
         continue

      state.beta = parameters["beta"] + rng.uniform(-1.0, 1.0)

      if rng.random() < parameters["observed"]:
         state.credited_observation_count = 1
         state.observation_count = 1

      if rng.random() < parameters["mastered"]:
         state.mastered = True
         state.mastered_at = datetime.combine(TODAY - timedelta(days=30), datetime.min.time())
         state.fading_stage = FadingStage.UNSUPPORTED
         state.unaided_success_count = 3
         state.credited_observation_count = max(state.credited_observation_count, 3)

      if rng.random() < parameters["stuck"]:
         state.fading_stage = FadingStage.EXAMPLE
         state.consecutive_failures = 2

   return states


def draw_inputs(library, template, rng, parameters, states):
   concepts, prerequisites, template_body = template
   targets = [target for target in concepts + prerequisites if rng.random() < parameters["coverage"]]
   bodies = {}
   servable = {}
   lesson_states = {}

   for target_id in targets:
      body = body_for(template_body, target_id, parameters["full"])
      bodies[body["id"]] = body
      servable[target_id] = (body["id"], body["version"])
      status = rng.choice(STATUSES)
      served_days_ago = rng.randint(0, 6)

      if status is not None:
         lesson_states[body["id"]] = {
            "status": status,
            "refresher_served_at": (TODAY - timedelta(days=served_days_ago)).isoformat() if rng.random() < 0.5 else None,
            "refresher_due_reason": None,
         }

   ratios = () if parameters["ratio"] is None else (parameters["ratio"],) * constants.LESSON_FORECAST_MIN_COMPLETIONS
   refreshers = refresh.refresher_targets(states, [], lesson_states, TODAY, graph=library.graph, servable=servable)
   chooser = (lambda concept_id, archetype: True) if parameters["example_first"] else None

   return gate.LessonInputs(
      servable=servable,
      bodies=bodies,
      lesson_states=lesson_states,
      completion_ratios=ratios,
      example_first=chooser,
      refreshers=tuple(refreshers),
   )


def draw_case(library, template, parameters):
   rng = random.Random(parameters["seed"])
   states = draw_states(library, rng, parameters)
   inputs = draw_inputs(library, template, rng, parameters, states)

   return states, inputs


def assemble(library, bank, states, inputs, seed):
   return assemble_session(states, library.graph, bank, None, [], random.Random(seed), TODAY, lessons=inputs)


def items_of(block):
   return [entry for entry in block if entry.get("kind") not in ("lesson", "refresher")]


def lessons_of(block):
   return [entry for entry in block if entry.get("kind") == "lesson"]


def item_after(block, entry):
   position = next(index for index, candidate in enumerate(block) if candidate is entry)

   return next(candidate for candidate in block[position + 1:] if candidate.get("kind") == "item")


def concept_skills(graph, concept_id):
   return {skill_id for skill_id, record in graph.skills.items() if record["concept"] == concept_id}


def check_l0(library, bank, states, inputs, seed):
   with_lessons = copy.deepcopy(states)
   without_lessons = copy.deepcopy(states)
   assemble(library, bank, with_lessons, inputs, seed)
   assemble(library, bank, without_lessons, None, seed)

   assert with_lessons == without_lessons
   assert with_lessons == states


def check_l1(session):
   assert len(lessons_of(session.block2)) <= constants.LESSONS_PER_SESSION_MAX
   assert session.refresher_count <= constants.REFRESHERS_PER_SESSION_MAX


def check_l2(session):
   assert session.lesson_minutes <= constants.LESSON_SHARE_MAX * session.forecast_total + 1e-9


def check_l3(session, graph):
   for entry in lessons_of(session.block2):
      item = item_after(session.block2, entry)
      archetype = graph.archetypes[item["archetype_id"]]
      is_prerequisite_lesson = entry["concept_id"].startswith("BC-PRQ")

      assert item["id"] == entry["before_item_id"]

      if is_prerequisite_lesson:
         assert entry["concept_id"] in archetype["prerequisites"]
      else:
         assert set(archetype["skills"]) & concept_skills(graph, entry["concept_id"])


def check_l4(session, states, graph):
   for entry in lessons_of(session.block2):
      item = item_after(session.block2, entry)
      band = gate.lesson_band(graph.archetypes[item["archetype_id"]], states, graph, None)

      assert band != "none"
      assert entry["band"] == band


def check_l7(session):
   assert all(entry.get("kind") not in ("lesson", "refresher") for entry in session.block3)
   assert all(isinstance(entry, str) or entry.get("kind") == "read_again" for entry in session.block4)


@PROPERTY
@given(parameters=case_parameters)
def test_l0_a_lesson_never_changes_an_engine_state(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)

   check_l0(library, bank, states, inputs, parameters["seed"])


@PROPERTY
@given(parameters=case_parameters)
def test_l1_at_most_lessons_per_session_max_lessons_in_block_2(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)

   check_l1(assemble(library, bank, states, inputs, parameters["seed"]))


@PROPERTY
@given(parameters=case_parameters)
def test_l2_the_reading_share_is_at_most_lesson_share_max_of_the_forecast(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)

   check_l2(assemble(library, bank, states, inputs, parameters["seed"]))


@PROPERTY
@given(parameters=case_parameters)
def test_l3_a_lesson_precedes_only_an_item_loading_a_skill_of_its_concept(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)

   check_l3(assemble(library, bank, states, inputs, parameters["seed"]), library.graph)


@PROPERTY
@given(parameters=case_parameters)
def test_l4_band_none_never_inserts(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)
   session = assemble(library, bank, copy.deepcopy(states), inputs, parameters["seed"])

   check_l4(session, states, library.graph)


def only_deferred(inputs, concept_id):
   lesson_id, version = inputs.servable[concept_id]

   return gate.LessonInputs(
      servable={concept_id: (lesson_id, version)},
      bodies={lesson_id: inputs.bodies[lesson_id]},
      lesson_states={lesson_id: {"status": "deferred"}},
   )


def check_l5(session, states, graph, concept_id, lesson_id):
   skills = concept_skills(graph, concept_id)

   for index, entry in enumerate(session.block2):
      is_item = entry.get("kind") == "item"
      loads_concept = is_item and set(graph.archetypes[entry["archetype_id"]]["skills"]) & skills

      if not loads_concept:
         continue

      band = gate.lesson_band(graph.archetypes[entry["archetype_id"]], states, graph, None)
      is_expert = band == "none"

      deferred_here = [
         deferral for deferral in session.lesson_deferrals
         if deferral["before_item_id"] == entry["id"] and deferral["reason"] in ("block_minutes", "reading_share")
      ]
      # The lesson waits again only when its minutes do not fit what is left of block 2 or of
      # the reading share; the count cap cannot bind with one servable lesson.
      is_postponed = len(deferred_here) > 0

      if is_expert or is_postponed:
         assert entry["lesson_link"]["lesson_id"] == lesson_id
      else:
         assert session.block2[index - 1].get("lesson_id") == lesson_id
         assert entry["preceded_by_lesson_id"] == lesson_id

      return


@PROPERTY
@given(parameters=case_parameters)
def test_l5_a_deferred_concepts_next_item_gets_the_lesson_first(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)
   baseline = assemble(library, bank, copy.deepcopy(states), None, parameters["seed"])
   reached = [
      library.graph.skills[skill]["concept"]
      for item in baseline.block2
      for skill in library.graph.archetypes[item["archetype_id"]]["skills"]
      if skill in library.graph.skills and library.graph.skills[skill]["concept"] in inputs.servable
   ]

   if not reached:
      return

   concept_id = reached[0]
   deferred = only_deferred(inputs, concept_id)
   session = assemble(library, bank, copy.deepcopy(states), deferred, parameters["seed"])

   check_l5(session, states, library.graph, concept_id, deferred.servable[concept_id][0])


@PROPERTY
@given(parameters=case_parameters)
def test_l7_block_3_has_no_lesson(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)

   check_l7(assemble(library, bank, states, inputs, parameters["seed"]))


@PROPERTY
@given(parameters=case_parameters, days=st.integers(min_value=0, max_value=10))
def test_l11_a_refresher_never_within_the_gap_of_the_last(library, template, parameters, days):
   states, inputs = draw_case(library, template, parameters)
   last = (TODAY - timedelta(days=days)).isoformat()
   lesson_states = {lesson_id: {"status": "read", "refresher_served_at": last} for lesson_id, _ in inputs.servable.values()}
   targets = refresh.refresher_targets(states, [], lesson_states, TODAY, graph=library.graph, servable=inputs.servable)

   if days < constants.REFRESHER_MIN_GAP_DAYS:
      assert targets == []


def check_l12(with_lessons, without_lessons, graph):
   lessoned = items_of(with_lessons.block2)
   plain = items_of(without_lessons.block2)
   shortfalls = [(entry["position"], entry["rule"]) for entry in with_lessons.shortfalls]

   assert [item["id"] for item in lessoned] == [item["id"] for item in plain[:len(lessoned)]]
   assert [item["id"] for item in with_lessons.served] == [item["id"] for item in with_lessons.block1 + lessoned + with_lessons.block3]
   assert interleaving_satisfied(with_lessons.block1 + with_lessons.block2 + with_lessons.block3, graph, shortfalls) == interleaving_satisfied(with_lessons.served, graph, shortfalls)


@PROPERTY
@given(parameters=case_parameters)
def test_l12_the_windows_are_unchanged_by_lessons(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)
   inputs.refreshers = ()
   with_lessons = assemble(library, bank, copy.deepcopy(states), inputs, parameters["seed"])
   without_lessons = assemble(library, bank, copy.deepcopy(states), None, parameters["seed"])

   check_l12(with_lessons, without_lessons, library.graph)


def check_l14(session, states, graph):
   for entry in lessons_of(session.block2):
      is_prerequisite_lesson = entry["concept_id"].startswith("BC-PRQ")

      if not is_prerequisite_lesson:
         continue

      item = item_after(session.block2, entry)

      assert states[entry["concept_id"]].mastered is False
      assert entry["concept_id"] in graph.archetypes[item["archetype_id"]]["prerequisites"]


@PROPERTY
@given(parameters=case_parameters)
def test_l14_an_lsn_prq_follows_only_a_flipped_bc_prq(library, bank, template, parameters):
   states, inputs = draw_case(library, template, parameters)
   session = assemble(library, bank, copy.deepcopy(states), inputs, parameters["seed"])

   check_l14(session, states, library.graph)
