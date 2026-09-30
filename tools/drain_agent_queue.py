"""Run one pass of the live tutor agent's consolidation queue by hand.

The running app does this on its own after each tutor drain (app/feedback/autodrain.py); this tool
runs one pass for a server that is not running or was started with GROWTH_AUTO_DRAIN=off.

Usage: python3 tools/drain_agent_queue.py [--limit N] [--dry-run]

The pass closes the conversations idle for 30 minutes, enqueues their consolidation, and runs the
due agent_consolidate jobs on the memory role's chain (app/agent/drain.py), built from the same
environment as the app: GROWTH_AI_BACKEND=subscription, the default, calls the operator's
subscription through the claude CLI under the subscription pacing guard, and GROWTH_AI_BACKEND=api
may also call the paid key under the memory caps and the developer spend cap. No other backend
drains. --dry-run counts the due jobs and changes nothing.

Exit 0 when the pass ran, whatever it found; 2 when the backend cannot drain.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session as OrmSession

from app.agent.drain import AGENT_JOBS_PER_PASS, drain_agent_jobs, due_jobs, sweep_idle_conversations
from app.auth.service import utc_now
from app.db.models import make_engine
from app.main import DEFAULT_DB_PATH, build_agent_caps, build_tutor, provider_links, resolve_ai_backend
from app.providers.router import CooldownBoard

DRAINING_BACKENDS = ("subscription", "api")


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Run one pass of the agent's consolidation queue.")
   parser.add_argument("--limit", type=int, default=AGENT_JOBS_PER_PASS, help="run at most this many due jobs")
   parser.add_argument("--dry-run", action="store_true", help="count the due jobs and change nothing")

   return parser.parse_args(argv)


def main(argv=None, env=None):
   arguments = parse_arguments(argv)
   env = os.environ if env is None else env
   backend = resolve_ai_backend(env)
   can_drain = backend in DRAINING_BACKENDS

   if not can_drain:
      print(f"GROWTH_AI_BACKEND={backend} cannot drain the agent queue; use subscription or api", file=sys.stderr)

      return 2

   engine = make_engine(env.get("GROWTH_DB_PATH", str(DEFAULT_DB_PATH)))

   with OrmSession(engine) as db:
      now = utc_now()
      print(f"backend = {backend}")
      print(f"due = {len(due_jobs(db, now))}")

      if arguments.dry_run:
         return 0

      provider = build_tutor(env)

      if provider is None:
         print("no provider is configured for this backend; nothing drained", file=sys.stderr)

         return 2

      swept = sweep_idle_conversations(db, now)
      db.commit()
      report = drain_agent_jobs(
         db,
         now,
         provider_links(env, provider),
         build_agent_caps(env),
         CooldownBoard(),
         limit=arguments.limit,
      )

   print(f"swept = {swept}")
   print(f"done = {report.done}")
   print(f"requeued = {report.requeued}")
   print(f"failed = {report.failed}")
   print(f"applied = {report.applied}")
   print(f"rejected = {report.rejected}")
   print(f"stopped_by = {report.stopped_by or 'none'}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
