"""Tests for the question standards of app/items/standards.py as tools/check_items.py enforces
them: docs/pedagogy/today/question-standards.md section 12.

Every red fixture starts from one real agent draft, content/items_p1_agent/ITM-AGT-02008-01.json,
and changes one field of it. No record in content/items_p1_agent carries a derivation or a
mechanism on its distractors, so the clean base adds a derivation to each distractor and is
otherwise the record as it stands.
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from app.items.standards import (
   BANK_STATISTIC_MINIMUM,
   LINTS,
   STEM_WORD_CAP,
   key_letter_distribution,
   statement_longest_key_share,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ITEMS_FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "items_p1"
BASE_RECORD_PATH = REPOSITORY_ROOT / "content" / "items_p1_agent" / "ITM-AGT-02008-01.json"


def clean_base_record():
   record = json.loads(BASE_RECORD_PATH.read_text())

   for option in record["options"]:
      is_distractor = option["is_key"] is not True

      if is_distractor:
         option["derivation"] = f"the slip {option['error_path']} names, applied to the quotient"

   return record


def distractor(record, option_id):
   return next(option for option in record["options"] if option["id"] == option_id)


def drop_one_distractor(record):
   record["options"] = [option for option in record["options"] if option["id"] != "D"]


def share_an_error_path(record):
   distractor(record, "A")["error_path"] = distractor(record, "B")["error_path"]


def put_a_free_variable_in_a_value_option(record):
   distractor(record, "D")["value"] = ["Multiply", "Pi", "x"]


def mark_calculator(record):
   record["calculator_status"] = "calculator"


def word_the_stem_as_a_choice(record):
   record["stem"]["text"] = (
      "Let g(x) = (x^2 cos(x))/(x + 1) for x > -1. Which of the following is the exact value of g'(pi)?"
   )


def drop_the_command_verb(record):
   record["stem"]["text"] = "Let g(x) = (x^2 cos(x))/(x + 1) for x > -1. Give the exact value of g'(pi)."


def lengthen_the_stem(record):
   padding = " ".join(["The function g is differentiable on its domain."] * 20)
   record["stem"]["text"] = f"{record['stem']['text']} {padding}"


def strip_a_derivation(record):
   del distractor(record, "A")["derivation"]


def label_a_composite_option(record):
   distractor(record, "A")["label"] = "None of the above"


MUTATIONS = {
   "option_count": drop_one_distractor,
   "distinct_error_paths": share_an_error_path,
   "value_option_type": put_a_free_variable_in_a_value_option,
   "calculator_decimals": mark_calculator,
   "choice_worded_short_answer": word_the_stem_as_a_choice,
   "command_verb": drop_the_command_verb,
   "stem_length": lengthen_the_stem,
   "distractor_provenance": strip_a_derivation,
   "no_all_none": label_a_composite_option,
}


def write_record_directory(tmp_path, record):
   directory = tmp_path / "items"
   directory.mkdir()
   (directory / f"{record['id']}.json").write_text(json.dumps(record))

   return directory


def run_check_items(*arguments):
   return subprocess.run(
      [sys.executable, "tools/check_items.py", *[str(argument) for argument in arguments]],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )


def named_standards(stdout):
   named = set()

   for line in stdout.splitlines():
      is_standard_line = line.startswith("  standard ")

      if is_standard_line:
         named.add(line.split()[1].rstrip(":"))

   return named


def test_every_lint_has_a_red_fixture():
   assert set(MUTATIONS) == set(LINTS)


def test_the_clean_base_record_passes_every_lint(tmp_path):
   directory = write_record_directory(tmp_path, clean_base_record())

   result = run_check_items("--standards", directory)

   assert named_standards(result.stdout) == set(), result.stdout
   assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("lint_name", sorted(MUTATIONS))
def test_the_red_fixture_is_named_by_its_lint_and_no_other(tmp_path, lint_name):
   record = clean_base_record()
   MUTATIONS[lint_name](record)
   directory = write_record_directory(tmp_path, record)

   result = run_check_items("--standards", directory)

   assert named_standards(result.stdout) == {lint_name}, result.stdout
   assert result.returncode == 1, result.stdout + result.stderr


def test_the_stem_length_fixture_is_over_the_cap():
   record = clean_base_record()
   lengthen_the_stem(record)

   assert len(record["stem"]["text"].split()) > STEM_WORD_CAP


def test_the_json_report_carries_the_lint_per_record(tmp_path):
   record = clean_base_record()
   share_an_error_path(record)
   directory = write_record_directory(tmp_path, record)
   json_path = tmp_path / "out" / "standards.json"

   run_check_items("--standards", "--json", json_path, directory)

   written = json.loads(json_path.read_text())

   assert "distinct_error_paths" in written["records"][record["id"]]["lints"]


def test_check_items_still_exits_zero_on_the_synthetic_fixture_without_a_flag():
   result = run_check_items(ITEMS_FIXTURE_DIR)

   assert result.returncode == 0, result.stdout + result.stderr


def test_the_bank_statistics_flag_a_lopsided_bank():
   record = clean_base_record()
   records = [record] * BANK_STATISTIC_MINIMUM

   statement_record = {
      "answer_key": {"form": "statement", "label": "the longest sentence of the two"},
      "options": [
         {"id": "A", "is_key": True, "label": "the longest sentence of the two"},
         {"id": "B", "is_key": False, "label": "short"},
      ],
   }
   statement_records = [statement_record] * BANK_STATISTIC_MINIMUM

   assert key_letter_distribution(records)["flagged"] is True
   assert statement_longest_key_share(statement_records)["flagged"] is True
