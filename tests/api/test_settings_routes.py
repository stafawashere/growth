"""GET and PUT /settings, GET /settings/providers, GET and PUT /settings/budgets, per 06's API surface.

Every write is checked by reading the column back out of the database, never by the response
echoing the request.
"""
import json

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession
from starlette.testclient import TestClient

from app.db import models
from app.engine import constants
from app.feedback import tutor as tutor_module
from app.feedback.tutor import MAX_OUTPUT_TOKENS, TUTOR_MODEL
from app.providers.guard import ROLES, price_for
from tests.api.conftest import TODAY, TUTOR_CAP_USD
from tests.api.test_routes import wrong_answer_for
from tests.api.test_tutor_budget import CountingProvider, budget_rows, wrong_short_answer

PROVIDER_FIELDS = {"role", "provider", "model", "wired"}


def user_row(engine, user_id):
   with OrmSession(engine) as db:
      return db.get(models.User, user_id)


def cap_changes(engine):
   with OrmSession(engine) as db:
      statement = (
         select(models.AuditLog)
         .where(models.AuditLog.action == "budget_cap_changed")
         .order_by(models.AuditLog.at)
      )

      return db.scalars(statement).all()


def registered_user_id(world, client):
   return world.register(client).json()["user"]["id"]


def second_wrong_answer(client, session_id):
   """A graded wrong answer on whatever comes next, which is what reaches the tutor.

   The fixture seeds every unmastered skill at stage unsupported, so the next item is served
   there, but R29 alternates its format per archetype and the draw decides whether the archetype
   was already attempted in this session. The answer is therefore shaped for the served format,
   so an expression is never sent to an item served as MCQ and left ungraded.
   """
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert item["stage"] == "unsupported"

   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": wrong_answer_for(item),
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200
   assert attempted.json()["correct"] is False

   return attempted.json()["id"]


def test_get_settings_reads_the_user_row_and_the_engines_retention(world, monkeypatch):
   monkeypatch.setattr(constants, "desired_retention", lambda today: 0.42)
   client = world.client()
   user_id = registered_user_id(world, client)
   stored = user_row(world.engine, user_id)
   body = client.get("/settings").json()

   assert body == {
      "exam_date": stored.exam_date,
      "purge_after": stored.purge_after,
      "desired_retention": 0.42,
   }


def test_put_settings_writes_both_dates_to_the_user_row(world):
   client = world.client()
   user_id = registered_user_id(world, client)
   updated = client.put("/settings", json={"exam_date": "2028-05-08", "purge_after": "2028-06-30"})
   stored = user_row(world.engine, user_id)

   assert updated.status_code == 200
   assert stored.exam_date == "2028-05-08"
   assert stored.purge_after == "2028-06-30"
   assert updated.json()["exam_date"] == stored.exam_date
   assert updated.json()["purge_after"] == stored.purge_after


def test_a_changed_exam_date_leaves_purge_after_where_it_was(world):
   client = world.client()
   user_id = registered_user_id(world, client)
   purge_after_before = user_row(world.engine, user_id).purge_after
   updated = client.put("/settings", json={"exam_date": "2028-05-08"})
   stored = user_row(world.engine, user_id)

   assert updated.status_code == 200
   assert stored.exam_date == "2028-05-08"
   assert stored.purge_after == purge_after_before


def test_put_settings_refuses_what_it_cannot_store(world):
   client = world.client()
   user_id = registered_user_id(world, client)
   before = user_row(world.engine, user_id)
   refused_bodies = (
      {"exam_date": "10 May 2027"},
      {"purge_after": "20270510"},
      {"exam_date": None},
      {"desired_retention": 0.5},
      {},
   )

   for refused_body in refused_bodies:
      assert client.put("/settings", json=refused_body).status_code == 400

   after = user_row(world.engine, user_id)

   assert (after.exam_date, after.purge_after) == (before.exam_date, before.purge_after)


def test_providers_lists_the_six_roles_and_only_the_wired_tutor(world):
   world.settings.tutor = CountingProvider()
   client = world.client()
   world.register(client)
   roles = client.get("/settings/providers").json()["roles"]
   by_role = {entry["role"]: entry for entry in roles}

   assert tuple(entry["role"] for entry in roles) == ROLES
   assert all(set(entry) == PROVIDER_FIELDS for entry in roles)
   assert by_role["tutor"] == {"role": "tutor", "provider": "replay", "model": TUTOR_MODEL, "wired": True}

   for role in ROLES[1:]:
      assert by_role[role] == {"role": role, "provider": None, "model": None, "wired": False}


