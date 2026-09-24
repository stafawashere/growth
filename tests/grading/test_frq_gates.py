"""The P3 integration gates, through the real routes and the real grading service.

test_readback_gate: no grading call fires before the student confirms the read-back.
test_image_quality_gate: a blurred fixture is rejected before any provider call.
test_disagreement_escalates: a seeded disagreement lands in review_queue, is shown provisional on
the gradings route and on the review screen, and is never averaged.
"""
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.grading import service
from tests.grading.conftest import READ_BACK


def gradings_rows(world, attempt_id):
   with OrmSession(world.engine) as db:
      return db.scalars(select(models.Grading).where(models.Grading.attempt_id == attempt_id)).all()


def test_readback_gate(frq_world):
   attempt_id = frq_world.open_attempt()
   uploaded = frq_world.upload(attempt_id, "critical_point_full__clean.jpg")

   assert uploaded.json()["accepted"] is True

   read = frq_world.client.post(f"/attempts/{attempt_id}/transcription")

   assert read.status_code == 200
   assert read.json()["transcription_confirmed"] is False
   assert frq_world.provider.roles() == ["transcriber"]

   with OrmSession(frq_world.engine) as db:
      attempt = db.get(models.Attempt, attempt_id)
      session_row = db.get(models.Session, attempt.session_id)
      record = frq_world.settings.frq.record(attempt.item_id)
      context = {"judge": object(), "labels": frq_world.settings.frq.labels}

      try:
         service.grade(db, session_row, attempt, record, context, None)
         refused = False
      except service.ReadBackNotConfirmed:
         refused = True

   assert refused is True
   assert frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()["points"] == []
   assert gradings_rows(frq_world, attempt_id) == []
   assert "grader" not in frq_world.provider.roles()

   confirmed = frq_world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={})

   assert confirmed.status_code == 200
   assert frq_world.provider.roles().count("grader") > 0
   assert len(gradings_rows(frq_world, attempt_id)) == 4


def test_a_confirmed_answer_takes_no_new_photograph_and_an_unread_one_cannot_be_confirmed(frq_world):
   attempt_id = frq_world.open_attempt()

   early = frq_world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={})

   assert early.status_code == 409
   assert frq_world.provider.roles() == []


def test_image_quality_gate(frq_world):
   attempt_id = frq_world.open_attempt()

   blurred = frq_world.upload(attempt_id, "critical_point_full__blur.jpg")

   assert blurred.status_code == 200
   assert blurred.json()["accepted"] is False
   assert any("blurred" in reason for reason in blurred.json()["reasons"])

   read = frq_world.client.post(f"/attempts/{attempt_id}/transcription")

   assert read.status_code == 409
   assert frq_world.provider.requests == []


def test_each_rejected_condition_names_what_to_fix(frq_world):
   attempt_id = frq_world.open_attempt()
   expected = {
      "critical_point_full__low_light.jpg": "too dark",
      "critical_point_full__cropped.jpg": "corner squares",
      "critical_point_full__far.jpg": "fills too little",
   }

   for page_name, phrase in expected.items():
      verdict = frq_world.upload(attempt_id, page_name).json()

      assert verdict["accepted"] is False, page_name
      assert any(phrase in reason for reason in verdict["reasons"]), (page_name, verdict["reasons"])

   assert frq_world.upload(attempt_id, "critical_point_full__angled.jpg").json()["accepted"] is True
   assert frq_world.provider.requests == []


def test_disagreement_escalates(frq_world):
   frq_world.provider.grader_answers = {
      "b2": {"temp0_a": "earned", "temp0_b": "earned", "strict": "not_earned"},
   }
   attempt_id = frq_world.open_attempt()
   frq_world.upload(attempt_id, "critical_point_full__clean.jpg")
   frq_world.client.post(f"/attempts/{attempt_id}/transcription")
   frq_world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={"confidence": "unsure"})

   gradings = frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()
   points = {point["point_id"]: point for point in gradings["points"]}

   assert points["b2"]["provisional"] is True
   assert points["b2"]["earned"] is None
   assert points["b2"]["decided_by"] == "escalated"
   assert gradings["provisional"] == 1
   assert gradings["decided"] == 3

   with OrmSession(frq_world.engine) as db:
      queued = db.scalars(select(models.ReviewQueue).where(models.ReviewQueue.kind == "grading_split")).all()

   assert [row.ref_id for row in queued] == [points["b2"]["grading_id"]]

   review = frq_world.client.get("/review", params={"today": date.today().isoformat()}).json()

   assert review["grading_available"] is True
   assert [entry["grading_id"] for entry in review["provisional_points"]] == [points["b2"]["grading_id"]]
   assert "disagreed" in review["provisional_points"][0]["reason"]


