"""The P5 evals of docs/plan/11: eval_mock_against_published_means and eval_pacing_metrics, run on
two mocks and a drill driven through the real routes. The operator's own numbers come from
tools/p5_evals.py over var/growth.db once real mocks exist."""
from sqlalchemy.orm import Session as OrmSession

from app.assessment import evals, shape
from app.checkpoint import published
from tests.assessment.conftest import answer_multiple_choice, assessment_app, session_part, worked_read_back


def run_mock(application, client, visit_ms):
   mock = client.post("/mocks", json={"capture_mode": "typed"}).json()

   for position in range(1, len(shape.part_keys()) + 1):
      part = session_part(client.post(f"/mocks/{mock['id']}/sections/{position}/start").json(), position)

      if part["multiple_choice"]:
         answer_multiple_choice(application, client, "mocks", mock["id"], position, part, visit_ms=visit_ms)

      submitted = client.post(f"/mocks/{mock['id']}/sections/{position}/submit").json()

      for capture in session_part(submitted, position).get("capture", []):
         record = application.state.settings.frq.record(capture["item_id"])
         client.post(f"/attempts/{capture['attempt_id']}/typed", json={"read_back": worked_read_back(record)})

   assert client.post(f"/mocks/{mock['id']}/finish").status_code == 200

   return mock["id"]


def eval_mock_against_published_means(assessment_app):
   application, client, user_id = assessment_app

   with OrmSession(application.state.engine) as db:
      empty = evals.mock_against_published_means(db, user_id, application.state.settings.frq)

   assert empty["available"] is False

   run_mock(application, client, visit_ms=60000)
   run_mock(application, client, visit_ms=90000)

   with OrmSession(application.state.engine) as db:
      compared = evals.mock_against_published_means(db, user_id, application.state.settings.frq)

   means = published.question_means()

   assert compared["mocks"] == 2
   assert [row["question"] for row in compared["questions"]] == list(range(1, shape.free_response_total() + 1))

   for row in compared["questions"]:
      assert row["mocks"] == 2
      assert 0 <= row["mean_earned"] <= row["possible"] == published.points_per_free_response_question()
      assert row["published"] == {year: means[(year, row["question"])].mean for year in (2023, 2024, 2025)}


def eval_pacing_metrics(assessment_app):
   application, client, user_id = assessment_app
   run_mock(application, client, visit_ms=60000)
   drill = client.post("/drills", json={"part": "I-B"}).json()
   part = session_part(client.post(f"/drills/{drill['id']}/sections/1/start").json(), 1)
   answer_multiple_choice(application, client, "drills", drill["id"], 1, part, visit_ms=120000)
   client.post(f"/drills/{drill['id']}/sections/1/submit")

   with OrmSession(application.state.engine) as db:
      pacing = evals.pacing_against_budgets(db, user_id)

   rows = {row["part_key"]: row for row in pacing["parts"]}

   assert rows["I-A"]["parts"] == 1
   assert rows["I-B"]["parts"] == 2
   assert rows["I-B"]["mean_seconds_per_question"] == 90.0
   assert rows["I-A"]["mean_seconds_per_question"] == 60.0

   for part_shape in shape.part_shapes():
      row = rows[part_shape.key]

      assert row["budget_seconds_per_question"] == part_shape.minutes * 60 / part_shape.questions
      assert row["submitted_before_time"]["denominator"] == row["parts"]
