"""Recheck every deterministic check's expected value in a free-response bank against a blind
formulation written from the question text alone, with a built-in control.

Usage:
   python3 tools/frq_key_recheck.py stems <bank_dir> <out.md>
      writes the questions with every answer, criterion, check and worked solution removed, for
      the agent that writes the formulations (question-bank-audit step 1);
   python3 tools/frq_key_recheck.py check <bank_dir> <formulations.py> [--report out.md]
      compares, point by point, the value the formulation computes with the check's expected
      value. formulations.py defines FORMULATIONS, a dict from "<item id>:<point id>" to a
      zero-argument function returning a SymPy expression.

Checks compared: sympy_equivalence and numeric_three_decimals (the value), bounds_match (lower and
upper). up_to_constant checks compare derivatives in the check's variable. units_present checks are
listed for reading, not compared. The control perturbs every computed value (2v + 1 and
v + sqrt(2)/7, skipping one identical to v, and only 2v + 1 for a check that accepts any
constant, since an added constant is not a wrong antiderivative) and requires each perturbation
to compare different;
if any does not, the comparator cannot tell a wrong key from a right one and the run exits 2.

Exit 0 when every checked point matches, 1 on a difference or a missing formulation, 2 when the
control fails.
"""
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import sympy

from app.frq.items import all_points, load_frq_records, sympy_of

COMPARED_KINDS = ("sympy_equivalence", "numeric_three_decimals", "bounds_match")


def stems_document(records):
   lines = ["# Free-response questions, stems and part prompts only", ""]

   for record in records:
      lines.append(f"## {record['id']} ({record['archetype_id']})")
      lines.append("")
      lines.append(record["stem"]["text"])
      lines.append("")

      for part in record["parts"]:
         lines.append(f"- part ({part['id']}): {part['prompt']}")

         for point in part["points"]:
            check = point.get("check") or {}
            kind = check.get("kind")

            if kind in COMPARED_KINDS:
               is_bounds = kind == "bounds_match"
               is_intermediate = check.get("target") == "any_line"
               wanted = "the lower and upper limits of the definite integral" if is_bounds else "the part's final answer"
               wanted = "an intermediate expression the work must contain" if is_intermediate else wanted
               note = " (an antiderivative, any constant)" if check.get("up_to_constant") else ""
               note = note + f" [{point['point_type_id']}]"
               lines.append(f"   - key {record['id']}:{point['point_id']}: {wanted} this point checks{note}; variable {check.get('variable') or 'x'}")

      lines.append("")

   return "\n".join(lines)


def load_formulations(path):
   spec = importlib.util.spec_from_file_location("frq_formulations", path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

   return module.FORMULATIONS


def equal(left, right, up_to_constant=False, variable=None):
   """Equal when the difference simplifies to 0 or vanishes at six rational points. Unevaluated
   integrals are evaluated first. A difference that cannot be evaluated is not called equal."""
   difference = sympy.sympify(left).doit() - sympy.sympify(right).doit()

   if up_to_constant:
      difference = sympy.diff(difference, variable)

   simplified = sympy.simplify(difference)

   if simplified == 0:
      return True

   free = sorted(simplified.free_symbols, key=lambda symbol: symbol.name)
   samples = [{symbol: sympy.Rational(3 + index, 7 + index) for symbol in free} for index in range(6)]
   try:
      values = [complex(simplified.subs(sample).evalf()) for sample in samples]
   except TypeError:
      return False

   return all(abs(value) < 1e-9 for value in values)


def expected_values(check):
   kind = check["kind"]

   if kind == "bounds_match":
      return [sympy_of(check["lower"]), sympy_of(check["upper"])]

   return [sympy_of(check["expected"])]


def computed_values(check, computed):
   is_bounds = check["kind"] == "bounds_match"

   return list(computed) if is_bounds else [computed]


def perturbations(value, up_to_constant=False):
   """Wrong answers the comparator must reject. An added constant is not a wrong antiderivative,
   so a check that accepts any constant is perturbed by scaling only."""
   candidates = [2 * value + 1] if up_to_constant else [2 * value + 1, value + sympy.sqrt(2) / 7]

   return [candidate for candidate in candidates if sympy.simplify(candidate - value) != 0]


def check_bank(records, formulations):
   results = []

   for record in records:
      for _part, point in all_points(record):
         check = point.get("check") or {}

         if check.get("kind") not in COMPARED_KINDS:
            continue

         key = f"{record['id']}:{point['point_id']}"
         formulation = formulations.get(key)

         if formulation is None:
            results.append((key, "not_formulated", None))
            continue

         variable = sympy.Symbol(check.get("variable") or "x")
         up_to_constant = bool(check.get("up_to_constant"))
         computed = computed_values(check, formulation())
         expected = expected_values(check)
         matches = all(equal(left, right, up_to_constant, variable) for left, right in zip(computed, expected))
         results.append((key, "match" if matches else "key_differs", (computed, expected, up_to_constant, variable)))

   return results


def control_holds(results):
   for _key, status, detail in results:
      if status != "match":
         continue

      computed, expected, up_to_constant, variable = detail

      for value, key_value in zip(computed, expected):
         for wrong in perturbations(sympy.sympify(value), up_to_constant):
            if equal(wrong, key_value, up_to_constant, variable):
               return False

   return True


def main(argv):
   command = argv[1]
   records = load_frq_records(argv[2])

   if command == "stems":
      Path(argv[3]).write_text(stems_document(records) + "\n")
      print(f"{len(records)} questions written to {argv[3]}")

      return 0

   formulations = load_formulations(argv[3])
   results = check_bank(records, formulations)
   control = control_holds(results)
   counts = {}

   for key, status, _detail in results:
      counts[status] = counts.get(status, 0) + 1

      if status != "match":
         print(f"{status}: {key}")

   print(f"control: {'held' if control else 'FAILED'}")
   print(f"checked points: {len(results)}, " + ", ".join(f"{name} {count}" for name, count in sorted(counts.items())))
   has_report = "--report" in argv

   if has_report:
      report_path = Path(argv[argv.index("--report") + 1])
      report_path.write_text(json.dumps({"counts": counts, "control": control}, indent=1) + "\n")

   if not control:
      return 2

   return 0 if counts.get("match", 0) == len(results) else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
