"""Operator command: the gate 29 worksheet for a drawn key-audit sample.

Usage: python3 tools/key_audit_worksheet.py <sample.json> <out_worksheet.md> <out_verdicts.json>
       [--items-dir DIR ...] [--content-root DIR]

--items-dir may be given more than once; unset, every content/items_* bank is searched.

docs/plan/10-quality-and-evaluation.md, "The audit": the operator solves each sampled item by hand,
without seeing the key, against the archetype's expected_solution_path. The worksheet lists, per
sampled item, its stem, that path and its options in served order, and never the stored key, which
option it is, or the worked solution. The verdicts file is the array docs/operator/key-audit.md
specifies, one record per sampled id with verdict, auditor and audited_at left for the operator;
tools/check_audit_verdicts.py refuses it until every record is filled.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sympy

from app.items.mathjson import to_sympy

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = REPO_ROOT / "content"
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Write the key-audit worksheet and verdict template.")
   parser.add_argument("sample")
   parser.add_argument("worksheet")
   parser.add_argument("verdicts")
   parser.add_argument("--items-dir", action="append", dest="items_dirs")
   parser.add_argument("--content-root", default=str(DEFAULT_CONTENT_ROOT))

   return parser.parse_args(argv)


def bank_directories(named):
   is_named = named is not None and len(named) > 0

   if is_named:
      return [Path(directory) for directory in named]

   return sorted(path for path in CONTENT_DIR.glob("items_*") if path.is_dir())


def record_path(item_id, directories):
   for directory in directories:
      candidate = directory / f"{item_id}.json"

      if candidate.is_file():
         return candidate

   return None


def option_text(value):
   return sympy.sstr(to_sympy(value))


def item_section(record, archetype):
   lines = [
      f"## {record['id']}",
      "",
      f"Archetype {record['archetype_id']}, served as {record['format']} or short answer.",
      "",
      record["stem"]["text"],
      "",
      "Solution path the archetype expects:",
      "",
   ]

   for number, step in enumerate(archetype.get("expected_solution_path", []), start=1):
      lines.append(f"{number}. {step}")

   options = record.get("options") or []
   has_options = len(options) > 0

   if has_options:
      lines.extend(["", "Options:", ""])

      for option in options:
         lines.append(f"- ({option['id']}) `{option_text(option['value'])}`")

   lines.extend(["", "Your working:", "", "Verdict (clean, key_wrong or ambiguous with the second answer):", ""])

   return lines


def main(argv):
   arguments = parse_arguments(argv[1:])
   sample = json.loads(Path(arguments.sample).read_text())
   directories = bank_directories(arguments.items_dirs)
   archetypes = {
      record["id"]: record
      for record in json.loads((Path(arguments.content_root) / "archetypes.json").read_text())["archetypes"]
   }
   missing = [item_id for item_id in sample if record_path(item_id, directories) is None]
   has_missing = len(missing) > 0

   if has_missing:
      searched = ", ".join(str(directory) for directory in directories)
      print(f"no record in {searched} for {', '.join(missing)}; nothing was written", file=sys.stderr)

      return 1

   lines = [
      "# Key audit worksheet",
      "",
      f"{len(sample)} sampled items. Solve each by hand first, then compare with the app's stored answer.",
      "",
   ]

   for item_id in sample:
      record = json.loads(record_path(item_id, directories).read_text())
      lines.extend(item_section(record, archetypes.get(record["archetype_id"], {})))

   template = [
      {"item_id": item_id, "verdict": None, "auditor": "", "audited_at": "", "second_answer": None}
      for item_id in sample
   ]
   Path(arguments.worksheet).write_text("\n".join(lines).rstrip("\n") + "\n")
   Path(arguments.verdicts).write_text(json.dumps(template, indent=3) + "\n")
   print(f"wrote {arguments.worksheet} and {arguments.verdicts} for {len(sample)} items")

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
