"""Run only the checks a change can affect, instead of the whole pytest suite, tsc and qa.

Python tests are picked by walking the reverse import graph of app/, tools/ and tests/ from the
changed modules. A test file that names a changed non-Python file (a fixture, a schema, a content
JSON) in a string literal is picked too, as is every test under a changed conftest.py. Client
changes go to `vitest related`, which follows Vite's own import graph, and to an incremental tsc.
The qa scripts run only when the registry, research or qa itself changed.

   python3 tools/affected_checks.py              # working tree against HEAD, untracked included
   python3 tools/affected_checks.py --since main # everything since a ref
   python3 tools/affected_checks.py --plan       # print the commands without running them

The style gate runs first on every changed file. Failures print one line each (pytest --tb=line,
vitest's dot reporter); rerun a single node for the full trace.
"""
import argparse
import ast
import fnmatch
import re
import subprocess
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT / "app" / "web"
PYTHON = ROOT / ".venv" / "bin" / "python"
PYTHON_PACKAGES = ("app", "tools", "tests")
QA_INPUT_PREFIXES = ("data/", "research/", "qa/", "cache/manifest.json", "schemas/")
WEB_SOURCE_SUFFIXES = (".ts", ".tsx", ".css")
WEB_CONFIG_FILES = {"app/web/package.json", "app/web/package-lock.json", "app/web/tsconfig.json", "app/web/vite.config.ts", "app/web/vitest.setup.ts"}
PYTEST_TIMEOUT_SECONDS = 1800
WEB_TIMEOUT_SECONDS = 900
QA_TIMEOUT_SECONDS = 600
STYLE_TIMEOUT_SECONDS = 60
MIN_DIRECTORY_PREFIX = 8
MIN_DIRECTORY_NAME = 6
MIN_GLOB_PREFIX = 4
GLOB_CHARACTERS = re.compile(r"[A-Za-z0-9_./*-]+")


def git_lines(*arguments):
   result = subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=True)
   return [line for line in result.stdout.splitlines() if line]


def changed_paths(since_ref):
   base = since_ref or "HEAD"
   tracked = git_lines("diff", "--name-only", base)
   untracked = git_lines("ls-files", "--others", "--exclude-standard")
   return sorted(set(tracked) | set(untracked))


def module_name(relative_path):
   parts = list(Path(relative_path).with_suffix("").parts)

   if parts[-1] == "__init__":
      parts = parts[:-1]

   return ".".join(parts)


def python_files():
   for package in PYTHON_PACKAGES:
      for path in (ROOT / package).rglob("*.py"):
         is_dependency_dir = "node_modules" in path.parts or "__pycache__" in path.parts

         if not is_dependency_dir:
            yield path.relative_to(ROOT).as_posix()


def resolve_relative_import(importer_module, is_package, level, imported):
   anchor = importer_module.split(".")
   drop = level - 1 if is_package else level
   anchor = anchor[:len(anchor) - drop] if drop else anchor
   return ".".join(part for part in [*anchor, imported or ""] if part)


def imported_modules(relative_path, tree):
   importer = module_name(relative_path)
   is_package = relative_path.endswith("__init__.py")

   for node in ast.walk(tree):
      if isinstance(node, ast.Import):
         for alias in node.names:
            yield alias.name

      elif isinstance(node, ast.ImportFrom):
         base = node.module or ""

         if node.level:
            base = resolve_relative_import(importer, is_package, node.level, node.module)

         yield base

         for alias in node.names:
            yield f"{base}.{alias.name}"


def string_literals(tree):
   for node in ast.walk(tree):
      is_string = isinstance(node, ast.Constant) and isinstance(node.value, str)
      is_short_enough = is_string and len(node.value) < 300

      if is_short_enough:
         yield node.value


def build_graph():
   module_to_file = {module_name(path): path for path in python_files()}
   importers_of = defaultdict(set)
   literals_by_file = {}

   for path in module_to_file.values():
      try:
         tree = ast.parse((ROOT / path).read_text(), filename=path)
      except (SyntaxError, UnicodeDecodeError):
         continue

      literals_by_file[path] = set(string_literals(tree))

      for imported in imported_modules(path, tree):
         candidate = imported

         while candidate:
            target = module_to_file.get(candidate)

            if target:
               importers_of[target].add(path)

            candidate = candidate.rpartition(".")[0]

   return importers_of, literals_by_file


def is_test_file(path):
   name = Path(path).name
   return path.startswith("tests/") and name.startswith("test_") and name.endswith(".py")


def names_directory(literal, directory_names):
   for directory_name in directory_names:
      is_distinctive = len(directory_name) >= MIN_DIRECTORY_NAME
      is_exact = is_distinctive and literal == directory_name
      is_path_tail = is_distinctive and literal.endswith("/" + directory_name)
      is_long_identifier = len(literal) >= MIN_DIRECTORY_PREFIX and literal.replace("_", "").isalnum()
      is_formatted_prefix = is_long_identifier and directory_name.startswith(literal)

      if is_exact or is_path_tail or is_formatted_prefix:
         return True

   return False


def matches_glob(literal, path_tails):
   has_wildcard = "*" in literal
   is_path_glob = has_wildcard and GLOB_CHARACTERS.fullmatch(literal) is not None
   fixed_text = literal.split("*")[0].rsplit("/", 1)[-1]
   is_specific = is_path_glob and len(fixed_text) >= MIN_GLOB_PREFIX

   if not is_specific:
      return False

   return any(fnmatch.fnmatchcase(tail, literal) for tail in path_tails)


