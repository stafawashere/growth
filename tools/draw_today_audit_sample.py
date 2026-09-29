"""Draws a stratified audit sample over the item bank on disk.

tools/draw_key_audit_sample.py draws operator-provenance items from a database, and every item in
the bank is an agent draft or a template instantiation, so it has nothing to draw from. This tool
reads every content/items_*/ directory instead and stratifies on unit (the first two-digit block
of the archetype id), provenance class, format and calculator status.

Units get a share in proportion to the bank, with a floor of 4 for any unit holding at least 4
items and a cap of 12. Inside a unit, provenance classes get a share in proportion with a floor
of 1 for every class present, and inside that calculator status is drawn in proportion. Short
answer items are rare, so the sample holds at least 6 of them when the bank does, swapped in for
multiple choice items of the same unit and provenance class.

--stems-only writes what a blind re-solver reads: the stem, the figure when there is one, and the
options in an order seeded by the item id, relabelled A, B, C, D, without is_key, error_path or
any distractor rationale. The option order is recorded in the main sample file so a verdict can be
mapped back to the key.

Usage: .venv/bin/python tools/draw_today_audit_sample.py <out.json> [--size 72] [--seed 2026]
   [--content-root content] [--stems-only <path>]
"""
import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SIZE = 72
DEFAULT_SEED = 2026

UNIT_FLOOR = 4
UNIT_CAP = 12
PROVENANCE_FLOOR = 1
SHORT_ANSWER_FLOOR = 6

TEMPLATE = "template"
AGENT_DRAFT = "agent_draft"
P1_DRAFT = "p1_draft"
UNCLASSIFIED = "unclassified"

P1_DRAFT_MARKER = "pending operator review"
SHORT_ANSWER = "short_answer"

ARCHETYPE_PATTERN = re.compile(r"^BC-QA-(\d{2})\d{3}$")

OPTION_TEXT_FIELDS = ("label", "value", "text")

STRATA = ("unit", "provenance_class", "format", "calculator_status", "representation", "figure_signal")


def unit_of(archetype_id):
   match = ARCHETYPE_PATTERN.match(archetype_id or "")

   if match is None:
      raise ValueError(f"archetype id {archetype_id!r} has no unit block")

   return match.group(1)


def provenance_class_of(record):
   template_id = (record.get("provenance") or {}).get("template_id")
   is_template = template_id is not None

   if is_template:
      return TEMPLATE

   author = record.get("drafted_by") or record.get("authored_by")
   names_no_author = author is None

   if names_no_author:
      return UNCLASSIFIED

   awaits_operator_review = P1_DRAFT_MARKER in author

   if awaits_operator_review:
      return P1_DRAFT

   return AGENT_DRAFT


def stem_text_of(record):
   stem = record.get("stem")

   if isinstance(stem, dict):
      return stem.get("text", "")

   return stem or ""


def figure_signal_of(record):
   """The stem check is a crude text match, so it is named as one rather than folded into the
   figure keys."""
   if record.get("figure"):
      return "figure_key"

   if record.get("figure_spec"):
      return "figure_spec_key"

   mentions_table = "table" in stem_text_of(record).lower()

   if mentions_table:
      return "stem_mentions_table"

   return "none"


def load_bank(content_root):
   content_root = Path(content_root)
   item_dirs = []

   for path in sorted(content_root.iterdir()):
      is_item_dir = path.is_dir() and path.name.startswith("items_")

      if is_item_dir:
         item_dirs.append(path)

   rows = []

   for item_dir in item_dirs:
      for path in sorted(item_dir.glob("*.json")):
         record = json.loads(path.read_text())
         figure_signal = figure_signal_of(record)

         rows.append({
            "item_id": record["id"],
            "path": str(path),
            "archetype_id": record["archetype_id"],
            "unit": unit_of(record["archetype_id"]),
            "format": record["format"],
            "provenance_class": provenance_class_of(record),
            "calculator_status": record["calculator_status"],
            "representation": record.get("representation"),
            "has_figure": figure_signal != "none",
            "figure_signal": figure_signal,
         })

   return rows


