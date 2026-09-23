import json

import pytest

from app.db import models
from app.engine.state import ResponseFormat
from app.engine.update import MasteryState, rule_based_mastery_states
from app.items import grade as grade_module
from app.items.grade import grade

ARCHETYPE = {"id": "BC-ARC-05001", "skills": ["BC-SKL-05022", "BC-SKL-05017", "BC-SKL-01045"]}

ERRORS = {
   "BC-ERR-05001": {
      "id": "BC-ERR-05001",
      "skills": ["BC-SKL-05017", "BC-SKL-01045", "BC-SKL-09999"],
   },
   "BC-ERR-05002": {"id": "BC-ERR-05002", "skills": []},
}


def build_item(answer_key, options=None, skills=None):
   loaded = skills if skills is not None else ARCHETYPE["skills"]

   return models.Item(
      id="ITM-test",
      archetype_id=ARCHETYPE["id"],
      variant_id=None,
      snapshot_id="SNAP-1",
      parameter_draw=json.dumps({}),
      stem=json.dumps({"text": "stem"}),
      figure_spec=None,
      options=options,
      answer_key=json.dumps(answer_key),
      worked_solution=json.dumps([]),
      calculator_status="no_calculator",
      representation="BC-REP-01",
      difficulty_settings=json.dumps([]),
      skills=json.dumps(loaded),
      provenance=json.dumps({"model": "operator"}),
      status="verified",
      dedupe_minhash=json.dumps([]),
      created_at="2026-09-19",
      updated_at="2026-09-19",
   )


def mcq_item(options):
   key = {"form": "option_id", "mathjson": ["Multiply", 2, "x"]}

   return build_item(key, options=options)


def symbolic_item(units=None):
   key = {"form": "symbolic", "mathjson": ["Multiply", 2, "x"]}

   if units is not None:
      key["units"] = units

   return build_item(key)


STANDARD_OPTIONS = [
   {"id": "A", "value": ["Multiply", 2, "x"], "is_key": True, "error_path": None},
   {"id": "B", "value": ["Multiply", 3, "x"], "is_key": False, "error_path": "BC-ERR-05001"},
   {"id": "C", "value": ["Multiply", 4, "x"], "is_key": False, "error_path": "BC-ERR-05002"},
]


def test_mcq_selection_compared_to_the_key():
   result = grade(mcq_item(STANDARD_OPTIONS), {"selected_option_id": "A"}, ERRORS)

   assert result["correct"] is True
   assert result["equivalent_but_misnotated"] is False
   assert result["error_path"] is None
   assert result["error_path_skills"] == []
   assert rule_based_mastery_states(ARCHETYPE, result) == {
      skill: MasteryState.MASTERED for skill in ARCHETYPE["skills"]
   }


def test_mcq_distractor_yields_its_error_path_skills():
   result = grade(mcq_item(STANDARD_OPTIONS), {"selected_option_id": "B"}, ERRORS)

   assert result["correct"] is False
   assert result["error_path"] == "BC-ERR-05001"
   assert result["error_path_skills"] == ["BC-SKL-05017", "BC-SKL-01045"]
   assert rule_based_mastery_states(ARCHETYPE, result) == {
      "BC-SKL-05022": MasteryState.NOT_ATTEMPTED,
      "BC-SKL-05017": MasteryState.NOT_MASTERED,
      "BC-SKL-01045": MasteryState.NOT_MASTERED,
   }


def test_mcq_option_set_without_exactly_one_key_is_refused():
   two_keys = [
      {"id": "A", "value": ["Multiply", 2, "x"], "is_key": True, "error_path": None},
      {"id": "B", "value": ["Multiply", 3, "x"], "is_key": True, "error_path": None},
   ]
   result = grade(mcq_item(two_keys), {"selected_option_id": "A"}, ERRORS)

   assert result["correct"] is None
   assert "key" in result["reason"]


def test_mcq_unknown_option_id_is_refused_not_wrong():
   result = grade(mcq_item(STANDARD_OPTIONS), {"selected_option_id": "Z"}, ERRORS)

   assert result["correct"] is None
   assert result["error_path"] is None
   assert "Z" in result["reason"]


def test_short_answer_equivalence_decides_correct():
   submission = {"mathjson": ["Add", ["Multiply", 1, "x"], "x"]}
   result = grade(symbolic_item(), submission, ERRORS)

   assert result["correct"] is True
   assert result["equivalent_but_misnotated"] is False
   assert result["error_path"] is None


