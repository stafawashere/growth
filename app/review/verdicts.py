"""The shape of a hand-authored item_audit verdict and the two checks CI makes on a
batch of them, for gate 29 (eval_p1_key_error_rate) in docs/plan/11-phased-delivery.md.

The 100 verdicts are the operator's and do not exist yet. This module defines the
record shape they must arrive in and the completeness and rate check that CI runs
once they do. The verdict vocabulary itself is owned by app.review.audit, not here.
"""
from app.review.audit import KEY_ERROR_VERDICTS
from app.review.audit import VERDICT_AMBIGUOUS
from app.review.audit import VERDICTS


def verdict_violations(record):
   violations = []

   item_id = record.get("item_id")
   has_item_id = isinstance(item_id, str) and item_id != ""

   if not has_item_id:
      violations.append("missing or unknown item_id")

   verdict = record.get("verdict")
   is_known_verdict = verdict in VERDICTS

   if not is_known_verdict:
      violations.append(f"verdict {verdict!r} is not in the audit module's vocabulary")

   auditor = record.get("auditor")
   has_auditor = isinstance(auditor, str) and auditor != ""

   if not has_auditor:
      violations.append("missing auditor")

   audited_at = record.get("audited_at")
   has_audited_at = audited_at is not None and audited_at != ""

   if not has_audited_at:
      violations.append("missing audited_at")

   is_ambiguous = verdict == VERDICT_AMBIGUOUS
   second_answer = record.get("second_answer")
   has_second_answer = second_answer is not None and second_answer != ""
   ambiguous_without_second_answer = is_ambiguous and not has_second_answer

   if ambiguous_without_second_answer:
      violations.append("ambiguous verdict has no second answer recorded")

   return violations


def audit_completeness(records, sample_ids):
   sample_id_set = set(sample_ids)
   records_by_item_id = {}
   unidentified_records = 0

   for record in records:
      item_id = record.get("item_id")
      is_identified = isinstance(item_id, str) and item_id != ""

      if not is_identified:
         unidentified_records = unidentified_records + 1
         continue

      records_by_item_id.setdefault(item_id, []).append(record)

   out_of_sample_ids = sorted(
      item_id for item_id in records_by_item_id if item_id not in sample_id_set
   )
   duplicate_ids = sorted(
      item_id
      for item_id, matching_records in records_by_item_id.items()
      if item_id in sample_id_set and len(matching_records) > 1
   )

   single_verdict_by_item_id = {
      item_id: matching_records[0]
      for item_id, matching_records in records_by_item_id.items()
      if item_id in sample_id_set and len(matching_records) == 1
   }

   audited_ids = sorted(single_verdict_by_item_id)
   missing_ids = sorted(sample_id_set - single_verdict_by_item_id.keys())

   verdict_counts = {verdict: 0 for verdict in VERDICTS}

   for record in single_verdict_by_item_id.values():
      verdict = record.get("verdict")
      is_counted_verdict = verdict in verdict_counts

      if is_counted_verdict:
         verdict_counts[verdict] += 1

   invalid_ids = sorted(
      item_id
      for item_id, record in single_verdict_by_item_id.items()
      if len(verdict_violations(record)) > 0
   )

   sample_is_complete = len(missing_ids) == 0
   every_verdict_is_usable = len(invalid_ids) == 0
   nothing_is_unidentified = unidentified_records == 0
   sample_is_populated = len(sample_id_set) > 0

   rate_is_publishable = (
      sample_is_complete
      and every_verdict_is_usable
      and nothing_is_unidentified
      and sample_is_populated
   )

   if rate_is_publishable:
      key_errors = sum(
         count for verdict, count in verdict_counts.items() if verdict in KEY_ERROR_VERDICTS
      )
      key_error_rate = key_errors / len(sample_id_set)
   else:
      key_error_rate = None

   return {
      "audited_ids": audited_ids,
      "missing_ids": missing_ids,
      "out_of_sample_ids": out_of_sample_ids,
      "duplicate_ids": duplicate_ids,
      "invalid_ids": invalid_ids,
      "unidentified_records": unidentified_records,
      "verdict_counts": verdict_counts,
      "key_error_rate": key_error_rate,
   }
