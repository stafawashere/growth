"""Every drill template over 50 seeded draws: the key tells rounding from truncation, the
exclusions of docs/calculator/architecture.md hold, the setup key reads back and agrees with the
value key, and the prompt carries no dash and no run of words from official text."""
import dataclasses
import json
import re
from fractions import Fraction
from functools import lru_cache

import pytest
import sympy

from app.calculator import registry
from app.calculator.check import check_setup, check_value
from app.calculator.kit import EQUATION, EXPRESSION
from app.generation import dedupe
from app.items.mathjson import to_sympy

DRAWS = 50
SETUP_CHECK_DRAWS = 3
LONGEST_SHARED_RUN = 12
AGREEMENT = 1e-12
DASHES = ("\u2013", "\u2014", "\u2012", "\u2015", "\u2212")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
TRIG_TEX = (r"\sin", r"\cos", r"\tan", r"\sec", r"\csc", r"\cot")
TEMPLATE_IDS = sorted(registry.templates())


@lru_cache(maxsize=None)
def tasks(template_id):
   module = registry.templates()[template_id]
   seeds = [f"{template_id}:v{module.TEMPLATE_VERSION}:test:{index}" for index in range(DRAWS)]

   return tuple(registry.draw_task(template_id, seed) for seed in seeds)


@lru_cache(maxsize=1)
def official_index():
   return dedupe.OfficialShingleIndex(dedupe.load_official_pages())


def three_place_forms(key):
   """Rounded and truncated forms by exact fraction arithmetic, apart from the kit's decimal code."""
   value = Fraction(str(sympy.Float(key, 20)))
   magnitude = abs(value) * 1000
   sign = -1 if value < 0 else 1
   truncated = sign * Fraction(int(magnitude), 1000)
   rounded = sign * Fraction(int(magnitude + Fraction(1, 2)), 1000)

   return rounded, truncated


def nonzero_decimals(key):
   text = str(sympy.Float(key, 20))
   is_plain = "e" not in text.lower()
   fraction_digits = text.partition(".")[2] if is_plain else format(sympy.Float(key, 20), ".25f").partition(".")[2]

   return sum(1 for digit in fraction_digits if digit != "0")


def numeric(expression):
   return complex(sympy.N(expression, 30))


def near(value, expected, scale=1.0):
   return abs(value - expected) <= AGREEMENT * max(scale, abs(expected))


def near_integer(value):
   return abs(value - round(value)) < 1e-9


def test_the_registry_finds_twelve_templates():
   assert len(TEMPLATE_IDS) == 12


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_every_draw_builds_a_clear_frozen_task(template_id):
   for task in tasks(template_id):
      assert task.exclusion is None
      assert task.setup_kind in (EXPRESSION, EQUATION)
      assert isinstance(task.value_key, sympy.Float)
      assert task.value_key.is_finite
      assert json.loads(json.dumps(task.draw)) == task.draw

      with pytest.raises(dataclasses.FrozenInstanceError):
         task.prompt = ""


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_every_key_tells_rounding_from_truncation(template_id):
   for task in tasks(template_id):
      rounded, truncated = three_place_forms(task.value_key)

      assert rounded != truncated, task.value_key
      assert nonzero_decimals(task.value_key) >= 3, task.value_key


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_both_accepted_forms_of_every_key_pass_the_value_check(template_id):
   for task in tasks(template_id):
      rounded, truncated = three_place_forms(task.value_key)

      assert check_value(f"{float(rounded):.3f}", task.value_key).correct is True
      assert check_value(f"{float(truncated):.3f}", task.value_key).correct is True


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_the_setup_key_reads_back_and_agrees_with_the_value_key(template_id):
   module = registry.templates()[template_id]

   for task in tasks(template_id):
      setup = to_sympy(task.setup_key)

      if task.setup_kind == EXPRESSION:
         has_integral = setup.has(sympy.Integral)
         evaluated = setup.evalf(30) if has_integral else setup.doit()

         assert near(numeric(evaluated), numeric(task.value_key))
         continue

      assert isinstance(setup, sympy.Eq)
      difference = setup.lhs - setup.rhs
      variable = next(iter(difference.free_symbols))
      is_extreme = module.CAPABILITY == "plot" and "peak" in task.draw
      solution = sympy.Float(task.draw["peak"], 20) if is_extreme else task.value_key

      assert abs(numeric(difference.subs(variable, solution))) < 1e-10

      if is_extreme:
         function = to_sympy(task.draw["functions"]["f"]["expression"])

         assert near(numeric(function.subs(variable, solution)), numeric(task.value_key))


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_the_exclusions_hold(template_id):
   for task in tasks(template_id):
      setup = to_sympy(task.setup_key)

      for integral in setup.atoms(sympy.Integral):
         integrand = integral.function
         variable = integral.limits[0][0]
         is_linear_polynomial = integrand.is_polynomial(variable) and sympy.degree(integrand, variable) <= 1

         assert not is_linear_polynomial, integrand

      for substitution in setup.atoms(sympy.Subs):
         for derivative in substitution.expr.atoms(sympy.Derivative):
            variable = derivative.variables[0]
            body = derivative.expr
            is_linear_polynomial = body.is_polynomial(variable) and sympy.degree(body, variable) <= 1

            assert not is_linear_polynomial, body

      module = registry.templates()[template_id]
      is_zero = module.CAPABILITY in ("zero", "plot") and "peak" not in task.draw

      if is_zero:
         assert not near_integer(2 * float(task.value_key)), task.value_key

      if module.CAPABILITY == "intersection":
         crossing = float(task.draw.get("crossing", task.value_key))
         f_expression = to_sympy(task.draw["functions"]["f"]["expression"])
         height = float(f_expression.subs(sympy.Symbol("x"), crossing))

         assert not (near_integer(crossing) and near_integer(height)), (crossing, height)


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_the_setup_key_passes_its_own_setup_check(template_id):
   for task in tasks(template_id)[:SETUP_CHECK_DRAWS]:
      verdict = check_setup(task.setup_key, task)

      assert (verdict.shown, verdict.correct, verdict.reason) == (True, True, None), task.prompt


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_radians_and_units_are_flagged_where_the_task_needs_them(template_id):
   for task in tasks(template_id):
      has_trig = any(name in task.function_tex for name in TRIG_TEX)

      assert task.radian_sensitive == has_trig

      if task.unit is not None:
         assert task.unit in task.prompt


@pytest.mark.parametrize("template_id", TEMPLATE_IDS)
def test_the_prompt_has_no_dash_emoji_or_official_phrase(template_id):
   index = official_index()
   longest = (0, None, None)

   for task in tasks(template_id):
      assert task.prompt.strip()
      assert not any(dash in task.prompt for dash in DASHES), task.prompt
      assert EMOJI.search(task.prompt) is None, task.prompt
      assert "three decimal places" in task.prompt

      run_length, where = index.longest_run(dedupe.normalise(task.prompt))

      if run_length > longest[0]:
         longest = (run_length, where, task.prompt)

   assert longest[0] <= LONGEST_SHARED_RUN, longest


def test_the_official_phrase_check_can_see_official_text():
   index = official_index()
   control_page = next(page for page in index.pages if page.doc_id.startswith("frq-") and len(page.tokens) >= 40)
   control_text = " ".join(control_page.tokens[10:30])
   run_length, _ = index.longest_run(dedupe.normalise(control_text))

   assert run_length > LONGEST_SHARED_RUN
