"""The running app drains queued tutor calls on its own, replacing a hand run of
tools/drain_subscription_queue.py after each usage-limit window.

A daemon thread wakes every PASS_INTERVAL and runs one drain pass (app/feedback/drain.py) over the
tutor's fallback chain. It is safe by construction rather than by care:

- Waiting for the window. The drain shares the app's cooldown board, so for LIMIT_COOLDOWN after
  the feedback route met a limit the subscription link is skipped without starting a process, and
  the pass defers the job by LIMIT_RETRY_AFTER and ends. A pass that meets the limit itself does
  the same. After a restart the board is empty, so the first pass may start one process to learn
  that the limit still holds.
- Paced. Every retry goes through the same guards as a live call, so the subscription's per-day
  and per-minute call counts bind the drain too, and a pacing stop ends the pass.
- Capped. A pass retries at most JOBS_PER_PASS jobs, so a long queue drains over several passes
  instead of in one burst after a window resets.
- Never paid unless allowed. The chain holds the paid API link only when GROWTH_AI_BACKEND=api put
  it there; replay and none have no link, and the drain never starts for them.

GROWTH_AUTO_DRAIN=off turns it off. Nothing starts until the application's startup event, so
building an application in a test starts no thread.
"""
import logging
import threading
from datetime import timedelta

from sqlalchemy.orm import Session as OrmSession

from app.auth.service import utc_now
from app.feedback.drain import drain_queued_calls
from app.providers.router import API_LINK, SUBSCRIPTION_LINK

logger = logging.getLogger(__name__)

AUTO_DRAIN_ENV_VAR = "GROWTH_AUTO_DRAIN"
PASS_INTERVAL = timedelta(minutes=10)
JOBS_PER_PASS = 5
DRAINING_LINKS = (SUBSCRIPTION_LINK, API_LINK)


def can_drain(links):
   """Only a live backend drains: a replayed sentence stored on a real attempt would be a canned
   answer the student reads as the tutor's."""
   has_links = len(links) > 0
   every_link_is_live = all(link.name in DRAINING_LINKS for link in links)

   return has_links and every_link_is_live


def auto_drain_enabled(env):
   configured = env.get(AUTO_DRAIN_ENV_VAR, "on")
   is_known = configured in ("on", "off")

   if not is_known:
      raise ValueError(f"{AUTO_DRAIN_ENV_VAR} must be on or off, got {configured!r}")

   return configured == "on"


class AutoDrain:
   def __init__(self, engine, links, tutor_caps, board, clock=None, interval=PASS_INTERVAL,
                jobs_per_pass=JOBS_PER_PASS):
      self._engine = engine
      self._links = tuple(links)
      self._tutor_caps = tutor_caps
      self._board = board
      self._clock = clock or utc_now
      self._interval = interval
      self._jobs_per_pass = jobs_per_pass
      self._stopping = threading.Event()
      self._thread = None
      self._pass_lock = threading.Lock()

   def run_pass(self):
      """One pass, never two at once. Returns the DrainReport, or None when the chain cannot drain."""
      if not can_drain(self._links):
         return None

      with self._pass_lock:
         with OrmSession(self._engine) as db:
            return drain_queued_calls(
               db,
               None,
               self._clock,
               tutor_caps=self._tutor_caps,
               limit=self._jobs_per_pass,
               links=self._links,
               board=self._board,
            )

   def start(self):
      is_running = self._thread is not None and self._thread.is_alive()
      should_not_start = is_running or not can_drain(self._links)

      if should_not_start:
         return False

      self._stopping.clear()
      self._thread = threading.Thread(target=self._loop, name="growth-auto-drain", daemon=True)
      self._thread.start()

      return True

   def stop(self):
      self._stopping.set()

      if self._thread is not None:
         self._thread.join(timeout=5)

   def _loop(self):
      while not self._stopping.wait(self._interval.total_seconds()):
         try:
            report = self.run_pass()
         except Exception:
            logger.exception("the automatic drain pass failed; the next pass will try again")
            continue

         ran = report is not None
         touched_a_job = ran and report.done + report.requeued + report.failed > 0

         if touched_a_job:
            logger.info(
               "automatic drain: done %s, requeued %s, failed %s, stopped by %s",
               report.done,
               report.requeued,
               report.failed,
               report.stopped_by,
            )
