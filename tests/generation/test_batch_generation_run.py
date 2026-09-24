"""11 P4 end to end, test_batch_generation_run: a batch of generation jobs runs offline, publishes
an item only when every check agrees, and queues each split decision with the rule that stopped
it, keeping the item and its provenance.

The re-solve here is a fixture, not an independent solver: it answers with the template's own
answer, and one item gets a planted wrong answer, so the test checks the pipeline's handling of
agreement and disagreement. The independence of the real re-solve is the offline agents' and is
rechecked by tests/items/test_key_recheck.py on every generated bank.
"""
import json

import pytest

from tools import generate_bank

ARCHETYPES = ["BC-QA-06004", "BC-QA-08001", "BC-QA-10007"]
PER_ARCHETYPE = 3


@pytest.fixture
def batch_paths(tmp_path, monkeypatch):
   paths = {
      "CANDIDATES": tmp_path / "var" / "candidates",
      "RESOLVE": tmp_path / "var" / "resolve",
      "GATE_REPORT": tmp_path / "var" / "gate_report.json",
      "CONTENT": tmp_path / "content",
      "REVIEW": tmp_path / "content" / "generation_review",
   }

   for name, path in paths.items():
      monkeypatch.setattr(generate_bank, name, path)

   monkeypatch.setattr(generate_bank, "ROOT", tmp_path)
   (tmp_path / "content").mkdir()

   return paths


def answer_literal(record):
   key = record["answer_key"]

   if key["form"] == "statement":
      return repr(key["label"])

   return f"to_sympy({json.dumps(key['mathjson'])})"


def write_fixture_resolve(paths, wrong_id):
   for bank_dir in paths["RESOLVE"].iterdir():
      lines = [
         "from app.items.mathjson import to_sympy",
         "import sympy",
         "",
         "FORMULATIONS = {",
      ]

      for entry in json.loads((bank_dir / "stems_main.json").read_text()):
         record = json.loads((paths["CANDIDATES"] / bank_dir.name / f"{entry['id']}.json").read_text())
         answer = answer_literal(record)

         if entry["id"] == wrong_id:
            answer = f"{answer} + 1"

         lines.append(f"   {entry['id']!r}: lambda: {answer},")

      lines.append("}")
      (bank_dir / "formulations_main.py").write_text("\n".join(lines) + "\n")


def test_batch_generation_run(batch_paths):
   assert generate_bank.main(["plan", "--gate", "--count", str(PER_ARCHETYPE), "--archetypes", *ARCHETYPES]) == 0

   candidates = sorted(batch_paths["CANDIDATES"].glob("*/ITM-GEN-*.json"))
   stems = [entry for path in batch_paths["RESOLVE"].glob("*/stems_*.json") for entry in json.loads(path.read_text())]

   assert len(candidates) == len(ARCHETYPES) * PER_ARCHETYPE
   assert {entry["id"] for entry in stems} == {path.stem for path in candidates}

   planted = "ITM-GEN-06004-01"
   write_fixture_resolve(batch_paths, planted)

   assert generate_bank.main(["publish"]) == 0

   published = sorted(path.stem for path in batch_paths["CONTENT"].glob("items_gen_*/ITM-GEN-*.json"))
   queued = sorted(batch_paths["REVIEW"].glob("*/ITM-GEN-*.json"))
   queued_ids = [path.stem for path in queued]

   assert planted in queued_ids
   assert planted not in published
   assert len(published) + len(queued) == len(candidates)
   assert len(published) >= len(candidates) - 2

   split = json.loads((batch_paths["REVIEW"] / "needs_review" / f"{planted}.json").read_text())

   assert 3 in split["review"]["rules"]
   assert split["provenance"]["parameter_seed"]
   assert split["provenance"]["template_id"] == "TPL-BC-QA-06004-v1"

   for bank_dir in batch_paths["CONTENT"].glob("items_gen_*"):
      assert (bank_dir / "key_formulations.py").exists()
