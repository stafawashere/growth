"""Route tests for the P1 HTTP layer: the session flow, the purge gate and the liveness rule."""
import json
import re
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.db import models
from tests.api.conftest import KEY_MATHJSON, SNAPSHOT_ID, TODAY, WRONG_MATHJSON, item_row


def correct_answer_for(item):
   """The submission shape the served format demands, carrying the stored key either way."""
   is_mcq = item["format"] == "mcq"

   if is_mcq:
      return {"option_id": "A"}

   return {"mathjson": KEY_MATHJSON}


PRIOR_ATTEMPT_AT = "2026-02-28T09:00:00+00:00"


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
   """Consume one stage-unsupported attempt on the archetype, so R29 serves the next one as MCQ.

   The format is resolved against the user's attempt history when the slot is served and again
   when the attempt is written, so an MCQ case cannot be forced onto the queue row: it has to be
   earned by a prior attempt the alternation counts.

   The prior attempt lands on a sibling published here for the purpose, rather than on whichever
   bank item the draw left out of the queue, because the fixture bank holds three items per
   archetype and a session can queue all three.
   """
   with OrmSession(world.engine) as db:
      row = db.get(models.Session, session_id)
      queue = json.loads(row.queue)
      slot = None

      for slots in queue.values():
         holds_slots = isinstance(slots, list)

         if not holds_slots:
            continue

         for item in slots:
            is_a_slot = isinstance(item, dict)
            is_target = is_a_slot and item.get("id") == item_id

            if is_target:
               slot = item

      if slot is None:
         raise AssertionError(f"{item_id} is not in the queue of session {session_id}")

      queued_ids = {
         item["id"]
         for slots in queue.values()
         if isinstance(slots, list)
         for item in slots
         if isinstance(item, dict)
      }
      archetype = world.settings.session_context.archetypes[slot["archetype_id"]]
      sibling = item_row(f"{item_id}-PRIOR", archetype["id"], archetype["skills"])

      if sibling.id in queued_ids:
         raise AssertionError(f"{sibling.id} is already queued in session {session_id}")

      db.add(sibling)
      sibling_id = sibling.id

      db.add(
         models.Attempt(
            id=f"ATT-PRIOR-{item_id}",
            session_id=session_id,
            item_id=sibling_id,
            started_at=PRIOR_ATTEMPT_AT,
            submitted_at=PRIOR_ATTEMPT_AT,
            response=json.dumps({"form": "symbolic", "mathjson": ["Add", 1, 1]}),
            confidence="confident",
            elapsed_ms=90000,
            correct=1,
            p_split=0.5,
            p_compensatory=0.5,
            served_stage="unsupported",
            format="short_answer",
            per_skill_states=json.dumps({}),
            snapshot_id=row.snapshot_id,
            created_at=PRIOR_ATTEMPT_AT,
            updated_at=PRIOR_ATTEMPT_AT,
         )
      )
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


def keys_anywhere(value):
   """Every mapping key at any depth of a decoded JSON body."""
   found = set()
   is_mapping = isinstance(value, dict)
   is_sequence = isinstance(value, list)

   if is_mapping:
      found.update(value)
      children = list(value.values())
   elif is_sequence:
      children = value
   else:
      children = []

   for child in children:
      found |= keys_anywhere(child)

   return found


PLAN_DIRECTORY = Path(__file__).resolve().parents[2] / "docs" / "plan"
SHOWN_ITEM_PROPERTIES = ("stem", "figure", "options", "metadata")
SHOWN_OPTION_PROPERTIES = ("id", "text")


def plan_item_schema():
   """The GeneratedItem output schema, parsed out of the json block under its heading in 04."""
   plan_text = (PLAN_DIRECTORY / "04-item-generation.md").read_text()
   after_heading = plan_text.split("### Output schema", 1)[1]
   block = after_heading.split("```json", 1)[1].split("```", 1)[0]

   return json.loads(block)


