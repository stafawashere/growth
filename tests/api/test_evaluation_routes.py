"""The P7 harness over HTTP: the metrics view, the A/B switches, the checkpoint and the probe
(11 P7 test_metrics_view_renders and test_checkpoint_isolated)."""
import json
from datetime import timedelta

from sqlalchemy.orm import Session as OrmSession

from app.checkpoint import forms
from app.checkpoint import service as checkpoint_service
from app.db import models
from app.experiments import switches
from app.runtime.probe_set import probe_item_ids
from tests.api.conftest import TODAY, WRONG_MATHJSON, item_row
from tests.api.test_routes import correct_answer_for, open_session, serve_as_mcq

CHECKPOINT_DAY = TODAY + timedelta(days=1)


def answer(client, session_id, item, body, confidence="unsure"):
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": body,
         "elapsed_ms": 75000,
         "today": TODAY.isoformat(),
         "confidence": confidence,
      },
   )

   assert attempted.status_code == 200

   return attempted.json()


def practise(client, count):
   session_id = open_session(client).json()["id"]

   for index in range(count):
      served = client.get(f"/sessions/{session_id}/next").json()["item"]

      if served is None:
         break

      is_even = index % 2 == 0
      body = correct_answer_for(served) if is_even else {"mathjson": WRONG_MATHJSON, "option_id": "B"}
      answer(client, session_id, served, body, confidence="confident" if is_even else "unsure")

   assert client.post(f"/sessions/{session_id}/close", json={}).status_code == 200

   return session_id


def run_checkpoint(client, day):
   started = client.post("/checkpoints", json={"today": day.isoformat()})

   assert started.status_code == 200

   checkpoint = started.json()

   for section in checkpoint["sections"]:
      for question in section["questions"]:
         for part in question["parts"]:
            scored = client.post(
               f"/checkpoints/{checkpoint['id']}/scores",
               json={"record_id": part["record_id"], "points_earned": part["points"] // 2, "today": day.isoformat()},
            )

            assert scored.status_code == 200

   finished = client.post(f"/checkpoints/{checkpoint['id']}/finish", json={"today": day.isoformat()})

   assert finished.status_code == 200

   return finished.json()


def test_metrics_view_renders(world):
   client = world.client()
   world.register(client)
   practise(client, 8)
   run_checkpoint(client, CHECKPOINT_DAY)

   response = client.get("/progress/metrics", params={"today": CHECKPOINT_DAY.isoformat()})

   assert response.status_code == 200

   metrics = {metric["key"]: metric for metric in response.json()["metrics"]}

   assert set(metrics) == {
      "mastery_growth",
      "retention_7_30",
      "mock_trajectory",
      "calibration",
      "method_selection",
      "error_recurrence",
      "adherence_effort",
      "free_response_participation",
      "external_checkpoint",
      "concept_probe",
   }

   for metric in metrics.values():
      assert len(metric["values"]) > 0

      for entry in metric["values"]:
         assert isinstance(entry["denominator"], (int, float))
         assert entry["denominator_label"].strip() != ""
         has_no_denominator = entry["denominator"] == 0

         if has_no_denominator:
            assert entry["value"] is None

   for key in ("calibration", "adherence_effort", "external_checkpoint", "error_recurrence"):
      assert metrics[key]["status"] == "measured", key

   brier = metrics["calibration"]["values"][0]
   assert brier["denominator"] >= 4

   checkpoint_value = metrics["external_checkpoint"]["values"][0]
   assert checkpoint_value["denominator"] == 54
   assert checkpoint_value["scored_by"] == checkpoint_service.SCORED_BY_STUDENT

   experiments = {entry["name"]: entry for entry in response.json()["experiments"]}
   assert set(experiments) == set(switches.DEFINITIONS)
   assert all(entry["stated"] is False for entry in experiments.values())


def test_checkpoint_refuses_bad_scores_an_early_finish_and_a_second_start_inside_six_weeks(world):
   client = world.client()
   world.register(client)
   day = CHECKPOINT_DAY.isoformat()
   checkpoint = client.post("/checkpoints", json={"today": day}).json()
   first_part = checkpoint["sections"][0]["questions"][0]["parts"][0]

   assert checkpoint["form_year"] == forms.forms()[0].year
   assert "stem" not in json.dumps(checkpoint)

   too_many = client.post(
      f"/checkpoints/{checkpoint['id']}/scores",
      json={"record_id": first_part["record_id"], "points_earned": first_part["points"] + 1},
   )
   assert too_many.status_code == 422

   early = client.post(f"/checkpoints/{checkpoint['id']}/finish", json={"today": day})
   assert early.status_code == 409

   client.post(f"/checkpoints/{checkpoint['id']}/finish", json={"today": day})
   assert client.post("/checkpoints", json={"today": day}).status_code == 409

   finished = run_checkpoint_on_open(client, checkpoint, day)
   assert finished["finished_at"] is not None

   inside = client.get("/checkpoints", params={"today": day}).json()["availability"]
   assert inside["available"] is False
   assert inside["opens_on"] == (CHECKPOINT_DAY + timedelta(days=checkpoint_service.CADENCE_DAYS)).isoformat()

   after = (CHECKPOINT_DAY + timedelta(days=checkpoint_service.CADENCE_DAYS)).isoformat()
   second = client.post("/checkpoints", json={"today": after})
   assert second.status_code == 200
   assert second.json()["form_year"] == forms.forms()[1].year


def run_checkpoint_on_open(client, checkpoint, day):
   for section in checkpoint["sections"]:
      for question in section["questions"]:
         for part in question["parts"]:
            client.post(
               f"/checkpoints/{checkpoint['id']}/scores",
               json={"record_id": part["record_id"], "points_earned": part["points"], "today": day},
            )

   return client.post(f"/checkpoints/{checkpoint['id']}/finish", json={"today": day}).json()


def publish_probe_items(world):
   archetype = next(iter(world.settings.session_context.archetypes.values()))

   with OrmSession(world.engine) as db:
      for item_id in sorted(probe_item_ids()):
         db.add(item_row(item_id, archetype["id"], archetype["skills"]))

      db.commit()


def learner_rows(engine, user_id):
   with OrmSession(engine) as db:
      states = sorted(
         (row.skill_id, row.observation_count, row.credited_successes, row.credited_failures, row.mastered, row.stability)
         for row in db.query(models.SkillState).filter(models.SkillState.user_id == user_id)
      )

      return {
         "states": states,
         "sessions": db.query(models.Session).count(),
         "attempts": db.query(models.Attempt).count(),
         "review_queue": db.query(models.ReviewQueue).count(),
         "diagnoses": db.query(models.Diagnosis).count(),
      }


def test_checkpoint_isolated(world):
   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   practise(client, 4)
   publish_probe_items(world)
   before = learner_rows(world.engine, user_id)

   run_checkpoint(client, CHECKPOINT_DAY)
   probe = client.post("/probe", json={"today": CHECKPOINT_DAY.isoformat()}).json()

   while True:
      served = client.get(f"/probe/{probe['id']}/next").json()["item"]

      if served is None:
         break

      body = {"option_id": "A"} if served["format"] == "mcq" else {"mathjson": WRONG_MATHJSON}
      answered = client.post(
         f"/probe/{probe['id']}/answers",
         json={"item_id": served["id"], "answer": body, "elapsed_ms": 30000, "today": CHECKPOINT_DAY.isoformat()},
      )
      assert answered.status_code == 200

   after = learner_rows(world.engine, user_id)
   history = client.get("/probe", params={"today": CHECKPOINT_DAY.isoformat()}).json()["history"]

   assert after == before
   assert len(history) == 1
   assert history[0]["answered"] == len(probe_item_ids())
   assert history[0]["graded"] == len(probe_item_ids())


def test_the_feedback_switch_on_serves_verification_only_and_records_the_arm(world):
   world.settings.experiment_default_state = switches.ON
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   serve_as_mcq(world, session_id, item["id"])
   attempted = answer(client, session_id, item, {"option_id": "B"}, confidence="confident")

   assert attempted["correct"] is False

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempted['id']}/feedback").json()

   assert feedback["kind"] == "verification"
   assert feedback["elaborated"] is None
   assert feedback["self_explanation_prompt"] is None
   assert feedback["sentence"] is None

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempted["id"])

   treatment = switches.DEFINITIONS[switches.FEEDBACK_ELABORATION].treatment_arm
   assert json.loads(stored.experiment_arms) == {switches.FEEDBACK_ELABORATION: treatment}


