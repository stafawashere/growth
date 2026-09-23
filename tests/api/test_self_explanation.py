"""Route tests for the answer to the structured self-explanation prompt.

docs/plan/11-phased-delivery.md P1 scope 10 attaches exactly one prompt to worked examples and
corrected errors only, so an attempt that is neither is refused, and a second answer never
replaces the first. Every assertion on a write reads attempts.self_explanation back out.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tests.api.test_routes import correct_answer_for, open_session, wrong_answer_for
from tests.api.test_served_steps import served_at, submit

FIRST_ANSWER = "The quotient rule, because the expression is one function divided by another."


def stored_self_explanation(world, attempt_id):
   with OrmSession(world.engine) as db:
      return db.execute(
         select(models.Attempt.self_explanation).where(models.Attempt.id == attempt_id)
      ).scalar_one()


def attempt_at(world, client, stage, answer_for):
   session_id, served = served_at(world, client, stage)
   item = served.json()["item"]
   attempted = submit(client, session_id, item, answer_for(item))

   assert attempted.status_code == 200

   return session_id, attempted.json()["id"]


def explain(client, session_id, attempt_id, answer):
   return client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/self-explanation",
      json={"answer": answer},
   )


def test_a_worked_example_attempt_stores_the_answer(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "example", correct_answer_for)

   written = explain(client, session_id, attempt_id, FIRST_ANSWER)

   assert written.status_code == 200
   assert written.json()["attempt_id"] == attempt_id
   assert stored_self_explanation(world, attempt_id) == FIRST_ANSWER


def test_a_corrected_attempt_stores_the_answer(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "unsupported", wrong_answer_for)

   written = explain(client, session_id, attempt_id, FIRST_ANSWER)

   assert written.status_code == 200
   assert stored_self_explanation(world, attempt_id) == FIRST_ANSWER


def test_a_correct_unsupported_attempt_is_refused(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "unsupported", correct_answer_for)

   refused = explain(client, session_id, attempt_id, FIRST_ANSWER)

   assert refused.status_code == 409
   assert stored_self_explanation(world, attempt_id) is None


def test_a_correct_completion_attempt_is_refused(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "completion", correct_answer_for)

   refused = explain(client, session_id, attempt_id, FIRST_ANSWER)

   assert refused.status_code == 409
   assert stored_self_explanation(world, attempt_id) is None


def test_a_second_answer_is_refused_and_the_first_survives(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "example", correct_answer_for)
   explain(client, session_id, attempt_id, FIRST_ANSWER)

   second = explain(client, session_id, attempt_id, "The chain rule, on reflection.")

   assert second.status_code == 409
   assert stored_self_explanation(world, attempt_id) == FIRST_ANSWER


def test_an_empty_answer_is_refused(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "example", correct_answer_for)

   blank = explain(client, session_id, attempt_id, "   ")

   assert blank.status_code == 422
   assert stored_self_explanation(world, attempt_id) is None


def test_an_unknown_attempt_is_refused(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]

   missing = explain(client, session_id, "ATT-nope", FIRST_ANSWER)

   assert missing.status_code == 404


def test_the_route_requires_the_cookie(world):
   client = world.client()
   session_id, attempt_id = attempt_at(world, client, "example", correct_answer_for)
   client.cookies.clear()

   refused = explain(client, session_id, attempt_id, FIRST_ANSWER)

   assert refused.status_code == 401
   assert stored_self_explanation(world, attempt_id) is None