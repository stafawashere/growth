"""The serving cost measurement of docs/plan/11-phased-delivery.md P1 exit criterion 8: median
cost per served item and the cache read share over the one wired role. 11 sets no threshold, so
this prints numbers and never judges them.

    python3 tools/serving_cost.py <sqlite path> [--user <id>]

The database is opened read-only. A served item is one attempts row.

Items that made no tutor call are counted at a cost of 0. The plan decides this in
docs/plan/06-architecture.md, attempts table: tutor_calls is "tutor calls made for this served
item" with DEFAULT 0, so an attempts row with no call is still a served item, and the same table
names these columns as "the per-served-item tutor accounting" that exit criterion 8 measures. The
median over items that made a call is printed on a second line, labelled, as a supplement. An
item that made a call but carries no cost (a provider with no accounting) has an unknown cost,
not a zero one, and is left out of both medians and counted.

The cache read share is cached read tokens over total input tokens (06, "Metrics"), and a null
cached read means the provider did not report, never zero (07-ai-provider-layer.md, the usage
shape). It is printed from two sources. The attempts line is the one 06 names for exit criterion
8. An attempts row sums its calls, so it uses only served items where
tutor_cached_read_reported_calls equals tutor_calls, and states the reported calls it had to leave
out because they share a served item with calls that did not report. The budgets line does the
same per day row with cached_read_reported_calls and settled_calls. A day row with settled_calls 0
and nonzero sums was written before the call counts existed, or by a call still in flight, and 06
reads it as not a measurement; it is left out and counted.
"""
import argparse
import sqlite3
import statistics
import sys
from pathlib import Path

TUTOR_ROLE = "tutor"

REQUIRED_COLUMNS = {
   "attempts": (
      "session_id",
      "tutor_calls",
      "tutor_cost_usd",
      "tutor_tokens_in",
      "tutor_tokens_cached_read",
      "tutor_cached_read_reported_calls",
   ),
   "sessions": ("id", "user_id"),
   "budgets": (
      "user_id",
      "role",
      "tokens_in",
      "tokens_cached_read",
      "settled_calls",
      "cached_read_reported_calls",
   ),
}


class UnreadableDatabase(Exception):
   pass


def open_read_only(database_path):
   uri = f"{Path(database_path).resolve().as_uri()}?mode=ro"

   try:
      connection = sqlite3.connect(uri, uri=True)
      connection.execute("SELECT name FROM sqlite_master LIMIT 1").fetchall()
   except sqlite3.Error as error:
      raise UnreadableDatabase(f"cannot open {database_path} read-only: {error}") from error

   return connection


def missing_columns(connection):
   missing = []

   for table_name, column_names in REQUIRED_COLUMNS.items():
      rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
      live_column_names = {row[1] for row in rows}

      for column_name in column_names:
         is_missing = column_name not in live_column_names

         if is_missing:
            missing.append(f"{table_name}.{column_name}")

   return missing


def served_attempts(connection, user_id):
   columns = (
      "a.tutor_calls, a.tutor_cost_usd, a.tutor_tokens_in, a.tutor_tokens_cached_read, "
      "a.tutor_cached_read_reported_calls"
   )
   has_user = user_id is not None

   if has_user:
      statement = (
         f"SELECT {columns} FROM attempts a JOIN sessions s ON s.id = a.session_id WHERE s.user_id = ?"
      )

      return connection.execute(statement, (user_id,)).fetchall()

   return connection.execute(f"SELECT {columns} FROM attempts a").fetchall()


def tutor_budget_rows(connection, user_id):
   columns = "tokens_in, tokens_cached_read, settled_calls, cached_read_reported_calls"
   has_user = user_id is not None

   if has_user:
      statement = f"SELECT {columns} FROM budgets WHERE role = ? AND user_id = ?"

      return connection.execute(statement, (TUTOR_ROLE, user_id)).fetchall()

   statement = f"SELECT {columns} FROM budgets WHERE role = ?"

   return connection.execute(statement, (TUTOR_ROLE,)).fetchall()


def cost_lines(attempts):
   costs_all = []
   costs_with_call = []
   unknown_cost_items = 0

   for calls, cost, _tokens_in, _cached_read, _reported_calls in attempts:
      made_a_call = (calls or 0) > 0
      has_cost = cost is not None
      cost_is_unknown = made_a_call and not has_cost

      if cost_is_unknown:
         unknown_cost_items = unknown_cost_items + 1
         continue

      if not made_a_call:
         costs_all.append(cost if has_cost else 0.0)
         continue

      costs_all.append(cost)
      costs_with_call.append(cost)

   excluded_note = f"{unknown_cost_items} excluded for tutor calls with no recorded cost"
   has_costs = len(costs_all) > 0

   if has_costs:
      all_line = (
         f"median tutor cost per served item: {statistics.median(costs_all)} USD over "
         f"{len(costs_all)} served items, items with no tutor call counted at 0; {excluded_note}"
      )
   else:
      all_line = f"median tutor cost per served item: not measurable, 0 served items with a known cost; {excluded_note}"

   has_costs_with_call = len(costs_with_call) > 0

   if has_costs_with_call:
      with_call_line = (
         f"median tutor cost per served item that made a tutor call: {statistics.median(costs_with_call)} "
         f"USD over {len(costs_with_call)} served items"
      )
   else:
      with_call_line = "median tutor cost per served item that made a tutor call: not measurable, 0 served items"

   return [all_line, with_call_line]


