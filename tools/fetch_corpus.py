"""Download the public College Board corpus into cache/ and record a manifest.

Live files come from apcentral.collegeboard.org. Withdrawn years come from the
Wayback Machine using the id_ raw-content form. Every fetch is recorded, including
failures, so the coverage matrix can state what was not obtainable.

Web pages (the `web` section) are fetched with curl too. A page that answers with a
PDF is stored as a PDF; anything else is stored as HTML under cache/web/<sha256>.html
with kind "web" in the manifest.

Pages curl cannot fetch (help.desmos.com answers 403, and some desmos.com pages only
render in a browser) are captured as text in a browser and ingested from disk:

   python3 tools/fetch_corpus.py --saved DOC_ID URL PATH [--saved DOC_ID URL PATH ...]
   python3 tools/fetch_corpus.py --saved-dir DIR

--saved takes exactly three values and may repeat. --saved-dir ingests every .txt file
in DIR, reading the URL from its "Source:" header line and taking the doc id from
SAVED_DOC_IDS, or for an unlisted file, desmos-help-<file slug lowercased> with the
leading article number removed. The stored file keeps its header. Add --force to
refetch or re-ingest documents already recorded as ok.
"""

import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "cache" / "pdf"
WEB_DIR = ROOT / "cache" / "web"
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


WEB_DOCS = {
   "web-bc-course": "https://apcentral.collegeboard.org/courses/ap-calculus-bc",
   "web-bc-exam": "https://apcentral.collegeboard.org/courses/ap-calculus-bc/exam",
   "web-bc-past": "https://apcentral.collegeboard.org/courses/ap-calculus-bc/exam/past-exam-questions",
   "web-bc-students": "https://apstudents.collegeboard.org/courses/ap-calculus-bc/assessment",
   "web-calc-policy": "https://apstudents.collegeboard.org/exam-policies-guidelines/calculator-policies",
   "web-calc-policy-central": "https://apcentral.collegeboard.org/exam-administration-ordering-scores/administering-exams/preparing-for-exam-day/calculator-policy",
   "web-ab-subscore": "https://apstudents.collegeboard.org/about-ap-scores/special-score-structure-calculus-bc",
   "web-exam-dates": "https://apcentral.collegeboard.org/exam-administration-ordering-scores/exam-dates",
   "web-score-setting": "https://apcentral.collegeboard.org/courses/how-ap-develops-courses-and-exams/score-setting-and-scoring",
   "web-equating": "https://apcentral.collegeboard.org/help-center/what-equating-processes-does-ap-use",
   "web-key-changes": "https://apcentral.collegeboard.org/courses/resources/ap-calculus-updates-key-changes",
   "web-bluebook-tools": "https://bluebook.collegeboard.org/students/tools",
   "hybrid-booklets-2026": BASE + "ap-hybrid-digital-exams-free-response-booklets-overview.pdf",
   "desmos-cb-calculators-pdf": "https://www.desmos.com/assessment-pdfs/CollegeBoard_Desmos_Calculator_AP_SAT.pdf",
   "desmos-default-testing-pdf": "https://www.desmos.com/state-pdfs/Default_Desmos_Calculators.pdf",
   "desmos-user-guide-pdf": "https://www.desmos.com/static-assets/user-guide-pdfs/Desmos_User_Guide.pdf",
   "desmos-api-docs": "https://www.desmos.com/api/v1.12/docs/index.html",
}

SAVED_DOC_IDS = {
   "desmos-terms.txt": "desmos-terms",
   "desmos-api-terms.txt": "desmos-api-terms",
   "desmos-testing.txt": "desmos-testing",
   "desmos-graphing-shortcuts.txt": "desmos-graphing-shortcuts",
   "30913914831757-Assessment-Resources-FAQ.txt": "desmos-help-assessment-faq",
   "18228147914381-Practice-With-Testing-Calculators.txt": "desmos-help-testing-calculators",
   "4405003743757-Using-Desmos-on-In-Class-Assessments.txt": "desmos-help-in-class-assessments",
   "4406810279693-Integrals.txt": "desmos-help-integrals",
   "4406809433613-Derivatives.txt": "desmos-help-derivatives",
   "212235786-Supported-Functions.txt": "desmos-help-supported-functions",
   "4406040715149-Getting-Started-Desmos-Graphing-Calculator.txt": "desmos-help-getting-started",
   "4405296853517-Graph-Settings.txt": "desmos-help-graph-settings",
   "4406029680653-Trigonometry.txt": "desmos-help-trigonometry",
   "4405177116941-Functions.txt": "desmos-help-functions",
   "4405489674381-Tables.txt": "desmos-help-tables",
   "202529069-Sliders-and-Movable-Points-in-a-Graph.txt": "desmos-help-sliders",
   "4405966811021-Keyboard-Shortcuts.txt": "desmos-help-keyboard-shortcuts",
   "4407885334285-Inequalities-and-Restrictions.txt": "desmos-help-restrictions",
   "4406972958733-Regressions.txt": "desmos-help-regressions",
   "4406360401677-FAQs.txt": "desmos-help-faqs",
   "202529279-Desmos-Graphing-Calculator-User-Guide.txt": "desmos-help-user-guide",
   "4405017454477--What-s-New-at-Desmos-Studio.txt": "desmos-help-whats-new",
   "49078363315725-API-Plans-for-Commercial-Use.txt": "desmos-help-api-plans",
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


def save_manifest(manifest):
   MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True))


