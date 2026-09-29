"""Machine-checkable question standards from docs/pedagogy/today/question-standards.md section 12,
as lints over one item record, plus the two statistics that only make sense over a whole bank.

Each lint takes a record and returns a list of violation strings, empty when the record meets
the standard. None of them repeats a check app/items/ingest.py or app/items/distractor_paths.py
already makes: a missing error_path, an option that equals the key and an option value that does
not convert are theirs, and a lint here skips what they already fail rather than failing it twice.

tools/check_items.py enforces DEFAULT_LINTS on every run and the rest only under --standards.
DEFAULT_LINTS holds the lints tests/fixtures/items_p1 met on 2026-09-29, because that fixture is
what tests/tools/test_operator_clis.py requires the plain run to pass.
"""
import re
from collections import Counter
from decimal import Decimal, InvalidOperation

import sympy

from app.items.ingest import distractor_options, is_statement_record, key_options
from app.items.mathjson import UnsupportedMathJSON, to_sympy

DEFAULT_OPTION_COUNT = 4
STEM_WORD_CAP = 110
CALCULATOR_KEY_DECIMALS = 3

KEY_SHARE_CAP = 0.40
LONGEST_KEY_SHARE_CAP = 0.40
BANK_STATISTIC_MINIMUM = 40

COMMAND_VERBS = (
   "find",
   "evaluate",
   "determine",
   "write",
   "interpret",
   "justify",
   "approximate",
   "estimate",
   "explain",
   "what is",
   "which",
   "compute",
   "use",
   "show",
)

THREE_DECIMALS_PATTERN = re.compile(
   r"\b(three|3)\s+decimal\s+places?\b|\b(three|3)\s+decimals\b|\bthird\s+decimal\s+place\b|\bnearest\s+thousandth\b",
   re.IGNORECASE,
)

CHOICE_WORDING_PATTERNS = (
   ("which of the following", re.compile(r"\bwhich\s+of\s+the\s+following\b", re.IGNORECASE)),
   ("which of these", re.compile(r"\bwhich\s+of\s+these\b", re.IGNORECASE)),
   ("which statement", re.compile(r"\bwhich\s+statement\b", re.IGNORECASE)),
   ("the options or choices", re.compile(r"\b(options|choices|answer\s+choices)\b", re.IGNORECASE)),
   ("an option letter", re.compile(r"\b(option|choice)\s+\(?[A-E]\)?(?![A-Za-z])")),
   ("listed below", re.compile(r"\blisted\s+below\b", re.IGNORECASE)),
)

COMPOSITE_OPTION_PATTERN = re.compile(r"\b(all|none)\s+of\s+the\s+above\b", re.IGNORECASE)

CONVERSION_ERRORS = (UnsupportedMathJSON, TypeError, ValueError, AttributeError)


def option_label(option):
   stated = option.get("id")

   if stated is None:
      return "with no id"

   return stated


def option_count(record):
   options = record.get("options") or []
   is_mcq = record.get("format") == "mcq"
   carries_options = len(options) > 0
   is_subject = is_mcq or carries_options

   if not is_subject:
      return []

   stored_count = record.get("option_count")
   stores_a_count = stored_count is not None
   expected = stored_count if stores_a_count else DEFAULT_OPTION_COUNT
   source = "the option_count stored on the record" if stores_a_count else "the default"
   count_matches = len(options) == expected

   if count_matches:
      return []

   return [f"carries {len(options)} options where {source} is {expected}"]


def distinct_error_paths(record):
   labels_by_path = {}

   for option in distractor_options(record):
      path = option.get("error_path")
      names_a_path = path is not None

      if names_a_path:
         labels_by_path.setdefault(path, []).append(option_label(option))

   violations = []

   for path, labels in labels_by_path.items():
      is_shared = len(labels) > 1

      if is_shared:
         violations.append(f"distractors {', '.join(labels)} share error_path {path}")

   return violations


