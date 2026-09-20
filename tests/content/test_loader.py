"""Tests for app/content/loader.py against the real data/ directory.

docs/plan/06-architecture.md "Content loader for research/", 11-phased-delivery.md P1 scope
item 1 and entry criterion 1, 02-adaptive-engine.md "Scope and inputs" and R13.
"""
import csv
import json
import shutil
from pathlib import Path

import pytest

from app.content.loader import LoaderError, load_snapshot

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = REPO_ROOT / "data"
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "graph_p1.json"


def _copy_data(tmp_path):
   copy_root = tmp_path / "data"
   shutil.copytree(DATA_ROOT, copy_root)

   return copy_root


def test_graph_acyclic():
   snapshot = load_snapshot(DATA_ROOT)

   top_edges = [
      edge for edge in snapshot.edges if "BC-TOP" in edge["from"] or "BC-TOP" in edge["to"]
   ]
   top_edges_from = [edge for edge in top_edges if "BC-TOP" in edge["from"]]
   top_edges_to = [edge for edge in top_edges if "BC-TOP" in edge["to"]]

   assert len(snapshot.edges) == 1226
   assert snapshot.counts["consumed_edges"] == 1226
   assert len(top_edges) == 48
   assert len(top_edges_from) == 31
   assert len(top_edges_to) == 17


def test_loader_against_real_data():
   snapshot = load_snapshot(DATA_ROOT)

   assert snapshot.counts["BC-SKL"] == 541
   assert snapshot.counts["BC-CON"] == 170
   assert snapshot.counts["BC-PRQ"] == 77
   assert snapshot.counts["edges"] == 1226
   assert snapshot.counts["hard_prerequisite"] == 602
   assert snapshot.counts["supporting"] == 622
   assert snapshot.counts["co_requisite"] == 2
   assert snapshot.counts["BC-QA_active"] == 139
   assert snapshot.counts["BC-QA_families"] == 77
   assert snapshot.counts["BC-QV"] == 395
   assert snapshot.counts["BC-PT"] == 76
   assert snapshot.counts["BC-ERR_active"] == 390
   assert snapshot.counts["BC-MIS_active"] == 213
   assert snapshot.counts["BC-SIG"] == 711
   assert snapshot.counts["BC-REP"] == 14
   assert snapshot.counts["BC-DF"] == 17
   assert snapshot.counts["BC-CV"] == 29
   assert snapshot.counts["frq_parts"] == 249
   assert snapshot.counts["BC-MCQ"] == 91
   assert snapshot.counts["BC-TOP_edges"] == 48
   assert snapshot.counts["empty_point_types"] == 56
   assert snapshot.counts["empty_official_examples"] == 36
   assert snapshot.counts["skill_in_no_archetype"] >= 1
   assert "BC-SKL-02001" not in {
      skill_id for record in snapshot.archetypes.values() for skill_id in record["skills"]
   }


def test_loader_refuses_on_injected_cycle(tmp_path):
   copy_root = _copy_data(tmp_path)
   edges_path = copy_root / "prereq_edges.csv"

   with edges_path.open() as handle:
      rows = list(csv.DictReader(handle))

   fieldnames = ["from", "to", "type", "evidence_tag", "note"]
   rows.append(
      {
         "from": "BC-SKL-01024",
         "to": "BC-PRQ-01001",
         "type": "hard_prerequisite",
         "evidence_tag": "inferred",
         "note": "injected cycle for test_loader_refuses_on_injected_cycle",
      }
   )

   with edges_path.open("w", newline="") as handle:
      writer = csv.DictWriter(handle, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(rows)

   with pytest.raises(LoaderError):
      load_snapshot(copy_root)


def test_loader_refuses_on_injected_dangling_id(tmp_path):
   copy_root = _copy_data(tmp_path)
   edges_path = copy_root / "prereq_edges.csv"

   with edges_path.open() as handle:
      rows = list(csv.DictReader(handle))

   fieldnames = ["from", "to", "type", "evidence_tag", "note"]
   rows.append(
      {
         "from": "BC-SKL-99999",
         "to": "BC-SKL-01024",
         "type": "supporting",
         "evidence_tag": "inferred",
         "note": "injected dangling id for test_loader_refuses_on_injected_dangling_id",
      }
   )

   with edges_path.open("w", newline="") as handle:
      writer = csv.DictWriter(handle, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(rows)

   with pytest.raises(LoaderError):
      load_snapshot(copy_root)


def test_inert_top_ids_include_p1_subgraph(tmp_path):
   copy_root = _copy_data(tmp_path)
   snapshot = load_snapshot(copy_root)
   fixture = json.loads(FIXTURE_PATH.read_text())

   assert set(fixture["inert_top"]).issubset(snapshot.inert_top_ids)
   assert len(snapshot.inert_top_ids) == 25


def test_loader_refuses_on_wrong_type_reference(tmp_path):
   copy_root = _copy_data(tmp_path)
   archetypes_path = copy_root / "archetypes.json"
   archetypes_doc = json.loads(archetypes_path.read_text())

   archetypes_doc["archetypes"][0]["skills"][0] = "BC-ERR-99001"
   archetypes_path.write_text(json.dumps(archetypes_doc))

   with pytest.raises(LoaderError):
      load_snapshot(copy_root)
