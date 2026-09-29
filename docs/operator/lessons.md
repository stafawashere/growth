---
title: Lesson records, ingest and sign-off
research_date: 2026-09-29
status: in_progress
purpose: How a lesson record under content/lessons/ reaches the lessons table, what stale means, the sign-off evidence file, and the six lesson endpoints.
---

# Lesson records, ingest and sign-off

`docs/lessons/BUILD-PLAN.md` "The design to record path" turns a design under `docs/lessons/` into
a record under `content/lessons/<id>.json`. This file is the operating guide for what happens to
that record afterwards: how the server ingests it, when it is served, and what the operator writes
to move it to `signed_off`.

## How a record is ingested

`app/lessons/ingest.py` `ingest_lessons` runs when the server starts, before it accepts a
connection, over the directory `GROWTH_LESSONS_DIR` names (unset: `content/lessons`; `none` turns
it off). For each `*.json` in file name order it:

1. Validates the record against `schemas/lessons/lesson.schema.json` and runs every lint of
   `tools/check_lessons.py` through `check_lesson`, the same checks the operator runs by hand with
   `PYTHONPATH=. .venv/bin/python tools/check_lessons.py content/lessons`.
2. Writes one `lesson_verifications` row per lint, `pass` or one `fail` row per finding with the
   section id the finding names, plus a `stale` row and, when a verification file exists, a
   `resolve` row.
3. Writes the `lessons` row for the record's id and version: the body as stored, the two read
   minute forecasts, the provenance and the source digest. A version already stored is rewritten
   in place, so a draft may be edited under the same version and ingested again.

The stored status is the record's own status, except:

- `stale` when the record is stale (next section);
- `draft` when any lint finds something, whatever status the record claims, because a record
  that fails the checker has not passed step 2 of the design to record path;
- `draft` when `docs/lessons/verification/<id>.json` exists and a worked example or check has no
  agreeing verdict in its `resolve` block (invariant L9). Worked examples are matched as
  `<id>#ex-1`, `<id>#ex-2` in record order and checks by their `chk-n` id.

A record that fails the schema is not stored at all; its `schema` verification rows are.

Only a `signed_off` row is served (invariant L8). A concept without one falls back to the example
first path of today, never blocks anything, and the library lists it as not yet available.

## What stale means

A record is stale when either holds:

- its `source_digest` differs from `app/lessons/source.py` `authoring_bundle`'s current digest for
  its concept, meaning a library record or a research line it was written from has changed;
- any BC-* id it cites is not `active` in the loaded snapshot, meaning an id it rests on was retired.

A stale version is stored with status `stale`, the audit action `lesson_stale` is written the first
time it goes stale, and it is never served. Prose is never rewritten automatically: the design
goes back through design, the record is re-transcribed, and the new version is ingested.

## The sign-off evidence file

The blind re-solve and the block audit are done once, on the design, in
`docs/lessons/verification/<id>.json`. The record inherits them through equality, confirmed by:

```
PYTHONPATH=. .venv/bin/python tools/lesson_resolve_compare.py content/lessons/<id>.json docs/lessons/unit-NN/<id>.md
```

It prints one line per compared field (every worked example problem, step cue and why, and key;
every check stem and key; the orientation, key ideas, strategy fields, error blocks, bridges,
representations and decision stems) and exits 0 only when every field is equal. Keys are equal
under `app/items/verify.py` `equivalence`; text is equal after whitespace is normalised.

On exit 0, when the verification file exists, it writes `docs/operator/lesson-audit/<id>.json`
with the record's id and version, the comparison date, the auditor model id and the copied
`resolve` and `audit` blocks. That file is the record's sign-off evidence. The operator then sets
`status` to `signed_off` with `signed_off_by` and `signed_off_at` in the record's provenance, and
the next ingest stores it and writes `lesson_signed_off` once.

A changed stem or key makes the comparison fail, which means the blind session runs again on the
design before the record can be signed off.

## The six endpoints

All six sit behind the signed-in session, like every other route, and answer 404 for a lesson that
is unknown or has no `signed_off` version.

| Endpoint | What it does |
|---|---|
| `GET /lessons?unit=BC-UNIT-06` | the library: units in `data/curriculum.json` order, each concept with its servable lesson and the student's state (`coming_up`, `read`, `skipped`, `not_available` and the rest); `unit` is optional |
| `GET /lessons/{lesson_id}?version=` | the stored body plus the student's `lesson_state` row or null |
| `GET /lessons/{lesson_id}/plan?band=low` | the body, `app/lessons/plan.py` `plan_lesson` for the band and reason (`reason` defaults to `read_again`), and the state |
| `POST /lessons/{lesson_id}/events` | a library read; `completed` marks the lesson read from the library |
| `POST /sessions/{session_id}/lessons/{lesson_id}/events` | a lesson or refresher inside a session; `opened` marks it served, `completed` read and `skipped` skipped; a refresher reason `T1` to `T5` counts a refresher instead |
| `POST /lessons/{lesson_id}/checks/{check_id}/answers` | grades a check answer through `app/items/grade.py`, names the error block a wrong option came from, and writes `lesson_check_responses` only |

A check answer never reaches `attempts`, the engine or the diagnostician, and no lesson event
changes any `skills_state` field.
