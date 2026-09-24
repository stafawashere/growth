"""Per-item verification of generated items and the publication rule.

docs/plan/04-item-generation.md, "Independent key verification" and "Rejection rules", in the
cheapest-first order of docs/plan/13-ai-engineering.md: the record checks ingest runs, the
template's own answer rebuilt from the seed, the duplicate gate, and the independent re-solve,
which is a blind formulation written by a second agent from the stem alone and compared by
tools/key_recheck.py. Publication needs every check to agree; anything else goes to the review
queue with the rule that stopped it, and is never averaged.
"""
from dataclasses import dataclass, field

from app.generation.template import library
from app.items import ingest
from app.items.distractor_paths import error_ids_for_skills

PUBLISHED = "published"
NEEDS_REVIEW = "needs_review"
REJECTED = "rejected"

TARGET_TOLERANCE = 0.15

RULE_NAMES = {
   3: "the independent re-solve disagrees with the key",
   4: "a comparison did not settle",
   5: "a distractor equals the key",
   6: "two options are equal",
   7: "a distractor's error path is missing or not held",
   8: "the calculator boundary",
   10: "the MinHash duplicate check",
   11: "stage two of the duplicate gate",
   12: "a span of official text above the anchor-quote cap",
   14: "the predicted success probability is off the requested target",
}


@dataclass
class Verdict:
   item_id: str
   status: str = PUBLISHED
   rules: list = field(default_factory=list)
   notes: list = field(default_factory=list)

   def fail(self, rule, note, status=NEEDS_REVIEW):
      self.rules.append(rule)
      self.notes.append(note)
      is_harsher = status == REJECTED or self.status == PUBLISHED

      if is_harsher:
         self.status = status

   def as_dict(self):
      return {"item_id": self.item_id, "status": self.status, "rules": self.rules, "notes": self.notes}


def record_checks(record, verdict):
   archetype = library().archetypes[record["archetype_id"]]
   error_ids = error_ids_for_skills(library(), archetype["skills"])

   for result in ingest.run_checks(record, error_ids):
      outcome = result["outcome"]

      if outcome == ingest.PASS:
         continue

      violations = result["detail"].get("violations") or []
      rule = 5 if "rule_5" in violations else 6 if "rule_6" in violations else 7 if "rule_7" in violations else 4
      status = REJECTED if outcome == ingest.FAIL else NEEDS_REVIEW
      verdict.fail(rule, f"{result['check_type']} {outcome}: {result['detail']}", status)


def calculator_boundary(record, verdict):
   key = record["answer_key"]
   is_no_calculator = record["calculator_status"] == "no_calculator"
   is_calculator = record["calculator_status"] == "calculator"
   reports_decimals = key.get("form") == "numeric"
   carries_decimal = isinstance(key.get("mathjson"), float)

   if is_no_calculator and (reports_decimals or carries_decimal):
      verdict.fail(8, "a no-calculator item carries a decimal key", REJECTED)

   if is_calculator and reports_decimals and key.get("decimals") != 3:
      verdict.fail(8, "a calculator key is not reported to three decimals", REJECTED)

   if is_calculator and not record["stem"].get("setup_required"):
      verdict.fail(8, "a calculator item does not ask for the setup", REJECTED)


def target_check(record, target, verdict):
   if target is None:
      return

   predicted = record.get("predicted_success_probability")
   is_off_target = predicted is None or abs(predicted - target) > TARGET_TOLERANCE

   if is_off_target:
      verdict.fail(14, f"predicted {predicted} against the requested {target}")


def duplicate_check(record, gate, verdict):
   if gate is None:
      return

   result = gate.check(record)

   if result.stage_one.hit:
      verdict.fail(10, f"Jaccard {result.stage_one.score:.3f} with {result.stage_one.neighbour} ({result.stage_one.corpus})")

   if result.stage_two.hit:
      measure = "math pair Jaccard" if result.stage_two.corpus == "bank" else "cosine"
      verdict.fail(11, f"{measure} {result.stage_two.score:.3f} with {result.stage_two.neighbour} ({result.stage_two.corpus})")

   if result.official_span.hit:
      verdict.fail(12, f"{result.official_span.length} words shared with {result.official_span.neighbour}", REJECTED)


def recheck_flags(flags, verdict):
   """The flags tools/key_recheck.py raised on this item, blind formulation and template mode."""
   for flag in flags:
      if flag == "key_matches":
         continue

      if flag in ("template_differs", "provenance_drift"):
         verdict.fail(3, flag, REJECTED)
      elif flag in ("comparison_undecided", "formulation_failed", "not_formulated"):
         verdict.fail(4, flag)
      elif flag == "option_mismatch":
         verdict.fail(5, flag)
      else:
         verdict.fail(3, flag)


def verify(record, recheck_result_flags, gate=None, target=None):
   verdict = Verdict(item_id=record["id"])
   record_checks(record, verdict)
   calculator_boundary(record, verdict)
   target_check(record, target, verdict)
   duplicate_check(record, gate, verdict)
   recheck_flags(recheck_result_flags, verdict)

   return verdict
