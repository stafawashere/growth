"""The P4 generation batch: instantiate templates into candidate items, hand the stems to the blind
re-solve, then verify and publish. It runs offline, outside any student session, and never calls a
model: the templates were authored and the re-solve is written by separate Claude Code sessions on
the operator's subscription (docs/operator/offline-authoring.md).

Usage:
  python3 tools/generate_bank.py plan [--archetypes BC-QA-06004 ...]
      Instantiate candidates for every template whose gate passed into var/p4/candidates/<bank>/
      and write the stems the blind solver reads to var/p4/resolve/<bank>/stems.json.
  python3 tools/generate_bank.py publish [--banks items_gen_unit06 ...]
      Verify every candidate against the blind formulations in
      var/p4/resolve/<bank>/key_formulations.py, the template's own answer, the duplicate gate and
      the record checks; write published items to content/<bank>/ and everything else to
      content/generation_review/.
"""
import argparse
import collections
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.generation import spec as spec_module
from app.generation.instantiate import instantiate, item_id
from app.generation.template import library, run_family, spec_for, template_modules

CANDIDATES = ROOT / "var" / "p4" / "candidates"
RESOLVE = ROOT / "var" / "p4" / "resolve"
GATE_REPORT = ROOT / "var" / "p4" / "gate_report.json"
CONTENT = ROOT / "content"
REVIEW = CONTENT / "generation_review"

BANK_TARGET = 20
SPARES = 2
MINIMUM_PER_TEMPLATE = 5
TARGET_PROBES = 60
MAX_TRIES_PER_ITEM = 40
TARGET_TOLERANCE = 0.15
GENERATED_PREFIX = "items_gen_"


def bank_for(archetype):
   unit = archetype["primary_unit"].split("-")[-1]

   return f"{GENERATED_PREFIX}unit{unit}"


def existing_counts():
   """Signed-off items already served, by archetype, from every bank that is not generated."""
   counts = collections.Counter()

   for directory in sorted(CONTENT.glob("items_*")):
      is_generated = directory.name.startswith(GENERATED_PREFIX)

      if is_generated:
         continue

      for path in directory.glob("ITM-*.json"):
         counts[json.loads(path.read_text())["archetype_id"]] += 1

   return counts


def wanted_count(existing):
   short_of_target = max(BANK_TARGET - existing, 0)

   if short_of_target == 0:
      return MINIMUM_PER_TEMPLATE

   return short_of_target + SPARES


def difficulty_targets(module, spec):
   """Three requested success probabilities spread over what the family can realise, so the
   batch asks for easier and harder items rather than whatever the draws happen to give."""
   archetype = library().archetypes[module.ARCHETYPE_ID]
   predictions = []

   for index in range(TARGET_PROBES):
      record = instantiate(module, 0, f"{module.ARCHETYPE_ID}:targets:{index}", generated_at="probe")
      predictions.append(record["predicted_success_probability"])

   predictions.sort()

   return [predictions[int(len(predictions) * share)] for share in (0.2, 0.5, 0.8)], archetype


def plan_archetype(module, count, generated_at, start=0):
   spec = spec_for(module)
   targets, _archetype = difficulty_targets(module, spec)
   records = []
   seen = set()
   tries = 0

   while len(records) < count and tries < count * MAX_TRIES_PER_ITEM:
      index = start + len(records)
      target = targets[index % len(targets)]
      seed = f"{module.ARCHETYPE_ID}:spec-{spec['spec_version']}:item-{index}:try-{tries}"
      tries += 1
      record = instantiate(module, index, seed, generated_at=generated_at)
      identity = record["stem"]["text"] + json.dumps(record.get("figure"), sort_keys=True)
      is_repeat = identity in seen
      off_target = abs(record["predicted_success_probability"] - target) > TARGET_TOLERANCE
      last_chance = tries >= count * MAX_TRIES_PER_ITEM - (count - len(records))

      if is_repeat:
         continue

      if off_target and not last_chance:
         continue

      seen.add(identity)
      record["provenance"]["requested_success_probability"] = target
      records.append(record)

   return records


