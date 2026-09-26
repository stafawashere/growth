"""The feedback route runs the tutor down its fallback chain, against tests/fixtures/fake_claude/claude.

With a second link, a subscription limit is answered by it and nothing is queued. Without one, the
limit degrades to static feedback and a queued call, and while the link cools no further CLI
process is started for the next attempt's feedback.
"""
import json
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.providers.call_queue import QUEUED_CALL_JOB_TYPE
from app.providers.guard import SubscriptionPacingCaps
from app.providers.replay import ReplayProvider
from app.providers.router import API_LINK, SUBSCRIPTION_LINK, ChainLink
from app.providers.subscription import SubscriptionProvider
from tests.api.conftest import TODAY, WRONG_MATHJSON
from tests.api.test_tutor_budget import wrong_short_answer
from tests.providers.test_subscription import FakeCli

CASSETTE = Path(__file__).resolve().parents[1] / "fixtures" / "provider_cassettes" / "tutor_elaborated_v1.json"


@pytest.fixture
def cli(tmp_path):
   home = tmp_path / "home"
   home.mkdir()

   return FakeCli(home)


def cassette_text():
   return json.loads(Path(CASSETTE).read_text())["text"]


def subscription_link(cli):
   return ChainLink(SUBSCRIPTION_LINK, SubscriptionProvider(environ=cli.environ()), pacing=SubscriptionPacingCaps())


def queued_jobs(engine):
   with OrmSession(engine) as db:
      return db.scalars(select(models.Job).where(models.Job.type == QUEUED_CALL_JOB_TYPE)).all()


def feedback_for(client, session_id, attempt_id):
   response = client.get(f"/sessions/{session_id}/attempts/{attempt_id}/feedback")

   assert response.status_code == 200

   return response.json()


def second_wrong_answer(client, session_id):
   item = client.get(f"/sessions/{session_id}/next").json()["item"]

   if item is None:
      return None

   attempted = client.post(
      f"/sessions/{session_id}/attempts",
      json={
         "item_id": item["id"],
         "answer": {"form": "symbolic", "mathjson": WRONG_MATHJSON},
         "elapsed_ms": 90000,
         "today": TODAY.isoformat(),
         "confidence": "confident",
      },
   )

   assert attempted.status_code == 200

   return attempted.json()["id"]


def test_a_limit_on_the_subscription_is_answered_by_the_next_link(world, cli):
   cli.mode("weekly_limit")
   world.settings.tutor_links = (subscription_link(cli), ChainLink(API_LINK, ReplayProvider(cassette_path=CASSETTE)))
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   body = feedback_for(client, session_id, attempt_id)

   assert body["tutor_unavailable"] is False
   assert body["sentence"] == cassette_text()
   assert queued_jobs(world.engine) == []
   assert cli.record()["argv"][0].endswith("claude")


def test_while_the_limit_cools_no_cli_process_is_started(world, cli):
   cli.mode("weekly_limit")
   world.settings.tutor_links = (subscription_link(cli),)
   client = world.client()
   world.register(client)
   session_id, attempt_id = wrong_short_answer(client)
   first = feedback_for(client, session_id, attempt_id)

   assert first["tutor_unavailable"] is True
   assert len(queued_jobs(world.engine)) == 1

   (cli.home / "fake_claude_record.json").unlink()
   next_attempt_id = second_wrong_answer(client, session_id)

   assert next_attempt_id is not None

   second = feedback_for(client, session_id, next_attempt_id)

   assert second["tutor_unavailable"] is True
   assert len(queued_jobs(world.engine)) == 2
   assert not (cli.home / "fake_claude_record.json").exists()
