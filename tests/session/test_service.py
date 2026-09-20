"""Persisted session service tests: open, serve, attempt, confidence, note, close.

The engine is driven through tests/fixtures/graph_p1.json and the same fixture helpers the
selection tests use, so nothing here re-implements assembly or the update rules. Invariant 23
(both predictions logged) and invariant 17 (rehearsal writes no mastery) are asserted on the rows.
"""
import json
import random
from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine.prior import p_compensatory, p_knowledge, split_skills
from app.engine.select import retrievability_map
from app.engine.state import Confidence, FadingStage, SkillState
from app.engine.update import EngineGraph
from app.session import repository, service
from tests.engine.conftest_selection import (
   ACCOUNT_CREATED_AT,
   build_bank,
   build_graph,
   build_states,
   load_fixture,
)

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)
SNAPSHOT_ID = "SNAP-0001"
USER_ID = "USER-0001"
SPLIT_ARCHETYPE = "BC-QA-01004"


def engine_graph_from(fixture):
   inert = set(fixture["inert_top"])
   hard_parents = {}
   supporting_parents = {}
   hard_children = {}

   for edge in fixture["edges"]:
      parent = edge["from"]
      child = edge["to"]
      touches_inert = parent in inert or child in inert
      is_co_requisite = edge["type"] == "co_requisite"

      if touches_inert or is_co_requisite:
         continue

      is_hard = edge["type"] == "hard_prerequisite"

      if is_hard:
         hard_parents.setdefault(child, set()).add(parent)
         hard_children.setdefault(parent, set()).add(child)
      else:
         supporting_parents.setdefault(child, set()).add(parent)

   archetype_counts = {}

   for record in fixture["archetypes"]:
      for skill_id in record["skills"]:
         archetype_counts[skill_id] = archetype_counts.get(skill_id, 0) + 1

   return EngineGraph(
      hard_parents=hard_parents,
      supporting_parents=supporting_parents,
      hard_children=hard_children,
      archetype_counts=archetype_counts,
   )


class World:
   def __init__(self, db, fixture, graph, engine_graph, archetypes, bank):
      self.db = db
      self.fixture = fixture
      self.graph = graph
      self.engine_graph = engine_graph
      self.archetypes = archetypes
      self.bank = bank

   def open(self, mode="learning", seed=7):
      return service.open_session(
         self.db,
         USER_ID,
         mode,
         self.graph,
         self.engine_graph,
         self.archetypes,
         self.bank,
         SNAPSHOT_ID,
         TODAY,
         random.Random(seed),
         now=NOW,
      )

   def attempt(self, session_row, answer, confidence=None, elapsed_ms=90000):
      item = service.next_item(self.db, session_row.id)

      return item, service.record_attempt(
         self.db,
         session_row.id,
         item["id"],
         answer,
         elapsed_ms,
         TODAY,
         archetypes=self.archetypes,
         engine_graph=self.engine_graph,
         confidence=confidence,
         now=NOW,
      )


@pytest.fixture
def world(tmp_path):
   fixture = load_fixture()
   engine = models.make_engine(tmp_path / "growth.db")
   graph = build_graph(fixture)
   bank = build_bank(fixture)
   archetypes = {record["id"]: record for record in fixture["archetypes"]}

   with OrmSession(engine) as db:
      states = build_states(fixture)
      repository.save_states(db, USER_ID, states, SNAPSHOT_ID, ACCOUNT_CREATED_AT)
      db.commit()

      yield World(db, fixture, graph, engine_graph_from(fixture), archetypes, bank)


def only_split_archetype(world):
   """Serve the one fixture archetype whose K_hard is non-empty, so the two predictions differ.

   Every other P1 archetype loads no hard ancestor of its own primary skill, which makes the
   split-model and the compensatory prediction the same number and leaves invariant 23 untestable.
   """
   states = repository.load_states(world.db, USER_ID)
   archetype = world.archetypes[SPLIT_ARCHETYPE]

   for parent in sorted(world.engine_graph.hard_parents.get(archetype["skills"][0], ())):
      states[parent].mastered = True
      states[parent].c = 3.0
      states[parent].stability = 5.0
      states[parent].difficulty = 5.0
      states[parent].last_practised_at = datetime(2026, 2, 1, 9, 0, 0)

   repository.save_states(world.db, USER_ID, states, SNAPSHOT_ID, ACCOUNT_CREATED_AT)
   world.db.commit()
   others = {
      record["id"]
      for record in world.fixture["archetypes"]
      if record["id"] != SPLIT_ARCHETYPE
   }
   world.bank = build_bank(world.fixture, draft_only=others)


def set_unsupported(world):
   """Serve at stage unsupported, which is the stage that collects a confidence rating."""
   states = repository.load_states(world.db, USER_ID)

   for state in states.values():
      if not state.mastered:
         state.fading_stage = FadingStage.UNSUPPORTED
         state.observation_count = 1

   repository.save_states(world.db, USER_ID, states, SNAPSHOT_ID, ACCOUNT_CREATED_AT)
   world.db.commit()


