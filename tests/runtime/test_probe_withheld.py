"""The concept probe's items never reach practice (11 P7 scope item 6: "never used for practice")."""
import json
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.db import models
from app.runtime.bank import ItemBank
from app.runtime.probe_set import PROBE_SET_PATH, probe_item_ids
from tests.runtime.test_context import _make_item


def test_the_default_bank_withholds_every_probe_item(tmp_path):
   probe_ids = sorted(probe_item_ids())
   probe_id = probe_ids[0]
   archetype_id = "-".join(["BC-QA", probe_id.split("-")[2]])
   engine = models.make_engine(tmp_path / "growth.db")

   with OrmSession(engine) as db:
      db.add(_make_item(probe_id, archetype_id, "verified"))
      db.add(_make_item("ITEM-PRACTICE", archetype_id, "verified"))
      db.commit()

   served = [item["id"] for item in ItemBank(engine).published_items(archetype_id)]

   assert served == ["ITEM-PRACTICE"]


def test_every_probe_item_is_a_bank_record(tmp_path):
   recorded = json.loads(Path(PROBE_SET_PATH).read_text())
   bank_ids = {
      path.stem
      for directory in (Path(PROBE_SET_PATH).parents[1]).glob("items_*")
      for path in directory.glob("ITM-*.json")
   }

   assert len(recorded["item_ids"]) == len(set(recorded["item_ids"])) > 0
   assert set(recorded["item_ids"]) <= bank_ids
   assert "operator's delegation" in recorded["drawn_by"]
