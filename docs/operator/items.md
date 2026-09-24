---
title: The 130 hand-authored items
research_date: 2026-09-20
status: in_progress
purpose: Field-by-field spec for the operator's 130 P1 items, and the command that checks them.
---

# The 130 hand-authored items

Gate 17 (`test_item_verification_tools`), gate 30 (`eval_p1_distractor_paths`) and exit
criterion 7 all rest on 130 items, 10 per archetype over the 13 P1 archetypes.

## The 13 archetype ids

Read from `tools/build_p1_fixture.py`, `P1_ARCHETYPES` (lines 15 to 19), not typed from the
plan:

BC-QA-01004, BC-QA-01008, BC-QA-01015, BC-QA-02002, BC-QA-02006, BC-QA-02007, BC-QA-02008,
BC-QA-02010, BC-QA-02011, BC-QA-03001, BC-QA-03004, BC-QA-03005, BC-QA-03008.

## Record shape

One JSON file per item. The shape below is read out of `app/items/ingest.py` (the fields the
checker actually reads) and a real record, `tests/fixtures/items_p1/ITM-SYN-01008-00.json`. That
file is a synthetic gate-23 fixture, not one of the 130, but its shape is the shape ingestion
reads and is shown here as a shape reference only, with its own placeholder values, not as a
model to copy content from.

- `id`: string, the item id.
- `archetype_id`: string, one of the 13 ids above.
- `variant_id`: string or null. P1 disables `pick_variant`, so this is normally null.
- `format`: `"mcq"` or `"short_answer"`. This is the item's stored format, not what a session
  serves it as: `app/engine/select.py` `format_for_attempt` picks the served format per attempt
  (R29), independently of this field, so a `short_answer` item may still carry `options` (see
  below) for the turns it is served as `mcq`.
- `stem`: object, at least `text`.
- `figure`: omit entirely for P1. No P1 archetype carries a figure.
- `answer_key`: object with `form` and `mathjson`. `mathjson` is what the SymPy and numeric
  checks read.
- `worked_solution`: array of steps, each `{"step": <int>, "text": <string>, "mathjson": <...>}`.
  The **last** step's `mathjson` is compared against `answer_key.mathjson` by both the SymPy
  equivalence check and the numeric check (`app/items/ingest.py`, `solution_expression`), so it
  must carry MathJSON equivalent to the key, not merely the final English step.
- `options`: array. Present on `mcq` items, and also worth setting on a `short_answer` item so it
  has something to serve on the turns `format_for_attempt` gives it as `mcq`, since a
  `short_answer` item never grows options at serve time. Each option is
  `{"id": <string>, "value": <mathjson>, "is_key": <bool>, "error_path": <BC-ERR id or null>}`.
  Exactly one option carries `is_key: true`. That option's `error_path` is null. Every other
  option (a distractor) must carry a non-null `error_path`, and it must be a BC-ERR id that one
  of the archetype's own skills holds, not just any BC-ERR id in the library. `error_path` is
  read from the option itself, never from `archetypes.common_distractors`, which is prose and is
  parsed by nothing (`app/items/distractor_paths.py`). `violated_step` is a zero-based index into
  the archetype's own `expected_solution_path` in `data/archetypes.json`, not into this item's
  `worked_solution`: `app/feedback/render.py` `violated_step_index` reads it straight off the
  chosen option (falling back to the error record) and indexes `archetype["expected_solution_path"]`
  with it. It is read by the feedback screen and is worth setting on every distractor even though
  the checker in `tools/check_items.py` does not enforce it.
- `calculator_status`: `"no_calculator"` for every P1 item.
- `representation`: `"BC-REP-01"` for every P1 item.
- `difficulty_settings`: array of `{"difficulty_factor_id": <BC-DF id>, "setting": <string>}`.
- `skills`: array of BC-SKL ids, in the same order as the archetype's own `skills` array in
  `data/archetypes.json`, so the primary skill (first entry) stays first.
- `parameter_draw`: object, whatever parameters the item's numbers were drawn from.
- `authored_on`: ISO date string.

There is no separate top-level `provenance` field to author. `app/items/ingest.py` builds the
provenance record itself: `model = "operator"`, `prompt_template_version` and
`generation_job_id` null, `authored_on`, `archetype_id` and `variant_id` taken from the record.

## Where to put the files

`tests/fixtures/items_p1/` already holds 36 synthetic items for gate 23 only (see that
directory's own README) and counts toward no item-quality gate. No plan document and no code
file names a directory for the 130 real items, so that choice is the operator's; put them
anywhere and pass that directory to the checker. Do not put the 130 items inside
`tests/fixtures/items_p1/` alongside the synthetic ones, since gate 30 and the audit sample must
be able to draw only from the real 130, not from the 36.

## The check

```
python3 tools/check_items.py <directory>
```

Run against `tests/fixtures/items_p1/` on 2026-09-20, this printed:

```
records read: 36
clean: 36
with violations: 0

items per archetype:
  BC-QA-01004: 0
  BC-QA-01008: 6
  BC-QA-01015: 0
  BC-QA-02002: 6
  BC-QA-02006: 6
  BC-QA-02007: 6
  BC-QA-02008: 0
  BC-QA-02010: 0
  BC-QA-02011: 6
  BC-QA-03001: 0
  BC-QA-03004: 0
  BC-QA-03005: 0
  BC-QA-03008: 6
```
and exited 0. That run is over the 36 synthetic items, not the 130, and is shown only to
demonstrate the tool's output shape; it is not evidence toward gate 17 or gate 30. Run it again
over the real 130 once they exist. A clean run prints no per-item violation lines and exits 0;
each violation line names the item id, then the check type (`sympy_equivalence`, `numeric_probe`,
`distractor_distinct`, or a gate-30 distractor-path violation) and what failed. The per-archetype
count at the bottom is how the operator confirms exactly 10 per archetype.

## Later banks [verified]

The 130 P1 items live in content/items_p1_agent/. Stage 1 adds one bank per unit,
content/items_unitNN_agent/, in the same record shape; its scope rule and the choices it settles
(format-neutral stems, symbolic keys, inline LaTeX, per-archetype error paths) are in
[items-units-4-to-10.md](items-units-4-to-10.md). Since 2026-09-24 `tools/check_items.py` checks
each distractor's error_path against the errors held by that record's own archetype, not the
union over the P1 archetypes, and prints a count for every archetype it reads.
