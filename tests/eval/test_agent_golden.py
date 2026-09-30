"""docs/agent/architecture.md, Evals: the live tutor's multi-turn golden set.

The set validates against its contract. Every candidate reply is scored with the deterministic
checks on the packet the route would compose for that turn: an acceptable turn passes every check
that applies, and an unacceptable turn fails every check its labels mark false. A leaking candidate
written into a practice case fails no_answer_before_submission.

The paired-profile cases (docs/agent/research/self-tuning.md, "The eval that guards it") give the
same verdict on every deterministic check across each pair, the applied field is visible where code
can read it and absent from the baseline reply, the instruction-shaped term is dropped by the
validator without a model call, and wants_answer never reaches a prompt.
"""
import copy
import json
from collections import Counter

import pytest

from app.agent import profile
from app.agent.context import render_prompt
from app.agent.drawing.spec import elements_in_order, shape_of
from app.content.loader import load_snapshot
from app.evals import agent_checks, figure_checks, golden
from app.providers.anthropic import AnthropicProvider
from app.providers.subscription import SubscriptionProvider
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


DETERMINISTIC_FIELDS = ("student_terms", "representation_lead", "turn_length")
EVERY_TURN_ABSENT_FIELDS = ("student_terms", "representation_lead")


@pytest.fixture
def no_model(monkeypatch):
   def refuse(*args, **kwargs):
      raise AssertionError("no model is called while a profile is validated or rendered")

   for provider in (AnthropicProvider, SubscriptionProvider):
      monkeypatch.setattr(provider, "generate", refuse)
      monkeypatch.setattr(provider, "stream", refuse)


def pairs_of(document):
   pairs = {}

   for case in document["cases"]:
      marker = case.get("profile_pair")

      if marker is not None:
         pairs.setdefault(marker["id"], {})[marker["role"]] = case

   return pairs


def adversarial_case(document, field_name):
   return next(
      members["adversarial"]
      for members in pairs_of(document).values()
      if "adversarial" in members and members["adversarial"]["profile_pair"]["field"] == field_name
   )


def test_the_set_holds_six_applied_pairs_and_two_adversarial_pairs(document):
   roles = [set(members) for members in pairs_of(document).values()]

   assert sum(1 for members in roles if members == {"applied", "baseline"}) >= 6
   assert sum(1 for members in roles if members == {"adversarial", "baseline"}) >= 2


def test_every_deterministic_verdict_is_identical_across_a_pair(rows):
   verdicts = {}

   for row in rows:
      if row["pair_id"] is None:
         continue

      verdicts.setdefault((row["pair_id"], row["turn"], row["check"]), []).append(row["passed"])

   unpaired = [key for key, found in verdicts.items() if len(found) != 2]
   split = [key for key, found in verdicts.items() if len(set(found)) != 1]

   assert len(verdicts) > 0
   assert unpaired == []
   assert split == []


def test_the_applied_field_shows_in_the_applied_reply_and_not_in_the_baseline(document, snapshot, library):
   scored = [row for row in golden.agent_profile_verdicts(document, snapshot, library["items"]) if row["passed"] is not None]
   context = golden.agent_context(snapshot)
   baseline_misses = {}

   for members in pairs_of(document).values():
      applied = members.get("applied")
      has_deterministic_field = applied is not None and applied["profile_pair"]["field"] in DETERMINISTIC_FIELDS

      if not has_deterministic_field:
         continue

      field_name = applied["profile_pair"]["field"]

      for index, entry in enumerate(members["baseline"]["turns"]):
         packet = golden.agent_turn_packet(applied, index, context, library["items"])
         verdict = agent_checks.profile_applied(entry["candidate_reply"], packet.profile, field_name)
         baseline_misses.setdefault((applied["profile_pair"]["id"], field_name), []).append(not verdict.passed)

   assert len(scored) >= 18
   assert all(row["passed"] == row["label"] for row in scored)
   assert len(baseline_misses) >= 6
   assert all(any(misses) for misses in baseline_misses.values())
   assert all(all(misses) for (_pair, field_name), misses in baseline_misses.items() if field_name in EVERY_TURN_ABSENT_FIELDS)


def test_an_instruction_shaped_term_is_dropped_by_the_validator_with_no_model_call(document, snapshot, library, no_model):
   case = adversarial_case(document, "student_terms")
   offered = case["profile"]["student_terms"]
   context = golden.agent_context(snapshot)
   packets = [golden.agent_turn_packet(case, index, context, library["items"]) for index in range(len(case["turns"]))]

   assert len(offered) == 1
   assert profile.validated_terms(offered, profile.active_concept_ids(snapshot)) == []
   assert all(packet.profile["student_terms"] == [] for packet in packets)
   assert all(offered[0]["term"] not in json.dumps(packet.profile) for packet in packets)


def test_wants_answer_is_never_rendered_into_a_prompt(document, snapshot, library, no_model):
   case = adversarial_case(document, "stated_requests")
   context = golden.agent_context(snapshot)

   assert case["profile"]["stated_requests"] == ["wants_answer"]

   for index, entry in enumerate(case["turns"]):
      packet = golden.agent_turn_packet(case, index, context, library["items"])
      rendered = render_prompt(packet, [], packet.profile, [], entry["student"])

      assert "wants_answer" not in rendered.user
      assert "wants_answer" not in rendered.system
      assert "stated_requests" not in rendered.user
      assert packet.profile is not None


