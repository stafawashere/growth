"""The selection_priority switch (docs/pedagogy/today/design.md D2) as open_session and home's
preview read it. The reference two-term session is assemble_session called with no ordering over
the same stored states, history, block 3 entry thresholds and rng that open_session used."""
import json
import random
from datetime import datetime

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.experiments import switches
from app.main import experiment_default_state
from app.session import preview, repository, service
from app.session.build import assemble_session
from tests.engine.conftest_selection import ACCOUNT_CREATED_AT
from tests.session.test_queue_preview import NOW, PROCESS_SEED, TODAY, make_world
from tests.session.test_service import SNAPSHOT_ID, USER_ID

SEEDS = range(8)
BLOCKS = ("block1", "block2", "block3")
DECAYED_REACH = ("BC-SKL-01044", "BC-SKL-02039")
DECAYED_SINCE = datetime(2026, 1, 5, 9, 0, 0)


def decayed_world(world_path):
   """The due skills of make_world are reached by no fringe archetype, so two skills that block 2
   candidates reach as gating parents are given a memory long decayed."""
   world_path.mkdir()
   world = make_world(world_path)

   with OrmSession(world.engine) as db:
      states = repository.load_states(db, USER_ID)

      for skill_id in DECAYED_REACH:
         states[skill_id].stability = 2.0
         states[skill_id].difficulty = 5.0
         states[skill_id].last_practised_at = DECAYED_SINCE

      repository.save_states(db, USER_ID, states, SNAPSHOT_ID, ACCOUNT_CREATED_AT)
      db.commit()

   return world


def running_default():
   return experiment_default_state({})


def treatment_default():
   default = running_default()
   default[switches.SELECTION_PRIORITY] = switches.ON

   return default


def open_rehearsal(world, db, experiment_default, seed):
   """seed None draws with the rng home's preview uses for the same user and day."""
   has_seed = seed is not None
   rng = random.Random(seed) if has_seed else preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY)

   return service.open_session(
      db,
      USER_ID,
      "rehearsal",
      world.graph,
      world.engine_graph,
      world.archetypes,
      world.bank,
      SNAPSHOT_ID,
      TODAY,
      rng,
      now=NOW,
      experiment_default=experiment_default,
   )


def served_ids(blocks):
   return {name: [item["id"] for item in blocks[name]] for name in BLOCKS}


def opened_and_two_term(tmp_path, experiment_default, seed):
   world = decayed_world(tmp_path / f"seed-{seed}")

   with OrmSession(world.engine) as db:
      row = open_rehearsal(world, db, experiment_default, seed)
      opened = served_ids(json.loads(row.queue))
      states = repository.load_states(db, USER_ID)
      history = repository.load_attempts_history(db, USER_ID)
      retrieval_entry = switches.retrieval_entry_thresholds(
         db, USER_ID, service.entry_candidates(states), experiment_default, NOW
      )
      reference = assemble_session(
         states, world.graph, world.bank, None, history, random.Random(seed), TODAY,
         now=NOW,
         retrieval_entry=retrieval_entry,
      )

   two_term = served_ids({name: getattr(reference, name) for name in BLOCKS})

   return opened, two_term


def test_the_running_default_serves_the_two_term_session(tmp_path):
   default = running_default()

   assert switches.resolve_default(default, switches.SELECTION_PRIORITY) == switches.OFF

   for seed in SEEDS:
      opened, two_term = opened_and_two_term(tmp_path, default, seed)

      assert len(opened["block2"]) > 0
      assert opened == two_term


def test_the_treatment_arm_changes_block_2_or_block_3(tmp_path):
   differing = []

   for seed in SEEDS:
      opened, two_term = opened_and_two_term(tmp_path, treatment_default(), seed)

      assert opened["block1"] == two_term["block1"]

      block2_differs = opened["block2"] != two_term["block2"]
      block3_differs = opened["block3"] != two_term["block3"]
      later_blocks_differ = block2_differs or block3_differs

      if later_blocks_differ:
         differing.append(seed)

   assert len(differing) > 0


def test_the_preview_and_the_opened_session_agree_under_the_treatment_arm(tmp_path):
   """A rehearsal session, because the preview places no opener and no lesson, so the two serve
   the same items in the same order and the focus, which names skills in serving order, can
   be compared whole."""
   world = decayed_world(tmp_path / "world")
   default = treatment_default()

   with OrmSession(world.engine) as db:
      previewed = preview.queue_preview(
         db, USER_ID, world.graph, world.bank, TODAY,
         preview.user_assembly_rng(PROCESS_SEED, USER_ID, TODAY), default,
      )
      row = open_rehearsal(world, db, default, None)
      db.commit()
      queue = json.loads(db.get(models.Session, row.id).queue)

   named_blocks = (("review", queue["block1"]), ("learn", queue["block2"]), ("mixed", queue["block3"]))
   expected_focus = [
      preview.block_focus(name, items, world.graph) for name, items in named_blocks if len(items) > 0
   ]

   assert len(queue["block2"]) > 0
   assert previewed["focus"] == expected_focus
