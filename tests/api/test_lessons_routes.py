"""The six lesson endpoints of the lessons framework contract (docs/plan/15-lessons.md, Endpoints),
over the conftest application with lesson rows stored directly, so these tests read the routes and
not the checker."""
import copy
import json
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db import models

REPO_ROOT = Path(__file__).resolve().parents[2]
RECORD = json.loads((REPO_ROOT / "content" / "lessons" / "LSN-CON-02013.json").read_text())
LESSON_ID = RECORD["id"]
TARGET_ID = RECORD["target_id"]
UNIT_ID = "BC-UNIT-02"
SESSION_ID = "SES-lesson-route"
STAMP = "2026-09-29T12:00:00+00:00"
KEY_CHECK = "chk-2"
MCQ_CHECK = "chk-3"
KEY_MATHJSON = ["Add", ["Multiply", 5, ["Power", "x", 4]], ["Multiply", -6, ["Power", "x", 2]], -3]
WRONG_MATHJSON = ["Add", ["Multiply", 5, ["Power", "x", 4]], -3]


@pytest.fixture(scope="module")
def snapshot():
   return load_snapshot(REPO_ROOT / "data")


def lesson_row(status, version=1):
   body = copy.deepcopy(RECORD)
   body["status"] = status
   body["version"] = version

   return models.Lesson(
      id=LESSON_ID,
      version=version,
      kind="con",
      target_id=TARGET_ID,
      snapshot_id="SNAP-0001",
      body=body,
      read_minutes_full=body["read_minutes"]["full"],
      read_minutes_brief=body["read_minutes"]["brief"],
      status=status,
      provenance=body["provenance"],
      source_digest=body["source_digest"],
      created_at=STAMP,
      updated_at=STAMP,
   )


def store_lesson(world, status):
   with OrmSession(world.engine) as db:
      db.add(lesson_row(status))
      db.commit()


@pytest.fixture
def reader(world, snapshot):
   world.settings.session_context.snapshot = snapshot
   store_lesson(world, "signed_off")
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]

   return client, user_id


def rows_of(world, model, user_id):
   with OrmSession(world.engine) as db:
      return db.scalars(select(model).where(model.user_id == user_id)).all()


def product_rule_entry(payload):
   return next(entry for unit in payload["units"] for entry in unit["concepts"] if entry["concept_id"] == TARGET_ID)


def test_the_lesson_routes_need_a_session(world):
   client = world.client()

   assert client.get("/lessons").status_code == 401
   assert client.get(f"/lessons/{LESSON_ID}").status_code == 401
   assert client.post(f"/lessons/{LESSON_ID}/events", json={"event": "opened", "elapsed_ms": 1}).status_code == 401


def test_the_listing_covers_every_unit_without_a_unit(reader):
   client, _ = reader
   payload = client.get("/lessons").json()
   entry = product_rule_entry(payload)

   assert len(payload["units"]) == 10
   assert payload["units"][0]["id"] == "BC-UNIT-01"
   assert entry["lesson_id"] == LESSON_ID
   assert entry["servable"] is True
   assert entry["state"] == "coming_up"


def test_the_listing_narrows_to_one_unit(reader):
   client, _ = reader
   payload = client.get("/lessons", params={"unit": UNIT_ID}).json()
   states = {entry["state"] for entry in payload["units"][0]["concepts"] if entry["concept_id"] != TARGET_ID}

   assert [unit["id"] for unit in payload["units"]] == [UNIT_ID]
   assert states == {"not_available"}


def test_an_unknown_unit_is_404(reader):
   client, _ = reader

   assert client.get("/lessons", params={"unit": "BC-UNIT-99"}).status_code == 404


def test_a_signed_off_lesson_is_served_with_a_null_state(reader):
   client, _ = reader
   response = client.get(f"/lessons/{LESSON_ID}")

   assert response.status_code == 200
   assert response.json()["id"] == LESSON_ID
   assert response.json()["state"] is None


