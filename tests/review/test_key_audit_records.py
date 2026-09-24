"""The committed gate 29 records, docs/operator/key-audit-p1/ over the P1 bank and
docs/operator/key-audit-p2/ over the stage 1 unit banks: gate 29 says CI checks that all 100
verdicts exist and that the rate is computed from them. Each record must also stay tied to the
banks it audited, and the rate written in its README must be the one the verdicts give."""
import json
import re
from pathlib import Path

import pytest

from app.items import ingest
from app.review.audit import EVAL_29_SAMPLE_SIZE
from app.review.verdicts import audit_completeness

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = REPOSITORY_ROOT / "content"
AUDITED_BANKS = {
   "key-audit-p1": [CONTENT_DIR / "items_p1_agent"],
   "key-audit-p2": sorted(CONTENT_DIR.glob("items_unit*_agent")),
}


def audited_record(item_id, banks):
   paths = [bank / f"{item_id}.json" for bank in banks if (bank / f"{item_id}.json").is_file()]

   assert len(paths) == 1, f"{item_id} is not in exactly one audited bank: {paths}"

   return json.loads(paths[0].read_text())


@pytest.mark.parametrize("record_name", sorted(AUDITED_BANKS))
def test_the_audit_record_is_complete_and_publishes_the_rate_its_verdicts_give(record_name):
   record_dir = REPOSITORY_ROOT / "docs" / "operator" / record_name
   sample = json.loads((record_dir / "sample.json").read_text())
   verdicts = json.loads((record_dir / "verdicts.json").read_text())
   completeness = audit_completeness(verdicts, sample)
   published = re.search(r"Key error rate: (\d+)/(\d+)", (record_dir / "README.md").read_text())

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
      record = audited_record(item_id, AUDITED_BANKS[record_name])

      assert ingest.is_operator_authored(record), item_id
