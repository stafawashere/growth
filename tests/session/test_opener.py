"""The productive-failure opener, docs/plan/02-adaptive-engine.md "Session assembly" and
docs/plan/01-learning-model.md "Productive-failure openers for conceptual targets".

The fixture graph carries none of the five live target concepts on an archetype with BC-DF-13 or
BC-DF-15, so each test names its own targets: BC-CON-03003, loaded by BC-QA-03004 (BC-DF-13),
has a generation item, and BC-CON-02002, loaded only by BC-QA-02002 (BC-DF-02), has none.
"""
import json
import random
from dataclasses import asdict
from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine import constants
from app.engine.fringe import DictItemBank, Graph
from app.engine.select import dress_item, format_for_item
from app.engine.state import FadingStage, PendingProbe, ResponseFormat
from app.session import diagnostic_session, repository, service
from app.session.build import OPENER_GAP_ACTION, assemble_session
from tests.engine.conftest_selection import (
   ACCOUNT_CREATED_AT,
   build_bank,
   build_states,
   load_fixture,
)
from tests.session.test_service import engine_graph_from

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)
SNAPSHOT_ID = "SNAP-0001"
USER_ID = "USER-0001"
GENERATION_CONCEPT = "BC-CON-03003"
GENERATION_ARCHETYPE = "BC-QA-03004"
GAP_CONCEPT = "BC-CON-02002"
SERVING_BLOCKS = ("block1", "block2", "block3")


def concepts_of(fixture):
   concepts = {}

   for record in fixture["skills"]:
      concepts.setdefault(record["concept"], []).append(record["id"])

   return [{"id": concept_id, "skills": skills} for concept_id, skills in concepts.items()]


def graph_with_concepts(fixture):
   return Graph.from_records(
      archetypes=fixture["archetypes"],
      skills=fixture["skills"],
      edges=fixture["edges"],
      inert_top=fixture["inert_top"],
      concepts=concepts_of(fixture),
   )


def generation_ready_mastery(fixture):
   """Everything mastered but the skills BC-QA-03004 loads, so BC-CON-03003 is on the fringe and
   the archetype's primary skill clears gating."""
   archetype = next(record for record in fixture["archetypes"] if record["id"] == GENERATION_ARCHETYPE)
   loaded = set(archetype["skills"])

   return {record["id"] for record in fixture["skills"] if record["id"] not in loaded}


class World:
   def __init__(self, db, fixture):
      self.db = db
      self.fixture = fixture
      self.graph = graph_with_concepts(fixture)
      self.engine_graph = engine_graph_from(fixture)
      self.archetypes = {record["id"]: record for record in fixture["archetypes"]}
      self.bank = build_bank(fixture)

   def open(self, mode="learning", today=TODAY, now=NOW, seed=7):
      return service.open_session(
         self.db,
         USER_ID,
         mode,
         self.graph,
         self.engine_graph,
         self.archetypes,
         self.bank,
         SNAPSHOT_ID,
         today,
         random.Random(seed),
         now=now,
      )

   def flag(self, skill_id):
      return self.db.get(models.SkillState, (USER_ID, skill_id)).concept_opener_done

   def gap_rows(self):
      return self.db.scalars(
         select(models.AuditLog).where(models.AuditLog.action == OPENER_GAP_ACTION)
      ).all()


def open_world(tmp_path, mastered):
   fixture = load_fixture()
   engine = models.make_engine(tmp_path / "growth.db")
   db = OrmSession(engine)
   states = build_states(fixture, mastered=mastered)
   repository.save_states(db, USER_ID, states, SNAPSHOT_ID, ACCOUNT_CREATED_AT)
   db.commit()

   return World(db, fixture)


@pytest.fixture
def generation_world(tmp_path, monkeypatch):
   monkeypatch.setattr(constants, "PRODUCTIVE_FAILURE_TARGETS", (GENERATION_CONCEPT,))
   world = open_world(tmp_path, generation_ready_mastery(load_fixture()))

   yield world

   world.db.close()


