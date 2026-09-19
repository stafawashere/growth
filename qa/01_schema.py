"""Validate every registry against its JSON Schema and every Markdown front matter."""
import json
import re
from jsonschema import Draft202012Validator
from qa_common import ROOT, DATA, load_json, markdown_files, finish

failures = []

for schema_path in sorted((ROOT / "schemas").glob("*.schema.json")):
   name = schema_path.name.replace(".schema.json", "")
   data = load_json(f"{name}.json")
   is_present = data is not None

   if not is_present:
      failures.append(f"data/{name}.json missing")
      continue

   validator = Draft202012Validator(json.loads(schema_path.read_text()))

   for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))[:50]:
      location = "/".join(str(part) for part in error.path)
      failures.append(f"{name}.json at {location}: {error.message[:160]}")

front_matter = re.compile(r"^---\n(.*?)\n---\n", re.S)

for path in markdown_files():
   is_plan = path.name.startswith("PLAN-")

   if is_plan:
      continue

   text = path.read_text()
   match = front_matter.match(text)
   has_front_matter = match is not None

   if not has_front_matter:
      failures.append(f"{path.relative_to(ROOT)}: no front matter")
      continue

   for field in ["title", "research_date", "status", "purpose"]:
      has_field = re.search(rf"^{field}:", match.group(1), re.M) is not None

      if not has_field:
         failures.append(f"{path.relative_to(ROOT)}: front matter lacks {field}")

finish("01_schema", failures)
