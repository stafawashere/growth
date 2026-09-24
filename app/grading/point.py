"""The per-point grader, docs/plan/11-phased-delivery.md P3 scope items 4 and 5.

grade_question decides every scoring point of one free-response question from the student's
confirmed read-back. For each point, in order:

1. Deterministic first. A point whose record carries a check and whose BC-PT is labelled
   deterministic in data/bc_pt_determinism_labels.json is decided by the check whenever the check
   settles, and the model is never asked (test_deterministic_precheck_priority). An unsettled
   check falls through to the model path, as 03 requires, carrying its result for the record.
2. Otherwise the model judges the point three times: two samples of the standard prompt and one
   of the strictness-varied prompt. Unanimity publishes the decision. Any disagreement, a failed
   sample, or an evidence quote that is not in the student's work escalates the point: earned is
   null, the point is provisional, and it is never averaged (test_disagreement_escalates).

Then three passes over the whole point vector, in the backend:

- Follow-through: a point whose follows_from names a lost point, and whose fixed-key check failed,
  is judged again by the model on the student's own earlier result (apply_follow_through).
- The rounding cap, the second of the two separately stated rules (R21): within one question at
  most one point is lost to inappropriate rounding, so the first rounding-only failure in part
  order stands and every later one is awarded. The cap is per question, never per part
  (test_three_decimal_cap).
- Eligibility after error: a point whose eligible_only_if names a point that was not earned is not
  earned, and one that names a provisional point is provisional too, with eligibility_note saying
  which (03, "Eligibility-after-error rules").

A model the grader cannot reach, because a budget or pacing cap stopped it or the subscription
hit its usage limit, leaves the remaining judged points pending: provisional, earned null, and
retried by the next grading pass. Nothing is guessed.
"""
from dataclasses import dataclass, field, replace

from app.grading import checks

DETERMINISTIC = "deterministic"
MODEL = "model"
ESCALATED = "escalated"
PENDING = "pending"

UNANIMOUS = "unanimous"
SPLIT = "split"
NOT_SAMPLED = "not_sampled"

EARNED = "earned"
NOT_EARNED = "not_earned"

STANDARD = "standard"
STRICT = "strict"
SAMPLE_PLAN = (("temp0_a", STANDARD), ("temp0_b", STANDARD), ("strict", STRICT))

SETTLED_OUTCOMES = (checks.PASS, checks.FAIL)


class JudgeUnavailable(Exception):
   """The judge could not be asked at all: a cap, a pacing stop or a usage limit. Grading stops
   asking and leaves the rest pending."""


class SampleFailed(Exception):
   """One sample came back unusable: a transport error, output that is not the schema, or a
   refusal. The point escalates."""


@dataclass
class PointDecision:
   part_id: str
   point_id: str
   point_type_id: str
   decided_by: str
   earned: int | None
   agreement: str
   provisional: bool
   rationale: str
   samples: list = field(default_factory=list)
   rule_field: str | None = None
   evidence_quote: str | None = None
   eligibility_note: str | None = None
   deterministic_check: dict | None = None
   rounding_only: bool = False


@dataclass
class QuestionGrading:
   decisions: list
   rounding_penalty_applied: bool

   def by_point(self):
      return {decision.point_id: decision for decision in self.decisions}


def is_deterministic_type(point_type_id, labels):
   return labels.get(point_type_id) == DETERMINISTIC


def work_for_part(work, part_id):
   for part_work in work.get("parts", []):
      if part_work.get("part_id") == part_id:
         return part_work

   return {"part_id": part_id, "lines": [], "answer": ""}


def work_text(work):
   """The confirmed work as one string, crossed-out lines left out, for the verbatim-quote rule."""
   pieces = []

   for part_work in work.get("parts", []):
      for line in checks.live_lines(part_work):
         pieces.append(line.get("content", ""))

      pieces.append(part_work.get("answer") or "")

   return "\n".join(pieces)


MATH_DELIMITERS = ("\\(", "\\)", "\\[", "\\]", "$")


def squeezed(text):
   """A quote and the work are compared with math delimiters, \\text wrappers and spacing taken
   out, because a grader quoting "g' changes sign" from a line written "\\(g'\\) changes sign" has
   quoted the page."""
   plain = text or ""

   for delimiter in MATH_DELIMITERS:
      plain = plain.replace(delimiter, " ")

   plain = plain.replace("\\text{", " ").replace("\\mathrm{", " ").replace("\\,", " ")
   plain = plain.replace("{", "").replace("}", "")

   return "".join(plain.split()).lower()


