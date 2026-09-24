"""Ingestion for the operator's hand-authored P1 items.

Scope item 7 of docs/plan/11-phased-delivery.md gives P1 the SymPy equivalence checker, the
numeric check and the distractor checks but no generator, no independent re-solve and no
generated-item queue, so what the operator hands this module is a finished record in the output
schema of docs/plan/04-item-generation.md. The checks here are the ones that already exist in
app/items/verify.py; this module runs them, writes one item_verifications row per check and sets
the items row status, verified only when every check passes.

An indeterminate symbolic comparison does not pass an item. It routes to review_queue, which is
the rule stated under item_verifications in docs/plan/06-architecture.md. The routed row carries
kind item_verification_disagreement, which is what 06 reserves for a check that did not settle;
06 also calls item_audit the only kind P1 writes, and 11 P1 scope 14 says item_audit holds the
operator's hand-audit verdicts on published items. Those two sentences cannot both hold of a
routed row, and the verdict reading wins, because app/review/audit.py computes the published key
error rate of gate 29 over item_audit rows and an ingestion artefact must not move that number.
"""
import json
import uuid

from app.db import models
from app.items.mathjson import to_sympy
from app.items.verify import (
   RULE_6,
   RULE_7,
   UNSETTLED_VIOLATION,
   distractor_checks,
   error_path_findings,
   equivalence,
   numeric_check,
)

REVIEW_KIND = "item_verification_disagreement"

CHECK_TYPES = ("sympy_equivalence", "numeric_probe", "distractor_distinct")
STATEMENT_CHECK_TYPES = ("statement_key", "distractor_distinct")

PASS = "pass"
FAIL = "fail"
INDETERMINATE = "indeterminate"

OPERATOR_MODEL = "operator"


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def load_records(directory):
   paths = sorted(path for path in directory.iterdir() if path.suffix == ".json")

   return [json.loads(path.read_text()) for path in paths]


def key_expression(record):
   return to_sympy(record["answer_key"]["mathjson"])


def solution_expression(record):
   steps = record["worked_solution"]
   has_steps = len(steps) > 0

   if not has_steps:
      raise ValueError(f"item {record.get('id')} has no worked solution to check the key against")

   valued_steps = [step for step in steps if "mathjson" in step]
   has_valued_step = len(valued_steps) > 0

   if not has_valued_step:
      raise ValueError(f"item {record.get('id')} has no worked-solution step carrying a value")

   return to_sympy(valued_steps[-1]["mathjson"])


def key_options(record):
   """04's Output schema makes is_key required on every option, so the key is read from it and
   never from a null error path, which a mis-authored distractor also has.
   """
   options = record.get("options") or []

   return [option for option in options if option.get("is_key") is True]


def distractor_options(record):
   options = record.get("options") or []

   return [option for option in options if option.get("is_key") is not True]


def option_set_violations(record):
   options = record.get("options") or []
   has_options = len(options) > 0

   if not has_options:
      return []

   keys = key_options(record)
   key_count_is_wrong = len(keys) != 1
   violations = []

   if key_count_is_wrong:
      violations.append({"rule": "exactly_one_key", "keys": len(keys)})

   for option in distractor_options(record):
      carries_no_path = option.get("error_path") is None

      if carries_no_path:
         violations.append({"rule": "distractor_without_error_path", "option": option.get("id")})

   return violations


def sympy_equivalence_check(record):
   result = equivalence(key_expression(record), solution_expression(record))

   if result == "equivalent":
      return PASS, {"comparison": result}

   if result == "unsettled":
      return INDETERMINATE, {"comparison": result}

   return FAIL, {"comparison": result}


def numeric_probe_check(record):
   result = numeric_check(key_expression(record), solution_expression(record))

   if result is True:
      return PASS, {"agrees": True}

   if result is None:
      return INDETERMINATE, {"agrees": None}

   return FAIL, {"agrees": False}


