"""A forkserver child that exits without sending a result is a distinct outcome from a timeout.

docs/plan/04-item-generation.md and 11's check 28 treat a comparison that outlives its bound as
unsettled, not as an error. A child that dies before the deadline, whether it crashes at startup
or is killed by something outside run_bounded, has not merely run long, so run_bounded must raise
rather than report unsettled. app/items/grade.py folds any other raised exception into an ungraded
result, but a dead child says nothing about the answer, so at each of the three bounded calls a
grade makes it is raised to the caller, which refuses the attempt rather than storing it ungraded.
"""
import os
import threading
import time

import pytest

from app.items import grade as grade_module
from app.items.grade import grade
from app.items.verify import COMPARISON_TIMEOUT_S, ChildDiedError, run_bounded
from tests.items.test_grade import ERRORS, numeric_item_with_units, symbolic_item
from tests.items.test_verify_bound import TEARDOWN_MARGIN_S, run_on_worker_thread


def _die_before_sending():
   os._exit(1)


def _sleep_past_the_deadline(seconds):
   time.sleep(seconds)

   return "reached"


def test_a_child_that_dies_before_sending_raises_off_the_main_thread():
   outcome = run_on_worker_thread(
      run_bounded, _die_before_sending, (), COMPARISON_TIMEOUT_S, "unsettled"
   )

   assert outcome.get("result") is None
   assert isinstance(outcome.get("failure"), ChildDiedError)


def test_a_genuine_timeout_still_reports_unsettled_off_the_main_thread():
   bound = 1

   outcome = run_on_worker_thread(
      run_bounded, _sleep_past_the_deadline, (bound + 2,), bound, "unsettled"
   )

   assert "failure" not in outcome, outcome.get("failure")
   assert outcome["result"] == "unsettled"
   assert outcome["elapsed"] < bound + TEARDOWN_MARGIN_S


def test_the_death_before_sending_is_not_mistaken_for_a_timeout():
   with_death = run_on_worker_thread(
      run_bounded, _die_before_sending, (), COMPARISON_TIMEOUT_S, "unsettled"
   )
   with_timeout = run_on_worker_thread(
      run_bounded, _sleep_past_the_deadline, (2,), 1, "unsettled"
   )

   assert with_death.get("result") is None
   assert isinstance(with_death.get("failure"), ChildDiedError)
   assert with_timeout.get("result") == "unsettled"
   assert "failure" not in with_timeout


def _child_dies(*arguments, **keywords):
   raise ChildDiedError("the bounded child exited with code 1 before sending a result")


def test_a_child_death_while_parsing_reaches_the_caller(monkeypatch):
   monkeypatch.setattr(grade_module, "run_bounded", _child_dies)

   with pytest.raises(ChildDiedError):
      grade(symbolic_item(), {"mathjson": ["Multiply", 2, "x"]}, ERRORS)


def test_a_child_death_during_the_symbolic_comparison_reaches_the_caller(monkeypatch):
   monkeypatch.setattr(grade_module, "equivalence", _child_dies)

   with pytest.raises(ChildDiedError):
      grade(symbolic_item(), {"mathjson": ["Multiply", 2, "x"]}, ERRORS)


def test_a_child_death_during_the_numeric_fallback_reaches_the_caller(monkeypatch):
   monkeypatch.setattr(grade_module, "equivalence", lambda left, right: "unsettled")
   monkeypatch.setattr(grade_module, "numeric_check", _child_dies)

   with pytest.raises(ChildDiedError):
      grade(numeric_item_with_units("m"), {"mathjson": 12.5, "units": "m"}, ERRORS)
