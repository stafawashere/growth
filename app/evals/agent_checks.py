"""The deterministic checks on a live tutor reply, shared by the output screen and the eval
(docs/agent/architecture.md, Streaming end to end and Evals; docs/agent/research/math-tutoring.md,
Multi-turn eval checks and Style rules for AP scoring language).

Each check is a pure function of the text, a facts mapping and, for the leak check, the item's key
forms, and returns a Verdict. The facts mapping carries mode, turn_index (0 for the first agent
turn on the item), rules (the path step strings and the BC-PT name the packet holds, since the
packet carries no key_ideas text by the architecture's allow-list) and ids (every library and lesson
id the packet holds). facts_from_packet builds it from a composed
packet, and the eval builds the same mapping from a golden case, so a check that holds in the eval
is the check that runs on the student's screen.

The key forms are built from the item record the harness holds even though the model never does:
the key's decimal to three places, its rational form, its LaTeX, its SymPy expression compared with
every side of every \\( \\) and \\[ \\] span that parses, every decimal or fraction written in plain
text compared numerically, and for an MCQ the key letter in the forms a sentence would use to name
it and the key option's rendered value. Integers written in plain text are not compared, because a
restated stem is full of them; inside a math span they are.

Two phrasings are carved out of the praise list because they are mathematics, not praise:
"perfect square" and the factorial sign inside a math span.
"""
import json
import math
import re
from dataclasses import dataclass

import sympy

from app.grading.latex import read_side, split_sides
from app.items.mathjson import to_sympy
from app.items.verify import equivalence

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)

PRACTICE = "practice"
AFTER_SUBMISSION = "after_submission"
BROWSING = "browsing"
PER_ITEM_TURN_CEILING = 3

NO_ANSWER_BEFORE_SUBMISSION = "no_answer_before_submission"
ASKS_BEFORE_TELLS = "asks_before_tells"
NAMES_RULE = "names_rule"
NO_STUDY_ADVICE = "no_study_advice"
NO_PREDICTION_TALK = "no_prediction_talk"
NO_PRAISE = "no_praise"
NO_DASH = "no_dash"
CITES_REAL_ID = "cites_real_id"
TURNS_WITHIN_CEILING = "turns_within_ceiling"

CHECKS = (
   NO_ANSWER_BEFORE_SUBMISSION,
   ASKS_BEFORE_TELLS,
   NAMES_RULE,
   NO_STUDY_ADVICE,
   NO_PREDICTION_TALK,
   NO_PRAISE,
   NO_DASH,
   CITES_REAL_ID,
   TURNS_WITHIN_CEILING,
)

STUDY_ADVICE_PHRASES = (
   "study",
   "review this",
   "practice more",
   "tonight",
   "before the exam",
   "each day",
   "every day",
   "schedule",
   "minutes a day",
   "plan",
)
PREDICTION_PHRASES = (
   "will be on the exam",
   "likely to appear",
   "always tested",
   "expect this",
   "the exam will",
   "shows up every year",
)
PRAISE_PHRASES = (
   "great",
   "nice",
   "good job",
   "well done",
   "excellent",
   "awesome",
   "perfect",
   "you got this",
   "oops",
   "amazing",
   "brilliant",
   "fantastic",
)
PRAISE_EXCEPTIONS = (re.compile(r"\bperfect\s+squares?\b", re.IGNORECASE),)

ID_PATTERN = re.compile(r"\b(?:BC|LSN)-[A-Z]+-[0-9A-Z]+(?:-[0-9A-Z]+)*(?:#[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)?")
MATH_SPAN = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.DOTALL)
PLAIN_DECIMAL = re.compile(r"(?<![\w.])-?\d+\.\d+(?!\d|\.\d)")
PLAIN_FRACTION = re.compile(r"(?<![\w./])(-?\d+)\s*/\s*(\d+)(?![\w/]|\.\d)")
NUMERIC_TOLERANCE = 0.0005


@dataclass(frozen=True)
class Verdict:
   passed: bool
   check: str
   reason: str


@dataclass(frozen=True)
class KeyForms:
   """What would give the key away, precomputed once per item so each sentence is cheap to check."""

   expression: object = None
   text_patterns: tuple = ()
   letter_patterns: tuple = ()
   literal_texts: tuple = ()


def _passed(check):
   return Verdict(True, check, "")


def _failed(check, reason):
   return Verdict(False, check, reason)


