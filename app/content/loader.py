"""Content loader for research/, per docs/plan/06-architecture.md "Content loader for research/"
and docs/plan/11-phased-delivery.md P1 scope item 1.

Reads the 12 registries plus data/ids.json, validates every JSON registry against its schema
exactly as qa/01_schema.py does, checks referential integrity, builds the typed edge set over
BC-SKL, BC-PRQ and BC-TOP ids, refuses on a cycle anywhere in that set, and refuses on any
dangling id. BC-TOP ids are validated against curriculum.json and held inert per R13.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from app.content.snapshot import ContentSnapshot

_SCHEMAS_DIR = Path(__file__).resolve().parent.parent.parent / "schemas"

if str(_SCHEMAS_DIR) not in sys.path:
   sys.path.insert(0, str(_SCHEMAS_DIR))

from common import REGISTRY_FILES  # noqa: E402

KNOWN_EDGE_TYPES = frozenset({"hard_prerequisite", "supporting", "co_requisite"})


class LoaderError(Exception):
   pass


def _load_json(root, name):
   path = root / f"{name}.json"
   is_missing = not path.exists()

   if is_missing:
      raise LoaderError(f"data/{name}.json missing")

   return json.loads(path.read_text())


def _load_edges(root):
   path = root / "prereq_edges.csv"
   is_missing = not path.exists()

   if is_missing:
      raise LoaderError("data/prereq_edges.csv missing")

   with path.open() as handle:
      rows = list(csv.DictReader(handle))

   edges = []

   for index, row in enumerate(rows):
      edge_type = row["type"]
      is_known_type = edge_type in KNOWN_EDGE_TYPES

      if not is_known_type:
         raise LoaderError(f"prereq_edges.csv row {index}: unknown edge type {edge_type!r}")

      edges.append(
         {
            "from": row["from"],
            "to": row["to"],
            "type": edge_type,
            "evidence_tag": row.get("evidence_tag", ""),
            "note": row.get("note", ""),
         }
      )

   return edges


def _validate_schemas(root):
   failures = []

   for schema_path in sorted(_SCHEMAS_DIR.glob("*.schema.json")):
      name = schema_path.name.replace(".schema.json", "")
      path = root / f"{name}.json"
      is_present = path.exists()

      if not is_present:
         failures.append(f"data/{name}.json missing")
         continue

      data = json.loads(path.read_text())
      validator = Draft202012Validator(json.loads(schema_path.read_text()))

      for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))[:50]:
         location = "/".join(str(part) for part in error.path)
         failures.append(f"{name}.json at {location}: {error.message[:160]}")

   has_failures = len(failures) > 0

   if has_failures:
      raise LoaderError("; ".join(failures))


def _is_active(record):
   carries_status = "status" in record

   if not carries_status:
      return True

   return record["status"] == "active"


def _index_by_id(records):
   return {record["id"]: record for record in records}


def _registry_file_names():
   file_names = sorted({location.split(":")[0] for location in REGISTRY_FILES.values()})
   file_names.append("sources.json")

   return sorted(set(file_names))


def _digest_for(root):
   hasher = hashlib.sha256()
   paths = [root / name for name in _registry_file_names()]
   paths.append(root / "prereq_edges.csv")

   for path in sorted(paths):
      hasher.update(path.name.encode("utf-8"))
      hasher.update(path.read_bytes())

   return hasher.hexdigest()


def _tombstoned_ids(ids_registry):
   tombstoned = set()

   for id_value, record in ids_registry.items():
      is_tombstone = record.get("status") == "retired"

      if is_tombstone:
         tombstoned.add(id_value)

   return tombstoned


def _prefix_of(id_value):
   parts = id_value.split("-")

   return "-".join(parts[:2])


def _check_reference(known_ids, allowed_prefixes, value, record_id, field_name):
   is_missing = value not in known_ids

   if is_missing:
      raise LoaderError(f"{record_id} field {field_name}: dangling id {value!r}")

   has_wrong_type = _prefix_of(value) not in allowed_prefixes

   if has_wrong_type:
      raise LoaderError(
         f"{record_id} field {field_name}: id {value!r} is not one of {sorted(allowed_prefixes)}"
      )


def _topological_sort(node_ids, edges):
   adjacency = {node: [] for node in node_ids}
   in_degree = {node: 0 for node in node_ids}

   for edge in edges:
      adjacency[edge["from"]].append(edge["to"])
      in_degree[edge["to"]] += 1

   queue = sorted(node for node, degree in in_degree.items() if degree == 0)
   ordered = []
   consumed_edges = 0

   while queue:
      current = queue.pop(0)
      ordered.append(current)

      next_ready = []

      for neighbour in adjacency[current]:
         in_degree[neighbour] -= 1
         consumed_edges += 1
         is_ready = in_degree[neighbour] == 0

         if is_ready:
            next_ready.append(neighbour)

      queue.extend(sorted(next_ready))

   has_cycle = len(ordered) != len(node_ids)

   if has_cycle:
      unresolved = sorted(node for node in node_ids if node not in ordered)
      raise LoaderError(f"prereq_edges.csv: cycle detected, unresolved nodes {unresolved[:10]}")

   return ordered, consumed_edges


SKILL_LIKE_PREFIXES = frozenset({"BC-SKL", "BC-PRQ"})
EDGE_NODE_PREFIXES = frozenset({"BC-SKL", "BC-PRQ", "BC-TOP"})


def load_snapshot(root):
   root = Path(root)

   _validate_schemas(root)

   curriculum = _load_json(root, "curriculum")
   skills_doc = _load_json(root, "skills")
   archetypes_doc = _load_json(root, "archetypes")
   errors_doc = _load_json(root, "errors")
   misconceptions_doc = _load_json(root, "misconceptions")
   signals_doc = _load_json(root, "diagnostic_signals")
   taxonomies_doc = _load_json(root, "taxonomies")
   scoring_points_doc = _load_json(root, "scoring_points")
   frq_doc = _load_json(root, "frq_records")
   mcq_doc = _load_json(root, "mcq_records")
   sources_doc = _load_json(root, "sources")
   ids_doc = _load_json(root, "ids")

   tombstoned = _tombstoned_ids(ids_doc["ids"])

   units = _index_by_id(curriculum["units"])
   topics = _index_by_id(curriculum["topics"])
   learning_objectives = _index_by_id(curriculum["learning_objectives"])
   essential_knowledge = _index_by_id(curriculum["essential_knowledge"])

   concepts = _index_by_id(skills_doc["concepts"])
   prerequisites = _index_by_id(skills_doc["prerequisites"])
   skills = _index_by_id(skills_doc["skills"])

   all_archetypes = _index_by_id(archetypes_doc["archetypes"])
   variants = _index_by_id(archetypes_doc["variants"])
   archetypes = {
      archetype_id: record
      for archetype_id, record in all_archetypes.items()
      if _is_active(record)
   }

   all_errors = _index_by_id(errors_doc["errors"])
   errors = {error_id: record for error_id, record in all_errors.items() if _is_active(record)}

   all_misconceptions = _index_by_id(misconceptions_doc["misconceptions"])
   misconceptions = {
      mis_id: record for mis_id, record in all_misconceptions.items() if _is_active(record)
   }

   all_signals = _index_by_id(signals_doc["signals"])
   signals = {
      signal_id: record for signal_id, record in all_signals.items() if _is_active(record)
   }

   scoring_points = _index_by_id(scoring_points_doc["point_types"])
   representations = _index_by_id(taxonomies_doc["representations"])
   difficulty_factors = _index_by_id(taxonomies_doc["difficulty_factors"])
   command_verbs = _index_by_id(taxonomies_doc["command_verbs"])
   frq_parts = _index_by_id(frq_doc["records"])
   mcq_records = _index_by_id(mcq_doc["records"])
   sources = _index_by_id(sources_doc["sources"])

   known_ids = set(tombstoned)

   for id_map in (
      units,
      topics,
      learning_objectives,
      essential_knowledge,
      concepts,
      prerequisites,
      skills,
      all_archetypes,
      variants,
      all_errors,
      all_misconceptions,
      all_signals,
      scoring_points,
      representations,
      difficulty_factors,
      command_verbs,
      frq_parts,
      mcq_records,
      sources,
   ):
      known_ids.update(id_map.keys())

   for archetype_id, record in all_archetypes.items():
      for skill_id in record.get("skills", []):
         _check_reference(known_ids, SKILL_LIKE_PREFIXES, skill_id, archetype_id, "skills")

   for signal_id, record in all_signals.items():
      skill_field = record.get("skill")

      if skill_field is not None:
         _check_reference(known_ids, SKILL_LIKE_PREFIXES, skill_field, signal_id, "skill")

      archetype_field = record.get("archetype")

      if archetype_field is not None:
         _check_reference(known_ids, {"BC-QA"}, archetype_field, signal_id, "archetype")

   for error_id, record in all_errors.items():
      for mis_id in record.get("possible_misconceptions") or []:
         _check_reference(known_ids, {"BC-MIS"}, mis_id, error_id, "possible_misconceptions")

   edges = _load_edges(root)

   for index, edge in enumerate(edges):
      row_label = f"prereq_edges.csv row {index}"
      _check_reference(known_ids, EDGE_NODE_PREFIXES, edge["from"], row_label, "from")
      _check_reference(known_ids, EDGE_NODE_PREFIXES, edge["to"], row_label, "to")

   node_ids = known_ids

   ordered, consumed_edges = _topological_sort(node_ids, edges)

   top_touching_edges = [
      edge for edge in edges if "BC-TOP" in edge["from"] or "BC-TOP" in edge["to"]
   ]
   inert_top_ids = frozenset(
      edge["from"] if "BC-TOP" in edge["from"] else edge["to"] for edge in top_touching_edges
   )

   hard_parents = {}
   supporting_parents = {}
   hard_children = {}

   for edge in edges:
      touches_top = edge["from"] in inert_top_ids or edge["to"] in inert_top_ids

      if touches_top:
         continue

      if edge["type"] == "hard_prerequisite":
         hard_parents.setdefault(edge["to"], set()).add(edge["from"])
         hard_children.setdefault(edge["from"], set()).add(edge["to"])
      elif edge["type"] == "supporting":
         supporting_parents.setdefault(edge["to"], set()).add(edge["from"])

   edge_type_counts = {}

   for edge in edges:
      edge_type_counts[edge["type"]] = edge_type_counts.get(edge["type"], 0) + 1

   family_ids = {record["family"] for record in archetypes.values()}

   skills_with_archetype = set()

   for record in archetypes.values():
      skills_with_archetype.update(record.get("skills", []))

   counts = {
      "BC-SKL": len(skills),
      "BC-CON": len(concepts),
      "BC-PRQ": len(prerequisites),
      "edges": len(edges),
      "consumed_edges": consumed_edges,
      "hard_prerequisite": edge_type_counts.get("hard_prerequisite", 0),
      "supporting": edge_type_counts.get("supporting", 0),
      "co_requisite": edge_type_counts.get("co_requisite", 0),
      "BC-QA_active": len(archetypes),
      "BC-QA_families": len(family_ids),
      "BC-QV": len(variants),
      "BC-PT": len(scoring_points),
      "BC-ERR_active": len(errors),
      "BC-MIS_active": len(misconceptions),
      "BC-SIG": len(signals),
      "BC-REP": len(representations),
      "BC-DF": len(difficulty_factors),
      "BC-CV": len(command_verbs),
      "frq_parts": len(frq_parts),
      "BC-MCQ": len(mcq_records),
      "BC-TOP_edges": len(top_touching_edges),
      "empty_point_types": sum(
         1 for record in archetypes.values() if not record.get("point_types")
      ),
      "empty_official_examples": sum(
         1 for record in archetypes.values() if not record.get("official_examples")
      ),
      "skill_in_no_archetype": sum(
         1 for skill_id in skills if skill_id not in skills_with_archetype
      ),
   }

   digest = _digest_for(root)

   return ContentSnapshot(
      skills=skills,
      prerequisites=prerequisites,
      concepts=concepts,
      archetypes=archetypes,
      all_archetypes=all_archetypes,
      variants=variants,
      errors=errors,
      misconceptions=misconceptions,
      signals=signals,
      scoring_points=scoring_points,
      representations=representations,
      difficulty_factors=difficulty_factors,
      command_verbs=command_verbs,
      frq_parts=frq_parts,
      mcq_records=mcq_records,
      edges=tuple(edges),
      hard_parents=hard_parents,
      supporting_parents=supporting_parents,
      hard_children=hard_children,
      inert_top_ids=inert_top_ids,
      counts=counts,
      digest=digest,
   )
