"""Operator command-line check over a hand-audited verdict file: gate 29
(eval_p1_key_error_rate) in docs/plan/11-phased-delivery.md, P1 exit criterion 4.

Prints every malformed verdict, then exactly what gate 29 says CI checks over the audited
sample: whether every sampled id has exactly one verdict, which ids are missing, and the key
error rate. A verdict for an item outside the sample refuses the rate, and the rate is taken over
the sample, so it never exceeds 1. No threshold is invented here; P1 sets none, so the rate is reported and never
compared against anything. Read-only: it never writes to data/, research/ or the database.

Usage: python3 tools/check_audit_verdicts.py <verdicts.json> <sample.json>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.review.verdicts import audit_completeness, verdict_violations


def load_json_array(path):
   return json.loads(Path(path).read_text())


def print_malformed(records):
   malformed_count = 0

   for record in records:
      violations = verdict_violations(record)
      record_is_malformed = len(violations) > 0

      if record_is_malformed:
         malformed_count += 1
         item_id = record.get("item_id", "<no item_id>")
         print(f"{item_id}:")

         for violation in violations:
            print(f"  {violation}")

   return malformed_count


def rate_refusal_reason(completeness):
   sample_is_complete = len(completeness["missing_ids"]) == 0
   every_verdict_is_sampled = len(completeness["out_of_sample_ids"]) == 0
   rate_was_computed = completeness["key_error_rate"] is not None

   if not sample_is_complete:
      return "the sample is incomplete"

   if not every_verdict_is_sampled:
      return "a verdict names an item outside the sample"

   if not rate_was_computed:
      return "a verdict in the sample is malformed"

   return None


def print_completeness(completeness, sample_size):
   print()
   print(f"sample size: {sample_size}")
   print(f"audited: {len(completeness['audited_ids'])}")
   print(f"missing: {len(completeness['missing_ids'])}")

   for item_id in completeness["missing_ids"]:
      print(f"  missing {item_id}")

   for item_id in completeness["out_of_sample_ids"]:
      print(f"  out of sample: {item_id}")

   for item_id in completeness["duplicate_ids"]:
      print(f"  duplicate verdict: {item_id}")

   refusal_reason = rate_refusal_reason(completeness)
   rate_is_refused = refusal_reason is not None

   if rate_is_refused:
      print(f"key error rate: not published, {refusal_reason}")

      return

   print(f"key error rate: {completeness['key_error_rate']}")
   print("no pass threshold is set in P1; this is a measurement, not a gate")


def main(argv):
   takes_two_path_arguments = len(argv) == 3

   if not takes_two_path_arguments:
      print("usage: python3 tools/check_audit_verdicts.py <verdicts.json> <sample.json>", file=sys.stderr)

      return 1

   verdicts_path, sample_path = argv[1], argv[2]
   records = load_json_array(verdicts_path)
   sample_ids = load_json_array(sample_path)

   malformed_count = print_malformed(records)
   completeness = audit_completeness(records, sample_ids)

   print_completeness(completeness, len(sample_ids))

   rate_is_published = rate_refusal_reason(completeness) is None
   no_malformed_verdicts = malformed_count == 0
   check_passes = rate_is_published and no_malformed_verdicts

   return 0 if check_passes else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
