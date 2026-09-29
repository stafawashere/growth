"""The first-contact gate of docs/plan/15-lessons.md, Engine and session integration: lesson_target,
lesson_band and bypass_placed_concepts, over tests/fixtures/graph_p1.json and the live graph."""
import pytest

from app.engine import constants
from app.engine.prior import p_knowledge
from app.lessons import gate
from app.runtime.graphs import graphs_from_snapshot
from tests.engine.conftest_selection import build_graph, build_states, load_fixture

SECONDARY_ARCHETYPE = "BC-QA-02002"
SECONDARY_CONCEPT = "BC-CON-02003"
PRIMARY_CONCEPT = "BC-CON-02002"


def fixture_world():
   fixture = load_fixture()

   return build_graph(fixture), build_states(fixture)


def item_on(archetype_id):
   return {"id": f"{archetype_id}-V00", "archetype_id": archetype_id}


def servable_for(*concept_ids):
   return {concept_id: (f"LSN-CON-{concept_id[7:]}", 1) for concept_id in concept_ids}


def observe(states, skill_ids):
   for skill_id in skill_ids:
      states[skill_id].credited_observation_count = 1


def test_the_primary_concept_is_the_target_of_an_unobserved_item():
   graph, states = fixture_world()
   target = gate.lesson_target(item_on(SECONDARY_ARCHETYPE), states, graph, {}, servable_for(PRIMARY_CONCEPT, SECONDARY_CONCEPT))

   assert target == PRIMARY_CONCEPT


def test_a_concept_reached_only_as_a_secondary_skill_still_gets_its_lesson():
   graph, states = fixture_world()
   observe(states, ["BC-SKL-02006", "BC-SKL-02007"])
   target = gate.lesson_target(item_on(SECONDARY_ARCHETYPE), states, graph, {}, servable_for(PRIMARY_CONCEPT, SECONDARY_CONCEPT))

   assert target == SECONDARY_CONCEPT


def test_a_read_or_served_lesson_is_not_a_target_and_a_deferred_one_is():
   graph, states = fixture_world()
   servable = servable_for(PRIMARY_CONCEPT)
   lesson_id = servable[PRIMARY_CONCEPT][0]

   for status in ("served", "read", "skipped", "bypassed_by_placement"):
      assert gate.lesson_target(item_on(SECONDARY_ARCHETYPE), states, graph, {lesson_id: {"status": status}}, servable) is None

   assert gate.lesson_target(item_on(SECONDARY_ARCHETYPE), states, graph, {lesson_id: {"status": "unseen"}}, servable) == PRIMARY_CONCEPT
   observe(states, ["BC-SKL-02006", "BC-SKL-02007"])
   assert gate.lesson_target(item_on(SECONDARY_ARCHETYPE), states, graph, {lesson_id: {"status": "deferred"}}, servable) == PRIMARY_CONCEPT


def test_no_servable_lesson_means_no_target():
   graph, states = fixture_world()

   assert gate.lesson_target(item_on(SECONDARY_ARCHETYPE), states, graph, {}, {}) is None


def test_every_never_primary_concept_of_the_live_graph_is_reached_through_a_secondary_skill(live_graph):
   """15 Tests names 59 never-primary concepts; data/ as loaded on this branch has 57, and the
   test reads the set from the graph rather than the count from the plan."""
   graph = live_graph
   primary = {graph.skills[record["skills"][0]]["concept"] for record in graph.archetypes.values() if record["skills"][0] in graph.skills}
   concepts = {record["concept"] for record in graph.skills.values()}
   never_primary = sorted(concepts - primary)
   reached = 0

   assert len(never_primary) > 0

   for concept_id in never_primary:
      record = next(
         record
         for record in sorted(graph.archetypes.values(), key=lambda entry: entry["id"])
         if any(graph.skills.get(skill, {}).get("concept") == concept_id for skill in record["skills"])
      )
      states = {skill: gate_state(skill, graph, concept_id) for skill in record["skills"] if skill in graph.skills}
      target = gate.lesson_target(item_on(record["id"]), states, graph, {}, servable_for(*concepts))

      assert target == concept_id
      reached += 1

   assert reached == len(never_primary)


def gate_state(skill_id, graph, concept_id):
   from app.engine.state import SkillState

   state = SkillState(skill_id)
   is_other_concept = graph.skills[skill_id]["concept"] != concept_id

   if is_other_concept:
      state.credited_observation_count = 1

   return state


