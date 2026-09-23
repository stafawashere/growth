"""Home's queue preview, and the per-day dedup of the fail-closed coverage gap audit row.

The preview's expected numbers are read back out of the queue column open_session persists with
the same rng, so the test compares the preview against the session a student would open, not
against a second copy of the preview's own arithmetic.
"""
import json
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session as OrmSession

from app.api.app import Settings
from app.db import models
from app.engine import constants
from app.engine.select import due_skills, hypercorrection_skills, retrievability_map
from app.session import preview, repository, service
from app.session.build import COVERAGE_GAP_ACTION
from tests.api.conftest import publish_bank_items
from tests.engine.conftest_selection import (
   ACCOUNT_CREATED_AT,
   build_bank,
   build_graph,
   build_states,
   load_fixture,
)
from tests.session.test_service import SNAPSHOT_ID, USER_ID, engine_graph_from

TODAY = date(2026, 3, 1)
NOW = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc)
OTHER_USER_ID = "USER-0002"
PROCESS_SEED = Settings.rng_seed
DRAFT_ARCHETYPE = "BC-QA-01008"
DUE_SKILLS = ("BC-SKL-02006", "BC-SKL-01024")
CORRECTED_ITEM = "BC-QA-02011-V01"
TIMED_ATTEMPT_MS = 60000
TIMED_ATTEMPT_DAY = datetime(2026, 2, 10, 9, 0, 0, tzinfo=timezone.utc)
CORRECTED_DAY = datetime(2026, 2, 28, 9, 0, 0, tzinfo=timezone.utc)
HISTORY_SESSION_ID = "SES-HISTORY"


def due_states(fixture):
   states = build_states(fixture, mastered=frozenset(DUE_SKILLS))

   for skill_id in DUE_SKILLS:
      states[skill_id].stability = 2.0
      states[skill_id].difficulty = 5.0
      states[skill_id].last_practised_at = datetime(2026, 2, 1, 9, 0, 0)

   return states


def attempt_row(attempt_id, item_id, moment, correct, elapsed_ms):
   stamp = moment.isoformat()

   return models.Attempt(
      id=attempt_id,
      session_id=HISTORY_SESSION_ID,
      item_id=item_id,
      started_at=stamp,
      submitted_at=stamp,
      response="{}",
      confidence="confident",
      elapsed_ms=elapsed_ms,
      correct=correct,
      p_split=0.5,
      p_compensatory=0.5,
      served_stage="unsupported",
      format="short_answer",
      per_skill_states="{}",
      snapshot_id=SNAPSHOT_ID,
      created_at=stamp,
      updated_at=stamp,
   )


def seed_history(db, fixture):
   """Half the archetypes get enough timed attempts for a median, so the forecast mixes both rules."""
   db.add(
      models.Session(
         id=HISTORY_SESSION_ID,
         user_id=USER_ID,
         mode="learning",
         sub_mode=None,
         started_at=TIMED_ATTEMPT_DAY.isoformat(),
         ended_at=TIMED_ATTEMPT_DAY.isoformat(),
         queue="{}",
         updates_mastery=1,
         snapshot_id=SNAPSHOT_ID,
         created_at=TIMED_ATTEMPT_DAY.isoformat(),
         updated_at=TIMED_ATTEMPT_DAY.isoformat(),
      )
   )
   timed_archetypes = [record["id"] for record in fixture["archetypes"]][::2]

   for archetype_id in timed_archetypes:
      for index in range(constants.FORECAST_MIN_ATTEMPTS):
         db.add(
            attempt_row(
               f"ATT-{archetype_id}-{index}",
               f"{archetype_id}-V00",
               TIMED_ATTEMPT_DAY + timedelta(minutes=index),
               1,
               TIMED_ATTEMPT_MS,
            )
         )

   db.add(attempt_row("ATT-CORRECTED", CORRECTED_ITEM, CORRECTED_DAY, 0, TIMED_ATTEMPT_MS))


class World:
   def __init__(self, engine, fixture, bank):
      self.engine = engine
      self.fixture = fixture
      self.graph = build_graph(fixture)
      self.engine_graph = engine_graph_from(fixture)
      self.archetypes = {record["id"]: record for record in fixture["archetypes"]}
      self.bank = bank

   def preview(self, db, user_id=USER_ID, today=TODAY):
      rng = preview.user_assembly_rng(PROCESS_SEED, user_id, today)

      return preview.queue_preview(db, user_id, self.graph, self.bank, today, rng)

   def open(self, db, user_id=USER_ID, today=TODAY):
      return service.open_session(
         db,
         user_id,
         "learning",
         self.graph,
         self.engine_graph,
         self.archetypes,
         self.bank,
         SNAPSHOT_ID,
         today,
         preview.user_assembly_rng(PROCESS_SEED, user_id, today),
         now=NOW,
      )


def make_world(tmp_path, draft_only=frozenset()):
   fixture = load_fixture()
   engine = models.make_engine(tmp_path / "growth.db")
   publish_bank_items(engine, fixture)

   with OrmSession(engine) as db:
      for user_id in (USER_ID, OTHER_USER_ID):
         repository.save_states(db, user_id, due_states(fixture), SNAPSHOT_ID, ACCOUNT_CREATED_AT)

      seed_history(db, fixture)
      db.commit()

   return World(engine, fixture, build_bank(fixture, draft_only=draft_only))


def row_counts(db):
   return {
      table.name: db.scalar(select(func.count()).select_from(table))
      for table in models.Base.metadata.sorted_tables
   }


def gap_rows(db):
   return db.scalars(
      select(models.AuditLog).where(models.AuditLog.action == COVERAGE_GAP_ACTION)
   ).all()


