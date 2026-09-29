---
title: Desmos fluency, build plan
research_date: 2026-09-29
status: draft
purpose: The ordered slices that implement docs/calculator/design.md and architecture.md, each with its files, tests, checks and acceptance, in the style of docs/lessons/BUILD-PLAN.md, plus the API contract the server and client slices build against and the plan amendments the feature needed.
---

# Desmos fluency, build plan

Every slice ends green on its own checks before the next starts, except slices 1a and 1b, and 3 and 4, which run in parallel against the contracts fixed here. Each new test is shown red against a broken input before it counts (CLAUDE.md, testing rules). Style: Python 3-space indent, double quotes, named conditions, blank lines between logic blocks; TypeScript as app/web's incumbent; no dashes as punctuation, no emojis; comments only where a human would write one.

## Contracts fixed for the parallel slices [inferred]

Capabilities: `plot`, `zero`, `derivative`, `integral`, `intersection`, `value`; the chooser also offers `mixed`, which the server resolves to one of the six by the draw's random source.

Template module interface (app/calculator/templates/cdt_<capability>_<nn>.py): constants `TEMPLATE_ID` (`CDT-<capability>-<nn>`), `CAPABILITY`, `CARD_ID`, `TEMPLATE_VERSION` (int), `SPEC` (an app/generation/spec.py spec dict), and `build(names) -> DrillTask`. `app/calculator/registry.py` exposes `templates() -> dict[str, module]` (every module in the package, keyed by `TEMPLATE_ID`), `templates_for(capability)`, and `draw_task(template_id, seed) -> DrillTask` (spec draw plus build plus the post-build exclusion guard, redrawing with `seed + ":r<k>"` up to 50 times, then `DrawExhausted`).

`DrillTask` (app/calculator/kit.py, frozen dataclass): `prompt` (str, LaTeX inline in `\( \)`), `function_tex` (str), `setup_key` (MathJSON), `setup_kind` (`"expression"` or `"equation"`), `value_key` (sympy.Float, 20 digits), `unit` (str or None), `radian_sensitive` (bool), `draw` (dict, JSON-serialisable parameters), `exclusion` (str or None; a non-None value means the task must be redrawn).

Check functions (app/calculator/check.py): `check_value(entered: str, key) -> ValueVerdict(correct: bool, reason: str | None, rounded: str, truncated: str)` with reasons `missing`, `not_a_number`, `not_three_places`, `outside_tolerance`; `check_setup(entered_mathjson, task) -> SetupVerdict(shown: bool, correct: bool | None, reason: str | None, key_latex: str)` with reasons `missing`, `not_equivalent`, `unsettled`, `unsupported`. Both pure, both importable by the checker and the routes.

Routes (app/api/routes/calculator.py) and payloads, which app/web/src/api/types.ts transcribes field for field:

| Route | Request | Response |
|---|---|---|
| GET /calculator/cards | | `{"cards": [{"id", "capability", "title", "task", "drills": [template ids]}]}` |
| GET /calculator/cards/{card_id} | | the full card record minus `sources` and `evidence_tag`: `{"id", "version", "capability", "title", "task", "steps": [{"text", "keys"}], "demonstration": {"function_tex", "lines": [{"typed", "shows"}], "setup_latex", "answer"}, "exam_habit": [{"text"}], "bluebook_note", "drills"}` |
| POST /calculator/drills | `{"capability": one of the six or "mixed", "template_id"?: str}` | `{"drill_id", "template_id", "capability", "card_id", "prompt", "function_tex", "unit", "radian_sensitive", "desmos_url", "served_at"}` |
| POST /calculator/drills/{drill_id}/answer | `{"value": str, "setup_mathjson": any or null, "elapsed_ms": int, "desmos_open": bool}` | `{"drill_id", "value": {"correct", "reason", "rounded", "truncated"}, "setup": {"shown", "correct", "reason", "key_latex"}, "elapsed_ms", "budget_seconds": {"I-B": float, "II-A": float}}`; 404 unknown drill, 409 already answered, 422 bad body |
| GET /calculator/measured | | `{"capabilities": [{"capability", "served", "answered", "value_correct": {"numerator", "denominator", "value"}, "setup_shown": {...}, "setup_correct": {...}, "median_ms": int or null}], "budget_seconds": {"I-B": float, "II-A": float}, "recent": [{"drill_id", "capability", "function_tex", "value_correct", "setup_correct", "setup_shown", "elapsed_ms", "submitted_at"}]}` with `recent` the last 20 answered, newest first, and `median_ms` null under 3 answered |