def distractor_distinct_check(record, active_error_ids):
   stated_key = key_options(record)
   has_stated_key = len(stated_key) == 1
   key_source = stated_key[0]["value"] if has_stated_key else record["answer_key"]["mathjson"]

   distractors = distractor_options(record)
   distractor_expressions = [to_sympy(option["value"]) for option in distractors]
   error_paths = [option.get("error_path") for option in distractors]

   violations = option_set_violations(record) + distractor_checks(
      to_sympy(key_source), distractor_expressions, error_paths, active_error_ids
   )
   detail = {"distractors": len(distractors), "violations": violations}

   settled_violations = [name for name in violations if name != UNSETTLED_VIOLATION]
   did_not_settle = UNSETTLED_VIOLATION in violations
   has_settled_violations = len(settled_violations) > 0

   if has_settled_violations:
      return FAIL, detail

   if did_not_settle:
      return INDETERMINATE, detail

   return PASS, detail


def is_statement_record(record):
   """04's key form "statement": a verdict, classification or interpretation chosen among
   labelled options, which no MathJSON value holds."""
   return record.get("answer_key", {}).get("form") == "statement"


def statement_key_check(record):
   key_label = record["answer_key"].get("label")
   keys = key_options(record)
   has_one_key = len(keys) == 1
   names_the_key = has_one_key and bool(key_label) and keys[0].get("label") == key_label

   if names_the_key:
      return PASS, {"label_matches": True}

   return FAIL, {"label_matches": False, "keys": len(keys)}


def statement_distractor_check(record, active_error_ids):
   options = record.get("options") or []
   labels = [(option.get("label") or "").strip() for option in options]
   blank_labels = [label for label in labels if not label]
   repeated_labels = len(set(labels)) != len(labels)
   distractors = distractor_options(record)
   error_paths = [option.get("error_path") for option in distractors]
   violations = option_set_violations(record)

   if blank_labels:
      violations.append({"rule": "option_without_label"})

   if repeated_labels:
      violations.append(RULE_6)

   violations.extend(RULE_7 for _ in error_path_findings(error_paths, active_error_ids))
   detail = {"distractors": len(distractors), "violations": violations}

   if violations:
      return FAIL, detail

   return PASS, detail


def run_statement_checks(record, active_error_ids):
   key_outcome, key_detail = statement_key_check(record)
   distractor_outcome, distractor_detail = statement_distractor_check(record, active_error_ids)

   return [
      {"check_type": "statement_key", "outcome": key_outcome, "detail": key_detail},
      {
         "check_type": "distractor_distinct",
         "outcome": distractor_outcome,
         "detail": distractor_detail,
      },
   ]


def run_checks(record, active_error_ids):
   if is_statement_record(record):
      return run_statement_checks(record, active_error_ids)

   symbolic_outcome, symbolic_detail = sympy_equivalence_check(record)
   numeric_outcome, numeric_detail = numeric_probe_check(record)
   distractor_outcome, distractor_detail = distractor_distinct_check(record, active_error_ids)

   return [
      {"check_type": "sympy_equivalence", "outcome": symbolic_outcome, "detail": symbolic_detail},
      {"check_type": "numeric_probe", "outcome": numeric_outcome, "detail": numeric_detail},
      {
         "check_type": "distractor_distinct",
         "outcome": distractor_outcome,
         "detail": distractor_detail,
      },
   ]


def status_for(results):
   """06's items.status vocabulary: a failed check rejects the item and keeps it with its
   provenance, while an unsettled check leaves it a draft for the operator to look at.
   """
   any_check_failed = any(result["outcome"] == FAIL for result in results)

   if any_check_failed:
      return "rejected"

   every_check_passed = all(result["outcome"] == PASS for result in results)

   if every_check_passed:
      return "verified"

   return "draft"


def needs_review(results):
   return any(result["outcome"] == INDETERMINATE for result in results)


def provenance_model(record):
   """Scope item 7 and R30 give a hand-authored item the model string operator. The operator's
   ruling of 2026-09-23 lets agent drafts be served before the operator reviews them, and such a
   record names its author in authored_by, which becomes the model so that nothing counting
   operator items (exit criterion 7, gates 17, 29 and 30) can count it. A record with no
   authored_by is the operator's own.
   """
   generated_by = (record.get("provenance") or {}).get("model")
   is_generated = generated_by is not None
   was_signed_off = record.get("signed_off_by") is not None

   if is_generated and not was_signed_off:
      return generated_by

   if is_generated:
      return OPERATOR_MODEL

   authored_by = record.get("authored_by")
   names_no_author = authored_by is None

   if names_no_author:
      return OPERATOR_MODEL

   return authored_by


