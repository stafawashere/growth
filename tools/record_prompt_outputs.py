"""Record what three runtime templates answer, on the operator's Claude subscription, for the output
goldens of tests/eval/test_prompt_output_goldens.py.

Usage: python3 tools/record_prompt_outputs.py --recorded-by "<who>" [--only tutor|memory]

Never run from a test: it spends the operator's subscription through the claude CLI, with the argv
and environment app/providers/subscription.py builds, at no API cost and with no key read. Four
calls: prompts/tutor/correct_reinforcement_v1.md on two P1 items, prompts/tutor/frq_points_v1.md on
one graded free-response question, and the memory template app/agent/consolidate.py renders on one
closed tutor conversation; --only narrows the run to the tutor's three or the memory role's one. Each request is built by the production builder (app/feedback/tutor.py request_for,
app/agent/consolidate.py request_for_fields) and sent to the role's routed model.

The items, the free-response record and the error record are the repository's own. The student's
side is constructed here and says so in each cassette: the grader rows and the observed error for
a part (b) written without the chain rule factor, and the six turns of the conversation. The
answer is the model's own and is written unedited, with the call's usage, to
tests/fixtures/provider_cassettes/.
"""
import argparse
import datetime
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.agent import consolidate
from app.engine.state import Confidence
from app.feedback import tutor
from app.feedback.render import FeedbackKind
from app.providers.guard import SubscriptionSpendLedger
from app.providers.subscription import SubscriptionProvider

CASSETTE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "provider_cassettes"
ITEMS_DIR = REPOSITORY_ROOT / "content" / "items_p1_agent"
FRQ_PATH = REPOSITORY_ROOT / "content" / "frq_items" / "FRQ-AGT-06012-02.json"
ARCHETYPES_PATH = REPOSITORY_ROOT / "data" / "archetypes.json"
ERRORS_PATH = REPOSITORY_ROOT / "data" / "errors.json"
REINFORCEMENT_ITEMS = ("ITM-AGT-02002-00.json", "ITM-AGT-03008-01.json")
CHAIN_FACTOR_ERROR = "BC-ERR-06027"

CONSTRUCTED_GRADER_ROWS = (
   {
      "part_id": "b",
      "point_id": "b1",
      "rule_field": "earns",
      "rationale": "The derivative is written as f(x^2) with no factor 2x, so the chain rule factor the point requires is absent.",
      "evidence_quote": "k'(x) = f(x^2)",
   },
   {
      "part_id": "b",
      "point_id": "b2",
      "rule_field": "eligibility_after_error",
      "rationale": "The reported value 6 follows from the derivative without the chain rule factor and is not the required value.",
      "evidence_quote": "k'(2) = f(4) = 6",
   },
)
CONSTRUCTED_OBSERVED_ERRORS = ({"error_id": CHAIN_FACTOR_ERROR, "evidence": "k'(x) = f(x^2)"},)

CONSTRUCTED_TURNS = (
   ("ATN-REC-001", "student", "For k(x) = integral from 0 to x^2 of f(t) dt I got k'(x) = f(x^2). Is that the whole derivative?"),
   ("ATN-REC-002", "agent", "Look at the upper limit. It is x^2, not x. What happens when the variable you differentiate with respect to sits inside another function?"),
   ("ATN-REC-003", "student", "Oh, the chain rule again. I always forget it when the limit is not just x."),
   ("ATN-REC-004", "agent", "Write the general form first: the integrand at the upper limit times the derivative of the upper limit. What is the derivative of x^2?"),
   ("ATN-REC-005", "student", "2x. So k'(x) = 2x f(x^2). Writing the general form first like that really helps me, can you keep doing that?"),
   ("ATN-REC-006", "agent", "Yes. With that form, what does k'(2) need from the table?"),
)


def provider_for_recording():
   ledger_path = Path(tempfile.mkdtemp(prefix="record-prompt-outputs-")) / "subscription_spend.json"

   return SubscriptionProvider(subscription_ledger=SubscriptionSpendLedger(path=ledger_path))


def archetypes_by_id():
   return {record["id"]: record for record in json.loads(ARCHETYPES_PATH.read_text())["archetypes"]}