def test_short_answer_unequal_blames_the_primary_skill_only():
   result = grade(symbolic_item(), {"mathjson": ["Multiply", 5, "x"]}, ERRORS)

   assert result["correct"] is False
   assert result["error_path"] is None
   assert result["error_path_skills"] == []
   assert rule_based_mastery_states(ARCHETYPE, result) == {
      "BC-SKL-05022": MasteryState.NOT_MASTERED,
      "BC-SKL-05017": MasteryState.NOT_ATTEMPTED,
      "BC-SKL-01045": MasteryState.NOT_ATTEMPTED,
   }


def test_numeric_key_is_compared_to_three_decimal_places():
   key = {"form": "numeric", "mathjson": 2.718282, "numeric": 2.718282, "decimals": 3}
   item = build_item(key)

   assert grade(item, {"mathjson": 2.718}, ERRORS)["correct"] is True
   assert grade(item, {"mathjson": 2.71}, ERRORS)["correct"] is False


def test_units_declared_but_absent_is_notation_only():
   key = {"form": "numeric", "mathjson": 12.5, "numeric": 12.5, "decimals": 3, "units": "m/sec"}
   item = build_item(key)

   missing_units = grade(item, {"mathjson": 12.5}, ERRORS)

   assert missing_units["correct"] is True
   assert missing_units["equivalent_but_misnotated"] is True
   assert rule_based_mastery_states(ARCHETYPE, missing_units) == {
      skill: MasteryState.NOTATION_ONLY for skill in ARCHETYPE["skills"]
   }

   wrong_units = grade(item, {"mathjson": 12.5, "units": "meters"}, ERRORS)

   assert wrong_units["correct"] is False
   assert wrong_units["equivalent_but_misnotated"] is False

   matching_units = grade(item, {"mathjson": 12.5, "units": " M/Sec "}, ERRORS)

   assert matching_units["correct"] is True
   assert matching_units["equivalent_but_misnotated"] is False


def numeric_item_with_units(units):
   key = {"form": "numeric", "mathjson": 12.5, "numeric": 12.5, "decimals": 3, "units": units}

   return build_item(key)


@pytest.mark.parametrize(
   "key_units, submitted_units",
   [
      ("m/sec", "meters"),
      ("m/sec", "m^2"),
      ("ft/s", "ft"),
      ("ft^2", "ft^3"),
      ("m/sec", "cm/sec"),
      ("ft/s", "m/s"),
      ("ft", "mi"),
      ("s", "h"),
      ("m^2", "ft^2"),
      ("L", "m^3"),
      ("mm", "Mm"),
   ],
)
def test_a_different_unit_earns_no_notation_credit(key_units, submitted_units):
   item = numeric_item_with_units(key_units)

   result = grade(item, {"mathjson": 12.5, "units": submitted_units}, ERRORS)

   assert result["equivalent_but_misnotated"] is False
   assert result["correct"] is False
   assert rule_based_mastery_states(ARCHETYPE, result) == {
      "BC-SKL-05022": MasteryState.NOT_MASTERED,
      "BC-SKL-05017": MasteryState.NOT_ATTEMPTED,
      "BC-SKL-01045": MasteryState.NOT_ATTEMPTED,
   }


@pytest.mark.parametrize(
   "key_units, submitted_units",
   [
      ("m/sec", "m/s"),
      ("m/s", "meters per second"),
      ("ft/s", "feet per second"),
      ("m^2", "m*m"),
   ],
)
def test_the_same_unit_written_differently_keeps_notation_credit(
   key_units, submitted_units
):
   item = numeric_item_with_units(key_units)

   result = grade(item, {"mathjson": 12.5, "units": submitted_units}, ERRORS)

   assert result["correct"] is True
   assert result["equivalent_but_misnotated"] is True
   assert rule_based_mastery_states(ARCHETYPE, result) == {
      skill: MasteryState.NOTATION_ONLY for skill in ARCHETYPE["skills"]
   }


def test_a_speed_in_metres_per_second_against_a_key_in_feet_per_second_is_wrong():
   item = numeric_item_with_units("ft/s")

   result = grade(item, {"mathjson": 12.5, "units": "m/s"}, ERRORS)

   assert result["correct"] is False
   assert result["equivalent_but_misnotated"] is False