def convert_option_value(value):
   try:
      return to_sympy(value)
   except CONVERSION_ERRORS:
      return None


def value_kind(expression):
   if isinstance(expression, sympy.Set):
      return "set"

   if isinstance(expression, sympy.core.relational.Relational):
      return "relation"

   if isinstance(expression, (sympy.Tuple, tuple, list)):
      return "tuple"

   is_plain_expression = isinstance(expression, sympy.Expr)

   if not is_plain_expression:
      return type(expression).__name__

   has_free_symbols = len(expression.free_symbols) > 0

   if has_free_symbols:
      return "expression"

   return "number"


def free_symbol_names(expression):
   symbols = getattr(expression, "free_symbols", set())

   return {str(symbol) for symbol in symbols}


def key_value_source(record):
   keys = key_options(record)
   has_one_key_option = len(keys) == 1

   if has_one_key_option:
      return keys[0].get("value")

   return (record.get("answer_key") or {}).get("mathjson")


def unconvertible_value_options(record):
   """Labels of the options value_option_type had to skip because their value does not convert.
   distractor_paths already fails such a record, so the skip is reported, not failed again.
   """
   is_value_item = not is_statement_record(record)

   if not is_value_item:
      return []

   options = record.get("options") or []

   return [
      option_label(option)
      for option in options
      if convert_option_value(option.get("value")) is None
   ]


def value_option_type(record):
   is_value_item = not is_statement_record(record)
   options = record.get("options") or []
   has_options = len(options) > 0

   has_value_options = is_value_item and has_options

   if not has_value_options:
      return []

   key = convert_option_value(key_value_source(record))
   key_converted = key is not None

   if not key_converted:
      return []

   key_kind = value_kind(key)
   key_symbols = free_symbol_names(key)
   skipped = unconvertible_value_options(record)
   skip_note = f" (options {', '.join(skipped)} skipped, their value does not convert)" if skipped else ""
   violations = []

   for option in distractor_options(record):
      expression = convert_option_value(option.get("value"))
      was_skipped = expression is None

      if was_skipped:
         continue

      label = option_label(option)
      kind = value_kind(expression)
      kind_differs = kind != key_kind
      extra_symbols = sorted(free_symbol_names(expression) - key_symbols)
      has_extra_symbols = len(extra_symbols) > 0

      if kind_differs:
         violations.append(f"option {label} is a {kind} where the key is a {key_kind}{skip_note}")

      if has_extra_symbols:
         violations.append(
            f"option {label} contains free symbol {', '.join(extra_symbols)} the key does not{skip_note}"
         )

   return violations


def decimal_places(value):
   """Digits after the decimal point as the record stores them, or None when the value is not
   a stored decimal. A float is read through repr, so 5.700 stored as a JSON number reads 5.7,
   and only the MathJSON object {"num": "5.700"} keeps the trailing zeros.
   """
   is_float = isinstance(value, float)
   is_number_object = isinstance(value, dict) and isinstance(value.get("num"), str)

   if is_float:
      text = repr(value)
   elif is_number_object:
      text = value["num"]
   else:
      return None

   try:
      exponent = Decimal(text).as_tuple().exponent
   except InvalidOperation:
      return None

   is_finite = isinstance(exponent, int)

   if not is_finite:
      return None

   return max(0, -exponent)


