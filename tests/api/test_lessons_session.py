"""Lessons in the learning session over HTTP (docs/plan/15-lessons.md, Tests, Integration; and
Diagnosis links to lesson sections).

A no-units student (every skill unobserved, a low prior, as a student who declared every unit not
learned) opens a session over the fixture graph with a fixture lesson directory: signed_off copies
of content/lessons/LSN-CON-02013.json retargeted to every concept of the fixture graph, so the test
does not depend on production content.
"""
import json
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session import repository
from tests.api.conftest import KEY_MATHJSON, SNAPSHOT_ID
from tests.engine.conftest_selection import build_graph, build_states, load_fixture

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "content" / "lessons" / "LSN-CON-02013.json"
STAMP = "2026-03-01T09:00:00+00:00"
NO_UNITS_BETA = -3.0
ANCHORED_ERROR = "BC-ERR-02020"
WORKED_STEPS = [
   {"step": 1, "text": "Divide out the common factor.", "mathjson": 0},
   {"step": 2, "text": "Evaluate what is left.", "mathjson": KEY_MATHJSON},
]


def write_lesson_directory(directory, concept_ids):
   """One signed_off record per concept, the section ids moved to the new lesson id."""
   directory.mkdir()
   record = json.loads(SOURCE.read_text())

   for concept_id in concept_ids:
      lesson_id = f"LSN-CON-{concept_id[7:]}"
      text = json.dumps(record).replace(record["id"], lesson_id)
      body = json.loads(text)
      body["target_id"] = concept_id
      body["status"] = "signed_off"
      body["read_minutes"] = {"full": 2.0, "brief": 1.5}
      (directory / f"{lesson_id}.json").write_text(json.dumps(body))

   return directory


def store_directory(engine, directory):
   with OrmSession(engine) as db:
      for path in sorted(directory.glob("*.json")):
         body = json.loads(path.read_text())
         db.add(
            models.Lesson(
               id=body["id"],
               version=body["version"],
               kind="con",
               target_id=body["target_id"],
               snapshot_id=SNAPSHOT_ID,
               body=body,
               read_minutes_full=body["read_minutes"]["full"],
               read_minutes_brief=body["read_minutes"]["brief"],
               status=body["status"],
               provenance=body["provenance"],
               source_digest=body["source_digest"],
               created_at=STAMP,
               updated_at=STAMP,
            )
         )

      db.commit()


def give_every_item_worked_steps(engine):
   """A stage example item shows its worked steps, so the fixture rows carry a step list."""
   with OrmSession(engine) as db:
      for row in db.scalars(select(models.Item)).all():
         row.worked_solution = json.dumps(WORKED_STEPS)

      db.commit()


def no_units_states(fixture):
   states = build_states(fixture)

   for state in states.values():
      if not state.mastered:
         state.beta = NO_UNITS_BETA

   return states


@pytest.fixture
def student(world, tmp_path):
   fixture = load_fixture()
   concepts = sorted({record["concept"] for record in build_graph(fixture).skills.values()})
   store_directory(world.engine, write_lesson_directory(tmp_path / "lessons", concepts))
   give_every_item_worked_steps(world.engine)

   def seed_hook(db, user_id, snapshot, created_at, snapshot_id=None):
      states = no_units_states(fixture)
      repository.save_states(db, user_id, states, SNAPSHOT_ID, created_at)

      return len(states)

   world.settings.seed_hook = seed_hook
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]

   return client, user_id


def entries_of(block, kind):
   return [entry for entry in block if entry.get("kind") == kind]


def state_rows(world, user_id):
   with OrmSession(world.engine) as db:
      rows = db.scalars(select(models.LessonState).where(models.LessonState.user_id == user_id)).all()

      return {row.lesson_id: row.status for row in rows}


def event_rows(world, user_id):
   with OrmSession(world.engine) as db:
      rows = db.scalars(select(models.LessonEvent).where(models.LessonEvent.user_id == user_id)).all()

      return [(row.lesson_id, row.kind, row.event, row.reason) for row in rows]


def all_lesson_ids(world):
   with OrmSession(world.engine) as db:
      return set(db.scalars(select(models.Lesson.id)).all())


LATER_DAYS = ("2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05", "2026-03-06", "2026-03-07")


def loads_concept(world, entry, concept_id):
   skills = world.settings.session_context.archetypes[entry["archetype_id"]]["skills"]
   concepts = {skill["concept"] for skill in build_graph(load_fixture()).skills.values() if skill["id"] in skills}

   return concept_id in concepts


