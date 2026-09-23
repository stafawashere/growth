from app.review import audit
from app.review import verdicts


def make_record(**overrides):
   record = {
      "item_id": "ITM-001",
      "verdict": "clean",
      "auditor": "operator",
      "audited_at": "2027-01-05T00:00:00",
   }
   record.update(overrides)

   return record


def test_a_well_formed_verdict_has_no_violations():
   record = make_record()

   assert verdicts.verdict_violations(record) == []


def test_an_unknown_verdict_string_is_a_violation():
   record = make_record(verdict="mostly_fine")

   violations = verdicts.verdict_violations(record)

   assert len(violations) == 1


def test_an_ambiguous_verdict_without_a_second_answer_is_a_violation():
   record = make_record(verdict="ambiguous")

   violations = verdicts.verdict_violations(record)

   assert len(violations) == 1


def test_a_clean_verdict_needs_no_second_answer():
   record = make_record(verdict="clean")

   assert verdicts.verdict_violations(record) == []


def test_completeness_names_the_ids_with_no_verdict():
   sample_ids = ["ITM-001", "ITM-002", "ITM-003"]
   records = [make_record(item_id="ITM-001")]

   result = verdicts.audit_completeness(records, sample_ids)

   assert result["missing_ids"] == ["ITM-002", "ITM-003"]


def test_the_rate_is_none_when_a_verdict_is_missing():
   sample_ids = ["ITM-001", "ITM-002"]
   records = [make_record(item_id="ITM-001")]

   result = verdicts.audit_completeness(records, sample_ids)

   assert result["key_error_rate"] is None


def test_the_rate_counts_key_wrong_and_ambiguous_over_the_sample():
   sample_ids = ["ITM-001", "ITM-002", "ITM-003", "ITM-004"]
   records = [
      make_record(item_id="ITM-001", verdict="clean"),
      make_record(item_id="ITM-002", verdict="key_wrong"),
      make_record(item_id="ITM-003", verdict="ambiguous", second_answer="x = 3"),
      make_record(item_id="ITM-004", verdict="clean"),
   ]

   result = verdicts.audit_completeness(records, sample_ids)

   assert result["key_error_rate"] == 0.5


def test_a_verdict_for_an_id_outside_the_sample_is_reported():
   sample_ids = ["ITM-001"]
   records = [
      make_record(item_id="ITM-001"),
      make_record(item_id="ITM-999"),
   ]

   result = verdicts.audit_completeness(records, sample_ids)

   assert result["out_of_sample_ids"] == ["ITM-999"]


def test_the_verdict_vocabulary_is_read_from_the_audit_module():
   assert verdicts.VERDICTS is audit.VERDICTS


audit_completeness = verdicts.audit_completeness


def well_formed(item_id, verdict="clean"):
   record = {
      "item_id": item_id,
      "verdict": verdict,
      "auditor": "operator",
      "audited_at": "2026-09-20T09:00:00+00:00",
   }

   is_ambiguous = verdict == audit.VERDICT_AMBIGUOUS

   if is_ambiguous:
      record["second_answer"] = "the other reading of the stem"

   return record


def test_a_malformed_verdict_makes_the_sample_incomplete():
   sample = [f"ITM-{index:03d}" for index in range(4)]
   records = [well_formed(item_id) for item_id in sample[:3]]
   records.append({**well_formed(sample[3]), "verdict": "mostly_fine"})

   result = audit_completeness(records, sample)

   assert sample[3] in result["invalid_ids"]
   assert result["key_error_rate"] is None


def test_a_verdict_outside_the_vocabulary_is_never_counted_as_clean():
   sample = ["ITM-000", "ITM-001"]
   records = [well_formed("ITM-000"), {**well_formed("ITM-001"), "verdict": None}]

   result = audit_completeness(records, sample)

   assert result["key_error_rate"] is None
   assert "ITM-001" in result["invalid_ids"]


def test_an_ambiguous_verdict_without_its_second_answer_blocks_the_rate():
   sample = ["ITM-000"]
   record = well_formed("ITM-000", audit.VERDICT_AMBIGUOUS)
   record.pop("second_answer")

   result = audit_completeness([record], sample)

   assert "ITM-000" in result["invalid_ids"]
   assert result["key_error_rate"] is None


def test_a_wholly_sound_sample_still_publishes_its_rate():
   sample = ["ITM-000", "ITM-001", "ITM-002", "ITM-003"]
   records = [
      well_formed("ITM-000"),
      well_formed("ITM-001"),
      well_formed("ITM-002", audit.VERDICT_KEY_WRONG),
      well_formed("ITM-003", audit.VERDICT_AMBIGUOUS),
   ]

   result = audit_completeness(records, sample)

   assert result["invalid_ids"] == []
   assert result["key_error_rate"] == 0.5


def test_a_record_with_no_item_id_is_reported_rather_than_raising():
   result = audit_completeness([{"verdict": "clean"}, well_formed("ITM-000")], ["ITM-000"])

   assert result["key_error_rate"] is None
   assert result["unidentified_records"] == 1
