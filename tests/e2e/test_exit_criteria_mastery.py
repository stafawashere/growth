"""Exit criteria 5 and 6 of P1 in docs/plan/11-phased-delivery.md, over the real HTTP application.

Both tests drive the student only through the routes and then read skills_state and attempts back
out of SQLite. The mastery flag is never taken as evidence for the six D2 conditions of
docs/plan/02-adaptive-engine.md, "Mastery declaration and un-mastery": each condition is recomputed
from the attempts rows (served_stage, per_skill_states, format, submitted_at and the item's
archetype) up to the attempt at which skills_state flipped.

The items are the synthetic fixtures in tests/fixtures/items_p1/, which count toward no item-quality
gate. What these tests demonstrate is the engine path from a route to a mastery transition, not the
quality of any item.
"""
import json
import math
import re
from datetime import date, timedelta

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.engine import fsrs
from app.engine.state import FADING_ORDER, FadingStage, MasteryState, ResponseFormat
from tests.e2e.conftest import FIRST_DAY, REPO_ROOT
from tests.e2e.test_session_login_to_feedback import (
   answer_for,
   collects_confidence,
   rate,
   submit,
)

PLAN_PHASES = REPO_ROOT / "docs" / "plan" / "11-phased-delivery.md"
GRAPH_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "graph_p1.json"
ARCHETYPE_REGISTRY = REPO_ROOT / "data" / "archetypes.json"
UNIT_TWO = "BC-UNIT-02"

PLAN_MASTERY_THRESHOLD = 0.9
PLAN_UNMASTERY_THRESHOLD = 0.75
PLAN_MIN_UNAIDED_SUCCESSES = 3
PLAN_MIN_DISTINCT_ARCHETYPES = 2
PLAN_MIN_DISTINCT_DAYS = 3
PLAN_MIN_DAY_SPAN = 7
PLAN_DESIRED_RETENTION = 0.90
PLAN_GAMMA = 1.0
PLAN_RHO = -0.5
PLAN_MCQ_SUCCESS_CREDIT = 0.75
PLAN_FADING_ADVANCE_AFTER = 2
PLAN_FADING_DROP_AFTER = 2

SUCCESS_CREDIT = {
   MasteryState.MASTERED.value: 1.0,
   MasteryState.NOTATION_ONLY.value: 0.25,
}
FAILURE_CREDIT = {
   MasteryState.NOT_MASTERED.value: 1.0,
   MasteryState.PARTIAL_PROCEDURAL.value: 0.5,
   MasteryState.PARTIAL_CONCEPTUAL.value: 0.5,
   MasteryState.PARTIAL_UNSPECIFIED.value: 0.5,
}

STAGE_ADVANCES_TO_UNAIDED = len(FADING_ORDER) - 1
SUCCESSES_TO_REACH_UNAIDED = STAGE_ADVANCES_TO_UNAIDED * PLAN_FADING_ADVANCE_AFTER

DAYS_APART_SO_DAY_COUNT_BINDS = PLAN_MIN_DAY_SPAN + 1
MAX_SESSIONS_DAY_COUNT_BINDS = SUCCESSES_TO_REACH_UNAIDED + PLAN_MIN_DISTINCT_DAYS

DAYS_APART_SO_SPAN_BINDS = 1
MAX_SESSIONS_SPAN_BINDS = (
   SUCCESSES_TO_REACH_UNAIDED + DAYS_APART_SO_DAY_COUNT_BINDS + PLAN_FADING_DROP_AFTER
)


def plan_q20_skill_ids():
   """The 54 P1 skills as Q20 lists them: the first id in full, the rest as bare numbers."""
   text = PLAN_PHASES.read_text()
   paragraph = [line for line in text.splitlines() if "**Q20.**" in line][0]
   listing = paragraph.split("graph_p1.json`", 1)[1].split("BC-SKL-02037 and", 1)[0]
   numbers = re.findall(r"\b(\d{5})\b", listing)

   return {f"BC-SKL-{number}" for number in numbers}


