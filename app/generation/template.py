"""Template registry, the template gate and the Monte Carlo family pass.

docs/plan/13-ai-engineering.md, "Verification pipeline ordering", stage 0: the family pass runs
once per archetype per spec version, over 300 seeded draws, and a single failing draw quarantines
the template rather than being filtered out, because filtering hides a spec defect
(docs/plan/04-item-generation.md, "Monte Carlo over the parameter family"). The gate's checks are
the eleven 13 lists under "Radicals and incidentals" plus the calculator boundary (11, P4 scope
item 5), each implemented below and named in the report.
"""
import ast
import importlib
import inspect
import json
import pkgutil
import random
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import sympy

from app.content.loader import load_snapshot
from app.generation import spec as spec_module
from app.generation.expressions import SpecExpressionError, evaluate
from app.generation.kit import Instance
from app.generation.mathjson_out import from_sympy
from app.items.distractor_paths import error_ids_for_skills
from app.items.mathjson import to_sympy

ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data"
TEMPLATE_PACKAGE = "app.generation.templates"

FAMILY_DRAWS = 300
FAMILY_FAILURE_BAR = 0
MIN_DRAW_SPACE = 2000
MIN_DISTINCT_STEMS = 40
MIN_DISTINCT_PROBLEMS = 100
INCIDENTAL_VARIANTS = 16
DISTRACTORS_PER_ITEM = 3
SURFACE_DEFECT_BAR = 0.02
NUMERIC_PROBES = 14
LABEL_LENGTH_RATIO = 1.6
UNIT_COEFFICIENT = re.compile(r"(^|[\s(+\-=])1 (?=[xtys]\b|[xtys]\^|\\left|\\sin|\\cos|\\tan|\\ln|e\^)")
FLOAT_RELATIVE_TOLERANCE = 1e-12
EXACT_RELATIVE_TOLERANCE = 1e-30

KEY_FORMS = ("symbolic", "numeric", "statement")
CALCULATOR_STATUSES = ("no_calculator", "calculator")
NUMERIC_METHODS = frozenset({"nsolve", "nintegrate", "evalf", "N", "Float", "three_decimals", "nroots", "quad"})
FIGURE_WORDS = ("shown", "figure", "the table")
MECHANISMS = (
   "conceptual_confusion", "algebra_slip", "sign_error", "wrong_limits", "reversed_quantities",
   "chain_rule_omitted", "product_rule_omitted", "theorem_condition_ignored", "forgot_constant",
   "compound",
)


@lru_cache(maxsize=1)
def library():
   return load_snapshot(DATA_ROOT)


BROKEN_TEMPLATES = {}


def template_module(archetype_id):
   digits = archetype_id.split("-")[-1]

   return importlib.import_module(f"{TEMPLATE_PACKAGE}.qa_{digits}")


def template_modules():
   """Every template module that imports, keyed by archetype id. One that does not import is
   recorded in BROKEN_TEMPLATES rather than stopping every other template."""
   package = importlib.import_module(TEMPLATE_PACKAGE)
   modules = {}

   for info in pkgutil.iter_modules(package.__path__):
      is_template = info.name.startswith("qa_")

      if not is_template:
         continue

      try:
         module = importlib.import_module(f"{TEMPLATE_PACKAGE}.{info.name}")
      except Exception as failure:
         BROKEN_TEMPLATES[info.name] = f"{type(failure).__name__}: {failure}"
         continue

      modules[module.ARCHETYPE_ID] = module

   return modules


def template_id(module):
   return f"TPL-{module.ARCHETYPE_ID}-v{module.TEMPLATE_VERSION}"


def spec_for(module):
   """The registry's spec when the library holds one, else the template's own proposal."""
   archetype = library().archetypes[module.ARCHETYPE_ID]
   registered = archetype.get("parameter_spec")

   return registered if registered is not None else module.SPEC


def build(module, names):
   instance = module.build(names)
   is_instance = isinstance(instance, Instance)

   if not is_instance:
      raise TypeError(f"{module.__name__}.build returned {type(instance).__name__}, not Instance")

   return instance