def test_the_experiment_switch_route_sets_and_refuses(world):
   client = world.client()
   world.register(client)
   listed = client.get("/settings/experiments").json()["experiments"]

   assert {entry["name"] for entry in listed} == set(switches.DEFINITIONS)
   assert {entry["state"] for entry in listed} == {switches.OFF}

   changed = client.post(f"/settings/experiments/{switches.RETRIEVAL_ENTRY}", json={"state": switches.RANDOMISED})
   states = {entry["name"]: entry for entry in changed.json()["experiments"]}

   assert changed.status_code == 200
   assert states[switches.RETRIEVAL_ENTRY]["state"] == switches.RANDOMISED
   assert states[switches.RETRIEVAL_ENTRY]["randomised_from"] is not None
   assert client.post(f"/settings/experiments/{switches.RETRIEVAL_ENTRY}", json={"state": "sometimes"}).status_code == 422
   assert client.post("/settings/experiments/unknown", json={"state": switches.ON}).status_code == 422


def test_the_representation_matrix_counts_translation_attempts_within_practice(world):
   client = world.client()
   world.register(client)
   practise(client, 6)
   matrix = client.get("/progress/representations")

   assert matrix.status_code == 200

   body = matrix.json()
   cell_attempts = sum(cell["attempts"] for cell in body["cells"])

   assert body["practice_attempts"] > 0
   assert body["translation_attempts"] <= body["practice_attempts"]
   assert (cell_attempts > 0) == (body["translation_attempts"] > 0)


def test_a_probe_item_with_no_items_row_is_refused_not_a_server_error(world):
   client = world.client()
   world.register(client)
   probe = client.post("/probe", json={"today": CHECKPOINT_DAY.isoformat()}).json()
   served = client.get(f"/probe/{probe['id']}/next")

   assert served.status_code == 409
   assert "no items row" in served.json()["detail"]
