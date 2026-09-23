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
         finish_reason="end_turn",
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


def attempt_with_sentinel_leak_check(world, client):
   """Seed every field the four selected ones are not with a distinctive sentinel string, so a
   template or a caller that widens what reaches the tutor is caught by an exact string check
   rather than by the mere absence of the word "only".
   """
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   item_id = item["id"]

   real_violated_step = "REAL-the true violated step for this leak check"
   real_observed_behavior = "REAL-the true observed behavior for this leak check"
   real_scoring_consequence = "REAL-the true scoring consequence for this leak check"
   real_worked_solution = "REAL-the true worked solution for this leak check"

   sentinel_step_0 = "SENTINEL-STEP-ZERO-4b12b6a9"
   sentinel_step_2 = "SENTINEL-STEP-TWO-7cd3e015"
   sentinel_step_3 = "SENTINEL-STEP-THREE-9ea1f420"
   sentinel_final_answer = "SENTINEL-FINAL-ANSWER-1f08c77e"
   sentinel_option_a_text = "SENTINEL-OPTION-A-TEXT-33aa9c02"
   sentinel_option_c_behavior = "SENTINEL-OPTION-C-BEHAVIOR-55bb1d40"
   sentinel_option_c_consequence = "SENTINEL-OPTION-C-CONSEQUENCE-55cc2e51"
   sentinel_option_d_behavior = "SENTINEL-OPTION-D-BEHAVIOR-77dd3f62"
   sentinel_option_d_consequence = "SENTINEL-OPTION-D-CONSEQUENCE-77ee4073"

   with OrmSession(world.engine) as db:
      stored = db.get(models.Item, item_id)
      archetype_id = stored.archetype_id
      stored.options = [
         {"id": "A", "is_key": True, "error_path": None, "distractor_text": sentinel_option_a_text},
         {"id": "B", "is_key": False, "error_path": "BC-ERR-SENTINEL-B", "violated_step": 1},
         {"id": "C", "is_key": False, "error_path": "BC-ERR-SENTINEL-C", "violated_step": 2},
         {"id": "D", "is_key": False, "error_path": "BC-ERR-SENTINEL-D", "violated_step": 3},
      ]
      stored.worked_solution = real_worked_solution
      stored.answer_key = json.dumps({"form": "symbolic", "mathjson": ["Symbol", sentinel_final_answer]})
      db.add(stored)
      db.commit()

   archetype = dict(world.settings.session_context.archetypes[archetype_id])
   path = list(archetype["expected_solution_path"])

   assert len(path) > 3

   path[0] = sentinel_step_0
   path[1] = real_violated_step
   path[2] = sentinel_step_2
   path[3] = sentinel_step_3
   archetype["expected_solution_path"] = path
   world.settings.session_context.archetypes[archetype_id] = archetype
   world.settings.session_context.errors = dict(
      world.settings.session_context.errors,
      **{
         "BC-ERR-SENTINEL-B": {
            "id": "BC-ERR-SENTINEL-B",
            "observed_behavior": real_observed_behavior,
            "scoring_consequence": real_scoring_consequence,
         },
         "BC-ERR-SENTINEL-C": {
            "id": "BC-ERR-SENTINEL-C",
            "observed_behavior": sentinel_option_c_behavior,
            "scoring_consequence": sentinel_option_c_consequence,
         },
         "BC-ERR-SENTINEL-D": {
            "id": "BC-ERR-SENTINEL-D",
            "observed_behavior": sentinel_option_d_behavior,
            "scoring_consequence": sentinel_option_d_consequence,
         },
      },
   )

   serve_as_mcq(world, session_id, item_id)
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item_id,
         "answer": {"option_id": "B"},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200

   selected_field_values = {
      "violated_step": real_violated_step,
      "observed_behavior": real_observed_behavior,
      "scoring_consequence": real_scoring_consequence,
      "worked_solution": real_worked_solution,
   }
   leaking_sentinels = {
      "the other option's error id": "BC-ERR-SENTINEL-C",
      "option A's own text": sentinel_option_a_text,
      "option C's observed behavior": sentinel_option_c_behavior,
      "option C's scoring consequence": sentinel_option_c_consequence,
      "option D's observed behavior": sentinel_option_d_behavior,
      "option D's scoring consequence": sentinel_option_d_consequence,
      "solution path step 0": sentinel_step_0,
      "solution path step 2": sentinel_step_2,
      "solution path step 3": sentinel_step_3,
      "the final answer": sentinel_final_answer,
   }

   return session_id, attempted.json()["id"], selected_field_values, leaking_sentinels


def test_the_tutor_receives_only_the_four_selected_fields(world):
   tutor = RecordingTutor()
   world.settings.tutor = tutor
   client = world.client()
   registered = world.register(client)
   student_id = registered.json()["user"]["id"]
   session_id, attempt_id, selected_field_values, leaking_sentinels = attempt_with_sentinel_leak_check(
      world, client
   )
   client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert len(tutor.requests) == 1

   request = tutor.requests[0]
   sent = "\n".join([request.system] + [message.content for message in request.messages])

   assert set(PROMPT_FIELDS) == {
      "violated_step",
      "observed_behavior",
      "scoring_consequence",
      "worked_solution",
   }

   for field_name, value in selected_field_values.items():
      assert value in sent, f"selected field {field_name} did not reach the tutor"

   for label, sentinel in leaking_sentinels.items():
      assert sentinel not in sent, f"{label} leaked into the tutor request"

   assert student_id not in sent
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
