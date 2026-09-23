"""Tests for app/items/distractor_paths.py, the property gate 30 (eval_p1_distractor_paths)
checks over an MCQ record: docs/plan/11-phased-delivery.md P1 items 17 and 30,
docs/plan/04-item-generation.md "Output schema".
"""
import copy
import json
import re
from pathlib import Path

import pytest

from app.content.loader import load_snapshot
from app.items import verify
from app.items.distractor_paths import distractor_path_violations, error_ids_for_skills
from app.items.ingest import distractor_options, key_options
from app.items.mathjson import to_sympy

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = REPO_ROOT / "data"
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "items_p1"
P1_ARCHETYPE_SOURCE = REPO_ROOT / "tools" / "build_p1_fixture.py"


@pytest.fixture(scope="module")
def snapshot():
   return load_snapshot(DATA_ROOT)


@pytest.fixture(scope="module")
def p1_error_ids(snapshot):
   return error_ids_for_skills(snapshot, p1_skill_ids(snapshot))


def p1_archetype_ids():
   source = P1_ARCHETYPE_SOURCE.read_text()
   block = re.search(r"P1_ARCHETYPES = \[(.*?)\]", source, re.DOTALL)
   found_the_list = block is not None

   if not found_the_list:
      raise AssertionError(f"no P1_ARCHETYPES list found in {P1_ARCHETYPE_SOURCE}")

   return re.findall(r"BC-QA-\d+", block.group(1))


def p1_skill_ids(snapshot):
   skill_ids = set()

   for archetype_id in p1_archetype_ids():
      skill_ids.update(snapshot.archetypes[archetype_id]["skills"])

   return frozenset(skill_ids)


def fixture_record(name):
   return json.loads((FIXTURE_DIR / f"{name}.json").read_text())


def clean_record():
   return copy.deepcopy(fixture_record("ITM-SYN-01008-00"))


def option_by_id(record, option_id):
   matches = [option for option in record["options"] if option["id"] == option_id]

   return matches[0]


def test_a_clean_mcq_record_has_no_violations(p1_error_ids):
   record = clean_record()

   assert distractor_path_violations(record, p1_error_ids) == []


def test_a_null_error_path_is_a_violation(p1_error_ids):
   record = clean_record()
   option_by_id(record, "B")["error_path"] = None

   violations = distractor_path_violations(record, p1_error_ids)
   mentions_the_option = [text for text in violations if "B" in text]

   assert len(violations) == 1
   assert len(mentions_the_option) == 1
   assert "error_path" in violations[0]


def test_an_error_path_outside_the_skills_error_set_is_a_violation(snapshot, p1_error_ids):
   outside_ids = sorted(set(snapshot.errors) - set(p1_error_ids))
   has_an_outside_id = len(outside_ids) > 0

   assert has_an_outside_id

   outside_id = outside_ids[0]
   record = clean_record()
   option_by_id(record, "B")["error_path"] = outside_id

   violations = distractor_path_violations(record, p1_error_ids)

   assert len(violations) == 1
   assert outside_id in violations[0]


def test_a_distractor_equal_to_the_key_is_a_violation(p1_error_ids):
   record = clean_record()
   key_value = option_by_id(record, "A")["value"]
   option_by_id(record, "B")["value"] = key_value

   violations = distractor_path_violations(record, p1_error_ids)
   mentions_the_key = [text for text in violations if "key" in text]

   assert len(mentions_the_key) == 1
   assert "B" in mentions_the_key[0]


def test_two_distractors_equal_to_each_other_is_a_violation(p1_error_ids):
   record = clean_record()
   option_by_id(record, "C")["value"] = option_by_id(record, "B")["value"]

   violations = distractor_path_violations(record, p1_error_ids)
   mentions_both = [text for text in violations if "B" in text and "C" in text]

   assert len(violations) == 1
   assert len(mentions_both) == 1


def test_a_record_with_no_options_has_no_violations(p1_error_ids):
   record = clean_record()
   record.pop("options")

   assert distractor_path_violations(record, p1_error_ids) == []
   assert distractor_path_violations({"options": []}, p1_error_ids) == []


