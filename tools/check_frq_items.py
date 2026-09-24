"""Check a directory of free-response records against the loaded library.

Usage: python3 tools/check_frq_items.py [content/frq_items]

Every record must pass app/frq/items.py record_violations (archetype and point types known, every
point type one the archetype lists, point skills the item's, checks well formed) and the rules
below, which the loader does not need but the bank does:

- the file is named by the record's id;
- the item's skills are the archetype's skills;
- every calculator part names a setup point (a point whose check is bounds_match or whose
  point type is BC-PT-99001, 99002, 99020, 99048, 99051, 99058 or 99059), and every other point
  in that part is eligible only if the setup point is earned (11 P3 scope item 6);
- every deterministic check's expected value is read by SymPy, and a numeric check's expected
  value is a finite real number;
- no stem, prompt or criterion carries an em dash.

Exit 0 when clean, 1 with one line per problem otherwise.
"""
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.content.loader import load_snapshot
from app.frq.items import all_points, record_violations, sympy_of

DEFAULT_DIRECTORY = REPO_ROOT / "content" / "frq_items"
SETUP_POINT_TYPES = {"BC-PT-99001", "BC-PT-99002", "BC-PT-99020", "BC-PT-99048", "BC-PT-99051", "BC-PT-99058", "BC-PT-99059"}
EM_DASH = chr(0x2014)


def is_setup_point(point):
   check = point.get("check") or {}
   is_bounds = check.get("kind") == "bounds_match"

   return is_bounds or point["point_type_id"] in SETUP_POINT_TYPES


def setup_problems(record):
   problems = []

   for part in record["parts"]:
      needs_setup = bool(part.get("setup_required"))

      if not needs_setup:
         continue

      setup_ids = [point["point_id"] for point in part["points"] if is_setup_point(point)]

      if not setup_ids:
         problems.append(f"{record['id']} part {part['id']}: setup_required but no setup point")
         continue

      for point in part["points"]:
         is_the_setup = point["point_id"] in setup_ids
         waits_for_setup = bool(set(setup_ids) & set(point.get("eligible_only_if") or []))

         if not is_the_setup and not waits_for_setup:
            problems.append(f"{record['id']} point {point['point_id']}: not eligible-only-if the setup point")

   return problems


def numeric_problems(record):
   problems = []

   for _part, point in all_points(record):
      check = point.get("check") or {}
      is_numeric = check.get("kind") == "numeric_three_decimals"

      if not is_numeric:
         continue

      try:
         value = float(sympy_of(check["expected"]))
      except (TypeError, ValueError):
         problems.append(f"{record['id']} point {point['point_id']}: expected is not a real number")
         continue

      if not math.isfinite(value):
         problems.append(f"{record['id']} point {point['point_id']}: expected is not finite")

   return problems


def text_problems(record):
   texts = [record["stem"]["text"]]

   for part in record["parts"]:
      texts.append(part["prompt"])
      texts.extend(point["criterion"] for point in part["points"])

   has_em_dash = any(EM_DASH in text for text in texts)

   return [f"{record['id']}: an em dash in the student-facing text"] if has_em_dash else []


def check_directory(directory, snapshot):
   problems = []
   paths = sorted(Path(directory).glob("*.json"))

   for path in paths:
      record = json.loads(path.read_text())
      structural = record_violations(record, snapshot.archetypes, snapshot.scoring_points)
      problems.extend(structural)

      if structural:
         continue

      if path.stem != record["id"]:
         problems.append(f"{path.name}: named differently from its id {record['id']}")

      archetype_skills = set(snapshot.archetypes[record["archetype_id"]]["skills"])

      if set(record["skills"]) != archetype_skills:
         problems.append(f"{record['id']}: skills differ from {record['archetype_id']}'s")

      problems.extend(setup_problems(record))
      problems.extend(numeric_problems(record))
      problems.extend(text_problems(record))

   return len(paths), problems


def main(argv):
   directory = Path(argv[1]) if len(argv) > 1 else DEFAULT_DIRECTORY
   snapshot = load_snapshot(REPO_ROOT / "data")
   count, problems = check_directory(directory, snapshot)

   for problem in problems:
      print(problem)

   print(f"{count} records, {len(problems)} problems")

   return 1 if problems else 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
