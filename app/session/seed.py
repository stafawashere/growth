"""skills_state seeding at account creation, per docs/plan/06-architecture.md, skills_state.

One row per BC-SKL and one row per BC-PRQ, 618 rows in every phase including P1 (R27). BC-TOP
ids get no row at all (R13). All 77 BC-PRQ rows are inserted mastered (invariant 19). Every BC-SKL
row starts unmastered. Q8 in docs/plan/11-phased-delivery.md also seeded six BC-SKL parents
mastered, which was a P1 subgraph device: on the whole graph they are ordinary skills, and the
P7 simulation found about half of them not known by a synthetic student, so mastery of a BC-SKL
now comes only from the diagnostic's placement or from practice.
"""
from app.engine.prior import beta_for_skill
from app.engine.state import SkillState
from app.session import repository


def has_existing_rows(db, user_id):
   states = repository.load_states(db, user_id)

   return len(states) > 0


def seed_skills_state(db, user_id, snapshot, created_at, snapshot_id=None):
   """All 77 BC-PRQ start mastered (invariant 19, R15).

   Every BC-SKL row starts unmastered with beta from beta_for_skill over the snapshot's
   active archetypes (Q2). Refuses if the user already has any skills_state row.
   snapshot_id is the content_snapshots row id (06 correction in the ledger); the digest is the
   fallback when no row has been recorded yet.
   """
   already_seeded = has_existing_rows(db, user_id)

   if already_seeded:
      raise ValueError(f"user {user_id} already has skills_state rows")

   states = initial_states(snapshot, created_at)
   row_id = snapshot_id or snapshot.digest
   repository.save_states(db, user_id, states, snapshot_id=row_id, now=created_at)

   return len(states)


def initial_states(snapshot, created_at):
   """The seeded state vector itself, which the whole-graph simulation starts every student from."""
   states = {}

   for prq_id in snapshot.prerequisites:
      states[prq_id] = SkillState.seeded_mastered(prq_id, created_at)

   for skill_id in snapshot.skills:
      states[skill_id] = SkillState(
         skill_id=skill_id,
         beta=beta_for_skill(skill_id, snapshot.archetypes),
      )

   return states
