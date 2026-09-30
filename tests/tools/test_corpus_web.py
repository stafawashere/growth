"""Web pages are first-class cached documents: fetched or browser-saved, extracted to one page,
checked by qa/00_manifest.py, and listed in data/sources.json as web_page records."""
import hashlib
import importlib.util
import json
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "qa"))

# The PDF path of extract_text needs PyMuPDF, which the test environment does not have.
sys.modules.setdefault("pymupdf", types.ModuleType("pymupdf"))

import build_sources  # noqa: E402
import extract_text  # noqa: E402
import fetch_corpus  # noqa: E402
import mint_id  # noqa: E402

manifest_spec = importlib.util.spec_from_file_location("manifest_check", ROOT / "qa" / "00_manifest.py")
manifest_check = importlib.util.module_from_spec(manifest_spec)
manifest_spec.loader.exec_module(manifest_check)

PAGE_HTML = b"""<html><head><title>Calculator Policy</title>
<style>.banner { color: red; }</style>
<script>var trackingPixel = "leaked";</script></head>
<body><nav><a href="/">Site menu</a></nav>
<p>Use an approved calculator &amp; the Desmos calculator in Bluebook.</p>
<footer>Copyright footer</footer></body></html>"""


def sha(data):
   return hashlib.sha256(data).hexdigest()


@pytest.fixture
def cache(tmp_path, monkeypatch):
   cache_dir = tmp_path / "cache"
   (cache_dir / "pdf").mkdir(parents=True)
   (cache_dir / "web").mkdir()
   (cache_dir / "text").mkdir()

   for module in (fetch_corpus, extract_text):
      monkeypatch.setattr(module, "PDF_DIR", cache_dir / "pdf")
      monkeypatch.setattr(module, "WEB_DIR", cache_dir / "web")
      monkeypatch.setattr(module, "MANIFEST", cache_dir / "manifest.json")

   monkeypatch.setattr(extract_text, "TEXT_DIR", cache_dir / "text")
   monkeypatch.setattr(extract_text, "QUARANTINE", cache_dir / "quarantine.json")
   return cache_dir


def stub_fetch(monkeypatch, status, body):
   monkeypatch.setattr(fetch_corpus, "fetch_with_retry", lambda url: (status, "", body))


def test_html_page_is_stored_under_cache_web_with_its_hash(cache, monkeypatch):
   stub_fetch(monkeypatch, 200, PAGE_HTML)
   manifest = {}
   fetch_corpus.store_web("web-calc-policy", "https://example.org/policy", manifest)
   record = manifest["web-calc-policy"]

   assert record["status"] == "ok"
   assert record["kind"] == "web" and record["format"] == "html" and record["fetch_method"] == "curl"
   assert record["sha256"] == sha(PAGE_HTML)
   assert (cache / "web" / f"{sha(PAGE_HTML)}.html").read_bytes() == PAGE_HTML
   assert json.loads((cache / "manifest.json").read_text())["web-calc-policy"] == record


def test_pdf_answer_is_stored_as_a_plain_pdf_record(cache, monkeypatch):
   body = b"%PDF-1.7 booklet"
   stub_fetch(monkeypatch, 200, body)
   manifest = {}
   fetch_corpus.store_web("hybrid-booklets-2026", "https://example.org/booklet.pdf", manifest)
   record = manifest["hybrid-booklets-2026"]

   assert record["status"] == "ok"
   assert "kind" not in record
   assert (cache / "pdf" / f"{sha(body)}.pdf").exists()


def test_refused_fetch_stays_missing(cache, monkeypatch):
   stub_fetch(monkeypatch, 403, b"<html>Forbidden</html>")
   manifest = {}
   fetch_corpus.store_web("web-key-changes", "https://example.org/key-changes", manifest)

   assert manifest["web-key-changes"]["status"] == "missing"
   assert manifest["web-key-changes"]["attempts"][0]["http"] == 403
   assert list((cache / "web").iterdir()) == []


def test_saved_dir_ingests_browser_text_with_derived_doc_ids(cache, tmp_path, monkeypatch):
   saved = tmp_path / "saved"
   saved.mkdir()
   known = saved / "4406810279693-Integrals.txt"
   known.write_text("Source: https://help.desmos.com/hc/en-us/articles/4406810279693-Integrals\nTitle: Integrals\n\nIntegrals body\n")
   unlisted = saved / "123456-Polar-Graphing.txt"
   unlisted.write_text("Source: https://help.desmos.com/hc/en-us/articles/123456-Polar-Graphing\nCaptured: 2026-09-29\n\nPolar body\n")
   (saved / "notes.txt").write_text("no header here\n")
   monkeypatch.setattr(sys, "argv", ["fetch_corpus.py", "--saved-dir", str(saved)])
   fetch_corpus.main()
   manifest = json.loads((cache / "manifest.json").read_text())

   assert sorted(manifest) == ["desmos-help-integrals", "desmos-help-polar-graphing"]
   record = manifest["desmos-help-polar-graphing"]
   assert record["requested_url"] == "https://help.desmos.com/hc/en-us/articles/123456-Polar-Graphing"
   assert record["format"] == "text" and record["fetch_method"] == "browser_saved_text"
   assert record["saved_from"] == "123456-Polar-Graphing.txt"
   assert (cache / "web" / f"{record['sha256']}.txt").read_bytes() == unlisted.read_bytes()


def test_saved_pair_takes_the_given_doc_id(cache, tmp_path, monkeypatch):
   page = tmp_path / "terms.txt"
   page.write_text("Source: https://www.desmos.com/terms\nCaptured: 2026-09-29\n\nTerms body\n")
   monkeypatch.setattr(sys, "argv", ["fetch_corpus.py", "--saved", "desmos-terms", "https://www.desmos.com/terms", str(page)])
   fetch_corpus.main()
   manifest = json.loads((cache / "manifest.json").read_text())

   assert list(manifest) == ["desmos-terms"]
   assert manifest["desmos-terms"]["resolved_url"] == "https://www.desmos.com/terms"


