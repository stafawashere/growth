"""A cap changed from settings binds on the very next guarded call.

docs/plan/06-architecture.md's API surface gives PUT /settings/budgets the trigger "budget guard
reload", and 07 stores the caps in budgets. The guard reads the cap from today's row on every call,
a new day's row carries the latest earlier row's caps forward, and the environment only seeds a
role that has no row at all.
"""
import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.providers.guard import ROLES, BudgetCaps, BudgetStopped
from app.providers.replay import ReplayProvider
from app.settings import budgets as budget_settings
from tests.providers.test_guard import (
   FakeClock,
   RecordingProvider,
   _budget_rows,
   _cassette,
   _db,
   _guard,
   _request,
)

PLAN_ROOT = Path(__file__).resolve().parents[2] / "docs" / "plan"
USER_ID = "USR-1"
MORNING = datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc)
ENVIRONMENT_CAPS = BudgetCaps(cap_tokens=None, cap_usd=1.0)


def roles_named_by_the_budgets_table():
   text = (PLAN_ROOT / "06-architecture.md").read_text()
   budgets_section = text.split("### budgets", 1)[1].split("###", 1)[0]
   role_line = next(line for line in budgets_section.splitlines() if line.startswith("| role |"))
   listed = role_line.strip("|").split("|")[2]

   return tuple(name.strip() for name in listed.split(","))


def roles_named_by_the_provider_layer():
   text = (PLAN_ROOT / "07-ai-provider-layer.md").read_text()
   sentence = re.search(r"Six roles, and only six: ([a-z, ]+)\.", text).group(1)

   return tuple(name.strip() for name in sentence.split(","))


def test_the_role_vocabulary_is_the_plans_six_roles():
   assert ROLES == roles_named_by_the_budgets_table()
   assert ROLES == roles_named_by_the_provider_layer()


def test_a_cap_lowered_below_todays_spend_refuses_the_next_call():
   db = _db()
   clock = FakeClock(MORNING)
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   _guard(db, double, caps=ENVIRONMENT_CAPS, clock=clock).generate(_request())
   spent_today = _budget_rows(db)[0].cost_usd

   budget_settings.change_cap(
      db,
      USER_ID,
      "tutor",
      {"cap_usd": spent_today / 2},
      configured={"tutor": ENVIRONMENT_CAPS},
      now=clock(),
   )

   with pytest.raises(BudgetStopped) as stopped:
      _guard(db, double, caps=ENVIRONMENT_CAPS, clock=clock).generate(_request())

   assert stopped.value.cap == "usd"
   assert double.calls == 1
   assert _budget_rows(db)[0].cap_usd == pytest.approx(spent_today / 2)


def test_a_cap_raised_after_a_hard_stop_lets_the_next_call_through():
   db = _db()
   clock = FakeClock(MORNING)
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   stopped_at_zero = BudgetCaps(cap_tokens=None, cap_usd=0.0)

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=stopped_at_zero, clock=clock).generate(_request())

   assert _budget_rows(db)[0].hard_stopped == 1

   budget_settings.change_cap(
      db,
      USER_ID,
      "tutor",
      {"cap_usd": 1.0},
      configured={"tutor": stopped_at_zero},
      now=clock(),
   )

   _guard(db, double, caps=stopped_at_zero, clock=clock).generate(_request())

   assert double.calls == 1
   assert _budget_rows(db)[0].hard_stopped == 0


def test_a_changed_cap_seeds_tomorrows_row_instead_of_the_environment():
   db = _db()
   clock = FakeClock(MORNING)
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))

   budget_settings.change_cap(
      db,
      USER_ID,
      "tutor",
      {"cap_usd": 0.0},
      configured={"tutor": ENVIRONMENT_CAPS},
      now=clock(),
   )
   clock.advance_days(1)

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=ENVIRONMENT_CAPS, clock=clock).generate(_request())

   tomorrow = [row for row in _budget_rows(db) if row.day == clock().date().isoformat()]

   assert double.calls == 0
   assert len(tomorrow) == 1
   assert tomorrow[0].cap_usd == 0.0


def test_the_second_of_two_changes_on_one_day_is_the_one_that_binds():
   db = _db()
   clock = FakeClock(MORNING)
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   configured = {"tutor": ENVIRONMENT_CAPS}

   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_usd": 1.0}, configured=configured, now=clock())
   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_usd": 0.0}, configured=configured, now=clock())

   with pytest.raises(BudgetStopped):
      _guard(db, double, caps=ENVIRONMENT_CAPS, clock=clock).generate(_request())

   assert double.calls == 0
   assert [row.cap_usd for row in _budget_rows(db)] == [0.0]


def test_a_new_day_carries_the_latest_earlier_rows_cap_not_the_oldest():
   db = _db()
   clock = FakeClock(MORNING)
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   configured = {"tutor": ENVIRONMENT_CAPS}

   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_usd": 0.0}, configured=configured, now=clock())
   clock.advance_days(1)
   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_usd": 2.0}, configured=configured, now=clock())
   clock.advance_days(1)

   _guard(db, double, caps=ENVIRONMENT_CAPS, clock=clock).generate(_request())

   third_day = [row for row in _budget_rows(db) if row.day == clock().date().isoformat()]

   assert double.calls == 1
   assert third_day[0].cap_usd == 2.0


def test_a_change_naming_one_unit_keeps_the_other_units_value():
   db = _db()
   clock = FakeClock(MORNING)
   configured = {"tutor": BudgetCaps(cap_tokens=50000.0, cap_usd=1.0)}

   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_tokens": 9000}, configured=configured, now=clock())

   assert (_budget_rows(db)[0].cap_usd, _budget_rows(db)[0].cap_tokens) == (1.0, 9000.0)

   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_usd": 0.5}, configured=configured, now=clock())

   assert (_budget_rows(db)[0].cap_usd, _budget_rows(db)[0].cap_tokens) == (0.5, 9000.0)

def test_after_a_change_a_lowered_startup_cap_leaves_the_changed_cap_in_force():
   db = _db()
   clock = FakeClock(MORNING)
   double = RecordingProvider(ReplayProvider(cassette=_cassette()))
   lowered_at_restart = BudgetCaps(cap_tokens=None, cap_usd=0.0)

   budget_settings.change_cap(db, USER_ID, "tutor", {"cap_usd": 2.0}, configured={"tutor": ENVIRONMENT_CAPS}, now=clock())
   _guard(db, double, caps=lowered_at_restart, clock=clock).generate(_request())

   assert double.calls == 1
   assert _budget_rows(db)[0].cap_usd == 2.0
