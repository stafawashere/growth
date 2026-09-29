"""Tests for tools/check_calculator.py, docs/calculator/build-plan.md Slice 1b: every lint is
shown red on a fixture under tests/fixtures/calculator and green on the clean card, and the
template section is driven by a fake registry injected in place of app.calculator.registry.

Each red fixture is the derivative card with one defect. It replaces that card in a copy of
content/calculator, so the set lints see a full card set and only the defect differs.
"""
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

import pytest
import sympy

from tools import check_calculator

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = REPOSITORY_ROOT / "content" / "calculator"
FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "calculator"
REPLACED_CARD = "CCD-derivative-01.json"
READABLE_SETUP = ["Add", "x", 1]
USABLE_KEY = sympy.Float("1.2345678912345678912", 20)

RED_FIXTURES = {
   "red_schema": "schema",
   "red_citations": "citations",
   "red_quotes": "quotes",
   "red_quotes_partial": "quotes",
   "red_error_ids_unknown": "error_ids",
   "red_error_ids_retired": "error_ids",
   "red_habit_words": "habit_words",
   "red_student_text_dash": "student_text",
   "red_student_text_emoji": "student_text",
   "red_student_text_praise": "student_text",
   "red_student_text_library_id": "student_text",
   "red_student_text_citation": "student_text",
   "red_student_text_tag": "student_text",
   "red_student_text_advice": "student_text",
   "red_student_text_prediction": "student_text",
   "red_keys": "keys",
   "red_answer": "answer",
   "red_coverage": "coverage",
   "red_template_set": "template_set",
}


def content_with(tmp_path, fixture_name):
   content_dir = tmp_path / "calculator"
   shutil.copytree(CONTENT_DIR, content_dir)
   shutil.copyfile(FIXTURE_DIR / f"{fixture_name}.json", content_dir / "cards" / REPLACED_CARD)

   return content_dir


def lint_names(report):
   return {name for findings in report["findings_by_file"].values() for name in findings}


def test_every_card_lint_and_set_lint_has_a_red_fixture():
   covered = set(RED_FIXTURES.values())
   linted = set(check_calculator.CARD_LINTS) | set(check_calculator.SET_LINTS)

   assert covered == linted


def test_clean_fixture_has_no_findings(tmp_path):
   report = check_calculator.check_paths([content_with(tmp_path, "clean")], include_templates=False)

   assert report["card_count"] == 9
   assert report["findings_by_file"] == {}


@pytest.mark.parametrize("fixture_name", sorted(RED_FIXTURES))
def test_red_fixture_fails_its_lint(tmp_path, fixture_name):
   report = check_calculator.check_paths([content_with(tmp_path, fixture_name)], include_templates=False)

   assert RED_FIXTURES[fixture_name] in lint_names(report)


def test_partial_quote_is_a_finding_not_a_warning(tmp_path):
   report = check_calculator.check_paths([content_with(tmp_path, "red_quotes_partial")], include_templates=False)
   messages = report["findings_by_file"][REPLACED_CARD]["quotes"]

   assert any("only partially matches" in message for message in messages)


def test_cli_prints_counts_and_exits_by_findings(tmp_path):
   clean_run = subprocess.run(
      [sys.executable, "tools/check_calculator.py", str(content_with(tmp_path / "clean", "clean")), "--no-templates"],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )
   red_run = subprocess.run(
      [sys.executable, "tools/check_calculator.py", str(content_with(tmp_path / "red", "red_keys")), "--no-templates"],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )

   assert clean_run.returncode == 0
   assert "cards read: 9\nclean: 9\nwith findings: 0" in clean_run.stdout
   assert red_run.returncode == 1
   assert "cards read: 9\nclean: 8\nwith findings: 1" in red_run.stdout
   assert f"{REPLACED_CARD}:\n  keys: steps/0 has no keys" in red_run.stdout


class DrawExhausted(Exception):
   pass


def listed_templates():
   return json.loads((CONTENT_DIR / "templates.json").read_text())["templates"]


