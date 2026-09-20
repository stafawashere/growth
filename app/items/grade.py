"""Deterministic grading of one submitted answer against the stored items row.

Scope items 5 and 7 of docs/plan/11-phased-delivery.md give P1 no diagnostician and no model
grader, so the three facts app/engine/update.py rule_based_mastery_states reads (R12) are decided
here: whether the response is correct, whether it is equivalent but mis-notated, and which skills
an incorrect MCQ distractor blames. The MCQ comparison is the one in 03's "MCQ grading"; the short
answer comparison is check 1 of 03's deterministic pre-checks with check 2 as the numeric fallback.
Check 4, units declared on the key and absent from or different in the response, is the only
mechanical notation check the plan supplies for P1, so it is the only one implemented.

An unsettled comparison and an unparseable submission both leave correct as None with a reason.
03 is explicit that an unsettled check falls through rather than defaulting to earned or not
earned, and nothing here scores a parse failure or a timeout against the student.
"""
import json

from app.engine.state import ResponseFormat
from app.items.mathjson import UnsupportedMathJSON, to_sympy
from app.items.verify import equivalence, numeric_check

DEFAULT_DECIMALS = 3


def grade(item, submission, errors, served_format=None):
   """served_format is attempts.format, which R16 and R29 set per attempt rather than per item.

   Every published item may carry options and still be served as a MathLive short answer, so the
   format decides the path whenever the caller knows it. With no format the path is read off the
   item and the submission, which is what a caller holding only the row can do.
   """
   submission = submission or {}
   options = _item_options(item)
   selected_option_id = submission.get("selected_option_id")
   submitted_mathjson = submission.get("mathjson")

   was_served_as = _format_name(served_format, options, selected_option_id)
   is_unknown_format = was_served_as is None

   if is_unknown_format:
      return _ungraded(f"served format {served_format} is not a response format")

   graded_as_mcq = was_served_as == ResponseFormat.MCQ.value
   format_was_stated = served_format is not None

   if graded_as_mcq:
      no_option_was_named = selected_option_id is None
      an_expression_arrived = submitted_mathjson is not None
      contradicts_mcq = format_was_stated and no_option_was_named and an_expression_arrived

      if contradicts_mcq:
         return _ungraded("an expression was submitted for an item served as mcq")

      return _grade_mcq(options, selected_option_id, _item_skills(item), errors)

   no_expression_arrived = submitted_mathjson is None
   an_option_was_named = selected_option_id is not None
   contradicts_short_answer = format_was_stated and no_expression_arrived and an_option_was_named

   if contradicts_short_answer:
      return _ungraded("an option id was submitted for an item served as short_answer")

   return _grade_short_answer(_answer_key(item), submission)


def _format_name(served_format, options, selected_option_id):
   is_enum_member = isinstance(served_format, ResponseFormat)

   if is_enum_member:
      return served_format.value

   was_stated = served_format is not None

   if was_stated:
      known = [member.value for member in ResponseFormat]
      is_known = served_format in known

      return served_format if is_known else None

   item_carries_options = len(options) > 0
   an_option_was_named = selected_option_id is not None
   looks_like_mcq = item_carries_options or an_option_was_named

   if looks_like_mcq:
      return ResponseFormat.MCQ.value

   return ResponseFormat.SHORT_ANSWER.value


def _grade_mcq(options, selected_option_id, loaded_skills, errors):
   has_options = len(options) > 0

   if not has_options:
      return _ungraded("an option id was submitted for an item that carries no options")

   keys = [option for option in options if option.get("is_key") is True]
   key_count_is_wrong = len(keys) != 1

   if key_count_is_wrong:
      return _ungraded(f"the option set names {len(keys)} keys and exactly one is required")

   was_selected = selected_option_id is not None

   if not was_selected:
      return _ungraded("no option id was submitted")

   selected = _option_by_id(options, selected_option_id)
   is_on_the_item = selected is not None

   if not is_on_the_item:
      return _ungraded(f"option id {selected_option_id} is not on this item")

   is_key = selected.get("is_key") is True

   if is_key:
      return _result(correct=True)

   error_path = selected.get("error_path")
   blamed_skills = _error_path_skills(error_path, loaded_skills, errors)

   return _result(correct=False, error_path=error_path, error_path_skills=blamed_skills)


