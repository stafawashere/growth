"""Quote caps and anchor-quote verification against cached text."""
import re
from qa_common import CACHE, all_records, finish

MAX_WORDS = 25
failures, warnings = [], []


def normalise(text):
   return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


for location, record in all_records():
   quote = record.get("anchor_quote")
   has_quote = bool(quote)

   if not has_quote:
      continue

   is_too_long = len(quote.split()) > MAX_WORDS

   if is_too_long:
      failures.append(f"{record['id']} anchor_quote exceeds {MAX_WORDS} words")

   doc_id, page = record.get("doc_id"), record.get("doc_page")
   page_file = CACHE / "text" / str(doc_id) / f"page-{int(page or 0):03d}.txt"
   raw_file = page_file.with_suffix(".raw.txt")
   has_page = page_file.exists()

   if not has_page:
      failures.append(f"{record['id']} cites {doc_id} page {page} which is not cached")
      continue

   haystack = normalise(page_file.read_text() + " " + (raw_file.read_text() if raw_file.exists() else ""))
   needle = normalise(quote)
   is_found = needle in haystack

   if not is_found:
      words = needle.split()
      partial = sum(1 for index in range(len(words) - 3) if " ".join(words[index:index + 4]) in haystack)
      is_mostly_found = partial >= max(1, (len(words) - 3) // 2)

      if is_mostly_found:
         warnings.append(f"{record['id']} anchor_quote only partially matches page {page} of {doc_id}")
      else:
         failures.append(f"{record['id']} anchor_quote not found on page {page} of {doc_id}")

finish("07_quotes", failures, warnings)
