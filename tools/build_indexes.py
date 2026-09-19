"""Generate the mechanical index files from cache/manifest.json and data/sources.json.

Writes research/official-material/official-question-index.md (coverage matrix),
scoring-guideline-index.md, student-response-index.md, and research/evidence/source-registry.md.
Hand-written analysis lives in other files; these are regenerated, never edited by hand.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "cache" / "manifest.json").read_text())
SOURCES = json.loads((ROOT / "data" / "sources.json").read_text())["sources"]
INDEX = json.loads((ROOT / "cache" / "page_index.json").read_text()) if (ROOT / "cache" / "page_index.json").exists() else {}
TODAY = str(date.today())
YEARS = list(range(2012, 2027))
DOC_TYPES = [("frq", "FRQ"), ("sg", "Scoring guidelines"), ("samples", "Samples and commentary"), ("stats", "Scoring statistics"), ("dist", "Score distribution"), ("absub", "AB subscore distribution"), ("cr", "Chief Reader report")]


def front(title, purpose):
   return f"---\ntitle: {title}\nresearch_date: {TODAY}\nstatus: generated\npurpose: {purpose}\n---\n\n"


def status_for(doc_id):
   record = MANIFEST.get(doc_id)
   is_missing = record is None or record["status"] != "ok"

   if is_missing:
      return "not_obtained"

   return "ok" if record["tier"] == "live" else "archived_only"


def cell(year, kind):
   yy = f"{year % 100:02d}"

   if kind == "samples":
      states = [status_for(f"samples-{yy}-q{n}") for n in range(1, 7)]
      count = sum(1 for state in states if state != "not_obtained")
      tier = "archived_only" if "archived_only" in states else "ok"
      return f"{tier} ({count}/6)" if count else "not_obtained"

   if kind == "cr":
      states = [status_for(f"cr-{yy}"), status_for(f"crabbc-{yy}")]
      obtained = [state for state in states if state != "not_obtained"]
      return obtained[0] if obtained else "not_obtained"

   return status_for(f"{kind}-{yy}")


def question_pages(doc_id):
   pages = INDEX.get(doc_id, {})
   found = {}

   for page, info in pages.items():
      for question in info["questions"]:
         found.setdefault(question, page)

   return ", ".join(f"Q{q} p.{p}" for q, p in sorted(found.items()))


def source_id(doc_id):
   for source in SOURCES:
      if source.get("doc_id") == doc_id:
         return source["id"]

   return ""


def write_coverage():
   lines = [front("Official Question Coverage Index", "Coverage matrix of every public official AP Calculus BC document by year and type, generated from the cache manifest. States: ok (live on AP Central), archived_only (recovered from the Wayback Machine at the original College Board URL), not_obtained (no public copy found at any tried URL).")]
   lines.append("# Official question coverage index\n\n## Coverage matrix [verified]\n\nGenerated from cache/manifest.json on " + TODAY + ". Source ids are BC-SRC-<doc id>. Years before 2012 were not attempted. 2020 had no standard administration file at the College Board URL pattern [uncertain]. A not_obtained cell is a statement about this project's fetch attempts, not a claim that the document never existed.\n\n")
   lines.append("| Year | " + " | ".join(label for _, label in DOC_TYPES) + " |\n|---|" + "---|" * len(DOC_TYPES) + "\n")

   for year in YEARS:
      lines.append(f"| {year} | " + " | ".join(cell(year, kind) for kind, _ in DOC_TYPES) + " |\n")

   lines.append("\n## Attempted URL templates [verified]\n\nSee tools/fetch_corpus.py for the exact templates: live `https://apcentral.collegeboard.org/media/pdf/ap{YY}-frq-calculus-bc.pdf` and siblings; archived via `https://web.archive.org/web/{ts}id_/<same URL>`; legacy `https://secure-media.collegeboard.org/digitalServices/pdf/ap/apcentral/ap{YY}_calculus_bc_*.pdf`. Every attempt with its HTTP status is recorded in cache/manifest.json (BC-SRC-frq-25 and siblings).\n\n## Question records\n\nOne record per FRQ part lives in data/frq_records.json (ids of the form BC-FRQ, year, question, part). The narrative bank is frq-question-bank.md in this directory once Phase 4 writes it. [verified]\n")
   (ROOT / "research" / "official-material" / "official-question-index.md").write_text("".join(lines))


def write_sg_index():
   lines = [front("Scoring Guideline Index", "Every cached official scoring guideline with its source id, resolved URL, page count, and the page on which each question starts.")]
   lines.append("# Scoring guideline index\n\n## Cached scoring guidelines [verified]\n\n| Year | Doc id | Source id | Tier | Pages | Question start pages | Resolved URL |\n|---|---|---|---|---|---|---|\n")

   for year in YEARS:
      yy = f"{year % 100:02d}"
      doc_id = f"sg-{yy}"
      record = MANIFEST.get(doc_id)
      is_ok = record is not None and record["status"] == "ok"

      if not is_ok:
         lines.append(f"| {year} | {doc_id} | | not_obtained | | | |\n")
         continue

      pages = len(INDEX.get(doc_id, {}))
      lines.append(f"| {year} | {doc_id} | {source_id(doc_id)} | {record['tier']} | {pages} | {question_pages(doc_id)} | {record.get('resolved_url', '')} |\n")

   lines.append("\nThe general scoring notes printed at the head of each guideline are analysed in [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md). Point-type records derived from these documents are in data/scoring_points.json. [verified]\n")
   (ROOT / "research" / "official-material" / "scoring-guideline-index.md").write_text("".join(lines))


def write_samples_index():
   lines = [front("Student Response Index", "Every cached Student Samples and Commentaries document, one per question per year, with page counts and the number of image-only (handwritten) pages that were quarantined from text extraction.")]
   lines.append("# Student response index\n\n## Cached sample documents [verified]\n\nScoring commentary is not a separate College Board document; it is printed inside each per-question samples file together with the sample responses. Handwritten response pages carry no text layer and are listed as quarantined; the commentary pages do extract.\n\n| Year | Question | Doc id | Source id | Tier | Pages | Quarantined pages | Resolved URL |\n|---|---|---|---|---|---|---|---|\n")
   quarantine = json.loads((ROOT / "cache" / "quarantine.json").read_text()) if (ROOT / "cache" / "quarantine.json").exists() else {}

   for year in YEARS:
      yy = f"{year % 100:02d}"

      for question in range(1, 7):
         doc_id = f"samples-{yy}-q{question}"
         record = MANIFEST.get(doc_id)
         is_ok = record is not None and record["status"] == "ok"

         if not is_ok:
            continue

         pages = len(INDEX.get(doc_id, {}))
         lines.append(f"| {year} | {question} | {doc_id} | {source_id(doc_id)} | {record['tier']} | {pages} | {len(quarantine.get(doc_id, []))} | {record.get('resolved_url', '')} |\n")

   (ROOT / "research" / "official-material" / "student-response-index.md").write_text("".join(lines))


def write_source_registry():
   lines = [front("Source Registry", "Every source used by the library: id, title, organisation, URL, resolved URL, fetch date, hash, exam years, type, primary status, and the files that use it. Generated from data/sources.json.")]
   lines.append("# Source registry\n\n## Sources [verified]\n\nGenerated on " + TODAY + ". Primary sources are College Board documents. The `used_by` column is filled by tools/build_indexes.py from ID references found in research/ files.\n\n| Id | Title | Organisation | Type | Primary | Years | Fetch date | Tier | URL | Used by |\n|---|---|---|---|---|---|---|---|---|---|\n")
   usage = {}

   for path in (ROOT / "research").rglob("*.md"):
      text = path.read_text()

      for source in SOURCES:
         doc_id = source.get("doc_id", "")
         is_used = source["id"] in text or (doc_id and (doc_id + ":") in text)

         if is_used:
            usage.setdefault(source["id"], []).append(path.relative_to(ROOT / "research").as_posix())

   for source in SOURCES:
      years = ", ".join(str(year) for year in source.get("exam_years", []))
      used = ", ".join(sorted(usage.get(source["id"], [])))
      lines.append(f"| {source['id']} | {source['title']} | {source['organization']} | {source['source_type']} | {source['primary']} | {years} | {source.get('fetch_date', '')} | {source.get('tier', '')} | {source['url']} | {used} |\n")

   (ROOT / "research" / "evidence" / "source-registry.md").write_text("".join(lines))


if __name__ == "__main__":
   write_coverage()
   write_sg_index()
   write_samples_index()
   write_source_registry()
   print("indexes written")
