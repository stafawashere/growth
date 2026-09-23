"""Additive schema migration for the SQLite database declared in app/db/models.py.

Base.metadata.create_all creates a missing table and leaves an existing one untouched, so a
column added to a model after a database file was created never reaches that file. The storage
rules are in docs/plan/06-architecture.md, "Data model".
"""
from sqlalchemy import inspect
from sqlalchemy.dialects import sqlite

from app.db.models import Base


class SchemaDriftError(RuntimeError):
   pass


def missing_columns(engine):
   """Maps table name to a tuple of column names that Base.metadata declares and the live
   database lacks. Tables the database does not have at all are not reported here, because
   create_all makes them."""
   inspector = inspect(engine)
   live_table_names = set(inspector.get_table_names())

   drift = {}

   for table_name, table in Base.metadata.tables.items():
      table_exists = table_name in live_table_names

      if not table_exists:
         continue

      live_column_names = {column["name"] for column in inspector.get_columns(table_name)}
      absent = tuple(column.name for column in table.columns if column.name not in live_column_names)

      if absent:
         drift[table_name] = absent

   return drift


def _column_definition(dialect, column):
   has_server_default = column.server_default is not None
   is_additive = column.nullable or has_server_default

   if not is_additive:
      raise SchemaDriftError(
         f"{column.table.name}.{column.name} is NOT NULL with no server default, "
         "which SQLite cannot add to an existing table"
      )

   is_unique = column.unique is True
   is_indexed = column.index is True
   carries_a_constraint_alter_cannot = is_unique or is_indexed

   if carries_a_constraint_alter_cannot:
      raise SchemaDriftError(
         f"{column.table.name}.{column.name} is declared unique or indexed, and "
         "ALTER TABLE ADD COLUMN carries neither, so the migrated database would differ "
         "from a fresh one while reporting no drift"
      )

   quoted_name = dialect.identifier_preparer.quote(column.name)
   rendered_type = dialect.type_compiler_instance.process(column.type, type_expression=column)
   definition = f"{quoted_name} {rendered_type}"

   if has_server_default:
      rendered_default = dialect.ddl_compiler(dialect, None).get_column_default_string(column)
      definition = f"{definition} NOT NULL DEFAULT {rendered_default}"

   return definition


def apply_additive_migrations(engine):
   """Adds every missing column with ALTER TABLE ADD COLUMN and returns a tuple of the
   "table.column" strings it added, sorted. Raises SchemaDriftError when a missing column
   cannot be added additively, which means a column that is NOT NULL with no server default,
   because SQLite cannot add one to a populated table."""
   drift = missing_columns(engine)
   dialect = sqlite.dialect()

   statements = []

   for table_name in sorted(drift):
      table = Base.metadata.tables[table_name]
      quoted_table = dialect.identifier_preparer.quote(table_name)

      for column_name in sorted(drift[table_name]):
         definition = _column_definition(dialect, table.columns[column_name])

         statements.append((f"{table_name}.{column_name}", f"ALTER TABLE {quoted_table} ADD COLUMN {definition}"))

   has_work = len(statements) > 0

   if has_work:
      with engine.begin() as connection:
         for _, statement in statements:
            connection.exec_driver_sql(statement)

   return tuple(name for name, _ in statements)
