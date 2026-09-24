"""The duplicate gate measured on the labelled sample it was validated on (docs/plan/11 P4:
test_minhash_threshold and eval_duplicate_gate_labelled; docs/operator/duplicate-gate/).

final.json was built after the thresholds were set and never used to set them. Its pairs hold no
official text: an official side is a page and an offset, rebuilt from cache/text at run time.
"""
import json
from pathlib import Path

import pytest

from app.generation import dedupe
from tools import duplicate_sample

SAMPLE = Path(__file__).resolve().parents[2] / "docs" / "operator" / "duplicate-gate" / "final.json"


@pytest.fixture(scope="module")
def scored():
   sample = json.loads(SAMPLE.read_text())
   pairs = duplicate_sample.rebuilt_pairs(sample)
   model = dedupe.DuplicateGate.from_cache().tfidf
   features = duplicate_sample.pair_features(sample, pairs, model)

   return sample, pairs, features


def test_minhash_threshold(scored):
   sample, pairs, features = scored
   labels = [pair["label"] for pair in sample["pairs"]]

   assert (dedupe.SHINGLE_SIZE, dedupe.JACCARD_THRESHOLD, dedupe.NUM_HASHES) == (5, 0.8, 256)

   flagged = [duplicate_sample.stage_one_flags(feature) for feature in features]
   rates = duplicate_sample.rates(flagged, labels)

   assert rates["false_positive"] == 0
   assert rates["true_positive"] >= 20

   for (text_a, text_b), flag in zip(pairs, flagged):
      if not flag:
         continue

      shared_bucket = set(dedupe.lsh_band_keys(dedupe.minhash_signature(dedupe.shingles(dedupe.normalise(text_a))))) & set(
         dedupe.lsh_band_keys(dedupe.minhash_signature(dedupe.shingles(dedupe.normalise(text_b))))
      )

      assert shared_bucket, "a pair at Jaccard 0.8 or more shares no LSH bucket, so the bank search would miss it"


def test_eval_duplicate_gate_labelled(scored):
   sample, _pairs, features = scored
   labels = [pair["label"] for pair in sample["pairs"]]
   categories = [pair["category"] for pair in sample["pairs"]]
   flagged = [
      duplicate_sample.stage_one_flags(feature) or duplicate_sample.adopted_stage_two_flags(feature)
      for feature in features
   ]
   rates = duplicate_sample.rates(flagged, labels)
   missed_categories = {categories[index] for index in rates["missed_pairs"]}

   assert rates["precision"] == 1.0
   assert missed_categories <= {"official paraphrase"}

   for category, flag in zip(categories, flagged):
      is_light_edit = category in ("official light edit", "bank light edit", "bank reformatted", "bank paraphrase")
      is_sibling = category == "bank sibling, other numbers"

      if is_light_edit:
         assert flag, f"a {category} pair was not blocked"

      if is_sibling:
         assert not flag, "two draws of one template with other numbers were called duplicates"


def test_two_draws_with_shared_boilerplate_and_other_numbers_are_not_copies():
   """Two published draws of one template whose math segments overlap above the 0.80 line but
   whose numbers differ: the numbers condition is what keeps the bank from calling them copies."""
   content = Path(__file__).resolve().parents[2] / "content" / "items_gen_unit06"
   first = json.loads((content / "ITM-GEN-99010-09.json").read_text())
   second = json.loads((content / "ITM-GEN-99010-03.json").read_text())
   gate = dedupe.DuplicateGate([], [first, second])

   math_overlap = dedupe.multiset_jaccard(
      dedupe.math_pairs(dedupe.problem_text(first)), dedupe.math_pairs(dedupe.problem_text(second))
   )

   assert math_overlap >= dedupe.BANK_MATH_THRESHOLD
   assert not gate.check(first).stage_two.hit
