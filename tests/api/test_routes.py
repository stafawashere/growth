"""Route tests for the P1 HTTP layer: the session flow, the purge gate and the liveness rule."""
import json

from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.db import models
from tests.api.conftest import KEY_MATHJSON, SNAPSHOT_ID, TODAY, WRONG_MATHJSON


def correct_answer_for(item):
   """The submission shape the served format demands, carrying the stored key either way."""
   is_mcq = item["format"] == "mcq"

   if is_mcq:
      return {"option_id": "A"}

   return {"mathjson": KEY_MATHJSON}


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
         "answer": correct_answer_for(item),
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
         "answer": correct_answer_for(item),
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


def serve_as_mcq(world, session_id, item_id):
   """Session assembly fixes the format per queue slot, so an MCQ case is set up on the row."""
   with OrmSession(world.engine) as db:
      row = db.get(models.Session, session_id)
      queue = json.loads(row.queue)

      for block, slots in queue.items():
         holds_slots = isinstance(slots, list)

         if not holds_slots:
            continue

         for item in slots:
            is_a_slot = isinstance(item, dict)
            is_target = is_a_slot and item.get("id") == item_id

            if is_target:
               item["format"] = "mcq"

      row.queue = json.dumps(queue)
      db.commit()


def test_feedback_route_returns_the_elaborated_payload(world):
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   serve_as_mcq(world, session_id, item["id"])
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"correct": True, "option_id": "B"},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200
   assert attempted.json()["correct"] is False

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

   client = world.client()
   world.register(client)
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


def wrong_answer_for(item):
   """The submission shape the served format demands, carrying a wrong value either way."""
   is_mcq = item["format"] == "mcq"

   if is_mcq:
      return {"option_id": "B"}

   return {"mathjson": WRONG_MATHJSON}


def test_attempt_is_graded_by_the_server_not_the_body(world):
   """R12 decides correctness from the stored key, so a body that claims a success is ignored."""
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   claimed = wrong_answer_for(item)
   claimed["correct"] = True
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": claimed,
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   )

   assert attempted.status_code == 200
   assert attempted.json()["correct"] is False

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempted.json()["id"])

      assert stored.correct == 0


def test_attempt_refuses_an_item_with_no_items_row(world):
   """Fail closed: nothing grades an item the bank cannot produce a key for."""
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   with OrmSession(world.engine) as db:
      db.delete(db.get(models.Item, item["id"]))
      db.commit()

   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"mathjson": WRONG_MATHJSON},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
      },
   )

   assert attempted.status_code == 409


def test_feedback_is_refused_on_an_ungraded_attempt(world):
   """An ungraded attempt lost no point, so it earns no elaborated feedback and no worked solution."""
   client = world.client()
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"option_id": "B"},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200
   assert attempted.json()["correct"] is None

   feedback = client.get(f"/sessions/{session_id}/attempts/{attempted.json()['id']}/feedback")

   assert feedback.status_code == 409
   assert "worked_solution" not in feedback.text
