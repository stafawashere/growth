"""Run the template gate and the Monte Carlo family pass, and show what an author needs.

Usage:
  python3 tools/template_gate.py BC-QA-08001 [BC-QA-06004 ...]      gate the named templates
  python3 tools/template_gate.py --all [--report out.json]          gate every template
  python3 tools/template_gate.py --context BC-QA-08001              the archetype as an author reads it
  python3 tools/template_gate.py --show 3 BC-QA-08001               three instantiated records

Exit 0 when every named template passes, 1 otherwise.
"""
import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.generation.instantiate import instantiate
from app.generation.template import BROKEN_TEMPLATES, library, run_family, template_module, template_modules
from app.items.distractor_paths import error_ids_for_skills


def context(archetype_id):
   snapshot = library()
   archetype = snapshot.archetypes[archetype_id]
   shown = {
      name: archetype.get(name)
      for name in (
         "id", "name", "description", "calculator_status", "representations", "difficulty_factors",
         "invariant_structure", "safe_variables", "difficulty_variables", "expected_solution_path",
         "common_distractors", "typical_wording", "point_types", "skills", "multipart_structure",
      )
   }
   print(json.dumps(shown, indent=1))
   print("\nBC-ERR records held by the archetype's skills:")

   for error_id in sorted(error_ids_for_skills(snapshot, archetype["skills"])):
      print(f"  {error_id}  {snapshot.errors[error_id]['name']}")

   print("\nBC-PT point types:")

   for point_id in archetype.get("point_types") or []:
      point = snapshot.scoring_points.get(point_id, {})
      print(f"  {point_id}  {point.get('name')}")

   print("\nBC-DF dials:")

   for factor_id in archetype.get("difficulty_factors") or []:
      print(f"  {factor_id}  {snapshot.difficulty_factors.get(factor_id, {}).get('name')}")


def gate_one(archetype_id):
   module = template_module(archetype_id)

   return run_family(module).as_dict()


def show(archetype_id, count):
   module = template_module(archetype_id)

   for index in range(count):
      record = instantiate(module, index, f"{archetype_id}:preview:{index}", generated_at="preview")
      print(json.dumps(record, indent=1)[:6000])


def main(argv):
   parser = argparse.ArgumentParser(description="Gate item templates.")
   parser.add_argument("archetypes", nargs="*")
   parser.add_argument("--all", action="store_true")
   parser.add_argument("--context", action="store_true")
   parser.add_argument("--show", type=int, default=0)
   parser.add_argument("--report")
   parser.add_argument("--workers", type=int, default=4)
   arguments = parser.parse_args(argv)

   if arguments.context:
      for archetype_id in arguments.archetypes:
         context(archetype_id)

      return 0

   if arguments.show:
      for archetype_id in arguments.archetypes:
         show(archetype_id, arguments.show)

      return 0

   wanted = sorted(template_modules()) if arguments.all else arguments.archetypes

   for name, failure in sorted(BROKEN_TEMPLATES.items()):
      print(f"BROKEN {name}: {failure}")

   with ProcessPoolExecutor(max_workers=arguments.workers) as pool:
      reports = list(pool.map(gate_one, wanted))

   passed = [report for report in reports if report["passed"]]

   for report in reports:
      verdict = "PASS" if report["passed"] else "FAIL"
      print(f"{verdict} {report['archetype_id']} draws {report['draws']} failures {report['failure_count']} "
            f"surface {report['surface_rate']} distinct {report['distinct_stems']} space {report['draw_space']}")

      if not report["passed"]:
         print(json.dumps({"template_problems": report["template_problems"], "failures": report["failures"]}, indent=1)[:4000])

   print(f"{len(passed)} of {len(reports)} templates pass the gate")

   if arguments.report:
      Path(arguments.report).write_text(json.dumps(reports, indent=1) + "\n")

   return 0 if len(passed) == len(reports) else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))