def quote_is_verbatim(quote, confirmed_text):
   has_quote = squeezed(quote) != ""

   if not has_quote:
      return True

   return squeezed(quote) in squeezed(confirmed_text)


def deterministic_decision(part, point, result):
   earned = 1 if result.outcome == checks.PASS else 0

   return PointDecision(
      part_id=part["id"],
      point_id=point["point_id"],
      point_type_id=point["point_type_id"],
      decided_by=DETERMINISTIC,
      earned=earned,
      agreement=NOT_SAMPLED,
      provisional=False,
      rationale=f"{result.check}: {result.detail}",
      deterministic_check=result.as_record(),
      rounding_only=result.rounding_only and earned == 0,
   )


def pending_decision(part, point, check_record, reason):
   return PointDecision(
      part_id=part["id"],
      point_id=point["point_id"],
      point_type_id=point["point_type_id"],
      decided_by=PENDING,
      earned=None,
      agreement=NOT_SAMPLED,
      provisional=True,
      rationale=reason,
      deterministic_check=check_record,
   )


def escalation_reason(samples, failures, unverified_quotes):
   if failures:
      return f"{len(failures)} of 3 gradings could not be read, so the point was sent for review"

   if unverified_quotes:
      return "a grading quoted work that is not on the page, so the point was sent for review"

   earned_count = sum(1 for sample in samples if sample["decision"] == EARNED)

   return (
      f"the gradings disagreed, {earned_count} of 3 earned, so the point was sent for review "
      f"rather than averaged"
   )


def model_decision(part, point, samples, failures, confirmed_text, check_record):
   unverified_quotes = [
      sample for sample in samples
      if not quote_is_verbatim(sample.get("evidence_quote"), confirmed_text)
   ]
   decisions = {sample["decision"] for sample in samples}
   complete = len(samples) == len(SAMPLE_PLAN) and not failures
   unanimous = complete and len(decisions) == 1 and not unverified_quotes

   if unanimous:
      decision = samples[0]["decision"]
      earned = 1 if decision == EARNED else 0

      return PointDecision(
         part_id=part["id"],
         point_id=point["point_id"],
         point_type_id=point["point_type_id"],
         decided_by=MODEL,
         earned=earned,
         agreement=UNANIMOUS,
         provisional=False,
         rationale=samples[0].get("rule_cited") or point["criterion"],
         samples=samples,
         rule_field=samples[0].get("rule_field"),
         evidence_quote=samples[0].get("evidence_quote"),
         eligibility_note=samples[0].get("eligibility_note") or None,
         deterministic_check=check_record,
      )

   return PointDecision(
      part_id=part["id"],
      point_id=point["point_id"],
      point_type_id=point["point_type_id"],
      decided_by=ESCALATED,
      earned=None,
      agreement=SPLIT,
      provisional=True,
      rationale=escalation_reason(samples, failures, unverified_quotes),
      samples=samples + [{"failed": reason} for reason in failures],
      evidence_quote=next((sample.get("evidence_quote") for sample in samples if sample.get("evidence_quote")), None),
      deterministic_check=check_record,
   )


def sample_point(judge, record, part, point, work):
   samples = []
   failures = []

   for label, strictness in SAMPLE_PLAN:
      try:
         sample = judge(record, part, point, work, strictness, label)
      except SampleFailed as failed:
         failures.append(str(failed))
         continue

      samples.append(dict(sample, sample=label, strictness=strictness))

   return samples, failures


def decide_point(record, part, point, work, labels, judge, judge_available):
   part_work = work_for_part(work, part["id"])
   has_check = point.get("check") is not None
   check_decides = has_check and is_deterministic_type(point["point_type_id"], labels)
   check_record = None

   if check_decides:
      result = checks.run_check(point["check"], part_work)
      is_settled = result.outcome in SETTLED_OUTCOMES

      if is_settled:
         return deterministic_decision(part, point, result), judge_available

      check_record = result.as_record()

   if not judge_available:
      return pending_decision(part, point, check_record, "waiting for the grader"), False

   try:
      samples, failures = sample_point(judge, record, part, point, work)
   except JudgeUnavailable as unavailable:
      return pending_decision(part, point, check_record, f"waiting for the grader: {unavailable}"), False

   decision = model_decision(part, point, samples, failures, work_text(work), check_record)

   return decision, True


def apply_rounding_cap(decisions):
   """At most one point per question is lost to rounding. The first rounding-only failure in part
   and point order stands; every later one is awarded."""
   penalty_taken = False
   capped = []

   for decision in decisions:
      is_rounding_loss = decision.rounding_only and decision.earned == 0

      if not is_rounding_loss:
         capped.append(decision)
         continue

      if not penalty_taken:
         penalty_taken = True
         capped.append(replace(decision, rationale=decision.rationale + "; the one rounding point this question can lose"))
         continue

      capped.append(
         replace(
            decision,
            earned=1,
            rounding_only=False,
            rationale=decision.rationale + "; awarded, because at most one point per question is lost to rounding",
         )
      )

   return capped, penalty_taken


