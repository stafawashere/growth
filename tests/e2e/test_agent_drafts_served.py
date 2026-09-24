"""A session built by app/main.py with GROWTH_ITEMS_DIR unset serves the agent drafts.

The operator ruled on 2026-09-23 that the drafts in content/items_p1_agent/ may be served so the
app can teach before the operator's own 130 items exist; since stage 1 the default is every
content/items_* bank. Nothing but the default wiring puts them in the bank here: the application
is built from an environment that names no item directory, the bank ingests the default ones on
its first query, and the student answers a Unit 2 item from them through the HTTP routes with the
replayed tutor, down to its feedback screen.
"""
import json

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.main import DEFAULT_ITEMS_DIR, build_application, default_item_directories
from tests.e2e.conftest import CASSETTE_PATH, FIRST_DAY, FakeVerifier, World
from tests.e2e.test_session_login_to_feedback import answer_for, collects_confidence, rate, submit

AGENT_AUTHORS = {
   "claude-opus-5-5 agent draft, pending operator review",
   "claude-opus-5-5 agent draft, stage 1 content run of 2026-09-24",
}
UNIT_2 = "BC-UNIT-02"
DAYS_BETWEEN_SESSIONS = 8
MAX_SESSIONS = 12


def agent_records():
   paths = sorted(path for directory in default_item_directories() for path in directory.glob("ITM-*.json"))

   return [json.loads(path.read_text()) for path in paths]


def key_answers(records):
   """The key of each draft, as an option id where the draft carries options (51 of the 130 are
   short answer only and carry none) and as MathJSON always.
   """
   answers = {}

   for record in records:
      key_options = [option for option in record.get("options") or [] if option["is_key"] is True]
      has_key_option = len(key_options) == 1

      answers[record["id"]] = {
         "key_option_id": key_options[0]["id"] if has_key_option else None,
         "key_mathjson": record["answer_key"].get("mathjson"),
      }

   return answers


@pytest.fixture
def agent_world(tmp_path, forbid_network):
   environment = {
      "GROWTH_DB_PATH": str(tmp_path / "growth.db"),
      "GROWTH_TUTOR_PROVIDER": "replay",
      "GROWTH_TUTOR_CASSETTE": str(CASSETTE_PATH),
      "GROWTH_RNG_SEED": "7",
      "GROWTH_EXAM_DATE": "2027-05-10",
   }
   application = build_application(environment)
   application.state.settings.verifier = FakeVerifier(application.state.settings.rp_id)

   return World(application, application.state.engine, key_answers(agent_records()))


def primary_unit(world, item):
   return world.settings.session_context.archetypes[item["archetype_id"]]["primary_unit"]


def on_disk_record(item_id):
   """The drafts were signed off on the operator's delegation of 2026-09-24, so each record now
   names its drafter in drafted_by and is served with provenance model operator."""
   paths = [directory / f"{item_id}.json" for directory in default_item_directories()]
   existing = [path for path in paths if path.is_file()]

   assert len(existing) == 1, existing

   return json.loads(existing[0].read_text())


def stored_provenance(world, item_id):
   with OrmSession(world.engine) as db:
      return json.loads(db.get(models.Item, item_id).provenance)


def answer_and_read_feedback(client, session_id, item, entry, today):
   submitted = submit(client, session_id, item, answer_for(entry, item, True), today)

   assert submitted.status_code == 200, submitted.text

   attempt = submitted.json()

   assert attempt["correct"] is True, json.dumps({"item": item, "attempt": attempt})

   if collects_confidence(item):
      rated = rate(client, session_id, attempt["id"], "confident", today)

      assert rated.status_code == 200, rated.text

   shown = client.get(f"/sessions/{session_id}/attempts/{attempt['id']}/feedback")

   assert shown.status_code == 200, shown.text

   return shown.json()


def serve_until_a_unit_2_item(world, client):
   """Drains whole sessions, answering every item correctly, until an agent draft from Unit 2 is
   served; generated items from Unit 2 are served alongside the drafts since P4."""
   served = []
   today = FIRST_DAY

   for _session_index in range(MAX_SESSIONS):
      opened = client.post("/sessions", json={"mode": "learning", "today": today.isoformat()})

      assert opened.status_code == 200, opened.text

      session_id = opened.json()["id"]

      while True:
         offered = client.get(f"/sessions/{session_id}/next")

         assert offered.status_code == 200, offered.text

         item = offered.json()["item"]
         is_drained = item is None

         if is_drained:
            break

         served.append(item)
         feedback = answer_and_read_feedback(
            client, session_id, item, world.answers[item["id"]], today
         )
         is_from_unit_2 = primary_unit(world, item) == UNIT_2
         is_an_agent_draft = item["id"].startswith("ITM-AGT-")

         if is_from_unit_2 and is_an_agent_draft:
            return item, feedback, served

      closed = client.post(f"/sessions/{session_id}/close", json={"today": today.isoformat()})

      assert closed.status_code == 200, closed.text

      today = today.fromordinal(today.toordinal() + DAYS_BETWEEN_SESSIONS)

   raise AssertionError(
      f"no Unit 2 item was served in {MAX_SESSIONS} sessions; served {[item['id'] for item in served]}"
   )


def test_a_session_serves_an_agent_drafted_unit_2_item_end_to_end(agent_world):
   assert agent_world.settings.items_directories == default_item_directories()
   assert DEFAULT_ITEMS_DIR in agent_world.settings.items_directories

   client = agent_world.client()
   registered = agent_world.register(client)

   assert registered.status_code == 200, registered.text

   unit_2_item, feedback, served = serve_until_a_unit_2_item(agent_world, client)
   served_ids = {item["id"] for item in served}
   not_an_agent_draft = sorted(served_ids - set(agent_world.answers))

   assert not_an_agent_draft == []
   assert unit_2_item["id"].startswith("ITM-AGT-02")
   assert feedback["stage"] == unit_2_item["stage"]
   assert stored_provenance(agent_world, unit_2_item["id"])["model"] == "operator"
   assert on_disk_record(unit_2_item["id"])["drafted_by"] in AGENT_AUTHORS
