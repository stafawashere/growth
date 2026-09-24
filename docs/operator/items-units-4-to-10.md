---
title: Items for Units 4 to 10, stage 1
research_date: 2026-09-24
status: complete
purpose: The canonical record of stage 1 (P2 scope item 8), which archetypes get items and why, where the banks live, how they are authored and verified, and what is still open.
---

# Items for Units 4 to 10, stage 1

Stage 1 of the eight-stage run (`.claude/prompts/stages/01-content.md`, local only) builds
verified, signed-off items for every active `no_calculator` archetype in Units 4 to 10 whose
answer is closed-form, and fills the Units 1 to 3 `no_calculator` archetypes P1 did not cover.
Before it, the bank held 130 signed-off items for 13 of 144 archetypes (`content/items_p1_agent/`).
The target is at least 10 items per archetype and 20 where the parameter family is rich, because
the student must not meet repeats and P4's exit asks for 20.

This file holds the scope rule, the bank layout and the verification workflow. The P1 record
shape it reuses is [items.md](items.md); the audit procedure is [key-audit.md](key-audit.md); the
subscription workflow it runs on is [offline-authoring.md](offline-authoring.md). Where the run
stands between sessions is BUILD-LEDGER.md, "In progress".

## Result [verified]

656 signed-off items in nine banks for 33 archetypes, 17 to 23 per archetype, every key
rechecked against a blind SymPy formulation with the control holding, `tools/check_items.py`
clean on every bank, and gate 29 over a fresh 100-item draw from these banks measured at 0/100
(Wilson 95 percent interval 0 to 0.037, docs/operator/key-audit-p2/).

| Bank | Items | Archetypes and counts |
| --- | --- | --- |
| `items_unit01_agent` | 40 | 01003 20, 01009 20 |
| `items_unit02_agent` | 40 | 02003 20, 02009 20 |
| `items_unit03_agent` | 20 | 03009 20 |
| `items_unit04_agent` | 40 | 04007 20, 04009 20 |
| `items_unit05_agent` | 35 | 05007 18, 05012 17 |
| `items_unit06_agent` | 120 | 06002, 06008, 06009, 06010, 06012, 06013, 20 each |
| `items_unit07_agent` | 84 | 07003 23, 07004 20, 07007 18, 07011 23 |
| `items_unit09_agent` | 20 | 99003 20 |
| `items_unit10_agent` | 257 | 10002, 10003, 10005, 10008, 10009, 10010, 10011, 10012, 10014, 10016, 10017, 10018 20 each, 10019 17 |

Five of the 38 in-scope archetypes got no items, because the BC-ERR records their skills hold
cannot produce three honest, distinct distractors (see "Distractor constraints"):

- BC-QA-01005, squeeze theorem: BC-ERR-01012 leaves bounds with the key's limit, and BC-ERR-01013
  gives the key or 0/0.
- BC-QA-06011, improper integrals: BC-ERR-06025 needs a divergent integral, and BC-ERR-99007
  gives at most two values.
- BC-QA-06014, limits of Riemann sums: BC-ERR-06003 makes the sum unbounded.
- BC-QA-07010, solution behaviour from the equation: BC-ERR-07018 and 99024 are about Euler
  estimates and sketching, and BC-ERR-07012 gives at most one value.
- BC-QA-10006, limit comparison: only BC-ERR-10018 changes the limit's value.

Each needs more error records linked to its skills, which is research-library work under the
repository CLAUDE.md (staging files and `tools/merge_staging.py`), not item work. Until then they
are coverage gaps the engine logs (R18).

## What the archetype registry holds [verified]

Counted from `data/archetypes.json` on 2026-09-24. It holds 144 archetype records, 139 of them
active (the count `app/content/loader.py` loads). Active `no_calculator` archetypes by unit:
Unit 1 12, Unit 2 11, Unit 3 6, Unit 4 2, Unit 5 4, Unit 6 11, Unit 7 8, Unit 10 20, Unit 8
none, and one in the synthesis block, BC-QA-99003, whose `primary_unit` is BC-UNIT-09. That is 46
for Units 4 to 10, as the stage brief says, and 29 for Units 1 to 3, of which P1 covers 13, so
16 are candidates there. 62 candidates in all.

The loaded snapshot also holds 390 active BC-ERR records and 541 skills.

## The closed-form rule [inferred]

An archetype is in scope when all of these hold:

1. it is active and `no_calculator`, and P1 does not already cover it;
2. what it asks for can be posed as one finite value or one expression;
3. that value can be written in the MathJSON `app/items/mathjson.py` reads, and so graded by the
   short-answer grader (`app/items/grade.py` `_grade_short_answer`) when R29 serves the item with
   no options;
