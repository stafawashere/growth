"""The gate table of docs/plan/11-phased-delivery.md, as it stands in tests/.

Every phase in 11 carries a "Tests that gate the phase" section naming the gates in backticks,
and P1 numbers them 1 to 31 while the later phases run them together in prose. This module reads
that section for every phase, finds each gate's test function in tests/, and reports whether it
is present and whether it passed on the last run of the suite. A session starts from this table
instead of grepping the plan by hand.

Outcomes come from a JUnit XML report written by the suite itself, so a gate reads as passing
only when a run of pytest in this session said so. A gate whose test function exists but which no
run has covered reads as unknown rather than as passing.
"""
import argparse
import re
import subprocess
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

PLAN_PATH = REPOSITORY_ROOT / "docs" / "plan" / "11-phased-delivery.md"

TESTS_ROOT = REPOSITORY_ROOT / "tests"

GATE_SECTION_HEADING = "### Tests that gate the phase"

PHASE_HEADING = re.compile(r"^## (P\d)\s")

GATE_NAME = re.compile(r"`((?:test|eval)_[A-Za-z0-9_]+)`")

NUMBERED_ITEM = re.compile(r"^(\d+)\.\s")

DEFINITION = re.compile(r"^\s*def\s+((?:test|eval)_[A-Za-z0-9_]+)\s*\(", re.MULTILINE)

PRESENT = "present"
MISSING = "missing"

PASSING = "passing"
FAILING = "failing"
UNKNOWN = "unknown"


class Gate:
   def __init__(self, phase, number, name):
      self.phase = phase
      self.number = number
      self.name = name


def read_gates(plan_path=PLAN_PATH):
   """Every gate 11 names, in plan order, carrying the phase and the plan's own item number where
   the phase numbers its list."""
   phase = None
   inside_section = False
   running_number = 0
   gates = []

   for line in plan_path.read_text().splitlines():
      phase_match = PHASE_HEADING.match(line)

      if phase_match:
         phase = phase_match.group(1)
         inside_section = False
         running_number = 0

      is_heading = line.startswith("### ")

      if is_heading:
         inside_section = line.strip() == GATE_SECTION_HEADING
         continue

      collecting = inside_section and phase is not None

      if not collecting:
         continue

      names = GATE_NAME.findall(line)

      if not names:
         continue

      numbered = NUMBERED_ITEM.match(line)

      for offset, name in enumerate(names):
         is_first_on_a_numbered_line = numbered is not None and offset == 0

         if is_first_on_a_numbered_line:
            running_number = int(numbered.group(1))
         else:
            running_number = running_number + 1

         gates.append(Gate(phase, running_number, name))

   return gates


def defined_test_names(tests_root=TESTS_ROOT):
   """Every test or eval function defined anywhere under tests/, mapped to the files defining it."""
   found = {}

   for path in sorted(tests_root.rglob("*.py")):
      for name in DEFINITION.findall(path.read_text()):
         found.setdefault(name, []).append(path.relative_to(REPOSITORY_ROOT))

   return found


def suite_interpreter():
   """The repository's own interpreter, because this tool is run as `python3 tools/gate_status.py`
   and the system interpreter has no pytest, which would make the run fail and every gate read
   unknown.
   """
   candidate = REPOSITORY_ROOT / ".venv" / "bin" / "python"

   if candidate.exists():
      return str(candidate)

   return sys.executable


def run_suite(report_path):
   """Runs the suite once and writes the JUnit report the outcomes are read from."""
   command = [
      suite_interpreter(),
      "-m",
      "pytest",
      "-p",
      "no:warnings",
      "-o",
      "addopts=",
      "--ignore-glob=* 2.py",
      f"--junitxml={report_path}",
   ]

   return subprocess.run(command, cwd=REPOSITORY_ROOT, capture_output=True, text=True)


