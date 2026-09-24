"""The labelled sample the duplicate gate's thresholds are validated on (docs/plan/04-item-generation.md,
"Validation on a labelled sample"; 11 P4, eval_duplicate_gate_labelled).

build   draws pairs from the committed banks and the official text cache, each labelled
        duplicate, near_duplicate or distinct by the rule that made it, and writes the sample as
        references (item ids, official page and offset, transformation and seed), never as text,
        because no official text may be committed. Each label is then read against the two texts.
score   rebuilds every pair's texts and reports each stage's precision and recall at its
        threshold, and the thresholds that hold false negatives at zero on this sample.

Usage:
  python3 tools/duplicate_sample.py build <sample.json> [--seed N]
  python3 tools/duplicate_sample.py score <sample.json> [--report out.json]
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.generation import dedupe

SEED = 20260924

SYNONYMS = {
   "find": "determine", "determine": "find", "value": "number", "function": "rule",
   "given": "stated", "shown": "displayed", "interval": "range", "approximate": "estimate",
   "rate": "speed", "measured": "recorded", "particle": "object", "moves": "travels",
   "graph": "plot", "region": "area", "total": "overall", "exact": "precise",
   "consider": "take", "where": "in which", "series": "sum", "curve": "path",
   "the": "this", "is": "equals", "of": "for", "for": "over", "at": "when",
}

FILLER_OPENERS = ("Consider the following. ", "Here is a problem. ", "Work out the answer. ")


def reformat(text, rng):
   """Case, spacing and delimiter spacing changed; nothing a reader would call a different item."""
   spaced = re.sub(r"\s+", "  ", text)

   return spaced.upper() if rng.random() < 0.5 else spaced.replace(r"\( ", r"\(").replace(r" \)", r"\)")


def light_edit(text, rng, substitutions=3):
   words = text.split(" ")
   positions = [index for index, word in enumerate(words) if word.lower().strip(".,") in SYNONYMS]
   rng.shuffle(positions)

   for index in positions[:substitutions]:
      bare = words[index].strip(".,")
      words[index] = words[index].replace(bare, SYNONYMS[bare.lower()])

   return " ".join(words)


def sentences_outside_math(text):
   """Sentences split at a full stop and a space, never inside a math segment between \\( and
   \\), where a full stop belongs to the mathematics."""
   sentences = []
   current = []
   inside_math = False
   position = 0

   while position < len(text):
      opens_math = text.startswith("\\(", position)
      closes_math = text.startswith("\\)", position)

      if opens_math or closes_math:
         inside_math = opens_math
         current.append(text[position:position + 2])
         position += 2
         continue

      character = text[position]
      current.append(character)
      ends_sentence = character == "." and not inside_math and text[position + 1:position + 2] == " "

      if ends_sentence:
         sentences.append("".join(current).strip())
         current = []

      position += 1

   if "".join(current).strip():
      sentences.append("".join(current).strip())

   return sentences


def paraphrase(text, rng):
   """Every synonym swapped, the sentences reordered and an opener added; the numbers and the
   mathematics stay, so the item is the same item in other words."""
   sentences = sentences_outside_math(text)
   rng.shuffle(sentences)
   swapped = light_edit(" ".join(sentences), rng, substitutions=len(text))

   return rng.choice(FILLER_OPENERS) + swapped


TRANSFORMS = {"reformat": reformat, "light_edit": light_edit, "paraphrase": paraphrase}


def served_and_candidate_records():
   """Only the committed banks, so every pair the sample names can be rebuilt from the repository."""
   return {record["id"]: record for record in dedupe.load_bank_records()}


def page_words(page_id):
   """The page's own words, read from the cache, for a page id such as frq-25/page-008.raw."""
   doc_id, page_name = page_id.split("/", 1)

   return (dedupe.CACHE_TEXT_DIR / doc_id / f"{page_name}.txt").read_text(errors="ignore").split()


def official_passages():
   pages = dedupe.load_official_pages()
   passages = []

   for page in pages:
      words = page_words(page.page_id)

      for start in range(0, max(len(words) - 60, 1), 120):
         span = words[start:start + 60]
         has_prose = sum(1 for word in span if word.isalpha()) >= 30

         if has_prose:
            passages.append({"page": page.page_id, "start": start, "length": 60})

   return passages


def item_side(record_id, transform=None, seed=None):
   return {"kind": "item", "id": record_id, "transform": transform, "seed": seed}


