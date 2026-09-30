"""The template registry: what it finds, how it draws and redraws, and what the package imports."""
import ast
import re
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.calculator import registry
from app.calculator.kit import DrillTask

PACKAGE_DIR = Path(registry.__file__).resolve().parent
FORBIDDEN_PACKAGES = ("app.engine", "app.session", "app.progress", "app.db")
CARD_IDS = {
   "CDT-plot-01": "CCD-plot-01",
   "CDT-plot-02": "CCD-plot-01",
   "CDT-zero-01": "CCD-zero-01",
   "CDT-zero-02": "CCD-zero-01",
   "CDT-derivative-01": "CCD-derivative-01",
   "CDT-derivative-02": "CCD-derivative-01",
   "CDT-integral-01": "CCD-integral-01",
   "CDT-integral-02": "CCD-integral-02",
   "CDT-intersection-01": "CCD-intersection-01",
   "CDT-intersection-02": "CCD-intersection-01",
   "CDT-value-01": "CCD-value-01",
   "CDT-value-02": "CCD-value-01",
}


def test_the_capabilities_are_the_six_of_the_contract():
   assert registry.CAPABILITIES == ("plot", "zero", "derivative", "integral", "intersection", "value")


def test_every_template_is_found_under_its_id_with_its_card():
   found = registry.templates()

   assert {template_id: module.CARD_ID for template_id, module in found.items()} == CARD_IDS

   for template_id, module in found.items():
      capability, number = re.fullmatch(r"CDT-([a-z]+)-(\d{2})", template_id).groups()

      assert module.CAPABILITY == capability
      assert Path(module.__file__).name == f"cdt_{capability}_{number}.py"
      assert isinstance(module.TEMPLATE_VERSION, int)
      assert callable(module.build)
      assert {"parameters", "constraints", "derived"} <= set(module.SPEC)


@pytest.mark.parametrize("capability", registry.CAPABILITIES)
def test_each_capability_has_two_templates(capability):
   chosen = registry.templates_for(capability)

   assert len(chosen) == 2
   assert all(module.CAPABILITY == capability for module in chosen.values())


def test_an_unknown_capability_has_no_templates():
   assert registry.templates_for("mixed") == {}


def test_a_seed_draws_the_same_task_every_time_and_seeds_differ():
   first = registry.draw_task("CDT-value-01", "CDT-value-01:v1:user:0")
   again = registry.draw_task("CDT-value-01", "CDT-value-01:v1:user:0")
   others = {registry.draw_task("CDT-value-01", f"CDT-value-01:v1:user:{index}").prompt for index in range(8)}

   assert (first.prompt, first.value_key, first.draw) == (again.prompt, again.value_key, again.draw)
   assert len(others) >= 6


def fake_template(clear_seed):
   def build(names):
      exclusion = None if names["seed"] == clear_seed else "key_trivial"

      return DrillTask(
         prompt=names["seed"],
         function_tex="",
         setup_key=0,
         setup_kind="expression",
         value_key=None,
         unit=None,
         radian_sensitive=False,
         draw={},
         exclusion=exclusion,
      )

   return SimpleNamespace(TEMPLATE_ID="CDT-fake-01", SPEC={}, build=build)


def with_fake(monkeypatch, clear_seed):
   seeds = []

   def recorded_draw(spec, seed):
      seeds.append(seed)

      return {}, {"seed": seed}

   monkeypatch.setattr(registry, "templates", lambda: {"CDT-fake-01": fake_template(clear_seed)})
   monkeypatch.setattr(registry, "draw_with_seed", recorded_draw)

   return seeds


def test_an_excluded_draw_is_redrawn_under_the_suffixed_seed(monkeypatch):
   seeds = with_fake(monkeypatch, "base:r2")
   task = registry.draw_task("CDT-fake-01", "base")

   assert seeds == ["base", "base:r1", "base:r2"]
   assert task.prompt == "base:r2"
   assert task.exclusion is None


def test_fifty_redraws_that_all_fail_raise_draw_exhausted(monkeypatch):
   seeds = with_fake(monkeypatch, "never")

   with pytest.raises(registry.DrawExhausted):
      registry.draw_task("CDT-fake-01", "base")

   assert len(seeds) == 51
   assert seeds[-1] == "base:r50"


def imported_modules(path):
   tree = ast.parse(path.read_text())
   names = []

   for node in ast.walk(tree):
      if isinstance(node, ast.Import):
         names.extend(alias.name for alias in node.names)

      if isinstance(node, ast.ImportFrom) and node.module:
         names.append(node.module)

   return names


def test_the_package_imports_nothing_from_the_engine_session_progress_or_db():
   imports = [name for path in sorted(PACKAGE_DIR.rglob("*.py")) for name in imported_modules(path)]
   forbidden = [name for name in imports if name.startswith(FORBIDDEN_PACKAGES)]

   assert "app.generation.spec" in imports
   assert "app.items.mathjson" in imports
   assert forbidden == []
