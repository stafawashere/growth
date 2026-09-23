"""Every active BC-PT record carries exactly one deterministic-grading label.

docs/plan/14-token-economy.md open question 2 and the P3 entry criterion in
docs/plan/11-phased-delivery.md ask whether a BC-PT record's `earns` text is fully expressible as
one of the four deterministic checks in docs/plan/03-diagnosis-and-feedback.md. The answer lives in
data/bc_pt_determinism_labels.json, one label per active data/scoring_points.json record.
"""
import json
from qa_common import DATA, load_json, finish

LABEL_VALUES = {"deterministic", "model_required"}

failures = []
warnings = []

scoring_points = load_json("scoring_points.json")
active_ids = {record["id"] for record in scoring_points["point_types"] if record.get("status") != "retired"}

labels_path = DATA / "bc_pt_determinism_labels.json"
labels_doc = json.loads(labels_path.read_text())
entries = labels_doc.get("labels", [])

seen_ids = []
by_id = {}

for entry in entries:
   entry_id = entry.get("id")
   label = entry.get("label")
   reason = entry.get("reason")
   has_reason = isinstance(reason, str) and len(reason.strip()) > 0

   if label not in LABEL_VALUES:
      failures.append(f"{entry_id} carries an unrecognised label {label!r}")

   if not has_reason:
      failures.append(f"{entry_id} carries no reason")

   seen_ids.append(entry_id)
   by_id.setdefault(entry_id, 0)
   by_id[entry_id] += 1

duplicates = sorted(entry_id for entry_id, count in by_id.items() if count > 1)

for entry_id in duplicates:
   failures.append(f"{entry_id} carries more than one label")

missing = sorted(active_ids - set(seen_ids))

for entry_id in missing:
   failures.append(f"{entry_id} is active and carries no label")

extra = sorted(set(seen_ids) - active_ids)

for entry_id in extra:
   failures.append(f"{entry_id} is labelled but is not an active BC-PT record")

deterministic = sum(1 for entry in entries if entry.get("label") == "deterministic")
model_required = sum(1 for entry in entries if entry.get("label") == "model_required")
print(f"15_determinism_labels: {len(active_ids)} active BC-PT records, "
      f"{deterministic} deterministic, {model_required} model_required")

finish("15_determinism_labels", failures, warnings)
