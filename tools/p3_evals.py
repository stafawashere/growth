"""Run the P3 grader evals and publish them to docs/operator/p3-grader-eval.md.

Usage:
   python3 tools/p3_evals.py record-goldens [--workers 4]
      grades every golden target on the operator's Claude subscription (never the API key),
      recording each call in tests/fixtures/grading_cassettes/grader_goldens.json;
   python3 tools/p3_evals.py record-transcription [--workers 3]
      renders golden set 3's pages, runs the quality gate, reads every accepted page with the
      transcriber and grades the target point from the unconfirmed read-back, recording into
      tests/fixtures/grading_cassettes/transcription_goldens.json;
   python3 tools/p3_evals.py publish
      replays both books, computes every metric and writes the record.

Never run the record commands from a test: they spend the subscription. The test suite replays
the books (tests/eval/test_p3_evals.py) and checks the published numbers against the replay.
"""
import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app.content.loader import load_snapshot
from app.frq.bank import read_labels
from app.grading import evaluate, transcription_eval
from app.grading.judge import ModelJudge
from app.providers.cassette_book import CassetteBookProvider

CASSETTES = REPO_ROOT / "tests" / "fixtures" / "grading_cassettes"
GOLDENS_BOOK = CASSETTES / "grader_goldens.json"
TRANSCRIPTION_BOOK = CASSETTES / "transcription_goldens.json"
RECORD_PATH = REPO_ROOT / "docs" / "operator" / "p3-grader-eval.md"
MEASURES_PATH = REPO_ROOT / "docs" / "operator" / "p3-grader-eval.json"


def point_types():
   return dict(load_snapshot(REPO_ROOT / "data").scoring_points)


def live_book(path):
   from app.providers.subscription import SubscriptionProvider

   return CassetteBookProvider(path=path, live=SubscriptionProvider(user_count=1), record=True)


def record_goldens(workers):
   records, responses, _authors = evaluate.load_goldens()
   labels = read_labels()
   book = live_book(GOLDENS_BOOK)
   judge = ModelJudge(book, point_types())

   def grade(response):
      return evaluate.grade_target(records[response["item_id"]], response, labels, judge)

   with ThreadPoolExecutor(max_workers=workers) as pool:
      list(pool.map(grade, responses))

   print(f"{len(book.book)} recorded grader calls in {GOLDENS_BOOK.relative_to(REPO_ROOT)}")


def record_transcription(workers):
   book = live_book(TRANSCRIPTION_BOOK)
   transcription_eval.run(book, point_types(), read_labels(), workers=workers)
   print(f"{len(book.book)} recorded calls in {TRANSCRIPTION_BOOK.relative_to(REPO_ROOT)}")


def replayed_goldens():
   """The golden run from its book, and the book, whose misses must be empty for the numbers to
   be the recorded ones."""
   records, responses, authors = evaluate.load_goldens()
   book = CassetteBookProvider(path=GOLDENS_BOOK)
   judge = ModelJudge(book, point_types())

   return evaluate.evaluate(records, responses, read_labels(), judge), authors, book


def replayed_transcription():
   book = CassetteBookProvider(path=TRANSCRIPTION_BOOK)

   return transcription_eval.run(book, point_types(), read_labels(), workers=1), book


def measures():
   goldens, authors, goldens_book = replayed_goldens()
   transcription, transcription_book = replayed_transcription()

   return {
      "goldens": goldens.as_record(),
      "transcription": transcription_eval.summary(transcription),
      "misses": len(goldens_book.misses) + len(transcription_book.misses),
   }, goldens, authors, transcription


def table(rows, header):
   lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
   lines.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)

   return "\n".join(lines)


def tally_row(name, record):
   return [
      name,
      record["targets"],
      f"{record['published']} of {record['targets']}",
      record["exact_agreement"],
      record["mean_absolute_error_per_point"],
      f"{record['escalated']} of {record['targets']}",
      record["single_sample_agreement"],
   ]


