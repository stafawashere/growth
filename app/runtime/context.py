"""Builds the SessionContext app/session/service.py is called with, from the live library.

docs/plan/11-phased-delivery.md P1 scope items 1 and 14: loads the registries through
app/content/loader.py, persists the content_snapshots row through app/content/persist.py, builds
the fringe graph app/engine/select.py and app/session/build.py read and the engine graph
app/engine/update.py reads, and wires the item bank of app/runtime/bank.py. No second loader is
built here.
"""
import json
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.api.app import SessionContext
from app.content.loader import load_snapshot
from app.content.persist import record_snapshot
from app.runtime.bank import ItemBank, ItemSource
from app.runtime.graphs import graphs_from_snapshot

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"


def unit_titles(root):
   curriculum = json.loads((Path(root) / "curriculum.json").read_text())

   return {record["id"]: record["name"] for record in curriculum["units"]}


def build_bank(engine, snapshot, snapshot_id, items_directories):
   has_items_directories = len(items_directories) > 0

   if not has_items_directories:
      return ItemBank(engine)

   source = ItemSource(
      directories=tuple(Path(directory) for directory in items_directories),
      active_error_ids=frozenset(snapshot.errors),
      snapshot_id=snapshot_id,
   )

   return ItemBank(engine, source=source)


def build_session_context(
   engine, content_root=None, library_commit=None, loaded_at=None, items_directories=()
):
   root = content_root or DEFAULT_CONTENT_ROOT
   snapshot = load_snapshot(root)

   with OrmSession(engine) as db:
      row = record_snapshot(db, snapshot, library_commit=library_commit, loaded_at=loaded_at)
      db.commit()
      snapshot_id = row.id

   graph, engine_graph = graphs_from_snapshot(snapshot)

   return SessionContext(
      graph=graph,
      engine_graph=engine_graph,
      archetypes=dict(snapshot.archetypes),
      bank=build_bank(engine, snapshot, snapshot_id, items_directories),
      snapshot_id=snapshot_id,
      errors=dict(snapshot.errors),
      unit_titles=unit_titles(root),
   )
