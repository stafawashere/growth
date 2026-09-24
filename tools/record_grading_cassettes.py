"""Record the cassette books the free-response tests replay, on the operator's Claude subscription.

Usage: python3 tools/record_grading_cassettes.py paper_to_grade [--fresh]

Never run from a test: it runs the real claude CLI through app/providers/subscription.py, which
bills the operator's subscription and not the API key (the CLI reports what the calls would have
cost on the API, recorded in var/subscription_ledger.json). The environment the CLI sees is the
subscription adapter's allowlist; this tool never reads CLAUDE_CODE_OAUTH_TOKEN and passes no key.

A book keeps every call it already recorded, so an interrupted run resumes; --fresh starts an empty
book. The flow is the one tools/frq_scenarios.py defines, run exactly as the test runs it.
"""
import argparse
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.providers.cassette_book import CassetteBookProvider
from app.providers.subscription import SubscriptionProvider
from tools import frq_scenarios

FLOWS = {
   "paper_to_grade": (frq_scenarios.PAPER_TO_GRADE_BOOK, frq_scenarios.paper_to_grade),
}


def main(argv=None):
   parser = argparse.ArgumentParser()
   parser.add_argument("flow", choices=sorted(FLOWS))
   parser.add_argument("--fresh", action="store_true")
   arguments = parser.parse_args(argv)
   book_path, flow = FLOWS[arguments.flow]

   if arguments.fresh and book_path.exists():
      book_path.unlink()

   live = SubscriptionProvider(user_count=1)
   recorder = CassetteBookProvider(path=book_path, live=live, record=True)

   with tempfile.TemporaryDirectory() as scratch:
      application = frq_scenarios.build(Path(scratch) / "record.db", recorder)
      client = frq_scenarios.client_for(application)
      frq_scenarios.register(client)
      steps = flow(client)

   print(frq_scenarios.summary(steps))
   print(f"book {book_path.relative_to(REPO_ROOT)}: {len(recorder.book)} recorded calls, {len(recorder.calls)} made this run")


if __name__ == "__main__":
   main()
