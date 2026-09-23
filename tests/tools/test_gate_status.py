"""The gate table must be read out of docs/plan/11-phased-delivery.md rather than typed here.

Every assertion below recomputes what it checks from the plan text or from the tests tree, so a
gate renamed in 11 or a test renamed in tests/ moves the table without anyone editing this file.
"""
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tools import gate_status

REPOSITORY_ROOT = Path(gate_status.REPOSITORY_ROOT)


@pytest.fixture(scope="module")
def gates():
   return gate_status.read_gates()


def plan_text():
   return gate_status.PLAN_PATH.read_text()


def test_every_gate_name_in_the_plan_is_in_the_table(gates):
   section_names = set()
   inside = False
   phase = None

   for line in plan_text().splitlines():
      phase_match = gate_status.PHASE_HEADING.match(line)

      if phase_match:
         phase = phase_match.group(1)
         inside = False

      if line.startswith("### "):
         inside = line.strip() == gate_status.GATE_SECTION_HEADING
         continue

      if inside and phase:
         section_names.update(gate_status.GATE_NAME.findall(line))

   assert section_names
   assert {gate.name for gate in gates} == section_names


def test_the_p1_gate_numbers_are_the_plans_own_numbering(gates):
   p1 = [gate for gate in gates if gate.phase == "P1"]
   numbers = [gate.number for gate in p1]

   assert numbers == sorted(numbers)
   assert numbers[0] == 1
   assert numbers == list(range(1, len(p1) + 1))

   for gate in p1:
      pattern = re.compile(rf"^{gate.number}\. `{re.escape(gate.name)}`", re.MULTILINE)
      assert pattern.search(plan_text()), f"gate {gate.number} is not numbered {gate.number} in 11"


def test_every_phase_named_in_the_plan_carries_gates(gates):
   headings = set(re.findall(r"^## (P\d)\s", plan_text(), re.MULTILINE))
   covered = {gate.phase for gate in gates}

   assert headings
   assert covered == headings


def test_a_gate_with_a_test_function_reads_present(gates):
   defined = gate_status.defined_test_names()
   rows = gate_status.gate_rows(gates, defined, {})

   present_rows = [row for row in rows if row["presence"] == gate_status.PRESENT]

   assert present_rows

   for row in present_rows:
      assert row["name"] in defined
      assert row["files"]


def test_a_gate_with_no_test_function_reads_missing(gates):
   defined = gate_status.defined_test_names()
   rows = gate_status.gate_rows(gates, defined, {})

   for row in rows:
      is_defined = row["name"] in defined
      expected = gate_status.PRESENT if is_defined else gate_status.MISSING

      assert row["presence"] == expected


def test_the_definition_scanner_finds_a_gate_that_exists(gates):
   defined = gate_status.defined_test_names()

   assert "test_purge_requires_reauth" in defined
   assert "test_session_login_to_feedback" in defined
   assert "made_up_gate_that_is_not_in_the_tree" not in defined


def test_a_missing_gate_is_never_reported_passing(gates):
   defined = gate_status.defined_test_names()
   outcomes = {gate.name: gate_status.PASSING for gate in gates}
   rows = gate_status.gate_rows(gates, defined, outcomes)

   for row in rows:
      is_missing = row["presence"] == gate_status.MISSING

      if is_missing:
         assert row["outcome"] == gate_status.UNKNOWN


def test_a_failing_case_makes_the_whole_gate_read_failing(tmp_path):
   report = tmp_path / "report.xml"
   report.write_text(
      "<testsuites><testsuite>"
      '<testcase name="test_one[a]"/>'
      '<testcase name="test_one[b]"><failure message="boom"/></testcase>'
      '<testcase name="test_two"/>'
      "</testsuite></testsuites>"
   )

   outcomes = gate_status.read_outcomes(report)

   assert outcomes["test_one"] == gate_status.FAILING
   assert outcomes["test_two"] == gate_status.PASSING


def test_an_uncovered_gate_reads_unknown_rather_than_passing(gates):
   defined = gate_status.defined_test_names()
   rows = gate_status.gate_rows(gates, defined, {})

   for row in rows:
      assert row["outcome"] == gate_status.UNKNOWN