def official_side(passage, transform=None, seed=None):
   return {"kind": "official", **passage, "transform": transform, "seed": seed}


def build(path, seed=SEED):
   rng = random.Random(seed)
   records = served_and_candidate_records()
   by_archetype = {}

   for record_id, record in records.items():
      by_archetype.setdefault(record["archetype_id"], []).append(record_id)

   ids = sorted(records)
   crowded = [archetype for archetype, members in sorted(by_archetype.items()) if len(members) >= 2]
   passages = official_passages()
   pairs = []

   def add(first, second, label, category):
      pairs.append({"pair_id": len(pairs), "a": first, "b": second, "label": label, "category": category})

   for record_id in rng.sample(ids, 20):
      add(item_side(record_id), item_side(record_id, "reformat", rng.randrange(10**6)), "duplicate", "bank reformatted")

   for record_id in rng.sample(ids, 20):
      add(item_side(record_id), item_side(record_id, "light_edit", rng.randrange(10**6)), "near_duplicate", "bank light edit")

   for record_id in rng.sample(ids, 30):
      add(item_side(record_id), item_side(record_id, "paraphrase", rng.randrange(10**6)), "near_duplicate", "bank paraphrase")

   for archetype in rng.sample(crowded, min(60, len(crowded))):
      first, second = rng.sample(by_archetype[archetype], 2)
      add(item_side(first), item_side(second), "distinct", "bank sibling, other numbers")

   for _ in range(20):
      first, second = rng.sample(ids, 2)
      add(item_side(first), item_side(second), "distinct", "bank, any two items")

   for passage in rng.sample(passages, 20):
      add(official_side(passage), official_side(passage, "light_edit", rng.randrange(10**6)), "near_duplicate", "official light edit")

   for passage in rng.sample(passages, 20):
      add(official_side(passage), official_side(passage, "paraphrase", rng.randrange(10**6)), "near_duplicate", "official paraphrase")

   for record_id in rng.sample(ids, 30):
      add(item_side(record_id), official_side(rng.choice(passages)), "distinct", "generated item against official text")

   sample = {
      "labelled_by": "claude-opus-5-5 on the operator's delegation of 2026-09-24; each label is the rule that built the pair, read against the rebuilt texts",
      "seed": seed,
      "pairs": pairs,
   }
   Path(path).write_text(json.dumps(sample, indent=1) + "\n")
   print(f"{len(pairs)} pairs written to {path}")


def side_text(side, records, problem_only=False):
   if side["kind"] == "item":
      record = records[side["id"]]
      text = dedupe.problem_text(record) if problem_only else dedupe.record_text(record)
   else:
      words = page_words(side["page"])
      text = " ".join(words[side["start"]:side["start"] + side["length"]])

   transform = side.get("transform")

   if transform is None:
      return text

   return TRANSFORMS[transform](text, random.Random(side["seed"]))


def rebuilt_pairs(sample, problem_only=False):
   records = served_and_candidate_records()

   return [
      (side_text(pair["a"], records, problem_only), side_text(pair["b"], records, problem_only))
      for pair in sample["pairs"]
   ]


def math_agreement(problem_a, problem_b, text_a, text_b, model):
   """The gate's bank comparison: ordered math pairs, or for two items with no mathematics at all
   the word cosine at the published threshold (app/generation/dedupe.py stage_two_bank)."""
   pairs_a = dedupe.math_pairs(problem_a)
   pairs_b = dedupe.math_pairs(problem_b)
   neither_has_mathematics = not pairs_a and not pairs_b

   if not neither_has_mathematics:
      return dedupe.multiset_jaccard(pairs_a, pairs_b)

   word_score = dedupe.cosine(model.vector(dedupe.normalise(text_a)), model.vector(dedupe.normalise(text_b)))

   return 1.0 if word_score >= dedupe.COSINE_THRESHOLD else word_score


def pair_features(sample, pairs, model):
   features = []
   problems = rebuilt_pairs(sample, problem_only=True)

   for pair, (text_a, text_b), (problem_a, problem_b) in zip(sample["pairs"], pairs, problems):
      tokens_a = dedupe.normalise(text_a)
      tokens_b = dedupe.normalise(text_b)
      involves_official = "official" in (pair["a"]["kind"], pair["b"]["kind"])
      features.append({
         "corpus": "official" if involves_official else "bank",
         "jaccard": dedupe.exact_jaccard(dedupe.shingles(tokens_a), dedupe.shingles(tokens_b)),
         "cosine": dedupe.cosine(model.vector(tokens_a), model.vector(tokens_b)),
         "math": math_agreement(problem_a, problem_b, text_a, text_b, model),
         "numbers": dedupe.number_agreement(dedupe.numbers(problem_a), dedupe.numbers(problem_b)),
      })

   return features


