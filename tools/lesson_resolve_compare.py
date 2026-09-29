"""Confirms a lesson record says what its design says, so the design's blind re-solve and block
audit carry over to the record (docs/lessons/BUILD-PLAN.md, The design to record path, steps 3
and 4).

Compared, in order: the prediction's stem, each option's id, label and key flag, its key and its
resolution; the orientation text; every key idea's text; every strategy block's cue, method, rival
and separating feature and its contrast texts (this, not this, why not, feature); every worked
example's problem text, each step's cue and why, its answer key and its fade_from; every error
block's observed behaviour, scoring consequence, wrong and right step text, possible reason and
fix_prompt, matched by error id; every prerequisite bridge's text,
matched by prerequisite id; the representations text; every check's stem and key; a decision
lesson's stems. Text is equal after whitespace normalisation. A key is equal when
app.items.verify.equivalence finds the record's MathJSON (app/items/mathjson.to_sympy) equivalent
to the design's SymPy string (tools/check_lesson_designs.parse_expression); a statement key is
compared as text.

When every field is equal and docs/lessons/verification/<id>.json exists, its resolve and audit
blocks are copied into docs/operator/lesson-audit/<id>.json with the record's version, the
comparison date and the auditor, which is the record's sign-off evidence.

Exit 0 only when every field is equal.

Usage: python3 tools/lesson_resolve_compare.py <record.json> <design.md>
"""
import json
import sys
from datetime import date
from pathlib import Path

import sympy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.items import verify
from app.items.mathjson import to_sympy
from tools.check_lesson_designs import Design, parse_expression

VERIFICATION_DIR = ROOT / "docs" / "lessons" / "verification"
AUDIT_DIR = ROOT / "docs" / "operator" / "lesson-audit"
AUDITOR = "claude-opus-5-5"
EQUAL = "equal"
DIFFERS = "DIFFERS"
STRATEGY_FIELDS = ("cue", "method", "rival", "separating_feature")
ERROR_FIELDS = ("observed_behavior", "scoring_consequence")
CONTRAST_TEXTS = (("this", ("this", "text")), ("not_this", ("not_this", "text")), ("why_not", ("not_this", "why_not")), ("feature", ("feature",)))


def normalised(text):
   return " ".join(str(text or "").split())


def sections_of(record, section_type):
   return [section for section in record.get("sections") or [] if section["type"] == section_type]


def text_of(node):
   if isinstance(node, dict):
      return node.get("text")

   return node


def text_row(field, record_text, design_text):
   both_absent = record_text is None and design_text is None
   one_absent = (record_text is None) != (design_text is None)
   is_equal = both_absent or (not one_absent and normalised(record_text) == normalised(design_text))

   return (field, is_equal, "" if is_equal else f"record {normalised(record_text)!r} against design {normalised(design_text)!r}")


def key_row(field, record_key, design_key):
   is_missing = record_key is None or design_key is None

   if is_missing:
      return (field, False, "a key is missing on one side")

   is_statement = design_key.get("form") == "statement"

   if is_statement:
      design_text = design_key.get("text") or design_key.get("label")
      record_text = record_key.get("text") or record_key.get("label")
      design_value = design_key.get("expr")
      record_value = record_key.get("mathjson")
      same_text = text_row(field, record_text, design_text)
      same_value = str(record_value) == str(design_value)

      if not same_value:
         return (field, False, f"record value {record_value!r} against design {design_value!r}")

      return same_text

   try:
      record_expression = to_sympy(record_key["mathjson"])
      design_expression = parse_expression(str(design_key["expr"]))
      outcome = verify.equivalence(record_expression, design_expression)
   except Exception as error:
      return (field, False, f"the keys did not compare: {type(error).__name__}: {error}")

   is_equal = outcome == "equivalent"

   return (field, is_equal, "" if is_equal else f"record {record_expression} against design {design_expression} ({outcome})")


def value_row(field, record_value, design_value):
   is_equal = record_value == design_value

   return (field, is_equal, "" if is_equal else f"record {record_value!r} against design {design_value!r}")


def text_at(node, path):
   for key in path:
      if not isinstance(node, dict):
         return None

      node = node.get(key)

   return node


def pairs(record_list, design_list):
   longest = max(len(record_list), len(design_list))

   for index in range(longest):
      record_entry = record_list[index] if index < len(record_list) else None
      design_entry = design_list[index] if index < len(design_list) else None

      yield index + 1, record_entry or {}, design_entry or {}


