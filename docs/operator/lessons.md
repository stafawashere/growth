---
title: Lesson records, ingest and sign-off
research_date: 2026-09-29
status: in_progress
purpose: How a lesson record under content/lessons/ reaches the lessons table, what stale means, the sign-off evidence file, and the seven lesson endpoints.
---

# Lesson records, ingest and sign-off

`docs/lessons/BUILD-PLAN.md` "The design to record path" turns a design under `docs/lessons/` into
a record under `content/lessons/<id>.json`. This file is the operating guide for what happens to
that record afterwards: how the server ingests it, when it is served, and what the operator writes
to move it to `signed_off`.

## How a record is transcribed

A record is never written by hand. `tools/lesson_transcribe.py` computes it from the design's
machine record and the authoring bundle:

```
PYTHONPATH=. .venv/bin/python tools/lesson_transcribe.py docs/lessons/unit-NN/<id>.md [<out.json>]
```

Without `<out.json>` it writes `content/lessons/<id>.json`. The same design and snapshot always
give the same bytes: texts verbatim, every SymPy string as MathJSON (`app/items/mathjson.py`
`from_sympy`), step relations kept, each block's delivery from the design's `delivery` array,
`word_count` from `app/lessons/plan.py` `band_words`, status `draft`, and provenance naming the
tool and the `design_path`. A design field the record cannot express is refused with the field
named, and the record is not written. Then run the checker on the file or the directory:

```
PYTHONPATH=. .venv/bin/python tools/check_lessons.py content/lessons/<id>.json
```

### The v2 fields and the pooled driver

Since 2026-09-29 the provenance names `generator/lesson_v2`, and the transcriber also carries:

- the design's `prediction` as the first section (`#s1`, both bands, the lesson's skills, tag
  `inferred`), with its stem, format, options (an option's `expr` becomes its MathJSON `value`), a
  short answer's `key` as `answer_key`, the resolution as `{"text": ...}`, and the delivery entry
  named by the prediction's id, else `text` with reason `rule 6`;
- `contrast` on the strategy block that has it, texts verbatim;
- `fade_from` on the worked example that has it;
- `fix_prompt` on every error block, refusing a concept design whose error block lacks it;
- `no_figure_reason` at the top level when the design states it.

A prediction or contrast field outside that shape is refused with the field named.
`tools/lesson_resolve_compare.py` compares all of these as well.

To transcribe many designs, the pooled driver loads the snapshot once per worker:

```
PYTHONPATH=. .venv/bin/python tools/lesson_transcribe_all.py [--workers 8] [--out-dir DIR] docs/lessons/unit-02 docs/lessons/decisions/LSN-DEC-06-01.md
```

A directory stands for every `LSN-*.md` directly inside it. It prints `wrote <path>` or
`refused <design>: <reason>` per design, then `designs: N, wrote: W, refused: R`, and exits 1 when
any design was refused. It must be run as a script file, since a pool started from a script read
on standard input cannot spawn its workers on macOS.

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

## The seven endpoints

All seven sit behind the signed-in session, like every other route, and answer 404 for a lesson that
is unknown or has no `signed_off` version.

| Endpoint | What it does |
|---|---|
| `GET /lessons?unit=BC-UNIT-06` | the library: units in `data/curriculum.json` order, each concept with its servable lesson and the student's state (`coming_up`, `read`, `skipped`, `not_available` and the rest); `unit` is optional |
| `GET /lessons/{lesson_id}?version=` | the stored body plus the student's `lesson_state` row or null |
| `GET /lessons/{lesson_id}/plan?band=low` | the body, `app/lessons/plan.py` `plan_lesson` for the band and reason (`reason` defaults to `read_again`), and the state |
| `POST /lessons/{lesson_id}/events` | a library read; `completed` marks the lesson read from the library |
| `POST /sessions/{session_id}/lessons/{lesson_id}/events` | a lesson or refresher inside a session; `opened` marks it served, `completed` read and `skipped` skipped; a refresher reason `T1` to `T5` counts a refresher instead |
| `POST /lessons/{lesson_id}/checks/{check_id}/answers` | grades a check answer through `app/items/grade.py`, names the error block a wrong option came from, and writes `lesson_check_responses` only |
| `POST /lessons/{lesson_id}/prompts/{section_id}/answers` | body `{"answer", "option_id", "elapsed_ms"}`; `section_id` is the full section id or its `#` suffix. Grades a prediction (an mcq by `option_id` against `is_key`, a short answer against `answer_key`), an error block's fix (`fix_prompt` true, against `right_step.expression` as a symbolic key) or a faded example's answer (against its `answer`); any other section answers 404. Writes `lesson_check_responses` only and returns `{"correct", "section_id", "kind"}` with `kind` `prediction`, `fix` or `fade`, and `resolution` for a prediction (else null) |

A check answer never reaches `attempts`, the engine or the diagnostician, and no lesson event
changes any `skills_state` field.