def stage_one_flags(feature):
   return feature["jaccard"] >= dedupe.JACCARD_THRESHOLD


def published_stage_two_flags(feature):
   return feature["cosine"] >= dedupe.COSINE_THRESHOLD


def adopted_stage_two_flags(feature):
   if feature["corpus"] == "official":
      return feature["cosine"] >= dedupe.OFFICIAL_COSINE_THRESHOLD

   same_mathematics = feature["math"] >= dedupe.BANK_MATH_THRESHOLD
   same_numbers = feature["numbers"] >= dedupe.BANK_NUMBER_THRESHOLD

   return same_mathematics and same_numbers


def rates(flags, labels):
   positives = [label in dedupe.POSITIVE_LABELS for label in labels]
   true_positive = sum(1 for flag, positive in zip(flags, positives) if flag and positive)
   flagged = sum(flags)
   positive_count = sum(positives)

   return {
      "precision": round(true_positive / flagged, 4) if flagged else None,
      "recall": round(true_positive / positive_count, 4) if positive_count else None,
      "true_positive": true_positive,
      "false_positive": flagged - true_positive,
      "false_negative": positive_count - true_positive,
      "missed_pairs": [index for index, (flag, positive) in enumerate(zip(flags, positives)) if positive and not flag],
      "false_alarm_pairs": [index for index, (flag, positive) in enumerate(zip(flags, positives)) if flag and not positive],
   }


def score(path, report_path=None):
   """Precision and recall of each stage at the published and at the adopted operating points,
   scored with the gate's own TF-IDF model over the official passages and the served bank."""
   sample = json.loads(Path(path).read_text())
   pairs = rebuilt_pairs(sample)
   labels = [pair["label"] for pair in sample["pairs"]]
   model = dedupe.DuplicateGate.from_cache().tfidf
   features = pair_features(sample, pairs, model)
   one = [stage_one_flags(feature) for feature in features]
   published_two = [published_stage_two_flags(feature) for feature in features]
   adopted_two = [adopted_stage_two_flags(feature) for feature in features]
   by_category = {}

   for pair, feature in zip(sample["pairs"], features):
      entry = by_category.setdefault(pair["category"], {"label": pair["label"], "pairs": 0, "jaccard": [], "cosine": [], "math": [], "numbers": []})
      entry["pairs"] += 1

      for name in ("jaccard", "cosine", "math", "numbers"):
         entry[name].append(feature[name])

   summary = {
      "sample": str(path),
      "pairs": len(labels),
      "positives": sum(1 for label in labels if label in dedupe.POSITIVE_LABELS),
      "published": {
         "stage_one_jaccard_0.8": rates(one, labels),
         "stage_two_cosine_0.85": rates(published_two, labels),
         "gate": rates([first or second for first, second in zip(one, published_two)], labels),
      },
      "adopted": {
         "stage_two": rates(adopted_two, labels),
         "gate": rates([first or second for first, second in zip(one, adopted_two)], labels),
      },
      "by_category": {
         name: {
            "label": entry["label"],
            "pairs": entry["pairs"],
            **{f"{feature}_range": [round(min(entry[feature]), 3), round(max(entry[feature]), 3)] for feature in ("jaccard", "cosine", "math", "numbers")},
         }
         for name, entry in sorted(by_category.items())
      },
   }
   print(json.dumps(summary, indent=1))

   if report_path:
      Path(report_path).write_text(json.dumps(summary, indent=1) + "\n")

   return summary


def main(argv):
   parser = argparse.ArgumentParser(description="Build or score the duplicate gate's labelled sample.")
   parser.add_argument("command", choices=("build", "score"))
   parser.add_argument("sample")
   parser.add_argument("--report")
   parser.add_argument("--seed", type=int, default=SEED)
   arguments = parser.parse_args(argv)

   if arguments.command == "build":
      build(arguments.sample, arguments.seed)
   else:
      score(arguments.sample, arguments.report)

   return 0


if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))