@pytest.fixture
def gap_world(tmp_path, monkeypatch):
   monkeypatch.setattr(constants, "PRODUCTIVE_FAILURE_TARGETS", (GAP_CONCEPT,))
   world = open_world(tmp_path, frozenset())

   yield world

   world.db.close()


def queue_of(session_row):
   return json.loads(session_row.queue)


def opener_slots(queue):
   return [
      (block, position)
      for block in SERVING_BLOCKS
      for position, item in enumerate(queue[block])
      if item.get("is_opener")
   ]


def first_skill(world, concept_id):
   return world.graph.concept_skills[concept_id][0]


def engine_fields(db):
   return {skill_id: asdict(state) for skill_id, state in repository.load_states(db, USER_ID).items()}


def test_a_learning_session_opens_block_two_with_the_opener_and_sets_the_flag(generation_world):
   world = generation_world

   assert world.flag(first_skill(world, GENERATION_CONCEPT)) == 0

   queue = queue_of(world.open())
   opener = queue["block2"][0]

   assert opener_slots(queue) == [("block2", 0)]
   assert opener["is_opener"] is True
   assert opener["is_probe"] is False
   assert opener["archetype_id"] == GENERATION_ARCHETYPE
   assert opener["stage"] == FadingStage.UNSUPPORTED.value
   assert opener["opener_concept"] == GENERATION_CONCEPT
   assert world.flag(first_skill(world, GENERATION_CONCEPT)) == 1

   others = [
      skill_id
      for skill_id in world.graph.skills
      if skill_id != first_skill(world, GENERATION_CONCEPT)
   ]

   assert all(world.flag(skill_id) == 0 for skill_id in others)


def test_a_second_session_does_not_repeat_the_opener(generation_world):
   world = generation_world
   world.open()

   later_day = TODAY + timedelta(days=constants.REPEAT_WINDOW_DAYS + 1)
   later_now = NOW + timedelta(days=constants.REPEAT_WINDOW_DAYS + 1)
   again = queue_of(world.open(today=later_day, now=later_now, seed=8))

   assert opener_slots(again) == []


@pytest.mark.parametrize("correct", [True, False])
def test_the_opener_attempt_writes_nothing_to_skills_state_but_observation_count(
   generation_world, correct
):
   """Uncredited is 02's not_attempted: observation_count moves, as the schema table says it does
   on an uncredited observation, and no other field does, rating and all."""
   world = generation_world
   session_row = world.open()
   before = engine_fields(world.db)
   item = service.next_item(world.db, session_row.id)

   assert item["is_opener"] is True

   attempt = service.record_attempt(
      world.db,
      session_row.id,
      item["id"],
      {"correct": correct},
      90000,
      TODAY,
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      now=NOW,
   )
   service.record_confidence(
      world.db,
      attempt.id,
      "confident",
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      today=TODAY,
      now=NOW,
   )
   service.close_session(
      world.db,
      session_row.id,
      now=NOW,
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      today=TODAY,
   )
   after = engine_fields(world.db)
   loaded = set(world.archetypes[GENERATION_ARCHETYPE]["skills"])

   for skill_id, fields in before.items():
      expected = dict(fields)

      if skill_id in loaded:
         expected["observation_count"] += 1

      assert after[skill_id] == expected, skill_id

   stored = json.loads(world.db.get(models.Attempt, attempt.id).per_skill_states)

   assert set(stored.values()) == {"not_attempted"}
   assert attempt.correct == int(correct)

   history = repository.load_attempts_history(world.db, USER_ID)

   assert [entry["corrected"] for entry in history] == [False]


def test_no_opener_outside_a_learning_session(generation_world):
   world = generation_world

   for mode in ("rehearsal", "review"):
      queue = queue_of(world.open(mode=mode))

      assert opener_slots(queue) == []

   assert world.flag(first_skill(world, GENERATION_CONCEPT)) == 0


