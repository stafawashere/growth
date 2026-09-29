"""The comparison step of a productive-failure opener over HTTP (01, Productive-failure openers).

The fixture graph carries no concept records, so no assembly here places an opener; each test
marks the served slot the way app/session/build.py does, which is all the attempt and feedback
routes read to tell an opener from an ordinary item.
"""
import json

from sqlalchemy import update
from sqlalchemy.orm import Session as OrmSession

from app.api.routes import sessions as session_routes
from app.db import models
from tests.api.conftest import KEY_MATHJSON, TODAY, WRONG_MATHJSON
from tests.api.test_routes import open_session

WORKED_STEPS = [
   {"step": 1, "text": "Divide out the common factor.", "mathjson": 0},
   {"step": 2, "text": "Evaluate what is left.", "mathjson": KEY_MATHJSON},
]


def give_every_item_worked_steps(engine):
   with OrmSession(engine) as db:
      db.execute(update(models.Item).values(worked_solution=json.dumps(WORKED_STEPS)))
      db.commit()


def mark_served_slot_as_opener(engine, session_id, item_id):
   with OrmSession(engine) as db:
      session_row = db.get(models.Session, session_id)
      queue = json.loads(session_row.queue)

      for block in ("block1", "block2", "block3"):
         for slot in queue[block]:
            if slot["id"] == item_id:
               slot["is_opener"] = True
               slot["opener_concept"] = "BC-CON-03003"

      session_row.queue = json.dumps(queue)
      db.commit()


def refuse_the_tutor(*_arguments, **_keywords):
   raise AssertionError("an opener's comparison makes no tutor call")


def attempt_the_served_item(world, client, mathjson, as_opener=True):
   give_every_item_worked_steps(world.engine)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   if as_opener:
      mark_served_slot_as_opener(world.engine, session_id, item["id"])

   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"form": "symbolic", "mathjson": mathjson},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "unsure",
      },
   )

   assert attempted.status_code == 200

   return session_id, item, attempted.json()


def test_an_opener_miss_gets_the_comparison_and_nothing_else(world, monkeypatch):
   monkeypatch.setattr(session_routes, "tutor_sentence_for", refuse_the_tutor)
   client = world.client()
   world.register(client)
   session_id, item, attempt = attempt_the_served_item(world, client, WRONG_MATHJSON)

   assert attempt["correct"] is False

   response = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback")

   assert response.status_code == 200

   body = response.json()
   first_step = world.settings.session_context.archetypes[item["archetype_id"]]["expected_solution_path"][0]
   comparison = body["comparison"]

   assert body["kind"] == "comparison"
   assert body["elaborated"] is None
   assert body["self_explanation_prompt"] is None
   assert body["sentence"] is None
   assert comparison["first_step"] == first_step
   assert comparison["label"] == f"The method's first step is to {first_step}."
   assert "\n" not in comparison["label"]
   assert comparison["attempt"]["mathjson"] == WRONG_MATHJSON
   assert comparison["worked_steps"] == [
      {"index": 1, "text": WORKED_STEPS[0]["text"]},
      {"index": 2, "text": WORKED_STEPS[1]["text"]},
   ]


def test_an_opener_miss_takes_no_error_note_and_no_self_explanation(world):
   client = world.client()
   world.register(client)
   session_id, _item, attempt = attempt_the_served_item(world, client, WRONG_MATHJSON)
   base = f"/sessions/{session_id}/attempts/{attempt['id']}"

   note = client.post(f"{base}/error-note", json={"note": "I cancelled too early"})
   explanation = client.post(f"{base}/self-explanation", json={"answer": "the factor rule"})

   assert note.status_code == 409
   assert explanation.status_code == 409


def test_an_ordinary_miss_still_gets_elaborated_feedback_and_its_note(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, _item, attempt = attempt_the_served_item(world, client, WRONG_MATHJSON, as_opener=False)
   base = f"/sessions/{session_id}/attempts/{attempt['id']}"
   body = client.get(f"{base}/feedback").json()

   assert body["kind"] == "elaborated"
   assert body["comparison"] is None
   assert client.post(f"{base}/error-note", json={"note": "I cancelled too early"}).status_code == 200


def test_an_opener_that_reaches_the_key_is_told_so(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, _item, attempt = attempt_the_served_item(world, client, KEY_MATHJSON)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback").json()

   assert attempt["correct"] is True
   assert body["kind"] == "correct"
   assert body["comparison"] is None