def store_web(doc_id, url, manifest, force=False):
   already_have = doc_id in manifest and manifest[doc_id].get("status") == "ok"
   should_skip = already_have and not force

   if should_skip:
      return

   record = {"doc_id": doc_id, "requested_url": url, "tier": "live", "fetch_date": str(date.today()), "status": "missing", "attempts": []}
   status, content_type, data = fetch_with_retry(url)
   is_pdf = data[:5] == b"%PDF-"
   record["attempts"].append({"url": url, "http": status, "pdf": is_pdf})
   is_success = status == 200
   has_body = len(data.strip()) > 0
   is_usable = is_success and has_body

   if is_usable and is_pdf:
      digest = sha256_of(data)
      PDF_DIR.mkdir(parents=True, exist_ok=True)
      (PDF_DIR / f"{digest}.pdf").write_bytes(data)
      record.update({"status": "ok", "resolved_url": url, "sha256": digest, "bytes": len(data)})
   elif is_usable:
      digest = sha256_of(data)
      WEB_DIR.mkdir(parents=True, exist_ok=True)
      (WEB_DIR / f"{digest}.html").write_bytes(data)
      record.update({"status": "ok", "resolved_url": url, "kind": "web", "format": "html", "fetch_method": "curl", "sha256": digest, "bytes": len(data)})

   manifest[doc_id] = record
   save_manifest(manifest)
   print(doc_id, record["status"], status, record.get("bytes", ""), flush=True)


def store_saved(doc_id, url, path, manifest, force=False):
   already_have = doc_id in manifest and manifest[doc_id].get("status") == "ok"
   should_skip = already_have and not force

   if should_skip:
      return

   path = Path(path)
   data = path.read_bytes()
   digest = sha256_of(data)
   WEB_DIR.mkdir(parents=True, exist_ok=True)
   (WEB_DIR / f"{digest}.txt").write_bytes(data)
   manifest[doc_id] = {
      "doc_id": doc_id, "requested_url": url, "resolved_url": url, "tier": "live", "kind": "web", "format": "text",
      "fetch_method": "browser_saved_text", "saved_from": path.name, "fetch_date": str(date.today()), "status": "ok",
      "sha256": digest, "bytes": len(data), "attempts": [],
   }
   save_manifest(manifest)
   print(doc_id, "ok saved", len(data), flush=True)


def saved_source_url(path):
   for line in Path(path).read_text().splitlines()[:3]:
      is_source = line.startswith("Source:")

      if is_source:
         return line[len("Source:"):].strip()

   return None


def saved_doc_id(path):
   path = Path(path)
   known = SAVED_DOC_IDS.get(path.name)

   if known:
      return known

   is_help_article = re.match(r"^\d+-", path.stem) is not None

   if not is_help_article:
      return path.stem.lower()

   slug = re.sub(r"^\d+-+", "", path.stem).lower()
   return "desmos-help-" + slug


def saved_dir_entries(directory):
   entries = []

   for path in sorted(Path(directory).glob("*.txt")):
      url = saved_source_url(path)

      if url is None:
         print("skipped, no Source header:", path.name, flush=True)
         continue

      entries.append((saved_doc_id(path), url, path))

   return entries


def saved_arguments(arguments):
   entries = []
   index = 0

   while index < len(arguments):
      argument = arguments[index]

      if argument == "--saved":
         doc_id, url, path = arguments[index + 1:index + 4]
         entries.append((doc_id, url, Path(path)))
         index += 4
      elif argument == "--saved-dir":
         entries.extend(saved_dir_entries(arguments[index + 1]))
         index += 2
      else:
         index += 1

   return entries


def main():
   PDF_DIR.mkdir(parents=True, exist_ok=True)
   manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
   arguments = sys.argv[1:]
   force = "--force" in arguments
   saved = saved_arguments(arguments)
   has_saved = len(saved) > 0

   if has_saved:
      for doc_id, url, path in saved:
         store_saved(doc_id, url, path, manifest, force)

      return

   only = [argument for argument in arguments if not argument.startswith("--")] or ["standalone", "live", "archived", "legacy", "web"]

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

   if "web" in only:
      for doc_id, url in WEB_DOCS.items():
         store_web(doc_id, url, manifest, force)


if __name__ == "__main__":
   main()
