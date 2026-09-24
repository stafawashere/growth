"""The representation matrix on the progress screen (docs/plan/08 "Progress", 11 P7 scope item 7):
source representation by target representation, over the student's practice attempts.

A cell counts an attempt when the attempt's archetype carries both representations and the BC-REP
taxonomy lists the pair as a conversion (app/engine/interleave.py conversion_pairs_from), which is
the same reading of a translation the interleaving floor uses. An archetype carrying several
conversion pairs counts once in each, so the cells do not sum to the attempt count; the matrix
reports its own attempt count beside them.
"""


def representation_matrix(attempts, archetypes, pairs, representation_names):
   cells = {}
   counted_attempts = 0

   for record in attempts:
      is_practice = record.updates_mastery and record.correct is not None
      archetype = archetypes.get(record.archetype_id)

      if not is_practice or archetype is None:
         continue

      carried = list(archetype.get("representations") or ())
      matched = sorted(
         (source, target)
         for source in carried
         for target in carried
         if source != target and (source, target) in pairs
      )

      if not matched:
         continue

      counted_attempts += 1

      for pair in matched:
         cell = cells.setdefault(pair, {"attempts": 0, "correct": 0})
         cell["attempts"] += 1
         cell["correct"] += 1 if record.correct else 0

   used = sorted({representation for pair in pairs for representation in pair})

   return {
      "representations": [
         {"id": representation_id, "name": representation_names.get(representation_id, representation_id)}
         for representation_id in used
      ],
      "cells": [
         {
            "source": source,
            "target": target,
            "attempts": cells.get((source, target), {}).get("attempts", 0),
            "correct": cells.get((source, target), {}).get("correct", 0),
         }
         for source, target in sorted(pairs)
      ],
      "translation_attempts": counted_attempts,
      "practice_attempts": sum(1 for record in attempts if record.updates_mastery and record.correct is not None),
   }
