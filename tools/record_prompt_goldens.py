"""Record the digest golden of every prompt template that has none.

Usage: python3 tools/record_prompt_goldens.py [--check]

tests/providers/test_prompts.py pins each template under prompts/ to a golden in
tests/fixtures/prompt_goldens/, named after the template's path with "/" written "__", holding the
version from the file name and the sha256 of the file's bytes. This writes the golden for a
template that has none. It never rewrites an existing golden: a template whose bytes no longer
match its golden changed after it was pinned, and the fix is a new versioned file, not a new
digest for the old one, so such a template is reported and the run exits 1.

--check writes nothing and exits 1 when any template lacks a golden or disagrees with it.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = REPOSITORY_ROOT / "prompts"
GOLDENS_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "prompt_goldens"
VERSION_SUFFIX = re.compile(r"_v(\d+)\.md$")


def golden_path_for(template_path):
   flat_name = str(template_path.relative_to(PROMPTS_DIR)).replace("/", "__")

   return GOLDENS_DIR / f"{flat_name}.json"


def golden_for(template_path):
   version_match = VERSION_SUFFIX.search(template_path.name)

   if version_match is None:
      return None

   return {
      "version": f"v{version_match.group(1)}",
      "sha256": hashlib.sha256(template_path.read_bytes()).hexdigest(),
   }


def survey():
   missing = []
   disagreeing = []
   unversioned = []

   for template_path in sorted(PROMPTS_DIR.rglob("*.md")):
      expected = golden_for(template_path)

      if expected is None:
         unversioned.append(template_path)
         continue

      golden_path = golden_path_for(template_path)

      if not golden_path.exists():
         missing.append((template_path, golden_path, expected))
         continue

      recorded = json.loads(golden_path.read_text())

      if recorded != expected:
         disagreeing.append(template_path)

   return missing, disagreeing, unversioned


def main(argv=None):
   parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
   parser.add_argument("--check", action="store_true", help="write nothing, exit 1 on any gap")
   arguments = parser.parse_args(argv)
   missing, disagreeing, unversioned = survey()

   for template_path in unversioned:
      print(f"no _v<n> version marker: {template_path.relative_to(REPOSITORY_ROOT)}")

   for template_path in disagreeing:
      print(f"changed after its golden was recorded, needs a new version: {template_path.relative_to(REPOSITORY_ROOT)}")

   for template_path, golden_path, expected in missing:
      relative = template_path.relative_to(REPOSITORY_ROOT)

      if arguments.check:
         print(f"no golden: {relative}")
         continue

      golden_path.write_text(json.dumps(expected, indent=3) + "\n")
      print(f"recorded {golden_path.relative_to(REPOSITORY_ROOT)} ({expected['version']}, {expected['sha256']})")

   has_gaps = len(unversioned) > 0 or len(disagreeing) > 0
   left_missing = arguments.check and len(missing) > 0

   return 1 if has_gaps or left_missing else 0


if __name__ == "__main__":
   sys.exit(main())
