"""The full purge (docs/plan/09-security-and-privacy.md, Audit log).

audit_log is deleted only by the full purge, and the purge writes itself as the final entry
before the store is emptied, so the audit row is written first here and every other table is
emptied afterward, audit_log last of all.
"""
import uuid

from sqlalchemy import select

from app.audit.vocabulary import is_known_action
from app.db import models

PURGE_ACTION = "purge"

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


def delete_by_column(db, model, column, value):
   rows = db.scalars(select(model).where(column == value)).all()
   count = len(rows)

   for row in rows:
      db.delete(row)

   return count


def delete_attempts_for_sessions(db, session_ids):
   has_sessions = len(session_ids) > 0

   if not has_sessions:
      return 0

   rows = db.scalars(
      select(models.Attempt).where(models.Attempt.session_id.in_(session_ids))
   ).all()
   count = len(rows)

   for row in rows:
      db.delete(row)

   return count


def purge_user(db, user_id, now):
   write_purge_audit_entry(db, user_id, now)

   counts = {}
   session_rows = db.scalars(
      select(models.Session).where(models.Session.user_id == user_id)
   ).all()
   session_ids = [row.id for row in session_rows]

   counts["attempts"] = delete_attempts_for_sessions(db, session_ids)
   counts["sessions"] = delete_by_column(db, models.Session, models.Session.user_id, user_id)
   counts["judgments"] = delete_by_column(db, models.Judgment, models.Judgment.user_id, user_id)
   counts["pending_probes"] = delete_by_column(
      db, models.PendingProbe, models.PendingProbe.user_id, user_id
   )
   counts["skills_state"] = delete_by_column(
      db, models.SkillState, models.SkillState.user_id, user_id
   )
   counts["provider_configs"] = delete_by_column(
      db, models.ProviderConfig, models.ProviderConfig.user_id, user_id
   )
   counts["budgets"] = delete_by_column(db, models.Budget, models.Budget.user_id, user_id)
   counts["users"] = delete_by_column(db, models.User, models.User.id, user_id)

   counts["passkey_credentials"] = delete_by_column(
      db, models.PasskeyCredential, models.PasskeyCredential.user_id, user_id
   )
   counts["auth_sessions"] = delete_by_column(
      db, models.AuthSession, models.AuthSession.user_id, user_id
   )

   all_audit_rows = db.scalars(select(models.AuditLog)).all()
   counts["audit_log"] = len(all_audit_rows)

   for row in all_audit_rows:
      db.delete(row)

   db.flush()

   return counts
