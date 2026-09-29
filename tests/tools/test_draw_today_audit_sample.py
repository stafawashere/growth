"""tools/draw_today_audit_sample.py: the draw must repeat for a seed, must hold the short answer
floor even when short answer items are scarce, and the stems-only file a blind re-solver reads
must carry no key and no distractor rationale."""
import json

from tools import draw_today_audit_sample

LEAKING_KEYS = {"is_key", "error_path", "answer_key", "worked_solution", "derivation", "mechanism", "violated_step"}


def write_item(directory, item_id, unit, item_format, calculator_status, provenance_fields):
   record = {
      "id": item_id,
      "archetype_id": f"BC-QA-{unit}001",
      "format": item_format,
      "stem": {"text": f"Find the value for {item_id}."},
      "answer_key": {"form": "numeric", "mathjson": 1},
      "worked_solution": [{"step": 1, "text": "the key is 1", "mathjson": 1}],
      "options": [
         {"id": "A", "value": 1, "is_key": True, "error_path": None},
         {"id": "B", "value": 2, "is_key": False, "error_path": "BC-ERR-01001", "derivation": "d", "mechanism": "m"},
         {"id": "C", "value": 3, "is_key": False, "error_path": "BC-ERR-01002", "violated_step": 0},
         {"id": "D", "value": 4, "is_key": False, "error_path": "BC-ERR-01003"},
      ],
      "calculator_status": calculator_status,
      "representation": "BC-REP-01",
      **provenance_fields,
   }
   (directory / f"{item_id}.json").write_text(json.dumps(record))


def build_bank(root):
   template_dir = root / "items_gen_unit01"
   agent_dir = root / "items_p1_agent"
   ignored_dir = root / "lessons"

   for directory in (template_dir, agent_dir, ignored_dir):
      directory.mkdir(parents=True)

   template_provenance = {"provenance": {"template_id": "TPL-1"}}
   draft_provenance = {"drafted_by": "agent draft, pending operator review"}

   for index in range(100):
      unit = "01" if index % 2 == 0 else "02"
      status = "calculator" if index % 5 == 0 else "no_calculator"
      write_item(template_dir, f"ITM-GEN-{index:05d}", unit, "mcq", status, template_provenance)

   for index in range(3):
      write_item(agent_dir, f"ITM-AGT-{index:05d}", "02", "short_answer", "no_calculator", draft_provenance)

   write_item(ignored_dir, "ITM-IGNORED", "01", "mcq", "no_calculator", template_provenance)

   return root


def draw(root, out_path, stems_path=None, seed=7):
   argv = [str(out_path), "--size", "20", "--seed", str(seed), "--content-root", str(root)]

   if stems_path is not None:
      argv += ["--stems-only", str(stems_path)]

   assert draw_today_audit_sample.main(argv) == 0

   return json.loads(out_path.read_text())


def walk_keys(node):
   if isinstance(node, dict):
      for key, value in node.items():
         yield key
         yield from walk_keys(value)
   elif isinstance(node, list):
      for value in node:
         yield from walk_keys(value)


def test_the_same_seed_draws_the_same_items(tmp_path):
   root = build_bank(tmp_path / "content")

   first = draw(root, tmp_path / "first.json")
   second = draw(root, tmp_path / "second.json")

   first_ids = [row["item_id"] for row in first["sample"]]
   second_ids = [row["item_id"] for row in second["sample"]]

   assert len(first_ids) == 20
   assert first_ids == second_ids


def test_every_short_answer_item_is_drawn_when_the_bank_holds_fewer_than_the_floor(tmp_path):
   root = build_bank(tmp_path / "content")

   drawn = draw(root, tmp_path / "sample.json")
   short_answers = [row for row in drawn["sample"] if row["format"] == "short_answer"]

   assert drawn["strata_counts"]["format"] == {"mcq": 100, "short_answer": 3}
   assert len(drawn["sample"]) == 20
   assert len(short_answers) == 3


def test_the_stems_only_file_carries_no_key_and_no_rationale(tmp_path):
   root = build_bank(tmp_path / "content")
   stems_path = tmp_path / "stems.json"

   drawn = draw(root, tmp_path / "sample.json", stems_path)
   stems = json.loads(stems_path.read_text())
   keys_present = set(walk_keys(stems))

   assert len(stems["items"]) == len(drawn["sample"]) == 20
   assert all(item["options"] for item in stems["items"])
   assert "stem" in keys_present
   assert keys_present.isdisjoint(LEAKING_KEYS), keys_present & LEAKING_KEYS
