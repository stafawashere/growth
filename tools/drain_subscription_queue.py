"""Retry the tutor calls a Claude subscription usage limit queued, once the window has reset.

Usage: python3 tools/drain_subscription_queue.py [--limit N] [--dry-run]

The backend is the one the app would run, from the same environment (app/main.py build_tutor):
GROWTH_AI_BACKEND=subscription, the default, retries on the operator's subscription through the
claude CLI under the subscription pacing guard, and GROWTH_AI_BACKEND=api retries on the paid key
under the per-role and developer spend caps. No other backend drains, so the paid API is never
reached unless GROWTH_AI_BACKEND=api says so. Each answered call is stored on its attempt, where
the feedback screen finds it (app/feedback/drain.py). --dry-run lists the due jobs and calls
nothing.

Exit 0 when the drain ran, whatever it found; 2 when the backend cannot drain.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session as OrmSession

from app.auth.service import utc_now
from app.db.models import make_engine
from app.feedback.drain import drain_queued_calls, due_jobs
from app.main import DEFAULT_DB_PATH, build_subscription_pacing, build_tutor, build_tutor_caps, resolve_ai_backend

DRAINING_BACKENDS = ("subscription", "api")


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Retry tutor calls queued behind a subscription limit.")
   parser.add_argument("--limit", type=int, default=None, help="drain at most this many due jobs")
   parser.add_argument("--dry-run", action="store_true", help="list the due jobs and call nothing")

   return parser.parse_args(argv)


def main(argv=None, env=None):
   arguments = parse_arguments(argv)
   env = os.environ if env is None else env
   backend = resolve_ai_backend(env)
   can_drain = backend in DRAINING_BACKENDS

   if not can_drain:
      print(f"GROWTH_AI_BACKEND={backend} cannot drain queued calls; use subscription or api", file=sys.stderr)

      return 2

   engine = make_engine(env.get("GROWTH_DB_PATH", str(DEFAULT_DB_PATH)))

   with OrmSession(engine) as db:
      due = due_jobs(db, utc_now())
      print(f"backend = {backend}")
      print(f"due = {len(due)}")

      if arguments.dry_run:
         return 0

      provider = build_tutor(env)

      if provider is None:
         print("no tutor is configured for this backend; nothing drained", file=sys.stderr)

         return 2

      report = drain_queued_calls(
         db,
         provider,
         utc_now,
         tutor_caps=build_tutor_caps(env),
         pacing=build_subscription_pacing(env),
         limit=arguments.limit,
      )

   print(f"done = {report.done}")
   print(f"requeued = {report.requeued}")
   print(f"failed = {report.failed}")
   print(f"skipped = {report.skipped}")
   print(f"stopped_by = {report.stopped_by or 'none'}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
