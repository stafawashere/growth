"""The P3 grader evals of docs/plan/11, replayed from recorded calls: eval_grader_against_operator_goldens,
eval_leniency_calibration and eval_transcription_error_share. tools/p3_evals.py records the calls on
the operator's Claude subscription and publishes docs/operator/p3-grader-eval.md with its measures
in p3-grader-eval.json; these evals replay the books, fail on any call the books do not hold, and
fail if a published number no longer matches the replay."""
import json
from collections import Counter
from pathlib import Path

import pytest

from app.frq.bank import read_labels
from app.grading import evaluate
from tools import p3_evals

REPO_ROOT = Path(__file__).resolve().parents[2]
MINIMUM_POINT_TYPES = 30
RESPONSES_PER_POINT_TYPE = 5


@pytest.fixture(scope="module")
def replayed():
   return p3_evals.measures()


@pytest.fixture(scope="module")
def published():
   return json.loads(p3_evals.MEASURES_PATH.read_text())


def test_golden_set_2_covers_thirty_point_types_that_reach_the_model_in_every_category():
   records, responses, authors = evaluate.load_goldens()
   labels = read_labels()
   per_type = Counter()
   categories = {}

   for response in responses:
      record = records[response["item_id"]]
      points = {point["point_id"] for part in record["parts"] for point in part["points"]}

      assert set(response["labels"]) == points, response["id"]
      assert evaluate.reaches_a_model(record, response["target_point"], labels), response["id"]

      per_type[response["target_point_type"]] += 1
      categories.setdefault(response["target_point_type"], set()).add(response["category"])

   assert len(per_type) >= MINIMUM_POINT_TYPES
   assert set(per_type.values()) == {RESPONSES_PER_POINT_TYPE}
   assert all(found == set(evaluate.CATEGORIES) for found in categories.values())
   assert all("model-authored" in author and "not human" in author for author in authors)


def eval_grader_against_operator_goldens(replayed, published):
   measured, goldens, _authors, _transcription = replayed
   overall = measured["goldens"]["overall"]

   assert measured["misses"] == 0
   assert overall["targets"] == MINIMUM_POINT_TYPES * RESPONSES_PER_POINT_TYPE
   assert overall["published"] + overall["escalated"] == overall["targets"]
   assert overall["exact_agreement"] is not None
   assert measured["goldens"] == published["goldens"]
   assert len(goldens.rows) == overall["targets"]


def eval_leniency_calibration(replayed, published):
   measured, _goldens, _authors, _transcription = replayed
   overall = measured["goldens"]["overall"]

   assert overall["reached_the_model"] > 0
   assert overall["standard_sample_mae"] is not None
   assert overall["strict_sample_mae"] is not None
   assert overall["standard_sample_mae"] == published["goldens"]["overall"]["standard_sample_mae"]
   assert overall["strict_sample_mae"] == published["goldens"]["overall"]["strict_sample_mae"]


def eval_transcription_error_share(replayed, published):
   measured, _goldens, _authors, _transcription = replayed
   transcription = measured["transcription"]

   assert measured["misses"] == 0
   assert transcription["pages"] == 20
   assert transcription["error_share"]["pages"] > 0
   assert transcription == published["transcription"]


def test_the_published_record_names_its_authors_and_its_denominators(published):
   text = p3_evals.RECORD_PATH.read_text()
   overall = published["goldens"]["overall"]

   assert "not human" in text
   assert f"**{overall['exact_agreement']}** ({overall['published']} points)" in text
   assert "rendered stand-in" in text