def stems_entry(record):
   entry = {"id": record["id"], "archetype_id": record["archetype_id"], "stem": record["stem"]["text"]}

   if record.get("figure"):
      entry["figure"] = record["figure"]

   is_statement = record["answer_key"]["form"] == "statement"

   if is_statement:
      entry["choices"] = sorted(option["label"] for option in record["options"])

   if record["answer_key"]["form"] == "numeric":
      entry["answer_format"] = "a decimal correct to three places"

   return entry


def passing_templates(modules):
   report = json.loads(GATE_REPORT.read_text()) if GATE_REPORT.exists() else []
   passed = {entry["archetype_id"] for entry in report if entry["passed"]}

   return {archetype_id: module for archetype_id, module in modules.items() if archetype_id in passed}


def plan(arguments):
   modules = template_modules()
   wanted_ids = arguments.archetypes or sorted(modules)
   modules = {archetype_id: modules[archetype_id] for archetype_id in wanted_ids}

   if arguments.gate:
      reports = [run_family(module).as_dict() for module in modules.values()]
      previous = json.loads(GATE_REPORT.read_text()) if GATE_REPORT.exists() else []
      merged = {entry["archetype_id"]: entry for entry in previous}
      merged.update({entry["archetype_id"]: entry for entry in reports})
      GATE_REPORT.parent.mkdir(parents=True, exist_ok=True)
      GATE_REPORT.write_text(json.dumps(sorted(merged.values(), key=lambda entry: entry["archetype_id"]), indent=1) + "\n")

   eligible = passing_templates(modules)
   counts = existing_counts()
   generated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
   by_bank = collections.defaultdict(list)

   for archetype_id, module in sorted(eligible.items()):
      archetype = library().archetypes[archetype_id]
      count = arguments.count or wanted_count(counts[archetype_id])
      records = plan_archetype(module, count, generated_at, arguments.start)
      by_bank[bank_for(archetype)].extend(records)
      print(f"{archetype_id}: {len(records)} candidates ({counts[archetype_id]} signed-off items already served)")

   for bank, records in sorted(by_bank.items()):
      candidate_dir = CANDIDATES / bank
      candidate_dir.mkdir(parents=True, exist_ok=True)

      for record in records:
         (candidate_dir / f"{record['id']}.json").write_text(json.dumps(record, indent=3) + "\n")

      resolve_dir = RESOLVE / bank
      resolve_dir.mkdir(parents=True, exist_ok=True)
      stems_path = resolve_dir / f"stems_{arguments.batch}.json"
      existing_stems = json.loads(stems_path.read_text()) if stems_path.exists() else []
      by_id = {entry["id"]: entry for entry in existing_stems}
      by_id.update({record["id"]: stems_entry(record) for record in records})
      stems_path.write_text(json.dumps([by_id[key] for key in sorted(by_id)], indent=1) + "\n")

   skipped = sorted(set(modules) - set(eligible))
   print(f"{sum(len(records) for records in by_bank.values())} candidates in {len(by_bank)} banks; "
         f"{len(skipped)} templates without a passing gate report: {skipped}")

   return 0


AGGREGATOR = '''"""The blind formulations for this bank, one part per solver run.

Each formulations_<batch>.py was written by a separate Claude Code session from the stems alone
(prompts/verifier/independent_resolve_v1.md), never from the keys. tools/key_recheck.py reads
FORMULATIONS from this file.
"""
import runpy
from pathlib import Path

FORMULATIONS = {}

for part in sorted(Path(__file__).parent.glob("formulations_*.py")):
   FORMULATIONS.update(runpy.run_path(str(part))["FORMULATIONS"])
'''


def write_aggregator(directory):
   directory.mkdir(parents=True, exist_ok=True)
   path = directory / "key_formulations.py"
   path.write_text(AGGREGATOR)

   return path