def test_unit_symbols_are_case_sensitive():
   item = numeric_item_with_units("mm")

   result = grade(item, {"mathjson": 12.5, "units": "Mm"}, ERRORS)

   assert result["correct"] is False
   assert result["equivalent_but_misnotated"] is False

   unreadable_capital = grade(numeric_item_with_units("m"), {"mathjson": 12.5, "units": "M"}, ERRORS)

   assert unreadable_capital["correct"] is True
   assert unreadable_capital["equivalent_but_misnotated"] is False

   readable_capital = grade(numeric_item_with_units("mm"), {"mathjson": 12.5, "units": "MM"}, ERRORS)

   assert readable_capital["correct"] is True
   assert readable_capital["equivalent_but_misnotated"] is False


def test_a_physical_constant_is_not_a_unit():
   item = numeric_item_with_units("m")

   result = grade(item, {"mathjson": 12.5, "units": "c*s"}, ERRORS)

   assert result["correct"] is None
   assert result["equivalent_but_misnotated"] is False
   assert result["reason"] is not None


def test_units_that_name_no_known_unit_are_ungraded():
   item = numeric_item_with_units("m/sec")

   result = grade(item, {"mathjson": 12.5, "units": "__import__('os')"}, ERRORS)

   assert result["correct"] is None
   assert result["equivalent_but_misnotated"] is False
   assert result["reason"] is not None


def test_units_absent_from_the_key_never_reports_misnotation():
   result = grade(symbolic_item(), {"mathjson": ["Multiply", 2, "x"], "units": "m/sec"}, ERRORS)

   assert result["correct"] is True
   assert result["equivalent_but_misnotated"] is False


def test_unparseable_submission_is_ungraded():
   result = grade(symbolic_item(), {"mathjson": ["Bogus", 1]}, ERRORS)

   assert result["correct"] is None
   assert result["equivalent_but_misnotated"] is False
   assert result["error_path_skills"] == []
   assert "Bogus" in result["reason"] or "parse" in result["reason"]


def test_indeterminate_comparison_is_ungraded(monkeypatch):
   monkeypatch.setattr(grade_module, "equivalence", lambda left, right: "unsettled")
   monkeypatch.setattr(grade_module, "numeric_check", lambda left, right, **kwargs: None)

   result = grade(symbolic_item(), {"mathjson": ["Multiply", 2, "x"]}, ERRORS)

   assert result["correct"] is None
   assert "settle" in result["reason"] or "indeterminate" in result["reason"]


def test_empty_submission_is_ungraded():
   result = grade(symbolic_item(), {}, ERRORS)

   assert result["correct"] is None


def test_result_keys_match_what_the_mastery_rule_reads():
   result = grade(mcq_item(STANDARD_OPTIONS), {"selected_option_id": "C"}, ERRORS)

   assert set(result) >= {
      "correct",
      "equivalent_but_misnotated",
      "error_path",
      "error_path_skills",
      "reason",
   }
   assert result["error_path_skills"] == []


def test_served_format_decides_the_grading_path():
   key = {"form": "symbolic", "mathjson": ["Multiply", 2, "x"]}
   item = build_item(key, options=STANDARD_OPTIONS)

   as_short_answer = grade(
      item, {"mathjson": ["Add", "x", "x"]}, ERRORS, ResponseFormat.SHORT_ANSWER
   )

   assert as_short_answer["correct"] is True
   assert as_short_answer["error_path"] is None

   wrong_short_answer = grade(
      item, {"mathjson": ["Multiply", 3, "x"]}, ERRORS, ResponseFormat.SHORT_ANSWER.value
   )

   assert wrong_short_answer["correct"] is False
   assert wrong_short_answer["error_path"] is None

   as_mcq = grade(item, {"selected_option_id": "B"}, ERRORS, "mcq")

   assert as_mcq["correct"] is False
   assert as_mcq["error_path"] == "BC-ERR-05001"


def test_submission_shape_that_contradicts_the_served_format_is_refused():
   key = {"form": "symbolic", "mathjson": ["Multiply", 2, "x"]}
   item = build_item(key, options=STANDARD_OPTIONS)

   option_id_on_a_short_answer = grade(
      item, {"selected_option_id": "B"}, ERRORS, ResponseFormat.SHORT_ANSWER
   )

   assert option_id_on_a_short_answer["correct"] is None
   assert option_id_on_a_short_answer["error_path"] is None
   assert "short_answer" in option_id_on_a_short_answer["reason"]

   mathjson_on_an_mcq = grade(
      item, {"mathjson": ["Multiply", 2, "x"]}, ERRORS, ResponseFormat.MCQ
   )

   assert mathjson_on_an_mcq["correct"] is None
   assert "mcq" in mathjson_on_an_mcq["reason"]
