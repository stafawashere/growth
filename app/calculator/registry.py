"""Every drill template in app/calculator/templates, and one task drawn from a template by seed
(docs/calculator/build-plan.md, Contracts fixed for the parallel slices)."""
import importlib
import pkgutil
from functools import lru_cache

from app.calculator import templates as template_package
from app.generation.spec import DrawExhausted, draw_with_seed

CAPABILITIES = ("plot", "zero", "derivative", "integral", "intersection", "value")
MAX_REDRAWS = 50

__all__ = ["CAPABILITIES", "DrawExhausted", "draw_task", "templates", "templates_for"]


@lru_cache(maxsize=1)
def _loaded():
   modules = {}

   for info in sorted(pkgutil.iter_modules(template_package.__path__), key=lambda entry: entry.name):
      is_template = info.name.startswith("cdt_")

      if not is_template:
         continue

      module = importlib.import_module(f"{template_package.__name__}.{info.name}")
      modules[module.TEMPLATE_ID] = module

   return modules


def templates():
   return dict(_loaded())


def templates_for(capability):
   return {template_id: module for template_id, module in templates().items() if module.CAPABILITY == capability}


def redraw_seed(seed, attempt):
   return seed if attempt == 0 else f"{seed}:r{attempt}"


def draw_task(template_id, seed):
   """The task the seed draws, or the first redraw no exclusion rejects."""
   module = templates()[template_id]

   for attempt in range(MAX_REDRAWS + 1):
      _, names = draw_with_seed(module.SPEC, redraw_seed(seed, attempt))
      task = module.build(names)

      if task.exclusion is None:
         return task

   raise DrawExhausted(f"{template_id} excluded {MAX_REDRAWS + 1} draws from seed {seed!r}")