def p1_unit_two_skills():
   """Unit 2 members of the P1 set, read off the fixture and held against the plan's own list."""
   fixture = json.loads(GRAPH_FIXTURE.read_text())
   fixture_ids = {record["id"] for record in fixture["skills"]}
   plan_ids = plan_q20_skill_ids()

   assert fixture_ids == plan_ids, (
      "tests/fixtures/graph_p1.json must hold exactly the Q20 skills of "
      f"docs/plan/11-phased-delivery.md; fixture only {sorted(fixture_ids - plan_ids)}, "
      f"plan only {sorted(plan_ids - fixture_ids)}"
   )

   unit_two = {
      record["id"]
      for record in fixture["skills"]
      if record["unit"] == UNIT_TWO and record["id"] in plan_ids
   }

   assert len(unit_two) > 0

   return unit_two


def fixture_primary_skills():
   fixture = json.loads(GRAPH_FIXTURE.read_text())

   return [record["skills"][0] for record in fixture["archetypes"]]


def active_archetype_count(skill_id):
   """Condition 3's ceiling: the archetypes of the active snapshot that list the skill."""
   registry = json.loads(ARCHETYPE_REGISTRY.read_text())["archetypes"]
   count = 0

   for record in registry:
      is_active = record.get("status", "active") == "active"
      lists_skill = skill_id in record["skills"]
      counts = is_active and lists_skill

      if counts:
         count += 1

   return count


def skill_rows(world):
   with OrmSession(world.engine) as db:
      rows = (
         db.query(models.SkillState)
         .filter(models.SkillState.user_id == world.user_id)
         .all()
      )

      return {
         row.skill_id: {
            "mastered": row.mastered,
            "mastered_at": row.mastered_at,
            "fading_stage": row.fading_stage,
            "consecutive_successes": row.consecutive_successes,
            "consecutive_failures": row.consecutive_failures,
            "credited_successes": row.credited_successes,
            "credited_failures": row.credited_failures,
            "success_days": row.success_days,
            "distinct_archetypes_succeeded": row.distinct_archetypes_succeeded,
            "beta": row.beta,
            "stability": row.stability,
            "difficulty": row.difficulty,
         }
         for row in rows
      }


def attempt_evidence(world, attempt_ids):
   """The attempts rows in the order the routes wrote them, with each item's archetype joined."""
   evidence = []

   with OrmSession(world.engine) as db:
      for attempt_id in attempt_ids:
         attempt = db.get(models.Attempt, attempt_id)
         session_row = db.get(models.Session, attempt.session_id)
         item = db.get(models.Item, attempt.item_id)

         assert session_row.user_id == world.user_id

         evidence.append({
            "id": attempt.id,
            "archetype_id": item.archetype_id,
            "served_stage": attempt.served_stage,
            "format": attempt.format,
            "per_skill_states": json.loads(attempt.per_skill_states),
            "day": date.fromisoformat(attempt.submitted_at[:10]),
         })

   return evidence


def credited_success(entry, skill_id):
   state = entry["per_skill_states"].get(skill_id)
   credit = SUCCESS_CREDIT.get(state, 0.0)
   is_mcq = entry["format"] == ResponseFormat.MCQ.value

   if is_mcq:
      credit *= PLAN_MCQ_SUCCESS_CREDIT

   return credit


def credited_failure(entry, skill_id):
   state = entry["per_skill_states"].get(skill_id)

   return FAILURE_CREDIT.get(state, 0.0)


def is_unaided_success(entry, skill_id):
   is_unaided = entry["served_stage"] == FadingStage.UNSUPPORTED.value
   is_full_success = entry["per_skill_states"].get(skill_id) == MasteryState.MASTERED.value

   return is_unaided and is_full_success


def sigmoid(logit):
   return 1.0 / (1.0 + math.exp(-logit))


