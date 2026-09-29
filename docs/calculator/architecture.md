---
title: Desmos fluency, architecture
research_date: 2026-09-29
status: draft
purpose: The tables, routes, drill templates, content files, checker, pacing and progress integration, purge and export, retention rows and the Desmos API decision behind docs/calculator/design.md, so a build agent can implement a slice without redesigning it.
---

# Desmos fluency, architecture

Companion to [design.md](design.md), which says what the student meets; this file says how it is built. The research behind both is under [research/](research/) and ranked in [research/synthesis.md](research/synthesis.md). Every decision here that a plan document already makes is cited to it; every new one is tagged [inferred] and listed in the plan amendments of [build-plan.md](build-plan.md).

## The invariant that bounds the layer [verified]

Plan 15 states the rule for fluency (docs/plan/15-lessons.md, Fluency, measured and never credited) and the bounding invariant L0 for a layer that measures without crediting. The calculator layer adopts the same shape:

> **C0.** For every user and every sequence of calculator card reads and calculator drill answers, the `skills_state`, `attempts`, `diagnoses`, `pending_probes`, `judgments`, `gradings`, `experiment_assignments`, `sessions`, `assessment_parts` and `assessment_responses` tables are unchanged before and after, and the only tables a calculator event may write are `calculator_drills` and `audit_log`.

Tested as a property test over random event sequences (tests/calculator/test_invariants.py) and as a route test that snapshots `skills_state` before and after a drill (tests/api/test_calculator_routes.py). No selection function, no FSRS update and no credit assignment reads `calculator_drills`.

## Tables and migration [inferred]

One new table, `calculator_drills`, in app/db/models.py. `Base.metadata.create_all` creates it on the next open (app/db/migrate.py adds columns, tables need only the model), so no hand migration step exists.

| Column | Type | Meaning |
|---|---|---|
| id | Text PK | `cdr-` plus a random suffix |
| user_id | Text, indexed | owner; puts the row under export and purge through `owner_clause` |
| template_id | Text | the drill template, `CDT-<capability>-<nn>` |
| capability | Text | one of `plot`, `zero`, `derivative`, `integral`, `intersection`, `value` (the four CED capabilities plus the two further exam uses the research catalogues; a mixed draw picks one of these at random) |
| draw | Text JSON | the parameter draw and its seed, so the task can be re-rendered |
| desmos_url | Text | the calculator variant opened beside the task, so a later change of variant is visible in the record |
| served_at | Text ISO | when the task was shown |
| submitted_at | Text ISO, nullable | when the answer arrived; null while open |
| elapsed_ms | Integer, nullable | client-measured from first paint of the task to submit, bounded by the server against served_at |
| value_entered | Text, nullable | the decimal string the student typed |
| value_correct | Integer 0/1, nullable | the three-decimal check |
| value_reason | Text, nullable | why the value failed: `not_three_places`, `outside_tolerance`, `not_a_number`, `missing` |
| setup_entered | Text JSON MathJSON, nullable | the setup expression typed in the math field |
| setup_shown | Integer 0/1 | whether any setup was entered |
| setup_correct | Integer 0/1, nullable | the equivalence check |
| setup_reason | Text, nullable | `missing`, `not_equivalent`, `unsettled`, `unsupported` |
| created_at, updated_at | Text ISO | as every table |

No column stores a score, a streak, a goal or a rate aim. `elapsed_ms` is a measurement, in the same sense as `attempts.elapsed_ms` (plan 09 retention table, "Timing per item"), never a grade input.

`tests/db/test_models.py` gains `calculator_drills` in its expected table set; `tests/export/test_export.py` `INVENTORY_TABLES` gains it because plan 09's inventory names it (the amendment in build-plan.md).

## Drill templates [inferred]

A template is a Python module under app/calculator/templates/ named `cdt_<capability>_<nn>.py`, shaped like app/generation/templates/qa_NNNNN.py so the same kit serves both: it exposes `TEMPLATE_ID`, `CAPABILITY`, `CARD_ID` (the procedure card it drills), `TEMPLATE_VERSION`, `SPEC` (an app/generation/spec.py spec dict with `parameters`, `constraints`, `derived`) and `build(names) -> DrillTask`.

`DrillTask` (app/calculator/kit.py, a thin layer over app/generation/kit.py):

