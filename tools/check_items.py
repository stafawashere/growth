"""Operator command-line check over a directory of hand-authored item records: gate 17
(test_item_verification_tools) and gate 30 (eval_p1_distractor_paths) in
docs/plan/11-phased-delivery.md, P1 exit criterion 7.

Runs the same checks app/items/ingest.py runs on the way into the bank, plus gate 30's
distractor-path property, without touching the database or writing anywhere. The operator
runs this over their own files before handing them over, so a malformed record shows up
here instead of turning a gate red later.

Usage: python3 tools/check_items.py <directory>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.content.loader import LoaderError, load_snapshot
from app.items.distractor_paths import distractor_path_violations, error_ids_for_skills
from app.items.ingest import load_records, run_checks
from tools.build_p1_fixture import P1_ARCHETYPES

DATA_ROOT = Path(__file__).resolve().parents[1] / "data"


def p1_skill_ids(snapshot):
   skill_ids = set()

   for archetype_id in P1_ARCHETYPES:
      skill_ids.update(snapshot.archetypes[archetype_id]["skills"])

   return frozenset(skill_ids)


def record_violations(record, active_error_ids):
   violations = []

   for result in run_checks(record, active_error_ids):
      check_passed = result["outcome"] == "pass"

      if not check_passed:
         violations.append(f"{result['check_type']} {result['outcome']}: {result['detail']}")

   violations.extend(distractor_path_violations(record, active_error_ids))

   return violations


def check_directory(directory, active_error_ids):
   records = load_records(directory)
   archetype_counts = {archetype_id: 0 for archetype_id in P1_ARCHETYPES}
   clean_ids = []
   violations_by_id = {}

   for record in records:
      record_id = record.get("id", "<no id>")
      archetype_id = record.get("archetype_id")
      is_a_p1_archetype = archetype_id in archetype_counts

      if is_a_p1_archetype:
         archetype_counts[archetype_id] += 1

      violations = record_violations(record, active_error_ids)
      record_is_clean = len(violations) == 0

      if record_is_clean:
         clean_ids.append(record_id)
      else:
         violations_by_id[record_id] = violations

   return {
      "record_count": len(records),
      "clean_ids": clean_ids,
      "violations_by_id": violations_by_id,
      "archetype_counts": archetype_counts,
   }


def print_report(report):
   for record_id, violations in report["violations_by_id"].items():
      print(f"{record_id}:")

      for violation in violations:
         print(f"  {violation}")

   print()
   print(f"records read: {report['record_count']}")
   print(f"clean: {len(report['clean_ids'])}")
   print(f"with violations: {len(report['violations_by_id'])}")
   print()
   print("items per archetype:")

   for archetype_id in P1_ARCHETYPES:
      print(f"  {archetype_id}: {report['archetype_counts'][archetype_id]}")


def main(argv):
   takes_one_directory_argument = len(argv) == 2

   if not takes_one_directory_argument:
      print("usage: python3 tools/check_items.py <directory>", file=sys.stderr)

      return 1

   directory = Path(argv[1])

   try:
      snapshot = load_snapshot(DATA_ROOT)
   except LoaderError as error:
      print(f"refusing: the content snapshot did not load, so gate 30 cannot run: {error}", file=sys.stderr)

      return 1

   active_error_ids = error_ids_for_skills(snapshot, p1_skill_ids(snapshot))
   report = check_directory(directory, active_error_ids)

   print_report(report)

   all_records_are_clean = len(report["violations_by_id"]) == 0

   return 0 if all_records_are_clean else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
