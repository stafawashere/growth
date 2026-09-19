"""Re-check every source URL (HEAD via curl) and report status changes. Network required."""
import subprocess
from qa_common import load_json, finish

failures, warnings = [], []
sources = load_json("sources.json")

if sources is None:
   finish("11_freshness", ["sources.json missing"])

for source in sources["sources"]:
   url = source["url"]
   result = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "-A", "Mozilla/5.0", "--max-time", "30", "-w", "%{http_code}", url], capture_output=True, text=True)
   code = result.stdout.strip()
   is_alive = code == "200"

   if not is_alive:
      warnings.append(f"{source['id']} {url} -> {code}")

finish("11_freshness", failures, warnings)
