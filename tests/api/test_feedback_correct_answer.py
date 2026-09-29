"""The feedback route carries the correct response once a wrong answer is graded (03, Content,
part 3), and the first worked step for a correct opener when the tutor is off (01)."""
import json

from sqlalchemy import update
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tests.api.conftest import ITEM_OPTIONS, KEY_MATHJSON, WRONG_MATHJSON
from tests.api.test_feedback_sentence import attempt_one_distractor
from tests.api.test_feedback_short_answer import attempt_a_wrong_short_answer
from tests.api.test_opener_feedback import WORKED_STEPS, attempt_the_served_item
from tests.api.test_ungraded_flow import UNSETTLED_ANSWER, served_at, submit

KEYED_LABEL = "The limit is 2x + 1."


def label_the_keyed_option(engine):
   labelled = [dict(option, label=KEYED_LABEL) if option["is_key"] else dict(option) for option in ITEM_OPTIONS]

   with OrmSession(engine) as db:
      db.execute(update(models.Item).values(options=labelled))
      db.commit()


def feedback_of(client, session_id, attempt_id):
   response = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert response.status_code == 200

   return response.json()


def test_a_wrong_short_answer_carries_the_key(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_a_wrong_short_answer(client)
   body = feedback_of(client, session_id, attempt_id)

   assert body["kind"] == "elaborated"
   assert body["correct_answer"] == {"label": None, "mathjson": KEY_MATHJSON}


def test_a_wrong_choice_carries_the_keyed_option_label(world):
   world.settings.tutor = None
   label_the_keyed_option(world.engine)
   client = world.client()
   world.register(client)
   session_id, attempt_id = attempt_one_distractor(world, client)
   body = feedback_of(client, session_id, attempt_id)

   assert body["kind"] == "elaborated"
   assert body["correct_answer"] == {"label": KEYED_LABEL, "mathjson": None}


def test_an_ungraded_attempt_carries_no_correct_answer(world):
   client = world.client()
   session_id, served = served_at(world, client, "unsupported")
   item = served.json()["item"]
   attempted = submit(client, session_id, item, UNSETTLED_ANSWER)
   attempt_id = attempted.json()["id"]

   client.post(
      f"/sessions/{session_id}/attempts/{attempt_id}/confidence",
      json={"confidence": "unsure"},
   )

   body = feedback_of(client, session_id, attempt_id)

   assert body["kind"] == "ungraded"
   assert body["correct_answer"] is None
   assert json.dumps(KEY_MATHJSON) not in json.dumps(body)


def test_an_opener_miss_carries_no_correct_answer(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, _item, attempt = attempt_the_served_item(world, client, WRONG_MATHJSON)
   body = feedback_of(client, session_id, attempt["id"])

   assert body["kind"] == "comparison"
   assert body["correct_answer"] is None


def test_a_correct_opener_without_the_tutor_carries_the_first_worked_step(world):
   world.settings.tutor = None
   client = world.client()
   world.register(client)
   session_id, _item, attempt = attempt_the_served_item(world, client, KEY_MATHJSON)
   body = feedback_of(client, session_id, attempt["id"])

   assert attempt["correct"] is True
   assert body["comparison"] is None
   assert body["sentence"] is None
   assert body["first_worked_step"] == {"index": 1, "text": WORKED_STEPS[0]["text"]}
