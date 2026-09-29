"""Transcribe a lesson design's machine record into a lesson record (docs/lessons/BUILD-PLAN.md,
The design to record path, step 2).

The record is computed from the design's machine record and the authoring bundle alone, so the
same design and snapshot always give the same bytes: no clock, no model, no hand edits. Texts are
copied verbatim; every SymPy string becomes MathJSON through app/items/mathjson.from_sympy; the
delivery entries become each block's delivery object; word_count is app.lessons.plan.band_words,
which is what the app serves (worker D decision 10), and read_minutes is the design's value or the
words at constants.WORDS_PER_MINUTE, whichever is larger.

The framework fields of 2026-09-29 are carried as well: the prediction becomes the first section,
the first strategy block keeps its contrast pair, the second worked example its fade_from, every
error block its fix_prompt (a concept lesson's error block without one is refused), and a lesson
with no drawn block its no_figure_reason.

A design field the record cannot express stops the transcription with the field named.

Usage: python3 tools/lesson_transcribe.py <design.md> [<out.json>]
       without <out.json> the record is written to content/lessons/<id>.json
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.content.loader import load_snapshot
from app.items.mathjson import UnsupportedMathJSON, from_sympy
from app.lessons import constants, plan
from app.lessons.source import authoring_bundle
from tools.check_lesson_designs import Design, parse_expression

DATA_ROOT = ROOT / "data"
CONTENT_LESSONS = ROOT / "content" / "lessons"
AUTHOR = "tools/lesson_transcribe.py"
PROMPT_VERSION = "generator/lesson_v2"
BOTH_BANDS = ["low", "mid"]
RELATION_FIELDS = ("relation", "subs", "approx", "variable", "point", "dir")
STEMS_FALLBACK = "the stems listed one under the other, the selecting feature named under each"
STEMS_KEYBOARD = "Tab moves between the stems"
DEFAULT_REPRESENTATION = "BC-REP-01"
PREDICTION_FIELDS = {"id", "stem", "format", "options", "key", "resolution", "sources"}
PREDICTION_STEM_FIELDS = {"text", "command_verb"}
PREDICTION_OPTION_FIELDS = {"id", "label", "is_key", "expr"}
CONTRAST_FIELDS = {"this", "not_this", "feature"}
CONTRAST_THIS_FIELDS = {"text", "archetype_id"}
CONTRAST_NOT_THIS_FIELDS = {"text", "why_not"}
DEFAULT_PREDICTION_DELIVERY = {"mode": "text", "reason": "rule 6"}


class TranscriptionError(Exception):
   pass


def mathjson_of(text, field):
   """MathJSON for a design's SymPy string, or a refusal naming the field."""
   try:
      expression = parse_expression(text)
   except Exception as error:
      raise TranscriptionError(f"{field}: {text!r} does not parse ({type(error).__name__})")

   try:
      return from_sympy(expression)
   except UnsupportedMathJSON as error:
      raise TranscriptionError(f"{field}: {text!r} has no MathJSON form ({error})")


def answer_of(answer, field):
   """A statement key keeps its text as a MathJSON string, because the design checker never
   parses one (rule_steps and rule_keys skip it)."""
   form = answer.get("form")
   expression = answer.get("expr")
   is_statement = form == "statement"

   if expression is None:
      raise TranscriptionError(f"{field}.expr is missing")

   if is_statement:
      mathjson = str(expression)
   else:
      mathjson = mathjson_of(expression, f"{field}.expr")

   record = {"form": form, "mathjson": mathjson}

   for key in ("label", "text"):
      if answer.get(key):
         record[key] = answer[key]

   return record


def refuse_unknown_fields(node, allowed, field):
   if not isinstance(node, dict):
      raise TranscriptionError(f"{field} is not an object")

   unknown = sorted(set(node) - allowed)

   if unknown:
      raise TranscriptionError(f"{field}.{unknown[0]} is a field the record cannot express")


def relation_fields(step):
   return {key: step[key] for key in RELATION_FIELDS if key in step}


