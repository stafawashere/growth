"""The golden sets for every model role (docs/plan/11 P7 scope item 1; 10 "Model-output evals";
13 "Golden set" sections), and the agreement measures each is scored with.

The sets live in content/golden/<role>.json. Every one was authored and labelled by a model on the
operator's delegation and says so in its authored_by and labelled_by lines; none is a human's work
and nothing here reports it as one. validate() is the contract a set must meet before any number
is read off it: the author lines, unique case ids, every library id active, and the per-role rules
below. Agreement is computed against a role's predictions, a mapping from case id to the role's
decision, so the same code scores a replayed model, a live model or a deterministic baseline.

Two roles can be measured today at $0.00. The verifier's deterministic checks
(app/items/ingest.run_checks plus the distractor-path rule) are scored on the verifier set as a
baseline, and the generator set is a regression guard that the bank still carries the frozen keys.
The grader, the diagnostician and the transcriber arrive with P3 and the generator with P4; their
sets are validated now and scored when the role exists. The transcriber set has no images: every
page is a specification and a reference transcript waiting for a photograph of a hand-written page,
which no session can take.
"""
import json
import math
from dataclasses import dataclass
from pathlib import Path

from app.items.distractor_paths import distractor_path_violations, error_ids_for_skills
from app.items.ingest import run_checks

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = REPOSITORY_ROOT / "content" / "golden"
ROLES = ("tutor", "grader", "transcriber", "diagnostician", "generator", "verifier")
DELEGATION_MARK = "on the operator's delegation of"
GRADER_CATEGORIES = (
   "fully_correct",
   "unconventional_valid",
   "narrow_fail",
   "notation_failure",
   "eligible_after_error",
)
VERIFIER_DEFECTS = (
   "none",
   "wrong_key",
   "distractor_equals_key",
   "duplicate_distractors",
   "unresolvable_error_path",
   "calculator_boundary",
   "wrong_worked_step",
)
TUTOR_CHECKS = ("names_rule", "states_consequence", "describes_correct_response")
FORBIDDEN_DASHES = (chr(0x2013), chr(0x2014))
Z_95 = 1.959963984540054


def load_set(role, directory=GOLDEN_DIR):
   return json.loads((Path(directory) / f"{role}.json").read_text())


def active_ids(records):
   return {record["id"] for record in records if record.get("status", "active") == "active"}


def bank_items(repository_root=REPOSITORY_ROOT):
   items = {}

   for path in sorted(Path(repository_root, "content").glob("items_*/ITM-*.json")):
      record = json.loads(path.read_text())
      items[record["id"]] = record

   return items


def judged_point_types(scoring_points):
   """The BC-PT records that reach a model (10, corrected 2026-09-20): active, and yes on at least
   one of justification_required, interpretation_required, hypotheses_required."""
   fields = ("justification_required", "interpretation_required", "hypotheses_required")

   return {
      record["id"]
      for record in scoring_points
      if record.get("status", "active") == "active" and any(record.get(name) == "yes" for name in fields)
   }


def header_problems(role, golden):
   problems = []
   expected = {"role", "set", "authored_by", "labelled_by", "authored_on", "note", "cases"}
   missing = expected - set(golden)

   if missing:
      problems.append(f"{role}: missing keys {sorted(missing)}")

   for field in ("authored_by", "labelled_by"):
      names_the_delegation = DELEGATION_MARK in golden.get(field, "")

      if not names_the_delegation:
         problems.append(f"{role}: {field} does not name the delegation it was written under")

   is_role = golden.get("role") == role

   if not is_role:
      problems.append(f"{role}: file names role {golden.get('role')!r}")

   case_ids = [case.get("id") for case in golden.get("cases", [])]

   if len(case_ids) != len(set(case_ids)):
      problems.append(f"{role}: duplicate case ids")

   text = json.dumps(golden, ensure_ascii=False)

   if any(dash in text for dash in FORBIDDEN_DASHES):
      problems.append(f"{role}: carries an en or em dash")

   return problems


