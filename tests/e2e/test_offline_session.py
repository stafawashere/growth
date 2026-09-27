"""11 P6 test_offline_session, cut to one student: with the network down, a whole learning session
runs to completion on pre-generated items.

The application is the one app/main.py builds on its default backend, the operator's subscription.
Offline, the claude CLI starts and fails, which tests/fixtures/fake_claude/claude plays in its
nonzero mode; no socket may open. Every item is answered wrongly, so every feedback screen asks the
tutor, and every one must still come back with the deterministic feedback and no sentence. After
FAILURES_BEFORE_COOLDOWN failures the subscription link cools and later screens start no process.
Grading, the engine and session assembly are local, so the session closes normally.
"""
import json

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.auth.service import utc_now
from app.db import models
from app.main import DEFAULT_CONTENT_DIR, build_application
from app.providers.router import FAILURES_BEFORE_COOLDOWN, SUBSCRIPTION_LINK
from tests.e2e.conftest import FIRST_DAY, FAST_SCRYPT_ENVIRONMENT, World
from tests.e2e.test_agent_drafts_served import key_answers
from tests.e2e.test_session_login_to_feedback import collects_confidence, rate, submit
from tests.providers.test_subscription import FakeCli

BANK = DEFAULT_CONTENT_DIR / "items_p1_agent"
NOT_ANY_KEY = 987654321


@pytest.fixture
def offline_world(tmp_path, forbid_network):
   home = tmp_path / "home"
   home.mkdir()
   cli = FakeCli(home)
   cli.mode("nonzero")
   records = [json.loads(path.read_text()) for path in sorted(BANK.glob("ITM-*.json"))]
   environment = cli.environ(
      GROWTH_DB_PATH=str(tmp_path / "growth.db"),
      GROWTH_RNG_SEED="7",
      GROWTH_EXAM_DATE="2027-05-10",
      GROWTH_ITEMS_DIR=str(BANK),
      GROWTH_AUTO_DRAIN="off",
      **FAST_SCRYPT_ENVIRONMENT,
   )
   application = build_application(environment)
   world = World(application, application.state.engine, key_answers(records))
   world.records = {record["id"]: record for record in records}

   return world, cli


def wrong_answer(world, item):
   is_mcq = item["format"] == "mcq"

   if is_mcq:
      options = world.records[item["id"]]["options"]
      wrong_option = next(option["id"] for option in options if option["is_key"] is not True)

      return {"option_id": wrong_option}

   return {"mathjson": NOT_ANY_KEY}


def every_skill_unsupported(world):
   """A new account's stage comes from its prior, mostly the worked-example end of the fading
   ladder, where feedback is step marks and no tutor is asked. A stored stage with one credited
   observation behind it wins over the prior (app/engine/fringe.py serve_stage), so every skill is
   moved to unsupported, which puts the tutor behind every wrong answer."""
   with OrmSession(world.engine) as db:
      rows = db.query(models.SkillState).filter(models.SkillState.user_id == world.user_id).all()

      for row in rows:
         row.fading_stage = "unsupported"
         row.credited_observation_count = max(row.credited_observation_count or 0, 1)

      db.commit()


def test_offline_session(offline_world):
   world, cli = offline_world
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200, registered.text

   every_skill_unsupported(world)
   assert [link.name for link in world.settings.tutor_links] == [SUBSCRIPTION_LINK]

   opened = client.post("/sessions", json={"mode": "learning", "today": FIRST_DAY.isoformat()})

   assert opened.status_code == 200, opened.text

   session_id = opened.json()["id"]
   feedback_screens = []

   while True:
      offered = client.get(f"/sessions/{session_id}/next")

      assert offered.status_code == 200, offered.text

      item = offered.json()["item"]

      if item is None:
         break

      submitted = submit(client, session_id, item, wrong_answer(world, item), FIRST_DAY)

      assert submitted.status_code == 200, submitted.text

      attempt = submitted.json()

      assert attempt["correct"] is False

      if collects_confidence(item):
         assert rate(client, session_id, attempt["id"], "unsure", FIRST_DAY).status_code == 200

      shown = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback")

      assert shown.status_code == 200, shown.text

      feedback_screens.append(shown.json())

   closed = client.post(f"/sessions/{session_id}/close", json={"today": FIRST_DAY.isoformat()})

   assert closed.status_code == 200, closed.text
   tutor_screens = [screen for screen in feedback_screens if screen["elaborated"] is not None]

   assert len(tutor_screens) > FAILURES_BEFORE_COOLDOWN
   assert all(screen["sentence"] is None for screen in feedback_screens)
   assert all(screen["tutor_unavailable"] is False for screen in feedback_screens)

   with OrmSession(world.engine) as db:
      session_row = db.get(models.Session, session_id)
      graded = db.query(models.Attempt).filter(models.Attempt.session_id == session_id).all()

   assert session_row.ended_at is not None
   assert len(graded) == len(feedback_screens)
   assert all(row.correct == 0 for row in graded)

   cooling = world.settings.provider_cooldowns.snapshot(utc_now())

   assert [entry["link"] for entry in cooling] == [SUBSCRIPTION_LINK]
