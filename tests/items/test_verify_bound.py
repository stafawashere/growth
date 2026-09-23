"""The time bound on app/items/verify.py equivalence, on the main thread and off it.

docs/plan/04-item-generation.md: SymPy equivalence is undecidable in general and an unsettled
comparison is not a pass. docs/plan/11-phased-delivery.md check 28 counts a comparison that times
out as not settled. A sync FastAPI route runs in a worker thread, where SIGALRM cannot be set, so
the bound there has to come from somewhere else.
"""
import json
import threading
import time
from pathlib import Path

import pytest
import sympy

from app.items.mathjson import to_sympy
from app.items.verify import equivalence

ROOT = Path(__file__).resolve().parents[2]
PAIRS_PATH = ROOT / "tests" / "fixtures" / "answers_equiv" / "pairs.json"

BOUND_UNDER_TEST_S = 1

# Past the deadline the caller still kills and reaps the child, or unwinds the alarm handler.
# Measured on the development machine at 4 to 17 ms past the deadline for both paths. One second
# leaves room for a loaded host and stays far below the pathological pair's unbounded run time.
TEARDOWN_MARGIN_S = 1

# Unbounded, _equivalence_impl on this pair ran 13.15 s on the development machine before
# settling, well past BOUND_UNDER_TEST_S and past equivalence's own default.
PATHOLOGICAL_DEGREE = 24


def pathological_pair():
   x, y, z = sympy.symbols("x y z")
   left = (x + y + z + 1) ** PATHOLOGICAL_DEGREE
   right = sympy.expand(left) + 1

   return left, right


def run_on_worker_thread(function, *args, **kwargs):
   outcome = {}

   def target():
      started = time.monotonic()

      try:
         outcome["result"] = function(*args, **kwargs)
      except BaseException as failure:
         outcome["failure"] = failure
      finally:
         outcome["elapsed"] = time.monotonic() - started

   worker = threading.Thread(target=target)
   worker.start()
   worker.join()

   return outcome


def warm_worker_path():
   x = sympy.Symbol("x")
   outcome = run_on_worker_thread(equivalence, x + x, 2 * x)

   assert outcome.get("result") == "equivalent", outcome


def test_a_pathological_comparison_off_the_main_thread_is_unsettled_within_the_bound():
   warm_worker_path()
   left, right = pathological_pair()

   outcome = run_on_worker_thread(equivalence, left, right, timeout_s=BOUND_UNDER_TEST_S)

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"] == "unsettled"
   assert outcome["elapsed"] < BOUND_UNDER_TEST_S + TEARDOWN_MARGIN_S


def test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound():
   assert threading.current_thread() is threading.main_thread()

   left, right = pathological_pair()
   started = time.monotonic()
   result = equivalence(left, right, timeout_s=BOUND_UNDER_TEST_S)
   elapsed = time.monotonic() - started

   assert result == "unsettled"
   assert elapsed < BOUND_UNDER_TEST_S + TEARDOWN_MARGIN_S


def test_fixture_pairs_settle_the_same_way_off_the_main_thread():
   pairs = json.loads(PAIRS_PATH.read_text())

   for pair in pairs:
      left = to_sympy(pair["left"])
      right = to_sympy(pair["right"])
      on_main_thread = equivalence(left, right)
      off_main_thread = run_on_worker_thread(equivalence, left, right)

      assert "failure" not in off_main_thread, (pair, off_main_thread.get("failure"))
      assert off_main_thread["result"] == on_main_thread, pair

      if pair["equivalent"]:
         assert off_main_thread["result"] == "equivalent", pair
      else:
         assert off_main_thread["result"] != "equivalent", pair


def test_an_error_inside_the_comparison_reaches_the_caller_off_the_main_thread():
   with pytest.raises(TypeError):
      equivalence("left", "right")

   outcome = run_on_worker_thread(equivalence, "left", "right")

   assert isinstance(outcome.get("failure"), TypeError), outcome


@pytest.mark.parametrize("disabling_timeout", [0, -1, None])
def test_a_timeout_that_would_disable_the_bound_is_refused(disabling_timeout):
   x = sympy.Symbol("x")

   with pytest.raises(ValueError):
      equivalence(x, x, timeout_s=disabling_timeout)

   outcome = run_on_worker_thread(equivalence, x, x, timeout_s=disabling_timeout)

   assert isinstance(outcome.get("failure"), ValueError), outcome