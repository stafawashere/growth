"""Route tests for the P1 HTTP layer: the session flow, the purge gate and the liveness rule."""
import json

from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.db import models
from tests.api.conftest import SNAPSHOT_ID, TODAY


def open_session(client):
   return client.post(
      "/sessions",
      json={"mode": "learning", "sub_mode": None, "today": TODAY.isoformat()},
   )


def test_session_routes_open_next_attempt_confidence_close(world):
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200

   user_id = registered.json()["user"]["id"]
   before = world.states(user_id)
   opened = open_session(client)

   assert opened.status_code == 200

   session_id = opened.json()["id"]
   queue = opened.json()["queue"]

   assert len(queue["block2"]) > 0

   fetched = client.get(f"/sessions/{session_id}")

   assert fetched.status_code == 200
   assert fetched.json()["mode"] == "learning"

   served = client.get(f"/sessions/{session_id}/next")

   assert served.status_code == 200

   item = served.json()["item"]
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"correct": True},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   )

   assert attempted.status_code == 200

   attempt_id = attempted.json()["id"]
   rated = client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": "unsure", "today": TODAY.isoformat()},
   )

   assert rated.status_code == 200

   judged = client.post(
      f"/sessions/{session_id}/judgments",
      json={"scope": "archetype", "scope_id": item["archetype_id"], "predicted_retention": 0.6},
   )

   assert judged.status_code == 200

   closed = client.post(f"/sessions/{session_id}/close", json={})

   assert closed.status_code == 200
   assert closed.json()["ended_at"] is not None

   after = world.states(user_id)
   primary = item["archetype_id"]
   moved = [
      skill_id
      for skill_id, state in after.items()
      if state.observation_count != before[skill_id].observation_count
   ]

   assert len(moved) > 0
   assert primary is not None

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempt_id)

      assert stored.confidence == "unsure"
      assert stored.snapshot_id == SNAPSHOT_ID
      assert db.query(models.Judgment).count() == 1


def test_session_routes_require_the_cookie(world):
   client = world.client()
   world.register(client)
   client.cookies.clear()

   assert open_session(client).status_code == 401
   assert client.get("/me").status_code == 401


def test_purge_requires_reauth(world):
   client = world.client()
   registered = world.register(client)
   user_id = registered.json()["user"]["id"]

   assert len(world.states(user_id)) > 0

   unauthenticated = client.post("/purge", json={"confirmation": PURGE_CONFIRMATION})

   assert 400 <= unauthenticated.status_code < 500
   assert world.purges.calls == []
   assert len(world.states(user_id)) > 0

   token = world.reauth(client).json()["reauth_token"]
   unconfirmed = client.post("/purge", json={"reauth_token": token})

   assert 400 <= unconfirmed.status_code < 500
   assert world.purges.calls == []
   assert len(world.states(user_id)) > 0

   purged = client.post(
      "/purge",
      json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token},
   )

   assert purged.status_code == 200
   assert world.purges.calls == [user_id]
   assert purged.json()["deleted"]["skills_state"] > 0
   assert len(world.states(user_id)) == 0


def test_healthz_localhost_only(world):
   assert world.client().get("/healthz").status_code == 200
   assert world.client(host="203.0.113.7").get("/healthz").status_code == 403


def test_content_snapshot_route_reports_the_active_row(world):
   client = world.client()
   world.register(client)
   fetched = client.get("/content/snapshot")

   assert fetched.status_code == 200
   assert fetched.json()["id"] == SNAPSHOT_ID
   assert fetched.json()["digest"] == "digest-0001"


def test_me_reports_exam_and_purge_dates(world):
   client = world.client()
   world.register(client)
   fetched = client.get("/me")

   assert fetched.status_code == 200
   assert fetched.json()["exam_date"] == "2027-05-10"
   assert fetched.json()["purge_after"] == "2027-06-09"


def test_close_route_applies_unrated_attempts(world):
   client = world.client()
   registered = world.register(client)
   user_id = registered.json()["user"]["id"]
   before = world.states(user_id)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"correct": True},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   )
   attempt_id = attempted.json()["id"]
   closed = client.post(f"/sessions/{session_id}/close", json={"today": TODAY.isoformat()})

   assert closed.status_code == 200

   after = world.states(user_id)
   moved = [
      skill_id
      for skill_id, state in after.items()
      if state.observation_count != before[skill_id].observation_count
   ]

   assert len(moved) > 0

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempt_id)

      assert stored.confidence == "unsure"


