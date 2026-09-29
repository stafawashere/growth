"""Derive confusable_with on BC-SKL records and write data/staging/corrections-skills-confusable.json.

A pair of skills is confusable when a student at the moment of choosing a method reaches for one in
place of the other. Candidate pairs come from three routes, each counted as a separate source:

cc      skill a names skill b in adaptive.common_confusions (cross-unit allowed, the text names b)
mis     skill a names misconception m in adaptive.common_confusions and skill b lists m in misconceptions
rival   as mis, but b lists one of m's rival_misconceptions
method  an archetype wrong approach names another archetype's method (see METHOD_NAMES)

mis and rival pairs are kept only inside one unit, because no misconception record names a skill in
its text. Pairs joined by a hard_prerequisite edge in data/prereq_edges.csv are dropped. The relation
is symmetric, and each list is capped by admitting pairs in order of independent source count.
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUT = DATA / "staging" / "corrections-skills-confusable.json"
LIST_CAP = 6

SKILL_ID = re.compile(r"BC-SKL-\d{5}")
MISCONCEPTION_ID = re.compile(r"BC-MIS-\d{5}")
ERROR_ID = re.compile(r"BC-ERR-\d{5}")

# Reviewed map from a phrase in an archetype's wrong_approaches to the archetype whose method it names.
# Each entry is (archetype holding the wrong approach, pattern in the wrong approach, archetype named).
METHOD_NAMES = [
   ("BC-QA-02002", r"power rule", "BC-QA-02006"),
   ("BC-QA-02007", r"power rule", "BC-QA-02006"),
   ("BC-QA-02008", r"numerator and denominator separately", "BC-QA-04009"),
   ("BC-QA-02010", r"numerator and denominator of the rewritten quotient separately", "BC-QA-04009"),
   ("BC-QA-03009", r"power rule", "BC-QA-02006"),
   ("BC-QA-04008", r"solving the differential equation", "BC-QA-07003"),
   ("BC-QA-04009", r"quotient rule", "BC-QA-02008"),
   ("BC-QA-06002", r"Riemann sum", "BC-QA-06001"),
   ("BC-QA-05001", r"solving for c", "BC-QA-05002"),
   ("BC-QA-05003", r"second derivative test", "BC-QA-05013"),
   ("BC-QA-05005", r"second derivative test", "BC-QA-05013"),
   ("BC-QA-05006", r"Extreme Value Theorem", "BC-QA-05010"),
   ("BC-QA-05007", r"solving the differential equation", "BC-QA-07003"),
   ("BC-QA-05010", r"differentiating to find the extremum", "BC-QA-05006"),
   ("BC-QA-07001", r"solving the differential equation", "BC-QA-07003"),
   ("BC-QA-07002", r"solving the equation", "BC-QA-07003"),
   ("BC-QA-07004", r"solving the differential equation", "BC-QA-07003"),
   ("BC-QA-07005", r"solving the equation", "BC-QA-07003"),
   ("BC-QA-07006", r"exponential formula", "BC-QA-07008"),
   ("BC-QA-07007", r"solving the equation from scratch", "BC-QA-07003"),
   ("BC-QA-07009", r"partial fractions", "BC-QA-06010"),
   ("BC-QA-07010", r"solving the differential equation", "BC-QA-07003"),
   ("BC-QA-08002", r"average rate of change", "BC-QA-99007"),
   ("BC-QA-09011", r"first or second derivative test", "BC-QA-05013"),
   ("BC-QA-99001", r"differentiating the polar equation", "BC-QA-09009"),
   ("BC-QA-99003", r"parametric slope formula", "BC-QA-09001"),
   ("BC-QA-99005", r"differentiating the radial function", "BC-QA-09009"),
   ("BC-QA-99007", r"dividing by the interval length", "BC-QA-08001"),
   ("BC-QA-99008", r"net change question", "BC-QA-06005"),
   ("BC-QA-99010", r"total converges", "BC-QA-06011"),
   ("BC-QA-10006", r"ratio test", "BC-QA-10013"),
   ("BC-QA-10008", r"Lagrange error bound", "BC-QA-10009"),
   ("BC-QA-10009", r"alternating series bound", "BC-QA-10008"),
   ("BC-QA-10020", r"geometric closed form", "BC-QA-10003"),
]


def load(name):
   return json.loads((DATA / name).read_text())


def resolver(records):
   by_id = {record["id"]: record for record in records}

   def resolve(record_id):
      seen = set()

      while record_id in by_id and by_id[record_id].get("superseded_by") and record_id not in seen:
         seen.add(record_id)
         record_id = by_id[record_id]["superseded_by"]

      return record_id

   return by_id, resolve


def hard_edges():
   pairs = set()

   with open(DATA / "prereq_edges.csv") as handle:
      for row in csv.DictReader(handle):
         is_hard = row["type"] == "hard_prerequisite"

         if is_hard:
            pairs.add(frozenset((row["from"], row["to"])))

   return pairs


def unit_of(skill_id):
   return skill_id[7:9]


def main():
   skills = {skill["id"]: skill for skill in load("skills.json")["skills"]}
   misconceptions, resolve_misconception = resolver(load("misconceptions.json")["misconceptions"])
   archetypes = {record["id"]: record for record in load("archetypes.json")["archetypes"]}
   blocked = hard_edges()

   skills_by_misconception = defaultdict(set)

   for skill_id, skill in skills.items():
      for misconception_id in skill.get("misconceptions", []):
         skills_by_misconception[resolve_misconception(misconception_id)].add(skill_id)

   sources = defaultdict(set)

   def add(first, second, source, cross_unit_named):
      is_self = first == second
      is_known = first in skills and second in skills

      if is_self or not is_known:
         return

      pair = frozenset((first, second))
      crosses_units = unit_of(first) != unit_of(second)
      is_prerequisite_pair = pair in blocked

      if is_prerequisite_pair:
         return

      if crosses_units and not cross_unit_named:
         return

      sources[pair].add(source)

   for skill_id in sorted(skills):
      confusions = skills[skill_id]["adaptive"].get("common_confusions", [])

      for entry in confusions:
         for other_id in SKILL_ID.findall(entry):
            add(skill_id, other_id, ("cc", skill_id), True)

         for raw_id in MISCONCEPTION_ID.findall(entry):
            misconception_id = resolve_misconception(raw_id)

            for other_id in sorted(skills_by_misconception[misconception_id]):
               add(skill_id, other_id, ("mis", misconception_id), False)

            rivals = misconceptions.get(misconception_id, {}).get("rival_misconceptions", [])

            for rival_raw in rivals:
               rival_id = resolve_misconception(rival_raw)

               for other_id in sorted(skills_by_misconception[rival_id]):
                  add(skill_id, other_id, ("rival", misconception_id, rival_id), False)

   for holder_id, pattern, named_id in METHOD_NAMES:
      holder = archetypes[holder_id]
      named = archetypes[named_id]
      matcher = re.compile(pattern, re.IGNORECASE)

      for approach in holder.get("wrong_approaches", []):
         if not matcher.search(approach):
            continue

         cited_errors = set(ERROR_ID.findall(approach))
         holder_skills = [skill_id for skill_id in holder["skills"] if skill_id not in named["skills"]]

         if cited_errors:
            holding = [skill_id for skill_id in holder_skills if cited_errors & set(skills.get(skill_id, {}).get("common_errors", []))]
            holder_skills = holding or holder_skills

         named_skills = [skill_id for skill_id in named["skills"] if skill_id not in holder["skills"]]
         method_skills = [skill_id for skill_id in named_skills if matcher.search(skills.get(skill_id, {}).get("name", ""))]
         named_skills = method_skills or named_skills

         for first in holder_skills:
            for second in named_skills:
               add(first, second, ("method", holder_id, named_id), True)

   def rank(pair):
      pair_sources = sources[pair]
      kinds = {source[0] for source in pair_sources}
      has_named_skill = "cc" in kinds or "method" in kinds
      return (-len(pair_sources), -len(kinds), not has_named_skill, sorted(pair))

   chosen = defaultdict(list)

   for pair in sorted(sources, key=rank):
      first, second = sorted(pair)
      first_has_room = len(chosen.get(first, [])) < LIST_CAP
      second_has_room = len(chosen.get(second, [])) < LIST_CAP
      has_room = first_has_room and second_has_room

      if has_room:
         chosen[first].append(second)
         chosen[second].append(first)

   provenance = {}
   records = []

   for skill_id in sorted(skills):
      partners = sorted(chosen.get(skill_id, []), key=lambda other: rank(frozenset((skill_id, other))))
      records.append({"id": skill_id, "confusable_with": partners})

      if not partners:
         continue

      provenance[skill_id] = {
         other: sorted("/".join(source) for source in sources[frozenset((skill_id, other))])
         for other in partners
      }

   pair_count = sum(len(partners) for partners in chosen.values()) // 2
   staged = {
      "registry": "skills",
      "merge": "fields",
      "note": (
         "confusable_with derived by tools/derive_confusable.py from adaptive.common_confusions (cc), shared "
         "misconceptions (mis), rival misconceptions (rival) and archetype wrong_approaches naming another "
         "archetype's method (method). Symmetric, same unit unless a cc or method source names the other skill, "
         "hard prerequisite pairs excluded, capped at 6 by independent source count. Every skill is listed so a rerun clears lists that no longer qualify. Evidence tag inferred."
      ),
      "evidence_tag": "inferred",
      "pair_count": pair_count,
      "candidate_pairs": len(sources),
      "provenance": provenance,
      "skills": records,
   }
   OUTPUT.write_text(json.dumps(staged, indent=1) + "\n")
   print(f"skills filled {len(provenance)} of {len(records)}, pairs {pair_count}, candidate pairs {len(sources)}")


if __name__ == "__main__":
   main()
