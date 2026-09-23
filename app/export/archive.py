"""The export archive of docs/plan/09-security-and-privacy.md, "Default purge 30 days after the exam
date, with an export first": everything in 09's data inventory, as JSON.

Which tables are the student's is read from the schema rather than listed. users is the root, any
table with user_id is the student's by that column, and a table with session_id or attempt_id
reaches the student through sessions or attempts. audit_log has none of these and is in 09's
table, so its rows go in when the actor is the student or one of the non-user actors: 09 gives the
actor as "user identifier, worker, or system", and app/review/audit.py writes as operator. In the
single-student deployment those entries are still the student's record. The actors are named rather
than inferred from the users table, because another user's entries must stay out even after that
user's row is gone. Every other table
stays out: 09 calls items "not personal data", and content_snapshots, review_queue, jobs and
item_verifications are not in its table.

Secret columns are left out by name. 09's Audit log excludes any key or any part of one, the
passphrase and a raw provider response body, 06 keeps provider key material to provider_configs,
and the auth layer stores its tokens and recovery code only as hashes. So a column is left out when
any underscore-separated word of its name is key (or ends in key, as apikey does), ciphertext,
nonce, hash, passphrase, password, secret or token, or when the name carries response_body or
raw_response. public_key is kept: a WebAuthn public key is public by construction and is part of
the credential record 09 lists.

The archive bytes are a file in an exports directory beside the SQLite database, and a jobs row of
type export (06, API surface: POST /export triggers an export job) records the owner and the file.
P1 has no worker, so the job is produced inline and written as done. A student holds one archive
at a time: a new export replaces the previous file and row, so copies of the record do not pile up
beside a database whose purpose ends on exam day. The new file is written and the new row committed
before the old file is removed, so a failure part way leaves the previous export whole. Archives
are readable by the owning account only (file 0600, directory 0700), because they hold the whole
record of a minor learner.
"""
import base64
import json
import os
from pathlib import Path

from sqlalchemy import select

from app.auth.service import as_iso, new_id, write_audit
from app.db import models

EXPORT_ACTION = "export_produced"
EXPORT_JOB_TYPE = "export"
EXPORT_JOB_DONE = "done"
FORMAT_VERSION = 1
EXPORTS_DIRECTORY_NAME = "exports"
ARCHIVE_FILE_MODE = 0o600
ARCHIVE_DIRECTORY_MODE = 0o700
SECRET_NAME_WORDS = ("key", "ciphertext", "nonce", "hash", "passphrase", "password", "secret", "token")
SECRET_NAME_FRAGMENTS = ("response_body", "raw_response")
PUBLIC_COLUMN_NAMES = ("public_key",)
NON_USER_ACTORS = ("worker", "system", "operator")
USERS_TABLE = models.User.__table__
AUDIT_TABLE = models.AuditLog.__table__


class ExportUnavailable(RuntimeError):
   pass


def is_secret_word(word):
   is_listed = word in SECRET_NAME_WORDS
   is_run_on_key = word.endswith("key")

   return is_listed or is_run_on_key


def is_secret_column(column_name):
   is_public = column_name in PUBLIC_COLUMN_NAMES

   if is_public:
      return False

   has_secret_word = any(is_secret_word(word) for word in column_name.lower().split("_"))
   has_secret_fragment = any(fragment in column_name.lower() for fragment in SECRET_NAME_FRAGMENTS)

   return has_secret_word or has_secret_fragment


def archive_directory_for(engine):
   database_path = engine.url.database
   is_file_backed = database_path not in (None, "", ":memory:")

   if not is_file_backed:
      raise ExportUnavailable("an export needs a file-backed database to sit beside")

   return Path(database_path).resolve().parent / EXPORTS_DIRECTORY_NAME


def owner_clause(table, user_id):
   column_names = {column.name for column in table.columns}
   session_ids = select(models.Session.id).where(models.Session.user_id == user_id)
   attempt_ids = select(models.Attempt.id).where(models.Attempt.session_id.in_(session_ids))

   if table is USERS_TABLE:
      return table.c.id == user_id

   if "user_id" in column_names:
      return table.c.user_id == user_id

   if "session_id" in column_names:
      return table.c.session_id.in_(session_ids)

   if "attempt_id" in column_names:
      return table.c.attempt_id.in_(attempt_ids)

   if table is AUDIT_TABLE:
      return table.c.actor.in_((user_id, *NON_USER_ACTORS))

   return None


