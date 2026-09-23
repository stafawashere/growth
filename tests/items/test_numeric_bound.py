"""The time bound on numeric_check, compare_expressions and the short answer grading path.

tests/items/test_verify_bound.py bounds equivalence. numeric_check runs after it in
app/items/grade.py and again in compare_expressions, and a student submission reaches both from a
sync FastAPI route, which runs in a worker thread where SIGALRM cannot be set.
"""
import json
import threading
import time

import pytest
import sympy
from sqlalchemy.orm import Session as OrmSession
from starlette.testclient import TestClient

from app.db import models
from app.items import grade as grade_module
from app.items.grade import grade
from app.items.mathjson import to_sympy
from app.items.verify import (
   COMPARISON_TIMEOUT_S,
   DISTINCT,
   EQUAL,
   UNSETTLED_VIOLATION,
   compare_expressions,
   numeric_check,
)
from tests.api.conftest import TODAY, world  # noqa: F401
from tests.api.test_routes import open_session
from tests.items.test_grade import build_item
from tests.items.test_verify_bound import (
   BOUND_UNDER_TEST_S,
   PAIRS_PATH,
   TEARDOWN_MARGIN_S,
   run_on_worker_thread,
)

# Unbounded on the development machine, numeric_check on sin(10**1000000) against itself plus one
# ran 34.0 s, because evalf reduces the argument modulo pi at a million digits. That is past the
# whole grade call's bound below, and the parse itself took 0.27 s.
SIN_ARGUMENT_EXPONENT = 1000000
PATHOLOGICAL_MATHJSON = ["Sin", ["Power", 10, SIN_ARGUMENT_EXPONENT]]

# Unbounded on the development machine, to_sympy on 10**10000000 ran 9.96 s, because SymPy
# evaluates an integer power eagerly. That is past COMPARISON_TIMEOUT_S + TEARDOWN_MARGIN_S.
SLOW_PARSE_MATHJSON = ["Power", 10, 10000000]

# grade.py runs parsing, equivalence and the numeric check to the key's decimal places in
# sequence, each under the bound, and grade takes no timeout of its own, so the whole call is
# bounded by three of verify's default.
BOUNDED_STAGES_IN_A_NUMERIC_GRADE = 3

# A student-typed Equal node reaches equivalence as a sympy Eq, and Symbol minus Eq raises
# TypeError. A Rational over a symbol raises TypeError inside to_sympy. Both messages are SymPy's
# and quote what the student typed.
RAISING_SUBMISSION = ["Equal", "x", 1]
RAISING_SUBMISSIONS = [RAISING_SUBMISSION, ["Rational", "x", 2]]


def pathological_pair():
   left = to_sympy(PATHOLOGICAL_MATHJSON)

   return left, left + 1


def numeric_item():
   return build_item({"form": "numeric", "mathjson": 0.5, "decimals": 3})


def warm_worker_path():
   x = sympy.Symbol("x")
   outcome = run_on_worker_thread(numeric_check, x + x, 2 * x)

   assert outcome.get("result") is True, outcome


def test_a_pathological_numeric_check_off_the_main_thread_is_unsettled_within_the_bound():
   warm_worker_path()
   left, right = pathological_pair()

   outcome = run_on_worker_thread(numeric_check, left, right, timeout_s=BOUND_UNDER_TEST_S)

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"] is None
   assert outcome["elapsed"] < BOUND_UNDER_TEST_S + TEARDOWN_MARGIN_S


def test_a_pathological_numeric_check_on_the_main_thread_is_unsettled_within_the_bound():
   assert threading.current_thread() is threading.main_thread()

   left, right = pathological_pair()
   started = time.monotonic()
   result = numeric_check(left, right, timeout_s=BOUND_UNDER_TEST_S)
   elapsed = time.monotonic() - started

   assert result is None
   assert elapsed < BOUND_UNDER_TEST_S + TEARDOWN_MARGIN_S