def grader_problems(golden, library):
   judged = judged_point_types(library["scoring_points"])
   problems = []
   seen = {}

   for case in golden["cases"]:
      point_type = case.get("point_type_id")
      category = case.get("category")

      if point_type not in judged:
         problems.append(f"{case['id']}: {point_type} is not a point type that reaches a model")

      if category not in GRADER_CATEGORIES:
         problems.append(f"{case['id']}: unknown category {category!r}")

      if not isinstance(case.get("earned"), bool):
         problems.append(f"{case['id']}: earned is not a boolean")

      seen.setdefault(point_type, set()).add(category)

   for point_type in sorted(judged):
      covered = seen.get(point_type, set())

      if covered != set(GRADER_CATEGORIES):
         problems.append(f"{point_type}: categories {sorted(covered)} do not cover all five")

   return problems


def diagnostician_problems(golden, library):
   errors = {record["id"]: record for record in library["errors"] if record.get("status", "active") == "active"}
   misconceptions = active_ids(library["misconceptions"])
   items = library["items"]
   problems = []

   for case in golden["cases"]:
      item = items.get(case.get("item_id"))

      if item is None:
         problems.append(f"{case['id']}: {case.get('item_id')} is not a bank item")
         continue

      if item["archetype_id"] != case.get("archetype_id"):
         problems.append(f"{case['id']}: archetype does not match the item")

      linked = set()

      for error_id in case.get("observed_errors", []):
         error = errors.get(error_id)

         if error is None:
            problems.append(f"{case['id']}: {error_id} is not an active BC-ERR")
            continue

         linked |= set(error.get("possible_misconceptions") or [])

      for hypothesis in case.get("misconception_hypotheses", []):
         is_active = hypothesis["id"] in misconceptions
         is_linked = hypothesis["id"] in linked

         if not (is_active and is_linked):
            problems.append(f"{case['id']}: {hypothesis['id']} is not an active misconception of the observed errors")

      is_single_certain = len(case.get("misconception_hypotheses", [])) == 1 and len(linked) > 1

      if is_single_certain:
         problems.append(f"{case['id']}: one hypothesis where the errors allow several")

   return problems


def tutor_problems(golden, library):
   items = library["items"]
   problems = []

   for case in golden["cases"]:
      item = items.get(case.get("item_id"))
      option = None

      if item is not None:
         option = next((entry for entry in item.get("options") or [] if entry["id"] == case.get("chosen_option_id")), None)

      if option is None or option.get("is_key"):
         problems.append(f"{case['id']}: the chosen option is not a distractor of a bank item")
         continue

      matches_option = option.get("error_path") == case.get("error_id") and option.get("violated_step") == case.get("violated_step")

      if not matches_option:
         problems.append(f"{case['id']}: error_id or violated_step differs from the option")

      labels = case.get("labels", {})
      should_accept = all(labels.get(check) for check in TUTOR_CHECKS) and not labels.get("reveals_final_answer")

      if case.get("acceptable") != should_accept:
         problems.append(f"{case['id']}: acceptable does not follow from the labels")

   return problems


def generator_problems(golden, library):
   items = library["items"]
   problems = []

   for case in golden["cases"]:
      item = items.get(case.get("item_id"))

      if item is None:
         problems.append(f"{case['id']}: {case.get('item_id')} is not a bank item")
         continue

      if item["answer_key"] != case.get("answer_key"):
         problems.append(f"{case['id']}: the bank's key for {item['id']} no longer matches the frozen key")

      frozen_paths = case.get("option_error_paths") or {}
      bank_paths = {option["id"]: option.get("error_path") for option in item.get("options") or []}

      if frozen_paths and frozen_paths != bank_paths:
         problems.append(f"{case['id']}: the bank's distractor paths for {item['id']} changed")

      if case.get("agrees_with_key") is not True:
         problems.append(f"{case['id']}: the independent solution disagrees with the key")

   return problems


def verifier_problems(golden, library):
   problems = []

   for case in golden["cases"]:
      defect = case.get("defect")
      expected = "accept" if defect == "none" else "reject"

      if defect not in VERIFIER_DEFECTS:
         problems.append(f"{case['id']}: unknown defect {defect!r}")

      if case.get("expected_verdict") != expected:
         problems.append(f"{case['id']}: expected verdict does not follow from the defect")

      if case.get("base_item_id") not in library["items"]:
         problems.append(f"{case['id']}: base item is not in the bank")

   return problems


