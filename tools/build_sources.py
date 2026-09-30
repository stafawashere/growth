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

TYPE_BY_PREFIX = {"frq": "free_response_questions", "sg": "scoring_guidelines", "samples": "student_samples_and_commentary", "stats": "scoring_statistics", "dist": "score_distribution", "absub": "ab_subscore_distribution", "cr": "chief_reader_report", "crabbc": "chief_reader_report", "web": "web_page", "desmos": "tool_documentation"}
ORGANIZATION_BY_PREFIX = {"web": "College Board", "hybrid": "College Board", "desmos": "Desmos Studio PBC"}

WEB_TITLES = {
   "web-bc-course": "AP Calculus BC Course page",
   "web-bc-exam": "AP Calculus BC Exam page",
   "web-bc-past": "AP Calculus BC Past Exam Questions",
   "web-bc-students": "AP Calculus BC assessment page for students",
   "web-calc-policy": "AP calculator policies",
   "web-calc-policy-central": "AP calculator policy for exam administrators",
   "web-ab-subscore": "Special score structure for Calculus BC",
   "web-exam-dates": "AP exam dates",
   "web-score-setting": "Score setting and scoring",
   "web-equating": "What equating processes does AP use",
   "web-key-changes": "AP Calculus updates key changes",
   "web-bluebook-tools": "Bluebook tools for students",
   "hybrid-booklets-2026": "AP hybrid digital exams free-response booklets overview",
   "desmos-cb-calculators-pdf": "Desmos calculators for College Board AP and SAT",
   "desmos-default-testing-pdf": "Default Desmos testing calculators",
   "desmos-user-guide-pdf": "Desmos Graphing Calculator User Guide (PDF)",
   "desmos-api-docs": "Desmos API v1.12 documentation",
   "desmos-terms": "Desmos Terms of Service",
   "desmos-api-terms": "Desmos API Terms of Service",
   "desmos-testing": "Desmos testing and assessments",
   "desmos-graphing-shortcuts": "Desmos Graphing Calculator Keyboard Shortcuts",
   "desmos-help-assessment-faq": "Assessment Resources and FAQ",
   "desmos-help-testing-calculators": "Practice With Testing Calculators",
   "desmos-help-in-class-assessments": "Using Desmos on In-Class Assessments",
   "desmos-help-integrals": "Integrals",
   "desmos-help-derivatives": "Derivatives",
   "desmos-help-supported-functions": "Supported Functions",
   "desmos-help-getting-started": "Getting Started with the Desmos Graphing Calculator",
   "desmos-help-graph-settings": "Graph Settings",
   "desmos-help-trigonometry": "Trigonometry",
   "desmos-help-functions": "Functions",
   "desmos-help-tables": "Tables",
   "desmos-help-sliders": "Sliders and Movable Points in a Graph",
   "desmos-help-keyboard-shortcuts": "Keyboard Shortcuts",
   "desmos-help-restrictions": "Inequalities and Restrictions",
   "desmos-help-regressions": "Regressions",
   "desmos-help-faqs": "FAQs",
   "desmos-help-user-guide": "Desmos Graphing Calculator User Guide",
   "desmos-help-whats-new": "What's New at Desmos Studio",
   "desmos-help-api-plans": "API Plans for Commercial Use",
}


def year_of(doc_id):
   parts = doc_id.split("-")
   is_year = len(parts) > 1 and parts[1].isdigit() and len(parts[1]) == 2
   return [2000 + int(parts[1])] if is_year else []


def organization_of(doc_id, url):
   prefix = doc_id.split("-")[0]
   is_college_board_url = "collegeboard.org" in url

   if is_college_board_url:
      return "College Board"

   return ORGANIZATION_BY_PREFIX.get(prefix, "College Board")


def title_of(doc_id):
   return WEB_TITLES.get(doc_id, doc_id.replace("-", " "))


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
      is_web = record.get("kind") == "web"
      source_type = "web_page" if is_web else TYPE_BY_PREFIX.get(prefix, "course_document")
      previous = by_doc.get(doc_id)
      identifier = previous["id"] if previous else register("BC-SRC-" + doc_id, doc_id)
      sources.append({
         "id": identifier, "name": doc_id, "scope": "n/a", "evidence_tag": "verified", "sources": [doc_id],
         "title": title_of(doc_id), "organization": organization_of(doc_id, record["requested_url"]), "url": record["requested_url"],
         "resolved_url": record.get("resolved_url", ""), "doc_id": doc_id, "sha256": record["sha256"],
         "fetch_date": record["fetch_date"], "exam_years": year_of(doc_id), "source_type": source_type,
         "primary": True, "tier": record["tier"], "used_by": previous.get("used_by", []) if previous else [],
      })

   for key, title, url, source_type in WEB_PAGES:
      is_cached = manifest.get(key, {}).get("status") == "ok"

      if is_cached:
         continue

      previous = by_doc.get(key)
      identifier = previous["id"] if previous else register("BC-SRC-" + key, key)
      sources.append({"id": identifier, "name": key, "scope": "n/a", "evidence_tag": "verified" if "gott" not in key else "single-source", "sources": [url], "title": title, "organization": "College Board" if "gott" not in key else "teachingcalculus.com", "url": url, "doc_id": key, "fetch_date": str(date.today()), "exam_years": [], "source_type": source_type, "primary": "gott" not in key, "used_by": previous.get("used_by", []) if previous else []})

   OUT.write_text(json.dumps({"sources": sources}, indent=1))
   print(len(sources), "sources")


if __name__ == "__main__":
   main()
