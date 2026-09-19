"""Generate data/sources.json from cache/manifest.json plus hand-listed web pages. Deterministic ordering by doc_id."""
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from mint_id import register  # noqa: E402

MANIFEST = ROOT / "cache" / "manifest.json"
OUT = ROOT / "data" / "sources.json"

WEB_PAGES = [
   ("web-bc-course", "AP Calculus BC Course page", "https://apcentral.collegeboard.org/courses/ap-calculus-bc", "web_page"),
   ("web-bc-exam", "AP Calculus BC Exam page", "https://apcentral.collegeboard.org/courses/ap-calculus-bc/exam", "web_page"),
   ("web-bc-past", "AP Calculus BC Past Exam Questions", "https://apcentral.collegeboard.org/courses/ap-calculus-bc/exam/past-exam-questions", "web_page"),
   ("web-bc-students", "AP Calculus BC assessment page for students", "https://apstudents.collegeboard.org/courses/ap-calculus-bc/assessment", "web_page"),
   ("web-calc-policy", "AP calculator policies", "https://apstudents.collegeboard.org/exam-policies-guidelines/calculator-policies", "web_page"),
   ("web-ab-subscore", "Special score structure for Calculus BC", "https://apstudents.collegeboard.org/about-ap-scores/special-score-structure-calculus-bc", "web_page"),
   ("web-exam-dates", "AP exam dates", "https://apcentral.collegeboard.org/exam-administration-ordering-scores/exam-dates", "web_page"),
   ("web-score-setting", "Score setting and scoring", "https://apcentral.collegeboard.org/courses/how-ap-develops-courses-and-exams/score-setting-and-scoring", "web_page"),
   ("web-equating", "What equating processes does AP use", "https://apcentral.collegeboard.org/help-center/what-equating-processes-does-ap-use", "web_page"),
   ("web-key-changes", "AP Calculus updates key changes (403 to direct fetch on 2026-09-19)", "https://apcentral.collegeboard.org/courses/resources/ap-calculus-updates-key-changes", "web_page"),
   ("web-gott-index", "Ted Gott Exam Index (teachingcalculus.com), secondary", "https://teachingcalculus.com/2017/03/29/ted-gotts-exam-index/", "secondary_index"),
]

TYPE_BY_PREFIX = {"frq": "free_response_questions", "sg": "scoring_guidelines", "samples": "student_samples_and_commentary", "stats": "scoring_statistics", "dist": "score_distribution", "absub": "ab_subscore_distribution", "cr": "chief_reader_report", "crabbc": "chief_reader_report"}


def year_of(doc_id):
   parts = doc_id.split("-")
   is_year = len(parts) > 1 and parts[1].isdigit() and len(parts[1]) == 2
   return [2000 + int(parts[1])] if is_year else []


def main():
   manifest = json.loads(MANIFEST.read_text())
   existing = json.loads(OUT.read_text())["sources"] if OUT.exists() else []
   by_doc = {source.get("doc_id"): source for source in existing}
   sources = []

   for doc_id, record in sorted(manifest.items()):
      is_ok = record["status"] == "ok"

      if not is_ok:
         continue

      prefix = doc_id.split("-")[0]
      source_type = TYPE_BY_PREFIX.get(prefix, "course_document")
      previous = by_doc.get(doc_id)
      identifier = previous["id"] if previous else register("BC-SRC-" + doc_id, doc_id)
      sources.append({
         "id": identifier, "name": doc_id, "scope": "n/a", "evidence_tag": "verified", "sources": [doc_id],
         "title": doc_id.replace("-", " "), "organization": "College Board", "url": record["requested_url"],
         "resolved_url": record.get("resolved_url", ""), "doc_id": doc_id, "sha256": record["sha256"],
         "fetch_date": record["fetch_date"], "exam_years": year_of(doc_id), "source_type": source_type,
         "primary": True, "tier": record["tier"], "used_by": previous.get("used_by", []) if previous else [],
      })

   for key, title, url, source_type in WEB_PAGES:
      previous = by_doc.get(key)
      identifier = previous["id"] if previous else register("BC-SRC-" + key, key)
      sources.append({"id": identifier, "name": key, "scope": "n/a", "evidence_tag": "verified" if "gott" not in key else "single-source", "sources": [url], "title": title, "organization": "College Board" if "gott" not in key else "teachingcalculus.com", "url": url, "doc_id": key, "fetch_date": str(date.today()), "exam_years": [], "source_type": source_type, "primary": "gott" not in key, "used_by": previous.get("used_by", []) if previous else []})

   OUT.write_text(json.dumps({"sources": sources}, indent=1))
   print(len(sources), "sources")


if __name__ == "__main__":
   main()