4. the stem can be written in text, with no figure. Items carry no figure field.

Rule 3 binds tightly. The reader accepts numbers, symbols, `Pi`, `ExponentialE` and the heads
Add, Subtract, Multiply, Divide, Power, Root, Log, Rational, Equal, Negate, Sqrt, Exp, Ln, the six
trigonometric functions, Arcsin, Arccos, Arctan and Abs. It has no Infinity, Interval, Sum,
Integrate, Factorial, set or list, and anything else raises `UnsupportedMathJSON`.

Extending the reader was considered and rejected for this stage. Adding Infinity or Interval
would change what the client's MathLive input must produce and what the grader compares, which
is outside a content stage and would need its own tests and client work.

### In scope, 38 archetypes [verified]

| Unit | Archetypes | Bank directory |
| --- | --- | --- |
| 1 | BC-QA-01003, 01005, 01009 | `content/items_unit01_agent/` |
| 2 | BC-QA-02003, 02009 | `content/items_unit02_agent/` |
| 3 | BC-QA-03009 | `content/items_unit03_agent/` |
| 4 | BC-QA-04007, 04009 | `content/items_unit04_agent/` |
| 5 | BC-QA-05007, 05012 | `content/items_unit05_agent/` |
| 6 | BC-QA-06002, 06008, 06009, 06010, 06011, 06012, 06013, 06014 | `content/items_unit06_agent/` |
| 7 | BC-QA-07003, 07004, 07007, 07010, 07011 | `content/items_unit07_agent/` |
| 9 | BC-QA-99003 | `content/items_unit09_agent/` |
| 10 | BC-QA-10002, 10003, 10005, 10006, 10008, 10009, 10010, 10011, 10012, 10014, 10016, 10017, 10018, 10019 | `content/items_unit10_agent/` |

### Out of scope, 24 archetypes, and why [inferred]

- The answer is a verdict, a classification or a justification, not a value: BC-QA-01006,
  01007, 01011, 01013, 01014, 02004, 02005, 02012, 05010, 06016, 07005, 10001, 10004, 10007,
  10015, 10020.
- The archetype exists to read a printed graph or slope field: BC-QA-01001, 03003, 05005,
  06003, 06004, 07001, 07002. BC-QA-07002 half computes slopes at named points, which is
  closed-form, but its defining task is matching a printed field, so it stays out.
- The answer is an interval the reader cannot hold: BC-QA-10013. BC-QA-10014 (radius only)
  covers its ratio-test half.

These stay coverage gaps for the engine (R18 logs them) until a figure-capable or
verdict-capable item form exists.

## How each in-scope archetype is posed [inferred]

Where the natural answer is a verdict, infinite or not unique, the stem asks for its finite part.
These were the framing notes handed to the authoring agents.

- 01003: limits of two or three functions at a point are stated; the stem asks for the limit of
  a sum, product, quotient with a nonzero denominator limit, or composite.
- 01005: bounding functions and the inequality are stated; the stem asks for the limit.
- 01009: exactly one vertical asymptote, sometimes beside a removable discontinuity; the stem
  asks for c in x = c. The one-sided infinite limits are not asked, since the reader has no
  Infinity.
- 02003: a difference quotient; its value. 02009: values of f, g, f', g' written inline as a
  table; the derivative of a product or quotient there. 03009: an expression whose rule must be
  chosen first; its derivative or its value at a point.
- 04007: a point moving on an implicit curve, one rate given; the other rate. 04009: a 0/0 or
  infinity/infinity limit, finite, sometimes with f known only through stated values.
- 05007: a function given by a differential equation or an accumulation function; the
  x-coordinate of the named relative extremum. 05012: the coordinate of a critical point, or a
  second derivative at a point, on an implicit curve or a differential equation.
- 06002: a rate table inline, uneven widths in some items; the trapezoidal sum. 06008, 06009,
  06010: a definite integral or a pinned antiderivative value F(b) given F(a), never "+ C", so the
  answer is unique. 06011: convergent improper integrals only. 06012: g'(c) for an integral with a
  plain or composite variable limit. 06013: combining stated integral values. 06014: the value of
  a limit of Riemann sums.
- 07003: the explicit particular solution, or y at a point. 07004: Euler's method, exact
  rational. 07007: the constant that makes a candidate family a solution, with a sign condition
  when two would work. 07010: a quantity read from the equation without solving, such as the
  x-coordinate of a critical point. 07011: the branch-correct particular solution, the finite
  endpoint of the largest open interval of existence, or y from the accumulation form.