def six_conditions(evidence, skill_id, beta, stability, difficulty):
   """D2's six conditions recomputed from attempts up to and including the flip attempt.

   Condition 1 counts direct credit only. Propagated credit from a descendant can only add to c_k
   in P1, because no rule-based diagnosis emits prerequisite_gap, so a strength that clears the
   threshold here clears it in the engine too.
   """
   loading = [entry for entry in evidence if skill_id in entry["per_skill_states"]]
   unaided = [entry for entry in loading if is_unaided_success(entry, skill_id)]
   days = sorted({entry["day"] for entry in unaided})
   has_days = len(days) > 0
   span = (days[-1] - days[0]).days if has_days else 0
   archetypes = {entry["archetype_id"] for entry in unaided}
   required_archetypes = max(
      1, min(PLAN_MIN_DISTINCT_ARCHETYPES, active_archetype_count(skill_id))
   )

   successes = sum(credited_success(entry, skill_id) for entry in loading)
   failures = sum(credited_failure(entry, skill_id) for entry in loading)
   strength = beta + PLAN_GAMMA * math.log1p(successes) + PLAN_RHO * math.log1p(failures)

   flip = evidence[-1]
   flip_state = flip["per_skill_states"].get(skill_id)
   flip_is_credited = flip_state not in (None, MasteryState.NOT_ATTEMPTED.value)
   retention_at_flip = fsrs.retrievability(stability, 0, difficulty=difficulty)

   return {
      "1 sigmoid(m_k) >= 0.9": sigmoid(strength) >= PLAN_MASTERY_THRESHOLD,
      "2 three unaided successes": len(unaided) >= PLAN_MIN_UNAIDED_SUCCESSES,
      "3 distinct archetypes": len(archetypes) >= required_archetypes,
      "4 three distinct days": len(days) >= PLAN_MIN_DISTINCT_DAYS,
      "5 seven-day span": span >= PLAN_MIN_DAY_SPAN,
      "6 R_k >= desired retention": flip_is_credited
      and retention_at_flip >= PLAN_DESIRED_RETENTION,
   }


def unaided_success_days(evidence, skill_id):
   loading = [entry for entry in evidence if skill_id in entry["per_skill_states"]]

   return sorted({entry["day"] for entry in loading if is_unaided_success(entry, skill_id)})


class Run:
   """One student's attempts, with skills_state read back after every single one."""

   def __init__(self, world, client):
      self.world = world
      self.client = client
      self.attempt_ids = []
      self.after_attempt = {}
      self.before_attempt = {}

   def answer(self, session_id, item, correctly, today):
      entry = self.world.answers[item["id"]]
      before = skill_rows(self.world)
      submitted = submit(self.client, session_id, item, answer_for(entry, item, correctly), today)

      assert submitted.status_code == 200, submitted.text

      attempt = submitted.json()

      assert attempt["correct"] is correctly

      if collects_confidence(item):
         confidence = "confident" if correctly else "unsure"
         rated = rate(self.client, session_id, attempt["id"], confidence, today)

         assert rated.status_code == 200, rated.text

      self.attempt_ids.append(attempt["id"])
      self.before_attempt[attempt["id"]] = before
      self.after_attempt[attempt["id"]] = skill_rows(self.world)

      return attempt["id"]

   def complete_session(self, today, answers_correctly):
      opened = self.client.post("/sessions", json={"mode": "learning", "today": today.isoformat()})

      assert opened.status_code == 200, opened.text

      session_id = opened.json()["id"]

      while True:
         offered = self.client.get(f"/sessions/{session_id}/next")

         assert offered.status_code == 200, offered.text

         item = offered.json()["item"]
         is_drained = item is None

         if is_drained:
            break

         correctly = answers_correctly(item, skill_rows(self.world))
         self.answer(session_id, item, correctly, today)

      emptied = self.client.get(f"/sessions/{session_id}")

      assert emptied.status_code == 200, emptied.text
      assert emptied.json()["remaining"] == []

      closed = self.client.post(f"/sessions/{session_id}/close", json={"today": today.isoformat()})

      assert closed.status_code == 200, closed.text

   def first_flip(self, skill_id, from_value, to_value):
      for position, attempt_id in enumerate(self.attempt_ids):
         was = self.before_attempt[attempt_id][skill_id]["mastered"]
         now = self.after_attempt[attempt_id][skill_id]["mastered"]
         is_flip = was == from_value and now == to_value

         if is_flip:
            return position

      return None


def always_correct(item, rows):
   return True


def start(world):
   client = world.client()
   registered = world.register(client)

   assert registered.status_code == 200, registered.text

   return Run(world, client)


def conditions_after(world, run, skill_id, position):
   attempt_id = run.attempt_ids[position]
   after = run.after_attempt[attempt_id][skill_id]
   evidence = attempt_evidence(world, run.attempt_ids[: position + 1])

   return six_conditions(
      evidence, skill_id, after["beta"], after["stability"], after["difficulty"]
   )


