"""docs/plan/11-phased-delivery.md gate 22, test_prompt_cache_prefix_length.

The tutor template's static prefix has to exceed the cache minimum of the model the tutor is
routed to, or Anthropic processes it uncached with no error (R30). Nothing here calls the network:
the count comes from tests/fixtures/prompt_token_counts.json, written by
tools/count_prompt_tokens.py against the free count_tokens endpoint, and it is only believed for
the exact prefix bytes it was measured on. The model is the one app/feedback/tutor.py routes to
and the minimum is read out of the sentence in docs/plan/07-ai-provider-layer.md that states it,
so neither is typed here.
"""
import hashlib
import json
import re
from pathlib import Path

from app.feedback import tutor
from app.providers.base import split_template

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
COUNTS_PATH = REPO_ROOT / "tests" / "fixtures" / "prompt_token_counts.json"
PROVIDER_PLAN = REPO_ROOT / "docs" / "plan" / "07-ai-provider-layer.md"
P1_ITEMS_DIR = REPO_ROOT / "tests" / "fixtures" / "items_p1"
ARCHETYPES_PATH = REPO_ROOT / "data" / "archetypes.json"
ERRORS_PATH = REPO_ROOT / "data" / "errors.json"

MINIMUM_SENTENCE = re.compile(r"a second test asserts that the prefix exceeds the routed model's cache minimum \(([^)]*)\)")
MINIMUM_CLAUSE = re.compile(r"([\d,]+) (?:tokens )?on ([A-Z][a-z]+ [\d.]+)")


def plan_cache_minimums():
   """Model family name, as 07 writes it, to its minimum cacheable prefix in tokens."""
   plan_text = " ".join(PROVIDER_PLAN.read_text().split())
   sentence = MINIMUM_SENTENCE.search(plan_text)

   assert sentence is not None, "07's cache-prefix stability sentence naming the minimums was not found"

   clauses = MINIMUM_CLAUSE.findall(sentence.group(1))

   return {family: int(count.replace(",", "")) for count, family in clauses}


def plan_family_name(model_id):
   """claude-sonnet-5 is what 07 calls Sonnet 5, and claude-haiku-4-5 is Haiku 4.5."""
   _vendor, family, *version = model_id.split("-")

   return f"{family.capitalize()} {'.'.join(version)}"


def tutor_prefix_bytes():
   prefix, _variable_section = split_template(tutor.TEMPLATE_PATH.read_text())

   return prefix.encode("utf-8")


def test_prompt_cache_prefix_length():
   minimums = plan_cache_minimums()
   family = plan_family_name(tutor.TUTOR_MODEL)

   assert family in minimums, f"07 states no cache minimum for {family}, the tutor's routed model"

   cache_minimum = minimums[family]
   template_name = str(tutor.TEMPLATE_PATH.relative_to(REPO_ROOT))
   counts = json.loads(COUNTS_PATH.read_text())

   assert template_name in counts, f"{template_name} has never been measured with count_tokens"

   entry = counts[template_name]
   current_digest = hashlib.sha256(tutor_prefix_bytes()).hexdigest()

   assert entry["sha256"] == current_digest, (
      f"{template_name}'s prefix changed after it was measured; rerun tools/count_prompt_tokens.py"
   )
   assert entry["model"] == tutor.TUTOR_MODEL, (
      f"{template_name} was measured on {entry['model']}, the tutor is routed to {tutor.TUTOR_MODEL}"
   )
   assert entry["prefix_tokens"] > cache_minimum, (
      f"{template_name}'s prefix is {entry['prefix_tokens']} tokens, which does not exceed "
      f"{family}'s cache minimum of {cache_minimum}, so it would be processed uncached"
   )


def representative_draws():
   """One draw per P1 fixture item, paired with a BC-ERR record, and one with both error fields
   empty as app/feedback/render.py sends them when the chosen answer matches no error path."""
   archetypes = {record["id"]: record for record in json.loads(ARCHETYPES_PATH.read_text())["archetypes"]}
   error_records = json.loads(ERRORS_PATH.read_text())["errors"]
   item_paths = sorted(P1_ITEMS_DIR.glob("*.json"))
   draws = []

   for position, item_path in enumerate(item_paths):
      item = json.loads(item_path.read_text())
      solution_path = archetypes[item["archetype_id"]]["expected_solution_path"]
      error_record = error_records[position % len(error_records)]
      has_no_error_path = position == 0

      draws.append({
         "violated_step": solution_path[position % len(solution_path)],
         "observed_behavior": "" if has_no_error_path else error_record["observed_behavior"],
         "scoring_consequence": "" if has_no_error_path else error_record["scoring_consequence"],
         "worked_solution": json.dumps(item["worked_solution"]),
      })

   return draws


def test_tutor_prefix_is_byte_identical_across_draws():
   """07, Cache-prefix stability: the rendered prefix does not move with the parameters."""
   draws = representative_draws()

   assert len(draws) > 1

   expected_prefix = tutor_prefix_bytes()
   systems = {tutor.request_for(fields).system.encode("utf-8") for fields in draws}

   assert systems == {expected_prefix}

   for fields in draws:
      for value in fields.values():
         is_substantive = len(value) > 0

         if is_substantive:
            assert value not in expected_prefix.decode("utf-8")
