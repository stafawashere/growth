"""The served item carries the worked steps its fading stage shows, and the pre-submission prompt.

docs/plan/11-phased-delivery.md P1 scope 8: backward fading, the last solution step is the blank
first. Scope 10: one self-explanation prompt, attached to worked examples. The steps come from the
items row's worked_solution, so the fixture rows are rewritten here to carry a step list longer
than two, which is what tells "every step but the last" apart from "only the first".
"""
import json

from sqlalchemy import update
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tests.api.conftest import KEY_MATHJSON, TODAY
from tests.api.test_routes import correct_answer_for, open_session, wrong_answer_for

WORKED_STEPS = [
   {"step": 1, "text": "Factor the numerator so the common factor shows.", "mathjson": ["Multiply", 2, "x"]},
   {"step": 2, "text": "Divide out the common factor from numerator and denominator.", "mathjson": ["Add", "x", 1]},
   {"step": 3, "text": "Evaluate what remains, which gives the final expression.", "mathjson": KEY_MATHJSON},
]

BLANKED_STEP_TEXT = WORKED_STEPS[-1]["text"]


def author_worked_steps(world, steps):
   with OrmSession(world.engine) as db:
      db.execute(update(models.Item).values(worked_solution=json.dumps(steps)))
      db.commit()


def stage_every_skill(world, user_id, stage):
   with OrmSession(world.engine) as db:
      db.execute(
         update(models.SkillState)
         .where(models.SkillState.user_id == user_id)
         .values(fading_stage=stage)
      )
      db.commit()


def served_at(world, client, stage, steps=WORKED_STEPS):
   """Register, move every skill to the stage, and return the session id and the served body."""
   user_id = world.register(client).json()["user"]["id"]
   author_worked_steps(world, steps)
   stage_every_skill(world, user_id, stage)
   session_id = open_session(client).json()["id"]
   served = client.get(f"/sessions/{session_id}/next")

   return session_id, served


def submit(client, session_id, item, answer):
   return client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": answer,
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   )


def test_example_serves_every_worked_step_without_mathjson(world):
   client = world.client()
   session_id, served = served_at(world, client, "example")

   assert served.status_code == 200

   item = served.json()["item"]

   assert item["stage"] == "example"
   assert item["served_steps"] == [
      {"index": position, "text": step["text"]}
      for position, step in enumerate(WORKED_STEPS, start=1)
   ]


def test_completion_serves_every_step_but_the_last(world):
   client = world.client()
   session_id, served = served_at(world, client, "completion")

   assert served.status_code == 200

   item = served.json()["item"]
   given = WORKED_STEPS[:-1]

   assert item["stage"] == "completion"
   assert item["served_steps"] == [
      {"index": position, "text": step["text"]}
      for position, step in enumerate(given, start=1)
   ]
   assert BLANKED_STEP_TEXT not in json.dumps(served.json())
   assert item["self_explanation_prompt"] is None


def test_completion_below_the_two_step_minimum_is_served_at_example(world):
   """Q16: an item with fewer than 2 worked steps is served at example and unsupported only, so a
   completion slot falls back to example rather than refusing the same slot on every read.
   """
   client = world.client()
   one_step = WORKED_STEPS[-1:]
   session_id, served = served_at(world, client, "completion", steps=one_step)

   assert served.status_code == 200

   item = served.json()["item"]

   assert item["stage"] == "example"
   assert item["served_steps"] == [{"index": 1, "text": one_step[0]["text"]}]

   queue = client.get(f"/sessions/{session_id}").json()["queue"]
   slots = [slot for block in ("block1", "block2", "block3") for slot in queue[block]]
   served_slot = next(slot for slot in slots if slot["id"] == item["id"])

   assert served_slot["stage"] == "example"

   attempted = submit(client, session_id, item, correct_answer_for(item))

   assert attempted.status_code == 200

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempted.json()["id"])

      assert stored.served_stage == "example"


def test_unsupported_serves_no_steps_and_no_prompt(world):
   client = world.client()
   session_id, served = served_at(world, client, "unsupported")
   item = served.json()["item"]

   assert item["stage"] == "unsupported"
   assert item["served_steps"] is None
   assert item["self_explanation_prompt"] is None


def test_the_example_prompt_before_submission_is_the_feedback_prompt(world):
   """The prompt names a step the student can see, and the feedback screen asks the same question."""
   client = world.client()
   session_id, served = served_at(world, client, "example")
   item = served.json()["item"]
   before = item["self_explanation_prompt"]
   visible = [f"step {step['index']}," for step in item["served_steps"]]

   assert isinstance(before, str)
   assert any(named in before for named in visible)

   attempted = submit(client, session_id, item, correct_answer_for(item))

   assert attempted.status_code == 200

   attempt_id = attempted.json()["id"]
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200
   assert feedback.json()["self_explanation_prompt"] == before


def test_attempt_response_keeps_only_the_answer_the_student_gave(world):
   """06 attempts.response holds MathJSON or an option id, so a claimed verdict is not stored."""
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   answered = wrong_answer_for(item)
   claimed = dict(answered, correct=True, form="symbolic")
   attempted = submit(client, session_id, item, claimed)

   assert attempted.status_code == 200

   with OrmSession(world.engine) as db:
      stored = json.loads(db.get(models.Attempt, attempted.json()["id"]).response)

   assert "correct" not in stored
   assert stored == answered


def feedback_after(world, client, stage, answer_for):
   session_id, served = served_at(world, client, stage)
   item = served.json()["item"]
   claimed = dict(answer_for(item), step_outcomes=[True] * len(WORKED_STEPS), correct=True)
   attempted = submit(client, session_id, item, claimed)

   assert attempted.status_code == 200

   attempt_id = attempted.json()["id"]
   rated = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": "unsure", "today": TODAY.isoformat()},
   )
   is_rated_stage = stage != "example"

   if is_rated_stage:
      assert rated.status_code == 200

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   return item, feedback.json()


def given_marks(steps):
   return [
      {"index": position, "text": step["text"], "given": True, "correct": None}
      for position, step in enumerate(steps, start=1)
   ]


def blank_mark(correct):
   return {
      "index": len(WORKED_STEPS),
      "text": BLANKED_STEP_TEXT,
      "given": False,
      "correct": correct,
   }


def test_a_wrong_completion_marks_the_blank_wrong_whatever_the_body_claims(world):
   client = world.client()
   item, body = feedback_after(world, client, "completion", wrong_answer_for)

   assert body["step_marks"] == given_marks(WORKED_STEPS[:-1]) + [blank_mark(False)]


def test_a_right_completion_marks_the_blank_right(world):
   client = world.client()
   item, body = feedback_after(world, client, "completion", correct_answer_for)

   assert body["step_marks"] == given_marks(WORKED_STEPS[:-1]) + [blank_mark(True)]


def test_a_worked_example_marks_every_step_as_given(world):
   client = world.client()
   item, body = feedback_after(world, client, "example", correct_answer_for)

   assert body["step_marks"] == given_marks(WORKED_STEPS)


def test_a_corrected_completion_prompt_names_a_step_the_student_was_shown(world):
   """08's feedback wireframe asks about the last given step of a completion, step 3 of 4."""
   client = world.client()
   item, body = feedback_after(world, client, "completion", wrong_answer_for)
   last_shown = item["served_steps"][-1]["index"]

   assert body["self_explanation_prompt"].startswith(f"which rule justifies step {last_shown},")