def _phrase_pattern(phrase):
   return re.compile(r"(?<![A-Za-z])" + re.escape(phrase) + r"(?![A-Za-z])", re.IGNORECASE)


def outside_math(text):
   return MATH_SPAN.sub(" ", text)


def math_spans(text):
   return [inline if inline else display for inline, display in MATH_SPAN.findall(text)]


def _decoded(value):
   is_encoded = isinstance(value, str)

   return json.loads(value) if is_encoded else value


def _field(record, name):
   has_attribute = hasattr(record, name) and not isinstance(record, dict)

   if has_attribute:
      return getattr(record, name)

   return record.get(name)


def _numeric_value(expression):
   if expression is None:
      return None

   has_symbols = bool(getattr(expression, "free_symbols", set()))

   if has_symbols:
      return None

   try:
      value = complex(sympy.N(expression))
   except (TypeError, ValueError):
      return None

   is_real = abs(value.imag) < 1e-12 and math.isfinite(value.real)

   return value.real if is_real else None


def _number_pattern(value):
   rounded = f"{value:.3f}"
   whole, _point, fraction = rounded.partition(".")
   fraction_stem = fraction.rstrip("0")
   has_fraction = fraction_stem != ""

   if has_fraction:
      decimal = re.escape(f"{whole}.{fraction_stem}") + r"0*"
   else:
      decimal = re.escape(f"{whole}.") + r"0+"

   return re.compile(r"(?<![\d.])" + decimal + r"(?!\d)")


def _rational_pattern(expression):
   is_rational = isinstance(expression, sympy.Rational) and not isinstance(expression, sympy.Integer)

   if not is_rational:
      return None

   return re.compile(
      r"(?<![\d./])" + re.escape(str(expression.p)) + r"\s*/\s*" + re.escape(str(expression.q)) + r"(?![\d])"
   )


def _letter_patterns(letter):
   named = [
      re.compile(r"\(\s*" + letter + r"\s*\)"),
      re.compile(r"\b(?i:option|choice)\s+\(?" + letter + r"\b"),
      re.compile(r"\b(?i:answer)\s+is\s+\(?" + letter + r"\b"),
      re.compile(r"\b" + letter + r"\s+(?:is|was|looks|seems)\s+(?:right|correct|the)\b"),
   ]
   is_article_letter = letter in ("A", "I")

   if is_article_letter:
      bare = re.compile(r"(?<![A-Za-z0-9\\'])" + letter + r"(?![A-Za-z0-9'])(?!\s+[a-z])")
   else:
      bare = re.compile(r"(?<![A-Za-z0-9\\'])" + letter + r"(?![A-Za-z0-9'])")

   return tuple(named + [bare])


def _expression_of(mathjson):
   if mathjson is None:
      return None

   try:
      return to_sympy(mathjson)
   except Exception:
      return None


def _has_distinct_latex(expression):
   """An integer or a float is left to the numeric comparisons, because its LaTeX is a digit string
   that also sits inside unrelated numbers."""
   if expression is None:
      return False

   is_plain_number = isinstance(expression, (sympy.Integer, sympy.Float))

   return not is_plain_number


def key_forms(item):
   """The key forms of a bank item or an items row. The item never reaches the model; this is the
   harness's copy, held by the screen and the eval."""
   answer_key = _decoded(_field(item, "answer_key")) or {}
   options = _decoded(_field(item, "options")) or []
   key_mathjson = answer_key.get("mathjson")

   if key_mathjson is None:
      key_mathjson = answer_key.get("numeric")

   key_option = next((option for option in options if option.get("is_key")), None)
   has_key_option = key_option is not None

   falls_back_to_option = key_mathjson is None and has_key_option

   if falls_back_to_option:
      key_mathjson = key_option.get("value")

   expression = _expression_of(key_mathjson)
   text_patterns = []
   literal_texts = []
   value = _numeric_value(expression)

   if value is not None:
      text_patterns.append(_number_pattern(value))

   rational = _rational_pattern(expression)

   if rational is not None:
      text_patterns.append(rational)

   if _has_distinct_latex(expression):
      literal_texts.append(sympy.latex(expression))

   letter_patterns = ()

   if has_key_option:
      letter_patterns = _letter_patterns(key_option["id"])
      label = key_option.get("label")
      has_label = isinstance(label, str) and label.strip() != ""

      if has_label:
         literal_texts.append(label.strip())

      option_expression = _expression_of(key_option.get("value"))

      if _has_distinct_latex(option_expression):
         literal_texts.append(sympy.latex(option_expression))

   return KeyForms(
      expression=expression,
      text_patterns=tuple(text_patterns),
      letter_patterns=letter_patterns,
      literal_texts=tuple(dict.fromkeys(literal_texts)),
   )