def deferred_session_block2(world, client, deferred_id):
   """Block 2 of the first later session that serves the deferred lesson. A session that does not
   serve it must hold no item on its concept, since that item would have needed the lesson first."""
   for day in LATER_DAYS:
      block2 = client.post("/sessions", json={"today": day}).json()["queue"]["block2"]
      lesson_ids = [lesson["lesson_id"] for lesson in entries_of(block2, "lesson")]
      has_deferred = deferred_id in lesson_ids

      if has_deferred:
         return block2

      concept_id = deferred_id.replace("LSN-CON-", "BC-CON-")
      unlessoned = [entry for entry in entries_of(block2, "item") if loads_concept(world, entry, concept_id)]

      assert unlessoned == []

   raise AssertionError(f"no session from {LATER_DAYS[0]} to {LATER_DAYS[-1]} served {deferred_id}")


def post_event(client, session_id, entry, event, section_id=None, mode=None):
   body = {"event": event, "elapsed_ms": 60000, "band": entry["band"], "reason": entry["reason"]}

   if section_id is not None:
      body["section_id"] = section_id
      body["mode"] = mode

   return client.post(f"/sessions/{session_id}/lessons/{entry['lesson_id']}/events", json=body)


def test_a_no_units_student_reads_two_lessons_defers_the_third_and_meets_it_next_session(world, student):
   client, user_id = student
   opened = client.post("/sessions", json={"today": "2026-03-01"}).json()
   block2 = opened["queue"]["block2"]
   lessons = entries_of(block2, "lesson")
   items = entries_of(block2, "item")

   assert len(lessons) == 2
   assert len({lesson["concept_id"] for lesson in lessons}) == 2

   for lesson in lessons:
      following = block2[block2.index(lesson) + 1]

      assert following["kind"] == "item"
      assert following["id"] == lesson["before_item_id"]
      assert following["stage"] == "example"
      assert following["preceded_by_lesson_id"] == lesson["lesson_id"]

   linked = [item for item in items if "lesson_link" in item]
   deferred_id = linked[0]["lesson_link"]["lesson_id"]
   served_ids = {lesson["lesson_id"] for lesson in lessons}

   assert deferred_id not in served_ids
   assert entries_of(opened["queue"]["block3"], "lesson") == []
   assert state_rows(world, user_id)[deferred_id] == "deferred"
   assert all(state_rows(world, user_id)[lesson_id] == "served" for lesson_id in served_ids)
   assert (deferred_id, "lesson", "deferred", "lesson_count") in event_rows(world, user_id)

   session_id = opened["id"]
   served = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert served["kind"] == "lesson"
   assert served["lesson"]["id"] == lessons[0]["lesson_id"]
   assert served["plan"]["reason"] == "first_contact"
   assert post_event(client, session_id, served, "section_viewed", served["plan"]["sections"][0]["id"], "text").status_code == 200
   assert post_event(client, session_id, served, "completed").status_code == 200

   first_item = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert first_item["id"] == lessons[0]["before_item_id"]

   attempt = client.post(
      f"/sessions/{session_id}/attempts",
      json={"item_id": first_item["id"], "answer": {"option_id": "A"}, "elapsed_ms": 1000, "today": "2026-03-01", "confidence": "unsure"},
   ).json()

   with OrmSession(world.engine) as db:
      row = db.get(models.Attempt, attempt["id"])

      assert (row.preceded_by_lesson_id, row.preceded_by_lesson_version) == (lessons[0]["lesson_id"], lessons[0]["version"])

   second = next(entry for entry in client.get(f"/sessions/{session_id}").json()["remaining"] if entry.get("kind") == "lesson")

   assert post_event(client, session_id, second, "completed").status_code == 200
   assert state_rows(world, user_id)[lessons[0]["lesson_id"]] == "read"
   assert state_rows(world, user_id)[lessons[1]["lesson_id"]] == "read"
   assert client.post(f"/sessions/{session_id}/close", json={"today": "2026-03-01"}).status_code == 200

   # The student reads every other lesson in the library, so the deferred one is the only lesson
   # the next session can serve and the test does not hang on which concept selection reaches.
   for concept_lesson in state_rows(world, user_id).keys() | all_lesson_ids(world):
      is_other = concept_lesson not in served_ids and concept_lesson != deferred_id

      if is_other:
         assert client.post(f"/lessons/{concept_lesson}/events", json={"event": "completed", "elapsed_ms": 1000}).status_code == 200

   # Selection keeps its random ties (R4), so the deferred concept's next item may land in any later
   # session; the lesson must precede it in whichever session it lands.
   later_block2 = deferred_session_block2(world, client, deferred_id)
   later_lessons = entries_of(later_block2, "lesson")
   deferred_lesson = next(lesson for lesson in later_lessons if lesson["lesson_id"] == deferred_id)
   concept_items = [entry for entry in entries_of(later_block2, "item") if loads_concept(world, entry, deferred_lesson["concept_id"])]

   assert later_lessons[0]["lesson_id"] == deferred_id
   assert all(lesson["lesson_id"] not in served_ids for lesson in later_lessons)
   assert later_block2.index(deferred_lesson) < later_block2.index(concept_items[0])
   assert later_block2[later_block2.index(deferred_lesson) + 1]["id"] == deferred_lesson["before_item_id"]


