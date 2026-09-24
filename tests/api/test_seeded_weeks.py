"""Twelve simulated weeks through the real routes with the A/B switches randomised, then a
checkpoint, a probe and the metrics view: the P7 machinery end to end on seeded data.

The student is a coin weighted by the item's archetype, so the run is reproducible and asks
nothing of a model. The fixture bank serves about five items a session, far fewer than the real
bank, so it takes twelve weeks here for both feedback arms to pass the 30-outcome floor an interval
needs. It shows the machinery works, not that anything was learned: no number here is evidence
about the real student.
"""
import json
import random
from datetime import timedelta

from sqlalchemy import update
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.experiments import switches
from app.runtime.probe_set import probe_item_ids
from tests.api.conftest import KEY_MATHJSON, TODAY, WRONG_MATHJSON
from tests.api.test_evaluation_routes import publish_probe_items, run_checkpoint

WEEKS = 12
SEED = 20260924
WORKED_STEPS = [
   {"step": 1, "text": "Divide out the common factor.", "mathjson": 0},
   {"step": 2, "text": "Evaluate what is left.", "mathjson": KEY_MATHJSON},
]


def give_every_item_worked_steps(engine):
   """The shared fixture rows carry a one-line worked solution, enough for stage unsupported. Eight
   weeks of failures fade some skills back to completion, which serves steps, so these rows get
   two."""
   with OrmSession(engine) as db:
      db.execute(update(models.Item).values(worked_solution=json.dumps(WORKED_STEPS)))
      db.commit()


def day_session(client, day, rng):
   opened = client.post("/sessions", json={"mode": "learning", "today": day.isoformat()})

   assert opened.status_code == 200

   session_id = opened.json()["id"]

   while True:
      served = client.get(f"/sessions/{session_id}/next")
      assert served.status_code == 200, served.text
      item = served.json()["item"]

      if item is None:
         break

      archetype_bias = (sum(ord(character) for character in item["archetype_id"]) % 5) / 10
      is_correct = rng.random() < 0.35 + archetype_bias
      is_mcq = item["format"] == "mcq"

      if is_mcq:
         body = {"option_id": "A" if is_correct else "B"}
      else:
         body = {"mathjson": KEY_MATHJSON if is_correct else WRONG_MATHJSON}

      attempted = client.post(
         f"/sessions/{session_id}/attempts",
         json={
            "item_id": item["id"],
            "answer": body,
            "elapsed_ms": 60000,
            "today": day.isoformat(),
            "confidence": rng.choice(["guess", "unsure", "confident"]),
         },
      )

      assert attempted.status_code == 200

   assert client.post(f"/sessions/{session_id}/close", json={"today": day.isoformat()}).status_code == 200


def eval_the_harness_runs_end_to_end_on_seeded_weeks(world):
   world.settings.experiment_default_state = switches.RANDOMISED
   client = world.client()
   world.register(client)
   publish_probe_items(world)
   give_every_item_worked_steps(world.engine)
   rng = random.Random(SEED)
   days = [TODAY + timedelta(days=offset) for offset in range(WEEKS * 7)]

   for day in days:
      day_session(client, day, rng)

   last_day = days[-1]
   checkpoint = run_checkpoint(client, last_day)
   probe = client.post("/probe", json={"today": last_day.isoformat()}).json()

   while True:
      served = client.get(f"/probe/{probe['id']}/next").json()["item"]

      if served is None:
         break

      client.post(
         f"/probe/{probe['id']}/answers",
         json={"item_id": served["id"], "answer": {"option_id": "A"}, "today": last_day.isoformat()},
      )

   body = client.get("/progress/metrics", params={"today": last_day.isoformat()}).json()
   metrics = {metric["key"]: metric for metric in body["metrics"]}
   experiments = {entry["name"]: entry for entry in body["experiments"]}
   switch_view = {entry["name"]: entry for entry in client.get("/settings/experiments").json()["experiments"]}
   feedback = experiments[switches.FEEDBACK_ELABORATION]

   assert checkpoint["finished_at"] is not None
   assert metrics["concept_probe"]["values"][0]["denominator"] == len(probe_item_ids())
   assert metrics["retention_7_30"]["status"] == "measured"
   assert metrics["calibration"]["status"] == "measured"
   assert all(count > 0 for count in switch_view[switches.FEEDBACK_ELABORATION]["assigned_units"].values())
   assert sum(switch_view[switches.RETRIEVAL_ENTRY]["assigned_units"].values()) > 0
   assert feedback["stated"] is True
   assert feedback["interval_low"] <= feedback["difference"] <= feedback["interval_high"]
   assert min(feedback["control"]["outcomes"], feedback["treatment"]["outcomes"]) >= feedback["minimum_outcomes_per_arm"]
