"""A database created before a model column existed, migrated additively.

The cases are driven off Base.metadata rather than a hand-written list of tables and columns,
so a column added to any model later is covered without touching this file.
"""
import pytest
from sqlalchemy import JSON, Float, Integer, LargeBinary, Numeric, inspect, select
from sqlalchemy.orm import Session

from app.db.migrate import SchemaDriftError, apply_additive_migrations, missing_columns
from app.db.models import Attempt, Base, make_engine


def droppable_nullable_columns():
   droppable = {}

   for table_name, table in Base.metadata.tables.items():
      candidates = [column.name for column in table.columns if column.nullable and not column.primary_key]

      if candidates:
         droppable[table_name] = tuple(candidates)

   return droppable


def first_required_column_without_server_default():
   for table_name, table in Base.metadata.tables.items():
      for column in table.columns:
         is_required = not column.nullable
         is_addable_anyway = column.server_default is not None
         blocks_alter = is_required and not is_addable_anyway and not column.primary_key

         if blocks_alter:
            return table_name, column.name

   raise AssertionError("no NOT NULL column without a server default exists in Base.metadata")


def drop_from_live_schema(engine, targets):
   with engine.begin() as connection:
      for table_name, column_names in targets.items():
         for column_name in column_names:
            connection.exec_driver_sql(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}"')

   inspector = inspect(engine)

   for table_name, column_names in targets.items():
      live = {column["name"] for column in inspector.get_columns(table_name)}

      for column_name in column_names:
         assert column_name not in live


def sample_value(column, marker):
   column_type = column.type

   if isinstance(column_type, JSON):
      return {}

   if isinstance(column_type, LargeBinary):
      return f"{marker}-{column.name}".encode()

   if isinstance(column_type, Integer):
      return 0

   if isinstance(column_type, (Float, Numeric)):
      return 0.0

   return f"{marker}-{column.name}"


def insert_one_row_per_table(engine, dropped, marker):
   written = {}

   with engine.begin() as connection:
      for table_name, table in Base.metadata.tables.items():
         surviving = [column for column in table.columns if column.name not in dropped.get(table_name, ())]
         values = {column.name: sample_value(column, marker) for column in surviving}

         connection.execute(table.insert().values(**values))

         written[table_name] = values

   return written


def attempt_row(marker):
   table = Base.metadata.tables["attempts"]
   required = [column for column in table.columns if not column.nullable]

   return {column.name: sample_value(column, marker) for column in required}


def test_missing_columns_reports_a_column_added_after_create_all(tmp_path):
   engine = make_engine(tmp_path / "drifted.sqlite")
   targets = droppable_nullable_columns()
   drop_from_live_schema(engine, targets)

   assert missing_columns(engine) == targets


def test_missing_columns_is_empty_on_a_fresh_database(tmp_path):
   engine = make_engine(tmp_path / "fresh.sqlite")

   assert missing_columns(engine) == {}


def test_apply_additive_migrations_adds_the_column_and_names_it(tmp_path):
   engine = make_engine(tmp_path / "named.sqlite")
   targets = droppable_nullable_columns()
   drop_from_live_schema(engine, targets)

   expected = tuple(sorted(f"{table_name}.{column_name}"
                           for table_name, column_names in targets.items()
                           for column_name in column_names))
   added = apply_additive_migrations(engine)

   assert added == expected
   assert "attempts.tutor_sentence" in added
   assert missing_columns(engine) == {}


def test_the_added_column_is_readable_and_writable_through_the_model(tmp_path):
   engine = make_engine(tmp_path / "roundtrip.sqlite")
   drop_from_live_schema(engine, {"attempts": ("tutor_sentence",)})
   apply_additive_migrations(engine)

   values = attempt_row("roundtrip")

   with Session(engine) as session:
      session.add(Attempt(**values))
      session.commit()

   with Session(engine) as session:
      stored = session.get(Attempt, values["id"])

      assert stored.tutor_sentence is None

      stored.tutor_sentence = "one sentence of feedback"
      session.commit()

   with Session(engine) as session:
      reread = session.get(Attempt, values["id"])

      assert reread.tutor_sentence == "one sentence of feedback"


def test_a_second_run_adds_nothing(tmp_path):
   engine = make_engine(tmp_path / "idempotent.sqlite")
   drop_from_live_schema(engine, droppable_nullable_columns())
   apply_additive_migrations(engine)

   assert apply_additive_migrations(engine) == ()
   assert missing_columns(engine) == {}


def test_a_not_null_column_without_a_default_raises_schema_drift(tmp_path):
   engine = make_engine(tmp_path / "blocked.sqlite")
   blocked_table, blocked_column = first_required_column_without_server_default()
   additive_targets = droppable_nullable_columns()
   drop_from_live_schema(engine, {blocked_table: (blocked_column,)})
   drop_from_live_schema(engine, additive_targets)

   before = missing_columns(engine)

   with pytest.raises(SchemaDriftError) as raised:
      apply_additive_migrations(engine)

   assert f"{blocked_table}.{blocked_column}" in str(raised.value)
   assert missing_columns(engine) == before


def test_migrating_preserves_the_rows_that_were_already_there(tmp_path):
   engine = make_engine(tmp_path / "rows.sqlite")
   targets = droppable_nullable_columns()
   drop_from_live_schema(engine, targets)

   written = insert_one_row_per_table(engine, targets, "preserved")
   apply_additive_migrations(engine)

   with engine.connect() as connection:
      for table_name, values in written.items():
         table = Base.metadata.tables[table_name]
         surviving = [table.c[name] for name in values]
         rows = connection.execute(select(*surviving)).all()

         assert len(rows) == 1
         assert dict(rows[0]._mapping) == values

         for column_name in targets.get(table_name, ()):
            restored = connection.execute(select(table.c[column_name])).scalar_one()

            assert restored is None


def test_a_unique_column_refuses_rather_than_migrating_without_its_constraint():
   """ALTER TABLE ADD COLUMN carries no UNIQUE and no index, so a migrated database would
   diverge silently from a fresh one while missing_columns reported it clean.
   """
   from sqlalchemy import Column, MetaData, String, Table
   from sqlalchemy.dialects import sqlite

   from app.db.migrate import _column_definition

   metadata = MetaData()
   table = Table(
      "drifting",
      metadata,
      Column("id", String, primary_key=True),
      Column("token", String, nullable=True, unique=True),
      Column("marker", String, nullable=True, index=True),
      Column("plain", String, nullable=True),
   )

   dialect = sqlite.dialect()

   assert _column_definition(dialect, table.columns["plain"])

   with pytest.raises(SchemaDriftError):
      _column_definition(dialect, table.columns["token"])

   with pytest.raises(SchemaDriftError):
      _column_definition(dialect, table.columns["marker"])


def test_a_database_with_no_drift_opens_no_write_transaction(tmp_path):
   engine = make_engine(tmp_path / "quiet.sqlite")

   opened = []

   original_begin = engine.begin

   def counting_begin(*arguments, **keywords):
      opened.append(True)

      return original_begin(*arguments, **keywords)

   engine.begin = counting_begin

   assert apply_additive_migrations(engine) == ()
   assert opened == []
