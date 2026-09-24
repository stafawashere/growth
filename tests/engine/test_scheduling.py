"""P2 review mode and FSRS scheduling, gated by the tests 11-phased-delivery.md P2 names.

The three named gates are test_desired_retention_switch, test_due_queue_finite and
test_repetition_compression. The rest pin the due test itself against R_k and mastery, and run a
year of daily sessions over tests/fixtures/graph_p1.json.
"""
import math
import random
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from app.engine import constants, fsrs
from app.engine.fringe import DictItemBank, Graph, covered_due_skills
from app.engine.retention import current_retrievability, retrievability_of_state
from app.engine.select import due_skills, next_item_review
from app.engine.state import FadingStage, SkillState
from app.session.build import assemble_session, due_today_queue, forecast_minutes
from tests.engine.conftest_selection import build_bank, build_graph, load_fixture

SWITCH_DAY = date(2027, 3, 15)
DAY_BEFORE_SWITCH = date(2027, 3, 14)
BETWEEN_TARGETS = 0.92
SIMULATION_START = date(2026, 9, 23)
SIMULATED_DAYS = 365


def practised_state(skill_id, practised_on, stability=5.0, mastered=True):
   state = SkillState(skill_id)
   state.mastered = mastered
   state.c = 40
   state.fading_stage = FadingStage.UNSUPPORTED
   state.stability = stability
   state.difficulty = 5.0
   state.last_practised_at = datetime.combine(practised_on, datetime.min.time())

   if mastered:
      state.mastered_at = state.last_practised_at

   return state


def all_mastered_states(fixture, practised_on):
   states = {
      record["id"]: practised_state(record["id"], practised_on)
      for record in fixture["skills"]
   }

   for record in fixture["seeded_parents"]:
      states[record["id"]] = SkillState.seeded_mastered(record["id"], datetime(2026, 1, 1))

   return states


def compression_world():
   """X has two hard parents; A loads X alone, B loads Y1 and Y2, and C loads X and Y1 unpublished."""
   skills = [{"id": skill_id} for skill_id in ("P1", "P2", "X", "Y1", "Y2")]
   edges = [
      {"from": "P1", "to": "X", "type": "hard_prerequisite"},
      {"from": "P2", "to": "X", "type": "hard_prerequisite"},
   ]
   archetypes = [
      {"id": "A", "skills": ["X"], "family": "a", "primary_unit": "U1", "difficulty_factors": []},
      {"id": "B", "skills": ["Y1", "Y2"], "family": "b", "primary_unit": "U1", "difficulty_factors": []},
      {"id": "C", "skills": ["X", "Y1"], "family": "c", "primary_unit": "U1", "difficulty_factors": []},
   ]
   graph = Graph.from_records(archetypes=archetypes, skills=skills, edges=edges, inert_top=[])
   items = [
      {"id": f"{archetype_id}-V{index}", "archetype_id": archetype_id, "status": "verified"}
      for archetype_id in ("A", "B")
      for index in range(3)
   ]
   items.append({"id": "C-V0", "archetype_id": "C", "status": "draft"})
   states = {record["id"]: practised_state(record["id"], date(2026, 9, 1)) for record in skills}
   retrievability = {record["id"]: 0.5 for record in skills}

   return graph, DictItemBank(items), states, retrievability


def test_desired_retention_switch():
   before = constants.desired_retention(DAY_BEFORE_SWITCH)
   on_switch = constants.desired_retention(SWITCH_DAY)
   exam_day = constants.desired_retention(date(2027, 5, 10))
   launch = constants.desired_retention(date(2026, 9, 23))
   last_minute_before = constants.desired_retention(datetime(2027, 3, 14, 23, 59, 59))
   first_minute_on = constants.desired_retention(datetime(2027, 3, 15, 0, 0, 0))
   late_evening_in_new_york = datetime(2027, 3, 14, 23, 30, tzinfo=ZoneInfo("America/New_York"))
   already_the_fifteenth_in_utc = late_evening_in_new_york.astimezone(timezone.utc)

   assert launch == 0.90
   assert before == 0.90
   assert last_minute_before == 0.90
   assert on_switch == 0.95
   assert first_minute_on == 0.95
   assert exam_day == 0.95
   assert constants.desired_retention(late_evening_in_new_york) == 0.90
   assert already_the_fifteenth_in_utc.date() == SWITCH_DAY
   assert constants.desired_retention(already_the_fifteenth_in_utc) == 0.95

   states = {"K": practised_state("K", date(2027, 1, 1))}
   retrievability = {"K": BETWEEN_TARGETS}

   assert due_skills(states, None, DAY_BEFORE_SWITCH, retrievability) == set()
   assert due_skills(states, None, SWITCH_DAY, retrievability) == {"K"}