def _error_path_skills(error_path, loaded_skills, errors):
   has_path = error_path is not None

   if not has_path:
      return []

   record = (errors or {}).get(error_path)
   is_resolvable = record is not None

   if not is_resolvable:
      return []

   named = record.get("skills") or []
   item_loads_nothing = len(loaded_skills) == 0

   if item_loads_nothing:
      return list(named)

   return [skill for skill in named if skill in loaded_skills]


def _grade_short_answer(answer_key, submission):
   has_key = answer_key is not None

   if not has_key:
      return _ungraded("the item carries no answer key")

   submitted_mathjson = submission.get("mathjson")
   was_submitted = submitted_mathjson is not None

   if not was_submitted:
      return _ungraded("the submission carries no MathJSON")

   key_mathjson = _key_mathjson(answer_key)
   key_is_expressible = key_mathjson is not None

   if not key_is_expressible:
      return _ungraded("the answer key carries no MathJSON to compare against")

   try:
      key_expression = to_sympy(key_mathjson)
      submitted_expression = to_sympy(submitted_mathjson)
   except UnsupportedMathJSON as failure:
      return _ungraded(f"the submission could not be parsed: {failure}")

   comparison = equivalence(key_expression, submitted_expression)
   is_equivalent = comparison == "equivalent"

   if is_equivalent:
      return _result(correct=True, equivalent_but_misnotated=_misnotated(answer_key, submission))

   key_is_numeric = answer_key.get("form") == "numeric"

   if key_is_numeric:
      return _grade_numeric(answer_key, submission, key_expression, submitted_expression)

   is_not_equivalent = comparison == "not_equivalent"

   if is_not_equivalent:
      return _result(correct=False)

   return _ungraded("the symbolic comparison did not settle")


def _grade_numeric(answer_key, submission, key_expression, submitted_expression):
   decimals = answer_key.get("decimals") or DEFAULT_DECIMALS
   tolerance = 0.5 * 10 ** (-decimals)
   agrees = numeric_check(
      key_expression, submitted_expression, rel_tol=0.0, abs_floor=tolerance
   )

   if agrees is True:
      return _result(correct=True, equivalent_but_misnotated=_misnotated(answer_key, submission))

   if agrees is False:
      return _result(correct=False)

   return _ungraded(f"the numeric comparison to {decimals} decimal places did not settle")


def _misnotated(answer_key, submission):
   """Check 4 of 03's deterministic pre-checks, and the only notation check P1 can run."""
   key_units = _normalised_units(answer_key.get("units"))
   key_declares_units = key_units != ""

   if not key_declares_units:
      return False

   return _normalised_units(submission.get("units")) != key_units


def _normalised_units(units):
   is_absent = units is None

   if is_absent:
      return ""

   return " ".join(str(units).split()).casefold()


def _option_by_id(options, option_id):
   for option in options:
      if option.get("id") == option_id:
         return option

   return None


def _result(correct, equivalent_but_misnotated=False, error_path=None, error_path_skills=None):
   return {
      "correct": correct,
      "equivalent_but_misnotated": equivalent_but_misnotated,
      "error_path": error_path,
      "error_path_skills": list(error_path_skills or []),
      "reason": None,
   }


def _ungraded(reason):
   return {
      "correct": None,
      "equivalent_but_misnotated": False,
      "error_path": None,
      "error_path_skills": [],
      "reason": reason,
   }


def _field(item, name):
   has_attribute = hasattr(item, name)

   if has_attribute:
      return getattr(item, name)

   return item.get(name) if hasattr(item, "get") else None


def _decoded(value):
   is_absent = value is None

   if is_absent:
      return None

   is_encoded = isinstance(value, str)

   if is_encoded:
      return json.loads(value)

   return value


def _item_options(item):
   return _decoded(_field(item, "options")) or []


def _answer_key(item):
   return _decoded(_field(item, "answer_key"))


def _item_skills(item):
   return _decoded(_field(item, "skills")) or []


def _key_mathjson(answer_key):
   has_mathjson = answer_key.get("mathjson") is not None

   if has_mathjson:
      return answer_key["mathjson"]

   return answer_key.get("numeric")