def apply_eligibility(record, decisions):
   by_point = {decision.point_id: decision for decision in decisions}
   points = {point["point_id"]: point for part in record["parts"] for point in part["points"]}
   settled = []

   for decision in decisions:
      requirements = points[decision.point_id].get("eligible_only_if") or []
      lost = [point_id for point_id in requirements if by_point[point_id].earned == 0]
      undecided = [point_id for point_id in requirements if by_point[point_id].earned is None]
      has_lost = len(lost) > 0
      has_undecided = len(undecided) > 0

      if has_lost:
         note = f"not eligible, because {', '.join(lost)} was not earned"
         decision = replace(decision, earned=0, eligibility_note=note)
      elif has_undecided and decision.earned == 1:
         note = f"eligible only if {', '.join(undecided)} is earned, which is still under review"
         decision = replace(decision, provisional=True, eligibility_note=note)

      by_point[decision.point_id] = decision
      settled.append(decision)

   return settled


def follow_through_point(point, lost_ids):
   """The point as the model sees it when an earlier result it builds on was lost: the criterion
   says the answer is judged for consistency with the student's own earlier work."""
   earlier = ", ".join(sorted(lost_ids))
   criterion = (
      f"{point['criterion']} An earlier result this builds on ({earlier}) was not earned, so judge this "
      f"point for consistency with the student's own earlier result, as follow-through, not against the key."
   )

   return dict(point, criterion=criterion, check=None)


def apply_follow_through(record, decisions, work, labels, judge, judge_available):
   """A fixed-key check cannot see AP follow-through: an answer that is wrong only because it
   carries an earlier lost result forward can still earn. A point whose follows_from names a point
   that was lost, and whose own check failed, is judged again by the model on the student's own
   earlier result. With no judge it stays failed, the conservative reading."""
   by_point = {decision.point_id: decision for decision in decisions}
   revised = []

   for part in record["parts"]:
      for point in part["points"]:
         decision = by_point[point["point_id"]]
         lost_ids = [point_id for point_id in point.get("follows_from") or [] if by_point[point_id].earned == 0]
         failed_its_check = decision.decided_by == DETERMINISTIC and decision.earned == 0
         is_follow_through = failed_its_check and len(lost_ids) > 0 and judge_available

         if is_follow_through:
            decision, judge_available = decide_point(
               record, part, follow_through_point(point, lost_ids), work, labels, judge, judge_available
            )
            decision = replace(decision, eligibility_note=f"judged as follow-through from {', '.join(lost_ids)}")

         revised.append(decision)

   return revised, judge_available


def grade_question(record, work, labels, judge):
   decisions = []
   judge_available = judge is not None

   for part in record["parts"]:
      for point in part["points"]:
         decision, judge_available = decide_point(
            record, part, point, work, labels, judge, judge_available
         )
         decisions.append(decision)

   decisions, judge_available = apply_follow_through(record, decisions, work, labels, judge, judge_available)
   capped, penalty_applied = apply_rounding_cap(decisions)
   settled = apply_eligibility(record, capped)

   return QuestionGrading(decisions=settled, rounding_penalty_applied=penalty_applied)


def remembering_judge(judge, stored_samples, fresh_point_id):
   """A judge that answers every point but fresh_point_id from the samples already stored for it,
   so a re-read asks the model about one point and the two passes still see raw decisions."""

   def answer(record, part, point, work, strictness, label):
      is_fresh = point["point_id"] == fresh_point_id
      remembered = {sample.get("sample"): sample for sample in stored_samples.get(point["point_id"], [])}
      has_memory = label in remembered and "decision" in remembered[label]

      if has_memory and not is_fresh:
         return {key: value for key, value in remembered[label].items() if key not in ("sample", "strictness")}

      if judge is None:
         raise JudgeUnavailable("no grader is configured")

      return judge(record, part, point, work, strictness, label)

   return answer


def regrade_point(record, work, labels, judge, stored_samples, point_id):
   """A re-read of one point: that point is judged again from scratch, every other point keeps its
   stored samples, and both passes run again over the raw vector."""
   known_ids = {point["point_id"] for part in record["parts"] for point in part["points"]}

   if point_id not in known_ids:
      raise KeyError(point_id)

   return grade_question(record, work, labels, remembering_judge(judge, stored_samples, point_id))
