"""Fixtures for the HTTP layer tests.

The engine graph, the archetypes and the item bank come from tests/fixtures/graph_p1.json through
the same helpers the selection and session-service tests use, so nothing here rebuilds a fixture.
The two hooks the other P1 modules own (skills_state seeding and the purge) are supplied as test
doubles through settings, which is what keeps the HTTP tests off the live library loader. Sign-in is
the real username and password path, hashed under scrypt parameters cheap enough to cost about a
millisecond, with a per-IP limit high enough that no test trips it by accident.
"""
import json
from datetime import date, datetime, timezone

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.api.app import SessionContext, Settings, create_app
from app.auth.guard import DEFAULT_ALLOWED_HOSTS
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
USERNAME = "student_one"
PASSWORD = "correct horse battery"
NEW_PASSWORD = "another long passphrase"
FAST_SCRYPT_N = 2 ** 10
FAST_SCRYPT_R = 8
FAST_SCRYPT_P = 1
UNREACHABLE_RATE_LIMIT = 100_000
TEST_ALLOWED_HOSTS = DEFAULT_ALLOWED_HOSTS + ("testserver",)
ERROR_RECORDS = {
   "BC-ERR-02001": {
      "id": "BC-ERR-02001",
      "observed_behavior": "the common factor is cancelled before the rewrite",
      "scoring_consequence": "the answer point is lost",
   },
}
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
   return build_world(tmp_path)


def build_world(tmp_path):
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
      allowed_hosts=TEST_ALLOWED_HOSTS,
      password_scrypt_n=FAST_SCRYPT_N,
      password_scrypt_r=FAST_SCRYPT_R,
      password_scrypt_p=FAST_SCRYPT_P,
      auth_rate_limit_count=UNREACHABLE_RATE_LIMIT,
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

   def register(self, client, username=USERNAME, password=PASSWORD):
      return client.post("/auth/signup", json={"username": username, "password": password})

   def recover(self, client, code, new_password=NEW_PASSWORD, username=None):
      payload = {"recovery_code": code, "new_password": new_password}
      names_a_username = username is not None

      if names_a_username:
         payload["username"] = username

      return client.post("/auth/recovery/reset", json=payload)

   def login(self, client, username=USERNAME, password=PASSWORD):
      return client.post("/auth/login", json={"username": username, "password": password})

   def reauth(self, client, password=PASSWORD):
      return client.post("/auth/reauth", json={"password": password})

   def states(self, user_id):
      with OrmSession(self.engine) as db:
         return repository.load_states(db, user_id)
