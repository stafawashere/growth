"""The structured parameter spec of an archetype (docs/plan/04-item-generation.md, "The missing
parameter spec"): validation against the registry schema, seeded draws, derived values and the
size of the draw space.

The backend draws, never a model. A draw is reproducible from its seed string, which is what an
item's provenance records.
"""
import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path

import sympy
from jsonschema import Draft202012Validator

from app.generation.expressions import SpecExpressionError, evaluate

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas" / "archetypes.schema.json"

MAX_DRAW_ATTEMPTS = 400
DRAW_SPACE_SAMPLE = 2000
CALCULATOR_GUARDED = ("no_calculator", "either")
FIGURE_REPRESENTATIONS = frozenset({"BC-REP-02", "BC-REP-03", "BC-REP-07", "BC-REP-08"})


class DrawExhausted(RuntimeError):
   pass


@lru_cache(maxsize=1)
def spec_validator():
   schema = json.loads(SCHEMA_PATH.read_text())
   spec_schema = dict(schema["$defs"]["parameter_spec"])
   spec_schema["$defs"] = schema["$defs"]

   return Draft202012Validator(spec_schema)


def schema_problems(spec):
   return [
      f"{'/'.join(str(part) for part in error.path)}: {error.message[:200]}"
      for error in spec_validator().iter_errors(spec)
   ]


def validate_spec(spec, archetype):
   """Every problem that makes the spec unusable for this archetype, schema first."""
   problems = schema_problems(spec)

   if problems:
      return problems

   names = [parameter["name"] for parameter in spec["parameters"]]
   derived_names = [entry["name"] for entry in spec["derived"]]
   all_names = names + derived_names
   repeated = sorted({name for name in all_names if all_names.count(name) > 1})

   if repeated:
      problems.append(f"names declared twice: {repeated}")

   needs_guard = archetype["calculator_status"] in CALCULATOR_GUARDED
   has_guard = bool(spec["calculator_guard"])

   if needs_guard and not has_guard:
      problems.append(f"calculator_guard is required on a {archetype['calculator_status']} archetype")

   allowed_factors = set(archetype.get("difficulty_factors") or [])

   for binding in spec["dial_bindings"]:
      binds_unknown_parameter = binding["parameter"] not in names
      moves_foreign_dial = binding["difficulty_factor_id"] not in allowed_factors

      if binds_unknown_parameter:
         problems.append(f"dial binding names unknown parameter {binding['parameter']!r}")

      if moves_foreign_dial:
         problems.append(f"{binding['difficulty_factor_id']} is not in the archetype's difficulty_factors")

   difficulty_parameters = [p["name"] for p in spec["parameters"] if p["role"] == "difficulty"]
   bound = {binding["parameter"] for binding in spec["dial_bindings"]}
   unbound = [name for name in difficulty_parameters if name not in bound]

   if unbound:
      problems.append(f"difficulty parameters with no dial binding: {unbound}")

   allowed_representations = set(archetype.get("representations") or [])

   for binding in spec["representation_bindings"]:
      representation = binding["representation"]
      is_foreign = representation not in allowed_representations
      needs_figure = representation in FIGURE_REPRESENTATIONS
      lacks_figure = needs_figure and binding["figure_kind"] is None
      unknown_requirements = [name for name in binding["requires"] if name not in all_names]

      if is_foreign:
         problems.append(f"{representation} is not in the archetype's representations")

      if lacks_figure:
         problems.append(f"{representation} needs a figure_kind")

      if unknown_requirements:
         problems.append(f"{representation} requires unknown names {unknown_requirements}")

   return problems


def _as_value(parameter_type, raw):
   if parameter_type in ("label", "unit", "function_form"):
      return raw

   if parameter_type == "symbol":
      return sympy.Symbol(raw)

   if parameter_type == "interval":
      return [sympy.nsimplify(str(end)) for end in raw]

   if isinstance(raw, str):
      return sympy.Rational(raw)

   if isinstance(raw, int):
      return sympy.Integer(raw)

   return sympy.Rational(str(raw))


def domain_values(parameter):
   domain = parameter["domain"]
   parameter_type = parameter["type"]

   if "values" in domain:
      return [_as_value(parameter_type, raw) for raw in domain["values"]]

   low = sympy.Rational(str(domain["min"]))
   high = sympy.Rational(str(domain["max"]))
   step = sympy.Rational(str(domain["step"]))
   excluded = {sympy.Rational(str(value)) for value in domain.get("exclude") or []}
   values = []
   current = low

   while current <= high:
      if current not in excluded:
         values.append(current)

      current += step

   return values


