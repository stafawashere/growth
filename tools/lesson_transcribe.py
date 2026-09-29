"""Transcribe a lesson design's machine record into a lesson record (docs/lessons/BUILD-PLAN.md,
The design to record path, step 2).

The record is computed from the design's machine record and the authoring bundle alone, so the
same design and snapshot always give the same bytes: no clock, no model, no hand edits. Texts are
copied verbatim; every SymPy string becomes MathJSON through app/items/mathjson.from_sympy; the
delivery entries become each block's delivery object; word_count is app.lessons.plan.band_words,
which is what the app serves (worker D decision 10), and read_minutes is the design's value or the
words at constants.WORDS_PER_MINUTE, whichever is larger.

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
PROMPT_VERSION = "generator/lesson_v1"
BOTH_BANDS = ["low", "mid"]
RELATION_FIELDS = ("relation", "subs", "approx", "variable", "point", "dir")
STEMS_FALLBACK = "the stems listed one under the other, the selecting feature named under each"
STEMS_KEYBOARD = "Tab moves between the stems"
DEFAULT_REPRESENTATION = "BC-REP-01"


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


def relation_fields(step):
   return {key: step[key] for key in RELATION_FIELDS if key in step}


class Transcriber:
   def __init__(self, design, snapshot):
      self.design = design
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
            "delivery": self.delivery_of(label),
         }
         self.ids[label] = section["id"]
         sections.append((example, section))

      return sections

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
      path = self.design.path.resolve()

      try:
         return str(path.relative_to(ROOT))
      except ValueError:
         return str(self.design.path)

   def transcribe(self):
      sections = self.orientation() + self.key_ideas() + self.strategies()
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


def transcribe(design_path, snapshot=None):
   path = Path(design_path)
   design = Design(path, path.read_text())

   if design.record is None:
      raise TranscriptionError(f"{path}: {design.record_error or 'no machine record'}")

   if snapshot is None:
      snapshot = load_snapshot(DATA_ROOT)

   return Transcriber(design, snapshot).transcribe()


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
