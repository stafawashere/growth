"""The per-served-item tutor accounting on attempts, reached on a database that predates it.

docs/plan/06-architecture.md, table attempts: tutor_calls, tutor_cost_usd, tutor_tokens_in and
tutor_tokens_cached_read carry what 11's P1 exit criterion 8 measures per served item. A file
created before those columns existed must gain them through apply_additive_migrations, and a row
already in it must read back a zero call count and a null cost rather than an invented number.

The same holds for the call counts on budgets (06, table budgets): a day row written before
settled_calls and the two reported counts existed reads back 0 in all three, which 06 and
tools/serving_cost.py read as a row whose cached sums are not a measurement.
"""
import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError

from app.db.migrate import apply_additive_migrations
from app.db.models import Base

TUTOR_COLUMNS = (
   "tutor_calls",
   "tutor_cost_usd",
   "tutor_tokens_in",
   "tutor_tokens_cached_read",
   "tutor_cached_read_reported_calls",
)

OLD_ROW = {
   "id": "ATT-OLD",
   "session_id": "SES-1",
   "item_id": "ITM-1",
   "started_at": "2026-09-20T10:00:00+00:00",
   "transcription_confirmed": 0,
   "served_stage": "learning",
   "format": "mcq",
   "per_skill_states": "{}",
   "snapshot_id": "SNP-1",
   "created_at": "2026-09-20T10:00:00+00:00",
   "updated_at": "2026-09-20T10:00:00+00:00",
}


def database_with_the_old_attempts_shape(tmp_path):
   engine = create_engine(f"sqlite:///{tmp_path / 'old.db'}")
   Base.metadata.create_all(engine)

   with engine.begin() as connection:
      for column_name in TUTOR_COLUMNS:
         connection.exec_driver_sql(f'ALTER TABLE "attempts" DROP COLUMN "{column_name}"')

      names = ", ".join(OLD_ROW)
      placeholders = ", ".join(f":{name}" for name in OLD_ROW)
      connection.exec_driver_sql(f"INSERT INTO attempts ({names}) VALUES ({placeholders})", OLD_ROW)

   live = {column["name"] for column in inspect(engine).get_columns("attempts")}
   assert live.isdisjoint(TUTOR_COLUMNS)

   return engine


def test_the_migrator_adds_the_tutor_columns_to_an_old_attempts_table(tmp_path):
   engine = database_with_the_old_attempts_shape(tmp_path)

   added = apply_additive_migrations(engine)

   assert set(added) == {f"attempts.{name}" for name in TUTOR_COLUMNS}

   with engine.connect() as connection:
      row = connection.exec_driver_sql(
         "SELECT tutor_calls, tutor_cost_usd, tutor_tokens_in, tutor_tokens_cached_read, "
         "tutor_cached_read_reported_calls FROM attempts WHERE id = 'ATT-OLD'"
      ).one()

   assert tuple(row) == (0, None, None, None, 0)


def test_tutor_calls_stays_not_null_after_migration(tmp_path):
   engine = database_with_the_old_attempts_shape(tmp_path)
   apply_additive_migrations(engine)

   with pytest.raises(IntegrityError):
      with engine.begin() as connection:
         connection.exec_driver_sql("UPDATE attempts SET tutor_calls = NULL WHERE id = 'ATT-OLD'")


def test_tutor_cached_read_reported_calls_stays_not_null_after_migration(tmp_path):
   engine = database_with_the_old_attempts_shape(tmp_path)
   apply_additive_migrations(engine)

   with pytest.raises(IntegrityError):
      with engine.begin() as connection:
         connection.exec_driver_sql(
            "UPDATE attempts SET tutor_cached_read_reported_calls = NULL WHERE id = 'ATT-OLD'"
         )


def test_a_fresh_database_declares_the_same_nullability(tmp_path):
   engine = create_engine(f"sqlite:///{tmp_path / 'fresh.db'}")
   Base.metadata.create_all(engine)

   declared = {column["name"]: column["nullable"] for column in inspect(engine).get_columns("attempts")}

   assert declared["tutor_calls"] is False
   assert declared["tutor_cost_usd"] is True
   assert declared["tutor_tokens_in"] is True
   assert declared["tutor_tokens_cached_read"] is True
   assert declared["tutor_cached_read_reported_calls"] is False


BUDGET_COUNT_COLUMNS = ("settled_calls", "cached_read_reported_calls", "cached_write_reported_calls")

OLD_BUDGET_ROW = {
   "id": "BUD-OLD",
   "user_id": "USR-1",
   "role": "tutor",
   "day": "2026-09-20",
   "tokens_in": 3000,
   "tokens_out": 120,
   "tokens_cached_read": 1100,
   "tokens_cached_write": 0,
   "cost_usd": 0.01,
   "hard_stopped": 0,
   "created_at": "2026-09-20T10:00:00+00:00",
   "updated_at": "2026-09-20T10:00:00+00:00",
}


def database_with_the_old_budgets_shape(tmp_path):
   engine = create_engine(f"sqlite:///{tmp_path / 'old_budgets.db'}")
   Base.metadata.create_all(engine)

   with engine.begin() as connection:
      for column_name in BUDGET_COUNT_COLUMNS:
         connection.exec_driver_sql(f'ALTER TABLE "budgets" DROP COLUMN "{column_name}"')

      names = ", ".join(OLD_BUDGET_ROW)
      placeholders = ", ".join(f":{name}" for name in OLD_BUDGET_ROW)
      connection.exec_driver_sql(f"INSERT INTO budgets ({names}) VALUES ({placeholders})", OLD_BUDGET_ROW)

   live = {column["name"] for column in inspect(engine).get_columns("budgets")}
   assert live.isdisjoint(BUDGET_COUNT_COLUMNS)

   return engine


def test_the_migrator_adds_the_call_counts_to_an_old_budgets_table(tmp_path):
   engine = database_with_the_old_budgets_shape(tmp_path)

   added = apply_additive_migrations(engine)

   assert set(added) == {f"budgets.{name}" for name in BUDGET_COUNT_COLUMNS}

   with engine.connect() as connection:
      row = connection.exec_driver_sql(
         "SELECT settled_calls, cached_read_reported_calls, cached_write_reported_calls, tokens_cached_read "
         "FROM budgets WHERE id = 'BUD-OLD'"
      ).one()

   assert tuple(row) == (0, 0, 0, 1100)


def test_the_budget_call_counts_stay_not_null_after_migration(tmp_path):
   engine = database_with_the_old_budgets_shape(tmp_path)
   apply_additive_migrations(engine)

   for column_name in BUDGET_COUNT_COLUMNS:
      with pytest.raises(IntegrityError):
         with engine.begin() as connection:
            connection.exec_driver_sql(f"UPDATE budgets SET {column_name} = NULL WHERE id = 'BUD-OLD'")
