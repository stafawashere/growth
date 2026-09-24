"""The stable concept probe of docs/plan/11 P7 scope item 6 and 01 "External checkpoint": a fixed
item set never used for practice, administered every 8 weeks and reported apart from practice
accuracy.

The set is a file, content/probe/concept_probe_v1.json, drawn once by draw_probe_set and then
frozen: an item on it is refused by the practice bank (app/runtime/bank.py) for as long as the file
names it, so no practice exposure can inflate the probe. The draw takes PER_UNIT items from each
unit, each from a different archetype, and only from archetypes left with at least
MINIMUM_PRACTICE_ITEMS items for practice once the probe item is withheld.
"""
import json
import random
from functools import lru_cache
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PROBE_SET_PATH = REPOSITORY_ROOT / "content" / "probe" / "concept_probe_v1.json"
PROBE_SET_NAME = "concept_probe_v1"

PER_UNIT = 2
MINIMUM_PRACTICE_ITEMS = 4
DRAW_SEED = 20261001


@lru_cache(maxsize=4)
def probe_item_ids(path=PROBE_SET_PATH):
   is_present = Path(path).exists()

   if not is_present:
      return frozenset()

   return frozenset(json.loads(Path(path).read_text())["item_ids"])


def draw_probe_set(item_records, archetypes, seed=DRAW_SEED):
   """item_records are bank records (id, archetype_id); archetypes maps id to its record."""
   by_archetype = {}

   for record in item_records:
      by_archetype.setdefault(record["archetype_id"], []).append(record["id"])

   eligible_by_unit = {}

   for archetype_id, item_ids in sorted(by_archetype.items()):
      leaves_enough = len(item_ids) - 1 >= MINIMUM_PRACTICE_ITEMS
      archetype = archetypes.get(archetype_id)

      if not leaves_enough or archetype is None:
         continue

      eligible_by_unit.setdefault(archetype["primary_unit"], []).append(archetype_id)

   rng = random.Random(seed)
   chosen = []

   for unit in sorted(eligible_by_unit):
      archetype_ids = sorted(eligible_by_unit[unit])
      picked = rng.sample(archetype_ids, min(PER_UNIT, len(archetype_ids)))

      for archetype_id in sorted(picked):
         chosen.append(rng.choice(sorted(by_archetype[archetype_id])))

   return sorted(chosen)