def plan_items_columns():
   """The column names of the items table in 06, read off the first cell of each table row."""
   plan_text = (PLAN_DIRECTORY / "06-architecture.md").read_text()
   section = plan_text.split("### items\n", 1)[1].split("\n### ", 1)[0]
   rows = [line for line in section.splitlines() if line.startswith("| ")]
   cells = [row.split("|")[1].strip() for row in rows]

   return {cell for cell in cells if re.fullmatch(r"[a-z_]+", cell)}


def plan_option_storage_names():
   """R26 in 04: the name a generated option field is written under on items.options."""
   plan_text = (PLAN_DIRECTORY / "04-item-generation.md").read_text()
   written = re.findall(r"emits it as `(\w+)` and it is written straight to `(\w+)`", plan_text)

   return dict(written)


def forbidden_item_names():
   """Every property of 04's item schema a student is not shown, and the name 06 stores it under.

   The student sees the stem, the figure and the options, and metadata is the backend's echo of
   the request; everything else in the schema is the answer. On an option the student sees its id
   and its text, so the key flag, the error path and the rest are the answer too.
   """
   schema = plan_item_schema()
   option_schema = schema["properties"]["options"]["items"]
   hidden_item = set(schema["properties"]) - set(SHOWN_ITEM_PROPERTIES)
   hidden_option = set(option_schema["properties"]) - set(SHOWN_OPTION_PROPERTIES)
   stored_item = {
      column
      for column in plan_items_columns()
      for name in hidden_item
      if column == name or column.endswith(f"_{name}")
   }
   renamed = plan_option_storage_names()
   stored_option = {renamed[name] for name in hidden_option if name in renamed}

   return hidden_item | stored_item, hidden_option | stored_option


def test_next_item_never_carries_the_answer_key(world):
   """The served item travels through sessions.queue to the student, so it must not hold the key.

   It is served at stage completion, where the most of the worked solution is shown. The forbidden
   names come from the plan's item schema and items table, not from the code under test.
   """
   from app.runtime.bank import ItemBank
   from tests.api.test_served_steps import WORKED_STEPS, author_worked_steps, stage_every_skill

   forbidden_item_fields, forbidden_option_fields = forbidden_item_names()

   assert {"key", "answer_key", "worked_solution"} <= forbidden_item_fields
   assert {"is_key", "error_path"} <= forbidden_option_fields

   client = world.client()
   user_id = world.register(client).json()["user"]["id"]
   author_worked_steps(world, WORKED_STEPS)
   stage_every_skill(world, user_id, "completion")
   world.settings.session_context.bank = ItemBank(world.engine)
   opened = open_session(client)

   assert opened.status_code == 200

   served = client.get(f"/sessions/{opened.json()['id']}/next").json()["item"]

   assert served["stage"] == "completion"
   assert len(served["options"]) > 0

   with OrmSession(world.engine) as db:
      stored = db.get(models.Item, served["id"])
      stored_option_fields = {name for option in stored.options for name in option}
      key_value = json.dumps(json.loads(stored.answer_key)["mathjson"])
      key_value_inside_a_string = json.dumps(key_value)[1:-1]
      blanked_text = json.loads(stored.worked_solution)[-1]["text"]

   assert {"is_key", "error_path"} <= stored_option_fields

   for body in (served, opened.json()["queue"]):
      carried_keys = keys_anywhere(body)
      serialised = json.dumps(body)

      assert carried_keys.isdisjoint(forbidden_item_fields)
      assert carried_keys.isdisjoint(forbidden_option_fields)
      assert key_value not in serialised
      assert key_value_inside_a_string not in serialised
      assert blanked_text not in serialised


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


def test_feedback_on_an_ungraded_attempt_carries_no_elaborated_error(world):
   """An ungraded attempt lost no point, so it earns no elaborated feedback and no worked solution,
   and the feedback screen still answers so the student can move on.
   """
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

   assert feedback.status_code == 200
   assert feedback.json()["kind"] == "ungraded"
   assert feedback.json()["elaborated"] is None
   assert "worked_solution" not in feedback.text
