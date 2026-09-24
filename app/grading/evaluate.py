"""Golden set 2 and the grader evals of 11 P3: eval_grader_against_operator_goldens,
eval_leniency_calibration and eval_transcription_error_share.

The golden set (tests/fixtures/grader_goldens) is model-authored and model-graded on the operator's
delegation, never human; every number here is a model's agreement with a model's hand grade and is
labelled that way wherever it is published. Each response names one target point. The grader
decides the target exactly as it would in the app (the deterministic check first, then three
samples, follow-through when a carried result was lost), the other points take their golden labels,
and the eligibility pass runs over the whole vector, so the target's decision is the one a student
would have seen.

Reported, per point type and in aggregate, each with its denominator:

- exact agreement on the points the grader published (not provisional), against the golden label;
- mean absolute error per point on those same points, which for a 0 or 1 point is the share wrong;
- escalation rate, the share of targets that came back provisional;
- single-sample agreement, the first standard sample alone against the label over every target
  that reached the model, which is what 10's monthly one-sample canary measures;
- the leniency comparison: the standard sample's error against the strict sample's error on the
  same targets (eval_leniency_calibration).
"""
import json
from dataclasses import dataclass, field
from pathlib import Path

from app.frq.items import load_frq_records
from app.grading import point as grader

REPO_ROOT = Path(__file__).resolve().parents[2]
GOLDENS_DIR = REPO_ROOT / "tests" / "fixtures" / "grader_goldens"
RESPONSE_FILES = ("responses_a.json", "responses_b.json")
CATEGORIES = ("fully_correct", "unconventional_valid", "narrow_fail", "notation_failure", "eligible_after_error")
GOLDEN = "golden"


def load_goldens(directory=GOLDENS_DIR):
   records = {record["id"]: record for record in load_frq_records(Path(directory) / "items")}
   responses = []
   authors = []

   for name in RESPONSE_FILES:
      document = json.loads((Path(directory) / name).read_text())
      authors.append(document["author"])
      responses.extend(document["responses"])

   return records, responses, authors


def golden_decision(part_id, point, label):
   return grader.PointDecision(
      part_id=part_id,
      point_id=point["point_id"],
      point_type_id=point["point_type_id"],
      decided_by=GOLDEN,
      earned=int(label),
      agreement=grader.NOT_SAMPLED,
      provisional=False,
      rationale="golden label",
   )


def grade_target(record, response, labels, judge):
   """The target point decided by the grader in the context of the golden labels."""
   work = response["work"]
   target_id = response["target_point"]
   decisions = []
   judge_available = judge is not None

   for part in record["parts"]:
      for point in part["points"]:
         is_target = point["point_id"] == target_id

         if not is_target:
            decisions.append(golden_decision(part["id"], point, response["labels"][point["point_id"]]))
            continue

         decision, judge_available = grader.decide_point(record, part, point, work, labels, judge, judge_available)
         decisions.append(decision)

   decisions, _available = grader.apply_follow_through(record, decisions, work, labels, judge, judge_available)
   settled = grader.apply_eligibility(record, decisions)

   return next(decision for decision in settled if decision.point_id == target_id)


@dataclass
class Tally:
   targets: int = 0
   published: int = 0
   agreed: int = 0
   escalated: int = 0
   sampled: int = 0
   single_sample_agreed: int = 0
   standard_errors: int = 0
   strict_errors: int = 0
   deterministic: int = 0

   def add(self, other):
      for name in self.__dataclass_fields__:
         setattr(self, name, getattr(self, name) + getattr(other, name))

   def as_record(self):
      published = self.published

      return {
         "targets": self.targets,
         "published": published,
         "exact_agreement": round(self.agreed / published, 4) if published else None,
         "mean_absolute_error_per_point": round((published - self.agreed) / published, 4) if published else None,
         "escalated": self.escalated,
         "escalation_rate": round(self.escalated / self.targets, 4) if self.targets else None,
         "decided_deterministically": self.deterministic,
         "reached_the_model": self.sampled,
         "single_sample_agreement": round(self.single_sample_agreed / self.sampled, 4) if self.sampled else None,
         "standard_sample_mae": round(self.standard_errors / self.sampled, 4) if self.sampled else None,
         "strict_sample_mae": round(self.strict_errors / self.sampled, 4) if self.sampled else None,
      }


def sample_decision(decision, name):
   for sample in decision.samples:
      if sample.get("sample") == name and "decision" in sample:
         return 1 if sample["decision"] == grader.EARNED else 0

   return None


def tally_for(decision, label):
   tally = Tally(targets=1)
   is_provisional = decision.provisional or decision.earned is None

   if is_provisional:
      tally.escalated = 1
   else:
      tally.published = 1
      tally.agreed = int(decision.earned == label)

   tally.deterministic = int(decision.decided_by == grader.DETERMINISTIC)
   standard = sample_decision(decision, "temp0_a")
   strict = sample_decision(decision, "strict")
   was_sampled = standard is not None and strict is not None

   if was_sampled:
      tally.sampled = 1
      tally.single_sample_agreed = int(standard == label)
      tally.standard_errors = int(standard != label)
      tally.strict_errors = int(strict != label)

   return tally


@dataclass
class EvalResult:
   overall: Tally = field(default_factory=Tally)
   by_point_type: dict = field(default_factory=dict)
   by_category: dict = field(default_factory=dict)
   rows: list = field(default_factory=list)

   def as_record(self):
      return {
         "overall": self.overall.as_record(),
         "by_point_type": {key: tally.as_record() for key, tally in sorted(self.by_point_type.items())},
         "by_category": {key: tally.as_record() for key, tally in sorted(self.by_category.items())},
      }


def evaluate(records, responses, labels, judge):
   result = EvalResult()

   for response in responses:
      record = records[response["item_id"]]
      decision = grade_target(record, response, labels, judge)
      label = int(response["labels"][response["target_point"]])
      tally = tally_for(decision, label)
      result.overall.add(tally)
      result.by_point_type.setdefault(response["target_point_type"], Tally()).add(tally)
      result.by_category.setdefault(response["category"], Tally()).add(tally)
      result.rows.append({
         "response": response["id"],
         "point_type": response["target_point_type"],
         "category": response["category"],
         "label": label,
         "decided_by": decision.decided_by,
         "earned": decision.earned,
         "provisional": bool(decision.provisional),
      })

   return result


def reaches_a_model(record, point_id, labels):
   for part in record["parts"]:
      for point in part["points"]:
         if point["point_id"] != point_id:
            continue

         has_check = point.get("check") is not None
         is_deterministic = labels.get(point["point_type_id"]) == grader.DETERMINISTIC

         return not (has_check and is_deterministic)

   return False