def test_the_error_set_is_read_from_the_snapshot_and_not_hand_listed(snapshot):
   skill_ids = p1_skill_ids(snapshot)
   expected = set()

   for error_id, error in snapshot.errors.items():
      holds_a_p1_skill = len(set(error.get("skills") or []) & skill_ids) > 0

      if holds_a_p1_skill:
         expected.add(error_id)

   computed = error_ids_for_skills(snapshot, skill_ids)

   assert isinstance(computed, frozenset)
   assert set(computed) == expected
   assert len(computed) > 0

   archetype_ids = p1_archetype_ids()

   for path in sorted(FIXTURE_DIR.glob("*.json")):
      record = json.loads(path.read_text())

      assert record["archetype_id"] in archetype_ids


def test_an_indeterminate_comparison_is_reported_and_never_passes(p1_error_ids):
   record = clean_record()
   option_by_id(record, "B")["value"] = ["Divide", 1, 0]

   violations = distractor_path_violations(record, p1_error_ids)
   mentions_settling = [text for text in violations if "settle" in text]

   assert len(violations) > 0
   assert len(mentions_settling) > 0
   assert "B" in mentions_settling[0]


def key_expression(record):
   return to_sympy(key_options(record)[0]["value"])


def distractor_expressions(record):
   return [to_sympy(option["value"]) for option in distractor_options(record)]


def stated_error_paths(record):
   return [option.get("error_path") for option in distractor_options(record)]


def test_both_callers_read_one_shared_comparison_core(monkeypatch, p1_error_ids):
   """Rejection rules 5 and 6 of 04 are one implementation, so a change to the comparison loops
   reaches gate 30's checker and ingest's distractor_distinct_check together. A forced finding
   stands in for that change and is asserted on both.
   """
   record = clean_record()

   def every_comparison_is_equal(key, distractors):
      return [
         {
            "kind": verify.KEY_COMPARISON,
            "left": None,
            "right": index,
            "comparison": verify.EQUAL,
         }
         for index in range(len(distractors))
      ]

   monkeypatch.setattr(verify, "comparison_findings", every_comparison_is_equal)

   checker_violations = distractor_path_violations(record, p1_error_ids)
   check_violations = verify.distractor_checks(
      key_expression(record),
      distractor_expressions(record),
      stated_error_paths(record),
      p1_error_ids,
   )

   mentions_the_key = [text for text in checker_violations if "equals the key" in text]

   assert len(mentions_the_key) == len(distractor_options(record))
   assert "rule_5" in check_violations


def test_both_callers_read_one_shared_error_path_core(monkeypatch, p1_error_ids):
   """Rejection rule 7 of 04 resolves an error path in one place, and both callers read it."""
   record = clean_record()

   def every_path_is_unresolvable(error_paths, active_error_ids):
      return [
         {"index": index, "reason": verify.UNRESOLVABLE_ERROR_PATH, "error_path": error_path}
         for index, error_path in enumerate(error_paths)
      ]

   monkeypatch.setattr(verify, "error_path_findings", every_path_is_unresolvable)

   checker_violations = distractor_path_violations(record, p1_error_ids)
   check_violations = verify.distractor_checks(
      key_expression(record),
      distractor_expressions(record),
      stated_error_paths(record),
      p1_error_ids,
   )

   mentions_an_error_path = [text for text in checker_violations if "error_path" in text]

   assert len(mentions_an_error_path) == len(distractor_options(record))
   assert "rule_7" in check_violations


def test_the_two_callers_keep_their_different_unsettled_policies(p1_error_ids):
   """The shared core reports a comparison that did not settle and the two callers read it
   differently on purpose: gate 30's checker calls it a violation outright, while the rule-code
   caller hands it back under its own code, which ingest reads as indeterminate and routes to
   review rather than rejecting the item.
   """
   record = clean_record()
   option_by_id(record, "B")["value"] = ["Divide", 1, 0]

   checker_violations = distractor_path_violations(record, p1_error_ids)
   check_violations = verify.distractor_checks(
      key_expression(record),
      distractor_expressions(record),
      stated_error_paths(record),
      p1_error_ids,
   )

   mentions_settling = [text for text in checker_violations if "did not settle" in text]

   assert len(mentions_settling) > 0
   assert verify.UNSETTLED_VIOLATION in check_violations
   assert "rule_5" not in check_violations
   assert "rule_6" not in check_violations