"""Operator command-line check over a directory of hand-authored item records: gate 17
(test_item_verification_tools) and gate 30 (eval_p1_distractor_paths) in
docs/plan/11-phased-delivery.md, P1 exit criterion 7.

Runs the same checks app/items/ingest.py runs on the way into the bank, plus gate 30's
distractor-path property, without touching the database or writing anywhere. The operator
runs this over their own files before handing them over, so a malformed record shows up
here instead of turning a gate red later.

Gate 30's error-path rule is applied per record: a distractor's error_path must be a BC-ERR id
held by one of the skills of that record's own archetype, not by any skill in the bank. A record
naming an archetype the snapshot does not hold is a violation.

A record whose provenance model is not operator (an agent draft, app/items/ingest.py
provenance_model) is checked like any other and counted under items per archetype, but only
operator-authored records are counted toward exit criterion 7, per the operator's ruling of
2026-09-23 in BUILD-LEDGER.md.

The question standards of app/items/standards.py run on every record. The lints in its
DEFAULT_LINTS count as violations on every run; --standards makes every lint count. The report
prints how many records fail each lint either way, and two statistics over the whole directory
(key letter balance, statement keys that are the longest option) that never change the exit
status. --json writes the per-record findings to a file for a fix pass to read.

Usage: python3 tools/check_items.py [--standards] [--json <path>] <directory>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.content.loader import LoaderError, load_snapshot
from app.items.distractor_paths import distractor_path_violations, error_ids_for_skills
from app.items.ingest import is_operator_authored, load_records, run_checks
from app.items.standards import (
   LINTS,
   MODE_DEFAULT,
   MODE_STANDARDS,
   all_lint_findings,
   command_verb_source,
   key_letter_distribution,
   lints_for_mode,
   statement_longest_key_share,
   unconvertible_value_options,
)
from tools.build_p1_fixture import P1_ARCHETYPES

DATA_ROOT = Path(__file__).resolve().parents[1] / "data"

USAGE = "usage: python3 tools/check_items.py [--standards] [--json <path>] <directory>"


def archetype_error_ids(snapshot, archetype_id):
   archetype = snapshot.archetypes.get(archetype_id)
   is_known_archetype = archetype is not None

   if not is_known_archetype:
      return None

   return error_ids_for_skills(snapshot, archetype["skills"])


def record_violations(record, snapshot):
   active_error_ids = archetype_error_ids(snapshot, record.get("archetype_id"))
   names_unknown_archetype = active_error_ids is None

   if names_unknown_archetype:
      return [f"archetype {record.get('archetype_id')!r} is not an active archetype in the snapshot"]

   violations = []

   for result in run_checks(record, active_error_ids):
      check_passed = result["outcome"] == "pass"

      if not check_passed:
         violations.append(f"{result['check_type']} {result['outcome']}: {result['detail']}")

   violations.extend(distractor_path_violations(record, active_error_ids))

   return violations


def lint_violation_lines(lint_findings, enforced_lints):
   lines = []

   for name in enforced_lints:
      for finding in lint_findings[name]:
         lines.append(f"standard {name}: {finding}")

   return lines


def check_directory(directory, snapshot, mode=MODE_DEFAULT):
   records = load_records(directory)
   enforced_lints = lints_for_mode(mode)
   lint_failure_counts = {name: 0 for name in LINTS}
   command_verb_sources = {"field": 0, "text": 0, "none": 0}
   skipped_value_options = 0
   findings_by_id = {}
   archetype_counts = {archetype_id: 0 for archetype_id in P1_ARCHETYPES}
   operator_archetype_counts = {archetype_id: 0 for archetype_id in P1_ARCHETYPES}
   clean_ids = []
   violations_by_id = {}

   for record in records:
      record_id = record.get("id", "<no id>")
      archetype_id = record.get("archetype_id")
      is_a_p1_archetype = archetype_id in operator_archetype_counts
      archetype_counts[archetype_id] = archetype_counts.get(archetype_id, 0) + 1

      counts_toward_exit_criterion_7 = is_a_p1_archetype and is_operator_authored(record)

      if counts_toward_exit_criterion_7:
         operator_archetype_counts[archetype_id] += 1

      lint_findings = all_lint_findings(record)

      for name, findings in lint_findings.items():
         if findings:
            lint_failure_counts[name] += 1

      verb_source = command_verb_source(record) or "none"
      command_verb_sources[verb_source.split(":")[0]] += 1
      skipped_options = unconvertible_value_options(record)
      skipped_value_options += len(skipped_options)

      violations = record_violations(record, snapshot) + lint_violation_lines(lint_findings, enforced_lints)
      record_is_clean = len(violations) == 0
      has_lint_findings = any(lint_findings.values())
      skipped_any_option = len(skipped_options) > 0
      has_any_finding = not record_is_clean or has_lint_findings or skipped_any_option

      if has_any_finding:
         findings_by_id[record_id] = {
            "violations": violations,
            "lints": {name: found for name, found in lint_findings.items() if found},
            "value_options_skipped": skipped_options,
         }

      if record_is_clean:
         clean_ids.append(record_id)
      else:
         violations_by_id[record_id] = violations

   return {
      "mode": mode,
      "enforced_lints": list(enforced_lints),
      "record_count": len(records),
      "clean_ids": clean_ids,
      "violations_by_id": violations_by_id,
      "findings_by_id": findings_by_id,
      "lint_failure_counts": lint_failure_counts,
      "command_verb_sources": command_verb_sources,
      "skipped_value_options": skipped_value_options,
      "key_letters": key_letter_distribution(records),
      "statement_longest_key": statement_longest_key_share(records),
      "archetype_counts": archetype_counts,
      "operator_archetype_counts": operator_archetype_counts,
   }


def print_standards_report(report):
   enforced = set(report["enforced_lints"])

   print(f"question standards, mode {report['mode']}, records failing each lint:")

   for name, count in report["lint_failure_counts"].items():
      status = "enforced" if name in enforced else "reported only, --standards enforces it"
      print(f"  {name}: {count} ({status})")

   sources = report["command_verb_sources"]
   print(
      f"  command verb from the stem field {sources['field']}, "
      f"from the stem text {sources['text']}, none {sources['none']}"
   )
   print(f"  value options value_option_type skipped as unconvertible: {report['skipped_value_options']}")
   print()

   letters = report["key_letters"]
   letter_counts = ", ".join(f"{letter} {count}" for letter, count in letters["counts"].items())
   chi_square = "n/a" if letters["chi_square"] is None else f"{letters['chi_square']:.2f}"
   letter_flag = "FLAGGED" if letters["flagged"] else "not flagged"
   print(
      f"key letters over {letters['total']} items: {letter_counts}; "
      f"chi-square {chi_square} on {letters['degrees_of_freedom']} df; "
      f"top share {letters['top_share']:.3f}; {letter_flag} (flagged when one letter holds over 40 percent of at least 40 keys)"
   )

   longest = report["statement_longest_key"]
   longest_flag = "FLAGGED" if longest["flagged"] else "not flagged"
   print(
      f"statement key is the longest label: {longest['key_longest']} of {longest['statement_items']} "
      f"({longest['share']:.3f}); {longest_flag} (flagged over 40 percent of at least 40 statement items)"
   )


def write_json_report(report, path):
   payload = {
      "mode": report["mode"],
      "enforced_lints": report["enforced_lints"],
      "record_count": report["record_count"],
      "clean_count": len(report["clean_ids"]),
      "lint_failure_counts": report["lint_failure_counts"],
      "key_letters": report["key_letters"],
      "statement_longest_key": report["statement_longest_key"],
      "records": report["findings_by_id"],
   }
   path.parent.mkdir(parents=True, exist_ok=True)
   path.write_text(json.dumps(payload, indent=3) + "\n")


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
   print_standards_report(report)
   print()
   print("items per archetype:")

   for archetype_id in sorted(report["archetype_counts"]):
      print(f"  {archetype_id}: {report['archetype_counts'][archetype_id]}")

   print()
   print("operator-authored items per archetype (exit criterion 7, gates 17 and 30 count only these):")

   for archetype_id in P1_ARCHETYPES:
      print(f"  {archetype_id}: {report['operator_archetype_counts'][archetype_id]}")


def parse_arguments(arguments):
   mode = MODE_DEFAULT
   json_path = None
   positionals = []
   remaining = list(arguments)

   while remaining:
      argument = remaining.pop(0)
      is_standards_flag = argument == "--standards"
      is_json_flag = argument == "--json"
      json_flag_has_path = is_json_flag and len(remaining) > 0

      if is_standards_flag:
         mode = MODE_STANDARDS
      elif json_flag_has_path:
         json_path = Path(remaining.pop(0))
      elif argument.startswith("--"):
         return None
      else:
         positionals.append(argument)

   takes_one_directory_argument = len(positionals) == 1

   if not takes_one_directory_argument:
      return None

   return Path(positionals[0]), mode, json_path


def main(argv):
   parsed = parse_arguments(argv[1:])

   if parsed is None:
      print(USAGE, file=sys.stderr)

      return 1

   directory, mode, json_path = parsed

   try:
      snapshot = load_snapshot(DATA_ROOT)
   except LoaderError as error:
      print(f"refusing: the content snapshot did not load, so gate 30 cannot run: {error}", file=sys.stderr)

      return 1

   report = check_directory(directory, snapshot, mode)

   print_report(report)

   if json_path is not None:
      write_json_report(report, json_path)
      print(f"\nwrote per-record findings to {json_path}")

   all_records_are_clean = len(report["violations_by_id"]) == 0

   return 0 if all_records_are_clean else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