def allocate(counts_by_key, total, floors, caps):
   """Starts every key at its floor and hands out the rest one at a time to the key furthest
   below its proportional share, ties broken by key, never past its cap."""
   population = sum(counts_by_key.values())
   targets = dict(floors)
   remaining = total - sum(targets.values())
   capacity = sum(caps.values())

   if remaining < 0:
      raise ValueError(f"the floors ask for {sum(targets.values())} items but only {total} are drawn")

   if capacity < total:
      raise ValueError(f"the caps allow {capacity} items but {total} are drawn")

   ideal = {key: total * count / population for key, count in counts_by_key.items()}

   for _ in range(remaining):
      open_keys = [key for key in counts_by_key if targets[key] < caps[key]]
      neediest = min(open_keys, key=lambda key: (-(ideal[key] - targets[key]), key))
      targets[neediest] += 1

   return targets


def group_by(rows, field):
   groups = defaultdict(list)

   for row in rows:
      groups[row[field]].append(row)

   return groups


def unit_targets(by_unit, size):
   counts = {unit: len(rows) for unit, rows in by_unit.items()}
   floors = {unit: UNIT_FLOOR if count >= UNIT_FLOOR else 0 for unit, count in counts.items()}
   caps = {unit: min(count, UNIT_CAP) for unit, count in counts.items()}

   return allocate(counts, size, floors, caps)


def provenance_floors(counts, unit_target):
   """A unit drawn smaller than its number of classes floors its largest classes first."""
   floors = {name: 0 for name in counts}
   largest_first = sorted(counts, key=lambda name: (-counts[name], name))

   for name in largest_first[:unit_target]:
      floors[name] = PROVENANCE_FLOOR

   return floors


def draw_cell(cell_rows, cell_target, rng):
   by_status = group_by(cell_rows, "calculator_status")
   counts = {status: len(rows) for status, rows in by_status.items()}
   floors = {status: 0 for status in counts}
   targets = allocate(counts, cell_target, floors, counts)
   drawn = []

   for status in sorted(by_status):
      pool = list(by_status[status])
      rng.shuffle(pool)
      drawn.extend(pool[:targets[status]])

   return drawn


def replaceable_for(candidate, selected):
   """Multiple choice rows the candidate may displace, nearest first: its own unit and
   provenance class, then its own unit without emptying another class, then any unit without
   emptying a class. Short answer items sit in only a few units and classes, so the later tiers
   are what let the floor hold."""
   cell_sizes = Counter((row["unit"], row["provenance_class"]) for row in selected)
   same_cell = []
   same_unit = []
   anywhere = []

   for index, row in enumerate(selected):
      is_multiple_choice = row["format"] != SHORT_ANSWER

      if not is_multiple_choice:
         continue

      shares_unit = row["unit"] == candidate["unit"]
      shares_provenance = row["provenance_class"] == candidate["provenance_class"]
      leaves_its_class_drawn = cell_sizes[(row["unit"], row["provenance_class"])] > PROVENANCE_FLOOR
      is_same_cell = shares_unit and shares_provenance
      is_same_unit = shares_unit and leaves_its_class_drawn

      if is_same_cell:
         same_cell.append(index)
      elif is_same_unit:
         same_unit.append(index)
      elif leaves_its_class_drawn:
         anywhere.append(index)

   return same_cell or same_unit or anywhere


def swap_in_short_answers(rows, selected, rng):
   bank_short_answers = [row for row in rows if row["format"] == SHORT_ANSWER]
   floor = min(SHORT_ANSWER_FLOOR, len(bank_short_answers))
   selected_ids = {row["item_id"] for row in selected}
   drawn_short_answers = sum(1 for row in selected if row["format"] == SHORT_ANSWER)
   waiting = [row for row in bank_short_answers if row["item_id"] not in selected_ids]
   rng.shuffle(waiting)

   for candidate in waiting:
      if drawn_short_answers >= floor:
         break

      replaceable = replaceable_for(candidate, selected)
      has_room = len(replaceable) > 0

      if not has_room:
         continue

      same_status = [
         index for index in replaceable
         if selected[index]["calculator_status"] == candidate["calculator_status"]
      ]
      choices = same_status or replaceable
      selected[rng.choice(choices)] = candidate
      drawn_short_answers += 1

   return selected


