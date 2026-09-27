"""The diagnostic session over HTTP (11 P2 scope items 1, 7 and 9), on the P1 fixture world."""
import json

import pytest

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session import diagnostic_session, repository, service
from tests.api.conftest import TODAY, WRONG_MATHJSON, build_world
from tests.api.test_routes import serve_as_mcq


def open_diagnostic(client):
   response = client.post("/sessions", json={"mode": "diagnostic", "today": TODAY.isoformat()})

   assert response.status_code == 200, response.text

   return response.json()["id"]


def next_item(client, session_id):
   response = client.get(f"/sessions/{session_id}/next", params={"today": TODAY.isoformat()})

   assert response.status_code == 200, response.text

   return response.json()


def say_not_learned(client, session_id, item):
   return client.post(
      f"/sessions/{session_id}/attempts",
      json={"item_id": item["id"], "answer": {"not_learned": True}, "elapsed_ms": 5000, "today": TODAY.isoformat()},
   )


def test_a_second_open_resumes_the_unfinished_diagnostic(world):
   client = world.client()
   world.register(client)

   first = open_diagnostic(client)

   assert open_diagnostic(client) == first
   assert client.get("/progress", params={"today": TODAY.isoformat()}).json()["diagnostic_in_progress"] == first


def test_not_learned_answers_credit_nothing_write_a_diagnosis_and_are_never_requeued(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   before = {skill_id: (state.c, state.f, state.mastered) for skill_id, state in world.states(user_id).items()}
   session_id = open_diagnostic(client)
   answered = 0

   while True:
      body = next_item(client, session_id)

      if body["diagnostic_finished"]:
         break

      assert body["item"]["served_steps"] is None

      submitted = say_not_learned(client, session_id, body["item"])

      assert submitted.status_code == 200, submitted.text
      assert submitted.json()["correct"] is None

      answered += 1

   after = {skill_id: (state.c, state.f, state.mastered) for skill_id, state in world.states(user_id).items()}

   assert answered > 0
   assert after == before

   with OrmSession(world.engine) as db:
      attempts = db.query(models.Attempt).filter(models.Attempt.session_id == session_id).all()
      diagnoses = db.query(models.Diagnosis).filter(
         models.Diagnosis.attempt_id.in_([attempt.id for attempt in attempts])
      ).all()
      history = repository.load_attempts_history(db, user_id)
      session_row = db.get(models.Session, session_id)

   assert len(diagnoses) == answered
   assert all(set(json.loads(row.mastery_states).values()) == {"not_attempted"} for row in diagnoses)
   assert all(row.diagnosed_by == "rule_r12_r26" for row in diagnoses)
   assert all(attempt.confidence_source == "diagnostic" for attempt in attempts)
   assert not any(entry["corrected"] for entry in history)
   assert session_row.ended_at is not None

   result = client.get(f"/sessions/{session_id}/diagnostic").json()

   assert result["finished"] is True
   assert result["asked"] == answered


def test_an_item_other_than_the_waiting_one_is_refused(world):
   client = world.client()
   world.register(client)
   session_id = open_diagnostic(client)
   item = next_item(client, session_id)["item"]
   wrong = dict(item, id=item["id"] + "-other")

   assert say_not_learned(client, session_id, wrong).status_code == 409
   assert say_not_learned(client, session_id, item).status_code == 200
   assert say_not_learned(client, session_id, item).status_code == 409


def test_the_diagnostic_result_route_refuses_an_ordinary_session(world):
   client = world.client()
   world.register(client)
   opened = client.post("/sessions", json={"today": TODAY.isoformat()}).json()

   assert client.get(f"/sessions/{opened['id']}/diagnostic").status_code == 404


def test_a_graded_distractor_in_an_ordinary_session_writes_its_error_path_as_the_diagnosis(world):
   client = world.client()
   world.register(client)
   session_id = client.post("/sessions", json={"mode": "learning", "today": TODAY.isoformat()}).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   serve_as_mcq(world, session_id, item["id"])
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={"item_id": item["id"], "answer": {"option_id": "B"}, "elapsed_ms": 90000, "today": TODAY.isoformat()},
   )

   assert attempted.status_code == 200, attempted.text
   assert attempted.json()["correct"] is False

   with OrmSession(world.engine) as db:
      rows = db.query(models.Diagnosis).filter(models.Diagnosis.attempt_id == attempted.json()["id"]).all()

   assert len(rows) == 1
   assert json.loads(rows[0].observed_errors) == ["BC-ERR-02001"]
   assert json.loads(rows[0].misconception_hypotheses) == []


def skip_unit(client, session_id, item):
   return client.post(
      f"/sessions/{session_id}/diagnostic/skip-unit",
      json={"item_id": item["id"], "elapsed_ms": 5000, "today": TODAY.isoformat()},
   )