def test_a_draft_lesson_is_404(world, snapshot):
   world.settings.session_context.snapshot = snapshot
   store_lesson(world, "draft")
   client = world.client()
   world.register(client)

   assert client.get(f"/lessons/{LESSON_ID}").status_code == 404
   assert client.get(f"/lessons/{LESSON_ID}/plan", params={"band": "low"}).status_code == 404
   assert client.post(f"/lessons/{LESSON_ID}/events", json={"event": "opened", "elapsed_ms": 1}).status_code == 404


def test_an_unknown_lesson_is_404(reader):
   client, _ = reader

   assert client.get("/lessons/LSN-CON-09999").status_code == 404


@pytest.mark.parametrize("band", ["low", "mid"])
def test_the_plan_is_served_for_both_bands(reader, band):
   client, _ = reader
   response = client.get(f"/lessons/{LESSON_ID}/plan", params={"band": band, "reason": "first_contact"})
   payload = response.json()

   assert response.status_code == 200
   assert payload["band"] == band
   assert payload["plan"]["lesson_id"] == LESSON_ID
   assert payload["plan"]["reason"] == "first_contact"
   assert len(payload["plan"]["sections"]) > 0
   assert payload["lesson"]["id"] == LESSON_ID


def test_the_plan_defaults_to_read_again_and_refuses_a_bad_band(reader):
   client, _ = reader

   assert client.get(f"/lessons/{LESSON_ID}/plan", params={"band": "low"}).json()["plan"]["reason"] == "read_again"
   assert client.get(f"/lessons/{LESSON_ID}/plan", params={"band": "high"}).status_code == 422
   assert client.get(f"/lessons/{LESSON_ID}/plan").status_code == 422


def test_a_library_completed_writes_read_state(reader, world):
   client, user_id = reader
   response = client.post(f"/lessons/{LESSON_ID}/events", json={"event": "completed", "elapsed_ms": 90000, "band": "low"})
   state = response.json()["state"]
   events = rows_of(world, models.LessonEvent, user_id)

   assert response.status_code == 200
   assert response.json()["ok"] is True
   assert state["status"] == "read"
   assert state["read_source"] == "library"
   assert state["version_seen"] == 1
   assert state["read_at"] is not None
   assert [(event.kind, event.event) for event in events] == [("library", "completed")]
   assert product_rule_entry(client.get("/lessons").json())["state"] == "read"


def test_a_library_section_view_records_its_mode_and_no_state(reader, world):
   client, user_id = reader
   body = {"event": "section_viewed", "section_id": f"{LESSON_ID}#s1", "mode": "text", "elapsed_ms": 4000}
   response = client.post(f"/lessons/{LESSON_ID}/events", json=body)
   events = rows_of(world, models.LessonEvent, user_id)

   assert response.json()["state"] is None
   assert [(event.section_id, event.mode) for event in events] == [(f"{LESSON_ID}#s1", "text")]


def test_an_event_body_is_validated(reader):
   client, _ = reader

   assert client.post(f"/lessons/{LESSON_ID}/events", json={"event": "burned", "elapsed_ms": 1}).status_code == 422
   assert client.post(f"/lessons/{LESSON_ID}/events", json={"event": "opened"}).status_code == 422


def own_session(world, user_id):
   with OrmSession(world.engine) as db:
      db.add(models.Session(
         id=SESSION_ID,
         user_id=user_id,
         mode="standard",
         sub_mode=None,
         started_at=STAMP,
         ended_at=None,
         queue="[]",
         updates_mastery=1,
         snapshot_id="SNAP-0001",
         created_at=STAMP,
         updated_at=STAMP,
      ))
      db.commit()


