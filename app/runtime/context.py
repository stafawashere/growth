"""Builds the SessionContext app/session/service.py is called with, from the live library.

docs/plan/11-phased-delivery.md P1 scope items 1 and 14: loads the registries through
app/content/loader.py, persists the content_snapshots row through app/content/persist.py, builds
the fringe graph app/engine/select.py and app/session/build.py read and the engine graph
app/engine/update.py reads, and wires the item bank of app/runtime/bank.py. No second loader is
built here.
"""
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.api.app import SessionContext
from app.content.loader import load_snapshot
from app.content.persist import record_snapshot
from app.engine.fringe import Graph
from app.engine.update import EngineGraph
from app.runtime.bank import ItemBank

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONTENT_ROOT = REPO_ROOT / "data"


def _archetype_counts(archetypes):
   counts = {}

   for record in archetypes.values():
      for skill_id in record["skills"]:
         counts[skill_id] = counts.get(skill_id, 0) + 1

   return counts


def build_session_context(engine, content_root=None, library_commit=None, loaded_at=None):
   root = content_root or DEFAULT_CONTENT_ROOT
   snapshot = load_snapshot(root)

   with OrmSession(engine) as db:
      row = record_snapshot(db, snapshot, library_commit=library_commit, loaded_at=loaded_at)
      db.commit()
      snapshot_id = row.id

   graph = Graph.from_records(
      archetypes=list(snapshot.archetypes.values()),
      skills=list(snapshot.skills.values()),
      edges=list(snapshot.edges),
      inert_top=snapshot.inert_top_ids,
   )
   engine_graph = EngineGraph(
      hard_parents=snapshot.hard_parents,
      supporting_parents=snapshot.supporting_parents,
      hard_children=snapshot.hard_children,
      archetype_counts=_archetype_counts(snapshot.archetypes),
   )

   return SessionContext(
      graph=graph,
      engine_graph=engine_graph,
      archetypes=dict(snapshot.archetypes),
      bank=ItemBank(engine),
      snapshot_id=snapshot_id,
      errors=dict(snapshot.errors),
   )
