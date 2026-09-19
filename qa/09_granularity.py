"""Skills-per-topic distribution; flag topics more than 2x the median or with zero skills."""
from collections import Counter
from statistics import median
from qa_common import load_json, finish

failures, warnings = [], []
curriculum = load_json("curriculum.json")
skills = load_json("skills.json")

if not (curriculum and skills):
   finish("09_granularity", ["curriculum.json or skills.json missing"])

counts = Counter(skill["topic"] for skill in skills["skills"])
values = [counts.get(topic["id"], 0) for topic in curriculum["topics"]]
mid = median(values) if values else 0
warnings.append(f"skills per topic: min {min(values)} median {mid} max {max(values)} total {sum(values)}")

for topic in curriculum["topics"]:
   count = counts.get(topic["id"], 0)
   is_outlier = mid and count > 2 * mid
   has_justification = bool(topic.get("granularity_note"))

   if is_outlier and not has_justification:
      warnings.append(f"{topic['id']} ({topic['ced_code']}) has {count} skills vs median {mid}")

for skill in skills["skills"]:
   words = skill["name"].split()
   is_too_long = len(words) > 14

   if is_too_long:
      warnings.append(f"{skill['id']} name is {len(words)} words")

finish("09_granularity", failures, warnings)