def fake_registry(task_for=None, redraws_for=None, card_for=None, left_out=()):
   """A registry module shaped like the contract: templates(), and draw_task, which calls the
   module's build once and again for each redraw."""
   task_for = task_for or (lambda template_id, seed: types.SimpleNamespace(value_key=USABLE_KEY, setup_key=READABLE_SETUP))
   redraws_for = redraws_for or (lambda seed: 0)
   card_for = card_for or (lambda template: template["card_id"])
   modules = {}

   for template in listed_templates():
      if template["id"] in left_out:
         continue

      module = types.ModuleType(f"fake_{template['id']}")
      module.TEMPLATE_ID = template["id"]
      module.CAPABILITY = template["capability"]
      module.CARD_ID = card_for(template)
      module.TEMPLATE_VERSION = 1
      module.build = lambda names, template_id=template["id"]: task_for(template_id, names["seed"])
      modules[template["id"]] = module

   registry = types.ModuleType("app.calculator.registry")
   registry.DrawExhausted = DrawExhausted
   registry.templates = lambda: modules

   def draw_task(template_id, seed):
      module = modules[template_id]
      redraws = redraws_for(seed)

      if redraws is None:
         for attempt in range(3):
            module.build({"seed": f"{seed}:r{attempt}"})

         raise DrawExhausted(template_id)

      for attempt in range(redraws):
         module.build({"seed": f"{seed}:r{attempt}"})

      return module.build({"seed": seed})

   registry.draw_task = draw_task

   return registry


def template_messages(monkeypatch, registry):
   monkeypatch.setitem(sys.modules, "app.calculator.registry", registry)
   report = check_calculator.check_paths([CONTENT_DIR], include_templates=True)

   return report["findings_by_file"].get("templates.json", {}).get("templates", [])


def seed_index(seed):
   return int(seed.split(":check:")[1].split(":")[0])


def test_template_section_green_on_a_conforming_registry(monkeypatch):
   assert template_messages(monkeypatch, fake_registry()) == []


def test_template_section_counts_redraws_as_exclusions(monkeypatch):
   registry = fake_registry(redraws_for=lambda seed: 1 if seed_index(seed) % 4 else 0)
   messages = template_messages(monkeypatch, registry)

   assert any("excludes 150 of 200 draws" in message for message in messages)


def test_template_section_accepts_exclusions_up_to_half(monkeypatch):
   registry = fake_registry(redraws_for=lambda seed: 1 if seed_index(seed) % 2 else 0)
   messages = template_messages(monkeypatch, registry)

   assert not any("excludes" in message for message in messages)


def test_template_section_counts_draw_exhausted(monkeypatch):
   registry = fake_registry(redraws_for=lambda seed: None if seed_index(seed) < 101 else 0)
   messages = template_messages(monkeypatch, registry)

   assert any("excludes 101 of 200 draws" in message for message in messages)


@pytest.mark.parametrize("key_text", ["1.5", "1.0006", "1.2341234", "0.100200000001"])
def test_template_section_refuses_a_key_the_drill_cannot_use(monkeypatch, key_text):
   weak_task = types.SimpleNamespace(value_key=sympy.Float(key_text, 20), setup_key=READABLE_SETUP)
   registry = fake_registry(task_for=lambda template_id, seed: weak_task)
   messages = template_messages(monkeypatch, registry)

   assert any("value_key lacks" in message for message in messages)


def test_template_section_refuses_a_setup_to_sympy_cannot_read(monkeypatch):
   unread_task = types.SimpleNamespace(value_key=USABLE_KEY, setup_key=["NoSuchHead", 1])
   registry = fake_registry(task_for=lambda template_id, seed: unread_task)
   messages = template_messages(monkeypatch, registry)

   assert any("setup_key is refused by to_sympy" in message for message in messages)


def test_template_section_refuses_a_template_naming_the_wrong_card(monkeypatch):
   registry = fake_registry(card_for=lambda template: "CCD-plot-01" if template["id"] == "CDT-zero-01" else template["card_id"])
   messages = template_messages(monkeypatch, registry)

   assert any(message.startswith("CDT-zero-01 names CCD-plot-01") for message in messages)


def test_template_section_refuses_a_listed_template_missing_from_the_registry(monkeypatch):
   registry = fake_registry(left_out=("CDT-value-02",))
   messages = template_messages(monkeypatch, registry)

   assert "CDT-value-02 is in templates.json but not in the registry" in messages
