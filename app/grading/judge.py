"""The grader role's model call: one structured judgement of every open scoring point of a part.

One call carries the question, the part, the solution skeleton and the student's work once, and
every point the checks left open with its own record and criterion; the answer is one verdict per
point id. A 9 point question judged by the model is 3 calls per part it spans rather than 27.

The prompt is prompts/grader/point_liberal_v2.md for the two standard samples and
prompts/grader/point_strict_v2.md for the strictness-varied one. The standard reading is the
liberal one because the one study that isolates the dial found a liberal policy lowered mean
absolute error for every model it tested (https://arxiv.org/html/2607.01247, [single-source]);
eval_leniency_calibration measures the difference on the golden set.

The two standard samples cannot be taken at temperature 0 on the routed model: a non-default
temperature is a 400 on Sonnet 5 through the API (app/providers/anthropic.py) and the CLI has no
temperature option. They are two samples at the model's own setting, which serves 03's purpose
for them, a disagreement detector, and is recorded in BUILD-LEDGER.md.

Every call goes through the provider handed in, which the caller wraps in the budget guard.
"""
import json
import time
from pathlib import Path

from app.grading.point import JudgeUnavailable, SampleFailed, STRICT
from app.providers.base import CacheSettings, Message, ProviderRequest, render_template, split_template
from app.providers.guard import BudgetStopped, ProviderCallFailed, SUBSCRIPTION_MINUTE_RATE
from app.providers.model_routing import model_for
from app.providers.subscription import SubscriptionAuthFailed, SubscriptionLimitReached

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts" / "grader"
STANDARD_TEMPLATE = PROMPTS_DIR / "point_liberal_v2.md"
STRICT_TEMPLATE = PROMPTS_DIR / "point_strict_v2.md"
MAX_OUTPUT_TOKENS_PER_POINT = 700
PROVIDER_OPTIONS = {"thinking": {"type": "disabled"}}
PACING_WAIT_SECONDS = 5
PACING_WAIT_LIMIT_SECONDS = 150

RULE_FIELDS = (
   "earns",
   "does_not_earn",
   "notation_requirements",
   "precision_rules",
   "eligibility_after_error",
   "dependency_on_other_points",
)

VERDICT_FIELDS = ("decision", "evidence_quote", "rule_field", "rule_cited", "eligibility_note")


def grader_schema(point_ids):
   verdict = {
      "type": "object",
      "properties": {
         "point_id": {"type": "string", "enum": list(point_ids)},
         "decision": {"type": "string", "enum": ["earned", "not_earned"]},
         "evidence_quote": {"type": "string"},
         "rule_field": {"type": "string", "enum": list(RULE_FIELDS)},
         "rule_cited": {"type": "string"},
         "eligibility_note": {"type": "string"},
      },
      "required": ["point_id", *VERDICT_FIELDS],
      "additionalProperties": False,
   }

   return {
      "type": "object",
      "properties": {"verdicts": {"type": "array", "items": verdict}},
      "required": ["verdicts"],
      "additionalProperties": False,
   }


def dependency_text(point_type):
   return (
      f"requires previous work: {point_type['requires_previous_work']}; "
      f"setup alone earns: {point_type['setup_alone_earns']}; "
      f"simplification required: {point_type['simplification_required']}; "
      f"{point_type['dependency_on_other_points']}"
   )


def rendered_work(work, part_ids=None):
   lines = []

   for part_work in work.get("parts", []):
      is_wanted = part_ids is None or part_work.get("part_id") in part_ids

      if not is_wanted:
         continue

      lines.append(f"({part_work.get('part_id')})")
      number = 0

      for line in part_work.get("lines", []):
         if line.get("crossed_out"):
            continue

         number += 1
         lines.append(f"  {number}. [{line.get('kind', 'math')}] {line.get('content', '')}")

      answer = (part_work.get("answer") or "").strip()

      if answer:
         lines.append(f"  answer: {answer}")

   return "\n".join(lines) if lines else "(no work written)"


def solution_skeleton(part):
   steps = [step.get("latex") or step.get("text") or "" for step in part.get("worked_solution", [])]

   return "\n".join(f"  {index}. {step}" for index, step in enumerate(steps, start=1))


def needs_previous_work(point_type):
   return str(point_type.get("requires_previous_work", "no")).lower().startswith("yes")


def parts_in_view(record, part, point_types):
   """The part's own work, and the earlier parts too when any point asked about needs previous work."""
   needs_previous = any(needs_previous_work(point_type) for point_type in point_types)
   ids = [candidate["id"] for candidate in record["parts"]]
   position = ids.index(part["id"])

   return ids[: position + 1] if needs_previous else [part["id"]]


def point_block(point, point_type):
   return "\n".join([
      f"Point {point['point_id']}: point type {point_type['id']}, {point_type['name']}.",
      f"What earns it: {point_type['earns']}",
      f"What does not earn it: {point_type['does_not_earn']}",
      f"Notation requirements: {point_type['notation_requirements']}",
      f"Precision rules: {point_type['precision_rules']}",
      f"Eligibility after an error: {point_type['eligibility_after_error']}",
      f"Dependence on other points: {dependency_text(point_type)}",
      f"This question's criterion for the point: {point['criterion']}",
   ])


