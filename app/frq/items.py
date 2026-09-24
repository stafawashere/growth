"""Free-response items: a question in parts, each part carrying the scoring points it can earn.

A record lives in content/frq_items/<id>.json. Its shape, checked by record_violations:

   id, archetype_id, calculator_status, representation, stem {text}, skills, authored_on,
   drafted_by, signed_off_by
   parts: [
      {
         id ("a", "b", ...), prompt, setup_required (true on every calculator part: 11 P3 scope
         item 6 and 05 "Setup shown"), answer_latex, worked_solution [{text, latex}],
         points: [
            {
               point_id, point_type_id (a BC-PT the archetype lists), skills (a subset of the
               item's), criterion (what earns this point on this question, in the author's own
               words), eligible_only_if [point ids that must be earned first],
               follows_from [optional: point ids whose result this point carries forward, so a
               failed check after one of them was lost is judged as follow-through],
               check (null, or one of the four deterministic checks below)
            }
         ]
      }
   ]

The four checks of 03 "Deterministic pre-checks decide the mechanical points", each as data:

   {"kind": "sympy_equivalence", "target": "answer" | "any_line", "expected": <SymPy text>,
    "up_to_constant": bool, "each_side": bool, "variable": "x"}
   {"kind": "numeric_three_decimals", "expected": <SymPy text for the exact value>}
   {"kind": "bounds_match", "lower": <SymPy text>, "upper": <SymPy text>,
    "integrand": <SymPy text or null>, "variable": "x"}
   {"kind": "units_present", "units": [<accepted spellings>]}

Expected values are SymPy text rather than MathJSON because they are compared with SymPy objects
read from the student's LaTeX, and the author states them once, in the form SymPy reads.

A point with a check is decided by the check whenever the check settles and the point type's
label in data/bc_pt_determinism_labels.json is deterministic. Everything else goes to the model.
No served record carries an official stem, figure or rubric sentence.
"""
import json
from pathlib import Path

import sympy

FRQ_FORMAT = "free_response"
FRQ_PUBLISHED_STATUS = "frq_verified"

CHECK_KINDS = ("sympy_equivalence", "numeric_three_decimals", "bounds_match", "units_present")
CHECK_TARGETS = ("answer", "any_line")
CALCULATOR_STATUSES = ("no_calculator", "calculator", "either")

SYMPY_LOCALS = {
   "e": sympy.E,
   "E": sympy.E,
   "pi": sympy.pi,
   "C": sympy.Symbol("C"),
}

REQUIRED_ITEM_FIELDS = (
   "id",
   "archetype_id",
   "calculator_status",
   "representation",
   "stem",
   "skills",
   "parts",
   "authored_on",
   "drafted_by",
)
REQUIRED_PART_FIELDS = ("id", "prompt", "setup_required", "answer_latex", "worked_solution", "points")
REQUIRED_POINT_FIELDS = ("point_id", "point_type_id", "skills", "criterion", "eligible_only_if", "check")


def sympy_of(text):
   return sympy.sympify(text, locals=SYMPY_LOCALS)


def load_frq_records(directory):
   directory_path = Path(directory)
   paths = sorted(directory_path.glob("*.json"))

   return [json.loads(path.read_text()) for path in paths]


def all_points(record):
   return [(part, point) for part in record["parts"] for point in part["points"]]


def point_by_id(record, point_id):
   for part, point in all_points(record):
      if point["point_id"] == point_id:
         return part, point

   return None, None


def _missing(fields, record, where):
   return [f"{where}: missing {name}" for name in fields if name not in record]