def attempts_share_line(attempts):
   cached_tokens = 0
   input_tokens = 0
   reporting_calls = 0
   reporting_items = 0
   excluded_calls = 0
   partial_reported_calls = 0
   partial_items = 0

   for calls, _cost, tokens_in, cached_read, reported_calls in attempts:
      call_count = calls or 0
      made_a_call = call_count > 0
      reported_cached_read = cached_read is not None
      has_input = tokens_in is not None
      every_call_reported = reported_calls == call_count
      counts_toward_share = made_a_call and reported_cached_read and has_input and every_call_reported

      if counts_toward_share:
         cached_tokens = cached_tokens + cached_read
         input_tokens = input_tokens + tokens_in
         reporting_calls = reporting_calls + call_count
         reporting_items = reporting_items + 1
         continue

      if not made_a_call:
         continue

      unreported_calls = max(call_count - reported_calls, 0)
      excluded_calls = excluded_calls + unreported_calls
      is_partial = reported_calls > 0 and unreported_calls > 0

      if is_partial:
         partial_reported_calls = partial_reported_calls + reported_calls
         partial_items = partial_items + 1

   excluded_note = (
      f"{excluded_calls} tutor calls excluded for not reporting; {partial_reported_calls} reported calls on "
      f"{partial_items} served items excluded for sharing a served item with calls that did not report"
   )
   is_measurable = input_tokens > 0

   if not is_measurable:
      return (
         f"cache read share from attempts: not measurable, {reporting_calls} tutor calls on "
         f"{reporting_items} served items where every call reported a cached read; {excluded_note}"
      )

   return (
      f"cache read share from attempts: {cached_tokens / input_tokens} = {cached_tokens} cached read tokens / "
      f"{input_tokens} input tokens over {reporting_calls} tutor calls on {reporting_items} served items "
      f"where every call reported a cached read; {excluded_note}"
   )


def budgets_share_line(budget_rows):
   cached_tokens = 0
   input_tokens = 0
   reporting_calls = 0
   complete_rows = 0
   not_reporting_calls = 0
   partial_row_reported_calls = 0

   uncounted_rows = 0

   for tokens_in, cached_read, settled, reported in budget_rows:
      has_calls = settled > 0
      every_call_reported = has_calls and reported == settled
      has_sums = tokens_in > 0 or cached_read > 0
      is_uncounted = not has_calls and has_sums

      if is_uncounted:
         uncounted_rows = uncounted_rows + 1
         continue

      if every_call_reported:
         cached_tokens = cached_tokens + cached_read
         input_tokens = input_tokens + tokens_in
         reporting_calls = reporting_calls + settled
         complete_rows = complete_rows + 1
         continue

      not_reporting_calls = not_reporting_calls + (settled - reported)
      partial_row_reported_calls = partial_row_reported_calls + reported

   excluded_note = (
      f"{not_reporting_calls} tutor calls excluded for not reporting and {partial_row_reported_calls} "
      f"reported calls excluded for sharing a day row with them; {uncounted_rows} day rows with no settled "
      "call count excluded as not measured"
   )
   is_measurable = input_tokens > 0

   if not is_measurable:
      return (
         f"cache read share from budgets: not measurable, {reporting_calls} tutor calls on "
         f"{complete_rows} day rows where every call reported; {excluded_note}"
      )

   return (
      f"cache read share from budgets: {cached_tokens / input_tokens} = {cached_tokens} cached read tokens / "
      f"{input_tokens} input tokens over {reporting_calls} tutor calls on {complete_rows} day rows "
      f"where every call reported; {excluded_note}"
   )


def report_lines(connection, user_id):
   attempts = served_attempts(connection, user_id)
   budget_rows = tutor_budget_rows(connection, user_id)
   scope = "all users" if user_id is None else f"user {user_id}"

   return [
      f"scope: {scope}, role {TUTOR_ROLE}",
      f"served items: {len(attempts)}",
      *cost_lines(attempts),
      attempts_share_line(attempts),
      budgets_share_line(budget_rows),
   ]


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("database")
   parser.add_argument("--user")
   arguments = parser.parse_args(argv)

   try:
      connection = open_read_only(arguments.database)
   except UnreadableDatabase as error:
      print(str(error), file=sys.stderr)
      return 1

   try:
      missing = missing_columns(connection)
      has_missing = len(missing) > 0

      if has_missing:
         print(
            f"{arguments.database} is not migrated, missing: {', '.join(missing)}. "
            "Starting the app once applies app/db/migrate.py.",
            file=sys.stderr,
         )
         return 1

      for line in report_lines(connection, arguments.user):
         print(line)
   finally:
      connection.close()

   return 0


if __name__ == "__main__":
   sys.exit(main())