def expected_from_queue(world, db, queue):
   """Each count read off the persisted queue by the definitions in app/session/preview.py."""
   states = repository.load_states(db, USER_ID)
   retrievability = retrievability_map(states, TODAY, None)
   reviewable = due_skills(states, world.graph, TODAY, retrievability)
   reviewable = reviewable | hypercorrection_skills(states, TODAY)
   served = queue["block1"] + queue["block2"] + queue["block3"]
   returning = [item for item in queue["block1"] if item["id"] == CORRECTED_ITEM]
   reviewed = [item for item in queue["block1"] if item["id"] != CORRECTED_ITEM]
   due_touched = {
      skill_id
      for item in reviewed
      for skill_id in world.archetypes[item["archetype_id"]]["skills"]
      if skill_id in reviewable
   }
   frontier = {world.graph.primary_skill(item["archetype_id"]) for item in queue["block2"]}

   return {
      "skills_due_for_review": len(due_touched),
      "frontier_skills": len(frontier),
      "corrected_items_returning": len(returning),
      "forecast_minutes": sum(queue["forecasts"][item["archetype_id"]] for item in served),
   }


def test_the_preview_matches_the_queue_open_session_persists(tmp_path):
   world = make_world(tmp_path)

   with OrmSession(world.engine) as db:
      previewed = world.preview(db)
      row = world.open(db)
      db.commit()
      stored = db.get(models.Session, row.id)
      queue = json.loads(stored.queue)
      expected = expected_from_queue(world, db, queue)
      served_count = len(queue["block1"]) + len(queue["block2"]) + len(queue["block3"])

   assert expected["corrected_items_returning"] == 1
   assert expected["skills_due_for_review"] >= 1
   assert expected["forecast_minutes"] != served_count * constants.FORECAST_DEFAULT_MINUTES

   for key, value in expected.items():
      assert previewed[key] == value, key


def test_the_preview_writes_nothing_even_with_a_coverage_gap(tmp_path):
   world = make_world(tmp_path, draft_only={DRAFT_ARCHETYPE})

   with OrmSession(world.engine) as db:
      before = row_counts(db)
      world.preview(db)
      db.flush()
      after = row_counts(db)

   assert before["attempts"] > 0
   assert after == before


def test_two_previews_on_one_day_agree(tmp_path):
   world = make_world(tmp_path)

   with OrmSession(world.engine) as db:
      first = world.preview(db)
      second = world.preview(db)

   assert first == second


def test_session_in_progress_names_only_this_users_open_session(tmp_path):
   world = make_world(tmp_path)

   with OrmSession(world.engine) as db:
      nothing_open = world.preview(db)["session_in_progress"]
      other_users_id = world.open(db, user_id=OTHER_USER_ID).id
      db.commit()
      only_other_open = world.preview(db)["session_in_progress"]
      mine_id = world.open(db).id
      db.commit()
      while_open = world.preview(db)["session_in_progress"]
      service.close_session(db, mine_id, now=NOW)
      db.commit()
      after_close = world.preview(db)["session_in_progress"]

   assert other_users_id != mine_id
   assert nothing_open is None
   assert only_other_open is None
   assert while_open == mine_id
   assert after_close is None


def test_two_sessions_opened_on_one_day_write_one_gap_row(tmp_path):
   world = make_world(tmp_path, draft_only={DRAFT_ARCHETYPE})

   with OrmSession(world.engine) as db:
      first = world.open(db)
      db.commit()
      service.close_session(db, first.id, now=NOW)
      db.commit()
      world.open(db)
      db.commit()
      rows = gap_rows(db)

   subjects = [row.subject for row in rows]

   assert f"archetypes:{DRAFT_ARCHETYPE}" in subjects
   assert len(subjects) == len(set(subjects))


def test_the_same_gap_on_the_next_day_writes_a_second_row(tmp_path):
   world = make_world(tmp_path, draft_only={DRAFT_ARCHETYPE})
   next_day = TODAY + timedelta(days=1)

   with OrmSession(world.engine) as db:
      world.open(db)
      db.commit()
      world.open(db, today=next_day)
      db.commit()
      rows = [row for row in gap_rows(db) if row.subject == f"archetypes:{DRAFT_ARCHETYPE}"]

   days = sorted(json.loads(row.detail).get("day", "") for row in rows)

   assert days == [TODAY.isoformat(), next_day.isoformat()]


def draw_state(rng):
   """The generator's whole state, which fixes every draw it will ever make."""
   return rng.getstate()


def test_the_same_user_on_the_same_day_gets_the_same_draw():
   first = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)
   second = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)

   assert draw_state(first) == draw_state(second)


def test_two_users_on_the_same_day_get_different_draws():
   mine = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)
   theirs = preview.user_assembly_rng(PROCESS_SEED, OTHER_USER_ID, TODAY)

   assert draw_state(mine) != draw_state(theirs)


def test_the_process_seed_still_moves_the_draw():
   seeded = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)
   reseeded = preview.user_assembly_rng(PROCESS_SEED + 1, USER_ID, TODAY)

   assert draw_state(seeded) != draw_state(reseeded)


def test_the_route_inputs_seed_by_user_and_day():
   today, rng = preview.user_assembly_inputs(PROCESS_SEED, USER_ID, TODAY.isoformat())
   expected = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)

   assert today == TODAY
   assert draw_state(rng) == draw_state(expected)


def test_the_same_user_on_the_next_day_gets_a_different_draw():
   today = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)
   tomorrow = preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY + timedelta(days=1))

   assert draw_state(today) != draw_state(tomorrow)
