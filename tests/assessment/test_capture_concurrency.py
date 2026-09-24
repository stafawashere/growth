"""A mock's capture step reads the next page while an earlier question is still grading. SQLite
admits one writer, so the diagnostician's model call, the slowest step of grading, must run while
no write transaction is open (app/grading/service.py observe_lost_points)."""
import sqlite3

from app.providers.base import Provider
from tests.assessment.conftest import publish_generated_items, session_part
from tools import frq_scenarios


class LockProbe(Provider):
   """Answers no role; when the diagnostician is called it checks, from a second connection,
   whether the database would take a writer right now."""

   def __init__(self, database_path):
      self.database_path = database_path
      self.writer_free_during_diagnosis = []

   def generate(self, request):
      is_diagnosis = request.role == "diagnostician"

      if is_diagnosis:
         connection = sqlite3.connect(self.database_path, timeout=0.2)

         try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("ROLLBACK")
            self.writer_free_during_diagnosis.append(True)
         except sqlite3.OperationalError:
            self.writer_free_during_diagnosis.append(False)
         finally:
            connection.close()

      raise RuntimeError(f"no answer for {request.role}")

   def stream(self, request):
      raise NotImplementedError


def wrong_work(record):
   return {
      "parts": [
         {"part_id": part["id"], "lines": [{"kind": "math", "content": "x = 12345", "crossed_out": False, "outside_box": False}], "answer": "12345"}
         for part in record["parts"]
      ],
      "unreadable": [],
   }


def test_no_write_lock_is_held_while_the_diagnostician_runs(tmp_path, monkeypatch):
   """The provider is handed over unguarded: on the subscription the guard writes nothing to the
   database for a paced call, and this test is about what grading itself holds open."""
   from app.api.routes import frq

   database_path = tmp_path / "growth.db"
   application = frq_scenarios.build(database_path, None)
   probe = LockProbe(str(database_path))
   application.state.settings.ai_provider = probe
   monkeypatch.setattr(frq, "guarded_provider", lambda settings, db, user_id: settings.ai_provider)
   publish_generated_items(application)
   client = frq_scenarios.client_for(application)
   frq_scenarios.register(client)

   drill = client.post("/drills", json={"part": "II-B", "capture_mode": "typed"}).json()
   client.post(f"/drills/{drill['id']}/sections/1/start")
   closed = session_part(client.post(f"/drills/{drill['id']}/sections/1/submit").json(), 1)
   capture = closed["capture"][0]
   record = application.state.settings.frq.record(capture["item_id"])

   typed = client.post(f"/attempts/{capture['attempt_id']}/typed", json={"read_back": wrong_work(record)})

   assert typed.status_code == 200
   assert probe.writer_free_during_diagnosis == [True]
