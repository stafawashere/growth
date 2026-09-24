"""The golden sets for every model role (11 P7 scope item 1) and the measures they are scored with."""
import copy
from pathlib import Path

import pytest

from app.content.loader import load_snapshot
from app.evals import golden
from app.runtime.context import DEFAULT_CONTENT_ROOT

RECORD_PATH = Path(__file__).resolve().parents[2] / "docs" / "operator" / "golden-sets.md"
STRUCTURAL_DEFECTS = ("none", "wrong_key", "distractor_equals_key", "duplicate_distractors", "unresolvable_error_path")


@pytest.fixture(scope="module")
def library():
   return golden.load_library()


@pytest.mark.parametrize("role", golden.ROLES)
def test_every_golden_set_validates(role, library):
   document = golden.load_set(role)

   assert len(document["cases"]) > 0
   assert golden.validate(role, document, library) == []


def test_validation_refuses_a_set_that_breaks_its_contract(library):
   grader = copy.deepcopy(golden.load_set("grader"))
   grader["labelled_by"] = "the operator"
   grader["cases"] = [case for case in grader["cases"] if case["category"] != "narrow_fail"]
   tutor = copy.deepcopy(golden.load_set("tutor"))
   flipped = next(case for case in tutor["cases"] if case["acceptable"])
   flipped["labels"]["reveals_final_answer"] = True
   generator = copy.deepcopy(golden.load_set("generator"))
   generator["cases"][0]["answer_key"] = {"form": "symbolic", "mathjson": 12345}

   grader_problems = golden.validate("grader", grader, library)
   tutor_problems = golden.validate("tutor", tutor, library)
   generator_problems = golden.validate("generator", generator, library)

   assert any("labelled_by" in problem for problem in grader_problems)
   assert any("do not cover all five" in problem for problem in grader_problems)
   assert any(flipped["id"] in problem for problem in tutor_problems)
   assert any("frozen key" in problem for problem in generator_problems)


def test_kappa_and_exact_match_on_a_known_table():
   reference = {"a": True, "b": True, "c": False, "d": False}
   predicted = {"a": True, "b": False, "c": False, "d": False, "z": True}
   measured = golden.agreement(reference, predicted)

   assert (measured.compared, measured.exact) == (4, 3)
   assert measured.kappa == pytest.approx(0.5)
   assert measured.kappa_low < 0.5 < measured.kappa_high


def test_the_deterministic_verifier_keeps_catching_every_structural_defect():
   verifier = golden.load_set("verifier")
   snapshot = load_snapshot(DEFAULT_CONTENT_ROOT)
   detection = golden.detection_by_defect(verifier, golden.deterministic_verifier_verdicts(verifier, snapshot))

   for defect in STRUCTURAL_DEFECTS:
      caught, total = detection[defect]
      assert caught == total > 0, defect


def test_the_record_names_every_role_and_the_delegation():
   record = RECORD_PATH.read_text()

   for role in golden.ROLES:
      assert f"| {role} |" in record

   assert "on the operator's delegation of 2026-09-24" in record
   assert "None is a human's work" in record
