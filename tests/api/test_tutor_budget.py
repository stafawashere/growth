"""The tutor call on the feedback route goes through the budget guard and is cached.

docs/plan/07-ai-provider-layer.md, "Budget caps": the guard runs inside the provider layer, before
the call, and no caller constructs a provider request directly, because the budget guard, the
usage accounting and the audit trail all live at that seam. Until this session the feedback route
called the tutor on every GET with none of the three, which is the defect the sixth session
recorded and deliberately worked around by making the role opt-in.

The tutor's behaviour at its cap is Stop, per 07's hard-stop table, and what the student sees is a
line saying the tutor is unavailable for the rest of today with the practice queue unaffected. The
route carries that as tutor_unavailable, which is the field the session screen will read.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.providers.guard import BudgetCaps
from app.providers.replay import ReplayProvider
from tests.api.conftest import TODAY, WRONG_MATHJSON
from tests.api.test_routes import open_session

CASSETTE = {
   "text": "The factor cancels only after the rewrite, so the answer point is lost.",
   "finish_reason": "end_turn",
   "provider": "anthropic",
   "model": "claude-sonnet-5",
   "usage": {
      "input_tokens": 1200,
      "output_tokens": 40,
      "cached_read_tokens": 0,
      "cached_write_tokens": 0,
   },
}


class CountingProvider(ReplayProvider):
   def __init__(self):
      super().__init__(cassette=CASSETTE)
      self.calls = 0

   def generate(self, request):
      self.calls = self.calls + 1

      return super().generate(request)


def wrong_short_answer(client):
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]
   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"form": "symbolic", "mathjson": WRONG_MATHJSON},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200

   return session_id, attempted.json()["id"]


def budget_rows(engine):
   with OrmSession(engine) as db:
      return db.scalars(select(models.Budget)).all()


def audit_actions(engine):
   with OrmSession(engine) as db:
      return [row.action for row in db.scalars(select(models.AuditLog)).all()]


def test_a_tutor_call_from_the_feedback_route_is_accounted_in_budgets(world):
   world.settings.tutor = CountingProvider()
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200
   assert feedback.json()["sentence"] == CASSETTE["text"]

   rows = budget_rows(world.engine)

   assert len(rows) == 1
   assert rows[0].role == "tutor"
   assert rows[0].tokens_in == 1200
   assert rows[0].tokens_out == 40
   assert rows[0].cost_usd > 0


def test_a_second_feedback_read_spends_no_second_tutor_call(world):
   provider = CountingProvider()
   world.settings.tutor = provider
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   first = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()
   spent_once = budget_rows(world.engine)[0].tokens_in
   second = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert provider.calls == 1
   assert second["sentence"] == first["sentence"]
   assert budget_rows(world.engine)[0].tokens_in == spent_once


def test_a_tutor_at_its_cap_serves_feedback_without_a_sentence(world):
   provider = CountingProvider()
   world.settings.tutor = provider
   world.settings.tutor_caps = {"tutor": BudgetCaps(cap_usd=0.0)}
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   feedback = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert feedback.status_code == 200

   body = feedback.json()

   assert body["sentence"] is None
   assert body["tutor_unavailable"] is True
   assert body["kind"] == "elaborated"
   assert provider.calls == 0
   assert "budget_hard_stop" in audit_actions(world.engine)


def test_an_unconfigured_tutor_leaves_the_payload_available(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback").json()

   assert body["sentence"] is None
   assert body["tutor_unavailable"] is False
   assert budget_rows(world.engine) == []