def test_open_session_persists_four_blocks(world):
   opened = world.open()
   stored = world.db.get(models.Session, opened.id)
   queue = json.loads(stored.queue)

   assert stored.user_id == USER_ID
   assert stored.mode == "learning"
   assert stored.updates_mastery == 1
   assert stored.snapshot_id == SNAPSHOT_ID
   assert [key in queue for key in ("block1", "block2", "block3", "block4")] == [True] * 4
   assert len(queue["block2"]) > 0
   assert isinstance(queue["forecasts"], dict)

   served_archetypes = {
      item["archetype_id"]
      for key in ("block1", "block2", "block3")
      for item in queue[key]
   }

   assert served_archetypes <= set(queue["forecasts"])


def test_attempt_row_logs_split_and_compensatory(world):
   only_split_archetype(world)
   states_before = repository.load_states(world.db, USER_ID)
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": True})

   assert item["archetype_id"] == SPLIT_ARCHETYPE

   archetype = world.archetypes[item["archetype_id"]]
   hard, _ = split_skills(archetype, world.engine_graph.hard_parents)
   retrievability = retrievability_map(states_before, TODAY)
   expected_split = p_knowledge(
      archetype, states_before, world.engine_graph.hard_parents, retrievability
   )
   expected_compensatory = p_compensatory(archetype, states_before, retrievability)

   assert len(hard) > 0
   assert attempt.p_split is not None
   assert attempt.p_compensatory is not None
   assert attempt.p_split <= attempt.p_compensatory
   assert attempt.p_split != attempt.p_compensatory
   assert attempt.p_split == pytest.approx(expected_split)
   assert attempt.p_compensatory == pytest.approx(expected_compensatory)
   assert attempt.served_stage == item["stage"]
   assert attempt.format == item["format"]
   assert set(json.loads(attempt.per_skill_states)) == set(archetype["skills"])


def test_record_attempt_refuses_duplicate(world):
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": True}, confidence=Confidence.UNSURE)
   states = repository.load_states(world.db, USER_ID)
   primary = world.archetypes[item["archetype_id"]]["skills"][0]
   count_after_first = states[primary].observation_count

   with pytest.raises(ValueError):
      service.record_attempt(
         world.db,
         opened.id,
         item["id"],
         {"correct": True},
         90000,
         TODAY,
         archetypes=world.archetypes,
         engine_graph=world.engine_graph,
         confidence=Confidence.UNSURE,
         now=NOW,
      )

   states = repository.load_states(world.db, USER_ID)

   assert states[primary].observation_count == count_after_first


def test_ungraded_answer_skips_the_update(world):
   opened = world.open()
   before = repository.load_states(world.db, USER_ID)
   item, attempt = world.attempt(opened, {"response": "3x^2"}, confidence=Confidence.UNSURE)
   after = repository.load_states(world.db, USER_ID)
   loaded = world.archetypes[item["archetype_id"]]["skills"]

   assert attempt.correct is None
   assert attempt.p_split is not None
   assert set(json.loads(attempt.per_skill_states).values()) == {"not_attempted"}

   for skill_id in loaded:
      assert after[skill_id] == before[skill_id]


def test_timestamps_are_timezone_aware_utc(world):
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": True}, confidence=Confidence.UNSURE)
   service.close_session(world.db, opened.id)
   stored = world.db.get(models.Session, opened.id)
   written = [stored.started_at, stored.ended_at, attempt.started_at, attempt.submitted_at]

   for value in written:
      assert datetime.fromisoformat(value).tzinfo is not None
      assert datetime.fromisoformat(value).utcoffset() == timedelta(0)


def test_attempt_updates_skills_state(world):
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": True}, confidence=Confidence.UNSURE)
   archetype = world.archetypes[item["archetype_id"]]
   states = repository.load_states(world.db, USER_ID)

   for skill_id in archetype["skills"]:
      assert states[skill_id].observation_count == 1
      assert states[skill_id].c > 0.0
      assert states[skill_id].last_practised_at is not None


def test_confidence_before_feedback_sets_hypercorrection(world):
   set_unsupported(world)
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": False})
   archetype = world.archetypes[item["archetype_id"]]
   primary = archetype["skills"][0]
   deferred = repository.load_states(world.db, USER_ID)

   assert item["stage"] == FadingStage.UNSUPPORTED
   assert attempt.confidence is None
   assert deferred[primary].observation_count == 1

   service.record_confidence(
      world.db,
      attempt.id,
      Confidence.CONFIDENT,
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      today=TODAY,
   )
   states = repository.load_states(world.db, USER_ID)

   assert world.db.get(models.Attempt, attempt.id).confidence == Confidence.CONFIDENT.value
   assert states[primary].observation_count == 2
   assert states[primary].hypercorrection_due == TODAY + timedelta(days=1)
   assert states[primary].f > 0.0


