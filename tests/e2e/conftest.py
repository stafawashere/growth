"""Fixtures for the end-to-end run that gates P1, test 23 of docs/plan/11-phased-delivery.md.

The application is built through app/main.py, the composition root a deployment uses, over a
temporary SQLite file and the live data/ registries, so the loader, the seeding hook, the engine
and the item bank are the ones that ship. The single substitution is the passkey verifier: a
WebAuthn assertion is signed by an authenticator holding a private key, which a test process does
not have, so the ceremony is answered by a double and the account lifecycle behind it stays real.

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
CREDENTIAL_ID = b"gate-23-credential"


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


class FakeVerifier:
   """The one double: a real assertion needs an authenticator this process cannot hold."""

   def __init__(self, rp_id="localhost"):
      self.rp_id = rp_id

   def begin_registration(self, user_id, user_name):
      return {
         "challenge": "registration-challenge",
         "options": {"rp": {"id": self.rp_id}, "user": {"id": user_id, "name": user_name}},
      }

   def finish_registration(self, challenge, credential):
      offered = credential.get("credential_id")
      names_a_credential = isinstance(offered, str) and offered != ""

      return {
         "credential_id": bytes.fromhex(offered) if names_a_credential else CREDENTIAL_ID,
         "public_key": b"gate-23-public-key",
         "sign_count": int(credential.get("sign_count", 0)),
         "transports": credential.get("transports"),
      }

   def begin_login(self):
      return {"challenge": "login-challenge", "options": {"rpId": self.rp_id}}

   def finish_login(self, challenge, credential, public_key, stored_sign_count):
      return {"sign_count": int(credential.get("sign_count", 0))}


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

      return TestClient(self.application, client=("127.0.0.1", 40000))

   def register(self, client, sign_count=1):
      begun = client.post("/auth/passkey/register/begin", json={"display_name": "Student"})

      assert begun.status_code == 200, begun.text

      finished = client.post(
         "/auth/passkey/register/finish",
         json={
            "challenge_id": begun.json()["challenge_id"],
            "credential": {
               "credential_id": CREDENTIAL_ID.hex(),
               "sign_count": sign_count,
            },
         },
      )

      if finished.status_code == 200:
         self.user_id = finished.json()["user"]["id"]

      return finished

   def login(self, client, sign_count=2):
      begun = client.post("/auth/passkey/login/begin", json={})

      assert begun.status_code == 200, begun.text

      return client.post(
         "/auth/passkey/login/finish",
         json={
            "challenge_id": begun.json()["challenge_id"],
            "credential": {
               "credential_id": CREDENTIAL_ID.hex(),
               "sign_count": sign_count,
            },
         },
      )

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
   }
   application = build_application(environment)
   application.state.settings.verifier = FakeVerifier(application.state.settings.rp_id)
   built = World(application, application.state.engine, answers_by_item(fixture_records()))
   publish_fixture_items(built)

   return built
