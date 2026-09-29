"""What a lesson author is given, and the scoring lines a lesson restates: docs/plan/15-lessons.md,
Sourcing, authoring and verification, and Methods, the scoring checklist.

authoring_bundle assembles every input the plan names from a ContentSnapshot, the topic slice of
research/units and the cached CED pages, and reader_checks turns BC-PT record fields into the
what_a_reader_scores lines, so the model writes none of them.
"""
import hashlib
import json
import re
from pathlib import Path

from app.lessons import constants

ROOT = Path(__file__).resolve().parents[2]
UNITS_DIR = ROOT / "research" / "units"
CACHE_TEXT_DIR = ROOT / "cache" / "text"

SEVERITY_RANK = {"high": 3, "medium": 2, "low": 1}
PARENT_EDGE_TYPES = ("hard_prerequisite", "supporting")
VOLATILE_KEYS = ("created", "updated")
CED_SOURCE = re.compile(r"^ced:(\d+)$")

NO_NOTATION_NOTE = "No special notation requirement"
NOT_A_VALUE_POINT = "Not a reported-value point"


def topic_number(topic_id):
   """BC-TOP-0208 is topic 2.8 and BC-TOP-0611 is topic 6.11."""
   digits = topic_id.rsplit("-", 1)[1]
   unit_number = int(digits[:2])
   topic_in_unit = int(digits[2:])

   return f"{unit_number}.{topic_in_unit}"


def unit_file(unit_id, units_dir):
   unit_number = unit_id.rsplit("-", 1)[1]
   matches = sorted(Path(units_dir).glob(f"unit-{unit_number}-*.md"))
   has_a_file = len(matches) > 0

   if not has_a_file:
      raise FileNotFoundError(f"no research/units file for {unit_id}")

   return matches[0]


def topic_section(topic_id, unit_id, units_dir):
   """The topic's `## N.M` section with its Official mapping subsection removed, because that
   subsection quotes essential-knowledge statements verbatim and may not be reused."""
   heading = re.compile(rf"^## {re.escape(topic_number(topic_id))} ")
   lines = unit_file(unit_id, units_dir).read_text().splitlines()
   start = next((index for index, line in enumerate(lines) if heading.match(line)), None)
   found_the_topic = start is not None

   if not found_the_topic:
      raise ValueError(f"no section for topic {topic_id} in {unit_id}")

   section = [lines[start]]

   for line in lines[start + 1:]:
      is_next_topic = line.startswith("## ")

      if is_next_topic:
         break

      section.append(line)

   return "\n".join(drop_subsection(section, "### Official mapping")).strip() + "\n"


def drop_subsection(lines, heading):
   kept = []
   is_dropping = False

   for line in lines:
      is_subheading = line.startswith("### ")

      if is_subheading:
         is_dropping = line.strip() == heading

      if not is_dropping:
         kept.append(line)

   return kept


def severity_rank(error, snapshot):
   linked = error.get("possible_misconceptions") or []
   ranks = [
      SEVERITY_RANK.get(snapshot.misconceptions[mis_id].get("severity"), 0)
      for mis_id in linked
      if mis_id in snapshot.misconceptions
   ]

   return max(ranks, default=0)


def concept_errors(skill_ids, snapshot):
   """Active BC-ERR whose skills meet the concept's, ordered by the highest severity of the
   linked BC-MIS and then by id."""
   wanted = set(skill_ids)
   errors = [
      error for error in snapshot.errors.values() if wanted.intersection(error.get("skills") or [])
   ]

   return sorted(errors, key=lambda error: (-severity_rank(error, snapshot), error["id"]))


def concept_archetypes(skill_ids, snapshot):
   """Active archetypes that load a skill of the concept, primary skill in the concept first."""
   wanted = set(skill_ids)
   loading = [
      archetype
      for archetype in snapshot.archetypes.values()
      if wanted.intersection(archetype.get("skills") or [])
   ]

   def order(archetype):
      is_primary = archetype["skills"][0] in wanted

      return (0 if is_primary else 1, archetype["id"])

   return sorted(loading, key=order)


def concept_prerequisites(skill_ids, snapshot):
   wanted = set(skill_ids)
   prerequisite_ids = {
      edge["from"]
      for edge in snapshot.edges
      if edge["from"].startswith("BC-PRQ-")
      and edge["to"] in wanted
      and edge["type"] in PARENT_EDGE_TYPES
   }

   return [snapshot.prerequisites[prq_id] for prq_id in sorted(prerequisite_ids) if prq_id in snapshot.prerequisites]