def _compact(text):
   return re.sub(r"\s+", "", text)


def _equals_key(candidate, key_expression, key_value):
   candidate_value = _numeric_value(candidate)
   both_numeric = candidate_value is not None and key_value is not None

   if both_numeric:
      return abs(candidate_value - key_value) <= NUMERIC_TOLERANCE

   either_numeric = candidate_value is not None or key_value is not None

   if either_numeric:
      return False

   try:
      return equivalence(candidate, key_expression) == "equivalent"
   except Exception:
      return False


def _readable_sides(span):
   """Each side of a chain of equalities read on its own, so one side the parser cannot read, such
   as h'(2), does not hide the value on the other."""
   try:
      sides, bindings = split_sides(span)
   except Exception:
      return []

   readable = []

   for side in sides:
      try:
         readable.append(read_side(side, bindings))
      except Exception:
         continue

   return readable


def _span_names_key(span, key_expression, key_value):
   return any(_equals_key(side, key_expression, key_value) for side in _readable_sides(span))


def _plain_numbers(text):
   numbers = [float(token) for token in PLAIN_DECIMAL.findall(text)]

   for numerator, denominator in PLAIN_FRACTION.findall(text):
      has_denominator = int(denominator) != 0

      if has_denominator:
         numbers.append(int(numerator) / int(denominator))

   return numbers


def no_answer_before_submission(text, facts, forms):
   check = NO_ANSWER_BEFORE_SUBMISSION
   is_practice = facts.get("mode") == PRACTICE
   has_forms = forms is not None
   applies = is_practice and has_forms

   if not applies:
      return _passed(check)

   prose = outside_math(text)
   compact_text = _compact(text)

   for pattern in forms.text_patterns:
      if pattern.search(text):
         return _failed(check, "the key's numeric form appears")

   for literal in forms.literal_texts:
      compact_literal = _compact(literal)
      is_meaningful = len(compact_literal) > 1
      is_present = is_meaningful and compact_literal in compact_text

      if is_present:
         return _failed(check, "the key's rendered form appears")

   for pattern in forms.letter_patterns:
      if pattern.search(prose):
         return _failed(check, "the key option's letter appears")

   key_value = _numeric_value(forms.expression)

   if key_value is not None:
      for number in _plain_numbers(prose):
         if abs(number - key_value) <= NUMERIC_TOLERANCE:
            return _failed(check, "a number equal to the key appears")

   if forms.expression is not None:
      for span in math_spans(text):
         if _span_names_key(span, forms.expression, key_value):
            return _failed(check, "a math span equals the key")

   return _passed(check)


def _names_a_rule(text, facts):
   lowered = " ".join(text.lower().split())

   for rule in facts.get("rules") or ():
      normalised_rule = " ".join(str(rule).lower().split())
      is_named = normalised_rule != "" and normalised_rule in lowered

      if is_named:
         return True

   return False


def names_rule(text, facts, _forms=None):
   if _names_a_rule(text, facts):
      return _passed(NAMES_RULE)

   return _failed(NAMES_RULE, "no path step, key idea or point name from the packet appears")


def asks_before_tells(text, facts, _forms=None):
   check = ASKS_BEFORE_TELLS
   is_first_practice_turn = facts.get("mode") == PRACTICE and facts.get("turn_index", 0) == 0

   if not is_first_practice_turn:
      return _passed(check)

   has_question = "?" in outside_math(text)

   if not has_question:
      return _failed(check, "the first turn on the item asks no question")

   if _names_a_rule(text, facts):
      return _failed(check, "the first turn on the item names the rule")

   return _passed(check)


def _phrase_check(check, phrases, text, exceptions=()):
   prose = outside_math(text)

   for exception in exceptions:
      prose = exception.sub(" ", prose)

   for phrase in phrases:
      if _phrase_pattern(phrase).search(prose):
         return _failed(check, f"contains {phrase!r}")

   return _passed(check)


def no_study_advice(text, _facts=None, _forms=None):
   return _phrase_check(NO_STUDY_ADVICE, STUDY_ADVICE_PHRASES, text)


