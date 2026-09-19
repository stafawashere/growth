"""Group misconception and error records that look like restatements of each other.

Two records are candidates when their normalised names or their description token sets overlap
above a threshold. The tool prints candidate groups for a human to review; it changes nothing.

Usage: python3 tools/find_duplicates.py [--threshold 0.34]
"""
import json
import re
import sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

STOP_WORDS = {
   "the", "a", "an", "of", "to", "in", "is", "as", "for", "and", "or", "that", "it", "its",
   "student", "students", "response", "responses", "holds", "believes", "belief", "with",
   "on", "by", "from", "at", "not", "be", "been", "so", "this", "which", "when", "where",
   "one", "than", "then", "but", "any", "are", "was", "were", "can", "may", "has", "have",
   "each", "into", "over", "same", "such", "their", "they", "them", "there", "without",
}

SYNONYMS = {
   "antiderivative": "antidifferentiation",
   "antiderivatives": "antidifferentiation",
   "antidifferentiate": "antidifferentiation",
   "derivatives": "derivative",
   "integrals": "integral",
   "integration": "integral",
   "integrate": "integral",
   "integrated": "integral",
   "series": "series",
   "convergent": "convergence",
   "converges": "convergence",
   "converge": "convergence",
   "diverges": "divergence",
   "divergent": "divergence",
   "speeds": "speed",
   "velocities": "velocity",
   "areas": "area",
   "volumes": "volume",
   "limits": "limit",
   "functions": "function",
   "theorems": "theorem",
   "hypothesis": "hypotheses",
   "terms": "term",
   "signs": "sign",
   "rates": "rate",
   "units": "unit",
}


def normalise(text):
   lowered = re.sub(r"[^a-z0-9 ]+", " ", (text or "").lower())
   tokens = [SYNONYMS.get(token, token) for token in lowered.split()]
   return [token for token in tokens if token not in STOP_WORDS and len(token) > 2]


def jaccard(left, right):
   if not left or not right:
      return 0.0

   return len(left & right) / len(left | right)


def name_key(name):
   return " ".join(sorted(set(normalise(name))))


def score_pair(first, second, text_field):
   name_tokens_first = set(normalise(first.get("name", "")))
   name_tokens_second = set(normalise(second.get("name", "")))
   body_tokens_first = set(normalise(first.get(text_field, "")))
   body_tokens_second = set(normalise(second.get(text_field, "")))

   name_overlap = jaccard(name_tokens_first, name_tokens_second)
   body_overlap = jaccard(body_tokens_first, body_tokens_second)

   return max(name_overlap, 0.6 * name_overlap + 0.4 * body_overlap), name_overlap, body_overlap


def evidence_weight(record):
   fields = ["observable_errors", "exposing_archetypes", "skills", "rival_misconceptions",
             "sources", "possible_misconceptions", "non_conceptual_causes", "concepts",
             "archetypes", "instances"]
   total = sum(len(record.get(field, []) or []) for field in fields)
   has_official = 2 if record.get("official_evidence_notes") else 0
   tag_rank = {"verified": 4, "single-source": 2, "inferred": 1, "uncertain": 0}

   return total + has_official + tag_rank.get(record.get("evidence_tag"), 0)


def block_of(identifier):
   return identifier.split("-")[2][:2]


def group(records, text_field, threshold):
   parent = {record["id"]: record["id"] for record in records}

   def find(identifier):
      while parent[identifier] != identifier:
         parent[identifier] = parent[parent[identifier]]
         identifier = parent[identifier]

      return identifier

   def union(left, right):
      root_left, root_right = find(left), find(right)

      if root_left != root_right:
         parent[root_right] = root_left

   pairs = []

   for first, second in combinations(records, 2):
      is_same_block = block_of(first["id"]) == block_of(second["id"])
      combined, name_overlap, body_overlap = score_pair(first, second, text_field)
      is_candidate = combined >= threshold and not is_same_block

      if is_candidate:
         pairs.append((first["id"], second["id"], round(combined, 2), round(name_overlap, 2), round(body_overlap, 2)))
         union(first["id"], second["id"])

   clusters = {}

   for record in records:
      clusters.setdefault(find(record["id"]), []).append(record)

   return {root: members for root, members in clusters.items() if len(members) > 1}, pairs


def report(label, records, text_field, threshold):
   clusters, pairs = group(records, text_field, threshold)
   print(f"== {label}: {len(clusters)} candidate groups from {len(pairs)} pairs above {threshold}")

   for root in sorted(clusters):
      members = sorted(clusters[root], key=evidence_weight, reverse=True)
      canonical = members[0]
      print(f"\n  group rooted at {canonical['id']} (richest evidence, weight {evidence_weight(canonical)})")

      for member in members:
         marker = "CANON" if member is canonical else "     "
         print(f"    {marker} {member['id']} w={evidence_weight(member)} {member.get('name','')}")

   print()


def main():
   threshold = 0.34

   for index, argument in enumerate(sys.argv):
      if argument == "--threshold":
         threshold = float(sys.argv[index + 1])

   misconceptions = json.loads((DATA / "misconceptions.json").read_text())["misconceptions"]
   errors = json.loads((DATA / "errors.json").read_text())["errors"]

   report("misconceptions", misconceptions, "description", threshold)
   report("errors", errors, "observed_behavior", threshold)


if __name__ == "__main__":
   main()
