"""The student's submitted attempts as plain records, the one read every P7 metric and every A/B
analysis starts from, so the definitions in docs/plan/10 "Learning-outcome metrics" are computed
over the same rows everywhere.

Attempts in a diagnostic session are left out: they place the student rather than practise, and
the diagnostic shows no verdict. Checkpoint and concept probe responses live in their own tables
and never appear here.
"""
import json
from dataclasses import dataclass
from datetime import date

from sqlalchemy import select

from app.db import models
from app.engine.prior import primary_skill

DIAGNOSTIC_MODE = "diagnostic"


@dataclass(frozen=True)
class AttemptRecord:
   id: str
   session_id: str
   session_mode: str
   item_id: str
   archetype_id: str
   primary_skill: str | None
   skills: tuple
   submitted_at: str
   correct: bool | None
   confidence: str | None
   confidence_source: str | None
   elapsed_ms: int | None
   served_stage: str
   format: str
   response: dict
   experiment_arms: dict
   image_ids: str | None
   transcription_confirmed: bool
   updates_mastery: bool

   @property
   def day(self):
      return date.fromisoformat(self.submitted_at[:10])


def load_attempts(db, user_id, archetypes):
   rows = db.execute(
      select(models.Attempt, models.Session.mode, models.Session.updates_mastery, models.Item.archetype_id)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .join(models.Item, models.Item.id == models.Attempt.item_id, isouter=True)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.submitted_at.is_not(None))
      .order_by(models.Attempt.submitted_at, models.Attempt.id)
   ).all()
   records = []

   for attempt, mode, updates_mastery, archetype_id in rows:
      is_diagnostic = mode == DIAGNOSTIC_MODE

      if is_diagnostic:
         continue

      archetype = archetypes.get(archetype_id) if archetype_id else None
      skills = tuple(archetype["skills"]) if archetype else ()
      records.append(
         AttemptRecord(
            id=attempt.id,
            session_id=attempt.session_id,
            session_mode=mode,
            item_id=attempt.item_id,
            archetype_id=archetype_id or "",
            primary_skill=primary_skill(archetype) if archetype else None,
            skills=skills,
            submitted_at=attempt.submitted_at,
            correct=None if attempt.correct is None else bool(attempt.correct),
            confidence=attempt.confidence,
            confidence_source=attempt.confidence_source,
            elapsed_ms=attempt.elapsed_ms,
            served_stage=attempt.served_stage,
            format=attempt.format,
            response=json.loads(attempt.response) if attempt.response else {},
            experiment_arms=json.loads(attempt.experiment_arms) if attempt.experiment_arms else {},
            image_ids=attempt.image_ids,
            transcription_confirmed=bool(attempt.transcription_confirmed),
            updates_mastery=bool(updates_mastery),
         )
      )

   return records
