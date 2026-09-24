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

## The P1 procedure, end to end

Added 2026-09-23. The 130 P1 items are agent drafts until the operator adopts them, and gate 29
samples only operator items, so the order is:

1. Review the drafts. `docs/operator/p1-agent-item-key-check.md` lists, per item, the answer SymPy
   computed from the stem beside the stored key; all 130 matched.
2. Adopt the reviewed items as the operator's own, which rewrites `authored_by` to `drafted_by` in
   each record and updates any row `var/growth.db` already holds:
   `python3 tools/sign_off_items.py all` (or name item ids or archetype ids instead of `all`).
3. Start the app once so the bank ingests the records, then draw the sample:
   `python3 tools/draw_key_audit_sample.py var/growth.db data var/key_audit_sample.json`.
   P1's items span three units, so the 15-per-unit cap rises to the smallest cap that fills 100
   (35 for the current 30, 60 and 40), `app/review/audit.py` `unit_cap_for`.
4. Write the worksheet and the verdict template:
   `python3 tools/key_audit_worksheet.py var/key_audit_sample.json var/key_audit_worksheet.md var/key_audit_verdicts.json`.
   The worksheet shows each stem, the expected solution path and the options, and never the key.
5. Solve each item by hand, then fill `verdict`, `auditor`, `audited_at` and, for `ambiguous`, the
   `second_answer` in the verdicts file.
6. `python3 tools/check_audit_verdicts.py var/key_audit_verdicts.json var/key_audit_sample.json`
   prints the key error rate once every record is complete.

## Auditing several banks [verified]

Added 2026-09-24. `tools/key_audit_worksheet.py` takes `--items-dir` more than once and, with
none given, searches every content/items_* bank, so a sample drawn over the per-unit banks of
[items-units-4-to-10.md](items-units-4-to-10.md) finds each record. The stage 1 audit draws over
the new items only, from a scratch database that ingested only the unit banks, and is recorded
in docs/operator/key-audit-p2/ beside key-audit-p1/.
