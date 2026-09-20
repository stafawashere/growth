"""A wrong short answer reaches elaborated feedback over HTTP.

R12 rule 3 gives a wrong short answer no error path, so until this session app/feedback/render.py
refused to compose a payload without a BC-ERR record and the feedback route turned that refusal
into a 409. docs/plan/03-diagnosis-and-feedback.md's Content section names the violated step of
expected_solution_path as what feedback carries when no error matched, which is what the payload
now holds, with the two BC-ERR fields empty rather than invented.
"""
from tests.api.conftest import TODAY, WRONG_MATHJSON
from tests.api.test_routes import open_session


def attempt_a_wrong_short_answer(client):
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert item["format"] == "short_answer"

   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"form": "symbolic", "mathjson": WRONG_MATHJSON},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200
   assert attempted.json()["correct"] is False

   return session_id, attempted.json()["id"]


def test_a_wrong_short_answer_gets_elaborated_feedback(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_a_wrong_short_answer(client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["kind"] == "elaborated"
   assert body["elaborated"]["worked_solution"] == "divide out the factor, then evaluate"
   assert body["elaborated"]["violated_step"]


def test_the_absent_error_fields_are_empty_over_http(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_a_wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["elaborated"]["observed_behavior"] == ""
   assert body["elaborated"]["scoring_consequence"] == ""
   assert body["elaborated"]["error_id"] is None
