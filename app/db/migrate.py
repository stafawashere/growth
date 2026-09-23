"""Additive schema migration for the SQLite database declared in app/db/models.py.

Base.metadata.create_all creates a missing table and leaves an existing one untouched, so a
column added to a model after a database file was created never reaches that file. The storage
rules are in docs/plan/06-architecture.md, "Data model".
"""
import json

from sqlalchemy import inspect, text
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


def _backfill_credited_observation_count(connection):
   """skills_state.credited_observation_count is new, and its server default of 0 leaves every
   row already in the table reading as if it had never had a credited observation. app/engine/
   fringe.py serve_stage reads that field to decide whether the stored fading_stage wins over the
   p_A_knowledge bands, so a 0 backfill would silently undo a student's fading progress on the
   first migrated read. Recomputed here from attempts.per_skill_states, replaying the same credit
   rule app/engine/update.py apply_observation uses, for every attempt in a session that writes
   mastery (sessions.updates_mastery); a session that does not write mastery never reached
   apply_observation and contributes nothing.
   """
   from app.engine.state import MasteryState, ResponseFormat
   from app.engine.update import credit_for

   rows = connection.execute(
      text(
         "SELECT sessions.user_id AS user_id, attempts.per_skill_states AS per_skill_states, "
         "attempts.format AS format "
         "FROM attempts JOIN sessions ON sessions.id = attempts.session_id "
         "WHERE sessions.updates_mastery = 1"
      )
   ).mappings().all()

   counts = {}

   for row in rows:
      per_skill_states = json.loads(row["per_skill_states"])
      response_format = ResponseFormat(row["format"])

      for skill_id, mastery_state_value in per_skill_states.items():
         mastery_state = MasteryState(mastery_state_value)
         c_credit, f_credit = credit_for(mastery_state, response_format)
         is_gap = mastery_state == MasteryState.PREREQUISITE_GAP
         is_credited = c_credit > 0.0 or f_credit > 0.0 or is_gap

         if not is_credited:
            continue

         key = (row["user_id"], skill_id)
         counts[key] = counts.get(key, 0) + 1

   for (user_id, skill_id), count in counts.items():
      connection.execute(
         text(
            "UPDATE skills_state SET credited_observation_count = :count "
            "WHERE user_id = :user_id AND skill_id = :skill_id"
         ),
         {"count": count, "user_id": user_id, "skill_id": skill_id},
      )


BACKFILLS = {
   "skills_state.credited_observation_count": _backfill_credited_observation_count,
}


def repair_wrapped_stems(engine):
   """items.stem held json.dumps(record["stem"]) before app/items/ingest.py item_row switched to
   record["stem"]["text"], so any row ingested under the old code still carries the wrapper, such
   as '{"text": "Differentiate f with respect to x."}', and app/runtime/bank.py _as_item_dict
   serves that string straight to the student. ingest_new_records skips a record whose id is
   already stored, so re-running ingestion never touches those rows; this repairs them in place on
   every startup, which is cheap and a no-op once every row has been unwrapped once.
   """
   with engine.connect() as connection:
      candidates = connection.execute(
         text("SELECT id, stem FROM items WHERE stem LIKE '{%'")
      ).mappings().all()

   repaired = []

   for row in candidates:
      try:
         payload = json.loads(row["stem"])
      except (TypeError, ValueError):
         continue

      is_wrapped_stem = isinstance(payload, dict) and isinstance(payload.get("text"), str)

      if not is_wrapped_stem:
         continue

      repaired.append((row["id"], payload["text"]))

   has_work = len(repaired) > 0

   if has_work:
      with engine.begin() as connection:
         for item_id, text_value in repaired:
            connection.execute(
               text("UPDATE items SET stem = :stem WHERE id = :id"),
               {"stem": text_value, "id": item_id},
            )

   return tuple(item_id for item_id, _ in repaired)


def apply_additive_migrations(engine):
   """Adds every missing column with ALTER TABLE ADD COLUMN and returns a tuple of the
   "table.column" strings it added, sorted. Raises SchemaDriftError when a missing column
   cannot be added additively, which means a column that is NOT NULL with no server default,
   because SQLite cannot add one to a populated table. A column named in BACKFILLS gets its
   values recomputed from history in the same transaction right after it is added, rather than
   left at its server default on every row that already existed."""
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
         for name, statement in statements:
            connection.exec_driver_sql(statement)

            backfill = BACKFILLS.get(name)

            if backfill is not None:
               backfill(connection)

   return tuple(name for name, _ in statements)
