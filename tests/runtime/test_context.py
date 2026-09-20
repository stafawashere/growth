"""The composition root: SessionContext over the live library, and the item bank over items.

docs/plan/11-phased-delivery.md P1 scope items 1, 12 and 14; docs/plan/06-architecture.md "items".
tests/api/conftest.py builds the SessionContext by hand over a fixture; this module is what does
the equivalent build over the real data/ registries and the real items table, and app/main.py is
the entrypoint that wires it to a FastAPI application with no network call.
"""
import importlib
import json
import socket
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db import models
from app.runtime.bank import ItemBank
from app.runtime.context import build_session_context

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_ROOT = REPO_ROOT / "data"

ITEM_REQUIRED_TEXT = {
   "parameter_draw": "{}",
   "stem": "stem",
   "answer_key": '{"key": "x"}',
   "worked_solution": "{}",
   "calculator_status": "no_calculator",
   "representation": "BC-REP-01",
   "difficulty_settings": "{}",
   "skills": '["BC-SKL-01024"]',
   "provenance": '{"model": "operator"}',
   "dedupe_minhash": "hash-0001",
}


def _make_item(item_id, archetype_id, status):
   return models.Item(
      id=item_id,
      archetype_id=archetype_id,
      variant_id=None,
      snapshot_id="SNAP-0001",
      figure_spec=None,
      options=None,
      status=status,
      created_at="2026-01-01T00:00:00+00:00",
      updated_at="2026-01-01T00:00:00+00:00",
      **ITEM_REQUIRED_TEXT,
   )


def test_context_builds_from_the_live_registries(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   expected = load_snapshot(DATA_ROOT)

   context = build_session_context(engine, DATA_ROOT)

   assert set(context.graph.archetypes.keys()) == set(expected.archetypes.keys())
   assert context.engine_graph.hard_parents == expected.hard_parents
   assert context.engine_graph.supporting_parents == expected.supporting_parents
   assert context.archetypes == expected.archetypes
   assert context.bank.has_published_item(next(iter(expected.archetypes))) is False
   assert isinstance(context.snapshot_id, str) and context.snapshot_id != ""

   with OrmSession(engine) as db:
      row = db.get(models.ContentSnapshot, context.snapshot_id)

   assert row is not None
   assert row.status == "active"


def test_bank_publishes_only_verified_rows(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      db.add(_make_item("ITEM-001", "BC-QA-01004", "verified"))
      db.add(_make_item("ITEM-002", "BC-QA-01004", "draft"))
      db.commit()

   bank = ItemBank(engine)
   published = bank.published_items("BC-QA-01004")

   assert [item["id"] for item in published] == ["ITEM-001"]
   assert published[0]["status"] == "verified"
   assert published[0]["skills"] == json.loads(ITEM_REQUIRED_TEXT["skills"])


def test_bank_has_no_published_item_for_a_draft_only_archetype(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      db.add(_make_item("ITEM-003", "BC-QA-01008", "draft"))
      db.commit()

   bank = ItemBank(engine)

   assert bank.has_published_item("BC-QA-01008") is False
   assert bank.published_items("BC-QA-01008") == []


def test_main_builds_an_application_without_touching_the_network(tmp_path, monkeypatch):
   def refuses_sockets(*args, **kwargs):
      raise AssertionError("app.main built an application but opened a network socket")

   monkeypatch.setenv("GROWTH_DB_PATH", str(tmp_path / "growth.db"))
   monkeypatch.setenv("GROWTH_CONTENT_ROOT", str(DATA_ROOT))
   monkeypatch.setattr(socket, "socket", refuses_sockets)

   import app.main as main_module

   importlib.reload(main_module)

   try:
      assert isinstance(main_module.application, FastAPI)
      assert main_module.application.state.settings.bind_host == "127.0.0.1"
      assert main_module.application.state.settings.rp_id == "localhost"
      assert main_module.application.state.settings.session_context is not None
   finally:
      monkeypatch.setenv("GROWTH_DB_PATH", str(tmp_path / "growth-reset.db"))
      importlib.reload(main_module)


def test_bank_hides_the_answer_key_and_the_error_paths(tmp_path):
   """A served item is what the student may see: no key, no worked solution, no error paths."""
   engine = models.make_engine(tmp_path / "growth.db")
   options = [
      {"id": "A", "value": "2x", "is_key": True, "error_path": None},
      {"id": "B", "value": "x", "is_key": False, "error_path": "BC-ERR-02001"},
   ]

   with OrmSession(engine) as db:
      row = _make_item("ITEM-KEY", "BC-QA-02006", "verified")
      row.options = options
      db.add(row)
      db.commit()

   served = ItemBank(engine).published_items("BC-QA-02006")[0]

   assert "answer_key" not in served
   assert "worked_solution" not in served
   assert [option["id"] for option in served["options"]] == ["A", "B"]

   for option in served["options"]:
      assert "error_path" not in option
      assert "is_key" not in option