`budget_seconds` values are `PartShape.budget_seconds_per_question` from app/assessment/shape.py for the two calculator parts, never literals. `desmos_url` is `app/calculator/service.py: DESMOS_COLLEGE_BOARD_URL = "https://www.desmos.com/testing/collegeboard/graphing"`, and the client's `DESMOS_URL` in DesmosPanel.tsx becomes the same string (the server value is recorded per drill so a later change is visible in the data).

## Slice 1a. Drill engine [inferred]

Files: app/calculator/__init__.py, kit.py, check.py, registry.py, templates/__init__.py and twelve template modules, two per capability (integral: a rate integrated over an interval with a trigonometric or exponential factor, and an average value; derivative: a model function at a point, and a velocity component's rate; zero: an x-intercept of a transcendental function, and f(x)=k; intersection: two curves whose intersection bounds a definite integral, and the intersection x-value itself; value: a function at a non-integer point, and an initial value plus an integral to a stated time; plot: an extreme value inside a stated window, and a window that exposes an interior zero, both answered by the value read from the point of interest). Tests: tests/calculator/test_check.py (rounded, truncated, short, long, wrong, blank, non-numeric, negative, integer-valued keys; equivalent forms, proportional equations, missing, unsupported, unsettled by a bounded stub), tests/calculator/test_templates.py (every template: 50 seeded draws, key with three nonzero decimals and rounded differs from truncated, exclusions hold, setup_key accepted by to_sympy, prompt has no dash and no released-stem phrase), tests/calculator/test_registry.py.

Checks: `timeout 120 .venv/bin/python -m pytest tests/calculator/test_check.py`, the same for the other two files, each in its own process.

Acceptance: every template builds under its seed sequence; the check verdicts match the rules in architecture.md; no import of app/engine, app/session or app/progress from the package.

## Slice 1b. Cards and checker [inferred]

Files: schemas/calculator/card.schema.json; content/calculator/cards/CCD-*.json, the ten cards of design.md; content/calculator/templates.json; tools/check_calculator.py; tests/tools/test_check_calculator.py with red fixtures under tests/fixtures/calculator/. Every card fact cited `doc:page` with an anchor quote of at most 25 words found on that cached page; the exam habit copies the reader's words from data/errors.json records by id in `error_ids` and the checker compares.

Checks: `python3 tools/check_calculator.py content/calculator` exit 0 (with `--no-templates` until slice 1a lands, then without); `timeout 120 .venv/bin/python -m pytest tests/tools/test_check_calculator.py`.

Acceptance: the cards clean (nine, after "Define f(x) once" and "Evaluate at a point" merged into CCD-value-01 so every drilled card has a template); every lint has a red fixture; the checker refuses a card with a dash, a praise word, a library id in student text, a quote not on its page, an unknown template or an unknown error id.

## Slice 2. Storage, service, routes, measured [inferred]

Files: app/db/models.py (`CalculatorDrill`), app/calculator/service.py (serve, answer, measured; writes `calculator_drills` and `audit_log` only), app/api/routes/calculator.py, app/api/app.py (registration), app/audit/vocabulary.py (`calculator_drill_served`, `calculator_drill_answered`), app/progress/calculator_fluency.py (the measured computation, using learning_metrics.value for the ratios), tests/db/test_models.py and tests/export/test_export.py table sets, tests/api/test_calculator_routes.py, tests/calculator/test_invariants.py (C0 as a hypothesis property over random sequences of serve and answer against a world fixture: skills_state, attempts, sessions unchanged), tests/session/test_purge.py and tests/export/test_export.py additions (a drill row is exported and purged).

Checks: the five pytest files each in its own process under `timeout 300`; `timeout 120 .venv/bin/python -m pytest tests/api/test_security_headers.py` (unchanged CSP still green).

Acceptance: a drill can be served and answered once; the verdicts and budgets come back as the contract says; measured says null median under 3; skills_state is byte-identical before and after; export contains the row; purge removes it.

## Slice 3. Web [inferred]

Files: app/web/src/routing.ts (`calculator` place with `section` and optional `cardId` and `capability`), app/web/src/shell/TopBar.tsx (Calculator tab, graph icon), app/web/src/App.tsx (lazy route, PlaceView case, UNSUPPLIED_INPUTS), app/web/src/App.test.tsx (BAR_LABELS, BAR_DESTINATIONS), app/web/vite.config.ts (`/calculator` in API_PATHS), app/web/src/api/client.ts and types.ts (readCalculatorCards, readCalculatorCard, startCalculatorDrill, answerCalculatorDrill, readCalculatorMeasured), app/web/src/calculator/ (CalculatorRoute.tsx, ProcedureCard.tsx, CapabilityChooser.tsx, DrillScreen.tsx, DrillClock.tsx, MeasuredView.tsx, CalculatorLink.tsx, words.ts, and their tests), app/web/src/input/DesmosPanel.tsx (`DESMOS_URL` to the College Board version, `DESMOS_OPENS_IN`, an `openByDefault` prop, the offline sentence from design.md), app/web/src/session/Item.tsx (CalculatorLink on calculator items), app/web/src/assessment/ (the link on the calculator part's setup screen, never inside a running part), app/web/src/lessons/LessonSection.tsx (the link after a worked example whose archetype is a calculator archetype; the lesson payload's section already carries `archetype_id`, and the archetype's calculator status is read from the content the client already loads or a field added to the lesson payload by slice 2 if none exists), app/web/src/app.css additions with tokens only, app/web/src/progress/PaceStatement.tsx or ProgressRoute.tsx (the one text link to Calculator).

Checks: `npm --prefix app/web run test`, `npm --prefix app/web run build`, the reduced-motion gate, and the client path test against the slice 2 routes.

Acceptance: the destination is reachable from the bar and by hash; a card renders from a mocked client with its steps and demonstration; the drill submits value, setup and elapsed time and shows the three verdict lines and both accepted forms; the measured view says "not measured yet" under three drills; keyboard-only through a drill; the link appears on a calculator item and not on a no-calculator item; the frame URL is the College Board version; no literal values in CSS; the bar test lists six labels.

## Slice 4. Verification in the app and the record [inferred]

Stage D of the operator's brief: servers from .claude/launch.json, the walk as the student, screenshots under var/calculator/, skills_state queried before and after, console, network and server logs read. Stage E: the ledger entry, research/PROGRESS.md, docs/calculator/HANDOFF.md, commit.

## Plan amendments made [inferred]

Appended on 2026-09-29 as dated sections: docs/plan/05-assessment-modes.md "Calculator fluency" (the mode, which Desmos, pacing, the rejected alternative); docs/plan/08-design-brief.md "Calculator destination and the Desmos frame" (the sixth destination, the fixed frame, the terms ruling); docs/plan/09-security-and-privacy.md (the `calculator_drills` retention row, the CSP unchanged, the API not adopted, the terms); docs/plan/11-phased-delivery.md P5 scope item 3 (the real Desmos on calculator parts and the fluency feature as a P5 addendum); docs/plan/12-open-questions.md (the Desmos question restated as settled for the variant, the inference for the capabilities, the new open items, two rulings for the operator).

## Rulings waiting on the operator [inferred]

1. Framing Desmos against the desmos.com terms: seek consent, keep the frame for private single-user use, or flip `DESMOS_OPENS_IN` to `"window"`.
2. The embedded Desmos API: obtain a Trial Tier key and allow `script-src https://www.desmos.com`, or leave the outcome-checking design as built.
3. Re-fetch the approved calculator list and the College Board Desmos PDF in spring 2027.
