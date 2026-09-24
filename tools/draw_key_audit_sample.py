"""Operator command-line draw of the key-audit sample: gate 29 (eval_p1_key_error_rate) in
docs/plan/11-phased-delivery.md, P1 exit criterion 4, and docs/operator/key-audit.md.

Draws app/review/audit.draw_key_audit_sample over every published operator-authored item in the database, stratified
by unit (no more than 15 per unit, or the smallest cap that fills the sample when the items span
fewer units, audit.unit_cap_for) and by calculator_status in proportion to what is published,
with a deterministic seed so the same database and seed always produce the same sample. Writes the
sample file docs/operator/key-audit.md describes: a JSON array of the sampled item ids, ready to
hand to tools/check_audit_verdicts.py and to Settings.key_audit_sample_path.

Usage: python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json> [seed] [--generated]

--generated restricts the draw to items instantiated from a template (P4's key audit, which
measures the generator against the P1 baseline), read from the provenance ingest stored.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session as OrmSession

from app.content.loader import load_snapshot
from app.db.models import Item, make_engine
from app.items.ingest import OPERATOR_MODEL
from app.review.audit import EVAL_29_SAMPLE_SIZE, draw_key_audit_sample, unit_cap_for
from app.runtime.bank import PUBLISHED_STATUS

DEFAULT_SEED = 2026


def published_candidates(engine, snapshot, generated_only=False):
   """Published is the bank's status, verified (app/runtime/bank.py). Only the operator's own
   items are candidates: an agent draft is served under the operator's ruling of 2026-09-23 but
   gate 29 audits operator provenance alone.
   """
   with OrmSession(engine) as db:
      rows = (
         db.query(Item.id, Item.archetype_id, Item.calculator_status, Item.provenance)
         .filter(Item.status == PUBLISHED_STATUS)
         .all()
      )

   candidates = []

   for item_id, archetype_id, calculator_status, provenance in rows:
      archetype = snapshot.archetypes.get(archetype_id)
      has_archetype = archetype is not None
      stored = json.loads(provenance)
      is_operator_item = stored.get("model") == OPERATOR_MODEL
      is_generated = stored.get("template_id") is not None
      is_in_scope = is_generated or not generated_only
      is_candidate = has_archetype and is_operator_item and is_in_scope

      if not is_candidate:
         continue

      candidates.append({
         "item_id": item_id,
         "unit": archetype["primary_unit"],
         "calculator_status": calculator_status,
      })

   return candidates


def main(argv):
   generated_only = "--generated" in argv
   argv = [argument for argument in argv if argument != "--generated"]
   takes_the_needed_arguments = len(argv) in (4, 5)

   if not takes_the_needed_arguments:
      print(
         "usage: python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json> [seed] [--generated]",
         file=sys.stderr,
      )

      return 1

   db_path, content_root, out_path = argv[1], argv[2], argv[3]
   seed = int(argv[4]) if len(argv) == 5 else DEFAULT_SEED

   engine = make_engine(db_path)
   snapshot = load_snapshot(content_root)
   candidates = published_candidates(engine, snapshot, generated_only)

   try:
      sample = draw_key_audit_sample(
         candidates,
         rng_seed=seed,
         sample_size=EVAL_29_SAMPLE_SIZE,
         max_per_unit=unit_cap_for(candidates),
      )
   except ValueError as refused:
      print(f"cannot draw the sample: {refused}", file=sys.stderr)

      return 1

   Path(out_path).write_text(json.dumps(sample, indent=2))
   print(f"drew {len(sample)} items from {len(candidates)} published candidates, seed {seed}")
   print(f"wrote {out_path}")

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