def band_states_at(graph, states, archetype, beta):
   for skill_id in archetype["skills"]:
      states[skill_id].beta = beta

   return p_knowledge(archetype, states, graph.hard_parents)


def test_the_band_edges_are_stage_low_and_stage_high(monkeypatch):
   graph, states = fixture_world()
   archetype = graph.archetypes["BC-QA-02011"]
   values = iter([constants.STAGE_LOW - 0.001, constants.STAGE_LOW, constants.STAGE_HIGH, constants.STAGE_HIGH + 0.001])
   monkeypatch.setattr(gate, "p_knowledge", lambda *args, **kwargs: next(values))

   assert gate.lesson_band(archetype, states, graph, None) == "low"
   assert gate.lesson_band(archetype, states, graph, None) == "mid"
   assert gate.lesson_band(archetype, states, graph, None) == "mid"
   assert gate.lesson_band(archetype, states, graph, None) == "none"


def test_the_band_reads_p_knowledge_as_serve_stage_does():
   graph, states = fixture_world()
   archetype = graph.archetypes["BC-QA-02011"]
   low = band_states_at(graph, states, archetype, -4.0)
   assert low < constants.STAGE_LOW
   assert gate.lesson_band(archetype, states, graph, None) == "low"

   high = band_states_at(graph, states, archetype, 6.0)
   assert high > constants.STAGE_HIGH
   assert gate.lesson_band(archetype, states, graph, None) == "none"


def test_bypass_names_the_concepts_whose_every_skill_is_mastered():
   graph, states = fixture_world()

   for skill_id, record in graph.skills.items():
      if record["concept"] == "BC-CON-02005":
         states[skill_id].mastered = True

   states["BC-SKL-02006"].mastered = True

   assert gate.bypass_placed_concepts(states, graph) == ["BC-CON-02005"]


def test_bypass_names_nothing_for_a_fresh_student():
   graph, states = fixture_world()

   assert gate.bypass_placed_concepts(states, graph) == []


@pytest.fixture(scope="module")
def live_graph():
   from app.content.loader import load_snapshot
   from app.runtime.context import DEFAULT_CONTENT_ROOT

   return graphs_from_snapshot(load_snapshot(DEFAULT_CONTENT_ROOT))[0]

def lesson_body(target_id, full=2.0, brief=1.5, prefix="LSN-CON"):
   import copy
   import json
   from pathlib import Path

   record = json.loads((Path(__file__).resolve().parents[2] / "content" / "lessons" / "LSN-CON-02013.json").read_text())
   body = copy.deepcopy(record)
   body["id"] = f"{prefix}-{target_id[7:]}"
   body["target_id"] = target_id
   body["status"] = "signed_off"
   body["read_minutes"] = {"full": full, "brief": brief}

   return body


def lesson_inputs(target_ids, full=2.0, brief=1.5, example_first=None, lesson_states=None):
   bodies = {}
   servable = {}

   for target_id in target_ids:
      prefix = "LSN-PRQ" if target_id.startswith("BC-PRQ") else "LSN-CON"
      body = lesson_body(target_id, full, brief, prefix)
      bodies[body["id"]] = body
      servable[target_id] = (body["id"], body["version"])

   return gate.LessonInputs(
      servable=servable,
      bodies=bodies,
      lesson_states=lesson_states or {},
      example_first=example_first,
   )


def fixture_concepts(graph):
   return sorted({record["concept"] for record in graph.skills.values()})


def assemble(lessons, seed=3, states=None):
   import random
   from datetime import date

   from app.session.build import assemble_session
   from tests.engine.conftest_selection import build_bank

   fixture = load_fixture()
   graph = build_graph(fixture)
   states = states if states is not None else build_states(fixture)

   return assemble_session(states, graph, build_bank(fixture), None, [], random.Random(seed), date(2026, 3, 1), lessons=lessons), graph


def lesson_entries(block):
   return [entry for entry in block if entry.get("kind") == "lesson"]


