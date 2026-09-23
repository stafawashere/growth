"""Tests for app/items/ingest.py, the hand-authored item path of gates 17 and 18 in
docs/plan/11-phased-delivery.md and the checks of docs/plan/04-item-generation.md.

The operator's fixture directory tests/fixtures/items_p1/ does not exist yet, so these tests
build their own records and write them to tmp_path in the same one-JSON-file-per-item shape.
"""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.items import ingest

ACTIVE_ERROR_IDS = {"BC-ERR-00001", "BC-ERR-00002", "BC-ERR-00003"}
SNAPSHOT_ID = "SNAP-0001"
NOW = "2026-09-19T09:00:00+00:00"


def good_record(item_id="ITM-0001"):
   return {
      "id": item_id,
      "archetype_id": "BC-QA-01004",
      "variant_id": "BC-QV-01004-01",
      "format": "mcq",
      "stem": {"text": "Differentiate f with respect to x."},
      "answer_key": {"form": "symbolic", "mathjson": ["Multiply", 2, "x"]},
      "worked_solution": [
         {"step": 1, "text": "Apply the power rule.", "mathjson": ["Multiply", 2, "x"]},
      ],
      "options": [
         {"id": "A", "value": ["Add", ["Multiply", 2, "x"], 0], "is_key": True, "error_path": None},
         {"id": "B", "value": ["Multiply", 2, ["Power", "x", 2]], "is_key": False, "error_path": "BC-ERR-00001"},
         {"id": "C", "value": ["Power", "x", 2], "is_key": False, "error_path": "BC-ERR-00002"},
         {"id": "D", "value": 2, "is_key": False, "error_path": "BC-ERR-00003"},
      ],
      "calculator_status": "no_calculator",
      "representation": "BC-REP-01",
      "difficulty_settings": [{"difficulty_factor_id": "BC-DF-01", "setting": "low"}],
      "skills": ["BC-SKL-01024"],
      "parameter_draw": {"coefficient": 2},
      "authored_on": "2026-09-19",
   }


def write_records(directory, records):
   directory.mkdir(parents=True, exist_ok=True)

   for record in records:
      path = directory / f"{record['id']}.json"
      path.write_text(json.dumps(record))

   return directory