def test_a_pathological_comparison_of_options_off_the_main_thread_is_unsettled_within_the_bound():
   warm_worker_path()
   left, right = pathological_pair()

   outcome = run_on_worker_thread(compare_expressions, left, right, timeout_s=BOUND_UNDER_TEST_S)

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"] == UNSETTLED_VIOLATION
   assert outcome["elapsed"] < BOUND_UNDER_TEST_S + TEARDOWN_MARGIN_S


def test_a_pathological_numeric_submission_leaves_the_whole_grade_call_bounded():
   warm_worker_path()

   outcome = run_on_worker_thread(grade, numeric_item(), {"mathjson": PATHOLOGICAL_MATHJSON}, {})
   one_stage_bound = COMPARISON_TIMEOUT_S + TEARDOWN_MARGIN_S
   whole_call_bound = BOUNDED_STAGES_IN_A_NUMERIC_GRADE * one_stage_bound

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"]["correct"] is None
   assert "numeric comparison" in outcome["result"]["reason"]
   assert outcome["elapsed"] < whole_call_bound


def test_a_submission_that_parses_slowly_is_ungraded_within_one_bound():
   warm_worker_path()

   outcome = run_on_worker_thread(grade, numeric_item(), {"mathjson": SLOW_PARSE_MATHJSON}, {})

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"]["correct"] is None
   assert "parsing" in outcome["result"]["reason"]
   assert outcome["elapsed"] < COMPARISON_TIMEOUT_S + TEARDOWN_MARGIN_S


def test_fixture_pairs_settle_by_their_label_off_the_main_thread():
   pairs = json.loads(PAIRS_PATH.read_text())

   for pair in pairs:
      left = to_sympy(pair["left"])
      right = to_sympy(pair["right"])
      expected_comparison = EQUAL if pair["equivalent"] else DISTINCT
      item = build_item({"form": "symbolic", "mathjson": pair["left"]})

      numeric = run_on_worker_thread(numeric_check, left, right)
      compared = run_on_worker_thread(compare_expressions, left, right)
      graded = run_on_worker_thread(grade, item, {"mathjson": pair["right"]}, {})

      assert numeric.get("result") is pair["equivalent"], (pair, numeric)
      assert compared.get("result") == expected_comparison, (pair, compared)
      assert graded.get("result", {}).get("correct") is pair["equivalent"], (pair, graded)


def sympy_message_for(submission):
   x = sympy.Symbol("x")

   try:
      x - to_sympy(submission)
   except TypeError as failure:
      return str(failure)

   raise AssertionError(f"{submission} was expected to raise")


@pytest.mark.parametrize("submission", RAISING_SUBMISSIONS)
def test_a_comparison_that_raises_leaves_the_grade_unsettled_without_its_message(submission):
   sympy_message = sympy_message_for(submission)
   item = build_item({"form": "symbolic", "mathjson": "x"})
   on_main_thread = grade(item, {"mathjson": submission}, {})
   off_main_thread = run_on_worker_thread(grade, item, {"mathjson": submission}, {})

   assert "failure" not in off_main_thread, off_main_thread.get("failure")

   for result in (on_main_thread, off_main_thread["result"]):
      assert result["correct"] is None
      assert "raised TypeError" in result["reason"]
      assert sympy_message not in result["reason"]


def test_a_numeric_fallback_that_raises_after_an_unsettled_comparison_is_ungraded(monkeypatch):
   monkeypatch.setattr(grade_module, "equivalence", lambda left, right: "unsettled")

   result = grade(numeric_item(), {"mathjson": RAISING_SUBMISSION}, {})

   assert result["correct"] is None
   assert "numeric comparison raised" in result["reason"]


def test_a_comparison_that_raises_is_stored_unsettled_through_the_attempt_route(world):  # noqa: F811
   client = TestClient(
      world.app,
      raise_server_exceptions=False,
      client=("127.0.0.1", 40000),
      base_url="http://127.0.0.1",
   )
   world.register(client)
   session_id = open_session(client).json()["id"]
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   assert item["format"] == "short_answer"

   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"form": "symbolic", "mathjson": RAISING_SUBMISSION},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200, attempted.text

   with OrmSession(world.engine) as db:
      stored = db.get(models.Attempt, attempted.json()["id"])

      assert stored is not None
      assert stored.correct is None
