"""Download the public College Board corpus into cache/ and record a manifest.

Live files come from apcentral.collegeboard.org. Withdrawn years come from the
Wayback Machine using the id_ raw-content form. Every fetch is recorded, including
failures, so the coverage matrix can state what was not obtainable.
"""

import hashlib
import json
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "cache" / "pdf"
MANIFEST = ROOT / "cache" / "manifest.json"
BASE = "https://apcentral.collegeboard.org/media/pdf/"
LEGACY = "https://secure-media.collegeboard.org/digitalServices/pdf/ap/"
WAYBACK = "https://web.archive.org/web/{ts}id_/{url}"

LIVE_YEARS = [23, 24, 25, 26]
ARCHIVED_YEARS = [18, 19, 21, 22]
LEGACY_YEARS = list(range(12, 18))


def per_year_docs(yy):
   docs = {
      f"frq-{yy}": f"ap{yy}-frq-calculus-bc.pdf",
      f"sg-{yy}": f"ap{yy}-sg-calculus-bc.pdf",
      f"stats-{yy}": f"ap{yy}-calculus-bc-scoring-statistics.pdf",
      f"dist-{yy}": f"ap{yy}-calculus-bc-score-distributions.pdf",
      f"absub-{yy}": f"ap{yy}-calculus-bc-ab-subscore-score-distributions.pdf",
      f"cr-{yy}": f"ap{yy}-cr-report-calculus.pdf",
      f"crabbc-{yy}": f"ap{yy}-cr-report-calculus-ab-bc.pdf",
   }

   for question in range(1, 7):
      docs[f"samples-{yy}-q{question}"] = f"ap{yy}-apc-calculus-bc-q{question}.pdf"

   return docs


def legacy_docs(yy):
   docs = {
      f"frq-{yy}": f"apcentral/ap{yy}_calculus_bc_frq.pdf",
      f"sg-{yy}": f"apcentral/ap{yy}_calculus_bc_scoring_guidelines.pdf",
   }

   for question in range(1, 7):
      docs[f"samples-{yy}-q{question}"] = f"apcentral/ap{yy}_calculus_bc_q{question}.pdf"

   return docs


STANDALONE = {
   "ced": BASE + "ap-calculus-ab-and-bc-course-and-exam-description.pdf",
   "ced-clarifications-2026": BASE + "ap-calculus-ab-bc-course-and-exam-description-clarifications-effective-fall-2026.pdf",
   "sample-questions": BASE + "sample-questions-ap-calculus-ab-and-bc-exams.pdf",
   "practice-exam-2012": BASE + "ap-calculus-bc-practice-exam-2012.pdf",
   "terms-conditions": BASE + "ap-services-terms-conditions.pdf",
}


def sha256_of(data):
   return hashlib.sha256(data).hexdigest()


def fetch(url, timeout=90):
   command = ["curl", "-sS", "-L", "-A", "Mozilla/5.0 research-cache", "--max-time", str(timeout), "-w", "\\n%{http_code}", url]
   result = subprocess.run(command, capture_output=True)
   body, _, code = result.stdout.rpartition(b"\n")

   try:
      status = int(code)
   except ValueError:
      status = -1

   return status, "", body


def fetch_with_retry(url, attempts=4):
   for attempt in range(attempts):
      status, content_type, data = fetch(url)
      is_rate_limited = status == 429

      if not is_rate_limited:
         return status, content_type, data

      time.sleep(15 * (attempt + 1))

   return status, content_type, data


def wayback_candidates(url):
   for ts in ["2024", "2023", "2022", "2021", "2020", "2019"]:
      yield WAYBACK.format(ts=ts, url=url)


def store(doc_id, url, tier, manifest, force=False):
   already_have = doc_id in manifest and manifest[doc_id].get("status") == "ok"
   should_skip = already_have and not force

   if should_skip:
      return

   attempts = [url] if tier == "live" else list(wayback_candidates(url))
   record = {"doc_id": doc_id, "requested_url": url, "tier": tier, "fetch_date": str(date.today()), "status": "missing", "attempts": []}

   for candidate in attempts:
      status, content_type, data = fetch_with_retry(candidate)
      is_pdf = data[:5] == b"%PDF-"
      record["attempts"].append({"url": candidate, "http": status, "pdf": is_pdf})

      if is_pdf:
         digest = sha256_of(data)
         (PDF_DIR / f"{digest}.pdf").write_bytes(data)
         record.update({"status": "ok", "resolved_url": candidate, "sha256": digest, "bytes": len(data)})
         break

      time.sleep(2)

   manifest[doc_id] = record
   MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True))
   print(doc_id, record["status"], record.get("bytes", ""), flush=True)


def main():
   PDF_DIR.mkdir(parents=True, exist_ok=True)
   manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
   only = sys.argv[1:] or ["standalone", "live", "archived", "legacy"]

   if "standalone" in only:
      for doc_id, url in STANDALONE.items():
         store(doc_id, url, "live", manifest)

   if "live" in only:
      for yy in LIVE_YEARS:
         for doc_id, name in per_year_docs(yy).items():
            store(doc_id, BASE + name, "live", manifest)

   if "archived" in only:
      for yy in ARCHIVED_YEARS:
         for doc_id, name in per_year_docs(yy).items():
            store(doc_id, BASE + name, "archived", manifest)

   if "legacy" in only:
      for yy in LEGACY_YEARS:
         for doc_id, name in legacy_docs(yy).items():
            store(doc_id, LEGACY + name, "archived", manifest)


if __name__ == "__main__":
   main()