def test_a_lesson_goes_immediately_before_the_item_it_serves_and_names_it():
   graph = build_graph(load_fixture())
   session, _ = assemble(lesson_inputs(fixture_concepts(graph)))
   block2 = session.block2
   inserted = lesson_entries(block2)

   assert 1 <= len(inserted) <= 2

   for index, entry in enumerate(block2):
      if entry["kind"] != "lesson":
         continue

      following = next(later for later in block2[index + 1:] if later["kind"] == "item")

      assert following["id"] == entry["before_item_id"]
      assert following["preceded_by_lesson_id"] in {lesson["lesson_id"] for lesson in inserted}
      assert entry["reason"] == "first_contact"
      assert entry["plan"]["lesson_id"] == entry["lesson_id"]
      assert entry["band"] in ("low", "mid")

   assert all(entry["kind"] in ("item", "lesson") for entry in block2)
   assert session.lesson_minutes == sum(entry["minutes"] for entry in session.lessons)


def test_the_third_new_concept_is_deferred_and_its_item_carries_the_link():
   graph = build_graph(load_fixture())
   session, _ = assemble(lesson_inputs(fixture_concepts(graph), full=1.0, brief=1.0))

   assert len(lesson_entries(session.block2)) == 2
   assert len(session.lesson_deferrals) >= 1

   deferral = session.lesson_deferrals[0]
   linked = next(entry for entry in session.block2 if entry.get("id") == deferral["before_item_id"])

   assert deferral["reason"] == "lesson_count"
   assert linked["lesson_link"] == {"lesson_id": deferral["lesson_id"], "version": deferral["version"]}
   assert "preceded_by_lesson_id" not in linked


def test_the_share_cap_defers_a_lesson_whose_minutes_would_pass_it():
   graph = build_graph(load_fixture())
   session, _ = assemble(lesson_inputs(fixture_concepts(graph), full=6.0, brief=3.0))

   assert session.lesson_minutes <= 0.30 * session.forecast_total
   assert any(deferral["reason"] == "reading_share" for deferral in session.lesson_deferrals)


def test_no_lesson_inputs_serves_no_lesson():
   session, _ = assemble(None)

   assert lesson_entries(session.block2) == []
   assert session.lessons == []
   assert all(entry["kind"] == "item" for entry in session.block2)


def test_the_example_first_arm_serves_the_item_and_defers_the_lesson():
   graph = build_graph(load_fixture())
   session, _ = assemble(lesson_inputs(fixture_concepts(graph), example_first=lambda concept_id, archetype: True))

   assert lesson_entries(session.block2) == []
   assert len(session.lesson_deferrals) > 0
   assert {deferral["reason"] for deferral in session.lesson_deferrals} == {"example_first"}


def test_the_control_arm_serves_the_lesson_first():
   graph = build_graph(load_fixture())
   session, _ = assemble(lesson_inputs(fixture_concepts(graph), example_first=lambda concept_id, archetype: False))

   assert len(lesson_entries(session.block2)) > 0


def flipped_world(prerequisite_id):
   fixture = load_fixture()
   states = build_states(fixture)
   states[prerequisite_id].mastered = False

   return states


def test_a_prerequisite_lesson_for_a_flipped_parent_goes_before_the_concept_lesson():
   graph = build_graph(load_fixture())
   first, _ = assemble(lesson_inputs(fixture_concepts(graph)))
   lesson = lesson_entries(first.block2)[0]
   archetype = graph.archetypes[next(entry for entry in first.block2 if entry.get("id") == lesson["before_item_id"])["archetype_id"]]
   prerequisite_id = archetype["prerequisites"][0]
   states = flipped_world(prerequisite_id)
   session, _ = assemble(lesson_inputs(fixture_concepts(graph) + [prerequisite_id]), states=states)
   kinds = [(entry.get("kind"), entry.get("lesson_id") or entry.get("id")) for entry in session.block2]
   prerequisite_lesson = f"LSN-PRQ-{prerequisite_id[7:]}"
   position = kinds.index(("lesson", prerequisite_lesson))

   assert kinds[position + 1][0] == "lesson"
   assert kinds[position + 1][1].startswith("LSN-CON")


def test_no_prerequisite_lesson_without_a_flipped_parent():
   graph = build_graph(load_fixture())
   prerequisite_ids = sorted({prq for record in graph.archetypes.values() for prq in record["prerequisites"]})
   session, _ = assemble(lesson_inputs(fixture_concepts(graph) + prerequisite_ids))

   assert all(not entry["lesson_id"].startswith("LSN-PRQ") for entry in lesson_entries(session.block2))