- 99003: the slope dy/dx of a polar curve at a stated angle.
- 10002, 10003: a series value, numeric or in x with the convergence condition stated. 10005: the
  value of the convergent improper integral the integral test pairs with a series. 10006: the
  limit of the ratio of general terms against a named comparison series. 10008: the alternating
  series error bound for a partial sum, or the least number of terms for a tolerance. 10009: the
  Lagrange error bound at a point. 10014: the radius. 10010, 10011, 10012, 10016, 10017, 10018,
  10019: a Taylor or Maclaurin polynomial of stated degree or number of nonzero terms, a
  coefficient, or a radius. No general term with n! is ever a key, because the reader has no
  Factorial.

## Distractor constraints the registry imposes [verified]

Every distractor's `error_path` must be a BC-ERR id held by a skill of the item's own archetype
(computed by `app/items/distractor_paths.py` `error_ids_for_skills`). For the in-scope
archetypes the held counts, from the snapshot of 2026-09-24, are:

| Held errors | Archetypes |
| --- | --- |
| 1 | 06010 (BC-ERR-06026), 06014 (BC-ERR-06003), 10019 (BC-ERR-99018) |
| 2 | 01003, 01005, 02003, 06011, 10016 |
| 3 | 01009, 06013, 07010, 10010, 10011, 10017 |
| 4 | 02009, 03009, 06012, 10002, 10012 |
| 5 | 04007, 04009, 05007, 06009, 07007, 07011, 10003, 10006, 10014, 10018 |
| 6 to 9 | 05012 (6), 06002 (7), 06008 (6), 07003 (9), 07004 (7), 99003 (8), 10005 (6), 10008 (9), 10009 (6) |

Two distractors may cite the same error when it is applied at different places, as P1's
BC-QA-03005 items do. Where a single held error cannot honestly produce three distinct values
the item family is narrowed or the archetype is reported as infeasible, never tagged with an
error it does not hold:

- 06010: BC-ERR-06026 is "improper rational integrand decomposed without a preliminary division",
  so every 06010 item must have numerator degree at least the denominator's.
- 06014: BC-ERR-06003 is "function values summed without the width", which makes a limit of
  sums unbounded, so 06014 got no items.
- 10019: BC-ERR-99018, mis-assembled general term, applied at three places in the term-by-term
  integration (power raised without dividing, divided without raising, divided by the old
  exponent); 17 items.
- Some held errors produce no different value at all (BC-ERR-10017, a limit written without
  limit notation), so they cannot tag a distractor.

## Bank layout and serving [verified]

- One directory per unit, `content/items_unitNN_agent/`, each with its own `key_formulations.py`,
  beside `content/items_p1_agent/`. Per-unit banks let authoring and formulation fan out without
  two writers sharing a formulations file, and `tools/key_recheck.py` takes one directory and one
  formulations file.
- Ids are `ITM-AGT-<5-digit archetype suffix>-NN`, NN from 00, so ids cannot collide across
  banks. The bank still refuses an id found in two directories
  (`app/runtime/bank.py` `refuse_duplicate_ids`), because `ingest_new_records` skips any id
  already stored and would otherwise serve whichever directory came first.
- `app/main.py` `items_directories(env)`: `GROWTH_ITEMS_DIR` unset means every directory matching
  `content/items_*`, in name order (`default_item_directories`); a set value lists directories
  separated by `os.pathsep`; `none` disables the bank; a listed path that is not a directory
  stops startup. `Settings.items_directory` became `items_directories`, a tuple, and
  `app/runtime/context.py` `build_session_context(..., items_directories=())` builds an
  `ItemSource(directories=...)`, which the bank ingests directory by directory on its first query.
- Ingestion still checks each record against every active error in the snapshot
  (`frozenset(snapshot.errors)` in `app/runtime/context.py`). The per-archetype rule is enforced
  by `tools/check_items.py` and the standing tests, not at ingest.

## Record rules for these banks [verified]

The shape is P1's ([items.md](items.md)), with these settled for stage 1:

- `format` `mcq`, four options A to D, exactly one `is_key`, the key letter spread over A to D;
  distractors carry `error_path` and `violated_step`, a zero-based index into the archetype's
  `expected_solution_path`.
- `answer_key.form` `symbolic` with an exact MathJSON value, never a decimal.
- At least three `worked_solution` steps. `app/runtime/bank.py` `COMPLETION_MINIMUM_STEPS` is 2,
  and the completion stage blanks the last step.
- Stems are format-neutral: "Find ...", never "Which of the following" or anything that assumes
  choices (`choice_worded_stem` in `tools/key_recheck.py` enforces the common wordings). Inline
  LaTeX between `\(` and `\)` is allowed and renders through `app/web/src/math/MathText.tsx`;
  P1's agent drafts used plain text.
