"""11 P5 scope items 1, 6 and 8: the unit check's cover and its withheld feedback, the rapid-guess
flag and its exclusion from diagnosis, and the radian-mode note on calculator work."""
import json
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.assessment import assemble, unit_check
from app.db import models
from app.engine.fringe import parents_mastered
from app.engine.prior import primary_skill
from app.session import repository
from tests.assessment.conftest import key_option_id, session_part


def test_unit_check_covers_the_unit_and_withholds_feedback(assessment_app):
   application, client, user_id = assessment_app
   context = application.state.settings.session_context
   units = client.get("/unit-checks/units").json()["units"]
   unit_id = next(entry["unit_id"] for entry in units if entry["available"] and entry["items"] >= unit_check.MIN_ITEMS)
   opened = client.post("/unit-checks", json={"unit_id": unit_id})
   assert opened.status_code == 200, opened.text
   check = opened.json()
   questions = session_part(check, 1)["questions"]

   assert unit_check.MIN_ITEMS <= len(questions) <= unit_check.MAX_ITEMS
   assert check["updates_mastery"] is True
   assert all(part["timed"] is False for part in check["parts"])

   with OrmSession(application.state.engine) as db:
      states = repository.load_states(db, user_id)
      session_row = db.get(models.Session, check["id"])
      coverage = json.loads(session_row.queue)["coverage"]

   archetype_ids = {question["item"]["archetype_id"] for question in questions}

   for archetype_id in archetype_ids:
      record = context.archetypes[archetype_id]

      assert record["primary_unit"] == unit_id
      assert parents_mastered(primary_skill(record), states, context.graph)

   loaded = {skill for archetype_id in archetype_ids for skill in context.archetypes[archetype_id]["skills"]}

   assert set(coverage["covered"]) <= loaded
   assert set(coverage["covered"]).isdisjoint(coverage["unreached"])

   first = questions[0]
   saved = client.put(
      f"/unit-checks/{check['id']}/questions/{first['number']}",
      json={"answer": {"option_id": key_option_id(application, first["item"]["id"])}, "confidence": "confident"},
   )

   assert saved.json() == {"number": first["number"], "saved": True}

   with OrmSession(application.state.engine) as db:
      attempts_before_submit = db.scalars(select(models.Attempt).where(models.Attempt.session_id == check["id"])).all()

   assert attempts_before_submit == []

   submitted = client.post(f"/unit-checks/{check['id']}/submit", json={})
   breakdown = submitted.json()

   assert submitted.status_code == 200
   assert breakdown["items"][0]["correct"] is True
   assert breakdown["items"][0]["key_option_id"] == key_option_id(application, first["item"]["id"])
   assert any(entry["skill_id"] in context.archetypes[first["item"]["archetype_id"]]["skills"] for entry in breakdown["moved"])
   assert client.post(f"/unit-checks/{check['id']}/submit", json={}).status_code == 409


def test_every_unit_check_holds_eight_to_twelve_items_when_the_unit_can_supply_them(assessment_app):
   application, client, user_id = assessment_app
   context = application.state.settings.session_context
   snapshot = context.snapshot or application.state.settings.resolve_snapshot()

   with OrmSession(application.state.engine) as db:
      states = repository.load_states(db, user_id)
      published = unit_check.published_by_archetype(db)

   units = sorted({record["primary_unit"] for record in context.graph.archetypes.values()})

   for unit_id in units:
      servable = [
         record
         for record in context.graph.archetypes.values()
         if record["primary_unit"] == unit_id and record["id"] in published and parents_mastered(primary_skill(record), states, context.graph)
      ]
      chosen, covered, unreached = unit_check.plan_check(snapshot, context.graph, states, unit_id, published)
      expected_floor = min(unit_check.MIN_ITEMS, len(servable))

      assert expected_floor <= len(chosen) <= unit_check.MAX_ITEMS, unit_id


