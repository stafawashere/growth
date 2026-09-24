"""P2 end to end: a new user runs the diagnostic and lands on a populated queue.

Built through app/main.py over the live data/ registries and the default item directory, the
published bank a real first login meets. The student answers Unit 1 items correctly and says
"I have not learned this yet" to everything else, then comes back the next day, and later after a
gap of more than 21 days, which offers a re-diagnostic that only adds to what was placed. One test
function carries the whole account's life because building the bank costs about a minute.
"""
import json
import math
from datetime import timedelta

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine import constants
from tests.e2e.conftest import FIRST_DAY
from tests.e2e.test_agent_drafts_served import agent_world  # noqa: F401

KNOWN_UNIT = "BC-UNIT-01"
UNIT_STATE_WORDS = {"not_started", "partial", "fluent", "unresolved", "not_probed"}


def progress(client, day):
   response = client.get("/progress", params={"today": day.isoformat()})

   assert response.status_code == 200, response.text

   return response.json()


def run_diagnostic(world, client, day):
   opened = client.post("/sessions", json={"mode": "diagnostic", "today": day.isoformat()})

   assert opened.status_code == 200, opened.text

   session_id = opened.json()["id"]
   archetypes = world.settings.session_context.archetypes
   asked = 0

   while True:
      served = client.get(f"/sessions/{session_id}/next", params={"today": day.isoformat()})

      assert served.status_code == 200, served.text

      body = served.json()

      if body["diagnostic_finished"]:
         break

      item = body["item"]
      asked += 1

      assert item["stage"] == "unsupported"
      assert item["format"] == "short_answer"
      assert asked <= constants.DIAG_CAP

      knows_it = archetypes[item["archetype_id"]]["primary_unit"] == KNOWN_UNIT
      answer = (
         {"mathjson": world.answers[item["id"]]["key_mathjson"]}
         if knows_it
         else {"not_learned": True}
      )
      submitted = client.post(
         f"/sessions/{session_id}/attempts",
         json={"item_id": item["id"], "answer": answer, "elapsed_ms": 60000, "today": day.isoformat()},
      )

      assert submitted.status_code == 200, submitted.text
      assert submitted.json()["correct"] is None

   return session_id, asked


def mastered_skills(world):
   with OrmSession(world.engine) as db:
      rows = (
         db.query(models.SkillState)
         .filter(models.SkillState.user_id == world.user_id, models.SkillState.mastered == 1)
         .all()
      )

      return {row.skill_id for row in rows}


def test_cold_start_to_first_session(agent_world):
   world = agent_world
   client = world.client()

   assert world.register(client).status_code == 200
   assert progress(client, FIRST_DAY)["home_state"] == "first_login"

   session_id, asked = run_diagnostic(world, client, FIRST_DAY)

   assert 0 < asked <= constants.DIAG_CAP

   result = client.get(f"/sessions/{session_id}/diagnostic")

   assert result.status_code == 200, result.text

   summary = result.json()
   rendered = json.dumps(summary)

   assert summary["finished"] is True
   assert len(summary["units"]) == 10
   assert {unit["state"] for unit in summary["units"]} <= UNIT_STATE_WORDS
   assert "%" not in rendered and "percent" not in rendered and "score" not in rendered

   with OrmSession(world.engine) as db:
      attempt_ids = [
         row.id for row in db.query(models.Attempt).filter(models.Attempt.session_id == session_id)
      ]
      diagnosed = db.query(models.Diagnosis).filter(models.Diagnosis.attempt_id.in_(attempt_ids)).count()

   assert len(attempt_ids) == asked
   assert diagnosed == asked

   day_two = FIRST_DAY + timedelta(days=1)
   home = progress(client, day_two)

   assert home["home_state"] == "queue"
   assert home["diagnostic_in_progress"] is None
   assert home["forecast_minutes"] > 0 and math.isfinite(home["forecast_minutes"])
   assert home["frontier_skills"] + home["skills_due_for_review"] > 0
   assert math.isfinite(home["due_today_minutes"])

   opened = client.post("/sessions", json={"today": day_two.isoformat()})

   assert opened.status_code == 200, opened.text

   queue = opened.json()["queue"]
   served = queue["block1"] + queue["block2"] + queue["block3"]

   assert len(served) > 0
   assert queue["interleaving_satisfied"] is True

   placed = mastered_skills(world)
   last_session_day = day_two

   assert progress(client, last_session_day + timedelta(days=constants.GAP_DAYS_DIAGNOSTIC))["home_state"] == "queue"

   returning_day = last_session_day + timedelta(days=constants.GAP_DAYS_DIAGNOSTIC + 1)

   assert progress(client, returning_day)["home_state"] == "long_gap"

   run_diagnostic(world, client, returning_day)

   assert progress(client, returning_day)["home_state"] == "queue"
   assert placed <= mastered_skills(world)
