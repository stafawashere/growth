"""Writes content_snapshots rows, per docs/plan/06-architecture.md "Versioning"."""
import json
import uuid
from datetime import datetime, timezone

from app.db.models import ContentSnapshot


def _now_iso():
   return datetime.now(timezone.utc).isoformat()


def active_snapshot_rows(db_session):
   return (
      db_session.query(ContentSnapshot)
      .filter(ContentSnapshot.status == "active")
      .all()
   )


def record_snapshot(db_session, snapshot, library_commit=None, loaded_at=None, row_id=None):
   """row_id lets a reload name the new row before it exists, so skills_state rows reconciled in
   their own transactions can point at it (app/content/reload.py)."""
   active_rows = active_snapshot_rows(db_session)
   unchanged_row = next(
      (row for row in active_rows if row.digest == snapshot.digest),
      None,
   )

   if unchanged_row is not None:
      timestamp = _now_iso()
      unchanged_row.loaded_at = loaded_at or timestamp
      unchanged_row.library_commit = library_commit
      unchanged_row.counts = json.dumps(snapshot.counts)
      unchanged_row.updated_at = timestamp
      db_session.flush()

      return unchanged_row

   for active_row in active_rows:
      active_row.status = "superseded"
      active_row.updated_at = _now_iso()

   timestamp = _now_iso()
   row = ContentSnapshot(
      id=row_id or uuid.uuid4().hex,
      loaded_at=loaded_at or timestamp,
      library_commit=library_commit,
      digest=snapshot.digest,
      counts=json.dumps(snapshot.counts),
      status="active",
      rejection_reason=None,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db_session.add(row)
   db_session.flush()

   return row


def record_rejected_snapshot(db_session, digest, reason):
   timestamp = _now_iso()
   row = ContentSnapshot(
      id=uuid.uuid4().hex,
      loaded_at=timestamp,
      library_commit=None,
      digest=digest,
      counts=json.dumps({}),
      status="rejected",
      rejection_reason=reason,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db_session.add(row)
   db_session.flush()

   return row
