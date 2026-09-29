---
title: Lessons
research_date: 2026-09-28
status: draft
purpose: Specify the adaptive instruction layer (lessons, decision lessons and refreshers) that sits in front of the fading ladder, sourced from the library, verified like items, adapted per student by predicted knowledge, diagnosed error, method confusion and prerequisite gap, teaching the recognition cues, method choice, thought process and scoring habits the exam rewards, and integrated with the engine, session assembly, diagnosis, UI, API, evaluation and phased delivery without adding any mastery evidence.
---

# Lessons

## Problem, goal and what was read [verified]

Today a student with no placed units meets every new skill as a stage `example` item. `serve_stage` in `app/engine/fringe.py` returns `FadingStage.EXAMPLE` whenever `p_A_knowledge < STAGE_LOW` (0.50) and the primary skill has no credited observation. Since ledger stage 3 (commit 4b85ba3) that example shows the worked steps with the last step blanked, collects a graded answer and a confidence rating, and credits the result. Nothing comes before it. The one self-explanation prompt on it is the only instruction the student gets, and a student who has learned no units meets 541 skills that way.

The goal of this layer is stated as an objective, not as an outcome. The layer exists to bring a student who has learned no units to mastery of every BC skill in the fewest student-minutes, where mastery is the six-condition rule in `evaluate_mastery` (`app/engine/update.py`) and delayed retention is 10's retention at 7 and 30 days and the six-week released-material checkpoint. Lessons read, lesson checks passed and refreshers served count toward nothing. The metric that watches the layer is minutes to mastery per skill, and the layer is kept only while that metric and delayed accuracy do not get worse under the A/B in 10.

Read for this design, in full: CLAUDE.md; docs/plan 01, 02, 03, 04, 08, 10, 11, 14 and this file's draft, with 05, 06, 12 and 13 skimmed; BUILD-LEDGER.md through the stage 13 entry and the 2026-09-27 rulings; `app/engine/{fringe,select,update,state,constants,diagnostic,exam_weights}.py`; `app/session/{build,service,repository}.py`; `app/content/{loader,persist,reconcile,snapshot}.py`; `app/db/{models,migrate}.py`; `app/experiments/switches.py`; `app/sim/learning.py`; `app/audit/vocabulary.py`; `app/web/src/session/*`. Skimmed: `data/skills.json`, `data/archetypes.json`, `data/errors.json`, `data/misconceptions.json`, `data/prereq_edges.csv`, `data/ids.json`, research/units/unit-06 and the heading structure of all ten unit files, research/README.md, research/exam/exam-structure.md.

Facts computed from `data/` on 2026-09-28 that shape the design. Every count below is a computation over the registry files named, not a recollection.

