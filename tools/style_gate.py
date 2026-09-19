"""PostToolUse hook: reject em dashes, spaced en dashes, and missing front matter in research and data files.

Reads the hook payload from stdin, checks the written file, and exits 2 with a message when the file breaks a rule.
"""
import json
import re
import sys
from pathlib import Path


def main():
   try:
      payload = json.load(sys.stdin)
   except Exception:
      return

   file_path = payload.get("tool_input", {}).get("file_path", "")
   is_library_file = "/research/" in file_path or "/data/" in file_path or file_path.endswith(".py")

   if not is_library_file:
      return

   path = Path(file_path)
   has_file = path.exists()

   if not has_file:
      return

   text = path.read_text(errors="ignore")
   problems = []
   has_em_dash = "—" in text
   has_spaced_en_dash = " – " in text
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

   if problems:
      print(f"style_gate: {path.name}: " + "; ".join(problems), file=sys.stderr)
      sys.exit(2)


if __name__ == "__main__":
   main()
