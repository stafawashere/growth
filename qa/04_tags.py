"""Every record carries a valid evidence tag and sources; every Markdown H2 section carries a tag or an ID."""
import json
import re
from qa_common import ROOT, CACHE, all_records, markdown_files, EVIDENCE_TAGS, ids_in_text, finish

manifest = json.loads((CACHE / "manifest.json").read_text())
allowed_cr_years = {doc_id for doc_id, record in manifest.items() if doc_id.startswith(("cr-", "crabbc-")) and record["status"] == "ok"}

failures, warnings = [], []
tag_pattern = re.compile(r"\[(verified|single-source|inferred|uncertain)\]")

for location, record in all_records():
   tag = record.get("evidence_tag")
   is_valid = tag in EVIDENCE_TAGS
   needs_sources = tag in ("verified", "single-source")
   has_sources = bool(record.get("sources"))

   if not is_valid:
      failures.append(f"{record.get('id')} bad evidence_tag {tag!r}")

   if needs_sources and not has_sources:
      failures.append(f"{record.get('id')} tagged {tag} without sources")

   uses_chief_reader = any("cr-" in source or "crabbc-" in source for source in record.get("sources", []))
   cited_cr = [source.split(":")[0].replace("BC-SRC-", "") for source in record.get("sources", []) if "cr-" in source or "crabbc-" in source]
   bad_cr = uses_chief_reader and not all(doc in allowed_cr_years for doc in cited_cr)

   if bad_cr:
      failures.append(f"{record.get('id')} cites a chief reader report that is not public")

for path in markdown_files():
   is_index = path.name in ("README.md", "PROGRESS.md") or path.name.startswith("PLAN-")

   if is_index:
      continue

   text = path.read_text()
   sections = re.split(r"^## ", text, flags=re.M)[1:]

   for section in sections:
      heading = section.split("\n", 1)[0][:60]
      has_tag = tag_pattern.search(section) is not None
      has_id = bool(ids_in_text(section))
      is_evidenced = has_tag or has_id

      if not is_evidenced:
         failures.append(f"{path.relative_to(ROOT)} section '{heading}' has no evidence tag or ID")

finish("04_tags", failures, warnings)
