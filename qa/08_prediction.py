"""No predictive language outside the historical-frequency file."""
import re
from qa_common import ROOT, markdown_files, FORBIDDEN_PREDICTION, finish

failures = []

for path in markdown_files():
   is_exempt = path.name in ("historical-frequency.md",) or path.name.startswith("PLAN-") or path.name == "README.md"

   if is_exempt:
      continue

   for line_number, line in enumerate(path.read_text().splitlines(), 1):
      for pattern in FORBIDDEN_PREDICTION:
         if re.search(pattern, line, re.I):
            failures.append(f"{path.relative_to(ROOT)}:{line_number} predictive phrasing: {line.strip()[:80]}")

finish("08_prediction", failures)