def answer_wrongly(client, session_id, item):
   return client.post(
      f"/sessions/{session_id}/attempts",
      json={"item_id": item["id"], "answer": {"mathjson": WRONG_MATHJSON}, "elapsed_ms": 5000, "today": TODAY.isoformat()},
   )


def unit_of_waiting_item(world, session_id):
   with OrmSession(world.engine) as db:
      return diagnostic_session.waiting_unit(db.get(models.Session, session_id))


def placement_and_answers(world, user_id, session_id):
   with OrmSession(world.engine) as db:
      run = diagnostic_session.load_run(db.get(models.Session, session_id))
      attempts = db.query(models.Attempt).filter(models.Attempt.session_id == session_id).all()
      answers = sorted((attempt.item_id, attempt.response) for attempt in attempts)

   states = {
      skill_id: (state.c, state.f, state.mastered, state.stability, state.difficulty)
      for skill_id, state in world.states(user_id).items()
   }

   return {"placement": run.placement, "posterior": run.posterior, "asked": run.asked, "answers": answers, "states": states}


def run_diagnostic(tmp_path, monkeypatch, skip_at=None):
   """One diagnostic on a fresh installation with the same session id, so the run draws the same
   items. The first item's unit is the one skipped. Its items are answered "I have not learned
   this yet" one by one, except that the skip route is used on the skip_at-th of them when given,
   after which the client must never be served that unit again. Every other item is answered
   wrongly, so an item of another unit taken as skipped would change the result."""
   monkeypatch.setattr(service, "new_id", lambda prefix: f"{prefix}-{next(counter)}")
   counter = iter(range(1, 10000))
   tmp_path.mkdir()
   world = build_world(tmp_path)
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   session_id = open_diagnostic(client)
   body = next_item(client, session_id)
   skipped = unit_of_waiting_item(world, session_id)
   occurrences = 0
   has_skipped = False
   served_after_skip = []

   while not body["diagnostic_finished"]:
      item = body["item"]
      unit = unit_of_waiting_item(world, session_id)
      is_skipped_unit = unit == skipped

      if has_skipped:
         served_after_skip.append(unit)

      if is_skipped_unit:
         occurrences += 1

      skips_here = is_skipped_unit and occurrences == skip_at

      if skips_here:
         reply = skip_unit(client, session_id, item)

         assert reply.status_code == 200, reply.text

         body = reply.json()
         has_skipped = True

         continue

      if is_skipped_unit:
         submitted = say_not_learned(client, session_id, item)
      else:
         submitted = answer_wrongly(client, session_id, item)

      assert submitted.status_code == 200, submitted.text

      body = next_item(client, session_id)

   assert skipped not in served_after_skip
   assert has_skipped == (skip_at is not None)

   return placement_and_answers(world, user_id, session_id), occurrences, skipped


@pytest.mark.parametrize("skip_at", [1, 2])
def test_skipping_a_unit_places_exactly_as_answering_not_learned_to_each_of_its_items(tmp_path, monkeypatch, skip_at):
   skipped_run, _, skipped_unit = run_diagnostic(tmp_path / "skip", monkeypatch, skip_at=skip_at)
   one_by_one_run, served_in_unit, unit = run_diagnostic(tmp_path / "one-by-one", monkeypatch)
   not_learned = [entry for entry in one_by_one_run["asked"] if entry["outcome"] == "not_learned"]

   assert skipped_unit == unit
   assert served_in_unit >= 3
   assert len(not_learned) == served_in_unit
   assert {entry["unit"] for entry in not_learned} == {unit}
   assert skipped_run["placement"] is not None
   assert skipped_run == one_by_one_run


def test_skipping_refuses_an_item_that_is_not_on_screen_and_an_ordinary_session(world):
   client = world.client()
   world.register(client)
   session_id = open_diagnostic(client)
   item = next_item(client, session_id)["item"]
   ordinary = client.post("/sessions", json={"mode": "learning", "today": TODAY.isoformat()}).json()["id"]

   assert skip_unit(client, session_id, dict(item, id=item["id"] + "-other")).status_code == 409
   assert skip_unit(client, ordinary, item).status_code == 404

   with OrmSession(world.engine) as db:
      attempts = db.query(models.Attempt).filter(models.Attempt.session_id == session_id).count()

   assert attempts == 0


def test_questions_are_numbered_from_the_first_and_never_past_the_cap(world):
   client = world.client()
   world.register(client)
   session_id = open_diagnostic(client)
   positions = []
   body = next_item(client, session_id)

   while not body["diagnostic_finished"]:
      positions.append(body["item"]["diagnostic_position"])

      assert say_not_learned(client, session_id, body["item"]).status_code == 200

      body = next_item(client, session_id)

   cap = client.get(f"/sessions/{session_id}/diagnostic").json()["cap"]

   assert positions == list(range(len(positions)))
   assert all(position < cap for position in positions)
