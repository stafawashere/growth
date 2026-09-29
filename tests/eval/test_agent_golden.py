"""docs/agent/architecture.md, Evals: the live tutor's multi-turn golden set.

The set validates against its contract. Every candidate reply is scored with the deterministic
checks on the packet the route would compose for that turn: an acceptable turn passes every check
that applies, and an unacceptable turn fails every check its labels mark false. A leaking candidate
written into a practice case fails no_answer_before_submission.
"""
import copy
from collections import Counter

import pytest

from app.content.loader import load_snapshot
from app.evals import agent_checks, golden
from app.runtime.context import DEFAULT_CONTENT_ROOT
from tools import agent_eval

MINIMUM_CASES = 24
PRESSURE_PATTERNS = (
   "asks for the answer",
   "asks whether work in progress is right",
   "claims permission",
   "a correct objection and an incorrect one",
   "asks for study advice",
   "asks what will be on the exam",
)


@pytest.fixture(scope="module")
def library():
   return golden.load_library()


@pytest.fixture(scope="module")
def document():
   return golden.load_set("agent")


@pytest.fixture(scope="module")
def snapshot():
   return load_snapshot(DEFAULT_CONTENT_ROOT)


@pytest.fixture(scope="module")
def rows(document, snapshot, library):
   return golden.agent_verdicts(document, snapshot, library["items"])


def test_the_set_validates_and_covers_every_mode_and_pressure(document, library):
   modes = Counter(case["mode"] for case in document["cases"])
   pressures = {case["pressure"] for case in document["cases"]}
   turns = [entry for case in document["cases"] for entry in case["turns"]]
   unacceptable = [entry for entry in turns if not entry["acceptable"]]

   assert golden.validate("agent", document, library) == []
   assert len(document["cases"]) >= MINIMUM_CASES
   assert set(modes) == {"practice", "after_submission", "browsing"}
   assert set(PRESSURE_PATTERNS) <= pressures
   assert 0.35 <= len(unacceptable) / len(turns) <= 0.65

   for case in document["cases"]:
      assert 3 <= len(case["turns"]) <= 6, case["id"]


def test_every_acceptable_turn_passes_every_applicable_check(rows):
   failing = [row for row in rows if row["acceptable"] and not row["passed"]]

   assert len(rows) > 0
   assert failing == []


def test_every_unacceptable_turn_fails_the_checks_its_labels_name(rows):
   named = [row for row in rows if not row["label"]]
   missed = [row for row in named if row["passed"]]

   assert len(named) > 0
   assert missed == []
   assert agent_eval.disagreements(rows) == []


def test_a_deliberately_leaking_candidate_fails_no_answer_before_submission(document, snapshot, library):
   case = copy.deepcopy(next(case for case in document["cases"] if case["item_id"] == "ITM-AGT-06002-00" and case["mode"] == "practice"))
   leaking = "What did you try? Either way the trapezoidal sum is \\( \\frac{145}{2} \\)."
   case["turns"][0]["candidate_reply"] = leaking
   context = golden.agent_context(snapshot)
   packet = golden.agent_turn_packet(case, 0, context, library["items"])
   facts = agent_checks.facts_from_packet(packet, 0)
   verdict = agent_checks.no_answer_before_submission(leaking, facts, agent_checks.key_forms(library["items"][case["item_id"]]))

   assert verdict.passed is False


def test_validation_refuses_a_case_that_breaks_the_contract(document, library):
   broken = copy.deepcopy(document)
   first = broken["cases"][0]
   first["screen"]["draft"] = "72.5"
   second = broken["cases"][1]
   second["turns"][0]["labels"].pop("no_praise")
   third = broken["cases"][2]
   third["item_id"] = "ITM-NOT-00000-00"
   problems = golden.validate("agent", broken, library)

   assert any(first["id"] in problem for problem in problems)
   assert any(second["id"] in problem and "no_praise" in problem for problem in problems)
   assert any(third["id"] in problem and "bank" in problem for problem in problems)


def test_the_live_flag_makes_no_call(capsys):
   assert agent_eval.main(["--live"]) == 2
   assert "orchestrator" in capsys.readouterr().out
