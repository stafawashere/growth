"""The forkserver child behind run_bounded is kept between calls, and never after a timeout.

A child per call refilled SymPy's caches every time: ingesting the 130 P1 agent drafts from a
thread other than the main one took 247 s, and 15.5 s with the child kept (2026-09-24, same
machine under load from other sessions). Keeping the child is only safe if a child that outlived its deadline is never asked again,
because its late answer would otherwise be read as the next caller's result.
"""
import os
import time

from app.items.verify import run_bounded
from tests.items.test_verify_bound import run_on_worker_thread


def _answer_after(seconds, answer):
   time.sleep(seconds)

   return answer


def test_consecutive_bounded_calls_off_the_main_thread_share_one_child():
   first = run_on_worker_thread(run_bounded, os.getpid, (), 5, None)
   second = run_on_worker_thread(run_bounded, os.getpid, (), 5, None)

   assert "failure" not in first, first.get("failure")
   assert "failure" not in second, second.get("failure")
   assert first["result"] != os.getpid()
   assert second["result"] == first["result"]


def test_a_call_after_a_timeout_gets_its_own_answer_from_a_new_child():
   bound = 1
   before = run_on_worker_thread(run_bounded, os.getpid, (), 5, None)
   timed_out = run_on_worker_thread(
      run_bounded, _answer_after, (bound + 0.5, "late"), bound, "unsettled"
   )
   after = run_on_worker_thread(run_bounded, _answer_after, (0, "fresh"), 5, None)
   after_pid = run_on_worker_thread(run_bounded, os.getpid, (), 5, None)

   assert timed_out.get("result") == "unsettled", timed_out
   assert after.get("result") == "fresh", after
   assert after_pid.get("result") != before.get("result")
