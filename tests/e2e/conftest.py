"""Fixtures for the end-to-end run that gates P1, test 23 of docs/plan/11-phased-delivery.md.

The application is built through app/main.py, the composition root a deployment uses, over a
temporary SQLite file and the live data/ registries, so the loader, the seeding hook, the engine
and the item bank are the ones that ship. Sign-in is the real username and password path with no
double; the environment only lowers the scrypt cost to about a millisecond per hash and raises the
per-IP limit out of reach, both through the variables a deployment would set.

The tutor is app/providers/replay.ReplayProvider over the hand-written cassette in
tests/fixtures/provider_cassettes/, and the socket ban below is what proves nothing else dialled
out while the flow ran.
"""
import json
import socket
from datetime import date
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.items import ingest
from app.main import build_application

REPO_ROOT = Path(__file__).resolve().parents[2]
ITEMS_DIRECTORY = REPO_ROOT / "tests" / "fixtures" / "items_p1"
CASSETTE_PATH = (
   REPO_ROOT / "tests" / "fixtures" / "provider_cassettes" / "tutor_elaborated_v1.json"
)
FIRST_DAY = date(2026, 9, 1)
INGESTED_AT = "2026-09-01T09:00:00+00:00"
USERNAME = "gate_student"
PASSWORD = "gate twenty three password"
FAST_SCRYPT_ENVIRONMENT = {
   "GROWTH_SCRYPT_N": str(2 ** 10),
   "GROWTH_SCRYPT_R": "8",
   "GROWTH_SCRYPT_P": "1",
   "GROWTH_AUTH_RATE_LIMIT": "100000",
}


class NetworkCallInTest(AssertionError):
   pass


REAL_SOCKET = socket.socket
ROUTED_FAMILIES = (socket.AF_INET, socket.AF_INET6)


def refuse_network_socket(family=socket.AF_INET, *arguments, **keywords):
   """AF_UNIX is what the test client's own event loop opens for its wake-up pipe, and it goes
   nowhere; a routed family is a call leaving this process and is what gate 23 forbids.
   """
   leaves_the_machine = family in ROUTED_FAMILIES

   if leaves_the_machine:
      raise NetworkCallInTest(
         "gate 23 forbids a network call: the tutor is the replayed cassette and the database is "
         f"a local SQLite file, so nothing in this flow may open a {family!r} socket"
      )

   return REAL_SOCKET(family, *arguments, **keywords)


def refuse_connection(*arguments, **keywords):
   raise NetworkCallInTest("gate 23 forbids a network call, and one was dialled")


@pytest.fixture
def forbid_network(monkeypatch):
   """Mechanical proof of the no-network half of gate 23, rather than a reading of the code."""
   monkeypatch.setattr(socket, "socket", refuse_network_socket)
   monkeypatch.setattr(socket, "create_connection", refuse_connection)

   return refuse_network_socket


def fixture_records():
   paths = sorted(path for path in ITEMS_DIRECTORY.iterdir() if path.suffix == ".json")

   return [json.loads(path.read_text()) for path in paths]


def answers_by_item(records):
   """What the student types: the key of each fixture item and one wrong answer for it."""
   answers = {}

   for record in records:
      options = record["options"]
      key_option = [option for option in options if option["is_key"] is True][0]
      distractors = [option for option in options if option["is_key"] is not True]

      answers[record["id"]] = {
         "key_option_id": key_option["id"],
         "key_mathjson": record["answer_key"]["mathjson"],
         "wrong_option_id": distractors[0]["id"],
         "wrong_mathjson": distractors[0]["value"],
         "wrong_error_path": distractors[0]["error_path"],
      }

   return answers


class World:
   def __init__(self, application, engine, answers):
      self.application = application
      self.settings = application.state.settings
      self.engine = engine
      self.answers = answers
      self.user_id = None

   def client(self):
      from starlette.testclient import TestClient

      return TestClient(self.application, client=("127.0.0.1", 40000), base_url="http://127.0.0.1")

   def register(self, client, username=USERNAME, password=PASSWORD):
      finished = client.post("/auth/signup", json={"username": username, "password": password})

      if finished.status_code == 200:
         self.user_id = finished.json()["user"]["id"]

      return finished

   def login(self, client, username=USERNAME, password=PASSWORD):
      return client.post("/auth/login", json={"username": username, "password": password})

   def attempt_error_note(self, attempt_id):
      """Read out of SQLite, because the POST's own echo says nothing about the column."""
      with OrmSession(self.engine) as db:
         return db.get(models.Attempt, attempt_id).error_note

   def skill_state_rows(self):
      with OrmSession(self.engine) as db:
         rows = (
            db.query(models.SkillState)
            .filter(models.SkillState.user_id == self.user_id)
            .order_by(models.SkillState.skill_id)
            .all()
         )

         return {
            row.skill_id: {
               "fading_stage": row.fading_stage,
               "observation_count": row.observation_count,
               "credited_successes": row.credited_successes,
               "credited_failures": row.credited_failures,
               "consecutive_successes": row.consecutive_successes,
               "consecutive_failures": row.consecutive_failures,
               "hypercorrection_due": row.hypercorrection_due,
               "updated_at": row.updated_at,
            }
            for row in rows
         }


def publish_fixture_items(world):
   """The fixture items reach the bank through app/items/ingest.py, the path the operator uses."""
   context = world.settings.session_context
   active_error_ids = set(context.errors)

   with OrmSession(world.engine) as db:
      results = ingest.ingest_directory(
         db, ITEMS_DIRECTORY, active_error_ids, context.snapshot_id, INGESTED_AT
      )
      db.commit()

   rejected = [result for result in results if result["status"] != "verified"]

   assert rejected == [], f"the fixture items must publish, and these did not: {rejected}"

   return results


@pytest.fixture
def world(tmp_path, forbid_network):
   environment = {
      "GROWTH_DB_PATH": str(tmp_path / "growth.db"),
      "GROWTH_CONTENT_ROOT": str(REPO_ROOT / "data"),
      "GROWTH_TUTOR_PROVIDER": "replay",
      "GROWTH_TUTOR_CASSETTE": str(CASSETTE_PATH),
      "GROWTH_RNG_SEED": "7",
      "GROWTH_EXAM_DATE": "2027-05-10",
      "GROWTH_ITEMS_DIR": "none",
      **FAST_SCRYPT_ENVIRONMENT,
   }
   application = build_application(environment)
   built = World(application, application.state.engine, answers_by_item(fixture_records()))
   publish_fixture_items(built)

   return built
