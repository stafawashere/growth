"""tools/key_audit_worksheet.py: the operator solves each sampled item without seeing the key
(docs/plan/10-quality-and-evaluation.md, "The audit"), so the worksheet must carry every sampled
stem and option and never mark which option is the key or print the stored answer."""
import json
from pathlib import Path

from tools import key_audit_worksheet

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
AGENT_DIR = REPOSITORY_ROOT / "content" / "items_p1_agent"
SAMPLED = ["ITM-AGT-01004-00", "ITM-AGT-02011-03", "ITM-AGT-03005-09"]


def test_the_worksheet_carries_every_stem_and_hides_every_key(tmp_path):
   sample_path = tmp_path / "sample.json"
   sample_path.write_text(json.dumps(SAMPLED))
   worksheet_path = tmp_path / "worksheet.md"
   template_path = tmp_path / "verdicts.json"

   exit_code = key_audit_worksheet.main(
      ["worksheet", str(sample_path), str(worksheet_path), str(template_path), "--items-dir", str(AGENT_DIR)]
   )
   worksheet = worksheet_path.read_text()
   template = json.loads(template_path.read_text())

   assert exit_code == 0
   assert [record["item_id"] for record in template] == SAMPLED
   assert all(record["verdict"] is None for record in template)

   for item_id in SAMPLED:
      record = json.loads((AGENT_DIR / f"{item_id}.json").read_text())
      key_option = next(option["id"] for option in record["options"] if option["is_key"])

      assert record["stem"]["text"] in worksheet
      assert f"({key_option})" in worksheet

   lowered = worksheet.lower()

   for giveaway in ("is_key", "answer_key", "worked_solution", "key:", "answer:", "correct"):
      assert giveaway not in lowered, giveaway


def test_the_worksheet_finds_items_across_several_banks(tmp_path):
   """A gate 29 sample over Units 4 to 10 draws from several content/items_unitNN_agent banks."""
   other_bank = tmp_path / "other_bank"
   other_bank.mkdir()
   record = json.loads((AGENT_DIR / "ITM-AGT-01004-00.json").read_text())
   record["id"] = "ITM-AGT-01004-90"
   (other_bank / "ITM-AGT-01004-90.json").write_text(json.dumps(record))
   sample = ["ITM-AGT-02011-03", "ITM-AGT-01004-90"]
   sample_path = tmp_path / "sample.json"
   sample_path.write_text(json.dumps(sample))
   worksheet_path = tmp_path / "worksheet.md"

   exit_code = key_audit_worksheet.main(
      [
         "worksheet", str(sample_path), str(worksheet_path), str(tmp_path / "verdicts.json"),
         "--items-dir", str(AGENT_DIR), "--items-dir", str(other_bank),
      ]
   )

   assert exit_code == 0
   assert "## ITM-AGT-01004-90" in worksheet_path.read_text()
   assert "## ITM-AGT-02011-03" in worksheet_path.read_text()