- `representation` is one the stem uses in text: BC-REP-01, 03 (a table written inline), 06, 11
  or 13.
- `authored_by` is `claude-opus-5-5 agent draft, stage 1 content run of 2026-09-24` until
  sign-off, when `tools/sign_off_items.py` moves it to `drafted_by` and writes `signed_off_by`.

## Authoring and verification workflow [verified]

1. Briefs. A scratch script wrote one brief per archetype: the record's fields and the held
   errors with their names and observed behaviour, and the solution path indexed for
   `violated_step`.
2. Authoring. Six subagents, each writing drafts only into its unit directories: Units 1 to 3;
   Units 4, 5 and 9; Unit 6; Unit 7; Unit 10 in two halves (10002 to 10014 and 10010 to 10019),
   both into `content/items_unit10_agent/`. Each had to compute every key and distractor in SymPy
   in its own scratch folder and run `tools/check_items.py` on its directory until clean, and to
   report archetypes where the held errors cannot give three honest distractors.
3. Blind formulation. For each bank a separate agent is given only a stems file (id, archetype,
   stem text) and writes `key_formulations.py` with the `tools/key_recheck.py` helpers. It may not
   open the item records, run the recheck or read git history. This replaces the authoring agent
   as the independent reader, because the author knows its keys.
4. Recheck and triage by the orchestrator, per the question-bank-audit skill: every flag is
   triaged by re-reading the stem, never by editing a formulation to agree with a key.
5. `tools/check_items.py` clean on every bank, then sign-off with `tools/sign_off_items.py
   --items-dir <bank> ... --by "<model> on the operator's delegation of 2026-09-24"`.
6. Gate 29 over the new items: ingest only the unit banks into a scratch database, draw 100 with
   `tools/draw_key_audit_sample.py` (the unit cap from `app/review/audit.py` `unit_cap_for`), write
   the worksheet with `tools/key_audit_worksheet.py` (now takes `--items-dir` more than once and,
   unset, searches every `content/items_*` bank), record verdicts in a
   `docs/operator/key-audit-p2/` beside `key-audit-p1/`, with the rate and its Wilson interval.

## Tooling changed in this stage [verified]

| Change | Where | Evidence |
| --- | --- | --- |
| Each distractor's error_path checked against its own archetype's held errors, where it used the union over the 13 P1 archetypes; an unknown archetype is a violation; counts printed for every archetype seen | `tools/check_items.py` | `test_check_items_rejects_an_error_path_held_only_by_another_archetype` failed on the old file (stash), passed on the new; P1 130 and the 36 fixtures stay clean |
| 20 helpers: definite and improper integrals, pinned antiderivative, accumulation derivative by the fundamental theorem, trapezoidal sum, Riemann-sum limit, series value, first omitted term, least terms for a tolerance, limit comparison, Lagrange bound, radius by the ratio test, Taylor polynomial, Taylor from derivative values, derivatives along a solution and Taylor from a relation, Euler, particular solutions with branch filtering, is_solution, polar slope, related rate, function_with_values | `tools/key_recheck.py`; symbols `t`, `theta` exported | `tests/items/test_key_recheck_helpers.py`, 21 tests; a mutation per helper turned its test red, all restored to 21 passed |
| Ingestion over several directories, duplicate-id refusal | `app/main.py`, `app/api/app.py`, `app/runtime/context.py`, `app/runtime/bank.py` | `tests/runtime/test_item_directories.py`, 5 tests; three mutations (first directory only, no duplicate check, default of P1 only) each turned one red |
| Worksheet over several banks | `tools/key_audit_worksheet.py` | new test failed with only the first `--items-dir` read |
| Standing recheck over every bank | `tests/items/test_key_recheck.py` `test_every_bank_rechecks_clean`, parametrised over `default_item_directories()` | red on the nine unit banks while they had no formulations, green on all ten banks once they did |
| Control perturbation without a fixed point | `tools/key_recheck.py` `perturbations` | two new tests, each red under its break |
| Record files named by their id | `tests/runtime/test_item_directories.py` | red with a duplicate copy in a bank |
| Audit record test over both gate 29 records | `tests/review/test_key_audit_records.py` (was `test_p1_key_audit_record.py`), parametrised over key-audit-p1 and key-audit-p2 | red with the P2 README's rate changed to 1/100 |
| Unit 6 served end to end | `tests/e2e/test_unit_6_item_served.py` | see the last section |

