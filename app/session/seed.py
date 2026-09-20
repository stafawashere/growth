"""skills_state seeding at account creation, per docs/plan/06-architecture.md, skills_state.

One row per BC-SKL and one row per BC-PRQ, 618 rows in every phase including P1 (R27). BC-TOP
ids get no row at all (R13). All 77 BC-PRQ rows are inserted mastered (invariant 19). The 6
external BC-SKL parents also start mastered, per Q8 in docs/plan/11-phased-delivery.md.
"""
from app.engine.prior import beta_for_skill
from app.engine.state import SkillState
from app.session import repository

SEEDED_PARENT_IDS = frozenset({
   "BC-SKL-01018",
   "BC-SKL-01039",
   "BC-SKL-01044",
   "BC-SKL-02001",
   "BC-SKL-02002",
   "BC-SKL-03001",
})


def has_existing_rows(db, user_id):
   states = repository.load_states(db, user_id)

   return len(states) > 0


def seed_skills_state(db, user_id, snapshot, created_at, snapshot_id=None):
   """Q8: all 77 BC-PRQ plus the 6 external BC-SKL parents start mastered (invariant 19, R15).

   Every other BC-SKL row starts unmastered with beta from beta_for_skill over the snapshot's
   active archetypes (Q2). Refuses if the user already has any skills_state row.
   snapshot_id is the content_snapshots row id (06 correction in the ledger); the digest is the
   fallback when no row has been recorded yet.
   """
   already_seeded = has_existing_rows(db, user_id)

   if already_seeded:
      raise ValueError(f"user {user_id} already has skills_state rows")

   states = {}

   for prq_id in snapshot.prerequisites:
      states[prq_id] = SkillState.seeded_mastered(prq_id, created_at)

   for skill_id in snapshot.skills:
      is_seeded_parent = skill_id in SEEDED_PARENT_IDS

      if is_seeded_parent:
         states[skill_id] = SkillState.seeded_mastered(skill_id, created_at)
         continue

      states[skill_id] = SkillState(
         skill_id=skill_id,
         beta=beta_for_skill(skill_id, snapshot.archetypes),
      )

   row_id = snapshot_id or snapshot.digest
   repository.save_states(db, user_id, states, snapshot_id=row_id, now=created_at)

   return len(states)
