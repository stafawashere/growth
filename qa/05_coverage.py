"""CED coverage: every topic, LO, EK, and practice skill from curriculum.json appears in the unit files; FRQ coverage matrix."""
import re
from qa_common import ROOT, RESEARCH, load_json, ids_in_text, finish

failures, warnings = [], []
curriculum = load_json("curriculum.json")
has_curriculum = curriculum is not None

if not has_curriculum:
   finish("05_coverage", ["curriculum.json missing"])

unit_text = {}

for path in sorted((RESEARCH / "units").glob("unit-*.md")):
   number = int(re.search(r"unit-(\d\d)", path.name).group(1))
   unit_text[number] = ids_in_text(path.read_text())

for unit in curriculum["units"]:
   number = unit["number"]
   has_file = number in unit_text

   if not has_file:
      failures.append(f"unit {number} has no unit file")
      continue

   present = unit_text[number]

   for topic_id in unit["topics"]:
      if topic_id not in present:
         failures.append(f"unit {number} file lacks topic {topic_id}")

topic_unit = {topic["id"]: topic["unit"] for topic in curriculum["topics"]}
unit_number = {unit["id"]: unit["number"] for unit in curriculum["units"]}
all_unit_ids = set().union(*unit_text.values()) if unit_text else set()

for lo in curriculum["learning_objectives"]:
   if lo["id"] not in all_unit_ids:
      failures.append(f"{lo['id']} ({lo['ced_code']}) not in any unit file")

for ek in curriculum["essential_knowledge"]:
   if ek["id"] not in all_unit_ids:
      failures.append(f"{ek['id']} ({ek['ced_code']}) not in any unit file")

skills = load_json("skills.json")
has_skills = skills is not None

if has_skills:
   covered_topics = {skill["topic"] for skill in skills["skills"]}

   for topic in curriculum["topics"]:
      if topic["id"] not in covered_topics:
         failures.append(f"{topic['id']} ({topic['ced_code']}) has no atomic skills")

frq = load_json("frq_records.json")
has_frq = frq is not None

if has_frq:
   years = sorted({record["year"] for record in frq["records"]})
   warnings.append(f"FRQ records cover years {years}")

   for year in years:
      questions = {record["question"] for record in frq["records"] if record["year"] == year}
      is_complete = questions == {1, 2, 3, 4, 5, 6}

      if not is_complete:
         warnings.append(f"{year} indexes questions {sorted(questions)} only")

finish("05_coverage", failures, warnings)
