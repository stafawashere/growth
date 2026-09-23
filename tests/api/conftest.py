"""Fixtures for the HTTP layer tests.

The engine graph, the archetypes and the item bank come from tests/fixtures/graph_p1.json through
the same helpers the selection and session-service tests use, so nothing here rebuilds a fixture.
The passkey verifier and the two hooks the other P1 modules own (skills_state seeding and the
purge) are supplied as test doubles through settings, which is what keeps the HTTP tests off the
live library loader.
"""
import json
from datetime import date, datetime, timezone

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.api.app import SessionContext, Settings, create_app
from app.db import models
from app.engine.state import FadingStage
from app.providers.guard import BudgetCaps
from app.session import repository
from tests.engine.conftest_selection import build_bank, build_graph, build_states, load_fixture
from tests.session.test_service import engine_graph_from

SNAPSHOT_ID = "SNAP-0001"
TUTOR_CAP_USD = 1.00
TODAY = date(2026, 3, 1)
ACCOUNT_CREATED_AT = datetime(2026, 1, 1, 9, 0, 0, tzinfo=timezone.utc)
CREDENTIAL_ID = b"cred-1"
ERROR_RECORDS = {
   "BC-ERR-02001": {
      "id": "BC-ERR-02001",
      "observed_behavior": "the common factor is cancelled before the rewrite",
      "scoring_consequence": "the answer point is lost",
   },
}
PUBLIC_KEY = b"public-key-1"
KEY_MATHJSON = ["Add", ["Multiply", 2, "x"], 1]
WRONG_MATHJSON = ["Add", ["Multiply", 2, "x"], 2]
ITEM_OPTIONS = [
   {"id": "A", "is_key": True, "error_path": None},
   {"id": "B", "is_key": False, "error_path": "BC-ERR-02001", "violated_step": 1},
   {"id": "C", "is_key": False, "error_path": "BC-ERR-02001", "violated_step": 2},
   {"id": "D", "is_key": False, "error_path": "BC-ERR-02001", "violated_step": 3},
]


def item_row(item_id, archetype_id, skills):
   """A published row for every item the fixture bank serves, so the route grades a real key."""
   return models.Item(
      id=item_id,
      archetype_id=archetype_id,
      variant_id=None,
      snapshot_id=SNAPSHOT_ID,
      parameter_draw="{}",
      stem="stem",
      figure_spec=None,
      options=[dict(option) for option in ITEM_OPTIONS],
      answer_key=json.dumps({"form": "symbolic", "mathjson": KEY_MATHJSON}),
      worked_solution="divide out the factor, then evaluate",
      calculator_status="no_calculator",
      representation="BC-REP-01",
      difficulty_settings="{}",
      skills=json.dumps(list(skills)),
      provenance="{}",
      status="verified",
      dedupe_minhash="[]",
      created_at=TODAY.isoformat(),
      updated_at=TODAY.isoformat(),
   )


def publish_bank_items(engine, fixture, items_per_archetype=3):
   with OrmSession(engine) as db:
      for record in fixture["archetypes"]:
         archetype_id = record["id"]

         for index in range(items_per_archetype):
            db.add(item_row(f"{archetype_id}-V{index:02d}", archetype_id, record["skills"]))

      db.commit()


class FakeVerifier:
   """A PasskeyVerifier that trusts the payload, so the tests exercise the service, not a library."""

   def __init__(self):
      self.rp_id = "localhost"

   def begin_registration(self, user_id, user_name, exclude_credential_ids=()):
      options = {
         "rp": {"id": self.rp_id},
         "user": {"id": user_id, "name": user_name},
         "excludeCredentials": [credential_id.hex() for credential_id in exclude_credential_ids],
      }

      return {"challenge": "reg-challenge", "options": options}

   def finish_registration(self, challenge, credential):
      offered = credential.get("credential_id")
      names_a_credential = isinstance(offered, str) and offered != ""

      return {
         "credential_id": bytes.fromhex(offered) if names_a_credential else CREDENTIAL_ID,
         "public_key": PUBLIC_KEY,
         "sign_count": int(credential.get("sign_count", 0)),
         "transports": credential.get("transports"),
      }

   def begin_login(self, credential_ids=None):
      allow_credentials = [
         {"id": credential_id.hex(), "type": "public-key"} for credential_id in (credential_ids or [])
      ]

      return {
         "challenge": "login-challenge",
         "options": {"rpId": self.rp_id, "allowCredentials": allow_credentials},
      }

   def finish_login(self, challenge, credential, public_key, stored_sign_count):
      return {"sign_count": int(credential.get("sign_count", 0))}


def unsupported_states(fixture):
   """Seed the fixture states at stage unsupported, which is the stage that collects a rating."""
   states = build_states(fixture)

   for state in states.values():
      if not state.mastered:
         state.fading_stage = FadingStage.UNSUPPORTED
         state.observation_count = 1
         state.credited_observation_count = 1

   return states


class Recorder:
   def __init__(self):
      self.calls = []
      self.snapshots = []


