"""Blind re-solve support for lesson designs under docs/lessons/.

extract: writes a problems file holding only the problem statements of every worked example and
check in the named designs (never a key, a step or an option value), for a blind re-solver.
compare: reads the re-solver's answers file and the designs, compares each answer with the design's
key by SymPy and numerically, and writes or updates docs/lessons/verification/<id>.json with a
"resolve" block per lesson. Nothing under docs/lessons/unit-*, prerequisites or decisions is edited.

Usage: python3 tools/lesson_design_resolve.py extract <problems.json> <design.md>...
       python3 tools/lesson_design_resolve.py compare <answers.json> <problems.json>
       python3 tools/lesson_design_resolve.py judge <judgments.json>
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sympy

from tools.check_lesson_designs import Design, close_enough, equivalent, parse_expression

VERIFICATION_DIR = ROOT / "docs" / "lessons" / "verification"
LETTER = re.compile(r"^\s*\(?([A-Ha-h])\)?\s*$")


def example_context(record, check):
   """The worked example problem a check's stem leans on, or None for a stem that stands alone."""
   examples = record.get("worked_examples") or []

   if not examples:
      return None

   stem = check["stem"]["text"]
   is_completion = check.get("check_kind") == "completion"
   cites_example = "example" in stem.lower()
   reuses_given = stem.startswith("Same ")
   leans_on_example = is_completion or cites_example or reuses_given

   if not leans_on_example:
      return None

   return examples[0]["problem"]["text"]


def problems_of(design):
   record = design.record
   problems = []

   for example in record.get("worked_examples") or []:
      problems.append({
         "id": f"{design.lesson_id}#{example['id']}",
         "kind": "worked_example",
         "text": example["problem"]["text"],
         "calculator_status": example.get("calculator_status"),
         "answer_form": (example.get("answer") or {}).get("form"),
      })

   for check in record.get("checks") or []:
      key = check.get("key") or {}
      is_statement = key.get("form") == "statement"
      entry = {
         "id": f"{design.lesson_id}#{check['id']}",
         "kind": check.get("check_kind"),
         "text": check["stem"]["text"],
         "calculator_status": check.get("calculator_status"),
         "answer_form": key.get("form"),
      }

      context = example_context(record, check)

      if context is not None:
         entry["context"] = context

      if is_statement:
         entry["options"] = [{"id": option["id"], "label": option.get("label")} for option in check.get("options") or []]

      problems.append(entry)

   return problems


def keys_of(design):
   record = design.record
   keys = {}

   for example in record.get("worked_examples") or []:
      keys[f"{design.lesson_id}#{example['id']}"] = {
         "form": example["answer"]["form"],
         "expr": example["answer"].get("expr"),
         "text": example["answer"].get("text"),
         "calculator_status": example.get("calculator_status"),
      }

   for check in record.get("checks") or []:
      key = check.get("key") or {}
      key_option = next((option["id"] for option in check.get("options") or [] if option.get("is_key")), None)
      keys[f"{design.lesson_id}#{check['id']}"] = {
         "form": key.get("form"),
         "expr": key.get("expr"),
         "text": key.get("text") or key.get("label"),
         "key_option": key_option,
         "calculator_status": check.get("calculator_status"),
      }

   return keys


def extract(problems_path, design_paths):
   problems = []
   designs = []

   for path in design_paths:
      design = Design(path, Path(path).read_text())
      has_record = design.record is not None

      if not has_record:
         raise SystemExit(f"{path}: {design.record_error or 'no machine record'}")

      problems.extend(problems_of(design))
      designs.append(str(Path(path).resolve().relative_to(ROOT)))

   Path(problems_path).write_text(json.dumps({"designs": designs, "problems": problems}, indent=1, ensure_ascii=False) + "\n")
   print(f"wrote {len(problems)} problems from {len(designs)} designs to {problems_path}")


UNIT_TAIL = re.compile(r"^(?P<value>[^A-Za-z]*(?:[A-Za-z]+\([^)]*\)[^A-Za-z]*)*?)\s+[a-z][A-Za-z ]*$")


def bare_value(text):
   """The value before a trailing unit phrase, so "21/5 meters per minute" compares as 21/5."""
   match = UNIT_TAIL.match(text.strip())
   has_units = match is not None and match.group("value").strip() != ""

   if has_units:
      return match.group("value").strip()

   return text


