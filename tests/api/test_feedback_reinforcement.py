"""A correct answer rated a guess or unsure gets a short tutor note on the rule that made it right,
and a confident correct answer gets no tutor call at all."""
from app.feedback import tutor
from tests.api.conftest import TODAY
from tests.api.test_feedback_sentence import RecordingTutor
from tests.api.test_routes import open_session, serve_as_mcq


def attempt_the_key(world, client, confidence):
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   serve_as_mcq(world, session_id, item["id"])
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"option_id": "A"},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": confidence,
      },
   )

   assert attempted.status_code == 200
   assert attempted.json()["correct"] is True

   return session_id, attempted.json()["id"]


def reinforcement_system_prompt():
   system, _variables = tutor.split_template(tutor.template_text(tutor.CORRECT_REINFORCEMENT))

   return system


def test_a_guessed_correct_answer_gets_one_reinforcement_call_and_keeps_it(world):
   recorder = RecordingTutor()
   world.settings.tutor = recorder
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_the_key(world, client, "guess")
   first = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()
   second = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert first["kind"] == "correct"
   assert first["sentence"] is not None
   assert second["sentence"] == first["sentence"]
   assert len(recorder.requests) == 1
   assert recorder.requests[0].system == reinforcement_system_prompt()


def test_a_confident_correct_answer_makes_no_tutor_call(world):
   recorder = RecordingTutor()
   world.settings.tutor = recorder
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_the_key(world, client, "confident")
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert feedback["kind"] == "correct"
   assert feedback["sentence"] is None
   assert recorder.requests == []
