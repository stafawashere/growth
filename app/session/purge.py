"""The full purge (docs/plan/09-security-and-privacy.md, Audit log and the default purge).

audit_log is deleted only by the full purge, and the purge writes itself as the final entry
before the store is emptied, so the audit row is written first here and every other table is
emptied afterward, audit_log last of all.

Which rows are the student's is the export's classification (app/export/archive.py owner_clause),
read from the schema, so a table the export carries is a table the purge empties. Every owned row
is resolved before any is deleted, because attempts and the tables beneath them reach the student
through sessions. The export archive files and their jobs rows go too: the export exists to be
downloaded before the purge, and a copy left on disk would outlive a purge 09 calls irreversible.

Two shared tables the export leaves out still hold rows about the student, and the purge removes
them: a jobs row whose payload names the student (a tutor call queued behind a usage limit carries
the student's own feedback text), and a review_queue row whose ref_id is one of the student's rows
(a split or disputed grading point). Rows of either table about anything else stay.
"""
import json

import uuid

from sqlalchemy import delete, select, tuple_

from app.audit.vocabulary import is_known_action
from app.db import models
from app.export import archive

PURGE_ACTION = "purge"
AUDIT_TABLE = models.AuditLog.__table__
EXPORT_JOBS_KEY = "jobs"
STUDENT_JOBS_KEY = "queued_jobs"
REVIEWS_KEY = "review_queue"


def write_purge_audit_entry(db, user_id, now):
   if not is_known_action(PURGE_ACTION):
      raise ValueError(f"{PURGE_ACTION!r} is not in the audit_log vocabulary")

   entry = models.AuditLog(
      id=f"AUD-{uuid.uuid4().hex}",
      at=now.isoformat(),
      actor=user_id,
      action=PURGE_ACTION,
      subject=f"users:{user_id}",
      created_at=now.isoformat(),
      updated_at=now.isoformat(),
   )
   db.add(entry)
   db.flush()


def owned_primary_keys(db, table, user_id):
   clause = archive.owner_clause(table, user_id)
   is_unowned = clause is None

   if is_unowned:
      return None

   key_columns = list(table.primary_key.columns)

   return [tuple(row) for row in db.execute(select(*key_columns).where(clause))]


def delete_rows(db, table, primary_keys):
   has_rows = len(primary_keys) > 0

   if not has_rows:
      return 0

   key_columns = list(table.primary_key.columns)
   has_single_key = len(key_columns) == 1

   if has_single_key:
      matches_owned_row = key_columns[0].in_([key[0] for key in primary_keys])
   else:
      matches_owned_row = tuple_(*key_columns).in_(primary_keys)

   return db.execute(delete(table).where(matches_owned_row)).rowcount


def delete_exports(db, user_id):
   export_jobs = archive.export_jobs_for(db, user_id)

   try:
      archive_directory = archive.archive_directory_for(db.get_bind().engine)
   except archive.ExportUnavailable:
      archive_directory = None

   has_archive_directory = archive_directory is not None

   if has_archive_directory:
      archive.remove_previous_exports(db, archive_directory, user_id)
   else:
      for job in export_jobs:
         db.delete(job)

      db.flush()

   return len(export_jobs)


def owned_single_keys(owned_by_table):
   keys = set()

   for table, primary_keys in owned_by_table.items():
      has_single_key = len(table.primary_key.columns) == 1

      if has_single_key:
         keys.update(key[0] for key in primary_keys)

   return keys


def names_the_student(payload_text, user_id):
   try:
      payload = json.loads(payload_text)
   except ValueError:
      return False

   is_object = isinstance(payload, dict)

   return is_object and payload.get("user_id") == user_id


def delete_student_jobs(db, user_id):
   student_jobs = [job for job in db.scalars(select(models.Job)) if names_the_student(job.payload, user_id)]

   for job in student_jobs:
      db.delete(job)

   db.flush()

   return len(student_jobs)


def delete_reviews_of(db, owned_keys):
   has_keys = len(owned_keys) > 0

   if not has_keys:
      return 0

   review_ids = [
      row.id
      for row in db.scalars(select(models.ReviewQueue))
      if row.ref_id in owned_keys
   ]

   return delete_rows(db, models.ReviewQueue.__table__, [(review_id,) for review_id in review_ids])


def purge_user(db, user_id, now):
   write_purge_audit_entry(db, user_id, now)

   owned_by_table = {}

   for table in models.Base.metadata.sorted_tables:
      primary_keys = owned_primary_keys(db, table, user_id)
      is_owned = primary_keys is not None

      if is_owned:
         owned_by_table[table] = primary_keys

   counts = {}

   for table, primary_keys in owned_by_table.items():
      is_audit_log = table is AUDIT_TABLE

      if not is_audit_log:
         counts[table.name] = delete_rows(db, table, primary_keys)

   counts[EXPORT_JOBS_KEY] = delete_exports(db, user_id)
   counts[STUDENT_JOBS_KEY] = delete_student_jobs(db, user_id)
   counts[REVIEWS_KEY] = delete_reviews_of(db, owned_single_keys(owned_by_table))
   counts[AUDIT_TABLE.name] = delete_rows(db, AUDIT_TABLE, owned_by_table.get(AUDIT_TABLE, []))
   db.flush()

   return counts