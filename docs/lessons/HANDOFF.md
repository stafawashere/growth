---
title: Handoff, adaptive specialized lessons, session of 2026-09-29
research_date: 2026-09-29
status: handoff
purpose: The exact state of the lessons work at the end of the 2026-09-29 cloud session, the goal it was pursuing, and the ordered next actions, so any fresh session resumes without re-deriving anything.
---

# Handoff, adaptive specialized lessons

## The goal

Implement the Lessons feature of the Growth tutor end to end (docs/plan/15-lessons.md; docs/lessons/BUILD-PLAN.md slices L1 to L3 plus the delivery amendments A-D1 to A-D5), and turn every lesson that has a design under docs/lessons/ into an ingested, signed-off lesson record under content/lessons/ that renders in the reader with its designed delivery mode, is inserted before first contact in a learning session, is readable from the progress library, and links from feedback on its error blocks. Mahfuj Mustafa set the rules: never run the full pytest suite (narrow selectors only; the full client vitest run is allowed); no em or en dashes anywhere; Python with 3-space indentation, double quotes and decomposed conditions; a new test counts only once shown red; never report a check passing without its quoted output; no engine constants change; .claude/ is tracked on the branch but never reaches main.

## Where the work stopped

The Opus weekly usage limit was reached at about 06:40 UTC on 2026-09-29 (it resets Oct 3, 5am UTC). Three agents were terminated by the API mid-task (audit batches 24 and 25, the fixer for audit batch 20) and two framework workers (engine insertion, checker alignment) were still running on Opus and may have stopped at their next call. Their partial edits are on the branch in the "in progress" commits; nothing they wrote is verified.

## What is done and verified

| Piece | State | Evidence |
|---|---|---|
| Designs | 129 concept designs checked (Units 1 to 8 complete, 09001, 09007) plus LSN-DEC-06-01; Units 9 (15) and 10 (26), all 77 LSN-PRQ and 9 LSN-DEC are todo | docs/lessons/PROGRESS.md manifest; tools/check_lesson_designs.py clean on every checked design |
| Delivery specs | all 876 design delivery specs draw in the reader (22 prose specs rewritten numerically) | commit 8e78ccb; the reader author's scan flagged 0 |
| Backend framework (slice L1) | schema delivery field, delivery lint, five tables, app/lessons/ingest.py, repository.py, app/api/routes/lessons.py (six endpoints), purge and export, tools/lesson_resolve_compare.py, docs/operator/lessons.md | narrow selectors: 269 passed; tools/check_lessons.py content/lessons exit 0 (before the alignment work began) |
| Web reader | app/web/src/lessons/ with every delivery mode and fallbacks, checks with error links, progress Lessons tab, lesson destination, render harness renderRecord.test.tsx | npm run build green; vitest 68 files, 786 tests |
| Blind re-solve | 524 of 524 problems across 130 designs agree (440 by machine, 82 by an Opus judge, 2 refuted or clarified) | docs/lessons/verification/<id>.json, resolve block |
| Sign-off audit | 124 of 130 designs audited by Opus in batches of five; fixes landed for batches 1 to 11, 13, 14, 15, 19 | docs/lessons/verification/<id>.json, audit block with fix_notes; docs/lessons/audit-notes.txt holds every advice item |

## What is not done, exactly

1. Audits: LSN-CON-08010 to 08014 (batch 24) have no audit block; batch 25 (08015 to 08019) reported nothing before termination, so check each file for an audit block and re-run the batch if missing. Audit prompt and batch files: the AUDITOR.md and FIXER.md texts are reproduced at the end of this file.
2. Unfixed audit findings, all recorded in the verification files:
   - batch 20 (LSN-CON-07002 to 07006): 07004 ki-2 reverses the slope field independence rule; 07005 ki-1 claims curves never cross the equilibrium; 07005 err-BC-ERR-05013 wrong step reaches a true conclusion; 07006 motion spec true_curve must be 4*exp(x) - 2*x - 3; 07006 err-BC-ERR-07020 and 07021 label final values as slopes; 07002 err-BC-ERR-07008 staged where the sides agree; 07003 block shows a particular solution where the record is about a general one.
   - batch 16: 06004 chk-3 option D wrong direction; 06006 "sample point at i = 0 gives a" holds only for right forms; 06003 ex-2 no-calculator item under a II-A budget.
   - batch 17: 06011 err-BC-ERR-99032 and chk-3 option D misattributed.
   - batch 18: 06015 chk-3 options A and D both cite BC-ERR-06018; 06013 BC-ERR-06030 block shows the BC-ERR-06016 picture; 06014 BC-ERR-06033 reason does not match.
   - batch 23: 08008 st-1 cue 23 words; 08009 err-BC-ERR-08017 same expr on both sides.
   - batch 26: 09007 vector_diagram head y should be -0.946; LSN-DEC-06-01 st-1 method wrong for composite upper limits, st-2 cue 23 words, stems drawn outside BC-QA-06012's parameter_spec, chk-1 and chk-3 error_path BC-ERR-06028 and chk-2 option B BC-ERR-99032 mislabelled.
