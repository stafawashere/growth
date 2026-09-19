"""Append or refresh a generated 'Official FRQ evidence' section at the end of each unit file,
listing every FRQ and MCQ record whose primary or secondary unit is that unit, with skills tagged.
The section sits between marker comments so re-running replaces it in place.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UNITS = ROOT / "research" / "units"
START = "<!-- generated:official-evidence:start -->"
END = "<!-- generated:official-evidence:end -->"


def main():
   frq = json.loads((DATA / "frq_records.json").read_text())["records"]
   mcq = json.loads((DATA / "mcq_records.json").read_text())["records"]
   topics = {t["id"]: t["unit"] for t in json.loads((DATA / "curriculum.json").read_text())["topics"]}

   for path in sorted(UNITS.glob("unit-*.md")):
      number = int(re.search(r"unit-(\d\d)", path.name).group(1))
      uid = f"BC-UNIT-{number:02d}"
      rows = []

      for r in sorted(frq, key=lambda x: (x["year"], x["question"], x["part"])):
         is_primary = r["primary_unit"] == uid
         is_secondary = uid in r.get("secondary_units", [])

         if is_primary or is_secondary:
            role = "primary" if is_primary else "secondary"
            rows.append(f"| {r['id']} | {role} | {r['calculator']} | {r.get('archetype', '')} | {', '.join(r.get('skills', [])[:6])} | {r.get('points', 0)} | {', '.join(r.get('point_types', []))} |")

      mrows = []

      for m in mcq:
         in_unit = any(topics.get(t) == uid for t in m.get("topics", []))

         if in_unit:
            mrows.append(f"| {m['id']} | {m['calculator']} | {m.get('archetype', '')} | {', '.join(m.get('skills', [])[:4])} |")

      section = [START, "", "## Official evidence index [verified]", "", f"Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with {uid} as primary or secondary unit: {len(rows)}. Public sample MCQ records tagged to this unit: {len(mrows)}.", "", "| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |", "|---|---|---|---|---|---|---|"] + rows + ["", "| MCQ record | Calculator | Archetype | Skills |", "|---|---|---|---|"] + mrows + ["", END]
      text = path.read_text()
      has_section = START in text

      if has_section:
         text = re.sub(re.escape(START) + ".*?" + re.escape(END), "\n".join(section), text, flags=re.S)
      else:
         text = text.rstrip("\n") + "\n\n" + "\n".join(section) + "\n"

      path.write_text(text)
      print(path.name, len(rows), "frq", len(mrows), "mcq")


if __name__ == "__main__":
   main()