def assert_flip_at_first_eligible_attempt(world, run, skill_id):
   """skills_state flipped on the first attempt whose evidence meets all six, and not before.

   Only attempts that credited the skill directly are candidates, because the engine re-evaluates
   mastery only on the skills an observation touched.
   """
   position = run.first_flip(skill_id, 0, 1)
   attempt_id = run.attempt_ids[position]
   at_flip = conditions_after(world, run, skill_id, position)
   failing = [name for name, holds in at_flip.items() if not holds]

   assert failing == [], (
      f"skills_state declared {skill_id} mastered at attempt {attempt_id}, but the attempts rows "
      f"up to it do not satisfy D2 conditions {failing}"
   )

   evidence = attempt_evidence(world, run.attempt_ids[: position + 1])

   for earlier in range(position):
      entry = evidence[earlier]
      state = entry["per_skill_states"].get(skill_id)
      was_credited = state not in (None, MasteryState.NOT_ATTEMPTED.value)

      if not was_credited:
         continue

      conditions = conditions_after(world, run, skill_id, earlier)
      all_held = all(conditions.values())

      assert not all_held, (
         f"the attempts up to {entry['id']} on {entry['day']} already met all six D2 conditions "
         f"for {skill_id}, yet skills_state flipped only at {attempt_id}"
      )

   return evidence


def test_unit2_session_changes_mastery_state(world):
   """Exit criterion 5: a completed session over Unit 2 skills flips a P1 Unit 2 skill mastered.

   Sessions are 8 days apart, one more than the plan's 7-day span, so two unaided days already
   satisfy condition 5 and condition 4, three distinct days, decides when the flip may come. The
   items are synthetic fixtures that count toward no item-quality gate; the test shows the engine
   path from the routes to skills_state and back to the attempts rows.
   """
   unit_two = p1_unit_two_skills()
   run = start(world)
   seeded = skill_rows(world)
   today = FIRST_DAY
   flipped = []

   for _session_index in range(MAX_SESSIONS_DAY_COUNT_BINDS):
      run.complete_session(today, always_correct)
      flipped = [
         skill_id
         for skill_id in sorted(unit_two)
         if run.first_flip(skill_id, 0, 1) is not None
      ]
      has_flip = len(flipped) > 0

      if has_flip:
         break

      today = today + timedelta(days=DAYS_APART_SO_DAY_COUNT_BINDS)

   assert flipped != [], (
      f"no P1 Unit 2 skill changed mastery state within {MAX_SESSIONS_DAY_COUNT_BINDS} sessions"
   )

   final = skill_rows(world)

   for skill_id in flipped:
      evidence = assert_flip_at_first_eligible_attempt(world, run, skill_id)
      flip_day = evidence[-1]["day"]
      days = unaided_success_days(evidence, skill_id)

      assert seeded[skill_id]["mastered"] == 0
      assert final[skill_id]["mastered"] == 1
      assert final[skill_id]["mastered_at"][:10] == flip_day.isoformat()
      assert json.loads(final[skill_id]["success_days"])[: len(days)] == [
         day.isoformat() for day in days
      ]