def prediction_rows(record, design):
   predictions = sections_of(record, "prediction")
   record_prediction = predictions[0] if predictions else None
   design_prediction = design.get("prediction")
   has_either = record_prediction is not None or design_prediction is not None

   if not has_either:
      return []

   record_prediction = record_prediction or {}
   design_prediction = design_prediction or {}
   rows = [text_row("prediction stem", text_at(record_prediction, ("stem", "text")), text_at(design_prediction, ("stem", "text")))]

   for index, record_option, design_option in pairs(record_prediction.get("options") or [], design_prediction.get("options") or []):
      record_marks = (record_option.get("id"), normalised(record_option.get("label")), bool(record_option.get("is_key")))
      design_marks = (design_option.get("id"), normalised(design_option.get("label")), bool(design_option.get("is_key")))
      rows.append(value_row(f"prediction option {index}", record_marks, design_marks))

   has_key = "answer_key" in record_prediction or "key" in design_prediction

   if has_key:
      rows.append(key_row("prediction key", record_prediction.get("answer_key"), design_prediction.get("key")))

   rows.append(text_row("prediction resolution", text_of(record_prediction.get("resolution")), text_of(design_prediction.get("resolution"))))

   return rows


def orientation_rows(record, design):
   orientation = sections_of(record, "orientation")
   record_text = orientation[0]["text"] if orientation else None
   design_orientation = design.get("orientation")

   if design_orientation is None:
      return []

   return [text_row("orientation", record_text, text_of(design_orientation))]


def key_idea_rows(record, design):
   return [
      text_row(f"key_idea {index}", record_entry.get("text"), design_entry.get("text"))
      for index, record_entry, design_entry in pairs(sections_of(record, "key_ideas"), design.get("key_ideas") or [])
   ]


def strategy_rows(record, design):
   rows = []

   for index, record_entry, design_entry in pairs(sections_of(record, "strategy"), design.get("strategy") or []):
      for name in STRATEGY_FIELDS:
         rows.append(text_row(f"strategy {index} {name}", record_entry.get(name), design_entry.get(name)))

      has_contrast = "contrast" in record_entry or "contrast" in design_entry

      if not has_contrast:
         continue

      for name, path in CONTRAST_TEXTS:
         record_text = text_at(record_entry.get("contrast"), path)
         design_text = text_at(design_entry.get("contrast"), path)
         rows.append(text_row(f"strategy {index} contrast {name}", record_text, design_text))

   return rows


def example_rows(record, design):
   rows = []

   for index, record_entry, design_entry in pairs(sections_of(record, "worked_example"), design.get("worked_examples") or []):
      label = f"worked_example {index}"
      rows.append(text_row(f"{label} problem", (record_entry.get("problem") or {}).get("text"), (design_entry.get("problem") or {}).get("text")))

      for step_index, record_step, design_step in pairs(record_entry.get("steps") or [], design_entry.get("steps") or []):
         rows.append(text_row(f"{label} step {step_index} cue", record_step.get("cue"), design_step.get("cue")))
         rows.append(text_row(f"{label} step {step_index} why", record_step.get("why"), design_step.get("why")))

      rows.append(key_row(f"{label} key", record_entry.get("answer"), design_entry.get("answer")))
      has_fade = "fade_from" in record_entry or "fade_from" in design_entry

      if has_fade:
         rows.append(value_row(f"{label} fade_from", record_entry.get("fade_from"), design_entry.get("fade_from")))

   return rows


def error_rows(record, design):
   rows = []
   record_blocks = {section["error_id"]: section for section in sections_of(record, "common_error")}
   design_blocks = {block["error_id"]: block for block in design.get("common_errors") or []}

   for error_id in sorted(set(record_blocks) | set(design_blocks)):
      record_block = record_blocks.get(error_id) or {}
      design_block = design_blocks.get(error_id) or {}
      label = f"error {error_id}"

      for name in ERROR_FIELDS:
         rows.append(text_row(f"{label} {name}", record_block.get(name), design_block.get(name)))

      for name in ("wrong_step", "right_step"):
         rows.append(text_row(f"{label} {name}", text_of(record_block.get(name)), text_of(design_block.get(name))))

      has_reason = "possible_reason" in record_block or "possible_reason" in design_block

      if has_reason:
         rows.append(text_row(f"{label} possible_reason", text_of(record_block.get("possible_reason")), text_of(design_block.get("possible_reason"))))

      has_fix_prompt = "fix_prompt" in record_block or "fix_prompt" in design_block

      if has_fix_prompt:
         rows.append(value_row(f"{label} fix_prompt", record_block.get("fix_prompt"), design_block.get("fix_prompt")))

   return rows


def bridge_rows(record, design):
   record_bridges = {section["prerequisite_id"]: section for section in sections_of(record, "prerequisite_bridge")}
   design_bridges = {bridge.get("prq_id"): bridge for bridge in design.get("prerequisite_bridges") or []}

   return [
      text_row(f"bridge {prerequisite_id}", (record_bridges.get(prerequisite_id) or {}).get("text"), (design_bridges.get(prerequisite_id) or {}).get("text"))
      for prerequisite_id in sorted(set(record_bridges) | set(design_bridges))
   ]


def representation_rows(record, design):
   record_sections = sections_of(record, "representations")
   design_representations = design.get("representations")
   has_either = len(record_sections) > 0 or bool(design_representations)

   if not has_either:
      return []

   if isinstance(design_representations, list):
      design_representations = design_representations[0] if design_representations else None

   record_text = record_sections[0]["text"] if record_sections else None

   return [text_row("representations", record_text, text_of(design_representations))]


