---
title: The 100-item key audit
research_date: 2026-09-20
status: in_progress
purpose: Verdict record spec for the operator's 100-item key audit, and the command that checks it.
---

# The 100-item key audit

Gate 29 (`eval_p1_key_error_rate`) and exit criterion 4 need a 100-item sample of the published
130 items, audited by hand, with every verdict recorded. This is a measurement, not a pass or
fail gate: P1 sets no threshold on the rate. What is required is that the number exists and is
measured rather than estimated.

## Verdict record fields

Read from `app/review/verdicts.py`, `verdict_violations`, which is what CI enforces:

- `item_id`: non-empty string, one of the 100 sampled item ids.
- `verdict`: one of the values in `app/review/audit.py`'s `VERDICTS`: `"key_wrong"`,
  `"ambiguous"`, `"clean"`.
- `auditor`: non-empty string.
- `audited_at`: non-empty value (an ISO date or timestamp).
- `second_answer`: required, non-empty, only when `verdict` is `"ambiguous"`. Omit or leave null
  otherwise.

One JSON array of these objects is the verdicts file. A separate JSON array of the 100 sampled
item ids is the sample file.

## Drawing the sample

`python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json> [seed]` draws
it: stratified by unit so no unit contributes more than 15 items, and by calculator status in
proportion to what is published, over the database's published items, deterministic for a given
seed (default 2026). Run it once the 130 hand-authored items are published, then point
`GROWTH_KEY_AUDIT_SAMPLE_PATH` (or `Settings.key_audit_sample_path`) at the file it writes so
`POST /review-queue/{id}/resolve` can check an item_audit verdict against it; without a sample
configured, that route refuses every item_audit verdict.

## What each verdict means

Audit each item by hand against its archetype's `expected_solution_path`, without looking at the
stated key first.

- `"clean"`: the stated key is mathematically correct and the stem is not ambiguous.
- `"key_wrong"`: the stated key is mathematically wrong.
- `"ambiguous"`: the stem admits a second correct answer, in the operator's judgement. Record
  that second answer in `second_answer`. This is an operator judgement, not a mechanical check,
  which is why it must be recorded rather than merely asserted.

`"key_wrong"` and `"ambiguous"` both count as key errors for the published rate
(`app/review/audit.py`, `KEY_ERROR_VERDICTS`); `"clean"` does not.

## The completeness rule

The rate is published only when, for every id in the 100-item sample, exactly one well-formed
verdict record exists: no missing id, no duplicate, no malformed record, nothing outside the
sample counted in. If any of that fails, the checker reports why and does not print a rate.

## The check

```
python3 tools/check_audit_verdicts.py <verdicts.json> <sample.json>
```

Run on 2026-09-20 against a one-item smoke file (`item_id: "ITM-0001"`, `verdict: "clean"`),
this printed:

```
sample size: 1
audited: 1
missing: 0
key error rate: 0.0
no pass threshold is set in P1; this is a measurement, not a gate
```
and exited 0. That run is a one-record smoke test of the tool, not the audit itself; it is
shown only to demonstrate the output shape. Any malformed verdict record is printed above the
completeness block, one line per violation, under the offending item id. Run the real command
once the 100-item sample and its verdicts exist, and paste that output, including the published
key error rate, into the pull request.
