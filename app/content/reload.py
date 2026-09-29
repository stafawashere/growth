"""snapshot_reload, per docs/plan/06-architecture.md "Library updates and retired IDs".

A load whose digest matches the active content_snapshots row changes no skills_state row. A load
with a new digest reconciles every user's rows against data/ids.json first, one transaction per
user, and only then makes the new row active and writes content_snapshot_reloaded. Any row the
reload would refuse over is found before anything is written, so a refusal leaves the old
snapshot active and every row as it was, with the refusal kept as a rejected content_snapshots
row. The new row's id is fixed before the per-user transactions, so if the process stops part way
the old snapshot is still active, the next start sees a new digest again, and the users already
reconciled are simply kept.
"""
import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.auth.service import write_audit
from app.content.persist import active_snapshot_rows, record_rejected_snapshot, record_snapshot
from app.content.reconcile import ReloadRefused, ReloadReport, reconcile_skills_state, refusals
from app.db import models

RELOAD_ACTION = "content_snapshot_reloaded"

RELOAD_ACTOR = "worker"


def reconciled_user_ids(db):
   statement = select(models.SkillState.user_id).distinct().order_by(models.SkillState.user_id)

   return db.scalars(statement).all()


def report_counts(report, users):
   return {
      "users": users,
      "kept": len(report.kept),
      "rewritten": len(report.rewritten),
      "merged": len(report.merged),
      "orphaned": len(report.orphaned),
   }


def add_report(total, report):
   total.kept.extend(report.kept)
   total.rewritten.extend(report.rewritten)
   total.merged.extend(report.merged)
   total.orphaned.extend(report.orphaned)
   total.notes.extend(report.notes)


def reload_snapshot(engine, snapshot, library_commit=None, loaded_at=None, today=None):
   """Returns the id of the content_snapshots row now active. Raises ReloadRefused."""
   day = today or date.today()

   with OrmSession(engine) as db:
      active_rows = active_snapshot_rows(db)
      has_active = len(active_rows) > 0
      digest_changed = has_active and all(row.digest != snapshot.digest for row in active_rows)

      if not digest_changed:
         row = record_snapshot(db, snapshot, library_commit=library_commit, loaded_at=loaded_at)
         db.commit()

         return row.id

      previous_digest = active_rows[0].digest
      found = refusals(db, snapshot, snapshot.ids)
      is_refused = len(found) > 0

      if is_refused:
         reason = "; ".join(found)
         record_rejected_snapshot(db, snapshot.digest, reason)
         db.commit()

         raise ReloadRefused(reason)

      user_ids = reconciled_user_ids(db)

   new_row_id = uuid.uuid4().hex
   total = ReloadReport()

   for user_id in user_ids:
      with OrmSession(engine) as db:
         report = reconcile_skills_state(
            db, snapshot, snapshot.ids, day, new_row_id, actor=RELOAD_ACTOR, user_id=user_id
         )
         db.commit()

      add_report(total, report)

   with OrmSession(engine) as db:
      row = record_snapshot(
         db, snapshot, library_commit=library_commit, loaded_at=loaded_at, row_id=new_row_id
      )
      detail = {
         "previous_digest": previous_digest,
         "digest": snapshot.digest,
         **report_counts(total, len(user_ids)),
      }
      write_audit(db, RELOAD_ACTOR, RELOAD_ACTION, f"content_snapshots:{row.id}", detail)
      db.commit()

      return row.id