| Fact | Value | Where computed |
|---|---|---|
| Concepts, skills, non-calculus prerequisites | 170 BC-CON, 541 BC-SKL, 77 BC-PRQ | `data/skills.json` |
| Skills per concept | 1 on 25, 2 on 28, 3 on 46, 4 on 41, 5 on 23, 6 on 6, 7 on 1 (by each skill's `concept` back-reference; the concept `skills` lists sum to 544 because BC-CON-06001 and BC-CON-06007 list skills whose back-reference names another concept) | `data/skills.json` |
| Concepts in exactly one topic | 162 of 170; 6 in two, 2 in three | `data/skills.json` |
| Concepts that are the primary skill's concept of at least one active archetype | 111 of 170. The other 59 are loaded only as secondary skills | `data/archetypes.json` `skills[0]` (R25) against `data/skills.json` |
| Concepts loaded by no active archetype at all | 1, BC-CON-06014 | same |
| Skills loaded by no active archetype | 19 (BC-SKL-02001, 03001, 03020, 03023, 05011, 05013, 06007, 06009, 06040 to 06046, 06053 to 06055, 07028) | same |
| Distinct concepts per active archetype | 1 on 44, 2 on 52, 3 on 29, 4 on 10, 5 on 2, 7 on 1, 8 on 1 | same |
| Skills per active archetype | 1:4, 2:15, 3:22, 4:34, 5:31, 6:14, 7:8, 8:5, 9:4, 11:1, 14:1, mean 4.55 | `data/archetypes.json` |
| Active errors, active misconceptions | 391 BC-ERR (the loader pins 391 since stage 13), 213 BC-MIS with severity high 123, medium 89, low 1; errors carry no severity field | `data/errors.json`, `data/misconceptions.json` |
| Active errors whose `skills` intersect a concept | 0 on 2 concepts, 1 on 18, 2 on 29, 3 on 36, 4 on 26, 5 on 21, 6 on 20, 7 on 9, 8 on 7, 9 on 1, 10 on 1 | same |
| Distinct BC-EK per concept, through its skills' `essential_knowledge` | 0 on 3, 1 on 110, 2 on 38, 3 on 16, 4 on 3 | `data/skills.json` |
| `description_plain`, `description_formal` median length | 16 and 32 words; `notation` non-empty on 163 of 170 | `data/skills.json` |
| Longest `hard_prerequisite` chain over BC-SKL | 10 (BC-SKL-05063, BC-SKL-07037); depth 0 on 158 skills, 1 on 93, 2 on 71, 3 on 57, 4 on 50, 5 on 42, 6 on 29, 7 on 21, 8 on 15, 9 on 3, 10 on 2 | `data/prereq_edges.csv` |
| Published items in the bank | 3,124 records under `content/items_*`, every one of the 139 active archetypes with at least 20 (ledger, stage 5) | `content/` |
| Days from 2026-09-28 to the exam, Monday 10 May 2027 | 224; the desired-retention switch on 2027-03-15 is 168 days away | `research/exam/exam-structure.md` [single-source] for the date |

Two of those facts change the draft. The draft keyed the first-contact lesson on the primary skill's concept, which can never reach 59 of the 170 concepts. And the draft assumed `concept_opener_done` is consumed by session assembly; the engine and session code only store, load and merge it (`app/session/repository.py`, `app/content/reconcile.py`), so the productive-failure opener is a plan rule with no code behind it yet (11, R35).

Two rulings in the ledger bind this document. On 2026-09-24 the operator ruled that no human review will ever be done and that Claude performs every review, sign-off and audit the plan assigns to the operator, naming itself as author and recording that the record is not human (ledger, Plan corrections, 2026-09-24). On 2026-09-23 the operator ruled that agent drafts may be served but count toward nothing unless relabelled `operator`. The publication rule in the sourcing section follows both.

## What a lesson is, and its granularity [inferred]

### The unit stays the BC-CON concept, with one change to how it is reached

The lesson unit is the concept, so there are 170 concept lessons, `LSN-CON-<nnnnn>`, and up to 77 prerequisite lessons, `LSN-PRQ-<nnnnn>`, the second kind built only for a BC-PRQ a diagnosis has flipped. Per-skill (541) and per-archetype (139) are rejected, for the reasons the draft gave and one more each.

- Per-skill is too fine. 510 of 541 skills are never isolated by an archetype, 25 concepts hold one skill and 46 hold three, and the skills of one concept share the concept's `description_formal`, its `notation` and its topic's Required mathematical knowledge paragraph. A per-skill lesson restates its siblings and the reading minutes break the share cap below.
- Per-archetype is the wrong axis. An archetype loads 1 to 14 skills across 1 to 8 concepts (44 load one concept, 95 load two or more). Teaching by archetype is teaching to the item, and the same concept would be taught up to 6 times (BC-CON count of archetypes whose primary skill it holds: 1 on 91, 2 on 16, 3 on 2, 4 on 1, 6 on 1).
- Per-topic (111) is too coarse in 54 topics, which hold 2 to 4 concepts each, and a topic lesson would front-load concepts the fringe has not reached. It is the right slice of research/units, so the topic section is the sourcing slice and the concept is the served unit.

The change: the first-contact trigger reads every skill the item loads, in the archetype's `skills` order, not only `skills[0]`. That reaches all 169 concepts an active archetype loads. BC-CON-06014 is loaded by nothing, so its lesson exists in the library and is never inserted, which is the same fail-open path a missing lesson takes (invariant L12).

### What adapts and what is fixed

A lesson is one authored body with sections that carry band, trigger and prerequisite flags, and a deterministic function assembles the served plan from the student's state at serve time. There is no per-band or per-error authoring, because 170 concepts times three bands times four errors would be an authoring and verification load no single operator can review, and because the adaptation the evidence supports is a change of dose and order, not of explanation. The four axes:

1. **Predicted knowledge band**, read from the same `p_A_knowledge` value `serve_stage` computes for the item the lesson precedes: below `STAGE_LOW` (0.50) the full form, between the bands the brief form, above `STAGE_HIGH` (0.90) no insertion and a link on the item. Reusing the two existing constants means the lesson dose and the initial fading stage move together, which is Salden's adaptive-fading argument applied one step earlier (01 Adaptive worked-example fading [single-source]), and the top band is Kalyuga's expertise-reversal guard (01 [single-source]).
2. **Diagnosed error**, a BC-ERR id from an MCQ distractor's `error_path` or from `DiagnosticianOutput.observed_errors[]`. It selects the `common_errors` block anchored to that error, both for the feedback link and for the refresher's opening block.
3. **Misconception candidate**, a BC-MIS id. It never selects content on its own. It appears only as the "a possible reason" line inside the error block it is linked to, in the corpus's own words, never in the second person, and the discriminating probe stays the only place the app acts on it (03, Feedback never names a misconception as established).
4. **Prerequisite gap**, a BC-PRQ or BC-SKL id from `prerequisite_gaps[]` or from a flipped BC-PRQ row. A BC-PRQ selects its `LSN-PRQ` lesson and the concept lesson's `prerequisite_bridge` paragraph for that prerequisite. A BC-SKL selects that skill's own concept refresher.

### IDs, with no minting

Lessons are application content, like `ITM-AGT-01004-00`, not library records. They are not minted in `data/ids.json`, which keeps the library's append-only rule untouched, and `BC-LSN` is not registered, because the library holds facts and a lesson is a product artefact built from them.

- `LSN-CON-06004` teaches BC-CON-06004. `LSN-PRQ-06005` teaches BC-PRQ-06005.
- A section id is `LSN-CON-06004#s<n>`; an error block is `#err-BC-ERR-06005`; a check is `#chk-<n>`; a prerequisite bridge is `#prq-BC-PRQ-06005`.
- `version` is an integer. The immutable body key is `(id, version)`. A served or read version is recorded in `lesson_state.version_seen` and never rewritten.
- `provenance.author` is `operator` or the model id; `provenance.signed_off_by` names who signed it off and is a model id under the 2026-09-24 ruling.

### Content model

Stored at `content/lessons/LSN-CON-06004.json`, schema `schemas/lesson.schema.json`. Sections come in a fixed order. Each carries `skills[]`, `sources[]`, `evidence_tag` (operator-facing only), `bands` (a subset of `low`, `mid`) and, on error blocks, `error_id`.

| Section | Cardinality | Bands | Source of every sentence |
|---|---|---|---|
| `orientation` | 1, at most 60 words | low, mid | the concept's `description_plain` and its topic's Assessment behaviour paragraph, stated as what a response must show; no count, no frequency, no predict-talk (`qa/08_prediction.py` lexicon reused as a lint) |
| `key_ideas` | 1 block per BC-EK the concept's skills map, at most 120 words each, `depth` `core` or `extended`; at most 2 core | core: low, mid; extended: low | the topic's Required mathematical knowledge paragraph paraphrased, citing `BC-EK-*` and `ced:<page>`; at most one anchor quote of 25 words or fewer per block; the notation line from the concept's `notation` |
| `strategy` | 1 per archetype family that loads a skill of this concept, at most 80 words each, at most 3 | low, mid (first only in mid) | the family's `asked_to_produce` and `common_givens` as the recognition cue, the first entry of `expected_solution_path` as the first written step, the `wrong_approaches` and `prohibited_shortcuts` entries as the named rival, all verbatim from the archetype record; see the methods section |
| `worked_examples` | 1 or 2; example 1 for both bands, example 2 for low only | as stated | a real archetype's `parameter_spec` draw, from an archetype whose `skills` include a skill of this concept, primary preferred; steps follow `expected_solution_path`; each step carries a MathJSON or SymPy expression, a `cue` line of at most 20 words naming what in the stem or the previous line selects the step, a `why` line of at most 25 words, and a BC-PT tag where `point_types` is non-empty (04 rule 9, R14) |
| `what_a_reader_scores` | 1 checklist per worked example, one line per BC-PT the archetype lists, at most 6 lines; absent on the 56 archetypes without `point_types` | low, mid | the BC-PT `earns`, `does_not_earn`, `notation_requirements`, `precision_rules`, `units_required` and `hypotheses_required` fields, restated as the check the student runs before the answer line; see the methods section |
| `common_errors` | 1 block per active BC-ERR whose `skills` intersect the concept's skills, at most 4, ordered by the highest `severity` of the linked BC-MIS then by id; the mid band shows the first 2 | low: all; mid: first 2 | `observed_behavior` and `scoring_consequence` verbatim from the record; the wrong step beside the right step, both CAS-checked; the "a possible reason" line from the BC-MIS `description`, kept separate from the error as CLAUDE.md requires |
| `representations` | 0 or 1 | low | the topic's Representations paragraph, with a declarative figure spec whose labels sit inside the figure (04 Figures, rule 13) |
| `prerequisite_bridge` | 1 paragraph per BC-PRQ that is a `hard_prerequisite` or `supporting` parent of a skill of this concept, at most 60 words | gated by state, not band | the BC-PRQ `description_plain` and `failure_signature` |
| `checks` | 2 or 3 item-shaped records: check 1 is the completion form of worked example 1 (last step blanked), check 2 an isomorph short answer from the same archetype, check 3 a 4-option MCQ whose distractors come from the error blocks above; low band serves all, mid band serves 1 and 2 | as stated | the item pipeline's record shape, so `app/items/grade.py` grades them unchanged; each distractor's `error_path` links to a `#err-` anchor (04 rules 5 to 7) |
| `refresher` | pointer list | trigger-selected | the ids of the `key_ideas` core blocks, the error blocks and worked example 1, in the order the refresher serves them |

Other fields: `read_minutes` with `full` and `brief` authored forecasts, capped by `LESSON_READ_MINUTES_MAX` (6) and `LESSON_BRIEF_MINUTES_MAX` (3); `word_count` with `full` and `brief`, capped by `LESSON_WORDS_FULL_MAX` (900) and `LESSON_WORDS_BRIEF_MAX` (450); `snapshot_digest`; `source_digest`, a hash over the exact library records and research/units lines used; `status` in `draft`, `checked`, `resolved`, `signed_off`, `stale`, `retired`; `provenance` with `author`, `prompt_version`, `generated_at`, `signed_off_by`, `signed_off_at`, `not_human: true`.

The word caps are the minute caps at an assumed 150 words per minute of mixed prose and mathematics. No source in the ledgers gives a reading rate for calculus prose, so both caps are [inferred] and the forecast replaces the assumption after five completed lessons (engine section). The 60-word orientation and the 25-word why line are choices made so the reader never holds more than one idea per screen (01 Split-attention-free presentation, [inferred] count).

Why the lesson's worked examples carry no free-text self-explanation prompt. 01 fixes exactly one structured prompt per worked example and per corrected error, and the graded example item that follows the lesson already carries it. A second prompt seconds earlier would double the time cost Rittle-Johnson names for mathematics (01 Structured self-explanation [single-source]) and the check questions already ask the student to produce the step. The why line on each step is the explanation; the prompt stays on the graded item.

### Storage and versioning through content snapshots

`app/lessons/ingest.py` follows `app/items/ingest.py` into the tables `lessons` and `lesson_verifications`. A signed-off lesson row records the `snapshot_id` it was signed off under.

On a snapshot reload, `app/content/reconcile.py` gains `reconcile_lessons(db_session, new_snapshot, ids_registry)`: a lesson goes to `stale` when any BC-* id it references is tombstoned in `data/ids.json` or the recomputed `source_digest` differs. It is never rewritten automatically, because prose cannot be merged the way counts are; it is enqueued in `review_queue` with kind `lesson_stale`, the audit action `lesson_stale` is written, and the engine stops inserting it. A concept with no servable lesson falls back to today's example-first behaviour and writes `lesson_gap_fail_open`, one row per user, concept and day like `write_coverage_gap_audit`. `lesson_state` rows for a tombstoned concept follow `superseded_by` as `reconcile_skills_state` does for skills. Note that `reconcile_skills_state` itself is called by no application code today (only `tests/content/test_reconcile.py`), so wiring the reload path is a prerequisite carried in the open questions.

## Sourcing, authoring and verification [inferred]

### Where the facts come from

Only from the library, under CLAUDE.md's rule that facts come from the cache or `data/sources.json` and never from model memory. The authoring input is assembled by code, `app/lessons/source.py: authoring_bundle(concept_id, snapshot)`: the BC-CON record; its BC-SKL records with their `adaptive.*` text; the topic section of research/units sliced by its `## N.M` heading, minus the Official mapping subsection, which quotes EK statements verbatim and may not be reused; the linked BC-ERR, BC-MIS, BC-SIG and BC-PT records; the archetype `parameter_spec` and `expected_solution_path`; the BC-PRQ records on the concept's parents; and the cached CED page text for each cited `ced:<page>`, used only to check quotes. The Required mathematical knowledge subsections already paraphrase (median 126 words, one section in 111 carries a quoted string of 20 characters or more), so they are the model's primary source for `key_ideas`.

The model writes connecting prose and chooses the parameter draws. Every mathematical claim in a worked example is computed and checked by CAS rather than asserted. Every exam-scoring claim cites an `sg-YY:page` or `cr-YY:page` already present in the input.

### Pipeline

It mirrors 04 and reuses `app/items/ingest.py`, `app/items/verify.py` and `tools/check_items.py`.

1. **Authoring** uses the existing `generator` role with a new template `prompts/generator/lesson_v1.md` and structured output against `schemas/lesson.schema.json`. No seventh role (07, R17). Authoring runs offline in Claude Code sessions under `docs/operator/offline-authoring.md`, one session per concept, at $0.00 API spend, the same shape as the item and template passes.
2. **Deterministic checks** in `tools/check_lessons.py`, exit 0 only when every lesson is clean: schema validation; referential integrity, every BC-* id active in the current snapshot; band coverage, every skill of the concept named by a `key_ideas` block or a worked example in both bands; each worked step following from the previous one under `verify.equivalence` (04 rule 15), no vacuous identity; final answers checked numerically at several points; the calculator boundary (04 rule 8); distractor rules 5 to 7 on check 3; at most one quote of 25 words or fewer per block, matched against the cached page (the `qa/07_quotes.py` rule reimplemented over `content/lessons/`); the MinHash duplicate gate against the official corpus text at the stage-one settings 04 records (rules 10 and 12); the style lint (no em dashes, no en dashes as punctuation, no emojis, no praise, no study advice, no schedules, no second-person belief statements); the prediction lint; the word and minute caps in both bands; every `#err-` anchor resolving; every check distractor's `error_path` among the errors held by the concept's skills (`app/items/distractor_paths.py` reused); and the draw exclusion, no worked-example or check parameter draw equal to the `parameter_draw` of any published item on the same archetype (invariant L10).
3. **Independent re-solve.** A separate blind Claude Code session sees each worked example's problem statement and each check stem, never the key or the steps, and writes its own keys to its own file; a script compares them by SymPy and numerically, as `docs/operator/offline-authoring.md` step 2 and the 2026-09-24 verifier ruling require. Agreement moves the lesson to `resolved`; disagreement opens a `review_queue` row of kind `lesson_resolve_disagreement`.
4. **Sign-off review.** A further blind Claude Code session on the operator's delegation reads the rendered lesson beside its source slice, re-derives every `key_ideas` claim against its cited record, and records a verdict per block in `docs/operator/lesson-audit/<id>.json` with `auditor` set to the model id. Zero unsourced claims and zero mathematical errors moves the lesson to `signed_off`. Anything else stays `resolved` with the blocks named. The operator may review any lesson in the review screen and may relabel provenance, exactly as the item ruling allows, but no gate waits on a human.

**Publication rule.** Servable means `status = signed_off` and not `stale`. This is stricter than the item precedent, where drafts are served on ingest, because a wrong lesson teaches a false rule to every later item on the concept while a wrong item teaches it once. It stays inside the 2026-09-24 ruling because the sign-off is a model review on delegation, not a human one.

### Costs against 14

Runtime cost is zero: lessons are static, no tutor call runs inside the reader, no chat box sits beside a lesson (01 What the evidence does not support; 08 anti-pattern "chat-first layout"), and checks grade deterministically through `app/items/grade.py`. The one-time work is priced by two new line groups in `tools/cost_model.py`, `lessons.author_*` and `lessons.verify_*`, so that `python3 tools/cost_model.py --check docs/plan/15-lessons.md` can hold this file to the calculator. Until those lines exist every figure below is the formula's output and [inferred], and none is quoted elsewhere.

| Line | Calls | Unit price basis | API-equivalent |
|---|---|---|---|
| `lessons.author_cycle` | 170 concept lessons plus up to 77 prerequisite lessons, at 1.5 authoring attempts each, 371 calls | the template call `template.call_cost` ($0.0540 on `claude-opus-5-5` batch, 14) times 2.0 for a lesson body priced at 2,200 visible tokens against a template's 1,100 | about $40 |
| `lessons.verify_cycle` | 170 by (2 examples and 3 checks) plus 77 by (1 example and 2 checks), 1,081 blind re-solves | `verifier.call_cost` on `claude-haiku-4-5` batch, $0.004360 (14) | $4.71 |
| `lessons.signoff_cycle` | 247 review sessions | priced as a verifier call per block, about 8 blocks per lesson, 1,976 calls | $8.62 |

That is about $53 against the $7.05 left under the $100.00 Claude-only ceiling, so it cannot run on the API key. All three lines run offline on the operator's Claude Code subscription, as the template and verifier lines already do (14, Offline work), at $0.00 API spend, and `app/providers/guard.py` refuses a lesson authoring, re-solve or sign-off job on the API backend. The 1.5 attempts and the 2.0 body multiplier are [inferred] and are the two quantities the first authoring pass measures; both go in the register.

## Adaptation to the student [inferred]

One function decides what is served: `app/lessons/plan.py: plan_lesson(lesson, band, reason, error_ids=(), prerequisite_ids=(), lesson_state=None) -> LessonPlan`. It is pure, it reads no database, and its output is `(sections in order, checks, minutes, reason, anchors)`. The reader renders the plan and nothing else.

### By predicted knowledge

`band` is computed once, in session assembly, from the item the lesson precedes: `p = p_knowledge(archetype, states, graph.hard_parents, retrievability)`, the same call `serve_stage` makes.

| `p` | Band | Plan | Minutes |
|---|---|---|---|
| `p < STAGE_LOW` | low | orientation, all key ideas, example 1, errors (up to 4), check 1, example 2, check 2, representations, check 3, closing line | at most `LESSON_READ_MINUTES_MAX` = 6 |
| `STAGE_LOW <= p <= STAGE_HIGH` | mid | orientation, core key ideas, example 1, first 2 errors, check 1, check 2, closing line | at most `LESSON_BRIEF_MINUTES_MAX` = 3 |
| `p > STAGE_HIGH` | none | no insertion; the item carries `lesson_link` | 0 |

The bands are the ones 02 already owns (R4, R32), so the band edges add no new threshold and no new tunable row. A student whose first item on a concept arrives at stage `unsupported` is exactly the student Kalyuga's expertise reversal warns against instructing (01 [single-source]), and the brief form for the middle band is the dose-reduction Salden's adaptive fading applies (01 [single-source]). Whether the mid band should get the brief form or nothing is the one real free choice here; it is Q2 in the register and an A/B candidate.

### By diagnosed error

When an attempt's graded result names a BC-ERR, `error_ids` carries it. In feedback, `plan_lesson` returns the anchor for the matching error block, which the feedback payload exposes as `lesson_link` (diagnosis section). In a refresher, the named error blocks are served first, then the core key ideas, then example 1 collapsed to its step list. A first-contact plan is never reordered by an error, because no error exists yet.

### By misconception candidate

`plan_lesson` accepts no misconception id. A BC-MIS reaches the reader only as the "a possible reason" line inside the error block that `possible_misconceptions` links it to, in the record's own words, and only when the error block is shown. The block never says what the student believes. When the diagnosis writes a probe to `pending_probes` for a top-two tie, the feedback carries no lesson link at all, so the probe stays uncontaminated (03, Rival handling).

### By prerequisite gap

`prerequisite_ids` carries the ids from `prerequisite_gaps[]` above the probe threshold, and the ids of any BC-PRQ parent whose `skills_state.mastered` is false. For each BC-PRQ in that list the concept lesson's `#prq-` bridge paragraph is inserted after the orientation, and if the BC-PRQ has a servable `LSN-PRQ` lesson and its `lesson_state` is `unseen`, that lesson is served as its own first-contact lesson before the concept lesson (engine section, order rule). A BC-SKL in the list selects that skill's concept refresher instead of a bridge, because a calculus prerequisite has its own lesson. `LSN-PRQ` bodies are built from `description_plain`, `failure_signature` and the topic Prerequisites lines that cite the record, with one worked example drawn from an archetype whose `prerequisites` list the record (BC-QA-06001 lists BC-PRQ-06005, 06008 and 06012, 02 BC-PRQ handling).

## Sequencing within and across concepts [inferred]

### Within a concept

The order for a concept the student meets for the first time, low band:

1. The productive-failure opener, only for a concept among the five conceptual targets in 01 and only while `concept_opener_done` is 0 on the concept's first skill. The opener is a generation attempt on an archetype carrying BC-DF-13 or BC-DF-15 (18 active archetypes carry one of them), uncredited (02 Session assembly). It is out of P1 scope and is not wired today (11, R35); until it is, step 1 is absent and the order starts at step 2.
2. The lesson, band-planned. When an opener preceded it, worked example 1 is rendered with a `comparison` callout that names the gap between the opener attempt and the canonical method, which is the obligatory comparison step of Loibl, Roll and Rummel (01 [single-source]). Putting the lesson before the opener would remove the "problem solving before instruction" condition behind Sinha and Kapur's g = 0.36 (01 [verified]).
3. The graded stage `example` item, with its one self-explanation prompt, credited under 02's rules. The lesson does not let the student skip it (R32 is untouched).
4. `completion`, then `unsupported`, moved only by the R7 counter pair.
5. Block 3 retrieval after `RETRIEVAL_ENTRY` (R8), FSRS reviews in block 1 after mastery, refreshers on the triggers in the re-teaching section.

Worked examples, completion problems and retrieval interleave inside the lesson by construction: example 1 is read, check 1 is its completion form, example 2 is read, check 2 is an isomorph the student produces. That is backward fading applied inside the lesson before the ladder begins (Renkl et al 2002, 01 [single-source]), and the checks are massed retrieval, which is why they are uncredited (01, Roediger and Karpicke's five-minute null [verified]).

### Across concepts

Lessons are not sequenced separately. Selection stays the two-term due-coverage rule with random ties (R4), and a lesson rides on the item it precedes, so gating (invariant 3), the interleaving window and `filter_exam_weight` (`app/engine/exam_weights.py`) apply unchanged. The only ordering the lesson layer adds is the rule that when an item's `lesson_target` is a concept whose `LSN-PRQ` prerequisite lesson is also due, the prerequisite lesson goes first.

The expertise-reversal guard has three parts: the none band above, the always-present skip control in the reader, and the deferral rule below, which bounds reading per session. No withholding probe is added at the lesson layer; 01's occasional withholding at stage `completion` already measures reversal on the ladder.

### When instruction steps back

Instruction steps back on the triggers in the next section and never on a timer. It never steps back into a full first-contact lesson except on trigger T4, where the ladder cannot drop further.

## Re-teaching [inferred]

A refresher is the `refresher` subset of the lesson at most `REFRESHER_MINUTES_MAX` (1.5) minutes, ordered trigger-first, with no orientation, no checks and no closing line. Every refresher is uncredited. Each trigger inserts at most one refresher per trigger event, a concept receives at most one refresher per `REFRESHER_MIN_GAP_DAYS` (3), a session carries at most `REFRESHERS_PER_SESSION_MAX` (2), and the share cap in the engine section bounds their minutes together with first-contact lessons.

| Trigger | Condition, read from state the engine already writes | Where the refresher goes | What differs from first contact |
|---|---|---|---|
| T1 un-mastery | `evaluate_unmastery` flipped `mastered` false on a skill of the concept since the last session | before that skill's next block 1 or block 2 item | error blocks for any BC-ERR on the failing attempt first, then core key ideas |
| T2 decayed support | a mastered skill with `R_k < DECAYED_SUPPORT_CAP_RETRIEVABILITY` (0.5) at its next encounter (02 Decay). The cap itself is a plan rule not yet read by any code, carried as Q9 | before the item in block 1 or 2; if the item lands in block 3 the refresher is deferred to block 4 as a "Read again" link so it never cues a criterion item | core key ideas, then example 1 collapsed |
| T3 prerequisite gap | a diagnosed `prerequisite_gap` naming a BC-SKL of the concept (03) | before the next item loading the dependent skill | the bridge paragraph for the named prerequisite, then the error block; for a BC-PRQ the `LSN-PRQ` first-contact lesson is served instead and the PRQ sits at the head of the queue (02 BC-PRQ handling) |
| T4 stuck at example | `fading_stage == EXAMPLE` and `consecutive_failures >= FADING_DROP_AFTER` (2) on a skill of the concept, the case where `drop_fading` clamps and nothing else responds | before that skill's next block 2 item | the full low-band plan minus the checks, once; a second T4 within `REFRESHER_MIN_GAP_DAYS` serves the refresher subset only |
| Hypercorrection requeue | none | the requeue is the treatment | |
| Re-diagnostic after `GAP_DAYS_DIAGNOSTIC` (21) | none | the diagnostic measures and changes no lesson state | |

| T5 method confusion | on a confusable set (methods section), method-selection accuracy over the last `METHOD_CONFUSION_WINDOW` (6) attempts is below `METHOD_CONFUSION_FLOOR` (0.5) while execution accuracy on the same attempts is at or above it, read from 10's method-selection against execution metric | before the next block 2 item on any skill of the set | the set's decision lesson `LSN-DEC`, not a concept refresher; once per set per `REFRESHER_MIN_GAP_DAYS` |

Refreshers are read, not restudied: the spacing literature's restudy is re-reading after a failure with no retrieval, and 01 restricts restudy to failure. T1, T3 and T4 fire on a failure, T2 fires when retrievability says the next attempt is likely to fail, and T5 fires on a run of method failures, so all five are restudy on failure in 01's sense.

## Methods, thought process and scoring habits [inferred]

Concept lessons say what an idea is and what goes wrong. They do not by themselves teach the three things the exam pays for on every item: seeing which method the stem is asking for, writing the first step that method needs, and checking the answer line against what a reader scores. This section adds those three, from library fields that already exist, and a fourth thing the app can measure but never credit, fluency.

### Recognition cues and the first step, the `strategy` section

Every archetype record already separates the cue from the method. On the 61 active archetypes that carry them, `asked_to_produce` names the object the stem asks for (BC-QA-06005: an integral expression with the initial value, or a numerical value with units), `common_givens` names what the stem supplies, `expected_solution_path[0]` is the first written step, and `wrong_approaches` names the rival methods (BC-QA-06005: reporting the net change as the amount; antidifferentiating and substituting only the upper limit). 10 active archetypes carry `prohibited_shortcuts`. On the 78 active archetypes without `asked_to_produce`, the strategy block is built from `typical_wording` and `expected_solution_path[0]` alone and carries `evidence_tag: inferred` until the library fills the fields, which is a library gap listed in the register.

A strategy block therefore reads, in this fixed order and with no other content: the cue, in the archetype's words; the method, named as the first step of `expected_solution_path`; the rival, from `wrong_approaches`, with the one feature of the stem that separates them. The `cue` line on every worked step carries the same discipline down the whole solution: not only why the step is right, but what selected it. That is the difference between a worked example a student can copy and one a student can transfer, and it is the boundary Renkl and Atkinson draw between example study and problem solving (01 Adaptive worked-example fading [single-source]).

### Decision lessons for confusable sets

01 names method-selection drills for antiderivative technique and series convergence tests and sources neither. The library now holds the two selection archetypes those drills need, BC-QA-06016 (selecting an antidifferentiation technique from the integrand) and BC-QA-10001 (selecting a convergence test for a given series), plus 18 active archetypes carrying BC-DF-09 (theorem recognition) and 4 carrying BC-DF-15 (unsignposted procedure selection). What the library does not hold is a `confusable_with` list: the field exists on every skill and is empty on all 541. The confusable sets are therefore derived, by code, from `adaptive.common_confusions`, which names a BC-SKL id on 315 of 541 skills and a BC-MIS id on most of the rest, and from `rival_misconceptions` on 210 of 213 active BC-MIS records mapped back to skills through `misconceptions.skills`. `app/lessons/confusable.py: confusable_sets(snapshot)` builds the undirected graph of those references over BC-SKL ids and returns its connected components of size 2 to `DECISION_SET_MAX` (6), each restricted to one unit, ordered by id. The count of sets is a computation, published by `tools/check_lessons.py --sets`, and is not guessed here.

A decision lesson, `LSN-DEC-<unit>-<nn>`, teaches one set. Its body is: two to four stems, one per method in the set, drawn from the set's archetypes with parameters chosen so the stems differ in exactly the feature that selects the method; the strategy blocks of those archetypes side by side; and `LESSON_CHECKS_MAX` discrimination checks in which the student names the method before any execution, built as 4-option MCQ whose options are the set's methods and whose distractors carry the `error_path` of the BC-ERR that the wrong method produces. No decision lesson asks the student to execute, because 01's drill strips execution on purpose: the metric it moves is method-selection accuracy with execution flat (10). Contrasting stems side by side is the interleaving mechanism itself, discrimination among confusable strategies (Rohrer et al 2020 [verified]; Brunmair and Richter 2019 [verified], both in 01), served as reading before the mixed set rather than instead of it.

When a decision lesson is served: first, as an insertion before the first block 3 item that loads a second member of a set whose first member the student has reached `unsupported` on, once per set, under the same count and share caps as a first-contact lesson; afterwards only on trigger T5. It is never served before a set's first concept is met, because a choice among methods the student has not learned is noise.

### The scoring checklist, `what_a_reader_scores`

The 76 BC-PT records already say what earns and what does not, and 03 turns them into the grader's per-point call. The same fields, restated once per worked example as the checks the student runs before writing the answer line, are the thought process the rubric rewards: limits match the requested interval (BC-PT-99001), the differential is present, the constant of integration is written or the record says it may be omitted (BC-PT-99003, sg-25:14), units are attached where `units_required` is yes, a reported decimal is accurate to three places (the general scoring note in 01, [verified]), the theorem's hypotheses are stated where `hypotheses_required` is yes, and no sentence is added that contradicts an earned claim (01 FRQ justification [single-source]). Each line is generated from the record fields by `app/lessons/source.py: reader_checks(point_type_ids)` and verified by the checker as a pure function of the records, so the model writes none of it. On the 56 archetypes without `point_types` the section is absent and the lesson says nothing about scoring, because a step named without a point would assert a rubric the library does not carry (R14).

The checklist is the one place a lesson names points, and it names them exactly as 03's feedback does, so the student meets the same six words on the lesson, on the feedback screen and on the checkpoint report.

### Fluency, measured and never credited

Time is a pacing metric, never mastery evidence, because speededness contaminates ability estimates (05, [single-source]). The exam's own budgets, from `research/exam/exam-structure.md` [verified]: Section I Part A is 29 questions in 62 minutes, 2.14 minutes each; Part B is 13 in 38, 2.92 each; Section II is 2 questions in 30 minutes and 4 in 60, 15.0 minutes each. A skill is `fluent` when it is mastered and the running median `elapsed_ms` of its credited unsupported attempts, over at least `FLUENCY_MIN_ATTEMPTS` (5), is at or below the budget for its archetype's exam shape: the Part A figure for a `no_calculator` MCQ-shaped archetype, the Part B figure for a `calculator` one, and `scoring_pattern`'s share of 15 minutes for a free-response part. `fluent` is a derived display value on the mastery map, computed by `app/progress/fluency.py`, stored nowhere in `skills_state`, and read by no selection function. What fluency does change is instruction: a mastered skill that stays below fluent after `FLUENCY_MIN_ATTEMPTS` attempts gets its strategy block, not its concept refresher, as a `read_again` entry in block 4, at most once per `REFRESHER_MIN_GAP_DAYS`, because a slow correct answer is a method found late, not an idea missing.

Accuracy is reported the same way. No target of 100 percent appears anywhere in the product, because a claimed accuracy is a prediction of an exam outcome and CLAUDE.md forbids predict-talk. What is shown, with denominators, is 10's method-selection accuracy against execution accuracy per confusable set, the per-point earning rate against the published 2025 per-point means (10, Leniency calibration), and time per item against the part budget.

### What this adds to the checker, the invariants and the evidence

`tools/check_lessons.py` gains: every strategy block's cue, method and rival traceable to the named archetype fields or, where absent, tagged inferred; every `cue` line present and at most 20 words; every `what_a_reader_scores` line a pure function of its BC-PT record, regenerated and compared; every decision lesson's stems differing in exactly one selecting feature, asserted by the checker over the two parameter draws; every discrimination check's distractors carrying an `error_path` held by the set's skills.

Invariants L15 to L18 in the quality section bound the additions. Evidence handling is unchanged: decision-lesson checks go to `lesson_check_responses`, fluency reads `attempts` and writes nothing, and T5 reads 10's metric and writes only `lesson_state`.

Constants, all [inferred] and in the register: `DECISION_SET_MAX = 6`, `METHOD_CONFUSION_WINDOW = 6`, `METHOD_CONFUSION_FLOOR = 0.5`, `FLUENCY_MIN_ATTEMPTS = 5`, `STRATEGY_WORDS_MAX = 80`, `CUE_WORDS_MAX = 20`.

## Evidence handling and the bounding invariant [verified]

Opening, reading, skipping or answering any part of a lesson or refresher writes nothing to `skills_state`: not `credited_successes`, `credited_failures`, `stability`, `difficulty`, `last_practised_at`, `observation_count`, `credited_observation_count`, `unaided_success_count`, `distinct_archetypes_succeeded`, `success_days`, `mastered`, `mastered_at`, `hypercorrection_due`, `consecutive_successes`, `consecutive_failures`, `fading_stage` or `concept_opener_done`. Check answers go to `lesson_check_responses`, never to `attempts`, so they never enter `load_attempts_history` (`app/session/repository.py`), `count_unsupported_successes`, `forecast_minutes`, the requeue lanes, the diagnostician's recurrence count (03, When the diagnostician is called at all) or FSRS.

The exception the task asked for was looked for and is not taken. The candidate was letting a passed lesson check stand in for the first credited attempt that R32's `example` skip condition requires. It fails on the evidence: 01 counts a retrieval only after at least one calendar day (the Roediger and Karpicke five-minute null [verified]), a check answered seconds after reading the same worked example is support-present and massed, and R7 and R32 name the counter pair and `serve_stage` as the only writers of `fading_stage`. The 02 tunables table does not gain a row for it; it is Q1 in the register as an A/B candidate only, and any arm would still have to write the skip through a credited attempt.

The invariant that bounds the layer, stated once so every test below is an instance of it:

> **L0.** For every user and every sequence of lesson events, refresher events and lesson check answers, the `skills_state`, `attempts`, `diagnoses`, `pending_probes`, `judgments`, `gradings` and `experiment_assignments` tables are unchanged before and after, and the only tables a lesson event may write are `lesson_state`, `lesson_events`, `lesson_check_responses` and `audit_log`.

The two `attempts` columns this design adds, `preceded_by_lesson_id` and `preceded_by_lesson_version`, are written by session assembly when the item is served, not by a lesson event, and are read by analysis only. The `lesson_first_contact` assignment row is written by `assemble_session` at the moment a concept is first targeted, for the same reason.

## Pacing to the exam date [inferred]

Nothing here is shown to the student and nothing sets a quota. It is the arithmetic that shows the lesson layer cannot be the binding constraint on covering every unit before the exam, with the denominators stated.

Dates, from `research/exam/exam-structure.md` [single-source] and the clock: 224 days from 2026-09-28 to 2027-05-10; 168 days to the desired-retention switch on 2027-03-15.

Sessions are counted as study days S, which the app does not set. Three values bracket it. The forecast per session is 01's 45-minute planning default, which is a forecast and never a target.

| S study days in 224 | 112 (one day in two) | 160 (five days in seven) | 224 (every day) |
|---|---|---|---|
| Concept lessons per session to serve all 170 first-contact lessons | 170 / 112 = 1.52 | 170 / 160 = 1.06 | 170 / 224 = 0.76 |
| Against `LESSONS_PER_SESSION_MAX` = 2 | fits | fits | fits |
| Reading minutes ceiling if every lesson were full band, 170 x 6 = 1,020 | 1,020 / (112 x 45) = 20.2 percent | 1,020 / (160 x 45) = 14.2 percent | 1,020 / (224 x 45) = 10.1 percent |
| Against `LESSON_SHARE_MAX` = 0.30 as a cycle share | under | under | under |
| Prerequisite lessons, 77 at most, only on a diagnosed gap, 77 x 3 minutes = 231 | 4.6 percent | 3.2 percent | 2.3 percent |
| Productive-failure openers, 5 targets at 10 to 15 minutes (01) | 50 to 75 minutes in all | same | same |

The per-session share cap is what ties the two constants together: two full lessons are 12 of a 45-minute forecast, 26.7 percent, and one refresher on top is 13.5 of 45, 30.0 percent, which is the cap. Three full lessons would be 40 percent and would break 01's 30 percent reading row, which is why the count cap is 2 and not 3.

What does bind. Mastery condition 5 needs a 7-day span between the first and last unaided success on a skill, and a child skill enters the fringe only once every `hard_prerequisite` parent is mastered, so a skill at hard depth d cannot be mastered before about 7 x (d + 1) days after its root is first credited. The deepest skills sit at depth 10, so about 77 days, inside 224. Items, not lessons, carry the load: the six conditions need 3 unaided successes per skill, one item credits every skill it loads (mean 4.55), so a lower bound on stage `unsupported` successes for 541 skills is 3 x 541 / 4.55 = 357, plus at least 2 successes at each of `example` and `completion` per skill group before `unsupported` (R7), at least 4 x 139 = 556 supported items, before any failure. At the 3-minute default forecast that is at least (357 + 556) x 3 = 2,739 minutes, 61 sessions of 45 minutes, against 112 to 224 available. The lesson layer adds at most 1,020 minutes to that, and its own cap keeps every session's reading under 30 percent.

The one pacing consequence the layer creates is the deferral rule in the engine section: a session in which more than two new concepts are first reached serves the third and later items without a lesson and defers the lesson to the next session. The number of deferrals per session is telemetry, and if it is often above 0 the fix is in the constants, not in a schedule.

## Engine and session integration [inferred]

### State: a gate in front of the ladder, not a fading stage

A fourth `fading_stage` value is rejected. R7 makes `consecutive_successes` and `consecutive_failures` the only writers of `fading_stage`, R32 makes `serve_stage` choose only the initial stage, and a `lesson` stage would need a writer that is neither. The lesson layer therefore keeps its state in `lesson_state`, one row per user and lesson, read as a gate.

`lesson_state` columns: `user_id`, `lesson_id` (primary key with `user_id`), `status` in `unseen`, `deferred`, `served`, `read`, `skipped`, `bypassed_by_placement`; `version_seen`; `band_served`; `first_served_at`; `read_at`; `read_source` in `session`, `library`; `refresher_due_reason`; `refresher_served_at`; `refresher_count`; `created_at`; `updated_at`. A missing row means `unseen`, so the seed writes none.

### First-contact target

`app/lessons/gate.py`:

```
def lesson_target(item, states, graph, lesson_states, lessons):
   # Every loaded skill, in the archetype's skills order, primary first (R25).
   for skill_id in item["skills"]:
      concept_id = graph.skills[skill_id]["concept"]
      state = states[skill_id]
      lesson_state = lesson_states.get(concept_id)

      is_unobserved = state.credited_observation_count == 0
      is_unseen = lesson_state is None or lesson_state.status in ("unseen", "deferred")
      is_servable = lessons.servable(concept_id)
      needs_lesson = is_unobserved and is_unseen and is_servable

      if needs_lesson:
         return concept_id

   return None


def lesson_band(archetype, states, graph, retrievability):
   knowledge = p_knowledge(archetype, states, graph.hard_parents, retrievability)

   if knowledge < constants.STAGE_LOW:
      return "low"

   if knowledge > constants.STAGE_HIGH:
      return "none"

   return "mid"
```

A lesson is inserted immediately before the item when all of these hold:

- (a) `lesson_target` is not `None`
- (b) `lesson_band` is not `none`, the expertise-reversal guard
- (c) the session's lesson count is below `LESSONS_PER_SESSION_MAX`
- (d) the session's reading share after insertion is at most `LESSON_SHARE_MAX`
- (e) the session mode is learning and the block is block 2

When (a) and (b) hold and (c) or (d) fails, the item is served without a lesson, the item carries `lesson_link`, and `lesson_state.status` becomes `deferred`, so the same concept's next item, in this session or the next, gets the lesson first. This departs from the draft, which ended block 2 early once the budget was spent. Ending early spends the block's remaining minutes on nothing, and block 2 is the only place new mastery is created (01 Time budget), while serving the item unlessoned is today's behaviour. The deferral count is telemetry; Q3 in the register keeps the alternative.

Condition (b) reads `serve_stage`'s bands but not `serve_stage` itself: a secondary-skill concept can be unseen while the item's primary skill is at `completion`, and the band is then `mid`, which serves the brief form.

### Session assembly

`app/session/build.py` changes:

- `Session` gains `lessons: list`, `lesson_minutes: float`, `lesson_deferrals: list`. `block2` entries gain a `kind` field, `"item"` on the existing dicts and `"lesson"` on new entries `{"kind": "lesson", "lesson_id", "version", "band", "reason", "before_item_id", "plan": LessonPlan.as_dict()}`. Block 1 and block 3 entries are unchanged, and block 4 stays a list of item ids plus, when present, `{"kind": "read_again", "lesson_id", "version"}` entries.
- `SERVING_BLOCKS`, `served_positions`, `consumed_positions`, `resolve_slot` and `next_item` in `app/session/service.py` learn the kind. A lesson slot is consumed by a `completed` or `skipped` event on `POST /sessions/{id}/lessons/{lesson_id}/events`, never by an attempt.
- Inside the block 2 loop, after `next_item_learning` returns `selection.item` and before `fits`, `lesson_target` and `lesson_band` run; when insertion holds, `serve_lesson(session.block2, entry)` appends the lesson entry, adds its minutes to `assembled` against `BLOCK2_MAX_MINUTES` (25), and the item follows. When a `LSN-PRQ` lesson is also due for a flipped parent, it is appended before the concept lesson. `lesson_target`'s concept is written to `lesson_state` as `served` and the item dict gains `preceded_by_lesson_id` and `preceded_by_lesson_version`.
- `interleaving_satisfied`, `unexplained_violations` and `window_filter` skip lesson entries, so lessons are transparent to invariant 12's windows; `unit_counts` does not count them; `forecast_total` includes them.
- Forecast: a lesson's minutes are the authored `read_minutes[band]` until the user has `LESSON_FORECAST_MIN_COMPLETIONS` (5) completed lessons, then the running median of `read_ms / read_minutes[band]` over completed lessons times the authored value, mirroring `forecast_minutes` and `FORECAST_MIN_ATTEMPTS`.
- Refreshers: `refresher_targets(states, attempts_history, lesson_states, today)` computes T1 to T4 before block 1, and `serve_refresher` inserts at most `REFRESHERS_PER_SESSION_MAX` entries `{"kind": "refresher", ...}` before the matching item in block 1 or block 2, under the share cap; a block 3 match writes a `read_again` entry to block 4 instead.
- The productive-failure order is enforced where the opener is wired: opener entry, then lesson entry, then the item (02 Session assembly, amended).

New constants in `app/engine/constants.py`, every one [inferred] and in the register: `LESSONS_PER_SESSION_MAX = 2`, `LESSON_READ_MINUTES_MAX = 6.0`, `LESSON_BRIEF_MINUTES_MAX = 3.0`, `LESSON_SHARE_MAX = 0.30`, `LESSON_FORECAST_MIN_COMPLETIONS = 5`, `REFRESHER_MINUTES_MAX = 1.5`, `REFRESHERS_PER_SESSION_MAX = 2`, `REFRESHER_MIN_GAP_DAYS = 3`, `LESSON_WORDS_FULL_MAX = 900`, `LESSON_WORDS_BRIEF_MAX = 450`, `LESSON_COMMON_ERRORS_MAX = 4`, `LESSON_CHECKS_MIN = 2`, `LESSON_CHECKS_MAX = 3`. `LESSON_SHARE_MAX` makes 01's "at most 30 percent reading" row operational as lesson plus refresher minutes over the assembled forecast; feedback-reading minutes are not forecast anywhere in the code today and the row in 01 is amended to say what the share counts.

### Cold start, placement and skipped units

- The diagnostic serves no lessons, because it measures. `diagnostic_session.advance` is untouched.
- `engine/diagnostic.place` marks skills mastered. `app/lessons/gate.py: bypass_placed_concepts(states, graph)` sets `bypassed_by_placement` on every concept all of whose skills are mastered after placement. Those lessons stay readable in the library and eligible for refreshers.
- `mark_unit_skipped` and `answer_skipped_units` answer `NOT_LEARNED_ANSWER`, which leaves those skills unmastered and unobserved. Their concepts stay `unseen` and get first-contact lessons as the fringe reaches them. This is the whole path for a student who has learned no units.
- The diagnostic result screen gains one line: "Ideas in the units you skipped start with a short lesson."
- The re-diagnostic after `GAP_DAYS_DIAGNOSTIC` changes no lesson state.

### Diagnosis links to lesson sections

The link is deterministic and needs no model call. When a graded attempt's option `error_path` (MCQ) or `DiagnosticianOutput.observed_errors[]` names BC-ERR-x and the item's concept lesson holds `#err-BC-ERR-x`, the feedback payload of `GET /sessions/{id}/attempts/{attempt_id}/feedback` gains `lesson_link: {lesson_id, version, anchor}`. `ElaboratedPanel.tsx` renders it as "Read the part on this error" after 03's three parts and replaces none of them. A misconception reaches the link only through its error. A top-two tie that writes a probe shows no link.

## UI [inferred]

The routes follow 08. The information architecture stays six screens plus settings: the library lives under progress and the reader is a session item state.

Session, lesson state, a new item state `lesson` beside `example`, `completion` and `unsupported` in `SessionScreen.tsx`, switched on `entry.kind`:

- Top bar: "Before the first problem on {concept.name}. About {plan.minutes} minutes." A refresher reads "Before the next problem on {concept.name}. About a minute."
- One section per screen with "Next part" and a persistent "Skip to the problem". Skipping is always allowed, logged with the section index, and has no engine effect.
- Paging keeps a defined end (08 bans infinite scroll).
- Worked steps reuse `StepMarks.tsx` with each `why` line beside its step (01 split-attention rule), and the `comparison` callout after an opener.
- Checks reuse `Item.tsx`'s MathLive field and `McqControl`. Feedback names the error block and links it, with no praise copy and no score.
- The last screen says "The first problem is next. It shows a full worked solution you complete." There is no completion badge.

Reader components in `app/web/src/lessons/`: `LessonReader.tsx`, `LessonSection.tsx`, `LessonCheck.tsx`, `LessonLink.tsx`, `RefresherPanel.tsx`. Mathematics renders through `math/MathText.tsx` and `MathValue.tsx`, figures through `figures/`, and `screenReaderMath` applies.

Library: progress gains a Lessons tab listing units from `data/curriculum.json` in order, then concepts, each row showing name and state ("Not read", "Read on {date}", "Placed, not needed", "Coming up"). A mastery map node links to its concept's lesson. There is no percent bar and no count of lessons read (08 bans percent-complete bars; reading is not mastery). The copy reads "Reading a lesson does not count toward mastery." Any signed-off lesson can be read from the library regardless of gating; a library read writes `read` with `read_source = library` and no engine state, so the lesson is not inserted again.

`App.tsx` gains `"lesson"` in `Destination` for the library reader, reached from progress only. It is not on the top bar and home keeps one primary action. Home's minute forecast includes lesson minutes. The operator's review screen (`app/web/src/review/`) gains kinds `lesson_stale` and `lesson_resolve_disagreement`.

Interface writing, added to 08's table:

| Context | Good | Bad |
|---|---|---|
| Lesson top bar | "Before the first problem on the product rule. About 4 minutes." | "Lesson 12 of 170: unlock the product rule!" |
| Check answered wrong | "Not yet. The two derivatives were multiplied. The part above on that error shows the right step beside it." | "Oops, read the lesson again more carefully" |
| Library row | "Read on 3 October" | "Completed, 100 percent" |

## API, migrations, telemetry [inferred]

### Endpoints

New file `app/api/routes/lessons.py`, registered in `app/api/app.py`.

| Endpoint | Purpose |
|---|---|
| `GET /lessons?unit=BC-UNIT-06` | library listing with per-user `lesson_state` |
| `GET /lessons/{lesson_id}` | current signed-off body; `?version=` returns the version seen |
| `GET /lessons/{lesson_id}/plan?band=low` | the plan for a band, so the library reader and the session reader render one shape |
| `POST /sessions/{session_id}/lessons/{lesson_id}/events` | body `{event, section_id?, elapsed_ms}`; events `opened`, `section_viewed`, `completed`, `skipped`; `completed` or `skipped` consumes the queue slot |
| `POST /lessons/{lesson_id}/events` | library reads |
| `POST /lessons/{lesson_id}/checks/{check_id}/answers` | graded by `app/items/grade.py`; returns `{correct, error_id?, anchor?}`; never touches `attempts` |

Changed: `GET /sessions/{id}/next` may return `{"kind": "lesson", ...}` or `{"kind": "refresher", ...}`; the feedback route gains `lesson_link`; `GET /review-queue` and `POST /review-queue/{row_id}/resolve` accept the two lesson kinds; `GET /me/export` includes the five lesson tables.

### Migrations

Additive, through `Base.metadata.create_all` for new tables and `apply_additive_migrations` in `app/db/migrate.py` for new columns, which must be nullable or carry a `server_default` and may not be unique or indexed (`SchemaDriftError` otherwise).

- `lessons`: `id`, `version` (primary key with `id`), `kind` in `con`, `prq`; `target_id`; `snapshot_id`; `body` JSON; `read_minutes_full`, `read_minutes_brief`; `status`; `provenance` JSON; `source_digest`; `created_at`; `updated_at`.
- `lesson_verifications`: shaped like `item_verifications`, with `lesson_id`, `version`, `section_id`, `check_type`, `outcome`, `detail`.
- `lesson_state`: as specified above.
- `lesson_events`: `id`, `user_id`, nullable `session_id`, `lesson_id`, `version`, `kind` in `lesson`, `refresher`, `library`; `event`; `section_id`; `reason`; `band`; `elapsed_ms`; `created_at`.
- `lesson_check_responses`: `id`, `user_id`, `lesson_id`, `version`, `check_id`, `response`, `correct`, `error_id`, `elapsed_ms`, `created_at`.
- `attempts`: nullable `preceded_by_lesson_id` and `preceded_by_lesson_version`.
- `experiments`: no schema change; `app/experiments/switches.py` `DEFINITIONS` gains `lesson_first_contact` with `unit="concept"`, `control_arm="lesson_before_first_item"`, `treatment_arm="example_first"`.

`app/session/purge.py`, the export route and `app/session/seed.py` cover the owned tables. `app/audit/vocabulary.py` gains `lesson_gap_fail_open`, `lesson_stale`, `lesson_signed_off`.

### Telemetry

Logged per lesson: served with reason and band, opened, per-section dwell, skipped with section index, completed, check answer with error, refresher served with trigger, library opened, deferred. Derived for 10's dashboard: skip rate by band; read time against forecast; check accuracy by check position; attempts from lesson to first credited success at `unsupported`; stage `example` first-attempt accuracy split by whether a lesson preceded; reading share per session; deferrals per session; refreshers per trigger. The two learning-outcome metrics the layer is judged on join 10's list: minutes to mastery per skill, defined as the sum of `attempts.elapsed_ms` on items loading the skill plus the lesson and refresher `elapsed_ms` on its concept, from first exposure to `mastered_at`, reported by unit with its denominator; and delayed accuracy at matched minutes, 10's retention at 7 and 30 days segmented by whether a lesson preceded first contact.

## Quality and evaluation [inferred]

### Invariants

L0 is stated in the evidence section. Numbers are provisional and 02 assigns the final ones when they join its list.

- L1. No lesson event, refresher event or check answer changes any `skills_state` field. Test: snapshot before and after 1,000 random event sequences over the real 541-skill graph.
- L2. Lesson check answers never appear in `attempts`, `load_attempts_history`, the diagnostician's recurrence count, `RETRIEVAL_ENTRY` counts, forecasts or FSRS.
- L3. No first-contact lesson and no refresher is inserted in diagnostic mode, rehearsal, unit checks, drills, mocks, checkpoints or block 3; refreshers may precede block 1 items.
- L4. A first-contact lesson is inserted only when `lesson_target` is non-null and `lesson_band` is not `none` for the item it precedes.
- L5. At most one first-contact insertion per user and lesson; at most `LESSONS_PER_SESSION_MAX` lessons and `REFRESHERS_PER_SESSION_MAX` refreshers per session; at most one refresher per concept per `REFRESHER_MIN_GAP_DAYS`; lesson plus refresher minutes at most `LESSON_SHARE_MAX` of the assembled forecast.
- L6. For a productive-failure target with `concept_opener_done == 0`, the opener precedes the lesson and the lesson precedes the item, once the opener is wired.
- L7. Invariants 3, 12 and 13 hold unchanged with lessons present; lessons are excluded from the windows and from the translation-floor denominator.
- L8. A served lesson is `signed_off`, not `stale`, and every BC-* id in it is active in the serving snapshot.
- L9. Every worked step passes `verify.equivalence`, and every example and check answer has an agreeing blind re-solve.
- L10. No lesson worked-example or check parameter draw equals the `parameter_draw` of a published item on the same archetype.
- L11. A skipped lesson and a read lesson lead to identical engine state.
- L12. A concept without a servable lesson falls back to example-first and writes `lesson_gap_fail_open`, and never blocks the fringe. This is the opposite of the items' fail-closed rule (R18), because a missing lesson removes support, not a measurement.
- L13. `plan_lesson` is deterministic: the same lesson, band, reason and ids give the same plan, and a plan never exceeds its band's minute and word caps.
- L14. A `LSN-PRQ` lesson is inserted only after a diagnosed gap has flipped that BC-PRQ to unmastered.
- L15. Every `what_a_reader_scores` line equals `reader_checks` recomputed from the current snapshot's BC-PT records, and no lesson on an archetype without `point_types` carries the section.
- L16. A decision lesson is inserted only after at least one skill of its set has a credited success at stage `unsupported`, at most once per set as a first insertion, and afterwards only on T5.
- L17. `fluent` is never read by `outer_fringe`, `candidates`, `serve_stage`, any `next_item_*` function or `evaluate_mastery`, and no `skills_state` column stores it. Test: grep-free, a property test that toggles the fluency input and asserts identical selection traces and states.
- L18. `confusable_sets` is deterministic over a snapshot, every set lies within one unit, and every set member is an active BC-SKL.

### Tests

- `tests/lessons/test_check_lessons.py`: every lint, each with a fixture shown red before it is shown green, per the testing discipline.
- `tests/lessons/test_plan.py`: L13 over every signed-off lesson and every band, reason and id combination in a fixture.
- A contract test of every `content/lessons/*.json` against the real `data/`.
- `tests/session/test_lesson_gate.py`: `lesson_target` over the 59 never-primary concepts, the deferral rule, the share cap and the `LSN-PRQ` ordering.
- Integration: a no-units student's first session shows a lesson and then an example item for two concepts, the third new concept's item carries `lesson_link` and a `deferred` row, block 3 has no lesson, and the next session opens block 2 with the deferred lesson.
- Property tests L0 to L14 at 1,000 cases in the standing gate.
- Vitest: keyboard-only reader, reduced motion, the skip path, the check feedback link, the refresher panel, the library tab.

### Gates

- Lesson audit: every signed-off lesson carries a block-level verdict file with zero unsourced claims and zero mathematical errors, reported as a rate with its denominator in the style of 10's key error rate gate, and labelled as a model audit under the 2026-09-24 ruling.
- Worked-step verification at 100 percent, blind re-solve agreement at 100 percent on served lessons.
- Quote, style, prediction and cap lints at 0 failures.
- No gate, threshold, tolerance or invariant elsewhere in the plan is loosened by this layer, and the A/B may not change the mastery rule (10, Switch design).

### Offline simulation

`app/sim/learning.py` gains a `lesson_effect` field on `WorldRules` and two arms in `ARMS`: `lessons_on` and `lessons_off`. A synthetic student's per-skill learning rate is multiplied by `lesson_effect` on the first `LESSON_EFFECT_EXPOSURES` (2) exposures after a lesson on the skill's concept, and lesson minutes are charged from `read_minutes[band]`. The sweep runs `lesson_effect` in 1.0, 1.25, 1.5, plus a negative arm where lessons cost minutes and the multiplier is 1.0. Outcomes are 10's: true skills mastered per simulated minute, delayed mastery per item at day 30, under both forgetting curves, decided by the paired-mean rule ruled 2026-09-27.

The simulation cannot establish the effect, because `lesson_effect` is invented. It reports the break-even value, the smallest multiplier at which `lessons_on` matches `lessons_off` on true skills mastered per simulated minute. If break-even is above 1.5 the budget constants shrink before any student sees a lesson. `LESSON_EFFECT_EXPOSURES` and the sweep values are [inferred] and in the register.

### Within-student A/B

`lesson_first_contact`, unit concept, seeded and stratified by unit and by the cold-start `p_A` band, through `app/experiments/switches.py`. Arms: the lesson before the first item, and today's example-first behaviour with the lesson readable in the library. The five productive-failure targets are excluded. Outcomes: attempts to reach `unsupported`; stage `example` and `completion` first-attempt accuracy; delayed accuracy at the 2 to 4 week checkpoint; un-mastery rate within 30 days; minutes to mastery per skill. Power is marginal, as 10 says of concept-level units: 170 concepts exist, only those the fringe reaches accrue data, and 10's Newcombe interval needs 30 outcomes per arm (ledger, stage 8). Per 10, the treatment changes no mastery rule, gate or threshold.

## The "better than a school class" hypothesis [single-source]

It is a hypothesis and this document does not claim it. What can be stated is the metric, the published evidence for each mechanism the layer uses, and how the app would test it.

**Metric.** Minutes to mastery per skill, as defined in the telemetry section, and delayed accuracy at matched minutes, as 10's retention at 7 and 30 days and the six-week checkpoint per-question means against the published 2023 to 2025 means. A school class has no per-skill mastery record, so the comparison a single student can make is against the published controls of the studies below, and it is reported as descriptive, never as an effect size (10, A/B readiness).

**Evidence per mechanism, as recorded in 01 with 01's tags and URLs.** No number below comes from memory; each is 01's line restated.

| Mechanism the layer uses | Published evidence | Effect | Tag | URL |
|---|---|---|---|---|
| Mastery learning with tutoring, the frame the whole app inherits | Bloom 1984 | about 2 SD above the conventional class, an upper bound from small studies with local measures | [verified] | https://journals.sagepub.com/doi/10.3102/0013189X013006004 |
| Same | Kulik, Kulik and Bangert-Drowns 1990 | about d = 0.61 weaker students, 0.4 stronger | [single-source] | https://journals.sagepub.com/doi/10.3102/00346543060002265 |
| Same, on intelligent tutors | Kulik and Fletcher 2016 | median 0.66 SD, much smaller on standardized tests | [verified] | https://journals.sagepub.com/doi/abs/10.3102/0034654315581420 |
| Retrieval over restudy, why checks and refreshers stay uncredited and short | Adesope, Trevisan and Sundararajan 2017 | g = 0.51 against restudy | [verified] | https://journals.sagepub.com/doi/abs/10.3102/0034654316689306 |
| Same | Rowland 2014 | g = 0.50 | [verified] | https://pubmed.ncbi.nlm.nih.gov/25150680/ |
| Same, the massed null behind L0 | Roediger and Karpicke 2006 | 61 against 40 percent at one week, none at five minutes | [verified] | https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x |
| Spacing, why refreshers fire on state and not on a timer | Cepeda et al 2008 | optimal gap 10 to 20 percent of the interval | [verified] | https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf |
| Same | Rohrer and Taylor 2006 | 74 against 49 percent at four weeks | [single-source] | https://onlinelibrary.wiley.com/doi/10.1002/acp.1266 |
| Worked examples faded on a running estimate, the band rule | Salden, Aleven, Schwonke and Renkl | adaptive fading beat fixed fading and pure solving | [single-source] | http://www.cee.uma.pt/ron/Salden%20et%20al.%20-%20The%20Expertise%20Reversal%20Effect%20and%20Worked%20Examples.pdf |
| Backward fading, the check 1 form | Renkl, Atkinson, Maier and Staley 2002 | beat an abrupt switch | [single-source] | https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6 |
| Expertise reversal, the none band and the skip | Kalyuga, Ayres, Chandler and Sweller 2003 | support becomes redundant then harmful | [single-source] | https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_4 |
| Worked-example effect size, the caution | 2023 review | about f = 0.25 | [single-source] | https://www.tandfonline.com/doi/full/10.1080/01443410.2023.2273762 |
| Interleaving, untouched by lessons | Rohrer, Dedrick, Hartwig and Cheung 2020 | d = 0.83 | [verified] | http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf |
| Same, the boundary | Brunmair and Richter 2019 | g = 0.42, near zero for expository text | [verified] | https://pubmed.ncbi.nlm.nih.gov/31556629/ |
| Self-explanation, one prompt kept on the graded item | Bisra et al 2018 | g = 0.55 | [verified] | https://link.springer.com/article/10.1007/s10648-018-9434-x |
| Productive-failure opener before the lesson | Sinha and Kapur 2021 | g = 0.36, CI [0.20, 0.51] | [verified] | https://journals.sagepub.com/doi/10.3102/00346543211019105 |
| Labels inside figures, the why line beside its step | Schroeder and Cenkci 2018 | g = 0.63 | [verified] | https://link.springer.com/article/10.1007/s10648-018-9435-9 |
| No chat box beside a lesson | Bastani et al | plain chat 17 percent below control on the unassisted exam | [single-source] | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486 |

What the ledgers do not hold: no study in any ledger compares a short pre-instruction lesson against example-first entry inside a mastery tutor, so the lesson layer's own contribution carries no effect size and is [uncertain]. Brunmair and Richter's near-zero result for expository text is the closest warning, and it is the reason the lesson is short, band-limited and followed within the same block by graded practice.

**How the app tests it.** The A/B above on minutes to mastery and delayed accuracy; the simulation's break-even; 10's six-week checkpoint against published means, which is the only measurement with authority to contradict the internal numbers; and the Kulik and Fletcher shrinkage rule, that internal mastery climbing while the checkpoint stays flat triggers a review of thresholds, not a claim.

## Phased delivery [inferred]

A parallel track that enters after P1's gates read green, as P4 did, because P2's entry criterion is P1 merged with all gates green and nothing here may loosen that. The ledger reads gates 17, 29 and 30 as satisfied by Claude sign-off on 2026-09-24, so the track can start.

| Slice | Entry | Scope | Exit | Offline work |
|---|---|---|---|---|
| L0 Spec and checker | this document accepted; Q1 to Q4 ruled | `schemas/lesson.schema.json`; `tools/check_lessons.py` with every lint; `prompts/generator/lesson_v1.md`; `app/lessons/plan.py` and its tests; `lessons.*` lines in `tools/cost_model.py`; one hand-authored lesson, `LSN-CON-02013` (the product rule, primary concept of BC-QA-02008) | checker red on each shown fixture and green on the hand-authored lesson; L13 green; `--check` passes on this file | author one lesson |
| L1 Storage, API and reader | L0 | the five tables and the two `attempts` columns; `app/lessons/ingest.py`; `GET /lessons*`; `LessonReader` and the library tab; lessons for the 19 concepts the 13 P1 archetypes load, authored, re-solved and signed off | L8 to L10 green; audit of all 19 at 0 errors with its denominator; vitest reader tests green | 19 authoring, re-solve and sign-off sessions |
| L2 Engine insertion | L1 | `lesson_target`, `lesson_band`, block 2 insertion, deferral, constants, events, telemetry, `lesson_first_contact` definition, L0 to L7 and L11 to L13 | standing gate plus L0 to L14 at 1,000 cases; the no-units session test; deferral telemetry rendering | confirm constants |
| L3 Re-teaching and diagnosis links | L2 | refreshers on T1 to T4, `lesson_link` in feedback, `read_again` in block 4, `LSN-PRQ` for flipped prerequisites, L14 | tests per trigger; no link on a probe-tied diagnosis; T4 shown on a synthetic student stuck at example | author `LSN-PRQ` lessons on demand |
| L4 Full coverage | L2; may run beside anything | the remaining lessons to 169 servable plus BC-CON-06014 for the library, then `LSN-PRQ` for every BC-PRQ | 100 percent verification; audit of every lesson at 0 errors | about 150 authoring, re-solve and sign-off sessions, paced under `docs/operator/offline-authoring.md` |
| L5 Evaluation | P7 harness (built, waiting on real data) | `lessons_on` and `lessons_off` arms, `lesson_effect` sweep, `lesson_first_contact` in `randomised`, the two metrics on the dashboard | break-even reported under both curves; A/B running; metrics rendering with denominators | switch the flag |
| L6 Methods | L2; L4 for the strategy blocks on every concept | `strategy`, `cue` and `what_a_reader_scores` on every signed-off lesson; `app/lessons/confusable.py`; decision lessons for the antiderivative-technique and series-test sets first, then every derived set; T5; `app/progress/fluency.py` and the map display; L15 to L18 | checker green on the new rules; the published set count; L15 to L18 at 1,000 cases; method-selection against execution accuracy rendering per set | author and sign off the decision lessons |

## Plan amendments by file and section [inferred]

Every departure from an existing plan decision, listed so none is silent. The amendment is proposed, not made; this document edits no other file.

| File | Section | Amendment |
|---|---|---|
| 01-learning-model.md | Practice testing over restudy, The mechanic | Add: a first-contact lesson and a trigger-fired refresher precede the ladder and are not restudy; they are uncredited and capped by `LESSON_SHARE_MAX` |
| 01-learning-model.md | Practice testing over restudy, Parameters | The "at most 30 percent reading" row states what the share counts: lesson and refresher minutes over the assembled forecast; feedback-reading minutes are not forecast |
| 01-learning-model.md | Productive-failure openers, The mechanic | The order is opener, lesson, first item; the lesson's first worked example carries the comparison step |
| 01-learning-model.md | Time budget | A line for lessons and refreshers inside the fringe-learning block's 25 minutes, and the 224-day arithmetic pointer to this file |
| 01-learning-model.md | Interleaving, The mechanic | The method-selection drill is sourced to BC-QA-06016 and BC-QA-10001 and delivered as the decision lesson of this file, with the derived confusable sets |
| 05-assessment-modes.md | Pacing metrics | `fluent` as a derived display value from the part budgets, never a mastery input |
| 08-design-brief.md | Progress wireframe | The map legend gains "fluent" beside "mastered and fresh", with the per-item time shown only on the node detail |
| 10-quality-and-evaluation.md | Method-selection versus execution accuracy | Reported per confusable set; T5 reads it; the decision lesson is the treatment whose effect the metric shows |
| 02-adaptive-engine.md | Session assembly | Block 2 entries carry `kind`; the lesson gate, band and deferral rule; the opener, lesson, item order; refresher entries in blocks 1 and 2 and `read_again` in block 4 |
| 02-adaptive-engine.md | Decay | Name T2 as the consumer of the `R_k < 0.5` support cap, and record that the cap is not yet read by code |
| 02-adaptive-engine.md | Unit-testable invariants | Append L0 to L14 as invariants 24 to 38 |
| 02-adaptive-engine.md | Tunables | The thirteen lesson constants and `LESSON_EFFECT_EXPOSURES` |
| 03-diagnosis-and-feedback.md | Feedback policy, Content | A fourth, optional element `lesson_link` after the three parts, absent on a probe-tied diagnosis |
| 03-diagnosis-and-feedback.md | When the diagnostician is called at all | Lesson check errors do not count as an occurrence of a BC-ERR path |
| 04-item-generation.md | Rejection rules | Rule 16: an item whose `parameter_draw` equals a signed-off lesson's worked-example or check draw on the same archetype is not published |
| 06-architecture.md | Data model | The five lesson tables, the two `attempts` columns, the `lesson_first_contact` definition |
| 06-architecture.md | API surface | The six lesson endpoints and the changed session and review routes |
| 08-design-brief.md | Information architecture | Session item state `lesson`, block 4 `read_again`, the progress Lessons tab, `Destination` `lesson` |
| 08-design-brief.md | Interface writing | The three copy rows above |
| 09-security-and-privacy.md | Audit log; Retention | Three audit actions; the five tables under export and purge |
| 10-quality-and-evaluation.md | Learning-outcome metrics | Minutes to mastery per skill; delayed accuracy at matched minutes |
| 10-quality-and-evaluation.md | Offline simulation | The `lessons_on` and `lessons_off` arm pair and the break-even report |
| 10-quality-and-evaluation.md | A/B readiness | The `lesson_first_contact` row, powered marginal, concept unit |
| 10-quality-and-evaluation.md | Release gates | L0 to L14 in the standing gate once L2 merges |
| 11-phased-delivery.md | Dependency order; What each phase is not allowed to defer | The L track beside P4; L2 may not defer L0, L5 may not defer the break-even report |
| 12-open-questions.md | Tunables register | The rows in the register below |
| 13-ai-engineering.md | Prompt templates, Evals | `lesson_v1.md` versioned with golden tests; the sign-off audit as an offline eval |
| 14-token-economy.md | Offline work; The $100 tier | The three `lessons.*` lines as offline lines at $0.00 API; the guard refusal |
| docs/operator/offline-authoring.md | The workflow shape | The lesson pass: author, blind re-solve, blind sign-off, `tools/check_lessons.py` clean |
| BUILD-LEDGER.md | Decisions | The rulings on Q1 to Q4 when made |

Departures from the 2026-09-28 draft of this file, for the record: the first-contact target reads every loaded skill, not the primary only; the budget defers instead of ending block 2; publication is model sign-off under the 2026-09-24 ruling, not operator provenance, and `GROWTH_SERVE_DRAFT_LESSONS` is dropped; the missing-lesson audit action is `lesson_gap_fail_open`; T4 is added; L0, L13 and L14 are added; the draft's conflict 10 is corrected, since research/units quotes EK text verbatim in Official mapping and paraphrases in Required mathematical knowledge.

## Open-questions register [uncertain]

Every parameter without a source, and every decision the operator or a measurement must make. Values are working values, not findings.

| Id | Question or parameter | Current | Tag | What would settle it |
|---|---|---|---|---|
| Q1 | May a passed lesson check let stage `example` be skipped? | no; L0 holds | [uncertain] | an A/B whose arm writes the skip only through a credited attempt, on delayed accuracy |
| Q2 | Does the mid band get the brief form or nothing? | brief form | [inferred] | stage `completion` first-attempt accuracy with and without the brief form, in the A/B |
| Q3 | Defer the lesson past the budget, or end block 2 early? | defer | [inferred] | deferrals per session and stage `example` accuracy on deferred items |
| Q4 | Full lesson or refresher-sized form for the 25 one-skill concepts? | full, band-planned | [uncertain] | read time and skip rate on one-skill concepts against the rest |
| Q5 | What items serve a BC-PRQ at the head of the queue? 02 does not say | `LSN-PRQ` then the dependent's item | [uncertain] | a ruling in 02 |
| Q6 | Does College Board regard an EK paraphrase in a product as protected? | paraphrase, 25-word quotes | [uncertain] | counsel, as 04 says of structural descriptions |
| Q7 | Sign-off throughput: about 247 lessons at one offline session each | paced under offline-authoring.md | [inferred] | the measured sessions per lesson on L1's 19 |
| Q8 | Worked examples from the 56 archetypes without `point_types` carry no BC-PT tag | allowed, rule 9 | [inferred] | nothing; a library gap |
| Q9 | `DECAYED_SUPPORT_CAP_RETRIEVABILITY` is read by no code | T2 waits on it | [inferred] | wiring the cap in `serve_stage` per 02 Decay |
| Q10 | `reconcile_skills_state` is called by no application code | `reconcile_lessons` waits on it | [inferred] | wiring the snapshot reload path per 06 |
| Q11 | The productive-failure opener is not wired | step 1 absent | [inferred] | R35's generator-backed opener |
| Q12 | `LESSONS_PER_SESSION_MAX` 2, `LESSON_READ_MINUTES_MAX` 6, `LESSON_BRIEF_MINUTES_MAX` 3, `LESSON_SHARE_MAX` 0.30 | as stated | [inferred] | reading share, deferrals and minutes to mastery over the first 8 weeks |
| Q13 | `REFRESHER_MINUTES_MAX` 1.5, `REFRESHERS_PER_SESSION_MAX` 2, `REFRESHER_MIN_GAP_DAYS` 3 | as stated | [inferred] | un-mastery re-entry accuracy with and without a refresher |
| Q14 | `LESSON_WORDS_FULL_MAX` 900, `LESSON_WORDS_BRIEF_MAX` 450, the 150 words per minute behind them | as stated | [inferred] | measured `read_ms` per word after five completed lessons |
| Q15 | `LESSON_COMMON_ERRORS_MAX` 4, `LESSON_CHECKS_MIN` 2, `LESSON_CHECKS_MAX` 3, `LESSON_FORECAST_MIN_COMPLETIONS` 5 | as stated | [inferred] | skip rate by section; forecast error after five completions |
| Q16 | `LESSON_EFFECT_EXPOSURES` 2 and the sweep 1.0, 1.25, 1.5 | as stated | [inferred] | the break-even report; a real effect is never measurable in simulation |
| Q17 | Authoring attempts 1.5 and body multiplier 2.0 in the cost lines | as stated | [inferred] | the first authoring pass's measured attempts and body tokens |
| Q18 | The lesson layer's own effect size | none in any ledger | [uncertain] | the `lesson_first_contact` A/B on minutes to mastery and delayed accuracy |
| Q19 | Whether the 3 references that make concept `skills` lists sum to 544 (BC-CON-06001, BC-CON-06007) are library errors | lessons follow the skill's `concept` back-reference | [uncertain] | a library staging fix through `tools/merge_staging.py` |
| Q20 | `confusable_with` is empty on all 541 skills; sets are derived from `common_confusions` and BC-MIS rivals | derived by `confusable_sets` | [inferred] | a library pass filling `confusable_with`, after which the derivation becomes a check |
| Q21 | `asked_to_produce`, `common_givens` and `wrong_approaches` are absent on 78 of 139 active archetypes, so their strategy blocks rest on `typical_wording` | tagged inferred | [uncertain] | a library staging pass filling the three fields from the cached solution guidelines |
| Q22 | `DECISION_SET_MAX` 6, `METHOD_CONFUSION_WINDOW` 6, `METHOD_CONFUSION_FLOOR` 0.5 | as stated | [inferred] | method-selection accuracy per set over the first 8 weeks, and the T5 fire rate |
| Q23 | `FLUENCY_MIN_ATTEMPTS` 5 and the part-budget mapping for free-response shapes through `scoring_pattern` | as stated | [inferred] | the operator's own latency distributions on drills (05) against the map's fluent share |
| Q24 | `STRATEGY_WORDS_MAX` 80, `CUE_WORDS_MAX` 20 | as stated | [inferred] | skip rate on strategy blocks and read time per word |
| Q25 | When a decision lesson is first inserted: before the first block 3 item on a set's second member, or before the second member's first block 2 item | block 3, as stated | [uncertain] | method-selection accuracy on the set's first mixed set under each placement, in the A/B |

## Risks [uncertain]

- Wrong instruction at scale. A false rule in a lesson reaches every later item on the concept. Mitigated by CAS checks on every step, the blind re-solve, the block-level sign-off audit and the `signed_off` publication rule.
- Expertise reversal from inserting too often. Mitigated by the none band, the brief mid band, the always-available skip and the skip-rate telemetry by band.
- Reading displacing retrieval. Mitigated by the share cap, the deferral rule and the A/B on minutes to mastery.
- Staleness after library edits. Mitigated by `source_digest` and `stale`, once the reload path is wired (Q10).
- No measurable effect for one student. The simulation gives break-even only and the A/B is marginal; the checkpoint is the only external anchor.
- Sign-off is a model review. Under the 2026-09-24 ruling every audit rate is a model audit's rate and is labelled so; the residual is accepted and recorded, as it is for items.

## First three implementation tasks [inferred]

1. **L0, the checker and the plan function.** Write `schemas/lesson.schema.json`; write `tools/check_lessons.py` with every lint named in the sourcing section, each shown red on a fixture under `tests/fixtures/lessons/` before it is shown green; write `app/lessons/plan.py: plan_lesson` and `tests/lessons/test_plan.py` for L13; add the `lessons.author_*`, `lessons.verify_*` and `lessons.signoff_*` lines to `tools/cost_model.py` so `--check docs/plan/15-lessons.md` exits 0; hand-author `content/lessons/LSN-CON-02013.json` from `authoring_bundle("BC-CON-02013")` and run the checker on it.
2. **L1, storage and API.** Add the five tables to `app/db/models.py` and the two nullable `attempts` columns through `apply_additive_migrations`; write `app/lessons/ingest.py` on the `app/items/ingest.py` pattern with `lesson_verifications` rows; add `app/api/routes/lessons.py` with the six endpoints and register it in `app/api/app.py`; extend `app/session/purge.py`, the export route and `app/audit/vocabulary.py`; tests for L8 to L10 and for purge and export coverage.
3. **L1, the reader and the library tab.** Build `app/web/src/lessons/` on `StepMarks.tsx`, `Item.tsx`'s input controls and `math/MathText.tsx`; add the `lesson` item state to `SessionScreen.tsx` behind a `kind` switch that today only the library path reaches; add the Lessons tab to `ProgressRoute.tsx` and `"lesson"` to `Destination`; vitest for keyboard-only reading, reduced motion, the skip path and the check feedback link. The engine insertion (L2) starts only after these three land.