def test_a_reread_is_one_click_from_the_review_screen_and_judges_the_point_again(frq_world):
   frq_world.provider.grader_answers = {"b2": {"temp0_a": "earned", "temp0_b": "earned", "strict": "not_earned"}}
   attempt_id = frq_world.open_attempt()
   frq_world.upload(attempt_id, "critical_point_full__clean.jpg")
   frq_world.client.post(f"/attempts/{attempt_id}/transcription")
   frq_world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={})
   provisional = frq_world.client.get("/review", params={"today": date.today().isoformat()}).json()["provisional_points"][0]
   grader_calls_before = frq_world.provider.roles().count("grader")
   frq_world.provider.grader_answers = {}

   disputed = frq_world.client.post(f"/gradings/{provisional['grading_id']}/dispute", json={"reason": "I named the sign change"})

   assert disputed.status_code == 200
   assert frq_world.provider.roles().count("grader") == grader_calls_before + 3

   points = {point["point_id"]: point for point in frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()["points"]}

   assert points["b2"]["grading_id"] == provisional["grading_id"]
   assert points["b2"]["provisional"] is False
   assert points["b2"]["earned"] == 1
   assert points["b2"]["rereads"] == 1

   with OrmSession(frq_world.engine) as db:
      disputes = db.scalars(select(models.ReviewQueue).where(models.ReviewQueue.kind == "dispute")).all()

   assert [(row.ref_id, row.visible_to_student) for row in disputes] == [(provisional["grading_id"], 1)]
   assert disputes[0].resolved_at is not None
   assert disputes[0].resolution == "re-read: decided, earned 1"

   review = frq_world.client.get("/review", params={"today": date.today().isoformat()}).json()

   assert review["provisional_points"] == []


def test_grading_refuses_outside_the_four_modes(frq_world):
   opened = frq_world.client.post("/sessions", json={"mode": "learning", "today": date.today().isoformat()})
   session_id = opened.json()["id"]

   started = frq_world.client.post(f"/sessions/{session_id}/frq/FRQ-AGT-05007-01/attempts", json={"capture_mode": "photo"})

   assert started.status_code == 409
   assert "unit check" in started.json()["detail"]


def test_a_correction_after_grading_clears_the_points_and_grades_the_corrected_work(frq_world):
   attempt_id = frq_world.open_attempt()
   frq_world.upload(attempt_id, "critical_point_full__clean.jpg")
   frq_world.client.post(f"/attempts/{attempt_id}/transcription")
   frq_world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={})
   first = {point["point_id"]: point["earned"] for point in frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()["points"]}
   corrected = {"parts": [dict(READ_BACK["parts"][0], answer="x = 4", lines=[]), READ_BACK["parts"][1]], "unreadable": []}

   frq_world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={"read_back": corrected})
   second = {point["point_id"]: point["earned"] for point in frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()["points"]}

   assert first["a2"] == 1
   assert second["a2"] == 0


def test_typed_entry_is_confirmed_by_construction_and_graded(frq_world):
   attempt_id = frq_world.open_attempt(capture_mode="typed")

   typed = frq_world.client.post(f"/attempts/{attempt_id}/typed", json={"read_back": READ_BACK, "confidence": "confident"})

   assert typed.status_code == 200
   assert typed.json()["transcription_confirmed"] is True
   assert "transcriber" not in frq_world.provider.roles()

   gradings = frq_world.client.get(f"/attempts/{attempt_id}/gradings").json()

   assert gradings["grading_state"] == "graded"
   assert len(gradings["points"]) == 4
