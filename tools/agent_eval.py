"""Score the live tutor's multi-turn golden set with the deterministic checks.

   .venv/bin/python tools/agent_eval.py            replay: score every recorded candidate reply
   .venv/bin/python tools/agent_eval.py --live     refused here; live runs are the orchestrator's

Replay composes, for every turn of every case in content/golden/agent.json, the packet the live
route would compose (app/evals/golden.py agent_turn_packet), runs each labelled check of
app/evals/agent_checks.py on the recorded candidate reply, and prints the pass rate per check with
its denominator and the ids of every turn where a check and its label disagree. No model is called.
A live run needs the agent role's provider chain, which the turn route wires (docs/agent/
build-plan.md, slice 4), so --live is parsed and exits with a message instead of calling anything.

Exits 1 when the set fails validation or any check disagrees with its label.
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.content.loader import load_snapshot  # noqa: E402
from app.evals import agent_checks, golden  # noqa: E402
from app.runtime.context import DEFAULT_CONTENT_ROOT  # noqa: E402

LIVE_REFUSAL = (
   "live runs of the agent golden set are made by the orchestrator only, once the turn route wires "
   "the agent provider chain; this run made no model call"
)


def pass_rates(rows):
   table = defaultdict(lambda: [0, 0])

   for row in rows:
      counts = table[row["check"]]
      counts[0] += 1 if row["passed"] else 0
      counts[1] += 1

   return {check: tuple(table[check]) for check in agent_checks.CHECKS if check in table}


def disagreements(rows):
   return [row for row in rows if row["label"] != row["passed"]]


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("--live", action="store_true", help="refused in this build")
   arguments = parser.parse_args(argv)

   if arguments.live:
      print(LIVE_REFUSAL)
      return 2

   library = golden.load_library()
   document = golden.load_set("agent")
   problems = golden.validate("agent", document, library)

   if problems:
      for problem in problems:
         print(problem)

      return 1

   rows = golden.agent_verdicts(document, load_snapshot(DEFAULT_CONTENT_ROOT), library["items"])
   turn_count = sum(len(case["turns"]) for case in document["cases"])
   print(f"{len(document['cases'])} cases, {turn_count} turns, replay")

   for check, (passed, total) in pass_rates(rows).items():
      print(f"{check}: {passed}/{total} passed")

   disagreeing = disagreements(rows)

   for row in disagreeing:
      print(f"disagreement: {row['case_id']} turn {row['turn']} {row['check']} label {row['label']} check {row['passed']}")

   print(f"{len(disagreeing)} disagreements between labels and checks")

   return 1 if disagreeing else 0


if __name__ == "__main__":
   sys.exit(main())
