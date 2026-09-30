"""A served drill row goes with the student at purge and another user's stays
(docs/calculator/architecture.md, Purge, export and retention)."""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.calculator_drills import service
from app.db import models
from app.session import purge

USER_ID = "USER-0001"
OTHER_USER_ID = "USR-other"
NOW = datetime(2026, 9, 29, 12, 0, 0, tzinfo=timezone.utc)


def test_purge_removes_the_students_drills_and_keeps_another_users(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      mine = service.serve(db, USER_ID, "value", now=NOW)
      theirs = service.serve(db, OTHER_USER_ID, "value", now=NOW)
      service.answer(db, USER_ID, mine["drill_id"], "1.000", None, 1000, True, now=NOW)
      db.commit()

   with OrmSession(engine) as db:
      counts = purge.purge_user(db, USER_ID, NOW)
      db.commit()

   with OrmSession(engine) as db:
      remaining = db.scalars(select(models.CalculatorDrill.id)).all()

   assert counts["calculator_drills"] == 1
   assert remaining == [theirs["drill_id"]]
