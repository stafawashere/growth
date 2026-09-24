"""The MCQ distractor property gate 30 (eval_p1_distractor_paths) ranges over, as a checker an
eval or the operator can run over one candidate record: docs/plan/11-phased-delivery.md P1
items 17 and 30, docs/plan/04-item-generation.md "Output schema".

Rejection rules 5, 6 and 7 of 04 are app/items/verify.py's comparison_findings and
error_path_findings, and the option split is app/items/ingest.py's. Neither is restated here,
and this module renders those findings into gate 30's prose.

Policy on a comparison that did not settle: it is a violation, because a record the checker
cannot settle is not a record it may pass. verify.distractor_checks reads the same findings
under the other policy and hands an unsettled comparison back under its own code, which
app/items/ingest.py reads as indeterminate and routes to review. Both policies are deliberate.
"""
from app.items import verify
from app.items.ingest import distractor_options, is_statement_record, key_options
from app.items.mathjson import UnsupportedMathJSON, to_sympy


def error_ids_for_skills(snapshot, skill_ids):
   """The BC-ERR ids reachable from the given skills in the loaded content snapshot, as a
   frozenset. This is the set gate 30 means by "the BC-ERR records the P1 skills hold".
   """
   wanted = frozenset(skill_ids)
   reachable = set()

   for error_id, error in snapshot.errors.items():
      held_skills = error.get("skills") or []
      holds_a_wanted_skill = not wanted.isdisjoint(held_skills)

      if holds_a_wanted_skill:
         reachable.add(error_id)

   return frozenset(reachable)


def distractor_path_violations(record, error_ids):
   """Every way the record breaks gate 30's property, as a list of human-readable strings,
   empty when the property holds. A record with no options is not an MCQ and has no
   violations.
   """
   options = record.get("options") or []
   is_not_an_mcq = len(options) == 0

   if is_not_an_mcq:
      return []

   violations = []
   keys = key_options(record)
   key_count = len(keys)
   has_exactly_one_key = key_count == 1

   if not has_exactly_one_key:
      violations.append(
         f"record carries {key_count} options marked is_key, and gate 30 wants exactly one"
      )

   distractors = distractor_options(record)

   violations.extend(_error_path_violations(distractors, error_ids))

   if is_statement_record(record):
      return violations + _statement_label_violations(options)

   expressions = {}

   for option in options:
      label = _label(option)
      expressions[label] = _expression(option, violations, label)

   key_label = _label(keys[0]) if has_exactly_one_key else None
   key_expression = expressions.get(key_label) if has_exactly_one_key else None

   readable = [option for option in distractors if expressions[_label(option)] is not None]
   readable_expressions = [expressions[_label(option)] for option in readable]

   findings = verify.comparison_findings(key_expression, readable_expressions)

   violations.extend(_comparison_violations(findings, readable, key_label))

   return violations


def _statement_label_violations(options):
   """A statement item's options are sentences: each needs one, and no two may be the same."""
   violations = []
   seen = {}

   for option in options:
      label = _label(option)
      text = " ".join((option.get("label") or "").split())

      if not text:
         violations.append(f"option {label} carries no label")
         continue

      if text in seen:
         violations.append(f"options {seen[text]} and {label} carry the same label")

      seen.setdefault(text, label)

   return violations


def _error_path_violations(distractors, error_ids):
   stated_paths = [option.get("error_path") for option in distractors]
   violations = []

   for finding in verify.error_path_findings(stated_paths, error_ids):
      label = _label(distractors[finding["index"]])
      carries_no_path = finding["reason"] == verify.MISSING_ERROR_PATH

      if carries_no_path:
         violations.append(f"option {label} carries no error_path")
      else:
         stated = finding["error_path"]
         violations.append(
            f"option {label} carries error_path {stated}, "
            "which is not one of the error ids the skills hold"
         )

   return violations


def _comparison_violations(findings, distractors, key_label):
   violations = []

   for finding in findings:
      is_key_comparison = finding["kind"] == verify.KEY_COMPARISON
      is_equal = finding["comparison"] == verify.EQUAL
      did_not_settle = finding["comparison"] == verify.UNSETTLED_VIOLATION
      right_label = _label(distractors[finding["right"]])

      if is_key_comparison:
         if is_equal:
            violations.append(f"option {right_label} equals the key {key_label}")

         if did_not_settle:
            violations.append(
               f"option {right_label} against the key {key_label} did not settle, "
               "so the record is not clean"
            )

         continue

      left_label = _label(distractors[finding["left"]])

      if is_equal:
         violations.append(f"options {left_label} and {right_label} equal each other")

      if did_not_settle:
         violations.append(
            f"options {left_label} and {right_label} against each other did not settle, "
            "so the record is not clean"
         )

   return violations


def _expression(option, violations, label):
   try:
      return to_sympy(option.get("value"))
   except UnsupportedMathJSON as error:
      violations.append(
         f"option {label} has a value that did not settle into an expression: {error}"
      )

      return None


def _label(option):
   stated = option.get("id")
   has_id = stated is not None

   if has_id:
      return stated

   return "with no id"
