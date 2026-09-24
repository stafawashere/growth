"""A real session serves a Unit 6 item from content/items_unit06_agent end to end.

Stage 1 exit criterion: the application built by app/main.py, with the test passkey verifier and
the replayed tutor, serves an item from a unit P1 never reached, takes the answer, grades it and
shows its feedback. A new account starts at the Unit 1 fringe, so the student's state is seeded:
every skill outside Unit 6 is marked mastered, which puts the Unit 6 skills whose parents lie
elsewhere on the fringe (app/engine/fringe.py outer_fringe). Everything after the seed, from
opening the session to reading the feedback, goes through the HTTP routes.
"""
import json

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.main import DEFAULT_CONTENT_DIR, build_application
from tests.e2e.conftest import CASSETTE_PATH, FIRST_DAY, FakeVerifier, World
from tests.e2e.test_agent_drafts_served import answer_and_read_feedback, key_answers, stored_provenance

UNIT_6_BANK_NAME = "items_unit06_agent"
UNIT_6 = "BC-UNIT-06"
UNIT_6_SKILL_PREFIX = "BC-SKL-06"


@pytest.fixture
def unit_6_world(tmp_path, forbid_network):
   bank = DEFAULT_CONTENT_DIR / UNIT_6_BANK_NAME
   records = [json.loads(path.read_text()) for path in sorted(bank.glob("ITM-*.json"))]
   environment = {
      "GROWTH_DB_PATH": str(tmp_path / "growth.db"),
      "GROWTH_TUTOR_PROVIDER": "replay",
      "GROWTH_TUTOR_CASSETTE": str(CASSETTE_PATH),
      "GROWTH_RNG_SEED": "7",
      "GROWTH_EXAM_DATE": "2027-05-10",
      "GROWTH_ITEMS_DIR": str(bank),
   }
   application = build_application(environment)
   application.state.settings.verifier = FakeVerifier(application.state.settings.rp_id)

   return World(application, application.state.engine, key_answers(records))


def master_every_skill_outside_unit_6(world):
   with OrmSession(world.engine) as db:
      rows = db.query(models.SkillState).filter(models.SkillState.user_id == world.user_id).all()
      outside_unit_6 = [row for row in rows if not row.skill_id.startswith(UNIT_6_SKILL_PREFIX)]

      for row in outside_unit_6:
         row.mastered = 1
         row.mastered_at = FIRST_DAY.isoformat()

      db.commit()

      return len(outside_unit_6)


def test_a_session_serves_a_unit_6_item_end_to_end(unit_6_world):
   client = unit_6_world.client()
   registered = unit_6_world.register(client)

   assert registered.status_code == 200, registered.text
   assert master_every_skill_outside_unit_6(unit_6_world) > 0

   opened = client.post("/sessions", json={"mode": "learning", "today": FIRST_DAY.isoformat()})

   assert opened.status_code == 200, opened.text

   session_id = opened.json()["id"]
   offered = client.get(f"/sessions/{session_id}/next")

   assert offered.status_code == 200, offered.text

   item = offered.json()["item"]

   assert item is not None
   assert item["id"].startswith("ITM-AGT-06")

   archetype = unit_6_world.settings.session_context.archetypes[item["archetype_id"]]

   assert archetype["primary_unit"] == UNIT_6

   feedback = answer_and_read_feedback(client, session_id, item, unit_6_world.answers[item["id"]], FIRST_DAY)

   assert feedback["stage"] == item["stage"]
   assert stored_provenance(unit_6_world, item["id"])["model"] == "operator"