def test_mastery_path_across_days_and_unmastery(world):
   """Exit criterion 6: mastery across 3 or more days spanning 7 or more, then un-mastery (R7).

   Sessions are one calendar day apart, so a skill can collect three unaided days inside a week
   and condition 5 decides when its flip may come. Once a primary skill is mastered, every item
   that loads it at stage unsupported is answered wrongly: the first credited failure there must
   flip mastered off without touching fading_stage, and the stage may drop only when the run of
   consecutive credited failures in attempts reaches 2.
   """
   primaries = fixture_primary_skills()
   run = start(world)
   target = {"skill_id": None}

   def answers_correctly(item, rows):
      has_target = target["skill_id"] is not None

      if not has_target:
         return True

      skill_id = target["skill_id"]
      loads_target = skill_id in item["skills"]
      is_unaided = item["stage"] == FadingStage.UNSUPPORTED.value
      at_stage_unsupported = rows[skill_id]["fading_stage"] == FadingStage.UNSUPPORTED.value
      fails_it = loads_target and is_unaided and at_stage_unsupported

      return not fails_it

   for session_index in range(MAX_SESSIONS_SPAN_BINDS):
      today = FIRST_DAY + timedelta(days=session_index * DAYS_APART_SO_SPAN_BINDS)
      run.complete_session(today, answers_correctly)
      has_target = target["skill_id"] is not None
      mastered_primaries = [
         skill_id for skill_id in primaries if run.first_flip(skill_id, 0, 1) is not None
      ]
      picks_target = not has_target and len(mastered_primaries) > 0

      if picks_target:
         target["skill_id"] = mastered_primaries[0]

   skill_id = target["skill_id"]

   assert skill_id is not None, (
      f"no P1 archetype's primary skill was mastered within {MAX_SESSIONS_SPAN_BINDS} daily sessions"
   )

   for mastered_skill in mastered_primaries:
      assert_flip_at_first_eligible_attempt(world, run, mastered_skill)

   mastered_position = run.first_flip(skill_id, 0, 1)
   evidence = attempt_evidence(world, run.attempt_ids[: mastered_position + 1])
   days = unaided_success_days(evidence, skill_id)

   assert len(days) >= PLAN_MIN_DISTINCT_DAYS
   assert (days[-1] - days[0]).days >= PLAN_MIN_DAY_SPAN

   unmastered_position = run.first_flip(skill_id, 1, 0)

   assert unmastered_position is not None, f"{skill_id} was mastered and never un-mastered"

   all_evidence = attempt_evidence(world, run.attempt_ids)
   unmastering = all_evidence[unmastered_position]
   unmastering_id = run.attempt_ids[unmastered_position]
   before = run.before_attempt[unmastering_id][skill_id]
   after = run.after_attempt[unmastering_id][skill_id]
   state_seen = unmastering["per_skill_states"][skill_id]
   strength_after = sigmoid(
      after["beta"]
      + PLAN_GAMMA * math.log1p(after["credited_successes"])
      + PLAN_RHO * math.log1p(after["credited_failures"])
   )
   served_unaided = unmastering["served_stage"] == FadingStage.UNSUPPORTED.value
   failed_unaided = served_unaided and credited_failure(unmastering, skill_id) > 0.0
   fell_below = strength_after < PLAN_UNMASTERY_THRESHOLD

   assert failed_unaided or fell_below, (
      f"{skill_id} un-mastered on attempt {unmastering_id} at stage "
      f"{unmastering['served_stage']} with state {state_seen} and sigmoid {strength_after:.3f}, "
      "which is neither un-mastery trigger of D2"
   )
   assert after["mastered_at"] is None
   assert after["fading_stage"] == before["fading_stage"], (
      "R7: un-mastery flips mastered and leaves fading_stage to the counter pair, and the stage "
      f"moved from {before['fading_stage']} to {after['fading_stage']} on the first failure"
   )
   assert after["consecutive_failures"] == before["consecutive_failures"] + 1
   assert after["success_days"] == before["success_days"]
   assert after["distinct_archetypes_succeeded"] == before["distinct_archetypes_succeeded"]
   assert after["credited_successes"] == before["credited_successes"]

   failure_run = 0
   success_run = 0
   stage_moves = []

   for position in range(mastered_position + 1, len(run.attempt_ids)):
      entry = all_evidence[position]
      attempt_id = run.attempt_ids[position]
      is_credited_failure = credited_failure(entry, skill_id) > 0.0
      is_credited_success = credited_success(entry, skill_id) > 0.0

      if is_credited_failure:
         failure_run += 1
         success_run = 0

      if is_credited_success:
         success_run += 1
         failure_run = 0

      stage_before = run.before_attempt[attempt_id][skill_id]["fading_stage"]
      stage_after = run.after_attempt[attempt_id][skill_id]["fading_stage"]
      stage_moved = stage_before != stage_after

      if stage_moved:
         stage_moves.append((attempt_id, stage_before, stage_after, failure_run, success_run))
         failure_run = 0
         success_run = 0

   drops = [move for move in stage_moves if move[1] == FadingStage.UNSUPPORTED.value]

   assert len(drops) > 0, (
      f"{skill_id} never left stage unsupported after un-mastery, so the counter drop was not seen"
   )

   for attempt_id, stage_before, stage_after, failures, successes in stage_moves:
      step = (
         FADING_ORDER.index(FadingStage(stage_after))
         - FADING_ORDER.index(FadingStage(stage_before))
      )
      dropped_on_the_pair = step == -1 and failures == PLAN_FADING_DROP_AFTER
      advanced_on_the_pair = step == 1 and successes == PLAN_FADING_ADVANCE_AFTER
      moved_on_the_counter = dropped_on_the_pair or advanced_on_the_pair

      assert moved_on_the_counter, (
         f"{skill_id} moved {stage_before} to {stage_after} on attempt {attempt_id} after "
         f"{failures} consecutive credited failures and {successes} consecutive credited "
         "successes in attempts, and R7 lets only the counter pair move the stage"
      )