def transcriber_problems(golden, library):
   problems = []
   variations = {case.get("variation") for case in golden["cases"]}

   if "injected_instruction" not in variations:
      problems.append("transcriber: no page carries an instruction addressed to the model")

   for case in golden["cases"]:
      has_transcript = len(case.get("transcript") or []) > 0
      is_pending = case.get("image") is None and str(case.get("image_status", "")).startswith("pending")
      has_image = case.get("image") is not None

      if not has_transcript:
         problems.append(f"{case['id']}: no reference transcript")

      if not (is_pending or has_image):
         problems.append(f"{case['id']}: neither an image nor a pending status")

   return problems


ROLE_CHECKS = {
   "grader": grader_problems,
   "diagnostician": diagnostician_problems,
   "tutor": tutor_problems,
   "generator": generator_problems,
   "verifier": verifier_problems,
   "transcriber": transcriber_problems,
}


def validate(role, golden, library):
   return header_problems(role, golden) + ROLE_CHECKS[role](golden, library)


def load_library(content_root=REPOSITORY_ROOT / "data"):
   def records(name, key):
      document = json.loads((Path(content_root) / name).read_text())

      return document[key] if isinstance(document, dict) else document

   return {
      "scoring_points": records("scoring_points.json", "point_types"),
      "errors": records("errors.json", "errors"),
      "misconceptions": records("misconceptions.json", "misconceptions"),
      "items": bank_items(),
   }


@dataclass(frozen=True)
class Agreement:
   compared: int
   exact: int
   kappa: float | None
   kappa_low: float | None
   kappa_high: float | None

   @property
   def exact_share(self):
      return self.exact / self.compared if self.compared else None


def cohen_kappa(reference, predicted):
   """Cohen's kappa for two raters over the same cases, with the large-sample 95 percent interval
   13 used to size golden set 2. None when chance agreement is total."""
   labels = sorted(set(reference) | set(predicted), key=str)
   count = len(reference)
   observed = sum(1 for left, right in zip(reference, predicted) if left == right) / count
   expected = sum(
      (reference.count(label) / count) * (predicted.count(label) / count)
      for label in labels
   )

   if expected >= 1.0:
      return None, None, None

   kappa = (observed - expected) / (1.0 - expected)
   spread = Z_95 * math.sqrt(observed * (1.0 - observed) / (count * (1.0 - expected) ** 2))

   return kappa, kappa - spread, kappa + spread


def agreement(reference_by_case, predicted_by_case):
   """Scores predictions against the labels on the cases both name."""
   shared = sorted(set(reference_by_case) & set(predicted_by_case))
   reference = [reference_by_case[case_id] for case_id in shared]
   predicted = [predicted_by_case[case_id] for case_id in shared]

   if not shared:
      return Agreement(0, 0, None, None, None)

   exact = sum(1 for left, right in zip(reference, predicted) if left == right)
   kappa, low, high = cohen_kappa(reference, predicted)

   return Agreement(len(shared), exact, kappa, low, high)


def grader_reference(golden):
   return {case["id"]: case["earned"] for case in golden["cases"]}


def per_point_type(golden, predicted_by_case):
   """Exact match per point type with its count, the measure 13 put on the P3 gate."""
   grouped = {}

   for case in golden["cases"]:
      grouped.setdefault(case["point_type_id"], {})[case["id"]] = case["earned"]

   return {
      point_type: agreement(labels, predicted_by_case)
      for point_type, labels in sorted(grouped.items())
   }


def deterministic_verifier_verdicts(golden, snapshot):
   """The verifier's deterministic baseline: reject when any check app/items/ingest.py runs on the
   way into the bank, or the distractor-path rule, fails."""
   verdicts = {}

   for case in golden["cases"]:
      item = case["item"]
      archetype = snapshot.archetypes.get(item.get("archetype_id"))
      active_error_ids = error_ids_for_skills(snapshot, archetype["skills"]) if archetype else set()
      failed = [result for result in run_checks(item, active_error_ids) if result["outcome"] != "pass"]
      failed_paths = distractor_path_violations(item, active_error_ids)
      verdicts[case["id"]] = "reject" if failed or failed_paths else "accept"

   return verdicts


def detection_by_defect(golden, verdicts):
   """For each defect kind, how many of its cases got the expected verdict, over how many."""
   table = {}

   for case in golden["cases"]:
      caught, total = table.get(case["defect"], (0, 0))
      is_right = verdicts.get(case["id"]) == case["expected_verdict"]
      table[case["defect"]] = (caught + (1 if is_right else 0), total + 1)

   return table