def test_providers_reports_an_unset_tutor_as_unwired(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   roles = client.get("/settings/providers").json()["roles"]
   tutor = next(entry for entry in roles if entry["role"] == "tutor")

   assert tutor == {"role": "tutor", "provider": None, "model": None, "wired": False}


def test_get_budgets_reads_todays_usage_and_the_cap_in_force(world):
   world.settings.tutor = CountingProvider()
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")
   stored = budget_rows(world.engine)[0]
   body = client.get("/settings/budgets").json()
   by_role = {entry["role"]: entry for entry in body["roles"]}

   assert tuple(by_role) == ROLES
   assert body["day"] == stored.day
   assert by_role["tutor"]["cap_usd"] == TUTOR_CAP_USD
   assert by_role["tutor"]["cost_usd"] == stored.cost_usd
   assert by_role["tutor"]["tokens_in"] == stored.tokens_in
   assert by_role["tutor"]["tokens_out"] == stored.tokens_out
   assert by_role["tutor"]["hard_stopped"] is False
   assert by_role["grader"]["cap_usd"] is None
   assert by_role["grader"]["cost_usd"] == 0
   assert body["month_to_date_usd"] == stored.cost_usd


def test_put_budgets_without_a_fresh_reauth_changes_nothing(world):
   client = world.client()
   world.register(client)
   stale = client.put("/settings/budgets", json={"role": "tutor", "cap_usd": 0.5, "cap_tokens": None})
   forged = client.put(
      "/settings/budgets",
      json={"role": "tutor", "cap_usd": 0.5, "cap_tokens": None, "reauth_token": "not-a-token"},
   )

   assert stale.status_code == 401
   assert forged.status_code == 401
   assert cap_changes(world.engine) == []
   assert budget_rows(world.engine) == []


def test_put_budgets_writes_the_cap_and_the_audit_entry(world):
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]
   changed = client.put(
      "/settings/budgets",
      json={"role": "tutor", "cap_usd": 0.5, "cap_tokens": 20000, "reauth_token": token},
   )
   rows = budget_rows(world.engine)
   entries = cap_changes(world.engine)

   assert changed.status_code == 200
   assert len(rows) == 1
   assert (rows[0].role, rows[0].cap_usd, rows[0].cap_tokens) == ("tutor", 0.5, 20000)
   assert len(entries) == 1
   assert entries[0].subject == f"budgets:{rows[0].id}"
   assert json.loads(entries[0].detail) == {
      "role": "tutor",
      "before": {"cap_usd": TUTOR_CAP_USD, "cap_tokens": None},
      "after": {"cap_usd": 0.5, "cap_tokens": 20000},
   }

   tutor = next(entry for entry in changed.json()["roles"] if entry["role"] == "tutor")

   assert (tutor["cap_usd"], tutor["cap_tokens"]) == (rows[0].cap_usd, rows[0].cap_tokens)


def test_put_budgets_refuses_a_role_outside_the_six_and_a_role_with_no_cap(world):
   client = world.client()
   world.register(client)

   refused_bodies = (
      {"role": "classifier", "cap_usd": 1.0},
      {"role": "tutor", "cap_usd": None, "cap_tokens": None},
      {"role": "tutor"},
   )

   for refused_body in refused_bodies:
      token = world.reauth(client).json()["reauth_token"]
      refused = client.put("/settings/budgets", json=dict(refused_body, reauth_token=token))

      assert refused.status_code == 400

   assert cap_changes(world.engine) == []


def put_cap(world, client, change):
   token = world.reauth(client).json()["reauth_token"]

   return client.put("/settings/budgets", json=dict(change, reauth_token=token))


def test_put_budgets_twice_keeps_the_second_cap_and_records_both(world):
   client = world.client()
   world.register(client)

   assert put_cap(world, client, {"role": "tutor", "cap_usd": 0.5}).status_code == 200
   assert put_cap(world, client, {"role": "tutor", "cap_usd": 0.25}).status_code == 200

   rows = budget_rows(world.engine)
   details = [json.loads(entry.detail) for entry in cap_changes(world.engine)]

   assert [row.cap_usd for row in rows] == [0.25]
   assert [detail["before"]["cap_usd"] for detail in details] == [TUTOR_CAP_USD, 0.5]
   assert [detail["after"]["cap_usd"] for detail in details] == [0.5, 0.25]


def test_put_budgets_naming_one_unit_keeps_the_other_units_value(world):
   client = world.client()
   world.register(client)

   assert put_cap(world, client, {"role": "tutor", "cap_tokens": 5000}).status_code == 200

   row = budget_rows(world.engine)[0]

   assert (row.cap_usd, row.cap_tokens) == (TUTOR_CAP_USD, 5000)

   assert put_cap(world, client, {"role": "tutor", "cap_usd": 0.5}).status_code == 200

   row = budget_rows(world.engine)[0]

   assert (row.cap_usd, row.cap_tokens) == (0.5, 5000)