class Transcriber:
   def __init__(self, design, snapshot, recorded_as=None):
      self.design = design
      self.recorded_as = recorded_as
      self.record = design.record
      self.snapshot = snapshot
      self.lesson_id = self.record["id"]
      self.kind = self.record["kind"]
      self.skills = list(self.record.get("skills") or [])
      self.bundle = authoring_bundle(self.record["target_id"], snapshot) if self.kind == "concept" else None
      self.delivery = {}
      self.ids = {}
      self.number = 0

      for entry in self.record.get("delivery") or []:
         self.delivery[entry["block"]] = entry

   def next_id(self):
      self.number += 1

      return f"{self.lesson_id}#s{self.number}"

   def delivery_of(self, block):
      entry = self.delivery.get(block)

      if entry is None:
         raise TranscriptionError(f"delivery has no entry for block {block}")

      return {key: value for key, value in entry.items() if key != "block"}

   def archetype(self, archetype_id):
      return self.snapshot.archetypes.get(archetype_id) or {}

   def skills_of_archetype(self, archetype_id):
      held = self.archetype(archetype_id).get("skills") or []
      shared = [skill for skill in self.skills if skill in held]

      return shared or list(self.skills)

   def skills_of_ek(self, ek_id):
      shared = [
         skill_id
         for skill_id in self.skills
         if ek_id in ((self.snapshot.skills.get(skill_id) or {}).get("essential_knowledge") or [])
      ]

      return shared or list(self.skills)

   def skills_of_error(self, error_id):
      held = (self.snapshot.errors.get(error_id) or {}).get("skills") or []

      return [skill for skill in self.skills if skill in held]

   def skills_of_prerequisite(self, prq_id):
      dependents = {edge["to"] for edge in self.snapshot.edges if edge["from"] == prq_id}
      shared = [skill for skill in self.skills if skill in dependents]

      return shared or list(self.skills)

   def evidence_of(self, identifier, default="inferred"):
      record = self.snapshot.ids.get(identifier) or {}

      return record.get("evidence_tag") or default

   def prediction_delivery(self, label):
      entry = self.delivery.get(label) or self.delivery.get("prediction")

      if entry is None:
         return dict(DEFAULT_PREDICTION_DELIVERY)

      return {key: value for key, value in entry.items() if key != "block"}

   def prediction_option(self, option, label):
      refuse_unknown_fields(option, PREDICTION_OPTION_FIELDS, label)
      record = {"id": option["id"], "label": option["label"], "is_key": option["is_key"]}
      expression = option.get("expr")

      if expression is not None:
         record["value"] = mathjson_of(expression, f"{label}.expr")

      return record

   def prediction(self):
      block = self.record.get("prediction")

      if block is None:
         return []

      refuse_unknown_fields(block, PREDICTION_FIELDS, "prediction")
      label = block.get("id") or "prediction"
      refuse_unknown_fields(block["stem"], PREDICTION_STEM_FIELDS, f"{label}.stem")
      is_short_answer = block["format"] == "short_answer"
      has_key = "key" in block
      has_options = "options" in block

      if has_key and not is_short_answer:
         raise TranscriptionError(f"{label}.key belongs to a short_answer prediction, and this one is {block['format']}")

      if has_options and is_short_answer:
         raise TranscriptionError(f"{label}.options belong to an mcq prediction, and this one is short_answer")

      section = {
         "id": self.next_id(),
         "type": plan.PREDICTION,
         "bands": list(BOTH_BANDS),
         "skills": list(self.skills),
         "sources": list(block.get("sources") or [self.record["target_id"]]),
         "evidence_tag": "inferred",
         "stem": dict(block["stem"]),
         "format": block["format"],
      }

      if has_options:
         section["options"] = [
            self.prediction_option(option, f"{label}.options[{index}]")
            for index, option in enumerate(block["options"])
         ]

      if is_short_answer:
         section["answer_key"] = answer_of(block["key"], f"{label}.key")

      section["resolution"] = {"text": block["resolution"]}
      section["delivery"] = self.prediction_delivery(label)
      self.ids[label] = section["id"]

      return [section]

   def contrast_of(self, contrast, label):
      refuse_unknown_fields(contrast, CONTRAST_FIELDS, label)
      refuse_unknown_fields(contrast["this"], CONTRAST_THIS_FIELDS, f"{label}.this")
      refuse_unknown_fields(contrast["not_this"], CONTRAST_NOT_THIS_FIELDS, f"{label}.not_this")

      return {
         "this": {"text": contrast["this"]["text"], "archetype_id": contrast["this"]["archetype_id"]},
         "not_this": {"text": contrast["not_this"]["text"], "why_not": contrast["not_this"]["why_not"]},
         "feature": contrast["feature"],
      }

   def orientation(self):
      block = self.record.get("orientation")

      if not block:
         return []

      section = {
         "id": self.next_id(),
         "type": plan.ORIENTATION,
         "bands": list(BOTH_BANDS),
         "skills": list(self.skills),
         "sources": list(block.get("sources") or [self.record["target_id"]]),
         "evidence_tag": "inferred",
         "text": block["text"],
         "delivery": self.delivery_of("orientation"),
      }
      self.ids["orientation"] = section["id"]

      return [section]

   def key_ideas(self):
      sections = []

      for block in self.record.get("key_ideas") or []:
         is_core = block.get("depth") == "core"
         section = {
            "id": self.next_id(),
            "type": plan.KEY_IDEAS,
            "bands": list(BOTH_BANDS) if is_core else ["low"],
            "skills": self.skills_of_ek(block["ek_id"]),
            "sources": list(block.get("sources") or [block["ek_id"]]),
            "evidence_tag": "verified" if block.get("quote") else "inferred",
            "ek_id": block["ek_id"],
            "depth": block["depth"],
            "text": block["text"],
         }

         if block.get("notation"):
            section["notation"] = block["notation"]

         if block.get("quote"):
            section["quote"] = {"text": block["quote"]["text"], "source": block["quote"]["source"]}

         section["delivery"] = self.delivery_of(block["id"])
         self.ids[block["id"]] = section["id"]
         sections.append(section)

      return sections

   def strategies(self):
      sections = []

      for block in self.record.get("strategy") or []:
         section = {
            "id": self.next_id(),
            "type": plan.STRATEGY,
            "bands": list(BOTH_BANDS),
            "skills": self.skills_of_archetype(block["archetype_id"]),
            "sources": list(block.get("sources") or [block["archetype_id"]]),
            "evidence_tag": block.get("evidence_tag") or "inferred",
            "archetype_id": block["archetype_id"],
         }

         for key in ("cue", "method", "rival", "separating_feature"):
            section[key] = block[key]

         if "contrast" in block:
            section["contrast"] = self.contrast_of(block["contrast"], f"{block['id']}.contrast")

         self.ids[block["id"]] = section["id"]
         sections.append(section)

      return sections

   def example_step(self, step, label):
      record = {"cue": step["cue"], "why": step["why"]}
      has_value = step.get("expr") is not None

      if has_value:
         record["expression"] = mathjson_of(step["expr"], f"{label}.expr")

      if step.get("point_type_id"):
         record["point_type_id"] = step["point_type_id"]

      if has_value:
         record.update(relation_fields(step))

      return record

   def worked_examples(self):
      sections = []

      for example in self.record.get("worked_examples") or []:
         label = example["id"]
         steps = [self.example_step(step, f"{label}.steps[{index}]") for index, step in enumerate(example["steps"])]
         section = {
            "id": self.next_id(),
            "type": plan.WORKED_EXAMPLE,
            "bands": list(example.get("bands") or BOTH_BANDS),
            "skills": self.skills_of_archetype(example["archetype_id"]),
            "sources": [example["archetype_id"]],
            "evidence_tag": "inferred",
            "archetype_id": example["archetype_id"],
            "parameter_draw": example["parameter_draw"],
            "problem": example["problem"],
            "calculator_status": example["calculator_status"],
            "steps": steps,
            "answer": answer_of(example["answer"], f"{label}.answer"),
         }

         if "fade_from" in example:
            section["fade_from"] = self.fade_from_of(example["fade_from"], label)

         section["delivery"] = self.delivery_of(label)
         self.ids[label] = section["id"]
         sections.append((example, section))

      return sections

   def fade_from_of(self, value, label):
      is_step_index = isinstance(value, int) and not isinstance(value, bool)

      if not is_step_index:
         raise TranscriptionError(f"{label}.fade_from: {value!r} is not a step number")

      return value

   def fix_prompt_of(self, block, label):
      has_fix_prompt = "fix_prompt" in block
      is_concept = self.kind == "concept"

      if not has_fix_prompt and is_concept:
         raise TranscriptionError(f"{label}.fix_prompt is missing, and every error block of a concept lesson carries one")

      if not has_fix_prompt:
         return None

      value = block["fix_prompt"]

      if not isinstance(value, bool):
         raise TranscriptionError(f"{label}.fix_prompt: {value!r} is not true or false")

      return value

   def reader_scores(self, examples):
      listed = {entry.get("example_id"): entry for entry in self.record.get("what_a_reader_scores") or []}
      sections = []

      for example, section in examples:
         entry = listed.get(example["id"])

         # An entry with no lines states that nothing on the example is scored; the record's
         # schema holds a scoring section only when it has a line, so none is written.
         if entry is None or not entry.get("lines"):
            continue

         lines = []

         for line in entry.get("lines") or []:
            if not isinstance(line, dict):
               raise TranscriptionError(f"what_a_reader_scores {example['id']} line {line!r} names no point_type_id")

            lines.append({"point_type_id": line["point_type_id"], "text": line["text"]})

         sections.append({
            "id": self.next_id(),
            "type": plan.READER_SCORES,
            "bands": list(section["bands"]),
            "skills": list(section["skills"]),
            "sources": list(entry.get("point_type_ids") or [example["archetype_id"]]),
            "evidence_tag": "verified",
            "example_id": section["id"],
            "lines": lines,
         })

      return sections

   def common_errors(self):
      sections = []

      for block in self.record.get("common_errors") or []:
         error_id = block["error_id"]
         label = f"err-{error_id}"
         section = {
            "id": f"{self.lesson_id}#{label}",
            "type": plan.COMMON_ERROR,
            "bands": list(BOTH_BANDS),
            "skills": self.skills_of_error(error_id),
            "sources": list(block.get("sources") or [error_id]),
            "evidence_tag": self.evidence_of(error_id),
            "error_id": error_id,
            "observed_behavior": block["observed_behavior"],
            "scoring_consequence": block["scoring_consequence"],
            "wrong_step": {
               "text": block["wrong_step"]["text"],
               "expression": mathjson_of(block["wrong_step"]["expr"], f"{label}.wrong_step.expr"),
            },
            "right_step": {
               "text": block["right_step"]["text"],
               "expression": mathjson_of(block["right_step"]["expr"], f"{label}.right_step.expr"),
            },
            "relation": block["relation"],
         }
         fix_prompt = self.fix_prompt_of(block, label)

         if fix_prompt is not None:
            section["fix_prompt"] = fix_prompt

         reason = block.get("possible_reason")

         if reason:
            section["possible_reason"] = {"misconception_id": reason["misconception_id"], "text": reason["text"]}

         section["delivery"] = self.delivery_of(label)
         self.ids[label] = section["id"]
         sections.append(section)

      return sections

   def representations(self):
      block = self.record.get("representations")

      if not block:
         return []

      section = {
         "id": self.next_id(),
         "type": plan.REPRESENTATIONS,
         "bands": ["low"],
         "skills": list(self.skills),
         "sources": list(block.get("sources") or [self.record["target_id"]]),
         "evidence_tag": "inferred",
         "text": block["text"],
      }

      if block.get("figure"):
         section["figure"] = block["figure"]

      section["delivery"] = self.delivery_of("representations")
      self.ids["representations"] = section["id"]

      return [section]

   def bridges(self):
      sections = []

      for block in self.record.get("prerequisite_bridges") or []:
         prq_id = block["prq_id"]
         section = {
            "id": f"{self.lesson_id}#prq-{prq_id}",
            "type": plan.PREREQUISITE_BRIDGE,
            "bands": list(BOTH_BANDS),
            "skills": self.skills_of_prerequisite(prq_id),
            "sources": [prq_id],
            "evidence_tag": self.evidence_of(prq_id),
            "prerequisite_id": prq_id,
            "text": block["text"],
         }
         self.ids[f"prq-{prq_id}"] = section["id"]
         sections.append(section)

      return sections

   def check_step(self, step, index, label):
      record = {"step": index, "text": step["text"]}
      has_value = step.get("expr") is not None

      if has_value:
         record["mathjson"] = mathjson_of(step["expr"], f"{label}.expr")

      if step.get("point_type_id"):
         record["point_type_id"] = step["point_type_id"]

      if has_value:
         record.update(relation_fields(step))

      return record

   def option(self, option, is_statement, label):
      record = {"id": option["id"], "is_key": option["is_key"], "error_path": option.get("error_path")}
      expression = option.get("expr")

      if expression is not None and is_statement:
         record["value"] = str(expression)
      elif expression is not None:
         record["value"] = mathjson_of(expression, f"{label}.expr")

      for key in ("label", "derivation"):
         if option.get(key):
            record[key] = option[key]

      return record

   def representation_of(self, archetype_id):
      listed = self.archetype(archetype_id).get("representations") or []

      return listed[0] if listed else DEFAULT_REPRESENTATION

   def checks(self):
      checks = []

      for position, check in enumerate(self.record.get("checks") or [], 1):
         label = check.get("id") or f"chk-{position}"
         is_statement = (check.get("key") or {}).get("form") == "statement"
         record = {
            "id": f"{self.lesson_id}#chk-{position}",
            "check_kind": check["check_kind"],
            "bands": list(check.get("bands") or BOTH_BANDS),
            "format": check["format"],
            "archetype_id": check["archetype_id"],
            "parameter_draw": check["parameter_draw"],
         }
         completes = check.get("completes")

         if completes:
            if completes not in self.ids:
               raise TranscriptionError(f"{label}.completes names {completes}, which is not a worked example")

            record["completes"] = self.ids[completes]

         record["stem"] = check["stem"]
         record["answer_key"] = answer_of(check["key"], f"{label}.key")
         record["worked_solution"] = [
            self.check_step(step, index, f"{label}.steps[{index - 1}]")
            for index, step in enumerate(check.get("steps") or [], 1)
         ]

         if check.get("options"):
            record["options"] = [
               self.option(option, is_statement, f"{label}.options[{index}]")
               for index, option in enumerate(check["options"])
            ]

         record["calculator_status"] = check["calculator_status"]
         record["representation"] = self.representation_of(check["archetype_id"])
         record["skills"] = list(check.get("skills") or self.skills)
         checks.append(record)

      return checks

   def decision(self):
      block = self.record.get("decision")

      if not block:
         return None

      stems = []

      for stem in block.get("stems") or []:
         stems.append({
            "id": f"{self.lesson_id}#{stem['id']}",
            "archetype_id": stem["archetype_id"],
            "method": stem["method"],
            "parameter_draw": stem["parameter_draw"],
            "text": stem["text"],
         })

      delivery = self.delivery_of("stems")
      has_spec = isinstance(delivery.get("spec"), dict)

      # Contract, Record shape: the decision record's stems block carries delivery mode contrast
      # with spec, fallback and keyboard; the design fixes the mode but gives no spec, so the
      # record builds the stems spec from the design's own stems and selecting feature.
      if not has_spec:
         delivery["spec"] = {
            "kind": "stems",
            "stems": [stem["id"] for stem in stems],
            "selecting_feature": block["selecting_feature"],
         }

      delivery.setdefault("fallback", STEMS_FALLBACK)
      delivery.setdefault("keyboard", STEMS_KEYBOARD)

      return {
         "unit": f"BC-UNIT-{self.record['unit']}",
         "skills": list(block["skills"]),
         "selecting_feature": block["selecting_feature"],
         "stems": stems,
         "delivery": delivery,
      }

   def refresher(self):
      pointers = []

      for block_id in self.record.get("refresher") or []:
         if block_id not in self.ids:
            raise TranscriptionError(f"refresher names {block_id}, which is not a transcribed block")

         pointers.append(self.ids[block_id])

      return pointers

   def source_digest(self):
      if self.bundle is not None:
         return self.bundle["source_digest"]

      # A decision or prerequisite lesson has no single concept bundle; its digest hashes the
      # digests of the bundles its skills are taught in, so it moves when any of them moves.
      concepts = sorted({
         (self.snapshot.skills.get(skill_id) or {}).get("concept")
         for skill_id in self.skills
         if (self.snapshot.skills.get(skill_id) or {}).get("concept") in self.snapshot.concepts
      })
      digests = [authoring_bundle(concept_id, self.snapshot)["source_digest"] for concept_id in concepts]

      return hashlib.sha256(json.dumps(digests).encode()).hexdigest()

   def design_path(self):
      if self.recorded_as is not None:
         return self.recorded_as

      path = self.design.path.resolve()

      try:
         return str(path.relative_to(ROOT))
      except ValueError:
         return str(self.design.path)

   def transcribe(self):
      sections = self.prediction() + self.orientation() + self.key_ideas() + self.strategies()
      examples = self.worked_examples()
      sections += [section for _, section in examples]
      sections += self.reader_scores(examples)
      sections += self.common_errors()
      sections += self.representations()
      sections += self.bridges()
      checks = self.checks()
      decision = self.decision()
      lesson = {
         "id": self.lesson_id,
         "version": 1,
         "kind": self.kind,
         "target_id": self.record["target_id"],
         "status": "draft",
         "snapshot_digest": self.snapshot.digest,
         "source_digest": self.source_digest(),
         "read_minutes": {"full": 1, "brief": 1},
         "word_count": {"full": 1, "brief": 1},
         "sections": sections,
         "checks": checks,
         "refresher": self.refresher(),
      }

      if "no_figure_reason" in self.record:
         lesson["no_figure_reason"] = self.record["no_figure_reason"]

      if decision is not None:
         lesson["decision"] = decision

      lesson["provenance"] = {
         "author": AUTHOR,
         "prompt_version": PROMPT_VERSION,
         "design_path": self.design_path(),
         "signed_off_by": None,
         "signed_off_at": None,
         "not_human": True,
      }
      self.fill_counts(lesson)

      return lesson

   def fill_counts(self, lesson):
      stated = self.record.get("read_minutes") or {}
      bands = {"full": "low", "brief": "mid"}

      for form, band in bands.items():
         words = plan.band_words(lesson, band)
         floor = plan.estimate_minutes(words)
         authored = stated.get(form)
         has_authored = isinstance(authored, (int, float)) and authored + 1e-9 >= words / constants.WORDS_PER_MINUTE
         lesson["word_count"][form] = words
         lesson["read_minutes"][form] = authored if has_authored else floor


