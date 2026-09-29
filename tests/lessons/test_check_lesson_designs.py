"""tools/check_lesson_designs.py: every rule has a red fixture that fails it, the clean designs
pass every rule, and the directory mode reports manifest coverage. The fixtures under
tests/fixtures/lesson_designs/ are the reference designs with one defect planted each, written by
make_red_fixtures.py, so a rule that stops firing turns its own test red."""
import json
import re
from pathlib import Path

import pytest

from tools import check_lesson_designs
from tools.check_lesson_designs import Context, Design, check_design, check_paths

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "lesson_designs"
CLEAN_FILES = sorted((FIXTURE_DIR / "clean").glob("*.md"))
RED_FILES = sorted(path for path in FIXTURE_DIR.glob("red_*/*.md"))
FENCE = re.compile(r"```json\n(.*?)\n```", re.S)


@pytest.fixture(scope="module")
def context(snapshot):
   return Context(snapshot)


def rule_named_by(path):
   stem = path.parent.name[len("red_"):]

   return stem.split("__")[0]


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


CLEAN_CONCEPT = FIXTURE_DIR / "clean" / "LSN-CON-02013.md"
CLEAN_DECISION = FIXTURE_DIR / "clean" / "LSN-DEC-06-01.md"


def planted_design(tmp_path, source, change):
   design = design_of(source)
   change(design.record)
   planted = tmp_path / source.name
   planted.write_text(with_record(source.read_text(), design.record))

   return design_of(planted)


def with_record(text, record):
   replacement = "```json\n" + json.dumps(record, indent=1, ensure_ascii=False) + "\n```"

   return FENCE.sub(lambda match: replacement, text)


def test_a_design_without_the_prediction_heading_fails_sections(tmp_path, context):
   planted = tmp_path / CLEAN_CONCEPT.name
   planted.write_text(CLEAN_CONCEPT.read_text().replace("\n## Prediction\n", "\n## Predict\n"))
   findings = check_design(design_of(planted), context)

   assert "section missing: Prediction" in findings.get("sections", [])


def test_a_prediction_heading_after_the_orientation_fails_sections(tmp_path, context):
   text = CLEAN_CONCEPT.read_text()
   prediction_start = text.index("## Prediction\n")
   orientation_start = text.index("## Orientation\n")
   key_ideas_start = text.index("## Key ideas\n")
   prediction_block = text[prediction_start:orientation_start]
   orientation_block = text[orientation_start:key_ideas_start]
   swapped = text[:prediction_start] + orientation_block + prediction_block + text[key_ideas_start:]
   planted = tmp_path / CLEAN_CONCEPT.name
   planted.write_text(swapped)
   findings = check_design(design_of(planted), context)

   assert "sections are not in template order" in findings.get("sections", [])


def short_answer_prediction(expr):
   def change(record):
      prediction = record["prediction"]
      prediction["format"] = "short_answer"
      prediction.pop("options")
      prediction["key"] = {"form": "symbolic", "expr": expr}

   return change


def test_a_short_answer_prediction_key_must_come_from_example_one(tmp_path, context):
   good = planted_design(tmp_path, CLEAN_CONCEPT, short_answer_prediction("2*x*cos(x) - (x**2+3)*sin(x)"))
   good_messages = check_lesson_designs.rule_prediction_section(good, context)
   bad = planted_design(tmp_path, CLEAN_CONCEPT, short_answer_prediction("2*x*(-sin(x))"))
   bad_messages = check_lesson_designs.rule_prediction_section(bad, context)

   assert good_messages == []
   assert any("key is neither the answer of ex-1" in message for message in bad_messages)


def test_a_prediction_with_two_keys_fails(tmp_path, context):
   def change(record):
      record["prediction"]["options"][0]["is_key"] = True

   design = planted_design(tmp_path, CLEAN_CONCEPT, change)
   messages = check_lesson_designs.rule_prediction_section(design, context)

   assert any("2 key options" in message for message in messages)


def test_a_decision_design_with_a_prediction_fails(tmp_path, context):
   def change(record):
      record["prediction"] = design_of(CLEAN_CONCEPT).record["prediction"]

   design = planted_design(tmp_path, CLEAN_DECISION, change)
   findings = check_design(design, context)

   assert findings.get("prediction_section") == ["a decision lesson carries no prediction"]


def test_the_decision_design_is_exempt_from_the_concept_only_rules(context):
   design = design_of(CLEAN_DECISION)

   for rule in ("prediction_section", "contrast", "fade", "fix_prompt", "figure_presence"):
      assert check_lesson_designs.RULES[rule](design, context) == []


def test_a_fade_outside_the_steps_fails(tmp_path, context):
   def change(record):
      record["worked_examples"][1]["fade_from"] = 9

   design = planted_design(tmp_path, CLEAN_CONCEPT, change)
   messages = check_lesson_designs.rule_fade(design, context)

   assert "ex-2 fade_from 9 is outside 2 to 3" in messages


def test_a_drawn_block_with_a_no_figure_reason_fails(tmp_path, context):
   def change(record):
      record["delivery"][0] = {
         "block": "orientation",
         "mode": "figure",
         "reason": "planted",
         "spec": {"kind": "graph"},
         "fallback": "f",
         "keyboard": "k",
      }

   design = planted_design(tmp_path, CLEAN_CONCEPT, change)
   messages = check_lesson_designs.rule_figure_presence(design, context)

   assert messages == ["the lesson draws orientation and carries no_figure_reason"]


def test_a_method_opening_with_the_reader_label_fails_served_text(tmp_path, context):
   def change(record):
      record["strategy"][1]["method"] = "First line: record the four supplied values."

   design = planted_design(tmp_path, CLEAN_CONCEPT, change)
   messages = check_lesson_designs.rule_served_text(design, context)

   assert messages == ["st-2 method starts with the reader's label 'First line:'"]


def test_a_rival_opening_with_the_reader_label_fails_served_text(context):
   design = design_of(FIXTURE_DIR / "red_served_text__rival" / "LSN-CON-02013.md")
   messages = check_lesson_designs.rule_served_text(design, context)

   assert messages == ["st-1 rival starts with the reader's label 'Rival:'"]


def test_a_prediction_stem_opening_with_the_reader_label_fails_served_text(context):
   design = design_of(FIXTURE_DIR / "red_served_text__prediction" / "LSN-CON-02013.md")
   messages = check_lesson_designs.rule_served_text(design, context)

   assert messages == ["pr-1 stem.text starts with the reader's label 'Predict.'"]


def test_the_prediction_and_contrast_count_in_both_bands(context):
   record = design_of(CLEAN_CONCEPT).record
   without = dict(record)
   without.pop("prediction")
   without["strategy"] = [dict(block) for block in record["strategy"]]
   without["strategy"][0].pop("contrast")
   added = check_lesson_designs.prediction_words(record["prediction"])
   added += check_lesson_designs.contrast_words(record["strategy"][0]["contrast"])

   for band in ("low", "mid"):
      difference = check_lesson_designs.band_words(record, band) - check_lesson_designs.band_words(without, band)

      assert difference == added


def test_a_prediction_may_name_one_delivery(tmp_path, context):
   def change(record):
      record["delivery"].append({"block": "pr-1", "mode": "text", "reason": "rule 5"})

   design = planted_design(tmp_path, CLEAN_CONCEPT, change)

   assert check_lesson_designs.rule_delivery(design, context) == []
