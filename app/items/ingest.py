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
from app.items.verify import distractor_checks, equivalence, numeric_check

REVIEW_KIND = "item_verification_disagreement"

CHECK_TYPES = ("sympy_equivalence", "numeric_probe", "distractor_distinct")

PASS = "pass"
FAIL = "fail"
INDETERMINATE = "indeterminate"


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

   return to_sympy(steps[-1]["mathjson"])


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
   has_violations = len(violations) > 0

   if has_violations:
      return FAIL, detail

   return PASS, detail


def run_checks(record, active_error_ids):
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


def provenance_for(record):
   """Scope item 7 and R30: model is the string operator, the other two keys are null."""
   return {
      "model": "operator",
      "prompt_template_version": None,
      "generation_job_id": None,
      "authored_on": record.get("authored_on"),
      "archetype_id": record["archetype_id"],
      "variant_id": record.get("variant_id"),
   }


def item_row(record, item_id, snapshot_id, status, now):
   return models.Item(
      id=item_id,
      archetype_id=record["archetype_id"],
      variant_id=record.get("variant_id"),
      snapshot_id=snapshot_id,
      parameter_draw=json.dumps(record.get("parameter_draw", {})),
      stem=json.dumps(record["stem"]),
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