def calculator_decimals(record):
   """A calculator item is in scope when its stem asks for a decimal answer, meaning it matches
   THREE_DECIMALS_PATTERN ("three decimal places", "3 decimal places", "three decimals", "third
   decimal place" or "nearest thousandth", case-insensitive), or when answer_key.mathjson is stored
   as a decimal. An item that asks for an exact value and keeps an exact key (an integer, a
   Rational, a symbolic expression) is out of scope. In scope, the stem must ask for three decimal
   places and the key must be stored as a decimal with at least three places, both as
   answer_key.mathjson and as the key option's value. Every violation names which case fired.
   """
   is_calculator_item = record.get("calculator_status") == "calculator"
   is_value_item = not is_statement_record(record)

   is_calculator_value_item = is_calculator_item and is_value_item

   if not is_calculator_value_item:
      return []

   stored_key = (record.get("answer_key") or {}).get("mathjson")
   stem_text = (record.get("stem") or {}).get("text") or ""

   stem_asks_for_decimals = THREE_DECIMALS_PATTERN.search(stem_text) is not None
   key_is_stored_decimal = decimal_places(stored_key) is not None

   is_in_scope = stem_asks_for_decimals or key_is_stored_decimal

   if not is_in_scope:
      return []

   if stem_asks_for_decimals:
      reason = "stem asks for three decimal places"
   else:
      reason = "key is stored as a decimal"

   violations = []

   if not stem_asks_for_decimals:
      violations.append(f"{reason}: calculator stem does not ask for three decimal places or the nearest thousandth")

   stored_values = [("answer_key.mathjson", stored_key)]
   keys = key_options(record)

   has_one_key_option = len(keys) == 1

   if has_one_key_option:
      stored_values.append((f"key option {option_label(keys[0])}", keys[0].get("value")))

   for place, value in stored_values:
      places = decimal_places(value)
      is_stored_as_decimal = places is not None
      has_enough_places = is_stored_as_decimal and places >= CALCULATOR_KEY_DECIMALS

      if has_enough_places:
         continue

      if is_stored_as_decimal:
         violations.append(
            f"{reason}: {place} stores {value!r}, {places} decimal places where {CALCULATOR_KEY_DECIMALS} are needed"
         )
      else:
         violations.append(f"{reason}: {place} stores {value!r}, which is not a decimal to {CALCULATOR_KEY_DECIMALS} places")

   return violations


def choice_worded_short_answer(record):
   is_short_answer = record.get("format") == "short_answer"

   if not is_short_answer:
      return []

   stem_text = (record.get("stem") or {}).get("text") or ""
   matched = [name for name, pattern in CHOICE_WORDING_PATTERNS if pattern.search(stem_text)]

   if not matched:
      return []

   return [f"short_answer stem is worded as a choice: {', '.join(matched)}"]


def command_verb_source(record):
   """How the stem carries its command: "field" when stem.command_verb is set, else the first
   verb of COMMAND_VERBS found in the text as a whole word, else None.
   """
   stem = record.get("stem") or {}
   stated_verb = stem.get("command_verb")
   has_field = isinstance(stated_verb, str) and stated_verb.strip() != ""

   if has_field:
      return "field"

   stem_text = stem.get("text") or ""

   for verb in COMMAND_VERBS:
      verb_pattern = r"\b" + r"\s+".join(verb.split()) + r"\b"
      found = re.search(verb_pattern, stem_text, re.IGNORECASE) is not None

      if found:
         return f"text:{verb}"

   return None


def command_verb(record):
   source = command_verb_source(record)

   if source is not None:
      return []

   return ["stem carries no command_verb field and its text contains none of the command verbs"]


def stem_word_count(record):
   """Whitespace-separated tokens of stem.text, inline LaTeX included, figure excluded."""
   stem_text = (record.get("stem") or {}).get("text") or ""

   return len(stem_text.split())


def stem_length(record):
   words = stem_word_count(record)
   is_too_long = words > STEM_WORD_CAP

   if not is_too_long:
      return []

   return [f"stem has {words} words, over the cap of {STEM_WORD_CAP}"]


def distractor_provenance(record):
   bare = []

   for option in distractor_options(record):
      has_derivation = bool(option.get("derivation"))
      has_mechanism = bool(option.get("mechanism"))
      carries_either = has_derivation or has_mechanism

      if not carries_either:
         bare.append(option_label(option))

   if not bare:
      return []

   return [f"distractors {', '.join(bare)} carry neither derivation nor mechanism"]