| Field | Meaning |
|---|---|
| prompt | the task sentence, LaTeX inline, no stem from any released question |
| function_tex | the function or functions as the student must type them |
| setup_key | MathJSON of the expected setup (an `Integrate`, a `D` applied at a point, an equation, a function application) |
| setup_kind | `expression` (compared by numeric equivalence through app/items/verify.py) or `equation` (compared as `lhs - rhs` proportional to the key's, since `f(x) = 2` and `f(x) - 2 = 0` and `2 f(x) = 4` are the same setup) |
| value_key | the exact value as a 20-digit `sympy.Float` from `kit.numeric_integral`, `kit.numeric_roots` or SymPy differentiation evaluated at the point |
| unit | optional unit string when the task states one |
| radian_sensitive | true when the function has a trigonometric factor, so the task carries the radian note plan 05 already requires on calculator items |
| exclusion | the reason a draw was rejected, for the checker's report (see next) |

Draws come from `spec.draw_with_seed(SPEC, seed)` with `seed = f"{TEMPLATE_ID}:v{TEMPLATE_VERSION}:{user_id}:{n}"`, where `n` counts that student's drills of that template, so the sequence is reproducible per student and never repeats a draw for the same student until the space is exhausted. Trivial draws are excluded by constraints in `SPEC` and by a post-build guard: a definite integral whose integrand is a polynomial of degree at most one, a zero at an integer or a half integer, a derivative at a point where the function is linear, an intersection at a lattice point, and any task whose `value_key` has fewer than three nonzero decimals (so rounding and truncation coincide and the drill cannot tell them apart) are rejected and redrawn. The checker counts exclusions per template over 200 seeded draws and fails a template that rejects more than half.

Keys are numeric: `kit.numeric_integral` (mpmath, 25 digits) for integrals, `kit.numeric_roots` for zeros and intersections (roots of `f - g`), SymPy `diff` then `N(..., 30)` for the derivative at a point, `N` for a function value. A template that needs SymPy to solve symbolically does not exist; every key is a numerical evaluation, which is what the calculator does.

## The three-decimal check [verified]

The rule is the scoring guideline's: a reported decimal is accurate to three places after the decimal point, rounded or truncated (research/exam/calculator-policy.md, Rounding and reporting, citing sg-25 p.3 and ced p.17). `app/calculator/check.py` `check_value(entered, key)`:

1. Parse `entered` as a decimal string (a leading minus, digits, at most one point; commas and spaces stripped; anything else is `not_a_number`; empty is `missing`).
2. Let `r = round(key, 3)` and `t = trunc(key, 3)` computed with the `decimal` module from the 20-digit key, never with binary floats.
3. Let `v` be the entered value and `d` its number of decimal places.
4. Accept when `round(v, 3)` or `trunc(v, 3)` equals `r` or `t` exactly. This accepts `3.900` for a key of 3.9004, `3.9` when the key is exactly 3.9, `3.90045` (more places than needed, still accurate), and both the rounded and the truncated three-place forms of every key.
5. Otherwise the reason is `not_three_places` when `d < 3` and the value would have been accepted with the missing places (that is, `v` agrees with `r` or `t` at `d` places), else `outside_tolerance`.

The app's item grader keeps its own absolute tolerance of half a unit in the third place (app/items/grade.py `DEFAULT_DECIMALS`); the drill check is stricter on form (it wants three places shown) and equal on value, and the two are kept separate because the item grader serves scoring while the drill check serves fluency feedback.

## The setup check [inferred]

`check_setup(entered_mathjson, task)`:

- `missing` when nothing was entered; the drill then reads "no setup shown", which is the reader's own error BC-ERR-99021 in the library's words.
- For `setup_kind == "expression"`: `app/items/mathjson.to_sympy` on both sides, then `app/items/verify.equivalence` (bounded, five seconds). An `Integrate` with numeric bounds and a `D` at a point both settle by `doit` or by the numeric sampler that `equivalence` already has; the check calls `doit()` on both sides first so a typed integral compares as a number against the key's integral. `UnsupportedMathJSON` gives `unsupported` and the drill says the expression could not be read, which counts as neither correct nor wrong and is recorded as such.
- For `setup_kind == "equation"`: both sides must be relations; `equivalence(lhs - rhs, k * (key_lhs - key_rhs))` is tried for the constant `k` that makes the leading terms agree, and a nonzero constant ratio is equivalent.
- `unsettled` from the bounded comparison is recorded as `unsettled`, never as wrong.

The setup does not have to be typed in the Desmos syntax; it is typed in the app's math field (MathLive) the way a written setup would appear on the booklet page, because the exam habit being carried is the written setup beside the result, not the Desmos keystrokes (the Desmos keystrokes are what the student does in the frame).

## Content files and the checker [inferred]

`content/calculator/cards/<CARD_ID>.json`, one procedure card per technique, id `CCD-<capability>-<nn>`:

| Field | Content |
|---|---|
| id, version, capability, title | identity |
| task | one sentence: what the exam asks for in this capability |
| steps | the exact Desmos steps, each `{text, keys}` where `keys` is the typed syntax or shortcut as Desmos documents it |
| demonstration | a worked instance: the function, the typed expressions in order, the result Desmos shows, the written setup and the three-place answer |
| exam_habit | the habit the card carries (radian mode, the setup beside the result, three places rounded or truncated, units), each with its `error_ids` (BC-ERR ids) |
| bluebook_note | how the Bluebook version changes the steps, or "none" |
| sources | page citations `doc:page` (for example `desmos-help-integrals:1`, `sg-25:3`, `ced:13`) with one `anchor_quote` per source of at most 25 words |
| evidence_tag | one of the four |
| drills | the template ids that drill the card |

`content/calculator/templates.json` lists every template id with its capability, card, version, the exclusion rules in words and its sources.

`tools/check_calculator.py` (CLI like tools/check_lessons.py, exit 1 on any finding): schema validity for every card (schemas/calculator/card.schema.json); every citation resolves to an existing cache/text/<doc>/page-NNN.txt and every anchor quote is found on that page (the same normalised search as qa/07_quotes.py); every `error_ids` entry is an active BC-ERR; no student-facing string contains a library id, citation, evidence tag, dash character, emoji, praise word, study advice or prediction word (the same lists tools/check_lessons.py uses, imported, not copied); every template module imports, builds 200 seeded draws, rejects fewer than half, produces a `value_key` with three nonzero decimals and a `setup_key` that `to_sympy` accepts, and is named by exactly one card; every card is drilled by at least one template; every capability in the table above has at least one card. The page-citation regex in tools/check_lessons.py is widened to admit the new doc ids (`[a-z0-9-]+:\d+`), which strengthens nothing and loosens nothing since existence on disk is what is checked.

## Routes [inferred]

app/api/routes/calculator.py, registered in app/api/app.py; the vite proxy list gains `/calculator`.

| Route | Body and response |
|---|---|
| GET /calculator/cards | the card list (id, capability, title, drills) |
| GET /calculator/cards/{card_id} | the full card |
| POST /calculator/drills | `{capability?, template_id?}`; draws a task for the signed-in user, writes the `calculator_drills` row with `served_at`, returns `{drill_id, template_id, capability, prompt, function_tex, unit, radian_sensitive, desmos_url, card_id}` and never the keys |
| POST /calculator/drills/{drill_id}/answer | `{value, setup_mathjson?, elapsed_ms}`; runs both checks, completes the row, returns `{value: {correct, reason, accepted_forms: [rounded, truncated]}, setup: {shown, correct, reason}, elapsed_ms, key: {rounded, truncated}, setup_key_latex}`; a second answer to the same drill is refused with 409 |
| GET /calculator/measured | per capability: `{drills, answered, value_correct, setup_shown, setup_correct, median_ms, budget_seconds}` with every count carrying its denominator, `median_ms` null under three answered drills with the words "not measured yet" supplied by the client; `budget_seconds` is the I-B per-question budget from app/assessment/shape.py, shown as the exam's own figure, never as a target |
| GET /calculator/drills?limit= | the student's recent drills for the measured view's list |

Every route uses `Depends(get_db, scope="function")`, `current_user`, and touches only `calculator_drills` and `audit_log` (`calculator_drill_served`, `calculator_drill_answered` in app/audit/vocabulary.py).

## Pacing and progress integration [inferred]

A sibling of app/progress/pace.py, `app/progress/calculator_fluency.py`, computes the measured payload: median `elapsed_ms` per capability over answered drills, accuracy of value and of setup as `value(label, numerator, denominator, denominator_label)` from app/progress/learning_metrics.py so the words match the other metrics ("median seconds per drill" over "answered drills"; "results accurate to three places" over "answered drills"; "setup shown" over "answered drills"). Nothing enters `pace_verdict`, `learning_metrics`, the mastery map or `fluent` (plan 15's `fluent` reads `attempts` only and stays so). The progress view links to the Calculator destination and does not repeat its numbers.

## Purge, export and retention [inferred]

`calculator_drills` has `user_id`, so app/export/archive.py `owner_clause` exports it and app/session/purge.py deletes it with no code change; the tests that enumerate tables are updated to expect it, and tests/session/test_purge.py's later-table test covers it. Plan 09's retention table gains one row, appended by the amendment in build-plan.md:

| Datum | Table or store | Purpose | Retention | Deletable |
|---|---|---|---|---|
| Calculator drill records: task draw, typed result, typed setup, correctness, elapsed time | `calculator_drills` | Fluency measurement per capability; never enters credit assignment | Until purge | Yes, individually, with no mastery consequence |

Nothing from inside the Desmos frame is stored: the app never receives the graph state (next section).

## The Desmos frame and the API decision [inferred]

The frame stays a sandboxed iframe of www.desmos.com under the existing `frame-src https://www.desmos.com` directive (docs/plan/09-security-and-privacy.md, CSP, 2026-09-27 exception), and no directive changes. Two decisions are recorded:

1. **Which Desmos, and how it opens.** The drill and the calculator items open the College Board version of the Desmos graphing calculator, https://www.desmos.com/testing/collegeboard/graphing, not the public https://www.desmos.com/calculator. Desmos states that testing calculators may differ from the public one and that the Testing page carries the version a test taker sees on test day, and its College Board PDF names what the Bluebook graphing calculator disables (research/bluebook-desmos.md). The origin is the same, so the CSP is unchanged; `DESMOS_URL` in app/web/src/input/DesmosPanel.tsx changes and the recorded `desmos_url` on each drill row names which variant was open. The page redirects `/testing/cb-sat-ap/graphing` to `/testing/collegeboard/graphing`, so the final URL is used. Verified to render inside the app's sandboxed frame in Stage D of the build ledger, or recorded there as failed with the public calculator kept. The desmos.com terms say the Desmos Tools may not be framed without Desmos's prior consent (research/synthesis.md, Rulings), so `DesmosPanel` carries one constant, `DESMOS_OPENS_IN`, `"frame"` today on the operator's 2026-09-27 instruction and `"window"` to open the same URL with `noopener` in a new window instead; the ruling is the operator's.
2. **The embedded API.** Not adopted. The Desmos API would let the app read the calculator state (`getState`, `observeEvent`), but it needs an API key from desmos.com/my-api, which means an account only the operator can create, and it loads `calculator.js` from desmos.com, which needs a `script-src https://www.desmos.com` amendment to the CSP that plan 09 today refuses on principle (every script is self-hosted). The API terms' free Trial Tier permits personal, non-commercial use, which this single-user app is, so the licence does not block it (research/bluebook-desmos.md quotes the clause). The drills therefore check outcomes only: the value the student reads off Desmos and the setup they type. If the operator obtains a key and rules that the CSP may name desmos.com for scripts, the frame can be replaced by the API calculator with the graph state kept in memory and never sent anywhere, and `check_setup` can additionally compare the typed Desmos expression; that is a ruling for the operator, listed in build-plan.md.

## Web [inferred]

app/web/src/calculator/: `CalculatorRoute.tsx` (destination, three sections: Cards, Drill, Measured), `ProcedureCard.tsx`, `DrillScreen.tsx`, `MeasuredView.tsx`, `calculatorLink.tsx` (the small link every calculator-part item, drill part and calculator lesson shows). Routing: `{view: "calculator", section: "cards" | "drill" | "measured", cardId?, capability?}` at `#/calculator/<section>[/<id>]`, a `TABS` entry labelled "Calculator" with the `graph` icon, and the App.tsx wiring the code context names. The drill screen reuses `DesmosPanel` opened by default beside the task from 1100px, stacked below it on narrower widths, `MathAnswerField` for the setup, a plain text input for the value (a decimal string, so the three-place rule is checked on what was typed), and an `elapsed_ms` measured from the task's first render with `performance.now()`.

## Tests [inferred]

pytest: tests/calculator/test_check.py (the value rule over rounded, truncated, short, long, wrong and non-numeric entries; the setup rule over equivalent forms, missing, unsupported, equation proportional forms), tests/calculator/test_templates.py (every template: 50 seeded draws build, keys have three nonzero decimals, exclusions hold), tests/calculator/test_invariants.py (C0 as a hypothesis property), tests/api/test_calculator_routes.py (draw, answer, refuse a second answer, measured with denominators, skills_state unchanged, purge and export reach the table), tests/tools/test_check_calculator.py (every lint shown red on a fixture). vitest: app/web/src/calculator/*.test.tsx (cards render from a mocked client, the drill submits value and setup and shows both verdicts and the accepted forms, the measured view says "not measured yet" under three drills, keyboard-only through the drill, reduced motion, the link on a calculator item and absence on a no-calculator item), App.test.tsx bar labels.
