"""Every cached document has a file whose hash matches and extracted text."""
import hashlib
import json
from qa_common import CACHE, finish

manifest = json.loads((CACHE / "manifest.json").read_text())
failures, warnings = [], []

for doc_id, record in sorted(manifest.items()):
   is_ok = record["status"] == "ok"

   if not is_ok:
      warnings.append(f"{doc_id} not obtained ({record['tier']})")
      continue

   pdf = CACHE / "pdf" / f"{record['sha256']}.pdf"
   has_pdf = pdf.exists()

   if not has_pdf:
      failures.append(f"{doc_id} pdf missing")
      continue

   digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
   hash_matches = digest == record["sha256"]

   if not hash_matches:
      failures.append(f"{doc_id} hash mismatch")

   meta = CACHE / "text" / doc_id / "meta.json"
   has_text = meta.exists()

   if not has_text:
      failures.append(f"{doc_id} text not extracted")

finish("00_manifest", failures, warnings)