def publish(arguments):
   from tools.key_recheck import load_formulations, recheck
   from app.generation.dedupe import DuplicateGate, load_bank_records, load_official_pages
   from app.generation.verify import PUBLISHED, Verdict, verify

   banks = arguments.banks or sorted(path.name for path in CANDIDATES.iterdir() if path.is_dir())
   candidate_ids = set()
   candidate_records = []

   for bank in banks:
      for path in sorted((CANDIDATES / bank).glob("ITM-*.json")):
         record = json.loads(path.read_text())
         candidate_ids.add(record["id"])
         candidate_records.append(record)

   served_records = [record for record in load_bank_records(CONTENT) if record["id"] not in candidate_ids]
   decisions_path = REVIEW / "decisions.json"
   recorded = json.loads(decisions_path.read_text()) if decisions_path.exists() else []
   latest_decisions = {entry["item_id"]: entry for entry in recorded}
   gate = DuplicateGate(load_official_pages(), served_records + candidate_records)
   summary = collections.Counter()
   verdicts = []

   for bank in banks:
      candidate_dir = CANDIDATES / bank
      formulations_path = write_aggregator(RESOLVE / bank)
      formulations = load_formulations(formulations_path)
      results, blind_on = recheck(candidate_dir, formulations, template_answers=True)

      if blind_on:
         print(f"{bank}: the recheck control failed on {blind_on}; nothing from this bank is published", file=sys.stderr)
         continue

      flags_by_id = {result.item_id: result.flags for result in results}
      bank_dir = CONTENT / bank
      bank_dir.mkdir(parents=True, exist_ok=True)

      for path in sorted(candidate_dir.glob("ITM-*.json")):
         record = json.loads(path.read_text())
         target = record["provenance"].get("requested_success_probability")

         try:
            verdict = verify(record, flags_by_id.get(record["id"], ["not_formulated"]), gate=gate, target=target)
         except Exception as failure:
            verdict = Verdict(item_id=record["id"])
            verdict.fail(4, f"a check raised {type(failure).__name__} and settled nothing")

         decision = latest_decisions.get(record["id"])
         decided_for_this_draw = decision is not None and decision.get("parameter_seed") in (None, record["provenance"]["parameter_seed"])

         if decided_for_this_draw:
            verdict.status = PUBLISHED if decision["decision"] == "approve" else "rejected"
            verdict.notes.append(f"review decision: {decision['decision']}, {decision['reason']}")

         verdicts.append(verdict.as_dict())
         summary[verdict.status] += 1
         destination = bank_dir if verdict.status == PUBLISHED else REVIEW / verdict.status
         destination.mkdir(parents=True, exist_ok=True)
         stale = [bank_dir / path.name, REVIEW / "needs_review" / path.name, REVIEW / "rejected" / path.name]

         for stale_path in stale:
            if stale_path.exists():
               stale_path.unlink()

         if verdict.status != PUBLISHED:
            record["review"] = verdict.as_dict()

         (destination / path.name).write_text(json.dumps(record, indent=3) + "\n")

      for part in sorted((RESOLVE / bank).glob("formulations_*.py")):
         shutil.copyfile(part, bank_dir / part.name)

      write_aggregator(bank_dir)

   report_path = CANDIDATES.parent / "publish_report.json"
   report_path.write_text(json.dumps({"summary": summary, "verdicts": verdicts}, indent=1) + "\n")
   print(dict(summary))

   return 0


def main(argv):
   parser = argparse.ArgumentParser(description="Run the P4 generation batch.")
   commands = parser.add_subparsers(dest="command", required=True)
   plan_parser = commands.add_parser("plan")
   plan_parser.add_argument("--archetypes", nargs="*")
   plan_parser.add_argument("--gate", action="store_true", help="rerun the template gate first")
   plan_parser.add_argument("--count", type=int, help="candidates per archetype, instead of filling to the bank target")
   plan_parser.add_argument("--batch", default="main", help="names the stems file one blind solver answers")
   plan_parser.add_argument("--start", type=int, default=0, help="first item index, so a top-up never reuses an id")
   publish_parser = commands.add_parser("publish")
   publish_parser.add_argument("--banks", nargs="*")
   arguments = parser.parse_args(argv)

   if arguments.command == "plan":
      return plan(arguments)

   return publish(arguments)


if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))
