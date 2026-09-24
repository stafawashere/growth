"""test_paper_to_grade, the P3 end-to-end gate: print, photograph a fixture page, correct one
transcription error, receive per-point grading with one provisional point.

The flow is tools/frq_scenarios.py paper_to_grade, run through app/main.py build_application. Every
model answer comes from tests/fixtures/grading_cassettes/paper_to_grade.json, recorded once on the
operator's Claude subscription by tools/record_grading_cassettes.py; a request that is not in the
book raises CassetteMiss, and a socket ban proves nothing dials out. The photograph is a rendered
stand-in for a real page (tests/fixtures/frq_pages/spec.json); no real handwriting exists yet.
"""
import json

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.providers.cassette_book import CassetteBookProvider
from tools import frq_scenarios


def test_paper_to_grade(tmp_path, forbid_network):
   book = CassetteBookProvider(path=frq_scenarios.PAPER_TO_GRADE_BOOK)
   application = frq_scenarios.build(tmp_path / "growth.db", book)
   client = frq_scenarios.client_for(application)
   frq_scenarios.register(client)

   steps = frq_scenarios.paper_to_grade(client)

   assert steps["booklet"].status_code == 200
   assert steps["booklet"].headers["content-type"] == "image/png"
   assert steps["uploaded"].json()["accepted"] is True

   read_back = steps["read_back"].json()

   assert read_back["transcription_confirmed"] is False
   assert [part["part_id"] for part in read_back["read_back"]["parts"]] == ["a", "b"]

   confirmed = steps["confirmed"].json()

   assert confirmed["transcription_confirmed"] is True
   assert confirmed["confirmed"]["parts"][1]["lines"] == frq_scenarios.PAPER_TO_GRADE_PART_B
   assert confirmed["confirmed"] != read_back["read_back"]

   gradings = steps["gradings"].json()
   points = {point["point_id"]: point for point in gradings["points"]}

   assert set(points) == {"a1", "a2", "b1", "b2"}
   assert points["a2"]["decided_by"] == "deterministic"
   assert gradings["provisional"] == 1
   assert gradings["decided"] == 3
   assert gradings["grading_state"] == "graded"

   provisional = [point for point in gradings["points"] if point["provisional"]]
   review_ids = [entry["grading_id"] for entry in steps["review"].json()["provisional_points"]]

   assert review_ids == [provisional[0]["grading_id"]]

   with OrmSession(application.state.engine) as db:
      attempt = db.get(models.Attempt, steps["attempt_id"])
      grader_prompts = [request for role, request in book.calls if role == "grader"]

      assert attempt.transcription_corrected == 1
      assert json.loads(attempt.transcription)["confirmed"] == steps["corrected"]
      assert db.scalars(select(models.Diagnosis).where(models.Diagnosis.attempt_id == attempt.id)).first() is not None

   assert book.calls[0][0] == "transcriber"
   assert len(grader_prompts) == 9