def _draw_parameter(parameter, rng):
   values = domain_values(parameter)
   count = parameter.get("count")

   if count is None:
      return rng.choice(values)

   is_distinct = parameter.get("distinct", False)

   if is_distinct:
      chosen = rng.sample(values, count)
   else:
      chosen = [rng.choice(values) for _ in range(count)]

   order = parameter.get("order")

   if order == "increasing":
      chosen = sorted(chosen)

   if order == "decreasing":
      chosen = sorted(chosen, reverse=True)

   return chosen


def with_derived(spec, draw):
   names = dict(draw)

   for entry in spec["derived"]:
      names[entry["name"]] = evaluate(entry["expression"], names)

   return names


def constraints_hold(spec, names):
   for constraint in spec["constraints"]:
      try:
         holds = bool(evaluate(constraint, names))
      except (SpecExpressionError, ZeroDivisionError, TypeError, IndexError, KeyError):
         return False

      if not holds:
         return False

   return True


def seed_for(archetype_id, spec_version, index):
   return f"{archetype_id}:spec-{spec_version}:draw-{index}"


def rng_for(seed):
   digest = hashlib.sha256(seed.encode()).hexdigest()

   return random.Random(int(digest[:16], 16))


def draw(spec, rng):
   """One draw that satisfies every constraint, with its derived values, or DrawExhausted."""
   for _ in range(MAX_DRAW_ATTEMPTS):
      parameters = {parameter["name"]: _draw_parameter(parameter, rng) for parameter in spec["parameters"]}

      try:
         names = with_derived(spec, parameters)
      except (SpecExpressionError, ZeroDivisionError, TypeError, ValueError, IndexError, KeyError):
         continue

      if constraints_hold(spec, names):
         return parameters, names

   raise DrawExhausted(f"no draw satisfied the constraints in {MAX_DRAW_ATTEMPTS} attempts")


def draw_with_seed(spec, seed):
   return draw(spec, rng_for(seed))


def draw_key(parameters):
   """A hashable identity for a draw, so two equal draws count once."""
   return json.dumps(serialise(parameters), sort_keys=True)


def serialise(value):
   if isinstance(value, dict):
      return {name: serialise(entry) for name, entry in value.items()}

   if isinstance(value, (list, tuple)):
      return [serialise(entry) for entry in value]

   if isinstance(value, (str, bool)) or value is None:
      return value

   return str(value)


def _domain_size(parameter):
   size = len(domain_values(parameter))
   count = parameter.get("count")

   if count is None:
      return size

   is_distinct = parameter.get("distinct", False)
   is_ordered = parameter.get("order") is not None

   if is_distinct and is_ordered:
      return sympy.binomial(size, count)

   if is_distinct:
      return sympy.ff(size, count)

   return size ** count


def draw_space(spec, rng=None):
   """The number of constraint-satisfying parameter tuples, estimated as the product of the
   domain sizes times the share of uniform tuples that satisfy the constraints."""
   rng = rng or random.Random(20260924)
   product = 1

   for parameter in spec["parameters"]:
      product *= int(_domain_size(parameter))

   accepted = 0

   for _ in range(DRAW_SPACE_SAMPLE):
      parameters = {parameter["name"]: _draw_parameter(parameter, rng) for parameter in spec["parameters"]}

      try:
         names = with_derived(spec, parameters)
      except (SpecExpressionError, ZeroDivisionError, TypeError, ValueError, IndexError, KeyError):
         continue

      if constraints_hold(spec, names):
         accepted += 1

   return int(product * accepted / DRAW_SPACE_SAMPLE)


def realised_settings(spec, parameters):
   """The BC-DF dial settings a draw realises, from the spec's dial bindings."""
   settings = {}

   for binding in spec["dial_bindings"]:
      value = serialise(parameters[binding["parameter"]])
      key = value if isinstance(value, str) else json.dumps(value)
      setting = binding["settings"].get(key)
      is_bound = setting is not None

      if not is_bound:
         continue

      factor = binding["difficulty_factor_id"]
      settings[factor] = _stronger(settings.get(factor), setting)

   return settings


SETTING_ORDER = ("off", "low", "medium", "high")


def _stronger(current, candidate):
   if current is None:
      return candidate

   return max(current, candidate, key=SETTING_ORDER.index)
