"""Adaptive metadata must be skill-specific: strip ids and numbers from mastered_if and partially_mastered_if,
then require at least 80 percent distinct sentence skeletons per unit and no empty required keys."""
import re
from collections import defaultdict
from qa_common import load_json, finish

REQUIRED = ["mastered_if", "partially_mastered_if", "prerequisite_gap_if", "common_confusions", "next_dependent_skills", "diagnostic_archetypes", "remediation_target"]
MIN_DISTINCT = 0.8
failures, warnings = [], []
skills = load_json("skills.json")

if skills is None:
   finish("13_adaptive", ["skills.json missing"])


def skeleton(text):
   text = re.sub(r"BC-[A-Z]+-[A-Z0-9-]+", "ID", text)
   text = re.sub(r"\d+", "N", text)
   return re.sub(r"\s+", " ", text.lower()).strip()


per_unit = defaultdict(list)

for skill in skills["skills"]:
   adaptive = skill.get("adaptive", {})

   for key in REQUIRED:
      value = adaptive.get(key)
      is_missing = key not in adaptive
      is_empty_string = isinstance(value, str) and not value.strip()
      is_empty_list = isinstance(value, list) and not value

      if is_missing or is_empty_string:
         failures.append(f"{skill['id']} adaptive.{key} missing or empty")
      elif is_empty_list:
         warnings.append(f"{skill['id']} adaptive.{key} is an empty list")

   per_unit[skill["unit"]].append(skeleton(str(adaptive.get("mastered_if", ""))) + " || " + skeleton(str(adaptive.get("partially_mastered_if", ""))))

for unit, skeletons in sorted(per_unit.items()):
   distinct = len(set(skeletons)) / len(skeletons)
   is_templated = distinct < MIN_DISTINCT
   line = f"{unit}: {len(set(skeletons))} distinct skeletons of {len(skeletons)} ({distinct:.0%})"

   if is_templated:
      failures.append(line + " below 80 percent")
   else:
      warnings.append(line)

finish("13_adaptive", failures, warnings)
