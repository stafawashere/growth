"""docs/plan/07-ai-provider-layer.md, "Budget caps", and docs/plan/09-security-and-privacy.md, "Audit log".

The money is already spent by the time _settle runs, so a result the guard cannot read leaves the
reservation at the worst case and nothing anywhere saying why. These tests pin the audit row that
records it, and read the row back out of the database rather than off a return value.
"""
import json
from datetime import datetime, timezone

import pytest
from sqlalchemy import select

from app.db import models
from app.providers.base import Message, ProviderResult, Usage
from app.providers.guard import BudgetCaps, GuardedProvider, UNREADABLE_RESULT_ACTION
from tests.providers.test_guard import (
   DEFAULT_TEST_CAPS,
   EXPECTED_ESTIMATE_USD,
   EXPECTED_PROMPT_TOKENS,
   MAX_OUTPUT_TOKENS,
   SYSTEM_TEXT,
   FakeClock,
   StubProvider,
   _budget_rows,
   _db,
   _guard,
   _request,
)

ROLES_UNDER_TEST = ("tutor", "grader")


def _unreadable_result():
   """usage is None, so the reconciliation raises AttributeError reading the usage block."""
   return ProviderResult(
      text="ok",
      finish_reason="end_turn",
      usage=None,
      provider="anthropic",
      model="claude-sonnet-5",
   )


def _readable_result():
   return ProviderResult(
      text="ok",
      finish_reason="end_turn",
      usage=Usage(input_tokens=50, output_tokens=20, cached_read_tokens=0, cached_write_tokens=0),
      provider="anthropic",
      model="claude-sonnet-5",
   )


def _multi_role_guard(db, double, clock=None):
   return GuardedProvider(
      double,
      db,
      user_id="USR-1",
      clock=clock or FakeClock(datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc)),
      caps={role: DEFAULT_TEST_CAPS for role in ROLES_UNDER_TEST},
      provider_name="anthropic",
   )


def _unreadable_rows(db):
   statement = select(models.AuditLog).where(models.AuditLog.action == UNREADABLE_RESULT_ACTION)

   return list(db.execute(statement).scalars().all())


def test_an_unreadable_result_writes_an_audit_entry():
   db = _db()
   guard = _guard(db, StubProvider(_unreadable_result()))

   guard.generate(_request())

   rows = _unreadable_rows(db)

   assert len(rows) == 1
   assert rows[0].actor == "USR-1"
   assert rows[0].subject == f"budgets:{_budget_rows(db)[0].id}"
   assert rows[0].at.startswith("2026-09-20T10:00")


def test_the_unreadable_entry_names_the_role_and_the_exception_type():
   db = _db()
   guard = _guard(db, StubProvider(_unreadable_result()))

   guard.generate(_request())

   detail = json.loads(_unreadable_rows(db)[0].detail)

   assert detail == {"role": "tutor", "model": "claude-sonnet-5", "exception": "AttributeError"}


def test_a_second_unreadable_result_the_same_day_writes_no_second_row():
   db = _db()
   guard = _guard(db, StubProvider(_unreadable_result()))

   guard.generate(_request())
   guard.generate(_request())
   guard.generate(_request())

   assert len(_unreadable_rows(db)) == 1


def test_an_unreadable_result_for_another_role_still_writes_a_row():
   db = _db()
   guard = _multi_role_guard(db, StubProvider(_unreadable_result()))

   guard.generate(_request(role="tutor"))
   guard.generate(_request(role="grader"))

   roles = sorted(json.loads(row.detail)["role"] for row in _unreadable_rows(db))

   assert roles == ["grader", "tutor"]


def test_an_unreadable_result_keeps_the_worst_case_reservation():
   db = _db()
   guard = _guard(db, StubProvider(_unreadable_result()))

   guard.generate(_request())
   guard.generate(_request())

   row = _budget_rows(db)[0]

   assert row.tokens_in == 2 * EXPECTED_PROMPT_TOKENS
   assert row.tokens_out == 2 * MAX_OUTPUT_TOKENS
   assert row.cost_usd == pytest.approx(2 * EXPECTED_ESTIMATE_USD)


def test_the_unreadable_detail_carries_no_key_material():
   secret_key = "sk-ant-api03-DO-NOT-LOG-THIS"
   student_text = "I think the integral diverges because of the endpoint"
   db = _db()
   guard = _guard(db, StubProvider(_unreadable_result()))

   guard.generate(
      _request(
         system=SYSTEM_TEXT + secret_key,
         messages=(Message(role="user", content=student_text),),
         provider_options={"api_key": secret_key},
      )
   )

   row = _unreadable_rows(db)[0]
   detail = json.loads(row.detail)
   recorded_text = f"{row.subject} {row.detail}"

   assert set(detail) == {"role", "model", "exception"}
   assert secret_key not in recorded_text
   assert student_text not in recorded_text
   assert "ok" not in detail.values()


def test_a_readable_result_writes_no_unreadable_entry():
   db = _db()
   guard = _guard(db, StubProvider(_readable_result()))

   guard.generate(_request())

   assert _unreadable_rows(db) == []
   assert _budget_rows(db)[0].tokens_in == 50