def test_no_opener_in_the_diagnostic(generation_world):
   world = generation_world
   session_row = world.open(mode="diagnostic")
   item = diagnostic_session.advance(
      world.db, session_row, world.graph, world.engine_graph, world.bank, TODAY, 0, NOW
   )
   served = json.loads(session_row.queue)[diagnostic_session.ITEMS_KEY]

   assert item is not None
   assert len(served) == 1
   assert item.get("is_opener") is not True
   assert all(entry.get("is_opener") is not True for entry in served)
   assert world.flag(first_skill(world, GENERATION_CONCEPT)) == 0


def test_a_pending_probe_still_goes_ahead_of_the_opener(monkeypatch):
   """02 puts the opener first among the ordinary items of block 2 and R6 keeps the probe first."""
   monkeypatch.setattr(constants, "PRODUCTIVE_FAILURE_TARGETS", (GENERATION_CONCEPT,))
   fixture = load_fixture()
   graph = graph_with_concepts(fixture)
   states = build_states(fixture, mastered=generation_ready_mastery(fixture))
   probe = PendingProbe("BC-QA-02002", "BC-DGN-0001", NOW - timedelta(days=1))
   session = assemble_session(
      states,
      graph,
      build_bank(fixture),
      [probe],
      [],
      random.Random(5),
      TODAY,
      now=NOW,
      openers=True,
   )

   assert session.block2[0]["is_probe"] is True
   assert session.block2[1].get("is_opener") is True


def test_a_concept_with_no_generation_item_is_skipped_and_audited_once_a_day(gap_world):
   world = gap_world
   first = queue_of(world.open())
   world.open(seed=8)

   assert opener_slots(first) == []
   assert world.flag(first_skill(world, GAP_CONCEPT)) == 0

   rows = world.gap_rows()

   assert len(rows) == 1
   assert rows[0].actor == USER_ID
   assert rows[0].subject == f"concepts:{GAP_CONCEPT}"
   assert json.loads(rows[0].detail)["day"] == TODAY.isoformat()

   world.open(today=TODAY + timedelta(days=1), now=NOW + timedelta(days=1), seed=9)

   assert len(world.gap_rows()) == 2


def test_an_opener_is_short_answer_on_a_turn_r29_would_give_to_mcq(generation_world):
   """R29 alternates only at stage unsupported and an opener is served there, so without its own
   rule the second unsupported attempt on the archetype would make the opener a choice."""
   world = generation_world
   record = world.archetypes[GENERATION_ARCHETYPE]
   chosen = world.bank.published_items(GENERATION_ARCHETYPE)[0]
   states = repository.load_states(world.db, USER_ID)
   one_unsupported_attempt = [{"archetype_id": GENERATION_ARCHETYPE, "stage": FadingStage.UNSUPPORTED}]

   assert format_for_item(one_unsupported_attempt, chosen, FadingStage.UNSUPPORTED) == ResponseFormat.MCQ

   slot = dress_item(
      record,
      chosen,
      states,
      world.graph,
      one_unsupported_attempt,
      opener_concept=GENERATION_CONCEPT,
   )

   assert slot["format"] == ResponseFormat.SHORT_ANSWER
   assert format_for_item(one_unsupported_attempt, slot, FadingStage.UNSUPPORTED) == ResponseFormat.SHORT_ANSWER


def test_a_statement_keyed_item_is_never_an_opener(generation_world):
   world = generation_world
   items = []

   for record in world.fixture["archetypes"]:
      for item in world.bank.published_items(record["id"]):
         is_generation_item = item["archetype_id"] == GENERATION_ARCHETYPE
         items.append(dict(item, requires_choice=True) if is_generation_item else item)

   world.bank = DictItemBank(items)
   queue = queue_of(world.open())

   assert opener_slots(queue) == []
   assert world.flag(first_skill(world, GENERATION_CONCEPT)) == 0
   assert [row.subject for row in world.gap_rows()] == [f"concepts:{GENERATION_CONCEPT}"]
