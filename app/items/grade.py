"""Deterministic grading of one submitted answer against the stored items row.

Scope items 5 and 7 of docs/plan/11-phased-delivery.md give P1 no diagnostician and no model
grader, so the three facts app/engine/update.py rule_based_mastery_states reads (R12) are decided
here: whether the response is correct, whether it is equivalent but mis-notated, and which skills
an incorrect MCQ distractor blames. The MCQ comparison is the one in 03's "MCQ grading"; the short
answer comparison is check 1 of 03's deterministic pre-checks with check 2 as the numeric fallback.
Check 4 asks for units present and dimensionally correct. Units declared on the key and absent
from the response, or the key's own unit written differently, meaning an SI conversion factor of
exactly 1 between them, are the only mechanical notation failure the plan supplies for P1. The
value is compared without converting units, so any other unit, in the same dimension or not,
fails the check itself and the answer is incorrect rather than mis-notated. Unit symbols are
case-sensitive, as SI symbols are, and only a spelled-out unit name is read without regard to
case. A physical constant is not a unit, and units that name no known unit leave the check
unsettled.

An unsettled comparison and an unparseable submission both leave correct as None with a reason.
03 is explicit that an unsettled check falls through rather than defaulting to earned or not
earned, and nothing here scores a parse failure or a timeout against the student. The same holds
for a comparison that raises, and because SymPy's message quotes the student's expression, the
reason names only the exception type. A bounded child that dies before sending a result
is the one exception that is raised rather than folded in, because it says nothing about the
answer, and recording it as ungraded would keep the student from ever submitting that answer again.

Parsing, the symbolic comparison and the numeric fallback each run under app/items/verify.py's
bound, so one grade call runs at most three of them.
"""
import json
import re

from sympy import Integer, simplify
from sympy.physics import units as sympy_units
from sympy.physics.units.prefixes import PREFIXES
from sympy.physics.units.quantities import PhysicalConstant, Quantity
from sympy.physics.units.systems.si import SI, dimsys_SI

from app.engine.state import ResponseFormat
from app.items.mathjson import UnsupportedMathJSON, to_sympy
from app.items.verify import (
   COMPARISON_TIMEOUT_S,
   ChildDiedError,
   equivalence,
   numeric_check,
   run_bounded,
)

DEFAULT_DECIMALS = 3

UNIT_SPELLINGS_SYMPY_LACKS = {
   "sec": "second",
   "secs": "seconds",
   "min": "minute",
   "mins": "minutes",
   "hr": "hour",
   "hrs": "hours",
}

UNIT_TOKEN = re.compile(r"\s*(?:(\*\*|[*/^()])|(\d+)|([A-Za-z]+))")


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
      parsed = run_bounded(
         _parsed_pair, (key_mathjson, submitted_mathjson), COMPARISON_TIMEOUT_S, None
      )
   except UnsupportedMathJSON as failure:
      return _ungraded(f"the submission could not be parsed: {failure}")
   except ChildDiedError:
      raise
   except Exception as failure:
      return _ungraded(f"parsing the submission raised {type(failure).__name__}")

   parse_did_not_finish = parsed is None

   if parse_did_not_finish:
      return _ungraded("parsing the submission did not finish within the bound")

   key_expression, submitted_expression = parsed

   try:
      comparison = equivalence(key_expression, submitted_expression)
   except ChildDiedError:
      raise
   except Exception as failure:
      return _ungraded(f"the symbolic comparison raised {type(failure).__name__}")

   is_equivalent = comparison == "equivalent"

   if is_equivalent:
      return _value_matched(answer_key, submission)

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

   try:
      agrees = numeric_check(
         key_expression, submitted_expression, rel_tol=0.0, abs_floor=tolerance
      )
   except ChildDiedError:
      raise
   except Exception as failure:
      return _ungraded(f"the numeric comparison raised {type(failure).__name__}")

   if agrees is True:
      return _value_matched(answer_key, submission)

   if agrees is False:
      return _result(correct=False)

   return _ungraded(f"the numeric comparison to {decimals} decimal places did not settle")


def _parsed_pair(key_mathjson, submitted_mathjson):
   return to_sympy(key_mathjson), to_sympy(submitted_mathjson)


def _value_matched(answer_key, submission):
   verdict = _units_verdict(answer_key.get("units"), submission.get("units"))

   if verdict == "unsettled":
      return _ungraded("the submitted units name no unit the dimension check knows")

   if verdict == "wrong_unit":
      return _result(correct=False)

   return _result(correct=True, equivalent_but_misnotated=verdict == "notation")


