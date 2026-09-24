"""Validate every golden set and write docs/operator/golden-sets.md, the inventory and the $0.00
baselines that can be measured before the roles exist.

   .venv/bin/python tools/golden_sets.py

Exits 1 when any set fails validation, so the record is never written over a broken set.
"""
import sys
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.content.loader import load_snapshot  # noqa: E402
from app.evals import golden  # noqa: E402
from app.runtime.context import DEFAULT_CONTENT_ROOT  # noqa: E402

RECORD_PATH = REPOSITORY_ROOT / "docs" / "operator" / "golden-sets.md"

MEASURED_WHEN = {
   "tutor": "now, on any recorded or live tutor sentence, once a sentence is labelled against the four checks",
   "grader": "when P3 wires the grader; per-point-type exact match with its count, kappa with its interval",
   "transcriber": "when P3 wires the transcriber and each page has been written by hand and photographed",
   "diagnostician": "when P3 wires the diagnostician; observed-error exact match and top-hypothesis agreement",
   "generator": "now as a regression guard on the bank's frozen keys; as a generator eval when P4 wires the generator",
   "verifier": "now, for the deterministic checks; for the model verifier when P4 wires it",
}

BREAKDOWN_FIELD = {
   "tutor": "acceptable",
   "grader": "category",
   "transcriber": "variation",
   "diagnostician": "archetype_id",
   "generator": "calculator",
   "verifier": "defect",
}


def breakdown(role, cases):
   field = BREAKDOWN_FIELD[role]
   counts = Counter(str(case.get(field)) for case in cases)
   is_long = len(counts) > 8

   if is_long:
      return f"{len(counts)} distinct {field} values"

   return ", ".join(f"{name} {count}" for name, count in sorted(counts.items()))


def main():
   library = golden.load_library()
   sets = {role: golden.load_set(role) for role in golden.ROLES}
   problems = {role: golden.validate(role, sets[role], library) for role in golden.ROLES}
   failing = {role: found for role, found in problems.items() if found}

   if failing:
      for role, found in failing.items():
         for problem in found:
            print(f"{role}: {problem}")

      return 1

   snapshot = load_snapshot(DEFAULT_CONTENT_ROOT)
   verifier = sets["verifier"]
   detection = golden.detection_by_defect(verifier, golden.deterministic_verifier_verdicts(verifier, snapshot))
   grader = sets["grader"]
   earned = sum(1 for case in grader["cases"] if case["earned"])

   lines = [
      "---",
      "title: Golden sets",
      "research_date: 2026-09-24",
      "status: recorded",
      "purpose: The golden set for every model role, who wrote and labelled each, what each measures and when, and the baselines measurable at no model cost.",
      "---",
      "",
      "# Golden sets",
      "",
      "Written by `tools/golden_sets.py`. Every set in `content/golden/` was authored and labelled by claude-opus-5-5 on the operator's delegation of 2026-09-24. None is a human's work and none has been reviewed by a human. Where 10 and 11 say the operator authors or verifies a set, a model did it and each file says so in its `authored_by` and `labelled_by` lines. `app/evals/golden.py` validates each set before any number is read off it, and every set passed on this run.",
      "",
      "| Role | Set | Cases | Breakdown | Measured |",
      "|---|---|---|---|---|",
   ]

   for role in golden.ROLES:
      document = sets[role]
      lines.append(
         f"| {role} | {document['set']} | {len(document['cases'])} | {breakdown(role, document['cases'])} | {MEASURED_WHEN[role]} |"
      )

   lines.extend([
      "",
      f"The grader set labels {earned} of {len(grader['cases'])} responses earned. It covers the {len(golden.judged_point_types(library['scoring_points']))} BC-PT records that reach a model, five responses each, one per adversarial category of 10. 10 asks for 30 point types drawn from those that reach a model, and only 17 exist, so 17 by 5 is the whole population rather than a sample of it.",
      "",
      "## Deterministic verifier baseline",
      "",
      "The checks `app/items/ingest.py` runs on the way into the bank, plus the distractor-path rule, scored against the verifier set. A case counts as caught when the verdict matches the expected one; the none row is the control, whose expected verdict is accept.",
      "",
      "| Defect | Caught | Cases |",
      "|---|---|---|",
   ])

   for defect in golden.VERIFIER_DEFECTS:
      caught, total = detection.get(defect, (0, 0))
      lines.append(f"| {defect} | {caught} | {total} |")

   lines.extend([
      "",
      "Every kind the checks do not catch is a defect only the independent re-solve and the model verifier of 04 can catch, which is the reason P4 keeps both.",
      "",
   ])

   RECORD_PATH.write_text("\n".join(lines))
   print(f"wrote {RECORD_PATH.relative_to(REPOSITORY_ROOT)}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