def check_rows(record, design):
   rows = []

   for index, record_check, design_check in pairs(record.get("checks") or [], design.get("checks") or []):
      label = f"check {index}"
      rows.append(text_row(f"{label} stem", (record_check.get("stem") or {}).get("text"), (design_check.get("stem") or {}).get("text")))
      rows.append(key_row(f"{label} key", record_check.get("answer_key"), design_check.get("key")))
      rows.extend(option_rows(label, record_check.get("options") or [], design_check.get("options") or []))

   return rows


def option_value(option):
   value = option["mathjson"] if "mathjson" in option else option["value"]
   is_symbol_name = isinstance(value, str) and value.isidentifier()
   is_mathjson = isinstance(value, (list, dict)) or is_symbol_name

   if is_mathjson:
      return to_sympy(value)

   return parse_expression(str(value))


def same_value(record_value, design_value):
   both_undefined = record_value is sympy.nan and design_value is sympy.nan

   if both_undefined:
      return "equivalent"

   return verify.equivalence(record_value, design_value)


def option_rows(label, record_options, design_options):
   """An option's letter, key flag, error path and value, so a distractor that says one number
   while the key says another cannot pass on the key row alone."""
   rows = []

   for index, record_option, design_option in pairs(record_options, design_options):
      field = f"{label} option {index}"
      record_marks = (record_option.get("id"), bool(record_option.get("is_key")), record_option.get("error_path"))
      design_marks = (design_option.get("id"), bool(design_option.get("is_key")), design_option.get("error_path"))
      marks_equal = record_marks == design_marks
      rows.append((f"{field} marks", marks_equal, "" if marks_equal else f"record {record_marks} against design {design_marks}"))
      has_design_value = "expr" in design_option

      if not has_design_value:
         rows.append(text_row(f"{field} text", record_option.get("text"), design_option.get("text")))
         continue

      try:
         outcome = same_value(option_value(record_option), parse_expression(str(design_option["expr"])))
      except Exception as error:
         rows.append((f"{field} value", False, f"the values did not compare: {type(error).__name__}: {error}"))
         continue

      is_equal = outcome == "equivalent"
      rows.append((f"{field} value", is_equal, "" if is_equal else f"record {record_option} against design {design_option['expr']} ({outcome})"))

   return rows


def decision_rows(record, design):
   record_stems = (record.get("decision") or {}).get("stems") or []
   design_stems = (design.get("decision") or {}).get("stems") or []

   return [
      text_row(f"decision stem {index}", record_stem.get("text"), design_stem.get("text"))
      for index, record_stem, design_stem in pairs(record_stems, design_stems)
   ]


def compare(record, design_record):
   """(field, equal, detail) rows for every compared field, in the order the module names."""
   rows = []

   for builder in (prediction_rows, orientation_rows, key_idea_rows, strategy_rows, example_rows, error_rows, bridge_rows, representation_rows, check_rows, decision_rows):
      rows.extend(builder(record, design_record))

   return rows


def load_design(path):
   path = Path(path)
   design = Design(path, path.read_text())

   if design.record is None:
      raise ValueError(f"{path} has no machine record: {design.record_error}")

   return design.record


def write_audit_evidence(record, verification_dir, audit_dir, today):
   source = Path(verification_dir) / f"{record['id']}.json"

   if not source.is_file():
      return None

   verification = json.loads(source.read_text())
   evidence = {
      "lesson_id": record["id"],
      "version": record["version"],
      "compared_on": today.isoformat(),
      "auditor": AUDITOR,
      "resolve": verification.get("resolve"),
      "audit": verification.get("audit"),
   }
   audit_dir = Path(audit_dir)
   audit_dir.mkdir(parents=True, exist_ok=True)
   target = audit_dir / f"{record['id']}.json"
   target.write_text(json.dumps(evidence, indent=1) + "\n")

   return target


def print_report(rows):
   for field, is_equal, detail in rows:
      verdict = EQUAL if is_equal else DIFFERS
      suffix = f": {detail}" if detail else ""
      print(f"{verdict} {field}{suffix}")

   differing = sum(1 for _, is_equal, _ in rows if not is_equal)
   print()
   print(f"fields compared: {len(rows)}")
   print(f"differing: {differing}")


def main(argv, verification_dir=VERIFICATION_DIR, audit_dir=AUDIT_DIR, today=None):
   takes_two_paths = len(argv) == 3

   if not takes_two_paths:
      print("usage: python3 tools/lesson_resolve_compare.py <record.json> <design.md>", file=sys.stderr)

      return 2

   record = json.loads(Path(argv[1]).read_text())
   rows = compare(record, load_design(argv[2]))
   print_report(rows)
   all_equal = len(rows) > 0 and all(is_equal for _, is_equal, _ in rows)

   if not all_equal:
      return 1

   written = write_audit_evidence(record, verification_dir, audit_dir, today or date.today())

   if written is not None:
      print(f"sign-off evidence written to {written}")

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
