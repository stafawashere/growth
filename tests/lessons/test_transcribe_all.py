"""tools/lesson_transcribe_all.py: many designs through a worker pool, one line per design, a
summary line, and exit 1 when any design was refused."""
import json
import os
import subprocess
import sys

from tests.lessons.conftest import REPO_ROOT

SCRIPT = REPO_ROOT / "tools" / "lesson_transcribe_all.py"
CLEAN_DESIGN = REPO_ROOT / "tests" / "fixtures" / "lesson_designs" / "clean" / "LSN-CON-02013.md"


def run_driver(*arguments):
   environment = dict(os.environ, PYTHONPATH=str(REPO_ROOT))
   completed = subprocess.run(
      [sys.executable, str(SCRIPT), "--workers", "2", *arguments],
      cwd=REPO_ROOT,
      env=environment,
      capture_output=True,
      text=True,
      timeout=240,
   )

   return completed.returncode, completed.stdout


def test_a_clean_design_is_written_and_counted(tmp_path):
   out_dir = tmp_path / "records"

   exit_code, output = run_driver("--out-dir", str(out_dir), str(CLEAN_DESIGN))

   assert exit_code == 0
   assert f"wrote {out_dir / 'LSN-CON-02013.json'}" in output
   assert output.splitlines()[-1] == "designs: 1, wrote: 1, refused: 0"
   assert json.loads((out_dir / "LSN-CON-02013.json").read_text())["sections"][0]["type"] == "prediction"


def test_a_refused_design_is_named_and_fails_the_run(tmp_path):
   designs = tmp_path / "designs"
   designs.mkdir()
   (designs / "LSN-CON-02013.md").write_text(CLEAN_DESIGN.read_text())
   broken = designs / "LSN-CON-02014.md"
   broken.write_text(CLEAN_DESIGN.read_text().replace('"fix_prompt": false,', "", 1))
   out_dir = tmp_path / "records"

   exit_code, output = run_driver("--out-dir", str(out_dir), str(designs))

   assert exit_code == 1
   assert f"refused {broken}: err-BC-ERR-02023.fix_prompt is missing" in output
   assert output.splitlines()[-1] == "designs: 2, wrote: 1, refused: 1"
