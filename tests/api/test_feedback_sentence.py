"""R35: the four fields are selected deterministically and the sentence is written by the tutor.

docs/plan/03-diagnosis-and-feedback.md, "Who composes the string in P1 (R35)"; docs/plan/11
P1 scope items 10, 12 and 13. The provider is a recorder here, so no test opens a socket.
"""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.feedback.render import PROMPT_FIELDS
from app.providers.base import ProviderResult, Usage
from tests.api.conftest import TODAY
from tests.api.test_routes import open_session, serve_as_mcq

SENTENCE = "The quotient rule was not applied to the second factor, so the answer point is lost."


class RecordingTutor:
   def __init__(self):
      self.requests = []

   def generate(self, request):
      self.requests.append(request)

      return ProviderResult(
         text=SENTENCE,
         stop_reason="end_turn",
         usage=Usage(
            input_tokens=1200,
            output_tokens=40,
            cached_read_tokens=1024,
            cached_write_tokens=0,
            reasoning_tokens=None,
         ),
         provider="anthropic",
         model=request.model,
      )

   def stream(self, request):
      raise AssertionError("the feedback route does not stream in P1")


def attempt_one_distractor(world, client):
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   serve_as_mcq(world, session_id, item["id"])
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"option_id": "B"},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200

   return session_id, attempted.json()["id"]


def test_feedback_sentence_is_written_by_the_tutor(world):
   tutor = RecordingTutor()
   world.settings.tutor = tutor
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["kind"] == "elaborated"
   assert body["sentence"] == SENTENCE
   assert len(tutor.requests) == 1


def test_the_tutor_receives_only_the_four_selected_fields(world):
   tutor = RecordingTutor()
   world.settings.tutor = tutor
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")
   request = tutor.requests[0]
   sent = "\n".join(message.content for message in request.messages)

   assert set(PROMPT_FIELDS) == {
      "violated_step",
      "observed_behavior",
      "scoring_consequence",
      "worked_solution",
   }
   assert "answer_key" not in sent
   assert "{{" not in sent
   assert request.role == "tutor"
   assert request.model == "claude-sonnet-5"


def test_feedback_without_a_tutor_still_returns_the_selected_payload(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["kind"] == "elaborated"
   assert body["sentence"] is None
   assert body["elaborated"]["scoring_consequence"] == "the answer point is lost"


def test_the_stored_attempt_is_untouched_by_the_tutor(world):
   world.settings.tutor = RecordingTutor()
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempt_id)

      assert json.loads(stored.response)["option_id"] == "B"
      assert stored.correct == 0


class FailingTutor:
   def generate(self, request):
      raise RuntimeError("the provider is unreachable")

   def stream(self, request):
      raise AssertionError("the feedback route does not stream in P1")


def test_the_selected_payload_survives_a_provider_failure(world):
   """The selection is deterministic, so a provider outage costs the sentence and nothing else."""
   world.settings.tutor = FailingTutor()
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200
   assert feedback.json()["sentence"] is None
   assert feedback.json()["elaborated"]["scoring_consequence"] == "the answer point is lost"


def test_the_tutor_call_caches_its_static_prefix(world):
   """11 P1 scope 12 puts the one wired role behind a cached prefix with a 1 hour TTL."""
   tutor = RecordingTutor()
   world.settings.tutor = tutor
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")
   request = tutor.requests[0]

   assert request.cache is not None
   assert request.cache.ttl == "1h"
   assert request.cache.prefix_breakpoints == 1