def test_session_events_write_kind_lesson_and_the_state(reader, world):
   client, user_id = reader
   own_session(world, user_id)
   path = f"/sessions/{SESSION_ID}/lessons/{LESSON_ID}/events"
   opened = client.post(path, json={"event": "opened", "elapsed_ms": 0, "band": "mid", "reason": "first_contact"})
   completed = client.post(path, json={"event": "completed", "elapsed_ms": 120000, "band": "mid", "reason": "first_contact"})
   events = rows_of(world, models.LessonEvent, user_id)

   assert opened.json()["state"]["status"] == "served"
   assert opened.json()["state"]["band_served"] == "mid"
   assert completed.json()["state"]["status"] == "read"
   assert completed.json()["state"]["read_source"] == "session"
   assert [(event.kind, event.event, event.session_id) for event in events] == [("lesson", "opened", SESSION_ID), ("lesson", "completed", SESSION_ID)]


def test_a_refresher_reason_writes_kind_refresher(reader, world):
   client, user_id = reader
   own_session(world, user_id)
   response = client.post(f"/sessions/{SESSION_ID}/lessons/{LESSON_ID}/events", json={"event": "completed", "elapsed_ms": 30000, "reason": "T1"})
   events = rows_of(world, models.LessonEvent, user_id)

   assert response.json()["state"]["refresher_count"] == 1
   assert [(event.kind, event.reason) for event in events] == [("refresher", "T1")]


def test_another_users_session_is_404(reader):
   client, _ = reader

   assert client.post(f"/sessions/SES-nobody/lessons/{LESSON_ID}/events", json={"event": "opened", "elapsed_ms": 0}).status_code == 404


def answer(client, check, body):
   return client.post(f"/lessons/{LESSON_ID}/checks/{check}/answers", json=body)


def test_a_correct_short_answer(reader, world):
   client, user_id = reader
   response = answer(client, KEY_CHECK, {"answer": KEY_MATHJSON, "elapsed_ms": 20000})
   responses = rows_of(world, models.LessonCheckResponse, user_id)

   assert response.json() == {"correct": True, "error_id": None, "anchor": None, "explanation_anchor": None}
   assert [(row.check_id, row.correct) for row in responses] == [(f"{LESSON_ID}#{KEY_CHECK}", 1)]


def test_a_wrong_short_answer_names_no_error(reader):
   client, _ = reader
   response = answer(client, KEY_CHECK, {"answer": WRONG_MATHJSON, "elapsed_ms": 20000})

   assert response.json()["correct"] is False
   assert response.json()["error_id"] is None
   assert response.json()["anchor"] is None


def test_a_wrong_mcq_option_links_its_error_block(reader):
   client, _ = reader
   response = answer(client, MCQ_CHECK, {"option_id": "B", "elapsed_ms": 15000})

   assert response.json()["correct"] is False
   assert response.json()["error_id"] == "BC-ERR-02020"
   assert response.json()["anchor"] == f"{LESSON_ID}#err-BC-ERR-02020"


def test_the_key_option_is_correct(reader):
   client, _ = reader

   assert answer(client, MCQ_CHECK, {"option_id": "C", "elapsed_ms": 15000}).json()["correct"] is True


def test_a_full_check_id_is_accepted_url_encoded(reader):
   client, _ = reader
   response = client.post(f"/lessons/{LESSON_ID}/checks/{LESSON_ID}%23{MCQ_CHECK}/answers", json={"option_id": "C", "elapsed_ms": 1})

   assert response.json()["correct"] is True


def test_an_unknown_check_is_404_and_a_bad_body_422(reader):
   client, _ = reader

   assert answer(client, "chk-9", {"option_id": "C", "elapsed_ms": 1}).status_code == 404
   assert answer(client, MCQ_CHECK, {"option_id": "C"}).status_code == 422


def test_check_answers_never_write_attempts(reader, world):
   client, _ = reader
   answer(client, KEY_CHECK, {"answer": KEY_MATHJSON, "elapsed_ms": 1})
   answer(client, MCQ_CHECK, {"option_id": "B", "elapsed_ms": 1})

   with OrmSession(world.engine) as db:
      assert db.scalars(select(models.Attempt)).all() == []
