"""Every ID referenced anywhere resolves; report orphans."""
import json
import re
from qa_common import ROOT, load_json, all_records, markdown_files, ids_in_text, finish

registry = load_json("ids.json") or {"ids": {}}
known = set(registry["ids"])
failures, warnings = [], []
referenced = set()

for location, record in all_records():
   text = json.dumps(record)
   for identifier in ids_in_text(text):
      referenced.add(identifier)
      is_known = identifier in known

      if not is_known:
         failures.append(f"{record.get('id')} references unknown {identifier}")

link = re.compile(r"\]\(([^)#]+)(#[^)]*)?\)")

for path in markdown_files():
   is_schema_doc = path.name.startswith("PLAN-") or path.name == "README.md"

   if is_schema_doc:
      continue

   text = path.read_text()

   for identifier in ids_in_text(text):
      referenced.add(identifier)
      is_known = identifier in known

      if not is_known:
         failures.append(f"{path.relative_to(ROOT)} references unknown {identifier}")

   for match in link.finditer(text):
      target = match.group(1)
      is_external = target.startswith("http") or target.startswith("mailto:")

      if is_external:
         continue

      resolved = (path.parent / target).resolve()
      is_missing = not resolved.exists()

      if is_missing:
         failures.append(f"{path.relative_to(ROOT)} broken link {target}")

orphans = sorted(identifier for identifier in known if identifier not in referenced)
warnings.extend(f"orphan {identifier}" for identifier in orphans[:40])

if len(orphans) > 40:
   warnings.append(f"{len(orphans) - 40} more orphans")

finish("03_links", failures, warnings)
