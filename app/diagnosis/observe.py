"""The diagnostician role's model call: what the confirmed work shows, checked against the library.

The model sees the question, the points lost, and three candidate lists drawn from the library
for the item's skills: the recorded errors (observed_behavior), the recorded signals
(observation) and the prerequisite-gap descriptions of the skills that lost a point. It answers
with ids from those lists and verbatim evidence. The answer is data: an id outside the lists is
dropped, an evidence quote that is not in the work drops its entry, and a new behaviour is kept
only as a candidate with no id, because minting an id is the library's job (03, "A new error the
library has not seen").
"""
import json
from pathlib import Path

from app.diagnosis.diagnose import CONCEPTUAL, PROCEDURAL, Observation
from app.grading.judge import rendered_work
from app.grading.point import quote_is_verbatim, work_text
from app.providers.base import CacheSettings, Message, ProviderRequest, render_template, split_template
from app.providers.model_routing import model_for

TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "prompts" / "diagnostician" / "error_hypotheses_v1.md"
MAX_OUTPUT_TOKENS = 1500
PROVIDER_OPTIONS = {"thinking": {"type": "disabled"}}
READINGS = (PROCEDURAL, CONCEPTUAL, "unclear")

OBSERVATION_SCHEMA = {
   "type": "object",
   "properties": {
      "observed_errors": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "error_id": {"type": "string"},
               "new_behavior": {"type": "string"},
               "evidence": {"type": "string"},
               "points_lost": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["error_id", "new_behavior", "evidence", "points_lost"],
            "additionalProperties": False,
         },
      },
      "matched_signals": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {"signal_id": {"type": "string"}, "evidence": {"type": "string"}},
            "required": ["signal_id", "evidence"],
            "additionalProperties": False,
         },
      },
      "skill_readings": {
         "type": "array",
         "items": {
            "type": "object",
            "properties": {
               "skill_id": {"type": "string"},
               "reading": {"type": "string", "enum": list(READINGS)},
            },
            "required": ["skill_id", "reading"],
            "additionalProperties": False,
         },
      },
      "gap_descriptions_matched": {"type": "array", "items": {"type": "string"}},
   },
   "required": ["observed_errors", "matched_signals", "skill_readings", "gap_descriptions_matched"],
   "additionalProperties": False,
}


class ObservationFailed(Exception):
   pass


def candidate_errors(record, library):
   item_skills = set(record["skills"])
   listed = {
      error_id
      for skill_id in item_skills
      for error_id in library.skills.get(skill_id, {}).get("common_errors") or []
   }
   linked = {
      error_id
      for error_id, error in library.errors.items()
      if item_skills & set(error.get("skills") or [])
   }

   return sorted((listed | linked) & set(library.errors))


def candidate_signals(record, library):
   item_skills = set(record["skills"])

   return sorted(
      signal_id
      for signal_id, signal in library.signals.items()
      if signal.get("skill") in item_skills or signal.get("archetype") == record["archetype_id"]
   )


def gap_descriptions(skill_ids, library):
   described = {}

   for skill_id in sorted(skill_ids):
      text = (library.skills.get(skill_id, {}).get("adaptive") or {}).get("prerequisite_gap_if")

      if text:
         described[skill_id] = text

   return described


def points_lost_text(record, decisions):
   points = {point["point_id"]: (part, point) for part in record["parts"] for point in part["points"]}
   lines = []

   for decision in decisions:
      if decision.earned != 0:
         continue

      part, point = points[decision.point_id]
      lines.append(f"{decision.point_id} (part {part['id']}, {point['point_type_id']}): {point['criterion']}")

   return "\n".join(lines) if lines else "(none)"


def request_for(record, decisions, work, library, lost_skills):
   errors = candidate_errors(record, library)
   signals = candidate_signals(record, library)
   gaps = gap_descriptions(lost_skills, library)
   text = TEMPLATE_PATH.read_text()
   system, _variables = split_template(text)
   fields = {
      "question_stem": record["stem"]["text"],
      "points_lost": points_lost_text(record, decisions),
      "error_candidates": "\n".join(f"{error_id}: {library.errors[error_id]['observed_behavior']}" for error_id in errors) or "(none)",
      "signal_candidates": "\n".join(f"{signal_id}: {library.signals[signal_id]['observation']}" for signal_id in signals) or "(none)",
      "gap_descriptions": "\n".join(f"{skill_id}: {text}" for skill_id, text in gaps.items()) or "(none)",
      "student_work": rendered_work(work),
   }
   request = ProviderRequest(
      role="diagnostician",
      model=model_for("diagnostician"),
      system=system,
      messages=(Message(role="user", content=render_template(text, fields)),),
      max_output_tokens=MAX_OUTPUT_TOKENS,
      output_schema=OBSERVATION_SCHEMA,
      cache=CacheSettings(prefix_breakpoints=1, ttl="5m"),
      provider_options={key: dict(value) for key, value in PROVIDER_OPTIONS.items()},
   )

   return request, set(errors), set(signals), set(gaps)


def checked_observation(payload, allowed_errors, allowed_signals, allowed_gap_skills, confirmed_text, point_ids):
   observation = Observation()

   for entry in payload.get("observed_errors") or []:
      evidence = str(entry.get("evidence") or "")
      is_verbatim = quote_is_verbatim(evidence, confirmed_text)

      if not is_verbatim:
         continue

      points_lost = [point_id for point_id in entry.get("points_lost") or [] if point_id in point_ids]
      error_id = str(entry.get("error_id") or "").strip()
      is_known = error_id in allowed_errors
      behavior = str(entry.get("new_behavior") or "").strip()

      if is_known and error_id not in observation.error_ids:
         observation.error_ids.append(error_id)
         observation.evidence[error_id] = evidence
         observation.points_lost_by_error[error_id] = points_lost
      elif not error_id and behavior:
         observation.new_behaviors.append({"observed_behavior": behavior, "evidence": evidence, "points_lost": points_lost})

   for entry in payload.get("matched_signals") or []:
      signal_id = str(entry.get("signal_id") or "")
      is_usable = signal_id in allowed_signals and quote_is_verbatim(entry.get("evidence"), confirmed_text)

      if is_usable and signal_id not in observation.signal_ids:
         observation.signal_ids.append(signal_id)

   for entry in payload.get("skill_readings") or []:
      reading = entry.get("reading")

      if reading in READINGS:
         observation.skill_readings[str(entry.get("skill_id"))] = reading

   observation.gap_skills = [skill_id for skill_id in payload.get("gap_descriptions_matched") or [] if skill_id in allowed_gap_skills]

   return observation


def observe(provider, record, decisions, work, library, lost_skills):
   request, errors, signals, gap_skills = request_for(record, decisions, work, library, lost_skills)

   try:
      result = provider.generate(request)
      payload = json.loads(result.text or "")
   except Exception as raised:
      raise ObservationFailed(f"the diagnostician could not be read: {type(raised).__name__}") from None

   is_object = isinstance(payload, dict)

   if not is_object:
      raise ObservationFailed("the diagnostician's answer was not an object")

   point_ids = {point["point_id"] for part in record["parts"] for point in part["points"]}

   return checked_observation(payload, errors, signals, gap_skills, work_text(work), point_ids)
