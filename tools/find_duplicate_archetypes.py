"""Report archetype pairs whose name and invariant_structure share enough vocabulary to be the same question.

Usage: python3 tools/find_duplicate_archetypes.py [threshold]
Scoring is Jaccard overlap on content tokens, weighted toward the name, and pairs are
printed worst first so a reviewer can read the close ones and decide by hand.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHETYPES = ROOT / "data" / "archetypes.json"

STOPWORDS = {
   "a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "from", "by", "with", "for",
   "is", "are", "as", "its", "it", "that", "which", "whose", "over", "into", "given", "when",
   "not", "be", "been", "may", "must", "than", "then", "this", "these", "those", "one", "two",
   "each", "any", "all", "same", "other", "some", "no", "where", "while", "also", "can",
}


def tokenise(text):
   words = re.findall(r"[a-z]+", text.lower())
   return {word for word in words if word not in STOPWORDS and len(word) > 2}


def jaccard(left, right):
   union = left | right

   if not union:
      return 0.0

   return len(left & right) / len(union)


def score_pair(first, second):
   name_overlap = jaccard(tokenise(first["name"]), tokenise(second["name"]))
   structure_overlap = jaccard(tokenise(first.get("invariant_structure", "")), tokenise(second.get("invariant_structure", "")))
   return 0.6 * name_overlap + 0.4 * structure_overlap, name_overlap, structure_overlap


def main():
   threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
   records = json.loads(ARCHETYPES.read_text())["archetypes"]
   active = [record for record in records if record.get("status", "active") != "retired"]

   candidates = []

   for index, first in enumerate(active):
      for second in active[index + 1:]:
         combined, name_overlap, structure_overlap = score_pair(first, second)
         is_candidate = combined >= threshold

         if is_candidate:
            candidates.append((combined, name_overlap, structure_overlap, first, second))

   candidates.sort(key=lambda row: -row[0])

   for combined, name_overlap, structure_overlap, first, second in candidates:
      cross_unit = first.get("primary_unit") != second.get("primary_unit")
      marker = "cross-unit" if cross_unit else "same-unit"
      print(f"{combined:.3f} name={name_overlap:.3f} struct={structure_overlap:.3f} {marker}")
      print(f"   {first['id']} {first.get('primary_unit')} {first['name']}")
      print(f"   {second['id']} {second.get('primary_unit')} {second['name']}")

   print(f"{len(candidates)} candidate pairs at threshold {threshold} over {len(active)} active archetypes")


if __name__ == "__main__":
   main()
