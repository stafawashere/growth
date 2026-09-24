"""The committed gate 29 record in docs/operator/key-audit-p1/: gate 29 says CI checks that all 100
verdicts exist and that the rate is computed from them. The record must also stay tied to the
bank it audited, and the rate written in its README must be the one the verdicts give."""
import json
import re
from pathlib import Path

from app.items import ingest
from app.review.audit import EVAL_29_SAMPLE_SIZE
from app.review.verdicts import audit_completeness

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
RECORD_DIR = REPOSITORY_ROOT / "docs" / "operator" / "key-audit-p1"
ITEMS_DIR = REPOSITORY_ROOT / "content" / "items_p1_agent"


def test_the_p1_audit_record_is_complete_and_publishes_the_rate_its_verdicts_give():
   sample = json.loads((RECORD_DIR / "sample.json").read_text())
   verdicts = json.loads((RECORD_DIR / "verdicts.json").read_text())
   completeness = audit_completeness(verdicts, sample)
   published = re.search(r"Key error rate: (\d+)/(\d+)", (RECORD_DIR / "README.md").read_text())

   assert len(sample) == EVAL_29_SAMPLE_SIZE
   assert len(set(sample)) == EVAL_29_SAMPLE_SIZE
   assert completeness["missing_ids"] == []
   assert completeness["out_of_sample_ids"] == []
   assert completeness["duplicate_ids"] == []
   assert completeness["key_error_rate"] is not None
   assert published is not None
   assert int(published.group(2)) == EVAL_29_SAMPLE_SIZE
   assert int(published.group(1)) / EVAL_29_SAMPLE_SIZE == completeness["key_error_rate"]

   for item_id in sample:
      record = json.loads((ITEMS_DIR / f"{item_id}.json").read_text())

      assert ingest.is_operator_authored(record), item_id