def transcribe(design_path, snapshot=None, recorded_as=None):
   """recorded_as is the docs/lessons path the provenance names when the design read is a copy
   kept elsewhere, such as a test fixture standing in for a library design."""
   path = Path(design_path)
   design = Design(path, path.read_text())

   if design.record is None:
      raise TranscriptionError(f"{path}: {design.record_error or 'no machine record'}")

   if snapshot is None:
      snapshot = load_snapshot(DATA_ROOT)

   return Transcriber(design, snapshot, recorded_as).transcribe()


def render(lesson):
   return json.dumps(lesson, indent=1, ensure_ascii=False) + "\n"


def main(argv):
   arguments = argv[1:]
   takes_one_or_two = len(arguments) in (1, 2)

   if not takes_one_or_two:
      print("usage: python3 tools/lesson_transcribe.py <design.md> [<out.json>]", file=sys.stderr)

      return 1

   try:
      lesson = transcribe(arguments[0])
   except TranscriptionError as error:
      print(f"refusing: {error}", file=sys.stderr)

      return 1
   except KeyError as error:
      print(f"refusing: the design lacks the field {error}", file=sys.stderr)

      return 1

   has_output = len(arguments) == 2
   output = Path(arguments[1]) if has_output else CONTENT_LESSONS / f"{lesson['id']}.json"
   output.write_text(render(lesson))
   print(f"wrote {output}: {len(lesson['sections'])} sections, {len(lesson['checks'])} checks, words {lesson['word_count']}")

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv))
