"""Gate 25 of docs/plan/11-phased-delivery.md, run from the operator's pytest suite.

The property is a client one, so the work is done by app/web/src/session/reduced_motion.test.tsx:
under prefers-reduced-motion: reduce every transform transition is replaced by an opacity
cross-fade, and each of the five P1 feedback affordances still reaches the student. This module
runs that case and reads the vitest JSON report, so a run that matched no file, or that passed
zero cases, is not read as a met gate. There is no skip here: a client that is not installed is a
gate that cannot be shown to hold, which is a failure.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent

CLIENT_ROOT = REPOSITORY_ROOT / "app" / "web"

CASE_PATH = CLIENT_ROOT / "src" / "session" / "reduced_motion.test.tsx"

REPORT_PATH = CLIENT_ROOT / ".gate-reduced-motion.json"

GATE_SCRIPT = "gate:reduced-motion"

CASE_TITLE = re.compile(
   r"""^\s*it(?P<modifier>\.[a-z]+)?\(\s*"(?P<title>(?:[^"\\]|\\.)+)"\s*,""", re.MULTILINE
)

# it.skip and it.todo declare a case that never runs, and it.only silences every other case in
# the file. Any of them would let a breach of 08's replace-do-not-delete rule pass this gate, so
# the gate refuses the file outright rather than counting a case it cannot see run.
DISQUALIFYING_MODIFIERS = (".skip", ".todo", ".only", ".fails", ".concurrent")

PASSED = "passed"

# No plan document fixes a wall-clock budget for a client test run, so this ceiling is an
# operational guard against a hung subprocess and not a specified value.
RUN_TIMEOUT_SECONDS = 600


def declared_case_titles():
   """The case titles the vitest file itself declares, read out of the source rather than copied
   into this module, so a case renamed or deleted there is caught here."""
   declared = list(CASE_TITLE.finditer(CASE_PATH.read_text()))
   disqualified = [
      match.group("title")
      for match in declared
      if match.group("modifier") in DISQUALIFYING_MODIFIERS
   ]

   assert disqualified == [], (
      f"these cases of {CASE_PATH.name} carry a modifier that stops them running or silences "
      f"the rest of the file: {disqualified}"
   )

   return sorted({match.group("title") for match in declared})


def run_gate():
   command = ["npm", "run", GATE_SCRIPT]

   return subprocess.run(
      command,
      cwd=CLIENT_ROOT,
      capture_output=True,
      text=True,
      timeout=RUN_TIMEOUT_SECONDS,
   )


def reported_cases(report):
   """Maps every case the reporter recorded to its status."""
   statuses = {}

   for file_result in report.get("testResults", []):
      for assertion in file_result.get("assertionResults", []):
         title = assertion.get("title") or ""
         statuses[title] = assertion.get("status")

   return statuses


def test_reduced_motion_replaces():
   npm_is_installed = shutil.which("npm") is not None
   client_is_installed = (CLIENT_ROOT / "node_modules").is_dir()
   case_exists = CASE_PATH.is_file()

   assert npm_is_installed, "npm is not on PATH, so gate 25 cannot be shown to hold"
   assert client_is_installed, f"{CLIENT_ROOT}/node_modules is absent, so gate 25 cannot be shown to hold"
   assert case_exists, f"{CASE_PATH} is absent, so gate 25 has no client case to run"

   expected_titles = declared_case_titles()

   assert expected_titles, f"{CASE_PATH} declares no cases, so a passing run would prove nothing"

   REPORT_PATH.unlink(missing_ok=True)

   completed = run_gate()

   report_was_written = REPORT_PATH.is_file()

   assert report_was_written, (
      f"npm run {GATE_SCRIPT} wrote no report at {REPORT_PATH}; it exited "
      f"{completed.returncode} and said:\n{completed.stdout}\n{completed.stderr}"
   )

   report = json.loads(REPORT_PATH.read_text())
   statuses = reported_cases(report)

   ran_nothing = report.get("numTotalTests", 0) == 0
   matched_no_file = len(report.get("testResults", [])) == 0

   assert not matched_no_file, f"the vitest run matched no test file:\n{completed.stdout}"
   assert not ran_nothing, f"the vitest run reported zero cases:\n{completed.stdout}"

   not_passing = [title for title in expected_titles if statuses.get(title) != PASSED]

   assert not_passing == [], (
      f"these cases of {CASE_PATH.name} did not pass: {not_passing}\n"
      f"{completed.stdout}\n{completed.stderr}"
   )

   assert report.get("numFailedTests") == 0, completed.stdout
   assert report.get("numPassedTests") == len(expected_titles), (
      f"the report holds {report.get('numPassedTests')} passing cases and the file declares "
      f"{len(expected_titles)}:\n{completed.stdout}"
   )
   assert report.get("numPendingTests") == 0, completed.stdout
   assert report.get("numTodoTests") == 0, completed.stdout
   assert report.get("success") is True, completed.stdout
   assert completed.returncode == 0, completed.stderr