def test_a_cap_set_below_todays_spend_refuses_the_next_tutor_call(world):
   provider = CountingProvider()
   world.settings.tutor = provider
   client = world.client()
   world.register(client)
   session_id, first_attempt = wrong_short_answer(client)
   client.get(f"/sessions/{session_id}/attempts/{first_attempt}/feedback")
   spent_today = budget_rows(world.engine)[0].cost_usd
   token = world.reauth(client).json()["reauth_token"]
   changed = client.put(
      "/settings/budgets",
      json={"role": "tutor", "cap_usd": spent_today / 2, "cap_tokens": None, "reauth_token": token},
   )

   assert changed.status_code == 200
   assert budget_rows(world.engine)[0].cap_usd == spent_today / 2
   assert provider.calls == 1

   second_attempt = second_wrong_answer(client, session_id)
   feedback = client.get(f"/sessions/{session_id}/attempts/{second_attempt}/feedback").json()

   assert feedback["tutor_unavailable"] is True
   assert provider.calls == 1
   assert budget_rows(world.engine)[0].hard_stopped == 1

WORST_CASE_OUTPUT_USD = (MAX_OUTPUT_TOKENS / 1_000_000) * price_for(TUTOR_MODEL).output_usd_per_mtok
STOPPING_MARGIN_USD = WORST_CASE_OUTPUT_USD / 2


def stopped_by_a_cap_just_above_the_spend(world, client, provider):
   """One tutor call spends, then a cap a little above that spend stops the role on the next
   attempt's feedback, because the worst-case estimate of 600 output tokens crosses it."""
   session_id, first_attempt = wrong_short_answer(client)
   client.get(f"/sessions/{session_id}/attempts/{first_attempt}/feedback")
   spent_today = budget_rows(world.engine)[0].cost_usd
   stopping_cap = spent_today + STOPPING_MARGIN_USD

   assert put_cap(world, client, {"role": "tutor", "cap_usd": stopping_cap}).status_code == 200

   second_attempt = second_wrong_answer(client, session_id)
   feedback = client.get(f"/sessions/{session_id}/attempts/{second_attempt}/feedback").json()
   row = budget_rows(world.engine)[0]

   assert feedback["tutor_unavailable"] is True
   assert provider.calls == 1
   assert (row.hard_stopped, row.stopped_by) == (1, "usd")

   return session_id, spent_today, stopping_cap


def test_a_cap_lowered_after_a_stop_but_still_above_the_spend_keeps_the_role_stopped(world, monkeypatch):
   provider = CountingProvider()
   world.settings.tutor = provider
   client = world.client()
   world.register(client)
   session_id, spent_today, stopping_cap = stopped_by_a_cap_just_above_the_spend(world, client, provider)
   lowered_cap = spent_today + STOPPING_MARGIN_USD * 0.8

   assert put_cap(world, client, {"role": "tutor", "cap_usd": lowered_cap}).status_code == 200

   row = budget_rows(world.engine)[0]

   assert row.cap_usd == lowered_cap < stopping_cap
   assert row.cost_usd < lowered_cap
   assert (row.hard_stopped, row.stopped_by) == (1, "usd")

   monkeypatch.setattr(tutor_module, "MAX_OUTPUT_TOKENS", 1)
   third_attempt = second_wrong_answer(client, session_id)
   feedback = client.get(f"/sessions/{session_id}/attempts/{third_attempt}/feedback").json()

   assert feedback["tutor_unavailable"] is True
   assert provider.calls == 1
   assert budget_rows(world.engine)[0].hard_stopped == 1


def test_a_cap_raised_above_the_spend_after_a_stop_clears_the_stop_and_its_cause(world):
   provider = CountingProvider()
   world.settings.tutor = provider
   client = world.client()
   world.register(client)
   stopped_by_a_cap_just_above_the_spend(world, client, provider)

   assert put_cap(world, client, {"role": "tutor", "cap_usd": TUTOR_CAP_USD}).status_code == 200

   row = budget_rows(world.engine)[0]

   assert (row.hard_stopped, row.stopped_by) == (0, None)


def test_put_budgets_refuses_a_cap_that_is_not_a_finite_number(world):
   """The JSON parser behind the route accepts NaN and Infinity. An infinite cap is no cap at all
   and would pass the rule that a role needs one, and NaN would be stored as no cap and written
   into the audit detail as a token no JSON reader accepts. A server error is answered rather than
   raised, so a cap the route took shows up as a status and as rows, not as a traceback."""
   client = TestClient(
      world.app,
      client=("127.0.0.1", 40000),
      base_url="http://127.0.0.1",
      raise_server_exceptions=False,
   )
   world.register(client)

   refused_bodies = (
      '"cap_usd": Infinity, "cap_tokens": null',
      '"cap_usd": NaN',
      '"cap_tokens": Infinity',
      '"cap_tokens": NaN, "cap_usd": 1.0',
      '"cap_usd": -Infinity',
   )

   for refused_body in refused_bodies:
      token = world.reauth(client).json()["reauth_token"]
      raw_body = f'{{"role": "tutor", {refused_body}, "reauth_token": "{token}"}}'
      refused = client.put(
         "/settings/budgets",
         content=raw_body,
         headers={"content-type": "application/json"},
      )

      assert refused.status_code == 400, refused_body

   assert budget_rows(world.engine) == []
   assert cap_changes(world.engine) == []
