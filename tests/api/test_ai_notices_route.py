"""GET /notices: a tutor call made through the feedback route is told to the student who made it,
and to no one else.

The tutor is a ReplayProvider, the backend GROWTH_AI_BACKEND=replay wires, so no test opens a
socket.
"""
from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.feedback import tutor
from app.providers import notices
from app.providers.guard import BudgetCaps, GuardedProvider
from app.providers.replay import ReplayProvider
from tests.api.test_feedback_sentence import attempt_one_distractor

SENTENCE = "The inner derivative is missing, so the answer point is lost."
OTHER_SENTENCE = "Another student's feedback sentence."
OTHER_USER_ID = "USR-SOMEONE-ELSE"
OTHER_FIELDS = {
   "violated_step": "Another student's step.",
   "observed_behavior": "Another student's behavior.",
   "scoring_consequence": "Another student's consequence.",
   "worked_solution": "Another student's solution.",
}

CASSETTE = {
   "text": SENTENCE,
   "finish_reason": "end_turn",
   "usage": {"input_tokens": 1200, "output_tokens": 40, "cached_read_tokens": 0, "cached_write_tokens": 0},
}


def feedback_read(world, client):
   session_id, attempt_id = attempt_one_distractor(world, client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200
   assert feedback.json()["sentence"] == SENTENCE


def test_one_tutor_call_is_one_notice_with_both_briefs(world):
   notices.reset_notices()
   world.settings.tutor = ReplayProvider(cassette=CASSETTE)
   client = world.client()
   world.register(client)
   feedback_read(world, client)
   response = client.get("/notices")

   assert response.status_code == 200

   body = response.json()

   assert len(body["notices"]) == 1

   notice = body["notices"][0]

   assert notice["role"] == "tutor"
   assert notice["outcome"] == "answered"
   assert notice["replayed"] is True
   assert notice["asked"].startswith("Asked the tutor")
   assert notice["answered"] == SENTENCE
   assert body["latest"] == notice["id"]

   later = client.get("/notices", params={"after": body["latest"]})

   assert later.json() == {"notices": [], "latest": body["latest"]}


def test_a_student_never_sees_another_students_notices(world):
   """An installation takes one account, so the other student's call is made through a guard built
   for another user id, the way the route's own chain builds one for the signed-in user."""
   notices.reset_notices()
   world.settings.tutor = ReplayProvider(cassette=CASSETTE)
   client = world.client()
   world.register(client)
   feedback_read(world, client)
   own_id = client.get("/me").json()["id"]

   with OrmSession(world.engine) as db:
      other = GuardedProvider(
         ReplayProvider(cassette=dict(CASSETTE, text=OTHER_SENTENCE)),
         db,
         user_id=OTHER_USER_ID,
         caps={"tutor": BudgetCaps(cap_usd=1000.0)},
      )
      other.generate(tutor.request_for(OTHER_FIELDS))

   seen = client.get("/notices").json()["notices"]

   assert [notice["answered"] for notice in seen] == [SENTENCE]
   assert [notice["answered"] for notice in notices.notices_for(OTHER_USER_ID, 0)] == [OTHER_SENTENCE]
   assert all(notice["answered"] != SENTENCE for notice in notices.notices_for(OTHER_USER_ID, 0))
   assert own_id != OTHER_USER_ID


def test_notices_need_a_signed_in_student(world):
   response = world.client().get("/notices")

   assert response.status_code == 401


def test_a_negative_cursor_is_refused(world):
   client = world.client()
   world.register(client)

   assert client.get("/notices", params={"after": -1}).status_code == 422


def test_a_purge_drops_the_students_notices(world):
   notices.reset_notices()
   world.settings.tutor = ReplayProvider(cassette=CASSETTE)
   client = world.client()
   world.register(client)
   feedback_read(world, client)
   user_id = client.get("/me").json()["id"]

   assert len(notices.notices_for(user_id, 0)) == 1

   token = world.reauth(client).json()["reauth_token"]
   purged = client.post("/purge", json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token})

   assert purged.status_code == 200
   assert notices.notices_for(user_id, 0) == []
