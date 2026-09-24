"""pending_probes between the table and the engine's queue (02 R6, 03 "Rival handling and the probe
trigger"). The diagnostician writes rows; a micro-session loads the live ones, at most
PROBE_QUEUE_MAX and oldest first, lets app/engine/fringe.py drain_probe_queue pop the front one
before its own scoring, and marks every row the drain consumed as served, so a probe is served
once and an expired one is never loaded again.
"""
from datetime import datetime

from sqlalchemy import select

from app.db import models
from app.engine import constants
from app.engine.state import PendingProbe


def live_rows(db, user_id, now):
   rows = db.scalars(
      select(models.PendingProbe)
      .where(models.PendingProbe.user_id == user_id)
      .where(models.PendingProbe.served_at.is_(None))
      .order_by(models.PendingProbe.enqueued_at)
   ).all()
   unexpired = [row for row in rows if datetime.fromisoformat(row.expires_at) > now]

   return unexpired[-constants.PROBE_QUEUE_MAX:]


def load_queue(db, user_id, now):
   """The engine's clock is naive (app/engine/select.py session_now), so enqueued_at is handed over
   without its zone; now is the aware wall clock the expiry is compared with."""
   rows = live_rows(db, user_id, now)
   queue = [
      PendingProbe(
         archetype_id=row.archetype_id,
         diagnosis_id=row.diagnosis_id,
         enqueued_at=datetime.fromisoformat(row.enqueued_at).replace(tzinfo=None),
      )
      for row in rows
   ]

   return rows, queue


def mark_drained(db, rows, remaining, now):
   left = {probe.diagnosis_id for probe in remaining}
   stamp = now.isoformat()

   for row in rows:
      was_drained = row.diagnosis_id not in left

      if was_drained:
         row.served_at = stamp
         row.updated_at = stamp

   db.flush()
