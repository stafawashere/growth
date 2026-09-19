"""Build cache/page_index.json: for every cached document, which pages mention which FRQ question numbers.

Uses the pdftotext raw text because the PyMuPDF layer drops some lines in the scoring guidelines.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "cache" / "text"
OUT = ROOT / "cache" / "page_index.json"
QUESTION = re.compile(r"(?:Question|QUESTION)\s+([1-6])\b|^\s*([1-6])\.\s+[A-Z(]", re.M)
PART = re.compile(r"\bPart\s+([A-F])\b|\(([a-f])\)")


def main():
   index = {}

   for doc_dir in sorted(TEXT.iterdir()):
      pages = {}

      for page_file in sorted(doc_dir.glob("page-*.raw.txt")):
         number = int(page_file.name[5:8])
         text = page_file.read_text()
         primary = page_file.with_name(page_file.name.replace(".raw", "")).read_text()
         questions = sorted({group for match in QUESTION.finditer(text) for group in match.groups() if group})
         parts = sorted({(a or b).upper() for a, b in PART.findall(text)})
         pages[number] = {"questions": questions, "parts": parts, "chars_primary": len(primary.strip()), "chars_raw": len(text.strip())}

      index[doc_dir.name] = pages

   OUT.write_text(json.dumps(index, indent=0, sort_keys=True))
   print(len(index), "documents indexed")


if __name__ == "__main__":
   main()