def test_error_note_stored_on_attempt(world):
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": False}, confidence=Confidence.UNSURE)
   service.record_error_note(world.db, attempt.id, "I differentiated the inner factor twice.")
   stored = world.db.get(models.Attempt, attempt.id)

   assert stored.error_note == "I differentiated the inner factor twice."


def test_close_session_writes_ended_at(world):
   opened = world.open()

   assert opened.ended_at is None

   closed_at = datetime(2026, 3, 1, 10, 30, 0, tzinfo=timezone.utc)
   service.close_session(world.db, opened.id, closed_at)
   stored = world.db.get(models.Session, opened.id)

   assert stored.ended_at == closed_at.isoformat()


def test_state_round_trip(world):
   states = repository.load_states(world.db, USER_ID)
   skill_id = sorted(states)[0]
   state = states[skill_id]
   state.beta = -0.35
   state.c = 2.25
   state.f = 0.5
   state.stability = 12.5
   state.difficulty = 5.25
   state.last_practised_at = datetime(2026, 2, 27, 8, 15, 0)
   state.fading_stage = FadingStage.COMPLETION
   state.observation_count = 4
   state.unaided_success_count = 2
   state.distinct_archetypes_succeeded = {"BC-QA-01004", "BC-QA-01008"}
   state.success_days = {date(2026, 2, 20), date(2026, 2, 27)}
   state.mastered = True
   state.mastered_at = datetime(2026, 2, 27, 8, 20, 0)
   state.hypercorrection_due = date(2026, 3, 2)
   state.consecutive_successes = 1
   state.consecutive_failures = 0
   state.concept_opener_done = True
   repository.save_states(world.db, USER_ID, states, SNAPSHOT_ID, NOW)
   world.db.commit()
   reloaded = repository.load_states(world.db, USER_ID)[skill_id]

   assert reloaded == state
   assert isinstance(reloaded, SkillState)


def test_rehearsal_session_writes_no_mastery(world):
   set_unsupported(world)
   before = {
      (row.skill_id): (
         row.credited_successes,
         row.credited_failures,
         row.stability,
         row.difficulty,
         row.mastered,
         row.fading_stage,
         row.observation_count,
      )
      for row in world.db.scalars(select(models.SkillState)).all()
   }
   opened = world.open(mode="rehearsal")

   assert opened.updates_mastery == 0

   item, attempt = world.attempt(opened, {"correct": True}, confidence=Confidence.CONFIDENT)
   after = {
      (row.skill_id): (
         row.credited_successes,
         row.credited_failures,
         row.stability,
         row.difficulty,
         row.mastered,
         row.fading_stage,
         row.observation_count,
      )
      for row in world.db.scalars(select(models.SkillState)).all()
   }

   assert after == before
   assert attempt.id is not None
   assert attempt.p_split is not None


def test_close_session_applies_unrated_attempts_as_unsure(world):
   set_unsupported(world)
   opened = world.open()
   item, attempt = world.attempt(opened, {"correct": True})

   assert attempt.confidence is None

   before = repository.load_states(world.db, USER_ID)
   closed = service.close_session(
      world.db,
      opened.id,
      NOW,
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      today=TODAY,
   )
   stored_attempt = world.db.get(models.Attempt, attempt.id)
   after = repository.load_states(world.db, USER_ID)
   primary = world.archetypes[item["archetype_id"]]["skills"][0]

   assert closed.ended_at is not None
   assert stored_attempt.confidence == Confidence.UNSURE.value
   assert after[primary].observation_count > before[primary].observation_count
   assert not after[primary].hypercorrection_due

   opened_second = world.open(seed=13)
   world.attempt(opened_second, {"correct": True})

   with pytest.raises(ValueError):
      service.close_session(world.db, opened_second.id, NOW)


def test_judgment_never_enters_credit(world):
   opened = world.open()

   def snapshot():
      return {
         row.skill_id: (
            row.credited_successes,
            row.credited_failures,
            row.stability,
            row.difficulty,
            row.mastered,
            row.fading_stage,
            row.observation_count,
            row.beta,
            row.last_practised_at,
            row.mastered_at,
            row.hypercorrection_due,
            row.consecutive_successes,
            row.consecutive_failures,
            row.concept_opener_done,
            row.distinct_archetypes_succeeded,
            row.success_days,
            row.updated_at,
         )
         for row in world.db.scalars(select(models.SkillState)).all()
      }

   before = snapshot()
   judgment = service.record_judgment(world.db, opened.id, "skill", "BC-SKL-01024", 0.7, NOW)
   after = snapshot()

   assert judgment.id is not None
   assert world.db.get(models.Judgment, judgment.id).scope_id == "BC-SKL-01024"
   assert after == before
