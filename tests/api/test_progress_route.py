"""GET /progress, the due counts home reads (06's API surface, P1 serves the due counts only)."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session as OrmSession

from starlette.testclient import TestClient

from app.db import models
from tests.api.conftest import TODAY

DECLARED_FIELDS = {
   "skills_due_for_review": int,
   "frontier_skills": int,
   "corrected_items_returning": int,
   "forecast_minutes": (int, float),
   "session_in_progress": (str, type(None)),
}


def row_counts(engine):
   with OrmSession(engine) as db:
      return {
         table.name: db.scalar(select(func.count()).select_from(table))
         for table in models.Base.metadata.sorted_tables
      }


def test_progress_refuses_a_request_without_a_session_cookie(world):
   client = world.client()

   assert client.get("/progress").status_code == 401


def test_progress_returns_the_declared_fields_writes_nothing_and_repeats(world):
   client = world.client()
   world.register(client)
   before = row_counts(world.engine)
   first = client.get("/progress")
   second = client.get("/progress")
   after = row_counts(world.engine)

   assert first.status_code == 200
   assert set(first.json()) == set(DECLARED_FIELDS)

   for name, expected_type in DECLARED_FIELDS.items():
      assert isinstance(first.json()[name], expected_type), name

   assert first.json()["frontier_skills"] > 0
   assert first.json()["forecast_minutes"] > 0
   assert first.json() == second.json()
   assert before["skills_state"] > 0
   assert after == before


def test_progress_names_the_open_session_until_it_is_closed(world):
   client = world.client()
   world.register(client)
   opened = client.post("/sessions", json={"mode": "learning", "today": TODAY.isoformat()})
   session_id = opened.json()["id"]
   while_open = client.get("/progress").json()["session_in_progress"]
   closed = client.post(f"/sessions/{session_id}/close", json={"today": TODAY.isoformat()})
   after_close = client.get("/progress").json()["session_in_progress"]

   assert opened.status_code == 200
   assert closed.status_code == 200
   assert while_open == session_id
   assert after_close is None

def served_blocks(queue):
   return {block: [item["id"] for item in queue[block]] for block in ("block1", "block2", "block3")}


def spy_on_the_preview_assembly(monkeypatch):
   """The assembled Session GET /progress counted, recorded as it passes through unchanged."""
   from app.session import preview

   assembled = []
   original = preview.assemble_session

   def recording_assembly(*args, **kwargs):
      session = original(*args, **kwargs)
      assembled.append(session)

      return session

   monkeypatch.setattr(preview, "assemble_session", recording_assembly)

   return assembled


def previewed_then_opened(world, monkeypatch, progress_path, open_body):
   client = world.client()
   world.register(client)
   assembled = spy_on_the_preview_assembly(monkeypatch)
   previewed = client.get(progress_path)
   opened = client.post("/sessions", json=open_body)

   assert previewed.status_code == 200
   assert opened.status_code == 200
   assert len(assembled) == 1

   session = assembled[0]
   predicted = {"block1": session.block1, "block2": session.block2, "block3": session.block3}

   return served_blocks(predicted), served_blocks(opened.json()["queue"]), previewed.json(), opened.json()


def test_progress_predicts_the_queue_post_sessions_assembles(world, monkeypatch):
   predicted, opened, previewed, _ = previewed_then_opened(
      world, monkeypatch, "/progress", {"mode": "learning"}
   )

   assert len(opened["block2"]) > 0
   assert predicted == opened


def test_progress_and_post_sessions_read_the_same_requested_day(world, monkeypatch):
   predicted, opened, previewed, body = previewed_then_opened(
      world,
      monkeypatch,
      f"/progress?today={TODAY.isoformat()}",
      {"mode": "learning", "today": TODAY.isoformat()},
   )
   served = [item for block in ("block1", "block2", "block3") for item in body["queue"][block]]
   forecast = sum(body["queue"]["forecasts"][item["archetype_id"]] for item in served)

   assert predicted == opened
   assert previewed["forecast_minutes"] == forecast


def test_the_preview_and_the_session_both_draw_from_the_signed_in_users_rng(world, monkeypatch):
   from app.session import preview

   seeded_user_ids = []
   real_user_assembly_inputs = preview.user_assembly_inputs

   def recording_user_assembly_inputs(process_seed, user_id, requested_day):
      seeded_user_ids.append(user_id)

      return real_user_assembly_inputs(process_seed, user_id, requested_day)

   monkeypatch.setattr(preview, "user_assembly_inputs", recording_user_assembly_inputs)
   client = world.client()
   world.register(client)
   user_id = client.get("/me").json()["id"]

   assert client.get("/progress", params={"today": TODAY.isoformat()}).status_code == 200
   assert client.post("/sessions", json={"mode": "learning", "today": TODAY.isoformat()}).status_code in (200, 201)
   assert seeded_user_ids == [user_id, user_id]


UNREADABLE_DAY = "not-a-date"


def answering_client(world):
   """A client that reports a server error as a status, so a 500 fails on the status assertion."""
   return TestClient(
      world.app,
      client=("127.0.0.1", 40000),
      base_url="http://127.0.0.1",
      raise_server_exceptions=False,
   )


def test_progress_refuses_an_unreadable_day_and_writes_nothing(world):
   client = answering_client(world)
   world.register(client)
   before = row_counts(world.engine)

   refused = client.get("/progress", params={"today": UNREADABLE_DAY})

   assert refused.status_code == 422
   assert row_counts(world.engine) == before


def test_post_sessions_refuses_an_unreadable_day_and_writes_nothing(world):
   client = answering_client(world)
   world.register(client)
   before = row_counts(world.engine)

   refused = client.post("/sessions", json={"mode": "learning", "today": UNREADABLE_DAY})

   assert refused.status_code == 422
   assert row_counts(world.engine) == before