def test_the_command_line_prints_a_row_for_every_gate(gates):
   result = subprocess.run(
      [sys.executable, "tools/gate_status.py", "--no-run", "--phase", "P1"],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )

   p1 = [gate for gate in gates if gate.phase == "P1"]

   for gate in p1:
      assert gate.name in result.stdout

   assert f"P1: {len(p1)} gates" in result.stdout

def test_a_present_gate_with_a_passing_outcome_reads_passing(gates):
   defined = gate_status.defined_test_names()
   present = [gate for gate in gates if gate.name in defined]

   assert present, "no gate in the plan has a test function, so this asserts nothing"

   outcomes = {gate.name: gate_status.PASSING for gate in present}
   rows = gate_status.gate_rows(gates, defined, outcomes)

   reported = {row["name"]: row["outcome"] for row in rows}

   for gate in present:
      assert reported[gate.name] == gate_status.PASSING


def test_a_present_gate_with_a_failing_outcome_reads_failing(gates):
   defined = gate_status.defined_test_names()
   present = [gate for gate in gates if gate.name in defined]

   outcomes = {present[0].name: gate_status.FAILING}
   rows = gate_status.gate_rows(gates, defined, outcomes)

   reported = {row["name"]: row["outcome"] for row in rows}

   assert reported[present[0].name] == gate_status.FAILING


def test_the_summary_counts_the_passing_gates(gates):
   defined = gate_status.defined_test_names()
   present = [gate for gate in gates if gate.name in defined]
   outcomes = {gate.name: gate_status.PASSING for gate in present}
   rows = gate_status.gate_rows(gates, defined, outcomes)

   summary = gate_status.summarise(rows)
   p1_present = len([row for row in rows if row["phase"] == "P1" and row["files"]])

   assert f"{p1_present} passing" in summary


def test_the_table_prints_the_outcome_column(gates):
   defined = gate_status.defined_test_names()
   present = [gate for gate in gates if gate.name in defined]
   rows = gate_status.gate_rows(gates, defined, {present[0].name: gate_status.PASSING})

   table = gate_status.format_table(rows)
   line = [row for row in table.splitlines() if present[0].name in row][0]

   assert gate_status.PASSING in line


def test_the_command_line_exits_non_zero_when_a_gate_is_missing(gates):
   defined = gate_status.defined_test_names()
   missing = [gate for gate in gates if gate.name not in defined]

   assert missing, "every gate in the plan has a test function, so this asserts nothing"

   result = subprocess.run(
      [sys.executable, "tools/gate_status.py", "--no-run"],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )

   assert result.returncode == 1


def test_the_suite_runs_under_the_repository_interpreter():
   chosen = gate_status.suite_interpreter()
   repository_python = REPOSITORY_ROOT / ".venv" / "bin" / "python"

   assert repository_python.exists(), "this repository has no .venv to run the suite with"
   assert chosen == str(repository_python)


def test_a_run_of_the_suite_marks_the_gates_that_passed(tmp_path):
   """run_suite is pointed at one gate's own file rather than at the whole tree, because this
   test runs inside the suite and a full run from here would recurse.
   """
   report = tmp_path / "report.xml"
   completed = subprocess.run(
      [
         gate_status.suite_interpreter(),
         "-m",
         "pytest",
         "-p",
         "no:warnings",
         "-o",
         "addopts=",
         f"--junitxml={report}",
         "tests/api/test_routes.py::test_purge_requires_reauth",
      ],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )

   assert report.exists(), (
      f"no report was written, so no gate can ever read passing; the runner exited "
      f"{completed.returncode} saying {completed.stderr}"
   )

   outcomes = gate_status.read_outcomes(report)
   rows = gate_status.gate_rows(
      gate_status.read_gates(), gate_status.defined_test_names(), outcomes
   )

   passing = [row for row in rows if row["outcome"] == gate_status.PASSING]

   assert [row["name"] for row in passing] == ["test_purge_requires_reauth"]
