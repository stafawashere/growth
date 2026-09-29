"""Every cached document has a file whose hash matches and extracted text."""
import hashlib
import json
from qa_common import CACHE, finish


def cached_file(record, cache_dir):
   is_web = record.get("kind") == "web"

   if not is_web:
      return cache_dir / "pdf" / f"{record['sha256']}.pdf", "pdf"

   is_html = record.get("format") == "html"
   suffix = "html" if is_html else "txt"
   return cache_dir / "web" / f"{record['sha256']}.{suffix}", f"web {suffix}"


def check_record(record, cache_dir):
   doc_id = record["doc_id"]
   path, label = cached_file(record, cache_dir)
   has_file = path.exists()

   if not has_file:
      return [f"{doc_id} {label} missing"]

   failures = []
   digest = hashlib.sha256(path.read_bytes()).hexdigest()
   hash_matches = digest == record["sha256"]

   if not hash_matches:
      failures.append(f"{doc_id} hash mismatch")

   meta = cache_dir / "text" / doc_id / "meta.json"
   has_text = meta.exists()

   if not has_text:
      failures.append(f"{doc_id} text not extracted")

   return failures


def main():
   manifest = json.loads((CACHE / "manifest.json").read_text())
   failures, warnings = [], []

   for doc_id, record in sorted(manifest.items()):
      is_ok = record["status"] == "ok"

      if not is_ok:
         warnings.append(f"{doc_id} not obtained ({record['tier']})")
         continue

      failures.extend(check_record(record, CACHE))

   finish("00_manifest", failures, warnings)


if __name__ == "__main__":
   main()
