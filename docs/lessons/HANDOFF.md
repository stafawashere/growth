---
title: Handoff, lesson framework redesign, session of 2026-09-29
research_date: 2026-09-29
status: handoff
purpose: The exact state of the lessons work at the end of the 2026-09-29 redesign session, what is verified, what is not done, and the ordered next actions, so a fresh session resumes without re-deriving anything.
---

# Handoff, lesson framework redesign

## The goal

The overnight brief (scratch/lesson-redesign-prompt.md, gitignored) asked for a research base on how the strong mathematics products teach, a clean-slate lesson design, a measured gap analysis of the served lessons, an additive framework amendment, every Unit 1 to 8 lesson redesigned and signed off, the Unit 9 and 10 designs brought to the new template, proof in the running app, and one ledger entry. Ground rules: project rules win (no praise, no study advice, no schedules, no prediction talk, no second-person belief statements, anchor quotes of 25 words at most, lessons count toward no mastery evidence); gates are strengthened, never loosened; lesson facts come from local sources only; code is written by Opus agents; every check is run by the orchestrator and quoted.

## Where the work stands

Branch `lessons/redesign`, 31 commits ahead of `main`, nothing pushed. The ledger entry "Lesson framework redesign, 2026-09-29" in BUILD-LEDGER.md is the full record: every check with its command and result, every decision, what is not done.

| Piece | State | Evidence |
|---|---|---|
| Research base | docs/pedagogy/: 12 product studies, learning-science.md, synthesis.md, rulings-for-operator.md, README.md | committed 84cbd30, fdba6be |
| Clean-slate design and gap analysis | docs/pedagogy/clean-slate-design.md, growth-gap-analysis.md (G1 to G16) | committed 8ca7535 |
| Framework v2 | schema, plan function, both checkers with six new lints and red fixtures, transcriber, prompts/generator/lesson_v2.md, prompts route, event modes, reader | committed 0b768d5, e1e55e8, ca73c13, e32380b; tests listed in the ledger table, all green |
| Units 1 to 8 | 127 designs redesigned, block-audited by Opus, fixed, transcribed, signed off, ingested | tools/check_lessons.py content/lessons: lessons read 127, clean 127; tools/lesson_sign_off.py refused 0 |
| Blind re-solve of changed stems and keys | deltas c, d, e: 80 problems, 0 disagreements, 8 judgments applied | docs/lessons/verification/answers/delta-2026-09-29-*.json |
| Units 9 and 10 | 43 designs at the v2 template, checked, marked checked in the manifest, not transcribed | tools/check_lesson_designs.py: unit-09 clean 18, unit-10 clean 27 |
| App proof | screenshots under var/lesson-redesign/ (gitignored), one lesson per unit, desktop and phone, dark and light | the ledger's walk paragraph |

## What is not done

1. Units 9 and 10 are not transcribed, audited or signed off. The brief stopped at the design check. To continue: `PYTHONPATH=. .venv/bin/python tools/lesson_transcribe_all.py docs/lessons/unit-09 docs/lessons/unit-10`, then tools/check_lessons.py on the records, the Opus block audit in batches of five (the audit and fixer briefs are described in the ledger), tools/lesson_resolve_compare.py, tools/lesson_sign_off.py, and a blind re-solve of every worked example and check (tools/lesson_design_resolve.py extract, a Sonnet solver, compare, judge).
2. The 77 prerequisite lessons and 9 decision lessons are untouched.
3. Nothing is merged to main. The branch carries no .claude/, mockup-redesign/ or CLAUDE.md changes.

## Rulings waiting on the operator

docs/pedagogy/rulings-for-operator.md: R1 to R12 (techniques rejected under the ground rules), C1 to C4 (caps the framework designed inside, with what a wider cap would restore), and the four earlier questions (archetype key invariants on lesson checks, a one-sided limit as a distractor, the exam-part budget, record ids in served text; the last is now settled by the served_text lint).

## Order to resume in

1. Read the ledger entry, then `git log main..lessons/redesign`.
2. Merge or rebase `lessons/redesign` onto main when the operator says so.
3. Units 9 and 10 through the pipeline in item 1 above, one unit per commit.
4. Prerequisite and decision lessons, per docs/lessons/BUILD-PLAN.md.

## How the pipeline runs (for a fresh session)

- Design check: `PYTHONPATH=. .venv/bin/python tools/check_lesson_designs.py docs/lessons/unit-NN` (directory runs also check manifest coverage).
- Transcribe: `tools/lesson_transcribe_all.py <dirs>` (pooled; loads the snapshot once).
- Record check: `tools/check_lessons.py content/lessons/<id>.json ...`; the whole directory once, in the background (about 90 s).
- Compare and sign off: `tools/lesson_resolve_compare.py <record> <design>` then `tools/lesson_sign_off.py <records>`; sign-off refuses any record whose verification file lacks an all-agree resolve block and an all-ok audit block.
- Blind re-solve: `tools/lesson_design_resolve.py extract <problems.json> <designs>`, a Sonnet solver that sees only that file, `compare <answers> <problems>`, `judge <judgments.json>` for statement answers.
- Rendering: from app/web, `LESSON_RECORD_DIR=../../content/lessons npx vitest run src/lessons/renderRecord.test.tsx`.
- Slow-command rules: never chain the checkers with the compares in one foreground call; one background process per unit; the full invariants gate as one process per property.