def check_violations(check, where):
   kind = check.get("kind")
   is_known_kind = kind in CHECK_KINDS

   if not is_known_kind:
      return [f"{where}: unknown check kind {kind!r}"]

   problems = []
   expressions = []

   if kind == "sympy_equivalence":
      target = check.get("target")
      has_known_target = target in CHECK_TARGETS

      if not has_known_target:
         problems.append(f"{where}: sympy_equivalence target must be one of {CHECK_TARGETS}")

      expressions.append(check.get("expected"))

   if kind == "numeric_three_decimals":
      expressions.append(check.get("expected"))

   if kind == "bounds_match":
      expressions.extend([check.get("lower"), check.get("upper")])
      has_integrand = check.get("integrand") is not None

      if has_integrand:
         expressions.append(check["integrand"])

   if kind == "units_present":
      units = check.get("units")
      has_units = isinstance(units, list) and len(units) > 0

      if not has_units:
         problems.append(f"{where}: units_present needs a non-empty units list")

   for text in expressions:
      try:
         sympy_of(str(text))
      except (sympy.SympifyError, TypeError, SyntaxError):
         problems.append(f"{where}: {text!r} is not SymPy text")

   return problems


def record_violations(record, archetypes, point_types):
   """Every structural problem with one record, as sentences. An empty list is a clean record."""
   record_id = record.get("id", "<no id>")
   problems = _missing(REQUIRED_ITEM_FIELDS, record, record_id)

   if problems:
      return problems

   archetype = archetypes.get(record["archetype_id"])

   if archetype is None:
      return [f"{record_id}: unknown archetype {record['archetype_id']}"]

   allowed_point_types = set(archetype.get("point_types") or [])
   has_point_types = len(allowed_point_types) > 0

   if not has_point_types:
      problems.append(f"{record_id}: {record['archetype_id']} carries no point_types, so it cannot be point-graded")

   is_known_status = record["calculator_status"] in CALCULATOR_STATUSES

   if not is_known_status:
      problems.append(f"{record_id}: calculator_status {record['calculator_status']!r}")

   item_skills = set(record["skills"])
   seen_point_ids = set()
   seen_part_ids = set()

   for part in record["parts"]:
      part_where = f"{record_id} part {part.get('id')}"
      problems.extend(_missing(REQUIRED_PART_FIELDS, part, part_where))

      if part.get("id") in seen_part_ids:
         problems.append(f"{part_where}: duplicate part id")

      seen_part_ids.add(part.get("id"))
      is_calculator_part = record["calculator_status"] == "calculator"
      states_setup = bool(part.get("setup_required"))

      if is_calculator_part and not states_setup:
         problems.append(f"{part_where}: a calculator part must set setup_required")

      for point in part.get("points", []):
         point_where = f"{part_where} point {point.get('point_id')}"
         problems.extend(_missing(REQUIRED_POINT_FIELDS, point, point_where))

         if point.get("point_id") in seen_point_ids:
            problems.append(f"{point_where}: duplicate point id")

         seen_point_ids.add(point.get("point_id"))
         point_type_id = point.get("point_type_id")
         is_known_point_type = point_type_id in point_types
         is_allowed = point_type_id in allowed_point_types

         if not is_known_point_type:
            problems.append(f"{point_where}: unknown point type {point_type_id}")
         elif not is_allowed:
            problems.append(f"{point_where}: {point_type_id} is not in {record['archetype_id']}'s point_types")

         stray_skills = set(point.get("skills") or []) - item_skills

         if stray_skills:
            problems.append(f"{point_where}: skills {sorted(stray_skills)} are not the item's")

         has_check = point.get("check") is not None

         if has_check:
            problems.extend(check_violations(point["check"], point_where))

   for _part, point in all_points(record):
      named = set(point.get("eligible_only_if") or []) | set(point.get("follows_from") or [])
      unknown = named - seen_point_ids

      if unknown:
         problems.append(f"{record_id} point {point['point_id']}: eligible_only_if names {sorted(unknown)}")

   return problems


def points_total(record):
   return len(all_points(record))


def served_record(record):
   """What the student sees before answering: the stem and each part's prompt, never an answer,
   a worked solution, a criterion or a check."""
   return {
      "id": record["id"],
      "archetype_id": record["archetype_id"],
      "calculator_status": record["calculator_status"],
      "stem": record["stem"]["text"],
      "parts": [
         {
            "id": part["id"],
            "prompt": part["prompt"],
            "setup_required": bool(part["setup_required"]),
            "points": len(part["points"]),
         }
         for part in record["parts"]
      ],
   }
