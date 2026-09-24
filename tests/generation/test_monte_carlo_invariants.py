"""11 P4 integration, test_monte_carlo_invariants: every template's family, 300 seeded draws from
its parameter spec, holds every invariant and every rule a single draw can break, with zero
failures (docs/plan/04-item-generation.md, "Monte Carlo over the parameter family")."""
import os
from concurrent.futures import ProcessPoolExecutor

from app.generation.template import FAMILY_DRAWS, library, run_family, template_module, template_modules


def family_report(archetype_id):
   return run_family(template_module(archetype_id)).as_dict()


def test_monte_carlo_invariants():
   archetype_ids = sorted(template_modules())
   workers = max(2, min(8, (os.cpu_count() or 2) - 1))

   with ProcessPoolExecutor(max_workers=workers) as pool:
      reports = list(pool.map(family_report, archetype_ids))

   failing = {
      report["archetype_id"]: (report["template_problems"], report["failures"][:1])
      for report in reports
      if not report["passed"]
   }

   assert len(reports) == len(library().archetypes)
   assert all(report["draws"] == FAMILY_DRAWS for report in reports)
   assert failing == {}
