"""A dated copy of the SQLite database taken each time the server starts.

var/growth.db is gitignored and holds the only record of a student's attempts, so the server
copies it before it opens it. One copy per day is kept, the first of that day, because a restart
later in the day should not replace a good morning copy with an afternoon one that already holds
whatever went wrong. The oldest copies past the keep count are removed.

A second kind of copy is named rather than dated. app/db/migrate.py takes one before it drops a
retired table, so the passkey rows it removes can still be read back. Its name never matches the
dated pattern, so the keep count never prunes it.
"""
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path

BACKUP_PREFIX = "growth-"
BACKUP_SUFFIX = ".db"
DEFAULT_KEEP = 14
RETIRE_BACKUP_PREFIX = "growth-before-retiring-"
BACKUP_DIRECTORY_NAME = "backups"


def copy_database(db_path, target):
   target.parent.mkdir(parents=True, exist_ok=True)
   partial = target.with_suffix(".partial")

   source = sqlite3.connect(db_path)
   destination = sqlite3.connect(partial)

   try:
      source.backup(destination)
   finally:
      destination.close()
      source.close()

   partial.replace(target)


def backup_path_for(backup_dir, day):
   return Path(backup_dir) / f"{BACKUP_PREFIX}{day.isoformat()}{BACKUP_SUFFIX}"


def dated_backups(backup_dir):
   return sorted(Path(backup_dir).glob(f"{BACKUP_PREFIX}????-??-??{BACKUP_SUFFIX}"))


def back_up_database(db_path, backup_dir, today=None, keep=DEFAULT_KEEP):
   """Returns the path written, or None when there was nothing to copy or today's copy exists."""
   db_path = Path(db_path)
   today = today or date.today()
   has_database = db_path.is_file()

   if not has_database:
      return None

   target = backup_path_for(backup_dir, today)
   already_copied_today = target.exists()

   if already_copied_today:
      return None

   copy_database(db_path, target)

   for stale in dated_backups(backup_dir)[:-keep]:
      stale.unlink()

   return target


def back_up_before_retiring(db_path, table_names, backup_dir=None, now=None):
   """Copies the database to backups/ beside it, named for the tables about to be dropped and the
   moment, and returns the path written."""
   db_path = Path(db_path)
   moment = now or datetime.now(timezone.utc)
   directory = Path(backup_dir) if backup_dir is not None else db_path.parent / BACKUP_DIRECTORY_NAME
   stamp = moment.strftime("%Y%m%dT%H%M%S%fZ")
   tables_named = "-".join(sorted(table_names))
   target = directory / f"{RETIRE_BACKUP_PREFIX}{tables_named}-{stamp}{BACKUP_SUFFIX}"
   copy_database(db_path, target)

   return target
