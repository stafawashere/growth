"""app/lessons/source.py: reader_checks is a pure function of BC-PT fields (L15) and
authoring_bundle assembles the plan's inputs without the Official mapping subsection."""
import copy
from types import SimpleNamespace

import pytest

from app.lessons import constants
from app.lessons.source import authoring_bundle, reader_checks

BASE_RECORD = {
   "id": "BC-PT-90001",
   "name": "Probe point",
   "earns": "The value with its setup.",
   "does_not_earn": "A bare value.",
   "notation_requirements": "No special notation requirement stated in the rubrics reviewed.",
   "precision_rules": "Not a reported-value point, so the three-decimal rule does not apply.",
   "units_required": "no",
   "hypotheses_required": "no",
}


def stub_snapshot(*records):
   return SimpleNamespace(scoring_points={record["id"]: record for record in records})


def record_with(**changes):
   record = copy.deepcopy(BASE_RECORD)
   record.update(changes)

   return record


def with_errors(snapshot, errors):
   return SimpleNamespace(**{**vars(snapshot), "errors": errors})


def test_reader_checks_states_earned_and_not_earned_and_nothing_else_for_a_plain_point():
   snapshot = stub_snapshot(record_with())

   lines = reader_checks(["BC-PT-90001"], snapshot)

   assert lines == [
      {"point_type_id": "BC-PT-90001", "text": "Probe point. Earned by: The value with its setup. Not earned by: A bare value."}
   ]


def test_reader_checks_adds_the_conditions_the_record_states():
   record = record_with(
      notation_requirements="Write the equation, not a bare expression.",
      precision_rules="Three decimal places.",
      units_required="yes",
      hypotheses_required="yes",
   )

   text = reader_checks(["BC-PT-90001"], stub_snapshot(record))[0]["text"]

   assert "Notation: Write the equation, not a bare expression." in text
   assert "Precision: Three decimal places." in text
   assert "Units are required on the answer." in text
   assert "The hypotheses of the theorem must be stated." in text


def test_reader_checks_is_pure_and_leaves_the_records_alone():
   snapshot = stub_snapshot(record_with(), record_with(id="BC-PT-90002", name="Other"))
   before = copy.deepcopy(snapshot.scoring_points)

   first = reader_checks(["BC-PT-90002", "BC-PT-90001"], snapshot)
   second = reader_checks(["BC-PT-90002", "BC-PT-90001"], snapshot)

   assert first == second
   assert [line["point_type_id"] for line in first] == ["BC-PT-90002", "BC-PT-90001"]
   assert snapshot.scoring_points == before


def test_reader_checks_lists_a_point_once_and_stops_at_the_cap():
   records = [record_with(id=f"BC-PT-9000{index}") for index in range(1, 9)]
   snapshot = stub_snapshot(*records)
   ids = ["BC-PT-90001", "BC-PT-90001"] + [record["id"] for record in records]

   lines = reader_checks(ids, snapshot)

   assert len(lines) == constants.READER_CHECK_LINES_MAX
   assert lines[0]["point_type_id"] == "BC-PT-90001"
   assert len({line["point_type_id"] for line in lines}) == len(lines)


def test_reader_checks_refuses_a_point_the_snapshot_does_not_hold():
   with pytest.raises(KeyError):
      reader_checks(["BC-PT-00000"], stub_snapshot(record_with()))


def test_reader_checks_over_the_real_product_rule_point(snapshot):
   lines = reader_checks(["BC-PT-99022"], snapshot)
   record = snapshot.scoring_points["BC-PT-99022"]

   assert lines[0]["text"].startswith(f"{record['name']}. Earned by: {record['earns']}")
   assert record["does_not_earn"] in lines[0]["text"]


def test_bundle_drops_the_official_mapping_and_keeps_the_topic_body(snapshot):
   bundle = authoring_bundle("BC-CON-02013", snapshot)
   section = bundle["topic_sections"]["BC-TOP-0208"]

   assert section.startswith("## 2.8 The Product Rule")
   assert "### Official mapping" not in section
   assert "### Required mathematical knowledge" in section
   assert "### Assessment behaviour" in section


def test_bundle_orders_errors_by_severity_then_id_and_names_the_cited_pages(snapshot):
   bundle = authoring_bundle("BC-CON-02013", snapshot)

   assert [error["id"] for error in bundle["errors"]] == ["BC-ERR-02020", "BC-ERR-02023", "BC-ERR-02024"]
   assert bundle["ced_sources"] == ["ced:67", "ced:68"]
   assert sorted(bundle["ced_pages"]) == ["ced:67", "ced:68"]
   assert [archetype["id"] for archetype in bundle["archetypes"]] == ["BC-QA-02008", "BC-QA-02009"]


def test_bundle_digest_is_stable_and_ignores_date_stamps(snapshot):
   first = authoring_bundle("BC-CON-02013", snapshot)["source_digest"]
   second = authoring_bundle("BC-CON-02013", snapshot)["source_digest"]
   restamped_errors = copy.deepcopy(snapshot.errors)
   restamped_errors["BC-ERR-02020"]["updated"] = "2099-01-01"

   after_restamp = authoring_bundle("BC-CON-02013", with_errors(snapshot, restamped_errors))["source_digest"]

   assert first == second
   assert first == after_restamp


def test_bundle_digest_moves_when_a_used_record_changes(snapshot):
   before = authoring_bundle("BC-CON-02013", snapshot)["source_digest"]
   edited_errors = copy.deepcopy(snapshot.errors)
   edited_errors["BC-ERR-02020"]["observed_behavior"] = "changed"

   after = authoring_bundle("BC-CON-02013", with_errors(snapshot, edited_errors))["source_digest"]

   assert before != after
