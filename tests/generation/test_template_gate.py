"""The template gate fails a family on each defect 04 and 13 name, and passes the exemplars.

Each test plants one defect into an exemplar template's output and asserts the family pass
reports that defect by name, so a check that silently stopped firing turns its test red.
"""
import copy
import importlib.util

import pytest
import sympy

from app.generation import template
from app.generation.kit import Step

DRAWS = 40


def module_named(archetype_id):
   return template.template_module(archetype_id)


def wrapped(module, change):
   """A stand-in for the template module whose build applies change to every instance."""

   class Wrapped:
      ARCHETYPE_ID = module.ARCHETYPE_ID
      TEMPLATE_VERSION = module.TEMPLATE_VERSION
      AUTHORED_BY = module.AUTHORED_BY
      SPEC = module.SPEC

      @staticmethod
      def build(names):
         instance = module.build(names)
         change(instance)

         return instance

   Wrapped.__name__ = module.__name__

   return Wrapped


def failure_texts(report):
   texts = list(report.template_problems)

   for failure in report.failures:
      texts.extend(failure["failures"])

   return " | ".join(texts)


@pytest.fixture(autouse=True)
def source_check_on_the_real_module(monkeypatch):
   """numeric_methods_used reads source, which a wrapper has none of; point it at the original."""
   original = template.numeric_methods_used

   def by_archetype(module):
      return original(module_named(module.ARCHETYPE_ID))

   monkeypatch.setattr(template, "numeric_methods_used", by_archetype)


@pytest.mark.parametrize("archetype_id", ["BC-QA-08001", "BC-QA-06004", "BC-QA-10007"])
def test_the_exemplar_templates_pass_the_gate(archetype_id):
   report = template.run_family(module_named(archetype_id), draws=DRAWS)

   assert report.passed, failure_texts(report)


def test_a_distractor_equal_to_the_key_fails_the_family():
   def plant(instance):
      instance.distractors[0].value = instance.key.value

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert not report.passed
   assert "two options are equal" in failure_texts(report)


def test_a_key_the_worked_solution_does_not_reach_fails_the_family():
   def plant(instance):
      instance.key.value = sympy.sympify(instance.key.value) + 1

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert "the last valued step does not equal the key" in failure_texts(report)


def test_a_step_that_restates_the_one_before_is_vacuous():
   def plant(instance):
      last = [step for step in instance.steps if step.value is not None][-1]
      instance.steps.append(Step(text="So the value is as found.", value=last.value))

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert "vacuous step" in failure_texts(report)


def test_an_error_path_the_archetype_does_not_hold_fails_the_family():
   def plant(instance):
      instance.distractors[0].error_path = "BC-ERR-10023"

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert "error paths not held" in failure_texts(report)


def test_a_graph_item_without_its_figure_fails_the_family():
   def plant(instance):
      instance.figure = None

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)
   texts = failure_texts(report)

   assert "needs a function_graph figure" in texts
   assert "refers to a figure the item does not carry" in texts


def test_a_label_outside_the_window_fails_the_family():
   def plant(instance):
      instance.figure["labels"][0]["anchor"] = [20.0, 0.0]

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert "label sits outside the figure" in failure_texts(report)


def test_a_three_decimal_key_must_not_be_degenerate():
   def plant(instance):
      instance.key.value = sympy.Float(3, 15)
      instance.steps[-1].value = sympy.Float(3, 15)

   report = template.run_family(wrapped(module_named("BC-QA-08001"), plant), draws=DRAWS)

   assert "the three-decimal key is degenerate" in failure_texts(report)


def test_a_calculator_item_must_ask_for_the_setup():
   def plant(instance):
      instance.setup_required = False

   report = template.run_family(wrapped(module_named("BC-QA-08001"), plant), draws=DRAWS)

   assert "must set setup_required" in failure_texts(report)


def test_a_statement_key_that_stands_out_by_length_fails_the_family():
   def plant(instance):
      instance.key.label = instance.key.label + " This is shown by checking every condition of every test in full detail."

   report = template.run_family(wrapped(module_named("BC-QA-10007"), plant), draws=DRAWS)

   assert "conspicuously longer" in failure_texts(report)


def test_the_source_scan_names_numeric_calls(tmp_path, monkeypatch):
   monkeypatch.undo()
   source = tmp_path / "numeric_template.py"
   source.write_text("import sympy\n\n\ndef build(names):\n   return sympy.Integral(names, (names, 0, 1)).evalf(10)\n")
   spec = importlib.util.spec_from_file_location("numeric_template", source)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

   assert template.numeric_methods_used(module) == ["evalf"]
   assert template.numeric_methods_used(module_named("BC-QA-06004")) == []


def test_a_safe_parameter_that_changes_the_path_fails_the_family(monkeypatch):
   module = module_named("BC-QA-06004")
   altered = copy.deepcopy(template.spec_for(module))

   for parameter in altered["parameters"]:
      if parameter["name"] == "direction":
         parameter["role"] = "safe"

   altered["dial_bindings"] = [binding for binding in altered["dial_bindings"] if binding["parameter"] != "direction"]
   monkeypatch.setattr(template, "spec_for", lambda _module: altered)
   report = template.run_family(module, draws=DRAWS)

   assert "safe parameter 'direction' changes the solution path" in failure_texts(report)


def test_a_draw_space_under_the_floor_fails_the_family(monkeypatch):
   module = module_named("BC-QA-10007")
   altered = copy.deepcopy(template.spec_for(module))

   for parameter in altered["parameters"]:
      if parameter["name"] in ("coefficient", "offset"):
         parameter["domain"] = {"values": [1]}

   monkeypatch.setattr(template, "spec_for", lambda _module: altered)
   report = template.run_family(module, draws=DRAWS)

   assert "draw space" in failure_texts(report)


def test_two_small_distinct_constants_are_never_called_equal():
   tiny = sympy.Rational(1, 10**12)

   assert template.equivalent(tiny, 2 * tiny) is False
   assert template.equivalent(sympy.sqrt(2) * sympy.sqrt(3), sympy.sqrt(6)) is True
   assert template.equivalent(sympy.Float("0.333333333333333333", 20), sympy.Float(1 / 3, 15)) is True


def test_a_family_whose_draws_are_copies_of_each_other_fails_the_gate():
   def plant(instance):
      instance.stem = r"Find \( \int_{0}^{8} f(x)\,dx \) for the function f whose graph is shown."
      instance.figure["alt"] = "The same graph on every draw."
      instance.figure["labels"] = []

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert "distinct problems" in failure_texts(report)


def test_a_coefficient_of_1_printed_in_the_mathematics_is_a_surface_defect():
   def plant(instance):
      instance.stem = instance.stem + r" Note that \( 1 x^{2} \ge 0 \)."

   report = template.run_family(wrapped(module_named("BC-QA-06004"), plant), draws=DRAWS)

   assert not report.passed
   assert report.surface_rate >= template.SURFACE_DEFECT_BAR