def is_operator_authored(record):
   return provenance_model(record) == OPERATOR_MODEL


def provenance_for(record):
   """Scope item 7 and R30: the two generation keys are null on a hand-authored or agent-drafted
   item. A generated item carries its own provenance block (04, "Provenance logging"), which is
   kept whole, with the template and seed as the generation job."""
   generated = record.get("provenance")
   provenance = {
      "model": provenance_model(record),
      "prompt_template_version": None,
      "generation_job_id": None,
      "authored_on": record.get("authored_on"),
      "archetype_id": record["archetype_id"],
      "variant_id": record.get("variant_id"),
   }

   if generated is None:
      return provenance

   provenance.update(generated)
   provenance["generated_by"] = generated.get("model")
   provenance["model"] = provenance_model(record)
   provenance["prompt_template_version"] = generated.get("prompt_version")
   provenance["generation_job_id"] = f"{generated.get('template_id')}:{generated.get('parameter_seed')}"
   provenance["authored_on"] = (generated.get("generated_at") or "")[:10] or None

   return provenance


def item_row(record, item_id, snapshot_id, status, now):
   return models.Item(
      id=item_id,
      archetype_id=record["archetype_id"],
      variant_id=record.get("variant_id"),
      snapshot_id=snapshot_id,
      parameter_draw=json.dumps(record.get("parameter_draw", {})),
      stem=record["stem"]["text"],
      figure_spec=json.dumps(record["figure"]) if record.get("figure") else None,
      options=record.get("options"),
      answer_key=json.dumps(record["answer_key"]),
      worked_solution=json.dumps(record["worked_solution"]),
      calculator_status=record["calculator_status"],
      representation=record["representation"],
      difficulty_settings=json.dumps(record.get("difficulty_settings", [])),
      skills=json.dumps(record.get("skills", [])),
      provenance=json.dumps(provenance_for(record)),
      status=status,
      dedupe_minhash=json.dumps([]),
      created_at=now,
      updated_at=now,
   )


def write_verification_rows(db, item_id, results, now):
   for result in results:
      db.add(models.ItemVerification(
         id=new_id("IVR"),
         item_id=item_id,
         check_type=result["check_type"],
         outcome=result["outcome"],
         detail=json.dumps(result["detail"]),
         model_id=None,
         created_at=now,
         updated_at=now,
      ))


def open_review_row(db, item_id, now):
   row = models.ReviewQueue(
      id=new_id("RVQ"),
      kind=REVIEW_KIND,
      ref_id=item_id,
      opened_at=now,
      resolved_at=None,
      resolution=None,
      visible_to_student=0,
      created_at=now,
      updated_at=now,
   )
   db.add(row)

   return row


def ingest_item(db, record, active_error_ids, snapshot_id, now):
   item_id = record.get("id") or new_id("ITM")
   results = run_checks(record, active_error_ids)
   status = status_for(results)

   db.add(item_row(record, item_id, snapshot_id, status, now))
   write_verification_rows(db, item_id, results, now)

   routes_to_review = needs_review(results)

   if routes_to_review:
      open_review_row(db, item_id, now)

   db.flush()

   return {
      "item_id": item_id,
      "status": status,
      "checks": results,
      "routed_to_review": routes_to_review,
   }


def ingest_directory(db, directory, active_error_ids, snapshot_id, now):
   records = load_records(directory)

   return [
      ingest_item(db, record, active_error_ids, snapshot_id, now) for record in records
   ]


def ingest_new_records(db, directory, active_error_ids, snapshot_id, now):
   """ingest_directory for a bank directory read on every start: a record whose id is already in
   items is left as it is, so a restart over the same database adds only what is new. Every record
   must carry its id, because one without would be minted a fresh id and ingested again each time.
   """
   records = load_records(directory)
   unnamed = [record for record in records if not record.get("id")]
   has_unnamed_records = len(unnamed) > 0

   if has_unnamed_records:
      raise ValueError(f"{len(unnamed)} records in {directory} carry no id")

   record_ids = [record["id"] for record in records]
   stored_ids = {
      item_id
      for (item_id,) in db.query(models.Item.id).filter(models.Item.id.in_(record_ids))
   }

   return [
      ingest_item(db, record, active_error_ids, snapshot_id, now)
      for record in records
      if record["id"] not in stored_ids
   ]
