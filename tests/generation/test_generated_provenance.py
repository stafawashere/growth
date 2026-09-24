"""A generated item's provenance (04, "Provenance logging") survives ingest whole, names the
template and seed as its generation job, and counts as the operator's only once it is signed off,
which is what the key-audit draw reads (tools/draw_key_audit_sample.py --generated)."""
from app.generation.instantiate import instantiate
from app.generation.template import template_module
from app.items import ingest


def generated_record():
   return instantiate(template_module("BC-QA-06004"), 0, "BC-QA-06004:provenance-test:0", generated_at="2026-09-24T00:00:00Z")


def test_an_unsigned_generated_item_is_the_generators():
   provenance = ingest.provenance_for(generated_record())

   assert provenance["model"] == template_module("BC-QA-06004").AUTHORED_BY
   assert provenance["template_id"] == "TPL-BC-QA-06004-v1"
   assert provenance["generation_job_id"] == "TPL-BC-QA-06004-v1:BC-QA-06004:provenance-test:0"


def test_a_signed_off_generated_item_counts_as_the_operators_and_keeps_its_author():
   record = generated_record()
   record["signed_off_by"] = "claude-opus-5-5 on the operator's delegation of 2026-09-24"
   provenance = ingest.provenance_for(record)

   assert provenance["model"] == ingest.OPERATOR_MODEL
   assert provenance["generated_by"] == template_module("BC-QA-06004").AUTHORED_BY
   assert provenance["parameter_seed"] == "BC-QA-06004:provenance-test:0"