def prompt_fields(record, part, points, work, point_types):
   blocks = [point_block(point, point_type) for point, point_type in zip(points, point_types)]

   return {
      "question_stem": record["stem"]["text"],
      "part_id": part["id"],
      "part_prompt": part["prompt"],
      "solution_skeleton": solution_skeleton(part),
      "points": "\n\n".join(blocks),
      "student_work": rendered_work(work, parts_in_view(record, part, point_types)),
   }


def request_for(record, part, points, work, point_types, strictness, sample_label):
   template_path = STRICT_TEMPLATE if strictness == STRICT else STANDARD_TEMPLATE
   text = template_path.read_text()
   system, _variables = split_template(text)
   rendered = render_template(text, prompt_fields(record, part, points, work, point_types))
   point_ids = [point["point_id"] for point in points]

   return ProviderRequest(
      role="grader",
      model=model_for("grader"),
      system=system,
      messages=(Message(role="user", content=rendered),),
      max_output_tokens=MAX_OUTPUT_TOKENS_PER_POINT * len(points),
      output_schema=grader_schema(point_ids),
      cache=CacheSettings(prefix_breakpoints=1, ttl="5m"),
      provider_options={key: dict(value) for key, value in PROVIDER_OPTIONS.items()},
      sample_label=sample_label,
   )


def parsed_verdict(payload):
   is_object = isinstance(payload, dict)

   if not is_object:
      raise SampleFailed("the grading was not an object")

   decision = payload.get("decision")
   has_decision = decision in ("earned", "not_earned")

   if not has_decision:
      raise SampleFailed("the grading named no decision")

   rule_field = payload.get("rule_field")
   has_known_field = rule_field in RULE_FIELDS

   return {
      "decision": decision,
      "evidence_quote": str(payload.get("evidence_quote") or ""),
      "rule_field": rule_field if has_known_field else None,
      "rule_cited": str(payload.get("rule_cited") or ""),
      "eligibility_note": str(payload.get("eligibility_note") or ""),
   }


def parsed_verdicts(text, point_ids):
   """Point id to its parsed verdict, or to the SampleFailed that explains why it has none. A
   verdict for a point that was not asked about is ignored, and a point with two verdicts has
   none, because the call did not say which one it meant."""
   try:
      payload = json.loads(text or "")
   except ValueError:
      raise SampleFailed("the grading was not JSON") from None

   verdicts = payload.get("verdicts") if isinstance(payload, dict) else None
   is_list = isinstance(verdicts, list)

   if not is_list:
      raise SampleFailed("the grading carried no list of verdicts")

   found = {point_id: [] for point_id in point_ids}

   for verdict in verdicts:
      point_id = verdict.get("point_id") if isinstance(verdict, dict) else None

      if point_id in found:
         found[point_id].append(verdict)

   answers = {}

   for point_id, candidates in found.items():
      if not candidates:
         answers[point_id] = SampleFailed("the grading named no verdict for this point")
         continue

      if len(candidates) > 1:
         answers[point_id] = SampleFailed("the grading named two verdicts for this point")
         continue

      try:
         answers[point_id] = parsed_verdict(candidates[0])
      except SampleFailed as failed:
         answers[point_id] = failed

   return answers


def is_minute_pacing(stopped):
   return SUBSCRIPTION_MINUTE_RATE in getattr(stopped, "caps", ())


SIGN_IN_EXPIRED = "the Claude sign-in expired, so the grader is unavailable"


def is_sign_in_failure(failed):
   return getattr(failed, "exception_type", None) == SubscriptionAuthFailed.__name__


def is_usage_limit(failed):
   return getattr(failed, "exception_type", None) == SubscriptionLimitReached.__name__


class ModelJudge:
   """The judge app/grading/point.py asks. A minute pacing stop waits for the window to clear, up
   to PACING_WAIT_LIMIT_SECONDS; a daily cap, a budget stop or a usage limit is JudgeUnavailable."""

   def __init__(self, provider, point_types, sleep=time.sleep, wait_limit_seconds=PACING_WAIT_LIMIT_SECONDS):
      self._provider = provider
      self._point_types = point_types
      self._sleep = sleep
      self._wait_limit_seconds = wait_limit_seconds
      self.requests = []

   def judge_points(self, record, part, points, work, strictness, sample_label):
      point_types = [self._point_types[point["point_type_id"]] for point in points]
      request = request_for(record, part, points, work, point_types, strictness, sample_label)
      self.requests.append(request)
      result = self._generate(request)

      return parsed_verdicts(result.text, [point["point_id"] for point in points])

   def _generate(self, request):
      waited = 0

      while True:
         try:
            return self._provider.generate(request)
         except BudgetStopped as stopped:
            can_wait = is_minute_pacing(stopped) and waited < self._wait_limit_seconds

            if not can_wait:
               raise JudgeUnavailable(str(stopped)) from None

            self._sleep(PACING_WAIT_SECONDS)
            waited += PACING_WAIT_SECONDS
         except SubscriptionLimitReached:
            raise JudgeUnavailable("the Claude subscription usage limit was reached") from None
         except SubscriptionAuthFailed:
            raise JudgeUnavailable(SIGN_IN_EXPIRED) from None
         except ProviderCallFailed as failed:
            if is_usage_limit(failed):
               raise JudgeUnavailable("the Claude subscription usage limit was reached") from None

            if is_sign_in_failure(failed):
               raise JudgeUnavailable(SIGN_IN_EXPIRED) from None

            raise SampleFailed(f"the grading call failed: {failed.exception_type}") from None
         except Exception as raised:
            raise SampleFailed(f"the grading call failed: {type(raised).__name__}") from None
