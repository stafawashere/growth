---
title: P3 grader evaluation
research_date: 2026-09-24
status: measured
purpose: The published result of eval_grader_against_operator_goldens, eval_leniency_calibration and eval_transcription_error_share, each number with its denominator.
---

# P3 grader evaluation [verified]

Measured by `tools/p3_evals.py publish` from recorded calls, and replayed by
`tests/eval/test_p3_evals.py` on every run, which fails if a number below stops matching the
replay.

**Who wrote the goldens.** claude-opus-5-5 subagent on the operator's delegation of 2026-09-24; model-authored and model-graded, not human The operator golden set the plan names does not exist and
never will (ruling of 2026-09-24): every response and every hand grade here is a model's, so every
agreement figure is one model grading against another model's reading of the BC-PT definitions,
not against an AP Reader or the operator. No official response, stem or rubric text is used.
The grader is `claude-sonnet-5` on the operator's Claude subscription, prompts
`prompts/grader/point_liberal_v1.md` (two samples) and `point_strict_v1.md` (one), recorded on
2026-09-24.

## Grader against the golden set [verified]

150 target points over 30 BC-PT ids, 5 responses per id,
one in each of 10's five categories. The grader published a decision on 146 of
150 and escalated 4 (0.0267).

- Exact agreement on published points: **0.9315** (146 points).
- Mean absolute error per point on published points: **0.0685**
  (146 points; a point is 0 or 1, so this is the share wrong).
- Decided by a deterministic check without the model: 0 of
  150.
- One-sample agreement, the first standard sample alone against the label, which is 10's monthly
  canary: **0.9133** (150 points that
  reached the model).

Question-total mean absolute error, 10's figure out of 9, is not measured: each response is
graded on its target point alone, with the other points at their golden labels, so no model-graded
question total exists. No threshold is imposed, as 11 P3's exit criteria say; the stopping rule
stays open in 12.

By point type:

|  | targets | published | exact agreement | MAE per point | escalated | one-sample agreement |
| --- | --- | --- | --- | --- | --- | --- |
| BC-PT-99005 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99007 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99008 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99009 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99010 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |
| BC-PT-99011 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |
| BC-PT-99012 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |
| BC-PT-99013 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99014 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99015 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99016 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99017 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |
| BC-PT-99018 | 5 | 4 of 5 | 1.0 | 0.0 | 1 of 5 | 1.0 |
| BC-PT-99026 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99028 | 5 | 4 of 5 | 0.75 | 0.25 | 1 of 5 | 0.6 |
| BC-PT-99031 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99033 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99034 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99041 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.6 |
| BC-PT-99043 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99046 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |
| BC-PT-99053 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99054 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |
| BC-PT-99056 | 5 | 4 of 5 | 0.75 | 0.25 | 1 of 5 | 0.8 |
| BC-PT-99061 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99062 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99063 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99064 | 5 | 5 of 5 | 1.0 | 0.0 | 0 of 5 | 1.0 |
| BC-PT-99066 | 5 | 4 of 5 | 1.0 | 0.0 | 1 of 5 | 0.8 |
| BC-PT-99068 | 5 | 5 of 5 | 0.8 | 0.2 | 0 of 5 | 0.8 |

By response category:

|  | targets | published | exact agreement | MAE per point | escalated | one-sample agreement |
| --- | --- | --- | --- | --- | --- | --- |
| eligible_after_error | 30 | 30 of 30 | 0.9 | 0.1 | 0 of 30 | 0.8667 |
| fully_correct | 30 | 30 of 30 | 1.0 | 0.0 | 0 of 30 | 1.0 |
| narrow_fail | 30 | 30 of 30 | 0.9333 | 0.0667 | 0 of 30 | 0.9333 |
| notation_failure | 30 | 27 of 30 | 0.8148 | 0.1852 | 3 of 30 | 0.7667 |
| unconventional_valid | 30 | 29 of 30 | 1.0 | 0.0 | 1 of 30 | 1.0 |

## Leniency calibration [verified]

The standard (liberal) sample against the strict sample, on the 150
targets both were taken on, each against the golden label:

- standard sample mean absolute error per point: **0.0867**
- strict sample mean absolute error per point: **0.08**

The one study that isolates the dial found a liberal policy lowered MAE for every model tested
(https://arxiv.org/html/2607.01247, [single-source]). The comparison against the published 2025
per-point means 10 describes needs point positions mapped to BC-PT ids, which is a judgement no
record here makes; it is not run.

## Transcription error share [verified]

Every page is a rendered stand-in: a handwriting font on the app's booklet page, photographed in
software (tools/render_frq_pages.py). No photograph of real handwriting exists yet, so these are a
floor on what the pipeline must survive, not a measurement of a student's pencil.

Golden set 3 (P7's 20 model-authored page specifications, content/golden/transcriber.json):
17 of 20 pages passed the quality gate. On the accepted pages
the transcriber read back 30 of 43
point-bearing expressions exactly (0.6977), with mean character
similarity 0.9919; 3 of
3 struck lines came back marked crossed out.

| variation | pages | passed the gate | point-bearing read |
| --- | --- | --- | --- |
| angled | 3 | 3 | 6 of 9 |
| crossed_out | 3 | 3 | 4 of 8 |
| good_light | 3 | 3 | 7 of 8 |
| injected_instruction | 2 | 2 | 4 of 4 |
| low_light | 3 | 0 | 0 of 0 |
| margin_work | 3 | 3 | 5 of 7 |
| slight_blur | 3 | 3 | 4 of 7 |

Pages carrying an instruction to the model: GLD-TRN-019 answer field ['4']; GLD-TRN-020 answer field ['\\frac{1}{3}']. The instruction is transcribed as a line of
text; the answer field shows whether the reader obeyed it.

Transcription error share (15 golden-2 responses rendered on their booklet
pages, 15 read): the grader got 1 targets
wrong from the unconfirmed read-back, and 1 of those it got
right from the true work, a share of **1.0** against the AIED study's
0.87. The read-back changed the decision on
5 of 15 targets, counting a point
that became or stopped being provisional. One error in fifteen is too few for the share to mean
more than that transcription can cause an error the grader would not otherwise make; it is not a
comparison with 0.87. The student's confirmation step exists to remove exactly these errors before
grading.

The point-bearing count is strict: an expression counts only when the read-back holds it with
spacing normalised, or when every side of it is equal in SymPy. A mean character similarity near
1 beside a lower point-bearing rate means most misses are spelling of the same mathematics (a
different fraction command, a dropped differential spacing, a line split in two), not a misread
digit; which is which was not labelled here.
