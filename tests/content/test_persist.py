"""docs/plan/06-architecture.md "content_snapshots" and "Versioning"."""
import json
from pathlib import Path
from types import SimpleNamespace

from sqlalchemy.orm import Session

from app.content.loader import load_snapshot
from app.content.persist import record_rejected_snapshot, record_snapshot
from app.db.models import ContentSnapshot, make_engine

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = REPO_ROOT / "data"


def test_snapshot_row_written_on_load(tmp_path):
   engine = make_engine(tmp_path / "p1.sqlite")
   snapshot = load_snapshot(DATA_ROOT)

   with Session(engine) as session:
      first_row = record_snapshot(session, snapshot, library_commit="abc123")
      session.commit()

      assert first_row.status == "active"
      assert first_row.digest == snapshot.digest
      assert first_row.library_commit == "abc123"
      assert json.loads(first_row.counts) == snapshot.counts

      changed_snapshot = SimpleNamespace(digest="a-different-digest", counts=snapshot.counts)
      second_row = record_snapshot(session, changed_snapshot)
      session.commit()

      rows = session.query(ContentSnapshot).order_by(ContentSnapshot.loaded_at).all()
      first_after = session.get(ContentSnapshot, first_row.id)

      assert first_after.status == "superseded"
      assert second_row.status == "active"
      assert len(rows) == 2


def test_reload_with_unchanged_digest_reuses_active_row(tmp_path):
   engine = make_engine(tmp_path / "p1.sqlite")
   snapshot = load_snapshot(DATA_ROOT)

   with Session(engine) as session:
      first_row = record_snapshot(session, snapshot, library_commit="abc123")
      session.commit()

      same_digest_row = record_snapshot(session, snapshot, library_commit="def456")
      session.commit()

      rows = session.query(ContentSnapshot).all()

      assert len(rows) == 1
      assert same_digest_row.id == first_row.id
      assert same_digest_row.status == "active"
      assert same_digest_row.library_commit == "def456"


def test_rejected_snapshot_row_records_reason(tmp_path):
   engine = make_engine(tmp_path / "p1.sqlite")

   with Session(engine) as session:
      row = record_rejected_snapshot(session, "deadbeef", "cycle detected in prereq_edges.csv")
      session.commit()

      assert row.status == "rejected"
      assert row.digest == "deadbeef"
      assert row.rejection_reason == "cycle detected in prereq_edges.csv"
