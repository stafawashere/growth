"""A grading child that dies is a server failure, never a verdict on the student.

app/items/verify.py raises ChildDiedError when a forkserver child exits before sending a result. That
is not the unsettled comparison 03 lets fall through as ungraded, so the attempt route answers 503
and writes no attempt row, and the same answer can be submitted again and graded.
"""
from sqlalchemy import func, select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.items import grade as grade_module
from app.items.verify import ChildDiedError
from tests.api.conftest import KEY_MATHJSON
from tests.api.test_served_steps import served_at, submit


def child_dies(*arguments, **keywords):
   raise ChildDiedError("the bounded child exited with code 1 before sending a result")


def attempt_count(world, session_id, item_id):
   with OrmSession(world.engine) as db:
      return db.scalar(
         select(func.count())
         .select_from(models.Attempt)
         .where(models.Attempt.session_id == session_id, models.Attempt.item_id == item_id)
      )


def stored_correct(world, attempt_id):
   with OrmSession(world.engine) as db:
      return db.get(models.Attempt, attempt_id).correct


def test_a_child_death_while_grading_writes_no_attempt_and_the_resubmit_is_graded(world, monkeypatch):
   client = world.client()
   session_id, served = served_at(world, client, "unsupported")
   item = served.json()["item"]
   answer = {"mathjson": KEY_MATHJSON}

   with monkeypatch.context() as patched:
      patched.setattr(grade_module, "run_bounded", child_dies)
      refused = submit(client, session_id, item, answer)

   assert refused.status_code == 503
   assert attempt_count(world, session_id, item["id"]) == 0

   resubmitted = submit(client, session_id, item, answer)

   assert resubmitted.status_code == 200
   assert resubmitted.json()["correct"] is True
   assert attempt_count(world, session_id, item["id"]) == 1
   assert stored_correct(world, resubmitted.json()["id"]) == 1
