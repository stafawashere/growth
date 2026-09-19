"""Propagate FRQ and MCQ records into the records they cite.

For every FRQ record: its id is added to archetype.official_examples, variant.official_examples,
skill.official_evidence, error.official_evidence (via commentary_errors), point_type usage, and
difficulty_factor.official_examples. Archetype.point_types becomes the union of point types seen
on records tagged with that archetype. Changes are staged and merged so the registries stay canonical.
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STAGING = DATA / "staging"


def load(name):
   return json.loads((DATA / name).read_text())


def add_unique(record, field, values):
   current = record.setdefault(field, [])

   for value in values:
      is_new = value not in current

      if is_new:
         current.append(value)


def main():
   frq = load("frq_records.json")["records"]
   mcq = load("mcq_records.json")["records"]
   skills = load("skills.json")
   archetypes = load("archetypes.json")
   errors = load("errors.json")
   taxonomies = load("taxonomies.json")
   scoring = load("scoring_points.json")

   by_id = {}

   for collection in [skills["skills"], archetypes["archetypes"], archetypes["variants"], errors["errors"], taxonomies["difficulty_factors"], scoring["point_types"]]:
      for record in collection:
         by_id[record["id"]] = record

   touched = defaultdict(dict)
   archetype_points = defaultdict(list)

   def touch(identifier, field, values):
      record = by_id.get(identifier)
      is_known = record is not None

      if not is_known:
         return

      add_unique(record, field, values)
      touched[identifier] = record

   for record in frq + mcq:
      rid = record["id"]
      archetype = record.get("archetype")

      if archetype:
         touch(archetype, "official_examples", [rid])
         archetype_points[archetype].extend(record.get("point_types", []))

      for variant in record.get("variants", []):
         touch(variant, "official_examples", [rid])

      for skill in record.get("skills", []):
         touch(skill, "official_evidence", [rid])

      for error in record.get("commentary_errors", []):
         touch(error, "official_evidence", [rid])

      for factor in record.get("difficulty_factors", []):
         touch(factor, "official_examples", [rid])

      for point in record.get("point_types", []):
         touch(point, "rubric_instances", [rid])

   for archetype, points in archetype_points.items():
      unique = list(dict.fromkeys(points))
      touch(archetype, "point_types", unique)

   grouped = defaultdict(lambda: defaultdict(list))
   registry_of = {"BC-SKL": ("skills", "skills"), "BC-QA": ("archetypes", "archetypes"), "BC-QV": ("archetypes", "variants"), "BC-ERR": ("errors", "errors"), "BC-DF": ("taxonomies", "difficulty_factors"), "BC-PT": ("scoring_points", "point_types")}

   for identifier, record in touched.items():
      prefix = "-".join(identifier.split("-")[:2])
      registry, collection = registry_of[prefix]
      grouped[registry][collection].append(record)

   for registry, collections in grouped.items():
      payload = {"registry": registry, **collections}
      (STAGING / f"link-evidence-{registry}.json").write_text(json.dumps(payload, indent=1))
      print(registry, {key: len(value) for key, value in collections.items()})


if __name__ == "__main__":
   main()
