"""tools/check_lesson_designs.py: every rule has a red fixture that fails it, the clean designs
pass every rule, and the directory mode reports manifest coverage. The fixtures under
tests/fixtures/lesson_designs/ are the reference designs with one defect planted each, written by
make_red_fixtures.py, so a rule that stops firing turns its own test red."""
from pathlib import Path

import pytest

from tools import check_lesson_designs
from tools.check_lesson_designs import Context, Design, check_design, check_paths

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "lesson_designs"
CLEAN_FILES = sorted((FIXTURE_DIR / "clean").glob("*.md"))
RED_FILES = sorted(path for path in FIXTURE_DIR.glob("red_*/*.md"))


@pytest.fixture(scope="module")
def context(snapshot):
   return Context(snapshot)


def rule_named_by(path):
   return path.parent.name[len("red_"):]


def design_of(path):
   return Design(path, path.read_text())


def test_every_rule_has_a_red_fixture():
   named = {rule_named_by(path) for path in RED_FILES}

   assert named == set(check_lesson_designs.RULES)


@pytest.mark.parametrize("path", RED_FILES, ids=[f"{p.parent.name}/{p.name}" for p in RED_FILES])
def test_red_fixture_fails_its_named_rule(path, context):
   rule = rule_named_by(path)
   findings = check_design(design_of(path), context)

   assert rule in findings, f"{path.parent.name} did not fail {rule}: {sorted(findings)}"


@pytest.mark.parametrize("path", CLEAN_FILES, ids=[p.name for p in CLEAN_FILES])
def test_clean_design_passes_every_rule(path, context):
   findings = check_design(design_of(path), context)

   assert findings == {}


def test_directory_mode_reports_missing_manifest_ids(context):
   report = check_paths([FIXTURE_DIR / "clean"], context, check_coverage=True)
   coverage = report["findings_by_file"]["<manifest coverage>"]["coverage"]
   missing = [message for message in coverage if message.startswith("manifest id without a design")]

   assert report["file_count"] == len(CLEAN_FILES)
   assert len(missing) == len(context.manifest) - len(CLEAN_FILES)


def test_directory_mode_reports_a_design_outside_the_manifest(tmp_path, context):
   stray = tmp_path / "LSN-CON-99999.md"
   stray.write_text(CLEAN_FILES[0].read_text())
   report = check_paths([tmp_path], context, check_coverage=True)
   coverage = report["findings_by_file"]["<manifest coverage>"]["coverage"]

   assert "design without a manifest id: LSN-CON-99999" in coverage


def test_support_documents_get_the_dash_rule_only(tmp_path, context):
   (tmp_path / "README.md").write_text("---\ntitle: t\nresearch_date: d\nstatus: s\npurpose: p\n---\n\nplain – dash\n")
   report = check_paths([tmp_path], context)
   findings = report["findings_by_file"][str(tmp_path / "README.md")]

   assert list(findings) == ["support"]
   assert any("en dash" in message for message in findings["support"])


def test_cli_exits_zero_on_the_clean_fixtures(capsys):
   exit_code = check_lesson_designs.main(["check_lesson_designs.py", str(FIXTURE_DIR / "clean")])
   output = capsys.readouterr().out

   assert exit_code == 0
   assert "with findings: 0" in output


def test_cli_exits_nonzero_on_a_red_fixture(capsys):
   exit_code = check_lesson_designs.main(["check_lesson_designs.py", str(FIXTURE_DIR / "red_style")])
   output = capsys.readouterr().out

   assert exit_code == 1
   assert "style:" in output


def test_manifest_counts_match_the_snapshot(snapshot, context):
   kinds = {}

   for entry in context.manifest.values():
      kinds[entry["kind"]] = kinds.get(entry["kind"], 0) + 1

   assert kinds["concept"] == len(snapshot.concepts)
   assert kinds["prerequisite"] == len(snapshot.prerequisites)
   assert kinds["decision"] == len(check_lesson_designs.confusable_sets(snapshot))


def test_a_strategy_cue_over_its_cap_fails_caps(tmp_path, context):
   clean = FIXTURE_DIR / "clean" / "LSN-CON-02013.md"
   record_text = clean.read_text()
   design = design_of(clean)
   cue = design.record["strategy"][0]["cue"]
   long_cue = " ".join(["word"] * 21)
   planted = tmp_path / "LSN-CON-02013.md"
   planted.write_text(record_text.replace(cue, long_cue, 1))
   findings = check_design(design_of(planted), context)

   assert any(message.startswith("st-1 cue has 21 words") for message in findings.get("caps", []))
