"""The item review queue for generated items (docs/plan/04-item-generation.md, "Review queue").

Every item the publication rule did not publish sits in content/generation_review/needs_review/
or content/generation_review/rejected/ with its provenance and the verdict that stopped it. This
tool shows one item the way 04 says a reviewer sees it and records the decision; a rejected item
is kept, never deleted, because it is what a template or prompt fix is tested against.

Usage:
  python3 tools/item_review.py list
  python3 tools/item_review.py show ITM-GEN-06004-01
  python3 tools/item_review.py decide ITM-GEN-06004-01 approve|reject --reason "..." --by "..."
  python3 tools/item_review.py groups
  python3 tools/item_review.py duplicates --by "..."

duplicates settles every item held only by the duplicate gate (rules 10 and 11), in id order,
against the bank as served at that moment, so of a set of copies exactly the first is kept.
"""
import argparse
import collections
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REVIEW = ROOT / "content" / "generation_review"
CONTENT = ROOT / "content"
DECISIONS = REVIEW / "decisions.json"
GATE_REPORT = ROOT / "var" / "p4" / "gate_report.json"
STATES = ("needs_review", "rejected")


def queued_paths():
   return [path for state in STATES for path in sorted((REVIEW / state).glob("ITM-*.json"))]


def find(item_id):
   for path in queued_paths():
      if path.stem == item_id:
         return path

   raise SystemExit(f"{item_id} is not in the review queue")


def decisions():
   return json.loads(DECISIONS.read_text()) if DECISIONS.exists() else []


def list_queue():
   for path in queued_paths():
      record = json.loads(path.read_text())
      review = record.get("review", {})
      print(f"{path.parent.name:13} {record['id']}  rules {review.get('rules')}  {'; '.join(review.get('notes', []))[:120]}")

   print(f"{len(queued_paths())} items in the queue")


def show(item_id):
   record = json.loads(find(item_id).read_text())
   review = record.get("review", {})
   provenance = record.get("provenance", {})
   gate = {entry["archetype_id"]: entry for entry in json.loads(GATE_REPORT.read_text())} if GATE_REPORT.exists() else {}
   family = gate.get(record["archetype_id"], {})

   print(f"Failing rules: {review.get('rules')}  status {review.get('status')}")
   print(f"Notes: {review.get('notes')}")
   print(f"\nStem: {record['stem']['text']}")

   if record.get("figure"):
      print(f"Figure ({record['figure']['kind']}): {record['figure'].get('alt')}")

   print(f"\nKey: {json.dumps(record['answer_key'])}")

   for step in record["worked_solution"]:
      print(f"  step {step['step']} [{step.get('point_type_id', '')}] {step['text']}")

   for option in record["options"]:
      shown = option.get("label") or json.dumps(option.get("value"))
      tag = "KEY" if option["is_key"] else f"{option['error_path']} {option.get('mechanism')}: {option.get('derivation')}"
      print(f"  {option['id']}. {shown}   <- {tag}")

   print(f"\nMonte Carlo: {family.get('draws')} draws, {family.get('failure_count')} failures, space {family.get('draw_space')}")
   print(f"Dials: {record.get('difficulty_settings')}  predicted {record.get('predicted_success_probability')} "
         f"against requested {provenance.get('requested_success_probability')}")
   print(f"Provenance: {json.dumps(provenance)}")


def decide(item_id, verdict, reason, by):
   path = find(item_id)
   record = json.loads(path.read_text())
   review = record.get("review", {})
   entry = {
      "item_id": item_id,
      "decision": verdict,
      "reason": reason,
      "by": by,
      "decided_on": str(date.today()),
      "rules": review.get("rules"),
      "archetype_id": record["archetype_id"],
      "prompt_version": record.get("provenance", {}).get("prompt_version"),
      "template_id": record.get("provenance", {}).get("template_id"),
      "parameter_seed": record.get("provenance", {}).get("parameter_seed"),
   }

   if verdict == "approve":
      from app.generation.template import library
      from tools.generate_bank import bank_for

      destination_dir = CONTENT / bank_for(library().archetypes[record["archetype_id"]])
      record.pop("review", None)
      record["review_decision"] = entry
      destination_dir.mkdir(parents=True, exist_ok=True)
      (destination_dir / path.name).write_text(json.dumps(record, indent=3) + "\n")
      path.unlink()
   else:
      record["review_decision"] = entry
      rejected = REVIEW / "rejected" / path.name
      rejected.parent.mkdir(parents=True, exist_ok=True)
      rejected.write_text(json.dumps(record, indent=3) + "\n")

      if path != rejected:
         path.unlink()

   DECISIONS.write_text(json.dumps(decisions() + [entry], indent=1) + "\n")
   print(f"{item_id}: {verdict}")


def groups():
   """Rejections grouped by rule and template version: a group that keeps growing is a template or
   prompt defect, not a draw defect (04, "How a rejection feeds a prompt fix")."""
   counts = collections.Counter()

   for entry in decisions():
      if entry["decision"] != "reject":
         continue

      for rule in entry["rules"] or [None]:
         counts[(rule, entry["template_id"])] += 1

   for (rule, template_id), count in counts.most_common():
      print(f"rule {rule}  {template_id}  {count}")


DUPLICATE_RULES = {10, 11}


def duplicates(by):
   """Take the items held only by the duplicate gate in id order, and check each against the bank
   as it is served now, the items approved before it included: one that still duplicates a
   served item is rejected, and one that no longer does is approved, so of a set of copies
   exactly the first is kept."""
   from app.generation import dedupe

   official_pages = dedupe.load_official_pages()

   for path in sorted((REVIEW / "needs_review").glob("ITM-*.json")):
      record = json.loads(path.read_text())
      rules = set(record.get("review", {}).get("rules") or [])
      held_only_as_duplicate = bool(rules) and rules <= DUPLICATE_RULES

      if not held_only_as_duplicate:
         continue

      gate = dedupe.DuplicateGate(official_pages, dedupe.load_bank_records(CONTENT))
      verdict = gate.check(record)

      if verdict.blocked:
         neighbour = verdict.stage_one.neighbour if verdict.stage_one.hit else verdict.stage_two.neighbour
         decide(record["id"], "reject", f"duplicate of the served item {neighbour}", by)
      else:
         decide(record["id"], "approve", "no served item duplicates it once its copies were settled in id order", by)


def main(argv):
   parser = argparse.ArgumentParser(description="Review generated items the publication rule held back.")
   parser.add_argument("command", choices=("list", "show", "decide", "groups", "duplicates"))
   parser.add_argument("item_id", nargs="?")
   parser.add_argument("verdict", nargs="?", choices=("approve", "reject"))
   parser.add_argument("--reason")
   parser.add_argument("--by")
   arguments = parser.parse_args(argv)

   if arguments.command == "list":
      list_queue()
   elif arguments.command == "show":
      show(arguments.item_id)
   elif arguments.command == "groups":
      groups()
   elif arguments.command == "duplicates":
      duplicates(arguments.by)
   else:
      has_reason = bool(arguments.reason) and bool(arguments.by)

      if not has_reason:
         raise SystemExit("a decision needs --reason and --by")

      decide(arguments.item_id, arguments.verdict, arguments.reason, arguments.by)

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))
