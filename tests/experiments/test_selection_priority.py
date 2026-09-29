"""The selection_priority switch of docs/pedagogy/today/design.md D2, whose unit is the session."""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine.priority import retrievability_priority_ordering
from app.experiments import switches

NOW = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)
USER = "USR-1"
SESSION_ID = "SES-0001"


def test_the_switch_view_lists_selection_priority_with_its_arms(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")

   with OrmSession(engine) as db:
      views = {view["name"]: view for view in switches.switch_view(db, USER, {}, NOW)}

   view = views[switches.SELECTION_PRIORITY]

   assert view["unit"] == "session"
   assert view["arms"] == ["two_term", "retrievability_priority"]
   assert view["state"] == switches.OFF


def test_randomised_assigns_a_session_once(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")
   later = NOW + timedelta(hours=2)

   with OrmSession(engine) as db:
      switches.set_state(db, USER, switches.SELECTION_PRIORITY, switches.RANDOMISED, {}, NOW)
      first = switches.selection_ordering(db, USER, SESSION_ID, {}, NOW)
      again = switches.selection_ordering(db, USER, SESSION_ID, {}, later)
      stored = (
         db.query(models.ExperimentAssignment)
         .filter(models.ExperimentAssignment.experiment == switches.SELECTION_PRIORITY)
         .all()
      )

   assert len(stored) == 1
   assert stored[0].unit_id == SESSION_ID
   assert again == first
   assert first in ((None, None), (retrievability_priority_ordering, retrievability_priority_ordering))


def test_the_preview_reads_a_randomised_arm_without_assigning_it(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")

   with OrmSession(engine) as db:
      switches.set_state(db, USER, switches.SELECTION_PRIORITY, switches.RANDOMISED, {}, NOW)
      switches.selection_ordering(db, USER, "2026-10-01", {}, NOW, assigns=False)
      stored = db.query(models.ExperimentAssignment).count()

   assert stored == 0
