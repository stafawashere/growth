"""A dated copy of the SQLite database taken each time the server starts.

var/growth.db is gitignored and holds the only record of a student's attempts, so the server
copies it before it opens it. One copy per day is kept, the first of that day, because a restart
later in the day should not replace a good morning copy with an afternoon one that already holds
whatever went wrong. The oldest copies past the keep count are removed.
"""
import sqlite3
from datetime import date
from pathlib import Path

BACKUP_PREFIX = "growth-"
BACKUP_SUFFIX = ".db"
DEFAULT_KEEP = 14


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

   for stale in dated_backups(backup_dir)[:-keep]:
      stale.unlink()

   return target