def publish():
   measured_all, goldens, authors, transcription = measures()

   if measured_all["misses"]:
      raise SystemExit(f"{measured_all['misses']} calls are missing from the books; record again")

   MEASURES_PATH.write_text(json.dumps(measured_all, indent=1, sort_keys=True) + "\n")
   measured = goldens.as_record()
   overall = measured["overall"]
   header = ["", "targets", "published", "exact agreement", "MAE per point", "escalated", "one-sample agreement"]
   by_type = [tally_row(name, record) for name, record in measured["by_point_type"].items()]
   by_category = [tally_row(name, record) for name, record in measured["by_category"].items()]
   text = f"""---
title: P3 grader evaluation
research_date: 2026-09-24
status: measured
purpose: The published result of eval_grader_against_operator_goldens, eval_leniency_calibration and eval_transcription_error_share, each number with its denominator.
---

# P3 grader evaluation [verified]

Measured by `tools/p3_evals.py publish` from recorded calls, and replayed by
`tests/eval/test_p3_evals.py` on every run, which fails if a number below stops matching the
replay.

**Who wrote the goldens.** {authors[0]} The operator golden set the plan names does not exist and
never will (ruling of 2026-09-24): every response and every hand grade here is a model's, so every
agreement figure is one model grading against another model's reading of the BC-PT definitions,
not against an AP Reader or the operator. No official response, stem or rubric text is used.
The grader is `claude-sonnet-5` on the operator's Claude subscription, prompts
`prompts/grader/point_liberal_v1.md` (two samples) and `point_strict_v1.md` (one), recorded on
2026-09-24.

## Grader against the golden set [verified]

{overall['targets']} target points over {len(measured['by_point_type'])} BC-PT ids, 5 responses per id,
one in each of 10's five categories. The grader published a decision on {overall['published']} of
{overall['targets']} and escalated {overall['escalated']} ({overall['escalation_rate']}).

- Exact agreement on published points: **{overall['exact_agreement']}** ({overall['published']} points).
- Mean absolute error per point on published points: **{overall['mean_absolute_error_per_point']}**
  ({overall['published']} points; a point is 0 or 1, so this is the share wrong).
- Decided by a deterministic check without the model: {overall['decided_deterministically']} of
  {overall['targets']}.
- One-sample agreement, the first standard sample alone against the label, which is 10's monthly
  canary: **{overall['single_sample_agreement']}** ({overall['reached_the_model']} points that
  reached the model).

Question-total mean absolute error, 10's figure out of 9, is not measured: each response is
graded on its target point alone, with the other points at their golden labels, so no model-graded
question total exists. No threshold is imposed, as 11 P3's exit criteria say; the stopping rule
stays open in 12.

By point type:

{table(by_type, header)}

By response category:

{table(by_category, header)}

## Leniency calibration [verified]

The standard (liberal) sample against the strict sample, on the {overall['reached_the_model']}
targets both were taken on, each against the golden label:

- standard sample mean absolute error per point: **{overall['standard_sample_mae']}**
- strict sample mean absolute error per point: **{overall['strict_sample_mae']}**

The one study that isolates the dial found a liberal policy lowered MAE for every model tested
(https://arxiv.org/html/2607.01247, [single-source]). The comparison against the published 2025
per-point means 10 describes needs point positions mapped to BC-PT ids, which is a judgement no
record here makes; it is not run.

## Transcription error share [verified]

{transcription_eval.summary_markdown(transcription)}
"""
   RECORD_PATH.write_text(text)
   print(f"wrote {RECORD_PATH.relative_to(REPO_ROOT)}")
   print(json.dumps(overall, indent=1))


def main(argv=None):
   parser = argparse.ArgumentParser()
   parser.add_argument("command", choices=["record-goldens", "record-transcription", "publish"])
   parser.add_argument("--workers", type=int, default=4)
   arguments = parser.parse_args(argv)

   if arguments.command == "record-goldens":
      record_goldens(arguments.workers)
   elif arguments.command == "record-transcription":
      record_transcription(arguments.workers)
   else:
      publish()


if __name__ == "__main__":
   main()
