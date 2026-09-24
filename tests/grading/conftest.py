"""The free-response application for the integration tests: app/main.py build_application over a
temporary database and the live data/ registries, with the provider replaced by ScriptedProvider.

ScriptedProvider stands at the provider seam, the boundary the grading code calls through, and
answers each role from a script the test sets, recording every request it receives. It never opens
a socket and never starts a process, so these tests are replay-only like the rest of the suite.
"""
import json
from pathlib import Path

import pytest

from app.providers.base import ProviderResult, Usage
from tools import frq_scenarios

REPO_ROOT = Path(__file__).resolve().parents[2]
PAGES = REPO_ROOT / "tests" / "fixtures" / "frq_pages"
ITEM_ID = "FRQ-AGT-05007-01"
UNIT_ID = "BC-UNIT-05"


def line(content, kind="math"):
   return {"kind": kind, "content": content, "crossed_out": False, "outside_box": False}


READ_BACK = {
   "parts": [
      {"part_id": "a", "lines": [line("g'(x) = (x-3)e^{x}"), line("(x-3)e^{x} = 0"), line("x = 3")], "answer": "x = 3"},
      {"part_id": "b", "lines": [line("g' changes from negative to positive at x = 3", "text")], "answer": ""},
   ],
   "unreadable": [],
}


def grading(decision, quote=""):
   return {"decision": decision, "evidence_quote": quote, "rule_field": "earns", "rule_cited": "the clause", "eligibility_note": ""}


class ScriptedProvider:
   name = "scripted"

   def __init__(self):
      self.requests = []
      self.read_back = READ_BACK
      self.grader_answers = {}
      self.default_decision = "earned"

   def roles(self):
      return [request.role for request in self.requests]

   def generate(self, request):
      self.requests.append(request)

      if request.role == "transcriber":
         text = json.dumps(self.read_back)
      elif request.role == "grader":
         point_id = self.point_of(request)
         decisions = self.grader_answers.get(point_id, {})
         text = json.dumps(grading(decisions.get(request.sample_label, self.default_decision)))
      else:
         text = json.dumps({"observed_errors": [], "matched_signals": [], "skill_readings": [], "gap_descriptions_matched": []})

      return ProviderResult(text=text, finish_reason="end_turn", usage=Usage(100, 20, None, None), provider=self.name, model=request.model)

   def stream(self, request):
      yield from ()

   def point_of(self, request):
      content = request.messages[0].content

      for point_id in ("a1", "a2", "b1", "b2"):
         criterion_marker = CRITERIA[point_id]

         if criterion_marker in content:
            return point_id

      return None


CRITERIA = {}


class FrqWorld:
   def __init__(self, application, provider):
      self.application = application
      self.provider = provider
      self.settings = application.state.settings
      self.engine = application.state.engine
      self.client = frq_scenarios.client_for(application)
      self.user_id = frq_scenarios.register(self.client)

   def open_attempt(self, capture_mode="photo", unit_id=UNIT_ID, item_id=ITEM_ID):
      opened = self.client.post("/frq/unit-checks", json={"unit_id": unit_id, "item_id": item_id})
      assert opened.status_code == 200, opened.text
      session_id = opened.json()["session_id"]
      started = self.client.post(f"/sessions/{session_id}/frq/{item_id}/attempts", json={"capture_mode": capture_mode})
      assert started.status_code == 200, started.text

      return started.json()["attempt_id"]

   def upload(self, attempt_id, page_name):
      return self.client.post(f"/attempts/{attempt_id}/images", json=frq_scenarios.photo_payload(PAGES / page_name))


@pytest.fixture
def frq_world(tmp_path):
   provider = ScriptedProvider()
   application = frq_scenarios.build(tmp_path / "growth.db", provider)
   record = application.state.settings.frq.record(ITEM_ID)

   for part in record["parts"]:
      for point in part["points"]:
         CRITERIA[point["point_id"]] = point["criterion"]

   return FrqWorld(application, provider)
