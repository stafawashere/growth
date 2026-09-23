"""Tests for tools/serving_cost.py, the measurement docs/plan/11-phased-delivery.md P1 exit
criterion 8 asks for: median cost per served item and the cache read share over the one wired
role, with no threshold.

Every test builds a real database through app.db.models, writes attempts and budgets rows with
known values, runs the CLI as a subprocess and reads the numbers back out of what it printed.
"""
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tools.serving_cost import TUTOR_ROLE

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TUTOR_SOURCE = REPOSITORY_ROOT / "app" / "feedback" / "tutor.py"
STAMP = "2026-09-23T00:00:00Z"

NUMBER = r"([0-9.e-]+)"
MEDIAN_ALL = re.compile(
   rf"^median tutor cost per served item: {NUMBER} USD over (\d+) served items, .*; (\d+) excluded",
   re.MULTILINE,
)
MEDIAN_WITH_CALL = re.compile(
   rf"^median tutor cost per served item that made a tutor call: {NUMBER} USD over (\d+) served items",
   re.MULTILINE,
)
ATTEMPTS_SHARE = re.compile(
   rf"^cache read share from attempts: {NUMBER} = (\d+) cached read tokens / (\d+) input tokens "
   r"over (\d+) tutor calls on (\d+) served items where every call reported a cached read; "
   r"(\d+) tutor calls excluded for not reporting",
   re.MULTILINE,
)
ATTEMPTS_PARTIAL = re.compile(
   r"^cache read share from attempts: .*; (\d+) reported calls on (\d+) served items excluded for "
   r"sharing a served item with calls that did not report",
   re.MULTILINE,
)
BUDGETS_UNCOUNTED = re.compile(
   r"^cache read share from budgets: .*; (\d+) day rows with no settled call count excluded as not measured",
   re.MULTILINE,
)
BUDGETS_SHARE = re.compile(
   rf"^cache read share from budgets: {NUMBER} = (\d+) cached read tokens / (\d+) input tokens "
   r"over (\d+) tutor calls on (\d+) day rows where every call reported; "
   r"(\d+) tutor calls excluded for not reporting and (\d+) reported calls excluded",
   re.MULTILINE,
)


def run_cli(database_path, *extra):
   return subprocess.run(
      [sys.executable, "tools/serving_cost.py", str(database_path), *extra],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )


def served_attempt(index, session_id, calls, cost, tokens_in=None, cached_read=None, read_reported=None):
   """read_reported defaults to every call reporting when a cached read is given and to none when
   it is null, the two shapes a served item takes when all its calls agree."""
   has_cached_read = cached_read is not None
   every_call_or_none = calls if has_cached_read else 0
   reported_calls = every_call_or_none if read_reported is None else read_reported

   return models.Attempt(
      id=f"att-{session_id}-{index}",
      session_id=session_id,
      item_id=f"ITM-{index}",
      started_at=STAMP,
      served_stage="completion",
      format="mcq",
      per_skill_states="{}",
      tutor_calls=calls,
      tutor_cost_usd=cost,
      tutor_tokens_in=tokens_in,
      tutor_tokens_cached_read=cached_read,
      tutor_cached_read_reported_calls=reported_calls,
      snapshot_id="snap-1",
      created_at=STAMP,
      updated_at=STAMP,
   )


def budget_row(user_id, role, day, settled, read_reported, tokens_in, cached_read):
   return models.Budget(
      id=f"bud-{user_id}-{role}-{day}",
      user_id=user_id,
      role=role,
      day=day,
      tokens_in=tokens_in,
      tokens_cached_read=cached_read,
      settled_calls=settled,
      cached_read_reported_calls=read_reported,
      created_at=STAMP,
      updated_at=STAMP,
   )


def study_session(session_id, user_id):
   return models.Session(
      id=session_id,
      user_id=user_id,
      mode="practice",
      started_at=STAMP,
      queue="[]",
      snapshot_id="snap-1",
      created_at=STAMP,
      updated_at=STAMP,
   )


def build_database(tmp_path, rows):
   database_path = tmp_path / "growth.db"
   engine = models.make_engine(database_path)

   with OrmSession(engine) as db:
      db.add_all(rows)
      db.commit()

   engine.dispose()

   return database_path


def parsed(pattern, output):
   match = pattern.search(output)
   assert match is not None, output

   return match.groups()


def test_tutor_role_matches_the_role_the_tutor_requests_under():
   declared_roles = re.findall(r"role=\"(\w+)\",\n\s+model=TUTOR_MODEL", TUTOR_SOURCE.read_text())

   assert declared_roles == [TUTOR_ROLE]


