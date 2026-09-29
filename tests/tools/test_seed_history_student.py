"""tools/seed_history_student.py driven through the app's TestClient over the fixture bank.

The tool's HTTP calls go through a Transport, so the same route sequence it sends a scratch server
is sent here to the fixture world. A rating the student gave is told apart from the unsure that
close_session sweeps onto an unrated attempt by attempts.confidence_source, so a tool that skipped
the confidence route would still leave every attempt rated and has to be caught by the source.
"""
import json
from argparse import Namespace
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.session import service
from tests.api.conftest import ITEM_OPTIONS, KEY_MATHJSON, build_world, load_fixture
from tools.seed_history_student import seed

USERNAME = "walk_history"
PASSWORD = "walk history passphrase"
LAST_DAY = date(2026, 3, 10)
DAYS = 2


class ClientTransport:
   def __init__(self, client):
      self.client = client

   def request(self, method, path, body=None, params=None):
      response = self.client.request(method, path, json=body, params=params)

      return response.status_code, response.text


def write_fixture_content(root):
   directory = root / "items_fixture"
   directory.mkdir(parents=True)

   for record in load_fixture()["archetypes"]:
      for index in range(3):
         item_id = f"{record['id']}-V{index:02d}"
         item = {
            "id": item_id,
            "options": ITEM_OPTIONS,
            "answer_key": {"form": "symbolic", "mathjson": KEY_MATHJSON},
         }
         (directory / f"{item_id}.json").write_text(json.dumps(item))

   return root


def test_two_days_of_history_leave_a_closed_rated_session_each_day(tmp_path):
   world = build_world(tmp_path)
   content_root = write_fixture_content(tmp_path / "content")
   options = Namespace(
      username=USERNAME,
      password=PASSWORD,
      days=DAYS,
      accuracy=1.0,
      seed=7,
      content_root=content_root,
      skip_diagnostic_units={3},
   )
   lines = []

   seed(ClientTransport(world.client()), options, last_day=LAST_DAY, out=lines.append)

   with OrmSession(world.engine) as db:
      users = db.scalars(select(models.User)).all()
      learning_sessions = db.scalars(select(models.Session).where(models.Session.mode == "learning")).all()
      learning_ids = [row.id for row in learning_sessions]
      attempts = db.scalars(select(models.Attempt).where(models.Attempt.session_id.in_(learning_ids))).all()

   closed_days = {
      datetime.fromisoformat(row.started_at).date()
      for row in learning_sessions
      if row.ended_at is not None
   }
   rated_by_student = [
      attempt
      for attempt in attempts
      if attempt.confidence is not None and attempt.confidence_source == service.CONFIDENCE_FROM_STUDENT
   ]
   rating_attempts = [attempt for attempt in attempts if service.collects_confidence(attempt.served_stage)]

   assert [user.username for user in users] == [USERNAME]
   assert closed_days == {date(2026, 3, 9), LAST_DAY}
   assert len(attempts) > 0
   assert len(rated_by_student) == len(rating_attempts)
