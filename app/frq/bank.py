"""The free-response bank and everything grading reads from the library, built once per process.

Records come from content/frq_items (GROWTH_FRQ_DIR overrides it). Each is checked by
app/frq/items.py record_violations against the loaded snapshot, and a record that fails is left
out and named in rejected, so a bad record never reaches a student and never stops the app.

Each served record also gets a row in the items table, status frq_verified rather than
verified, because an attempt row names an item row and because app/runtime/bank.py serves only
status verified: a free-response item can therefore never reach a micro-session (R10).
"""
import json
from dataclasses import dataclass, field
from pathlib import Path

from sqlalchemy import select

from app.db import models
from app.diagnosis.diagnose import Library
from app.frq.items import FRQ_PUBLISHED_STATUS, load_frq_records, record_violations

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FRQ_DIR = REPO_ROOT / "content" / "frq_items"
LABELS_PATH = REPO_ROOT / "data" / "bc_pt_determinism_labels.json"


@dataclass
class FrqContext:
   records: dict
   rejected: dict
   point_types: dict
   labels: dict
   library: Library
   archetypes: dict
   unit_titles: dict = field(default_factory=dict)

   def record(self, item_id):
      return self.records.get(item_id)

   def unit_of(self, record):
      return self.archetypes[record["archetype_id"]]["primary_unit"]

   def records_for_unit(self, unit_id):
      return [record for record in self.records.values() if self.unit_of(record) == unit_id]

   def units(self):
      return sorted({self.unit_of(record) for record in self.records.values()})


def read_labels(path=LABELS_PATH):
   document = json.loads(Path(path).read_text())

   return {entry["id"]: entry["label"] for entry in document["labels"]}


def library_from_snapshot(snapshot):
   return Library(
      skills=dict(snapshot.skills),
      prerequisites=dict(snapshot.prerequisites),
      errors=dict(snapshot.errors),
      misconceptions=dict(snapshot.misconceptions),
      signals=dict(snapshot.signals),
      archetypes=dict(snapshot.archetypes),
      hard_parents={child: tuple(parents) for child, parents in snapshot.hard_parents.items()},
   )


def build_frq_context(snapshot, frq_dir=DEFAULT_FRQ_DIR, unit_titles=None):
   records = {}
   rejected = {}
   directory = Path(frq_dir)
   has_directory = directory.is_dir()
   loaded = load_frq_records(directory) if has_directory else []

   for record in loaded:
      problems = record_violations(record, snapshot.archetypes, snapshot.scoring_points)

      if problems:
         rejected[record.get("id", "<no id>")] = problems
         continue

      records[record["id"]] = record

   return FrqContext(
      records=records,
      rejected=rejected,
      point_types=dict(snapshot.scoring_points),
      labels=read_labels(),
      library=library_from_snapshot(snapshot),
      archetypes=dict(snapshot.archetypes),
      unit_titles=dict(unit_titles or {}),
   )


def item_row(record, snapshot_id, now):
   stamp = now.isoformat()

   return models.Item(
      id=record["id"],
      archetype_id=record["archetype_id"],
      variant_id=None,
      snapshot_id=snapshot_id,
      parameter_draw="{}",
      stem=record["stem"]["text"],
      figure_spec=None,
      options=None,
      answer_key=json.dumps({"form": "free_response", "parts": [part["answer_latex"] for part in record["parts"]]}),
      worked_solution=json.dumps([step for part in record["parts"] for step in part["worked_solution"]]),
      calculator_status=record["calculator_status"],
      representation=record["representation"],
      difficulty_settings="[]",
      skills=json.dumps(record["skills"]),
      provenance=json.dumps({"drafted_by": record["drafted_by"], "signed_off_by": record.get("signed_off_by")}),
      status=FRQ_PUBLISHED_STATUS,
      dedupe_minhash="[]",
      created_at=stamp,
      updated_at=stamp,
   )


def ensure_item_rows(db, context, snapshot_id, now):
   known = set(db.scalars(select(models.Item.id).where(models.Item.id.in_(list(context.records)))).all())

   for item_id, record in context.records.items():
      if item_id not in known:
         db.add(item_row(record, snapshot_id, now))

   db.flush()
