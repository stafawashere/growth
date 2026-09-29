"""Operator command-line check over the Desmos fluency content: the procedure cards under
content/calculator/cards and the template list in content/calculator/templates.json, as
docs/calculator/architecture.md (Content files and the checker) and build-plan.md (Slice 1b)
describe them.

The dash, emoji, praise, study advice, schedule and served-text patterns are imported from
tools/check_lessons.py and the prediction patterns from schemas/common.py. The quote rule is
qa/07_quotes.py's: that module runs its check on import, so its normalisation is taken from
check_lessons.normalise_text, which is the same expression, and its page, raw and OCR haystack is
rebuilt here. Unlike 07_quotes, a partial match is a finding.

Usage: python3 tools/check_calculator.py <directory or card file> [...] [--no-templates]
"""
import importlib
import json
import re
import sys
from decimal import ROUND_DOWN, ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import jsonschema
import sympy
from jsonschema.exceptions import best_match

from tools import check_lessons

SCHEMA_PATH = ROOT / "schemas" / "calculator" / "card.schema.json"
CACHE_TEXT_DIR = ROOT / "cache" / "text"
ERRORS_PATH = ROOT / "data" / "errors.json"
IDS_PATH = ROOT / "data" / "ids.json"
TEMPLATES_FILE = "templates.json"
CARD_SET = "card set"

DRILLED_CAPABILITIES = ("plot", "zero", "derivative", "integral", "intersection", "value")
QUOTE_WORDS_MAX = 25
HABIT_RUN_WORDS = 5
PARTIAL_RUN_WORDS = 4
DRAWS_PER_TEMPLATE = 200
KEY_DIGITS = 20
MIN_NONZERO_DECIMALS = 3
THREE_PLACES = Decimal("0.001")
THREE_PLACE_ANSWER = re.compile(r"^-?\d+\.\d{3}$")
CONTENT_ID = re.compile(r"\b(?:CCD|CDT)-[a-z]+-\d{2}\b")
HYPHENATED_CITATION = re.compile(r"\b[a-z0-9]+(?:-[a-z0-9]+)+:\d+\b")

STYLE_PATTERNS = (
   ("praise", check_lessons.PRAISE),
   ("study advice", check_lessons.STUDY_ADVICE),
   ("schedule", check_lessons.SCHEDULE),
)
SERVED_PATTERNS = (
   ("library id", check_lessons.SERVED_ID),
   ("library id", CONTENT_ID),
   ("citation", check_lessons.SERVED_PAGE),
   ("citation", HYPHENATED_CITATION),
   ("evidence tag", check_lessons.SERVED_TAG),
)


class Context:
   """What the lints read besides the card: the schema, the error registry, the cache and the
   template list that sits beside the cards."""

   def __init__(self, templates, cache_dir=CACHE_TEXT_DIR):
      self.schema = json.loads(SCHEMA_PATH.read_text())
      self.templates = templates
      self.cache_dir = Path(cache_dir)
      self.errors = {record["id"]: record for record in json.loads(ERRORS_PATH.read_text())["errors"]}
      self.ids = json.loads(IDS_PATH.read_text())["ids"]

   def error_is_active(self, error_id):
      registered = self.ids.get(error_id)
      record = self.errors.get(error_id)
      is_registered_active = registered is not None and registered.get("status") == "active"
      is_recorded = record is not None and record.get("status") != "retired"

      return is_registered_active and is_recorded

   def page_files(self, doc, page):
      page_file = self.cache_dir / doc / f"page-{int(page):03d}.txt"

      return [page_file, page_file.with_suffix(".raw.txt"), page_file.with_suffix(".ocr.txt")]

   def page_text(self, doc, page):
      texts = [path.read_text() for path in self.page_files(doc, page) if path.exists()]

      return check_lessons.normalise_text(" ".join(texts))


def student_strings(card):
   """Every string the card screen shows, with a label for the finding."""
   demonstration = card["demonstration"]
   found = [("title", card["title"]), ("task", card["task"]), ("bluebook_note", card["bluebook_note"])]

   for index, step in enumerate(card["steps"]):
      found.append((f"steps/{index}/text", step["text"]))
      found.append((f"steps/{index}/keys", step["keys"]))

   found.append(("demonstration/function_tex", demonstration["function_tex"]))
   found.append(("demonstration/setup_latex", demonstration["setup_latex"]))
   found.append(("demonstration/answer", demonstration["answer"]))

   for index, line in enumerate(demonstration["lines"]):
      found.append((f"demonstration/lines/{index}/typed", line["typed"]))
      found.append((f"demonstration/lines/{index}/shows", line["shows"]))

   for index, habit in enumerate(card["exam_habit"]):
      found.append((f"exam_habit/{index}/text", habit["text"]))

   return found


