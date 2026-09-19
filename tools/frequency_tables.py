"""Compute observed historical frequency tables from data/frq_records.json and write them as Markdown
fragments to cache/frequency/ for inclusion in research/question-analysis/historical-frequency.md.
Counts only. Denominators are the years actually indexed. 2021 is flagged as anomalous.
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "cache" / "frequency"
ANOMALOUS = {2021}


def load(name):
   return json.loads((DATA / name).read_text())


def table(headers, rows):
   lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
   lines += ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
   return "\n".join(lines) + "\n"


def main():
   OUT.mkdir(parents=True, exist_ok=True)
   records = load("frq_records.json")["records"]
   archetypes = {a["id"]: a for a in load("archetypes.json")["archetypes"]}
   units = {u["id"]: u for u in load("curriculum.json")["units"]}
   years = sorted({r["year"] for r in records})
   normal_years = [y for y in years if y not in ANOMALOUS]
   fragments = {}

   fragments["years"] = f"Indexed years: {', '.join(str(y) for y in years)} ({len(years)} administrations; {len(normal_years)} after excluding the anomalous {sorted(ANOMALOUS)}). Question-part records: {len(records)}.\n"

   fam_year = defaultdict(set)
   fam_parts = Counter()
   fam_calc = defaultdict(Counter)
   fam_units = defaultdict(Counter)

   for r in records:
      a = archetypes.get(r.get("archetype"))
      family = a.get("family", "unassigned") if a else "unassigned"
      fam_year[family].add(r["year"])
      fam_parts[family] += 1
      fam_calc[family][r["calculator"]] += 1

      for u in [r["primary_unit"]] + r.get("secondary_units", []):
         fam_units[family][u] += 1

   rows = []

   for family in sorted(fam_year, key=lambda f: -len(fam_year[f])):
      ys = fam_year[family]
      normal = len([y for y in ys if y not in ANOMALOUS])
      rows.append([family, f"{normal} of {len(normal_years)}", ", ".join(str(y) for y in sorted(ys)), fam_parts[family], fam_calc[family]["calculator"], fam_calc[family]["no_calculator"]])

   fragments["family_by_year"] = table(["Archetype family", "Years present (of indexed, excluding 2021)", "Years", "Part records", "Calculator parts", "No-calculator parts"], rows)

   unit_year = defaultdict(Counter)

   for r in records:
      unit_year[r["primary_unit"]][r["year"]] += 1

   rows = []

   for uid in sorted(unit_year):
      counts = unit_year[uid]
      rows.append([uid, units[uid]["name"] if uid in units else uid, sum(counts.values())] + [counts.get(y, 0) for y in years])

   fragments["unit_by_year"] = table(["Unit id", "Unit", "Total parts"] + [str(y) for y in years], rows)

   qnum = defaultdict(Counter)

   for r in records:
      qnum[r["question"]][r["primary_unit"]] += 1

   rows = [[q, ", ".join(f"{u} ({c})" for u, c in qnum[q].most_common())] for q in sorted(qnum)]
   fragments["question_slot_units"] = table(["Question number", "Primary units of part records (count)"], rows)

   combos = Counter()

   for r in records:
      us = sorted(set([r["primary_unit"]] + r.get("secondary_units", [])))
      is_multi = len(us) > 1

      if is_multi:
         combos[" + ".join(us)] += 1

   rows = [[k, v] for k, v in combos.most_common(30)]
   fragments["unit_combinations"] = table(["Units combined in one part", "Part records"], rows)

   arche_year = defaultdict(set)
   arche_parts = Counter()

   for r in records:
      arche_year[r.get("archetype")].add(r["year"])
      arche_parts[r.get("archetype")] += 1

   rows = []

   for aid in sorted(arche_year, key=lambda x: (-len(arche_year[x]), x)):
      a = archetypes.get(aid, {})
      rows.append([aid, a.get("name", "")[:70], len([y for y in arche_year[aid] if y not in ANOMALOUS]), ", ".join(str(y) for y in sorted(arche_year[aid])), arche_parts[aid]])

   fragments["archetype_by_year"] = table(["Archetype", "Name", "Years (excl. 2021)", "Years", "Parts"], rows)

   part_letters = Counter(r["part"] for r in records)
   fragments["parts_per_question"] = table(["Part", "Records"], [[k, v] for k, v in sorted(part_letters.items())])

   for name, text in fragments.items():
      (OUT / f"{name}.md").write_text(text)

   print({k: len(v) for k, v in fragments.items()})


if __name__ == "__main__":
   main()