def test_validation_refuses_a_pair_that_differs_in_more_than_its_field(document, library):
   broken = copy.deepcopy(document)
   members = pairs_of(broken)["PAIR-01"]
   members["baseline"]["profile"] = {"turn_length": "short"}
   members["applied"]["turns"][0]["student"] = "Something else entirely?"
   members["applied"]["turns"][1].pop("profile_applied")
   problems = [problem for problem in golden.validate("agent", broken, library) if "PAIR-01" in problem or members["applied"]["id"] in problem]

   assert any("differ in exactly" in problem for problem in problems)
   assert any("student" in problem for problem in problems)
   assert any("profile_applied" in problem for problem in problems)


FIGURE_MINIMUM_TURNS = 14
SHOULD_DRAW = (("name_rule", "secant"), ("discuss_step", "riemann"), ("explain", "slope_field"), ("explain", "triangle"))
CLOSED_MOVES = ("ask_what_tried", "probe")
LEAK_CHANNELS = (
   "a marked coordinate",
   "a line's slope or intercept",
   "the key option's letter",
   "an area",
   "an approximation total",
)
REFUSAL_REASONS = ("malformed", "oversized")
OPEN_PRACTICE_TURNS = (1, 2)


@pytest.fixture(scope="module")
def figure_turns(document, snapshot, library):
   context = golden.agent_context(snapshot)
   found = []

   for case in document["cases"]:
      for index, entry in enumerate(case["turns"]):
         split = golden.agent_split_reply(entry["candidate_reply"])

         if not split.opens_figure:
            continue

         packet = golden.agent_turn_packet(case, index, context, library["items"])
         source = golden.agent_figure_reading(split).source
         elements = elements_in_order(source) if source is not None else []
         found.append({
            "case_id": case["id"],
            "turn": index,
            "move": packet.move,
            "entry": entry,
            "shapes": {shape_of(element) for _step_id, element in elements},
         })

   return found


def failing_figure_rows(rows, check):
   return [row for row in rows if row["check"] == check and not row["label"]]


def is_open_practice_turn(row):
   is_practice = row["mode"] == "practice"
   is_open_turn = row["turn"] in OPEN_PRACTICE_TURNS

   return is_practice and is_open_turn


def test_every_figure_label_agrees_with_its_check(rows):
   figure_rows = [row for row in rows if row["check"] in golden.FIGURE_CHECKS]
   disagreeing = [(row["case_id"], row["turn"], row["check"]) for row in figure_rows if row["label"] != row["passed"]]

   assert {row["check"] for row in figure_rows} == set(golden.FIGURE_CHECKS)
   assert disagreeing == []


def test_the_figure_turns_cover_every_drawing_channel(figure_turns, rows):
   drawn_well = {
      (turn["move"], shape)
      for turn in figure_turns
      if turn["entry"]["acceptable"]
      for shape in turn["shapes"]
   }
   drawn_when_closed = {turn["move"] for turn in figure_turns if turn["entry"]["labels"]["draws_only_when_open"] is False}
   leaks = failing_figure_rows(rows, figure_checks.NO_ANSWER_IN_FIGURE)
   refusals = {row["reason"] for row in failing_figure_rows(rows, figure_checks.FIGURE_WELL_FORMED)}
   misplaced_leaks = [(row["case_id"], row["turn"]) for row in leaks if not is_open_practice_turn(row)]

   assert len(figure_turns) >= FIGURE_MINIMUM_TURNS
   assert set(SHOULD_DRAW) <= drawn_well
   assert set(CLOSED_MOVES) <= drawn_when_closed
   assert misplaced_leaks == []
   assert set(REFUSAL_REASONS) <= refusals

   for channel in LEAK_CHANNELS:
      assert any(channel in row["reason"] for row in leaks), channel


def test_a_leaking_figure_relabelled_acceptable_disagrees_with_its_check(document, snapshot, library):
   leaking = [
      (case, index)
      for case in document["cases"]
      for index, entry in enumerate(case["turns"])
      if entry["labels"].get(figure_checks.NO_ANSWER_IN_FIGURE) is False
   ]

   assert len(leaking) >= len(LEAK_CHANNELS)

   for case, index in leaking:
      mutated = copy.deepcopy(case)
      entry = mutated["turns"][index]
      entry["labels"][figure_checks.NO_ANSWER_IN_FIGURE] = True
      entry["acceptable"] = all(entry["labels"].values())
      mutated_rows = golden.agent_verdicts({"cases": [mutated]}, snapshot, library["items"])
      disagreeing = [(row["turn"], row["check"]) for row in agent_eval.disagreements(mutated_rows)]

      assert entry["acceptable"] is True, case["id"]
      assert disagreeing == [(index, figure_checks.NO_ANSWER_IN_FIGURE)], case["id"]


def test_validation_refuses_figure_labels_that_break_the_contract(document, library):
   broken = copy.deepcopy(document)
   cases = {case["id"]: case for case in broken["cases"]}
   cases["GLD-AGT-045"]["turns"][1]["labels"].pop(figure_checks.NO_ANSWER_IN_FIGURE)
   cases["GLD-AGT-045"]["turns"][0]["labels"][figure_checks.FIGURE_DESCRIBED] = True
   cases["GLD-AGT-046"]["turns"][1]["labels"]["figure_is_pretty"] = True
   cases["GLD-AGT-050"]["diagnosis"]["misconception_hypotheses"][0]["id"] = "BC-MIS-02011"
   problems = golden.validate("agent", broken, library)

   assert any("GLD-AGT-045 turn 1" in problem and "no_answer_in_figure" in problem for problem in problems)
   assert any("GLD-AGT-045 turn 0" in problem and "draws nothing" in problem for problem in problems)
   assert any("GLD-AGT-046 turn 1" in problem and "figure_is_pretty" in problem for problem in problems)
   assert any("GLD-AGT-050" in problem and "BC-MIS-02011" in problem for problem in problems)
