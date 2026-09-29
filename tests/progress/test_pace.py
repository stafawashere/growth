"""The pace verdict: mastery rate against the rate the exam date requires."""
from datetime import date, datetime, timedelta

from app.engine.fringe import Graph
from app.engine.state import SkillState
from app.progress import pace
from app.progress.attempt_log import AttemptRecord

TODAY = date(2026, 10, 1)
FAR_EXAM = date(2027, 5, 10)
EQUAL_WEIGHTS = {"BC-UNIT-01": 1, "BC-UNIT-02": 1}
SKILL_IDS = [f"BC-SKL-0100{index}" for index in range(5)] + [f"BC-SKL-0200{index}" for index in range(5)]


def graph_of(skill_ids):
   skills = [{"id": skill_id, "unit": f"BC-UNIT-{skill_id[7:9]}", "name": skill_id} for skill_id in skill_ids]

   return Graph.from_records(archetypes=[], skills=skills, edges=[], inert_top=())


def earned(skill_id, mastered_on):
   return SkillState(
      skill_id=skill_id,
      mastered=True,
      mastered_at=datetime.combine(mastered_on, datetime.min.time()),
      stability=400.0,
      difficulty=5.0,
      last_practised_at=datetime.combine(mastered_on, datetime.min.time()),
      observation_count=6,
      unaided_success_count=3,
   )


def decayed(skill_id, mastered_on):
   state = earned(skill_id, mastered_on)
   state.stability = 1.0

   return state


def seeded(skill_id):
   return SkillState.seeded_mastered(skill_id, datetime(2026, 9, 1))


def attempt(index, day, correct=True, skill_id="BC-SKL-01000"):
   return AttemptRecord(
      id=f"ATT-{index}",
      session_id="SES-1",
      session_mode="learning",
      item_id=f"ITEM-{index}",
      archetype_id="BC-QA-01001",
      primary_skill=skill_id,
      skills=(skill_id,),
      submitted_at=f"{day.isoformat()}T12:00:00+00:00",
      correct=correct,
      confidence=None,
      confidence_source=None,
      elapsed_ms=120_000,
      served_stage="unsupported",
      format="mcq",
      response={},
      experiment_arms={},
      image_ids=None,
      transcription_confirmed=False,
      updates_mastery=True,
   )


def enough_practice(days=28, per_day=3):
   return [
      attempt(day_index * per_day + slot, TODAY - timedelta(days=day_index))
      for day_index in reversed(range(days))
      for slot in range(per_day)
   ]


def verdict(states, attempts, exam_date=FAR_EXAM):
   return pace.pace_verdict(graph_of(SKILL_IDS), states, attempts, exam_date, TODAY, midpoints=EQUAL_WEIGHTS)


def test_a_fast_rate_against_a_distant_exam_is_ahead_and_a_near_exam_is_well_behind():
   states = {skill_id: earned(skill_id, TODAY - timedelta(days=3)) for skill_id in SKILL_IDS[:4]}

   distant = verdict(states, enough_practice())
   near = verdict(states, enough_practice(), exam_date=TODAY + timedelta(days=pace.REVIEW_RESERVE_DAYS + 14))

   assert distant["verdict"] == pace.AHEAD
   assert distant["rate"]["weekly"] == 1.0
   assert date.fromisoformat(distant["rate"]["projected_finish"]) < date.fromisoformat(distant["new_mastery_deadline"])
   assert near["verdict"] == pace.WELL_BEHIND
   assert near["rate"]["required_weekly"] == 3.0


def test_seeded_and_fading_mastery_count_as_remaining_work():
   states = {
      SKILL_IDS[0]: earned(SKILL_IDS[0], TODAY - timedelta(days=3)),
      SKILL_IDS[1]: seeded(SKILL_IDS[1]),
      SKILL_IDS[2]: decayed(SKILL_IDS[2], TODAY - timedelta(days=90)),
   }

   result = verdict(states, enough_practice())

   assert result["skills"]["held"] == 1
   assert result["skills"]["assumed"] == 1
   assert result["skills"]["fading"] == 1
   assert result["skills"]["remaining"] == 9


def test_no_verdict_before_the_minimum_practice():
   states = {skill_id: earned(skill_id, TODAY) for skill_id in SKILL_IDS[:4]}

   result = verdict(states, enough_practice(days=3, per_day=20))

   assert result["verdict"] == pace.TOO_EARLY


def test_failing_retention_caps_a_fast_rate_at_behind():
   states = {skill_id: earned(skill_id, TODAY - timedelta(days=3)) for skill_id in SKILL_IDS[:4]}
   successes = [attempt(1000 + index, TODAY - timedelta(days=60), skill_id=f"BC-SKL-9{index:04d}") for index in range(12)]
   lapses = [
      attempt(2000 + index, TODAY - timedelta(days=30), correct=False, skill_id=f"BC-SKL-9{index:04d}")
      for index in range(12)
   ]

   result = verdict(states, successes + lapses + enough_practice())

   assert result["evidence"]["retention_30_day"]["attempts"] == 12
   assert result["verdict"] == pace.BEHIND
   assert result["statement"].startswith("Behind pace. New skills arrive fast enough")
