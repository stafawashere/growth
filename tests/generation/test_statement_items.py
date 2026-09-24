"""Statement-keyed items: a verdict or classification chosen among labelled options.

A statement item has nothing a student could type into the math field, so serving it as R29's
short answer would ask for an answer the grader cannot read, and ingest has no MathJSON key to
compare; both paths are checked here.
"""
from app.engine.select import format_for_item
from app.engine.state import FadingStage, ResponseFormat
from app.items import ingest

ERROR_IDS = frozenset({"BC-ERR-10003", "BC-ERR-10018", "BC-ERR-10023"})


def statement_record(**changes):
   record = {
      "id": "ITM-GEN-10007-00",
      "archetype_id": "BC-QA-10007",
      "answer_key": {"form": "statement", "label": "The series converges conditionally."},
      "options": [
         {"id": "A", "label": "The series converges absolutely.", "is_key": False, "error_path": "BC-ERR-10023"},
         {"id": "B", "label": "The series converges conditionally.", "is_key": True, "error_path": None},
         {"id": "C", "label": "The series diverges.", "is_key": False, "error_path": "BC-ERR-10003"},
         {"id": "D", "label": "The series converges.", "is_key": False, "error_path": "BC-ERR-10018"},
      ],
   }
   record.update(changes)

   return record


def outcomes(record):
   return {result["check_type"]: result["outcome"] for result in ingest.run_checks(record, ERROR_IDS)}


def test_a_statement_item_is_a_choice_on_the_turn_r29_gives_short_answer():
   item = {"archetype_id": "BC-QA-10007", "options": statement_record()["options"], "requires_choice": True}
   value_item = {"archetype_id": "BC-QA-10007", "options": [{"id": "A", "value": 3}], "requires_choice": False}

   assert format_for_item([], item, FadingStage.UNSUPPORTED) == ResponseFormat.MCQ
   assert format_for_item([], item, FadingStage.EXAMPLE) == ResponseFormat.MCQ
   assert format_for_item([], value_item, FadingStage.UNSUPPORTED) == ResponseFormat.SHORT_ANSWER


def test_a_well_formed_statement_record_passes_ingest():
   assert outcomes(statement_record()) == {"statement_key": "pass", "distractor_distinct": "pass"}


def test_a_key_label_that_no_option_marked_as_key_carries_is_rejected():
   record = statement_record(answer_key={"form": "statement", "label": "The series diverges."})

   assert outcomes(record)["statement_key"] == "fail"


def test_two_options_with_one_label_are_rejected():
   record = statement_record()
   record["options"][2]["label"] = "The series converges absolutely."

   assert outcomes(record)["distractor_distinct"] == "fail"


def test_a_distractor_whose_error_is_not_held_is_rejected():
   record = statement_record()
   record["options"][3]["error_path"] = "BC-ERR-06014"

   assert outcomes(record)["distractor_distinct"] == "fail"


def test_the_bank_marks_a_statement_keyed_row_as_always_a_choice():
   import json
   from types import SimpleNamespace

   from app.runtime.bank import _as_item_dict

   def row(answer_key):
      return SimpleNamespace(
         id="ITM-GEN-10007-00", archetype_id="BC-QA-10007", variant_id=None, snapshot_id=None,
         parameter_draw=None, stem="Classify the series.", figure_spec=None,
         options=statement_record()["options"], calculator_status="no_calculator",
         representation="BC-REP-11", difficulty_settings=None, skills=None, status="verified",
         answer_key=json.dumps(answer_key),
      )

   assert _as_item_dict(row({"form": "statement", "label": "The series diverges."}))["requires_choice"] is True
   assert _as_item_dict(row({"form": "symbolic", "mathjson": 3}))["requires_choice"] is False


def test_gate_30s_checker_reads_a_statement_item_by_its_labels():
   from app.items.distractor_paths import distractor_path_violations

   clean = statement_record()
   repeated = statement_record()
   repeated["options"][3]["label"] = repeated["options"][0]["label"]

   assert distractor_path_violations(clean, ERROR_IDS) == []
   assert any("same label" in violation for violation in distractor_path_violations(repeated, ERROR_IDS))