def draw_sample(rows, size, seed):
   if size > len(rows):
      raise ValueError(f"the bank holds {len(rows)} items; {size} were requested")

   ordered = sorted(rows, key=lambda row: row["item_id"])
   rng = random.Random(seed)
   by_unit = group_by(ordered, "unit")
   targets = unit_targets(by_unit, size)
   selected = []

   for unit in sorted(by_unit):
      by_provenance = group_by(by_unit[unit], "provenance_class")
      counts = {name: len(cell) for name, cell in by_provenance.items()}
      floors = provenance_floors(counts, targets[unit])
      provenance_targets = allocate(counts, targets[unit], floors, counts)

      for name in sorted(by_provenance):
         selected.extend(draw_cell(by_provenance[name], provenance_targets[name], rng))

   selected = swap_in_short_answers(ordered, selected, rng)

   return sorted(selected, key=lambda row: row["item_id"])


def strata_counts(rows):
   return {
      stratum: dict(sorted(Counter(str(row[stratum]) for row in rows).items()))
      for stratum in STRATA
   }


def presented_options(record):
   options = list(record.get("options") or [])
   random.Random(record["id"]).shuffle(options)
   presented = []

   for position, option in enumerate(options):
      shown = {"choice": chr(ord("A") + position)}

      for field in OPTION_TEXT_FIELDS:
         if field in option:
            shown[field] = option[field]

      presented.append(shown)

   original_order = [option["id"] for option in options]

   return presented, original_order


def stems_only_entry(row, record, presented):
   entry = {
      "item_id": row["item_id"],
      "archetype_id": row["archetype_id"],
      "unit": row["unit"],
      "format": row["format"],
      "stem": stem_text_of(record),
   }

   if record.get("figure"):
      entry["figure"] = record["figure"]

   entry["options"] = presented

   return entry


def markdown_tables(sample, bank):
   sample_counts = strata_counts(sample)
   bank_counts = strata_counts(bank)
   lines = []

   for stratum in ("unit", "provenance_class", "format", "calculator_status"):
      lines.append(f"| {stratum} | sample | bank |")
      lines.append("|---|---:|---:|")

      for value, bank_count in bank_counts[stratum].items():
         lines.append(f"| {value} | {sample_counts[stratum].get(value, 0)} | {bank_count} |")

      lines.append(f"| total | {len(sample)} | {len(bank)} |")
      lines.append("")

   return "\n".join(lines)


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Draw a stratified audit sample over the item bank on disk.")
   parser.add_argument("out")
   parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
   parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
   parser.add_argument("--content-root", default="content")
   parser.add_argument("--stems-only")

   return parser.parse_args(argv)


def main(argv=None):
   arguments = parse_arguments(argv)
   bank = load_bank(arguments.content_root)

   try:
      sample = draw_sample(bank, arguments.size, arguments.seed)
   except ValueError as refused:
      print(f"cannot draw the sample: {refused}", file=sys.stderr)

      return 1

   sample_entries = []
   stems_entries = []

   for row in sample:
      record = json.loads(Path(row["path"]).read_text())
      presented, original_order = presented_options(record)
      entry = dict(row)
      entry["stems_option_order"] = original_order
      sample_entries.append(entry)
      stems_entries.append(stems_only_entry(row, record, presented))

   output = {
      "seed": arguments.seed,
      "size": arguments.size,
      "drawn_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
      "figure_signal_note": (
         "has_figure is true when the record carries a figure key or a figure_spec key, or when "
         "the stem text contains the word table, which is a crude text match"
      ),
      "strata_counts": strata_counts(bank),
      "sample": sample_entries,
   }

   out_path = Path(arguments.out)
   out_path.parent.mkdir(parents=True, exist_ok=True)
   out_path.write_text(json.dumps(output, indent=2))

   if arguments.stems_only:
      stems_path = Path(arguments.stems_only)
      stems_path.parent.mkdir(parents=True, exist_ok=True)
      stems_path.write_text(json.dumps({"seed": arguments.seed, "items": stems_entries}, indent=2))

   print(markdown_tables(sample, bank))
   print(f"drew {len(sample)} of {len(bank)} items, seed {arguments.seed}, wrote {out_path}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
