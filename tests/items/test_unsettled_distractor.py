"""An unsettled distractor comparison must not verify an item.

app/items/ingest.py's own docstring says an indeterminate symbolic comparison does not pass an
item and routes to review_queue, and sympy_equivalence_check and numeric_probe_check both honour
it. distractor_distinct_check did not: _equals_key collapsed unsettled into not-equal, so a
distractor the checker could not compare against the key read as distinct from it and the item
reached status verified. Rejection rule 5 in 04 is that no distractor equals the key, and a
comparison that did not settle has not established that.
"""
import json
from pathlib import Path

import sympy

from app.items import ingest, verify

FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "items_p1"

UNSETTLED_VALUE = ["Divide", 1, 0]


def clean_record():
   path = sorted(FIXTURE_DIR.glob("*.json"))[0]

   return json.loads(path.read_text())


def option_by_id(record, option_id):
   for option in record["options"]:
      is_wanted = option.get("id") == option_id

      if is_wanted:
         return option

   raise AssertionError(f"no option {option_id} on {record.get('id')}")


def active_error_ids_for(record):
   return {option["error_path"] for option in ingest.distractor_options(record)}


def first_distractor_id(record):
   return ingest.distractor_options(record)[0]["id"]


def test_an_unsettled_pair_is_reported_by_the_distractor_checks():
   key = sympy.Symbol("x")
   unsettled = verify.to_sympy(UNSETTLED_VALUE) if hasattr(verify, "to_sympy") else None

   from app.items.mathjson import to_sympy

   candidate = to_sympy(UNSETTLED_VALUE)

   assert unsettled is None or unsettled == candidate
   assert verify.equivalence(key, candidate) == "unsettled"

   violations = verify.distractor_checks(key, [candidate], ["BC-ERR-01001"], {"BC-ERR-01001"})

   assert verify.UNSETTLED_VIOLATION in violations


def test_an_unsettled_distractor_leaves_the_item_a_draft_rather_than_verified():
   record = clean_record()
   option_by_id(record, first_distractor_id(record))["value"] = UNSETTLED_VALUE

   results = ingest.run_checks(record, active_error_ids_for(record))

   by_type = {result["check_type"]: result["outcome"] for result in results}

   assert by_type["distractor_distinct"] == ingest.INDETERMINATE
   assert ingest.status_for(results) == "draft"


def test_an_unsettled_distractor_routes_the_item_to_review():
   record = clean_record()
   option_by_id(record, first_distractor_id(record))["value"] = UNSETTLED_VALUE

   results = ingest.run_checks(record, active_error_ids_for(record))

   assert ingest.needs_review(results) is True


def test_a_distractor_that_really_equals_the_key_still_fails_rather_than_routing():
   record = clean_record()
   key_value = ingest.key_options(record)[0]["value"]
   option_by_id(record, first_distractor_id(record))["value"] = key_value

   results = ingest.run_checks(record, active_error_ids_for(record))

   by_type = {result["check_type"]: result["outcome"] for result in results}

   assert by_type["distractor_distinct"] == ingest.FAIL
   assert ingest.status_for(results) == "rejected"


def test_the_clean_fixture_record_still_verifies_its_distractors():
   record = clean_record()

   results = ingest.run_checks(record, active_error_ids_for(record))

   by_type = {result["check_type"]: result["outcome"] for result in results}

   assert by_type["distractor_distinct"] == ingest.PASS