Mutation lesson: the first break of `derivatives_along_solution` (dropping the `* slope_field`
factor) survived because the test used y' = x + y with y(0) = 1, where y'(0) = 1 and the factor
is invisible. The test now uses y' = x + y^2 with y(0) = 2, where the break gives 5 for y''(0)
instead of 17.

## Known gaps and risks [inferred]

- Ingestion cost. The bank runs every record's checks on its first query, and off the main
  thread each bounded SymPy comparison runs in its own forkserver child
  (`app/items/verify.py` `run_bounded`). Measured on 2026-09-24: 120 Unit 6 records in 3.4 s,
  766 records in 77.8 s, and the two end-to-end tests that ingest the Unit 6 bank and every bank
  took 370 s together while other stages ran on the machine. On the operator's database this is
  paid once per new record, because stored ids are skipped; every test that builds the app with
  the default banks pays it in full. A fix (one bounded child per record, or checks cached by
  record hash) is left for a later stage.
- `tests/e2e/test_agent_drafts_served.py` now asserts `items_directories ==
  default_item_directories()`, reads keys from every bank and accepts either drafting string in
  `drafted_by`.
- Some distractor tags stretch their error's wording, each named by its authoring agent and
  accepted on review: 05022 (extremum of g' read as g's extremum), 03023 (every dy/dx term
  dropped), 06010's third distractor (constants from one root and x = 0), 06012 options that
  contain t, 10005 options that contain b, 02003's wrong-base readings such as e^e, and 10016's
  index offsets tagged 99018.
- Every 10005 stem presupposes convergence, and 06011 has no items, so no item asks the student to
  recognise a divergent improper integral.
- Ingestion time over about 800 records is unmeasured. P1's 130 take seconds on the first query,
  and every test that builds the app with `GROWTH_ITEMS_DIR` unset will pay for all banks.
- The standing recheck now recomputes every bank on each suite run; its time over about 800
  items, several needing `dsolve` or `summation`, is unmeasured.
- The briefs, the authoring and formulation instructions, the stems-dump script and the mutation
  script exist only in the session scratchpad, not the repository. A session resuming this stage
  regenerates them: a brief is the archetype record plus
  `error_ids_for_skills(snapshot, archetype["skills"])` with each error's name and observed
  behaviour, and a stems file is id, archetype and `stem.text` for every record in a bank.
- The formulation agents and the authoring agents are the same model family, so an error both
  would make the same way is not excluded; the recheck's control proves only that the comparator
  can see a difference.

## Review findings that changed items [verified]

- The 20 BC-QA-10005 stems asked for "the improper integral whose convergence matches that of the
  series" or the integral "used in that test", which any lower limit at or above the starting index
  satisfies. They now say to take the series' general term with n replaced by x and the lower
  limit at the starting index; the 7 that already named f keep only the lower-limit sentence.
  No key changed.
- Two byte-identical copies, `ITM-AGT-03009-00 3.json` and `ITM-AGT-03009-01 2.json`, appeared
  beside their originals (the same file-system duplication as the stray
  `.gate-reduced-motion N.json` files the stage brief names). They would have been ingested as
  second records with the same id. Deleted, and
  `tests/runtime/test_item_directories.py` `test_every_record_file_is_named_by_its_id` now fails on
  any record file not named `<id>.json` (shown red with a copy in place).
- The recheck's control perturbed each sampled answer as 2v + 1, which leaves -1 fixed, so the
  Unit 10 bank's run exited 2 on ITM-AGT-10003-04, whose answer is -1, with a sound comparator. The
  control now also applies v + sqrt(2)/7, which has no fixed point, and drops any perturbation
  identical to the value (`tools/key_recheck.py` `perturbations`). Every answer still meets 2v + 1
  unless it is -1, so no case the old control caught is lost.
  `test_the_control_holds_on_an_answer_of_minus_one` failed with the old perturbation and
  `test_a_comparator_that_calls_everything_equal_fails_the_control` failed with the control
  disabled.

## The end-to-end requirement [verified]

`tests/e2e/test_unit_6_item_served.py` builds the application with `build_application`, the test
passkey verifier and the replayed tutor, with `GROWTH_ITEMS_DIR` naming only the Unit 6 bank. It
registers a student, marks every seeded `skills_state` row outside Unit 6 mastered (registration
seeds 618 rows, 83 already mastered, probe of 2026-09-24), and then goes through the HTTP routes
only. It opens a learning session and asserts that the first item served is a Unit 6 item
(`primary_unit` BC-UNIT-06). It answers the item, rates it and reads the feedback. It asserts that
the stored provenance model is `operator`. Before sign-off it failed on that last assertion, with
the model still the drafting string. After sign-off it passes.
