"""R16 and R29 resolved at serve time rather than at session assembly.

dress_item fixes served["format"] when the queue is built, so every slot of a fresh session
carries the format the user's history implied before the session started. The alternation is per
user per archetype per stage-unsupported attempt, so it has to advance while the session runs.
These tests drive the service through the same fixture world tests/session/test_service.py uses.
"""
import json

from app.db import models
from app.engine.state import Confidence, FadingStage, ResponseFormat
from app.session import repository, service
from tests.engine.conftest_selection import ACCOUNT_CREATED_AT
from tests.session.test_service import (
   NOW,
   SNAPSHOT_ID,
   TODAY,
   USER_ID,
   only_split_archetype,
   world,
)

ITEMS_PER_ARCHETYPE = 3
UNGRADED = {"response": "3x^2"}


def item_row(item_id, archetype_id, skills):
   return models.Item(
      id=item_id,
      archetype_id=archetype_id,
      variant_id=None,
      snapshot_id=SNAPSHOT_ID,
      parameter_draw="{}",
      stem="stem",
      figure_spec=None,
      options=None,
      answer_key=json.dumps({"form": "symbolic", "mathjson": ["Add", "x", 1]}),
      worked_solution="differentiate term by term",
      calculator_status="no_calculator",
      representation="BC-REP-01",
      difficulty_settings="{}",
      skills=json.dumps(list(skills)),
      provenance="{}",
      status="verified",
      dedupe_minhash="[]",
      created_at=TODAY.isoformat(),
      updated_at=TODAY.isoformat(),
   )


def publish_items(world):
   """load_attempts_history reads archetype_id off the items table, so the bank needs rows."""
   for record in world.fixture["archetypes"]:
      for index in range(ITEMS_PER_ARCHETYPE):
         world.db.add(item_row(
            f"{record['id']}-V{index:02d}", record["id"], record["skills"]
         ))

   world.db.commit()


def set_stage(world, stage):
   states = repository.load_states(world.db, USER_ID)

   for state in states.values():
      if not state.mastered:
         state.fading_stage = stage
         state.observation_count = 1
         state.credited_observation_count = 1

   repository.save_states(world.db, USER_ID, states, SNAPSHOT_ID, ACCOUNT_CREATED_AT)
   world.db.commit()


def one_archetype_at(world, stage):
   """Serve one archetype only, at one stage, so consecutive slots share an alternation counter."""
   only_split_archetype(world)
   publish_items(world)
   set_stage(world, stage)


def stored_slot(world, session_id, item_id):
   queue = json.loads(world.db.get(models.Session, session_id).queue)

   for block in service.SERVING_BLOCKS:
      for slot in queue[block]:
         if slot["id"] == item_id:
            return slot

   return None


def serve_and_submit(world, session_row):
   item = service.next_item(world.db, session_row.id)
   service.record_attempt(
      world.db,
      session_row.id,
      item["id"],
      UNGRADED,
      90000,
      TODAY,
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      now=NOW,
   )

   return item


def test_first_unsupported_serve_is_short_answer(world):
   one_archetype_at(world, FadingStage.UNSUPPORTED)
   opened = world.open()
   item = service.next_item(world.db, opened.id)

   assert item["stage"] == FadingStage.UNSUPPORTED
   assert item["format"] == ResponseFormat.SHORT_ANSWER


def test_second_unsupported_serve_on_the_same_archetype_is_mcq(world):
   one_archetype_at(world, FadingStage.UNSUPPORTED)
   opened = world.open()
   first = serve_and_submit(world, opened)
   second = service.next_item(world.db, opened.id)

   assert first["format"] == ResponseFormat.SHORT_ANSWER
   assert second["archetype_id"] == first["archetype_id"]
   assert second["stage"] == FadingStage.UNSUPPORTED
   assert second["format"] == ResponseFormat.MCQ


def test_example_and_completion_slots_are_always_short_answer(world):
   one_archetype_at(world, FadingStage.EXAMPLE)
   at_example = world.open()
   first = serve_and_submit(world, at_example)
   second = service.next_item(world.db, at_example.id)

   assert first["stage"] == FadingStage.EXAMPLE
   assert first["format"] == ResponseFormat.SHORT_ANSWER
   assert second["format"] == ResponseFormat.SHORT_ANSWER

   set_stage(world, FadingStage.COMPLETION)
   at_completion = world.open()
   third = service.next_item(world.db, at_completion.id)

   assert third["stage"] == FadingStage.COMPLETION
   assert third["format"] == ResponseFormat.SHORT_ANSWER


def test_serving_twice_without_submitting_returns_the_same_format(world):
   one_archetype_at(world, FadingStage.UNSUPPORTED)
   opened = world.open()
   serve_and_submit(world, opened)
   served = service.next_item(world.db, opened.id)
   served_again = service.next_item(world.db, opened.id)

   assert served["id"] == served_again["id"]
   assert served["format"] == ResponseFormat.MCQ
   assert served_again["format"] == ResponseFormat.MCQ


def test_the_served_format_is_persisted_on_the_queue_slot(world):
   one_archetype_at(world, FadingStage.UNSUPPORTED)
   opened = world.open()
   first = serve_and_submit(world, opened)
   second = service.next_item(world.db, opened.id)
   attempt = service.record_attempt(
      world.db,
      opened.id,
      second["id"],
      UNGRADED,
      90000,
      TODAY,
      archetypes=world.archetypes,
      engine_graph=world.engine_graph,
      now=NOW,
   )

   assert stored_slot(world, opened.id, first["id"])["format"] == ResponseFormat.SHORT_ANSWER
   assert stored_slot(world, opened.id, second["id"])["format"] == ResponseFormat.MCQ
   assert attempt.format == ResponseFormat.MCQ

def test_an_attempt_that_skipped_the_serve_still_records_the_resolved_format(world):
   """Gate 12 states the property over attempts, so the write path resolves the format too.

   A client that posts straight to the attempts route without ever reading GET /next would
   otherwise record the assembly-frozen format on every row, and Observation.response_format is
   what applies the 0.75 MCQ credit discount.
   """
   one_archetype_at(world, FadingStage.UNSUPPORTED)
   opened = world.open()
   slots = [item for _, _, item in service.served_positions(opened)]
   formats = []

   for item in slots[:2]:
      attempt = service.record_attempt(
         world.db,
         opened.id,
         item["id"],
         {"form": "symbolic", "mathjson": ["Add", 1, 1]},
         90000,
         TODAY,
         archetypes=world.archetypes,
         engine_graph=world.engine_graph,
         confidence=Confidence.CONFIDENT,
         now=NOW,
      )
      formats.append(attempt.format)

   assert len(formats) == 2
   assert formats == [ResponseFormat.SHORT_ANSWER.value, ResponseFormat.MCQ.value]
