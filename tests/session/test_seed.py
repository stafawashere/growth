"""Tests for app/session/seed.py against the live data/ content, per docs/plan/06-architecture.md
skills_state and Q8/Q2 in docs/plan/11-phased-delivery.md.
"""
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db import models
from app.engine.prior import beta_for_skill
from app.session import repository, seed

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = REPO_ROOT / "data"
USER_ID = "USER-0001"
CREATED_AT = datetime(2026, 1, 1, 9, 0, 0, tzinfo=timezone.utc)


@pytest.fixture(scope="module")
def snapshot():
   return load_snapshot(DATA_ROOT)


def test_seed_writes_618_rows_with_83_mastered(tmp_path, snapshot):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      written = seed.seed_skills_state(db, USER_ID, snapshot, CREATED_AT)
      db.commit()

      rows = db.query(models.SkillState).filter(models.SkillState.user_id == USER_ID).all()
      skill_ids = {row.skill_id for row in rows}
      mastered_rows = [row for row in rows if row.mastered == 1]

      assert written == 618
      assert len(rows) == 618
      assert len(mastered_rows) == 83
      assert not any(skill_id.startswith("BC-TOP") for skill_id in skill_ids)


def test_seed_beta_matches_prior(tmp_path, snapshot):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      seed.seed_skills_state(db, USER_ID, snapshot, CREATED_AT)
      db.commit()

      states = repository.load_states(db, USER_ID)

   external_parent = "BC-SKL-01018"

   assert states[external_parent].mastered is True
   assert states[external_parent].beta == 0.0

   unmastered_skill_id = next(
      skill_id
      for skill_id, state in states.items()
      if skill_id.startswith("BC-SKL") and not state.mastered
   )
   expected_beta = beta_for_skill(unmastered_skill_id, snapshot.archetypes)

   assert states[unmastered_skill_id].beta == pytest.approx(expected_beta)


def test_seed_refuses_second_run(tmp_path, snapshot):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      seed.seed_skills_state(db, USER_ID, snapshot, CREATED_AT)
      db.commit()

      with pytest.raises(ValueError):
         seed.seed_skills_state(db, USER_ID, snapshot, CREATED_AT)
