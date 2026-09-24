"""Operator command: the gate 29 worksheet for a drawn key-audit sample.

Usage: python3 tools/key_audit_worksheet.py <sample.json> <out_worksheet.md> <out_verdicts.json>
       [--items-dir DIR] [--content-root DIR]

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
DEFAULT_ITEMS_DIR = REPO_ROOT / "content" / "items_p1_agent"
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Write the key-audit worksheet and verdict template.")
   parser.add_argument("sample")
   parser.add_argument("worksheet")
   parser.add_argument("verdicts")
   parser.add_argument("--items-dir", default=str(DEFAULT_ITEMS_DIR))
   parser.add_argument("--content-root", default=str(DEFAULT_CONTENT_ROOT))

   return parser.parse_args(argv)


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
   items_dir = Path(arguments.items_dir)
   archetypes = {
      record["id"]: record
      for record in json.loads((Path(arguments.content_root) / "archetypes.json").read_text())["archetypes"]
   }
   missing = [item_id for item_id in sample if not (items_dir / f"{item_id}.json").is_file()]
   has_missing = len(missing) > 0

   if has_missing:
      print(f"no record in {items_dir} for {', '.join(missing)}; nothing was written", file=sys.stderr)

      return 1

   lines = [
      "# Key audit worksheet",
      "",
      f"{len(sample)} sampled items. Solve each by hand first, then compare with the app's stored answer.",
      "",
   ]

   for item_id in sample:
      record = json.loads((items_dir / f"{item_id}.json").read_text())
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