def option_texts(option):
   texts = []

   for field in ("label", "text", "value"):
      stated = option.get(field)

      if isinstance(stated, str):
         texts.append(stated)

   return texts


def no_all_none(record):
   violations = []

   for option in record.get("options") or []:
      for text in option_texts(option):
         match = COMPOSITE_OPTION_PATTERN.search(text)

         if match:
            violations.append(f"option {option_label(option)} reads {match.group(0)!r}")

   return violations


LINTS = {
   "option_count": option_count,
   "distinct_error_paths": distinct_error_paths,
   "value_option_type": value_option_type,
   "calculator_decimals": calculator_decimals,
   "choice_worded_short_answer": choice_worded_short_answer,
   "command_verb": command_verb,
   "stem_length": stem_length,
   "distractor_provenance": distractor_provenance,
   "no_all_none": no_all_none,
}

DEFAULT_LINTS = (
   "calculator_decimals",
   "choice_worded_short_answer",
   "command_verb",
   "stem_length",
   "no_all_none",
)

MODE_DEFAULT = "default"
MODE_STANDARDS = "standards"


def lints_for_mode(mode):
   if mode == MODE_STANDARDS:
      return tuple(LINTS)

   if mode == MODE_DEFAULT:
      return DEFAULT_LINTS

   raise ValueError(f"unknown standards mode {mode!r}")


def all_lint_findings(record):
   return {name: lint(record) for name, lint in LINTS.items()}


def standards_violations(record, snapshot, mode):
   """The violations of the lints the mode enforces, keyed by lint name, only lints that found
   something. snapshot is taken so a lint that needs the content library can be added without
   changing callers; none of the current lints reads it.
   """
   violations = {}

   for name in lints_for_mode(mode):
      found = LINTS[name](record)

      if found:
         violations[name] = found

   return violations


def key_letter_distribution(records):
   letters = Counter()

   for record in records:
      keys = key_options(record)
      has_one_key = len(keys) == 1

      if has_one_key:
         letters[option_label(keys[0])] += 1

   total = sum(letters.values())
   letter_count = len(letters)
   chi_square = None

   can_compare_letters = total > 0 and letter_count > 1

   if can_compare_letters:
      expected = total / letter_count
      chi_square = sum((count - expected) ** 2 / expected for count in letters.values())

   top_share = max(letters.values()) / total if total else 0.0
   has_enough_items = total >= BANK_STATISTIC_MINIMUM
   is_flagged = has_enough_items and top_share > KEY_SHARE_CAP

   return {
      "counts": dict(sorted(letters.items())),
      "total": total,
      "chi_square": chi_square,
      "degrees_of_freedom": max(letter_count - 1, 0),
      "top_share": top_share,
      "flagged": is_flagged,
   }


def normalised_label(option):
   return " ".join((option.get("label") or "").split())


def statement_key_is_longest(record):
   options = record.get("options") or []
   keys = key_options(record)
   has_one_key = len(keys) == 1

   has_labelled_options = has_one_key and len(options) > 0

   if not has_labelled_options:
      return None

   key_length = len(normalised_label(keys[0]))
   longest = max(len(normalised_label(option)) for option in options)

   return key_length == longest


def statement_longest_key_share(records):
   """Share of statement items whose key label is the longest option label, ties included,
   measured in characters after collapsing whitespace.
   """
   measured = 0
   longest = 0

   for record in records:
      if not is_statement_record(record):
         continue

      is_longest = statement_key_is_longest(record)

      if is_longest is None:
         continue

      measured += 1

      if is_longest:
         longest += 1

   share = longest / measured if measured else 0.0
   has_enough_items = measured >= BANK_STATISTIC_MINIMUM
   is_flagged = has_enough_items and share > LONGEST_KEY_SHARE_CAP

   return {"statement_items": measured, "key_longest": longest, "share": share, "flagged": is_flagged}