@pytest.fixture
def world(tmp_path):
   fixture = load_fixture()
   engine = models.make_engine(tmp_path / "growth.db")
   seeds = Recorder()
   purges = Recorder()

   def seed_hook(db, user_id, snapshot, created_at, snapshot_id=None):
      seeds.calls.append(user_id)
      seeds.snapshots.append(snapshot)
      states = unsupported_states(fixture)
      repository.save_states(db, user_id, states, SNAPSHOT_ID, created_at)

      return len(states)

   def purge_hook(db, user_id, now):
      purges.calls.append(user_id)
      deleted = (
         db.query(models.SkillState)
         .filter(models.SkillState.user_id == user_id)
         .delete()
      )

      return {"skills_state": deleted}

   context = SessionContext(
      graph=build_graph(fixture),
      engine_graph=engine_graph_from(fixture),
      archetypes={record["id"]: record for record in fixture["archetypes"]},
      bank=build_bank(fixture),
      snapshot_id=SNAPSHOT_ID,
      errors=ERROR_RECORDS,
   )
   settings = Settings(
      engine=engine,
      snapshot=fixture,
      session_context=context,
      verifier=FakeVerifier(),
      seed_hook=seed_hook,
      purge_hook=purge_hook,
      tutor_caps={"tutor": BudgetCaps(cap_usd=TUTOR_CAP_USD)},
   )

   with OrmSession(engine) as db:
      db.add(
         models.ContentSnapshot(
            id=SNAPSHOT_ID,
            loaded_at=ACCOUNT_CREATED_AT.isoformat(),
            library_commit=None,
            digest="digest-0001",
            counts='{"skills": 54}',
            status="active",
            rejection_reason=None,
            created_at=ACCOUNT_CREATED_AT.isoformat(),
            updated_at=ACCOUNT_CREATED_AT.isoformat(),
         )
      )
      db.commit()

   publish_bank_items(engine, fixture)

   return World(create_app(settings), engine, seeds, purges)


class World:
   def __init__(self, app, engine, seeds, purges):
      self.app = app
      self.settings = app.state.settings
      self.engine = engine
      self.seeds = seeds
      self.purges = purges
      self.sign_count = 5

   def client(self, host="127.0.0.1"):
      """Starlette's TestClient parses its own base_url netloc by splitting on the first colon,
      which breaks on a bracketed IPv6 literal (`[::1]`.split(":", 1)` leaves `":1]"` for `int()`
      to choke on). The base_url stays a host httpx can parse, and an explicit Host header carries
      the IPv6 literal instead, which Starlette's own URL(scope=...) accepts through _HOST_RE and
      uses ahead of scope["server"], so request.url.hostname still comes back "::1"."""
      from starlette.testclient import TestClient

      is_ipv6_literal = ":" in host
      headers = {"host": f"[{host}]"} if is_ipv6_literal else None
      base_url = "http://127.0.0.1" if is_ipv6_literal else f"http://{host}"

      return TestClient(self.app, client=(host, 40000), base_url=base_url, headers=headers)

   def register(self, client, sign_count=5, credential_id=None, recovery_code=None):
      begun = client.post("/auth/passkey/register/begin", json={"display_name": "Student"})
      assert begun.status_code == 200
      credential = {"sign_count": sign_count}
      names_a_credential = credential_id is not None

      if names_a_credential:
         credential["credential_id"] = credential_id

      payload = {
         "challenge_id": begun.json()["challenge_id"],
         "credential": credential,
      }
      offers_a_code = recovery_code is not None

      if offers_a_code:
         payload["recovery_code"] = recovery_code

      return client.post("/auth/passkey/register/finish", json=payload)

   def recover(self, client, code, credential_id=None, sign_count=1):
      begun = client.post("/auth/recovery/register/begin", json={})
      assert begun.status_code == 200
      credential = {"sign_count": sign_count}
      names_a_credential = credential_id is not None

      if names_a_credential:
         credential["credential_id"] = credential_id

      payload = {
         "challenge_id": begun.json()["challenge_id"],
         "credential": credential,
         "recovery_code": code,
      }

      return client.post("/auth/recovery/register/finish", json=payload)

   def login(self, client, sign_count=6):
      begun = client.post("/auth/passkey/login/begin", json={})
      assert begun.status_code == 200
      payload = {
         "challenge_id": begun.json()["challenge_id"],
         "credential": {
            "credential_id": CREDENTIAL_ID.hex(),
            "sign_count": sign_count,
         },
      }

      return client.post("/auth/passkey/login/finish", json=payload)

   def reauth(self, client, sign_count=None):
      """The counter advances on every ceremony, because a stalled counter is refused as a clone."""
      begun = client.post("/auth/reauth/begin", json={})
      assert begun.status_code == 200
      self.sign_count = (sign_count or self.sign_count) + 1
      payload = {
         "challenge_id": begun.json()["challenge_id"],
         "credential": {
            "credential_id": CREDENTIAL_ID.hex(),
            "sign_count": self.sign_count,
         },
      }

      return client.post("/auth/reauth/finish", json=payload)

   def states(self, user_id):
      with OrmSession(self.engine) as db:
         return repository.load_states(db, user_id)
