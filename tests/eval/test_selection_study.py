"""The stage 12 world corrections, the study's controls and the decay term's path into what is
served (docs/operator/selection-study.md). tools/selection_study.py runs the study at size."""
import random
from datetime import timedelta

from app.sim import learning, selection_study, whole_graph

DECAY_DIVERGES_SEED = 20270513
DECAY_DIVERGES_DAYS = 6


def a_world(rules, seed=11):
   library = whole_graph.library()
   student = learning.make_learning_student("study", seed)

   return learning.LearningWorld(
      student,
      library.engine_graph.hard_parents,
      random.Random(seed),
      rules=rules,
      seed=seed,
      start_day=whole_graph.START_DAY,
   )


def test_the_decay_arm_serves_differently_from_two_term():
   two_term = learning.run_student(
      learning.ARMS["two_term"], DECAY_DIVERGES_SEED, DECAY_DIVERGES_DAYS, keep_trace=True
   )
   decay = learning.run_student(
      learning.ARMS["decay_lambda_2"], DECAY_DIVERGES_SEED, DECAY_DIVERGES_DAYS, keep_trace=True
   )

   assert len(two_term.trace) > 0
   assert decay.trace != two_term.trace


def test_a_keyed_roll_does_not_depend_on_what_else_was_rolled():
   first = learning.KeyedDraws(5)
   second = learning.KeyedDraws(5)
   day = whole_graph.START_DAY

   first.random("answer", "BC-QA-01001", day)
   rolled_after_another = first.random("answer", "BC-QA-02006", day)
   rolled_alone = second.random("answer", "BC-QA-02006", day)

   assert rolled_after_another == rolled_alone
   assert second.random("answer", "BC-QA-02006", day) != rolled_alone


def test_same_day_successes_grow_a_half_life_once():
   world = a_world(learning.WORLD)
   skill_id = "BC-SKL-01001"
   day = whole_graph.START_DAY
   world.half_life.pop(skill_id, None)

   world.reinforce([skill_id], day)
   once = world.half_life[skill_id]
   world.reinforce([skill_id], day)

   assert world.half_life[skill_id] == once

   world.reinforce([skill_id], day + timedelta(days=1))

   assert world.half_life[skill_id] > once


def test_practising_a_skill_known_before_the_run_never_lowers_its_later_retention():
   world = a_world(learning.WORLD)
   known = sorted(skill_id for skill_id, is_known in world.student.known.items() if is_known)
   skill_id = known[0]
   later = whole_graph.START_DAY + timedelta(days=40)
   before = world.retention(skill_id, later)

   world.reinforce([skill_id], whole_graph.START_DAY + timedelta(days=1))

   assert world.retention(skill_id, later) >= before


def test_the_controls_order_by_the_hidden_world():
   world = a_world(learning.WORLD)
   day = whole_graph.START_DAY + timedelta(days=10)
   known = sorted(skill_id for skill_id, is_known in world.student.known.items() if is_known)
   fresh, stale = known[0], known[1]
   world.half_life[fresh] = 5.0
   world.last_success[fresh] = day
   world.half_life[stale] = 5.0
   world.last_success[stale] = day - timedelta(days=9)
   world.learned[fresh] = day
   world.learned[stale] = day - timedelta(days=9)
   records = [{"id": "A-fresh", "skills": [fresh]}, {"id": "B-stale", "skills": [stale]}]
   rng = random.Random(3)

   forgetting = selection_study.most_forgetting_ordering(world)(records, {}, None, day, {}, rng, [])
   recent = selection_study.most_recent_ordering(world)(records, {}, None, day, {}, rng, [])

   assert forgetting[0]["id"] == "B-stale"
   assert recent[0]["id"] == "A-fresh"