def _units_verdict(key_units, submitted_units):
   """Check 4 of 03's deterministic pre-checks, and the only notation check P1 can run."""
   normalised_key = _normalised_units(key_units)
   normalised_submission = _normalised_units(submitted_units)
   key_declares_units = normalised_key != ""

   if not key_declares_units:
      return "match"

   written_identically = normalised_submission == normalised_key

   if written_identically:
      return "match"

   units_are_absent = normalised_submission == ""

   if units_are_absent:
      return "notation"

   key_expression = _unit_expression(key_units)
   submitted_expression = _unit_expression(submitted_units)
   unreadable_as_written = submitted_expression is None
   same_letters_in_another_case = normalised_submission.casefold() == normalised_key.casefold()
   is_the_key_in_another_case = unreadable_as_written and same_letters_in_another_case

   if is_the_key_in_another_case:
      return "match"

   either_is_unknown = key_expression is None or submitted_expression is None

   if either_is_unknown:
      return "unsettled"

   same_dimension = _dimension_of(key_expression) == _dimension_of(submitted_expression)
   conversion_factor = simplify(_scale_of(submitted_expression) / _scale_of(key_expression))
   is_same_unit = same_dimension and conversion_factor == 1

   return "notation" if is_same_unit else "wrong_unit"


def _unit_expression(units):
   try:
      tokens = _unit_tokens(str(units))
      expression, position = _unit_product(tokens, 0)
   except ValueError:
      return None

   consumed_everything = position == len(tokens)

   if not consumed_everything:
      return None

   return expression


def _dimension_of(expression):
   dimensional_expression = SI.get_dimensional_expr(expression)

   return dimsys_SI.get_dimensional_dependencies(dimensional_expression)


def _scale_of(expression):
   factors = {
      quantity: SI.get_quantity_scale_factor(quantity)
      for quantity in expression.atoms(Quantity)
   }

   return expression.subs(factors)


def _unit_tokens(text):
   spelled_with_per = re.sub(r"\bper\b", "/", text, flags=re.IGNORECASE)
   tokens = []
   position = 0
   stripped_end = len(spelled_with_per.rstrip())

   while position < stripped_end:
      match = UNIT_TOKEN.match(spelled_with_per, position)

      if match is None:
         raise ValueError(f"unexpected character at {position}")

      operator, digits, name = match.groups()

      if operator is not None:
         tokens.append(("op", "^" if operator == "**" else operator))
      elif digits is not None:
         tokens.append(("int", int(digits)))
      else:
         tokens.append(("unit", _quantity_named(name)))

      position = match.end()

   return tokens


def _quantity_named(name):
   """A symbol as written, then a prefixed symbol, then a spelled-out name in any case."""
   exact = _unit_attribute(name) or _unit_attribute(UNIT_SPELLINGS_SYMPY_LACKS.get(name))

   if exact is not None:
      return exact

   prefixed = _prefixed_symbol(name)

   if prefixed is not None:
      return prefixed

   folded = name.casefold()
   spelled = _unit_attribute(folded) or _unit_attribute(UNIT_SPELLINGS_SYMPY_LACKS.get(folded))
   is_spelled_out = spelled is not None and folded != str(spelled.abbrev)

   if is_spelled_out:
      return spelled

   raise ValueError(f"{name} is not a unit")


def _unit_attribute(name):
   is_absent = not name

   if is_absent:
      return None

   quantity = getattr(sympy_units, name, None)
   is_unit = isinstance(quantity, Quantity) and not isinstance(quantity, PhysicalConstant)

   return quantity if is_unit else None


def _prefixed_symbol(name):
   for prefix_symbol, prefix in PREFIXES.items():
      starts_with_prefix = name.startswith(prefix_symbol) and len(name) > len(prefix_symbol)

      if not starts_with_prefix:
         continue

      unit_symbol = name[len(prefix_symbol):]
      quantity = _unit_attribute(unit_symbol)
      is_symbol = quantity is not None and unit_symbol == str(quantity.abbrev)

      if is_symbol:
         return prefix.scale_factor * quantity

   return None


def _unit_product(tokens, position):
   product, position = _unit_power(tokens, position)

   while position < len(tokens):
      kind, value = tokens[position]
      is_division = (kind, value) == ("op", "/")
      is_explicit_product = (kind, value) == ("op", "*")
      starts_implicit_product = kind == "unit" or (kind, value) == ("op", "(")
      continues_product = is_division or is_explicit_product or starts_implicit_product

      if not continues_product:
         break

      if is_division or is_explicit_product:
         position += 1

      factor, position = _unit_power(tokens, position)
      product = product / factor if is_division else product * factor

   return product, position


def _unit_power(tokens, position):
   base, position = _unit_atom(tokens, position)
   has_exponent = position < len(tokens) and tokens[position] == ("op", "^")

   if not has_exponent:
      return base, position

   exponent_is_present = position + 1 < len(tokens) and tokens[position + 1][0] == "int"

   if not exponent_is_present:
      raise ValueError("an exponent must be a whole number")

   return base ** Integer(tokens[position + 1][1]), position + 2


def _unit_atom(tokens, position):
   is_past_end = position >= len(tokens)

   if is_past_end:
      raise ValueError("units end early")

   kind, value = tokens[position]

   if kind == "unit":
      return value, position + 1

   opens_group = (kind, value) == ("op", "(")

   if not opens_group:
      raise ValueError(f"unexpected {value}")

   inner, position = _unit_product(tokens, position + 1)
   closes_group = position < len(tokens) and tokens[position] == ("op", ")")

   if not closes_group:
      raise ValueError("unclosed parenthesis")

   return inner, position + 1


def _normalised_units(units):
   is_absent = units is None

   if is_absent:
      return ""

   return " ".join(str(units).split())


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
