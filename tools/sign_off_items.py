"""Operator command: adopt agent-drafted items the operator has reviewed as the operator's own.

Usage: python3 tools/sign_off_items.py <target>... --by WHO [--items-dir DIR] [--db PATH]

A target is an item id (ITM-AGT-01004-00), an archetype id (BC-QA-01004, every draft of it), or
all. Run it only after reviewing the named items: provenance model operator is what exit
criterion 7, gates 17 and 30 and the gate 29 audit sample count, and app/items/ingest.py
provenance_model reads a record with no authored_by as the operator's. The previous author moves
to drafted_by and --by is written to signed_off_by, so the record says who adopted it and on
whose authority.

The database, var/growth.db unless --db says otherwise, keeps the provenance it ingested,
because ingest_new_records never re-reads a stored id, so a row already there is updated too. A
target that names nothing refuses the whole run before any file changes.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session as OrmSession

from app.db.models import Item, make_engine
from app.items.ingest import OPERATOR_MODEL

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ITEMS_DIR = REPO_ROOT / "content" / "items_p1_agent"
DEFAULT_DB_PATH = REPO_ROOT / "var" / "growth.db"
EVERY_ITEM = "all"


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Adopt reviewed agent drafts as operator items.")
   parser.add_argument("targets", nargs="+", help="item ids, archetype ids, or all")
   parser.add_argument("--items-dir", default=str(DEFAULT_ITEMS_DIR))
   parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
   parser.add_argument("--by", required=True, help="who signed off, and on whose authority")

   return parser.parse_args(argv)


def matching_paths(directory, target):
   records = sorted(directory.glob("ITM-*.json"))
   is_everything = target == EVERY_ITEM

   if is_everything:
      return records

   is_archetype = target.startswith("BC-QA-")

   if is_archetype:
      return [path for path in records if json.loads(path.read_text())["archetype_id"] == target]

   return [path for path in records if path.stem == target]


def signed_record(record, signed_off_by):
   adopted = dict(record)
   drafted_by = adopted.pop("authored_by", None)
   was_a_draft = drafted_by is not None

   if was_a_draft:
      adopted["drafted_by"] = drafted_by

   adopted["signed_off_by"] = signed_off_by

   return adopted


def update_database(db_path, item_ids):
   has_database = Path(db_path).is_file()

   if not has_database:
      return 0

   engine = make_engine(db_path)
   updated = 0

   with OrmSession(engine) as db:
      for row in db.query(Item).filter(Item.id.in_(item_ids)):
         provenance = json.loads(row.provenance)
         provenance["model"] = OPERATOR_MODEL
         row.provenance = json.dumps(provenance)
         updated += 1

      db.commit()

   return updated


def main(argv):
   arguments = parse_arguments(argv[1:])
   directory = Path(arguments.items_dir)
   chosen = {}

   for target in arguments.targets:
      paths = matching_paths(directory, target)
      names_nothing = len(paths) == 0

      if names_nothing:
         print(f"{target} names no item in {directory}; nothing was changed", file=sys.stderr)

         return 1

      for path in paths:
         chosen[path.stem] = path

   for path in chosen.values():
      record = json.loads(path.read_text())
      path.write_text(json.dumps(signed_record(record, arguments.by), indent=3, ensure_ascii=False) + "\n")

   updated_rows = update_database(arguments.db, sorted(chosen))
   print(f"signed off {len(chosen)} items in {directory}")
   print(f"updated {updated_rows} stored rows in {arguments.db}")

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