def test_a_fast_answer_in_the_final_minutes_is_flagged_and_left_out_of_diagnosis(assessment_app):
   application, client, user_id = assessment_app
   drill = client.post("/drills", json={"part": "I-A"}).json()
   part = session_part(client.post(f"/drills/{drill['id']}/sections/1/start").json(), 1)
   early, late = part["questions"][0], part["questions"][1]
   wrong = {
      question["number"]: next(option["id"] for option in question["item"]["options"] if option["id"] != key_option_id(application, question["item"]["id"]))
      for question in (early, late)
   }
   client.put(f"/drills/{drill['id']}/sections/1/questions/{early['number']}", json={"answer": {"option_id": wrong[early["number"]]}, "visit_ms": 1000})

   with OrmSession(application.state.engine) as db:
      part_row = db.scalar(select(models.AssessmentPart).where(models.AssessmentPart.session_id == drill["id"]))
      part_row.deadline_at = (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()
      early_row = db.scalar(select(models.AssessmentResponse).where(models.AssessmentResponse.part_id == part_row.id, models.AssessmentResponse.number == early["number"]))
      early_row.first_answered_at = (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat()
      db.commit()

   client.put(f"/drills/{drill['id']}/sections/1/questions/{late['number']}", json={"answer": {"option_id": wrong[late["number"]]}, "visit_ms": 1000})
   result = client.post(f"/drills/{drill['id']}/sections/1/submit")
   assert result.status_code == 200

   with OrmSession(application.state.engine) as db:
      responses = {row.number: row for row in db.scalars(select(models.AssessmentResponse).where(models.AssessmentResponse.session_id == drill["id"])).all()}
      diagnosed = {
         row.attempt_id
         for row in db.scalars(select(models.Diagnosis)).all()
      }

   assert responses[late["number"]].rapid_guess == 1
   assert responses[early["number"]].rapid_guess == 0
   assert responses[early["number"]].attempt_id in diagnosed
   assert responses[late["number"]].attempt_id not in diagnosed

   pacing = client.get(f"/drills/{drill['id']}/result").json()["pacing"][0]

   assert pacing["rapid_guess"] == {"numerator": 1, "denominator": len(part["questions"]), "value": 1 / len(part["questions"])}
   assert pacing["mean_counts"]["numerator"] == 1


def test_the_radian_note_rides_on_calculator_trigonometry_only():
   trig_stem = "Let \\( W(t) = 2\\sin\\left(t^{2}\\right) \\). Find the average value."
   plain_stem = "Let \\( W(t) = e^{t} - t^{2} \\). Find the average value."

   assert assemble.radian_note_applies(trig_stem, calculator_part=True) is True
   assert assemble.radian_note_applies(trig_stem, calculator_part=False) is False
   assert assemble.radian_note_applies(plain_stem, calculator_part=True) is False


def test_a_wrong_timed_answer_comes_back_through_the_corrected_item_requeue(assessment_app):
   """05: timed work reaches D3 through corrected items only, at the usual short gap."""
   from app.session.build import requeue_pending

   application, client, user_id = assessment_app
   drill = client.post("/drills", json={"part": "I-B"}).json()
   part = session_part(client.post(f"/drills/{drill['id']}/sections/1/start").json(), 1)
   wrong_question = part["questions"][0]
   right_question = part["questions"][1]
   wrong_option = next(option["id"] for option in wrong_question["item"]["options"] if option["id"] != key_option_id(application, wrong_question["item"]["id"]))
   client.put(f"/drills/{drill['id']}/sections/1/questions/{wrong_question['number']}", json={"answer": {"option_id": wrong_option}, "visit_ms": 60000})
   client.put(f"/drills/{drill['id']}/sections/1/questions/{right_question['number']}", json={"answer": {"option_id": key_option_id(application, right_question["item"]["id"])}, "visit_ms": 60000})
   client.post(f"/drills/{drill['id']}/sections/1/submit")

   with OrmSession(application.state.engine) as db:
      pending = requeue_pending(repository.load_attempts_history(db, user_id), datetime.now(timezone.utc).date())

   requeued = {correction.item_id for correction in pending}

   assert wrong_question["item"]["id"] in requeued
   assert right_question["item"]["id"] not in requeued


def test_a_revisit_is_a_visit_that_began_after_the_question_was_answered(assessment_app):
   application, client, user_id = assessment_app
   drill = client.post("/drills", json={"part": "I-B"}).json()
   part = session_part(client.post(f"/drills/{drill['id']}/sections/1/start").json(), 1)
   first, second = part["questions"][0], part["questions"][1]
   base = f"/drills/{drill['id']}/sections/1/questions"
   option = first["item"]["options"][0]["id"]

   client.put(f"{base}/{first['number']}", json={"answer": {"option_id": option}})
   client.put(f"{base}/{first['number']}", json={"visit_ms": 60000})
   client.put(f"{base}/{second['number']}", json={"answer": {"option_id": second["item"]["options"][0]["id"]}})

   with OrmSession(application.state.engine) as db:
      row = db.scalar(select(models.AssessmentResponse).where(models.AssessmentResponse.session_id == drill["id"], models.AssessmentResponse.number == second["number"]))
      row.first_answered_at = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
      db.commit()

   client.put(f"{base}/{second['number']}", json={"visit_ms": 30000})
   client.post(f"/drills/{drill['id']}/sections/1/submit")
   pacing = client.get(f"/drills/{drill['id']}/result").json()["pacing"][0]
   revisited = {entry["number"]: entry["revisited"] for entry in pacing["per_question"]}

   assert revisited[first["number"]] is False
   assert revisited[second["number"]] is True
