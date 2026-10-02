"""PostToolUse hook: reject em dashes, spaced en dashes, and missing front matter in research and data files.

As a hook it reads the payload from stdin and checks the written file. Given paths on the command line
(`python3 tools/style_gate.py FILE...`) it checks those instead and never reads stdin. Either way it exits
2 with a message when a file breaks a rule.
"""
import json
import re
import sys
from pathlib import Path


def file_problems(file_path):
   is_library_file = "/research/" in file_path or "/data/" in file_path or "/docs/" in file_path or file_path.endswith(".py")

   if not is_library_file:
      return []

   path = Path(file_path).resolve()
   has_file = path.is_file()

   if not has_file:
      return []

   text = path.read_text(errors="ignore")
   problems = []
   has_em_dash = "\u2014" in text
   has_spaced_en_dash = " \u2013 " in text
   is_markdown = path.suffix == ".md"
   lacks_front_matter = is_markdown and not text.startswith("---\n")
   has_predictive = is_markdown and path.name != "historical-frequency.md" and re.search(r"likely to appear|will (definitely |certainly )?(appear|be tested)|expect(ed)? to see", text, re.I) is not None

   if has_em_dash:
      problems.append("em dash present")

   if has_spaced_en_dash:
      problems.append("spaced en dash present")

   if lacks_front_matter:
      problems.append("markdown lacks front matter")

   if has_predictive:
      problems.append("predictive exam language present")

   return problems


def main():
   file_paths = [str(Path(argument).resolve()) for argument in sys.argv[1:]]

   if not file_paths:
      try:
         payload = json.load(sys.stdin)
      except Exception:
         return

      file_paths = [payload.get("tool_input", {}).get("file_path", "")]

   failed = False

   for file_path in file_paths:
      problems = file_problems(file_path)

      if problems:
         print(f"style_gate: {Path(file_path).name}: " + "; ".join(problems), file=sys.stderr)
         failed = True

   if failed:
      sys.exit(2)


if __name__ == "__main__":
   main()
