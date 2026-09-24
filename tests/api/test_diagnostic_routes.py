"""The diagnostic session over HTTP (11 P2 scope items 1, 7 and 9), on the P1 fixture world."""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session import repository
from tests.api.conftest import TODAY
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