def test_mastered_skill_is_due_exactly_when_retrievability_drops_below_target():
   first_day = date(2027, 2, 1)
   states = {"K": practised_state("K", first_day, stability=20.0)}
   flips = []
   was_due = False

   for offset in range(120):
      today = first_day + timedelta(days=offset)
      retention = retrievability_of_state(states["K"], today)
      target = constants.desired_retention(today)
      due_now = "K" in due_skills(states, None, today, current_retrievability(states, today))

      assert due_now == (retention < target), (today, retention, target)

      if due_now and not was_due:
         flips.append(today)

      was_due = due_now

   assert len(flips) == 1
   assert flips[0] < SWITCH_DAY


def test_unmastered_skill_is_never_due_for_review():
   fixture = load_fixture()
   graph = build_graph(fixture)
   bank = build_bank(fixture)
   long_ago = date(2026, 1, 1)
   today = date(2027, 4, 1)
   states = all_mastered_states(fixture, today)

   for record in fixture["skills"]:
      states[record["id"]] = practised_state(record["id"], long_ago, stability=0.5, mastered=False)

   retrievability = current_retrievability(states, today)
   decayed = [
      record["id"]
      for record in fixture["skills"]
      if retrievability[record["id"]] < constants.desired_retention(today)
   ]
   queue = due_today_queue(states, graph, bank, [], today)
   selection = next_item_review(states, graph, bank, None, [], random.Random(3), today)

   assert len(decayed) == len(fixture["skills"])
   assert due_skills(states, graph, today, retrievability) == set()
   assert queue.skills == ()
   assert queue.item_count == 0
   assert queue.minutes == 0
   assert selection.item is None


def assert_queue_is_finite_and_stated(queue, states, graph, bank, today, attempts):
   retrievability = current_retrievability(states, today)
   due = due_skills(states, graph, today, retrievability)
   retired = set()

   assert set(queue.skills) == due
   assert len(queue.archetypes) == len(set(queue.archetypes))
   assert len(queue.archetypes) <= len(graph.archetypes)

   for archetype_id in queue.archetypes:
      record = graph.archetypes[archetype_id]
      newly_retired = covered_due_skills(record, states, graph, today, retrievability) - retired

      assert bank.has_published_item(archetype_id), archetype_id
      assert len(newly_retired) > 0, archetype_id

      retired |= newly_retired

   assert retired | set(queue.uncovered_skills) == due
   assert retired.isdisjoint(queue.uncovered_skills)

   queued_archetypes = (
      list(queue.hypercorrection_archetypes)
      + list(queue.archetypes)
      + [archetype_id for _, archetype_id in queue.requeued]
   )
   stated = sum(forecast_minutes(archetype_id, attempts) for archetype_id in queued_archetypes)

   assert isinstance(queue.minutes, (int, float))
   assert math.isfinite(queue.minutes)
   assert queue.minutes == stated

   nothing_due = len(due) == 0 and len(queue.requeued) == 0

   if nothing_due:
      assert queue.item_count == 0
      assert queue.minutes == 0
   else:
      assert queue.minutes > 0


def test_due_queue_finite():
   fixture = load_fixture()
   graph = build_graph(fixture)
   bank = build_bank(fixture)
   practised_on = date(2026, 9, 1)
   states = all_mastered_states(fixture, practised_on)
   corrected_item = f"{fixture['archetypes'][0]['id']}-V00"
   attempts = [{
      "item_id": corrected_item,
      "archetype_id": fixture["archetypes"][0]["id"],
      "attempted_on": date(2026, 12, 31),
      "stage": FadingStage.UNSUPPORTED,
      "corrected": True,
   }]
   saw_due = False
   saw_empty = False

   for offset in range(0, 400, 7):
      today = practised_on + timedelta(days=offset)
      queue = due_today_queue(states, graph, bank, attempts, today)

      assert_queue_is_finite_and_stated(queue, states, graph, bank, today, attempts)

      saw_due = saw_due or len(queue.skills) > 0
      saw_empty = saw_empty or queue.item_count == 0

   requeue_day = date(2027, 1, 1)
   requeue_queue = due_today_queue(states, graph, bank, attempts, requeue_day)
   session = assemble_session(states, graph, bank, None, attempts, random.Random(5), requeue_day)

   assert saw_due
   assert saw_empty
   assert requeue_queue.requeued == ((corrected_item, fixture["archetypes"][0]["id"]),)
   assert session.due_queue == requeue_queue
   assert any(item["id"] == corrected_item for item in session.block1)


