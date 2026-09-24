"""D13 item (c): every active archetype carries a structured parameter spec in the library, the
spec validates against the registry schema and against its own archetype, and the template that
generates from it proposes exactly that spec, so the two cannot drift apart."""
import json

from app.generation.spec import validate_spec
from app.generation.template import BROKEN_TEMPLATES, library, template_modules


def test_every_active_archetype_carries_a_valid_parameter_spec():
   missing = []
   invalid = {}

   for archetype_id, archetype in sorted(library().archetypes.items()):
      spec = archetype.get("parameter_spec")

      if spec is None:
         missing.append(archetype_id)
         continue

      problems = validate_spec(spec, archetype)

      if problems:
         invalid[archetype_id] = problems

   assert missing == [], f"{len(missing)} active archetypes carry no parameter_spec"
   assert invalid == {}


def test_every_active_archetype_has_a_template_proposing_its_registered_spec():
   modules = template_modules()
   archetypes = library().archetypes
   without_template = sorted(set(archetypes) - set(modules))
   drifted = [
      archetype_id
      for archetype_id, module in sorted(modules.items())
      if json.dumps(module.SPEC, sort_keys=True) != json.dumps(archetypes[archetype_id].get("parameter_spec"), sort_keys=True)
   ]

   assert BROKEN_TEMPLATES == {}
   assert without_template == []
   assert drifted == []


def test_the_validator_refuses_a_spec_the_generator_could_not_draw_from():
   from app.generation.template import template_module
   import copy

   module = template_module("BC-QA-06004")
   archetype = library().archetypes["BC-QA-06004"]

   assert validate_spec(module.SPEC, archetype) == []

   unguarded = copy.deepcopy(module.SPEC)
   unguarded["calculator_guard"] = None
   untyped = copy.deepcopy(module.SPEC)
   untyped["parameters"][0]["type"] = "free text"
   foreign_dial = copy.deepcopy(module.SPEC)
   foreign_dial["dial_bindings"][0]["difficulty_factor_id"] = "BC-DF-17"
   unbound = copy.deepcopy(module.SPEC)
   unbound["dial_bindings"] = unbound["dial_bindings"][1:]
   figureless = copy.deepcopy(module.SPEC)
   figureless["representation_bindings"][0]["figure_kind"] = None

   assert any("calculator_guard" in problem for problem in validate_spec(unguarded, archetype))
   assert any("free text" in problem for problem in validate_spec(untyped, archetype))
   assert any("BC-DF-17" in problem for problem in validate_spec(foreign_dial, archetype))
   assert any("no dial binding" in problem for problem in validate_spec(unbound, archetype))
   assert any("needs a figure_kind" in problem for problem in validate_spec(figureless, archetype))
