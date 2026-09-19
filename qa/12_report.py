"""Run every check, summarise, and print counters for PROGRESS.md."""
import json
import subprocess
import sys
from pathlib import Path
from qa_common import ROOT, load_json, REGISTRY_FILES

checks = sorted(path for path in (ROOT / "qa").glob("[0-9][0-9]_*.py") if not path.name.startswith("12") and not path.name.startswith("11"))
include_network = "--network" in sys.argv

if include_network:
   checks.append(ROOT / "qa" / "11_freshness.py")

summary = {}

for check in checks:
   result = subprocess.run([sys.executable, str(check)], capture_output=True, text=True, cwd=ROOT / "qa")
   last = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else result.stderr.strip()[-200:]
   summary[check.stem] = {"exit": result.returncode, "summary": last}
   print(f"{'PASS' if result.returncode == 0 else 'FAIL'} {check.stem}: {last}")

counts = {}
seen = set()

for prefix, location in REGISTRY_FILES.items():
   file_name, key = location.split(":")

   if (file_name, key) in seen:
      continue

   seen.add((file_name, key))
   data = load_json(file_name)
   counts[f"{file_name}:{key}"] = len(data[key]) if data and key in data else 0

manifest = json.loads((ROOT / "cache" / "manifest.json").read_text())
counts["cache:documents_ok"] = sum(1 for record in manifest.values() if record["status"] == "ok")
counts["cache:documents_missing"] = sum(1 for record in manifest.values() if record["status"] != "ok")
print(json.dumps(counts, indent=1))
(ROOT / "qa" / "last_report.json").write_text(json.dumps({"checks": summary, "counts": counts}, indent=1))
all_pass = all(entry["exit"] == 0 for entry in summary.values())
sys.exit(0 if all_pass else 1)