def write_web_record(cache, doc_id, body, text_format):
   suffix = "html" if text_format == "html" else "txt"
   (cache / "web" / f"{sha(body)}.{suffix}").write_bytes(body)
   record = {"doc_id": doc_id, "status": "ok", "tier": "live", "kind": "web", "format": text_format, "sha256": sha(body)}
   (cache / "manifest.json").write_text(json.dumps({doc_id: record}))
   return record


def test_extract_html_drops_scripts_and_chrome_and_unescapes(cache, monkeypatch):
   write_web_record(cache, "web-calc-policy", PAGE_HTML, "html")
   monkeypatch.setattr(sys, "argv", ["extract_text.py"])
   extract_text.main()
   out_dir = cache / "text" / "web-calc-policy"
   primary = (out_dir / "page-001.txt").read_text()
   meta = json.loads((out_dir / "meta.json").read_text())

   assert "Use an approved calculator & the Desmos calculator in Bluebook." in primary
   assert "trackingPixel" not in primary
   assert "color: red" not in primary
   assert "Site menu" not in primary
   assert "Copyright footer" not in primary
   assert "\n\n\n" not in primary
   assert "calculator & the Desmos" in (out_dir / "page-001.raw.txt").read_text()
   assert meta["pages"] == 1 and meta["kind"] == "web" and meta["sha256"] == sha(PAGE_HTML)


def test_extract_saved_text_copies_the_body(cache, monkeypatch):
   body = "Source: https://www.desmos.com/testing\nCaptured: 2026-09-29\n\nRestrict with {x<3}  and  <b>tags</b> &amp; text.\n\n\n\nEnd\n".encode()
   write_web_record(cache, "desmos-testing", body, "text")
   monkeypatch.setattr(sys, "argv", ["extract_text.py"])
   extract_text.main()
   out_dir = cache / "text" / "desmos-testing"

   assert (out_dir / "page-001.txt").read_bytes() == body
   assert (out_dir / "page-001.raw.txt").read_bytes() == body


def test_manifest_check_covers_web_records(cache):
   record = write_web_record(cache, "desmos-terms", b"Source: x\n\nTerms\n", "text")
   (cache / "text" / "desmos-terms").mkdir()
   (cache / "text" / "desmos-terms" / "meta.json").write_text("{}")

   assert manifest_check.check_record(record, cache) == []

   (cache / "web" / f"{record['sha256']}.txt").write_bytes(b"tampered")
   assert manifest_check.check_record(record, cache) == ["desmos-terms hash mismatch"]

   (cache / "web" / f"{record['sha256']}.txt").unlink()
   assert manifest_check.check_record(record, cache) == ["desmos-terms web txt missing"]


def test_manifest_check_requires_extracted_text_for_web_records(cache):
   record = write_web_record(cache, "web-bc-exam", PAGE_HTML, "html")

   assert manifest_check.check_record(record, cache) == ["web-bc-exam text not extracted"]


def test_build_sources_emits_web_pages_and_keeps_previous_ids(tmp_path, monkeypatch):
   manifest = {
      "web-calc-policy": {"doc_id": "web-calc-policy", "status": "ok", "tier": "live", "kind": "web", "format": "html", "requested_url": "https://apstudents.collegeboard.org/exam-policies-guidelines/calculator-policies", "resolved_url": "https://apstudents.collegeboard.org/exam-policies-guidelines/calculator-policies", "sha256": "a" * 64, "fetch_date": "2026-09-29"},
      "desmos-help-integrals": {"doc_id": "desmos-help-integrals", "status": "ok", "tier": "live", "kind": "web", "format": "text", "requested_url": "https://help.desmos.com/hc/en-us/articles/4406810279693-Integrals", "resolved_url": "https://help.desmos.com/hc/en-us/articles/4406810279693-Integrals", "sha256": "b" * 64, "fetch_date": "2026-09-29"},
   }
   previous = {"id": "BC-SRC-web-calc-policy", "doc_id": "web-calc-policy", "used_by": ["BC-QA-00001"]}
   (tmp_path / "manifest.json").write_text(json.dumps(manifest))
   (tmp_path / "sources.json").write_text(json.dumps({"sources": [previous]}))
   (tmp_path / "ids.json").write_text(json.dumps({"ids": {}}))
   monkeypatch.setattr(build_sources, "MANIFEST", tmp_path / "manifest.json")
   monkeypatch.setattr(build_sources, "OUT", tmp_path / "sources.json")
   monkeypatch.setattr(mint_id, "IDS", tmp_path / "ids.json")
   build_sources.main()
   sources = json.loads((tmp_path / "sources.json").read_text())["sources"]
   policy = [source for source in sources if source["doc_id"] == "web-calc-policy"]
   integrals = [source for source in sources if source["doc_id"] == "desmos-help-integrals"]

   assert len(policy) == 1
   assert policy[0]["id"] == "BC-SRC-web-calc-policy"
   assert policy[0]["used_by"] == ["BC-QA-00001"]
   assert policy[0]["source_type"] == "web_page" and policy[0]["organization"] == "College Board"
   assert policy[0]["sha256"] == "a" * 64 and policy[0]["tier"] == "live"
   assert integrals[0]["source_type"] == "web_page"
   assert integrals[0]["organization"] == "Desmos Studio PBC"
   assert integrals[0]["title"] == "Integrals"
   assert "BC-SRC-desmos-help-integrals" in json.loads((tmp_path / "ids.json").read_text())["ids"]