def no_prediction_talk(text, _facts=None, _forms=None):
   return _phrase_check(NO_PREDICTION_TALK, PREDICTION_PHRASES, text)


def no_praise(text, _facts=None, _forms=None):
   has_exclamation = "!" in outside_math(text)

   if has_exclamation:
      return _failed(NO_PRAISE, "contains an exclamation mark")

   return _phrase_check(NO_PRAISE, PRAISE_PHRASES, text, PRAISE_EXCEPTIONS)


def no_dash(text, _facts=None, _forms=None):
   has_dash = EM_DASH in text or EN_DASH in text

   if has_dash:
      return _failed(NO_DASH, "contains an en or em dash")

   return _passed(NO_DASH)


def cited_ids(text):
   return [token.rstrip("-") for token in ID_PATTERN.findall(text)]


def cites_real_id(text, facts, _forms=None):
   known = set(facts.get("ids") or ())

   for token in cited_ids(text):
      is_known = token in known

      if not is_known:
         return _failed(CITES_REAL_ID, f"{token} is not in this turn's packet")

   return _passed(CITES_REAL_ID)


def turns_within_ceiling(_text, facts, _forms=None):
   is_practice = facts.get("mode") == PRACTICE
   is_past_ceiling = is_practice and facts.get("turn_index", 0) >= PER_ITEM_TURN_CEILING

   if is_past_ceiling:
      return _failed(TURNS_WITHIN_CEILING, "past the per-item ceiling of 3 turns")

   return _passed(TURNS_WITHIN_CEILING)


CHECK_FUNCTIONS = {
   NO_ANSWER_BEFORE_SUBMISSION: no_answer_before_submission,
   ASKS_BEFORE_TELLS: asks_before_tells,
   NAMES_RULE: names_rule,
   NO_STUDY_ADVICE: no_study_advice,
   NO_PREDICTION_TALK: no_prediction_talk,
   NO_PRAISE: no_praise,
   NO_DASH: no_dash,
   CITES_REAL_ID: cites_real_id,
   TURNS_WITHIN_CEILING: turns_within_ceiling,
}

SENTENCE_CHECKS = (
   NO_ANSWER_BEFORE_SUBMISSION,
   NO_STUDY_ADVICE,
   NO_PREDICTION_TALK,
   NO_PRAISE,
   NO_DASH,
   CITES_REAL_ID,
)

EVERY_TURN_CHECKS = (NO_STUDY_ADVICE, NO_PREDICTION_TALK, NO_PRAISE, NO_DASH, CITES_REAL_ID)


def applicable_checks(mode, turn_index):
   """The checks a whole reply is scored on in this mode and turn. names_rule is a
   conversation-level check during practice (at least one turn by the ceiling), so it is scored per
   reply only after submission."""
   if mode == PRACTICE:
      first_turn_checks = (ASKS_BEFORE_TELLS,) if turn_index == 0 else ()

      return (NO_ANSWER_BEFORE_SUBMISSION,) + first_turn_checks + EVERY_TURN_CHECKS + (TURNS_WITHIN_CEILING,)

   if mode == AFTER_SUBMISSION:
      return (NAMES_RULE,) + EVERY_TURN_CHECKS

   if mode == BROWSING:
      return EVERY_TURN_CHECKS

   raise ValueError(f"unknown mode {mode!r}")


def run_checks(text, facts, forms, checks):
   return [CHECK_FUNCTIONS[check](text, facts, forms) for check in checks]


def score_reply(text, facts, forms):
   return run_checks(text, facts, forms, applicable_checks(facts["mode"], facts.get("turn_index", 0)))


def packet_ids(body):
   found = set(cited_ids(json.dumps(body, sort_keys=True)))
   lesson_ids = {token.split("#", 1)[0] for token in found if token.startswith("LSN-")}

   return found | lesson_ids


def packet_rules(body):
   rules = list((body.get("archetype") or {}).get("expected_solution_path") or [])
   point = (body.get("feedback") or {}).get("point") or {}
   has_point_name = bool(point.get("name"))

   if has_point_name:
      rules.append(point["name"])

   return tuple(rules)


def facts_from_packet(packet, turn_index=None):
   """The facts mapping for a composed Packet (app/agent/context.py)."""
   return {
      "mode": packet.mode,
      "turn_index": packet.turn_index if turn_index is None else turn_index,
      "rules": packet_rules(packet.body),
      "ids": tuple(sorted(packet_ids(packet.body))),
   }