def test_judgment_route_validates_scope_id_and_retention(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   wrong_scope = client.post(
      f"/sessions/{session_id}/judgments",
      json={"scope": "skill", "scope_id": item["archetype_id"], "predicted_retention": 0.6},
   )

   assert wrong_scope.status_code == 400

   out_of_range = client.post(
      f"/sessions/{session_id}/judgments",
      json={"scope": "archetype", "scope_id": item["archetype_id"], "predicted_retention": 1.5},
   )

   assert out_of_range.status_code == 400

   accepted = client.post(
      f"/sessions/{session_id}/judgments",
      json={"scope": "archetype", "scope_id": item["archetype_id"], "predicted_retention": 0.6},
   )

   assert accepted.status_code == 200
   assert accepted.json()["id"].startswith("JDG")


def test_register_finish_seeds_from_the_resolved_snapshot(world, monkeypatch):
   import app.content.loader as loader

   sentinel = object()
   monkeypatch.setattr(loader, "load_snapshot", lambda root: sentinel)
   world.settings.snapshot = None
   world.settings.content_root = "unused"
   client = world.client()
   world.register(client)

   assert world.seeds.snapshots == [sentinel]


def publish_item(world, item_id, archetype_id):
   """The feedback route reads the items row, which the fixture bank does not carry."""
   options = [
      {"id": "A", "error_path": None},
      {"id": "B", "error_path": "BC-ERR-02001", "violated_step": 1},
   ]

   with OrmSession(world.engine) as db:
      db.add(
         models.Item(
            id=item_id,
            archetype_id=archetype_id,
            variant_id=None,
            snapshot_id=SNAPSHOT_ID,
            parameter_draw="{}",
            stem="stem",
            figure_spec=None,
            options=options,
            answer_key="key",
            worked_solution="divide out the factor, then evaluate",
            calculator_status="no_calculator",
            representation="BC-REP-01",
            difficulty_settings="{}",
            skills="[]",
            provenance="{}",
            status="verified",
            dedupe_minhash="[]",
            created_at=TODAY.isoformat(),
            updated_at=TODAY.isoformat(),
         )
      )
      db.commit()


def test_feedback_route_returns_the_elaborated_payload(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   publish_item(world, item["id"], item["archetype_id"])
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"correct": False, "option_id": "B"},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200

   attempt_id = attempted.json()["id"]
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["kind"] == "elaborated"
   assert body["elaborated"]["error_id"] == "BC-ERR-02001"
   assert body["elaborated"]["scoring_consequence"] == "the answer point is lost"
   assert body["elaborated"]["violated_step"]
   assert body["self_explanation_prompt"].startswith("which rule justifies step 2")
   assert "answer_key" not in body["elaborated"]


def test_feedback_route_refuses_an_unknown_attempt(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   missing = client.get(f"/sessions/{session_id}/attempts/ATT-nope/feedback")

   assert missing.status_code == 404


def test_register_finish_returns_a_recovery_code_once(world):
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200

   code = registered.json()["recovery_code"]

   assert isinstance(code, str) and len(code) > 0

   user_id = registered.json()["user"]["id"]

   with OrmSession(world.engine) as db:
      stored = db.get(models.User, user_id).recovery_code_hash

   assert stored is not None
   assert code not in stored


def test_registration_with_a_valid_recovery_code_adds_a_credential(world):
   """The ordinary ceremony stays closed after the first user, so recovery has its own path."""
   client = world.client()
   code = world.register(client).json()["recovery_code"]
   refused = world.recover(client, "WRONG-CODE-HERE-XXXXX", credential_id="aa" * 8)

   assert refused.status_code == 401

   recovered = world.recover(client, code, credential_id="aa" * 8)

   assert recovered.status_code == 200

   with OrmSession(world.engine) as db:
      credentials = db.query(models.PasskeyCredential).count()

   assert credentials == 2

   replayed = world.recover(client, code, credential_id="bb" * 8)

   assert replayed.status_code == 401


def test_next_item_never_carries_the_answer_key(world):
   """The served item travels through sessions.queue to the student, so it must not hold the key."""
   from app.runtime.bank import ItemBank
   from tests.engine.conftest_selection import load_fixture

   client = world.client()
   world.register(client)

   for record in load_fixture()["archetypes"]:
      publish_item(world, f"{record['id']}-PUB", record["id"])

   world.settings.session_context.bank = ItemBank(world.engine)
   opened = open_session(client)

   assert opened.status_code == 200

   served = client.get(f"/sessions/{opened.json()['id']}/next").json()["item"]

   assert "answer_key" not in served
   assert "worked_solution" not in served

   for option in served["options"]:
      assert "error_path" not in option

   queued = opened.json()["queue"]

   assert "answer_key" not in json.dumps(queued)