def errors_by_id():
   return {record["id"]: record for record in json.loads(ERRORS_PATH.read_text())["errors"]}


def reinforcement_cases():
   archetypes = archetypes_by_id()
   low_confidence_correct = SimpleNamespace(kind=FeedbackKind.CORRECT, confidence=Confidence.GUESS)

   for file_name in REINFORCEMENT_ITEMS:
      item = json.loads((ITEMS_DIR / file_name).read_text())
      archetype = archetypes[item["archetype_id"]]
      fields = tutor.reinforcement_fields(low_confidence_correct, archetype, json.dumps(item["worked_solution"]))
      source = {"item": f"content/items_p1_agent/{file_name}", "archetype": item["archetype_id"]}

      yield source, tutor.request_for(fields, template=tutor.CORRECT_REINFORCEMENT)


def frq_points_case():
   record = json.loads(FRQ_PATH.read_text())
   rows = [SimpleNamespace(earned=0, provisional=False, **row) for row in CONSTRUCTED_GRADER_ROWS]
   fields = tutor.frq_points_fields(record, rows, list(CONSTRUCTED_OBSERVED_ERRORS), errors_by_id())
   source = {
      "record": "content/frq_items/FRQ-AGT-06012-02.json",
      "error": CHAIN_FACTOR_ERROR,
      "constructed": "the grader rows and the observed error, for a part (b) written without the chain rule factor",
   }

   return source, tutor.request_for(fields, template=tutor.FRQ_POINTS)


def consolidation_case():
   archetype = archetypes_by_id()["BC-QA-06012"]
   fields = {
      "turns": json.dumps([{"id": turn_id, "role": role, "text": text} for turn_id, role, text in CONSTRUCTED_TURNS]),
      "active_entries": json.dumps([]),
      "own_notes": json.dumps([]),
      "active_skill_ids": json.dumps(sorted(archetype["skills"])),
   }
   source = {
      "archetype": "BC-QA-06012",
      "constructed": "the six conversation turns, with no active entries and no notes",
   }

   return source, consolidate.request_for_fields(fields, consolidate.template_text())


def cassette_for(template, source, request, result, recorded_by):
   return {
      "template": template,
      "role": request.role,
      "model": result.model,
      "provider": result.provider,
      "backend": "subscription",
      "recorded": True,
      "recorded_on": datetime.date.today().isoformat(),
      "recorded_by": recorded_by,
      "source": source,
      "rendered_message": request.messages[0].content,
      "text": result.text,
      "finish_reason": result.finish_reason,
      "usage": {
         "input_tokens": result.usage.input_tokens,
         "output_tokens": result.usage.output_tokens,
         "cached_read_tokens": result.usage.cached_read_tokens,
         "cached_write_tokens": result.usage.cached_write_tokens,
      },
   }


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("--recorded-by", required=True, help="who ran the recording, written into each cassette")
   parser.add_argument("--only", choices=("tutor", "memory"), help="record one role's templates alone")
   arguments = parser.parse_args(argv)
   provider = provider_for_recording()
   planned = []
   records_tutor = arguments.only in (None, "tutor")
   records_memory = arguments.only in (None, "memory")

   if records_tutor:
      planned.extend(
         (f"tutor_correct_reinforcement_live_{index:02d}.json", "prompts/tutor/correct_reinforcement_v1.md", case)
         for index, case in enumerate(reinforcement_cases())
      )
      planned.append(("tutor_frq_points_live_00.json", "prompts/tutor/frq_points_v1.md", frq_points_case()))

   if records_memory:
      memory_template = consolidate.TEMPLATE_PATH
      file_name = f"memory_{memory_template.stem}_live_00.json"
      planned.append((file_name, str(memory_template.relative_to(REPOSITORY_ROOT)), consolidation_case()))

   for file_name, template, (source, request) in planned:
      result = provider.generate(request)
      cassette = cassette_for(template, source, request, result, arguments.recorded_by)
      (CASSETTE_DIR / file_name).write_text(json.dumps(cassette, indent=3, sort_keys=True) + "\n")
      print(f"{file_name}: {result.model}, {result.usage.output_tokens} output tokens")

   return 0


if __name__ == "__main__":
   sys.exit(main())
