"""A diagnosis whose top two hypotheses are close schedules a probe in pending_probes, and the next
micro-session drains it before its own scoring (03, R6)."""
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.grading import service


def diagnosis_result(probe):
   return {
      "observed_errors": [],
      "candidate_misconceptions": [],
      "non_conceptual_causes": [],
      "prerequisite_gaps": [],
      "per_skill_mastery_state": [],
      "recommended_probe": probe,
   }


def test_a_recommended_probe_is_queued_and_the_next_session_drains_it(frq_world):
   attempt_id = frq_world.open_attempt()
   now = datetime.now(timezone.utc)
   probe = {"archetype_id": "BC-QA-04003", "reason": "rival_pair", "separates": ["BC-MIS-99001", "BC-MIS-04005"]}

   with OrmSession(frq_world.engine) as db:
      attempt = db.get(models.Attempt, attempt_id)
      service.write_diagnosis(db, attempt, diagnosis_result(probe), service.DIAGNOSED_BY_MODEL, now)
      service.write_diagnosis(db, attempt, diagnosis_result(None), service.DIAGNOSED_BY_MODEL, now)
      stale = models.PendingProbe(
         id="PRB-stale",
         user_id=frq_world.user_id,
         archetype_id="BC-QA-02006",
         diagnosis_id="DGN-stale",
         enqueued_at=(now - timedelta(days=9)).isoformat(),
         expires_at=(now - timedelta(days=2)).isoformat(),
         served_at=None,
         created_at=now.isoformat(),
         updated_at=now.isoformat(),
      )
      db.add(stale)
      db.commit()
      queued = db.scalars(select(models.PendingProbe).where(models.PendingProbe.id != "PRB-stale")).all()

   assert [row.archetype_id for row in queued] == ["BC-QA-04003"]
   assert queued[0].served_at is None

   opened = frq_world.client.post("/sessions", json={"mode": "learning", "today": date.today().isoformat()})

   assert opened.status_code == 200

   with OrmSession(frq_world.engine) as db:
      drained = db.get(models.PendingProbe, queued[0].id)
      untouched = db.get(models.PendingProbe, "PRB-stale")

   assert drained.served_at is not None
   assert untouched.served_at is None