def without_units(key_expression, given):
   """A key written with unit symbols (440*cm**3) compares as its number when the answer is bare."""
   key_symbols = getattr(key_expression, "free_symbols", set())
   given_symbols = getattr(given, "free_symbols", set())
   has_unit_symbols = len(key_symbols) > 0 and len(given_symbols) == 0

   if has_unit_symbols:
      return key_expression.subs({symbol: 1 for symbol in key_symbols})

   return key_expression


def loosened(given, key_expression):
   """The re-solver's answer with an arbitrary constant C dropped when the key carries none, and
   absolute values inside logarithms dropped when the key writes none (the design checker's
   integrate relation cannot verify log(Abs(...)), so designs omit the bars)."""
   result = given
   key_names = {str(symbol) for symbol in getattr(key_expression, "free_symbols", set())}
   given_names = {str(symbol) for symbol in getattr(given, "free_symbols", set())}
   drops_constant = "C" in given_names and "C" not in key_names

   if drops_constant:
      result = result.subs(sympy.Symbol("C"), 0)

   drops_bars = result.has(sympy.Abs) and not key_expression.has(sympy.Abs)

   if drops_bars:
      result = result.replace(sympy.Abs, lambda argument: argument)

   return result


def top_level_parts(text):
   """Splits on commas outside any parentheses, so "(1, 2), 3" gives two parts."""
   parts = []
   depth = 0
   current = ""

   for character in text:
      if character in "([{":
         depth += 1
      elif character in ")]}":
         depth -= 1

      is_separator = character == "," and depth == 0

      if is_separator:
         parts.append(current)
         current = ""
      else:
         current += character

   parts.append(current)

   return [part.strip() for part in parts]


def as_member_set(text):
   """A FiniteSet for an answer written as "[a, b]", "{a, b}" or "a, b", else None."""
   stripped = text.strip()
   is_bracketed = stripped.startswith("[") and stripped.endswith("]")
   is_braced = stripped.startswith("{") and stripped.endswith("}")
   inner = stripped[1:-1] if is_bracketed or is_braced else stripped
   members = top_level_parts(inner)
   is_list = is_bracketed or is_braced or len(members) > 1

   if not is_list:
      return None

   return sympy.FiniteSet(*[parse_expression(member) for member in members])


def agrees(key, answer):
   """(agree, detail) for one problem."""
   is_statement = key.get("form") == "statement"

   has_options = key.get("key_option") is not None

   has_option_field = answer.get("option") not in (None, "")
   judges_by_option_field = is_statement and has_options and has_option_field

   if judges_by_option_field:
      chosen = re.sub(r"[()\s]", "", str(answer["option"])).upper()
      key_option = str(key["key_option"]).upper()

      if chosen == key_option:
         return True, f"agree (option {chosen})"

      return False, f"disagree (key option {key_option}, re-solver option {chosen})"

   if is_statement and has_options:
      given = LETTER.match(str(answer.get("answer", "")))
      letter = given.group(1).upper() if given else str(answer.get("answer", "")).strip().upper()

      return letter == key.get("key_option"), f"key option {key.get('key_option')}, re-solver {letter}"

   if is_statement:
      return None, f"judgment: key says {key.get('text')!r}; re-solver says {str(answer.get('answer', ''))!r}"

   text = answer.get("answer")

   if text in (None, ""):
      return False, "no answer given"

   try:
      key_expression = parse_expression(key["expr"])
      cleaned = str(text).replace("Abs(", "abs(")
      given = as_member_set(cleaned)

      if given is None:
         given = parse_expression(bare_value(cleaned))
   except Exception as error:
      return False, f"could not parse {text!r}: {type(error).__name__}"

   is_set_answer = isinstance(given, sympy.FiniteSet)
   is_set_key = isinstance(key_expression, sympy.Set)

   if is_set_answer and not is_set_key:
      return False, f"key {key['expr']!r} is one value, re-solver gave the set {text!r}"

   is_decimal = key.get("calculator_status") == "calculator"
   key_expression = without_units(key_expression, given)

   try:
      symbolic = equivalent(key_expression, given) or equivalent(key_expression, loosened(given, key_expression))
      numeric = close_enough(key_expression, given) if is_decimal else False
   except Exception as error:
      return False, f"comparison failed on {text!r}: {type(error).__name__}"

   if symbolic or numeric:
      return True, f"agree ({'symbolic' if symbolic else 'three places'})"

   return False, f"key {key['expr']!r}, re-solver {text!r}"


