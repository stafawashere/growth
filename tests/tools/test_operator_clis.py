"""Tests for the two operator command-line tools, tools/check_items.py and
tools/check_audit_verdicts.py: docs/plan/11-phased-delivery.md P1 items 17, 29 and 30,
exit criteria 4 and 7, and remaining implementer decision 5.

Both tools are read-only checkers over files the operator hands them, so every test here
either drives the real CLI as a subprocess or asserts against a source the tools themselves
read, never a hand-copied duplicate of that source.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from app.review.audit import VERDICT_AMBIGUOUS, VERDICT_CLEAN, VERDICT_KEY_WRONG
from tools.build_p1_fixture import P1_ARCHETYPES

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ITEMS_FIXTURE_DIR = REPOSITORY_ROOT / "tests" / "fixtures" / "items_p1"
DATA_DIR = REPOSITORY_ROOT / "data"


def run_check_items(directory):
   return subprocess.run(
      [sys.executable, "tools/check_items.py", str(directory)],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )


def run_check_verdicts(verdicts_path, sample_path):
   return subprocess.run(
      [sys.executable, "tools/check_audit_verdicts.py", str(verdicts_path), str(sample_path)],
      cwd=REPOSITORY_ROOT,
      capture_output=True,
      text=True,
   )


def fixture_ids_and_archetypes():
   mapping = {}

   for path in sorted(ITEMS_FIXTURE_DIR.glob("*.json")):
      record = json.loads(path.read_text())
      mapping[record["id"]] = record["archetype_id"]

   return mapping


def broken_record_directory(tmp_path):
   source = ITEMS_FIXTURE_DIR / "ITM-SYN-01008-00.json"
   record = json.loads(source.read_text())
   record["answer_key"]["mathjson"] = 999

   broken_dir = tmp_path / "broken_items"
   broken_dir.mkdir()
   (broken_dir / "ITM-SYN-01008-00.json").write_text(json.dumps(record))

   return broken_dir, record["id"]


def directory_digest(root):
   hasher = hashlib.sha256()

   for path in sorted(root.rglob("*")):
      is_file = path.is_file()

      if not is_file:
         continue

      hasher.update(str(path.relative_to(root)).encode("utf-8"))
      hasher.update(path.read_bytes())

   return hasher.hexdigest()


def test_check_items_exits_zero_on_the_synthetic_fixture_directory():
   result = run_check_items(ITEMS_FIXTURE_DIR)

   assert result.returncode == 0, result.stdout + result.stderr


def test_check_items_names_the_violations_of_a_broken_record(tmp_path):
   broken_dir, item_id = broken_record_directory(tmp_path)

   result = run_check_items(broken_dir)

   assert item_id in result.stdout
   assert "sympy_equivalence" in result.stdout
   assert "numeric_probe" in result.stdout


def test_check_items_exits_one_when_a_record_is_broken(tmp_path):
   broken_dir, _ = broken_record_directory(tmp_path)

   result = run_check_items(broken_dir)

   assert result.returncode == 1


def test_check_items_counts_per_archetype():
   fixture_mapping = fixture_ids_and_archetypes()
   expected_counts = {archetype_id: 0 for archetype_id in P1_ARCHETYPES}

   for archetype_id in fixture_mapping.values():
      is_a_p1_archetype = archetype_id in expected_counts

      if is_a_p1_archetype:
         expected_counts[archetype_id] += 1

   result = run_check_items(ITEMS_FIXTURE_DIR)

   assert result.returncode == 0, result.stdout + result.stderr

   for archetype_id, count in expected_counts.items():
      assert f"{archetype_id}: {count}" in result.stdout


def test_check_items_rejects_an_error_path_held_only_by_another_archetype(tmp_path):
   """BC-ERR-02015 is held by a skill of BC-QA-02006, a P1 archetype, but by none of BC-QA-01004's
   skills, so a BC-QA-01004 distractor citing it names an error its own archetype cannot produce."""
   record = json.loads((REPOSITORY_ROOT / "content" / "items_p1_agent" / "ITM-AGT-01004-00.json").read_text())
   distractor = next(option for option in record["options"] if option["is_key"] is False)
   distractor["error_path"] = "BC-ERR-02015"
   directory = tmp_path / "foreign_error"
   directory.mkdir()
   (directory / "ITM-AGT-01004-00.json").write_text(json.dumps(record))

   result = run_check_items(directory)

   assert result.returncode == 1, result.stdout
   assert "BC-ERR-02015" in result.stdout


def test_check_verdicts_reports_a_missing_verdict_and_exits_one(tmp_path):
   sample_ids = ["ITM-TEST-0001", "ITM-TEST-0002", "ITM-TEST-0003"]
   verdicts = [
      {
         "item_id": "ITM-TEST-0001",
         "verdict": VERDICT_CLEAN,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
      {
         "item_id": "ITM-TEST-0002",
         "verdict": VERDICT_CLEAN,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
   ]

   sample_path = tmp_path / "sample.json"
   verdicts_path = tmp_path / "verdicts.json"
   sample_path.write_text(json.dumps(sample_ids))
   verdicts_path.write_text(json.dumps(verdicts))

   result = run_check_verdicts(verdicts_path, sample_path)

   assert result.returncode == 1
   assert "ITM-TEST-0003" in result.stdout
   assert "not published" in result.stdout.lower()


def test_check_verdicts_publishes_the_rate_on_a_complete_sample(tmp_path):
   sample_ids = ["ITM-TEST-0001", "ITM-TEST-0002", "ITM-TEST-0003", "ITM-TEST-0004"]
   verdicts = [
      {
         "item_id": "ITM-TEST-0001",
         "verdict": VERDICT_CLEAN,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
      {
         "item_id": "ITM-TEST-0002",
         "verdict": VERDICT_CLEAN,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
      {
         "item_id": "ITM-TEST-0003",
         "verdict": VERDICT_KEY_WRONG,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
      {
         "item_id": "ITM-TEST-0004",
         "verdict": VERDICT_AMBIGUOUS,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
         "second_answer": "x = 2",
      },
   ]

   sample_path = tmp_path / "sample.json"
   verdicts_path = tmp_path / "verdicts.json"
   sample_path.write_text(json.dumps(sample_ids))
   verdicts_path.write_text(json.dumps(verdicts))

   result = run_check_verdicts(verdicts_path, sample_path)

   assert result.returncode == 0, result.stdout + result.stderr
   assert "0.5" in result.stdout


def test_check_verdicts_names_a_malformed_verdict(tmp_path):
   sample_ids = ["ITM-TEST-0001"]
   verdicts = [
      {
         "item_id": "ITM-TEST-0001",
         "verdict": "not_a_real_verdict",
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
   ]

   sample_path = tmp_path / "sample.json"
   verdicts_path = tmp_path / "verdicts.json"
   sample_path.write_text(json.dumps(sample_ids))
   verdicts_path.write_text(json.dumps(verdicts))

   result = run_check_verdicts(verdicts_path, sample_path)

   assert "ITM-TEST-0001" in result.stdout
   assert "not in the audit module's vocabulary" in result.stdout


def test_check_verdicts_refuses_a_verdict_outside_the_sample(tmp_path):
   sample_ids = ["ITM-TEST-0001"]
   verdicts = [
      {
         "item_id": "ITM-TEST-0001",
         "verdict": VERDICT_KEY_WRONG,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
      {
         "item_id": "ITM-TEST-0099",
         "verdict": VERDICT_KEY_WRONG,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
   ]

   sample_path = tmp_path / "sample.json"
   verdicts_path = tmp_path / "verdicts.json"
   sample_path.write_text(json.dumps(sample_ids))
   verdicts_path.write_text(json.dumps(verdicts))

   result = run_check_verdicts(verdicts_path, sample_path)

   assert result.returncode == 1, result.stdout + result.stderr
   assert "out of sample: ITM-TEST-0099" in result.stdout
   assert "key error rate: not published" in result.stdout


def test_neither_tool_writes_to_the_data_directory(tmp_path):
   sample_ids = ["ITM-TEST-0001"]
   verdicts = [
      {
         "item_id": "ITM-TEST-0001",
         "verdict": VERDICT_CLEAN,
         "auditor": "operator",
         "audited_at": "2026-09-20T00:00:00Z",
      },
   ]

   sample_path = tmp_path / "sample.json"
   verdicts_path = tmp_path / "verdicts.json"
   sample_path.write_text(json.dumps(sample_ids))
   verdicts_path.write_text(json.dumps(verdicts))

   digest_before = directory_digest(DATA_DIR)

   run_check_items(ITEMS_FIXTURE_DIR)
   run_check_verdicts(verdicts_path, sample_path)

   digest_after = directory_digest(DATA_DIR)

   assert digest_before == digest_after