@dataclass
class FamilyReport:
   archetype_id: str
   draws: int = 0
   failures: list = field(default_factory=list)
   template_problems: list = field(default_factory=list)
   surface_defects: int = 0
   surface_units: int = 0
   distinct_stems: int = 0
   distinct_problems: int = 0
   draw_space: int = 0
   incidentals_checked: int = 0

   @property
   def surface_rate(self):
      return self.surface_defects / self.surface_units if self.surface_units else 0.0

   @property
   def passed(self):
      within_failure_bar = len(self.failures) <= FAMILY_FAILURE_BAR
      within_surface_bar = self.surface_rate < SURFACE_DEFECT_BAR
      no_template_problem = not self.template_problems

      return within_failure_bar and within_surface_bar and no_template_problem

   def as_dict(self):
      return {
         "archetype_id": self.archetype_id,
         "draws": self.draws,
         "failures": self.failures[:5],
         "failure_count": len(self.failures),
         "template_problems": self.template_problems,
         "surface_rate": round(self.surface_rate, 4),
         "distinct_stems": self.distinct_stems,
         "distinct_problems": self.distinct_problems,
         "draw_space": self.draw_space,
         "incidentals_checked": self.incidentals_checked,
         "passed": self.passed,
      }


def problem_signature(instance):
   """The problem as the bank half of the duplicate gate sees it: two draws with one signature
   are copies of each other (app/generation/dedupe.py problem_text)."""
   from app.generation import dedupe

   problem = dedupe.problem_text({"stem": {"text": instance.stem}, "figure": instance.figure})
   pairs = sorted(dedupe.math_pairs(problem).items())
   numbers = sorted(dedupe.numbers(problem).items())

   return json.dumps([pairs, numbers])


def numeric_methods_used(module):
   """Names of numeric-approximation calls in the template's source, which a no-calculator
   template may not make: its path must be closed-form (rejection rule 8)."""
   tree = ast.parse(inspect.getsource(module))
   used = set()

   for node in ast.walk(tree):
      is_call = isinstance(node, ast.Call)

      if not is_call:
         continue

      function = node.func
      name = function.attr if isinstance(function, ast.Attribute) else getattr(function, "id", None)

      if name in NUMERIC_METHODS:
         used.add(name)

   return sorted(used)


def equivalent(left, right):
   """True, False or None, symbolic first and then numeric at probe points."""
   left = sympy.sympify(left)
   right = sympy.sympify(right)

   try:
      difference = sympy.simplify(left - right)
   except Exception:
      difference = None

   if difference == 0:
      return True

   free = sorted((left.free_symbols | right.free_symbols), key=lambda symbol: symbol.name)
   both_are_numbers = not free

   if both_are_numbers:
      return _numbers_agree(left, right)
   rng = random.Random(7)
   agreed = 0

   for _ in range(NUMERIC_PROBES * 6):
      point = {symbol: sympy.Rational(rng.randint(-170, 170), 17) + sympy.Rational(1, 7) for symbol in free}

      try:
         left_value = complex(sympy.N(left.subs(point), 20))
         right_value = complex(sympy.N(right.subs(point), 20))
      except (TypeError, ValueError, ZeroDivisionError):
         continue

      scale = max(1.0, abs(left_value), abs(right_value))
      differs = abs(left_value - right_value) > 1e-9 * scale

      if differs:
         return False

      agreed += 1

      if agreed >= NUMERIC_PROBES:
         return True

   return None


def _numbers_agree(left, right):
   """Two exact constants agree when their difference is exactly zero, or, when SymPy cannot settle
   it, when it vanishes at 50 digits relative to their size, so two small distinct rationals are
   never called equal. A decimal agrees within twelve significant digits, the precision a stored
   float keeps."""
   carries_decimals = left.has(sympy.Float) or right.has(sympy.Float)
   difference = left - right
   settles = not carries_decimals and difference.is_zero is not None

   if settles:
      return bool(difference.is_zero)

   relative_tolerance = FLOAT_RELATIVE_TOLERANCE if carries_decimals else EXACT_RELATIVE_TOLERANCE

   try:
      gap = abs(complex(sympy.N(difference, 50)))
      scale = max(abs(complex(sympy.N(left, 50))), abs(complex(sympy.N(right, 50))), 1e-300)
   except (TypeError, ValueError):
      return None

   return gap <= relative_tolerance * scale


def _round_trips(value):
   try:
      back = to_sympy(from_sympy(value))
   except Exception:
      return False

   return equivalent(back, value) is True


