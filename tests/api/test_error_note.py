"""Route tests for the error-note endpoint that block 4 collects before a corrected item requeues.

docs/plan/02-adaptive-engine.md, Session assembly block 4: "the one-line student-authored error
note for each item corrected in this session". The note belongs to an item the student got wrong,
so a correct attempt is refused rather than annotated.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tests.api.conftest import TODAY, WRONG_MATHJSON
from tests.api.test_routes import correct_answer_for, open_session


def submit_an_attempt(client, session_id, answer=None):
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   submitted = answer if answer is not None else {"form": "symbolic", "mathjson": WRONG_MATHJSON}

   return client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": submitted,
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   ).json()["id"]


def submit_a_correct_attempt(client, session_id):
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   return client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": correct_answer_for(item),
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   ).json()["id"]


def test_error_note_route_refuses_a_correct_attempt(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_a_correct_attempt(client, session_id)

   refused = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "nothing went wrong here"},
   )

   assert refused.status_code == 409

   with OrmSession(world.engine) as db:
      assert db.get(models.Attempt, attempt_id).error_note is None


def test_error_note_route_stores_the_note_on_the_attempt(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)

   noted = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "I dropped the chain rule factor on the inner function."},
   )

   assert noted.status_code == 200
   assert noted.json()["error_note"] == "I dropped the chain rule factor on the inner function."

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempt_id)

      assert stored.error_note == "I dropped the chain rule factor on the inner function."


def test_error_note_route_requires_the_cookie(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)
   client.cookies.clear()

   refused = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "a note"},
   )

   assert refused.status_code == 401


def test_error_note_route_refuses_an_unknown_attempt(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]

   missing = client.post(
      f"/sessions/{session_id}/attempts/ATT-nope/error-note",
      json={"note": "a note"},
   )

   assert missing.status_code == 404


def test_error_note_route_refuses_an_empty_note(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)

   blank = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "   "},
   )

   assert blank.status_code == 400


def test_a_second_error_note_is_refused_and_the_first_survives(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)
   first = "I dropped the chain rule factor on the inner function."
   client.post(f"/sessions/{session_id}/attempts/{attempt_id}/error-note", json={"note": first})

   second = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "actually I misread the bounds"},
   )

   assert second.status_code == 409

   with OrmSession(world.engine) as db:
      stored = db.execute(
         select(models.Attempt.error_note).where(models.Attempt.id == attempt_id)
      ).scalar_one()

      assert stored == first


def test_a_multiline_error_note_is_refused(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)

   refused = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "I dropped the chain rule\nand then I misread the bounds"},
   )

   assert refused.status_code == 400

   with OrmSession(world.engine) as db:
      assert db.get(models.Attempt, attempt_id).error_note is None


def test_a_note_with_a_carriage_return_is_refused(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)

   refused = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": "I dropped the chain rule\rand then I misread the bounds"},
   )

   assert refused.status_code == 400

   with OrmSession(world.engine) as db:
      assert db.get(models.Attempt, attempt_id).error_note is None


def test_error_note_route_refuses_a_note_over_500_characters(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)
   too_long = "a" * 501

   refused = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": too_long},
   )

   assert refused.status_code == 422

   with OrmSession(world.engine) as db:
      stored = db.execute(
         select(models.Attempt.error_note).where(models.Attempt.id == attempt_id)
      ).scalar_one()

      assert stored is None


def test_a_note_of_exactly_500_characters_is_stored(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)
   exactly_500 = "a" * 500

   stored_response = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": exactly_500},
   )

   assert stored_response.status_code == 200

   with OrmSession(world.engine) as db:
      stored = db.execute(
         select(models.Attempt.error_note).where(models.Attempt.id == attempt_id)
      ).scalar_one()

      assert stored == exactly_500


def test_the_refused_second_note_never_reaches_the_column(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   attempt_id = submit_an_attempt(client, session_id)
   first = "I differentiated the outer function only."
   overwrite = "I integrated instead of differentiating."
   client.post(f"/sessions/{session_id}/attempts/{attempt_id}/error-note", json={"note": first})

   client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/error-note",
      json={"note": overwrite},
   )

   with OrmSession(world.engine) as db:
      stored = db.execute(
         select(models.Attempt.error_note).where(models.Attempt.id == attempt_id)
      ).scalar_one()

      assert overwrite not in stored
      assert stored == first