def open_db(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   return OrmSession(engine)


def test_ingest_publishes_an_item_whose_key_passes_every_check(tmp_path):
   directory = write_records(tmp_path / "items_p1", [good_record()])

   with open_db(tmp_path) as db:
      results = ingest.ingest_directory(db, directory, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      assert len(results) == 1
      assert results[0]["status"] == "verified"

      row = db.get(models.Item, "ITM-0001")

      assert row is not None
      assert row.status == "verified"
      assert row.archetype_id == "BC-QA-01004"
      assert row.snapshot_id == SNAPSHOT_ID

      provenance = json.loads(row.provenance)

      assert provenance["model"] == "operator"
      assert provenance["prompt_template_version"] is None
      assert provenance["generation_job_id"] is None
      assert provenance["authored_on"] == "2026-09-19"
      assert provenance["archetype_id"] == "BC-QA-01004"
      assert provenance["variant_id"] == "BC-QV-01004-01"
      assert "provenance" not in provenance

      queued = db.query(models.ReviewQueue).count()

      assert queued == 0


def test_ingested_stem_is_the_plain_text_not_the_wrapping_object(tmp_path):
   """A served item hands its stem straight to the student (app/runtime/bank.py
   _as_item_dict), so the row must hold the plain text of record["stem"]["text"], never the
   record's {"text": ...} wrapper serialized back into the column.
   """
   directory = write_records(tmp_path / "items_p1", [good_record()])

   with open_db(tmp_path) as db:
      ingest.ingest_directory(db, directory, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      row = db.get(models.Item, "ITM-0001")

      assert row.stem == "Differentiate f with respect to x."


def test_a_short_answer_item_carrying_mcq_options_still_ingests(tmp_path):
   """Operator ruling of 2026-09-23: every agent draft becomes MCQ-capable with four options
   regardless of its format field, and the served format (app/engine/select.py
   format_for_attempt) decides which is shown, not the record's own format. Nothing in this
   module reads format at all, so a short_answer record carrying a full option set is checked
   and ingested exactly like an mcq one.
   """
   record = good_record()
   record["format"] = "short_answer"
   directory = write_records(tmp_path / "items_p1", [record])

   with open_db(tmp_path) as db:
      results = ingest.ingest_directory(db, directory, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      assert len(results) == 1
      assert results[0]["status"] == "verified"

      row = db.get(models.Item, "ITM-0001")

      assert row is not None
      assert row.status == "verified"
      assert row.options is not None
      assert len(row.options) == 4


def test_ingest_refuses_a_seeded_bad_key(tmp_path):
   record = good_record("ITM-0002")
   record["answer_key"] = {"form": "symbolic", "mathjson": ["Power", "x", 2]}
   directory = write_records(tmp_path / "items_p1", [record])

   with open_db(tmp_path) as db:
      results = ingest.ingest_directory(db, directory, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      assert results[0]["status"] == "rejected"

      row = db.get(models.Item, "ITM-0002")

      assert row.status == "rejected"

      outcomes = {
         verification.check_type: verification.outcome
         for verification in db.query(models.ItemVerification).all()
      }

      assert outcomes["sympy_equivalence"] == "fail"
      assert outcomes["numeric_probe"] == "fail"


def test_indeterminate_check_routes_to_review_queue(tmp_path, monkeypatch):
   monkeypatch.setattr(ingest, "equivalence", lambda left, right: "unsettled")
   monkeypatch.setattr(ingest, "numeric_check", lambda left, right: None)

   record = good_record("ITM-0003")

   with open_db(tmp_path) as db:
      result = ingest.ingest_item(db, record, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      assert result["status"] == "draft"

      row = db.get(models.Item, "ITM-0003")

      assert row.status == "draft"

      outcomes = {
         verification.check_type: verification.outcome
         for verification in db.query(models.ItemVerification).all()
      }

      assert outcomes["sympy_equivalence"] == "indeterminate"

      queued = db.query(models.ReviewQueue).all()

      assert len(queued) == 1
      assert queued[0].kind == "item_verification_disagreement"
      assert queued[0].ref_id == "ITM-0003"
      assert queued[0].resolved_at is None


def test_verification_rows_written_per_check(tmp_path):
   record = good_record("ITM-0004")

   with open_db(tmp_path) as db:
      ingest.ingest_item(db, record, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      rows = db.query(models.ItemVerification).all()
      check_types = {row.check_type for row in rows}

      assert check_types == set(ingest.CHECK_TYPES)
      assert len(rows) == len(ingest.CHECK_TYPES)

      for row in rows:
         assert row.item_id == "ITM-0004"
         assert row.outcome == "pass"
         assert row.created_at == NOW
         assert json.loads(row.detail) is not None


def test_a_distractor_without_an_error_path_is_refused(tmp_path):
   """04 rejection rule 7: a non-key option carrying no error path is never published."""
   record = good_record("ITM-0005")
   record["options"][1] = {
      "id": "B",
      "value": ["Multiply", 2, ["Power", "x", 2]],
      "is_key": False,
      "error_path": None,
   }

   with open_db(tmp_path) as db:
      result = ingest.ingest_item(db, record, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      assert result["status"] == "rejected"

      outcomes = {
         verification.check_type: verification.outcome
         for verification in db.query(models.ItemVerification).all()
      }

      assert outcomes["distractor_distinct"] == "fail"


def test_the_key_is_read_from_is_key_not_from_a_null_error_path(tmp_path):
   """A distractor equal to the key is caught even when it is listed before the key."""
   record = good_record("ITM-0006")
   key = record["options"][0]
   duplicate = {"id": "B", "value": key["value"], "is_key": False, "error_path": "BC-ERR-00001"}
   record["options"] = [duplicate, key] + record["options"][2:]

   with open_db(tmp_path) as db:
      result = ingest.ingest_item(db, record, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      assert result["status"] == "rejected"


AGENT_AUTHOR = "claude-opus-5-5 agent draft, pending operator review"


def test_an_agent_draft_keeps_its_author_as_the_provenance_model(tmp_path):
   """The operator's ruling of 2026-09-23: an agent draft may be served but is never operator
   provenance, so exit criterion 7 and gates 17, 29 and 30 cannot count it by accident.
   """
   record = good_record("ITM-0007")
   record["authored_by"] = AGENT_AUTHOR

   with open_db(tmp_path) as db:
      ingest.ingest_item(db, record, ACTIVE_ERROR_IDS, SNAPSHOT_ID, NOW)
      db.commit()

      provenance = json.loads(db.get(models.Item, "ITM-0007").provenance)

      assert provenance["model"] == AGENT_AUTHOR
      assert provenance["prompt_template_version"] is None
      assert provenance["generation_job_id"] is None