3. Served text carries record ids and [inferred] tags in 159 blocks across 82 designs (a scripted sweep: strip parenthetical ids and page citations from orientation, key idea and strategy text, move them to sources, then re-run the design checker and copy its computed word counts). Batch 6 was fixed by hand; the rest were not.
4. Delta blind re-solve for the lessons whose problems or keys changed after the re-solve: LSN-CON-01001, 01007, 01010, 01012, 01013, 01014, 01015, 01016, 01019, 02001, 02002, 02003, 02004, 02006, 02007, 02009, 03007, 03008, 03009, 03010, 04007, 04011, 05002, 05004, 05009, 07001 (extract with tools/lesson_design_resolve.py extract, solve blind on Sonnet, compare, judge statement answers).
5. Record checker alignment and the transcriber (worker D, WORKER_D.md): the record checker tools/check_lessons.py predates the designs and rejects faithful transcriptions (Set, Union, Interval, SetMinus, infinities and NaN MathJSON heads; equation equivalence; step relations; research heading citations; strategy substring rule; numeric form on exact keys; a wrong drawn-block cap; provenance.design_path; delivery.sources; file paths). Partial edits exist in app/items/mathjson.py, app/items/verify.py, schemas/lessons/lesson.schema.json, tests/items/test_verify.py. Unverified. Finish per WORKER_D.md and prove it by transcribing every design into a scratch directory and driving the record checker to zero findings.
6. Engine insertion and re-teaching (worker C, WORKER_C.md): partial edits exist in app/lessons/gate.py, app/session/build.py, app/session/service.py, app/api/routes/sessions.py, app/experiments/switches.py, app/web/src/session/SessionScreen.tsx, ElaboratedPanel.tsx, SessionLesson.test.tsx, tests/session/test_lesson_gate.py. Unverified. Finish per WORKER_C.md; run tests/session, tests/lessons, tests/api/test_lessons_routes.py and the client vitest.
7. Records: content/lessons/ holds LSN-CON-02013 (predates its design, differs in 32 of 47 fields) and drafts for 01008, 01014, 01015, 02002, 02003, all status draft. Once item 5 lands: transcribe every audited design with tools/lesson_transcribe.py, run tools/check_lessons.py and tools/lesson_resolve_compare.py per record, set status signed_off where the verification file shows all_agree and audit counts of zero unsourced and zero wrong, ingest, and run the render harness (LESSON_RECORD=../../content/lessons/<id>.json npx vitest run src/lessons/renderRecord.test.tsx from app/web).
8. Ledger and plan: BUILD-LEDGER.md has no entry for this session; docs/lessons/BUILD-PLAN.md still has the draft numbers. The amendments list to write is in docs/lessons/audit-notes.txt (recurring defect classes: error blocks whose wrong and right expressions coincide; error blocks and distractors citing a BC-ERR whose behaviour does not match; verbatim scoring_consequence text from other rubrics; ids and tags in served text; "either" archetypes timed as I-A; brief cap dropping scoring tags, amendment A-8).
9. Pushing to main from the cloud session was denied by the auto-mode classifier; main was to carry the branch with .claude/ stripped.

## Rulings still needed from Mahfuj Mustafa

- Whether archetype key invariants ("k =" in key, "continuous on" in key) apply to lesson checks.
- Whether a one-sided limit value (oo) is acceptable as an MCQ distractor when the two-sided limit does not exist (LSN-CON-02003 chk-3 option C).
- Whether the exam-part budget for a lesson is the whole free-response question or the part (several Unit 4 and 8 lessons budget 15.0 minutes for one part).
- Whether served text may carry record ids (the sweep in item 3 assumes not).

## Order to resume in

1. Verify or revert the partial worker C and D edits (items 5 and 6); do not trust the in-progress commits.
2. Finish audits (item 1) and fixes (item 2) on Opus; then the served-text sweep (item 3) and the delta re-solve (item 4).
3. Transcribe, check, sign off, ingest and render every record (item 7).
4. Ledger, BUILD-PLAN numbers, PROGRESS.md, merge to main without .claude (items 8 and 9).

## Prompts used (reproduced so the process is repeatable)

Auditor: audit each design's machine record block by block against the authoring bundle, the cached CED page text and the cited research headings only; verify every mathematical claim with SymPy; per block one verdict of ok, unsourced, wrong, over_cap or lint with one line of evidence; judge delivery fit as advice; write the audit block {date, auditor, blocks, advice, counts} into docs/lessons/verification/<id>.json, keeping the resolve block; edit nothing else.

Fixer: for each audited design, fix every non-ok block at the source in the design (machine record and the prose that repeats it), proving value changes with SymPy; also fix defect-class advice (identical wrong and right expressions, a claim a check contradicts, a window that cuts the curve, a key form the lesson's invariant rejects); run tools/check_lesson_designs.py to zero findings and copy its computed word counts; set fixed blocks to ok with evidence "fixed <date>: ..." and add fix_notes.

Blind re-solver (Sonnet): read only the problems file, solve every entry independently, answer as a SymPy-parsable expression, three decimals for calculator problems, or the option letter; write answers.json. Judge (Opus): for statement-form keys, decide agree or disagree with SymPy evidence; write judgments.json; apply with tools/lesson_design_resolve.py judge.
