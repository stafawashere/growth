"""Turn one seeded draw of a template into an item record in the shape app/items/ingest.py reads.

docs/plan/13-ai-engineering.md, "Template architecture and the migration": instantiation happens
at build time, into records that go through the same ingest door as every other item. The
template supplies the mathematics; everything else on the record is written here from the
archetype, the spec and the seed, so a template cannot misstate its own provenance.
"""
import math
from datetime import datetime, timezone

import sympy

from app.engine.constants import BETA_PER_FACTOR
from app.generation import spec as spec_module
from app.generation.kit import three_decimals
from app.generation.mathjson_out import from_sympy
from app.generation.template import build, library, spec_for, template_id

OPTION_IDS = ("A", "B", "C", "D")
SETTING_STEPS = {"off": 0, "low": 1, "medium": 2, "high": 3}
MEDIAN_FACTOR_COUNT = 2
GENERATOR_PROMPT_VERSION = "generator/template_v1"
ITEM_PREFIX = "ITM-GEN-"


def item_id(archetype_id, index):
   digits = archetype_id.split("-")[-1]

   return f"{ITEM_PREFIX}{digits}-{index:02d}"


def difficulty_settings(archetype, spec, parameters, calculator_status):
   """The realised dial vector, with 04's two hard rules applied over whatever the draw set."""
   settings = spec_module.realised_settings(spec, parameters)
   is_calculator = calculator_status == "calculator"

   if is_calculator:
      current = settings.get("BC-DF-16", "off")
      settings["BC-DF-16"] = current if SETTING_STEPS[current] >= 1 else "low"
   else:
      settings["BC-DF-07"] = "off"

   return [
      {"difficulty_factor_id": factor, "setting": settings[factor]}
      for factor in sorted(settings)
   ]


def predicted_success(archetype, settings):
   """04, "Mapping a requested success probability to dial settings": the centred prior for an
   archetype carrying this many factors, less 0.35 logits per dial step, on the guessing-corrected
   scale."""
   factor_count = len(archetype.get("difficulty_factors") or [])
   steps = sum(SETTING_STEPS[entry["setting"]] for entry in settings if entry["difficulty_factor_id"] != "BC-DF-07")
   logit = BETA_PER_FACTOR * (factor_count - MEDIAN_FACTOR_COUNT) + BETA_PER_FACTOR * steps

   return round(1 / (1 + math.exp(-logit)), 4)


def _option_value(instance, value):
   is_numeric = instance.key.form == "numeric"

   if is_numeric:
      return from_sympy(three_decimals(value))

   return from_sympy(sympy.sympify(value))


def options_for(instance, rng):
   is_statement = instance.key.form == "statement"
   entries = [{"is_key": True, "error_path": None, "source": instance.key}]
   entries += [
      {"is_key": False, "error_path": distractor.error_path, "source": distractor}
      for distractor in instance.distractors
   ]
   rng.shuffle(entries)
   options = []

   for option_id, entry in zip(OPTION_IDS, entries):
      source = entry["source"]
      option = {"id": option_id, "is_key": entry["is_key"], "error_path": entry["error_path"]}

      if is_statement:
         option["label"] = source.label
      else:
         option["value"] = _option_value(instance, source.value)

      if not entry["is_key"]:
         option["derivation"] = source.derivation
         option["mechanism"] = source.mechanism

      options.append(option)

   return options


def answer_key(instance):
   key = instance.key
   is_statement = key.form == "statement"

   if is_statement:
      return {"form": "statement", "label": key.label}

   value = sympy.sympify(key.value)
   is_numeric = key.form == "numeric"
   mathjson = float(sympy.N(value, 15)) if is_numeric else from_sympy(value)
   record = {"form": key.form, "mathjson": mathjson}

   if is_numeric:
      record["decimals"] = 3

   if key.units:
      record["units"] = key.units

   return record


def worked_solution(instance):
   steps = []

   for number, step in enumerate(instance.steps, start=1):
      entry = {"step": number, "text": step.text}

      if step.value is not None:
         value = sympy.sympify(step.value)
         entry["mathjson"] = float(sympy.N(value, 15)) if value.has(sympy.Float) else from_sympy(value)

      if step.point_type_id:
         entry["point_type_id"] = step.point_type_id

      if step.rule:
         entry["rule_named"] = step.rule

      steps.append(entry)

   return steps


def instantiate(module, index, seed, generated_at=None, model=None, snapshot_digest=None):
   """One item record, or the exception that stopped it."""
   archetype_id = module.ARCHETYPE_ID
   archetype = library().archetypes[archetype_id]
   spec = spec_for(module)
   parameters, names = spec_module.draw_with_seed(spec, seed)
   instance = build(module, names)
   settings = difficulty_settings(archetype, spec, parameters, instance.calculator_status)
   rng = spec_module.rng_for(f"{seed}:options")
   generated_at = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
   has_official_examples = bool(archetype.get("official_examples"))
   variants = archetype.get("variants") or []

   stem = {"text": instance.stem}

   if instance.setup_required:
      stem["setup_required"] = True

   if instance.command_verb:
      stem["command_verb"] = instance.command_verb

   record = {
      "id": item_id(archetype_id, index),
      "archetype_id": archetype_id,
      "variant_id": variants[0] if variants else None,
      "format": "mcq",
      "stem": stem,
      "answer_key": answer_key(instance),
      "worked_solution": worked_solution(instance),
      "options": options_for(instance, rng),
      "calculator_status": instance.calculator_status,
      "representation": instance.representation,
      "difficulty_settings": settings,
      "skills": list(archetype["skills"]),
      "parameter_draw": spec_module.serialise(parameters),
      "predicted_success_probability": predicted_success(archetype, settings),
      "provenance": {
         "template_id": template_id(module),
         "template_version": module.TEMPLATE_VERSION,
         "spec_version": spec["spec_version"],
         "parameter_seed": seed,
         "parameter_draw": spec_module.serialise(parameters),
         "model": model or module.AUTHORED_BY,
         "prompt_version": GENERATOR_PROMPT_VERSION,
         "generated_at": generated_at,
         "content_snapshot": snapshot_digest or library().digest,
         "no_official_examples": not has_official_examples,
      },
   }

   if instance.figure is not None:
      record["figure"] = instance.figure

   return record
