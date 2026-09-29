"""Extract per-page text from every cached PDF into cache/text/<doc_id>/page-NNN.txt.

PyMuPDF is the primary extractor. Span font-size and baseline offsets are used to
mark superscripts with ^{...} and subscripts with _{...} so exponents, limit
subscripts, and integral bounds survive. pdftotext -raw is run as a cross-check
and stored beside the primary text. Pages with too little text are quarantined.

Web pages (manifest kind "web") become a single page. HTML is converted to text with
a small deterministic converter; the raw cross-check is the same HTML with every tag
replaced by a space. Browser-saved text is copied as it is to both files.
"""

import html
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "cache" / "pdf"
WEB_DIR = ROOT / "cache" / "web"
TEXT_DIR = ROOT / "cache" / "text"
MANIFEST = ROOT / "cache" / "manifest.json"
QUARANTINE = ROOT / "cache" / "quarantine.json"
MIN_CHARS_PER_PAGE = 40
SKIPPED_ELEMENTS = {"script", "style", "noscript", "nav", "header", "footer"}
BLOCK_ELEMENTS = {
   "address", "article", "aside", "blockquote", "dd", "details", "div", "dl", "dt", "figcaption", "figure",
   "form", "h1", "h2", "h3", "h4", "h5", "h6", "li", "main", "ol", "p", "pre", "section", "summary", "table",
   "tbody", "td", "th", "thead", "title", "tr", "ul",
}


class PageTextParser(HTMLParser):
   def __init__(self):
      super().__init__(convert_charrefs=True)
      self.pieces = []
      self.skip_depth = 0

   def handle_starttag(self, tag, attrs):
      is_skipped = tag in SKIPPED_ELEMENTS

      if is_skipped:
         self.skip_depth += 1
         return

      is_break = tag in ("br", "hr")
      is_inside_skipped = self.skip_depth > 0

      if is_break and not is_inside_skipped:
         self.pieces.append("\n")

   def handle_endtag(self, tag):
      is_skipped = tag in SKIPPED_ELEMENTS
      is_inside_skipped = self.skip_depth > 0

      if is_skipped and is_inside_skipped:
         self.skip_depth -= 1
         return

      is_block = tag in BLOCK_ELEMENTS

      if is_block and not is_inside_skipped:
         self.pieces.append("\n")

   def handle_data(self, data):
      is_inside_skipped = self.skip_depth > 0

      if not is_inside_skipped:
         self.pieces.append(data)


def tidy(text):
   lines = [re.sub(r"[ \t\r\f\v\u00a0]+", " ", line).strip() for line in text.split("\n")]
   joined = "\n".join(lines)
   return re.sub(r"\n{3,}", "\n\n", joined).strip() + "\n"


def html_to_text(markup):
   parser = PageTextParser()
   parser.feed(markup)
   parser.close()
   return tidy("".join(parser.pieces))


def html_to_raw_text(markup):
   return tidy(html.unescape(re.sub(r"<[^>]*>", " ", markup)))


def line_text(line):
   spans = line["spans"]
   has_spans = len(spans) > 0

   if not has_spans:
      return ""

   base_size = max(span["size"] for span in spans)
   base_origin = min(span["origin"][1] for span in spans)
   pieces = []

   for span in spans:
      text = span["text"]
      is_small = span["size"] < 0.8 * base_size
      is_raised = span["origin"][1] < base_origin - 0.5
      is_lowered = span["origin"][1] > base_origin + 1.5
      is_superscript = is_small and is_raised
      is_subscript = is_small and is_lowered

      if is_superscript:
         pieces.append("^{" + text.strip() + "}")
      elif is_subscript:
         pieces.append("_{" + text.strip() + "}")
      else:
         pieces.append(text)

   return "".join(pieces)


def page_text(page):
   blocks = page.get_text("dict")["blocks"]
   lines = []

   for block in blocks:
      is_text_block = block.get("type") == 0

      if not is_text_block:
         continue

      for line in block["lines"]:
         lines.append(line_text(line))

      lines.append("")

   return "\n".join(lines)


def pdftotext_pages(pdf_path):
   result = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"], capture_output=True, text=True)
   return result.stdout.split("\f")


def extract(doc_id, record):
   pdf_path = PDF_DIR / f"{record['sha256']}.pdf"
   out_dir = TEXT_DIR / doc_id
   out_dir.mkdir(parents=True, exist_ok=True)
   document = pymupdf.open(pdf_path)
   raw_pages = pdftotext_pages(pdf_path)
   quarantined = []

   for index, page in enumerate(document):
      primary = page_text(page)
      raw = raw_pages[index] if index < len(raw_pages) else ""
      (out_dir / f"page-{index + 1:03d}.txt").write_text(primary)
      (out_dir / f"page-{index + 1:03d}.raw.txt").write_text(raw)
      is_thin = len(primary.strip()) < MIN_CHARS_PER_PAGE

      if is_thin:
         quarantined.append(index + 1)

   (out_dir / "meta.json").write_text(json.dumps({"doc_id": doc_id, "pages": len(document), "sha256": record["sha256"], "quarantined_pages": quarantined}, indent=1))
   return len(document), quarantined


def extract_web(doc_id, record):
   is_html = record.get("format") == "html"
   suffix = "html" if is_html else "txt"
   body = (WEB_DIR / f"{record['sha256']}.{suffix}").read_bytes().decode("utf-8", errors="replace")
   out_dir = TEXT_DIR / doc_id
   out_dir.mkdir(parents=True, exist_ok=True)

   if is_html:
      primary = html_to_text(body)
      raw = html_to_raw_text(body)
   else:
      primary = body
      raw = body

   (out_dir / "page-001.txt").write_text(primary)
   (out_dir / "page-001.raw.txt").write_text(raw)
   is_thin = len(primary.strip()) < MIN_CHARS_PER_PAGE
   quarantined = [1] if is_thin else []
   (out_dir / "meta.json").write_text(json.dumps({"doc_id": doc_id, "pages": 1, "sha256": record["sha256"], "quarantined_pages": quarantined, "kind": "web"}, indent=1))
   return 1, quarantined


def main():
   manifest = json.loads(MANIFEST.read_text())
   quarantine = json.loads(QUARANTINE.read_text()) if QUARANTINE.exists() else {}
   wanted = sys.argv[1:]

   for doc_id, record in sorted(manifest.items()):
      is_ok = record.get("status") == "ok"
      is_wanted = not wanted or doc_id in wanted
      already_done = (TEXT_DIR / doc_id / "meta.json").exists()
      should_extract = is_ok and is_wanted and not already_done

      if not should_extract:
         continue

      is_web = record.get("kind") == "web"
      extractor = extract_web if is_web else extract
      pages, quarantined = extractor(doc_id, record)
      quarantine[doc_id] = quarantined
      print(doc_id, pages, "pages,", len(quarantined), "quarantined", flush=True)

   QUARANTINE.write_text(json.dumps(quarantine, indent=1, sort_keys=True))


if __name__ == "__main__":
   main()
