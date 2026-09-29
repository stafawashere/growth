"""Blind re-solve support for lesson designs under docs/lessons/.

extract: writes a problems file holding only the problem statements of every worked example and
check in the named designs (never a key, a step or an option value), for a blind re-solver.
compare: reads the re-solver's answers file and the designs, compares each answer with the design's
key by SymPy and numerically, and writes or updates docs/lessons/verification/<id>.json with a
"resolve" block per lesson. Nothing under docs/lessons/unit-*, prerequisites or decisions is edited.

Usage: python3 tools/lesson_design_resolve.py extract <problems.json> <design.md>...
       python3 tools/lesson_design_resolve.py compare <answers.json> <problems.json>
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
         "calculator_status": example.get("calculator_status"),
      }

   for check in record.get("checks") or []:
      key = check.get("key") or {}
      key_option = next((option["id"] for option in check.get("options") or [] if option.get("is_key")), None)
      keys[f"{design.lesson_id}#{check['id']}"] = {
         "form": key.get("form"),
         "expr": key.get("expr"),
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


def agrees(key, answer):
   """(agree, detail) for one problem."""
   is_statement = key.get("form") == "statement"

   if is_statement:
      given = LETTER.match(str(answer.get("answer", "")))
      letter = given.group(1).upper() if given else str(answer.get("answer", "")).strip().upper()

      return letter == key.get("key_option"), f"key option {key.get('key_option')}, re-solver {letter}"

   text = answer.get("answer")

   if text in (None, ""):
      return False, "no answer given"

   try:
      key_expression = parse_expression(key["expr"])
      given = parse_expression(str(text))
   except Exception as error:
      return False, f"could not parse {text!r}: {type(error).__name__}"

   is_decimal = key.get("calculator_status") == "calculator"
   symbolic = equivalent(key_expression, given)
   numeric = close_enough(key_expression, given) if is_decimal else False

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

   for lesson_id, verdicts in lessons.items():
      path = VERIFICATION_DIR / f"{lesson_id}.json"
      existing = json.loads(path.read_text()) if path.exists() else {"id": lesson_id}
      all_agree = all(verdict["agree"] for verdict in verdicts) and len(verdicts) > 0
      existing["resolve"] = {
         "date": date.today().isoformat(),
         "problems": len(verdicts),
         "agreed": sum(1 for verdict in verdicts if verdict["agree"]),
         "all_agree": all_agree,
         "verdicts": verdicts,
         "answers_file": str(Path(answers_path)),
      }
      path.write_text(json.dumps(existing, indent=1, ensure_ascii=False) + "\n")
      disagreements += sum(1 for verdict in verdicts if not verdict["agree"])

      for verdict in verdicts:
         if not verdict["agree"]:
            print(f"DISAGREE {verdict['id']}: {verdict['detail']}")

   print(f"lessons: {len(lessons)}, problems: {len(problems['problems'])}, disagreements: {disagreements}")

   return 0 if disagreements == 0 else 1


def main(argv):
   if len(argv) >= 4 and argv[1] == "extract":
      extract(argv[2], argv[3:])

      return 0

   if len(argv) == 4 and argv[1] == "compare":
      return compare(argv[2], argv[3])

   print(__doc__, file=sys.stderr)

   return 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
