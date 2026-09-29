"""tools/lesson_design_resolve.py agrees: a statement multiple-choice answer that names its choice in
an "option" field is judged by that field, not by a letter parsed out of the answer sentence."""
from tools.lesson_design_resolve import agrees, problems_of

KEY = {"form": "statement", "text": "The limit does not exist", "key_option": "C"}


def test_option_field_equal_to_key_agrees():
   answer = {"answer": "The limit does not exist", "option": "(c) "}

   assert agrees(KEY, answer) == (True, "agree (option C)")


def test_option_field_different_from_key_disagrees():
   answer = {"answer": "The limit is 0", "option": "B"}

   assert agrees(KEY, answer) == (False, "disagree (key option C, re-solver option B)")


def test_bare_letter_answer_without_option_field_still_compares():
   assert agrees(KEY, {"answer": "(C)"})[0] is True
   assert agrees(KEY, {"answer": "D"})[0] is False


SET_KEY = {"form": "symbolic", "expr": "FiniteSet(10/3, 8)", "calculator_status": "no_calculator"}
SCALAR_KEY = {"form": "symbolic", "expr": "10/3", "calculator_status": "no_calculator"}


def test_bracketed_list_agrees_with_finite_set_key():
   assert agrees(SET_KEY, {"answer": "[10/3, 8]"})[0] is True
   assert agrees(SET_KEY, {"answer": "{8, 10/3}"})[0] is True
   assert agrees(SET_KEY, {"answer": "10/3, 8"})[0] is True


def test_list_missing_or_changing_a_member_disagrees():
   assert agrees(SET_KEY, {"answer": "[10/3]"})[0] is False
   assert agrees(SET_KEY, {"answer": "[10/3, 7]"})[0] is False


def test_list_against_scalar_key_disagrees():
   assert agrees(SCALAR_KEY, {"answer": "[10/3, 8]"})[0] is False


class StubDesign:
   lesson_id = "LSN-CON-99999"

   def __init__(self, checks):
      self.record = {
         "worked_examples": [
            {"id": "ex-1", "problem": {"text": "Example one problem."}, "answer": {"form": "numeric"}},
            {"id": "ex-2", "problem": {"text": "Example two problem."}, "answer": {"form": "numeric"}},
         ],
         "checks": checks,
      }


def check(check_id, check_kind, stem, **extra):
   return {"id": check_id, "check_kind": check_kind, "stem": {"text": stem}, "key": {"form": "numeric"}, **extra}


def test_extract_adds_example_context_to_dependent_checks():
   design = StubDesign([
      check("chk-1", "completion", "Given F(t) = t^3, find A(3).", completes="ex-1"),
      check("chk-2", "isomorph", "As in the example, with rate 4t. Find A(3)."),
      check("chk-3", "isomorph", "Rate -3t^2 + 6t + 4 tons per hour; 30 tons at t = 1. Amount at t = 3?"),
      check("chk-4", "mcq", "Same f as the worked example. Which gives every inflection point of g?"),
      check("chk-5", "isomorph", "f joins (0, 1), (2, 0), then a semicircle above the axis. Find g(12)."),
   ])
   by_id = {problem["id"]: problem for problem in problems_of(design)}
   completion = by_id["LSN-CON-99999#chk-1"]
   dependent = by_id["LSN-CON-99999#chk-2"]
   independent = by_id["LSN-CON-99999#chk-3"]
   same_function = by_id["LSN-CON-99999#chk-4"]
   figure_above = by_id["LSN-CON-99999#chk-5"]

   assert completion["context"] == "Example one problem."
   assert completion["text"] == "Given F(t) = t^3, find A(3)."
   assert dependent["context"] == "Example one problem."
   assert dependent["text"] == "As in the example, with rate 4t. Find A(3)."
   assert "context" not in independent
   assert same_function["context"] == "Example one problem."
   assert "context" not in figure_above