def latex_problems(text):
   problems = []
   opens = text.count(r"\(")
   closes = text.count(r"\)")

   if opens != closes:
      problems.append("unbalanced math delimiters")

   if text.count("{") != text.count("}"):
      problems.append("unbalanced braces")

   if text.count(r"\left") != text.count(r"\right"):
      problems.append("unbalanced left and right")

   for segment in text.split(r"\(")[1:]:
      math_text = segment.split(r"\)")[0]
      doubled = any(pair in math_text.replace(" ", "") for pair in ("+-", "-+", "--", "++"))

      if doubled:
         problems.append(f"doubled sign in {math_text.strip()[:60]!r}")

      if UNIT_COEFFICIENT.search(math_text):
         problems.append(f"a coefficient of 1 printed in {math_text.strip()[:60]!r}")

   return problems


def _labels_inside(figure):
   domain = figure.get("domain")
   range_ = figure.get("range")
   has_window = domain is not None and range_ is not None

   if not has_window:
      return all(label.get("placement") == "inside" for label in figure.get("labels", []))

   for label in figure.get("labels", []):
      x_value, y_value = label["anchor"]
      inside_x = domain[0] <= x_value <= domain[1]
      inside_y = range_[0] <= y_value <= range_[1]
      is_inside = inside_x and inside_y and label.get("placement") == "inside"

      if not is_inside:
         return False

   return True


def check_instance(instance, archetype, spec, names, error_ids):
   """Every rule a single draw can break, as a list of named failures."""
   failures = []
   key = instance.key
   point_types = set(archetype.get("point_types") or [])
   calculator_status = archetype["calculator_status"]

   if key.form not in KEY_FORMS:
      return [f"key form {key.form!r} is not one of {KEY_FORMS}"]

   if instance.calculator_status not in CALCULATOR_STATUSES:
      failures.append(f"item calculator_status {instance.calculator_status!r}")

   status_matches = calculator_status == "either" or instance.calculator_status == calculator_status

   if not status_matches:
      failures.append(f"a {calculator_status} archetype emitted a {instance.calculator_status} item")

   is_statement = key.form == "statement"

   if is_statement:
      failures.extend(_statement_failures(instance))
   else:
      failures.extend(_value_failures(instance))

   is_no_calculator = instance.calculator_status == "no_calculator"
   is_numeric_key = key.form == "numeric"

   if is_no_calculator and is_numeric_key:
      failures.append("a no-calculator item carries a three-decimal key")

   if instance.calculator_status == "calculator":
      if not instance.setup_required:
         failures.append("a calculator item must set setup_required")

   distractor_paths = [distractor.error_path for distractor in instance.distractors]
   foreign = [path for path in distractor_paths if path not in error_ids]

   if len(instance.distractors) != DISTRACTORS_PER_ITEM:
      failures.append(f"{len(instance.distractors)} distractors, not {DISTRACTORS_PER_ITEM}")

   if foreign:
      failures.append(f"error paths not held by the archetype's skills: {foreign}")

   unknown_mechanisms = [d.mechanism for d in instance.distractors if d.mechanism not in MECHANISMS]

   if unknown_mechanisms:
      failures.append(f"unknown distractor mechanisms: {unknown_mechanisms}")

   has_step_texts = len(instance.steps) >= 2

   if not has_step_texts:
      failures.append("fewer than two worked-solution steps")

   foreign_point_types = [
      step.point_type_id for step in instance.steps
      if step.point_type_id is not None and step.point_type_id not in point_types
   ]

   if foreign_point_types:
      failures.append(f"step point types outside the archetype's list: {foreign_point_types}")

   failures.extend(_figure_failures(instance, spec))
   failures.extend(_invariant_failures(instance, spec, names))

   return failures


