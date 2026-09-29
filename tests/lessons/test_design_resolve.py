"""tools/lesson_design_resolve.py agrees: a statement multiple-choice answer that names its choice in
an "option" field is judged by that field, not by a letter parsed out of the answer sentence."""
from tools.lesson_design_resolve import agrees

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