def exportable_value(value):
   if isinstance(value, bytes):
      return base64.b64encode(value).decode()

   return value


def exported_rows(db, table, clause):
   kept_columns = [column for column in table.columns if not is_secret_column(column.name)]
   ordering = list(table.primary_key.columns)
   statement = select(*kept_columns).where(clause).order_by(*ordering)

   return [
      {name: exportable_value(value) for name, value in row._mapping.items()}
      for row in db.execute(statement)
   ]


def build_archive(db, user_id, produced_at):
   tables = {}

   for table in models.Base.metadata.sorted_tables:
      clause = owner_clause(table, user_id)
      is_exported = clause is not None

      if is_exported:
         tables[table.name] = exported_rows(db, table, clause)

   return {
      "format_version": FORMAT_VERSION,
      "produced_at": produced_at,
      "user": {"id": user_id},
      "tables": tables,
   }


def export_jobs_for(db, user_id):
   jobs = db.scalars(select(models.Job).where(models.Job.type == EXPORT_JOB_TYPE)).all()

   return [job for job in jobs if json.loads(job.payload).get("user_id") == user_id]


def archive_path_for(archive_directory, job):
   archive_name = json.loads(job.payload).get("archive")
   has_archive_name = isinstance(archive_name, str) and archive_name != ""

   if not has_archive_name:
      return None

   return archive_directory / archive_name


def remove_archive_files(paths):
   for path in paths:
      path.unlink(missing_ok=True)


def remove_previous_exports(db, archive_directory, user_id):
   for job in export_jobs_for(db, user_id):
      archive_path = archive_path_for(archive_directory, job)
      has_archive = archive_path is not None

      if has_archive:
         archive_path.unlink(missing_ok=True)

      db.delete(job)

   db.flush()


def write_archive_file(path, text):
   descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, ARCHIVE_FILE_MODE)

   with os.fdopen(descriptor, "w") as handle:
      handle.write(text)


def produce_export(db, archive_directory, user_id, now):
   """Commits the session, because the previous archive may only be removed once the new one is
   durable."""
   timestamp = as_iso(now)
   stale_jobs = export_jobs_for(db, user_id)
   stale_paths = [archive_path_for(archive_directory, job) for job in stale_jobs]
   stale_archive_paths = [path for path in stale_paths if path is not None]

   job_id = new_id("JOB")
   archive_name = f"{job_id}.json"
   new_archive_path = archive_directory / archive_name
   write_audit(db, user_id, EXPORT_ACTION, f"jobs:{job_id}", None, now)
   archive = build_archive(db, user_id, timestamp)

   is_committed = False

   try:
      archive_directory.mkdir(mode=ARCHIVE_DIRECTORY_MODE, parents=True, exist_ok=True)
      write_archive_file(new_archive_path, json.dumps(archive, sort_keys=True))

      for stale_job in stale_jobs:
         db.delete(stale_job)

      db.flush()

      job = models.Job(
         id=job_id,
         type=EXPORT_JOB_TYPE,
         payload=json.dumps({"user_id": user_id, "archive": archive_name}),
         idempotency_key=f"{EXPORT_JOB_TYPE}:{user_id}",
         state=EXPORT_JOB_DONE,
         not_before=timestamp,
         created_at=timestamp,
         updated_at=timestamp,
      )
      db.add(job)
      db.flush()
      db.commit()
      is_committed = True
   finally:
      if not is_committed:
         new_archive_path.unlink(missing_ok=True)

   remove_archive_files(stale_archive_paths)

   return job


def read_export(db, archive_directory, user_id, export_id):
   job = db.get(models.Job, export_id)
   is_missing = job is None or job.type != EXPORT_JOB_TYPE

   if is_missing:
      return None

   payload = json.loads(job.payload)
   is_owner = payload.get("user_id") == user_id

   if not is_owner:
      return None

   archive_path = archive_path_for(archive_directory, job)
   archive_exists = archive_path is not None and archive_path.is_file()

   if not archive_exists:
      return None

   return archive_path.read_bytes()