def test_odd_median_counts_items_with_no_tutor_call_at_zero(tmp_path):
   database_path = build_database(tmp_path, [
      study_session("s1", "u1"),
      served_attempt(1, "s1", calls=1, cost=0.003),
      served_attempt(2, "s1", calls=0, cost=None),
      served_attempt(3, "s1", calls=2, cost=0.001),
      served_attempt(4, "s1", calls=1, cost=None),
   ])

   completed = run_cli(database_path)

   assert completed.returncode == 0, completed.stderr
   assert "served items: 4" in completed.stdout

   median_all, counted_all, excluded = parsed(MEDIAN_ALL, completed.stdout)
   assert float(median_all) == pytest.approx(0.001)
   assert (int(counted_all), int(excluded)) == (3, 1)

   median_with_call, counted_with_call = parsed(MEDIAN_WITH_CALL, completed.stdout)
   assert float(median_with_call) == pytest.approx(0.002)
   assert int(counted_with_call) == 2


def test_even_median_over_all_served_items(tmp_path):
   database_path = build_database(tmp_path, [
      study_session("s1", "u1"),
      served_attempt(1, "s1", calls=0, cost=None),
      served_attempt(2, "s1", calls=1, cost=0.002),
      served_attempt(3, "s1", calls=1, cost=0.006),
      served_attempt(4, "s1", calls=1, cost=0.010),
   ])

   completed = run_cli(database_path)

   median_all, counted_all, _excluded = parsed(MEDIAN_ALL, completed.stdout)
   assert float(median_all) == pytest.approx(0.004)
   assert int(counted_all) == 4


def test_attempts_share_leaves_out_items_whose_calls_reported_no_cached_read(tmp_path):
   database_path = build_database(tmp_path, [
      study_session("s1", "u1"),
      served_attempt(1, "s1", calls=1, cost=0.001, tokens_in=1000, cached_read=400),
      served_attempt(2, "s1", calls=2, cost=0.002, tokens_in=500, cached_read=0),
      served_attempt(3, "s1", calls=1, cost=0.003, tokens_in=2000, cached_read=None),
      served_attempt(4, "s1", calls=0, cost=None),
   ])

   completed = run_cli(database_path)

   share, cached, total_in, calls, items, excluded = parsed(ATTEMPTS_SHARE, completed.stdout)
   assert float(share) == pytest.approx(400 / 1500)
   assert (int(cached), int(total_in), int(calls), int(items), int(excluded)) == (400, 1500, 3, 2, 1)


def test_budgets_share_uses_only_tutor_day_rows_where_every_call_reported(tmp_path):
   database_path = build_database(tmp_path, [
      budget_row("u1", "tutor", "2026-09-20", settled=3, read_reported=3, tokens_in=3000, cached_read=1200),
      budget_row("u1", "tutor", "2026-09-21", settled=2, read_reported=1, tokens_in=2000, cached_read=500),
      budget_row("u1", "tutor", "2026-09-22", settled=1, read_reported=0, tokens_in=900, cached_read=0),
      budget_row("u1", "generator", "2026-09-20", settled=5, read_reported=5, tokens_in=10000, cached_read=0),
   ])

   completed = run_cli(database_path)

   share, cached, total_in, calls, rows, not_reporting, partial = parsed(BUDGETS_SHARE, completed.stdout)
   assert float(share) == pytest.approx(0.4)
   counts = (int(cached), int(total_in), int(calls), int(rows), int(not_reporting), int(partial))
   assert counts == (1200, 3000, 3, 1, 2, 1)


def test_no_reported_cached_read_prints_not_measurable_rather_than_zero(tmp_path):
   database_path = build_database(tmp_path, [
      study_session("s1", "u1"),
      served_attempt(1, "s1", calls=1, cost=0.001, tokens_in=1000, cached_read=None),
      served_attempt(2, "s1", calls=2, cost=0.002, tokens_in=800, cached_read=None),
      budget_row("u1", "tutor", "2026-09-20", settled=3, read_reported=0, tokens_in=1800, cached_read=0),
   ])

   completed = run_cli(database_path)

   assert completed.returncode == 0, completed.stderr
   assert re.search(
      r"^cache read share from attempts: not measurable, .*; 3 tutor calls excluded for not reporting",
      completed.stdout,
      re.MULTILINE,
   ), completed.stdout
   assert re.search(
      r"^cache read share from budgets: not measurable, .*; 3 tutor calls excluded for not reporting",
      completed.stdout,
      re.MULTILINE,
   ), completed.stdout
   assert ATTEMPTS_SHARE.search(completed.stdout) is None
   assert BUDGETS_SHARE.search(completed.stdout) is None


def test_empty_database_reports_no_median(tmp_path):
   database_path = build_database(tmp_path, [])

   completed = run_cli(database_path)

   assert completed.returncode == 0, completed.stderr
   assert "served items: 0" in completed.stdout
   assert re.search(r"^median tutor cost per served item: not measurable", completed.stdout, re.MULTILINE)
   assert MEDIAN_ALL.search(completed.stdout) is None