def lint_schema(card, context):
   validator = jsonschema.Draft202012Validator(context.schema)
   errors = sorted(validator.iter_errors(card), key=lambda error: list(error.absolute_path))
   messages = []

   for error in errors[:5]:
      deepest = best_match([error])
      location = "/".join(str(part) for part in deepest.absolute_path) or "<root>"
      messages.append(f"{location}: {deepest.message[:160]}")

   return messages


def lint_citations(card, context):
   messages = []

   for source in card["sources"]:
      page_file = context.page_files(source["doc"], source["page"])[0]

      if not page_file.exists():
         messages.append(f"{source['doc']}:{source['page']} has no cached page at {page_file.relative_to(ROOT)}")

   return messages


def quote_problem(quote, page_text):
   length = len(quote.split())

   if length > QUOTE_WORDS_MAX:
      return f"is {length} words, and the cap is {QUOTE_WORDS_MAX}"

   needle = check_lessons.normalise_text(quote)

   if needle and needle in page_text:
      return None

   words = needle.split()
   runs = [" ".join(words[index:index + PARTIAL_RUN_WORDS]) for index in range(len(words) - PARTIAL_RUN_WORDS + 1)]
   matched_runs = sum(1 for run in runs if run in page_text)
   is_mostly_found = matched_runs >= max(1, (len(words) - PARTIAL_RUN_WORDS + 1) // 2)

   if is_mostly_found:
      return "only partially matches the page"

   return "is not found on the page"


def lint_quotes(card, context):
   messages = []

   for source in card["sources"]:
      page_file = context.page_files(source["doc"], source["page"])[0]

      if not page_file.exists():
         continue

      problem = quote_problem(source["anchor_quote"], context.page_text(source["doc"], source["page"]))

      if problem is not None:
         messages.append(f"quote on {source['doc']}:{source['page']} {problem}: {source['anchor_quote'][:60]!r}")

   return messages


def lint_error_ids(card, context):
   messages = []

   for habit in card["exam_habit"]:
      for error_id in habit["error_ids"]:
         if not context.error_is_active(error_id):
            messages.append(f"{error_id} is not an active record in data/errors.json")

   return messages


def word_runs(text, length):
   words = check_lessons.normalise_text(text).split()

   return {" ".join(words[index:index + length]) for index in range(len(words) - length + 1)}


def reader_words(record):
   fields = (record.get("name"), record.get("observed_behavior"), record.get("teacher_advice"))

   return " ".join(field for field in fields if field)


def lint_habit_words(card, context):
   """An exam habit carries the reader's words: it shares a run of words with the name, observed
   behaviour or teacher advice of one of the records it names."""
   messages = []

   for index, habit in enumerate(card["exam_habit"]):
      records = [context.errors[error_id] for error_id in habit["error_ids"] if error_id in context.errors]
      habit_runs = word_runs(habit["text"], HABIT_RUN_WORDS)
      shares_words = any(habit_runs & word_runs(reader_words(record), HABIT_RUN_WORDS) for record in records)

      if not shares_words:
         messages.append(
            f"exam_habit/{index} shares no run of {HABIT_RUN_WORDS} words with the records it names"
         )

   return messages


def lint_student_text(card, context):
   messages = []

   for location, text in student_strings(card):
      if check_lessons.DASHES.search(text):
         messages.append(f"{location}: an em dash or en dash appears")

      if check_lessons.EMOJI.search(text):
         messages.append(f"{location}: an emoji or pictograph appears")

      for name, pattern in SERVED_PATTERNS + STYLE_PATTERNS:
         found = pattern.search(text)

         if found:
            messages.append(f"{location}: {name} {found.group(0)!r}")

      for pattern in check_lessons.COMMON.FORBIDDEN_PREDICTION:
         found = re.search(pattern, text, re.I)

         if found:
            messages.append(f"{location}: prediction {found.group(0)!r}")

   return messages


def lint_keys(card, context):
   messages = []

   for index, step in enumerate(card["steps"]):
      is_blank = step["keys"].strip() == ""

      if is_blank:
         messages.append(f"steps/{index} has no keys")

   return messages


def lint_answer(card, context):
   answer = card["demonstration"]["answer"]
   has_three_places = THREE_PLACE_ANSWER.match(answer) is not None

   if has_three_places:
      return []

   return [f"demonstration answer {answer!r} does not have exactly three decimal places"]


CARD_LINTS = {
   "schema": lint_schema,
   "citations": lint_citations,
   "quotes": lint_quotes,
   "error_ids": lint_error_ids,
   "habit_words": lint_habit_words,
   "student_text": lint_student_text,
   "keys": lint_keys,
   "answer": lint_answer,
}


def check_card(card, context):
   """Lint name to messages. A card that fails the schema is reported for the schema alone,
   because the other lints read fields it may lack."""
   schema_messages = lint_schema(card, context)

   if schema_messages:
      return {"schema": schema_messages}

   findings = {}

   for name, lint in CARD_LINTS.items():
      if name == "schema":
         continue

      try:
         messages = lint(card, context)
      except Exception as error:
         messages = [f"lint crashed: {type(error).__name__}: {error}"]

      if messages:
         findings[name] = messages

   return findings


def lint_coverage(cards, context):
   present = {card.get("capability") for card in cards}

   return [f"no card for the {capability} capability" for capability in DRILLED_CAPABILITIES if capability not in present]


def lint_template_set(cards, context):
   messages = []
   card_ids = {card.get("id") for card in cards}
   listed = {template["id"]: template for template in context.templates}

   if len(listed) != len(context.templates):
      messages.append(f"{TEMPLATES_FILE} lists a template id twice")

   for template in context.templates:
      card_id = template["card_id"]

      if card_id not in card_ids:
         messages.append(f"{template['id']} names card {card_id}, which does not exist")

   for card in cards:
      for template_id in card.get("drills", []):
         template = listed.get(template_id)

         if template is None:
            messages.append(f"{card.get('id')} drills {template_id}, which {TEMPLATES_FILE} does not list")
            continue

         if template["card_id"] != card.get("id"):
            messages.append(f"{card.get('id')} drills {template_id}, which {TEMPLATES_FILE} gives to {template['card_id']}")

   for template_id, template in listed.items():
      naming_cards = [card.get("id") for card in cards if template_id in card.get("drills", [])]
      names_one_card = len(naming_cards) == 1

      if not names_one_card and template["card_id"] in card_ids:
         messages.append(f"{template_id} is drilled by {len(naming_cards)} cards, not exactly one")

   return messages


SET_LINTS = {
   "coverage": lint_coverage,
   "template_set": lint_template_set,
}


def has_enough_nonzero_decimals(key):
   decimals = format(abs(key_decimal(key)), "f").partition(".")[2]
   nonzero = sum(1 for digit in decimals if digit != "0")

   return nonzero >= MIN_NONZERO_DECIMALS


def key_decimal(key):
   return Decimal(str(sympy.Float(key, KEY_DIGITS)))


def forms_differ(key):
   exact = key_decimal(key)
   rounded = exact.quantize(THREE_PLACES, rounding=ROUND_HALF_UP)
   truncated = exact.quantize(THREE_PLACES, rounding=ROUND_DOWN)

   return rounded != truncated


def is_draw_exhausted(error):
   return type(error).__name__ == "DrawExhausted"


class CountingBuild:
   """Stands in for a template's build while the checker draws, so a redraw inside draw_task
   shows as a second call."""

   def __init__(self, build):
      self.build = build
      self.calls = 0

   def __call__(self, names):
      self.calls += 1

      return self.build(names)


def draw_findings(registry, template_id, module):
   from app.items.mathjson import to_sympy

   messages = []
   excluded = 0
   weak_keys = []
   unread_setups = []
   counter = CountingBuild(module.build)
   module.build = counter

   try:
      for index in range(DRAWS_PER_TEMPLATE):
         seed = f"{template_id}:v{module.TEMPLATE_VERSION}:check:{index}"
         calls_before = counter.calls

         try:
            task = registry.draw_task(template_id, seed)
         except Exception as error:
            if not is_draw_exhausted(error):
               raise

            excluded += 1
            continue

         was_redrawn = counter.calls - calls_before > 1

         if was_redrawn:
            excluded += 1

         key_is_usable = has_enough_nonzero_decimals(task.value_key) and forms_differ(task.value_key)

         if not key_is_usable:
            weak_keys.append(f"{seed} gives {task.value_key}")

         try:
            to_sympy(task.setup_key)
         except Exception as error:
            unread_setups.append(f"{seed}: {type(error).__name__}")
   finally:
      module.build = counter.build

   if excluded * 2 > DRAWS_PER_TEMPLATE:
      messages.append(f"{template_id} excludes {excluded} of {DRAWS_PER_TEMPLATE} draws, more than half")

   if weak_keys:
      messages.append(
         f"{template_id} value_key lacks {MIN_NONZERO_DECIMALS} nonzero decimals or rounds as it truncates "
         f"in {len(weak_keys)} of {DRAWS_PER_TEMPLATE} draws, first {weak_keys[0]}"
      )

   if unread_setups:
      messages.append(
         f"{template_id} setup_key is refused by to_sympy in {len(unread_setups)} of {DRAWS_PER_TEMPLATE} draws, first {unread_setups[0]}"
      )

   return messages


def naming_findings(template_id, module, cards, context):
   messages = []
   card_ids = {card.get("id") for card in cards}
   listed = {template["id"]: template for template in context.templates}
   template = listed.get(template_id)
   card_id = getattr(module, "CARD_ID", None)
   naming_cards = [card.get("id") for card in cards if template_id in card.get("drills", [])]

   if template is None:
      messages.append(f"{template_id} is in the registry but not in {TEMPLATES_FILE}")
   elif template["card_id"] != card_id:
      messages.append(f"{template_id} names {card_id}, and {TEMPLATES_FILE} gives it to {template['card_id']}")

   if card_id not in card_ids:
      messages.append(f"{template_id} names card {card_id}, which does not exist")

   if naming_cards != [card_id]:
      messages.append(f"{template_id} names {card_id}, and the cards that drill it are {naming_cards or 'none'}")

   return messages


def lint_templates(cards, context, registry=None):
   """The template section: every registered template draws, keys and names its card as the
   contract in docs/calculator/build-plan.md says."""
   if registry is None:
      registry = importlib.import_module("app.calculator.registry")

   modules = registry.templates()
   messages = []

   for template in context.templates:
      if template["id"] not in modules:
         messages.append(f"{template['id']} is in {TEMPLATES_FILE} but not in the registry")

   for template_id, module in sorted(modules.items()):
      messages.extend(naming_findings(template_id, module, cards, context))

      try:
         messages.extend(draw_findings(registry, template_id, module))
      except Exception as error:
         messages.append(f"{template_id} did not draw: {type(error).__name__}: {error}")

   return messages


def content_paths(given):
   """The card files and the template list a path names. A directory holding cards/ is a content
   root; any other directory holds cards; the template list sits in the directory or its parent."""
   path = Path(given)

   if path.is_dir():
      card_dir = path / "cards" if (path / "cards").is_dir() else path
      cards = sorted(child for child in card_dir.iterdir() if child.suffix == ".json" and child.name != TEMPLATES_FILE)
      search = [path, path.parent]
   else:
      cards = [path]
      search = [path.parent, path.parent.parent]

   templates = next((directory / TEMPLATES_FILE for directory in search if (directory / TEMPLATES_FILE).exists()), None)

   return cards, templates


def check_paths(paths, include_templates=True, registry=None):
   card_files = []
   template_files = []

   for given in paths:
      cards, templates = content_paths(given)
      card_files.extend(cards)

      if templates is not None and templates not in template_files:
         template_files.append(templates)

   templates = []

   for template_file in template_files:
      templates.extend(json.loads(template_file.read_text())["templates"])

   context = Context(templates)
   cards = []
   findings_by_file = {}

   for card_file in card_files:
      card = json.loads(card_file.read_text())
      cards.append(card)
      findings = check_card(card, context)

      if findings:
         findings_by_file[card_file.name] = findings

   set_findings = {}

   if not template_files:
      set_findings["template_set"] = [f"no {TEMPLATES_FILE} beside the cards"]

   for name, lint in SET_LINTS.items():
      messages = lint(cards, context)

      if messages:
         set_findings.setdefault(name, []).extend(messages)

   if set_findings:
      findings_by_file[CARD_SET] = set_findings

   if include_templates:
      messages = lint_templates(cards, context, registry)

      if messages:
         findings_by_file[TEMPLATES_FILE] = {"templates": messages}

   return {"card_count": len(card_files), "card_names": [path.name for path in card_files], "findings_by_file": findings_by_file}


def print_report(report):
   for file_name, findings in report["findings_by_file"].items():
      print(f"{file_name}:")

      for name, messages in findings.items():
         for message in messages:
            print(f"  {name}: {message}")

   dirty_cards = [name for name in report["card_names"] if name in report["findings_by_file"]]
   print()
   print(f"cards read: {report['card_count']}")
   print(f"clean: {report['card_count'] - len(dirty_cards)}")
   print(f"with findings: {len(report['findings_by_file'])}")


def main(argv):
   arguments = argv[1:]
   include_templates = "--no-templates" not in arguments
   unknown_flags = [argument for argument in arguments if argument.startswith("--") and argument != "--no-templates"]
   paths = [argument for argument in arguments if not argument.startswith("--")]
   is_usable = len(paths) > 0 and not unknown_flags

   if not is_usable:
      print("usage: python3 tools/check_calculator.py <directory or card file> [...] [--no-templates]", file=sys.stderr)

      return 1

   missing = [path for path in paths if not Path(path).exists()]

   if missing:
      print(f"refusing: {', '.join(missing)} does not exist", file=sys.stderr)

      return 1

   report = check_paths(paths, include_templates=include_templates)
   print_report(report)
   has_no_cards = report["card_count"] == 0

   if has_no_cards:
      print("refusing: no card files were read, so nothing was checked", file=sys.stderr)

      return 1

   all_clean = len(report["findings_by_file"]) == 0

   return 0 if all_clean else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
