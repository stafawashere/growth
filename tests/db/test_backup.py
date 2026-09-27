import sqlite3
from datetime import date, timedelta

from app.db.backup import back_up_database, dated_backups


def write_rows(db_path, *values):
   connection = sqlite3.connect(db_path)
   connection.execute("CREATE TABLE IF NOT EXISTS attempts (value TEXT)")
   connection.executemany("INSERT INTO attempts VALUES (?)", [(value,) for value in values])
   connection.commit()
   connection.close()


def read_rows(db_path):
   connection = sqlite3.connect(db_path)
   rows = [row[0] for row in connection.execute("SELECT value FROM attempts ORDER BY rowid")]
   connection.close()

   return rows


def test_copy_holds_the_rows_the_database_held(tmp_path):
   db_path = tmp_path / "growth.db"
   write_rows(db_path, "first", "second")

   written = back_up_database(db_path, tmp_path / "backups", today=date(2026, 9, 26))

   assert written.name == "growth-2026-09-26.db"
   assert read_rows(written) == ["first", "second"]


def test_a_later_start_the_same_day_keeps_the_first_copy(tmp_path):
   db_path = tmp_path / "growth.db"
   backup_dir = tmp_path / "backups"
   today = date(2026, 9, 26)
   write_rows(db_path, "morning")
   first = back_up_database(db_path, backup_dir, today=today)

   write_rows(db_path, "afternoon")
   second = back_up_database(db_path, backup_dir, today=today)

   assert second is None
   assert read_rows(first) == ["morning"]


def test_only_the_newest_copies_are_kept(tmp_path):
   db_path = tmp_path / "growth.db"
   backup_dir = tmp_path / "backups"
   write_rows(db_path, "row")
   start = date(2026, 9, 1)

   for offset in range(5):
      back_up_database(db_path, backup_dir, today=start + timedelta(days=offset), keep=3)

   kept = [path.name for path in dated_backups(backup_dir)]

   assert kept == ["growth-2026-09-03.db", "growth-2026-09-04.db", "growth-2026-09-05.db"]


def test_nothing_is_written_before_the_database_exists(tmp_path):
   written = back_up_database(tmp_path / "growth.db", tmp_path / "backups", today=date(2026, 9, 26))

   assert written is None
   assert not (tmp_path / "backups").exists()