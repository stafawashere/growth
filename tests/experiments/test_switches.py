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


def test_tutor_profile_is_a_skill_switch_that_starts_off():
   definition = switches.DEFINITIONS[switches.TUTOR_PROFILE]

   assert definition.unit == "skill"
   assert definition.arms == ("profile_withheld", "profile_applied")
   assert definition.description.strip() != ""
   assert switches.resolve_default({switches.RETRIEVAL_ENTRY: switches.RANDOMISED}, switches.TUTOR_PROFILE) == switches.OFF


def test_two_skills_of_one_unit_share_a_stratum_and_are_balanced_into_different_arms(tmp_path):
   engine = models.make_engine(tmp_path / "ab.db")
   first_skill = "BC-SKL-02005"
   second_skill = "BC-SKL-02017"
   other_unit_skill = "BC-SKL-06010"

   with OrmSession(engine) as db:
      arms = {
         skill: switches.arm_for(db, USER, switches.TUTOR_PROFILE, skill, skill, None, switches.RANDOMISED, NOW)
         for skill in (first_skill, second_skill, other_unit_skill)
      }
      strata = {
         row.unit_id: row.stratum
         for row in db.query(models.ExperimentAssignment).filter_by(experiment=switches.TUTOR_PROFILE)
      }

   assert strata == {first_skill: "02", second_skill: "02", other_unit_skill: "06"}
   assert arms[first_skill] != arms[second_skill]


def test_the_three_earlier_definitions_keep_their_strata():
   feedback = switches.DEFINITIONS[switches.FEEDBACK_ELABORATION]
   retrieval = switches.DEFINITIONS[switches.RETRIEVAL_ENTRY]
   lesson = switches.DEFINITIONS[switches.LESSON_FIRST_CONTACT]

   assert (feedback.stratum, retrieval.stratum, lesson.stratum) == (None, None, None)
   assert switches.stratum_for(feedback, "BC-SKL-01001", 0.8) == "BC-SKL-01001|high"
   assert switches.stratum_for(feedback, "BC-SKL-01001", 0.2) == "BC-SKL-01001|low"
   assert switches.stratum_for(feedback, "BC-SKL-01001", None) == "BC-SKL-01001|unknown"
   assert switches.stratum_for(retrieval, "BC-SKL-02005", None) == "BC-SKL-02005"
   assert switches.stratum_for(lesson, "BC-UNIT-02", None) == "BC-UNIT-02"
