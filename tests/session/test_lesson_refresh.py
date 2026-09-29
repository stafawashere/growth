"""Refreshers, docs/plan/15-lessons.md Re-teaching: one test per trigger T1 to T4, the gap rule,
the per-session cap, and a block 3 match turned into a "Read again" entry in block 4."""
import random
from datetime import date, timedelta

from app.engine.state import FadingStage, MasteryState
from app.engine.update import Observation, apply_observation
from app.lessons import constants, refresh
from app.session.build import assemble_session
from tests.engine.conftest_selection import build_bank, build_graph, build_states, load_fixture
from tests.session.test_lesson_gate import lesson_inputs
from tests.session.test_service import engine_graph_from

TODAY = date(2026, 3, 1)
ARCHETYPE = "BC-QA-02011"
SKILL = "BC-SKL-02012"
CONCEPT = "BC-CON-02005"


def world():
   fixture = load_fixture()

   return fixture, build_graph(fixture), build_states(fixture)


def servable(*concept_ids):
   return lesson_inputs(list(concept_ids)).servable


def targets_for(states, graph, history=(), lesson_states=None, gaps=(), retrievability=None):
   return refresh.refresher_targets(
      states,
      list(history),
      lesson_states or {},
      TODAY,
      graph=graph,
      servable=servable(CONCEPT),
      prerequisite_gaps=gaps,
      retrievability=retrievability,
   )


def test_t1_fires_on_a_skill_that_lost_mastery_and_failed_since():
   _, graph, states = world()
   state = states[SKILL]
   state.unaided_success_count = 3
   state.consecutive_failures = 1
   state.fading_stage = FadingStage.UNSUPPORTED
   history = [{"archetype_id": ARCHETYPE, "item_id": f"{ARCHETYPE}-V00", "attempted_on": TODAY - timedelta(days=1), "corrected": True}]

   assert [(target.reason, target.concept_id) for target in targets_for(states, graph, history)] == [("T1", CONCEPT)]
   assert targets_for(states, graph, []) == []


def test_t2_fires_on_a_mastered_skill_below_the_decayed_support_cap():
   _, graph, states = world()
   states[SKILL].mastered = True
   states[SKILL].fading_stage = FadingStage.UNSUPPORTED

   decayed = targets_for(states, graph, retrievability={SKILL: 0.3})
   fresh = targets_for(states, graph, retrievability={SKILL: 0.9})

   assert [target.reason for target in decayed] == ["T2"]
   assert fresh == []


def test_t3_fires_on_a_diagnosed_gap_naming_a_skill_of_the_concept():
   _, graph, states = world()
   found = targets_for(states, graph, gaps=[(SKILL, ("BC-SKL-02036",))])

   assert [(target.reason, target.skills, target.prerequisite_ids) for target in found] == [("T3", ("BC-SKL-02036",), (SKILL,))]


def test_a_synthetic_student_stuck_at_example_gets_t4():
   fixture, graph, states = world()
   engine_graph = engine_graph_from(fixture)
   skills = graph.archetypes[ARCHETYPE]["skills"]

   history = []

   for day in range(2):
      attempted_on = TODAY - timedelta(days=2 - day)
      history.append({"archetype_id": ARCHETYPE, "item_id": f"{ARCHETYPE}-V0{day}", "attempted_on": attempted_on, "corrected": True, "stage": FadingStage.EXAMPLE})
      observation = Observation(
         archetype_id=ARCHETYPE,
         skills=list(skills),
         per_skill_states={skill: MasteryState.NOT_MASTERED for skill in skills},
         served_stage=FadingStage.EXAMPLE,
      )
      apply_observation(states, engine_graph, observation, attempted_on)

   assert states[SKILL].fading_stage == FadingStage.EXAMPLE
   assert [target.reason for target in targets_for(states, graph, history)] == ["T4"]
   assert targets_for(states, graph, history[:1]) == []


def test_no_refresher_inside_the_gap_since_the_last():
   _, graph, states = world()
   states[SKILL].consecutive_failures = 2
   lesson_id = servable(CONCEPT)[CONCEPT][0]
   recent = {lesson_id: {"status": "read", "refresher_served_at": (TODAY - timedelta(days=constants.REFRESHER_MIN_GAP_DAYS - 1)).isoformat()}}
   later = {lesson_id: {"status": "read", "refresher_served_at": (TODAY - timedelta(days=constants.REFRESHER_MIN_GAP_DAYS)).isoformat()}}

   assert targets_for(states, graph, lesson_states=recent) == []
   assert [target.reason for target in targets_for(states, graph, lesson_states=later)] == ["T4"]


def stuck_everywhere(graph, states):
   for skill_id in graph.skills:
      states[skill_id].consecutive_failures = 2

   return states


def test_assembly_places_at_most_two_refreshers_before_their_items_in_block_2():
   _, graph, states = world()
   stuck_everywhere(graph, states)
   concepts = sorted({record["concept"] for record in graph.skills.values()})
   inputs = lesson_inputs(concepts, lesson_states={f"LSN-CON-{concept[7:]}": {"status": "read"} for concept in concepts})
   inputs.refreshers = tuple(refresh.refresher_targets(states, [], inputs.lesson_states, TODAY, graph=graph, servable=inputs.servable))
   session = assemble_session(states, graph, build_bank(load_fixture()), None, [], random.Random(3), TODAY, lessons=inputs)
   refreshers = [entry for entry in session.block2 if entry.get("kind") == "refresher"]

   assert 1 <= len(refreshers) <= constants.REFRESHERS_PER_SESSION_MAX
   assert all(entry["reason"] == "T4" for entry in refreshers)

   for entry in refreshers:
      position = session.block2.index(entry)
      following = session.block2[position + 1]

      assert following["id"] == entry["before_item_id"]
      assert set(graph.archetypes[following["archetype_id"]]["skills"]) & set(graph.skills) >= {
         skill for skill in graph.archetypes[following["archetype_id"]]["skills"] if graph.skills[skill]["concept"] == entry["concept_id"]
      }
      assert entry["plan"]["reason"] == "T4"


def test_a_block_3_match_becomes_a_read_again_entry_in_block_4():
   fixture, graph, states = world()
   target = refresh.RefresherTarget(CONCEPT, "LSN-CON-02005", 1, "T2", (SKILL,))
   placement_inputs = lesson_inputs([CONCEPT])
   placement_inputs.refreshers = (target,)

   from app.session.build import LessonPlacement, Session

   placement = LessonPlacement(Session(), placement_inputs, states, graph, {})
   placement.note_block3({"id": f"{ARCHETYPE}-V00", "archetype_id": ARCHETYPE})

   assert placement.read_again == [{"kind": "read_again", "lesson_id": "LSN-CON-02005", "version": 1}]


def test_t5_is_a_named_hook_that_serves_nothing_yet():
   _, graph, states = world()

   assert refresh.method_confusion_targets(states, [], {}, TODAY) == ()
