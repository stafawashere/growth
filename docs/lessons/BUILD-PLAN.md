---
title: Adaptive specialized lessons, engineered build plan
research_date: 2026-09-29
status: draft
purpose: The build plan for implementing docs/plan/15-lessons.md slices L1 to L6 in this codebase, with the files, schema and migration steps, routes, engine insertion points, tests and invariants, acceptance checks, dependencies, risks, the offline authoring and sign-off process that turns each design under docs/lessons/ into a signed-off lesson record, the order of lesson production, the cost lines, the pacing arithmetic and the proposed plan amendments.
---

# Adaptive specialized lessons, engineered build plan

Every decision here that plan 15 already made is cited to its section; every decision plan 15 does not make is marked [inferred] and listed under Proposed amendments. The plan is a build plan: it schedules code under app/, the web client, migrations and the lesson records under content/lessons/, none of which this design run touches. What this run produced is the input to it: one design per lesson under docs/lessons/, checked by tools/check_lesson_designs.py, re-solved blind and audited.

## What exists (L0, read 2026-09-29)

| Piece | Where | State |
|---|---|---|
| Plan | docs/plan/15-lessons.md | draft, Q1 to Q4 ruled 2026-09-29, L0 exit read the same day (BUILD-LEDGER.md, 2026-09-29, lessons L0) |
| Schema | schemas/lessons/lesson.schema.json | in place, 471 lines |
| Checker | tools/check_lessons.py, 26 lints in LINTS, red fixtures under tests/fixtures/lessons/ | tests/lessons 71 passed (ledger) |
| Plan function | app/lessons/plan.py plan_lesson, L13 in tests/lessons/test_plan.py | green |
| Authoring input | app/lessons/source.py authoring_bundle, reader_checks | in place |
| Confusable sets | app/lessons/confusable.py, 10 sets over confusable_with (505 of 541 skills filled by tools/derive_confusable.py) | in place |
| Constants | app/lessons/constants.py, 30 values, every one [inferred] in 15's register | in place |
| Prompt | prompts/generator/lesson_v1.md | in place |
| Hand-authored lesson | content/lessons/LSN-CON-02013.json, status draft | checker clean |
| Designs | docs/lessons/ (this run): TEMPLATE.md, unit-NN/, prerequisites/, decisions/, verification/ | see PROGRESS.md |
| Design checker | tools/check_lesson_designs.py, 21 rules plus directory coverage; tests/lessons/test_check_lesson_designs.py | 30 passed |

Two facts that changed since plan 15 was written, both computed from data/ on 2026-09-29 (PROGRESS.md, Stage 0): BC-CON-06014 is now loaded by BC-QA-06017, so every concept is reachable by the first-contact trigger and 15's "never inserted" case for it is empty; and `confusable_with` is filled, so 15's derivation paragraph describes a library state that no longer holds and the set count is published by `tools/check_lessons.py --sets` as 10.

## The design to record path (every slice depends on it)

A design doc under docs/lessons/ becomes a lesson record under content/lessons/ by this offline process, run per lesson in a Claude Code session at $0.00 API spend (15, Sourcing, Pipeline; docs/operator/offline-authoring.md):

1. **Author.** The session reads the design (TEMPLATE.md fixes the shape) and prompts/generator/lesson_v1.md, and writes `content/lessons/<id>.json`. Every served sentence, every draw, every step's cue and why, every check and every error path is already in the design's machine record; the author's work is transcription to MathJSON (`app/items/mathjson.py` heads), section ids (`<id>#s<n>`, `#err-BC-ERR-x`, `#chk-<n>`, `#prq-BC-PRQ-x`), `snapshot_digest` and `source_digest` from the bundle, and the `delivery` field (amendment A-D1). No teaching decision is made at this step; where the author finds one is needed, the design goes back to design, not forward.
2. **Check.** `tools/check_lessons.py content/lessons` exit 0. The design checker has already run the same caps, lints and CAS checks on the SymPy form, so the expected outcome is clean on the first pass; a finding here is a transcription error.
3. **Blind re-solve.** Already done on the design (docs/lessons/verification/<id>.json, `resolve` block): the record's problems are the design's problems verbatim, so the verdict carries over when `tools/lesson_resolve_compare.py` (new, L1) confirms the record's stems equal the design's stems and its keys equal the design's keys under `verify.equivalence`. A changed stem or key re-runs the blind session.
4. **Sign-off.** Already done on the design (`audit` block of the same file, per block). The record's sign-off is a check that every block's text equals the design's text, recorded in `docs/operator/lesson-audit/<id>.json` with `auditor` the model id, per 15's step 4 and the 2026-09-24 ruling. Status moves to `signed_off` and the ingest writes `lesson_signed_off`.