def cited_pages(records):
   pages = set()

   for record in records:
      for source in record.get("sources") or []:
         is_ced_page = CED_SOURCE.match(source) is not None

         if is_ced_page:
            pages.add(source)

   return sorted(pages, key=lambda source: int(source.split(":")[1]))


def ced_page_texts(sources, cache_dir):
   texts = {}

   for source in sources:
      page_number = int(source.split(":")[1])
      page_file = Path(cache_dir) / "ced" / f"page-{page_number:03d}.txt"
      has_page = page_file.exists()

      if has_page:
         texts[source] = page_file.read_text()

   return texts


def stable_record(record):
   return {key: value for key, value in record.items() if key not in VOLATILE_KEYS}


def digest_of(parts):
   encoded = json.dumps(parts, sort_keys=True, ensure_ascii=True).encode()

   return hashlib.sha256(encoded).hexdigest()


def authoring_bundle(concept_id, snapshot, units_dir=UNITS_DIR, cache_dir=CACHE_TEXT_DIR):
   concept = snapshot.concepts[concept_id]
   skills = [snapshot.skills[skill_id] for skill_id in concept["skills"] if skill_id in snapshot.skills]
   skill_ids = [skill["id"] for skill in skills]

   errors = concept_errors(skill_ids, snapshot)
   misconception_ids = sorted(
      {mis_id for error in errors for mis_id in error.get("possible_misconceptions") or []}
      | set(concept.get("misconceptions") or [])
   )
   misconceptions = [snapshot.misconceptions[mis_id] for mis_id in misconception_ids if mis_id in snapshot.misconceptions]
   signals = [signal for signal in snapshot.signals.values() if signal.get("skill") in skill_ids]
   signals = sorted(signals, key=lambda signal: signal["id"])
   archetypes = concept_archetypes(skill_ids, snapshot)
   point_type_ids = sorted({pt_id for archetype in archetypes for pt_id in archetype.get("point_types") or []})
   point_types = [snapshot.scoring_points[pt_id] for pt_id in point_type_ids if pt_id in snapshot.scoring_points]
   prerequisites = concept_prerequisites(skill_ids, snapshot)

   topic_sections = {
      topic_id: topic_section(topic_id, concept["unit"], units_dir)
      for topic_id in concept.get("topics") or []
   }
   ced_sources = cited_pages([concept] + skills + errors)

   library_records = {
      "concept": stable_record(concept),
      "skills": [stable_record(skill) for skill in skills],
      "errors": [stable_record(error) for error in errors],
      "misconceptions": [stable_record(record) for record in misconceptions],
      "signals": [stable_record(signal) for signal in signals],
      "archetypes": [stable_record(archetype) for archetype in archetypes],
      "point_types": [stable_record(record) for record in point_types],
      "prerequisites": [stable_record(record) for record in prerequisites],
   }

   return {
      "concept_id": concept_id,
      **library_records,
      "topic_sections": topic_sections,
      "ced_sources": ced_sources,
      "ced_pages": ced_page_texts(ced_sources, cache_dir),
      "source_digest": digest_of({**library_records, "topic_sections": topic_sections}),
   }


def reader_line(record):
   name = record["name"]
   earns = record["earns"]
   does_not_earn = record["does_not_earn"]
   line = f"{name}. Earned by: {earns} Not earned by: {does_not_earn}"

   notation = record.get("notation_requirements") or ""
   states_notation = notation != "" and not notation.startswith(NO_NOTATION_NOTE)

   if states_notation:
      line += f" Notation: {notation}"

   precision = record.get("precision_rules") or ""
   states_precision = precision != "" and not precision.startswith(NOT_A_VALUE_POINT)

   if states_precision:
      line += f" Precision: {precision}"

   needs_units = record.get("units_required") == "yes"

   if needs_units:
      line += " Units are required on the answer."

   needs_hypotheses = record.get("hypotheses_required") == "yes"

   if needs_hypotheses:
      line += " The hypotheses of the theorem must be stated."

   return line


def reader_checks(point_type_ids, snapshot):
   """One line per BC-PT id, in the order given, each a pure function of that record's fields."""
   lines = []
   seen = set()

   for point_type_id in point_type_ids:
      already_listed = point_type_id in seen

      if already_listed:
         continue

      seen.add(point_type_id)
      record = snapshot.scoring_points.get(point_type_id)
      is_unknown = record is None

      if is_unknown:
         raise KeyError(f"{point_type_id} is not an active BC-PT record in the snapshot")

      lines.append({"point_type_id": point_type_id, "text": reader_line(record)})

   return lines[:constants.READER_CHECK_LINES_MAX]
