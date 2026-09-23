"""An attempt the grader cannot settle still reaches a feedback screen the student can leave.

app/items/grade.py returns ungraded for an empty submission and for a comparison it cannot settle.
Stage example collects a graded answer like completion and unsupported do (BUILD-LEDGER.md,
"Decisions taken on the operator's instruction, 2026-09-23", which withdraws 11 implementer
decision 3), so an ungraded attempt at example behaves like one at completion: the blank carries no
verdict and mastery does not move.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.feedback.render import FeedbackKind
from tests.api.conftest import TODAY
from tests.api.test_served_steps import WORKED_STEPS, served_at, submit

UNSETTLED_ANSWER = {"mathjson": None}

VERDICT_KINDS = {FeedbackKind.CORRECT.value, FeedbackKind.ELABORATED.value}


def skills_state_rows(world, user_id):
   with OrmSession(world.engine) as db:
      rows = db.scalars(select(models.SkillState).where(models.SkillState.user_id == user_id)).all()

      return {
         row.skill_id: {
            column.name: getattr(row, column.name) for column in models.SkillState.__table__.columns
         }
         for row in rows
      }


def user_id_of(client):
   return client.get("/me").json()["id"]


def stored_attempt(world, attempt_id):
   with OrmSession(world.engine) as db:
      row = db.get(models.Attempt, attempt_id)

      return {"correct": row.correct, "confidence": row.confidence}


def test_an_example_blank_carries_no_verdict_when_ungraded(world):
   client = world.client()
   session_id, served = served_at(world, client, "example")
   item = served.json()["item"]
   user_id = user_id_of(client)
   before = skills_state_rows(world, user_id)
   attempted = submit(client, session_id, item, UNSETTLED_ANSWER)
   attempt_id = attempted.json()["id"]
   rated = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": "unsure", "today": TODAY.isoformat()},
   )

   assert attempted.status_code == 200
   assert stored_attempt(world, attempt_id)["correct"] is None
   assert rated.status_code == 200
   assert skills_state_rows(world, user_id) == before

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["kind"] not in VERDICT_KINDS
   assert body["elaborated"] is None
   assert [mark["correct"] for mark in body["step_marks"]] == [None] * len(WORKED_STEPS)
   assert body["step_marks"][-1]["given"] is False
   assert body["self_explanation_prompt"] == item["self_explanation_prompt"]


def test_an_ungraded_completion_blank_carries_no_verdict(world):
   client = world.client()
   session_id, served = served_at(world, client, "completion")
   item = served.json()["item"]
   user_id = user_id_of(client)
   before = skills_state_rows(world, user_id)
   attempted = submit(client, session_id, item, UNSETTLED_ANSWER)
   attempt_id = attempted.json()["id"]
   rated = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": "unsure", "today": TODAY.isoformat()},
   )

   assert rated.status_code == 200
   assert skills_state_rows(world, user_id) == before

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   marks = feedback.json()["step_marks"]

   assert [mark["correct"] for mark in marks] == [None] * len(WORKED_STEPS)
   assert marks[-1]["given"] is False
   assert feedback.json()["elaborated"] is None


def test_an_ungraded_unsupported_answer_states_no_verdict_and_the_next_item_follows(world):
   client = world.client()
   session_id, served = served_at(world, client, "unsupported")
   item = served.json()["item"]
   user_id = user_id_of(client)
   before = skills_state_rows(world, user_id)
   attempted = submit(client, session_id, item, UNSETTLED_ANSWER)
   attempt_id = attempted.json()["id"]

   assert attempted.status_code == 200
   assert attempted.json()["confidence"] is None

   rated = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": "confident", "today": TODAY.isoformat()},
   )

   assert rated.status_code == 200
   assert stored_attempt(world, attempt_id) == {"correct": None, "confidence": "confident"}

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["kind"] == FeedbackKind.UNGRADED.value
   assert body["elaborated"] is None
   assert body["step_marks"] == []
   assert body["self_explanation_prompt"] is None
   assert "worked_solution" not in feedback.text

   following = client.get(f"/sessions/{session_id}/next")

   assert following.status_code == 200
   assert following.json()["item"] is not None
   assert following.json()["item"]["id"] != item["id"]
   assert skills_state_rows(world, user_id) == before


def test_an_ungraded_completion_rated_in_the_same_request_moves_no_state(world):
   client = world.client()
   session_id, served = served_at(world, client, "completion")
   item = served.json()["item"]
   user_id = user_id_of(client)
   before = skills_state_rows(world, user_id)
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": UNSETTLED_ANSWER,
         "elapsed_ms": 90000,
         "confidence": "confident",
         "today": TODAY.isoformat(),
      },
   )

   assert attempted.status_code == 200
   assert stored_attempt(world, attempted.json()["id"]) == {"correct": None, "confidence": "confident"}
   assert skills_state_rows(world, user_id) == before
