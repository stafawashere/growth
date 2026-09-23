"""Operator command-line draw of the key-audit sample: gate 29 (eval_p1_key_error_rate) in
docs/plan/11-phased-delivery.md, P1 exit criterion 4, and docs/operator/key-audit.md.

Draws app/review/audit.draw_key_audit_sample over every published item in the database, stratified
by unit (no more than 15 per unit) and by calculator_status in proportion to what is published,
with a deterministic seed so the same database and seed always produce the same sample. Writes the
sample file docs/operator/key-audit.md describes: a JSON array of the sampled item ids, ready to
hand to tools/check_audit_verdicts.py and to Settings.key_audit_sample_path.

Usage: python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json> [seed]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db.models import Item, make_engine
from app.review.audit import EVAL_29_SAMPLE_SIZE, draw_key_audit_sample

DEFAULT_SEED = 2026


def published_candidates(engine, snapshot):
   with OrmSession(engine) as db:
      rows = db.query(Item.id, Item.archetype_id, Item.calculator_status).filter(Item.status == "published").all()

   candidates = []

   for item_id, archetype_id, calculator_status in rows:
      archetype = snapshot.archetypes.get(archetype_id)
      has_archetype = archetype is not None

      if not has_archetype:
         continue

      candidates.append({
         "item_id": item_id,
         "unit": archetype["unit"],
         "calculator_status": calculator_status,
      })

   return candidates


def main(argv):
   takes_the_needed_arguments = len(argv) in (4, 5)

   if not takes_the_needed_arguments:
      print(
         "usage: python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json> [seed]",
         file=sys.stderr,
      )

      return 1

   db_path, content_root, out_path = argv[1], argv[2], argv[3]
   seed = int(argv[4]) if len(argv) == 5 else DEFAULT_SEED

   engine = make_engine(db_path)
   snapshot = load_snapshot(content_root)
   candidates = published_candidates(engine, snapshot)

   try:
      sample = draw_key_audit_sample(candidates, rng_seed=seed, sample_size=EVAL_29_SAMPLE_SIZE)
   except ValueError as refused:
      print(f"cannot draw the sample: {refused}", file=sys.stderr)

      return 1

   Path(out_path).write_text(json.dumps(sample, indent=2))
   print(f"drew {len(sample)} items from {len(candidates)} published candidates, seed {seed}")
   print(f"wrote {out_path}")

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
