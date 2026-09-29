"""Replaying every staging file must rebuild the committed registries.

tools/merge_staging.py is documented as the only writer of the registries, so a replay of
data/staging over the committed data/ has to land where data/ already is. On 2026-09-29 it did not:
whole-record snapshots replayed after the derived-link files took links back out (BC-PT-99068 from
BC-QA-99004, BC-FRQ-2014-Q3-C from BC-PT-99080) and every replayed record had its created date
rewritten to the day of the replay.
"""
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import merge_staging  # noqa: E402
import mint_id  # noqa: E402

REGISTRIES = (
   "archetypes",
   "diagnostic_signals",
   "errors",
   "frq_records",
   "mcq_records",
   "misconceptions",
   "scoring_points",
   "skills",
   "taxonomies",
)
REPLAY_DATES = ("updated",)


def without_replay_dates(value):
   if isinstance(value, dict):
      return {name: without_replay_dates(item) for name, item in value.items() if name not in REPLAY_DATES}

   if isinstance(value, list):
      return [without_replay_dates(item) for item in value]

   return value


@pytest.fixture(scope="module")
def replayed(tmp_path_factory):
   data = tmp_path_factory.mktemp("data")
   shutil.copytree(ROOT / "data", data, dirs_exist_ok=True)
   patch = pytest.MonkeyPatch()
   patch.setattr(merge_staging, "DATA", data)
   patch.setattr(merge_staging, "STAGING", data / "staging")
   patch.setattr(mint_id, "IDS", data / "ids.json")
   patch.setattr(sys, "argv", ["merge_staging.py"])

   try:
      merge_staging.main()
   finally:
      patch.undo()

   return data


@pytest.mark.parametrize("registry", REGISTRIES)
def test_replaying_every_staging_file_rebuilds_the_committed_registry(replayed, registry):
   committed = json.loads((ROOT / "data" / f"{registry}.json").read_text())
   rebuilt = json.loads((replayed / f"{registry}.json").read_text())

   assert without_replay_dates(rebuilt) == without_replay_dates(committed)