def _statement_failures(instance):
   failures = []
   key_label = (instance.key.label or "").strip()
   labels = [(distractor.label or "").strip() for distractor in instance.distractors]
   all_labels = [key_label] + labels

   if not key_label:
      failures.append("a statement key carries no label")

   if any(not text for text in labels):
      failures.append("a statement distractor carries no label")

   if len(set(all_labels)) != len(all_labels):
      failures.append("two options share a label")

   distractor_lengths = sorted(len(text) for text in labels)
   median_length = distractor_lengths[len(distractor_lengths) // 2] if distractor_lengths else 0
   key_stands_out_by_length = median_length > 0 and len(key_label) > LABEL_LENGTH_RATIO * median_length
   key_has_math = r"\(" in key_label
   distractors_with_math = sum(1 for text in labels if r"\(" in text)
   key_stands_out_by_math = key_has_math and distractors_with_math < 2

   if key_stands_out_by_length:
      failures.append("the key label is conspicuously longer than the distractor labels")

   if key_stands_out_by_math:
      failures.append("the key label is the only one carrying mathematics")

   return failures


def _value_failures(instance):
   failures = []
   key = instance.key

   try:
      key_value = sympy.sympify(key.value)
   except Exception:
      return ["the key value does not parse"]

   if key.form == "symbolic":
      has_float = key_value.has(sympy.Float)

      if has_float:
         failures.append("a symbolic key carries a decimal")

   if key.form == "numeric":
      if key.decimals != 3:
         failures.append("a numeric key must be reported to three decimals")

      try:
         nondegenerate = evaluate("nondegenerate_three_decimals(key)", {"key": key_value})
      except Exception:
         nondegenerate = False

      if not nondegenerate:
         failures.append("the three-decimal key is degenerate")

   if not _round_trips(key_value):
      failures.append("the key does not round-trip through MathJSON")

   value_steps = [step for step in instance.steps if step.value is not None]

   if not value_steps:
      failures.append("no worked-solution step carries a value")
   else:
      last = sympy.sympify(value_steps[-1].value)
      agrees = _numeric_agreement(last, key_value) if key.form == "numeric" else equivalent(last, key_value)

      if agrees is not True:
         failures.append("the last valued step does not equal the key")

   for previous, current in zip(value_steps, value_steps[1:]):
      restates = equivalent(previous.value, current.value) is True

      if restates:
         failures.append(f"vacuous step: {current.text[:60]!r} restates the step before")

   values = [key_value]

   for distractor in instance.distractors:
      if distractor.value is None:
         failures.append("a distractor carries no value")
         continue

      try:
         distractor_value = sympy.sympify(distractor.value)
      except Exception:
         failures.append("a distractor value does not parse")
         continue

      if not _round_trips(distractor_value):
         failures.append("a distractor does not round-trip through MathJSON")

      values.append(distractor_value)

   for index, left in enumerate(values):
      for right in values[index + 1:]:
         same = _numeric_agreement(left, right) if key.form == "numeric" else equivalent(left, right)

         if same is not False:
            failures.append("two options are equal or could not be told apart")

   return failures


def _numeric_agreement(left, right):
   """Numeric options are told apart at the reported precision, three decimals."""
   try:
      return round(float(sympy.N(left)), 3) == round(float(sympy.N(right)), 3)
   except (TypeError, ValueError):
      return None


def _figure_failures(instance, spec):
   failures = []
   bindings = {binding["representation"]: binding for binding in spec["representation_bindings"]}
   binding = bindings.get(instance.representation)

   if binding is None:
      return [f"representation {instance.representation} has no binding in the spec"]

   wants_figure = binding["figure_kind"] is not None
   figure = instance.figure

   if wants_figure and figure is None:
      failures.append(f"{instance.representation} needs a {binding['figure_kind']} figure")

   if figure is not None and figure.get("kind") != binding["figure_kind"]:
      failures.append(f"figure kind {figure.get('kind')!r} against binding {binding['figure_kind']!r}")

   if figure is not None and not _labels_inside(figure):
      failures.append("a figure label sits outside the figure")

   lowered = instance.stem.lower()
   refers_to_figure = any(word in lowered for word in FIGURE_WORDS)

   if refers_to_figure and figure is None:
      failures.append("the stem refers to a figure the item does not carry")

   return failures


def _invariant_failures(instance, spec, names):
   failures = []
   scope = dict(names)
   scope.update(instance.notes)
   is_statement = instance.key.form == "statement"
   scope["key"] = instance.key.label if is_statement else sympy.sympify(instance.key.value)

   for invariant in spec["invariants"]:
      try:
         holds = bool(evaluate(invariant, scope))
      except (SpecExpressionError, ZeroDivisionError, TypeError, ValueError) as failure:
         failures.append(f"invariant {invariant!r} raised {type(failure).__name__}")
         continue

      if not holds:
         failures.append(f"invariant {invariant!r} failed")

   return failures


def surface_problems(instance):
   texts = [instance.stem] + [step.text for step in instance.steps]
   texts += [distractor.label for distractor in instance.distractors if distractor.label]

   if instance.key.label:
      texts.append(instance.key.label)

   problems = []

   for text in texts:
      problems.extend(latex_problems(text))

   return problems, len(texts)


def structure(value):
   """What a safe parameter may not move (13, "Radicals and incidentals")."""
   if value is None:
      return None

   value = sympy.sympify(value)

   if value.is_number:
      return ("number", "zero" if value == 0 else "nonzero")

   heads = tuple(sorted({function.func.__name__ for function in value.atoms(sympy.Function)}))
   symbol = sympy.Symbol("x")
   degree = sympy.degree(value, symbol) if value.is_polynomial(symbol) else None

   return (value.func.__name__, heads, degree, len(value.args))


def path_signature(instance):
   steps = tuple(structure(step.value) for step in instance.steps)
   key = instance.key.form if instance.key.form == "statement" else structure(instance.key.value)

   return (len(instance.steps), steps, key)


def incidental_problems(module, spec, rng):
   """Vary each safe parameter alone from a base draw; the solution path may not move."""
   parameters, names = spec_module.draw(spec, rng)
   base = path_signature(build(module, names))
   problems = []
   checked = 0

   for parameter in spec["parameters"]:
      is_safe = parameter["role"] == "safe"

      if not is_safe:
         continue

      checked += 1
      candidates = spec_module.domain_values(parameter)
      rng.shuffle(candidates)

      for value in candidates[:INCIDENTAL_VARIANTS]:
         variant = dict(parameters)

         if parameter.get("count") is not None:
            variant[parameter["name"]] = spec_module._draw_parameter(parameter, rng)
         else:
            variant[parameter["name"]] = value

         try:
            variant_names = spec_module.with_derived(spec, variant)
         except Exception:
            continue

         if not spec_module.constraints_hold(spec, variant_names):
            continue

         moved = path_signature(build(module, variant_names)) != base

         if moved:
            problems.append(f"safe parameter {parameter['name']!r} changes the solution path")
            break

   return problems, checked


def run_family(module, draws=FAMILY_DRAWS):
   """Stage 0 for one template: the Monte Carlo family pass and the template-level checks."""
   archetype_id = module.ARCHETYPE_ID
   report = FamilyReport(archetype_id=archetype_id)
   archetype = library().archetypes.get(archetype_id)

   if archetype is None:
      report.template_problems.append(f"{archetype_id} is not an active archetype")
      return report

   spec = spec_for(module)
   report.template_problems.extend(spec_module.validate_spec(spec, archetype))
   registered = archetype.get("parameter_spec")
   drifted = registered is not None and json.dumps(registered, sort_keys=True) != json.dumps(module.SPEC, sort_keys=True)

   if drifted:
      report.template_problems.append("the template's SPEC differs from the registry's parameter_spec")

   if report.template_problems:
      return report

   is_no_calculator = archetype["calculator_status"] == "no_calculator"
   numeric_calls = numeric_methods_used(module)

   if is_no_calculator and numeric_calls:
      report.template_problems.append(f"a no-calculator template calls {numeric_calls}")

   report.draw_space = spec_module.draw_space(spec)

   if report.draw_space < MIN_DRAW_SPACE:
      report.template_problems.append(f"draw space {report.draw_space} is under {MIN_DRAW_SPACE}")

   error_ids = error_ids_for_skills(library(), archetype["skills"])
   stems = set()
   problems = set()

   for index in range(draws):
      seed = f"{archetype_id}:family:{index}"
      report.draws += 1

      try:
         parameters, names = spec_module.draw_with_seed(spec, seed)
         instance = build(module, names)
      except Exception as failure:
         report.failures.append({"seed": seed, "failures": [f"{type(failure).__name__}: {failure}"[:300]]})
         continue

      failures = check_instance(instance, archetype, spec, names, error_ids)
      surface, units = surface_problems(instance)
      report.surface_defects += len(surface)
      report.surface_units += units
      stems.add(instance.stem + json.dumps(instance.figure, sort_keys=True))
      problems.add(problem_signature(instance))

      if failures:
         report.failures.append({"seed": seed, "draw": spec_module.serialise(parameters), "failures": failures})

   report.distinct_stems = len(stems)

   report.distinct_problems = len(problems)
   problem_floor = min(MIN_DISTINCT_PROBLEMS, draws // 3)

   if report.distinct_problems < problem_floor:
      report.template_problems.append(
         f"only {report.distinct_problems} distinct problems in {draws} draws, where the duplicate gate would see the rest as copies"
      )

   distinct_floor = min(MIN_DISTINCT_STEMS, draws // 2)

   if report.distinct_stems < distinct_floor:
      report.template_problems.append(f"only {report.distinct_stems} distinct stems and figures in {draws} draws")

   try:
      problems, checked = incidental_problems(module, spec, random.Random(20260924))
   except Exception as failure:
      problems, checked = [f"incidental check raised {type(failure).__name__}: {failure}"[:300]], 0

   report.template_problems.extend(problems)
   report.incidentals_checked = checked

   return report
