"""test_full_mock_run, the P5 end-to-end gate of docs/plan/11: a complete mock at the documented
shape, the multiple choice answered in the app, every free-response question captured from its
booklet page (photographed, read back, confirmed) and graded, pacing recorded per part, the band
produced, and no skills_state row changed.

The application is app/main.py's, over a temporary database. The transcriber is a scripted
provider that reads a page as the question's own worked solution, standing in for the recorded
cassettes P3 uses, because these questions have no recordings yet; every other model role raises,
so the judged points stay provisional, which is the path a grader outage takes. The photograph is
the P3 rendered fixture page. The socket ban proves nothing dials out.
"""
import json

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.assessment import shape
from app.checkpoint import published
from app.db import models
from app.providers.base import Provider, ProviderResult, Usage
from tests.assessment.conftest import (
   answer_multiple_choice,
   publish_generated_items,
   session_part,
   skills_state_rows,
   worked_read_back,
)
from tools import frq_scenarios


class ScriptedTranscriber(Provider):
   def __init__(self, records):
      self.records = records
      self.calls = []

   def generate(self, request):
      self.calls.append(request.role)
      is_transcription = request.role == "transcriber"

      if not is_transcription:
         raise RuntimeError(f"no scripted answer for the {request.role} role")

      prompt = request.messages[0].content
      record = next(record for item_id, record in self.records.items() if item_id in prompt)
      text = json.dumps(worked_read_back(record))

      return ProviderResult(text=text, finish_reason="end_turn", usage=Usage(input_tokens=1, output_tokens=1, cached_read_tokens=0, cached_write_tokens=0), provider="scripted", model=request.model)

   def stream(self, request):
      raise NotImplementedError


def test_full_mock_run(tmp_path, forbid_network):
   application = frq_scenarios.build(tmp_path / "growth.db", None)
   provider = ScriptedTranscriber(application.state.settings.frq.records)
   application.state.settings.ai_provider = provider
   publish_generated_items(application)
   client = frq_scenarios.client_for(application)
   user_id = frq_scenarios.register(client)
   before = skills_state_rows(application, user_id)

   mock = client.post("/mocks", json={"capture_mode": "photo"})
   assert mock.status_code == 200, mock.text
   mock_id = mock.json()["id"]
   served_numbers = []

   for position, part_shape in enumerate(shape.part_shapes(), start=1):
      started = client.post(f"/mocks/{mock_id}/sections/{position}/start")
      assert started.status_code == 200, started.text
      part = session_part(started.json(), position)

      assert len(part["questions"]) == part_shape.questions
      served_numbers.extend(question["number"] for question in part["questions"])

      if part["multiple_choice"]:
         answer_multiple_choice(application, client, "mocks", mock_id, position, part, correct_every=3)
      else:
         for question in part["questions"]:
            client.put(f"/mocks/{mock_id}/sections/{position}/questions/{question['number']}", json={"visit_ms": 600000})

         for capture in part["capture"]:
            booklet = client.get(f"/attempts/{capture['attempt_id']}/booklet.png")
            assert booklet.status_code == 200
            assert booklet.headers["content-type"] == "image/png"

      submitted = client.post(f"/mocks/{mock_id}/sections/{position}/submit")
      assert submitted.status_code == 200, submitted.text

      for capture in session_part(submitted.json(), position).get("capture", []):
         attempt_id = capture["attempt_id"]
         uploaded = client.post(f"/attempts/{attempt_id}/images", json=frq_scenarios.photo_payload(frq_scenarios.PAPER_TO_GRADE_PAGE))
         assert uploaded.json()["accepted"] is True

         read_back = client.post(f"/attempts/{attempt_id}/transcription")
         assert read_back.status_code == 200, read_back.text
         assert read_back.json()["transcription_confirmed"] is False

         confirmed = client.post(f"/attempts/{attempt_id}/transcription/confirm", json={"read_back": read_back.json()["read_back"]})
         assert confirmed.status_code == 200, confirmed.text

         gradings = client.get(f"/attempts/{attempt_id}/gradings").json()
         assert gradings["total"] == published.points_per_free_response_question()
         assert gradings["decided"] + gradings["provisional"] == len(gradings["points"])

   assert served_numbers == list(range(1, shape.multiple_choice_total() + 1)) + list(range(1, shape.free_response_total() + 1))

   finished = client.post(f"/mocks/{mock_id}/finish")
   assert finished.status_code == 200, finished.text
   result = finished.json()

   assert [row["part_key"] for row in result["pacing"]] == list(shape.part_keys())
   assert all(len(row["per_question"]) == row["questions"] for row in result["pacing"])
   assert all(row["answered"]["numerator"] == row["questions"] for row in result["pacing"])
   assert result["multiple_choice"]["total"] == shape.multiple_choice_total()
   assert result["free_response"]["total"] == shape.free_response_total() * published.points_per_free_response_question()
   assert result["free_response"]["earned"] > 0
   assert result["band"]["high"] - result["band"]["low"] >= 2
   assert [row["question"] for row in result["questions"]] == list(range(1, shape.free_response_total() + 1))
   assert provider.calls.count("transcriber") == shape.free_response_total()
   assert skills_state_rows(application, user_id) == before

   with OrmSession(application.state.engine) as db:
      images = db.scalars(select(models.FrqImage).where(models.FrqImage.accepted == 1)).all()
      mock_attempts = db.scalars(select(models.Attempt).where(models.Attempt.session_id == mock_id)).all()

   assert len(images) == shape.free_response_total()
   assert len(mock_attempts) == shape.multiple_choice_total() + shape.free_response_total()
