"""The A/B switches of docs/plan/10 "Switch design" (11 P7 test_ab_assignment_balanced)."""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.experiments import switches

NOW = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)
USER = "USR-1"
SKILLS = ("BC-SKL-01001", "BC-SKL-02003", "BC-SKL-06010")


def assign_items(db, count):
   arms = {}

   for index in range(count):
      skill = SKILLS[index % len(SKILLS)]
      p_predicted = 0.2 if index % 4 < 2 else 0.8
      item_id = f"ITEM-{index:03d}"
      arms[item_id] = (
         skill,
         switches.arm_for(
            db, USER, switches.FEEDBACK_ELABORATION, item_id, skill, p_predicted, switches.RANDOMISED, NOW
         ),
      )

   return arms


def test_ab_assignment_balanced(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")
   definition = switches.DEFINITIONS[switches.FEEDBACK_ELABORATION]

   with OrmSession(engine) as db:
      arms = assign_items(db, 121)
      rows = db.query(models.ExperimentAssignment).all()

      per_stratum = {}

      for row in rows:
         counts = per_stratum.setdefault(row.stratum, {arm: 0 for arm in definition.arms})
         counts[row.arm] += 1

      per_skill = {skill: {arm: 0 for arm in definition.arms} for skill in SKILLS}

      for skill, arm in arms.values():
         per_skill[skill][arm] += 1

   assert len(rows) == 121
   assert len(per_stratum) == len(SKILLS) * 2
   assert all(abs(counts[definition.control_arm] - counts[definition.treatment_arm]) <= 1 for counts in per_stratum.values())
   assert all(abs(counts[definition.control_arm] - counts[definition.treatment_arm]) <= 2 for counts in per_skill.values())
   assert all(min(counts.values()) > 0 for counts in per_skill.values())


def test_a_unit_keeps_its_arm_through_state_changes(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")

   with OrmSession(engine) as db:
      first = assign_items(db, 12)
      switches.set_state(db, USER, switches.FEEDBACK_ELABORATION, switches.OFF, switches.RANDOMISED, NOW)
      off_arms = {
         switches.arm_for(db, USER, switches.FEEDBACK_ELABORATION, item_id, skill, 0.5, switches.RANDOMISED, NOW)
         for item_id, (skill, _) in first.items()
      }
      later = NOW + timedelta(days=3)
      switches.set_state(db, USER, switches.FEEDBACK_ELABORATION, switches.RANDOMISED, switches.RANDOMISED, later)
      again = {
         item_id: switches.arm_for(db, USER, switches.FEEDBACK_ELABORATION, item_id, skill, 0.9, switches.RANDOMISED, later)
         for item_id, (skill, _) in first.items()
      }
      stored = db.query(models.ExperimentAssignment).count()

   assert off_arms == {switches.DEFINITIONS[switches.FEEDBACK_ELABORATION].control_arm}
   assert again == {item_id: arm for item_id, (_, arm) in first.items()}
   assert stored == 12


def test_off_and_on_assign_nothing(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")
   definition = switches.DEFINITIONS[switches.RETRIEVAL_ENTRY]

   with OrmSession(engine) as db:
      off = switches.retrieval_entry_thresholds(db, USER, SKILLS, switches.OFF, NOW)
      switches.set_state(db, USER, switches.RETRIEVAL_ENTRY, switches.ON, switches.OFF, NOW)
      on = switches.retrieval_entry_thresholds(db, USER, SKILLS, switches.OFF, NOW)
      stored = db.query(models.ExperimentAssignment).count()

   assert set(off.values()) == {switches.ENTRY_THRESHOLDS[definition.control_arm]}
   assert set(on.values()) == {switches.ENTRY_THRESHOLDS[definition.treatment_arm]}
   assert stored == 0


def test_the_running_app_randomises_retrieval_entry_and_keeps_elaborated_feedback(tmp_path):
   from app.main import experiment_default_state

   defaults = experiment_default_state({})
   engine = models.make_engine(tmp_path / "ab.db")

   with OrmSession(engine) as db:
      feedback = switches.experiment_row(db, USER, switches.FEEDBACK_ELABORATION, defaults, NOW)
      retrieval = switches.experiment_row(db, USER, switches.RETRIEVAL_ENTRY, defaults, NOW)

   assert (feedback.state, retrieval.state) == (switches.OFF, switches.RANDOMISED)
   assert retrieval.randomised_from == NOW.isoformat()
   assert experiment_default_state({"GROWTH_EXPERIMENTS_DEFAULT": "on"}) == switches.ON