def test_a_skipped_lesson_consumes_its_slot_and_the_item_follows(world, student):
   client, user_id = student
   opened = client.post("/sessions", json={"today": "2026-03-01"}).json()
   session_id = opened["id"]
   served = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert post_event(client, session_id, served, "skipped", served["plan"]["sections"][1]["id"], "text").status_code == 200

   following = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert following["kind"] == "item"
   assert following["id"] == served["before_item_id"]
   assert state_rows(world, user_id)[served["lesson_id"]] == "skipped"


def first_lessoned_item(client):
   opened = client.post("/sessions", json={"today": "2026-03-01"}).json()
   session_id = opened["id"]
   lesson = client.get(f"/sessions/{session_id}/next").json()["item"]
   post_event(client, session_id, lesson, "completed")
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   return session_id, item


def wrong_attempt(client, session_id, item):
   return client.post(
      f"/sessions/{session_id}/attempts",
      json={"item_id": item["id"], "answer": {"option_id": "B"}, "elapsed_ms": 1000, "today": "2026-03-01", "confidence": "unsure"},
   ).json()


def anchor_error(world, error_id):
   """Make the fixture bank's distractors name an error the lessons anchor."""
   with OrmSession(world.engine) as db:
      for row in db.scalars(select(models.Item)).all():
         row.options = [dict(option, error_path=error_id if option["error_path"] else None) for option in row.options]

      db.commit()


def test_feedback_links_the_error_block_the_concept_lesson_anchors(world, student):
   client, _ = student
   anchor_error(world, ANCHORED_ERROR)
   session_id, item = first_lessoned_item(client)
   attempt = wrong_attempt(client, session_id, item)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback").json()

   assert feedback["lesson_link"]["lesson_id"] == item["preceded_by_lesson_id"]
   assert feedback["lesson_link"]["anchor"] == f"{item['preceded_by_lesson_id']}#err-{ANCHORED_ERROR}"


def test_no_link_when_the_lesson_has_no_block_for_the_error(world, student):
   client, _ = student
   session_id, item = first_lessoned_item(client)
   attempt = wrong_attempt(client, session_id, item)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback").json()

   assert feedback["lesson_link"] is None


def test_no_link_on_a_probe_tied_diagnosis(world, student):
   client, _ = student
   anchor_error(world, ANCHORED_ERROR)
   session_id, item = first_lessoned_item(client)
   attempt = wrong_attempt(client, session_id, item)

   with OrmSession(world.engine) as db:
      db.add(
         models.Diagnosis(
            id="DGN-probe-tie",
            attempt_id=attempt["id"],
            observed_errors=json.dumps([ANCHORED_ERROR]),
            misconception_hypotheses=json.dumps([]),
            non_conceptual_causes=json.dumps([]),
            prerequisite_gap=None,
            mastery_states=json.dumps({}),
            matched_signal=None,
            probe_scheduled=json.dumps({"archetype_id": item["archetype_id"]}),
            diagnosed_by="test_probe_tie",
            created_at=STAMP,
            updated_at=STAMP,
         )
      )
      db.commit()

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback").json()

   assert feedback["lesson_link"] is None


def test_the_example_first_arm_defers_the_lesson_to_after_the_first_item(world, student):
   client, user_id = student
   world.settings.experiment_default_state = {"lesson_first_contact": "on"}
   opened = client.post("/sessions", json={"today": "2026-03-01"}).json()
   block2 = opened["queue"]["block2"]
   first_item = entries_of(block2, "item")[0]

   assert block2[0]["kind"] == "item"
   assert "lesson_link" in first_item
   assert ("example_first" in {reason for _, kind, event, reason in event_rows(world, user_id) if event == "deferred"})


def test_the_control_arm_serves_the_lesson_before_the_first_item(world, student):
   client, _ = student
   world.settings.experiment_default_state = {"lesson_first_contact": "off"}
   opened = client.post("/sessions", json={"today": "2026-03-01"}).json()

   assert opened["queue"]["block2"][0]["kind"] == "lesson"