def read_outcomes(report_path):
   """Maps a test function name to passing or failing, from a JUnit report. A name that several
   cases share reads as failing when any of them failed, because a gate is not met in part."""
   report = Path(report_path)
   has_report = report.exists()

   if not has_report:
      return {}

   outcomes = {}

   for case in ElementTree.parse(report).getroot().iter("testcase"):
      name = case.get("name") or ""
      bare_name = name.split("[")[0]

      failed_children = [child for child in case if child.tag in ("failure", "error")]
      case_failed = len(failed_children) > 0

      already_failing = outcomes.get(bare_name) == FAILING

      if case_failed or already_failing:
         outcomes[bare_name] = FAILING
      else:
         outcomes[bare_name] = PASSING

   return outcomes


def gate_rows(gates, defined, outcomes):
   rows = []

   for gate in gates:
      files = defined.get(gate.name, [])
      is_present = len(files) > 0

      presence = PRESENT if is_present else MISSING
      outcome = outcomes.get(gate.name, UNKNOWN)

      reported_outcome = outcome if is_present else UNKNOWN

      rows.append(
         {
            "phase": gate.phase,
            "number": gate.number,
            "name": gate.name,
            "presence": presence,
            "outcome": reported_outcome,
            "files": [str(path) for path in files],
         }
      )

   return rows


def format_table(rows):
   header = ("phase", "gate", "test name", "presence", "outcome")
   widths = [len(column) for column in header]

   printable = [
      (row["phase"], str(row["number"]), row["name"], row["presence"], row["outcome"])
      for row in rows
   ]

   for line in printable:
      for index, cell in enumerate(line):
         widths[index] = max(widths[index], len(cell))

   def render(cells):
      return "  ".join(cell.ljust(widths[index]) for index, cell in enumerate(cells)).rstrip()

   lines = [render(header), render(tuple("-" * width for width in widths))]
   lines.extend(render(line) for line in printable)

   return "\n".join(lines)


def summarise(rows):
   phases = {}

   for row in rows:
      bucket = phases.setdefault(row["phase"], {PRESENT: 0, MISSING: 0, PASSING: 0})

      bucket[row["presence"]] = bucket[row["presence"]] + 1

      is_passing = row["outcome"] == PASSING

      if is_passing:
         bucket[PASSING] = bucket[PASSING] + 1

   lines = []

   for phase in sorted(phases):
      bucket = phases[phase]
      total = bucket[PRESENT] + bucket[MISSING]
      lines.append(
         f"{phase}: {total} gates, {bucket[PRESENT]} present, "
         f"{bucket[MISSING]} missing, {bucket[PASSING]} passing"
      )

   return "\n".join(lines)


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("--phase", help="report one phase only, for instance P1")
   parser.add_argument(
      "--no-run",
      action="store_true",
      help="do not run the suite; read outcomes from an existing report if there is one",
   )
   parser.add_argument(
      "--report",
      default=str(REPOSITORY_ROOT / "var" / "gate_report.xml"),
      help="where the JUnit report is written and read",
   )
   arguments = parser.parse_args(argv)

   report_path = Path(arguments.report)
   report_path.parent.mkdir(parents=True, exist_ok=True)

   if not arguments.no_run:
      completed = run_suite(report_path)
      report_was_written = report_path.exists()

      if not report_was_written:
         print(
            "the suite run produced no report, so every outcome below is unknown rather than "
            f"measured; the runner exited {completed.returncode} and said:\n{completed.stderr}",
            file=sys.stderr,
         )

   gates = read_gates()
   wanted_phase = arguments.phase

   if wanted_phase:
      gates = [gate for gate in gates if gate.phase == wanted_phase]

   rows = gate_rows(gates, defined_test_names(), read_outcomes(report_path))

   print(format_table(rows))
   print()
   print(summarise(rows))

   any_gate_missing = any(row["presence"] == MISSING for row in rows)
   any_gate_failing = any(row["outcome"] == FAILING for row in rows)
   phase_is_not_met = any_gate_missing or any_gate_failing

   if phase_is_not_met:
      return 1

   return 0


if __name__ == "__main__":
   raise SystemExit(main())