def test_due_queue_finite_leaves_a_skill_without_a_published_archetype_uncovered():
   fixture = load_fixture()
   graph = build_graph(fixture)
   unpublished = "BC-QA-03008"
   covering = "BC-QA-03004"
   sharing_one_skill = "BC-QA-03005"
   bank = build_bank(fixture, draft_only={unpublished})
   today = date(2027, 1, 10)
   states = all_mastered_states(fixture, today)
   stale_skills = set(graph.archetypes[covering]["skills"]) | set(graph.archetypes[unpublished]["skills"])

   for skill_id in stale_skills:
      states[skill_id] = practised_state(skill_id, date(2026, 1, 10))

   queue = due_today_queue(states, graph, bank, [], today)
   unpublished_only = set(graph.archetypes[unpublished]["skills"]) - set(
      skill_id
      for archetype_id, record in graph.archetypes.items()
      if archetype_id != unpublished
      for skill_id in record["skills"]
   )

   assert_queue_is_finite_and_stated(queue, states, graph, bank, today, [])
   assert set(queue.skills) == stale_skills
   assert queue.archetypes == (covering,)
   assert sharing_one_skill not in queue.archetypes
   assert unpublished not in queue.archetypes
   assert len(unpublished_only) > 0
   assert set(queue.uncovered_skills) == unpublished_only


def test_repetition_compression():
   graph, bank, states, retrievability = compression_world()
   today = date(2026, 10, 1)
   chosen = set()

   for seed in range(40):
      selection = next_item_review(
         states, graph, bank, None, [], random.Random(seed), today,
         retrievability=retrievability,
      )
      chosen.add(selection.item["archetype_id"])

   queue = due_today_queue(states, graph, bank, [], today, retrievability)

   assert chosen == {"A"}
   assert queue.archetypes == ("A", "B")
   assert queue.uncovered_skills == ()


def test_due_skill_reached_only_as_a_hard_parent_is_covered_and_served():
   skills = [{"id": "S"}, {"id": "T"}]
   edges = [{"from": "S", "to": "T", "type": "hard_prerequisite"}]
   archetypes = [
      {"id": "A", "skills": ["T"], "family": "a", "primary_unit": "U1", "difficulty_factors": []},
   ]
   graph = Graph.from_records(archetypes=archetypes, skills=skills, edges=edges, inert_top=[])
   bank = DictItemBank([
      {"id": f"A-V{index}", "archetype_id": "A", "status": "verified"}
      for index in range(3)
   ])
   states = {record["id"]: practised_state(record["id"], date(2026, 9, 1)) for record in skills}
   retrievability = {"S": 0.5, "T": 0.99}
   today = date(2026, 10, 1)

   queue = due_today_queue(states, graph, bank, [], today, retrievability)
   selection = next_item_review(
      states, graph, bank, None, [], random.Random(0), today,
      retrievability=retrievability,
   )

   assert queue.skills == ("S",)
   assert queue.archetypes == ("A",)
   assert queue.uncovered_skills == ()
   assert queue.minutes == forecast_minutes("A", [])
   assert selection.item is not None
   assert selection.item["archetype_id"] == "A"


def test_a_year_of_daily_sessions_never_grows_an_unbounded_queue():
   fixture = load_fixture()
   graph = build_graph(fixture)
   bank = build_bank(fixture)
   states = all_mastered_states(fixture, SIMULATION_START)
   rng = random.Random(11)
   mastered_count = sum(1 for state in states.values() if state.mastered)
   largest_queue = 0
   days_with_reviews = 0

   for offset in range(SIMULATED_DAYS):
      today = SIMULATION_START + timedelta(days=offset)
      retrievability = current_retrievability(states, today)
      session = assemble_session(states, graph, bank, None, [], rng, today, retrievability=retrievability)
      queue = session.due_queue

      assert_queue_is_finite_and_stated(queue, states, graph, bank, today, [])
      assert len(queue.skills) <= mastered_count
      assert queue.item_count <= len(graph.archetypes)

      largest_queue = max(largest_queue, queue.item_count)
      practised = set()

      for item in session.block1:
         record = graph.archetypes[item["archetype_id"]]
         practised |= covered_due_skills(record, states, graph, today, retrievability)

      days_with_reviews += 1 if practised else 0

      for skill_id in practised:
         state = states[skill_id]
         state.stability = fsrs.next_stability_success(
            state.stability, state.difficulty, retrievability[skill_id]
         )
         state.last_practised_at = datetime.combine(today, datetime.min.time())

   assert days_with_reviews > 0
   assert largest_queue <= len(graph.archetypes)


def test_due_queue_counts_the_hypercorrection_requeue_block_one_serves_first():
   graph, bank, states, _ = compression_world()
   today = date(2026, 10, 1)
   retrievability = {skill_id: 0.99 for skill_id in states}
   states["X"].mastered = False
   states["X"].hypercorrection_due = today

   queue = due_today_queue(states, graph, bank, [], today, retrievability)
   session = assemble_session(states, graph, bank, None, [], random.Random(0), today, retrievability=retrievability)

   assert queue.skills == ()
   assert session.block1[0]["archetype_id"] == "A"
   assert queue.item_count == 1
   assert queue.minutes == forecast_minutes("A", [])
   assert queue.hypercorrection_skills == ("X",)
   assert queue.hypercorrection_archetypes == ("A",)
