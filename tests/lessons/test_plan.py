"""plan_lesson: determinism and the band caps of invariant L13, and the band table and refresher
rules of docs/plan/15-lessons.md."""
import copy
import itertools

import pytest

from app.lessons import constants
from app.lessons.plan import REASONS, plan_lesson
from tests.lessons.conftest import load_fixture

ERROR_SETS = ((), ("BC-ERR-02020",), ("BC-ERR-02024", "BC-ERR-02020"), ("BC-ERR-99999",))
PREREQUISITE_SETS = ((), ("BC-PRQ-06002",), ("BC-SKL-02031",))
BANDS = ("low", "mid", "none")
RECENT_T4 = {"refresher_reason": "T4", "days_since_refresher": 1}
LESSON_STATES = (None, RECENT_T4, {"refresher_reason": "T2", "days_since_refresher": 9})


def lessons_under_test(hand_authored):
   return [hand_authored, load_fixture("decision_clean.json")]


def every_plan_input():
   return itertools.product(BANDS, REASONS, ERROR_SETS, PREREQUISITE_SETS, LESSON_STATES)


def section_ids(plan):
   return [ref.id for ref in plan.sections]


def is_repeat_t4(state):
   has_state = state is not None
   was_t4 = has_state and state.get("refresher_reason") == "T4"

   return was_t4 and state["days_since_refresher"] < constants.REFRESHER_MIN_GAP_DAYS


def test_the_same_inputs_give_the_same_plan(hand_authored):
   for band, reason, errors, prerequisites, state in every_plan_input():
      first = plan_lesson(hand_authored, band, reason, errors, prerequisites, state)
      second = plan_lesson(copy.deepcopy(hand_authored), band, reason, errors, prerequisites, state)

      assert first == second
      assert first.as_dict() == second.as_dict()


def test_no_plan_exceeds_its_band_caps(hand_authored):
   for lesson in lessons_under_test(hand_authored):
      for band, reason, errors, prerequisites, state in every_plan_input():
         served = plan_lesson(lesson, band, reason, errors, prerequisites, state)
         is_first_contact = reason == "first_contact"
         is_first_t4 = reason == "T4" and not is_repeat_t4(state)
         is_refresher = reason in ("T1", "T2", "T3", "T4", "T5", "read_again") and not is_first_t4

         if band == "low" and (is_first_contact or is_first_t4):
            assert served.minutes <= constants.LESSON_READ_MINUTES_MAX
            assert served.words <= constants.LESSON_WORDS_FULL_MAX

         if band == "mid" and is_first_contact:
            assert served.minutes <= constants.LESSON_BRIEF_MINUTES_MAX
            assert served.words <= constants.LESSON_WORDS_BRIEF_MAX

         if is_refresher and band != "none":
            assert served.minutes <= constants.REFRESHER_MINUTES_MAX
            assert served.words <= constants.REFRESHER_MINUTES_MAX * constants.WORDS_PER_MINUTE

         if band == "none":
            assert served.minutes == 0
            assert served.sections == ()


def test_an_over_long_lesson_is_trimmed_to_the_cap_and_keeps_its_teaching(hand_authored):
   bloated = copy.deepcopy(hand_authored)
   second_example = next(section for section in bloated["sections"] if section["id"].endswith("#s6"))
   second_example["steps"][0]["why"] = "word " * 800

   served = plan_lesson(bloated, "low", "first_contact")
   kept = section_ids(served)

   assert served.words <= constants.LESSON_WORDS_FULL_MAX
   assert "LSN-CON-02013#s6" not in kept
   assert "LSN-CON-02013#s2" in kept
   assert "LSN-CON-02013#s5" in kept


def test_low_band_serves_the_full_form_in_table_order(hand_authored):
   served = plan_lesson(hand_authored, "low", "first_contact")
   kinds = [ref.type for ref in served.sections]

   assert kinds == [
      "orientation",
      "key_ideas",
      "strategy",
      "strategy",
      "worked_example",
      "what_a_reader_scores",
      "common_error",
      "common_error",
      "common_error",
      "check",
      "worked_example",
      "what_a_reader_scores",
      "check",
      "check",
   ]
   assert len(served.checks) == 3
   assert served.minutes == hand_authored["read_minutes"]["full"]


def test_mid_band_serves_the_brief_form(hand_authored):
   served = plan_lesson(hand_authored, "mid", "first_contact")
   kinds = [ref.type for ref in served.sections]

   assert kinds.count("worked_example") == 1
   assert kinds.count("strategy") == 1
   assert kinds.count("common_error") == constants.MID_ERRORS
   assert len(served.checks) == constants.LESSON_CHECKS_MIN
   assert served.minutes == hand_authored["read_minutes"]["brief"]


def test_the_top_band_inserts_nothing(hand_authored):
   served = plan_lesson(hand_authored, "none", "first_contact")

   assert served.sections == ()
   assert served.minutes == 0.0


def test_a_first_contact_plan_is_not_reordered_by_an_error(hand_authored):
   plain = plan_lesson(hand_authored, "low", "first_contact")
   named = plan_lesson(hand_authored, "low", "first_contact", error_ids=("BC-ERR-02024",))

   assert section_ids(plain) == section_ids(named)


def test_feedback_returns_only_the_anchor_of_the_named_error(hand_authored):
   served = plan_lesson(hand_authored, "low", "feedback", error_ids=("BC-ERR-02024", "BC-ERR-99999"))

   assert served.anchors == ("LSN-CON-02013#err-BC-ERR-02024",)
   assert served.sections == ()


def test_t1_serves_the_named_error_before_the_core_key_ideas(hand_authored):
   served = plan_lesson(hand_authored, "low", "T1", error_ids=("BC-ERR-02024",))

   assert section_ids(served) == ["LSN-CON-02013#err-BC-ERR-02024", "LSN-CON-02013#s2"]
   assert served.anchors == ("LSN-CON-02013#err-BC-ERR-02024",)


def test_t2_ends_with_example_one_collapsed(hand_authored):
   served = plan_lesson(hand_authored, "low", "T2")
   last = served.sections[-1]

   assert last.id == "LSN-CON-02013#s5"
   assert last.form == "steps_only"
   assert served.sections[0].type == "key_ideas"


def test_t3_without_a_bridge_or_error_falls_back_to_the_core_key_ideas(hand_authored):
   served = plan_lesson(hand_authored, "low", "T3", prerequisite_ids=("BC-PRQ-06002",))

   assert section_ids(served) == ["LSN-CON-02013#s2"]


def test_a_second_t4_inside_the_gap_serves_only_the_refresher_subset(hand_authored):
   first = plan_lesson(hand_authored, "low", "T4")
   repeat = plan_lesson(hand_authored, "low", "T4", lesson_state=RECENT_T4)
   first_types = [ref.type for ref in first.sections]
   repeat_types = [ref.type for ref in repeat.sections]

   assert "orientation" in first_types
   assert "check" not in first_types
   assert "orientation" not in repeat_types
   assert repeat.minutes <= constants.REFRESHER_MINUTES_MAX


def test_an_unknown_reason_is_refused(hand_authored):
   with pytest.raises(ValueError):
      plan_lesson(hand_authored, "low", "T9")