def test_user_filter_reads_only_that_users_sessions_and_budgets(tmp_path):
   database_path = build_database(tmp_path, [
      study_session("s1", "u1"),
      study_session("s2", "u2"),
      served_attempt(1, "s1", calls=1, cost=0.001, tokens_in=1000, cached_read=100),
      served_attempt(2, "s2", calls=1, cost=0.009, tokens_in=1000, cached_read=900),
      served_attempt(3, "s2", calls=1, cost=0.009, tokens_in=1000, cached_read=900),
      budget_row("u1", "tutor", "2026-09-20", settled=1, read_reported=1, tokens_in=1000, cached_read=100),
      budget_row("u2", "tutor", "2026-09-20", settled=2, read_reported=2, tokens_in=2000, cached_read=1800),
   ])

   completed = run_cli(database_path, "--user", "u1")

   assert completed.returncode == 0, completed.stderr
   assert "served items: 1" in completed.stdout

   median_all, _counted, _excluded = parsed(MEDIAN_ALL, completed.stdout)
   assert float(median_all) == pytest.approx(0.001)

   attempts_share = parsed(ATTEMPTS_SHARE, completed.stdout)[0]
   budgets_share = parsed(BUDGETS_SHARE, completed.stdout)[0]
   assert float(attempts_share) == pytest.approx(0.1)
   assert float(budgets_share) == pytest.approx(0.1)


def test_missing_database_exits_non_zero_and_creates_nothing(tmp_path):
   database_path = tmp_path / "absent.db"

   completed = run_cli(database_path)

   assert completed.returncode != 0
   assert str(database_path) in completed.stderr
   assert not database_path.exists()


def test_unmigrated_database_exits_non_zero_naming_the_missing_columns(tmp_path):
   database_path = tmp_path / "old.db"
   connection = sqlite3.connect(database_path)
   connection.execute("CREATE TABLE attempts (id TEXT PRIMARY KEY, session_id TEXT)")
   connection.execute("CREATE TABLE sessions (id TEXT PRIMARY KEY, user_id TEXT)")
   connection.execute("CREATE TABLE budgets (id TEXT PRIMARY KEY, user_id TEXT, role TEXT)")
   connection.commit()
   connection.close()

   completed = run_cli(database_path)

   assert completed.returncode != 0
   assert "attempts.tutor_cost_usd" in completed.stderr
   assert "budgets.cached_read_reported_calls" in completed.stderr
   assert completed.stdout == ""


def test_attempts_share_leaves_out_an_item_where_only_some_calls_reported(tmp_path):
   """06, attempts: the row sums its calls, so an item with two calls and one report carries a
   cached read that covers half its input. Only items where the reported count equals tutor_calls
   enter the share, and the rest are counted in the output."""
   database_path = build_database(tmp_path, [
      study_session("s1", "u1"),
      served_attempt(1, "s1", calls=1, cost=0.001, tokens_in=1000, cached_read=400),
      served_attempt(2, "s1", calls=2, cost=0.002, tokens_in=2000, cached_read=900, read_reported=1),
   ])

   completed = run_cli(database_path)

   share, cached, total_in, calls, items, excluded = parsed(ATTEMPTS_SHARE, completed.stdout)
   partial_calls, partial_items = parsed(ATTEMPTS_PARTIAL, completed.stdout)

   assert float(share) == pytest.approx(400 / 1000)
   assert (int(cached), int(total_in), int(calls), int(items), int(excluded)) == (400, 1000, 1, 1, 1)
   assert (int(partial_calls), int(partial_items)) == (1, 1)


def test_a_budgets_row_written_before_the_call_counts_is_not_measured(tmp_path):
   """A pre-migration day row reads settled_calls 0 with its old token sums, so its cached read
   is not a measurement (06, budgets) and is counted as excluded rather than folded in."""
   database_path = build_database(tmp_path, [
      budget_row("u1", "tutor", "2026-09-19", settled=0, read_reported=0, tokens_in=3000, cached_read=1100),
      budget_row("u1", "tutor", "2026-09-20", settled=2, read_reported=2, tokens_in=2000, cached_read=500),
   ])

   completed = run_cli(database_path)

   share, cached, total_in, calls, rows, not_reporting, partial = parsed(BUDGETS_SHARE, completed.stdout)
   uncounted_rows = parsed(BUDGETS_UNCOUNTED, completed.stdout)[0]

   assert float(share) == pytest.approx(0.25)
   assert (int(cached), int(total_in), int(calls), int(rows)) == (500, 2000, 2, 1)
   assert int(uncounted_rows) == 1