The two "already done" steps are why the designs were verified in this run: the expensive work (a blind re-solve and a block audit per lesson) is done once on the design and inherited by the record through text equality, not repeated.

## Slice L1. Storage, API, reader, first 19 lessons

Entry: L0 (15, Phased delivery). Depends on the throughput ruling in the ledger (2026-09-29, prerequisite gates), since lessons add minutes to block 2 without adding evidence; the pacing section below shows the arithmetic under the current ceiling and does not assume it lifted.

### Files

| Path | Change |
|---|---|
| app/db/models.py | five tables: `lessons` (id, version, kind in con, prq, dec; target_id; snapshot_id; body JSON; read_minutes_full, read_minutes_brief; status; provenance JSON; source_digest; created_at; updated_at), `lesson_verifications` (shaped like item_verifications: lesson_id, version, section_id, check_type, outcome, detail), `lesson_state` (user_id, lesson_id primary; status in unseen, deferred, served, read, skipped, bypassed_by_placement; version_seen; band_served; first_served_at; read_at; read_source; refresher_due_reason; refresher_served_at; refresher_count; created_at; updated_at), `lesson_events`, `lesson_check_responses` (15, Migrations) |
| app/db/migrate.py | `apply_additive_migrations` adds nullable `attempts.preceded_by_lesson_id` and `attempts.preceded_by_lesson_version` (15, Migrations: nullable or server_default, not unique, not indexed, else SchemaDriftError) |
| app/lessons/ingest.py | new, on app/items/ingest.py: reads content/lessons/*.json, validates against schemas/lessons/lesson.schema.json, runs tools/check_lessons.py's `check_lesson` (importable), writes `lessons` and `lesson_verifications`, refuses a record whose status is not signed_off from serving (15, Publication rule) |
| app/lessons/repository.py | new: `servable(concept_id)`, `lesson_states(user_id)`, `write_state`, `write_event`, `write_check_response` |
| app/api/routes/lessons.py, app/api/app.py | the six endpoints of 15, Endpoints: `GET /lessons?unit=`, `GET /lessons/{id}` with `?version=`, `GET /lessons/{id}/plan?band=`, `POST /sessions/{sid}/lessons/{id}/events`, `POST /lessons/{id}/events`, `POST /lessons/{id}/checks/{cid}/answers` graded by app/items/grade.py and written to `lesson_check_responses` only |
| app/session/purge.py, app/api/routes/me.py (export), app/session/seed.py | the five tables under purge and export; the seed writes no lesson_state row (15, State) |
| app/audit/vocabulary.py | `lesson_gap_fail_open`, `lesson_stale`, `lesson_signed_off` |
| app/web/src/lessons/ | `LessonReader.tsx`, `LessonSection.tsx`, `LessonCheck.tsx`, `LessonLink.tsx`, `RefresherPanel.tsx`; plus `FigureControl.tsx`, `FrameStepper.tsx`, `ModelTable.tsx`, `ContrastPanel.tsx` for the delivery modes (amendment A-D4); mathematics through `math/MathText.tsx`, figures through `figures/` |
| app/web/src/App.tsx, progress route | `"lesson"` in `Destination`, the progress Lessons tab listing units from data/curriculum.json (15, UI, Library) |
| tools/lesson_resolve_compare.py | new: confirms a record's stems and keys equal its design's, so the design's re-solve verdict carries over (step 3 above) |
| tools/cost_model.py | no change; the `lessons.*` lines exist (ledger, L0 exit) |
| content/lessons/ | the 19 concept lessons the 13 P1 archetypes load, authored from their designs (15, L1 scope) |

### Tests and invariants

- L8 (served lesson signed_off, not stale, every BC-* id active), L9 (every worked step passes `verify.equivalence`, every key has an agreeing blind re-solve), L10 (no draw equals a published item's draw): `tests/lessons/test_ingest.py`, each shown red on a fixture before green.
- Purge and export coverage: `tests/session/test_purge.py` and the export test gain the five tables.
- Contract test of every content/lessons/*.json against the real data/ (15, Tests).
- Vitest: keyboard-only reader, reduced motion, the skip path, the check feedback link, the library tab (15, Tests), plus per delivery mode: a `motion` block steps frames on key press and never auto-advances under `prefers-reduced-motion: reduce`; an `interactive` control is operable by arrow keys and its fallback renders when the spec cannot; a `contrast` panel renders two to four stems on one screen.
- L13 stays green over every signed-off lesson (tests/lessons/test_plan.py).

### Acceptance

L8 to L10 green; audit of all 19 at 0 errors with its denominator (docs/lessons/verification/ for the designs, docs/operator/lesson-audit/ for the records); vitest reader tests green; `tools/check_lessons.py content/lessons` clean over 20 files (the hand-authored lesson plus 19).

### Risks

- The 19 P1 lessons are Units 1 to 3 concepts; if the P1 archetype list has moved since 11 was written, L1 takes the concepts of the 13 archetypes `app/engine/constants.py` names for P1, computed, not the plan's list.
- The reader adds four components beyond 15's five; each is behind a mode switch, so a lesson with only text and step_reveal renders with the original five.

## Slice L2. Engine insertion

Landed 2026-09-29: app/lessons/gate.py, the block 2 insertion and deferral in app/session/build.py, the lesson slots in app/session/service.py, `lesson_first_contact` in switches.DEFINITIONS, the lesson forecast, tests/session/test_lesson_gate.py, tests/lessons/test_invariants.py, tests/api/test_lessons_session.py, the SessionScreen lesson state. Not landed: home's forecast (app/session/preview.py assembles without lesson inputs), `lesson_gap_fail_open`.

Entry: L1. Scope per 15, Engine and session integration.

### Files

| Path | Change |
|---|---|
| app/lessons/gate.py | new: `lesson_target(item, states, graph, lesson_states, lessons)` reading every loaded skill in the archetype's `skills` order (15, First-contact target), `lesson_band(archetype, states, graph, retrievability)` on `STAGE_LOW` and `STAGE_HIGH`, `bypass_placed_concepts(states, graph)` |
| app/session/build.py | `Session` gains `lessons`, `lesson_minutes`, `lesson_deferrals`; block 2 entries gain `kind`; inside the block 2 loop, after `next_item_learning` returns `selection.item` and before `fits`: `lesson_target`, `lesson_band`, conditions (a) to (e), `serve_lesson`, the deferral write, `preceded_by_lesson_*` on the item dict; `interleaving_satisfied`, `unexplained_violations`, `window_filter` and `unit_counts` skip lesson entries; `forecast_total` includes them (15, Session assembly) |
| app/session/service.py | `SERVING_BLOCKS`, `served_positions`, `consumed_positions`, `resolve_slot`, `next_item` learn `kind`; a lesson slot is consumed by `completed` or `skipped` on the events route |
| app/engine/constants.py | none: the thirteen lesson constants live in app/lessons/constants.py already; 15's register rows are unchanged |
| app/experiments/switches.py | `DEFINITIONS` gains `lesson_first_contact` (unit concept, control `lesson_before_first_item`, treatment `example_first`) |
| app/session/forecast | a lesson's minutes are the authored `read_minutes[band]` until `LESSON_FORECAST_MIN_COMPLETIONS` completions, then the running median of `read_ms / read_minutes[band]` times the authored value (15, Forecast) |
| telemetry | served with reason and band, opened, per-section dwell, skipped with section index, completed, check answer with error, deferred, and the delivery mode of each section viewed (amendment A-D5) |

### Tests and invariants

- L0 (the bounding invariant, 15, Evidence handling), L1, L2, L3, L4, L5, L7, L11, L12, L13 as property tests at 1,000 cases over the real 541-skill graph, in the standing gate once L2 merges (15, Gates).
- `tests/session/test_lesson_gate.py`: `lesson_target` over the 59 never-primary concepts, the deferral rule, the share cap, the LSN-PRQ ordering.
- Integration: a no-units student's first session shows a lesson then an example item for two concepts, the third new concept's item carries `lesson_link` and a `deferred` row, block 3 has no lesson, the next session opens block 2 with the deferred lesson (15, Tests).

### Acceptance

Standing gate plus L0 to L14 at 1,000 cases; the no-units session test; deferral telemetry rendering. Nothing in app/engine/fringe.py, update.py or the mastery rule changes (15, Gates: no threshold loosened).

### Risks

- Block 2's 25 minutes (`BLOCK2_MAX_MINUTES`) now hold lesson minutes; the pacing section shows two full lessons take 12 minutes of it, leaving 13 for items, which at the 3-minute default is 4 items rather than 8. The deferral rule (Q3, ruled defer) bounds it, and deferrals per session are the telemetry that says whether `LESSONS_PER_SESSION_MAX` should be 1 for a student who is opening many concepts a day.

## Slice L3. Re-teaching and diagnosis links

Landed 2026-09-29: app/lessons/refresh.py (T1 to T4, T5 a named hook), refreshers in blocks 1 and 2 and `read_again` in block 4, the LSN-PRQ ordering, `lesson_link` on feedback, "Read the part on this error" in app/web/src/session/ElaboratedPanel.tsx, tests/session/test_lesson_refresh.py. No LSN-PRQ records were authored.

Entry: L2.

### Files

| Path | Change |
|---|---|
| app/lessons/refresh.py | new: `refresher_targets(states, attempts_history, lesson_states, today)` for T1 to T4 (15, Re-teaching table); `serve_refresher` under `REFRESHERS_PER_SESSION_MAX`, `REFRESHER_MIN_GAP_DAYS` and the share cap; a block 3 match writes a `read_again` entry to block 4 |
| app/session/build.py | refresher entries in blocks 1 and 2, `read_again` entries in block 4; the LSN-PRQ ordering rule (prerequisite lesson before the concept lesson) |
| app/api/routes/sessions.py (feedback) | `lesson_link: {lesson_id, version, anchor}` when the graded option's `error_path` or `observed_errors[]` names an error the lesson anchors; none on a probe-tied diagnosis (15, Diagnosis links) |
| app/web/src/feedback/ElaboratedPanel.tsx | "Read the part on this error" after 03's three parts |
| content/lessons/ | LSN-PRQ records for flipped prerequisites, on demand from the 77 designs under docs/lessons/prerequisites/ |

### Tests and invariants

L14 (an LSN-PRQ is inserted only after a diagnosed gap flipped its BC-PRQ); a test per trigger; no link on a probe-tied diagnosis; T4 shown on a synthetic student stuck at example; T2 depends on Q9 (the decayed-support cap is now read by `serve_stage` since stage 14, ledger 2026-09-28, so Q9 is closed and T2 can be wired).

### Acceptance

Tests per trigger green; the no-link case; T4 on the synthetic student.

## Slice L4. Full coverage

Entry: L2; may run beside anything. Scope: the remaining concept lessons to 170 servable (BC-CON-06014 included, since it is now loaded), then LSN-PRQ for every BC-PRQ, from the designs in production order (below). Exit: 100 percent verification, audit of every lesson at 0 errors. Offline work: about 150 authoring sessions on top of L1's 19; the re-solve and sign-off sessions were run on the designs in this run and carry over by text equality (design to record path, steps 3 and 4), so the per-lesson offline cost is one authoring session plus the two comparison scripts, not three sessions.

## Slice L5. Evaluation

Entry: the P7 harness (built, waiting on real data). `app/sim/learning.py` gains `lesson_effect` on `WorldRules` and the `lessons_on` and `lessons_off` arms; the sweep 1.0, 1.25, 1.5 plus the negative arm; the break-even report under both forgetting curves (15, Offline simulation). `lesson_first_contact` in `randomised`; the two metrics (minutes to mastery per skill, delayed accuracy at matched minutes) on the dashboard with denominators. Amendment A-D5 adds the modality A/B: within `lesson_first_contact`'s treatment, the section-level delivery mode is switched between its designed mode and `text` on a per-concept seed, and skip rate by mode and time to first credited success by mode are reported per unit.

## Slice L6. Methods

Entry: L2; L4 for the strategy blocks on every concept. `strategy`, `cue` and `what_a_reader_scores` are on every signed-off lesson by construction of the designs (every design carries them). Decision lessons: the 10 designs under docs/lessons/decisions/ authored to records, the antiderivative-technique and series-test sets first where the derived sets hold them (the derived sets are LSN-DEC-02-01 to 02-03, 04-01, 05-01, 06-01, 06-02, 07-01, 08-01, 10-01; the two 01 names are checked against the set members at authoring). T5 in app/lessons/refresh.py reading 10's method-selection against execution metric. `app/progress/fluency.py` with the part budgets (I-A 2.14, I-B 2.92, II 15.0 by `scoring_pattern` share) and the map display; L15 to L18 at 1,000 cases.

## Order of lesson production

The entry fringe is Unit 1 (ledger 2026-09-29: "With the entry fringe in Unit 1"), so lessons are produced in fringe order: units 1 to 10, and within a unit in a topological order of concepts over the hard prerequisite edges between their skills (ties by id). The order was computed from data/prereq_edges.csv and data/skills.json on 2026-09-29 (PROGRESS.md records the command); the first twenty concepts are BC-CON-01001, 01002, 01003, 01006, 01004, 01005, 01007 to 01019 in id order, then Unit 2 in id order, then 03010 before 03001 to 03009, then Unit 4 as 04003, 04011 to 04015, 04001, 04002, 04004 to 04010, and so on. L1's 19 come first regardless of position because they are the P1 archetypes' concepts. Prerequisite lessons are produced on demand by flipped BC-PRQ (L3) and then in id order (L4). Decision lessons follow the unit order of their sets.

## Costs

Per plan 15, Costs against 14: `lessons.author_cycle` 371 calls at about $40, `lessons.verify_cycle` 1,081 re-solves at $4.71, `lessons.signoff_cycle` 1,976 block calls at $8.62, all offline at $0.00 API spend, with 1.5 attempts and a 2.0 body multiplier [inferred] (Q17). This run changes the split: the design run already spent the re-solve and sign-off sessions on the designs (257 designs, re-solved in batches and audited per lesson, counts in PROGRESS.md), so what L1 and L4 spend per lesson is one authoring session plus two scripts. The measured attempts per design and per authoring transcription go into 15's register as Q17's answer. The delivery layer adds a one-time build cost (four reader components) and no per-lesson cost, because a mode is chosen in the design and its spec is declarative.

## Pacing arithmetic

Dates from research/exam/exam-structure.md: 224 days from 2026-09-28 to 2027-05-10.

The binding constraint is not lessons. The ledger's 2026-09-29 throughput entry records that a perfect synthetic student masters 120 of 539 teachable skills in 220 days under the current mastery rule, and that changing it waits for the operator. Lessons add reading minutes inside block 2's 25 minutes and add no mastery evidence (15, L0), so under the current ceiling:

| Quantity | Value | Basis |
|---|---|---|
| Concepts a 120-skill student reaches | at most 120 skills across their concepts, about 40 to 60 concepts by the skills-per-concept distribution (1 on 25, 2 on 28, 3 on 46, 4 on 41, 5 on 23, 6 on 6, 7 on 1; 15, facts table) | 15 facts table; ledger throughput |
| First-contact lesson minutes for those concepts, full band | 60 x 6 = 360 minutes at the cap; the designs' measured full-band minutes (PROGRESS.md, Stage 5 numbers) replace the cap | 15 band table |
| Share of a 45-minute session, two full lessons | 12 of 45 = 26.7 percent; one refresher on top 13.5 of 45 = 30.0 percent, the cap | 15, Pacing |
| Sessions needed to serve 60 lessons at 2 per session | 30 of the 112 to 224 study days | 15, Pacing table |
| Items displaced per lessoned session | two full lessons take 12 of block 2's 25 minutes, so 4 items at the 3-minute default instead of 8 | `BLOCK2_MAX_MINUTES` 25; 01 Time budget |

So under the current ceiling the lesson layer cannot be what stops a student covering every unit; the mastery rule is (ledger, throughput). If the ruling lifts the ceiling toward 539 skills, the 15 pacing table applies unchanged: 170 lessons at 6 minutes are 1,020 minutes, 10 to 20 percent of 112 to 224 sessions of 45 minutes. Neither case is assumed here; the deferral count and reading share are the telemetry that decides `LESSONS_PER_SESSION_MAX`.

## Proposed amendments

Numbered, each with its source. None is made by this run; each is a proposal for the file named.

| Id | File and section | Amendment | Source |
|---|---|---|---|
| A-D1 | 15, Content model | Every section carries a `delivery` field: `mode` in text, step_reveal, figure, table, motion, interactive, model, contrast; `spec` (declarative, labels inside), `fallback`, `keyboard`, `reduced_motion` on motion; chosen in the design, never by the author | docs/lessons/TEMPLATE.md, Delivery; 01 Split-attention-free presentation; 04 Figures |
| A-D2 | 04, Figures | The figure spec gains `controls` (one slider or one draggable point, with domain and step) and `frames` (a parameter sweep rendered as discrete states) so interactive and motion blocks stay declarative and rule 13 still applies to every label | TEMPLATE.md Delivery; 04 rule 13 |
| A-D3 | 08, Motion rules | Instructional motion is distinguished from interface motion: a `motion` block is student-paced frames, may exceed 300 ms because it is content, and under `prefers-reduced-motion: reduce` steps on key press with a cross-fade (replace, do not delete) | 08 Motion rules; TEMPLATE.md |
| A-D4 | 15, UI | Reader components gain `FigureControl.tsx`, `FrameStepper.tsx`, `ModelTable.tsx`, `ContrastPanel.tsx`; one control per screen; no mode is served without its fallback | TEMPLATE.md |
| A-D5 | 10, A/B readiness and Learning-outcome metrics; 15, Telemetry | The modality A/B inside `lesson_first_contact`: designed mode against text per section, reporting skip rate by mode and time to first credited success by mode; section views log the mode | TEMPLATE.md; 15 Telemetry |
| A-1 | 15, What a lesson is | BC-CON-06014 is loaded by BC-QA-06017 (stage 15), so the "exists and is never inserted" case is empty | PROGRESS.md Stage 0 |
| A-2 | 15, Decision lessons | `confusable_with` is filled on 505 skills by tools/derive_confusable.py; the sets are read from it, and Q20's "after which the derivation becomes a check" has happened | PROGRESS.md Stage 0 |
| A-3 | 15, Content model, checks row | A concept whose skills hold no active BC-ERR (BC-CON-01003, BC-CON-01018) carries 2 checks; check 3 needs error blocks it cannot have | PROGRESS.md D3 |
| A-4 | 15, Sourcing, Pipeline | Steps 3 and 4 run once on the design and carry to the record by text equality (tools/lesson_resolve_compare.py); a changed stem, key or block text re-runs them | this file, design to record path |
| A-5 | 15, Content model, worked_examples row | Valued steps may relate by differentiate, integrate, evaluate, solve or limit as well as equivalence, each checked by CAS; tools/check_lessons.py gains the relations | TEMPLATE.md step relations; tools/check_lesson_designs.py |
| A-6 | 15, Re-teaching, T2 and Q9 | The decayed-support cap is read by `serve_stage` since stage 14, so T2 no longer waits on Q9 | ledger 2026-09-28 stage 14 |
| A-7 | 15, Register Q21 | The 78 archetypes without `asked_to_produce` are now counted from the designs (PROGRESS.md gap list) with the exact ids, so the library staging pass has its list | Stage 5 numbers |

## Library gaps hit by the designs

Filled at Stage 5 from the designs' `inferred` entries: archetypes without `asked_to_produce` or `common_givens`, archetypes whose `parameter_spec` lacks a parameter the lesson's draw needs (BC-QA-02008, product against quotient), BC-PRQ listed by no archetype's `prerequisites` (5), concepts without an active error (2), and any BC-FRQ or research heading a designer could not find.