def compare(answers_path, problems_path):
   problems = json.loads(Path(problems_path).read_text())
   answers = json.loads(Path(answers_path).read_text())
   by_id = {entry["id"]: entry for entry in (answers if isinstance(answers, list) else answers.get("answers", []))}
   keys = {}
   lessons = {}

   for relative in problems["designs"]:
      design = Design(ROOT / relative, (ROOT / relative).read_text())
      keys.update(keys_of(design))
      lessons[design.lesson_id] = []

   for problem in problems["problems"]:
      problem_id = problem["id"]
      lesson_id = problem_id.split("#")[0]
      answer = by_id.get(problem_id) or {}
      unsolved = answer.get("unsolvable") or answer.get("ambiguous")

      if unsolved:
         verdict = {"id": problem_id, "agree": False, "detail": f"re-solver: {unsolved}", "method": answer.get("method")}
      else:
         agree, detail = agrees(keys[problem_id], answer)
         verdict = {"id": problem_id, "agree": agree, "detail": detail, "method": answer.get("method")}

      lessons[lesson_id].append(verdict)

   VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
   disagreements = 0
   pending = 0

   for lesson_id, verdicts in lessons.items():
      path = VERIFICATION_DIR / f"{lesson_id}.json"
      existing = json.loads(path.read_text()) if path.exists() else {"id": lesson_id}
      judgments = [verdict for verdict in verdicts if verdict["agree"] is None]
      all_agree = all(verdict["agree"] for verdict in verdicts) and len(verdicts) > 0
      existing["resolve"] = {
         "date": date.today().isoformat(),
         "problems": len(verdicts),
         "agreed": sum(1 for verdict in verdicts if verdict["agree"]),
         "judgments_pending": len(judgments),
         "all_agree": all_agree,
         "verdicts": verdicts,
         "answers_file": str(Path(answers_path)),
      }
      path.write_text(json.dumps(existing, indent=1, ensure_ascii=False) + "\n")
      disagreements += sum(1 for verdict in verdicts if verdict["agree"] is False)
      pending += len(judgments)

      for verdict in verdicts:
         if verdict["agree"] is False:
            print(f"DISAGREE {verdict['id']}: {verdict['detail']}")

   print(f"lessons: {len(lessons)}, problems: {len(problems['problems'])}, disagreements: {disagreements}, judgments pending: {pending}")

   return 0 if disagreements == 0 else 1


def apply_judgments(judgments_path):
   """Writes a judge's verdicts onto the pending statement problems of the verification files."""
   judgments = json.loads(Path(judgments_path).read_text())
   changed = 0

   for problem_id, judgment in judgments.items():
      lesson_id = problem_id.split("#")[0]
      path = VERIFICATION_DIR / f"{lesson_id}.json"
      existing = json.loads(path.read_text())
      verdicts = existing["resolve"]["verdicts"]

      for verdict in verdicts:
         is_target = verdict["id"] == problem_id and verdict["agree"] is None

         if is_target:
            verdict["agree"] = bool(judgment["agree"])
            verdict["detail"] = f"judged: {judgment['reason']}"
            changed += 1

      existing["resolve"]["agreed"] = sum(1 for verdict in verdicts if verdict["agree"])
      existing["resolve"]["judgments_pending"] = sum(1 for verdict in verdicts if verdict["agree"] is None)
      existing["resolve"]["all_agree"] = all(verdict["agree"] for verdict in verdicts) and len(verdicts) > 0
      path.write_text(json.dumps(existing, indent=1, ensure_ascii=False) + "\n")

   print(f"judgments applied: {changed}")

   return 0


def main(argv):
   if len(argv) == 3 and argv[1] == "judge":
      return apply_judgments(argv[2])

   if len(argv) >= 4 and argv[1] == "extract":
      extract(argv[2], argv[3:])

      return 0

   if len(argv) == 4 and argv[1] == "compare":
      return compare(argv[2], argv[3])

   print(__doc__, file=sys.stderr)

   return 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
