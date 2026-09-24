"""Engine credit from a graded free-response answer: applied only in a unit check, only from points
the grader published, and reversible (03, "What the student sees for a provisional grade": the
dispute reverses any credit the point produced)."""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.grading import service

ITEM_SKILLS = ("BC-SKL-05010", "BC-SKL-05020", "BC-SKL-05039")


def skill_rows(world):
   with OrmSession(world.engine) as db:
      rows = db.scalars(
         select(models.SkillState)
         .where(models.SkillState.user_id == world.user_id)
         .where(models.SkillState.skill_id.in_(ITEM_SKILLS))
      ).all()

      return {row.skill_id: (row.credited_successes, row.credited_failures, row.observation_count) for row in rows}


def graded_attempt(world):
   attempt_id = world.open_attempt()
   world.upload(attempt_id, "critical_point_full__clean.jpg")
   world.client.post(f"/attempts/{attempt_id}/transcription")
   world.client.post(f"/attempts/{attempt_id}/transcription/confirm", json={"confidence": "confident"})

   return attempt_id


def test_a_graded_unit_check_answer_credits_the_engine_and_the_credit_can_be_reversed(frq_world):
   before = skill_rows(frq_world)
   attempt_id = graded_attempt(frq_world)
   credited = skill_rows(frq_world)

   assert credited != before
   assert all(credited[skill][2] == before[skill][2] + 1 for skill in ITEM_SKILLS)

   with OrmSession(frq_world.engine) as db:
      attempt = db.get(models.Attempt, attempt_id)
      reversed_rows = service.reverse_credit(db, attempt, frq_world.user_id, datetime.now(timezone.utc))
      db.commit()

   assert reversed_rows > 0
   assert skill_rows(frq_world) == before


def test_a_point_still_provisional_moves_no_credit_for_its_skill(frq_world):
   frq_world.provider.grader_answers = {
      "b1": {"temp0_a": "earned", "temp0_b": "not_earned", "strict": "not_earned"},
      "b2": {"temp0_a": "earned", "temp0_b": "not_earned", "strict": "not_earned"},
   }
   before = skill_rows(frq_world)
   graded_attempt(frq_world)
   after = skill_rows(frq_world)

   assert after["BC-SKL-05039"][:2] == before["BC-SKL-05039"][:2]
   assert after["BC-SKL-05010"][:2] != before["BC-SKL-05010"][:2]
