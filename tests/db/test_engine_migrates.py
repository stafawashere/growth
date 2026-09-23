"""make_engine is the only place the application opens the database, so it is where the schema
has to be reconciled. create_all makes a missing table and never alters an existing one, which is
how attempts.tutor_sentence reached the models and never reached a database created before it.
"""
import pytest
from sqlalchemy import inspect, text

from app.db import models
from app.db.migrate import SchemaDriftError, missing_columns


def required_columns(table_name):
   """Every NOT NULL column without a default, filled with a value of the right shape, so the
   insert exercises the restored column rather than failing on an unrelated constraint."""
   table = models.Base.metadata.tables[table_name]
   filled = {}

   for column in table.columns:
      needs_a_value = not column.nullable and column.server_default is None

      if not needs_a_value:
         continue

      python_type = column.type.python_type

      if python_type is int:
         filled[column.name] = 0
      elif python_type is float:
         filled[column.name] = 0.0
      else:
         filled[column.name] = "x"

   return filled


def drifted_database(tmp_path, table_name, column_name):
   path = tmp_path / "drifted.sqlite"
   engine = models.make_engine(path)

   with engine.begin() as connection:
      connection.execute(text(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"'))

   engine.dispose()

   return path


def test_opening_a_drifted_database_restores_the_missing_column(tmp_path):
   path = drifted_database(tmp_path, "attempts", "tutor_sentence")

   reopened = models.make_engine(path)

   columns = {column["name"] for column in inspect(reopened).get_columns("attempts")}

   assert "tutor_sentence" in columns
   assert missing_columns(reopened) == {}


def test_the_restored_column_is_writable_through_the_model(tmp_path):
   path = drifted_database(tmp_path, "attempts", "tutor_sentence")

   reopened = models.make_engine(path)

   required = required_columns("attempts")
   required.pop("id", None)

   names = ["id", "tutor_sentence"] + sorted(required)
   placeholders = ", ".join(f":{name}" for name in names)
   values = {"id": "ATT-drift", "tutor_sentence": "one sentence"}
   values.update(required)

   with reopened.begin() as connection:
      connection.execute(
         text(f"INSERT INTO attempts ({', '.join(names)}) VALUES ({placeholders})"), values
      )

   with reopened.connect() as connection:
      stored = connection.execute(
         text("SELECT tutor_sentence FROM attempts WHERE id = 'ATT-drift'")
      ).scalar_one()

   assert stored == "one sentence"


def test_a_fresh_database_needs_no_migration(tmp_path):
   engine = models.make_engine(tmp_path / "fresh.sqlite")

   assert missing_columns(engine) == {}


def test_a_non_additive_drift_refuses_to_open(tmp_path):
   not_null_column = None

   for table in models.Base.metadata.tables.values():
      for column in table.columns:
         is_blocking = (
            not column.nullable
            and not column.primary_key
            and column.server_default is None
         )

         if is_blocking and not_null_column is None:
            not_null_column = (table.name, column.name)

   assert not_null_column is not None, "no NOT NULL column without a default to drift"

   table_name, column_name = not_null_column
   path = drifted_database(tmp_path, table_name, column_name)

   with pytest.raises(SchemaDriftError):
      models.make_engine(path)
