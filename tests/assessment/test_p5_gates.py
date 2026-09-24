"""The P5 gates of docs/plan/11: test_part_shapes, test_timed_does_not_update_mastery,
test_score_band_never_single_number, test_calculator_lockout, test_part_boundary_closed and
test_tool_set_present. test_full_mock_run is in tests/e2e."""
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.assessment import band
from app.db import models
from tests.assessment.conftest import (
   answer_multiple_choice,
   session_part,
   skills_state_rows,
   worked_read_back,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAM_STRUCTURE = REPO_ROOT / "research" / "exam" / "exam-structure.md"
ROW = re.compile(r"^\|\s*(I{1,2})\s*\|\s*([AB])\s*\|\s*[^|]+\|\s*(\d+)\s*\|\s*(\d+) minutes\s*\|\s*([^|]+?)\s*\|")

SIX_TOOLS = {"timer", "highlight_and_notes", "mark_for_review", "option_eliminator", "question_menu", "zoom"}
FORBIDDEN_RESULT_KEYS = {"score", "predicted_score", "predicted", "centre", "center", "band_centre", "band_center", "point_estimate"}


def documented_parts():
   """Read straight off the table in exam-structure.md, independently of app/checkpoint/published.py."""
   parts = {}

   for line in EXAM_STRUCTURE.read_text().splitlines():
      found = ROW.match(line)

      if found:
         section, part, questions, minutes, calculator = found.groups()
         parts[f"{section}-{part}"] = {"questions": int(questions), "minutes": int(minutes), "calculator": calculator == "Required"}

   assert len(parts) == 4, parts

   return parts


def test_part_shapes(assessment_app):
   application, client, user_id = assessment_app

   for key, documented in documented_parts().items():
      opened = client.post("/drills", json={"part": key})
      assert opened.status_code == 200, opened.text
      session_id = opened.json()["id"]
      started = client.post(f"/drills/{session_id}/sections/1/start").json()
      part = session_part(started, 1)
      started_at = datetime.fromisoformat(part["started_at"])
      deadline_at = datetime.fromisoformat(part["deadline_at"])

      assert part["key"] == key
      assert part["question_count"] == documented["questions"]
      assert len(part["questions"]) == documented["questions"]
      assert part["minutes"] == documented["minutes"]
      assert deadline_at - started_at == timedelta(minutes=documented["minutes"])
      assert part["calculator"] is documented["calculator"]


def test_timed_does_not_update_mastery(assessment_app):
   """Invariant 17 over the real routes: a multiple-choice drill with right and wrong answers and a
   free-response drill graded from typed work leave every skills_state column as it was, while
   the same answers in a unit check do move it, which proves the snapshot can see a change."""
   application, client, user_id = assessment_app
   before = skills_state_rows(application, user_id)

   drill = client.post("/drills", json={"part": "I-A"}).json()
   started = client.post(f"/drills/{drill['id']}/sections/1/start").json()
   answer_multiple_choice(application, client, "drills", drill["id"], 1, session_part(started, 1))
   assert client.post(f"/drills/{drill['id']}/sections/1/submit").status_code == 200

   frq_drill = client.post("/drills", json={"part": "II-B", "capture_mode": "typed"}).json()
   frq_started = client.post(f"/drills/{frq_drill['id']}/sections/1/start").json()
   capture = session_part(frq_started, 1)["capture"]
   assert client.post(f"/drills/{frq_drill['id']}/sections/1/submit").status_code == 200

   for question in capture:
      record = application.state.settings.frq.record(question["item_id"])
      typed = client.post(f"/attempts/{question['attempt_id']}/typed", json={"read_back": worked_read_back(record), "confidence": "confident"})
      assert typed.status_code == 200, typed.text

   with OrmSession(application.state.engine) as db:
      drill_attempts = db.scalars(select(models.Attempt).where(models.Attempt.session_id == drill["id"])).all()
      frq_points = db.scalars(select(models.Grading).where(models.Grading.attempt_id.in_([question["attempt_id"] for question in capture]))).all()

   assert {attempt.correct for attempt in drill_attempts} == {0, 1}
   assert any(point.earned == 1 and not point.provisional for point in frq_points)
   assert skills_state_rows(application, user_id) == before

   units = client.get("/unit-checks/units").json()["units"]
   unit_id = next(entry["unit_id"] for entry in units if entry["available"])
   check = client.post("/unit-checks", json={"unit_id": unit_id}).json()

   for question in session_part(check, 1)["questions"]:
      body = {"confidence": "confident"}

      if question["format"] == "mcq":
         body["answer"] = {"option_id": question["item"]["options"][0]["id"]}

      client.put(f"/unit-checks/{check['id']}/questions/{question['number']}", json=body)

   assert client.post(f"/unit-checks/{check['id']}/submit", json={}).status_code == 200
   assert skills_state_rows(application, user_id) != before


def keys_of(value):
   if isinstance(value, dict):
      found = set(value)

      for inner in value.values():
         found |= keys_of(inner)

      return found

   if isinstance(value, list):
      found = set()

      for inner in value:
         found |= keys_of(inner)

      return found

   return set()


def test_score_band_never_single_number(assessment_app):
   application, client, user_id = assessment_app
   mock = client.post("/mocks", json={"capture_mode": "typed"}).json()

   for position in (1, 2, 3, 4):
      started = client.post(f"/mocks/{mock['id']}/sections/{position}/start").json()
      part = session_part(started, position)

      if part["multiple_choice"]:
         answer_multiple_choice(application, client, "mocks", mock["id"], position, part)

      submitted = client.post(f"/mocks/{mock['id']}/sections/{position}/submit").json()

      for question in session_part(submitted, position).get("capture", []):
         record = application.state.settings.frq.record(question["item_id"])
         client.post(f"/attempts/{question['attempt_id']}/typed", json={"read_back": worked_read_back(record)})

   finished = client.post(f"/mocks/{mock['id']}/finish")
   assert finished.status_code == 200, finished.text
   result = finished.json()

   assert result["band"]["high"] - result["band"]["low"] >= 2
   assert 1 <= result["band"]["low"] < result["band"]["high"] <= 5
   assert len(result["assumptions"]) >= 5
   assert all(entry["text"] for entry in result["assumptions"])
   assert keys_of(result) & FORBIDDEN_RESULT_KEYS == set()
   assert keys_of(client.get("/mocks").json()) & FORBIDDEN_RESULT_KEYS == set()

   with OrmSession(application.state.engine) as db:
      stored = db.scalar(select(models.MockResult).where(models.MockResult.session_id == mock["id"]))
      assert stored.band_high - stored.band_low >= 2


def test_band_is_never_narrower_than_two_points_anywhere():
   for mcq_correct in range(0, 43, 3):
      for frq_points in range(0, 55, 6):
         for pending in (0, 5):
            placed = band.band_for(mcq_correct, 42, frq_points, min(pending, 54 - frq_points), 54)

            assert placed["high"] - placed["low"] >= 2
            assert 1 <= placed["low"] and placed["high"] <= 5


def test_calculator_lockout(assessment_app):
   application, client, user_id = assessment_app
   mock = client.post("/mocks", json={"capture_mode": "typed"}).json()

   for part in mock["parts"]:
      has_panel = "graphing_panel" in part["tools"]

      assert has_panel is part["calculator"]

      if not part["calculator"]:
         assert part["calculator_label"] == "NO CALCULATOR ALLOWED"
         assert part["calculator_note"]

   calculator_keys = [part["key"] for part in mock["parts"] if part["calculator"]]
   documented = documented_parts()

   assert calculator_keys == [key for key, shape in documented.items() if shape["calculator"]]


def test_part_boundary_closed(assessment_app):
   application, client, user_id = assessment_app
   mock = client.post("/mocks", json={"capture_mode": "typed"}).json()
   mock_id = mock["id"]

   early = client.post(f"/mocks/{mock_id}/sections/2/start")
   assert early.status_code == 409

   started = client.post(f"/mocks/{mock_id}/sections/1/start").json()
   first = session_part(started, 1)["questions"][0]
   assert client.post(f"/mocks/{mock_id}/sections/1/submit").status_code == 200

   reopened = client.post(f"/mocks/{mock_id}/sections/1/start")
   late_save = client.put(f"/mocks/{mock_id}/sections/1/questions/{first['number']}", json={"answer": {"option_id": "A"}})
   resubmitted = client.post(f"/mocks/{mock_id}/sections/1/submit")

   assert reopened.status_code == 409
   assert late_save.status_code == 409
   assert resubmitted.status_code == 409
   assert session_part(client.get(f"/mocks/{mock_id}").json(), 1)["questions"] == []

   drill = client.post("/drills", json={"part": "I-B"}).json()
   drill_part = session_part(client.post(f"/drills/{drill['id']}/sections/1/start").json(), 1)
   question = drill_part["questions"][0]
   option_id = question["item"]["options"][0]["id"]
   assert client.put(f"/drills/{drill['id']}/sections/1/questions/{question['number']}", json={"answer": {"option_id": option_id}}).status_code == 200

   with OrmSession(application.state.engine) as db:
      part_row = db.scalar(select(models.AssessmentPart).where(models.AssessmentPart.session_id == drill["id"]))
      part_row.deadline_at = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
      db.commit()

   after_time = client.put(f"/drills/{drill['id']}/sections/1/questions/{question['number']}", json={"answer": {"option_id": option_id}})
   closed = session_part(client.get(f"/drills/{drill['id']}").json(), 1)

   assert after_time.status_code == 409
   assert closed["status"] == "closed"
   assert closed["closed_by"] == "time"

   with OrmSession(application.state.engine) as db:
      graded = db.scalars(select(models.Attempt).where(models.Attempt.session_id == drill["id"])).all()

   assert [attempt.item_id for attempt in graded] == [question["item"]["id"]]


def test_tool_set_present(assessment_app):
   application, client, user_id = assessment_app
   mock = client.post("/mocks", json={"capture_mode": "typed"}).json()

   for part in mock["parts"]:
      tools = set(part["tools"])
      expected = set(SIX_TOOLS)

      if not part["multiple_choice"]:
         expected.discard("option_eliminator")

      if part["calculator"]:
         expected.add("graphing_panel")

      assert tools == expected, part["key"]
      assert part["five_minute_alert_seconds"] == 300

   started = client.post(f"/mocks/{mock['id']}/sections/1/start").json()
   question = session_part(started, 1)["questions"][0]
   options = [option["id"] for option in question["item"]["options"]]
   saved = client.put(
      f"/mocks/{mock['id']}/sections/1/questions/{question['number']}",
      json={"marked": True, "eliminated": options[:2], "notes": "check the sign", "highlights": [{"start": 0, "end": 4}], "visit_ms": 1000},
   )
   assert saved.status_code == 200

   reread = session_part(client.get(f"/mocks/{mock['id']}").json(), 1)["questions"][0]

   assert reread["marked"] is True
   assert reread["eliminated"] == sorted(options[:2])
   assert reread["notes"] == "check the sign"
   assert reread["highlights"] == [{"start": 0, "end": 4}]


def test_an_unfinished_assessment_can_be_found_again_and_a_closed_part_still_names_its_questions(assessment_app):
   application, client, user_id = assessment_app
   drill = client.post("/drills", json={"part": "II-A", "capture_mode": "typed"}).json()
   client.post(f"/drills/{drill['id']}/sections/1/start")

   listed = client.get("/assessments/unfinished").json()["unfinished"]

   assert [entry["id"] for entry in listed] == [drill["id"]]

   closed = session_part(client.post(f"/drills/{drill['id']}/sections/1/submit").json(), 1)

   assert all(capture["item"]["parts"] for capture in closed["capture"])
   assert [entry["id"] for entry in client.get("/assessments/unfinished").json()["unfinished"]] == [drill["id"]]

   for capture in closed["capture"]:
      record = application.state.settings.frq.record(capture["item_id"])
      client.post(f"/attempts/{capture['attempt_id']}/typed", json={"read_back": worked_read_back(record)})

   assert client.get("/assessments/unfinished").json()["unfinished"] == []


def test_an_open_mock_is_not_offered_as_todays_set_in_progress(assessment_app):
   application, client, user_id = assessment_app
   mock = client.post("/mocks", json={"capture_mode": "typed"}).json()
   client.post(f"/mocks/{mock['id']}/sections/1/start")

   home = client.get("/progress").json()

   assert home["session_in_progress"] is None
