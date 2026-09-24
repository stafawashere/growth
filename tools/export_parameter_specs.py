"""Propose every template's parameter spec to the library as one staging file.

docs/plan/04-item-generation.md, "The missing parameter spec": the spec is authored with the
template in the app repository and proposed back to the library as a staging file. This writes
data/staging/parameter-spec-p4.json, a "fields" staging file that sets only parameter_spec on each
archetype, for tools/merge_staging.py. A spec that does not validate against the archetype stops
the export.

Usage: python3 tools/export_parameter_specs.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.generation.spec import validate_spec
from app.generation.template import BROKEN_TEMPLATES, library, template_modules

STAGING = ROOT / "data" / "staging" / "parameter-spec-p4.json"


def main():
   modules = template_modules()
   archetypes = library().archetypes
   problems = [f"{name}: {failure}" for name, failure in sorted(BROKEN_TEMPLATES.items())]
   records = []

   for archetype_id, module in sorted(modules.items()):
      spec_problems = validate_spec(module.SPEC, archetypes[archetype_id])

      if spec_problems:
         problems.append(f"{archetype_id}: {spec_problems}")
         continue

      records.append({"id": archetype_id, "parameter_spec": module.SPEC})

   if problems:
      print("\n".join(problems), file=sys.stderr)
      return 1

   staged = {"registry": "archetypes", "merge": "fields", "archetypes": records}
   STAGING.write_text(json.dumps(staged, indent=1) + "\n")
   print(f"{len(records)} parameter specs in {STAGING.relative_to(ROOT)}")

   return 0


if __name__ == "__main__":
   sys.exit(main())