def contiguous_tails(parts):
   tails = set()

   for start in range(1, len(parts)):
      for end in range(start + 1, len(parts) + 1):
         tails.add("/".join(parts[start:end]))

   return tails


def files_naming(changed_path, literals_by_file):
   parts = Path(changed_path).parts
   name = Path(changed_path).name
   stem = Path(changed_path).stem
   has_extension = "." in name
   is_distinctive_stem = len(stem) >= MIN_DIRECTORY_PREFIX
   is_python = changed_path.endswith(".py")
   below_top_level = set() if is_python else set(parts[1:-1])
   path_tails = set() if is_python else contiguous_tails(parts)
   matches = set()

   for path, literals in literals_by_file.items():
      for literal in literals:
         names_full_path = changed_path in literal
         names_file = has_extension and (literal == name or literal.endswith("/" + name))
         names_stem = is_distinctive_stem and path.startswith("tests/") and literal == stem
         names_parent = names_directory(literal, below_top_level)
         names_by_glob = matches_glob(literal, path_tails)

         if names_full_path or names_file or names_stem or names_parent or names_by_glob:
            matches.add(path)
            break

   return matches


def affected_tests(changed, importers_of, literals_by_file):
   seeds = set()
   tests = set()
   all_tests = {path for path in literals_by_file if is_test_file(path)}

   for path in changed:
      is_python = path.endswith(".py")
      is_conftest = Path(path).name == "conftest.py" and path.startswith("tests/")

      if is_conftest:
         folder = Path(path).parent.as_posix() + "/"
         tests |= {test for test in all_tests if test.startswith(folder)}

      if is_python:
         seeds.add(path)

      seeds |= files_naming(path, literals_by_file)

   queue = deque(seeds)
   seen = set(seeds)

   while queue:
      current = queue.popleft()

      for importer in importers_of.get(current, ()):
         if importer not in seen:
            seen.add(importer)
            queue.append(importer)

   tests |= {path for path in seen if is_test_file(path)}
   return sorted(tests)


def web_plan(changed):
   web_changes = [path for path in changed if path.startswith("app/web/") and "node_modules" not in path]
   config_changed = any(path in WEB_CONFIG_FILES for path in web_changes)
   sources = [path for path in web_changes if path.startswith("app/web/src/") and path.endswith(WEB_SOURCE_SUFFIXES)]
   existing_sources = [path for path in sources if (ROOT / path).exists()]
   commands = []

   if config_changed:
      commands.append(["npx", "vitest", "run", "--reporter=dot"])

   elif existing_sources:
      relative = [str(Path(path).relative_to("app/web")) for path in existing_sources]
      commands.append(["npx", "vitest", "related", "--run", "--reporter=dot", *relative])

   needs_typecheck = config_changed or any(path.endswith((".ts", ".tsx")) for path in web_changes)

   if needs_typecheck:
      commands.append(["npx", "tsc", "--noEmit", "--incremental", "--tsBuildInfoFile", "node_modules/.cache/tsc.tsbuildinfo"])

   return commands


def qa_plan(changed):
   touches_qa_inputs = any(path.startswith(QA_INPUT_PREFIXES) for path in changed)

   if not touches_qa_inputs:
      return []

   checks = sorted(path.name for path in (ROOT / "qa").glob("[0-9][0-9]_*.py"))
   skipped = {"11_freshness.py", "12_report.py"}
   return [[sys.executable, name] for name in checks if name not in skipped]


def run(command, cwd, timeout_seconds):
   print("$ " + " ".join(command), flush=True)

   try:
      return subprocess.run(command, cwd=cwd, timeout=timeout_seconds).returncode
   except subprocess.TimeoutExpired:
      print(f"timed out after {timeout_seconds} s", flush=True)
      return 124


def main():
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("--since", help="compare against this ref instead of HEAD")
   parser.add_argument("--plan", action="store_true", help="print the commands and exit")
   arguments = parser.parse_args()

   changed = changed_paths(arguments.since)

   if not changed:
      print("no changes")
      return 0

   importers_of, literals_by_file = build_graph()
   tests = affected_tests(changed, importers_of, literals_by_file)
   steps = []
   existing = [path for path in changed if (ROOT / path).is_file()]

   if existing:
      steps.append(([sys.executable, "tools/style_gate.py", *existing], ROOT, STYLE_TIMEOUT_SECONDS))

   if tests:
      steps.append(([str(PYTHON), "-m", "pytest", "-q", "--tb=line", "-p", "no:cacheprovider", *tests], ROOT, PYTEST_TIMEOUT_SECONDS))

   steps += [(command, WEB_DIR, WEB_TIMEOUT_SECONDS) for command in web_plan(changed)]
   steps += [(command, ROOT / "qa", QA_TIMEOUT_SECONDS) for command in qa_plan(changed)]

   print(f"{len(changed)} changed files, {len(tests)} test files selected")

   if arguments.plan or not steps:
      for command, cwd, _ in steps:
         print(f"({cwd.relative_to(ROOT).as_posix() or '.'}) " + " ".join(command))

      return 0

   failures = [" ".join(command[:4]) for command, cwd, timeout_seconds in steps if run(command, cwd, timeout_seconds) != 0]

   if failures:
      print("FAILED: " + "; ".join(failures))
      return 1

   print("all selected checks passed")
   return 0


if __name__ == "__main__":
   sys.exit(main())
