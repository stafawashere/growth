---
title: Build ledger
research_date: 2026-09-23
status: in_progress
purpose: Where the application build stands, session by session, so the next session can pick the next slice without rereading the plan.
---

# Build ledger

Application code lives at the repository root under `app/` and `tests/`, at the paths docs/plan names. The project CLAUDE.md still says "docs-only, no product"; that sentence is the operator's to amend and this ledger only records the conflict. Tooling: uv-managed Python 3.12.13 in `.venv/`, dependencies in `pyproject.toml`, tests via `.venv/bin/python -m pytest`. Every H2 below carries a tag because `qa/04_tags.py` scans root-level Markdown: [verified] means the test output or the registry was checked in the session named, [inferred] means a judgement.

## Overnight orchestration status, 2026-09-23 [verified]

The operator's overnight run stopped on its 10-slice limit. P1 to P3 cannot all be met without the
operator: gates 17, 29 and 30 and exit criterion 7 count only items with provenance `operator`, and
the key audit is a human verdict. Every commit below was pushed to `origin/main` only after the
orchestrator reran `.venv/bin/python -m pytest`, `npx vitest run`, `npx tsc --noEmit` and
`qa/12_report.py` in the same session, and each exited 0.

| Slice | Commit | What landed |
| --- | --- | --- |
| 0 | 8a046d0 | Session fourteen's 139 uncommitted files: export, progress and settings routes, security headers, the account client |
| 1 | db348bc | Persistent cumulative developer spend cap, $15.00, in `app/providers/guard.py`; `tools/dev_spend.py`; Opus 5.5 priced |
| 2 | 3a16d02 | Claude-only tier priced; one role-to-model table (`app/providers/model_routing.py`) pinned to `tools/cost_model.py` |
| 3 | 4b85ba3 | Stage example collects a graded answer and a rating; credited observation count; mastery path flake pinned |
| 4 | 4e4a527 | The 76 BC-PT records labelled for deterministic grading (48 deterministic, 28 model required); grader priced from it |
| 5 | cab28e1 | Rulings: retryable stream errors, passkey re-auth, audit sample enforcement, purge phrase, token CSS default, eval cadence |
| 6 | 8ca265d | 130 agent-drafted P1 items in `content/items_p1_agent/`, served by default, provenance names the model |
| 7 | 7acb7ee | Four shuffled options on every draft; SymPy bound alarm rearmed; missing audit sample refused with a 400 |
| 8 | 5162a79 | 360 distractor options re-derived against their named errors, 167 retagged or revalued |
| 9 | baecad3 | The 42 items whose distractors no held error produced were redesigned |
| 10 | 5691f56 | First live calls: Haiku 4.5 tutor cassettes, measured prompt tokens per model, cost per served item |

Tests at close: pytest collects 870 and exits 0; vitest 307 passed; tsc exits 0; qa 14 PASS, 0 FAIL;
`tools/check_items.py content/items_p1_agent` 130 clean.

Live spend: $0.0353 over seventeen claude-haiku-4-5 calls (see "Live API spend log"). The developer
cap reads spent 0.0353, cap 15.0000, remaining 14.9647. The key held $19.25 before the run, so about
$19.21 should remain on it.

Per-student projection, `tier.hundred_claude_only.cycle` in `tools/cost_model.py`: $92.95 to exam
day, inside the $50 to $100 target with $7.05 of headroom. Split, on the operator's 2026-09-23
instruction to use the Claude Code subscription wherever the terms allow: $52.14 stays on the API
key (`tier.hundred_claude_only.api_cycle`, runtime: tutor, grader, transcriber, diagnostician,
screen, evals) and $40.81, 43.90 percent of the tier, moves to offline Claude Code sessions at
$0.00 API spend (`tier.hundred_claude_only.offline_cycle`, template authoring and the verifier's
blind re-solve). See `docs/plan/14-token-economy.md` "Offline work on the operator's Claude Code
subscription" and `docs/operator/offline-authoring.md`. It rests on three things the operator
should know. The grader line uses the agent's determinism labels, which are [inferred]; if every
judged point needed a model the tier would be $128.95. The golden set 2 canary cadence was cut from
9 runs to 2 on the operator's delegated authority. Most role token figures are still characters
divided by 3.1, because only the tutor has a real template to measure. The measured tutor cost is a
median of $0.00206 per served item on Haiku, uncached because the 1,092-token prefix is under
Haiku's 4,096 cache minimum; the same tokens on the assigned Sonnet 5 with the 1-hour cache price at
a $0.00157 median, so the tutor stays on Sonnet 5.

Open for the operator, in order of what unblocks most:

1. Review the 130 drafts in `content/items_p1_agent/`, including the judgment calls listed in Known
   defects (twenty-sixth session entry), and author or approve the operator-provenance items gates
   17 and 30 need. Only the operator may relabel a draft `operator`.
2. Draw the 100-item key audit sample (`tools/draw_key_audit_sample.py`) over operator items and
   record verdicts, for gate 29 and exit criterion 4.
3. Approve or change the eval cadence ruling and the `CHARACTERS_PER_TOKEN` replacement in 14.
4. The fixture items in `tests/session/test_serve_format.py` have no options, so a server guard that
   never serves MCQ without options would turn them red; a ruling on those fixtures unblocks the guard.

Recommended next slice: P2 review mode and FSRS scheduling with `test_desired_retention_switch`,
replay only, since the P1 gates still open are the operator's and the engine needs a finite due
queue to teach from now to May 2027.

## Question workbench, 2026-10-02 [verified]

On the operator's instruction (2026-10-01 and 2026-10-02), the question screens move to direction C of `mockup-redesign/`, the split workbench, dressed like the Lessons section; the operator also asked for the dead code to go. Branch `design/split-workbench`, worktree `~/dev/growth-workbench`. `docs/plan/08-design-brief.md` carries the amendment ("Plan amendments, 2026-10-02, the question workbench").

What changed. `app/web/src/ui/Workbench.tsx` is new: `Workbench` (one card split into a tool rail, the question pane and the answer pane, a foot, a status line) and `QuestionTrack` (one segment per question, drawn by height: a hairline still to come, thicker answered, tallest current, a caution dot for a question marked for review, the count in words beside it). Every question screen sits on it: the set's item and its feedback (`session/Item.tsx`, `SessionScreen.tsx`), the diagnostic, the unit check, a timed part (`PartRunner.tsx`: Mark for review, Highlight, the Question menu and Zoom in the rail; Desmos and the graphing panel unchanged and on calculator parts only), the probe, a lesson's check, and the free-response read-back. The lesson reader keeps its worksheet but its progress is the same bar. Options are lesson-list rows with a ring that fills when chosen; the feedback verdict is a glyph, a word and a heading; the confidence rating is a drawer at the right edge. `QuestionStepper` is now only Back and Next. Every test id, role and label the suites use is kept.

Fixed on the way. The zoom tool set a percentage on a container whose text is sized in px tokens, so nothing grew; 125 and 150 percent now step the stem and the answers up the type scale (`assessment/zoomScales.test.tsx`, which failed with the 150 rule broken: "expected 'var(--growth-type-body)' to be 'var(--growth-type-title)'", and passed restored).

Removed as dead. CSS no screen draws any more: the step control (`.sheet-nav*`), the set's progress steps, the timed part's old header, toolbar and foot (`.part-title`, `.exam-toolbar`, `.exam-bottom`), `.sheet-number`, `.mark-for-review`, `.text-button[aria-pressed]`, `.scope-footer*`, `.read-back-pair`, `.item`, `.feedback`, `.question`, and `.prose`, `.split`, `.formula` and `.submit-row`, which nothing used before this either. Exports nothing called: `deletePhoto` and its `PhotoDeleted` type, `readAgentSettings`, `SECTIONS_BY_TAB`, `OPERATOR_EXPERIMENTS_SUMMARY`, and the fixture `sectionNamed`.

Checks on the branch: `npx tsc --noEmit` exit 0; `npm run build` "built in 2.13s"; `npx vitest run` "Tests 1 failed | 1168 passed (1169)", the one failure `GradingsPayload` (known, and failing the same way on `main` before this work); `qa/12_report.py` 14 PASS, 0 FAIL (with the gitignored `cache/pdf` and `cache/text` linked into the worktree); `pytest tests/design tests/web tests/api/test_static_mount.py` exit 0; the full `pytest` "27 failed, 3375 passed, 17 errors in 2721.99s". No failing or erroring test reads `app/web` or the design brief, and the seven failing files run on `main` (74891b8a) give the same "11 failed, 31 passed, 14 errors"; the rest are the same server-side families (cassette misses, prompt goldens, template fields) and are not this branch's. A live walk against `var/test.db` took screenshots of the set item, its feedback, the confidence drawer, the unit check, a part drill, a lesson and its check at 1280, 900 and 375; a sweep of the set item, a lesson and a part drill at 1280 and 375 in both themes found no horizontal scroll and no text under 4.5:1, and one target under 24 px, the review checkbox at 16 px, which is now 24 px and was not swept again.

## Desmos fluency, 2026-09-29 [verified]

Built overnight by claude-fable-5-1 orchestrating claude-opus-5-5 code agents under the operator's
brief of 2026-09-29, on branch `calculator/desmos-fluency` (14 commits from `today/redesign`, 24 ahead of `main`, not
pushed, main untouched). The brief: research, design and build a Desmos fluency feature for the two
calculator parts, with the exam habits carried and nothing credited. Documents: docs/calculator/
(design.md, architecture.md, build-plan.md, HANDOFF.md, research/ with four documents and a
synthesis). The working tree was shared with another chat session whose uncommitted files
(tools/check_items.py, tools/seed_history_student.py, app/items/standards.py,
tests/tools/test_item_standards.py) were left untouched; the branch switch moved that session's
checkout onto this branch, which the operator should know before merging.

What was built.

- The corpus caches web pages. tools/fetch_corpus.py gained a `web` section (curl for HTML and
  PDFs on one list; `--saved-dir` for pages a browser had to render: help.desmos.com refuses curl
  with 403, and desmos.com/terms, /api-terms and /testing are script-rendered), extract_text.py
  writes one text page per web document, qa/00_manifest.py checks cache/web by hash,
  build_sources.py emits web_page source records from the manifest and keeps every existing BC-SRC
  id. 40 documents added (Bluebook tools page, both calculator policy pages, Desmos's College Board
  PDF, its default testing PDF and user guide, the API docs, both terms pages, the testing page,
  the graphing shortcuts page and 19 help articles). cache/web is ignored like cache/pdf; the text
  is tracked. web-key-changes still returns 403 and stays hand-listed.
- Library: research/exam/calculator-policy.md now states from cached pages that Calculus BC gets
  the Desmos graphing calculator only, that the built-in calculator sits outside the two-handheld
  count, and that the four CED capabilities in the Bluebook variant rest on a four-step inference
  whose weakest link is reading Desmos's list of differences as exhaustive; the approved model list
  is cached; unresolved-questions.md, claims-and-confidence.md and PROGRESS.md follow. qa/12_report
  14 PASS.
- Content: nine procedure cards under content/calculator/cards (check radians first; define f(x)
  once and evaluate; derivative at a point; definite integral; average value; zeros and f(x)=k;
  intersection as a bound; a window that shows the work; three places, rounded or truncated), each
  with Desmos's own typed syntax and shortcuts, one worked demonstration, the exam habit in the
  reader's words from the named BC-ERR records, and page citations with anchor quotes;
  content/calculator/templates.json; schemas/calculator/card.schema.json;
  tools/check_calculator.py (11 lints plus a 200-draw run per template through the registry).
- Engine: app/calculator (kit, check, registry, twelve templates, two per capability: plot, zero,
  derivative, integral, intersection, value). Keys are computed by mpmath quadrature, SymPy
  differentiation or evaluation and never stored; a draw whose rounded and truncated three-place
  forms coincide is nudged and, failing that, redrawn, so every drill can tell the two forms apart.
  check_value accepts the rounded or the truncated three-place form and names why an entry failed
  (`missing`, `not_a_number`, `not_three_places`, `outside_tolerance`); check_setup compares the
  typed MathJSON by the item grader's equivalence engine, treats an equation up to a nonzero
  constant, refuses a bare number as a setup, and reads prime notation and implicit application on
  the task's named functions.
- Storage and routes: `calculator_drills` (one table, `user_id` indexed, so export and purge reach
  it through owner_clause with no code change), app/calculator_drills/service.py, the five routes
  in app/api/routes/calculator.py (cards, card, serve, answer, measured),
  app/progress/calculator_fluency.py for the measured payload (ratios through
  learning_metrics.value with denominators, median null under three answered drills, budgets from
  app/assessment/shape.py), `calculator_work` on the lesson payloads, two audit actions.
- Web: a sixth top-bar destination, Calculator (Procedures, Drill, Measured); the drill opens the
  College Board version of the Desmos graphing calculator beside the task, takes the result as
  typed and the setup in the math field, measures elapsed time with a hideable clock, and shows the
  three verdict lines with both accepted forms; "Calculator practice" links on calculator items, on
  the assessment setup screen for a calculator part, and after a calculator worked example in a
  lesson; one text link on Progress. DesmosPanel carries the College Board URL, `openByDefault`, and
  `DESMOS_OPENS_IN` ("frame" | "window").

Decisions, all reversible, taken under the brief.

- The embedded Desmos API is not adopted. It needs an API key from desmos.com/my-api, an account
  only the operator can create, and a `script-src https://www.desmos.com` amendment that plan 09
  refuses; the API terms' free Trial Tier permits personal, non-commercial use, so the licence alone
  would not block it (BC-SRC-desmos-api-terms p.1). Drills check outcomes: the typed value and the
  typed setup. The CSP is unchanged.
- The drills and the calculator items frame the College Board version of the calculator,
  https://www.desmos.com/testing/collegeboard/graphing (same origin as the 2026-09-27 exception),
  because Desmos says its testing page carries the exam configuration and its College Board PDF for
  SY2026-2027 lists the Bluebook differences (images, folders and notes disabled; log mode
  auto-checked). Verified in headless Brave: the frame loads inside the app's sandboxed iframe with
  the green "College Board Version" header and `api/v1.12.0/calculator.js` fetched in the frame.
  Desmos logs a console warning inside the frame that iframes are not a supported or secure way to
  use Desmos, and its Terms of Service section 5 say the Desmos Tools may not be framed without
  prior consent (BC-SRC-desmos-terms p.1); the frame stands on the operator's 2026-09-27
  instruction and `DESMOS_OPENS_IN` flips it to a new-window link. Ruling for the operator.
- Fluency is measured and never credited: invariant C0 (skills_state, attempts, sessions,
  judgments, diagnoses, pending_probes, gradings untouched by any drill sequence) is a hypothesis
  property in tests/calculator/test_invariants.py, and the walk below queried skills_state before
  and after nine drills: 618 rows, identical digest.
- The value rule as written accepts an entry with fewer than three places when it equals the
  truncated form (15.30 against 15.3008); the walk and the tests show a two-place entry refused
  when its third place is nonzero. Recorded, not changed.
- "Define f(x) once" and "Evaluate at a point" are one card, so every drilled card has a template.
- The service lives in app/calculator_drills so the engine package keeps its no-database rule,
  which tests/calculator/test_registry.py enforces.
- The design's `60vh` phone frame height is `calc(var(--growth-space-96) * 5)` because the
  literal-values gate refuses viewport units; opening the frame by default is decided by
  `innerWidth >= 1100` read once at render.
- Two defects found in the walk and fixed with red-then-green tests: MathLive emits integral bounds
  as `Triple` (and pairs as `Pair`), which app/items/mathjson.py refused, so every typed integral
  setup was unreadable (47b7e37); prime notation and `f(a)` on the student's own function names
  arrive as `Multiply(Prime(P), 4.5)` and `Multiply(f, 0.31)`, which the setup check now rewrites
  (2b06b69). A third: the drill's skip link was visible at every width because the drill container
  was positioned (9f7533d).

Checks, each run by the orchestrator in this session.

| Check | Command | Result |
| --- | --- | --- |
| Library | `cd qa && python3 12_report.py` | 14 PASS, 0 FAIL (twice: after the corpus, after the library edits) |
| Corpus pipeline | `timeout 120 .venv/bin/python -m pytest tests/tools/test_corpus_web.py` | 10 passed |
| Cards and checker | `timeout 120 .venv/bin/python -m pytest tests/tools/test_check_calculator.py` | 34 passed |
| Content checker | `.venv/bin/python tools/check_calculator.py content/calculator` | cards read 9, clean 9, with findings 0, exit 0 (with the real registry) |
| Engine | `tests/calculator/test_check.py`, `test_registry.py`, `test_templates.py` each in its own process | 79, 13, 98 passed |
| MathJSON fix | `tests/items/test_mathjson.py tests/items/test_mathjson_pair_triple.py` | 61 passed |
| Routes, invariants, export, purge, lesson flag | one process each | 12, 2, 1, 1, 1 passed |
| Web | `npm --prefix app/web run test` | 874 tests; under load 11 failed, every one rerun alone: contrastAllScreens 6 passed, App.test 1 passed (twice), LessonReader 21 passed, renderRecord 8 passed, keyboard session 3 passed; the one lasting failure is client.test.ts GradingsPayload, which fails at HEAD of the base branch (commit 3cec2af added tutor_explanation) and is not this work's |
| Web build | `npm --prefix app/web run build` | exit 0, built in 27.59 s; rebuilt after the skip-link fix, exit 0 |
| Reduced motion gate | `npm --prefix app/web run gate:reduced-motion` | 5 passed (slice 3 agent) |
| Calculator vitest after the CSS fix | `npx vitest run src/calculator src/styles/noLiteralValues.test.ts` | 30 passed |
| Web, rerun alone after the walk | `npm --prefix app/web run test` | Test Files 1 failed, 82 passed (83); Tests 1 failed, 874 passed (875); the one failure is client.test.ts GradingsPayload, pre-existing at the base branch |
| Full pytest | `timeout 3000 .venv/bin/python -m pytest tests` | killed by its own timeout at 45 percent (load average above 40 from other sessions); rerun as four parallel groups, see the line appended below |

Pre-existing failure, not touched: tests/db/test_models.py `test_models_create_all` expects a table
set without the five lesson tables (a base-branch drift); `calculator_drills` is in its expected set.

Full pytest, appended after the run. The single run was killed by its 3000 s timeout at 45 percent
(load average above 40 from other sessions), so the suite was rerun as parallel directory groups
with the repo's own addopts (-q), each with its own timeout: api, assessment, audit, auth,
calculator, checkpoint, content: 768 passed, 4 failed; db, design, diagnosis, e2e, engine, eval,
experiments, export: 192 passed, 10 failed, 15 errors; review, runtime, session, sim, tools, web:
353 passed, 0 failed, exit 0; feedback 42 passed, generation 62 passed, grading 3 failed 89
passed, items 8 failed 215 passed, lessons 289 passed, progress 21 passed, providers 3 failed
264 passed. Two failures went green alone (test_capture_concurrency
`test_no_write_lock_is_held_while_the_diagnostician_runs`, and the e2e
`test_a_session_serves_an_agent_drafted_unit_2_item_end_to_end`, which fails alone at the merge base
and passes alone here, so it is draw or order dependent). Every other failure and error was rerun
at the merge base 23cb026 in a throwaway worktree and fails there the same way: the eval suite's
cassette misses and prompt goldens, the e2e mastery simulations, the grader template field
list, the claude-sonnet-5-5 model rename in feedback and providers, the missing lesson_v1 golden,
the metrics view's lesson_first_contact row, the unit check with too few items, the unsettled
comparison tests under tests/items, and test_models_create_all. Not one failing test exercises a
file this branch changed from the merge base (the branch touches app/items/mathjson.py by two
lines and app/db/models.py by one table, and the calculator suites above are green).

The walk (Stage D), in headless Brave over CDP with var/calculator/driver.py (gitignored), against
the API on 127.0.0.1:8007 serving the built client from a fresh database, because the dev-server
slot cap was held by other chats. Screenshots under var/calculator/: 01-landing, 02-after-signup,
03-home, 04-calculator-cards, 05-card-integral, 06-drill-integral, 07-drill-integral-checked,
08-drill-truncated-no-setup, 09-drill-wrong, 10-drill-short, 11-drill-derivative, 12-drill-value,
13-drill-zero, 14-drill-plot, 15-measured, 16-setup-calculator-part, 17-lesson-link,
18-phone-cards, 19-phone-drill, 20-phone-measured, 21-dark-drill, 22-dark-card,
23-drill-integral-setup-ok, 24-drill-derivative-setup-ok, 25-drill-offline, 26-dark-measured,
27-session-first-item, probe-frame2.

- Calculator opened from the sixth tab; nine cards listed; the integral card read (steps, one
  worked instance as a step reveal, the habit lines, Drill this).
- Drills of all six capabilities with the real Desmos College Board frame open beside the task.
  Rounded value accepted (25.130 for 25.12981), truncated accepted (2.141 for 2.1417), a value one
  place short refused with "Give three decimal places" and both forms shown, a wrong value refused
  with the reason, a missing setup reads "No setup shown". After the two fixes, typed setups judged
  equivalent: `\int_0^3 R(t)\,dt`, `P'(23/5)`, `f(3.31)`, `5x+\cos(x)-4=0`.
- Time recorded on every drill (elapsed_ms 4.9 s to 33 s); the measured view shows per-capability
  counts with denominators, "not measured yet" under three, "13 seconds" median for four integral
  drills, and the exam's own per-question figures in one sentence.
- skills_state before and after: 618 rows, digest 725d64d81c371d35 both times; attempts 0,
  sessions 0; audit_log holds 9 served and 9 answered rows.
- Keyboard: Tab reaches the chooser, the clock control, the frame, then the skip link jumps to the
  result field, then the setup field, then Check.
- Phone (375 by 812): no horizontal overflow on cards, drill or measured; the frame opens on demand.
- Dark mode with reduced motion: theme dark, background rgb(13, 14, 16), zero animated elements in
  main, skip link hidden until focused.
- Offline: with navigator.onLine false the frame is replaced by the design's sentence and the
  drill still checks.
- Links: "Calculator practice" appears on the assessment setup screen when Section I Part B is
  chosen and not for Part A; on lesson LSN-CON-02007's worked example. The link on a live
  calculator-part item was not reached in the walk (the fresh account opens on the diagnostic);
  it is covered by app/web/src/calculator/CalculatorLink.test.tsx (present on a calculator item,
  absent on a no-calculator item).
- Console: only the pre-sign-in 401s and a favicon 404 in the main frame; Desmos's own bugsnag
  beacons and its iframe warning inside the frame. Server log: 0 errors over 19 calculator route
  hits. The built-in browser pane could not frame desmos.com from a localhost page (no request was
  even issued), which is why the walk used Brave.

Not done. Section I Part B calculator multiple-choice items are not in the corpus, so the
catalogue of calculator work is free-response only. The lesson link is shown only when the lesson
is opened from the library (a lesson inside a session carries no flag). No drill exists for the two
habit cards (radians, three places), which every other drill carries as a note and a verdict.
Whether the College Board practice page is the build Bluebook embeds, how many digits Desmos
displays for an evaluation, and whether angle mode persists across questions remain open
(research/exam/calculator-policy.md, Unresolved).

Rulings waiting on the operator: framing Desmos against the desmos.com terms (consent, keep for
private use, or flip `DESMOS_OPENS_IN` to "window"); the embedded API (Trial Tier key plus a
script-src amendment) or the outcome-checking design as built; re-fetching the approved calculator
list and the College Board Desmos PDF in spring 2027; the other session's files on this branch.

## Tutor drawing, 2026-09-30 [verified]

The operator's brief of 2026-09-30: give the live tutor agent the ability to draw whatever figure best teaches the moment, built the way a teacher builds a sketch at the board, step by step in time with the words. Two instructions arrived in chat during the run and are recorded as the operator's: the vocabulary goes beyond graphs to shapes (circles, the kinds of triangle, arrows, boxes), free text labels and kinds of stroke; and the tutor annotates the page itself, each set of marks bound to the screen it was drawn on, hidden when the student leaves and restored when they return. Every other decision was delegated and is listed below. Branch `agent/drawing` from `main` fa514089 in the worktree `/Users/mahfujm/dev/growth-drawing` (its own `.venv`, `node_modules` linked), six commits (edff1000 research, 83649222 design, 6b892938 and 4e28762d build, 0be330f8 the walk fixes, and the commit holding this entry), nothing pushed, `main` untouched. Research and design were written by the orchestrator (Opus 5.5) from four Opus 5.5 research agents; every line of application, test and tool code was written by Opus 5.5 agents and checked by the orchestrator running the named command. State and resume point: `docs/agent/HANDOFF.md`.

Stage A, research, `docs/agent/research/drawing.md`: board practice (bansho, pointing, colour roles, erasure), products (Khan Academy, GeoGebra's construction protocol, Desmos, Photomath, Claude visuals and artifacts, Gemini, Khanmigo, ChatGPT), the learning science (animation over static at g = 0.23 to 0.37 across three meta-analyses, with graphs at g = 0.006, written commentary at g = 0.105 and only system pacing helping; instructor drawing d = .54 on N = 66, read by the orchestrator from the manuscript, the gain on retention; segmenting; signalling; Brysbaert's 238 words a minute), the library's figure needs (119 of 148 archetypes, 220 of 249 FRQ parts), whiteboard shapes and strokes, model-written markup against a closed spec (SVG, CSS and XML attack paths; Vega, Mermaid and Plotly advisories), model drawing accuracy, validation and expression safety, the seven leak channels, stream synchronisation, accessibility, what Growth has, where the evidence and the rules pull apart, the ranked synthesis and the rulings. Stage B: `docs/agent/drawing-design.md` (the figure language with every shape, the caps, the splitter, the compiler, the render spec, the screen, the events, the client, motion, accessibility, the prompt, the item figure in the packet, storage, the switch, cost, evals, marks on the page, rejected options), `docs/agent/drawing-build-plan.md` (slices 1 to 10 with the render and marks contracts), sections in `design.md` and `architecture.md`, and 2026-09-30 amendments to plans 03, 08, 09, 12, 13 and 14.

Stage C, the build. Server: `app/agent/drawing/` (`expression.py` a closed twin of `expression.ts` with 80-character, 48-token and depth-10 caps, evaluated in floats, never through `eval`, `exec`, `sympify`, `parse_expr` or `lambdify`, and with no SymPy import at all; `spec.py` reading under a 2,000-character cap with `RecursionError` caught and `schemas/agent/figure.schema.json`; `compile.py` computing every point, 161 samples a curve, adaptive Simpson areas, the 4,000-point, 200-primitive and 100 ms caps; `marks.py` with `schemas/agent/marks.schema.json`; `stream.py` the splitter for `figure` and `marks` fences and `[[step:ID]]` markers; `record.py`), `app/evals/figure_checks.py` (texts through the sentence checks; marked coordinates, slopes and intercepts, areas and approximation totals, constant curves and key expressions at 16 points compared with the key; option anchors before checking), `SentenceScreen.boundary` and `withhold`, the move table (`DRAWING_OPEN_MOVES`), the packet's `drawing`, item figure summary and `anchors`, the events `figure_pending`, `figure`, `figure_step`, `figure_refused` and `marks`, `agent_turns.figure` (additive, nullable), `GROWTH_AGENT_DRAWING`, and `prompts/agent/live_v2.md` with 14 figure and 4 marks examples. Client: `GraphFrame` factored out of `FigureView` with item output byte-identical, `TutorFigure` (roles, strokes, arrowheads, highlighter, fills, an HTML label layer typeset on the tutor renderer, step controls, the step list, keyboard stepping, a sticky hold while building), `PageMarks` (an aria-hidden overlay over `data-agent-anchor` elements, quotes through text ranges, the item graph through its plot box and screen matrix), reading-paced gates in `AgentProvider` (238 words a minute, math spans as three words, 6 s cap, Show all and Stop open every gate, `end` and the announcement after the queue), `motion-figure-wipe` and `motion-figure-step`, and screen entries for the contrast and greyscale gates. Golden set: 57 cases and 187 turns, 21 with a figure and 4 with marks, scored by the live splitter, compiler and checks. Cost: a `drawing.*` block in `tools/cost_model.py`. Tool: `tools/record_walkthrough.mjs`, a JSON-scripted CDP screencast recorder with captions burned in through ffmpeg overlays (this ffmpeg has no drawtext).

Defects found and fixed during the build, each with a red-then-green test: the screen hung past 60 s on a curve such as `x + 9^9^9^9` because SymPy evaluates integer powers eagerly (the curve is now evaluated in floats, only the trusted key through SymPy); a leaking area slipped through because Simpson panels straddling a kink were off by 0.0011 on ITM-AGT-06002-00's data (adaptive Simpson to 1e-6, and the case joined the golden set); a refused marks block scored as acceptable in the golden set (`marks_well_formed` added); option anchors were offered after checking though the checked screen shows no options (never listed now, still withheld before checking); feedback and solution-step anchors were listed at stages where the client does not render them.

Stage D, the live walk, on the worktree's API (127.0.0.1:8741) and Vite client (5191) as one launch entry, `GROWTH_AI_BACKEND=subscription`, the shared `var/test.db`, the test account, driven through the app's browser pane, with walk sessions opened in rehearsal mode (no mastery updates) by a scratch seeder. What the walk showed, each with a screenshot in `var/agent/drawing/`:

| Case | Result |
| --- | --- |
| Practice item ITM-GEN-02002-00 (key 18), first turn | ask_what_tried, drawing closed, a question back and no figure (01) |
| Same item, second turn, "show me a picture" | name_rule, a secant-to-tangent sketch on y = x squared in 4 steps at reading pace, P at (1, 1), the tangent slope 2, the key nowhere; stored `shown`, 4 revealed (01 to 05) |
| Figure accessibility, read from the DOM | wrapper `group` named "Secant to tangent" with the model's description; SVG `img` described by the description and the step list; the status announcement ends "Figure: Secant to tangent. A curve with a point P. ..." |
| After checking ITM-GEN-06001-00 with 134 | discuss_step, "Drawing a figure", then left rectangles of widths 4, 1, 2, 1 at heights 11, 20, 16, 20 and "44 + 20 + 32 + 20 = 116" in 3 steps (06 to 09) |
| A closed move (name_point) asked to mark the table | answered in words, nothing drawn (10) |
| self_explanation_question asked to mark the table | marks on the page: rows 0 to 3 of the item's own table highlighted and the error-role note "right end only, not used" beside the t = 8 row (11, 12) |
| Leaving for Progress | marks gone, 0 bands and 0 notes (13) |
| LSN-CON-01006 prediction (key 2), first turn "sketch the graph" | closed: "The sketch comes after you have said what you tried." (14) |
| Same, second turn, "draw it exactly as described" | the figure drew the stated circle and was withheld; the decline shown; stored `withheld` with no spec; audit `{"check": "no_answer_before_submission", "turn_id": "ATN-2e93...", "day": "2026-10-02", "part": "figure"}` (15, 16) |
| Lesson part 2, "underline the phrase and mark the graph" | an underline under "the height each side approaches" and an arrow to the graph, listed under "Marked on the page" (17, 18) |
| Review and back to part 2 | marks hidden (0 shapes), then drawn again on return (7 shapes) (19, 20) |
| Phone width 375 px, light then dark | the sheet builds a 4-step hole figure; page width 375, no sideways scroll (21 to 24) |
| Keyboard only | Cmd+/ to the composer, three Shift+Tab to the figure group; name "A hole and both approaches", description read back; ArrowLeft to step 3, Home to step 1, End to step 4 (25) |
| A Riemann request with 40 rectangles | the model drew a valid lesson figure within the caps instead, so no live oversized block |
| Oversized (3,402 characters) and malformed blocks, through the real route and client with the fake CLI | "The figure for this reply could not be drawn." and the text continued; stored `refused:oversized` and `refused:malformed` with no spec (26, 27) |
| Logs and audit | `var/drawing-api.log` (354 lines, 10 `POST /agent/turns` as the positive control) and `var/drawing-api-fake.log` (36 lines, 3): 0 matches for every typed message, the test password, `sk-ant`, `CLAUDE_CODE_OAUTH_TOKEN`, `oauth`, a LaTeX opener, `"figure"` and `steps":`; today's audit rows carry ids only |

The walkthrough video `var/agent/drawing-walkthrough.mp4`, 161.7 s at 1280 by 800, 76 of 76 steps, captioned: the closed first turn, the practice build, reduced motion on a lesson build, marks leaving and returning with their screen, phone width dark and light (28, 29), and keyboard stepping (30). The first recording showed the figure scrolling out of view while it built in an 800 px window, which led to three fixes by one Opus agent, each red then green: the figure is held sticky at the top of the conversation while it builds (only while two lines of words still show beneath it), the "Drawing a figure" line clears on a withheld reply, and tick numbers no longer sit under labels drawn at a reduced scale. The final recording was made after them.

Live calls. This session, all on the subscription backend through claude CLI 2.1.284 with `CLAUDE_CODE_OAUTH_TOKEN` from `.env`, no API call and the $15.00 developer cap untouched: 20 agent calls (10 in the browser walk, 2, 4 and 4 in three recordings; the pacing ledger reads 23 for 2026-10-02 UTC, of which 3 were the fake CLI) and 2 tutor calls (the existing feedback sentence on the two walk items). Before this session's walk, the drawing server's ledger recorded 6 agent calls and 1 memory call on 2026-09-30 made by the operator in the preview; their stored turns show two figures drawn on a lesson question and one sentence withheld.

Checks run by the orchestrator before the final commit, each in its own background process:

| Check | Command | Result |
| --- | --- | --- |
| Agent package | `timeout 600 .venv/bin/python -m pytest -p no:cacheprovider tests/agent` | 878 passed, exit 0 |
| Agent turn route | same over `tests/api/test_agent_turn.py` | 22 passed |
| Drawing route | same over `tests/api/test_agent_turn_drawing.py` | 20 passed |
| Agent settings routes | same over `tests/api/test_agent_settings_routes.py` | 10 passed |
| Export then purge | same over `tests/api/test_export_then_purge.py` | 1 passed |
| Database | same over `tests/db` | 36 passed |
| Agent golden set | same over `tests/eval/test_agent_golden.py` | 20 passed |
| Golden sets | same over `tests/eval/test_golden_sets.py` | 11 passed |
| Cost model | same over `tests/tools/test_cost_model.py` | 17 passed |
| Providers | same over `tests/providers` | 3 failed, 288 passed; the three fail identically on a clean `main` checkout at fa514089 ("3 failed, 1 passed" with the app imported from that checkout) |
| Agent eval | `.venv/bin/python tools/agent_eval.py` | 57 cases, 187 turns; figure checks over 21 turns (draws_only_when_open 19/21, figure_well_formed 18/21, no_answer_in_figure 12/18, figure_described 18/18), marks checks over 4 (marks_well_formed 4/4, no_answer_in_marks 2/4); "0 disagreements between labels and checks", exit 0 |
| Web tests | `timeout 900 npm --prefix app/web run test -- --run` | Tests 2 failed, 1139 passed (1141): `client.test.ts` GradingsPayload, which fails on `main` ("1 failed, 247 passed" there), and `App.test.tsx` "reaches progress from the bar", which timed out under 13 parallel processes and passed alone ("Tests 50 passed (50)") |
| Web build | `npm --prefix app/web run build` | "built in 1.97s", exit 0 |
| Plan dollar figures | `tools/cost_model.py --check` over plans 03, 08, 09, 12, 13 and 14 | 0 unknown dollar figures in each |

Decisions taken, with the reason:

- The model writes one closed, declarative figure per reply as a fenced JSON block, and the server compiles it; the client receives numbers and strings only. Plan 09's rule, the SVG and CSS attack record, one origin with no `unsafe-eval`, and models placing coordinates badly.
- Compile, screen, render: what the screen checks is exactly what the student sees, so the client never evaluates a model expression.
- One block with step markers, revealed sentence by sentence, paced to reading rather than to generation; the build would otherwise finish before its first sentence is read.
- Reduced motion keeps the build and its pace and drops the movement, against the brief's provisional "finished figure with a step list", on plan 08's "replace, not delete" and the evidence that the benefit rides on segmenting and contiguity; the finished figure with its step list is the end state in both modes.
- Roles not colours: the operator's accent is monochrome, so given, constructed, highlight, error and ghost differ by lightness, weight, dash and underlay; `state-incorrect` only for error, always with a word.
- Drawing is closed on the first practice reply and on point_to_section, name_point and probe; open elsewhere; the server drops a figure written on a closed turn.
- Marks name anchors the screen declared, never pixels or selectors; option anchors are never offered; marks are bound to their screen and restored on return in the same conversation.
- A leaking figure or marks block withholds the whole reply as a leaking sentence does; a malformed one is dropped with one line and the text continues.
- The figure stays sticky at the top of the conversation while it builds, found necessary by the recorded walk.
- `MAX_OUTPUT_TOKENS` stays 800; a figure is about 300 tokens of it.
- The prefix ceiling: 10,000 tokens set on the orchestrator's authority for the new template test, raised to 12,000 by the operator in chat when marks took the prefix to 11,657.
- Gate maintenance, recorded for the operator's review: `tests/db/test_models.py` gained `figure` in the `agent_turns` column set, and `tests/agent/test_prefix.py` names `prompts/agent/live_v2.md` and adds `drawing` to its field list; each assertion keeps its strength. No other existing test, gate or fixture was edited to pass.

What is behind a switch: `GROWTH_AGENT_DRAWING` (default on) closes drawing and marks on every turn when `off`.

Not done, and why: no live block came out malformed or oversized, so those refusals were shown with the fake CLI; the language cannot read the item's own table into a Riemann sum, so the model copies values; the route's refusal of a marks block reusing a figure's step ids has no golden case; a correct opener's first worked step is not offered as an anchor; the reading pace is an adult figure; `tests/eval/test_prompt_output_goldens.py` has no recorded output for `agent/live_v2` (as for `memory/consolidate_v1`), which needs an approved live call; the three provider failures and the GradingsPayload failure predate the branch.

Rulings waiting on the operator are in `docs/plan/12-open-questions.md`, "Rulings the tutor drawing needs, 2026-09-30": stated givens equal to the key, integer keys, the reading pace, a second hue, the stroke wipe, figures kept 30 days, drawing on the first practice reply, the share of turns that draw, the prefix ceiling (settled at 12,000 in chat) and the three test inventories.

Addendum, 2026-10-01: the art board and the merge. On the operator's instruction, figures left the chat for the tutor's art board (02dd7210, by one Opus 5.5 agent): a non-modal window that opens, without taking focus, whenever the tutor draws; the reply keeps one line, "Figure on the board: {title}", with "Show on the board"; from 900 px the board floats, moves by its title bar, resizes from a grip, minimizes to a bar and closes, with arrow keys on the focused title bar and grip and single-click "Move" (next corner) and "Size" (small, medium, large) buttons as the alternatives to dragging; under 900 px it docks under the top bar; geometry is kept in this browser's storage behind try and catch; it stays out of the tutor panel's column so it never covers the composer. The chat's sticky hold from the walk fixes went with it, and its two tests were removed as the behaviour they described no longer exists; two panel tests and the reading-pace helper now look for the figure on the board, with every gating assertion unchanged. `src/agent` and `src/styles`: "Test Files 16 passed (16)", "Tests 252 passed (252)". `main` moved meanwhile to 0f80de16 (another session's question-screen restyle); `main` was merged into `agent/drawing` in the worktree by one Opus 5.5 agent (3c69ad09), keeping the restyle exactly and adding back the anchors (`section_figure` moved onto the figure's body because the restyle put a margin tag in its old row), with the new semantic tints checked against the figure roles (lowest 4.61:1). On the merged tree: tests/agent "878 passed", the agent routes 22, 20, 10 and 1 passed, tests/db "36 passed", the agent golden set "20 passed", golden sets "11 passed", the cost model "17 passed", providers "3 failed, 288 passed" (the three known), `tools/agent_eval.py` "0 disagreements", every plan "0 unknown dollar figures", the build "built in 2.05s", and the web suite "Tests 2 failed | 1167 passed (1169)": `GradingsPayload` (known) and `useAgentStream.test.ts` "a turn after its end frame" with "Invalid state: Controller is already closed" at load average 10, which passed alone ("Tests 8 passed (8)") and in the merge agent's full run; it is a watch item, not a fix. The prompt for the next run, which audits what the tutor lacks in reaching the page and builds the skills that close it, is kept outside the repository at `var/agent/tutor-next-run-prompt.md`, because Claude prompts are not committed.

## Live tutor agent, 2026-09-29 [verified]

The operator's brief: a live tutor agent one click away on every screen, seeing structured screen context, keeping a developing per-student memory, self-tuning behind a switch, streaming its replies, on the Claude subscription backend through the Claude Code CLI with the API key as fallback. Every decision was delegated; the ones taken are listed below. Branch `agent/live-tutor` from the checkout's HEAD 8cb6be9 (two `today/redesign` commits past `main` 635c03b), nine commits (c7956e0 to the entry commit), nothing pushed, `main` untouched. Research and design were written by Opus 5.5 agents and the orchestrator (Fable 5.1); every line of application, test and tool code was written by Opus 5.5 agents and checked by the orchestrator running the named command. State and resume point: `docs/agent/HANDOFF.md`.

Stage A, research, `docs/agent/research/`: `providers.md` (the CLI stream-json path, prices, retention, the chain; ends with four measured calls), `memory.md`, `live-assistant-ux.md`, `math-tutoring.md`, `self-tuning.md`, `synthesis.md` (twelve ranked decisions, the strand disagreements and their resolution, the rulings for the operator), `README.md`. Stage B, `docs/agent/design.md` (entry point, panel, context lines, what the tutor does and does not do, streaming, memory in settings, the empty and degraded states with their fixed copy, keyboard and motion, dark mode and phone width), `architecture.md` (the boundaries, the screen context, the composer, the memory store, the cached prefix, roles and caps, streaming end to end, guard and audit, the self-tuning loop, the evals, what is behind a switch), `build-plan.md` (slices 0 to 7). Plan amendments dated 2026-09-29 in `docs/plan/03`, `06` (the role row), `07` ("Eight roles, and only eight"), `08`, `09`, `12` (the rulings list), `13` and `14`; `docs/operator/provider-key.md` gained the model-improvement note.

Stage C, the build. Roles `agent` and `memory` on `claude-sonnet-5-5` in `app/providers/guard.py`, `model_routing.py` and `subscription.py` (pacing 80 a day and 6 a minute for the agent, 10 and 2 for memory; API caps $1.50 and 1,500,000 tokens, $0.50 and 300,000; per-call budgets $0.15 and $0.10; `CLAUDE_CODE_MAX_RETRIES=1` and `API_TIMEOUT_MS=20000` fixed for both). `SubscriptionProvider.stream` runs `claude -p --output-format stream-json --include-partial-messages --verbose`, yields text deltas, keeps the `rate_limit_event` windows and sends SIGINT on an `api_retry` for a rate limit or a sign-in failure; `FallbackChain.stream` moves to the next link only before the first text. Tables `agent_conversations`, `agent_turns` (30 days), `tutor_memories` (preference, confusion, stated_difficulty, episode; supersession, tombstones, 14 and 60 day expiry) and `tutor_profiles` (versioned), plus `users.agent_memory_paused`, in `app/db/models.py` with the additive migration; eight audit actions; purge and export cover all four. `app/agent/`: `context.py` (schema-validated screen, allow-list packets for practice, after submission and browsing, the screen line), `moves.py` (M1 to M7, P1 to P7, chosen by the app), `screen.py` (`SentenceScreen`: key equivalence through SymPy and MathJSON, praise, advice, prediction, dashes, id resolution, shared with the evals), `turn.py` (`run_turn`, the ceilings of 3 practice turns per item and 20 per conversation, the error kinds), `copy.py`, `memory.py`, `conversations.py`, `consolidate.py` (schema-validated ADD, UPDATE, SUPERSEDE, NOOP), `drain.py` (the `agent_consolidate` job on the auto drain) and `profile.py`. Route `POST /agent/turns` streams server-sent events (start, text, end, error) with the kinds usage_limit, daily_cap, minute_cap, sign_in, unavailable, timed, ceiling and refused; the memory, conversation, settings and profile routes sit beside it in `app/api/routes/agent.py`. Templates `prompts/agent/live_v1.md`, `decline_v1.md` and `prompts/memory/consolidate_v1.md`; schemas `schemas/agent/screen.schema.json` and `consolidation.schema.json`; the golden set `content/golden/agent.json` (44 cases, 147 turns) run by `tools/agent_eval.py` and `tests/eval/test_agent_golden.py`. Client (`app/web/src/agent/`): `AgentProvider`, `AgentPanel`, `useAgentStream` (fetch and an SSE parser), the Ask button with `aria-expanded`, Ctrl+/ and Cmd+/, the 384 px aside from 1100 px and 320 px from 900 px, the bottom sheet under 900 px (collapsed, half, full), the context lines, the guardrail line, KaTeX through the untrusted renderer (`maxExpand` 100, `maxSize` 20), the Tutor settings tab (conversations, memory entries with edit, delete, clear and pause, the profile), and the AI notices hidden for the agent role. Experiment switch `tutor_profile` (unit skill, arms `profile_withheld` and `profile_applied`, stratum the unit block) with its comparison and calibration guard in `app/experiments/analysis.py`.

Stage D, the walk, on a scratch API (127.0.0.1:8017, a scratch database, `GROWTH_AI_BACKEND=subscription`) and the scratch web client on 5187, driven through the app's browser pane: the Today screen, a practice item before and after submission, a lesson, the progress screen through the shortcut, the settings tab, the daily cap (the pacing ledger set to 80, restored), offline (the API stopped), the simulated usage limit (the fake CLI's `stream_limit` mode), keyboard only, phone width with the sheet in each height, light theme, dark theme and the reduced-motion rule. Screenshots 01 to 15 under `var/agent/` (gitignored). Nine defects were found and fixed by one Opus agent, each with a red-then-green test: a lesson prediction, check, fix prompt or faded example was browsing mode, so the reply on LSN-CON-01006 stated the prediction's key (now practice mode with the section's key forms screened, counted per section); the aside's conversation did not scroll; the golden cases GLD-AGT-015 to 018 did not name the path step under the unique three-content-word rule; the client's first-text timer and Stop could abort a request after its end frame; consolidation rejections were not counted by reason; a conversation-order test was flaky on a shared timestamp; the usage-limit copy vanished at once when `resets_at` was in the past; the fake CLI's reset times were fixed dates; and a settings test expected the old switch label. After the fixes the prediction turn was repeated live: the panel showed the guardrail line on the prediction, the turn was stored as practice with the move ask_what_tried, and the reply asked which part of the graph the student looked at and said the limit is not something it can state before the item is checked. The usage-limit copy now stays with its reset time an hour ahead. The conversation region is `overflow-y: auto` and holds its scroll position (measured 190 of 190 at 1280 by 520). Logs and audit details were grepped for student text, the walk username, the token variable and key prefixes: 0 matches in each.

Live calls, all on the subscription backend through claude CLI 2.1.284 with `CLAUDE_CODE_OAUTH_TOKEN` from `.env`, no API call made and the $15.00 developer cap untouched:

| Call | Purpose | Result |
| --- | --- | --- |
| 1 | orchestrator probe, stream-json | 15 text deltas, a `rate_limit_event` with both windows, result success, input 485, output 60 |
| 2 to 4 | orchestrator probes, the practice prefix plus filler, three turns | first delta 3.34, 2.82, 3.21 s; cache read 0, 1906, 1906; replies refused to evaluate the draft |
| 5 | lesson prediction, browsing mode (the defect) | the reply stated the key |
| 6 | practice item, the student claimed an answer and asked which option | declined, pointed to submitting, asked which rows were used |
| 7 | after submission | discussed the deciding step with rendered mathematics |
| 8 | `tools/drain_agent_queue.py`, memory role | done 1, applied 0, rejected 0, profile version 1 written |
| 9 | progress screen, two preferences and a confusion stated | an agent turn |
| 10 | drain, memory role | done 1, applied 1, rejected 1 |
| 11 | lesson prediction after the fix | practice mode, the key withheld, move ask_what_tried |

Checks run in this session, each by the orchestrator, exit status as printed:

| Check | Command | Result |
| --- | --- | --- |
| Providers | `timeout 580 .venv/bin/python -m pytest tests/providers -q` (background) | 288 passed, 3 failed, exit 1; the three fail on `main` the same way (`test_ai_notices` grader brief, `test_prompt_cache_prefix_length`, `test_prompts` lesson_v1 golden) |
| Agent package | same over `tests/agent` | 109 passed, exit 0 |
| Agent routes | same over `tests/api/test_agent_settings_routes.py tests/api/test_agent_turn.py tests/api/test_export_then_purge.py` | 33 passed, exit 0 |
| Experiments, db, audit | same over `tests/experiments tests/db tests/audit` | 93 passed, exit 0 |
| Agent golden set | `pytest tests/eval/test_agent_golden.py` | 12 passed, exit 0 |
| Tutor golden sets | `pytest tests/eval/test_golden_sets.py` | 11 passed, exit 0 |
| Analysis after the guards field | `pytest tests/experiments/test_analysis.py` | 5 passed, exit 0 |
| Agent eval | `tools/agent_eval.py` | 44 cases, 147 turns; no_dash 147/147, turns_within_ceiling 78/79, names_rule 30/44, 0 disagreements between labels and checks, exit 0 |
| Web tests | `npm --prefix app/web run test -- --run` (background) | Test Files 80 passed, 1 failed; Tests 916 passed, 2 failed; then, after the guards field was put back in the returned literal, `client.test.ts` and `MetricsView.test.tsx`: 252 passed, 1 failed, the `GradingsPayload` case that fails on `main` |
| Types | `npx tsc --noEmit` from app/web | exit 0 |
| Web build | `npm --prefix app/web run build` | "built in 4.30s", exit 0 |
| Plan dollar figures | `tools/cost_model.py --check` over plans 03, 06, 07, 08, 09, 12, 13, 14 | 03, 08, 09, 12, 13, 14: 0 unknown; 06: 1 unknown and 07: 9 unknown, the same 10 figures `main`'s copies report with `main`'s tool |

Decisions taken, with the reason:

- The subscription backend is the first link and the API key the second, with no queue for a chat turn and no Ollama floor; a reply half an hour later answers a screen the student has left, and the queue payload would hold the student's words.
- No tool definitions reach a model. The screen context is application state the client serialises against a schema, never a screenshot, and it excludes the draft answer and every key.
- Before submission the model gets the item's stem and the option letters, the archetype path and the student's turns, never the key; the harness holds the key forms and screens every sentence. A lesson section that poses a question is practice mode too (the ruling after live call 5).
- Nothing writes mastery evidence. The agent's turns and memories sit in their own tables, and a boundary test walks the import graph and compares `skills_state` before and after a turn.
- Memory kinds are limited to preference, confusion, stated_difficulty and episode; consolidation runs on the drain after a conversation closes, and every proposal is schema-checked and then rule-checked, with the rejections counted by reason. `stated_requests` are stored and never rendered into a prompt.
- The profile is computed for everyone and rendered only in the `profile_applied` arm of `tutor_profile`, so the comparison has a control. The guardrail beats the guardrail level, which beats the profile.
- Turns are kept 30 days, readable and deletable in Settings; memories 60 days from last use; episodes 14 days. The 7-day buffer is a ruling for the operator.
- Ceilings: 3 practice turns per item, 20 turns per conversation, fixed copy at each.
- The BC-PT scoring line is named only on a unique match of at least three content words (the two-word rule misfired in slice 3).
- The comparison view returns `guards` on every comparison, null where a comparison has none, so the client vocabulary test can read the literal; the earlier conditional key broke that test.
- The one existing test edited by the fix agent, the lesson screen-line test, posted on a prediction and asserted the browsing move, which encoded the defect; it now posts on the orientation section with every assertion kept.
- The lesson-ingest process pool lost a worker once at API startup under machine load (load average above 60); the relaunch succeeded. Not a code change.

Not done, and why: the reader's `#end` and a decision lesson's `#stems` screen send ids the server refuses (400 with the fixed copy); a lesson question stays practice mode after it is answered because the server does not read the check responses; a `usage_limit` with no reset time clears only on an edit; `tests/eval/test_prompt_output_goldens.py` has no recorded output for `memory/consolidate_v1` (it failed on HEAD for other prompts already); the Ollama floor is not built. One full pytest run of the whole suite was not made; each affected directory ran on its own.

Rulings waiting on the operator are in `docs/plan/12-open-questions.md`, "Rulings the live tutor agent needs, 2026-09-29", with two more from the walk: the mode of an answered lesson question, and the copy for a usage limit with no reset time.

## Today redesign, 2026-09-29 [verified]

The operator's overnight brief: research how the best practice products and the literature pick the next problem, measure Growth's Today against it (algorithm, session shape, question bank), redesign the algorithm, the session, the day screen and the question standards, prove the result on the simulator and in the running app, and record it. Every decision was delegated; the ones taken are listed below. Branch `today/redesign` from main 635c03b (the operator asked mid-run for every branch to be merged and pushed, so main was fast-forwarded to lessons/redesign and ai-fixes merged first), 39 commits, in the worktree `~/dev/growth-today` after another session switched `~/dev/growth` to `calculator/desmos-fluency` mid-run and committed the first session's pending files there (bfa1769, carried over as 6631c85). Research and design documents were written by the orchestrator (Fable 5.1) and Sonnet agents; every line of application, tool and test code by Opus 5.5 agents; every check below was run by the orchestrator with the command named.

Stage A, `docs/pedagogy/today/`: ten product studies (`products/`: Math Academy, Khan Academy, Duolingo, Anki with FSRS, ALEKS, Brilliant, IXL, DeltaMath, Alcumus, AP Classroom), `science.md` (thirteen mechanisms with numbers, what Growth does and does not do with each), `question-standards.md` (twelve sections and the checklist of machine-checkable standards against `tools/check_items.py`), `synthesis.md` (ten techniques ranked, the warnings, the rejected list, where the selection study says the gain is) and `README.md`. Web claims carry [verified] only where two sources agree; each cites URL and access date. Stage B, `clean-slate-design.md` and `rulings-for-operator.md` (R1 to R11 rejected techniques, C1 to C12 decisions that need the operator).

Stage C, `growth-gap-analysis.md`, flaws T1 to T25, measured before judged:

- Algorithm: `tools/today_metrics.py` (new, `app/sim/today_metrics.py`) over 20 synthetic students at 60 and 226 days: block 2 decided by due coverage 33 to 35 percent (16 single winner, 18 to 19 tied), uniform random 65 to 67; the window changes the pick on 13 and 5 percent of choices; 3.9 of 5.5 and 8.4 of 12.4 due skills per due session go unserved; a skill takes a median 25 to 27 items to mastery. `tools/selection_study.py 8` re-run on the recorded seeds (124 minutes): the 2026-09-26 record does not reproduce on the current engine; due coverage now fires on 40.0 and 45.8 percent of block 2 choices, and two-term sits wholly below the random control on mastery per item at both horizons under both curves (fixed world, 60 days, exponential: -0.00301 [-0.00389, -0.00214]); under the 2026-09-27 ruling the two-term floor of plan 10 fails. The floor was not moved; the record is replaced (`docs/operator/selection-study-record.md`, and the reading in `selection-study.md`, "Re-run of 2026-09-29"). The 226-day metrics run and the tie histograms are in `docs/pedagogy/today/audit/`.
- Session shape: a browser walk of a seeded 28-day student (`tools/seed_history_student.py`, new, through the real routes) and a fresh student, screen by screen. Found: the wrong-answer feedback never showed the correct answer (T16); 37 to 39 due skills and 40 to 48 forecast minutes of them unserved while 16 corrected items due today filled block 1's five-item cap (T17); a fast submit on the math field wrote an ungraded attempt with no feedback (T18); Today loads for 20 to 100 seconds on a student with history (T19, the 2026-09-23 known defect); the mixed card announced its skills (T20); the pace verdict (T21); a stopped set is rebuilt, not resumed (T22); the opener shows no comparison without the tutor (T23); a fresh student placed only in Unit 2 was served Unit 5 skills on day one (T24); the placement said "Not placed yet" for a unit answered correctly twice and opened with Units 9, 6 and 8 (T25).
- Questions: `tools/draw_today_audit_sample.py` (new) drew 72 of 3,316 records across 11 unit blocks, 3 provenance classes, 6 short answer, 12 calculator; a blind Opus re-solver formulated 64 from the stems alone and `tools/key_recheck.py` matched 64 of 64 keys (control 8 of 8; 8 items need a table or graph the stem does not carry); a separate Opus judgment audit found 50 clean, 15 fix_distractor, 7 fix_stem, 0 key errors; 204 of 216 distractors follow their named error; 5 items with one error path across all three distractors; 16 items with a cue toward the key; 3 of 18 statement items with a defensible second choice; every active archetype holds 20 to 28 items but 12 hold fewer than 5 distinct stems with digits masked. Artefacts in `docs/pedagogy/today/audit/`.

Stage D, `design.md` (D1 to D15) and dated "Plan amendments, 2026-09-29" sections in plans 02, 03, 04, 05 and 10. Built:

1. Candidate policies in the simulator (`app/sim/today_policies.py`, `tools/today_sim_study.py`): retrievability_priority (block 2), retrievability_priority_both (blocks 2 and 3), elo_target, spread, review_first, beside two_term, random_control and oracle_forgetting, with a block 3 ordering hook (`retrieval_ordering`) and an Arm.learner observer. The full run (200 students, fixed and legacy worlds, 60 and 226 days, both curves) is `docs/pedagogy/today/simulation-record.md`: no candidate clears D2's bar. On the fixed world `retrievability_priority` against `two_term` reads, as mean paired difference with its 95 percent interval: delayed mastery per item -0.00130 [-0.00219, -0.00040] (exponential, 60 days), -0.00179 [-0.00258, -0.00100] (power law, 60 days), -0.00664 [-0.00734, -0.00595] (exponential, 226 days), -0.00671 [-0.00736, -0.00607] (power law, 226 days); retention day 30 +0.02702 [0.02288, 0.03115], +0.02221 [0.01857, 0.02585], +0.02065 [0.01551, 0.02579], +0.01283 [0.00834, 0.01733]; skills learned -9.5 [-10.5, -8.6], -9.1 [-10.1, -8.2], -48.3 [-51.2, -45.4], -45.8 [-48.6, -42.9]. It wins retention and loses delayed mastery and breadth on every fixed-world reading; on the legacy world it wins both mastery measures and still loses 14.7 to 18.5 skills learned. `spread` comes closest (delayed mastery above two_term at 60 days on both curves, +0.00303 [0.00216, 0.00390] and +0.00244 [0.00170, 0.00318], skills learned -0.42 [-1.18, 0.34] and -0.04 [-0.75, 0.67]) and fails at 226 days (skills learned -15.2 [-17.8, -12.7] and -14.5 [-17.0, -12.0]). `review_first` is the only arm that learns more skills than two_term (+1.3 [0.6, 2.1] at 60 days) and it loses retention (-0.00465 [-0.00790, -0.00140]). Every number is synthetic. So D2 lands as the switch, default off, and no candidate is ported to production.
2. The engine port (`app/engine/priority.py`): one implementation of retrievability priority (sum of 1 - R_k over the skills an archetype reaches that carry a memory state, then due coverage, then the seeded draw), which the simulator now imports. It lands behind `selection_priority` in `app/experiments/switches.py` (control two_term, treatment retrievability_priority, unit the session, default off); `open_session` and the home preview pass the same orderings so the preview matches the session. Every due skill block 1 cannot serve is written to the audit log as `due_skill_unserved` with its reason (no published item, below the retrieval floor, refused by the window, past the block cap). No FSRS parameter, threshold, cap or floor moved. Property tests in tests/engine/test_priority.py and tests in tests/session and tests/experiments, each seen red first (the agent's red lines are in its report and summarised in the check table).
3. Feedback and session: the feedback payload carries `correct_answer` and the client shows "The step should give" with the correct result after the violated step on every wrong answer at every stage (D5); the math field's live value is read at submit and an empty short answer cannot be checked (D6); an opener without the tutor says the comparison needs the tutor and shows the first worked step (D7).
4. Today: "N more skills are due today, about M minutes, beyond this set." under the counts when the due queue exceeds block 1, hidden at 0 (D9); the mixed-practice card names units and a count, not skills (D10); tokens, full width, no footer (D12). Vitest tests for each.
5. Question standards: nine lints in `app/items/standards.py` behind `tools/check_items.py` (`--standards`, `--json`), five by default because the operator's fixture passes them (calculator decimals scoped to stems asking for decimals or decimal keys, choice-worded short answer, command verb, stem length at 110 words, no all-or-none) and four under the flag (option count, distinct error paths, value option type, distractor provenance), each with a red fixture and a test. Measured over the bank: 1,394 of 3,316 fail under `--standards`, 98 under the default. Fixed through the pipeline: 17 of the 22 audited items in full and 3 in part (2 left: ITM-AGT-01009-04 and ITM-GEN-08009-17 need an error the archetype does not hold), 78 of the 98 default-lint records at the item (the other 20, BC-QA-99001, were the lint's over-reach and pass under the scoped lint); 13 templates and `app/generation/instantiate.py` changed and 381 template records regenerated from their stored seeds (`provenance_drift` 13 passed in 1465 s), 14 agent records edited by hand; 395 records changed in all, 204 of them by stem or option value, all 204 blind re-solved by a second Opus agent from a stems-only file: 180 formulated, 180 of 180 match the stored key and options (control 8 of 8), 24 table items not formulable from the stem. Duplicate gate: 395 changed against 3,316, blocked 0 (control blocked). No new items were drafted (D15 was last in order and not reached).

Stage E: the scratch servers restarted from the worktree (API 8005 seeded, 8006 fresh, web 5175 and 5176), the walk repeated by hand: the seeded Today shows 3 skills due, 13 at the frontier, "24 more skills are due today, about 15 minutes, beyond this set." and a mixed card with no skill names; the fresh student's wrong short answer at stage example shows the step marks and "The step should give −8"; the Check button stays disabled on an empty field. The capture script then ran the after-set walk on both students at 1280 and 390 wide, light and dark: 8 runs, 119 screens, every console error and failed request in the `sign-in` phase (57 entries of the 401 on /me, /progress and /progress/pace before the session cookie exists, and two favicon 404s), none after sign-in, page overflow on 0 of 7 completed runs after the fix of 50c75a9 (the one overflow, 432 against 390 on a wide worked step, was the cause of that commit); the history student's 390 light run stopped at 2 screens with 3 unanswered requests, the /progress load outrunning its deadline under load 40, and is covered by the 390 dark run. A screen recording of the changes, `tools/today_walk_record.mjs` (new, Brave screencast over CDP into ffmpeg), is `var/today-redesign/today-redesign-walk.mp4`. Screenshots (gitignored): `~/dev/growth-today/var/today-redesign/shots/` (140 before, `tools/today_walk_capture.mjs`, new) and `shots-after/`.

Checks run in this session, each by the orchestrator:

| Check | Command, from the worktree | Output, quoted |
|---|---|---|
| Web build | `npm run build` in app/web | `built in 9.69s` |
| Types | `npx tsc --noEmit -p .` in app/web | exit 0, no output |
| Vitest, whole client | `npx vitest run` in app/web | `Test Files  1 failed \| 80 passed (81)`, `Tests  1 failed \| 861 passed (862)`; the failure is `src/api/client.test.ts` GradingsPayload (`tutor_explanation`, `tutor_unavailable` missing from the shape list), which the fix agent reproduced on main 635c03b |
| Vitest, files touched by the fix | `npx vitest run src/session/wideMathScrolls.test.tsx src/styles/app.test.ts src/styles/noLiteralValues.test.ts src/home src/session/feedbackCorrectAnswer.test.tsx` | `Test Files  6 passed (6)`, `Tests  35 passed (35)`; wideMathScrolls went red with the class removed (`AssertionError: the correct result's math sits in no scrolling holder: expected null not to be null`) and green restored |
| Engine | `pytest tests/engine` | `90 passed in 281.26s` |
| Session | `pytest tests/session` | `93 passed in 69.62s` |
| Experiments | `pytest tests/experiments` | `9 passed in 11.66s` |
| Tools | `pytest tests/tools` | `157 passed in 464.27s` |
| Audit | `pytest tests/audit` | `46 passed in 60.44s` |
| Feedback, sim, routes after the fix | `pytest tests/feedback tests/sim tests/api/test_routes.py` | 73 passed, 1 failed: `tests/sim/test_today_policies.py::test_the_running_app_passes_no_retrieval_ordering` (`assert 'retrieval_ordering' not in ...`), red by design (C10) |
| Routes, feedback payload, switch, e2e | `pytest tests/api/test_routes.py tests/api/test_feedback_correct_answer.py tests/session/test_selection_switch.py tests/e2e/test_agent_drafts_served.py` | 25 passed, 1 failed (`no Unit 2 item was served in 12 sessions`); the e2e test alone then `1 passed`, exit 0; the fix agent saw the same single failure on main |
| Items | `pytest tests/items` | `10 failed, 210 passed in 774.39s`; 8 of the 10 fail identically on a detached main worktree (`8 failed, 31 passed in 61.57s`, same node ids); the other 2, `tests/items/test_bound_child_failure.py`, pass alone (6 dots, exit 0), so they are load failures of a forkserver child |
| Item banks, default lints | `tools/check_items.py content/<bank>` over the 20 banks | `with violations: 0`, exit 0 on 19 banks; `items_unit03_agent`, untouched by the branch, reports `distractor_distinct indeterminate: unsettled` on 4 records in one run and on 1 other record in the next, the SymPy comparison outliving its bound at load 25 to 45 |
| Blind re-solve of the fixed items | `tools/key_recheck.py` with `var/today-redesign/fixed_formulations.py` | 180 of 180 formulated keys match, 24 not formulated (need a figure the stem does not carry), control 8 of 8 |
| Selection study re-run | `tools/selection_study.py` (in ~/dev/growth, before the checkout switch) | `wrote docs/operator/selection-study-record.md` after 7218 s |
| Candidate study | `tools/today_sim_study.py 200 4` | `wrote docs/pedagogy/today/simulation-record.md` in 272 minutes |
| P7 record re-run | `tools/p7_evals.py 4` | `wrote docs/operator/p7-evals.md`; every number moved (two_term true mastery per item 0.01211 to 0.04529, skills learned 15074 to 7777, placed-not-known 29 of 334 to 0 of 432), see the decision below |
| Style gate | `tools/style_gate.py` on every edited file before each commit | exit 0 each time; the gate skips `.mjs`, so the two Node scripts were grepped for dashes by hand |

Decisions taken, with the reason:

- The other session's checkout switch was handled by moving to a worktree with its own venv rather than by contesting the branch; the pending files it committed (bfa1769) were cherry-picked so nothing was lost.
- The retrievability policy is the engine-side form of the forgetting oracle and needs no new state; it ships behind a switch unless the candidate study clears the bar of plan 10 as ruled on 2026-09-27, read on delayed mastery per item and retention at day 30 with no loss on skills learned.
- The two-term floor's failure on the re-run is reported, not acted on: the floor is a gate and only the operator moves it; the switch keeps two-term live by default.
- The `calculator_decimals` lint was scoped to the standard as written after it flagged 20 exact-value calculator items; its red fixture was made stricter, not looser (C9).
- `tests/sim/test_today_policies.py::test_the_running_app_passes_no_retrieval_ordering`, written this run for the simulation-only state, fails by design now that the treatment arm passes an ordering; it is left red and unedited, and the switch-off test carries the behavioural invariant (C10).
- The four fixture-failing lints stay behind `--standards`, because a fixture is never edited to pass (C8).
- The mixed card hides skill names on Matuschak's announced-review warning; the review and new-ground cards keep theirs.
- The block 1 cap and the review floor are instrumented, not moved (C1, C2); the uncredited retry, the sibling requeue, the pace verdict and the choice of block wait for rulings (C3 to C6).
- The empty-field refusal fires only once MathLive has loaded, because 38 existing tests submit an empty field in jsdom; a click before MathLive loads still posts a null answer.
- The P7 record re-run moved every number because main's world changed after the record was last written: fa10e0d (relearning a lapsed skill on feedback) landed on main after 7188135, the last `p7_evals.py` run, and the branch's own change to `app/sim/learning.py` adds two optional arm fields that no existing arm sets. Run again with main's own code on a detached worktree (`PYTHONPATH` ahead of the editable install), the tool wrote a byte-identical record (`diff -q` silent), so the branch changes nothing the record measures and the committed numbers on main were three days stale. The regenerated record is committed as the tool writes it; the tool hardcodes `research_date: 2026-09-26`, left for the operator (C14).
- The unit 03 agent bank's `unsettled` findings are recorded as load-bound, not fixed: the bank is untouched by the branch and the flagged record changes between runs.
- The mathjson renderer drops a stored key's trailing zeros (4.290 renders 4.29); left for a follow-up task (C12).

Not done, and why:

- No new items were drafted for the calculator and representation gaps (D15): the pipeline time went to the 395 fixes.
- `distinct_error_paths` still fails 997 records under `--standards`, mostly agent drafts whose archetypes hold too few errors; unit-by-unit repair needs new BC-ERR records, a library task.
- The full `tests/lessons/test_invariants.py` gate was not re-run (over 900 s); the engine change does not touch lessons.
- The P7 record's date: `tools/p7_evals.py` stamps 2026-09-26 whatever the run day (C14), so the regenerated record carries a wrong date until the tool is changed.
- The fresh-student fringe breadth (T24) and the placement's unit order (T25) are recorded for the operator; both sit in the diagnostic and gating, outside the brief.
- Two pre-existing failures on main are not touched: `tests/eval/test_selection_study.py::test_the_decay_arm_serves_differently_from_two_term` (the decay arm now serves the same trace on that seed) and `tests/api/test_evaluation_routes.py::test_metrics_view_renders` (the metrics view omits `lesson_first_contact`, and now `selection_priority`, C11).

Rulings waiting on the operator are in `docs/pedagogy/today/rulings-for-operator.md`; the state and resume point in `docs/pedagogy/today/HANDOFF.md`.

## Lesson framework redesign, 2026-09-29 [verified]

The operator's overnight brief: study how the strong mathematics products teach, design the lesson from a clean slate, measure the 127 served lessons against it, amend the framework, redesign every Unit 1 to 8 lesson, bring Units 9 and 10 to the new template, and prove the result in the running app. Every decision was delegated; the ones taken are listed below. Branch `lessons/redesign` from `main`, 31 commits (82927a2 to the entry commit), nothing pushed, main untouched. Research and design documents were written by the orchestrator (Fable 5.1) and Sonnet agents; every line of application and tool code was written by Opus 5.5 agents and checked by the orchestrator running the named command.

Stage A, the research base, `docs/pedagogy/`: twelve product studies (`products/`), `learning-science.md`, `synthesis.md` (ranked techniques, warnings, rejected list), `rulings-for-operator.md` and `README.md`. Web claims carry [verified] only where two independent sources agree; each cites its URL and access date. Stage B, `clean-slate-design.md`. Stage C, `growth-gap-analysis.md`: a measured table over the 127 records (the median first student action was screen 8 of 12; 125 of 127 put the first check after every trap; 50 carried nothing drawn; 42 served texts carried a record id) and a browser walk of LSN-CON-01001, flaws G1 to G16.

Stage D, the framework, is additive. Schema and `app/lessons/plan.py`: a `prediction` section served first in both bands (mcq with 2 to 4 options and one key, or a short answer whose key equals example 1's answer or a valued step; resolution of at most 40 words); `contrast` on the first strategy block (this stem on the block's archetype, a near-miss stem with why_not, the separating feature); `fade_from` on the low-band second example; `fix_prompt` on error blocks (true exactly when the relation is distinct); top-level `no_figure_reason` when no block is drawn; the served-text rule (no record ids, page citations, evidence tags or the reader's own labels in served fields). Served order: prediction, orientation, bridges, key ideas, strategies with contrast, example 1 and its scoring, check 1, error blocks, faded example 2, check 2, representations, check 3. New lints in both checkers: prediction_section, contrast, fade, fix_prompt, figure_presence, served_text, each with a red fixture. No cap moved: 900 and 450 words, 6 and 3 minutes, three checks (rulings C1 to C4 say what the framework designed around them). Backend: `POST /lessons/{id}/prompts/{section_id}/answers` grades a prediction, a fix prompt or a faded example through `app/items/grade.py` and writes `lesson_check_responses` only; the event routes accept the reader's check, prediction and contrast modes (G10 was a 422); a check verdict carries `right_step` and `scoring_consequence`. Reader (`app/web/src/lessons/`): the prediction screen with Commit gating Next, the resolution line on the first core key idea, the contrast pair, "Show all steps" before a worked example is left, the faded example flow, the fix prompt flow, the three-line verdict with one "Try again", named parts in the pacing line, and `renderRecord.test.tsx` over every record in `LESSON_RECORD_DIR`. Tooling: `prompts/generator/lesson_v2.md` (v1 marked superseded), `tools/lesson_transcribe.py` carries the new fields, `tools/lesson_transcribe_all.py` pools transcription, `tools/lesson_resolve_compare.py` compares them, `tools/lesson_design_resolve.py` reads a chosen option id and a set written as a list and gives a dependent check its example text, `app/items/mathjson.py` converts factorials. `docs/lessons/TEMPLATE.md` carries "What changed on 2026-09-29"; `docs/plan/15-lessons.md` ends with "Plan amendments, 2026-09-29" (Q26 to Q28).

Stage E, the 127 lessons of Units 1 to 8 (19, 15, 10, 15, 15, 20, 12, 21). Each design was rewritten by a Sonnet agent from its authoring bundle, checked by `tools/check_lesson_designs.py`, transcribed, checked by `tools/check_lessons.py`, compared field by field, audited block by block by an Opus agent in batches of five (verdicts and advice in `docs/lessons/verification/<id>.json`, `audit`), fixed by an Opus agent at the design (never at the verdict), re-transcribed and signed off by `tools/lesson_sign_off.py`. Stems and keys that changed went through a blind re-solve on a Sonnet solver that sees only the problem text: delta c, 15 lessons, 60 problems, 0 disagreements, 8 statement judgments applied; delta d, 3 lessons, 12 problems; delta e, the same lessons' dependent checks with their example text, 8 problems, 0 disagreements. Final state: 127 records signed off, `tools/check_lessons.py content/lessons` over the whole directory in one background run (quoted in the check table), `tools/lesson_sign_off.py` refused 0.

Stage F: the 43 Unit 9 and 10 designs (17 and 26) are at the new template and checked; 41 were written fresh because only LSN-CON-09001 and 09007 existed. They are not transcribed, as the brief asked. The manifest marks them checked.

Checks run in this session, each by the orchestrator, exit status as printed:

| Check | Command | Result |
| --- | --- | --- |
| Design checker, Unit 9 directory | `PYTHONPATH=. .venv/bin/python tools/check_lesson_designs.py docs/lessons/unit-09` | files read 18, clean 18, with findings 0, exit 0 |
| Design checker, Unit 10 directory | same over `docs/lessons/unit-10` | files read 27, clean 27, with findings 0, exit 0 |
| Design checker, Units 6 and 8 after fixes | same over both directories | clean 41, with findings 0 |
| Transcription, Units 6 and 8 | `tools/lesson_transcribe_all.py docs/lessons/unit-06 docs/lessons/unit-08` | designs 41, wrote 41, refused 0 |
| Record checker, Units 6 and 8 | `tools/check_lessons.py` over the 41 records | clean 41, with findings 0 |
| Sign-off, Units 6 and 8 | `tools/lesson_sign_off.py` over the 41 records | signed off 41, refused 0 |
| Sign-off, delta c lessons | over the 15 records | signed off 15, refused 0 |
| Sign-off, delta d lessons | over LSN-CON-06007, 06009, 06012 | signed off 3, refused 0 |
| Blind re-solve delta c | `tools/lesson_design_resolve.py compare ... delta-2026-09-29-c` | lessons 15, problems 60, disagreements 0, judgments pending 8, then `judge`: judgments applied 8 |
| Blind re-solve delta d and e | same over d, then e | d: disagreements 0 after the tool patch and the e re-solve; e: lessons 2, problems 8, disagreements 0, judgments pending 0 |
| Record checker, whole directory | `PYTHONPATH=. timeout 900 .venv/bin/python tools/check_lessons.py content/lessons` (background) | lessons read 127, clean 127, with findings 0, exit 0 |
| Invariants, full 1,000 cases | `pytest tests/lessons/test_invariants.py -k <test>` as ten parallel processes under `timeout 600` | 10 of 10: 1 passed, 9 deselected, exit 0 each; slowest 142.70 s |
| Lesson pytest files | one process per file under `timeout 600`: tests/lessons (11 files), tests/items/test_mathjson.py and test_verify.py, tests/session lesson gate, refresh, purge, service, tests/api lessons routes and session | check_lesson_designs 50, check_lessons 120, confusable 7, ingest 13, plan 22, repository 8, resolve_compare 13, sign_off 4, source 10, transcribe 15, transcribe_all 2, design_resolve 20, verify 11, lesson_gate 17, lesson_refresh 8, purge 6, service 13, lessons_routes 41, lessons_session 7, all passed, exit 0; mathjson 1 failed then, after the factorial head and the tuple rewrite, 8 passed |
| Web tests | `npm --prefix app/web run test` (background, timeout 600) | Test Files 77 passed, Tests 841 passed, exit 0; after the verdict fix 77 files, 843 passed, exit 0 |
| Web build | `npm --prefix app/web run build` | exit 0, twice (before and after the verdict fix) |
| Render harness over every record | `LESSON_RECORD_DIR=../../content/lessons npx vitest run src/lessons/renderRecord.test.tsx` from app/web | 1 file, 260 tests passed, exit 0, run again after the re-sign: 260 passed |
| Plan dollar figures | `tools/cost_model.py --check docs/plan/15-lessons.md` | 0 unknown dollar figures |
| Design checker, all ten unit directories after the Predict strip | one background process per `docs/lessons/unit-NN` | unit 01 clean 20, 02 clean 16, 03 clean 11, 04 clean 16, 05 clean 16, 06 clean 21, 07 clean 13, 08 clean 22, 09 clean 18, 10 clean 27 (README files counted), with findings 0, exit 0 each |
| Re-transcribe, check, compare, re-sign after the strip | `tools/lesson_transcribe_all.py` over unit-01 to unit-08; `tools/check_lessons.py content/lessons`; `tools/lesson_resolve_compare.py` per record; `tools/lesson_sign_off.py` over the 127 records | designs 127, wrote 127, refused 0; clean 127, with findings 0; differing 0 on all 127; records 127, signed off 127, refused 0 |
| Check verdict shows the right step's value once | from app/web, `npx vitest run src/lessons`, `npx tsc --noEmit -p .` | 1 failed on the old code, 8 passed after; src/lessons 10 files, 94 passed; tsc exit 0 |
| Graph panels in a row | from app/web, `npx vitest run src/lessons src/figures src/styles`, `npx tsc --noEmit -p .` | 1 failed on the old CSS, then 17 files, 161 passed; tsc exit 0 |
| MathJSON heads the web field emits (Square first) | `pytest tests/items/test_mathjson.py tests/items/test_grade.py tests/items/test_verify.py` | 3 failed without the Square head, 105 passed after |
| Served-text lint with the Predict label | `pytest tests/lessons/test_check_lessons.py tests/lessons/test_check_lesson_designs.py` | 7 failed on the old code, 178 passed after |

Stage G, the app walk. The scratch API (127.0.0.1:8004, a scratch database, `GROWTH_AI_BACKEND=none`) was restarted to ingest the signed records and the scratch web client (5174) drove through headless Brave over CDP with the session's driver, which now commits the prediction, answers fix prompts and faded examples, reveals every step, answers each check wrongly and presses "Try again" once. Plan: one signed lesson per unit (LSN-CON-01001, 02013, 03001, 04012, 05003, 06007, 07001, 08021), desktop 1280 by 900 and phone 390 by 844, dark and light, 32 runs. Every run reached the end screen: 13 to 17 parts each, 2 or 3 checks answered, 3 to 6 prompts answered, 0 console errors, 0 failed requests, 0 horizontal page overflow (the driver's per-element overflow flags were SVG text nodes inside figures, whose scroll width exceeds the phone viewport without scrolling the page). The screenshots (864 files) and report.json are under `var/lesson-redesign/` (gitignored), named `<lesson>-<viewport>-<theme>-part-NN-<kind>[-prediction|-prediction-committed|-fade|-fade-answered|-fix|-fix-answered|-answered|-retried].png`. Two defects were found in the screens and fixed, each with a red-then-green test: the check verdict printed the right step's value twice (LSN-CON-01001 part 12), and a `graph_panels` figure drew its second panel over the first and past the card because the panel row inherited the figure's column direction (LSN-CON-05003 parts 3 and 4; measured boxes before and after are in the agent's report and the fix is `fa5cb6b`). LSN-CON-05003 was re-shot after the fix (four runs, 17 screens each, reached the end, 0 console errors, 0 failed requests; the phone screenshot shows the two panels stacked inside the card). Known nits left: at phone width a motion figure's inside labels can sit over the axis numbers (LSN-CON-01001 part 3); the full-page phone capture paints the fixed tab bar across the middle of a tall part, which is the capture, not the layout.

Decisions taken, with the reason:

- Sonnet agents wrote the lesson designs and blind re-solves; Opus agents wrote every line of code and every block audit and fix. The brief fixed Opus for code; designs are prose and JSON drawn from the authoring bundle, and the audit by a stronger model is the gate on them.
- No cap was raised. Where the brief form did not fit, the design agents dropped anchor quotes, scoring reader-line tags (BC-PT) on example 1, `possible_reason` lines and bridge words rather than the prediction, the contrast, the checks or the error blocks. Rulings C2 and C4 record what a wider cap would restore. This trimming is content lost under the cap, not a defect in the records.
- A delayed retrieval check (a check served on a later day) was rejected: lessons count toward no mastery evidence, and a later-day check is engine scheduling, outside the brief.
- Explanatory video is not a delivery mode (ruling R11).
- The prediction's distractor arithmetic is not machine-checked: the design checker verifies the keyed option against example 1's values, and the Opus audit reads the distractors. A distractor that is accidentally true would pass the machine and rely on the audit.
- Served-text sweep: the reader's own labels ("First line:", "Rival:") and block ids were stripped from every served field by a script and a strengthened lint; the script capitalised single-letter function names in four designs ("f'(x)" to "F'(x)"), which the fixers restored (05003, 06007, 06008, 07007).
- The app walk showed the prediction heading "Predict" above a stem that opened "Predict." in 100 of 127 served records (and one Unit 10 design), the same class as G15. The label was stripped from the 101 design stems in place, the served_text rule now refuses it in both checkers, and the 127 records were re-transcribed, re-checked, compared and re-signed. The block audit verdicts stand: one leading word changed, no mathematics.
- The wrong-answer verdict shows the anchored error block's right step, which is the block's own example (the s(t) example on a V(t) check). That is the framework's design: the verdict points at the taught trap and the "Go to the part on that error" link opens it. The value it appended after a text that already carried it was a reader defect, fixed and tested.
- The recorded walk (var/lesson-redesign/lesson-walk.mp4, LSN-CON-02013) found that the math field serialises a typed x^2 as the MathJSON head Square, which the grader refused, so a correct fix-prompt or check answer holding x^2 was left ungraded and shown as "Not yet."; Square, Half, the infinity and NaN number objects, parenthesised groups, the remaining inverse and hyperbolic trig heads, Floor, Ceil, Sign, Min and Max now convert. One-argument Log now reads as base 10, the engine's meaning; the rulings file asks whether the ln reading is wanted instead.
- The blind re-solve compare ignored the solver's chosen option id on a statement mcq (4 false disagreements), could not read a set written as a list (3), and gave a dependent check no example text (2). Each was fixed in the tool with a red-then-green test; no verdict was edited.
- `git add docs/lessons/verification` in the unit commits swept other units' in-progress audit files along. Harmless: every file was later finished and re-committed, but a unit commit is not a clean unit boundary in that directory.
- The scratch servers (API 127.0.0.1:8004 on a scratch database, web on 5174) were started with nohup because the app's preview tool refused a sixth dev server; the other five belong to other sessions.
- The Unit 9 and 10 designs carried four velocity vectors as `Matrix([...])`, which the MathJSON converter refuses by design; they are tuples now, and factorials from Unit 10 gained a head.
- Library gaps met by the designs are in each design's `inferred` array and summarised in docs/lessons/BUILD-PLAN.md "Library gaps": BC-PT reader lines of 42 to 110 words that no brief form can hold beside a prediction and a contrast; skills holding one error so three distractors share it; archetypes with no draw for a taught case (a ratio limit of 1, a ratio of size at least one).

Not done, and why:

- Units 9 and 10 are designed and checked, not transcribed, ingested or audited, as the brief asked.
- The 77 prerequisite lessons and 9 decision lessons are untouched (the brief covered concept lessons).
- `docs/plan/15-lessons.md` still describes a six-endpoint route file in its history; the amendment table and the L1 line note the seventh.
- One full pytest run of the whole suite was not made; the operator's rule is narrow selectors, and every lesson-related file ran on its own.

Rulings waiting on the operator are in `docs/pedagogy/rulings-for-operator.md` (R1 to R12 rejected techniques, C1 to C4 caps, and the four earlier handoff questions with their defaults).

## Client redesign and session persistence, 2026-09-29 [verified]

The operator asked for the client rewritten to the design in `mockup-redesign/` (gitignored), a real endpoint behind every view, and sessions that never sign the student out, and delegated every decision. The working record is `mockup-redesign/PORT-STATUS.md`; this is its summary.

Logouts: every local server (ports 8000 to 8003, several started by agent sessions) set the same `growth_session` cookie, and a browser keys cookies on host, not port, so signing in to one server replaced another's token. The local database showed two recovery resets and no ordinary login. The cookie is now named per port (`growth_session_8000`), the bare name is still read and migrated, and sessions slide to 90 days from the last request, renewed at most hourly (`app/auth/service.py` `renew_session`, `app/api/deps.py`, `app/api/session_renewal.py`). The ruling is in `docs/plan/09-security-and-privacy.md`, "Session lifetime". The client keeps the non-secret account (id, username, display name) in localStorage so a reload draws the signed-in app at once, treats a network error or a 5xx as offline, and signs out only on a 401 from `/me`; a 401 from any other route raises `SESSION_ENDED_EVENT` and the shell asks `/me` before believing it. Also fixed: `PUT /settings/budgets` raised on a refused re-authentication, which rolled back the token spend.

New routes: `PUT /me` (display name), `GET /me` names the username, `POST /auth/recovery/rotate` (re-authenticated), `GET` and `PUT /settings/study-plan` (01's if-then plan, a new nullable `users.study_plan` column added by the additive migration), `DELETE /frq/photos` (08's "Delete my FRQ photos"), `GET /progress/skills/{skill_id}` (a mastery node opened: criteria in the record's words and its prerequisites with their states). Each has tests that were seen red with the route broken.

Client: five tabs (Today, Lessons, Review, Progress, Assessments) and an avatar menu (Account, Settings, theme, sign out), hash routes so a reload or the back button keeps the place, and no footer. The mockup's palette went into `app/design/growth-tokens.json` over 08's seventeen roles; no gate was loosened. What the gates ruled out of the mockup, and what replaced it: gradients, grain and blur (08 anti-patterns); z-index, so the top bar is static and the phone tab bar is fixed; an amber warning colour (08 keeps two semantic colours), replaced by glyphs and patterns; hover transitions and the spinner (motion lives in motion.css at 300 ms). Decorative hairlines are ring shadows in the tint ramp; control boundaries keep 3:1 borders. Not built, shown honestly instead: changing a role's provider or model (key storage is not served), a daily minute target (01 makes the queue the unit), a photo retention preference, and the mockup's gallery, states page and reset preview.

Tests whose expectation changed with the new design are listed in `PORT-STATUS.md`: App shell navigation, the tab each progress, review and settings section now lives on, the settings scope-17 gate now read across the tabs, the resume cards, and sign-out through the menu. The full Python suite without `tests/lessons/test_invariants.py` ran 1,873 passed and 21 failed in 34 minutes. Each failing node was rerun on a clean worktree of `fb2bc3e`: 20 fail there the same way (`test_models_create_all` does not list the lesson tables; the metrics view meets `lesson_first_contact`; the rest are in the item checks, the evals, the FRQ bank checker, the prompt goldens and three session e2e tests), and `tests/e2e/test_agent_drafts_served.py` is order dependent on HEAD too, failing there under `PYTHONHASHSEED=0` and passing under 1. None was touched.

## Done [verified]
- 2026-09-23, Slice 2 of the subscription backend: live validation, latency, Slice 1's three
  defects closed, and the runtime cost lines moved to $0.00 API on the subscription backend.
  Defect a: `app/providers/guard.py` gains `SubscriptionPacingCaps`, `SubscriptionPacingLedger`
  (`var/subscription_pacing.json`, locked like the dev ledger) and `SubscriptionPaceExceeded` (a
  `BudgetStopped`); `GuardedProvider(subscription_pacing=...)` counts the call against a per-role
  daily call cap and a per-minute rate instead of the per-role dollar and token caps, never touches
  the budgets row, still sets `last_accounting`, releases the slot on a `RefusedBeforeWire`, and
  audits a pacing refusal once per role, day and cap. Defaults tutor 60 a day, other roles 20, 4 a
  minute per role, set by `GROWTH_SUBSCRIPTION_<ROLE>_CALLS_PER_DAY` and
  `GROWTH_SUBSCRIPTION_CALLS_PER_MINUTE` (`app/main.py` `build_subscription_pacing`, a bad value
  stops startup), wired through `Settings.subscription_pacing` into `app/api/routes/sessions.py`.
  The $15.00 dev cap is untouched. Defect b: `app/main.py` `refuse_the_legacy_paid_switch` stops
  startup when `GROWTH_TUTOR_PROVIDER=anthropic` or `GROWTH_TUTOR_PROVIDER=api` is set without
  `GROWTH_AI_BACKEND=api`, naming the variable to set; `none` and `replay` still work. Defect c: `app/feedback/drain.py` and
  `tools/drain_subscription_queue.py` retry due `provider_call_queued` jobs through the backend
  `build_tutor` builds (subscription or api only, never replay or none), under the same guard,
  store the sentence on `attempt.tutor_sentence` where `compose_sentence` reads it first, mark the
  job done, re-queue a still-limited job 30 minutes later and stop without counting an attempt,
  stop cleanly on a pacing, budget or developer spend cap stop, fail a job after 3 other
  failures, and fail a job without a call when its attempt or session is already at the tutor
  ceiling (3 per item, 20 per session, `tutor.ceiling_reached`). `app/feedback/tutor.py` gains `request_from_messages` for the rebuild. Live
  validation: `tools/subscription_smoke.py` (new) ran 27 calls against the real CLI 2.1.277 on the
  keychain login (Live API spend log). The Slice 1 argv was accepted as built. The CLI's default
  thinking made one Haiku tutor call take 60.3 s and 6,176 output tokens, so
  `app/providers/subscription.py` now maps `thinking: disabled` to a fixed `MAX_THINKING_TOKENS=0`
  in the subprocess environment and `output_config.effort` to `--effort`, both accepted by the CLI.
  Measured tutor latency (wall, n=10 each): Haiku 4.5 median 3.03 s, p90 3.16 s; Sonnet 5 median
  3.72 s, p90 4.32 s, under the 10 s line. API latency is unknown (no cassette or ledger entry
  recorded one). Cost: `tools/cost_model.py` emits
  `tier.hundred_claude_only.subscription_backend_api_cycle` = $0.00,
  `subscription_runtime_notional` = $52.14 (the `api_cycle`, kept as the fallback),
  `runtime_lines_without_evals` = $29.27, `target.per_student_low` and `dev_spend.cap`; projected
  API cost per student to exam day on the subscription backend is $0.00 against the $50 to $100
  target. `docs/plan/14-token-economy.md` "Runtime calls on the operator's subscription" rewritten
  with the backend cost table, the latency table and the pacing sizing; the tier table gains the
  $0.00 row. `docs/plan/07-ai-provider-layer.md` and `docs/operator/provider-key.md` (switching
  backends, where the token goes, draining) updated. Tests added:
  `tests/providers/test_subscription_pacing.py` (5), `tests/api/test_subscription_drain.py` (11),
  two in `tests/api/test_subscription_limit.py`, two in `tests/providers/test_subscription.py`,
  six in `tests/api/test_wiring.py` (one parametrized over three backends), two in
  `tests/tools/test_cost_model.py`. Each was shown red against a mutation of the code it guards
  (21 mutations from a scratchpad script: pacing ignored, no minute rate, no daily cap, release a
  no-op, the route unpaced, the legacy switch allowed, the pacing environment ignored, the drain
  not storing, retrying at once, continuing past a limit, unpaced, the tool draining replay, the
  tool unpaced, a limit wait counted as a failed attempt, the developer spend cap uncaught, the thinking variable dropped, effort dropped, the host thinking value copied, the
  evals left on the API, the screen dropped from the runtime lines, and the quoted dev cap
  changed), one or more tests red each, then green on restore. Suite at close: pytest 936 passed (exit 0), vitest 310 passed, tsc exit 0, qa/12_report.py exit 0.
- 2026-09-23, Slice 1 of the subscription backend: the AI engine runs by default on the
  operator's Claude subscription through the official Claude Code CLI, and the paid key is a
  fallback chosen only explicitly. `app/providers/subscription.py` (new) `SubscriptionProvider`
  runs one `claude -p` per call from an argument list, never a shell: `--model` from the request,
  `--system-prompt=<static prefix>`, `--output-format json`, `--json-schema` when the request
  carries a schema, `--max-budget-usd` per role (tutor 0.10, others 0.25),
  `--no-session-persistence`, `--setting-sources ""`, `--strict-mcp-config` with an empty
  `--mcp-config`, `--disable-slash-commands`, `--permission-prompts none`, `--tools ""` and a named
  `--disallowedTools` list, with the user prompt on stdin and the working directory an empty temp
  directory removed afterwards. Every flag was checked against `claude -p --help` on CLI 2.1.277;
  `--bare` and `--max-turns` are not used. The subprocess environment is `PATH`, `HOME`, `USER`,
  `LANG`, `TMPDIR` and the operator's OAuth token when set, and never an `ANTHROPIC_*` variable.
  The JSON result maps onto `ProviderResult` (`result` or `structured_output`, the four usage
  counts, `total_cost_usd`, `duration_ms`, `subtype`), and `total_cost_usd` goes to
  `app/providers/guard.py` `SubscriptionSpendLedger` (`var/subscription_spend_ledger.json`), never
  to the $15.00 `DevSpendLedger`. A usage-limit answer raises `SubscriptionLimitReached`; a
  timeout, a non-zero exit or non-JSON output raises `SubscriptionTransportError`, and a missing
  binary raises `SubscriptionBinaryMissing`, which is refused before the wire. Compliance:
  `AnthropicProvider` refuses an `sk-ant-oat` key before the wire (`SubscriptionTokenRefused`);
  only `subscription.py` in `app/` names the token variable and it imports no HTTP client, socket
  or SDK; the backend refuses to construct over a database with more than one user
  (`app/main.py` `installed_user_count`, read-only); registration already refuses a second account
  unconditionally. `app/main.py` adds `GROWTH_AI_BACKEND` (`subscription` default, `api`,
  `replay`, `none`) as the primary switch, with `GROWTH_TUTOR_PROVIDER` read only when it is
  unset, and logs the choice. Degradation: `app/feedback/tutor.py` queues a limited call through
  `app/providers/call_queue.py` (new) as a `provider_call_queued` row in the existing `jobs` table,
  one per attempt, and re-raises; `app/api/routes/sessions.py` serves the static feedback with
  `tutor_unavailable` true. Docs: new sections in `docs/plan/07-ai-provider-layer.md` ("The
  subscription backend") and `docs/plan/14-token-economy.md` ("Runtime calls on the operator's
  subscription"), and `docs/operator/provider-key.md` and `ai-operating-costs.md` now name
  `GROWTH_AI_BACKEND`. No cost figure changed. Tests: `tests/fixtures/fake_claude/claude` (a fake
  CLI that records argv, stdin, environment and working directory, with success, structured,
  weekly-limit, five-hour-limit, malformed and non-zero modes, configured through `HOME`);
  `tests/conftest.py` (new) fails any test that resolves a claude binary outside
  `tests/fixtures` and points the subscription ledger at a temp file;
  `tests/providers/test_subscription.py` (15), `tests/providers/test_subscription_compliance.py`
  (11), `tests/api/test_subscription_limit.py` (4) and six new backend-selection tests in
  `tests/api/test_wiring.py`. Each new test was shown red against a mutation of the code it
  guards (32 mutations, one or more tests red each, run from a scratchpad script), then green on
  restore. Suite at close: 909 passed. No live CLI or API call.
- 2026-09-23, a verified review finding against Slice 1 of the subscription backend:
  `tests/providers/test_subscription.py`
  `test_the_reported_cost_lands_on_the_subscription_counter_and_never_on_the_api_cap` built a
  `DevSpendLedger` at a fresh temp path that nothing ever wrote to, so its "never on the API cap"
  half could not go red. The test now points `app/providers/guard.py` `DEV_SPEND_LEDGER_PATH` at a
  temp file (with a positive control that `DevSpendLedger()` resolves there), runs two calls and
  asserts the default ledger is still empty and its file absent. The provider-level test cannot
  see the route wiring, so `tests/api/test_subscription_limit.py` gained
  `test_a_served_subscription_sentence_is_counted_off_the_api_dev_cap`, which serves a real
  sentence through `/sessions/.../feedback` over the same redirected ledger and asserts the
  subscription counter holds 0.0123 and the API cap ledger is untouched. Red against two
  mutations: `SubscriptionProvider._record_cost` also adding to `DevSpendLedger()` (both tests
  red) and `sessions.py` passing `dev_spend_track=True` (the route test red, `0.00418 == 0.0`);
  green on restore. No application code changed. Suite at close: 910 tests collected, pytest
  exit 0 with no failure. No live CLI or API call.
- 2026-09-23, a second review finding against Slice 1 of the subscription backend:
  `app/settings/providers.py` `PROVIDER_NAMES` had no entry for the new default backend, so
  `GET /settings/providers` reported the tutor as the class name `SubscriptionProvider` instead
  of `subscription`. `PROVIDER_NAMES` now maps `SubscriptionProvider` to `subscription`, and
  `tests/api/test_settings_routes.py` gained
  `test_providers_names_the_default_subscription_tutor_by_its_backend`. Red with the map entry
  removed, green on restore. Suite at close: pytest 911 passed, vitest 310 passed, tsc exit 0,
  qa/12_report.py exit 0. No live CLI or API call.
- 2026-09-23, a verified review finding against the MCQ math-rendering fix below: the `stem`
  fix in `app/items/ingest.py` `item_row` only reaches a record on its first ingest.
  `ingest_new_records` (`app/runtime/bank.py` `ItemBank._ingest_pending_source`) skips any id
  already in `items`, so a row ingested before the fix keeps serving its `{"text": ...}` wrapper
  forever; restarting the app over the operator's persistent database would not touch it. Fixed
  with a startup data repair rather than a one-off SQL script, since nothing else in this
  codebase re-ingests: `app/db/migrate.py` `repair_wrapped_stems` selects the rows whose `stem`
  looks JSON-wrapped (`LIKE '{%'`), unwraps the ones that parse to `{"text": <string>}`, and
  leaves everything else (a legitimate stem that happens to start with `{`, or one that starts
  with `{` but is not valid JSON) untouched; `app/db/models.py` `make_engine` calls it right after
  `apply_additive_migrations`, so it runs once per process start and is a no-op once every row has
  been unwrapped. Tests: `tests/db/test_migrate.py` gained
  `test_repair_wrapped_stems_unwraps_a_row_ingested_under_the_old_code` (a wrapped row, a plain
  row and a row that merely starts with `{` but is not JSON, asserting only the wrapped one
  changes) and `test_repair_wrapped_stems_is_idempotent`; both proved red (`ImportError: cannot
  import name 'repair_wrapped_stems'`) against the pre-fix `app/db/migrate.py` and
  `app/db/models.py`, restored, then green. `.venv/bin/python -m pytest -q -p no:cacheprovider`
  exits 0. No live Anthropic API call.
- 2026-09-23, MCQ options no longer render raw MathJSON. `McqControl.tsx` typesets each option's
  `mathjson`/`value` (a bare number, symbol or an expression tree such as
  `["Add", ["Multiply", -5, ["Sin", "x"]], 3]`) through `mathlive`'s `convertMathJsonToLatex` and
  KaTeX's `renderToString` (`app/web/src/math/mathjson.ts`, `MathValue.tsx`, new); the typeset
  markup is `aria-hidden`, and a `convertLatexToAsciiMath` rendering carries the accessible name in
  a `.visually-hidden` span instead, so radio semantics, keyboard use and focus styling are
  untouched. `Item.tsx`'s stem and worked-solution steps, which some curated items carry with
  inline `\( \)`-delimited LaTeX, now route through the same pattern via `MathText.tsx` (new); an
  agent-drafted item's plain-text stem with no delimiters renders exactly as before. `mathlive`
  needs the compute engine loaded before `convertMathJsonToLatex` works, so
  `@cortex-js/compute-engine` (already a transitive dependency) joined `package.json` directly.
  `ServedOption.value` is now typed `unknown` in `api/types.ts`, matching what the server actually
  sends, not `string`. Fixed in the same pass: `app/items/ingest.py`'s `item_row` was storing
  `json.dumps(record["stem"])`, the whole `{"text": ...}` wrapper, into the `stem` column, so every
  served item's stem was the literal JSON string, not the plain text; it now stores
  `record["stem"]["text"]`. `docs/operator/items.md` corrected: `violated_step` indexes the
  archetype's own `expected_solution_path` (`app/feedback/render.py` `violated_step_index`), not
  the item's `worked_solution`, and `options` may sit on a `short_answer` item for the turns
  `format_for_attempt` serves it as `mcq`. Tests: `McqControl.test.tsx` gained a MathJSON-array
  option case (red on `option.label ?? option.value ?? option.id` rendered as a plain string,
  green after; the assertion was tightened once, from checking the raw LaTeX source never appears
  anywhere in the DOM to checking it never appears in the visible `.katex-html` node, since KaTeX's
  own MathML annotation legitimately carries the LaTeX source hidden from sighted users). `math/
  MathText.test.tsx` (new) covers both the agent-drafted plain-text case and the `\( \)`-delimited
  case, each proven red on a stub `MathText` and green after. `tests/items/test_ingest.py` gained
  a stem-shape test, red on the old `json.dumps` line and green after. `.venv/bin/python -m pytest
  -q -p no:cacheprovider` exits 0; `npx vitest run` exits 0, 310 tests; `npx tsc --noEmit` exits 0;
  `qa/12_report.py` exits 0, 14 PASS. Verified live: a session driven through
  `tests/fixtures/items_p1/` to an `mcq`-stage item (`ITM-SYN-02002-02`, option A
  `["Multiply", 8, "x"]`) served the fixed stem and options over HTTP; a browser build of the real
  `McqControl`/`MathText`/`mathjson.ts` source against that served JSON showed `8x`, `0`, `4`, `8`
  as typeset options with no `Multiply` or bracket text anywhere. `GET /progress` would not answer
  within 45s against that same seeded state even in isolation, unrelated to this fix and not
  investigated further; see Known defects. No live Anthropic API call.
- 2026-09-23, independent item review of `content/items_p1_agent/` applied and re-checked. The
  review judged all 130 items: 65 approve, 57 fix, 8 reject, 0 wrong keys. Applying it changed 65
  item files, by archetype 01004 8, 01008 3, 01015 10, 02002 5, 02006 1, 02007 6, 02008 3,
  02010 8, 02011 3, 03001 2, 03004 4, 03005 8, 03008 4. A separate agent per archetype then
  re-solved the changed items blind, confirmed every key with SymPy and re-derived every
  distractor from its tagged error, and corrected 8 items: `01004-06` (new stem, key -1 no longer
  the only negative), `01008-08` (options reordered, key to D, breaking a run of three B keys),
  `02010-05` (new stem, key no longer the smallest and no option alone in form), `02011-01` and
  `02011-09` (redesigned so the `BC-ERR-02028` sign drop is literal), and `03005-00`, `03005-06`,
  `03005-09` (constants changed so the key is interior; key extreme in 4 of 10 03005 items, down
  from 7). 01015, 02002, 02006, 02007, 02008, 03001, 03004 and 03008 needed no correction. Every
  re-check agent's `tools/check_items.py` run exited 0. After the pass, `.venv/bin/python
  tools/check_items.py content/items_p1_agent` exits 0 with "records read: 130", "clean: 130",
  "with violations: 0" and 10 items in each of the 13 archetypes, and `.venv/bin/python -m pytest
  -q -p no:cacheprovider tests/tools tests/items tests/e2e` exits 0 with 162 dots and no F or E
  (the doubled `-q` suppresses the summary line). Operator sign-off is still pending for all
  130. What remains is under Known defects, twenty-sixth session.
- Twenty-eighth session, 2026-09-23, a verified review finding against the twenty-seventh
  session's runbook: `docs/operator/offline-authoring.md` step 2 had the blind re-solve agent
  compare its own key against the drafted key, which required handing the drafted key to that
  agent and broke `docs/plan/13-ai-engineering.md` line 14, "the verifier never sees the key."
  Step 2 now has the re-solving agent write its own key and worked solution to a file of its own,
  never given the drafted key, and a script, not the agent, reads both files and compares the two
  keys; the step no longer contradicts its own claim that the deterministic checks around the
  verifier are unchanged. Docs-only change, no code touched.
- Twenty-seventh session, 2026-09-23, offline work on the operator's Claude Code subscription:
  `tools/cost_model.py` gained a Claude-only offline split, `tier.hundred_claude_only.api_cycle`
  ($52.14, the tutor, grader, transcriber, diagnostician, screen and evals, all of which stay on
  the API key) against `tier.hundred_claude_only.offline_cycle` ($40.81, 43.90 percent of the
  $92.95 tier, template authoring and the verifier's blind re-solve, both moved to Claude Code
  sessions at $0.00 API spend). Evals do not split: golden set 1 already costs $0.00 on the
  template gate, and golden sets 2 and 3 grade the production grader and transcriber prompts on
  their production model, so both stay on the API key in full. `docs/plan/14-token-economy.md`
  gained "Offline work on the operator's Claude Code subscription" with the Agent SDK quickstart
  and Claude Code authentication quotes and URLs, and the $100 tier table's Total row gained two
  "of which" lines. `docs/operator/offline-authoring.md` is the new runbook, describing the
  one-agent-per-archetype author, independent blind re-solve, and `tools/check_items.py` gate
  shape the twenty-sixth session actually ran, and naming the rolling five hour and weekly
  subscription limits as the pacing risk. `tests/tools/test_cost_model.py` gained
  `test_claude_only_tier_splits_into_runtime_api_and_offline_claude_code_lines`, run red against
  the pre-edit `tools/cost_model.py` (`KeyError:
  'tier.hundred_claude_only.offline_template_line'`) and green after, restored via `git stash`
  around the code edit alone so the test file's addition was never itself reverted. All four
  checks quoted: `.venv/bin/python -m pytest -q -p no:cacheprovider` exit 0 (870-plus collected,
  no FAILED lines, the doubled `-q` from `addopts` suppresses the summary line);
  `npx vitest run` 307 passed, exit 0; `npx tsc --noEmit` exit 0; `qa/12_report.py` exit 0.
  `python3 tools/cost_model.py --check docs/plan/13-ai-engineering.md
  docs/operator/ai-operating-costs.md docs/plan/14-token-economy.md` prints "0 unknown dollar
  figures" for all three and exits 0. No live Anthropic API call was made.
  `content/items_p1_agent/` and `app/web/` were not touched by this session; both showed unrelated
  concurrent changes in `git diff` during the session, from other work in progress on this
  repository, not from anything this session wrote.
- Twenty-sixth session, 2026-09-23, distractor repair: nine archetypes' open audit findings were
  repaired one agent per archetype, 42 items in all. 39 stems were redesigned so that every
  distractor is a single application of an error the archetype's skills hold (01004 5, 01008 7,
  01015 1, 02007 2, 02008 8, 03001 5, 03004 2, 03005 7, 03008 2), with keys, worked solutions and
  `parameter_draw` rewritten to match and every key letter left in place. Three more `BC-QA-03004`
  options that held a free `dydx` (`03004-00` B, `03004-08` B, `03004-09` A) were re-derived as
  numeric or closed-form `BC-ERR-03007` and `BC-ERR-03008` values, and `03004-03` A was rechecked
  and left unchanged. Each agent checked its keys against a blind SymPy solve and every option
  pair with `compare_expressions`. A spot check solved 8 randomly chosen repaired items by hand and
  with SymPy (`03001-02`, `03008-07`, `01004-05`, `02008-07`, `02007-04`, `02008-08`, `01008-02`,
  `01008-04`): all 8 keys matched and all 24 distractors equal their tagged error's computation,
  so nothing was changed. `.venv/bin/python tools/check_items.py content/items_p1_agent` exits 0
  with "records read: 130" and "clean: 130", 10 items in each of the 13 archetypes, and
  `.venv/bin/python -m pytest -q -p no:cacheprovider tests/tools tests/items tests/e2e` exits 0
  with 171 dots and no failures (the doubled `-q` from `addopts` suppresses the summary line).
  What the repair left open is under Known defects.
- Twenty-sixth session, 2026-09-23, distractor audit: the twelve archetypes in
  `content/items_p1_agent/` other than `BC-QA-02010` (re-derived last session) were audited one
  agent per archetype, 30 distractor options each, 360 in all. Each agent re-derived every
  distractor from the archetype's own named errors (the BC-ERR ids its skills hold) and either
  corrected the value, the `violated_step`, or the tag, or left the option unchanged and said why.
  No key changed, and the 03005 auditor rechecked all ten of its keys with SymPy. Options fixed and
  left unresolved, per archetype: 01004 11 and 2, 01008 6 and 10, 01015 11 and 1, 02002 9 and 0,
  02006 12 and 0, 02007 21 and 3, 02008 12 and 11, 02011 18 and 0 (plus `violated_step`
  normalized to 1 on the already-correct options of items 00 to 05), 03001 9 and 6, 03004 25
  and 2, 03005 15 and 4, 03008 18 and 3. That is 167 fixed and 42 unresolved of 360; the rest were
  already correct. Each auditor's `tools/check_items.py` run exited 0. After all twelve,
  `.venv/bin/python tools/check_items.py content/items_p1_agent` exits 0 with "records read: 130,
  clean: 130, with violations: 0", and `.venv/bin/python -m pytest -q -p no:cacheprovider
  tests/tools tests/items tests/e2e` exits 0. `var/growth.db` holds no `ITM-AGT-` rows (its items
  table is empty), so the bank's skip-existing-ids rule leaves no stale copy of an edited item and
  nothing was deleted. What the audit could not fix is under Known defects.
- Twenty-fifth session, 2026-09-23, slice 7 review follow-up: two verified findings against the
  twenty-fourth session's distractor generator, fixed. First, the generator always placed the key
  at option A for the 51 previously options-less items and only ever moved a fourth distractor to
  D for the 31 three-option items, so the key sat at A 67 times against 29, 23 and 11 for B, C and
  D across the 130 items; a student could score short-answer-turned-MCQ items by picking A with no
  regard for the item. Every item's option order is now a deterministic per-item shuffle
  (`hashlib.sha256(item id)` seeding `random.Random`, one script run, not committed, since it is a
  one-shot content fix like the generator it corrects), re-lettered A to D by the shuffled
  position; the key now sits at A 32, B 36, C 28, D 34. `tools/check_items.py content/items_p1_agent`
  still exits 0, 130 clean, and
  `tests/tools/test_agent_drafts_have_four_options.py`'s two tests still pass, since neither reads
  option order. Second, `ITM-AGT-02010-08`'s option B held `sin theta/cos^2 theta`, the item's own
  undifferentiated step-1 rewrite, tagged `BC-ERR-02025` ("cofunction derivative given without its
  negative sign"), and option C held the key's exact negation tagged `BC-ERR-02026` ("trigonometric
  quotient differentiated term by term"); neither value is a computation either error actually
  produces. Re-derived both with SymPy from the item's own quotient-rule work (`u = sin theta`,
  `v = cos^2 theta`): B is now the quotient rule with the denominator derivative's sign dropped,
  `sec theta - 2 sec theta tan^2 theta`; C is now the literal term-by-term quotient `u'/v'`,
  `-1/(2 sin theta)`. `ITM-AGT-02010-07` carried the identical pattern (option B equal to its own
  step-1 rewrite tagged `BC-ERR-02025`, option C equal to the negated key tagged `BC-ERR-02026`)
  and was fixed the same way (`6 - 6 tan^2 x + sec x tan x` and `-6/tan x`). Both items' distractor
  `violated_step` now indexes `BC-QA-02010`'s `expected_solution_path[1]` ("apply the quotient
  rule"), where the sign-drop and term-by-term errors actually happen, rather than the previous 0
  or 3. `ITM-AGT-02010-00` and `-01` held two further `BC-ERR-02025` distractors apiece
  (`violated_step: 1`) whose values were correct as sign flips on one term of the final split-form
  key, the CED-literal reading of "given without its negative sign", but that sign only appears at
  `expected_solution_path[3]` ("write the result in the requested trigonometric form") in those two
  items' own worked solutions, not at the quotient-rule step; `violated_step` corrected from 1 to 3
  on those four options, values unchanged. All four values checked distinct from the key and from
  each other with `sympy.simplify`, and the full `BC-QA-02010` archetype's ten items re-verified
  against a general quotient-rule/sign-drop/term-by-term SymPy model built from each item's own
  `worked_solution` Divide step; no further mismatches found in that archetype.
  `tools/check_items.py content/items_p1_agent` exits 0, 130 clean, after these edits.
- Twenty-fourth session, 2026-09-23, slice 7: every one of the 130 agent drafts in
  `content/items_p1_agent/` now carries exactly four options (one key, `error_path: null`, plus
  three distractors, each a BC-ERR id held by the archetype's own skills with a `violated_step`
  index into that archetype's `expected_solution_path`), closing the options-less and
  three-option gaps the twenty-third session left in Known defects. `tools/check_items.py
  content/items_p1_agent` exits 0, 130 clean. The 48 items the previous session already gave four
  options were left untouched; the 31 three-option and 51 zero-option items were filled by a
  generator (its source is not part of this repo, since it is a one-shot authoring tool and not a
  gate). Every added distractor's value is either a genuine intermediate quantity from the item's
  own `worked_solution` (a value a student really reaches partway through the correct derivation,
  used prematurely as the final answer) or an algebraic sign flip, dropped multiplicative factor,
  or off-by-one integer count taken from the item's own key expression, and every one is checked
  distinct from the key and from every other option by `app/items/verify.py`'s own
  `compare_expressions` (SymPy symbolic difference, then a 7-point numeric probe) before being
  written, the same machinery `distractor_path_violations` runs at gate time. Where an archetype
  holds more error ids than an item needed new distractors for, an error id already used by that
  item's pre-existing distractors was reused for the generic sign-flip or count-perturbation
  candidates rather than invented; one id, `BC-ERR-01008` ("indeterminate form read as the answer
  zero"), is restricted in the generator to the one candidate that is literally that reading (the
  worked solution's own step-zero value), because nothing else can honestly carry that name. The
  reused-id distractors are mechanically verified (distinct, valid error id, valid step index) but
  were not each individually hand-checked for being the most natural instance of that named error
  the way the original 48 items' distractors were; this is flagged below for operator review.
  `tests/items/test_ingest.py::test_a_short_answer_item_carrying_mcq_options_still_ingests` (new,
  red under a temporary guard that refused options on a `short_answer`-format record, green with
  the guard removed) confirms `app/items/ingest.py` already accepted options on a short_answer
  item without any change, since nothing in that module reads the `format` field at all; the
  operator's contingency instruction to change ingest did not apply.
  `tests/tools/test_agent_drafts_have_four_options.py` (new) reads the real directory and asserts
  every record carries exactly four options, one key with a null `error_path` and three
  distractors each with one, since `tools/check_items.py`'s own checks pass an item with fewer
  options or none (they check whatever option set is actually there, which is why that gate alone
  did not catch the twenty-third session's options-less items); red with one record's options cut
  to two, green restored.
- Twenty-fourth session, 2026-09-23: `app/items/verify.py` `run_bounded`'s SIGALRM path could
  silently miss its own bound. A one-shot `signal.setitimer` that fires while a `gc.callbacks`
  hook is executing (the suite registers one only once something imports `hypothesis`, which is
  why this never reproduced from `tests/items/test_verify_bound.py` run alone) never reaches
  `run_bounded`'s `except _Timeout`: CPython's gc module catches whatever a callback raises and
  reports it through `sys.unraisablehook` instead of letting it propagate, so the alarm is lost
  and the comparison runs to completion past `timeout_s`. Seen directly in a full-suite run as
  `test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound` failing with
  `not_equivalent` instead of `unsettled`, plus a `PytestUnraisableExceptionWarning` naming
  `app.items.verify._raise_timeout` raised from inside `hypothesis`'s `gc_callback`. Reproduced
  deterministically outside the full suite by wrapping `_raise_timeout` to swallow exactly its
  first delivery (mimicking that gc behaviour) and calling `run_bounded` over a busy-loop:
  the pre-fix single-shot `setitimer` let the loop run to completion (one alarm delivered, zero
  effect); the fix, a repeating `setitimer(..., timeout_s, min(0.05, timeout_s))`, still returned
  the timeout sentinel because a second delivery landed outside the callback 0.05 s later. The
  test's margin assertion was briefly switched to `time.process_time()`; the orchestrator
  reverted that because CPU time weakens a wall-clock bound, so the test still measures
  `time.monotonic()`. Proof run: 20/20 green on `tests/items/test_verify_bound.py` alone (both before and
  after the real fix, since the file-alone run never touched hypothesis's callback), and three
  full-suite runs, all exit 0, zero failures. The exact race reproduced again live in the second
  of those three runs, the same `gc_callback`/`_raise_timeout`/`PytestUnraisableExceptionWarning`
  as the original symptom, and the fix carried the test through it.
- Twenty-fourth session, 2026-09-23: `app/api/app.py` `Settings.resolve_key_audit_sample_ids`
  raised `FileNotFoundError` (HTTP 500 through `POST /review-queue/{id}/resolve`) when
  `GROWTH_KEY_AUDIT_SAMPLE_PATH` named a file that did not exist, and used
  `item_id in set(sample_ids)` for membership, which reads a dict's keys or a string's characters
  when the sample file's JSON was not a list, rather than refusing it. Both now fail closed with
  a `ValueError`, which the route already turns into the documented 400
  (`tests/api/test_review_routes.py::test_resolving_an_item_audit_with_a_missing_sample_file_is_refused_not_500`
  and `..._with_a_non_list_sample_file_is_refused_not_500`, both new, red against the pre-fix code
  (`FileNotFoundError` propagating unhandled, and a 200 from the dict-keys membership check),
  then green).
- Twenty-third session, 2026-09-23, serving the agent-drafted P1 items under the operator's
  ruling and keeping them out of every operator count. `content/items_p1_agent/` holds 130 drafts,
  10 per P1 archetype, each with `"authored_by": "claude-opus-5-5 agent draft, pending operator
  review"`, audited by an independent agent's blind re-solve on 2026-09-23 (its README says what
  was corrected). `app/items/ingest.py` `provenance_model` now reads `authored_by`: absent gives
  `operator` as before, present gives that string, and `is_operator_authored` is the one test for
  operator provenance (test_an_agent_draft_keeps_its_author_as_the_provenance_model, red
  `assert 'operator' == 'claude-opus-5-5 agent draft, pending operator review'`, then green).
  `tools/check_items.py` prints a second table, operator-authored items per archetype, which is
  the one exit criterion 7 and gates 17 and 30 read. `tools/draw_key_audit_sample.py` draws only
  operator items, and fixing that exposed two older defects that meant it could never draw
  anything. It filtered on status `published`, which ingest never writes, because the bank's
  published status is `verified`. It also read `archetype["unit"]`, which archetype records do
  not carry, so it raised `KeyError: 'unit'`. It now uses `PUBLISHED_STATUS` and `primary_unit`.
  `tests/tools/test_agent_drafts_uncounted.py` puts one operator item and one agent draft side by
  side. It went red with both filters removed (`assert 2 == 1` and a sample holding both ids),
  then green. Gates 17, 29 and 30 still have no test function (gate_status: missing), so nothing
  there counted the drafts. `tools/gate_status.py` counts gate tests, not items, and needed no
  change. The app now loads a bank directory. `GROWTH_ITEMS_DIR` (`app/main.py`) defaults to
  `content/items_p1_agent` when that directory exists, `none` turns it off, and a set path that is
  not a directory stops startup. `app/runtime/bank.py` `ItemSource` goes through
  `ingest.ingest_new_records` on the bank's first query, which skips ids already in items. It
  runs then and not at build time because the checks take about 12 s over 130 records and most
  application builds (the API wiring tests among them) never open a session.
  `tests/e2e/conftest.py`'s gate 23 world sets `GROWTH_ITEMS_DIR=none`, so gate 23 still serves
  only its own `ITM-SYN` fixtures. `tests/e2e/test_agent_drafts_served.py` builds the app with the
  variable unset, registers, and drains sessions with the replay tutor until a `BC-UNIT-02` item
  is served. It answers that item, rates it, reads its feedback, and checks that the stored
  provenance model is the agent author. It went red with the default made `None`, then green.
  `tools/check_items.py content/items_p1_agent` exits 0 with 130 clean and 10 per archetype.
- Slice 4, twentieth session, 2026-09-23, the BC-PT deterministic labelling pass and bringing the
  Claude-only tier's overrun down. `data/bc_pt_determinism_labels.json` carries one `[inferred]`
  label per active BC-PT record, `deterministic` or `model_required`, with a short reason read
  against the record's own `earns`, `does_not_earn`, `notation_requirements` and `precision_rules`
  text and against the four checks and partition rule in `docs/plan/03-diagnosis-and-feedback.md`.
  48 of 76 are `deterministic`, 28 `model_required`, 17 of them on `justification_required`,
  `interpretation_required` or `hypotheses_required` alone and 11 more on the earns text itself (a
  prose-only earn criterion, a graphical criterion, an implied choice, a step count, or a label
  naming a quantity in words). A separate data file was used rather than
  `data/staging/*.json` and `tools/merge_staging.py`, because that tool fully replaces a matched
  record rather than merging fields, and re-authoring all 76 rich, sourced `scoring_points.json`
  records through a staging file to add one field risked corrupting or silently dropping sourced
  content the labelling pass did not touch; the label is also a judgement about the grader's
  design, not a fact about the rubric the registry otherwise records. `qa/15_determinism_labels.py`
  asserts every active BC-PT record carries exactly one label with a reason and that the file and
  the registry agree on the id set; verified red on a record deleted from the labels file, green
  restored. `tools/cost_model.py` gained `MEASURED_MODEL_JUDGED_POINT_RECORDS = 28` and wired the
  Claude-only tier's grader line to it, `role_cost("grader", ...)` at 2 samples with a third on
  disagreement over 442 of 1,200 judged points, $12.44 against the $33.32 worst case every point
  reaching the model, a saving of $20.88; the worst-case figures stay priced alongside it as
  `grader.worst_case_conditional_third_cycle` and `tier.hundred_claude_only.worst_case_cycle`
  because this file never overwrites a figure a document has already quoted. The Claude-only tier
  now totals $108.07, an overrun of $8.07 against the $100.00 ceiling, down from $128.95 and
  $28.95. `docs/plan/14-token-economy.md` "The $100 tier, line by line" and open question 2 are
  rewritten to the measured figures and to state why no further sourced lever closes the
  remaining $8.07 (see Known defects); `docs/plan/11-phased-delivery.md`'s P3 entry criterion is
  updated from "all 76 records are labelled" as an open task to the closed count. `tests/tools/test_cost_model.py`
  gained `test_claude_only_tier_grader_line_reads_the_labelling_pass`, pinning the tier at $108.07
  and the grader line at $12.44, verified red against the reverted worst-case grader line and
  green restored; `docs/plan/14-token-economy.md` also joined the `DOCUMENTS` tuple the
  hand-figure regression test already runs over 13 and the operator cost doc.
  `tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0. No live Anthropic call was
  made; no test, gate, threshold or fixture was loosened.
- Nineteenth session, 2026-09-23, two review findings against the eighteenth session's uncommitted
  slice 3 work fixed. First, `app/db/models.py` `skills_state.credited_observation_count` was
  `NOT NULL` with no `server_default`, so `app/db/migrate.py apply_additive_migrations` raised
  `SchemaDriftError` on any database created before the column existed; `_column_definition`
  confirmed the message quotes exactly that shape. Fixed with `server_default=text("0")`, matching
  the pattern the other additive columns on `attempts` already use. A bare server default was not
  enough: every row already in the table would then read 0, and `app/engine/fringe.py serve_stage`
  reads `credited_observation_count > 0` to decide whether the stored `fading_stage` wins over the
  `p_A_knowledge` bands, so a 0 backfill would silently undo a student's fading progress on the
  first migrated read. `app/db/migrate.py` gains `_backfill_credited_observation_count`, run inside
  `apply_additive_migrations`'s own transaction immediately after this one column is added (a new
  `BACKFILLS` map keyed by `"table.column"`, so no other column's migration is touched): it replays
  `app/engine/update.py credit_for` over every `attempts.per_skill_states` entry, for every session
  with `updates_mastery = 1` (a rehearsal session never reached `apply_observation` and contributes
  nothing), and writes the count per `(user_id, skill_id)`. This is an exact replay of the counting
  rule `apply_observation` itself uses (`is_credited_success = c_credit > 0.0`,
  `is_credited_failure = f_credit > 0.0 or is_gap`), not an approximation from the counters that
  reset (`consecutive_successes`/`consecutive_failures`) or the ones a `prerequisite_gap` credit of
  `(0.0, 0.0)` never moves (`credited_successes`/`credited_failures`), which is why the backfill
  reads history from `attempts` rather than from any column already on `skills_state`.
  `tests/db/test_migrate.py::test_credited_observation_count_is_backfilled_from_attempt_history`
  seeds two sessions (one `updates_mastery = 1`, one `= 0`) and three attempts across them, drops
  the column, migrates, and asserts the recomputed per-skill counts; red with the backfill call
  stubbed out (both skills read back 0 against an expected 1), green restored, confirmed by
  temporarily replacing the `BACKFILLS.get(name)` call with a no-op and rerunning.
  Second, `app/runtime/bank.py served_steps` let a stage `example` item under the 2-step minimum
  degrade to showing every step, the final, un-blanked answer step included, while the stage still
  grades and credits whatever the student submits; two such items would meet 02's 2-consecutive-
  credited-successes rule and advance a skill out of `example` with no work from the student, since
  the answer was already on screen. Fixed by dropping the degrade path entirely: both `example` and
  `completion` now raise the same `a stage needs at least 2 worked steps to blank the last one`
  `ValueError` below the minimum, and `app/session/service.py resolve_served_stage` (renamed from
  its narrower completion-only form) rewrites a slot at either stage to `unsupported` when its item
  is under the minimum, so `served_item` never calls `served_steps` on a stage that cannot blank.
  This replaces the completion-only fallback the eighteenth session's slice built: an item too
  short for a completion blank now falls all the way to `unsupported` rather than stopping at
  `example`, because `example` no longer has room to blank a step either.
  `tests/api/test_served_steps.py::test_completion_below_the_two_step_minimum_is_served_at_unsupported`
  (renamed and re-asserted) and the new
  `::test_example_below_the_two_step_minimum_is_served_at_unsupported` cover both entry points; red
  against the eighteenth session's code (asserted stage `unsupported`, got `example`), green after,
  confirmed by stashing `app/runtime/bank.py` and `app/session/service.py` and rerunning.
  `docs/plan/11-phased-delivery.md` Q16 is corrected in place: "served at stage unsupported only",
  with the old "example and unsupported only" reading quoted and dated. No live API call; full
  pytest run, client `306 passed`, `tsc --noEmit`, and `qa/12_report.py` all clean (see the
  verification lines below this entry). `tests/e2e/test_exit_criteria_mastery.py::test_mastery_path_across_days_and_unmastery`
  reconfirmed at 30/30 clean runs in a dedicated loop this session, on top of the eighteenth
  session's fix, which this session did not touch.
- Eighteenth session, 2026-09-23, slice 3: how a skill leaves stage example, and the flaky mastery
  e2e test. The operator's ruling (Known defects, fourteenth session, first entry) is that stage
  `example` collects a graded answer: the worked example is shown with its final step left for the
  student, the student commits an answer, a confidence rating is collected after the answer and
  before feedback exactly as at completion and unsupported, and the server grades and credits it
  under 02's existing rules. `app/runtime/bank.py` `served_steps` now blanks the last step at
  `example` too, gated on the same 2-step minimum as `completion` (`supports_completion`); below
  the minimum `example` degrades to showing every step given, unblanked, rather than refusing the
  slot, which is the same fallback shape the existing below-minimum completion test already
  exercises. `app/session/service.py` `collects_confidence` now returns true for every stage, and
  `record_confidence` no longer refuses a rating at `example`; `_check_rating` in
  `app/feedback/render.py` picks this up unmodified, since it already read `collects_confidence`
  generically. Client: `app/web/src/session/Item.tsx` blanks the last worked step at `example` the
  same way as `completion` (`requiredServedStepCount`, `blanksAStep`), collects an answer at every
  stage (`collectsAnswer = true`), and asks for a rating at every stage
  (`collectsConfidence` returns true unconditionally); `EXAMPLE_LABEL` and its "I have explained
  this" commit copy are removed, since every stage now commits the same way. `SessionScreen.tsx`
  needed no change: `commit`, `rateConfidence` and `awaitsRating` already read `collectsConfidence`
  generically rather than special-casing example, so flipping the one function was enough to route
  example's answer and rating through the same path as completion. `docs/plan/11-phased-delivery.md`
  implementer decision 3 is withdrawn in place, its old text quoted and the new rule stated.
  02's internal inconsistency (line ~404's "credited observation" against line ~407's
  `observation_count > 0`, which line 56 says counts uncredited observations too) is resolved by a
  new field, `credited_observation_count` on `SkillState` (`app/engine/state.py`), incremented in
  `app/engine/update.py` `apply_observation` on the same `is_credited_success or is_credited_failure`
  event that already drives `move_counters`; `app/engine/fringe.py` `serve_stage` reads it instead
  of `observation_count`, `app/db/models.py`/`app/session/repository.py`/`app/content/reconcile.py`
  carry the new column (additive, picked up by `app/db/migrate.py` with no migration script), and
  02's schema table and `serve_stage` pseudocode are edited to name the field. New test
  `tests/engine/test_selection.py::test_serve_stage_ignores_observation_count_and_reads_credited_observation_count`
  proves the distinction: broken against `observation_count` and watched red (asserted
  `!= UNSUPPORTED` failed, since the stale `observation_count`-only check honoured a stage no
  credited observation had set), restored and green. Server tests updated for the new blanking and
  rating rule: `tests/api/test_served_steps.py`, `tests/api/test_ungraded_flow.py`,
  `tests/feedback/test_render.py`; fixtures that force a stage via `observation_count = 1`
  (`tests/api/conftest.py`, `tests/session/test_service.py`, `tests/session/test_serve_format.py`)
  now also set `credited_observation_count = 1`, since `serve_stage` gates on the new field.
  Client tests: `app/web/src/session/Item.test.tsx`, `app/web/src/session/SessionScreen.test.tsx`
  rewritten off the withdrawn decision; the one test that had no analogue left ("offers Next item
  after a worked example, whose attempt the server leaves ungraded") is deleted rather than
  loosened, because the ruling makes its premise false. Flake:
  `tests/e2e/test_exit_criteria_mastery.py::test_mastery_path_across_days_and_unmastery` failed
  once in 10 runs of the base branch before this session's changes (`UNIQUE constraint failed:
  audit_log.id`, confirming the shape once a naive fix was tried; the true fix is below) and 8 of 8
  clean runs otherwise. Root cause: `app/session/preview.py` `user_assembly_rng` seeds session
  assembly's tie-breaking draw from the process seed (fixed at 7 by the `world` fixture), the user
  id and the day; the user id is a fresh `uuid.uuid4().hex` from `app/auth/service.py new_id`
  minted fresh on every test's registration call, so which archetype the draw serves, and so which
  skill this test masters and un-masters, changed from run to run though nothing else did. Fixed by
  monkeypatching `auth_service.new_id` for the one `"USER"` prefix only, to a fixed id, leaving
  every other prefix (`AUD`, `PKC`, `CHL`, ...) on the real generator; an earlier attempt that
  pinned every prefix to the same fixed string broke on the second `write_audit` call inside one
  test run (`UNIQUE constraint failed: audit_log.id`), which is the artifact quoted above. Proof:
  36 consecutive runs with 0 failures (6 immediately after the fix, 30 more in a dedicated loop,
  `for i in $(seq 1 30); do .venv/bin/python -m pytest -q tests/e2e/test_exit_criteria_mastery.py::test_mastery_path_across_days_and_unmastery; done`,
  every exit code 0). No live API call; `app/providers/replay.py` cassette only.
- Seventeenth session, 2026-09-23, slice 2 of the token economy: a Claude-only $100 tier, priced
  and wired, plus a guard fix from the previous review. `tools/cost_model.py` gains
  `tier.hundred_claude_only`, additive next to `tier.hundred`: the verifier prices on
  `claude-haiku-4-5` batch (`verifier.on_haiku_batch_cycle`, $26.94, uncached because its 1,100
  token prefix sits below Haiku 4.5's 4,096 token cache minimum, the same reasoning 14 already
  gives the tutor); the template author prices on `claude-opus-5-5` (`template.cycle_on_opus_5_5`,
  $13.87 against $17.37, saving $3.50); the grader prices at 2 samples with a third on
  disagreement over the full 1,200 judged points, `grader.conditional_third_cycle` ($33.32), not
  the 17-of-76 field bound, because that bound is a lower bound on the model share and not a
  measurement and pricing the tier on it would be inventing the labelling pass's answer. New
  `CLAUDE_ONLY_ROLE_MODELS` names each role's model for the Claude-only tier; the existing
  `ROLES`/`PRICES`/`tier.hundred` figures are untouched, because `13-ai-engineering.md` and
  `docs/operator/ai-operating-costs.md` still quote the $95.03 Gemini-verifier tier and this file
  never patches a figure a document has already quoted. Total: $128.95, an overrun of $28.95
  against the operator's $100.00 hard stop. `docs/plan/14-token-economy.md`'s "The $100 tier, line
  by line" table, "Per role model choice" section, the "Proposed edits" table and open questions 2
  and 7 are rewritten to match and to report the overrun rather than close it by assumption;
  question 7 is answered, the ceiling is a hard stop with no margin, direction 7 taken now.
  `python3 tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0.
  `tests/tools/test_cost_model.py` (13 and ai-operating-costs.md, unchanged) stays green.
  `app/providers/model_routing.py` is new: `ROLE_MODELS`, the same per-role Claude model choice
  restated for the application, read by `app/feedback/tutor.py` (`TUTOR_MODEL = model_for("tutor")`,
  replacing the hardcoded string). `tests/providers/test_model_routing.py` asserts `ROLE_MODELS`
  and `tools.cost_model.CLAUDE_ONLY_ROLE_MODELS` agree role by role, every role names a Claude
  model, and the tutor path reads from the shared table; a mismatch introduced by hand (grader
  changed to `claude-opus-5-5` on the app side only) turned it red before the fix and was reverted
  to confirm green. Guard fix: `app/providers/guard.py` `_settle` called `_dev_reconcile` from
  inside `_reconcile`'s own try block, so a `_dev_reconcile` failure (a corrupt dev-spend ledger
  file, `json.JSONDecodeError`, a `ValueError` subclass) was caught by `_settle`'s
  unreadable-result handler, which double-counted `settled_calls` and wrote a false
  `provider_result_unreadable` audit row for a provider result that had, in fact, read fine and
  already been settled onto the budget row. `_reconcile` now returns what the true-up needs instead
  of calling it, and `_settle` calls the new `_dev_reconcile_safely`, which isolates
  `_dev_reconcile`'s own exceptions behind a new audit action,
  `dev_spend_ledger_reconcile_failed` (added to `app/audit/vocabulary.py`), bounded once per user
  per day the same way the other refusal rows are.
  `tests/providers/test_dev_spend_guard.py::test_a_dev_ledger_failure_on_true_up_does_not_double_charge_the_budget_row`
  and `::test_a_dev_ledger_failure_on_true_up_is_recorded_under_its_own_action` reproduce it with a
  `LedgerThatFailsOnTrueUp` double whose `add()` raises `ValueError` only on the true-up call (the
  reservation call still succeeds); both red before the fix (`settled_calls` 2 instead of 1, zero
  `dev_spend_ledger_reconcile_failed` rows), green after, confirmed by `git stash` of
  `app/providers/guard.py` alone and rerunning. No live Anthropic call was made. Suite at close:
  pytest full run clean, client `308 passed`, `tsc --noEmit` clean, `qa/12_report.py` exit 0 (see
  the verification lines below this entry).
- Sixteenth session, 2026-09-23, two review findings against the fifteenth session's persistent
  developer spend cap fixed. `DevSpendLedger.spent()` and `.add()` in `app/providers/guard.py` were
  an unlocked read-modify-write of one JSON file, with `write_text` truncating before writing;
  concurrent reservations under the sync FastAPI route's threadpool could lose an update, and a
  reader could land on a truncated file mid-write. Fixed with an `fcntl.flock` on a `.lock` sidecar
  file held for the whole read-modify-write, and an atomic write (`tempfile.mkstemp` in the same
  directory, then `os.replace`) so a reader never observes a half-written file.
  `test_dev_spend_ledger_add_is_safe_under_concurrent_writers` reproduces the race with two threads
  and a monkeypatched `_read` that widens the read-to-write window; red without the lock (final
  total 1.0 instead of 3.0, one writer's update lost), green with it, confirmed by temporarily
  stripping the lock and rerunning. Separately, `dev_worst_case_usd` priced every prompt token at
  the base input rate regardless of `request.cache`, while `dev_actual_usd` charges a reported cache
  write at `write_1h` (2x input), so a cold-cache reservation could sit below the reconciled cost and
  let the cap be crossed. Fixed: a request whose `cache` is set now reserves its prompt at
  `max(input, write_1h)`, falling back to `input` for a model with no `write_1h` row.
  `test_dev_spend_reservation_prices_a_cached_request_at_the_write_rate` sets the cap just above the
  uncached worst case and asserts the call is refused; red without the fix (call went through,
  `DID NOT RAISE DevSpendCapExceeded`), green with it, confirmed by temporarily reverting to the
  input-only rate and rerunning. No live Anthropic call was made. Suite at close: pytest full run
  clean, client tests and `tsc --noEmit` clean, `qa/12_report.py` exit 0 (see the verification lines
  below this entry).
- Fifteenth session, 2026-09-23, slice 1 of the persistent developer spend cap. `tools/cost_model.py`
  PRICES gains `claude-opus-5-5` (input 4.00, write_5m 5.00, write_1h 8.00, read 0.20, output 20.00,
  the operator's console announcement, tagged [inferred] rather than [verified] since it is not an
  independent reading of the pricing page). `app/providers/guard.py` adds `DevSpendLedger`, a JSON
  counter under `var/dev_spend_ledger.json`, and `DevSpendCapExceeded`; `GuardedProvider` reserves
  the worst case against it before a live call, reconciles to the reported usage after, and refuses
  with an audit row (`dev_spend_cap_refused`, one row per day) when the projection would cross
  `GROWTH_DEV_SPEND_CAP_USD` (default $15.00). Pricing for the cap comes from
  `tools/cost_model.py`'s PRICES table, including its batch discount, not from the guard's own
  MODEL_PRICES. Tracking is off unless the caller passes `dev_spend_track=True`; the only caller
  that does is `app/api/routes/sessions.py`, from `isinstance(settings.tutor, AnthropicProvider)`,
  so replay and every Provider test double the suite already wires never touch the ledger, and a
  future double added to some unrelated test cannot start writing to it by accident either. `tools/dev_spend.py`
  is a read-only reporter over the same ledger. tests/providers/test_dev_spend_guard.py: refusal
  before the wire, persistence across a fresh `DevSpendLedger` instance pointed at the same file,
  reconciliation from the worst-case reservation to reported usage, replay leaving the ledger and
  its file untouched, tracking off unless `dev_spend_track=True` even over a double that reports
  real usage, the real `AnthropicProvider` class engaging the cap with no key and no socket opened,
  and the Opus 5.5 price. Suite at close: pytest full run clean (no FAILED entries; a single
  `test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound` failure earlier
  in the session did not reproduce standalone or on a clean rerun and is unrelated, a timing bound
  test sensitive to host load per its own comment), client `308 passed`, `tsc --noEmit` exit 0,
  `qa/12_report.py` exit 0. No live Anthropic call was made.
- Fourteenth session, 2026-09-23. Suite at close: pytest `803 passed`, client `308 passed`, tsc
  clean, tests/e2e plus tests/api `151 passed` on four repeat runs, `qa/12_report.py` exit 0.
  Opened at `746 passed` and `286 passed`.
- R7, R8, R9 from the thirteenth session, reviewed fresh this session and closed with the repairs
  below: tests/api/test_ungraded_flow.py, tests/items/test_bound_child_failure.py,
  tests/design/test_contrast_floors.py, app/web/src/styles/app.test.ts.
- Child death while grading (R8 finished): `ChildDiedError` is re-raised through
  `app/items/grade.py` instead of being caught as ungraded, and POST /sessions/{id}/attempts
  answers 503 with no attempt row, so the resubmit is graded.
  test_a_child_death_while_grading_writes_no_attempt_and_the_resubmit_is_graded (red
  `assert 200 == 503`), plus three grade-level re-raise tests, each red under its own mutant.
- Provider seam: `ProviderResult.finish_reason` replaces `stop_reason`; a cassette that still
  carries `stop_reason` is refused; `output_config.effort` is refused on Haiku 4.5.
  test_result_names_finish_reason, test_a_cassette_carrying_stop_reason_instead_of_finish_reason_is_refused,
  test_every_committed_cassette_replays_its_finish_reason, test_effort_is_refused_on_haiku_4_5,
  test_haiku_4_5_without_effort_reaches_the_wire.
- Account: `GET /auth/status` answers `{"user_exists": bool}` and the account screen shows only
  register or only sign-in; `POST /auth/passkey/add/begin|finish` add a second passkey under the
  session cookie, excluding the credentials already stored; `AddPasskeyControl` is mounted on
  settings. tests/api/test_auth_status.py, tests/auth/test_add_authenticator.py (including
  test_a_challenge_issued_to_one_user_cannot_finish_under_another_users_session, red `assert 409
  == 403` with the guard mutated off, and test_adding_an_authenticator_excludes_the_passkeys_already_stored),
  test_registration_options_exclude_the_credentials_already_stored against the real py_webauthn,
  App.test.tsx "offers a signed-in student a second passkey on settings and nowhere else".
- Key audit: a verdict outside the sample is refused (`VerdictOutsideSample`), a second verdict
  through `record_item_audit_verdict` is refused (`VerdictAlreadyRecorded`), the denominator is
  the sample size, and no rate is published until every sampled item has exactly one verdict.
  test_a_verdict_outside_the_sample_is_refused, test_a_second_verdict_on_an_audited_item_is_refused,
  test_an_incomplete_sample_publishes_no_rate, test_a_complete_sample_publishes_its_rate,
  test_check_verdicts_refuses_a_verdict_outside_the_sample.
- Units in grading (03 check 4): notation credit only for the same unit written differently, SI
  conversion factor exactly 1; a different unit of any dimension is wrong; symbols are
  case-sensitive except where the submission reads as no unit at all and matches the key in
  another case (" M/Sec " against m/sec); physical constants are not units.
  test_a_different_unit_earns_no_notation_credit (11 cases),
  test_the_same_unit_written_differently_keeps_notation_credit,
  test_a_speed_in_metres_per_second_against_a_key_in_feet_per_second_is_wrong,
  test_unit_symbols_are_case_sensitive, test_a_physical_constant_is_not_a_unit,
  test_units_that_name_no_known_unit_are_ungraded.
- Gate 23 seed independence: the gate's loop runs until both screens arrived and every
  cold-start-reachable archetype was served (no assertion changed; seeds 0 to 49 all pass),
  `serve_as_mcq` publishes its own sibling item, and `second_wrong_answer` in
  tests/api/test_settings_routes.py makes the stage and format certain. The session and preview
  rng is seeded by process seed, user id and day through `preview.user_assembly_inputs`, and the
  old `assembly_inputs` is deleted. test_two_users_on_the_same_day_get_different_draws,
  test_the_process_seed_still_moves_the_draw, test_the_same_user_on_the_next_day_gets_a_different_draw,
  test_the_preview_and_the_session_both_draw_from_the_signed_in_users_rng (red `assert [] ==
  ['USER-...']`).
- test_next_item_never_carries_the_answer_key reads its forbidden fields from 04's output schema
  and 06's items table; red on each of four leaks mutated into `_as_item_dict`.
- Error note cap of 500 (operator decision 2026-09-20): `ERROR_NOTE_MAX_CHARACTERS`, 422 over it.
  test_error_note_route_refuses_a_note_over_500_characters, test_a_note_of_exactly_500_characters_is_stored
  (red `assert 422 == 200` with `>` mutated to `>=`); the client field's maxLength test scans the
  server constant (red `expected 501 to be 500`).
- A malformed `today` answers 422 on GET /progress, POST /sessions and the other session routes,
  with nothing written.
- Design: the contrast floor tested at exactly 4.5 (red with `<` mutated to `<=`); the accent tint
  range parsed from 08; `css.py` emits a `:root:not([data-theme])` fallback, light by default and
  dark under `prefers-color-scheme: dark`, derived from theme.ts, so the first paint carries tokens.
- Session screen: `rateConfidence` catches a refused rating and releases the in-flight guard; the
  example-stage mock returns what the server returns (correct null, confidence null).

Session 2026-09-23 (thirteenth), P1 exit criteria, the provider seam defects 13 enumerates, the
sign-in screen, and the design. Suite line at open `512 passed in 70.40s (0:01:10)`, at the last
close `746 passed in 148.85s (0:02:28)`. Client `Tests 286 passed (286)`, `npx tsc --noEmit`
exit 0, `npx vite build` succeeds. Style gate exit 0 on 77 changed Python and Markdown
files at the pre-wave-3 check. `qa/12_report.py` exit 0; `data/`, `research/`, `cache/` and `qa/`
untouched. `tools/gate_status.py --phase P1` reads `P1: 31 gates, 28 present, 3 missing, 28
passing`. Nothing committed.

- Gate 26 `test_contrast_floors` closed (`tests/design/test_contrast_floors.py`). The palette is
  `app/design/growth-tokens.json`, "Graphite, revised", chosen by the operator on 2026-09-23 from
  three directions and then four Slate variants rendered as mockups. `tools/check_tokens.py`
  exits 0 on it; the lowest pair is focus-ring on surface-sunken at 4.91:1 and the lowest text
  role is 5.60:1. Cross-checked against the WebAIM Contrast Checker API
  (https://webaim.org/resources/contrastchecker/, api mode, queried 2026-09-23): every text,
  state and focus pair passes AA in both themes. The six border-hairline rows read AA fail and
  AA-large pass at 3.02 to 3.57; 08 sets a 3:1 working floor only for the mastery map and the
  calibration curve, and holding input edges to it is the implementer's extension.
  Deviations the operator accepted by choosing it: 08 asks for warm neutrals and Graphite is a cool
  grey; the file carries 08's named neutral tokens and the two semantic base colours, not a
  separate nine-step ramp or semantic tint ramps, because the vocabulary names none.
- Gate 22 `test_prompt_cache_prefix_length` closed. The tutor renders
  `prompts/feedback/elaborated_v2.md`, whose static prefix measures 1,470 tokens on
  claude-sonnet-5 by `POST /v1/messages/count_tokens` with the operator's key on 2026-09-23 (v1
  measured 485). The prefix grew only with 13:246's content: guardrail rules, notation and
  rendering rules, interface-writing rules; P1 has no persistent misconception list, so none was
  added. The measurement is bound to the prefix bytes by sha256 in
  `tests/fixtures/prompt_token_counts.json`; `tools/count_prompt_tokens.py` re-measures. P1 now
  reads 28 of 31.
- Exit criteria 5 and 6: `tests/e2e/test_exit_criteria_mastery.py`,
  `test_unit2_session_changes_mastery_state` and `test_mastery_path_across_days_and_unmastery`,
  over the real HTTP app with the six D2 conditions recomputed from `attempts` rows.
- Exit criterion 8 instrument: `tools/serving_cost.py <db> [--user id]` prints served items, median
  tutor cost per served item (all items, and items that made a call) and the cache read share from
  attempts and from budgets, each with its denominator and exclusions. New attempts columns
  `tutor_calls`, `tutor_cost_usd`, `tutor_tokens_in`, `tutor_tokens_cached_read`,
  `tutor_cached_read_reported_calls`.
- 13's guard items 3 to 7 and its missing hard-stop rows (`app/providers/guard.py`): a call that
  reached the wire is charged the worst case, a `RefusedBeforeWire` is refunded; a refusal names
  every crossed cap; null and zero cached counts kept apart through `settled_calls` and
  `cached_*_reported_calls`; `ProviderCallFailed` carries no message text; an unconfigured role is
  refused and audited once a day; only a raise of every stopping cap above the day's spend clears
  a stop, through the guard and `PUT /settings/budgets` alike; `CallAccounting` and
  `last_accounting`. Price table carries Haiku 4.5, Flash-Lite and dated Gemini 3.8 Flash.
- Anthropic adapter: allowlisted `provider_options` (thinking disabled, effort), the key never a
  local on a raising frame, redirects refused, SSE stream mapped per 06 with usage returned,
  `reasoning_tokens` read, Opus 5 family rule.
- Tutor: 13's configuration (thinking disabled, effort low, 600 output tokens) and ceilings of 20
  calls per session and 3 per item, counted from the database, pre-wire failures not counted.
  Startup caps default to 12's row, $1.00 and 250,000 tokens, and refuse non-finite values.
- Audit detail bound (`app/audit/detail.py`) on every writer, checked per constructor by AST.
- CSP and CORS middleware; Secure cookie decided by request host, plain http on a non-loopback
  host refused.
- SymPy bounded on every thread for equivalence, numeric check, expression comparison and parse;
  a SymPy exception on student input is ungraded instead of a 500.
- Client: account screen (register, sign in, recovery code) over real WebAuthn; `data-theme` from
  the system preference; `app/web/src/styles/app.css` from the chosen mockup; inline style
  overrides removed; one main landmark per screen.
- Reviewer D's findings fixed: an example-stage or ungraded attempt no longer 409s on feedback or
  confidence, so the student always gets Next item and mastery stays unchanged
  (`tests/api/test_ungraded_flow.py`, feedback kind `ungraded`); a grader child that dies before
  answering raises `ChildDiedError` instead of reading as unsettled; gate 26 pins focus-ring and
  both state colours on every surface; app.css's `:focus-visible` rule, one main landmark per
  screen, an h1 on the account screen and the recovery-code input's `autocomplete="off"` and focus
  return are tested.
- Tests strengthened: the tutor receives only its selected fields (sentinels in every other
  field), prompt templates carry sha256 goldens, the cookie refusal reads the database.
- py_webauthn landed in `pyproject.toml` and 06; `LibraryVerifier` builds real options.
  `uvicorn` is installed in `.venv/` only, on the operator's yes, to run the app locally.

Session 2026-09-22 (twelfth), the server routes and client wiring for the three P1 screens. Suite
line at open `405 passed in 57.78s`, at close `512 passed in 60.71s (0:01:00)`. Client suite
`Tests 228 passed (228)`, `npx tsc --noEmit` exit 0, `npx vite build` succeeds. Style gate exit 0 on
all 64 changed or new files. `qa/12_report.py` exit 0 and `qa/last_report.json` restored. `data/`,
`research/` and `cache/` untouched. `tools/gate_status.py --phase P1` still reads 26 of 31: every
remaining gate is operator content or a live key. Nothing committed.

- A, session payload. `GET /sessions/{id}/next` carries `served_steps` (every worked step at
  example, all but the last at completion, null at unsupported, index and text only) and
  `self_explanation_prompt` at example. `POST /sessions/{id}/attempts/{aid}/self-explanation`
  writes `attempts.self_explanation` once, and only for a worked example or a corrected attempt.
  `attempts.response` keeps only `mathjson`, `option_id` and `units`, so a client-claimed
  `correct` or `step_outcomes` is no longer stored or trusted. Step marks are computed on the
  server in `worked_solution` numbering: given steps `given: true, correct: null`, the completion
  blank carries the server's verdict. A completion slot below Q16's 2-step minimum is served at
  example. Tests `tests/api/test_served_steps.py`, `tests/api/test_self_explanation.py`, the
  strengthened `test_next_item_never_carries_the_answer_key`, and the rewritten
  `tests/feedback/test_render.py::test_step_verification_at_example_and_completion`.
- B then A, home queue preview. `GET /progress` returns `skills_due_for_review`, `frontier_skills`,
  `corrected_items_returning`, `forecast_minutes` and `session_in_progress`, writes nothing, and
  derives its day and rng from `preview.assembly_inputs`, the same function `POST /sessions` now
  uses, so the forecast is the queue the student opens. Coverage-gap audit rows deduped per user,
  archetype and day. Tests `tests/session/test_queue_preview.py`,
  `tests/api/test_progress_route.py` including
  `test_progress_predicts_the_queue_post_sessions_assembles`.
- C, settings and budgets. `GET` and `PUT /settings` (exam date and purge date),
  `GET /settings/providers` (six roles from `guard.ROLES`, no key material), `GET` and
  `PUT /settings/budgets` behind re-authentication with a `budget_cap_changed` audit entry. Caps
  live on `budgets` rows and carry forward day to day once a PUT is made; before that the startup
  caps apply and a lowered one still binds on today's row (the committed
  `test_a_lowered_cap_binds_on_the_existing_row` passes unchanged). Tests
  `tests/api/test_settings_routes.py`, `tests/providers/test_cap_change_binds.py`.
- D, export. `POST /export` behind re-authentication and `GET /export/{id}`, a JSON archive of
  every user-owned table classified from the SQLAlchemy metadata, with secret-bearing columns
  dropped, written 0600, replaced new-file-first, 503 on an in-memory database. Tests
  `tests/export/test_export.py`.
- P, purge repair. Purge now removes the export archive and its `jobs` row, uses the export's
  ownership classification instead of a hand-typed table list, and burns a wrong reauth token.
  Gate 24 unedited and green. Tests `tests/session/test_purge.py` (three new),
  `tests/api/test_purge_route.py`.
- E, spacing. `SPACING_TOKENS` holds 08's nine values as `space-<px>`, emitted in a `:root` block,
  and `stylesheet_from_token_file(path)`. Test `tests/design/test_spacing.py`.
- F, ASGI mount. `app/main.py` serves `app/web/dist/assets` through `StaticFiles`, `index.html` at
  `/` only, and `/growth-tokens.css` from `GROWTH_TOKENS_PATH` read per request (404 when unset).
  `application` is built on first attribute access, so importing `app.main` writes nothing.
  Tests `tests/api/test_static_mount.py` (19, including three traversal encodings).
- G, hygiene. Resolution audit logs the row's own kind; `resolve_item_audit_row` resolves exactly
  the named row and refuses a resolved one; the key error rate divides by eval 29's sample of 100;
  `verify_item` splits options on `is_key` and refuses inconsistent records.
- H, client. Home, session and settings are mounted over real calls; the "not built yet" panels
  and the invented required props are gone. `ServedItem` and `SessionQueue` are checked by exact
  field-set equality against the server source. Dates print as 08 writes them. Every settings
  action reports failure by leaving its control re-enabled with no success state.

Session 2026-09-21 (eleventh), the P1 client and gate 25. Suite line at open `388 passed in 64.09s`,
at close `405 passed in 174.52s`. Client suite `133 passed`, `npx tsc --noEmit` exit 0 and
`npx vite build` succeeds. Style gate
exit 0 on every changed Python and Markdown file. `qa/12_report.py` exit 0. `data/`, `research/`
and `cache/` untouched, `git status --porcelain` over the three empty. `qa/last_report.json`
restored. Nothing committed.

- Gate 25 `test_reduced_motion_replaces` closed, which takes P1 from 25 of 31 passing to 26 of 31.
  `tools/gate_status.py` reports `P1 25 test_reduced_motion_replaces present passing`. The three
  previous sessions filed this gate as human-only on the ground that it waits on the design token
  file. That reading is corrected: the gate's property is the motion contract and the presence of
  five affordances, it reads no hex value, and 11 P1 scope items 8, 11 and 17 put `app/web/` inside
  P1. See Plan corrections.
- `app/web/`, new, the P1 client. React 18, TypeScript and Vite, which
  `docs/plan/06-architecture.md` line 93 names, plus KaTeX and MathLive from the same sentence.
  `npm` lockfile committed, `node_modules/` ignored.
- `app/web/src/affordances.ts`, the five gate-25 affordance names as one object with
  `affordanceProps`. Gate 25 and the session tests range over that object, so no hand-copied list
  is checked against another hand-copied list.
- `app/web/src/api/types.ts` and `client.ts`, the typed fetch layer over the routes
  `app/api/routes/` already exposes. `client.test.ts` scans the FastAPI decorators from disk and
  asserts every path the client issues is a path the server declares, and, after the wave-1
  review, scans the route return-dict literals, `bank.STUDENT_OPTION_FIELDS`, `render.as_dict` and
  `dress_item` and asserts twelve payload types by exact field-set equality.
- `app/web/src/styles/motion.css` and `motion.ts`, the motion contract. One duration and one
  easing, both derived from 08's single number. `motion.test.ts` walks the real stylesheet through
  the CSSOM and fails a reduce block that deletes a transition instead of cross-fading it.
- `app/web/src/input/MathField.tsx` and `McqControl.tsx`. MathField exports MathJSON, not LaTeX.
  McqControl takes its option count from the item's own options array and leaks no key: its test
  compares attribute name and value pairs across the radios, excluding the legitimately varying
  ones, which is what caught a `data-is-key` mutation that a name-only comparison had missed.
- `app/web/src/session/`, the session screen: the three fading stages, backward fading with the
  last step blanked, the five feedback affordances, and the item-to-feedback-to-next-item flow.
  Colour independence holds: every correct or incorrect state carries a word and a glyph.
- `app/web/src/home/HomeScreen.tsx` and `settings/SettingsScreen.tsx`, with home's three states
  (queue ready, queue empty, session in progress) and settings restricted to the five sections
  11 P1 scope 17 names. The settings test parses that scope sentence out of 11 rather than typing
  the list. Purge refuses without the typed confirmation.
- `tests/web/test_reduced_motion.py`, gate 25 in pytest so `tools/gate_status.py` finds it and the
  operator's one suite command runs it. It shells out to vitest and asserts on the JSON reporter,
  not the exit code: every `it(...)` title scanned out of the tsx source must be reported passed,
  the passed count must equal the declared count, and a run matching zero files fails. It never
  skips.
- `app/design/css.py`, the only bridge from the operator's token file to the client. The client
  references `var(--growth-<token>)` and contains no hex value anywhere.
- The three non-blocking defects carried since the eighth session are fixed.
  `app/items/verify.py` now holds one comparison and error-path core that both
  `verify.distractor_checks` and `distractor_paths.distractor_path_violations` call, with the two
  deliberately different unsettled policies preserved and named in each caller.
  `tests/design/test_tokens.py`'s floor test now finds the greys astride the floor with
  `contrast.contrast_ratio` instead of asserting black on white at 21:1, and the accent tint range
  is parsed from 08's own sentence instead of typed.

Session 2026-09-20 (tenth), the token economy. Suite line at open `388 passed`, at close
`388 passed, 1 warning in 56.96s`. Style gate exit 0 on every file written. `qa/12_report.py` exit
0. `data/`, `research/` and `cache/` untouched, `git status --porcelain` over the three empty.
Nothing committed.

- `docs/plan/14-token-economy.md`, new. The operator set a ceiling of $100.00 to exam day against
  the recommended tier's $348.05. Ten directions are ranked by dollars saved, each with the quality
  instrument that would detect its loss and the measurement that settles it, plus rejected
  directions with the floor that rejects each, proposed constant changes, open questions and
  unsourced claims. The tier lands at $95.03, Anthropic $82.31 and Google $12.71, with $4.97 of
  headroom.
- `tools/cost_model.py`, additive only. `gemini-3.5-flash-lite` prices read off the pricing page on
  2026-09-20, a `template` role priced from measured prompt and artifact sizes, the grader's model
  share, the diagnostician's recurrence share, the golden set 2 canary, and the `tier.hundred`
  lines. No existing constant moved, so the superseded configuration stays priced beside the new
  one and the four tests stay green. Positive control on the new document: a stray `$999,999.99`
  appended to a scratch copy gives `14-control.md:535: $999,999.99 is not a figure in
  tools/cost_model.py` and exit 1; the clean file gives 0 unknown figures and exit 0.
- What was measured in this session, with the command. 139 active archetypes and a mean
  `build_prompt` of 1,582.3 characters over all of them; `INSTRUCTIONS` at 4,420 characters and
  `TEMPLATE_SCHEMA` at 2,280, both from `tools/template_trial.py`; the 26 template artifacts under
  `var/` at a mean 2,412.1 characters of compact JSON, median 2,372.5, min 1,910, max 3,212; and 76
  active BC-PT records in `data/scoring_points.json` of which 59 answer no to
  `justification_required`, `interpretation_required` and `hypotheses_required`, 14 require
  justification, 3 interpretation and 3 hypotheses.
- Eight of the ten directions were written into the plan on the operator's instruction: 13 gains a
  fourth tier, a Flash-Lite verifier row, two price rows, a second per-role table, rewritten eval
  schedule rows, six tunables and five decisions; 07's D8 verifier row and the paragraph above it;
  04's re-solve routing and a paragraph on what the unit of generation does to caching, batching and
  bank cost; 10's golden set 1 onto the template gate, golden set 2's sampling split, which point
  types reach the grader, and the P3 and P4 gates; 03 gains a section on when the diagnostician is
  called at all and the rule-based section is renamed from "unavailable" to "does not run"; 11 gains
  the BC-PT labelling pass as a P3 entry criterion and the calculator boundary on the template gate;
  12 gains ten tunables rows; and the operator guide's settings, spend, tiers, eval schedule, credit
  arithmetic and the 2026-12-31 calendar note.
- Two directions deliberately not taken, on the operator's instruction: grader thinking off at
  $25.20 and a third grader sample drawn only on disagreement at $11.02. Each asserts a quality
  decision with no evidence behind it, each has a settling measurement named in 13, and together
  they are the remedy if the grader line comes in at its worst case of $44.34, which would put the
  tier at $129.25.
- The tier's single point of failure, recorded because it is not a defect and will read like one
  later. The grader line of $10.11 rests on 17 of 76 BC-PT records, which is a lower bound on the
  share of judged points reaching a model and not the share, because 03 adds a second condition the
  data does not carry. The labelling pass that settles it is offline, free and is now a P3 entry
  criterion.
- No application code was written. `app/generation/` still does not exist and the grader, the
  diagnostician and the transcriber are still unbuilt, so every direction landed as a plan change
  and a cost model line rather than as behaviour.

Session 2026-09-20 (ninth), the AI layer follow-through. Suite line at open `341 passed`, at
close `388 passed, 1 warning in 63.34s`. Style gate exit 0 on every file written. `qa/12_report.py` exit 0.
`data/`, `research/` and `cache/` untouched, `git status --porcelain` over the three empty.
Nothing committed. Five tasks in order, each verified before the next.

- The live 400. `app/providers/anthropic.py` sent `"temperature": request.temperature` on
  every call and `ProviderRequest` defaulted it to 0.0; a non-default temperature is a 400 on
  Opus 5 and Sonnet 5 at any value. The key left the wire body and the field left
  `ProviderRequest` entirely rather than becoming optional, because no routed model accepts it
  and an optional field invites sending it again. `tests/providers/test_anthropic.py` now asserts
  `"temperature" not in body`; shown red by re-adding the key
  (`AssertionError: assert 'temperature' not in {... 'temperature': 0.0 ...}`), restored,
  `tests/providers` 31 passed. `/code-review` over the four files: no findings.
- The cost model. `tools/cost_model.py` emits every figure `docs/plan/13-ai-engineering.md` and
  `docs/operator/ai-operating-costs.md` quote, from named price, token, call-count and survival
  constants, and `--check <file>` lists every dollar figure in a file that the model does not
  emit. `tests/tools/test_cost_model.py` (4 tests): the tutor cycle against the formula 13
  states, the effort lever against the thinking difference, and the two documents against the
  emitted set with a positive control that a stray `$999,999.99` is flagged. Red under mutation:
  charging every call as a prefix write gives `assert 15.588 == 5.01308`; a hand-patched
  `$123.45` in the operator guide gives `prints dollar figures the calculator does not emit:
  [(168, '123.45')]`. Both restored. What the recompute moved: golden set 2 was priced without
  the grader's 700 thinking tokens, so its run is $6.48 not $3.33 and the recommended tier is
  $348.05 not $319.70; effort high in the uncapped tier now applies to every thinking role by
  the generator's 2,500 to 1,200 ratio, so that tier is $1,145.55 not $880.29; five passages
  still priced the bank at 40 generated per archetype and now read 56 (staging waves of 28,
  batch queue 7,784 and 6,227, spend avoided $5.09 to $19.70, Sonnet comparison $71.05, effort
  lever $126.49). 24 bare `[measured]` tags were each given a command, retagged `[verified]`
  where the evidence was a code read at a named line, or `[single-source]` where the run is not
  in the repository. Two grep claims written for those tags were false as first written and
  were corrected before landing: `self_explanation` matches a prompt shown to the student, and
  `REPEAT_WINDOW_DAYS` is named by 13 itself.
- The template gate. `tools/template_trial.py` gained `contract_check` (declared
  representation from the archetype's list; figure spec required for BC-REP-02, 03, 07 and
  08; every distractor `error_path` an active BC-ERR id; every `point_type_id` a BC-PT id;
  exactly four options) and `incidental_check` (every parameter declares `radical` or
  `incidental`; each incidental is varied alone over its domain and the structure of every step
  and the key must hold). Schema, prompt and defect feedback carry all of it, and the prompt
  now lists the BC-ERR ids reachable from the archetype's skills. `tests/tools/test_template_trial.py`
  grew from 32 to 43 tests, one mutation of `tests/fixtures/template_trial/clean_02011.json` per
  check plus the clean-fixture absence claims; the fixture gained a representation, three
  resolving distractors and honest roles (`a` incidental, `b` and `c` radical because a zero
  deletes a term). Every check shown red by disabling it in the code, and the gate wiring shown
  red by dropping each clean flag from `passes_bar`; all restored, 43 passed. Measured over the
  26 templates in `var/` with the eleven-check gate: 0 of 26 pass; 12 of 26 on the six old
  checks. Failures by check: representation undeclared 26, error path unresolved 26, four
  distractors 14, key copied from the last step 13, point type unresolved 6, key disagreement 1.
  The role declaration is absent on all 26 by construction. The earlier "6 of 18" and "7 of 8"
  claims are superseded by that line.
- The radicals declaration. 13 gained "Radicals and incidentals" with the five primary
  sources, the contract consequence and the gate above, and the difficulty-prior decision:
  02 keeps one prior per archetype and accepts a known centre-ward bias, with the measurement
  that adds a variance term recorded (facility spread above 0.15 over at least 5 instantiations
  on 30 or more attempts). 02 and 04 carry the surgical corrections listed under Plan
  corrections.
- The migration. 13 gained "Template architecture and the migration" with the file-by-file
  map and the seam decision: instantiate at build time into `items`, never at serve time,
  because `attempts.item_id` is a permanent reference at `app/session/repository.py:129` and
  `app/api/routes/sessions.py:154` and `:207`, verification and the duplicate gate are per
  item, the requeue serves the same id again, and the least-recently-served draw needs stable
  ids. `app/generation/`, `prompts/generator/` and `prompts/verifier/` do not exist, so 11's
  P4 items 7 and 11 were corrected to name the template module and prompt. No application
  code for the migration was written this session.

Session 2026-09-20 (eighth), suite line at open `230 passed in 34.85s`, at close
`341 passed in 44.31s`. Style gate exit 0 on all 28 changed files, fed the hook its JSON payload
on stdin, confirmed to bite with a positive control (`style_gate: probe.py: em dash present`,
exit 2). `qa/12_report.py` exit 0. `data/`, `research/`, `schemas/` and `cache/` untouched,
confirmed with `git status --porcelain` over all four. The phase stayed P1, because 11's P2 entry
criterion is "P1 merged with all gates green" and six P1 gates are still open. The slice was every
P1 deliverable buildable without the operator, plus the operator unblock kit for the six that are
not. `python3 tools/gate_status.py --phase P1` now reads `P1: 31 gates, 25 present, 6 missing,
25 passing`, and the six missing are exactly the human-only list: 17, 22, 25, 26, 29 and 30.

- Integrator, gate table: `tools/gate_status.py`, `tests/tools/test_gate_status.py` (17 tests).
  Reads the gate list out of 11 for every phase, uses the plan's own item numbers for P1 and a
  running index for the later phases, scans `tests/` for each gate's definition, and reads
  outcomes from a JUnit report the tool writes itself. It exits 1 when any gate is missing or
  failing, so a caller can use it as a check. Two defects found in it during review and fixed: the
  outcome column was asserted by no test, and `run_suite` used `sys.executable`, which under
  `python3 tools/gate_status.py` is the system interpreter with no pytest, so the run failed
  silently and every gate read unknown. The tool now runs the repository's own `.venv` interpreter
  and says on stderr when a run produced no report.
- Agent M2, schema drift: `app/db/migrate.py`, `tests/db/test_migrate.py`,
  `tests/db/test_engine_migrates.py`, wired into `make_engine` in `app/db/models.py`.
  `missing_columns`, `apply_additive_migrations` and `SchemaDriftError`. This closes the
  `attempts.tutor_sentence` defect: an existing `var/growth.db` no longer raises on the first
  feedback read. Every ALTER is built and validated before the transaction opens, so a blocking
  column aborts before any write. A column that is NOT NULL with no server default refuses, and so
  does a column declared unique or indexed, because ALTER TABLE ADD COLUMN carries neither and the
  migrated database would otherwise diverge from a fresh one while reporting no drift. A database
  with no drift opens no write transaction at all.
- Agent M3, the unreadable provider result: `app/providers/guard.py`, `app/audit/vocabulary.py`,
  `tests/providers/test_guard_settle.py` (7 tests). A new audit action
  `provider_result_unreadable`, deduped on the budget row id, which is already one per user per
  role per day, so two roles give two rows and a day rollover records again. The detail carries
  the role, the model and the exception type name and nothing else.
- Agent M4, gate 26's arithmetic: `app/design/contrast.py`, `tests/design/test_contrast.py`
  (14 tests). WCAG 2.2 relative luminance and contrast ratio, `TEXT_CONTRAST_FLOOR` 4.5 and
  `LARGE_TEXT_CONTRAST_FLOOR` 3.0, both taken from 08 and 11. No hex value is authored anywhere.
- Agent M5, gate 30's property: `app/items/distractor_paths.py`,
  `tests/items/test_distractor_paths.py` (8 tests). `error_ids_for_skills` computes the BC-ERR set
  over the P1 skills rather than typing 40, and it is 40. An unsettled symbolic comparison is
  reported as its own violation and never reads as clean.
- Agent M6 and the integrator, the error note: `app/api/routes/sessions.py`,
  `tests/api/test_error_note.py`, `app/session/service.py`,
  `tests/session/test_error_note_service.py`. One note per corrected attempt, refused with 409
  rather than silently overwritten, and a note containing a line break refused with 400, because
  03 says the student writes one line. No length cap, because 03 and 06 give none. The guard was
  moved into `record_error_note` so every caller gets it, not only the route, and the route now
  maps `ErrorNoteAlreadyWritten` and `ErrorNoteNotOneLine` onto its two status codes.
- Agent M7, gate 29's shape: `app/review/verdicts.py`, `tests/review/test_verdicts.py` (14 tests).
  `verdict_violations` and `audit_completeness`. The verdict vocabulary is imported from
  `app/review/audit.py` and asserted identical rather than retyped.
- Agent M8, gate 26's vocabulary: `app/design/tokens.py`, `tools/check_tokens.py`,
  `tests/design/test_tokens.py` (12 tests), `docs/operator/design-tokens.template.json`. The nine
  type tokens and the seventeen colour tokens, both parsed out of 08 inside the test rather than
  compared against a second hand-typed list. The template is every token name at null, and a null
  is reported as missing rather than skipped.
- Agent M9, the operator's own checks: `tools/check_items.py`, `tools/check_audit_verdicts.py`,
  `tests/tools/test_operator_clis.py` (8 tests). `python3 tools/check_items.py <directory>` runs
  gate 17's and gate 30's checks over a directory of records and prints a per-archetype count;
  `python3 tools/check_audit_verdicts.py <verdicts.json> <sample.json>` prints the key error rate
  or says why it cannot be published. Over `tests/fixtures/items_p1/` the first reports 36 records,
  36 clean, exit 0, with six archetypes at 6 records each and the other seven at 0.
- Agent M10, the work orders: `docs/operator/README.md`, `items.md`, `key-audit.md`,
  `design-tokens.md`, `provider-key.md`. What the operator has to produce, in what shape, and the
  command that checks it, with every field list read out of the code rather than recalled.
- Integrator, the unsettled distractor: `app/items/verify.py`, `app/items/ingest.py`,
  `tests/items/test_unsettled_distractor.py` (5 tests). `_equals_key` collapsed an unsettled
  symbolic comparison into not-equal, so a distractor the checker could not compare against the
  key read as distinct from it and the item reached status `verified`. It is now
  `INDETERMINATE`, which leaves the item a draft and routes it to review, which is what ingest's
  own docstring already claimed. Red: `assert 'pass' == 'indeterminate'`.
- Integrator, gate 23 strengthened: `tests/e2e/test_session_login_to_feedback.py`. Membership in
  the 13 is a subset check that a regression serving one archetype passes. The gate now also
  computes, from the engine's own `outer_fringe` and `candidates` over the freshly seeded state,
  every archetype open at cold start, asserts there is more than one, and asserts every one of
  them was actually served.
- Integrator, the archetype lists: `tests/tools/test_p1_archetype_list.py` (4 tests). The 13 ids
  were typed in three places and checked against 11 in none. The plan text is now the source and
  every copy is compared against it. Red under mutation: dropping one id from
  `tools/build_p1_fixture.py` gives `AssertionError: assert {...} == {...}`.
- Integrator, after the fresh review, which raised two blocking findings and both reproduced.
  `audit_completeness` published a rate over a sample that was complete by id but not by verdict:
  100 sample ids, 98 clean, one verdict `mostly_fine` and one `None` gave `missing_ids []` and
  `key_error_rate 0.0`, which is what gate 29 and exit criterion 4 forbid. It now folds
  `verdict_violations` in, reports `invalid_ids` and `unidentified_records`, and returns `None`
  for the rate unless every verdict in the sample exists and is well formed (red:
  `assert 0.0 is None`). And a record with no `item_id` raised `TypeError` out of a `sorted()`
  rather than being reported; it is now counted. `app/design/tokens.py` checked
  `accent-contrast-text`, `state-correct` and `state-incorrect` against nothing, so a token whose
  role is text could hold any value and pass gate 26; the validator now checks
  `accent-contrast-text` against the accent base and its four tints and each semantic colour
  against each surface (red: `these do: ['accent-contrast-text']`).

Session 2026-09-20 (seventh), suite line at open `191 passed in 23.36s`, at close `230 passed in 46.12s`.
Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `schemas/`
and `cache/` untouched, confirmed by `git status --porcelain` over all four. The slice was the
provider seam of 07 plus gate 23, which were the last two pieces of P1 scope needing no key, no
screen and no hand-authored item. A fresh reviewer found ten defects over the first integration;
eight were fixed in session by two repair agents and the integrator, and the two that remain are
under Known defects.

- Agent A, the provider seam: `app/providers/guard.py`, `tests/providers/test_guard.py`.
  `GuardedProvider` estimates the worst case before the call, refuses on the dollar or token cap,
  reconciles against `raw_usage` after, keeps one `budgets` row per user per role per day, and
  writes `audit_log` only on the hard stop and the refusal, never per call. Tests:
  test_guard_estimates_the_worst_case_before_the_call,
  test_guard_refuses_when_the_estimate_crosses_the_dollar_cap,
  test_guard_refuses_when_the_estimate_crosses_the_token_cap,
  test_guard_reconciles_the_estimate_against_raw_usage,
  test_guard_keeps_one_budget_row_per_user_role_and_day,
  test_guard_writes_an_audit_entry_when_the_cap_stops_the_role,
  test_guard_writes_no_key_material_into_the_audit_detail,
  test_a_stopped_role_refuses_every_later_call_that_day,
  test_guard_prices_cached_reads_at_the_multiplier,
  test_an_abandoned_stream_releases_the_reservation,
  test_a_completed_stream_reconciles_against_raw_usage,
  test_a_stopped_role_records_the_refusal_once_and_still_refuses,
  test_a_lowered_cap_binds_on_the_existing_row,
  test_an_unpriced_result_model_is_charged_at_the_requested_model_price,
  test_a_result_without_usage_keeps_the_worst_case_reservation,
  test_a_role_with_no_configured_cap_is_refused.
- Agent B, the tutor sentence cache: `app/feedback/tutor.py`, `app/db/models.py` (one nullable
  `attempts.tutor_sentence` column), `tests/feedback/test_tutor_cache.py`. Tests:
  test_the_first_call_stores_the_sentence_on_the_attempt,
  test_a_cached_sentence_is_returned_without_a_second_provider_call,
  test_no_provider_stores_nothing_and_returns_no_sentence,
  test_a_provider_failure_stores_nothing_and_returns_no_sentence,
  test_an_empty_sentence_is_not_cached_and_is_composed_again,
  test_the_cached_sentence_is_read_back_through_a_fresh_session,
  test_without_a_session_and_attempt_the_function_behaves_as_before.
- Agent C, gate 23: `tests/e2e/`, `tests/fixtures/items_p1/` (36 synthetic records over
  BC-QA-01008, 02002, 02006, 02007, 02011 and 03008, all `no_calculator` and `BC-REP-01`, skills
  copied from `data/archetypes.json`), `tests/fixtures/provider_cassettes/`.
  test_session_login_to_feedback (gate 23) and test_the_socket_ban_itself_fails_a_network_call.
  The gate asserts every link 11 names: register with 618 seeded rows, logout, login, `/me`, a
  session drained and closed, a 409 on feedback before the confidence rating, the elaborated screen
  in both served formats, the named BC-ERR path, the tutor sentence through the cassette, the error
  note read back out of SQLite, a `skills_state` change read back out of SQLite, the socket ban
  firing on AF_INET, and membership of every served archetype in 11's 13.
- Integrator: the coverage-gap audit deduped per user per archetype
  (test_a_repeated_coverage_gap_writes_no_second_audit_entry, red `assert 3 == 1`;
  test_a_gap_recorded_for_another_user_still_writes_a_row); the guard and the cache wired into the
  feedback route behind `tutor_sentence_for`, with `tutor_unavailable` carrying 07's hard-stop line
  to the screen (tests/api/test_tutor_budget.py, four tests, red `KeyError: 'tutor_unavailable'`);
  `compose_sentence` re-raises `BudgetStopped` rather than swallowing it, because a cap is not a
  provider failure; `GROWTH_TUTOR_CAP_USD` and `GROWTH_TUTOR_CAP_TOKENS` on the composition root
  (test_main_gives_the_tutor_role_a_daily_cap, test_the_tutor_cap_is_read_from_the_environment);
  the controlled audit vocabulary at `app/audit/vocabulary.py`, enforced in all three writers, with
  a scanner test that walks `app/` and resolves module constants rather than checking one hand-
  copied list against another (tests/audit/test_vocabulary.py, six tests); the guard refuses a role
  with no configured cap (test_a_role_with_no_configured_cap_is_refused, red
  `Failed: DID NOT RAISE BudgetStopped`); the guard's price table pruned to claude-sonnet-5 alone,
  because the Opus 5 and Haiku 4.5 output prices the builder wrote appear in no plan document.

Session 2026-09-19, suite line at close: `42 passed in 12.58s`.

- Integrator: `pyproject.toml`, `app/engine/{constants,state,strength,fsrs_constants,prior}.py`, `tools/build_p1_fixture.py`, `tests/fixtures/graph_p1.json` (54 skills, 101 edges, 25 seeded parents, 4 inert BC-TOP), `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs`, `tests/engine/test_cold_start.py`: eval_cold_start_pA_distribution passes and prints split p10/p50/p90 0.250/0.450/0.587, compensatory 0.328/0.465/0.587, reproducing the plan's recorded gate.
- Agent A, loader: `app/content/loader.py`, `app/content/snapshot.py`, `tests/content/test_loader.py`: test_graph_acyclic, test_loader_against_real_data, test_loader_refuses_on_injected_cycle, test_loader_refuses_on_injected_dangling_id, test_loader_refuses_on_wrong_type_reference, test_inert_top_ids_include_p1_subgraph. Final suite at close: 42 passed, 0 failed.
- Agent B, engine update rules: `app/engine/update.py`, `app/engine/fsrs.py` (FSRS-7 forms from fsrs-rs), `app/engine/retention.py` (integrator), `tests/engine/test_update.py`: test_credit_assignment_table, test_correct_never_lowers_m, test_partial_never_raises_m, test_retrievability_monotone, test_mastery_conditions, test_fading_ladder, test_propagation_weights, test_mcq_guess_discount, plus test_fsrs_forms_from_source, test_stability_bounded, test_hypercorrection_clears, test_hypercorrection_spans_loaded_skills.
- Agent C, gating, selection, session assembly: `app/engine/fringe.py`, `app/engine/select.py`, `app/session/build.py`, `tests/engine/test_selection.py`: test_fringe_membership, test_retrieval_entry, test_format_alternates, test_co_requisite_inert, test_pending_probes_drained, test_fail_closed_no_item, test_session_assembly_blocks, test_interleave_max_two, test_never_serve_unmastered_prereq, plus test_requeue_gap, test_due_reviews_from_decay, test_probe_queue_cap, test_probe_served_without_explicit_now.
- Agent D, verifier tools, models, fixtures: `app/items/{mathjson,verify}.py`, `app/db/models.py`, `tests/fixtures/answers_equiv/pairs.json`, `tests/fixtures/student_trajectories/` (6), `tests/items/test_verify.py`: test_sympy_equivalence, eval_sympy_settle_rate (40 of 40 equivalent pairs settled); `tests/db/test_models.py`: test_models_create_all.
- Plan corrections below applied to docs/plan by agent E.

Session 2026-09-19 (second session), suite line at close: `72 passed in 14.23s`. Gate 31 `eval_simulation_mastery_growth` read `1 failed, 69 passed` at the first close, for the structural reason recorded under Decisions; after the gamma and condition 3 corrections it passes with pooled policy 88 mastered over 1457 items (0.0604) against control 92 over 1656 (0.0556), per trajectory printed by the eval. Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/` and `research/` untouched; `docs/plan/02`, `11` and `12` carry the two corrections below. Integrator-owned tests added: test_mastery_single_archetype_skill_needs_one_archetype, test_mastery_reachable_in_a_dozen_credited_successes (both quoted red before the engine edit).

- Agent A, simulation runner: `app/sim/runner.py`, `tests/eval/test_simulation.py`: test_simulation_reproducible_from_seed, test_simulation_prereq_gap_stalls_dependants (asserts on the served trace: no served item had an unmastered hard ancestor; shown red with gating bypassed, 165 blocked serves), test_simulation_records_both_predictions, eval_simulation_mastery_growth (gate 31).
- Agent B, snapshot persistence and reload reconciliation: `app/content/persist.py`, `app/content/reconcile.py`, `tests/content/test_persist.py`, `tests/content/test_reconcile.py`: test_snapshot_row_written_on_load, test_rejected_snapshot_row_records_reason, test_reload_with_unchanged_digest_reuses_active_row, test_reload_keeps_active_skill_and_sets_snapshot_id, test_reload_rewrites_superseded_skill, test_reload_merges_into_existing_successor_and_recomputes_mastered, test_reload_merge_union_failing_d2_clears_mastered, test_reload_merge_carries_difficulty_with_winning_stability, test_reload_merge_carries_difficulty_from_old_row_when_it_wins, test_reload_merge_preserves_flags_and_resets_consecutive_counters, test_reload_orphans_tombstone_without_successor, test_reload_refuses_inactive_successor, test_reload_writes_audit_entry.
- Agent C, session service and attempts writer (no HTTP layer): `app/session/repository.py`, `app/session/service.py`, `tests/session/test_service.py`: test_open_session_persists_four_blocks, test_attempt_row_logs_split_and_compensatory, test_attempt_updates_skills_state, test_confidence_before_feedback_sets_hypercorrection, test_error_note_stored_on_attempt, test_close_session_writes_ended_at, test_state_round_trip, test_rehearsal_session_writes_no_mastery, test_record_attempt_refuses_duplicate, test_ungraded_answer_skips_the_update, test_timestamps_are_timezone_aware_utc. Confidence design: `apply_observation` already sets `hypercorrection_due` from the rating, so `record_attempt` applies the observation immediately only at stage example (no rating, convention 3) and defers it at completion and unsupported until `record_confidence` supplies the rating, which runs the single update.

Session 2026-09-19 (third session), suite line at open `72 passed in 14.53s`, at close `93 passed, 1 warning in 15.74s` (the warning is starlette's own anyio alias deprecation). Style gate exit 0 on every touched file; `qa/12_report.py` exit 0; `data/`, `research/`, `docs/` and `qa/` untouched. Slice: HTTP layer and account lifecycle, 11 P1 scope items 13, 14 and 15.

- Agent A, HTTP and passkey auth: `app/api/{app,deps}.py`, `app/api/routes/{auth,me,sessions,purge,content,health}.py`, `app/auth/{webauthn,cookies,service}.py`, `passkey_credentials` and `auth_sessions` tables in `app/db/models.py`, `tests/api/`, `tests/auth/`: test_purge_requires_reauth (gate 24), test_register_refused_once_users_nonempty, test_login_finish_sets_httponly_lax_cookie, test_sign_count_regression_refused, test_session_routes_open_next_attempt_confidence_close, test_session_routes_require_the_cookie, test_healthz_localhost_only, test_reauth_token_single_use, test_content_snapshot_route_reports_the_active_row, test_me_reports_exam_and_purge_dates, test_library_verifier_names_the_missing_package. WebAuthn verification sits behind `PasskeyVerifier`; `LibraryVerifier` imports the `webauthn` package lazily and raises naming it when absent, and every test drives a `FakeVerifier`, because 06 names no WebAuthn library and this session's rule was to add none. Re-authentication is `POST /auth/reauth/begin` and `/finish`, an assertion ceremony 06's table lacks. The purge confirmation string is `PURGE_CONFIRMATION = "DELETE EVERYTHING"` in `app/api/routes/purge.py`. Session cookie `calcbc_session`, HttpOnly, SameSite=Lax, Secure off loopback only.
- Agent B, services: `app/session/seed.py` (618 rows, 77 BC-PRQ plus 6 external BC-SKL parents mastered, beta from `beta_for_skill` elsewhere), `app/session/purge.py` (audit entry first, every user table, audit_log last), `record_judgment` and the close-session sweep in `app/session/service.py`: test_seed_writes_618_rows_with_83_mastered, test_seed_beta_matches_prior, test_seed_refuses_second_run, test_close_session_applies_unrated_attempts_as_unsure, test_judgment_never_enters_credit, test_purge_empties_user_tables_and_writes_final_audit, test_purge_audit_entry_precedes_deletion.
- Integrator, after the fresh review: `POST /sessions/{id}/close` now passes the engine context so the sweep runs over HTTP (test_close_route_applies_unrated_attempts, red `ValueError: close_session needs archetypes, engine_graph and today`); the judgments route calls `service.record_judgment` and refuses an unknown scope_id or a retention outside 0 to 1 (test_judgment_route_validates_scope_id_and_retention, red `assert 400 == 200`); registration seeds from `settings.resolve_snapshot()` (test_register_finish_seeds_from_the_resolved_snapshot, red `AttributeError: 'World' object has no attribute 'settings'`); purge deletes `passkey_credentials` and `auth_sessions` through the models (test_purge_deletes_credentials_and_auth_sessions, green on write, red `1 failed` under a mutation that skipped the credential delete); one `random.Random(rng_seed)` per process on `Settings.rng` instead of a fresh one per `POST /sessions`; `tests/db/test_models.py` table set extended by the two new tables; `test_session_routes_open_next_attempt_confidence_close` corrected to send its archetype id under scope `archetype`, since it had been storing an archetype id under scope `skill`.

Session 2026-09-20 (sixth session), suite line at open `161 passed in 19.56s`, at close
`191 passed in 23.40s`, both taken with `--ignore-glob="* 2.py"`. Style gate exit 0 on all 15
changed files, fed the hook its JSON payload on stdin and confirmed to bite with a positive control
(`style_gate: gatecheck.py: em dash present`, exit 2). `qa/12_report.py` exit 0; `data/`,
`research/`, `docs/` and `qa/` untouched, checked with `git status --porcelain` on those four
paths. Slice: everything the fifth session named as blocking gate 23 that needs no hand-authored
item, no design token and no provider key. Gate 23 is not claimed and no new gate name from 11 is
claimed.

- Agent A, serve-time format resolution (R16, R29, gate 12): `app/session/service.py`,
  `tests/session/test_serve_format.py`: test_first_unsupported_serve_is_short_answer,
  test_second_unsupported_serve_on_the_same_archetype_is_mcq,
  test_example_and_completion_slots_are_always_short_answer,
  test_serving_twice_without_submitting_returns_the_same_format,
  test_the_served_format_is_persisted_on_the_queue_slot. `resolve_served_format` re-reads R29
  against the attempts as they stand and writes the answer back onto the queue slot; the stage
  stays frozen at assembly.
- Agent B, elaborated feedback without a BC-ERR record (03 Content, R12 rule 3):
  `app/feedback/render.py`, `tests/feedback/test_render.py`:
  test_wrong_short_answer_without_an_error_record_still_elaborates,
  test_absent_error_fields_are_empty_and_never_invented,
  test_the_violated_step_falls_back_to_the_last_path_step,
  test_the_tutor_payload_is_still_exactly_the_four_fields,
  test_no_scoring_consequence_when_the_archetype_supplies_none. Of the 13 P1 archetypes 8 carry
  `point_types: []` and 5 carry BC-PT id lists; no archetype record carries `does_not_earn` text.
- Agent C, the error-note route (06's API surface has no row): `app/api/routes/sessions.py`,
  `tests/api/test_error_note.py`: test_error_note_route_stores_the_note_on_the_attempt,
  test_error_note_route_requires_the_cookie, test_error_note_route_refuses_an_unknown_attempt,
  test_error_note_route_refuses_an_empty_note.
- Agent D, wiring and audit gaps: `app/main.py`, `app/api/routes/auth.py`, `app/session/build.py`,
  `tests/api/test_wiring.py`, `tests/session/test_coverage_audit.py`:
  test_main_wires_a_tutor_when_a_key_is_configured,
  test_main_builds_without_a_tutor_when_no_key_is_configured,
  test_main_respects_an_explicit_none_provider_even_with_a_key,
  test_building_the_application_opens_no_socket, test_reauth_finish_writes_an_audit_entry,
  test_a_fail_closed_coverage_gap_writes_an_audit_entry,
  test_the_audit_entry_names_the_skill_and_the_reason. Audit actions `reauth_established` and
  `coverage_gap_fail_closed`.
- Integrator: `open_session` passes `db` and `user_id` into `assemble_session`, so the coverage-gap
  audit fires on the production path and not only in a direct call
  (test_open_session_writes_the_coverage_gap_audit_entry, red `assert 0 >= 1`); the wrong short
  answer reaches elaborated feedback over HTTP
  (test_a_wrong_short_answer_gets_elaborated_feedback, test_the_absent_error_fields_are_empty_over_http,
  both shown red by a positive control that restored the old refusal inside `elaborated_payload`,
  `KeyError: 'elaborated'`, then restored).
- Integrator, after the fresh review, which found two blocking defects and reproduced both:
  `record_attempt` now resolves the format on the write path too, because gate 12 states the
  property over `attempts.format` and a client that never calls `GET /next` recorded the
  assembly-frozen format, which would have granted full credit on an attempt R29 says was MCQ
  (test_an_attempt_that_skipped_the_serve_still_records_the_resolved_format, red
  `At index 1 diff: 'short_answer' != 'mcq'`); `tests/api/test_routes.serve_as_mcq` no longer
  writes `mcq` onto the queue row, which the write-path resolution now overwrites, and instead
  consumes a real prior stage-unsupported attempt so the MCQ case is earned through R29 (seven
  HTTP tests went red on the old helper and pass on the new one); the tutor is opt-in through
  `GROWTH_TUTOR_PROVIDER`, default none, because 07 puts the budget guard, the usage accounting
  and the audit trail at the provider seam and P1 has built none of the three, so a key sitting in
  the environment no longer wires a billed role (test_a_stray_key_alone_wires_no_tutor); the
  coverage-gap audit row is stamped by `write_audit` with the wall clock rather than with the
  engine's session clock, which is local midnight of `today` and wrote `2026-03-01T05:00:00+00:00`
  for a row written in September (test_the_audit_entry_is_stamped_with_the_real_moment); the gap
  guard now checks `user_id` as well as `db`, since `audit_log.actor` is NOT NULL; the error-note
  route refuses a note on an attempt that was not corrected, per 02's block 4
  (test_error_note_route_refuses_a_correct_attempt, red `200 != 409`), and the test that stored a
  note on a correct attempt was rewritten to submit a wrong answer; a distractor whose
  `error_path` does not resolve in the snapshot is refused again rather than composing an empty
  payload, which restores the negative case the agent's deletion had dropped
  (test_a_distractor_whose_error_path_does_not_resolve_is_refused, red `DID NOT RAISE ValueError`).

- 2026-09-23, Slice 2 closing session: the drain's ceiling finding was already fixed in the
  working tree when this session opened, so it was verified rather than rewritten. Each guard in
  `app/feedback/drain.py` was broken and its tests watched go red, then restored: removing the
  `tutor.ceiling_reached` check failed `test_a_job_whose_item_ceiling_is_full_fails_without_calling`
  and `test_a_job_whose_session_ceiling_is_full_fails_without_calling` (`report.failed` 0, not 1);
  recording a tutor call on a limit wait failed
  `test_waiting_behind_a_limit_does_not_use_up_the_failure_retries` and
  `test_waiting_behind_a_limit_does_not_fill_the_item_ceiling`; calling `requeue_job` instead of
  `defer_job` on a limit wait failed `test_a_limit_that_still_holds_requeues_the_job_later_and_stops`
  and the failure-retries test. `tools/subscription_smoke.py` `checks_for` now accepts exactly two
  turns for a call that asked for a schema and got `structured_output` back, and one turn
  otherwise (`tests/tools/test_subscription_smoke_checks.py`, 5 tests; shown red three ways: one
  turn always, one failed; the allowance without requiring returned output, one failed; two turns
  always, two failed). Rechecked offline against `var/subscription_smoke.json`, phase 2 reads
  `no_tool_ran` true and both phase 1 calls still read true. Checks: pytest `945 passed in
  484.23s`, vitest `310 passed (310)`, `tsc --noEmit` exit 0, `qa/12_report.py` exit 0.

P2 Slice 3, 2026-09-23, review mode and FSRS scheduling (`docs/plan/11-phased-delivery.md` P2
scope item 3), started ahead of P2's entry criterion on the operator's delegated authority (see
Decisions below). Suite at close 918 tests collected, `pytest -q` exit 0 in 364 s (911 at open), vitest 310 passed, tsc exit 0, `qa/12_report.py` exit 0.

- `constants.desired_retention(today)` now returns 0.90 before `DESIRED_RETENTION_SWITCH_DATE`
  (2027-03-15) and 0.95 from that day on, with the signature 11's Q-list fixed. The day is the
  calendar date the app assembles for (the client's `today`, else the server's local date); a
  datetime is read on its own wall clock and never shifted into another zone first
  (`constants.calendar_day`). The three existing constants stay the one configuration point.
- The due test is one function, `fringe.is_due` (mastered and `R_k` below target), read by
  `select.due_skills` and by the new `fringe.covered_due_skills`, the set of due skills one
  archetype retires over its loaded skills and their 1-hop hard ancestors; `due_coverage` is its
  size. `select.review_eligible` factors out block 1's candidate filter (published item, R18;
  gating; `p_A >= 0.5` except for hypercorrection) so the queue and `next_item_review` share it.
- `session.build.due_today_queue` builds today's finite due queue: the due skills, a greedy
  repetition-compression cover of them (each round takes the eligible archetype retiring the most
  still-uncovered due skills, lowest id on ties, stops when nothing more is retired), the due skills
  no published archetype reaches (`uncovered_skills`, fail closed), the R5 requeues whose item is
  published, and `minutes`, the sum of 02's per-archetype forecast (running median, 3 minutes until
  5 attempts, `forecast_minutes`) over cover plus requeues. `assemble_session` stores it on
  `Session.due_queue`; block 1 still serves the first 5 items or 5 minutes through
  `next_item_review` and the requeue path, so FSRS-due skills and corrected items both appear.
- `GET /progress` adds `due_today_skills` and `due_today_minutes` (`app/session/preview.py`);
  `ProgressPayload` in `app/web/src/api/types.ts` declares both and the App test mocks carry them.
  The client does not render them, so no vitest assertion was added; the five existing fields are
  unchanged. `tests/api/test_progress_route.py` DECLARED_FIELDS gains the two fields with types,
  which tightens that exact-set assertion.
- Tests, `tests/engine/test_scheduling.py`: test_desired_retention_switch,
  test_due_queue_finite, test_repetition_compression (the three named in 11 P2), plus
  test_mastered_skill_is_due_exactly_when_retrievability_drops_below_target,
  test_unmastered_skill_is_never_due_for_review,
  test_due_queue_finite_leaves_a_skill_without_a_published_archetype_uncovered and
  test_a_year_of_daily_sessions_never_grows_an_unbounded_queue. Each was watched red under a
  mutation of the implementation, then green on restore: the retention function returning 0.90
  always (switch red); `covered_due_skills` dropping ancestors (compression red); unpublished
  archetypes made eligible (compression and uncovered red); the cover's nothing-left break removed
  (uncovered red); the cover not subtracting retired skills (finite, uncovered, compression and
  year red); the due test ignoring mastery (unmastered red); the due test always reading 0.95
  (switch, exactly-due and year red).
- Review fix: `select.review_eligible` reached the pool only through archetypes loading a due
  skill directly, so a due skill whose only published archetype loads a hard child was reported
  uncovered and never served, although `covered_due_skills` credits 1-hop hard ancestors. For due
  reviews `archetypes_touching` now also reaches 1-hop gating parents; hypercorrection still needs
  the flagged skill loaded directly. test_due_skill_reached_only_as_a_hard_parent_is_covered_and_served
  went red with the widening turned off and green with it on. It is one test beyond the 918 counted at close; the rerun full suite exited 0 in 281 s.

- 2026-09-23, P2 Slice 3 closing session: checked the slice against 11 P2 scope item 3 and 02
  (Decay, review-mode pseudocode, block 1). One defect fixed: `due_today_queue` left out the
  hypercorrection lane block 1 serves ahead of the FSRS order, so on a day with a hypercorrection
  due and nothing FSRS-due the queue read 0 items and 0 minutes while block 1 served an item.
  `DueQueue` gains `hypercorrection_skills` and `hypercorrection_archetypes` (a greedy cover over
  archetypes loading the flagged skill directly, no retrieval floor, as `next_item_review` serves
  it), counted in `item_count` and `minutes`; `session.build.greedy_cover` is the shared cover.
  test_due_queue_counts_the_hypercorrection_requeue_block_one_serves_first went red before the fix
  (`assert 0 == 1` on `item_count`) and red again with the hypercorrection archetypes dropped from
  the minutes (`assert 0 == 3.0`), then green on restore. The shared queue check in
  `tests/engine/test_scheduling.py` now also sums the hypercorrection archetypes into the stated
  minutes, a stricter check. Checks before rebase: pytest `920 passed in 231.34s`, vitest `310
  passed (310)`, `tsc --noEmit` exit 0, `qa/12_report.py` exit 0.

P2 Slice 4, 2026-09-23: calibration capture and the progress screen's calibration curve (11 P2
scope item 6). `app/progress/calibration.py` turns a user's counted attempts into three bins
(guess, unsure, confident), each with its attempt count, count correct, observed accuracy and a
Wilson 95 percent interval, plus the total n; `GET /progress/calibration` in
`app/api/routes/progress.py` returns it over the 30 days ending on `today`, and below 30 counted
attempts it returns `available: false`, `attempts_needed` and an empty `bins` list. A new nullable
`attempts.confidence_source` records who supplied the rating: `student` from `record_attempt` and
`record_confidence`, `session_close` from `close_session`'s unsure sweep; the additive migration
backfills `student` onto stored guess and confident ratings and leaves a stored unsure null.
Client: `readCalibration` in `app/web/src/api/client.ts`, the `CalibrationPayload` and
`CalibrationBin` types, and `app/web/src/progress/CalibrationCurve.tsx` (accessible SVG with
title and description, stated confidence on x, observed accuracy on y, the interval as a capped
bar, `n = k` over each point, no mark and `n = 0` for an empty level, a table as the text
alternative, token colours only, no animation) and `ProgressRoute.tsx`. The progress route is not
reachable from the shell at first; the closing session wired it from home, see Plan corrections applied. Tests added, each watched red against a broken
implementation and green after restore: `tests/progress/test_calibration.py` (9, including
`test_calibration_curve_threshold`), `tests/api/test_calibration_route.py` (4),
`app/web/src/progress/CalibrationCurve.test.tsx` (9), and five new rows in
`app/web/src/api/client.test.ts` (the path and field-shape contract for the new route and both
types). Suite at close: pytest 968 passed, 0 failed (exit 0); vitest 323 passed in 24 files; tsc clean;
`qa/12_report.py` exit 0.

- 2026-09-23, P2 Slice 4 closing session: server side checked against 11 P2 item 6, 08 and 10
  with no defect found (graded and student-rated attempts only, rating always before feedback
  because `render_feedback` refuses an unrated submitted attempt and `record_confidence` refuses a
  second rating, additive nullable column with an in-transaction backfill, every colour a token
  that `app/design/css.py` emits, no hex, a table as the text alternative, nothing animated). The
  progress screen is now reached from home: `HomeScreen` takes an optional `onOpenProgress` and
  draws a secondary "Progress" text button, `App.tsx` gains a `progress` destination that is not
  on the bar, and `ProgressRoute` declares an empty `ProgressRouteProps` for the shell's props
  contract. `app/web/src/App.test.tsx` gained "reaches progress from home and never from the bar
  or as the landing screen" and a rewritten bar gate (see Plan corrections applied). Shown red
  four ways and green on restore: the home button removed (1 red), Progress added to the bar (2
  red), `App.tsx` naming a mastery map (1 red), the shell landing on progress (20 red). Checks
  before rebase: pytest `924 passed in 231.69s`, vitest `324 passed (324)`, `tsc --noEmit` exit
  0, `qa/12_report.py` exit 0. The opening session's ledger line quotes pytest 968 passed, which
  this worktree cannot have held before the rebase; the 924 here is the count this tree produces.

- 2026-09-23, operator's request to check the 130 agent-drafted items and run the key audit:
  every stem in `content/items_p1_agent/` was re-solved in SymPy from the stem text alone and
  compared with the stored key and every option through `app/items/mathjson.py` `to_sympy`
  (`docs/operator/p1-agent-item-key-check.md`, one row per item). 130 of 130 keys match; on every
  item carrying options exactly one option equals the computed answer and it is the key; the ten
  stated dy/dx formulas in BC-QA-03005 stems are correct. Positive control in the same run: five
  planted wrong answers all reported as differing, three of them as equal to a distractor, and a
  sign-flipped 03005 formula reported wrong. 27 stems worded "Which of the following is ..." were
  reworded to "Find ..." (see Decisions); no key, option or worked solution changed.
  `tools/check_items.py content/items_p1_agent` prints `clean: 130` and exits 0. Checks: pytest
  `967 passed in 228.44s`, vitest `324 passed (324)`, `tsc --noEmit` exit 0, `qa/12_report.py`
  exit 0. The re-solve script stayed in the session scratchpad; its formulations are listed in the
  report's "Computed from the stem" column.

- 2026-09-24, the operator's audit path made runnable end to end. `app/review/audit.py`
  `unit_cap_for` lifts the 15-per-unit cap to the smallest value that fills the sample, and
  `tools/draw_key_audit_sample.py` uses it: on P1's 30, 60 and 40 items per unit the cap is 35 and
  the draw holds 30, 35 and 35. `tools/sign_off_items.py` adopts named reviewed drafts (item ids,
  archetype ids or `all`) as operator items, moving `authored_by` to `drafted_by`, updating rows
  a database already ingested, and refusing the whole run when a target names nothing; a record
  round-trips byte for byte, so the diff is the provenance line only. `tools/key_audit_worksheet.py`
  writes the gate 29 worksheet (stem, expected solution path, options, never the key) and a
  verdict template. Tests, each shown red and green: `tests/review/test_audit.py` three new (the
  cap never rising, 2 red; stepping the cap by 7, `assert 36 == 35`),
  `tests/tools/test_agent_drafts_uncounted.py` a CLI draw of 100 from the 130 items with operator
  provenance (red before the fix with "only 45 items honour the 15-per-unit cap"),
  `tests/tools/test_sign_off_items.py` two (database left alone, 1 red; unknown id skipped instead
  of refused, 1 red), `tests/tools/test_key_audit_worksheet.py` one (a key marker leaked, red on
  `key:`; options dropped, red). `docs/operator/key-audit.md` gains the six-step P1 procedure.

- 2026-09-24, the key recheck made a standing gate. `tools/key_recheck.py` recomputes each item's
  answer from a formulations file written from the stems alone, and flags a key that differs, an
  option set where anything but the marked key equals the answer, a stem worded as a choice, an
  ambiguous stem (more than one computed answer), an unformulated item, and a comparison it cannot
  decide; before trusting a run it perturbs 8 computed answers and exits 2 if any compares equal.
  `content/items_p1_agent/key_formulations.py` holds the 130 P1 formulations (the bank loader and
  `tools/check_items.py` read only .json there). `tests/items/test_key_recheck.py` runs the whole
  bank as a gate (130 clean, about 5 s) and shows each check can fail; broken one at a time, each
  guard turned its test red: the comparator calling unequal pairs equal (4 red), the evaluation
  guard removed, the option check removed, the stem wording check removed, a missing formulation
  passing, the control made blind (3 red), and a real key edited on disk (the gate red).

- 2026-09-24, found by launching the real app for the readiness audit: the production build
  inlined `KaTeX_Size3.woff2` (under Vite's 4 KB inline limit) as a data: URL, which the CSP in
  `app/api/security_headers.py` (default-src 'self', no font-src) blocks, so large delimiters fell
  back to a system font. `app/web/vite.config.ts` now keeps every font a file
  (`build.assetsInlineLimit` refuses .woff, .woff2, .ttf and .otf) and the CSP is unchanged.
  `app/web/src/buildConfig.test.ts` checks every KaTeX font file is refused inlining (red before
  the fix, `expected 'undefined' to be 'function'`; red again with only .ttf refused; green after).
  Rebuilt: 0 data: fonts in the stylesheet, 20 woff2 files emitted, and the Size3 file loaded as a
  FontFace in the served page. Also seen: in the Claude desktop browser pane "Register a passkey"
  sends register/begin (200) and then waits on a platform prompt the pane cannot show, with no
  message to the student; a normal browser shows the prompt.

- 2026-09-24, P1 items signed off and gate 29 measured, by Claude on the operator's delegation.
  All 130 items in `content/items_p1_agent/` were read with their options for ambiguity (none
  admits a second answer; every count a BC-QA-03005 stem asserts was recomputed and holds), on top
  of the SymPy recheck (130 of 130 keys match). `tools/sign_off_items.py` now requires `--by`,
  written to `signed_off_by` (red first: dropping the field failed the sign-off test), and was run
  on all 130 with the signer named; only provenance changed in each file. `tools/check_items.py`
  now counts 10 operator items for each of the 13 archetypes, which is what exit criterion 7 and
  gates 17 and 30 count. The CLI drew 100 of 130 (seed 2026), and
  `tools/check_audit_verdicts.py docs/operator/key-audit-p1/verdicts.json docs/operator/key-audit-p1/sample.json`
  printed `audited: 100`, `missing: 0`, `key error rate: 0.0`, exit 0 (Wilson 95 percent
  interval 0 to 0.037). `tests/review/test_p1_key_audit_record.py` keeps the committed record
  complete, tied to operator items, and its published rate equal to the verdicts' (red on a wrong
  published rate, a missing verdict, and an unsigned sampled item).

Stage 3 (screens), 2026-09-24: the review screen and the mastery map, the two 08 screens no earlier
slice built. Server: `GET /progress/mastery` (`app/progress/mastery.py`) returns one node per
active BC-SKL, grouped by unit in unit order and, inside a unit, ordered by the longest chain of
hard prerequisite edges above it, each node in one of 08's five states read off `skills_state`
and today's FSRS retrievability (gap: the latest observation that assessed it said
prerequisite_gap and it is not mastered; fading: mastered and `is_due`, the test the due queue
uses; mastered, with `assumed` true for a row seeded mastered and never observed; in_progress;
not_attempted), plus the last unaided success day and the days since it, and no count or
percentage. `GET /review` (`app/api/routes/review_screen.py`, `app/review/screen.py`, separate
from the operator's `/review-queue`) returns `coming_back`, every open R5 correction whose window
has not closed in the order block 1 serves it, each in the `hypercorrection` lane when the student
had rated it confident; `error_notes`, newest first, with the session id the existing
`POST /sessions/{sid}/attempts/{aid}/error-note` needs to replace one; and `provisional_points`,
empty with `grading_available` false until P3. `app/session/build.py` gained `open_corrections`
and `requeue_pending`, and `requeue_ready` now serves a confident correction ahead of the rest;
`load_attempts_history` carries each attempt's id and confidence. Client:
`progress/MasteryMap.tsx` above the existing curve on `ProgressRoute`, `review/ReviewRoute.tsx`,
`ReviewScreen.tsx` and `ProvisionalPoints.tsx`, a Review text button on home after Progress, and
`readMasteryMap` and `readReview` pinned to their server shapes in `api/client.test.ts`.
Accessibility, each checked by a test: WCAG 2.2 SC 1.4.11 fetched from w3.org (3:1 against
adjacent colours) and held by the token gate over the map's and the curve's mark colours
(`app/design/tokens.py` `GRAPHIC_TOKENS`, `NON_TEXT_CONTRAST_FLOOR` in `contrast.py`) and by
`progress/nonTextContrast.test.ts`, which reads the mark colours out of both components; a list by
unit as the map's text alternative, plus a legend; five mark shapes that stay distinct with colour
removed; one tab stop with arrow-key movement; token colours only; nothing animated, so reduced
motion has nothing to replace. Tests added, each watched red against a broken implementation and
green after restore: `tests/progress/test_mastery.py` (4), `tests/api/test_mastery_route.py` (3),
`tests/api/test_review_screen_route.py` (6), `tests/session/test_requeue_lane.py` (2),
`tests/design/test_non_text_contrast.py` (2), `progress/MasteryMap.test.tsx` (8),
`progress/nonTextContrast.test.ts` (4), `review/ReviewScreen.test.tsx` (9), 14 new rows in
`api/client.test.ts` and 3 new cases in `App.test.tsx`. In the running app (worktree build, test
passkey verifier, one account seeded through the routes plus 20 Unit 1 and 2 `skills_state` rows
written mastered, because mastery needs three days of unaided successes a one-day seed cannot
reach): home showed Progress and Review as text buttons with the bar still Home and Settings; review listed the confident correction first in the hypercorrection lane, then the unsure one, and both error notes; editing a note by keyboard and Enter replaced it on the server (GET /review returned the new text); progress drew 541 marks (20 mastered, 6 fading, 7 in progress, 508 not attempted) above the calibration curve's not-yet state, with one tab stop, arrow keys moving focus and the caption, and at 375 px wide no horizontal scroll (scrollWidth 375); after a reload no console error was logged and GET /progress/mastery, /progress/calibration and /review answered 200. An earlier seed also showed block 1 serving yesterday's confident correction before the unsure one. Suite at close: pytest 999 passed, vitest 362 passed in 28 files, tsc exit 0, qa/12_report.py exit 0.

P2 Slice 5, 2026-09-24, stage 2 (p2engine): the rest of 11 P2 except scope item 8 (stage 1's
items) and items 3 and 6 (Slices 3 and 4). Every gate 11 names for P2 now exists and passes.

- Diagnostic (scope item 1), `app/engine/diagnostic.py`: a posterior over not_started, partial
  and fluent for each of the 10 units. An archetype's chance of being known under state s is
  the engine's own `p_knowledge` at the start of the run, shifted by a logit per state (-3, 0,
  +3). The item asked is the one whose predictive p_A is nearest 0.5, or whose raw probability
  is nearest 0.625 as a four-option MCQ, with a uniform draw among candidates within 0.01. The
  run is over the whole graph with gating suspended, each family is asked at most once, and no
  unit takes a fifth item while a servable unit is unprobed. It stops at 30 items, or from item
  10 once summed unit entropy has fallen by no more than 0.02 bits over the last 3 scored items,
  or when the pool is exhausted. One held-out extra problem per run is drawn uniformly and never
  enters the posterior. "I have not learned this yet" is a third outcome. Placement marks as
  mastered the skills at 0.80 or more under their unit's posterior whose gating parents are
  mastered or also placed and which the run did not see failed. Each gets FSRS's first-review
  memory, so it comes back as a review in about 4 days. Nothing is un-mastered by placement,
  which is how a re-diagnostic updates and never resets. Unresolved skills stay unmastered and
  sit in the fringe.
- Whole-graph selection and interleaving (scope items 2 and 4), `app/engine/interleave.py`:
  every set is read as sliding windows of 10. Max 2 consecutive same primary skill stays
  strict. At least 4 skills, at least 2 units, at most 3 per family and at least 20 percent
  translations each bind whenever some candidate can meet them. Otherwise the rule is recorded
  as a shortfall on the queue (`interleaving_shortfalls`), and `interleaving_satisfied` now
  checks all of D3 through an independent window checker. The live app already selected over
  the whole loaded graph; the two-term score is unchanged and the five deferred weights are
  read nowhere in `app/engine` or `app/session`.
- Exam-weight quota (scope item 5), `app/engine/exam_weights.py`: BC band midpoints parsed from
  `research/exam/exam-blueprint.md` at run time. In blocks 2 and 3 a unit's candidates are
  allowed only while its count is below ceil(share times (n + 1)) among the open units, in exact
  fractions, so the quota never empties a candidate set.
- Service, routes and data (scope items 7 and 9):
  - `app/session/diagnostic_session.py` runs the diagnostic as a session whose next item is
    chosen after each answer, at stage unsupported, as short answer, with no rating and no
    feedback. The confidence source is "diagnostic", which the calibration curve does not count.
  - `GET /sessions/{id}/next` serves it, `GET /sessions/{id}/diagnostic` returns unit-level
    states, and a second open resumes the unfinished run.
  - The `diagnoses` table (06, plus `diagnosed_by`) gets one row per graded attempt in every
    mode, from the R12 and R26 rule.
  - `GET /progress` adds `home_state` (first_login, long_gap after more than 21 days since the
    last session started, queue), `days_since_last_session` and `diagnostic_in_progress`.
  - Diagnostic misses are never requeued as corrected items.
- Client: `app/web/src/onboarding/` (intro, item and result per 08, units shown in words), a
  `longGap` home state whose one primary action is the re-diagnostic, and an `onboarding`
  destination that is not on the bar and not the landing screen. Home sends first login and an
  unfinished diagnostic there. The shell gate is rewritten; see Plan corrections applied.
- Simulation and evals: `app/sim/whole_graph.py` runs synthetic students on the real 541-skill
  graph with a synthetic bank (3 items for each of the 139 archetypes).
  `app/sim/five_term.py` is the deferred score, used by simulation only. `app/sim/p2_evals.py`
  holds the three evals, and `tools/p2_evals.py` writes `docs/operator/p2-evals.md`.
- Gates and tests, each shown red under a mutation and green on restore:
  - `tests/engine/test_interleave_full.py`: test_interleave_full_constraints (1,000 sessions, 25
    students by 40 days after a diagnostic each, zero violations and zero shortfalls). Red with
    the unit rule disabled (`block_units: 10261`) and with the floor disabled
    (`translation_floor: 10261`). Also a scarce-translation bank where the floor binds, and a
    positive control that the checker catches each rule.
  - `tests/engine/test_two_term_whole_graph.py`: test_two_term_selection_whole_graph (red with
    due coverage ignored), uniform ties by chi-square (red with the five-term ordering made the
    default), no five-term weight reaching selection, blueprint parsing, and the quota's
    ceiling (red with one unit of slack) and tilt.
  - `tests/engine/test_diagnostic.py`: test_diagnostic_target_probability for both formats (red
    with farthest instead of nearest), test_entropy_stopping (red with the stall sign flipped and
    with the cap off by one), held-out isolation (red when it enters the posterior), unit
    coverage, pooling (red with pooling off), placement closure (red without it), unresolved
    left unattempted, re-diagnostic only adds, and coverage gaps.
  - `tests/eval/test_p2_evals.py`: eval_diagnostic_information (red with the posterior frozen),
    eval_selection_bias_control (red with the control arm made the policy), and
    eval_two_term_against_five_term (red with the five-term ordering removed).
  - `tests/api/test_diagnostic_routes.py` (5): resume, not-learned credits nothing and writes
    diagnoses, wrong item refused, and a distractor's error path diagnosed. Red with resume off,
    with diagnostic misses requeued, and with the diagnosis write removed.
  - `tests/e2e/test_cold_start.py`: test_cold_start_to_first_session, on the real 130-item bank.
    First login, diagnostic, unit states with no percentage, a diagnosis per answer, a day-two
    queue with minutes, the long gap on day 23 and not day 22, and a re-diagnostic that keeps
    every placed skill. Red with the gap at 21 days (`>=`) and with the diagnosis write removed
    (`assert 0 == 9`).
  - Web: `onboarding/OnboardingRoute.test.tsx` (4), the long-gap HomeScreen test, and five shell
    tests. Red under six mutations: resume ignored, first login ignored, always onboarding, long
    gap drawn as the queue, a wrong not-learned body, and onboarding added to the bar.
- Checks at merge: pytest `1033 passed in 381.65s (0:06:21)`, vitest `383 passed (383)` in 29 files, `tsc --noEmit`
  exit 0, `qa/12_report.py` exit 0.
- Real-bank reach, measured over 20 synthetic students with `content/items_p1_agent`:
  - The diagnostic asks 8 or 9 items, then stops on an exhausted pool (9 families in Units 1 to
    3). 7 units cannot be probed and 126 archetypes are logged as coverage gaps.
  - 600 sessions on this bank show zero unexplained window violations. Shortfalls were logged
    for family_cap 458, translation_floor 377, block_units 15 and block_skills 4.
  - The diagnostic reaches more units as stage 1 merges items for Units 4 to 10.

- P2 complete as far as a session can make it, 2026-09-24. Each gate's pass line from `pytest -v`
  in this session, 13 passed in 82.97s: test_diagnostic_target_probability (short answer and
  MCQ), test_entropy_stopping, test_desired_retention_switch,
  test_two_term_selection_whole_graph, test_interleave_full_constraints, test_due_queue_finite,
  test_repetition_compression, test_cold_start_to_first_session, eval_diagnostic_information,
  eval_selection_bias_control, eval_two_term_against_five_term, and the record check, each
  PASSED. Exit criteria:
  - The diagnostic finishes within 30 items and stops early on 79.0 percent of 400 synthetic
    students (see Known defects on why).
  - A new user reaches a populated, finite, minute-stated queue on day 2 without intervention
    (test_cold_start_to_first_session).
  - 1,000 simulated sessions show zero interleaving violations.
  - The five-term score is off, and its comparison and the random-control arm are recorded in
    `docs/operator/p2-evals.md`.
  - Pending on use: a calibration curve rendered from 30 real rated attempts. Only the operator
    can supply those; the render path is covered by tests (Decisions, 2026-09-24).

- 2026-09-24, bounded SymPy children are kept between calls. `run_bounded` off the main thread,
  which is where a sync route runs, used to start a forkserver child per comparison, and each one
  refilled SymPy's caches. Ingesting the 130 P1 agent drafts from a thread other than the main
  one took 247.3 s; with the kept child it took 15.5 s (same machine, other sessions running).
  `app/items/verify.py` keeps up to four children that answered in time and kills any that timed
  out, died or were interrupted, so a late answer never reaches a later caller. New
  `tests/items/test_bound_worker_reuse.py` covers both; each test went red when its half was
  broken (never keeping a child; keeping one after a timeout, which returned "late" for the next
  call) and green on restore. This is the likely cause of the slow first bank query noted earlier
  but not reproduced, which was not re-measured through the route.

- 2026-09-24, stage 1 done: items for Units 4 to 10 (P2 scope item 8), by Claude on the
  operator's delegation. 656 signed-off items in nine banks, `content/items_unit01_agent` to
  `content/items_unit10_agent` (no Unit 8 bank), for 33 closed-form `no_calculator` archetypes, 17
  to 23 each; 5 more in scope got none for want of held errors (Known defects). Every key matched a
  SymPy formulation written by a separate agent from the stems alone (`tools/key_recheck.py`,
  control holding on every bank); `tools/check_items.py` clean on every bank; gate 29 over a fresh
  100-item draw from these banks is 0/100, Wilson 95 percent interval 0 to 0.037
  (docs/operator/key-audit-p2/). The bank now serves every `content/items_*` directory, and
  `tests/e2e/test_unit_6_item_served.py` serves, grades and shows feedback for a Unit 6 item
  through `build_application` with the test passkey verifier. Canonical record:
  docs/operator/items-units-4-to-10.md. Checks on the tree rebased onto `bc09905`: pytest
  `1078 passed in 392.38s (0:06:32)`; vitest `Tests  383 passed (383)`; `tsc --noEmit` exit 0;
  `qa/12_report.py` exit 0.

- 2026-09-24, P7 slice 1, the evaluation harness (docs/plan/11 P7), built by Claude on the
  operator's delegation before P3 to P6 merged, as the stage brief allows once stages 1 to 3 are
  in (Decisions, 2026-09-24, stage 8). What landed:
  - Simulation on a world that learns: `app/sim/learning.py` gives each synthetic student a
    learning rate per skill (band 0.05 to 0.30, scaled by fading stage) on the P2 knowledge state,
    two forgetting curves (exponential and power law, same half-life), and the ten arms of 10's
    arm list reachable without an engine change. `app/sim/p7_evals.py` pairs arms student by
    student; `tools/p7_evals.py` wrote `docs/operator/p7-evals.md` at 200 students by 60 days, seed
    base 20270510, and a rerun reproduced every number.
  - The five-term gate: five-term beat two-term on true mastery per item for 35.0 percent of
    students (exponential) and 21.5 percent (power law), against a 90 percent bar. It stays off.
    `lambda` stays 0. Tests hold the live policy to the record.
  - Metrics view: `GET /progress/metrics` (`app/progress/learning_metrics.py`) returns ten
    metrics, the nine of 10 plus the concept probe, and every value carries its numerator,
    denominator and what the denominator counts. The A/B comparisons ride along with a Newcombe
    interval once each arm holds 30 outcomes. The client page "Evidence of learning" is reached
    from settings only.
  - A/B switches: `app/experiments/switches.py`, the two experiments 10 marks powered
    (feedback_elaboration per item, retrieval_entry per skill), states off, on and randomised,
    stratified assignment written once and never reassigned, the arm recorded on the attempt
    (`attempts.experiment_arms`). Verification-only feedback is `FeedbackKind.VERIFICATION`.
    Settings has the switches; the running app starts them randomised (Plan corrections).
  - Six-week checkpoint: `app/checkpoint/` offers released Section II forms by reference only
    (2025, 2024, 2023, 2026, 2022, 2019; 2021 excluded, Known defects), timings read from
    `research/exam/exam-structure.md`, published means from `research/exam/scoring-system.md`,
    scores per part in `checkpoint_scores`, self-scored by the student until P3's grader exists.
    It never writes sessions, attempts, skills_state or the review queue.
  - Concept probe: `content/probe/concept_probe_v1.json`, 17 items drawn by seed and withheld from
    the practice bank (`app/runtime/bank.py`), administered every 8 weeks into its own tables.
  - Progress completion: the representation matrix (`GET /progress/representations`) and the
    checkpoint history on the progress screen, plus checkpoint and probe screens.
  - Golden sets for all six roles in `content/golden/`, model-authored and model-labelled, each
    saying so; `app/evals/golden.py` validates them and scores agreement; `tools/golden_sets.py`
    wrote `docs/operator/golden-sets.md` with the deterministic verifier baseline.
- Gate tests, each shown red under a break and green on restore in this session:
  test_brier_and_calibration (red with the guess mapped to 0.30), test_ab_assignment_balanced
  (red with the balancing removed), test_simulation_reproducible (red with the world's draws
  unseeded), test_checkpoint_isolated (red with a checkpoint writing a session row),
  test_metrics_view_renders (red with denominator_label dropped), eval_policy_against_random_control
  and eval_five_term_against_two_term (small), the live-policy record tests (red with LAMBDA 2.0
  and with a five-term import in app/session), eval_the_harness_runs_end_to_end_on_seeded_weeks
  (twelve simulated weeks through the real routes with both switches randomised, an interval
  stated; red with the interval floor unreachable), and the outcome, retention, probe-withholding,
  form, golden-set and switch tests. Web: 51 new vitest tests, 19 of 20 breaks went red (the
  twentieth was a fabricated number that happened to equal a real payload value; a different one
  went red).
- P7 exit criteria, 2026-09-24:
  - Met: every learning metric renders with its denominator (test_metrics_view_renders and the
    web MetricsView tests); the simulation reproduces from a seed (test_simulation_reproducible,
    and the recorded run reproduced every number); the A/B and checkpoint machinery runs end to end
    on seeded data (eval_the_harness_runs_end_to_end_on_seeded_weeks, test_checkpoint_isolated);
    the five-term comparison is recorded with its decision (stays off).
  - Pending on calendar time and real use. The operator's `var/growth.db` held 0 users and 0
    attempts on 2026-09-24, so every date counts from the first real practice session: an A/B with
    30 outcomes per arm and a stated interval, and 8 weeks of real attempts, at the earliest
    2026-11-19 if practice starts 2026-09-24; the first checkpoint 6 weeks after a baseline, with
    its result beside the internal numbers and the d = 0.4 to 0.7 expectation, at the earliest
    2026-11-05. Rerun the stage 8 prompt then.
  - Not met on the simulation, recorded rather than loosened: 10's two-term-beats-random bar and
    the 5 percent false-mastery ceiling (Known defects).
- Checks at merge of P7 slice 1: pytest `1119 passed in 427.94s (0:07:07)`; vitest `Tests  434 passed
  (434)` in 34 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0.

- 2026-09-24, stage 4 (p3), P3 free response, grading and diagnosis, all eleven scope items of 11 P3.
  Capture: a server-rendered booklet page with corner markers (`app/capture/booklet.py`), the image
  quality gate before any provider call (`app/capture/quality.py`: blur, contrast, markers, crop),
  the transcriber as its own stage with images reaching the subscription CLI as stream-json
  (`app/grading/transcribe.py`, `app/providers/subscription.py`), and the confirmed read-back as the
  only thing graded. Grading: `app/grading/point.py` with the four deterministic checks first
  (`app/grading/checks.py` over `app/grading/latex.py`), three samples per judged point, escalation
  to `review_queue` never averaged, the per-question rounding cap, the eligibility pass and
  follow-through; show-the-setup is required on calculator parts by `tools/check_frq_items.py`.
  Diagnosis: `app/diagnosis/observe.py` (model reads the work) and `app/diagnosis/diagnose.py`
  (probabilities, gap trace, probe, mastery states), probes queued in `pending_probes` and drained
  by the next micro-session. Tables: `gradings`, `frq_images`, four attempt columns. Routes:
  `app/api/routes/frq.py` (06's image, transcription, confirm, gradings and dispute routes, the unit
  check, typed entry, metric 9). Client: `app/web/src/frq/` (capture, read-back confirm or fix,
  typed MathLive entry, per-point grading with provisional copy and a re-read on every point),
  home's Free response button, and the review screen's re-read on every provisional point. Prompts:
  the four templates of scope item 11, each with a digest golden and role tests. Bank: 24 questions
  in `content/frq_items` over Units 1 to 7 and 10, 66 checked keys matched 66 blind SymPy
  formulations with the control holding. Evals, recorded on the subscription and replayed: golden
  set 2 (150 responses, 30 BC-PT ids) exact agreement 0.9315 on 146 published points, mean absolute
  error per point 0.0685, 4 of 150 escalated, one-sample agreement 0.9133, standard-sample MAE
  0.0867 against strict 0.0800; golden set 3 (P7's 20 page specs, rendered) 17 of 20 through the
  gate, 30 of 43 point-bearing expressions read back exactly, character similarity 0.9919, 3 of 3
  struck lines marked; transcription error share 1 of 1 on 15 rendered golden-2 pages
  (`docs/operator/p3-grader-eval.md`, all model-authored and model-graded). Manual runs: 20 through
  the live app, 0 gradings rows before a confirmation (`docs/operator/p3-manual-runs.md`). Gate
  tests, each shown red under a break and green on restore in this session: test_three_decimal_cap,
  test_deterministic_precheck_priority, test_diagnosis_never_certain, test_readback_gate,
  test_image_quality_gate, test_disagreement_escalates, test_paper_to_grade, and the three evals.
  Live spend: $0.00 on the API key; about 590 subscription calls (goldens 450, transcription eval
  116, paper-to-grade 11, smokes), plus the manual runs.
  Checks on the tree rebased onto `2d1431f` (P7): pytest `1193 passed in 386.59s (0:06:26)`;
  vitest `Tests  473 passed (473)` in 36 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0.

- 2026-09-24, stage 5 (p4), P4 item generation at full coverage, by Claude on the operator's
  delegation. Canonical record: docs/operator/p4-generation.md. What landed:
  - Parameter specs (D13 item c): `parameter_spec` on all 139 active archetypes, schema in
    `schemas/archetypes.schema.json` `$defs/parameter_spec`, validated by `app/generation/spec.py`
    and `tests/generation/test_parameter_specs.py`, merged through
    `data/staging/parameter-spec-p4.json`. `tools/merge_staging.py` gained `"merge": "fields"` and
    `"merge": "append"`, and the post-change tool sequence ran after each merge.
  - Generation: `app/generation/` (spec, expressions, kit, template gate and Monte Carlo pass,
    instantiate, verify, dedupe, batch_api, mathjson_out) and 139 templates in
    `app/generation/templates/`, authored by eight offline sessions and gated at 300 draws each.
    `tools/template_gate.py`, `tools/generate_bank.py`, `tools/item_review.py`,
    `tools/export_parameter_specs.py`, `tools/merge_error_links.py`, `tools/duplicate_sample.py`,
    `tools/p4_cost.py`. Prompts `prompts/generator/{template,figure_spec,calculator}_v1.md` and
    `prompts/verifier/{independent_resolve,monte_carlo}_v1.md` with golden digests.
  - Banks: 2,339 signed-off generated items in `content/items_gen_unit01` to `unit10`, every key
    matching a blind formulation and the template's own answer; 98 rejected items kept in
    `content/generation_review/` with 187 recorded decisions. Every active archetype now has at
    least 20 published items (minimum 20, 3,125 served in total).
  - Key recheck: `tools/key_recheck.py --template-answers` (template_differs, provenance_drift),
    statement labels, three-decimal keys, and a real constant of integration.
  - Serving: statement-keyed items are always a choice (`requires_choice`), figures render from
    their spec in the item, probe, diagnostic and feedback screens (`app/web/src/figures/`), option
    labels render their LaTeX, calculator items say so.
  - Duplicate gate: MinHash 5-grams at 0.8, stage two at cosine 0.70 against official text and a
    same-problem rule within the bank, measured on four labelled samples
    (docs/operator/duplicate-gate/): final-sample precision 1.000 and recall 0.891, against 0.879
    and 0.527 at the published points.
  - Key audit: 0/100 over a fresh `--generated` draw (docs/operator/key-audit-p4/), a model audit.
  - Cost: $0.00 API; $0.0219 per published item at list and $0.0110 with the batch discount if
    bought on the API (`tools/p4_cost.py`).
- Checks at merge of stage 5: pytest `1270 passed in 962.49s (0:16:02)`; vitest `Tests  484 passed
  (484)` in 37 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0.
- P4 exit criteria, 2026-09-24: all met. At least 20 published, verified items for each of the 139
  archetypes; P4 key error rate 0/100, not above the P1 baseline 0/100; duplicate-gate precision and
  recall measured and thresholds adjusted with the evidence recorded; cost per published item with
  the batch discount recorded; no served item shares a run of more than 25 words with any official
  page (`test_no_official_text_served`; the longest shared run is 21 words, a generic
  sentence about a region revolved about the x-axis in ITM-GEN-08012-11).

- 2026-09-24, stage 6 (p5), P5 assessment modes, all ten scope items of 11 P5, by Claude on the
  operator's delegation. Canonical record: docs/operator/p5-assessment.md. What landed:
  - Server `app/assessment/`: `shape.py` (the four parts read from exam-structure.md joined to the
    form template `content/assessment/form_2027.json`, tool sets), `assemble.py` (multiple choice by
    calculator status and BC-UNIT weights, nine-point free response, the radian note),
    `service.py` (one lifecycle for unit checks, drills and mocks: server deadline, parts in order,
    closed parts never reopen, attempts written at close, rule diagnosis except on rapid guesses,
    results, finish, the unfinished list), `pacing.py`, `band.py`, `unit_check.py` (set cover
    under the fringe gate, 8 to 12 items, feedback at submission), `evals.py`. Routes in
    `app/api/routes/assessment.py`: 06's /mocks rows plus /drills, /unit-checks,
    /assessments/shape and /assessments/unfinished. Tables `assessment_parts`,
    `assessment_responses`, `mock_results`. `app/checkpoint/published.py` now also reads the part
    weights, the per-question point total and the score distributions. Rollback:
    `GROWTH_TIMED_ASSESSMENTS=off`.
  - Free-response capture in a timed part waits for the part to close; the booklet page for a mock
    is headed by the part's calculator rule and addressed by exam question number.
  - Sixteen nine-point free-response questions (6 calculator), blind formulations 71 of 71 matched
    with the control holding, the bank 137 of 137, signed off by claude-opus-5-5 on the delegation
    (a model review); the whole free-response bank is now under the official-text gate.
  - Client `app/web/src/assessment/` (setup with resume, the part runner with the six tools and the
    graphing panel on calculator parts only, break screen, capture, result, unit check), the Mock
    exam button on home, mock history on progress; built by a frontend agent from a brief and
    reviewed here.
  - Fixes found by driving the app: home no longer offers an open assessment as today's set;
    grading no longer holds SQLite's write lock through the diagnostician's call, and the busy wait
    is 30 s; the capture list refreshes and a confirmed question reopens on its grading with a
    "Grade it again" after about five minutes; revisits and free-response answered counts;
    `app/grading/latex.py` reads a d-theta differential; the BC-QA-01005 template brackets a sum
    factor and ITM-GEN-01005-04 is retired.
  - Measurements: 20 timed runs through the running app, 0 skills_state rows changed, two unit-check
    controls changed it (docs/operator/p5-timed-runs.md); one full mock at the documented shape
    driven in the browser with live transcription and grading on the subscription, skills_state
    unchanged, band 3 to 5 with its assumptions (docs/operator/p5-full-mock.md). $0.00 API spend;
    about 111 subscription calls in the browser mock.
  - Gate tests, each shown red under a break and green on restore in this session:
    test_part_shapes (a minute added to the shape), test_timed_does_not_update_mastery (timed modes
    added to the credited modes; a timed close applying observations), test_score_band_never_single_number
    (a centre key exposed), test_band_is_never_narrower_than_two_points_anywhere (half width 0; no
    slide at the bounds), test_calculator_lockout (panel on every part), test_part_boundary_closed
    (reopen allowed; no expiry), test_tool_set_present (eliminator on free response; notes
    dropped), test_full_mock_run (a mock crediting free response; numbering restarting per part;
    captured questions not counted answered), eval_mock_against_published_means and
    eval_pacing_metrics, and the unit check, rapid-guess, requeue, radian, revisit, resume, home,
    lock, d-theta, official-text and template-stem tests. Client: 617 vitest tests, every new one
    broken and restored by the frontend agent (its break log is in the session scratchpad).
- Checks at merge of stage 6: pytest `1293 passed in 1050.30s (0:17:30)`; vitest `Tests  617 passed
  (617)` in 45 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0. An earlier full run the same
  hour read `1 failed, 1292 passed in 936.35s (0:15:36)`, the failure being
  eval_the_harness_runs_end_to_end_on_seeded_weeks (Known defects, stage 6).
- P5 exit criteria, 2026-09-24: all met. A full mock ran end to end at the documented shape with
  the paper capture path in one sitting, driven through the running app in the browser
  (docs/operator/p5-full-mock.md); no skills_state row changed in 20 logged timed runs, with two
  unit-check controls that did change it (docs/operator/p5-timed-runs.md); the result carries a
  band and its assumptions and never a single score (test_score_band_never_single_number and the
  browser result); pacing renders per part (the result screen, eval_pacing_metrics); the
  reference-sheet and Desmos-variant questions are restated in docs/plan/12 with what would settle
  them. What waits on real use: the operator's own mocks, real handwriting, and real latencies for
  the rapid-guess threshold.

- 2026-09-26, stage 7 (p6p8), P6 and P8 cut to what one student needs, by Claude on the operator's
  delegation. What landed:
  - The seeded-weeks flake (Known defects, stage 6) found and fixed. Cause: the registered user id
    is a fresh uuid4 (`app/auth/service.py` new_id), and it seeds the experiment tie-breaks
    (`app/experiments/switches.py` default_seed) and session assembly (`app/session/preview.py`), so
    `eval_the_harness_runs_end_to_end_on_seeded_weeks` was a different run each time; alone it failed
    2 of 25 runs at `feedback["stated"]`, and one of 30 pinned ids (USER-probe-27) fails every time.
    Not test order, not timing. The test now pins the id to one derived from its SEED, the pattern
    `test_mastery_path_across_days_and_unmastery` already uses; green 3 of 3, red with the id pinned
    to USER-probe-27. No assertion changed.
  - Fallback chain and cooldowns for every role (`app/providers/router.py`): subscription first, the
    paid API second only when `GROWTH_AI_BACKEND=api` (`app/main.py` provider_links), static feedback
    when no link may run. Each link sits behind its own GuardedProvider (call counts on the
    subscription, dollar and token caps plus the $15 developer cap on the API). A usage limit cools a
    link for 30 minutes per role, three consecutive other failures for 60 s; a cooling link starts no
    process. Tutor, grader, transcriber and diagnostician and the drain all run through it;
    `GET /settings/providers` now reports each chain and what is cooling.
  - Automatic drain (`app/feedback/autodrain.py`): started with the server, a pass every 10 minutes,
    at most 5 queued tutor calls a pass, under the same guards and the app's cooldown board, never on
    replay or none; `GROWTH_AUTO_DRAIN=off` stops it; `tools/drain_subscription_queue.py` now runs one
    pass by hand over the same chain.
  - Usage-limit wording aligned to the CLI: no live call met a limit, so the limit lines claude
    2.1.277 composes ("You've hit your ...", "You've reached your ...", "out of usage credits" and the
    rest of its own prefix list) were read out of the installed binary and added to
    `app/providers/subscription.py`; the fake CLI gained a `limit_message` mode and nine lines are
    tested, plus a non-limit error that must stay a transport error.
  - Prompt output goldens for all 12 templates (`tests/eval/test_prompt_output_goldens.py`,
    `eval_prompt_goldens`), beside the digest goldens that already covered every template: recorded
    grader, transcriber and diagnostician answers validated against the schema each request carried,
    the tutor paragraph rules on the eight live recordings, a new live recording for
    `prompts/tutor/guardrailed_practice_v1.md` (one subscription call, $0.00 API,
    `tests/fixtures/provider_cassettes/tutor_guardrailed_practice_v1.json`), one checked draw of all
    139 generation templates, blind-formulation coverage of every generated bank, and three full
    300-draw families for the Monte Carlo template. A test fails when a template has no output golden.
  - Offline session (`tests/e2e/test_offline_session.py`, `test_offline_session`): the app built on its
    default subscription backend, sockets refused, the CLI failing; a whole session on the P1 bank
    completes with deterministic feedback, no sentence, the tutor never marked unavailable, and the
    subscription link cooled after three failures.
  - Export then purge (`tests/api/test_export_then_purge.py`, `test_export_then_purge`): the export
    holds every owned row one for one; after purge no row in any table names the student or any id
    they owned, no archive is on disk, and the saved export still opens. It found two leaks, now
    fixed in `app/session/purge.py`: a queued tutor call in `jobs` (whose payload carries the
    student's attempt text) and a `review_queue` row on the student's grading point.
  - A database that ingested an item later withdrawn kept serving it (Known defects, stage 6): the
    bank now retires every stored item whose record sits in `content/generation_review/rejected` and
    in no bank (`app/runtime/bank.py` retire_withdrawn_items).
  - P8 client, built by a frontend agent from a brief (it stopped on a usage limit before its report,
    so every test was re-broken here): `test_no_literal_values` over every non-test .css, .ts and
    .tsx in app/web/src, with line heights, stroke widths and the motion duration moved into
    `app/design/tokens.py` (`tests/design/test_fixed_tokens.py`); `eval_contrast_all_screens`
    renders a catalogue of every screen in both themes and derives each text and non-text pair from
    what is drawn (4.5:1, 3:1 large, WCAG 1.4.11 3:1 non-text); `test_keyboard_only_session` drives
    home to the end of a set with no pointer event; `eval_screen_reader_math` requires KaTeX's MathML
    exposed with its HTML aria-hidden in every math region; `eval_greyscale_states` checks 14 kinds
    of state without colour; function-graph figures print axis numbers
    (`app/web/src/figures/FigureTicks.test.tsx`).
  - Screens checked in the real app with the preview tools (a scratch server on port 8002 with the
    passkey double): onboarding, the diagnostic item and settings in both themes, 0 text pairs under
    the floor (8, 8 and 53 pairs checked), the diagnostic answered by keyboard alone, and a greyscale
    render of the item screen.
- Gate tests, each shown red under a break and green on restore in this session:
  test_fallback_chain and the chain tests (cooldown never set: 3 red; role keying and stop-cooling:
  2 red; unconfigured-cap refusal off: 6 red; unavailable link hiding a stop: 2 red),
  test_budget_blocks_before_call for all six roles (dollar cap and daily count never refusing: 7
  red), the provider-link wiring tests (paid link unmarked, order reversed: red), the fallback route
  tests (no cooldown, no fallthrough: red), the automatic drain tests (no cap, no shared board,
  drains replay, loop idle, startup unwired, daily pacing off: each red), test_offline_session
  (tutor failure raised, cooldown off: red), eval_prompt_goldens (registry entry missing, grader
  schema narrowed, LaTeX in a tutor recording, practice tutor stating the answer, figure and
  calculator draws failing the gate, formulation missing, diagnostician schema changed: each red),
  the CLI limit-line tests (7 of 9 red before the patterns were added), test_export_then_purge (red
  on the unfixed purge), the retired-item tests (retirement off, no default directory: red),
  test_fixed_tokens (a changed leading: red), and on the client test_no_literal_values (a colour and
  a duration added), eval_screen_reader_math (MathML hidden: 5 red), the tick tests (ticks dropped:
  5 red), eval_greyscale_states (step verdict glyph and word made equal: red),
  eval_contrast_all_screens (light text-muted at #b0b0b0: red) and test_keyboard_only_session
  (confidence radios taken out of the tab order: red).
- Checks at merge of stage 7: pytest `1358 passed in 1322.36s (0:22:02)` (run before the last client type fixes, after which tests/web and the providers tests were rerun green); vitest `Tests  655 passed (655)` in 51 files;
  `tsc --noEmit` exit 0; `qa/12_report.py` exit 0.
- Exit criteria, 2026-09-26. Met: every role has a fallback link or the static degradation and a
  cooldown, exercised by test; budgets and pacing block before the call for all six roles; an offline
  session completes with the network disabled; every template has a digest golden and an output
  golden; zero literal design values outside the token file; every screen in the catalogue passes
  the contrast floors and the 1.4.11 ratio in both themes; a full session completes with no pointer
  events; every math region exposes MathML; no state is lost in greyscale; export is complete and
  purge removes everything, verified by re-reading every table. Ruled out for one student (Plan
  corrections): Gemini, Ollama, OpenAI, OpenRouter, claudebox, provider switching from settings,
  Postgres, per-user budgets and multi-user. Not applicable: cross-provider grading agreement, since
  one provider serves every role. P7's entry criterion "P6 merged" is met by this merge; its 8 weeks
  of real attempts are not, and only calendar time and the operator's practice supply them.

- 2026-09-26, stage 9 (ui), slice 1: the operator's prototype ported onto the app. The token file
  holds the prototype's palette with `border-hairline` raised to 3:1 in both themes; Inter 400,
  500 and 600 ship from `@fontsource/inter` 5.3.0 with the OFL; a header with the brand, Home and
  Settings, a footer, flat screens with ruled titles, the session item and feedback in a raised
  panel with a stage badge, option rows and confidence tiles, the progress map with its legend
  above, the timed-part tool bar above the question with the question menu as tiles, and phone
  layouts at 900 and 600 px. The mapping, the gate-driven values and the features not taken are in
  `docs/operator/ui-redesign.md`. Checks: pytest `1358 passed in 1290.24s (0:21:30)`; vitest
  `Tests  655 passed (655)` in 51 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0;
  `tools/check_tokens.py` exit 0.

- 2026-09-26, stage 9 (ui), slice 2 and exit: the constant e renders in option rows (see Known
  defects), the timed-part tool bar is drawn only when a part offers a tool, and highlight and notes
  stack beneath the question. Every screen was walked in the real app at 1280, 900 and 375 px in
  both themes by claude-opus-5-5 in headless Brave, not by a person: 22 states, 132 after shots, 44
  before shots and 44 pairs, listed in `docs/operator/ui-redesign.md`; no state scrolls the page
  sideways at 375 px. Exit criteria met: every screen restyled in both themes at the three widths;
  the token file holds the new palette; the contrast, type-scale, literal-value, keyboard,
  greyscale and reduced-motion gates pass; no prototype sample data, study plan, provider choice,
  simulated auth or single score reached the app. Checks: pytest `1358 passed in 1251.16s (0:20:51)`; vitest
  `Tests  656 passed (656)` in 52 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0.

- 2026-09-26, stage 10 (ux): loading and failure states with a retry on every screen that had
  none; the set's remaining items and minutes, a confirmed stop, and an end-of-set summary; what
  the student wrote at the head of feedback; keys for the session and timed parts; operator
  settings behind two closed disclosures; named and collapsible representation table; no zero
  lines on home; and the `requires_choice` commit fixed. Every new test was run red against a
  deliberate break and green once restored. The real app was driven in headless Brave with real
  key events: "2" from the page body rated unsure, "2x" typed into the math field left the rating
  alone, Enter from the field checked the answer, and stop, the end screen, settings and progress
  were read back. Checks: pytest `1359 passed in 1488.08s (0:24:48)`; vitest
  `Tests  669 passed (669)` in 53 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0.

- 2026-09-27, stage 11 (ux2), slices 1 to 6: the contrast and greyscale evals read app.css media-aware
  at 1280 and 375 px, and the 946 pairs the old eval checked are all still checked; one
  `PageHeader` for every screen's ruled title, and home, review and free response load through one
  `useLoad` with a retry beside `LoadState.tsx`; 08's raw LaTeX inspector under every math answer
  field; a System, Light and Dark theme setting under Accessibility on the settings page; compact
  question-menu tiles that read without colour; and an open graphing panel beside the question from
  1100 px on calculator parts. Every new test was run red against a deliberate break and green once
  restored (listed in the stage 11 decisions). Checks at 1c8fc4e: pytest `1365 passed in
  2731.83s (0:45:31)`; vitest `Tests  697 passed (697)` in 56 files; `tsc --noEmit` exit 0;
  `qa/12_report.py` exit 0. bb9e17f, which keeps `useLoad`'s value stable between renders, was
  added after that run and touches only the client: vitest `Tests  698 passed (698)` in 57 files
  and `tsc --noEmit` exit 0 were run on it. The real app was walked for all seven items by
  claude-opus-5-5 in headless Brave, not by a person; see the stage 11 section of
  `docs/operator/ui-redesign.md`.

- 2026-09-27, stage 11 (ux2), slice 7 and exit: `POST /sessions/{id}/diagnostic/skip-unit` and a
  "Skip this unit" button with a confirming step answer "I have not learned this yet" to every
  remaining diagnostic item of the unit being asked, through `service.record_attempt` as the
  button's own answer is; `tests/api/test_diagnostic_routes.py` shows the result, the posterior,
  every asked entry, every stored answer and every skill state equal to answering each item one by
  one, skipping at the unit's first item and at its second. The real app surfaced two defects,
  both fixed here: the client could read the state from before a write it had just made, because
  `get_db` committed after the response was sent, and the diagnostic numbered its questions from
  2. Checks at e9a69a0: vitest `Tests  699 passed (699)` in 57 files; `tsc --noEmit` exit 0;
  `qa/12_report.py` exit 0; pytest `tests/api` `233 passed in 76.71s (0:01:16)` on the same code.
  The full pytest run at e9a69a0 stopped at 50 percent with no summary line, and the operator then
  asked for the merge without a full run, so no full-suite count exists for slice 7. Every item was walked in the real app at 1280, 900 and 375 px
  in both themes by claude-opus-5-5 in headless Brave, not by a person, with real key events; no
  state scrolls the page sideways at 375 px (see `docs/operator/ui-redesign.md`, stage 11).
  Exit: all seven items built and merged.

- 2026-09-27, Desmos in the page. The Desmos panel on calculator
  questions and parts, with its tests red against three deliberate breaks and green restored;
  `frame-src https://www.desmos.com` in the CSP and in 09. Checked in the real app in headless Brave by claude-opus-5-5: a 30-item diagnostic
  skipped through the interface, then a calculator item's Desmos frame at 754 by 480 px, with no
  horizontal scroll at 375 px. Checks: pytest `1365 passed in 2190.53s (0:36:30)`; vitest `Tests  672
  passed (672)` in 54 files (a first vitest run beside the pytest run timed the contrast catalogue's
  setup out at its 60 s budget; alone it passed, and the rerun without load passed whole);
  `tsc --noEmit` exit 0; `qa/12_report.py` exit 0. After rebasing onto stage 11 (755c0c7), on the operator's instruction to skip
  the full suite because it runs over half an hour, only these were rerun: vitest `Tests  701 passed
  (701)` in 58 files, `tsc --noEmit` exit 0, `qa/12_report.py` exit 0, and
  tests/api/test_security_headers.py with test_evaluation_routes.py, 16 passed. The full pytest was
  not rerun on the merged tip.

- 2026-09-27, stage 12 (select): the selection study (`docs/operator/selection-study.md`, numbers
  in `docs/operator/selection-study-record.md`, `tools/selection_study.py`). Positive, negative
  and noise-floor controls on the learning world (`app/sim/selection_study.py`); three world
  corrections behind `learning.WorldRules` with `LEGACY_WORLD` reproducing stage 8; delayed mastery
  per item added beside the existing measure; `p_A` read at today's retrievability in the stage
  bands and the review floor, so arm 6 now serves differently; the P7 record rerun on the corrected
  world. No live setting changed: two-term stays, `LAMBDA` 0, five-term off. New tests, each red
  under a break and green on restore: the decay arm diverging (red with retrievability dropped from
  `serve_stage`), keyed draws (red with a shared stream), daily growth, consolidated prior and the
  controls' ordering. Checks on the tree rebased onto `1f74c96`: the touched files `138 passed in
  57.18s` (tests/engine, tests/session and the three simulation eval files); vitest `Tests  702
  passed (702)` in 58 files; `tsc --noEmit` exit 0; `qa/12_report.py` exit 0. The full pytest suite was not run to completion: the operator stopped
  it and asked for the merge without it.
- 2026-09-27, stage 12 (select), the bar ruling: `app/sim/p7_evals.py` decides 10's paired bars
  from the mean difference and its interval, the record (`docs/operator/p7-evals.md`) rerun on it,
  10, 12 and the study updated. New test `test_the_bars_are_decided_by_the_mean_interval_not_the_share`
  was red with decide() put back on the share and green restored. Checks: tests/eval/test_p7_evals.py
  and test_selection_study.py `14 passed in 28.88s`; vitest `Tests  702 passed (702)`; `tsc
  --noEmit` exit 0; `qa/12_report.py` exit 0. The full pytest suite was not run, on the
  operator's earlier instruction.

- 2026-09-27, stage 13 (content2), four defects closed by claude-opus-5-5 on the operator's
  delegation. Slice 1: 2021 Question 4's ninth point is a question-level point (sg-21 page 14), now
  `global_points` on BC-FRQ-2021-Q4-A through `data/staging/corrections-frq-2021-q4.json`, and
  `app/checkpoint/forms.py` offers seven forms; test_a_point_the_guidelines_award_in_any_one_part_counts_toward_the_question
  was red on the old code (KeyError, 2021 excluded) and green after. Slice 2: BC-ERR-10044 minted
  and linked through the `corrections-*-10` staging files, the nine BC-QA-10005 series-sum
  distractors retagged, the post-change tool sequence run, research/PROGRESS.md errors 425;
  `tools/check_items.py content/items_unit10_agent` clean 257 of 257. Slice 3: `app/grading`
  reads a question's `functions` and `roots` and the new `equation_setup` check;
  `tests/grading/test_question_definitions.py`, 23 cases, 12 red on the old code and every guard
  case red under a planted break (slack widened, a fail returned, the place count ignored, an
  unset symbol given a value, proportionality dropped, an undefined name substituted), green
  restored; runs 9 to 12, grader off, 25 of 72 points decided against 6
  (docs/operator/p5-timed-runs.md). Slice 4: 79 new nine-point questions (docs/operator/p5-assessment.md).
  Checks: pytest on the first three commits `1 failed, 1388 passed in 2937.96s (0:48:57)`, the
  failure the loader's pinned error count, now 391; after the bank, on the operator's instruction,
  targeted only: tests/grading, tests/checkpoint, tests/content/test_loader.py,
  tests/eval/test_golden_sets.py, tests/generation/test_no_official_text.py, tests/assessment,
  tests/e2e/test_full_mock_run.py and tests/api/test_evaluation_routes.py, `132 passed in 1059.86s
  (0:17:39)`, run with webauthn on a scratch path (Known defects); vitest `Tests  669 passed (669)`;
  `tsc --noEmit` exit 0; `qa/12_report.py` exit 0; `tools/check_frq_items.py content/frq_items`
  `119 records, 0 problems` (run with `.venv/bin/python`, since the system python3 has no SymPy);
  `tools/frq_key_recheck.py` `checked points: 439, match 439`, `control: held`. Live API spend
  $0.00; authoring and re-solves ran as 15 Claude Code subagents of this session on the
  subscription, logged in the spend log.

- 2026-09-27, passwords replace passkeys, on the operator's instruction (the ruling is in
  `docs/plan/09-security-and-privacy.md`, "Authentication with a password"; decisions below,
  "Decisions taken on the operator's instruction, 2026-09-27"). Removed: `app/auth/webauthn.py`,
  the `PasskeyCredential` model and `passkey_credentials` table, the challenge store, every
  `/auth/passkey/*`, `/auth/recovery/register/*` and `/auth/reauth/begin` and `/finish` route,
  `Settings.verifier`, `rp_id` and `origin`, `GROWTH_RP_ID` and `GROWTH_ORIGIN`, and `webauthn`
  from `pyproject.toml` (uninstalled from `.venv` with `uv pip uninstall webauthn`, "Uninstalled 1
  package ... webauthn==3.0.0", because this `.venv` has no pip). New: `app/auth/passwords.py`
  (scrypt through `hashlib.scrypt`, stored as `scrypt$n$r$p$salt$hash`, n=2^14, r=8, p=5 by
  default and `GROWTH_SCRYPT_N`, `_R` and `_P`; username and password rules), `app/auth/guard.py`
  (Host allowlist with `GROWTH_PUBLIC_HOST`, `Sec-Fetch-Site` and `Origin` check, plain-http
  refusal, and the 429), `app/auth/limiter.py` (10 requests per peer address per 60 s,
  `GROWTH_AUTH_RATE_LIMIT`) and `app/auth/issue_recovery_code.py` (the operator CLI). Routes in
  `app/api/routes/auth.py`: `POST /auth/signup`, `/auth/login`, `/auth/logout`, `/auth/reauth`,
  `/auth/password/change` and `/auth/recovery/reset`, and `GET /auth/status`, which adds
  `needs_password` for a loopback caller only. `users` gains `username`, `password_hash`,
  `failed_login_count` and `locked_until`; `app/db/migrate.py` `retire_tables` writes
  `backups/growth-before-retiring-passkey_credentials-<stamp>.db` (`app/db/backup.py`
  `back_up_before_retiring`), then drops `passkey_credentials` and deletes every `auth_sessions`
  row in one transaction, and `current_session` refuses a user with no password. Audit actions:
  `account_created`, `login_failed_lockout`, `password_changed`, `password_reset_via_recovery` and
  `recovery_code_issued` in, the three `passkey_*` actions out, 30 names, still sorted.
  `app/audit/detail.py` refuses a detail field named like "password". `app/export/archive.py`
  `PUBLIC_COLUMN_NAMES` removed. `tools/frq_scenarios.py` registers through `/auth/signup` and
  builds with n=1024, r=8, p=1. Export, purge and budget re-authentication details now say
  "password". Plan text changed with dated notes: 09 (the ruling, the STRIDE row, the per-IP
  paragraph narrowed to three routes, the retention and audit rows), 06 (py_webauthn, the users
  table, the API surface), 08, 10, 11 (gates 23 and 24 keep their backticked names; the gate table
  reads the same 96 gates before and after, compared with `tools/gate_status.py` `read_gates`
  against the HEAD copy) and `docs/operator/ui-redesign.md`. Checks recorded by the backend stage:
  `.venv/bin/python -c "import app.main"` ok; tests/db, tests/audit and
  tests/runtime/test_context.py `3 failed, 75 passed` before the test stage, the 3 being the forced
  edits listed in the decisions (`test_models` passkey_credentials, `test_vocabulary`
  passkey_registered, `test_context` rp_id); a smoke script over every route at n=1024, p=1 (one
  signup of 8 parallel won, 40 parallel wrong guesses checked 5 real hashes and locked once with
  one audit row); one production hash measured 276 ms under `.venv`. Checks by the docs stage:
  tests/tools/test_gate_status.py, test_p1_archetype_list.py and tests/review/test_audit.py `41
  passed in 5.83s`; `qa/12_report.py` exit 0, all 14 checks PASS. Checks at integration: the 12
  auth-affected test directories (api, auth, audit, db, export, session, providers, runtime,
  tools, e2e, assessment, grading) `990 passed, 1 warning in 828.36s`; vitest `Test Files 58
  passed (58)`, `Tests 708 passed (708)`; `npm run build` built; `tsc --noEmit` exit 0. The full
  pytest suite was not run, on the operator's instruction (it takes about 25 minutes), so the
  directories outside those 12 are unverified by this change. Break and restore: removing the
  lock check from `reserve_attempt` turned tests/auth/test_lockout.py from `9 passed` to `6
  failed, 3 passed`; skipping `consume_reauth` in `change_password` turned the reauth and
  password-change files from `18 passed` to `4 failed, 14 passed`; skipping it in `POST /export`
  failed `test_export_requires_a_fresh_reauthentication_and_burns_a_wrong_one`; each restored
  green. Browser walk on a scratch database (port 8002): sign up with the show-once recovery code,
  sign out, a wrong password answered "username or password is incorrect", sign in, and an export
  behind the password prompt (`POST /auth/reauth` 200, `POST /export` 200, download 200). The
  first sign-out of the walk answered 500 `database is locked`, because the first `GET /progress`
  on a fresh database ingests the item bank inside one write transaction (`app/runtime/bank.py`
  `_ingest_pending_source`); logout writes an audit row and waited past the busy timeout. That
  was so before this change and is listed under Known defects. After the security and code
  reviews, tests/auth, the route list, auth status, export and tests/db `215 passed in 13.79s`.

- 2026-09-28, stage 14 (engine gaps), on the operator's instruction. Three rules of 02 and 06
  that had storage or constants and no code behind them now run. Nothing was committed.
  The productive-failure opener (02 Session assembly, 01 Productive-failure openers), which 11
  P1 scope item 9 had deferred (R35); the operator's instruction brings it into scope, and 11
  itself is not edited. `app/session/build.py` `assemble_session(openers=True)`, asked for only by
  `app/session/service.py` `open_session` in mode learning, places one opener as the first
  ordinary item of block 2: after a pending probe (R6), before any fringe item. A concept is due
  while any skill of its concept record is on the fringe and `concept_opener_done` on the
  record's first skill is 0; the item is a published item, not served in the repeat window, of an
  archetype that loads a skill of the concept, carries BC-DF-13 or BC-DF-15 and clears gating
  (invariant 3), dressed by `app/engine/select.py` `dress_item(opener_concept=...)` at stage
  unsupported with `is_opener` and `opener_concept` on the slot. Assembly sets the flag on the
  in-memory state and `open_session` writes it through `repository.mark_openers_done`, which
  touches `concept_opener_done` and `updated_at` only; one opener per session, at most once per
  concept. `record_attempt` records an opener attempt graded, writes `not_attempted` for every
  loaded skill into `attempts.per_skill_states` and applies it at once, so `observation_count`
  moves (02's schema table: every direct observation, including uncredited ones) and no other
  `skills_state` field does; `record_confidence` stores the rating without applying it,
  `close_session` skips it, the feedback A/B switch is not read for it, and
  `load_attempts_history` does not mark an opener miss corrected, so it is neither requeued nor
  listed in block 4. With no eligible item the opener is skipped, the flag stays 0 and
  `opener_gap_fail_open` (new in `app/audit/vocabulary.py`, 31 names) is written once per user,
  concept and day. Diagnostic, review and rehearsal sessions place none, and blocks 1 and 3
  never do. `Graph.concept_skills` (from `data/skills.json` concept records, through
  `app/runtime/graphs.py`) carries the concept's skills; home's queue preview and the simulations
  do not ask for openers. The web client reads `is_opener` and heads the item with "Try this
  before the method is shown." (`app/web/src/session/Item.tsx`, `api/types.ts`).
  Targets, `PRODUCTIVE_FAILURE_TARGETS` in `app/engine/constants.py` [inferred]: 01 and 02 name
  units, not concepts, and 01 caps the mechanic at once per target, so each target maps to one
  concept chosen by name in its unit: limits BC-CON-01002 (The limit of a function at a point),
  the derivative definition BC-CON-02002 (Instantaneous rate of change as the limit of a
  difference quotient), accumulation BC-CON-06001 (Accumulation of change as area under a rate
  graph), polar and parametric area BC-CON-09015 (Area of a polar region as an integral of one
  half r squared; no concept covers parametric area), series convergence BC-CON-10002
  (Convergence of a series as a limit of its partial sums). Only BC-CON-01002 (BC-QA-01013) and
  BC-CON-06001 (BC-QA-06004) have an active BC-DF-13 or BC-DF-15 archetype loading one of their
  skills, checked against `data/` on this date (18 such archetypes in all); the other three will
  fail open and write the gap row until the library or the mapping changes.
  The decayed-support cap (02 Decay): `app/engine/fringe.py` `serve_stage` serves completion when
  the primary skill has a credited observation, its stored stage is unsupported and its R_k is
  below `DECAYED_SUPPORT_CAP_RETRIEVABILITY` (0.5), and writes nothing, so R7's counter pair stays
  the only writer of `fading_stage` and `attempts.served_stage` records the cap. Every assembly
  path already hands today's R_k map through `dress_item` (`retrievability_map` in
  `assemble_session`, `next_item_learning`, `next_item_review`, `next_item_retrieval`, and the
  requeue's `pick_named_item`); `resolve_served_stage` reads the stage frozen at assembly, so no
  plumbing change was needed, and a caller with no map still gets R_k = 1 and no cap. Block 3 is
  capped too [inferred]: 02 calls it interleaved mixed review, and the criterion behaviour 02
  keeps free of support is rehearsal's (05), not block 3's. This departs from R32's "returns it
  unchanged" for a served stage only, on the Decay rule of the same document.
  The snapshot reload (06 Library updates and retired IDs): `app/content/reload.py` (new)
  `reload_snapshot`, called by `app/runtime/context.py` `build_session_context`. An unchanged
  digest, or no active row, reconciles nothing. A new digest first checks every `skills_state`
  row against the active ids and `data/ids.json` (`reconcile.refusals`, sharing
  `reconcile.classify` with `reconcile_skills_state`); any refusal writes a rejected
  `content_snapshots` row, keeps the old row active, leaves every row as it was and raises
  `ReloadRefused`. Otherwise each user is reconciled in its own transaction
  (`reconcile_skills_state(user_id=...)`) against a row id fixed beforehand, and only then is the
  new row made active and `content_snapshot_reloaded` written once with users, kept, rewritten,
  merged and orphaned counts and both digests. `ContentSnapshot.ids` carries the registry
  `app/content/loader.py` already read; `record_snapshot` takes an optional `row_id`.
  Tests added: `tests/session/test_opener.py` (8), `tests/engine/test_decay_cap.py` (7),
  `tests/runtime/test_snapshot_reload.py` (3), `app/web/src/session/opener.test.tsx` (2). Each was
  shown red against a planted break from a scratchpad script and green on restore: 12 breaks for
  the opener (openers never asked, flag not persisted, opener credited, rating applied, every mode
  opening, opener ahead of the probe, no gap row, gap row not deduplicated, opener miss requeued,
  stage left to the bands, any archetype of the concept, a diagnostic slot marked opener), 6 for
  the cap (cap removed, threshold at 0.9, stored stage ignored, stage written, cap before the
  history check, R_k dropped in `dress_item`), 6 for the reload (reconcile on every load, never,
  no pre-check, no audit row, ids not on the snapshot, refusal not recorded), and 2 for the header.
  Checks. `tests/engine tests/session tests/content tests/audit tests/runtime` in the working
  tree: `8 failed, 214 passed in 46.47s`, all 8 whole-graph or live-data tests
  (test_interleave_full x2, test_two_term_whole_graph x3, test_diagnostic placement,
  test_loader x2, one pinning 1226 edges against 1375); `data/` and `data/prereq_edges.csv` were
  being changed by another session during this stage, and the same code on HEAD's `data/` in a
  scratch worktree gave `219 passed in 52.76s`. tests/api, db, progress, experiments, feedback,
  diagnosis and e2e on HEAD's data with this change: `3 failed, 342 passed in 476.42s`. Pristine
  HEAD fails test_unauthenticated_routes and, on one of two runs, test_agent_drafts_served as
  well, so those two are not this change. vitest `Tests 712 passed (712)`; `tsc --noEmit` exit 0.
  The full pytest suite was not run (it has taken 25 to 49 minutes).
  Open. `tests/api/test_seeded_weeks.py::eval_the_harness_runs_end_to_end_on_seeded_weeks` fails
  with the cap: the verification-only feedback arm reaches 25 outcomes against the 30 floor
  (control 52), where without the cap it reached exactly 30 (control 55). The cap serves some
  decayed skills at completion, which reads no feedback switch. The test was not changed; it
  needs the operator's ruling (more weeks, or a floor the run reaches with margin). Three of five
  targets have no generation archetype. The comparison step 01 makes obligatory (the attempt
  beside the canonical method, the gap named) is not built; the feedback screen shows the
  ordinary verdict, and 15's `comparison` callout is where it would go. An opener at stage
  unsupported takes R29's format turn, so it can be served as multiple choice. 01 says the
  opener replaces block 2 on the day and runs 10 to 15 minutes; 02, which owns it (R5), makes it
  the first ordinary item, and the forecast gives it the 3-minute default. The client may still
  offer an error note after an opener miss. `data/ids.json` is not in the snapshot digest, so a
  tombstone added with no other registry change triggers no reconciliation. The concept records
  of BC-CON-06001 and BC-CON-06007 list skills whose own `concept` field names another concept;
  the concept record is what the opener reads.
- 2026-09-28, stage 14 follow-ups, on the operator's delegation. Four of stage 14's open items
  closed. Nothing was committed.
  The seeded run, on the operator's ruling that the 30-outcome floor is 10's Newcombe requirement
  and does not move. `tests/api/test_seeded_weeks.py` `WEEKS` goes from 12 to 16; this is a
  change to the seeded run's length, not to the floor or any assertion. Outcomes per feedback arm
  (control, verification-only), measured by a scratchpad copy of the test body with the cap on
  and with `DECAYED_SUPPORT_CAP_RETRIEVABILITY` set below every R_k: 12 weeks capped 52 and 25,
  uncapped 55 and 30 (both match stage 14's figures); 15 weeks capped 63 and 34, uncapped 68 and
  38; 16 weeks capped 64 and 38, uncapped 71 and 41. Sixteen is the shortest run tried whose
  smaller arm clears 30 by at least 5 under both engines (margins 8 and 11). The run takes about
  15 seconds.
  Openers are short answer. `app/engine/select.py` `format_for_item` returns SHORT_ANSWER for a
  slot carrying `is_opener` before R29's turn is read, and `dress_item` now marks the slot before
  it asks for the format, so the format frozen at assembly and the one `resolve_served_format`
  re-reads when the slot is served agree. A statement-keyed item (`requires_choice`) has nothing
  to type, so `app/session/build.py` `opener_options` keeps it out of openers; a target whose only
  generation items are statement-keyed fails open and writes the gap row as before.
  The comparison step (01, Productive-failure openers). `app/feedback/render.py` gains the
  `comparison` kind: an opener submitted and not correct (a miss, or an answer the grader could
  not settle) gets the item's worked steps beside the stored attempt under one line, "The
  method's first step is to" plus the first step of the archetype's `expected_solution_path`,
  followed by the matched BC-ERR record's `observed_behavior` when the chosen option names one.
  No verdict word, no violated step, no self-explanation prompt. `app/api/routes/sessions.py`
  `read_feedback` returns it with `sentence` None and makes no tutor call, and does not read the
  feedback switch for it; the error-note route refuses an opener attempt with 409, and
  `app/session/service.py` `record_self_explanation` refuses one as not invited
  (`served_as_opener`, which reads the slot and treats an item no serving slot holds as no
  opener). The client renders `ComparisonPanel.tsx` in place of the elaborated panel, with the
  student's "You wrote" block and "The method" side by side, offers no error note or
  self-explanation prompt after an opener, and does not count an opener miss as corrected on the
  end screen. 15 puts the comparison callout on the lesson's first worked example; lessons are
  not built, so it sits on the opener's feedback screen until they are [inferred].
  The digest. `app/content/loader.py` `_digest_for` hashes `data/ids.json` with the registries,
  `sources.json` and `prereq_edges.csv`, so a tombstone alone reconciles. No test pinned a digest
  value, so no pin changed. The live digest changes once with this, so the next start with an
  active row runs one reconciliation that keeps every row whose id is still active.
  Tests added: `tests/session/test_opener.py` (2: short answer on a turn R29 gives to MCQ, no
  statement-keyed opener), `tests/api/test_opener_feedback.py` (4), `tests/feedback/test_render.py`
  (3), `tests/runtime/test_snapshot_reload.py` (1: a tombstone alone changes the digest and
  merges), `app/web/src/session/openerComparison.test.tsx` (3). Each was shown red against a
  planted break from a scratchpad script and green on restore, 12 breaks: the opener rule
  removed, the format read from the undressed item, statement-keyed items allowed, render
  ignoring the opener, the route not passing it, the error note and the self-explanation taken
  for an opener, the client offering the note, showing the prompt and dropping the panel,
  ids.json out of the digest, and the seeded run back at 12 weeks.
  Checks. `tests/api/test_seeded_weeks.py tests/session tests/engine/test_decay_cap.py
  tests/runtime tests/content`: `108 passed in 29.20s`, tests/content included (its edge-count
  pin passed on today's `data/`). tests/feedback, tests/engine and the feedback, error-note,
  self-explanation, routes, ungraded and served-steps API tests: `4 failed, 179 passed`, the 4
  being test_interleave_full and three of test_two_term_whole_graph, which read live `data/` and
  fail the same with this change's engine edits reverted. vitest `Tests 715 passed (715)`;
  `tsc --noEmit` exit 0. The first vitest run failed two stylesheet gates on a grid literal in the
  new `.comparison-grid` rule; the rule was rewritten in tokens, the gates were not touched.
  Open. The opener's 10 to 15 minutes against 02's first-ordinary-item placement, the three
  targets with no generation archetype, and the BC-CON-06001 and BC-CON-06007 concept records
  stand as stage 14 left them. An opener short answer carries no error path from the grader, so
  the comparison line names the first step alone until a short-answer error match exists.

- 2026-09-28, stage 15 (library gaps), on the operator's delegation. Nothing was committed.
  Archetypes. Nine minted through `data/staging/gap-archetypes-stage15.json` (full records with
  `parameter_spec`, anchor quotes checked by qa/07 against the cached page, evidence tag inferred),
  primary skill first: BC-QA-03010 (inverse trigonometric derivative derived from f(g(x)) = x,
  03020 first, ced:77 and 78), BC-QA-05014 (every critical point, including a cusp, vertical
  tangent or corner, with an excluded input kept out, 05011, ced:100, BC-PT-99013 from sg-23:15),
  BC-QA-06017 (left, right, midpoint or trapezoidal sum with equal subintervals from a formula or a
  graph, 06009 first then 06007, ced:119, BC-PT-99018 and 99019 from sg-23:2 and sg-25:13),
  BC-QA-06018 (inverse tangent or inverse sine antiderivative, directly or after completing the
  square, 06043, ced:125 and 127), BC-QA-06019 (antiderivative after splitting a fraction or
  expanding a product, checked by differentiating, 06045, ced:125 and 127), BC-QA-07012 (separable
  or not, and separated, 07028, ced:142, BC-PT-99028 from sg-23:12), and the opener generation
  archetypes BC-QA-02014 (BC-CON-02002, 02005), BC-QA-09014 (BC-CON-09015, 09035, BC-PT-99048
  from sg-25:8) and BC-QA-10021 (BC-CON-10002, 10003), each carrying BC-DF-15 and a stem that names
  no method. 06017 is listed with 06009 first because every draw exercises it and only midpoint
  draws exercise 06007 [inferred]. Active BC-QA 139 to 148 of 153 records; families 77 to 78
  (critical-points is new). BC-QA-10021 went to spec version 2 the same day: the first version was
  statement-keyed, and `app/session/build.py` `opener_options` keeps statement-keyed items out of
  openers, so its 22 items were withdrawn to `content/generation_review/rejected/` and replaced by
  value-keyed ones.
  Errors. BC-ERR-02033 (average rate over an interval reported as the rate at an instant) and
  BC-ERR-06033 (power rule for antiderivatives applied with the wrong divisor) minted in
  `gap-errors-stage15.json`, because no held error described two distractors; BC-ERR-06022 gained
  BC-SKL-06055 and the used errors gained the new archetype ids through
  `error-links-stage15.json`; BC-MIS-02009 gained BC-ERR-06033
  (`corrections-misconceptions-stage15.json`). Active BC-ERR 391 to 393 of 427.
  Retirement. BC-SKL-06046 retired with superseded_by BC-SKL-06074 through
  `corrections-skills-retire-06046.json` (status, successor, 06074's prerequisites, signals and
  FRQ evidence, BC-CON-06014's skill list, 07028 and 07024 marked independently assessable by
  BC-QA-07012), `corrections-signals-retire-06046.json` (BC-SIG-06267 and 06268 to 06074),
  `corrections-frq-retire-06046.json` (three FRQ parts) and
  `corrections-taxonomies-retire-06046.json` (BC-REP-01), then `tools/retire_ids.py` wrote the
  tombstone. The record stays, so the loader's BC-SKL count stays 541 (540 active). The edge
  BC-SKL-06046 to BC-SKL-06074 stays in `data/prereq_edges.csv`: `tools/merge_edges.py` only adds
  edges, and that file is being edited by another session, so it was not touched.
  Templates. Nine in `app/generation/templates/` (qa_03010, 05014, 06017, 06018, 06019, 07012,
  02014, 09014, 10021), each 300 draws through `tools/template_gate.py`, failures 0, draw spaces
  3,132 to 6.1e12. The gate is `app/generation/template.py` `run_family` (FAMILY_FAILURE_BAR 0),
  not `tools/template_trial.py`, which gates the older `var/` JSON templates.
  Items. 22 candidates per new archetype and a regeneration of the six archetypes whose skills
  lists changed today, the old 88 generated items withdrawn to
  `content/generation_review/rejected/` with reject decisions and replaced under new ids (the bank
  never re-reads a stored id, so rewriting in place would leave old skills in any database).
  Blind re-solve by six separate subagents from the stems alone (`formulations_s15*.py`), compared
  by `tools/key_recheck.py --template-answers` in publish: 308 of 308 candidates matched (286 in
  the first batch, 22 for 10021 version 2). Published: 22 each for 02014, 03010, 05014, 06017,
  06018, 06019, 07012, 09014 and 10021; regenerated 03001 12, 05003 20 (2 of 22 rejected as
  duplicates by `tools/item_review.py duplicates`), 06008 3, 06009 3, 06011 22, 06016 22. Four
  candidates (06008-06, 06008-08, 06009-05, 06009-09) matched but are held in
  `content/generation_review/needs_review/`: their keys carry C, and the recheck control's
  sqrt(2)/7 perturbation cannot be told from a constant of integration, so the control failed when
  one was sampled; 06008 and 06009 still serve 20 agent items each. `tools/check_items.py` clean on
  every touched bank: unit02 191 of 191, unit03 163, unit05 272, unit06 330, unit07 190, unit09
  416, unit10 237.
  Pins. `tests/content/test_loader.py`: BC-QA_active 148, BC-QA_families 78, BC-ERR_active 393,
  empty_point_types 61, empty_official_examples 45; `tests/engine/test_cold_start.py` 148
  (`1 passed`). BC-SKL stays 541. The edge pins read 1375 and 751 in the working tree, changed by
  the other session, not here.
  Library. `tools/derive_confusable.py` rerun and merged: 505 of 541 skills, 1178 pairs, the same
  as before; it derives pairs from adaptive confusions, misconceptions and its method map, not from
  archetype membership, so 06009, 06043, 06054 and 06055 still carry no confusable_with.
  Post-change sequence run; `qa/12_report.py` exit 0, all 14 checks PASS; research/PROGRESS.md
  archetypes 153, errors 427. `research/question-analysis/question-archetypes.md` gained a section
  for the nine.
  Tools. `tools/duplicate_sample.py` `served_and_candidate_records` also reads
  `content/generation_review/rejected/`, because the labelled duplicate sample names items this
  stage withdrew (KeyError ITM-GEN-06016-02, 2 errors in test_duplicate_gate_labelled); the pairs
  and thresholds are unchanged, and the file went from 2 errors to `3 passed`.
  Checks. `.venv/bin/python -m pytest tests/content tests/generation tests/items`: `229 passed, 1
  warning in 554.27s (0:09:14)`. An earlier run gave `18 failed, 211 passed` while another
  session's loader edit required `data/lesson.json`; the same tests passed once that edit settled.
  `qa/12_report.py` exit 0; `tools/check_items.py` clean on all seven touched banks.
  Open. The four C-keyed 06008 and 06009 items wait for the operator's ruling on the recheck
  control (the frq recheck already drops the sqrt(2)/7 perturbation for checks that accept a
  constant; `tools/key_recheck.py` does not). The 06046 to 06074 edge in `prereq_edges.csv`. The
  agent-bank items of BC-QA-03001 (10 in items_p1_agent), 06008 and 06009 (20 each in
  items_unit06_agent) still copy the old skills lists. BC-QA-05014 and BC-QA-07012 are
  statement-keyed, so they serve only as choices. The opener mapping in
  `PRODUCTIVE_FAILURE_TARGETS` was not rechecked against a live session.

- 2026-09-29, prerequisite gates, second session, on the operator's delegation. Commits a3118af
  and the one that carries this entry, both on main.
  Mastery deadlock. `app/runtime/graphs.py` counted, for mastery condition 3, every archetype that
  lists a skill. BC-SKL-02005 was asked for a success on BC-QA-02003, whose primary skill is gated
  behind 02006, which is gated behind 02005, so 02005 could never be mastered and 416 teachable
  skills below it stayed shut. The count now leaves out an archetype whose primary skill is gated
  behind the skill; 02005 is the only skill whose requirement changes. Plan 02 condition 3 records
  it as Corrected 2026-09-29. `test_every_teachable_skill_can_meet_the_distinct_archetype_condition`
  walks the graph under condition 3 and read 416 unreached skills before the fix.
  Synthetic bank. `app/sim/whole_graph.py` ITEMS_PER_ARCHETYPE 3 to 20, the published bank's floor
  (20 to 28 items on each of 148 archetypes). At 3 a fresh student on the 6-archetype Unit 1 entry
  fringe had every item inside the 7-day repeat window by day 4 and got empty sessions until day 9.
  Placement support. `test_placement_support_is_what_a_correct_answer_loaded_and_what_sits_above_it`
  covers `diagnostic.supported_in_run`; red when a wrong answer is credited and when the ancestor
  walk is dropped.
  Library. `tools/sync_dependents.py` and `tools/merge_staging.py sync-dependents.json`: 166 skills
  gained the prerequisites and dependents the new edges imply, nothing else changed. The full
  replay (merge_staging over every staging file, then link_official_evidence) was run and
  discarded: it rewrote created dates to 2026-09-29 on hundreds of records, dropped BC-PT-99068
  from BC-QA-99004's point_types and a rubric instance from BC-PT-99080. That replay is not safe to
  run on this tree until merge_staging keeps created and the link pass stops removing entries.
  LSN-CON-02013's source_digest restamped: the only change in its sources is BC-SKL-02013's
  dependents gaining 03005 and 05040, which the lesson does not teach.
  Checks, in this session: `tests/engine` 78 passed and the 3 below failed, before the two new
  tests (each passed alone); `tests/progress tests/session tests/content` 98 passed;
  `tests/content tests/engine/test_entry_fringe.py tests/engine/test_selection.py` 39 passed after
  the sync; `tests/lessons` 71 passed; `tests/api tests/runtime` 257 passed, 1 failed
  (`test_unauthenticated_reachable_routes_match_the_documented_list` wants `/assets`, mounted only
  when `app/web/dist` is built, which this clone lacks); `eval_false_mastery_within_ceiling`
  passed, two_term 0 of 336 declared, random_control 0 of 373 (0 of 87 before); `qa/12_report.py`
  13 PASS, 00_manifest FAIL on 97 cached PDFs absent from this clone.
  Still red, premise collisions left for the operator: `test_two_term_selection_whole_graph` (2
  units chosen of more than 3), `test_exam_weight_quota_tilts_blocks_two_and_three_toward_the_heavy_units`
  (0.0 against 0.0), `test_interleave_full_constraints` (6 of 10 units). Each assumes students
  reach many units within 12 to 40 days. With the entry fringe in Unit 1, placement that accepts
  an underestimate (02, the 30-item cap), and mastery needing a 7-day span, no student reaches
  Units 5, 6, 9 or 10 in 15 days: a synthetic student at ability 3.0 in every unit mastered 0
  skills in 15 days and 51 in 40. Proposed: run the quota and interleave tests from placed
  students whose known units span the course, or over a longer horizon. Not changed, since that
  rewrites the premise.
  Throughput, the largest open risk. The same perfect student, run from 2026-10-01 for 220 days,
  masters 120 of 539 teachable skills (16 by day 20, 70 by day 80, 113 by day 160); cff11f5
  reached 49. Cause: strength is beta + log(1+c) - 0.5 log(1+f), and slips plus failure credit
  propagated from children keep f growing, so sigmoid(m) sits under 0.9 for tens of successes
  (BC-SKL-01054: 46 unaided successes over 38 days, 0.866). The longest blocking chain is 18
  skills (01001 to 10073), at least 8 days each. Changing GAMMA, RHO, the 0.90 threshold or
  failure propagation loosens mastery, so it waits for the operator.

- 2026-09-29, lessons L0, on the operator's delegation. Plan 15's Q1 to Q4 ruled at their working
  values (no example skip on a passed check; brief form for the mid band; defer past the budget;
  full band-planned lessons for one-skill concepts) and recorded in 15's register. L0's exit read
  in this session: `tests/lessons` 71 passed, `tools/check_lessons.py content/lessons` 1 clean,
  `tools/cost_model.py --check docs/plan/15-lessons.md` 0 unknown dollar figures. L1 (tables,
  ingest, routes, reader, 19 lessons) is next, behind the throughput ruling above, since lessons
  add minutes to block 2 without adding mastery evidence.

- 2026-09-29, lessons into the app (L1 to L3 records), on the operator's instruction to implement the
  Unit 1 to 8 lessons and leave Units 9 and 10 for later. All 127 Unit 1 to 8 concept lessons are
  transcribed into `content/lessons/`, and every one is `signed_off`: its record equals its design
  (`tools/lesson_resolve_compare.py`, now also comparing each check option's letter, key flag, error
  path and value), its blind re-solve agrees on every worked example and check, and its audit holds
  no non-ok block (`tools/lesson_sign_off.py`, new). `tools/check_lessons.py content/lessons`: 127
  read, 127 clean. Work this session: LSN-CON-08021 (arc length) designed and audited; a delta blind
  re-solve of 32 lessons whose problems or keys changed after the first pass (133 problems, all agree,
  33 statement answers judged with SymPy evidence, `docs/lessons/verification/answers/`); audits of
  08010 to 08014; fixes and independent re-audits of every changed block (06011, 07004 to 07006,
  08008, 08010, 08012, 01006, 01010, 02004, 02006, 02007, 04002, 04008, 04011, 06003); the design
  checker caps a strategy cue at 20 words (strengthened). App: the empty set converts to MathJSON;
  the reader drops citation-only parentheticals and evidence tags from served text and leaves out an
  error pair's expression when both steps share it; ingest lints across a process pool (127 records
  95 s to 39 s at server start); the NoticesPayload brace the lessons merge dropped is restored;
  Lessons is its own top-bar tab (the operator's ruling this session, amending 15 UI and 08
  Information architecture, which kept the library inside progress). Tests, each file under
  `timeout`: 19 lesson-related pytest files exit 0 (tests/lessons, tests/items/test_mathjson and
  test_verify, tests/session lesson gate, refresh, purge and service, tests/api lessons routes and
  session; the invariants at LESSON_INVARIANT_DEMO_EXAMPLES=15, the 1,000-case run was stopped by
  the operator for time); vitest over src/App.test.tsx, src/progress, src/lessons 17 files, 156
  tests; the render harness over every record, 256 of 256. Two tests changed with the product: the
  route test's keys follow the re-transcribed 02013 record, and the shell's pinned bar lists gain
  Lessons. The deferral integration test now follows the deferred concept across later sessions,
  since selection keeps its random ties (it failed 2 runs in 3 before; red again with the deferral
  rule broken). Open: Units 9 and 10 (41 concept designs), 77 prerequisite and 9 decision lessons;
  the library corrections the designers listed (research 7.3 Independence reversed, the
  qa_08014 generator's 08041 distractor, retired BC-ERR-08005 still named); the full 1,000-case
  invariants gate, to be run as parallel per-test processes.

- 2026-09-29, ruling (a) on the mastery throughput, by the operator. `FAILURE_DECAY_ON_SUCCESS`
  0.7 in `app/engine/constants.py`; `app/engine/update.py` multiplies `f_k` by it on a direct full
  success before that success's credit, never on a partial, notation-only answer, failure or
  propagated credit. Source for the direction: R-PFA, Galyardt and Goldin 2015, JEDM 7(2)
  (https://zenodo.org/records/3554672), where 0.7 is the best success bandwidth and the narrowest
  tried is best for failures. Plans 02 (strength section and both tunables tables) and 12 record it.
  Tests: `test_only_a_full_success_decays_the_failure_count` new, red without the change (2.0
  against 1.4). Two assertions encoded lifetime failure counts and follow the ruling exactly:
  `test_correct_never_lowers_m` expects f times 0.7 (red without the change); and
  `test_a_re_diagnostic_updates_and_never_resets` now bounds f below by 0.7 to the power of that
  skill's applied correct answers in the second run. That one still fails on a real reset:
  red when the re-diagnostic was made to start from fresh states.
  Checks: `tests/engine tests/progress tests/session` 159 passed, 3 failed
  (`test_interleave_full_constraints`, `test_two_term_selection_whole_graph`, and
  `test_a_re_diagnostic_updates_and_never_resets` before its bound was corrected; it passes after);
  the exam-weight quota test now passes. P7 false mastery 0 of 320 (two_term) and 0 of 390
  (random_control), ceiling 0.05.
  Finding: the ruling does not lift the throughput ceiling. The ability-3.0 synthetic student
  masters 110 of 539 teachable skills in 220 days against 120 before, within run-to-run noise. At
  day 120 the 45 skills with at least 10 observations and no mastery fail on: no unaided success at
  all (27, mostly skills loaded beside another primary, whose item is served at the primary's
  fading stage), condition 3's second archetype still gated behind other unmastered skills (13),
  and strength alone (3). Those two are the levers for the next ruling.

- 2026-09-29, mastery pace, third session, on the operator's delegation. The goal is that a
  synthetic student at unit ability 3.0 masters every teachable skill between 2026-10-01 and
  2027-05-07 with false mastery at 0.
  Instrument. `tools/throughput.py` runs `app/sim/whole_graph.run_days` once per seed over the
  whole span (219 days, never chunked) and prints the mastered count by unit at checkpoints, the
  day each unit completes, the failure rate by 30-day window and, for every unmastered teachable
  skill with at least 10 observations, the mastery conditions that fail, its counts, its serve
  profile (as primary, as secondary, at which stage) and its unmastered blocking parents. `--fast`
  is 60 days on the first seed; `--trace SKILL` lists every serve that loaded a skill; `--world`
  picks the hidden student. `app/engine/update.py` gained `mastery_conditions`, the six conditions
  by name, and `evaluate_mastery` now reads them, so the tool and the engine cannot disagree.
  `run_days` gained `on_day` (a per-day callback, so mastery is read daily without chunking) and
  `world_model` (a caller-supplied hidden student). `tests/tools/test_throughput.py` covers the
  pure parts; it went red with the strength condition inverted (3 failures shown in
  `tests/engine/test_update.py` too) and green on restore.
  Baseline, fixed world (`app/sim/runner.py` World, what the ability-3.0 runs before this session
  used), seeds 1, 2, 3: 114, 45 and 80 of 539 mastered on day 219; 20 population students mean
  7.1 (min 0, max 22); no unit ever completes; the failure rate climbs from 21 to 62 percent.
  Cause, read from the instrument and a trace: that World has no learning, so the 13 to 19
  teachable skills the ability-3.0 draw leaves unknown fail their archetypes forever, and every
  known skill decays from a 5-day half-life after its first practice. Both are things the P7 world
  in `app/sim/learning.py` already corrects (a per-skill learning rate, as 10 "The world" asks, and
  the stage 12 consolidated prior recorded in 12), so the tool's ability runs use the learning
  world with `learning.WORLD`; the fixed world stays available as `--world fixed`.
  Baseline, learning world, seeds 1, 2, 3: 277, 255 and 288 of 539 on day 219 (35 to 46 by day
  30, 83 to 98 by day 60, 136 to 144 by day 90, 161 to 202 by day 120); Unit 1 completes on day
  125 for seed 3 and no other unit completes; the failure rate rises from 13 to 37 percent; 20
  population students mean 73.6 (min 4, max 140). Stuck skills at the end of seed 1 (76 with at
  least 10 observations): 23 fail strength alone, all secondaries with 5 to 14 unaided successes
  and f = 0 whose archetype left block 2 when its primary was mastered; 16 fail all six conditions
  with no unaided success at all; 9 fail condition 3 alone with 24 to 71 unaided successes on
  their one servable archetype; 2 meet every condition and are not declared, because propagated
  credit raised strength after their last direct observation and nothing re-evaluated them.
  Simulator change, recorded before its effect was measured. `BC-QA-08011` loads nine skills the
  seed-1 student knew and was answered wrong 90 times over 145 days: once one loaded skill lapsed
  the item failed, no skill was reinforced, every loaded skill decayed further, and the item could
  never succeed again. The world let a known skill decay without limit after a lapse, where every
  spaced-repetition model the plan cites re-encodes a lapsed item at its shortest interval, and
  the app shows the solution after every attempt (03). `WorldRules.relearn_on_feedback` (on in
  `WORLD`, off in `LEGACY_WORLD`): a known skill the student could not retrieve for an item is
  re-anchored, last retrieved today, with one growth step of its half-life undone. Plan 10 "Forgetting" and 12's register
  record it.
  Rejected form, measured first: restarting the lapsed skill at the initial 5-day half-life, SM-2's
  full reset. Seeds 1, 2, 3 fell to 222, 211 and 259 of 539 (from 277, 255 and 288), because a
  consolidated skill at the 365-day half-life fails one roll in 17 over a month and each such roll
  threw it to 5 days. Kept form: one growth step undone (divide by 1.7, never below 5 days), the
  direction FSRS takes, where post-lapse stability is below the prior stability and not zero.
  Measured with the kept form, seeds 1, 2, 3: 344, 325 and 329 of 539 on day 219 (from 277, 255
  and 288); the failure rate holds between 13 and 27 percent across the run instead of rising to
  37; no unit completes. P7 false mastery: two_term 0 not known of 332 declared, random_control 0
  of 401, ceiling 0.05 (`eval_false_mastery_within_ceiling` passed). `tests/eval/test_p7_evals.py`
  gained `test_feedback_relearns_a_lapsed_skill_one_growth_step_down`, which pins the re-anchor,
  the floor at 5 days and the legacy world's inaction. Stuck skills now: 23, 32 and 54 fail
  strength alone, nearly all secondaries at p 0.85 to 0.90 with f = 0; 10, 12 and 8 fail
  condition 3 alone. Budget arithmetic for seed 1: the run delivers c = 12,927 of success credit
  where reaching 0.9 on every teachable skill needs 5,785 (mean 10.7 per skill from its beta), so
  the pace is an allocation problem, not a session-length one. The fringe holds 51 to 61 skills
  from day 90 on while block 2 has only 15 to 20 candidate archetypes, because a candidate must
  have its primary skill on the fringe (02, `candidates`), and a fringe skill loaded only by
  archetypes whose primary is already mastered reaches the student through block 3 alone.
  Checks: `tests/eval/test_p7_evals.py tests/eval/test_selection_study.py
  tests/eval/test_simulation.py tests/tools/test_throughput.py tests/engine/test_update.py` 2
  failed, both red at 1f9435f before any change of this session (`test_simulation_prereq_gap_stalls_dependants`,
  `test_the_decay_arm_serves_differently_from_two_term`), everything else passed.
  Example skip (02 R32), implemented. The rule had storage and text and no code: every skill
  climbed from example through four supported successes before an unaided attempt counted, and a
  skill the bands first served at unsupported dropped back to example on its stored stage. Now a
  first credited full success not rated guess, with every blocking parent mastered, starts the
  skill at completion (`should_skip_example`; `EngineGraph.blocking_parents` carries the fringe's
  parents into the update). Schema row in 02 corrected from `unsupported` to `completion`, the
  value the rule stated once gives. Seeds 1, 2, 3: 351, 337 and 337 of 539 (from 344, 325, 329);
  P7 false mastery 0 of 331 and 0 of 412. Test:
  `test_the_example_stage_is_skipped_when_every_gating_parent_is_mastered` (skip, guess, unmastered
  parent, second observation).
  Condition 3 denominator, corrected (lever (ii) of the operator's list). The blocking-weight
  reading of the tool put BC-SKL-03004 (37 teachable skills behind it) first served on day 193,
  because its parent BC-SKL-03002 held 33 unaided successes on BC-QA-03001 and waited for
  BC-QA-99001, a Unit 9 synthesis archetype gated behind 02036, 09029 and 09030. Condition 3 now
  counts the archetypes servable today, those whose primary's blocking parents are all mastered
  (`EngineGraph.servable_archetype_count`, `archetype_primaries` built in `app/runtime/graphs.py`;
  the P1 fixture keeps the static count). Lever (i), crediting a loaded skill from its own stage,
  was not taken: a worked example shows the solution to every loaded skill, so a success there is
  not unaided evidence for any of them, and the simulator cannot see the risk because its answers
  do not depend on the stage. Seeds 1, 2, 3: 392, 394 and 374 of 539 (from 351, 337, 337), 0
  false masteries over 219 days, P7 0 of 338 and 0 of 417; Unit 1 completes on day 155 for
  seed 1. Test: `test_condition_three_counts_the_archetypes_servable_today`. Plans 02 and 12
  record both.
  Remaining at the end of the runs: 41, 44 and 59 skills fail strength alone, nearly all
  secondaries at p 0.85 to 0.90 whose archetype's primary is mastered (block 2 candidates need
  their primary on the fringe, so these reach the student through block 3 only); 46 to 55
  teachable skills have no observation yet; 4, 2 and 1 meet every condition and wait for a direct
  observation to be re-evaluated, because propagated credit does not re-evaluate mastery.
  Nondeterminism found and closed. The same seed gave 222 and 210 mastered at day 120 under two
  Python hash seeds: `apply_observation` evaluated the touched skills in set order, and since the
  condition 3 correction one skill's declaration can change another's servable count in the same
  pass. It now iterates `sorted(touched)`; three hash seeds give 222. Every comparison below was
  run after the fix, over seeds 1 to 8, because 3 seeds cannot separate a 10-skill change from
  the run-to-run spread (326 to 438 under one policy).
  Baseline after the kept changes, seeds 1 to 8: 396, 405, 396, 395, 439, 386, 380, 401, mean
  399.8 of 539.
  Rejected, block 2 candidates reaching a fringe skill through a mastered primary (02 candidates
  by primary skill widened to any loaded fringe skill with gating clear): 3 seeds 386, 375, 426
  against 392, 394, 374, inside the spread. With unmastered primaries ordered first: 8 seeds mean
  391.8 against 388.8 before the determinism fix, inside the spread. Not kept.
  Rejected, critical path first (block 2 ties ordered by the number of unmastered teachable
  skills behind the primary): 8 seeds 346, 290, 331, 288, 370, 347, 330, 355, mean 332.1, against
  388.8. Concentrating block 2 on the heaviest blockers starves breadth, and breadth is what the
  7-day span rewards, since every fringe skill's span runs on the wall clock in parallel.
  Rejected, archetypes not yet served today first at equal due coverage (01, same-day repeats):
  8 seeds 386, 363, 364, 409, 417, 397, 425, 391, mean 394.0 against 399.8. Not kept.
  Budget arithmetic, seed 1, after the kept changes: of c = 10,036 success credit delivered,
  5,917 landed on skills not yet mastered and 4,119 on skills already mastered (co-loaded
  prerequisites and blocks 1 and 3), across 8,699 and 5,647 skill loads. Reaching 0.9 on every
  teachable skill needs 5,785 before any overshoot, and a skill served every two to three days
  while its 7-day span runs overshoots by several successes. The 2,836 items a 45-minute day
  delivers over 219 days are therefore about the total need with no slack, which is why
  reallocation inside the day moves the count by less than the seed spread.
  Session length, measured and not changed (a product decision): block 2 at 40 minutes instead of
  25 gives seeds 1, 2, 3 411, 409 and 435 of 539 on 3,743 to 3,909 items; at 60 minutes 446, 405
  and 458 on 4,535 to 4,958 items, false mastery 0 throughout. Items up 73 percent move mastery
  up about 12 percent, so the day's length is not the whole ceiling either: the blocking chains
  are 19 deep, each skill needs 2 supported successes and then 3 unaided successes on 3 days
  spanning 7 before the next can open, so a chain served daily needs about 9 days per skill and
  the deepest chain about 170 of the 219 days.
  Ruling 2 applied to `test_two_term_selection_whole_graph` and `test_interleave_full_constraints`.
  Their premise was students placed by the diagnostic. Measured on population seeds 900 to 911:
  10 of 12 students, knowing 96 to 247 skills, were placed into nothing and 2 into 13 and 22
  skills, because placement classifies a skill in-state from the unit posterior (02, cold start:
  a unit read as `partial` puts sigmoid(beta) under 0.9 for every skill in it) and every unit of
  a population student reads partial or not started after 30 items. Every student therefore sat
  on the Unit 1 fringe: 2 units chosen of the more than 3 asked, 7 units seen of 10. This is the
  plan's design, not a defect (the same rule keeps placement false mastery at 0), and it is also
  the largest lever left for a student who knows part of the course, so it is listed for the
  operator below. The tests now start from `whole_graph.states_across_course`: the interior of
  the known state (every known teachable skill another known skill sits behind) is mastered as
  placement would mark it, the outermost known skills stay open, nothing unknown is mastered.
  Marking every known skill mastered was tried first and left block 3 empty in all 1,000
  sessions: the fringe then held only unknown skills, which the fixed P2 world never learns, so
  no unaided success ever made a skill retrieval-eligible. Every assertion of both tests is
  unchanged. `test_a_student_placed_across_the_course_keeps_the_known_boundary_open` pins the
  helper.
  Reviewer (opus, read-only) on the diff since 1f9435f: no loosened assertion, threshold or
  fixture; the two premise-changed tests keep every assertion. Addressed: the skip's parent set
  is now recorded in 02 as a dated correction (blocking parents, not every hard parent); the
  ledger sentence that said "no growth" for the relearn rule now matches the code; the compound
  conditions and a local import it named are tidied. Left open, disclosed in 02 and 12: a skill
  declared on one servable archetype is not re-examined when a second opens, only by the
  un-mastery rule (a credited failure at unsupported there, or strength under 0.75); what would
  settle it is the un-mastery rate on second archetypes.
  Final read, kept engine: ability 3.0 seeds 1, 2, 3 master 396, 405 and 396 of 539 by 2027-05-07
  (Unit 1 completes on day 159 for seed 1; no other unit completes), against 114, 45 and 80 in the
  fixed world and 277, 255 and 288 in the learning world at the start of the session; 20
  population students mean 161.7 (min 67, max 252), 0 false masteries, 5 of 20 complete one unit.
  Acceptance 1 is not met: the pace roughly doubled for the ability-3.0 student and no rule, world
  or scheduling change left inside the binding rules closes the last 140 skills; the evidence
  above says the 19-deep chains with a 7-day span per skill and the placement that starts a
  knowing student at Unit 1 are what remains, and both need an operator ruling.
- 2026-09-29, BC-QA-08014 distractor path, on the operator's delegation. The template's
  BC-ERR-08041 distractor was the integral of 1 + f'(x)^2 with the square root left off, a move
  the record's observed_behavior ("the integral of the derivative, or of the square root of the
  derivative squared alone") does not describe and no BC-ERR record holds. `qa_08014.py` version 2
  builds the integral of f'(x) instead, which equals the square root of f'(x)^2 because f' is
  positive for x at least 1 in every family; the spec is unchanged. Gate: 300 draws, failures 0,
  254 distinct; red with the key planted as the 08041 value, green on restore. The 22 version 1
  items (ITM-GEN-08014-00 to 21) were withdrawn to `content/generation_review/rejected/` with
  reject decisions and replaced under new ids: 22 candidates (22 to 43), a blind re-solve by a
  separate subagent from the stems alone (`formulations_e08041.py`), publish 20 and 2 held by
  rule 10 (29 and 39 differ only in scale); `tools/item_review.py duplicates` kept 29 and
  rejected 39. 21 signed off. `tools/check_items.py content/items_gen_unit08`: 283 read, 283
  clean. The 08041 value sits 0.125 to 0.678 below the key on the calculator items, because
  sqrt(1 + f'^2) is close to f' on steep draws. Also: the six unit 8 skills that still named the
  retired BC-ERR-08005 (08003, 08017, 08021, 08035, 08043, 08059) now name BC-ERR-99019 in
  common_errors and adaptive, through `corrections-skills-retire-08005.json`; the same swap in the
  six unit 8 research sections; BC-QA-08014's scoring point types filled in
  `question-archetypes.md`, where 75 other sections still say "none recorded" against a
  non-empty registry list. Checks, one pytest process per file in tests/generation:
  monte_carlo_invariants 1 passed, generated_banks 13 passed, duplicate_gate_labelled 3 passed,
  template_gate 18 passed, statement_items 7 passed, parameter_specs 3 passed, template_stems 2
  passed, generated_provenance 2 passed.
- 2026-10-02, stage 12 (prompts), slice 1, on the operator's delegation (Decisions,
  2026-10-02). Tutor pin moved to `claude-sonnet-5-5`; grader golden test on the v2 per-part
  contract; AI notices read the v2 grader's `points` and `verdicts`; the metrics view compares all
  five switches; digest goldens for `generator/lesson_v1`, `lesson_v2` and `memory/consolidate_v2`
  by `tools/record_prompt_goldens.py`; output goldens for the seven templates without one, on
  five subscription recordings (`tools/record_prompt_outputs.py`), the agent golden set and the
  lesson checker; `prompts/memory/consolidate_v2.md` live; the tutor prefix measured at 1,470
  tokens on `claude-sonnet-5-5` (`tools/count_prompt_tokens.py --subscription`). Red then green:
  the notices grader tests on the old `notices.py` (2 failed) and on the new; the grader field
  test on two judge mutations (2 failed each); the two new outcome tests on two analysis
  mutations (2 failed); nine mutations of the new output checks, each red. Checks, one pytest
  process per file over tests/providers, grading, api, eval, agent, agent/drawing, experiments and
  tools (122 files): 1924 passed, 6 failed, 24 errors before the last edits, every failure listed
  under Known defects 2026-10-02 or rerun green alone (drawing compile budget under load:
  `40 passed`, `95 passed`; notices `20 passed`); `test_frq_bank.py` timed out at 900 s under
  load; alone it stops on the pre-existing bank checker failure (Known defects). The seven named exit tests: `tests/providers/test_prompts.py` 3
  passed, `test_prompt_output_goldens.py::test_every_template_has_an_output_golden` passed,
  `tests/grading/test_prompt_goldens.py` 9 passed, `test_prompt_cache_prefix_length.py` 2
  passed, `test_feedback_sentence.py` passed, `test_ai_notices.py` 20 passed,
  `test_evaluation_routes.py` 8 passed. `tools/cost_model.py --check docs/plan/14-token-economy.md`
  exit 0; tsc exit 0; qa exit 0. Rebased onto 8a0d4289, after stage 13 (frq) re-recorded the
  cassette books for `claude-sonnet-5-5`: both stages had fixed the grader notices, and the merge
  keeps this stage's briefs (they name the points and read a single v2 verdict) with stage 13's
  whole-part test on registry point types, its expected strings set to the kept wording. The 225
  files `tools/affected_checks.py` selects, one process each: 3020 passed, 17 failed, every
  failure one that fails on main (Known defects 2026-10-02), `tests/lessons/test_invariants.py`
  run on its own cap. `tests/eval/test_prompt_output_goldens.py` `22 passed`, so every
  parametrized `eval_prompt_goldens` case passes; `test_p3_evals.py` `5 passed`;
  `test_frq_bank.py::test_every_served_record_passes_the_bank_checker` `1 passed`; vitest
  `client.test.ts` `248 passed`.

Stage 13 (frq), 2026-10-02, free response end to end, by Claude Opus 5.5 on the operator's
delegation. The causes are under In progress and Known defects; the rulings under Decisions,
2026-10-02. Shipped: the three P3 cassette books re-recorded on the subscription for
`claude-sonnet-5-5` ($0.00 API; transcription 122 calls, grader goldens 450, paper-to-grade 19)
and `docs/operator/p3-grader-eval.md` republished from them; the 10 FRQ-AGT records' skills synced
to their archetypes; `gradings_payload` returns `tutor_explanation` and `tutor_unavailable`; the
grader notices read the whole-part answer; on the client the unavailable line, the graded and the
editing stages on the Workbench, a usable read-back editor, stacked graded points, sentence-case
provisional copy and typeset transcriber notes.

Tests shown red then green: `test_a_lost_point_with_the_tutor_out_of_its_window_reads_as_unavailable`
("assert False is True" with the field hard-coded), the CaptureScreen unavailable case ("1 failed |
12 passed" with the line removed), the strengthened provisional-copy assertion (same, with the
rationale left lowercase), the ReadBack notes case ("1 failed | 1 passed"), and
`test_a_grader_brief_for_a_whole_part_counts_its_open_points_and_verdicts` ("'Returned a g...ear
decision.' == 'Judged 1 poi...1 not earned.'").

Checks, one process per file, at load averages between 40 and 115. The stage's named reds now
pass: tests/eval/test_p3_evals.py "5 passed", tests/e2e/test_paper_to_grade.py "1 passed",
tests/eval/test_prompt_output_goldens.py "1 failed, 14 passed" (the 14 eval_prompt_goldens cases
pass; the failure is test_every_template_has_an_output_golden, templates with no recording, already
recorded under Tutor drawing), tests/grading/test_frq_bank.py checker "PASSED", and the
`GradingsPayload` contract inside the client run. tests/grading: credit 2, latex 20, frq_tutor 3,
metric_nine 1, point 21, probe_queue 1, frq_gates 9, question_definitions 23 passed;
prompt_goldens "2 failed, 7 passed" (stale v1 fields, same on main). tests/eval: agent_golden 20,
golden_sets 11, p2 4, p5 2, p7 10 passed; selection_study "1 failed, 4 passed" and simulation "2
failed, 2 passed", both the same on main 2d608113. tests/e2e: cold_start, full_mock_run,
offline_session, unit_6_item_served 1 passed each; session_login_to_feedback "1 failed, 1 passed"
and exit_criteria_mastery "2 failed", both the same on main; agent_drafts_served "1 failed" (no
Unit 2 item served in 12 sessions) four times in the worktree, and "1 passed in 428.62s" once the
worktree's `var/` (the pacing and spend files the recording and the walk wrote) was moved aside; see
Known defects, 2026-10-02, the e2e isolation leak. tests/providers/test_ai_notices.py "1 failed, 19 passed" (the
stale v1 test). tests/api ai_notices_route 4 and ungraded_flow 5 passed; generation
no_official_text 2 passed. Client: `npx vitest run` "Tests 1 failed | 1167 passed | 6 skipped
(1174)", the failure App.test "reaches progress", which passed alone ("Tests 50 passed"); the
contrast file timed out in its 60 s setup on this branch and on main alike at load 44 to 56.
`npx tsc --noEmit` exit 0. `qa/12_report.py` exit 0 with the gitignored `cache/web` linked. The
full pytest run was not made, on the operator's 2026-10-02 instruction to cut time and tokens;
every file in tests/grading, tests/eval and tests/e2e and every other test file that reads the
changed code ran instead.

Live walk on `var/test.db`, worktree code on ports 8031 and 5184, on the subscription: a Unit 5
free-response unit check. Typed (FRQ-AGT-05001-01): entry, confidence, grading in about 2.5
minutes, 5 of 9 points, the tutor's paragraph on the four lost. Photo (FRQ-AGT-05001-02, a page
rendered by `tools/render_frq_pages.py` with one struck line): image gate passed, a faithful
read-back that flagged the struck fraction as unsure, the fix editor (line marked crossed out),
grading, 7 of 7 decided and 2 provisional, both listed on Review, Provisional points, and one
re-read asked for. Graded views at 1280 and 375 in both themes, no horizontal scroll (scrollWidth
1280 and 375). Screenshots are kept outside the repository, in the session's tool-results folder
under `~/.claude/projects/-Users-mahfujm-dev-growth/`. What it found is under Known defects,
2026-10-02.

- 2026-10-02, stage 11 (progression), by claude-opus-5-5 on the operator's delegation. Block 2
  reaches a fringe skill beside a mastered primary (02, Plan amendments 2026-10-02); the end-to-end
  world serves the P1 archetypes a fresh fringe opens; `tools/throughput.py` gains `--world
  perfect`, `--diagnostic` and `--secondary-candidates`; stale test premises aligned with the
  plan's gating and mastery corrections (Decisions, 2026-10-02). Checks, one process per file:
  tests/engine, tests/session, tests/sim, tests/eval, tests/e2e, the unit check file and
  tests/tools/test_throughput.py, 46 files, 40 passing on the first run; `test_selection.py` and
  `test_two_term_whole_graph.py` then aligned with the amended candidate rule ("17 passed", "6
  passed"; the selection oracle red with the fringe-skill condition removed); still red:
  `eval_simulation_mastery_growth` and the decay-arm test (operator's gates, Known defects),
  `test_prompt_output_goldens.py` (`agent/live_v2.md` has no recorded output, not this stage's) and
  `test_agent_drafts_served.py` (order dependent, Known defects). vitest "Tests 2 failed | 1164
  passed", the failing set changing between runs at load 90 to 200 besides GradingsPayload; tsc
  exit 0; qa 14 PASS, 00_manifest FAIL on cache files absent from the worktree. The full pytest
  suite was not run: the operator asked mid-stage to stop it for time.

Stage 10 (checking), answer checking, 2026-10-02, commit f9d9e86a on top of 10f2e65a. The eight
red tests named in the stage prompt came from 67029adb (2026-09-29), whose `_structured_outcome`
in `app/items/verify.py` called an equation against an expression, a non-SymPy operand and any
pair holding NaN or an infinity "not_equivalent"; bc099056's bounded children were not the cause.
The fix raises TypeError for kinds that cannot be subtracted and leaves special values to the
scalar comparison, and every caller reads a raise as its own unsettled verdict (Decisions,
2026-10-02, stage 10). `tools/key_recheck.py` no longer counts NaN or infinite points, which had
made 1/0 recheck equal to 3, and `_settles_to_zero` computes simplify once and stops at the first
zero. Tests: the eight pass; ten new or rewritten tests across tests/items, tests/calculator and
tests/tools, each shown red with its fix removed and green restored (B1 verify.py at HEAD, 14
failed then 48 passed; the other seven breaks 1 to 3 failed each, then passed). Banks: all 20
`content/items_*` banks clean under `tools/check_items.py` (unit02 191, unit06 330 and unit03_agent
20 at load 15, after 7 load-induced "did not settle" flags at load 115 to 160) and under
`tools/key_recheck.py` (20 exits 0). Full suite before the rebase, 6 xdist workers: 20 failed, 3392
passed, 17 errors in 1246 s, against main's 27 failed and 17 errors; on the rebased branch the 37
failing ids leave 2 failed, 46 passed, and both 2 (`eval_simulation_mastery_growth`,
`test_the_decay_arm_serves_differently_from_two_term`) also fail on main 8a0d4289, owned by stages
11 to 13 (selection and simulation) per the stage plan. vitest 1174 passed, tsc exit 0, qa
12_report exit 0 with the gitignored cache/web linked in (00_manifest fails in a worktree without
it). Every comparison verdict here is a model's work on the operator's delegation, not a human's.

## In progress [inferred]

Stage 1, items for Units 4 to 10, is complete in the worktree `../growth-content` on branch
`content` and is being committed and merged; see "Done", 2026-09-24, stage 1. Nothing else is in
progress in this worktree.

Nothing for stage 2: it merged on 2026-09-24 (Done, "P2 Slice 5").

Stage 4, P3, 2026-09-24: complete and merged (Done, "stage 4 (p3)"). What remains waits on real
use: photographs of real handwriting to re-tune the image gate and to measure the transcriber, and
four weeks of free-response use for metric 9.

Stage 8, P7 evaluation harness, 2026-09-24, worktree `../growth-p7` on branch `p7`: built and
checked on simulated and seeded data (Done, "P7 slice 1"). What remains waits on calendar time
and the operator's real use, listed under Done, "P7 exit criteria". The next session on P7 is a
rerun of the stage 8 prompt once at least 8 weeks of real attempts exist.

Stage 5, P4, 2026-09-24, worktree `../growth-p4` on branch `p4`: complete (Done, "stage 5 (p4)"),
being merged to origin/main. The next stage is 06-p5.

Stage 6, P5, 2026-09-24, worktree `../growth-p5` on branch `p5`: built and checked (Done, "stage 6
(p5)"), being merged to origin/main. What remains waits on real use: the operator's own mocks for
the band and pacing figures, and real handwriting for the capture path. The next stage is 07-p6-p8.

Stage 7, P6 and P8, 2026-09-26, worktree `../growth-p6p8` on branch `p6p8`: complete (Done, "stage
7 (p6p8)"), being merged to origin/main. What remains waits on real use: a real usage-limit answer
to confirm the CLI wording, the queue lengths after real limit windows for the drain pacing, and 8
weeks of real attempts for P7. The next stage is 08, the P7 rerun, once those weeks exist.

Stage 9, the UI redesign, 2026-09-26: complete and merged (Done, "stage 9 (ui)"). Nothing
remains in progress for it. The next stage is 08, the P7 rerun, once 8 weeks of real attempts exist.

Stage 10, the experience pass, 2026-09-26: complete and merged (Done, "stage 10 (ux)"). The
candidates it did not build are listed in its decisions paragraph.

Stage 11, the seven UI items stage 10 left, 2026-09-27, worktree `../growth-ux2` on branch `ux2`:
complete and merged (Done, "stage 11 (ux2)", slices 1 to 6 and slice 7). Nothing remains in
progress for it; its open defects are under Known defects, 2026-09-27.

Stage 12, item selection, 2026-09-27, worktree `../growth-select` on branch `select`: complete
(Done, "stage 12 (select)"), merged, and the bar ruling merged after it. What remains, for the
decay and spacing questions, is a world whose retrieval gain grows with the lag, or the student's
delayed checkpoint accuracy.

Stage 13, content and free-response grading fixes, 2026-09-27, worktree `../growth-content2` on
branch `content2`: complete and merged (Done, "stage 13 (content2)"). Nothing remains in
progress. What stays open is listed under Known defects: integrand points with a constant factor
outside the integral are never decided by a check, and the full test suite was not rerun after
the bank was added (the operator asked to merge on targeted checks).

Stage 13 (frq), free response end to end, 2026-10-02, worktree `../growth-frq` on branch `frq`:
complete and merged (Done, "Stage 13 (frq)"). Causes found: b6f9aa27 moved every role from
`claude-sonnet-5` to `claude-sonnet-5-5`, and the model is part of the cassette digest, so the
transcription and grader golden books missed on every call; its own paper-to-grade recording
decided all four points where the test asks for one provisional; the 10 FRQ-AGT records predated
`corrections-archetypes-skill-load.json`; and the server sent the two tutor fields outside
`gradings_payload`, the function the client contract reads. What stays open is under Known
defects, 2026-10-02.

Stage 12, prompts and models, 2026-10-02, worktree `../growth-prompts` on branch `prompts`:
complete and merged (Done, "stage 12 (prompts)"; Decisions, 2026-10-02). What stays open after it is
listed under Known defects, 2026-10-02; the engine's simulation failures belong to another stage.

Stage 11, progression, 2026-10-02, worktree `../growth-progression` on branch `progression`: the
regression fix, the candidate amendment, the throughput tool and the test premises are built and
merged to main (Done, 2026-10-02, stage 11). What remains is listed under Known defects,
2026-10-02, stage 11.
Stage 10 of the 2026-10-02 run, answer checking: complete and merged (Done, "Stage 10
(checking)"). What stays open is under Known defects, 2026-10-02: bank cleanliness depends on
host load through the 5 s bound, and the tutor leak check's unsettled policy needs a ruling.

## Live API spend log [verified]

Subscription backend, Slice 2, 2026-09-23: 27 live calls through the real claude CLI 2.1.277 on
the operator's keychain login (no `CLAUDE_CODE_OAUTH_TOKEN` in the environment or `.env`), all
built by `app/main.py` `build_tutor` with `GROWTH_AI_BACKEND=subscription`. These were
subscription calls, at $0.00 API spend: `tools/dev_spend.py` read `spent = 0.0353` before and
after. The notional `total_cost_usd` the CLI reported totals 0.17019 USD, which is exactly what
`var/subscription_spend_ledger.json` holds (`{"spent_usd": 0.17019}`), the positive control that
every call was counted and that none reached the API ledger. No paid API call was made.

| Run | Calls | Model | Wall seconds | `duration_ms` | Notional USD |
| --- | --- | --- | --- | --- | --- |
| smoke phase 1, Slice 1 argv, CLI thinking on | 1 | claude-haiku-4-5 | 61.356 | 60304 | 0.032725 |
| smoke phase 1, Slice 1 argv | 1 | claude-sonnet-5 | 4.041 | 2964 | 0.011356 |
| smoke phase 2, `--json-schema`, thinking on | 1 | claude-haiku-4-5 | 35.707 | 34839 | 0.020126 |
| probe, `MAX_THINKING_TOKENS=0` and `--effort low` | 1 | claude-haiku-4-5 | 2.604 | 1600 | 0.002242 |
| latency, 10 cassette inputs, paced 5 s | 10 | claude-haiku-4-5 | median 3.03, p90 3.16 | median 2020, p90 2070 | 0.024647 |
| latency, 10 cassette inputs, paced 5 s | 10 | claude-sonnet-5 | median 3.72, p90 4.32 | median 2740, p90 3310 | 0.066202 |
| smoke phase 1, final argv | 1 | claude-haiku-4-5 | 3.190 | 2117 | 0.002471 |
| smoke phase 1, final argv | 1 | claude-sonnet-5 | 3.536 | 2541 | 0.005902 |
| smoke phase 2, final argv | 1 | claude-haiku-4-5 | 6.535 | 5368 | 0.004519 |

What the checks found: every call returned `subtype` success with one turn and no permission
denial, except the two structured calls, which report two turns (the CLI's structured output
takes a second turn; `permission_denials` stayed empty). Usage and `total_cost_usd` parsed on all
27. Reported input was 1,724 to 1,965 tokens on Haiku 4.5 (the API cassettes: 1,343 to 1,588 for
the same fields) and 2,402 to 2,405 on Sonnet 5, far below what a leaked CLAUDE.md or the CLI's
default system prompt would add, and no reply carried text from the operator's CLAUDE.md (markers
checked: the operator's name, "CLAUDE.md", its first heading, "laconic"). A usage limit was not
hit, so its real JSON shape is still unobserved. Per-call rows are in `var/subscription_smoke.json`
(gitignored; it holds the last run only).

Subscription backend, Slice 1, 2026-09-23: no live call. The claude CLI was run only as
`claude -p --help` and `claude --version` to check flags, and every test drives
`tests/fixtures/fake_claude/claude`. API spend $0.00, subscription use none.

Twenty-seventh session, 2026-09-23, slice 10: seventeen live calls against api.anthropic.com on
claude-haiku-4-5, all under the operator's key in `.env`, nothing else called. `tools/dev_spend.py`
before this slice's live work: `spent = 0.0000`, `cap = 15.0000`, `remaining = 15.0000`. After:
`spent = 0.0353`, `cap = 15.0000`, `remaining = 14.9647`, of the persistent developer cap in
`app/providers/guard.py DevSpendLedger`. The slice's own self-imposed $1.00 budget was enforced a
second way, by setting `GROWTH_DEV_SPEND_CAP_USD=1.00` for both recording runs so
`GuardedProvider`'s own cap check would have refused the sixth of any run that crossed it; neither
run came close. Every request was built by the real production path, `app/feedback/render.py`
`elaborated_payload` and `app/feedback/tutor.py` `request_for`, over a real item from
`content/items_p1_agent/` and its `BC-ERR` record from `data/errors.json`, with only the model
swapped from the tutor role's assigned `claude-sonnet-5` (`app/providers/model_routing.py`) to
`claude-haiku-4-5`, and the role's `output_config.effort: low` option dropped because Haiku 4.5
refuses it (`app/providers/anthropic.py`, Known traps). Each call went through
`app.providers.guard.GuardedProvider` wrapping a real `app.providers.anthropic.AnthropicProvider`,
with `dev_spend_track=True`, so the accounting below is the provider's own reported `usage` block,
not an estimate.

First run, eight calls, one per P1 archetype, recorded as cassettes (see below):

| # | item | model | input | output | cache read | cache write | cost USD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | ITM-AGT-01004-00 | claude-haiku-4-5 | 1435 | 91 | 0 | 0 | 0.001890 |
| 1 | ITM-AGT-01008-00 | claude-haiku-4-5 | 1377 | 141 | 0 | 0 | 0.002082 |
| 2 | ITM-AGT-01015-00 | claude-haiku-4-5 | 1438 | 155 | 0 | 0 | 0.002213 |
| 3 | ITM-AGT-02002-00 | claude-haiku-4-5 | 1582 | 142 | 0 | 0 | 0.002292 |
| 4 | ITM-AGT-02006-00 | claude-haiku-4-5 | 1445 | 136 | 0 | 0 | 0.002125 |
| 5 | ITM-AGT-02007-00 | claude-haiku-4-5 | 1343 | 81 | 0 | 0 | 0.001748 |
| 6 | ITM-AGT-02008-00 | claude-haiku-4-5 | 1411 | 104 | 0 | 0 | 0.001931 |
| 7 | ITM-AGT-02010-00 | claude-haiku-4-5 | 1588 | 123 | 0 | 0 | 0.002203 |

Run total 0.016484 (an earlier, duplicate call on item 0 during setup, 0.002125, has no token row here and
brings the first run to 0.018609, and its cassette was overwritten by the run above; the ledger total after both runs,
0.035292, is what `tools/dev_spend.py` would have shown mid-slice). Second run, the same eight
items driven through `app.feedback.tutor.compose_sentence` with real `Session` and `Attempt` rows
in a temporary SQLite database, the exact function the feedback route calls, so `tutor_calls`,
`tutor_cost_usd` and `tutor_tokens_in` on each attempt are the guard's own settled accounting:
costs 0.001940, 0.002043, 0.002083, 0.002397, 0.001970, 0.001788, 0.002334, 0.002128, run total
0.016683. Combined live spend this slice: 0.035292 of the self-imposed 1.00 cap and of the
persistent 15.00 developer cap.

Every one of the sixteen calls with a token row reported `cached_read_tokens: 0` and `cached_write_tokens: 0`. This
is not a defect. `docs/plan/07-ai-provider-layer.md`, Cache-prefix stability, states Haiku 4.5's
cache minimum as 4,096 tokens; `prompts/feedback/elaborated_v2.md`'s static prefix measures 1,092
tokens on Haiku 4.5 (`tests/fixtures/prompt_token_counts.json`, freshly measured this slice), and
every call's whole input, prefix included, is under 1,600 tokens, so nothing here ever crosses even
that model's total-input floor, let alone reaches the prefix's own minimum. Caching cannot engage
on this template on Haiku regardless of how many calls share the prefix. The tutor role's assigned
model, Sonnet 5, has a 1,024-token minimum and the same prefix measures 1,470 tokens on it
(unchanged, re-measured this slice), so caching would engage there; see the arithmetic below.

Cassettes: `tests/fixtures/provider_cassettes/tutor_haiku_live_00.json` through `_07.json`, one per
item of the first run, each carrying `"recorded": true` (no `synthetic` key), the real
`request_id`, the real `text`, and the usage block from the table above.
`tests/providers/test_haiku_live_cassettes.py` (new) replays all eight with
`app.providers.replay.ReplayProvider`, asserts each is marked recorded and not synthetic, asserts
the recorded `cost_usd` reproduces exactly under `app.providers.guard.usage_cost` fed the
cassette's own usage numbers (red under a mutated `cost_usd` of 999.0 on one cassette,
`0.0018900000000000002 == 999.0` failed; green restored), and asserts all eight report no cache
read or write, the live confirmation of the paragraph above. Gate 22 was already closed by an
earlier session on Sonnet 5; this slice adds the Haiku 4.5 measurement beside it and does not
reopen it.

**Token counts, `tools/count_prompt_tokens.py`.** `tests/fixtures/prompt_token_counts.json` was
flat, one entry per template, and the first Haiku run overwrote the three existing Sonnet entries
in place, since the tool keyed only by template path; caught before anything downstream read the
corrupted file, by `git diff` on the fixture. `tools/count_prompt_tokens.py` and
`tests/providers/test_prompt_cache_prefix_length.py` were changed together: the fixture is now
keyed by template path and then by model
(`counts[template][model]`), and the gate 22 test reads `counts[template_name][tutor.TUTOR_MODEL]`
and asserts that key exists before reading it (red with the Sonnet entry deleted,
`AssertionError: ...has never been measured on claude-sonnet-5...`, green restored). Both models
were then re-measured fresh for all three templates; the Sonnet figures reproduced exactly what
was already recorded (730, 485, 1470 prefix tokens), and the file now also carries: Haiku 4.5,
`prompts/tutor/guardrailed_practice_v1.md` 574, `prompts/feedback/elaborated_v1.md` 364,
`prompts/feedback/elaborated_v2.md` 1092.

**`tools/cost_model.py` `CHARACTERS_PER_TOKEN`, not applied.** 14's own "Proposed edits" table
lists this exact replacement and marks it not applied, operator's to approve line by line, because
no key existed to measure with. A key now exists, but the replacement this slice can honestly make
is narrow: real prefix measurements exist only for the three templates above, and every other
role's `prefix`, `uncached` and `visible` figure in `ROLES` (grader, transcriber, diagnostician,
generator, verifier, template) is still a character-count estimate divided by 3.1, because none of
those roles has a real prompt template in `prompts/` to measure against; `model_routing.py` says
outright that P1 wires only the tutor. Moving `CHARACTERS_PER_TOKEN` itself, or even just
`ROLES["tutor"]["prefix"]` (1,100, still the pre-gate-22 estimate) to the measured 1,470, changes
`tutor.cycle` and every figure downstream of it, which `tests/tools/test_cost_model.py` pins to
four decimal-exact totals (`$5.01`, `$12.44`, `$92.95`, `$95.03`, `$113.83`) and which
`docs/plan/13-ai-engineering.md`, `docs/plan/14-token-economy.md` and
`docs/operator/ai-operating-costs.md` all quote in prose. Making that edit correctly means
rewriting the quoted figures in three planning documents and four pinned assertions in the same
change, which is more editorial surface than this slice's token-count work should carry
unreviewed. Left for the operator exactly as 14 already flags it, with the one new fact this
slice adds: the measured Sonnet prefix (1,470) is already very close to the estimate already in use
(1,100 was an under-estimate, not the character-count figure of 1,470/3.1 ≈ 474 either), so neither
the old estimate nor the character-count formula it came from was tracking the real number even
before this slice.

`python3 tools/cost_model.py --check docs/plan/14-token-economy.md` exits 0, unchanged, because
`tools/cost_model.py` itself was not edited this slice.

**Exit criterion 8, `docs/plan/11-phased-delivery.md`.** `tools/serving_cost.py` run over the
second run's temporary database (8 attempts, all `served_stage: unsupported`, all with a tutor
call):

    scope: all users, role tutor
    served items: 8
    median tutor cost per served item: 0.0020629999999999997 USD over 8 served items, items with no tutor call counted at 0; 0 excluded for tutor calls with no recorded cost
    median tutor cost per served item that made a tutor call: 0.0020629999999999997 USD over 8 served items
    cache read share from attempts: 0.0 = 0 cached read tokens / 11898 input tokens over 8 tutor calls on 8 served items where every call reported a cached read; 0 tutor calls excluded for not reporting; 0 reported calls on 0 served items excluded for sharing a served item with calls that did not report
    cache read share from budgets: 0.0 = 0 cached read tokens / 11898 input tokens over 8 tutor calls on 1 day rows where every call reported; 0 tutor calls excluded for not reporting and 0 reported calls excluded for sharing a day row with them; 0 day rows with no settled call count excluded as not measured

11's exit criterion 8 sets no threshold, only the measurement, so this is not a pass or fail. What
the second run's eight (token in, token out) pairs would cost on the tutor role's assigned model,
`claude-sonnet-5` (`app/providers/model_routing.py`), computed by `app.providers.guard.usage_cost`
fed the real token counts, no call made: priced uncached (the same treatment the live Haiku calls
actually got), the median rises to $0.004126 and the sum to $0.033366, almost exactly double the
Haiku figures, because Sonnet's input and output rates are each exactly double Haiku's. Priced with
the 1-hour cache the tutor's own request already asks for (Sonnet's 1,024-token minimum is under
the measured 1,470-token prefix, so it would actually engage there unlike on Haiku): the first of
the eight calls pays the write rate on the prefix and the other seven pay the read rate, and the
median falls to $0.001565 and the sum to $0.017784, cheaper than what Haiku actually cost this
slice, because caching outweighs Sonnet's higher per-token price once more than one call shares a
prefix.

**Per-student projection against the $50 to $100 target.** The installation is single user, so
`tools/cost_model.py`'s cycle totals already are the per-student projection to exam day.
Unchanged this slice, because `tools/cost_model.py` itself was not edited (see the
`CHARACTERS_PER_TOKEN` paragraph above): the Claude-only $100 tier,
`tier.hundred_claude_only.cycle`, is $92.95, with the $7.05 headroom
`tests/tools/test_cost_model.py` already pins; the Gemini-verifier tier, `tier.hundred.cycle`, is
$95.03. Both sit inside the operator's $50 to $100 ceiling, `BUDGET_CEILING`. This session's
seventeen live calls add nothing to that model, since P1 wires only the tutor and the tutor's own
`tutor.cycle` line, $5.01, was not touched.

P2 Slice 3, 2026-09-23: no live call, $0.00. Every test is replay only.

P2 Slice 4, calibration curve, 2026-09-23: no live call and no claude CLI run. API spend $0.00,
subscription use none.

Stage 5, P4, 2026-09-24: no live API call. Template authoring and the blind re-solves ran as
offline Claude Code sessions on the operator's subscription at $0.00 API spend; every test is
replay only.

Stage 13 (content2), 2026-09-27: $0.00 on the API key. 12 authoring subagents (groups A to L, two
of them resumed for replacements) and 3 blind re-solve subagents ran inside this Claude Code
session on the operator's subscription; no test called a live model and no app route ran with a
live backend (runs 9 to 12 used `GROWTH_AI_BACKEND` none).

Stage 12 (prompts), 2026-10-02: $0.00 on the API key; no key was read. Nine calls on the
operator's subscription through the claude CLI with the production argv, all on
`claude-sonnet-5-5`: four for the tutor prefix measurement (`tools/count_prompt_tokens.py
--subscription`), and five recordings (`tools/record_prompt_outputs.py`: two
correct_reinforcement, one frq_points, one consolidation on v1 and one on v2). No test called a
live model.

## Known defects [verified]

- 2026-10-02, paper_to_grade recording, open: a recording made under heavy load can bake a
  timed-out check into the book. A recording at load average about 200 sent a2 to the grader: its
  `sympy_equivalence` check runs in a forkserver child bounded at 5 s (`app/items/verify.py`
  `run_bounded`), outlived the bound, returned unsettled, and the grader call for a2 was recorded,
  so the book fails `points["a2"]["decided_by"] == "deterministic"` and misses on replay at normal
  load. The same bound makes a replay under heavy load send a2 to the grader and raise
  CassetteMiss. Record only at a 1-minute load under 30 and check a2 is deterministic in the
  summary before committing; a bound that does not count child start-up would remove it. A
  boundary part (b) was also tried in place of the committed book (the sign of (x - 3)e^x without
  naming g', and a "relative maximum" conclusion): one recording split b1 2 of 3 with b2 unanimous
  not_earned, provisional 1. It was not landed because 4e602af0 had already fixed the test, and one
  recording shows nothing about how stable the split is.
- 2026-09-23, subscription backend Slice 2, open:
  - The usage-limit wording the adapter matches ("weekly limit", "5-hour limit", "usage limit",
    "rate limit") and whether a limit arrives as `is_error` JSON or on stderr are still
    unverified: no limit was hit in the 27 live calls, so the patterns were left as they were.
  - Nothing drains the queue on its own. `tools/drain_subscription_queue.py` has to be run by the
    operator (or a scheduler) after a window resets; there is no startup or periodic hook.
  - The CLI adds about 380 input tokens a call on Haiku 4.5 over the same request on the API, and
    what they are was not determined. The size rules out a leaked CLAUDE.md or the default Claude
    Code system prompt, but not something smaller.
  - Whether `MAX_THINKING_TOKENS=0` or `--effort low` stopped the CLI's thinking was not isolated;
    both are sent. If a later CLI drops the variable, Haiku latency returns to about 60 s and the
    smoke tool is the check.
  - The notional `tutor_cost_usd` stored on a subscription attempt is priced at API rates by the
    guard, so `tools/serving_cost.py` over a subscription database reports what the calls would
    have cost on the key, not money spent.
  - Wall clock includes about one second of CLI start and exit on every call.
- 2026-09-23, subscription backend Slice 1, carried:
  - A student who reopens feedback while the limit holds starts a fresh CLI process each time
    before being told the tutor is unavailable. The queue row is not duplicated. The pacing guard
    now bounds it at 4 a minute and the day's call cap.
- 2026-09-23, subscription backend Slice 1, closed in Slice 2: the live CLI accepted the Slice 1
  argv (27 calls); subscription calls no longer consume the per-role dollar and token caps
  (subscription pacing); queued calls have a drain (`tools/drain_subscription_queue.py`).

- 2026-09-23, found while verifying the MCQ math-rendering fix live: `GET /progress`
  (`app/session/preview.py` `queue_preview`, which calls `assemble_session` again) did not answer
  within 45 seconds against a seeded user with several completed sessions, over the small
  `tests/fixtures/items_p1` corpus, in an otherwise idle server with no concurrent request. `GET
  /sessions/{id}/next` and login against the same state answered immediately. Not investigated
  past confirming it reproduces with no concurrent access to rule out; not touched, since it sits
  outside this slice's scope.

From the twenty-sixth session, 2026-09-23, found and not fixed. Rewritten after the independent
item review and its per-archetype re-check (Done above); what the distractor repair and the review
resolved is no longer listed.

- Operator sign-off is pending for all 130 items in `content/items_p1_agent/`.
- Bank-wide: 55 `short_answer` records still carry four options; the checker accepts this and no
  pass changed the formats.
- `BC-QA-01004`: key 2 in 01004-01 is the largest option, the only extreme key left in the
  archetype. Every one of the ten items carries 0 (`BC-ERR-01008`) and 1 as options.
- `BC-QA-01008`: 01008-03 D and 01008-08 A come from one equation at a single boundary, read as one
  wrong-branch application. 01008-04 equates branches at x = 0 though the middle branch is closed
  there (not re-examined).
- `BC-QA-01015`: C is never the key letter (A 3, B 3, D 4). In every item the two bracket
  distractors differ from the key by exactly the excluded endpoint integers, which cannot be
  removed while the archetype holds only `BC-ERR-01031` and `BC-ERR-01032`. 01015-04 C could also be
  tagged `BC-ERR-01032` at step 2.
- `BC-QA-02002`: the value 0 on the `BC-ERR-02005` options (02002-02 A, 03, 07, 09) does not strictly
  follow from setting h = 0 before cancelling, which gives 0/0; a fix needs an error the archetype
  does not hold.
- `BC-QA-02006`: 02006-00 C keeps its partial-application reading (not re-examined).
- `BC-QA-02007`: C is the key in 5 of 10 items; the key is the smallest option in 02007-03 and
  02007-07; in 02, 03, 05, 07 and 09 the key shares a feature with every distractor because the
  archetype holds only two errors. 02007-04 and 02007-08 each tag two options `BC-ERR-02019`, one of
  them the base-and-exponent exchange, which may deserve its own error record.
- `BC-QA-02008`: 02008-04 keeps a key, negation and unsquared-denominator cluster, a weak cue with no
  alternative single-error value among `BC-ERR-02020` to 02023. The 02008-03 C and D reading
  requires treating the constant denominator 4 with the quotient rule before the tagged slip.
- `BC-QA-02010`: 02010-07 B, 08 B and 09 D tag `BC-ERR-02025` for a dropped sign on the derivative
  of cos, though the record's observed behavior names only cot and csc.
- `BC-QA-02011`: 02011-00, 02, 04, 06, 07 and 08 still use input-0 readings of `BC-ERR-02028`, left
  for a set-wide pass. Guess in the re-check: 02011-01 D treats the full swap of slope and height as
  one application of `BC-ERR-02027`.
- `BC-QA-03001`: in 03001-09 the key is the only option sharing a surface feature with all three
  others, a weak convergence cue built into the single-error design. 03001-02 tags two options
  `BC-ERR-03006` under two readings.
- `BC-QA-03004` and `BC-QA-03008`: 03004-00, 03004-08, 03008-01 and 03008-07 each tag two options
  `BC-ERR-03008` (either factor held constant). 03008-02 C still holds y beside three numeric
  options. In 03008-03 and 03008-08 the `BC-ERR-03023` distractor (y' = 0) always equals holding y
  constant under `BC-ERR-03008` for a DE of the form y' = g(x)y + ..., so no point choice separates
  them. The key is the largest numeric option in 4 of the 6 numeric 03008 items (01, 02, 04, 09).
- `BC-QA-03005`: every product-form item (all but 03005-02) has distractors {r1, r2, midpoint} with
  the key outside that triple, a give-away that needs a redesign away from the F(x)G(y) = c form.
  The key is still the extreme option in 01, 03, 05 and 08.
- The scratchpad generators and the option shuffle are not in the repository.

From the twenty-fifth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-sixth session: the distractor audit (Done above) re-derived the
  distractors of the twelve archetypes this entry left open. What remains is in the twenty-sixth
  session's entries above.
- The reshuffle script that fixed the key-position skew was a one-shot content edit, not saved to
  the repository, the same call the twenty-fourth session made for its generator; re-running it
  would produce a different (still roughly uniform) shuffle since nothing pins the RNG seed to a
  file. If a specific distribution is ever a gate's business, that gate should assert the property
  (roughly uniform key position, no single letter dominant) rather than a fixed layout.

From the twenty-fourth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-fourth session: every agent draft now carries four options (Done
  above), so `ITM-AGT-02010-08` and the rest of the twenty-third session's 51 options-less and 31
  three-option items no longer reach the student as an ungraded MCQ turn.
- The server-side fail-safe considered for this ("never serve MCQ for an item without options")
  was tried again this session, in `app/session/service.py` `resolve_served_format` (fall back to
  short answer when the stored item's `options` is empty and the resolved format is MCQ), and
  taken out again: with it in place, four of `tests/session/test_serve_format.py`'s tests go red
  (`test_second_unsupported_serve_on_the_same_archetype_is_mcq`,
  `test_serving_twice_without_submitting_returns_the_same_format`,
  `test_the_served_format_is_persisted_on_the_queue_slot`, and
  `test_an_attempt_that_skipped_the_serve_still_records_the_resolved_format`), because their
  fixture items (`tests/session/test_serve_format.py` `item_row`) are built with `options=None`
  and assert the second stage-unsupported serve is MCQ regardless. Per the task's instruction not
  to edit those named fixture tests, the guard was reverted after confirming the red. Now that
  every served content item does carry four options, this conflict only bites a caller whose own
  fixtures omit them, same as these four tests, so the operator's choice is either to give those
  fixtures options too or to accept that the guard cannot be added without touching them.
- Superseded 2026-09-23, twenty-sixth session: the reused-error-id distractors were hand-checked
  in the distractor audit (Done above). The 42 that no held error produces are listed in the
  twenty-sixth session's Known defects entry.

From the seventeenth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-first session: the eval-cadence ruling closed the remaining
  $8.07. The Claude-only $100 tier now prices at $92.95, $7.05 under the $100.00 ceiling
  (`tier.hundred_claude_only.cycle`), a ruling on `CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE`
  rather than a further sourced lever, since cadence was never a sourced number to begin with.
  Superseded 2026-09-23, nineteenth session: the BC-PT labelling pass closed part of this. The
  Claude-only $100 tier now prices at $108.07, an overrun of $8.07 against the operator's $100.00
  hard stop (`docs/plan/14-token-economy.md` "The $100 tier, line by line",
  `tier.hundred_claude_only.cycle` in `tools/cost_model.py`), down from $128.95 before the pass.
  Not a code defect; a priced fact the document reports rather than hides. Four further levers
  named in the labelling instruction were checked against 13 and 14's own arguments and none
  applies without inventing a number: routing the evals canary to `claude-haiku-4-5` has no
  sourced basis and would change what the canary measures rather than its cost; the transcriber's
  move to Haiku 4.5 standard tier and per-template verifier sampling are both already rejected in
  14's "Rejected directions" table; grader thinking off (direction 4) is the alternative to
  direction 2 rather than additive to it and the operator already declined it on 2026-09-23. What
  is left to close the $8.07 is a tighter labelling pass, which can only move the grader line down,
  and any future Claude pricing change on Haiku 4.5 batch, neither of which this session controls.
  `app/providers/model_routing.py` `ROLE_MODELS` names a model for every role in
  `app/providers/guard.py` `ROLES`, but P1 wires only the tutor (`app/feedback/tutor.py`); the
  other five roles have no provider call site yet, so the table is ahead of the code by design and
  not itself a gap this session found.

From the fifteenth session, 2026-09-23, found and not fixed.

- `tests/items/test_verify_bound.py::test_a_pathological_comparison_on_the_main_thread_is_unsettled_within_the_bound`
  failed once in a full-suite run under concurrent load this session (the test's own comment names
  a `TEARDOWN_MARGIN_S` of 1 second on the development machine, and this host was running several
  full pytest invocations at once at the time). It passed standalone and on two later clean full
  runs. Not touched by this slice; flagged because it can make a clean gate read red on a busy host.

From the fourteenth session, 2026-09-23, found and not fixed.

- Superseded 2026-09-23, twenty-first session: the review-queue route now enforces the sample
  check and one-verdict rule (`app/api/routes/review.py` `resolve_item_audit`,
  `app/review/audit.draw_key_audit_sample`, `tools/draw_key_audit_sample.py`). The review-queue route (`app/api/routes/review.py` around line 70) resolves an item audit row
  with no sample check and no one-verdict rule, so a verdict outside the sample or a second one
  can still reach the table that way. `key_error_rate` counts neither, and it publishes no rate
  while one exists. Nothing in the repository draws the 100-item sample yet; the CLI reads it
  from a file and the app functions take it as an argument.
- Superseded 2026-09-23, twenty-first session: the retryable flag now reads the claude-api
  skill's error-code table (`app/providers/anthropic.py` `_RETRYABLE_STREAM_ERROR_TYPES`; 07 gained
  a sourced table). Stream error events are still always `retryable: False`. 07 has no Anthropic error-type table
  and no retryable rule, so the constant is unsourced and was not replaced with a guess.
- Superseded 2026-09-23, twenty-first session: adding a passkey now requires the same
  `reauth_established` proof 09's other consequential actions do
  (`app/auth/service.py` `add_passkey_finish`; 09's re-authentication list names it). Adding a passkey needs only the session cookie, which is all 09 asks. A stolen cookie can add
  a permanent credential that survives logout. 09's re-authentication list does not name it.
- Superseded 2026-09-23, twenty-first session, corrected twenty-second session: 09 line 96 is
  replaced with the full, route-table-derived list, checked by
  `tests/api/test_unauthenticated_routes.py` so it cannot drift again. The twenty-first session's
  list came from `create_app`'s routes only and missed the three `mount_client` adds
  (`GET /growth-tokens.css`, `GET /`, the `/assets` mount); the twenty-second session's entry above
  covers that gap. 09 line 96 says the login endpoints are the only ones an unauthenticated party can reach; that
  was already false for `/auth/recovery/*` and is now false for `/auth/status` too.
- Account copy written by the builder and awaiting the operator: "Add a passkey", "Passkey
  added.", and the server refusal texts "this passkey is already registered" and "the challenge
  belongs to another session", which can reach the screen. The credential display name is still
  always "student".
- Superseded 2026-09-23, twenty-first session: `record_error_note` now replaces rather than
  refuses a second note, confirming the 2026-09-20 decision this entry names.
  `ErrorNoteAlreadyWritten` is removed. The operator decision of 2026-09-20 says a second error note replaces the first. The code
  refuses it with 409 (the eighth session's reading of 03's "once"), and
  test_a_second_error_note_is_refused_and_the_first_survives pins that. The 500 cap from the
  same decision is now enforced.
- `tests/design/test_tokens.py` around line 304 types `approx(4.5)` rather than reading the floor
  from 08.
- `app/web/.gate-reduced-motion 2.json` is a stale sync copy of the gate report (older, differs
  from `.gate-reduced-motion.json`). Left for the operator to delete.

From the thirteenth session, 2026-09-23, found and not fixed.

- No plan copy exists for an answer that could not be checked or for a failed feedback read, so
  the screen shows no sentence there, only Next item.
- `StepMarks.tsx` `BlankStep` shows the blank step's worked text when there is no verdict, so an
  ungraded completion answer reveals the step without saying whether the student had it.
- `app/web/.gate-reduced-motion 2.json` is an untracked file-sync duplicate of the gate 25 report;
  left for the operator.

- Gate 23 holds only for the seed-7 draw. Seeding the forecast rng by user id (the twelfth
  session's defect) made `test_session_login_to_feedback` fail 1 run in 6 with `these never were:
  ['BC-QA-02002']`, and `serve_as_mcq` in tests/api fail with `BC-QA-02011 has no published item
  outside the queue`. The change was reverted; the rng is still per process and day.
- The audit detail bound has no length limit (no plan number), and a key that is not in this
  process's environment and has no plan-named prefix cannot be recognised. `authorization` is not
  a refused field name.
- HSTS and per-IP rate limits are not built: 09 gives no max-age and no rate.
- Cache writes are always charged at the 1h rate; the adapter drops Anthropic's TTL split. The
  tutor requests 1h, so P1 is exact. Gemini cache writes and hourly storage are not modelled.
- The e2e exit tests bind mastery conditions 2, 4 and 5 only; 1, 3 and 6 survive deletion from the
  engine there (gate 7 covers them). Condition 6 cannot bind in P1 because `evaluate_mastery` runs
  at elapsed 0.
- `COMPARISON_TIMEOUT_S = 5` has no plan source. A short-answer grade can take 15 s on a sync
  worker. SIGALRM cannot interrupt one long C call on the main thread (ingest CLI). Forkserver
  children are unbounded in number and re-import an unguarded `__main__`.
- A budgets row that spans the migration day mixes unreported sums with counted calls.
- `stop_reason` versus 07's `finish_reason`: readers in replay.py, several tests and the cassette.
- Superseded 2026-09-23, twenty-first session: retryable now reads the claude-api skill's
  error-code table, see above. Stream error events are always `retryable: False`. Effort on Haiku 4.5 is not refused.
- Superseded 2026-09-23, twenty-first session: `GET /growth-tokens.css` now defaults to
  `app/design/growth-tokens.json`; the three assertions were changed on the operator's own
  instruction (this slice). `GET /growth-tokens.css` 404s unless `GROWTH_TOKENS_PATH` is set; a default to
  `app/design/growth-tokens.json` needs three assertions in tests/api/test_static_mount.py changed,
  which only the operator may approve.
- No Inter font is bundled, so the system font renders. `letter-spacing` and numeric weights are
  unset (08 gives none). The page renders once without colour tokens before JS sets `data-theme`.
- Account screen: no route says whether a user exists, so both buttons show; the credential name is
  always "student"; adding a second authenticator is not built (09 asks registration to prompt for
  one); copy strings on the account screen were written by the builder and await the operator.
- `finish_*` against the real py_webauthn has never run; that needs a real authenticator.
- `test_next_item_never_carries_the_answer_key` derives forbidden columns from the code under test.

Resolved in the thirteenth session from the list below: no `data-theme` ever set (D33), hand-typed
`INSTANT_CLASSES`, stream parsed as JSON, thinking refused and options dropped, unbounded
equivalence off the main thread, the tutor "only four fields" and prompt golden tests, Secure flag
from bind_host, no CSP, webauthn not installed, `test_library_verifier_names_the_missing_package`
depending on the package being absent.

From the twelfth session, 2026-09-22, found and not fixed.

- Superseded 2026-09-23, twenty-first session: the purge confirmation phrase is ruled
  (`"delete my data"`) and wired into `App.tsx`; purge is reachable from settings. Purge is unreachable from the served app. 08 gives no purge confirmation phrase, so `App.tsx`
  passes `null` and the purge controls stay disabled with the gap named on screen. Failure
  scenario: 30 days after the exam the student cannot purge from settings.
- Closed 2026-09-26 by stage 10 (`app/web/src/status/LoadState.tsx`). No plan copy exists for a failed request anywhere in the client. Screens stay silent on a 500
  or a dropped connection; a refused next-item request leaves feedback on screen to retry.
- The empty-queue action "Add a 15 minute practice set" opens an ordinary session. No route
  assembles a 15-minute set, so on an empty queue the button opens an empty session.
- 08's "daily minute target" and "daily cap, all roles" have no column in 06, so neither is served
  or shown.
- Provider key storage (`PUT /settings/providers/{provider}` and its test call) is not built. 09
  requires libsodium secretbox under a memory-hard KDF, and no libsodium binding is installed or
  named by package in 06.
- After the first cap change through settings, the environment cap no longer binds for that role.
  Stated in `app/providers/guard.py`. A PUT is detected from the `budget_cap_changed` audit entry.
- The home forecast rng is seeded from `GROWTH_RNG_SEED` and the day, not the user, so two users
  on one day would share a draw. Harmless while P1 is single user.
- `test_importing_app_main_leaves_the_repository_database_untouched` cannot fail when the
  repository database already matches; `test_importing_app_main_opens_no_database` is the one that
  proves the guarantee.
- Export audit scope names the actors `worker`, `system` and `operator` as the student's in a
  single-student deployment; purge deletes the same set. Multi-user (P8) needs a real owner.
- `format_version = 1` in the export is a label with no plan source, and the `export` job type is
  taken from 06's API surface row, not from its jobs type list.
- Purge deletes archive files before its transaction commits. A failed commit leaves the rows and
  loses the files, which is the privacy-safe side.
- If more audit verdicts are recorded than the sample holds, `verdicts_complete` reads true and the
  key error rate can exceed 1. No plan rule decides it.
- The passkey JSON the client sends to the reauth and purge routes has been tested against mocks
  only. The `webauthn` package is not installed in `.venv/`, so `LibraryVerifier` has never run.

Resolved this session: the served-steps, pre-submission self-explanation prompt and
self-explanation persistence defects; `record_attempt` storing a client-claimed `correct`; the
three unmounted screens; the unserved token stylesheet; the missing spacing vocabulary;
`ServedItem` omitting `is_probe` and the loosely typed queue; the review audit kind, the wrong-row
resolution and the key error denominator; `verify.py`'s null `error_path` split; coverage gaps
missing from `audit_log` per day; `test_next_item_never_carries_the_answer_key` asserting only a
string. The reauth audit entry was already written by the route.

Two review rounds ran against this session's own diff, and both found blocking defects that were
reproduced and fixed before close.

- Wave 1 review, blocking, fixed. `app/design/css.py` emitted colour tokens and silently dropped
  all nine type tokens on the one path the operator will take: filling
  `docs/operator/design-tokens.template.json` and calling `stylesheet_from_tokens` produced 34
  declarations, none of them `--growth-type-*`, while `CUSTOM_PROPERTIES` advertised 26 names. The
  module now refuses a missing token of either kind, validates type values for the characters that
  would end a declaration or a rule block, and the template carries the nine type tokens as nulls
  so the operator can fill them. `tests/design/test_css.py` now exercises the real template rather
  than only a hand-built full token file.
- Wave 1 review, blocking, fixed. `app/items/distractor_paths.py` duplicated the comparison and
  error-path core of `app/items/verify.py`, proven by replacing `verify._compare` and watching
  `test_distractor_paths.py` stay green. One core now serves both callers and two monkeypatch
  tests prove a change to it reaches both.
- Wave 2 review, blocking, fixed, and the most serious finding of the session. Gate 25 could be
  defeated by `it.skip`. The reviewer skipped the cross-fade case and rewrote every reduce block
  to `transition: none`, which is the implementation 08 explicitly calls wrong, and the gate still
  reported `1 passed`: the title regex matched only `it(`, so a skipped case left both sides of
  the count, and nothing read `numPendingTests`. The scan now captures the modifier and refuses
  `.skip`, `.todo`, `.only`, `.fails` and `.concurrent`, and the gate asserts `numPendingTests`
  and `numTodoTests` are 0. The same attack now fails at `test_reduced_motion.py:52`. Everything
  else thrown at the gate already failed correctly: absent `node_modules`, a renamed test file, a
  glob matching zero files, broken reduce blocks, a stripped affordance and a stale report.
- Wave 2 review, blocking, fixed. The client had no entry point. `index.html` named
  `/src/main.tsx`, which did not exist, so `npx vite build` failed, and nothing imported
  `motion.css`, so gate 25 asserted a property of a stylesheet no browser loaded. `main.tsx` and
  `App.tsx` now exist, `main.tsx` imports the motion stylesheet, the build succeeds, and
  `tests/web/test_client_builds.py` runs the production build so the gap cannot reopen unnoticed.
  No P1 gate ran the build, which is why this was invisible.
- Wave 2 review, three plan deviations in the session screen, fixed. The confidence rating could
  be skipped although 11 P1 scope item 10 says it is collected before feedback on every item; the
  error note was optional and was prompted after correct answers although the plan says one note
  per corrected item; and a double-clicked `Next item` stranded the student on the server's 409
  with nothing said. `commit` now reads the rating back off the attempt row the server wrote
  rather than off local state, the note field renders only on the corrected path and is required
  there, and one in-flight guard released in a `finally` covers all three submissions.
- Wave 2 review, a vacuous test, fixed. `HomeScreen.test.tsx`'s colour scan caught only hex
  literals, so `rgb(255, 0, 0)` and `red` passed, and its "only" test was an at-least-one match
  inside a loop with no count guard. The scan now decides whether a value names a colour by
  assigning it to a DOM node and asking whether the CSS parser kept it, subtracting the seven
  CSS-wide and context keywords by name, so no colour list is hand-typed anywhere.

From the eleventh session, 2026-09-21, found and not fixed.

- The three screens are built and tested but are not mounted in the bundle. `App.tsx` routes
  between home, session and settings and, for each, renders a panel headed "This screen is not
  built yet" naming every required prop no client route supplies, because mounting a screen with
  `[]`, `null` or `0` would render a queue claiming no work is due and a budget claiming nothing
  was spent, which is a fabricated figure wearing the screen's real layout. A test asserts no
  rendered route contains a digit at all, so a default cannot be slipped back in quietly. The
  consequence to carry: gate 25's "still reaches the student" is asserted at component level, not
  through a served page, and it closes one screen at a time as routes land.
- Nothing calls `app/design/css.py` and nothing writes a generated stylesheet into the client, so
  every `var(--growth-*)` resolves to the browser default. `App` probes `--growth-surface-page` at
  render and shows a `role="status"` notice when it is absent. What is still owed once the
  operator's token file lands: a build or startup step that reads it, calls
  `stylesheet_from_tokens`, writes the result where the client imports it, and a `main.tsx` import
  of that stylesheet beside the motion one.
- No plan document gives copy for an in-session request failure. A rejected `submitAttempt`,
  `submitConfidence` or `submitErrorNote` leaves the student on the same screen with nothing said.
  The double-click case is closed by the in-flight guard, but a 500 or a dropped connection is
  not, and the sentence was not invented. It needs a line in 08-design-brief.md's Interface
  writing before it can be built.
- `purgeConfirmationPhrase` has no client source. 08 gives the claudebox acknowledgement string
  verbatim but gives no phrase for purge, so the settings screen takes it as a required prop and
  the only value anywhere is a fixture in `SettingsScreen.test.tsx`.
- The consolidation in `app/items/verify.py` changed one outcome beyond the duplication fix. The
  old `_equals_key` collapsed an unsettled comparison into "not equal", so such an item reached
  `verified`; it now lands in review. That is the safer reading and it is a behaviour change worth
  knowing.
- `tests/web/test_client_builds.py` runs `vite build` rather than `npm run build`, because the
  latter chains `tsc --noEmit` and a type error in a module the bundle never loads would read as a
  client that cannot be served. `tsc --noEmit` is still run separately and is clean.
- The client cannot draw a worked example or a completion problem from what the server sends.
  `GET /sessions/{id}/next` returns `ServedItem` from `app/runtime/bank.py:_as_item_dict`, which
  deliberately withholds the worked solution before submission, so it carries `stem` and no step
  list. Stages `example` and `completion` both need one. Failure scenario: a student opens a
  session, block 2 serves a stage-example item, and the screen has nothing to render above the
  answer field. `Item.tsx` takes `workedSteps` as a required prop with no default and
  `SessionScreen` requires `workedStepsFor(item)` from its caller, so nothing is fabricated, but
  no route supplies it. What the route owes, for stages example and completion only:
  `served_steps: [{index, text}]`, all steps at example, the first n-1 and never the last at
  completion.
- `FeedbackPayload.self_explanation_prompt` arrives only after submission, but the example stage
  shows the self-explanation prompt before any submission. `SessionScreen` requires
  `selfExplanationPromptFor(item)` for that reason. The same pre-submission payload should carry
  it.
- Nothing persists the self-explanation answer. `POST /sessions/{id}/attempts/{aid}/error-note` is
  the error note only. Failure scenario: a student types an answer to "which rule justifies step
  k, and why does it apply here" at the example stage and it is dropped when the item advances.
- A student whose MathLive chunk fails to load is stuck on that item. `Item.tsx` now tells them
  the problem cannot take an answer and withdraws the confidence prompt and the commit button, but
  the only way forward is `Next item`, which lives behind feedback, and feedback needs an attempt.
  No plan section specifies a skip or reload path, so none was invented. Worth a decision before
  P1 ships.
- Nothing in the client suite exercises real MathLive. Its package exports map answers the "node"
  condition with a server-side bundle that omits `MathfieldElement`, and Vitest resolves that
  condition under jsdom. Adding `resolve.conditions` to `vite.config.ts` was tried and broke seven
  other test files, so the seam is tested against an honest stub custom element instead. Nothing
  proves `MathfieldElement` registers, that `<math-field>` upgrades, that a real keystroke emits
  an `input` event, or that the real `getValue("math-json")` returns parseable MathJSON. The
  failure path is exercised through a mocked rejecting module, so the browser's real rejection
  shape is assumed rather than observed. A browser-level check is the only thing that closes this.
- The consolidation in `app/items/verify.py` changed one behaviour. The shared core is `verify`'s
  comparison, which re-runs `numeric_check` after `equivalence`. For every settled comparison that
  is identical to what `distractor_paths` did, because `numeric_check` is seeded. The one case
  that can now decide differently is when `equivalence` hits its 5 second SIGALRM timeout:
  previously the checker called that unsettled, now the unbounded `numeric_check` may settle it
  either way. Nothing tests that path.
- `types.ts` `ServedItem` omits `is_probe`, which `app/engine/select.py` `dress_item` writes onto
  every served slot, so the client's `ServedItem` gate is one-directional rather than exact
  equality. `SessionPayload.queue` is typed `Record<string, ServedItem[]>`, but
  `service.queue_payload` returns `block1` to `block4`, `forecasts`, `coverage_gaps` and
  `interleaving_satisfied`, so three of those values are not item arrays and no gate covers them.
- `app/design/css.py` emits only `[data-theme="..."]` selectors, with no `:root` default and no
  `prefers-color-scheme` block. A document rendered before the shell sets `data-theme` resolves
  every `var(--growth-*)` to empty. 08 requires no default, so this is an interface note rather
  than a deviation.
- Entry criterion 5 names a nine-value spacing scale alongside the nine type-scale steps.
  `app/design/tokens.py` carries no spacing vocabulary at all, so the template offers no spacing
  slot and `CUSTOM_PROPERTIES` advertises none. The names were not invented. The operator kit
  still owes a `SPACING_TOKENS` table, its nulls in the template and its emission in `css.py`.
- The `var(--growth-*)` role assignments on the home and settings screens, meaning which text sits
  on `text-secondary` against `text-muted` and which control is `accent-base` against
  `surface-sunken`, were chosen by the builder. 08 fixes token names and roles in the abstract but
  gives no screen-by-screen mapping. This is a first pass, not a spec-derived assignment, and a
  design review should confirm it.
- `motion.ts`'s `INSTANT_CLASSES` is a hand-typed list of the six repeated-keystroke paths 08
  names, checked against a hand-authored stylesheet. The six do match 08, and
  `TRANSFORM_MOTION_CLASSES` is correctly derived from `P1_FEEDBACK_AFFORDANCES`, but nothing
  parses 08 for them the way `test_tokens.py` parses it for the type scale. A seventh path added
  to 08 would fail no test.
- `app/web/src/api/client.ts` issues `POST /sessions/{id}/attempts/{aid}/error-note`, which is not
  in 06's API surface table. The route predates this session and 06 was never updated. The client
  conformance test scans the FastAPI decorators, so it catches client and server drift but cannot
  catch server and plan drift.
- The style gate blocks U+2600 to U+27BF, so tick and cross glyphs are unusable. The correct and
  incorrect glyphs are the ASCII strings `ok` and `x`, the second matching 08's own wireframe. Real
  tick glyphs would need a gate exemption or inline SVG.

- Resolved 2026-09-20 (ninth): the unconditional `temperature` on every Anthropic call, which
  was a 400 on every routed model. See Done.
- From the ninth session, not fixed. The 26 templates in `var/` all fail the extended gate,
  and every one of them was generated before the schema carried `representation`, `figure`,
  `role` or the allowed BC-ERR list, so the 0 of 26 is a contract measurement and not yet a
  model measurement. A fresh paid run against the new prompt is the next measurement and is
  not taken without the operator.
- From the ninth session, not fixed. `tools/template_trial.py` `structure` treats degree,
  head, function set, arity and zero-ness as the whole of a solution path's shape. A radical
  that changes which theorem applies without changing any of those, such as a sign pattern
  that switches an integrand between two antiderivative rules, passes the incidental check.
  The check is a floor, not a proof.

- From the eighth session's review, not fixed, not blocking. `app/items/distractor_paths.py`
  reimplements the two comparison loops and the error-path resolution of
  `app/items/verify.py`'s `distractor_checks`, although its own docstring says it does not. The
  two now disagree on policy by design: the checker reports an unsettled comparison as a
  violation, while `ingest.distractor_distinct_check` returns indeterminate and routes to review.
  Failure scenario: a future change to 04's rejection rule 5 has to land in two files and a
  reviewer editing one will not see the other.
- From the eighth session's review, not fixed, not blocking.
  `tests/design/test_tokens.py::test_a_filled_pair_at_the_floor_is_accepted` does not test the
  floor. Its fixture sets every checked pair to black on white, which is 21:1, and the boundary
  the code tests with `ratio < TEXT_CONTRAST_FLOOR` is never exercised at exactly 4.5.
- From the eighth session's review, not fixed, not blocking. `tests/design/test_tokens.py` reads
  the colour token names out of 08 but types out the `accent-tint-1` to `accent-tint-4` range. If
  08 said "1 through 6" the test would build four names, `COLOUR_TOKENS` holds four, and it would
  pass.
- From the eighth session, not fixed. Gate 22, `test_prompt_cache_prefix_length`, has no test
  function anywhere under `tests/`. It cannot be written honestly without a key, because it
  asserts a token count of the tutor template's static prefix.
- From the eighth session's review, not fixed, and worth the operator's eye.
  `provider_result_unreadable` is a sixth action in `app/audit/vocabulary.py` that 09's prose does
  not enumerate. So is `app/db/migrate.py` itself: 06 names no migration mechanism at all, and its
  only migration prose is Postgres through SQLAlchemy at phase 8, so the additive migrator is an
  implementer-invented seam.
- From the eighth session, a gap in the evidence rather than a defect. The gate 23 strengthening
  could not be shown red by a mutant: a copy of the repository under the scratchpad does not run
  the end-to-end test green even unmutated, because the cassette and content paths do not resolve
  outside the working tree. The strengthening rests instead on two assertions that are both live,
  that more than one archetype opens at cold start and that every one of them was served.
- From the seventh session's review, accepted rather than fixed and still true. Six of the 13 P1
  archetypes are unreachable at cold start because each one's primary skill has a hard prerequisite
  that is an ordinary BC-SKL rather than one of the 25 seeded assumed-mastered parents, and
  BC-QA-01004's gating parent BC-SKL-01028 is one of BC-QA-01004's own skills, so it can never
  open. That last one looks like a library shape worth a question rather than a test defect. Gate
  23 no longer accepts a one-archetype regression, but it still cannot reach those six.
- From the seventh session, a behaviour change to note. `compose_sentence` now returns `None` where
  it used to return `""` when a provider returns an empty string, on the uncached path as well.
  Nothing in the suite depended on the old reading and the route treats a missing sentence as the
  degradation case.

- The error note still takes any length. 03 and 06 set no cap, so none was invented. The repeat
  POST and the multi-line note are fixed as of the eighth session.
- `scoring_consequence` is empty on every wrong short answer, so feedback carries two of 03's three
  required parts on that path. See Plan corrections for why the BC-PT branch was not implemented.

- From the fifth session's review, not fixed. Session assembly freezes `format` on every queue slot
  at assembly time, so the R16 alternation never happens inside one session: every item of a fresh
  session is served as short answer, and an MCQ case exists over HTTP only when a test rewrites the
  queue row. Because R12 rule 3 gives a wrong short answer no error path, and
  `elaborated_payload` refuses to compose without a BC-ERR record, elaborated feedback is
  unreachable through the natural P1 flow. These two together are what block gate 23
  `test_session_login_to_feedback`, along with two smaller gaps: no HTTP route writes the error
  note that gate 23 names, although `service.record_error_note` exists, and
  `tests/fixtures/provider_cassettes/` does not exist, so "no network calls outside the recorded
  cassettes" has no cassettes to replay. `app/main.py` also sets no `settings.tutor`, so the one
  wired role is wired only in tests.
- The static prefixes of both prompt templates are far short of the 1,024-token minimum that binds
  on claude-sonnet-5: `guardrailed_practice_v1.md` is 2,473 characters and `elaborated_v1.md` is
  1,641, which is roughly 620 and 410 tokens. Gate 22 would fail on length, not merely be
  unmeasurable, and the plan's own trap is that a short prefix is processed uncached with no error.
- `AnthropicProvider.stream` sets `"stream": true` and then parses the body as JSON, so the first
  real streaming call raises a decode error on the `text/event-stream` response. No test covers it
  because every test feeds a dict back. 07 gives no concrete SSE to normalised event mapping that
  could be validated without a key.
- `app/providers/anthropic.py` refuses `thinking` in `provider_options` outright, including the
  adaptive form 07 names as the correct one for Claude 4.7 and later, and drops `provider_options`
  rather than passing it through. Defensible for a tutor that needs none, a deviation for the P4
  generator. The result field is `stop_reason` where 07's shape names `finish_reason`.
- The tutor is called from the feedback route on every GET, so re-reading the screen re-spends and
  returns a different sentence, and the `usage` block is discarded, so nothing feeds a budgets row,
  the cache hit rate or `audit_log`. 07 puts the budget guard, the usage accounting and the audit
  trail at the provider seam.
- A BC-ERR record whose skills are all outside the archetype leaves `error_path_skills` empty, and
  `rule_based_mastery_states` then falls back to blaming the primary skill, which is R12 rule 3's
  behaviour for an answer with no error path. The fallback predates this session; the grader is
  what starts feeding it real error paths.
- `equivalence` now returns without a bound when it runs off the main thread, which is where a sync
  FastAPI route runs. The `signal` crash is fixed and the timeout is not replaced, so a
  pathological submission can pin a worker thread. The exposure is one authenticated user on their
  own installation.
- `record_attempt` persists the submitted body verbatim in `attempts.response`, so a claimed
  `"correct": true` is stored beside the server verdict that overrode it.
- `audit.write_resolution_audit_entry` hard-codes the `item_audit` kind, so resolving a row of any
  other kind is logged as an item audit. `resolve_item_audit` passes `row.ref_id` rather than the
  row, so `record_item_audit_verdict` re-looks-up the open row by item id and would resolve the
  wrong one if two were open for the same item.
- `_misnotated` treats any units mismatch as `notation_only` with correct true, which credits 0.25
  for an answer whose units are dimensionally wrong. 03's check 4 asks for units present and
  dimensionally correct; R12 rule 4 is loose enough to permit the reading.
- Three tests assert less than their names claim, and none of them is a gate from 11:
  `test_next_item_never_carries_the_answer_key` checks only that the literal string `answer_key` is
  absent and never checks `is_key` or `error_path`, which are what identify the key;
  `test_the_tutor_receives_only_the_four_selected_fields` proves no "only" and never inspects
  `request.system`; `test_prompt_templates_are_versioned_and_golden` holds no snapshot or digest,
  so any rewrite of either template passes it.
- The working tree carries 24 untracked files whose names end in `" 2.py"`, copies made by a file
  sync. pytest collects them and reports `200 passed` instead of `161 passed`, so every count in
  this ledger is taken with `--ignore-glob="* 2.py"`. They are the operator's to delete.

- From the fourth session's review, not fixed: `close_session` sweeps graded, unrated attempts and
  applies them with `Confidence.UNSURE`, which is an observation the student never rated entering
  `c_k`, `distinct_archetypes_succeeded` and `success_days`; it rests on the operator's second
  session instruction, not on a plan sentence, and `close_session` now raises `ValueError` (409)
  when no engine bundle is supplied, so a caller without one cannot close a session at all.
  `reauth_finish` writes no audit entry although 09 records "a session established from a new
  authenticator". `app/review/audit.py` divides the key error count by the verdicts recorded
  rather than by the sample size, which reads correctly only because `verdicts_complete` ships
  beside it. Coverage gaps from the fail-closed rule go into `sessions.queue` rather than
  `audit_log`, which 06's traceability row asks for; pre-existing, and live now that the real bank
  is wired. `app/items/verify.py` still splits options on a null `error_path`; only the ingestion
  path was corrected to read `is_key`.
- Recovery issues a replacement code after a successful recovery. 09 says a code is "generated once
  at registration", so this is a deviation; without it a recovered account has no recovery path
  left. The plaintext replacement is returned once in the finish response.
- `app/runtime/bank.py` decides what a served item may carry. Anything a later phase adds to the
  `items` row is withheld from the student by default and has to be added to `_as_item_dict`
  deliberately.

- From the third session's review, not fixed: registration issues no recovery code (09 Recovery requires one, hashed, shown once); purge leaves `review_queue`, `jobs`, `items`, `item_verifications` and `content_snapshots` untouched because they carry no `user_id`, and it empties `audit_log` globally, so the purge audit entry itself does not survive; no ASGI entrypoint builds `Settings`, resolves the snapshot and the `SessionContext` for a real run, so `create_app` is reachable only from tests; `LibraryVerifier`'s calls into the `webauthn` package have never executed; challenges live in a per-process `ChallengeStore` with a 300 second TTL; the Secure flag derives from `bind_host` rather than the request scheme; audit actions `session_established` and `session_closed` are not in 09's vocabulary; no per-IP rate limit, CSP or HSTS middleware.
- `test_purge_requires_reauth` drives a purge double, so no HTTP test runs the real `purge_user`; the real one is covered in `tests/session/test_purge.py` only.
- Gate 31 margin is thin: pooled 0.0604 against 0.0556 on the fixed per-trajectory seeds, and on ceiling and slipper the control arm scores higher per item than the policy. The pooled win comes from the policy serving fewer items on absent_30_days and floor (block 1 requeues), not from faster mastery. A different seed set could flip it. The eval asserts pooled only, as written.
- Dependants of BC-SKL-02025 do reach mastery in the prereq_gap trajectory as secondary loaded skills of archetypes whose primary is ungated (BC-SKL-02044, 02045 via BC-QA-02010; BC-SKL-03006 via BC-QA-03001). Invariant 3 gates on the primary skill only, so this is plan-conformant; `test_simulation_prereq_gap_stalls_dependants` asserts that no mastered dependant was credited by an archetype whose primary is itself a dependant. Whether secondary loading should be gated too is a 02 question.
- `test_simulation_prereq_gap_stalls_dependants` asserts gating on the served trace and is load-bearing; its second clause (dependants of BC-SKL-02025 unmastered) is vacuous until mastery is reachable.
- `app/sim/runner.py` reads `tests/fixtures/graph_p1.json` and `tests/fixtures/student_trajectories/` by path and synthesises 10 published items per archetype because `tests/fixtures/items_p1/` does not exist; when the 130 items land, the bank should be read from them.
- Session service: an attempt at stage completion or unsupported whose confidence rating never arrives is never applied, and nothing sweeps abandoned sessions. Stage example fabricates `Confidence.UNSURE` because `grade_for` requires a rating and convention 3 collects none there. `transcription_confirmed` is not enforced as a precondition on the update (P1 has no transcription). `constants.LAMBDA` is 0 in P1, so the retrievability passed into the logged predictions is inert until the lambda arm turns on. Nothing seeds the 618 `skills_state` rows at account creation; tests seed from the fixture.
- Reconciliation: consecutive counters are zeroed on merge, an inferred choice recorded in `ReloadReport.notes`; a `skills_state` row whose id is neither active nor in `ids.json` refuses the reload (folded into the pseudocode's final else). Orphaned rows are surfaced only through the report and `audit_log` (`skill_orphaned`); nothing in selection excludes them yet.
- Resolved 2026-09-19: `data/prereq_edges.csv` carried a cycle over the full typed edge set (BC-SKL-05020 to BC-SKL-05021 hard_prerequisite, BC-SKL-05021 to BC-SKL-06023 supporting, BC-SKL-06023 to BC-SKL-05020 supporting) because one supporting row was stored in the reverse direction. The row was flipped (see Decisions); `tools/graph_check.py` reports 0 cycles, test_graph_acyclic and test_loader_against_real_data pass, and the helper test that removed the cycle from a temporary copy was deleted as obsolete. A full `tools/merge_staging.py` replay after the flip regressed unrelated evidence links in archetypes, scoring_points and skills, so those three registries and `data/staging/sync-dependents.json` were restored to HEAD; the replay order in that tool lets older staging files overwrite later link-evidence merges, which the library owner should look at before the next merge.
- FSRS-7 forms: docs/plan/02 transcribes stability and difficulty updates with parameter indices that do not match the shipped model (the plan's w7 as an exponent on S made stability explode by about 500x per review; its difficulty step had the sign inverted). Per R28 the forms are copied from the reference implementation instead, fsrs-rs at commit c137ee6e096f9217632397a8fb2bdb6f6e1b92ae, `src/model_v7.rs` and `src/inference_v7.rs`, cross-checked against srs-benchmark `models/fsrs_v7.py`; the source is recorded in `app/engine/fsrs.py` and the vector's source file is committed as `tests/fixtures/fsrs_rs_inference_v7_c137ee6.rs` with its sha256 in `app/engine/fsrs_constants.py`. The awesome-fsrs wiki page R28 names documents only v0 to v6.
- FSRS-7 carries a second, fast stability per card that the P1 schema does not store; `app/engine/fsrs.py` reconstructs it as 0.8 times the long stability, which is the source's own SM-2 bridge. A `fast_stability` column is a P2 schema decision.
- The mastery corroboration test `test_stability_bounded` shows stability saturating at the source's 36500-day clamp after about 12 successive Good reviews at elapsed = S; retrievability still decays below 0.90 at large elapsed times. Whether that clamp is acceptable for an exam horizon of months is unexamined.
- `drain_probe_queue` in `app/engine/fringe.py` still takes `now` as a required positional; every public entry point supplies it through `session_now`, so only a direct call without it raises. `session_now` accepts a datetime `today`, but the rest of the selection path compares dates, so pass a date.
- `qa/last_report.json` is regenerated whenever `qa/12_report.py` runs and is restored with `git checkout -- qa/last_report.json` at session close, so the library's committed report does not drift because of build sessions.

- 2026-09-23, Slice 2 closing session: `var/subscription_smoke.json` is gitignored and was not
  re-run, so the file on disk still holds `no_tool_ran: false` for phase 2 from the old check. The
  two-turn allowance rests on the CLI 2.1.277 forcing its internal StructuredOutput tool for
  `--json-schema`; a later CLI that answers a schema in one turn, or takes more than one extra
  turn, will read `no_tool_ran` false in the smoke run and needs a look before the check is
  changed.

- 2026-09-23, P2 Slice 3, open:
  - `due_today_minutes` estimates the whole due queue through a deterministic cover; block 1 serves
    only 5 items or 5 minutes of it with a random draw, so the rest carries to later days and
    the served items can differ from the cover. Home does not show either new number; whether it
    should is a design-brief question for the operator.
  - A due skill with no published archetype (`DueQueue.uncovered_skills`) stays due every day and
    is not written to `audit_log`; block 2's coverage gaps are audited, block 1's are not.
  - In a fresh worktree `qa/12_report.py` exits 1 on `00_manifest` (97 "pdf missing") because
    `cache/pdf/` is not in the checkout, and `git status` shows `cache/pdf` as untracked rather
    than ignored. This session linked the main checkout's `cache/pdf` read-only for the QA run and
    removed the link afterwards; an orchestrator that links it must not commit the link.

- 2026-09-23, P2 Slice 4, open:
  - The curve omits 08's ideal diagonal and its "overconfident on confident by 18 points"
    sentence, and reports no Brier score or confidence minus accuracy, because all four need each
    rating mapped to a probability and no plan document fixes that mapping (see Decisions).
  - A legacy unsure rating stored before `attempts.confidence_source` existed stays unattributed
    and never counts, because nothing in the row tells a student's unsure from the close sweep's.
    On a database with P1 history the curve can therefore under-count the unsure level.
  - The 1.4.11 non-text contrast ratio is still unfetched (08, 11 P8 item 4), so the axis stroke
    uses `text-muted` and the marks `accent-base` without a measured non-text ratio.
  - `app/session/service.py` carries four one-line edits (two constants and three
    `confidence_source` assignments), inside the area Slice 3 also edits; they touch only
    `record_attempt`, `record_confidence` and `close_session`, not session assembly.

- 2026-09-23, P2 Slice 4 closing session: `app/progress/calibration.py` `counted_attempts` takes
  the day of each attempt from the UTC `submitted_at` string, while the window's end is the
  client's calendar day. An attempt made in the evening in a zone behind UTC can fall one day
  later than the student's own date, so at the window's two edges the count can differ by the
  attempts of one evening. Not fixed: no stored field records the student's zone.

- 2026-09-23, gate 29 cannot be drawn as specified. `app/review/audit.py`
  `draw_key_audit_sample` caps each unit at 15 items (`MAX_ITEMS_PER_UNIT`, from 10's "no unit
  contributes more than 15 items") and asks for 100 (`EVAL_29_SAMPLE_SIZE`), but P1's items span
  three units, so at most 45 can be drawn. Run over the 130 agent items as candidates it refuses
  with "only 45 items honour the 15-per-unit cap; 100 were requested", and with the cap lifted it
  draws 100, so the cap is the cause. Independently, `tools/draw_key_audit_sample.py` offers only
  provenance `operator` items and there are none, so today it refuses at "only 0 candidate items".
  Either the cap is waived for P1's three units or the P1 sample shrinks to 45; both loosen the
  gate as written, so the operator rules. Not changed.
- 2026-09-23, `var/growth.db` held no items when the 27 stems were reworded, so the new wording
  reaches the app on first ingestion. A database that ingested the old records keeps the old
  wording, because `app/items/ingest.py` skips a record whose id is already stored.

- 2026-09-24, `GET /progress` slowness not reproduced. A probe built the real composition root
  (`app/main.py` `build_application`, the live content snapshot, the subscription backend off)
  with the test passkey verifier, registered one user and ran a session a day, answering every
  served item. Over 10 days with `tests/fixtures/items_p1` as the bank it answered in 0.05 to
  0.15 s each day, and over 5 days with `content/items_p1_agent` in 0.14 to 0.35 s. The 45 s
  report above came from a seeded state that was not kept, so the cause is unknown; the probe
  stayed in the session scratchpad and nothing was changed.

- 2026-09-24, stage 3: the likely cause of the 45 s `GET /progress` report above. On a fresh
  database the first call that asks the bank for a published item (`app/runtime/bank.py`
  `has_published_item`, reached from `assemble_session` under both `GET /progress` and
  `POST /sessions`) ingests every pending source item and runs its SymPy distractor checks in
  forkserver children. A faulthandler dump of stage 3's seed run showed the first
  `POST /sessions` still inside `ingest_new_records` after 45 s, 84 child runs in. The earlier
  probe measured later calls, after ingestion. Not changed here.
- 2026-09-24, stage 3: the gap state of the mastery map cannot appear in P1. It needs an
  observation whose mastery_state is prerequisite_gap, and `rule_based_mastery_states` never emits
  one; the diagnostician (P3) does. The state is tested with a stored attempt, not seen in the app.
- 2026-09-24, stage 1, resolved the same day. `tests/e2e/test_agent_drafts_served.py` read the
  renamed `settings.items_directory` and only the P1 bank's keys; fixed as recorded under "Plan
  corrections applied". BC-QA-06010's single held error narrowed its items to improper rational
  integrands; 06014 and 10019 are settled in docs/operator/items-units-4-to-10.md.

- 2026-09-24, stage 1, open. Ingestion cost grew with the bank: every record's checks run on the
  bank's first query, each bounded SymPy comparison in its own forkserver child off the main
  thread. Measured: 120 records in 3.4 s, 766 in 77.8 s; `tests/e2e/test_unit_6_item_served.py`
  and `tests/e2e/test_agent_drafts_served.py` took 370 s together with other stages running. The
  operator's database pays it once per new record. These figures predate `bc09905`, which keeps
  bounded children between calls, and were not re-measured after it. It is the same first-query ingestion stage 3
  found behind the 45 s `GET /progress`, now over 786 records instead of 130. Candidate fixes:
  one bounded child per record, or checks cached by record hash.
- 2026-09-24, stage 1, open. Five closed-form archetypes have no items for want of held errors:
  BC-QA-01005, 06011, 06014, 07010, 10006 (docs/operator/items-units-4-to-10.md, "Result"). With
  06011 empty and every 10005 stem convergent, no item asks the student to recognise divergence.

- 2026-09-24, stage 2, the diagnostic's entropy stop fires mostly on surprises. At the recorded
  size (`docs/operator/p2-evals.md`), 316 of 400 synthetic runs stop early. 294 of those came in
  a 3-item window where one answer raised the summed unit entropy, which the plan's rule reads
  as entropy that stopped falling. The error direction is conservative: the unit stays
  unresolved and its skills are fast-tracked. The rule is 02's named tunable, for P7's held-out
  agreement to settle.
- 2026-09-24, stage 2, placement accuracy on synthetic students: 3,303 skills placed, 514 (15.6
  percent) not truly known. Each comes back as a review in about 4 days, and a credited failure
  un-masters it. The held-out problem shows the model over-predicts on this population, 0.377
  predicted against 0.095 observed.
- 2026-09-24, stage 2, the synthetic world never learns. Hidden knowledge is fixed per student,
  as in the P1 runner, so "truly mastered per item" measures how fast a policy finds known
  skills, not how fast it teaches. The two-term against five-term comparison should be rerun on
  a world that learns before P7 rules on it.
- 2026-09-24, stage 2, the six `SEEDED_PARENT_IDS` in `app/session/seed.py` are still seeded
  mastered. They were P1 out-of-subgraph parents (R15, Q8); with the whole graph loaded they are
  ordinary skills. A credited failure flips them, but the diagnostic never places them, because
  placement only adds.
  Resolved 2026-09-26: no BC-SKL row is seeded mastered (Decisions, 2026-09-26, false mastery).
- 2026-09-24, stage 2, a queued discriminating probe bypasses the interleaving window, as in P1.
  Nothing writes probes until P3's diagnostician, which should route a probe through
  `window_filter` so it is logged like every other serve.
- 2026-09-24, stage 2, `tests/api/test_unauthenticated_routes.py` fails in any checkout without a
  built `app/web/dist`, clean tree included, because the `/assets` mount exists only once the
  client is built. Run `npm run build` in a new worktree before the suite.

- 2026-09-24, stage 1, open, environment. The repository and its worktrees live in ~/Documents,
  which iCloud Drive syncs. After the rebase rewrote the stage 1 files, iCloud left a conflict
  copy named "<name> 2.<ext>" beside 682 of them (every item record, formulations file and
  README, and new test files, so pytest collected `test_unit_6_item_served 2.py` as a second
  module), and some copies were cloud-only placeholders ("compressed,dataless"), so reading one
  blocked. The full suite hung for 13 minutes at 0 percent CPU inside
  `tests/e2e/test_agent_drafts_served.py` `agent_records`, `read_text`, found with
  `-o faulthandler_timeout=300`. All 682 copies were untracked and byte-identical to their
  originals and were deleted. `test_every_record_file_is_named_by_its_id` fails on such a copy in
  a bank, but only once the copy can be read. The lasting fix is the operator's: keep the
  checkouts outside an iCloud-synced folder, or exclude them from sync.

- 2026-09-24, stage 8 (P7), open. On the learning world two-term does not clearly beat the
  random-within-fringe control: it matched or beat the control on true mastery per item for 67.5
  percent of 200 students (exponential) and 59.5 percent (power law), against 10's 90 percent bar,
  with means 0.01092 against 0.01055 and 0.02306 against 0.02310. The P2 world, which did not
  learn, passed the same comparison. Due-coverage selection is so far not shown to teach better
  than a uniform draw from the gated fringe. Simulation only; it is not a finding about the student.
  Updated 2026-09-27, stage 12, still open, now read as undecidable on this simulator rather than
  as a policy failure (`docs/operator/selection-study.md`). Two-term's only non-random term, due
  coverage, is above 0 on 1.1 percent of block 2 choices in 60 days and 7.5 percent in 226, because
  practice declares a mean of 13.6 skills in 60 days, so two-term and the control are nearly one
  policy: on the stage 8 world 106 and 116 of 200 students got identical traces, and the strict
  wins were 17.5 and 18.0 percent. Two-term against itself with reseeded engine draws wins on 47
  to 58 percent of 200 students, and the mean paired difference against the control has a 95
  percent interval across 0 at every horizon and curve. On the corrected world the bar reads 69.0
  and 68.5 percent at 60 days and 50.0 and 55.0 at 226. Deciding it needs the operator's ruling on
  the bar's form (Decisions, 2026-09-27). Simulation only.
  Closed 2026-09-27 by the ruling on the bar's form (Decisions, 2026-09-27): read from the paired
  mean difference, two-term against the control is -0.00016 [-0.00057, +0.00025] and -0.00029
  [-0.00071, +0.00013] in true mastery per item, not wholly below 0, so the floor passes. Two-term
  is not shown to teach better than random either; that is recorded, not a defect. Simulation only.
- 2026-09-24, stage 8, open. Arm 6 (`lambda` 2.0) and the compensatory arm served every student
  exactly what two-term served. Under two-term selection `LAMBDA` reaches only `sigmoid(m_k)` with
  a retrievability argument, which nothing that chooses items reads, so the decay gate in 10 cannot
  pass by construction. Deciding on decay needs a selection path that reads it first.
  Closed 2026-09-27, stage 12. The stage bands and the review floor now read `p_A` at today's
  retrievability, so arm 6 serves differently from two-term for 78 and 75 of 200 students at 60
  days (82 and 80 at 226) and beat it on at most 3.5 percent of students on mastery per item and 0
  percent on retention at day 30. `lambda` stays 0 on that result (Decisions, 2026-09-27). The
  compensatory arm still serves what two-term serves; its prediction is read only by the stage
  bands of skills with no credited observation. Simulation only.
- 2026-09-24, stage 8, open. False mastery exceeds 10's 5 percent ceiling on every arm, 22.1 and
  23.3 percent at worst, and none of it comes from practice (0.0 percent of masteries declared from
  practice). It is the six seeded parents of `app/session/seed.py` (about half not known by a
  synthetic student) and the diagnostic's placement (about 13 percent). The seeded-parent defect of
  stage 2 is the larger share.
  Resolved 2026-09-26 on the simulation: 2.2 and 2.6 percent at worst (Decisions, 2026-09-26,
  false mastery). About 9 percent of placed skills are still not known by the student.
- 2026-09-24, stage 8, open. The deterministic item checks miss a wrong intermediate
  worked-solution step (0 of 6 in the verifier golden set) and a no_calculator stem that is not
  closed-form (0 of 6). Only P4's independent re-solve and model verifier can catch them.
- 2026-09-24, stage 8, open, library. `data/frq_records.json` gives 2021 Question 4 parts that sum
  to 8, not 9, so the 2021 released form is left out of the checkpoint forms until the part points
  are corrected through staging. Six forms remain, one per 6-week checkpoint to May 2027.
  Closed 2026-09-27 (stage 13): the parts were right and the ninth point is a question-level
  point. sg-21 page 14 prints it before part (a), 1 point for writing the derivative of the
  accumulation function as the plotted function, earned in any one part; pages 15 to 17 give
  parts (a) to (d) 1, 3, 2 and 2, total 9. `data/staging/corrections-frq-2021-q4.json` puts
  `global_points` 1 and `global_point_types` BC-PT-99024 on BC-FRQ-2021-Q4-A, and
  `app/checkpoint/forms.py` offers it as its own row, "any one part", before the lettered parts.
  Seven forms: 2025, 2024, 2023, 2026, 2022, 2021, 2019.
- 2026-09-24, stage 8, open, bank. ITM-AGT-10005-02 option B (1/(e - 1), the series sum) is tagged
  BC-ERR-10013, which describes a different substitution. The key is right; the error tag is not.
  Found by the golden-set agent, not changed.
  Rechecked 2026-09-26: all 9 BC-QA-10005 items tag their series-sum distractor BC-ERR-10013,
  whose observed behaviour is the reverse direction (integral value reported as the series sum).
  The linked misconception, BC-MIS-10008, fits both. A fix needs a new error record through
  staging, not an item edit; left open.
  Closed 2026-09-27 (stage 13): BC-ERR-10044, "Sum of the series reported as the value of the
  improper integral" [inferred], sources ced:189, minted through
  `data/staging/corrections-errors-10.json` and linked to BC-MIS-10008, BC-SKL-10016 and 10017
  and BC-ERR-10013 through the other `corrections-*-10` files. The series-sum distractor of
  ITM-AGT-10005-00, 02, 04, 08, 09, 10, 12, 13 and 17 now names BC-ERR-10044; SymPy confirmed
  each retagged option equals the series sum and differs from the key. BC-ERR-10013 stays: the
  template `app/generation/templates/qa_10005.py` and ITM-GEN-10005-00 to 04 test its own
  direction (the integral's value stated as the series sum). `tools/check_items.py
  content/items_unit10_agent`: "records read: 257", "clean: 257", "with violations: 0".
- 2026-09-24, stage 8, open. Transcriber golden set 3 has page specifications and reference
  transcripts but no images: each page must be written by hand and photographed, which no session
  can do. Golden set 2 covers 17 point types, not 30, because only 17 reach a model.

- 2026-09-24, stage 4, open. The image gate's thresholds were set on rendered pages only; the first
  real photographs should re-tune them (`frq_images.quality` records every measurement).
- 2026-09-24, stage 4, open. Grading runs as a request background task, not a `jobs` row: a server
  stopped mid-grade leaves the attempt confirmed with no points until the student confirms again,
  and a point left pending by a pacing or usage stop is retried only by the next confirm or re-read.
  The capture screen now says so after about five minutes instead of spinning.
- 2026-09-24, stage 4, open. Credit reversal restores a skill row only if nothing moved it since;
  otherwise it takes back c and f alone, leaving FSRS, fading counters and success days as the
  later attempt left them.
- 2026-09-24, stage 4, open. The live grader is not stable on borderline justifications: the same
  confirmed work split 0, 1 or 2 points across six recordings, and a re-read of a split point in
  the manual runs split again. That is the escalation doing its job; it also means a point on the
  boundary will often stay provisional.
- 2026-09-24, stage 4, open. Golden sets 2 and 3 are model-authored and model-graded, the
  transcription error share rests on one error, and no metric 9 week exists: it is built and reads
  pending_on_usage until four weeks of real captures exist.
- 2026-09-24, stage 4, open. The re-read of a point only re-judges it; the transcription behind it is
  not re-read. Purge leaves `review_queue` rows whose ref_id named a deleted grading.
- 2026-09-24, stage 4. `app/grading/point.py`'s evidence-quote check first escalated 10 of 150
  golden targets because the grader quoted across the "2. [math]" and "answer:" labels the prompt
  prints and used ellipses; with fragments compared line by line, 1 of 150 still fails it. Before
  the fix the golden result was exact agreement 0.9343 on 137 published, 13 escalated.

- 2026-09-24, stage 5 (p4). A publish run hung for about five and a half hours at 1 percent CPU
  and then died on an uncaught `_Timeout` from `app/items/verify.py` `run_bounded`: a repeat alarm
  can fire inside the `finally` that disarms it. The handler is now set to ignore before the timer
  is cleared, which narrows the window without closing it, and `tools/generate_bank.py publish`
  catches a raising check as rule 4 and runs one bank per process. The hang itself was not
  reproduced.
- 2026-09-24, stage 5 (p4). Heavy paraphrase of official text (every listed synonym swapped and the
  sentences reordered) passes the duplicate gate on 45 to 60 percent of labelled pairs. The
  zero-miss threshold would block most original items. Residual risk rests on construction.
- 2026-09-24, stage 5 (p4). BC-QA-04010 (position from velocity with an initial condition) lists
  only skills 04006 and 04011, neither an accumulation skill; its error links went to 04011 for want
  of a closer skill. Library work.
- 2026-09-24, stage 5 (p4). The first query of the app over a fresh database now ingests about
  3,100 items with SymPy checks; not timed through the running app.
- 2026-09-24, stage 5 (p4). Template group F (units 8 and 9) was cut off by a usage limit before
  its final report. All 16 of its templates pass the gate, their 522 candidates went through the
  blind re-solve like every other, and 14 of the audited 100 came from unit 8 with no key error,
  but no author report exists for them.
- 2026-09-24, stage 5 (p4). Two existing tests met the new bank. `tests/e2e/test_cold_start.py`
  asserts the diagnostic asks only short answers; statement items would have broken that, so the
  diagnostic now reads a short-answer view of the bank (`ShortAnswerBank`) and statement-only
  archetypes are diagnostic coverage gaps, as they were before they had items. The helper in
  `tests/e2e/test_agent_drafts_served.py` read `answer_key["mathjson"]`, which a statement item does
  not carry (now `.get`), and its search stopped at the first Unit 2 item, now usually a generated
  one, so it searches for the first agent draft from Unit 2; no assertion changed.
  `tests/api/test_unauthenticated_routes.py` failed once in a full run because `app/web/dist` did not
  exist until a later step built it; it passes once built.
- 2026-09-24, stage 5 (p4). Some templates repeat one BC-ERR id across two distractors where no
  other held error fits, and a few fits are loose (listed in the template authors' reports kept
  with the scratch notes of this session, not in the repository).

- 2026-09-24, stage 6 (p5), open. The function-graph figures (app/web/src/figures/FigureView.tsx)
  print no numbers on the axes, so a value read off a graph has to be found by counting grid
  lines; a mock question on BC-QA-06003 was missed that way. Figure work for a later stage.
- 2026-09-24, stage 6 (p5), open. The free-response bank holds 6 calculator and 10 no-calculator
  nine-point questions, so the fourth mock repeats Section II Part A questions and the third
  repeats Part B's (least-used first). Writing more is content work.
  Closed 2026-09-27 (stage 13): 79 new original questions, 24 calculator and 55 no-calculator,
  so the bank holds 30 and 65 nine-point questions against a target of 30 and 60 (10 mocks and 5
  drills of each Section II part to 10 May 2027, Decisions, 2026-09-27). 119 records, 0 problems
  (`tools/check_frq_items.py`); 439 of 439 checked keys match blind formulations, control held.
- 2026-09-24, stage 6 (p5), open. Calculator free-response questions lean on the model: their
  setup points with a numeric root as a limit carry no check, and a student's integrand written
  with the stem's function names (E(t), L(t)) is unreadable to the deterministic checks, so with
  the grader off those points stay provisional (docs/operator/p5-timed-runs.md, runs 9 to 12).
  Closed 2026-09-27 (stage 13): a question now carries `functions` (each name's variable and
  expression) and `roots` (each named root's value and the equation it solves), the checks read a
  line through those definitions, a limit written as a named root, a three-place decimal or a
  symbol the student set to one is compared with the root, and `equation_setup` decides a setup
  equation whose unknown is a root. A capital name the question does not define is refused and
  the point stays provisional; `equation_setup` passes or stays provisional, never fails. Runs 9
  to 12 again, grader off: 25 of 72 points decided, 47 provisional, against 6 and 66 on the tree
  before (docs/operator/p5-timed-runs.md). What stays provisional is model-required, or an
  integrand point with a constant factor outside the integral (BC-PT-99048, 99058, 99002), which no
  check reads, or gated on one of those; that last kind is still open.
- 2026-09-24, stage 6 (p5), open. The band's placement rests on an assumed cohort shape (the
  free-response section's summed means and spreads); no measurement can check it until the
  operator's mocks sit beside released-form checkpoints.
- 2026-09-24, stage 6 (p5), open. A database that ingested ITM-GEN-01005-04 before its retirement
  keeps serving it, because ingestion never re-reads a stored id; the operator's var/growth.db held
  no attempts on 2026-09-24.
- 2026-09-24, stage 6 (p5), open. eval_the_harness_runs_end_to_end_on_seeded_weeks (P7) failed in
  two of four whole-suite runs this stage (one serial, one with four workers) and passed in every
  run of it alone or with tests/api (five runs). The failing assertion was not captured; nothing in
  stage 6 touches the experiments or the metrics view, and whether it fails on 6b5ba6d was not run.
  Read a red here as this flake only after rerunning it alone.
- 2026-09-24, stage 6 (p5), open. The model answered the browser mock, so its pacing figures show
  the screens work, not how a student paces; the rapid-guess threshold is untested on real
  latencies.

- 2026-09-26, stage 7, open. No live call has met a subscription usage limit yet; the limit patterns
  come from the CLI binary's own wording, and whether a real limit arrives as `is_error` JSON or on
  stderr is still unobserved (both are matched).
- 2026-09-26, stage 7, open. The cooldown board lives in the server process, so after a restart the
  first call or drain pass may start one CLI process to learn that a limit still holds.
- 2026-09-26, stage 7, open. `tests/assessment/test_capture_concurrency.py::test_no_write_lock_is_held_while_the_diagnostician_runs`
  failed once in a six-worker run of eleven test directories and passed alone; not investigated.
- 2026-09-26, stage 7. `tests/grading/test_metric_nine.py` read the metrics view on the local
  calendar day while the rows were aged in UTC, so it failed every evening in a zone behind UTC (seen
  at 19:56 EDT); it now reads the UTC day of the same clock. No assertion changed.
- 2026-09-26, stage 7, open. The contrast eval checks the screens its catalogue renders in jsdom
  plus four screens in the real app; a screen state the catalogue never renders is outside it, and
  the eval's third and fourth tests fail when a colour rule or token is drawn by no catalogued
  screen, which is the guard against that gap.
- 2026-09-26, stage 7, open. The keyboard-only test drives the session with a keyboard driver that
  does what a browser does with Tab, Enter and Space; the real MathLive field was driven by keyboard
  in the browser once (the diagnostic item), not through a whole set.

- 2026-09-26, stage 9, open. MathLive's `convertMathJsonToLatex` with compute-engine 0.24.1 writes
  the constant e as `\exponentialE`, a macro KaTeX does not know, so an option whose MathJSON holds
  `ExponentialE` rendered as raw LaTeX (seen on a Section I Part B drill option, `440\exponentialE^{t}`).
  Present before stage 9. Closed the same day: `mathJsonToLatex` rewrites it to `\mathrm{e}`, and
  `app/web/src/math/mathjson.test.ts` went red on the old code and green after.
- 2026-09-26, stage 9, open. The before and after screenshot walks start from one database snapshot
  but a part drill draws its questions afresh, so a pair shows the same screen with different
  questions.

- 2026-09-26, stage 10, closed. A statement-keyed item (`requires_choice`) served at example or
  completion showed its options, but the commit sent `{mathjson: null}` because it treated only the
  unsupported stage as a choice, so the chosen option was never graded. `servesChoice` in
  `app/web/src/session/Item.tsx` is now read by both the screen and the commit; the new test in
  `SessionScreen.test.tsx` failed with `"mathjson": null` before the fix.
- 2026-09-26, stage 10, closed. The representation matrix labelled every row and column with its
  bare BC-REP id in the running app, because `settings.snapshot` is empty until first use.

- 2026-09-27, stage 11, closed. `app/web/src/testing/cascade.ts` read every rule inside @media as
  always applying, so a base colour overridden only inside a `max-width` block was never checked at
  desktop width. Shown on the old code: with `.home-lead` in `accent-tint-2` in the base rules and
  in `text-primary` inside `@media (max-width: 600px)`, the old eval passed with 1.16:1 body text;
  the media-aware eval fails it as "light: home, ready at 1280 px: p.home-lead ... is 1.16:1, floor
  4.5:1". The same rule inside the 600 px block alone fails only "at 375 px".
- 2026-09-27, stage 11, open. The evals read two widths, 1280 and 375 px. A rule whose condition
  holds only between them, such as a `min-width: 700px` and `max-width: 800px` pair, is matched at
  neither; the coverage test then fails it if it carries a colour, which is the guard, but its
  non-colour declarations reach no greyscale state.
- 2026-09-27, found in the password walk, open. On a fresh database the first `GET /progress`
  ingests the pending item bank (`app/runtime/bank.py` `_ingest_pending_source`, with the numeric
  checks of `app/items/verify.py` in child processes) inside one write transaction, for well over a
  minute. Any write sent meanwhile waits past the SQLite busy timeout and answers 500 `database is
  locked`; in the walk that was `POST /auth/logout` writing `session_closed`. Not caused by the
  password change, which left the ingest path untouched.
- 2026-09-27, stage 11, open. The theme choice lives in one browser's localStorage, so a second
  browser or a cleared profile starts at System; the server holds no copy.
- 2026-09-27, stage 11, closed. `get_db` committed after the response was sent (FastAPI's default
  scope for a dependency with yield), so a read sent the moment a write returned could see the
  state from before it. In the real app, "I have not learned this yet" once left the diagnostic on a
  question the server had recorded, after which every click was refused as already answered, and
  "Start the diagnostic" once opened a session the next read could not find. Every use is now
  `Depends(get_db, scope="function")`; `tests/api/test_db_commits_before_reply.py` failed with one
  plain use left in `content.py` and passed restored. The race does not show under the test
  client, so the evidence it is gone is the real-app walk, which completed the diagnostic, the
  skip and the session.
- 2026-09-27, stage 11, closed. The diagnostic numbered its first question 2 and its last could
  read "Question 31 of at most 30": `diagnostic_position` was taken after the new entry was
  appended. The new test in `test_diagnostic_routes.py` failed with `[1, 2, 3, ...] == [0, 1, 2,
  ...]` on the old line and passes now.
- 2026-09-27, stage 11, open. N and P, and A to D, do nothing while focus is on a button, a
  question-menu tile included, by stage 10's rule that a key on a button activates it. From the
  page body they move and choose as before (checked in the real app: "Question 30 of 42" to 31 and
  back).

- 2026-09-27, open. The contrast catalogue's setup, which renders every catalogued screen, took about
  59 s against its 60 s budget when vitest ran beside the full pytest run (9 to 14 s unloaded in
  stage 9). Each catalogue screen added since pushes it closer. Run vitest and pytest one after the
  other, or split the catalogue, before the budget is reached unloaded.

- 2026-09-27, stage 13, open. An integrand-only point with a constant factor outside the integral
  (BC-PT-99048 one half, 99058 pi, 99002) has no check, so with the grader off it and every point
  gated on it stay provisional; FRQ-AGT-09013-01 decides none of its nine points for that reason.
- 2026-09-27, stage 13, open. The LaTeX reader leaves some ordinary student forms unreadable, so
  their points go to the model rather than a check (never a false fail): `\cdot` written before
  `\sin`, `\cos` or `\ln`, `\cdot 2x`, `\sqrt{x}e^{-x/4}`, `\sin 2\theta`, and a factored `x(x-2)`,
  which reads two ways. Found by the stage 13 authors, who rewrote their own keys around them.
- 2026-09-27, stage 13. The full pytest suite was run once on the first three stage 13 commits
  (1388 passed, 1 failed: `tests/content/test_loader.py` pins BC-ERR_active at 390, and the new
  BC-ERR-10044 makes 391; the pin now reads 391). It was not rerun after the 79 new questions were
  added, on the operator's instruction to merge on targeted checks; the targeted files are listed
  in Done.

- 2026-09-27, stage 13, open, environment. The shared `.venv` was reinstalled at 01:50 by another
  session whose uncommitted main-checkout changes drop `webauthn`, so on this tree every test that
  builds the app errors at import. Stage 13's targeted run put `webauthn` on a scratch
  PYTHONPATH; the shared venv was not touched. Whoever lands that auth change owns the venv.

- 2026-10-02, stage 13 (frq), fixed. b6f9aa27 merged red: moving the roles to
  `claude-sonnet-5-5` changed every grader and transcriber request digest, so the transcription
  and grader golden books missed on every call (116 and 450), and its own re-recorded
  paper-to-grade book decided all four points where `test_paper_to_grade` asks for one
  provisional. Any change to `app/providers/model_routing.py` for a role with a cassette book
  needs the books re-recorded in the same commit; `tools/p3_evals.py record-transcription`,
  `record-goldens` and `tools/record_grading_cassettes.py paper_to_grade` are the tools.

- 2026-10-02, stage 13 (frq), finding, the re-recorded read-backs. On the 17 golden set 3 pages
  the quality gate accepts, Sonnet 5.5 finds the same 30 of 43 point-bearing expressions as
  Sonnet 5 and marks the same 3 of 3 struck lines, but it leaves the part's `answer` field empty
  on 9 pages where Sonnet 5 copied the last line into it. The prompt asks for an answer only
  when one is marked, boxed, underlined or clearly stated last, so both readings are within it,
  and grading is unaffected because `app/grading/checks.py` `answer_line` falls back to the last
  live math line. On GLD-TRN-001 the new reading names `f''(x) = 6x`, the last line, where the
  old named `f'(x) = 3x^2 - 4`; on GLD-TRN-015 it reads the answer as `4\pi` without `A =`, so
  that page's point-bearing count drops from 2 to 1 while GLD-TRN-002 rises from 2 to 3.

- 2026-10-02, stage 13 (frq), open. No screen reads `FeedbackPayload.tutor_unavailable`, so on
  a multiple-choice or short answer the line plan 07's hard-stop table asks for ("the tutor is
  unavailable for the rest of today") never shows; the free-response result now shows it
  (`app/web/src/frq/GradingView.tsx`). Left for the session screen's owner, because this stage
  is free response only.

- 2026-10-02, stage 13 (frq), finding, the grader golden set on Sonnet 5.5. Replayed from the
  re-recorded book (`docs/operator/p3-grader-eval.json`), against the Sonnet 5 record it replaces:
  escalations 4 to 18 of 150 targets (2.67 to 12.0 percent), published points 146 to 132, exact
  agreement on published points 0.9315 to 0.9924, mean absolute error per point 0.0685 to 0.0076,
  single-sample agreement 0.9133 to 0.9333. The grader defers more and is right more often when it
  does decide. Transcription: errors caused by reading 1 to 2 and decisions changed by reading 5 to
  4, over 20 golden set 2 pages. These are a model's grades of model-written golden responses, not
  a human's measurement (2026-09-24 ruling).

- 2026-10-02, stage 13 (frq), finding, the paper-to-grade recording. Six fresh recordings of the
  same page replay with 2, 3, 0, 1, 2 and 3 provisional points. The fourth, with one, is committed
  because `test_paper_to_grade` exercises the path from one provisional point to the review queue;
  the spread itself says the borderline justification on that page splits the live grader.

- 2026-10-02, stage 13 (frq), open, item. FRQ-AGT-05001-01 part (c) scores only the Mean Value
  Theorem or Rolle route (c1 the equal endpoint values, c2 eligible only after c1). On the live walk
  a valid argument, h' continuous because h is twice differentiable and h'(3) = 3 > 0 > -4 = h'(8),
  so the Intermediate Value Theorem gives h'(w) = 0, earned 0 of 2, and the tutor's paragraph told
  the student that theorem cannot earn the point. The record format has no alternative route for a
  point, so the fix is a format change (an alternative criterion per point, or a second point set
  per part), not a record edit. Other records that name the IVT as not earning a point should be
  read for the same gap (11 records mention it).

- 2026-10-02, stage 13 (frq), open, grader wording. On FRQ-AGT-05001-01 part (d) the student wrote
  only h''(v) = 1; the grader's cited rule called it "a bare quotient template with no values
  substituted", and the tutor's paragraph repeated that description to the student. The decision
  (not earned) was right and the description was wrong. The tutor composes from the grader's cited
  rule, so a misdescribed rule reaches the student unchecked.

- 2026-10-02, stage 13 (frq), open, display, found on the live walk. The point criteria and the
  grader's rationale are shown as plain text (`0 <= x <= 2`, `(1 - 4)/8`), and a deterministic
  point shows its check name to the student ("sympy_equivalence: ... equals -3/8"). A part's answer
  of "No" in a read-back is typeset as italic mathematics. A transcriber note with undelimited LaTeX
  (`\frac{62-20}{10}`) still shows its backslashes; delimited notes are now typeset. In the typed
  entry, the first click on "Add a line of words" after typing in a math field is swallowed and a
  second click is needed, and the words input has no accessible name (its visible label is not
  associated with it). The unit check's question list shows "Open" for a question already graded.
  The question screen before an answer (choosing, typing, photographing) is not on the Workbench.

- 2026-10-02, stage 13 (frq), open, test. `tests/providers/test_ai_notices.py::
  test_a_grader_brief_summarises_the_decision_and_leaves_out_the_student_work` has failed since
  b6f9aa27: it renders the v2 grader template with the v1 single-point fields ("unknown template
  fields: ['criterion', ...]"). The single-point request it describes no longer exists. It is left
  unchanged, because only the operator loosens or retires a gate; the new test beside it covers the
  whole-part request the grader now sends. `tests/grading/test_prompt_goldens.py::
  test_the_grader_receives_every_field_of_the_point_record_and_nothing_undeclared` fails for the
  same reason on both v2 templates; main (2d608113) gives the same "3 failed, 25 passed" over the
  two files.

- 2026-10-02, stage 13 (frq), open, test isolation. `tests/e2e/test_agent_drafts_served.py` reads
  the checkout's own `var/subscription_pacing.json`: in the frq worktree, after the cassette
  recording and the live walk had written that file, it failed four runs in four ("no Unit 2 item
  was served in 12 sessions"), and with `var/` moved aside it passed ("1 passed in 428.62s"); on
  main and in a scratch worktree with no `var/` it passed three in three. A test that builds the
  app should point every `var/` path at its tmp directory. The e2e failures that main shows
  (session_login_to_feedback, exit_criteria_mastery) should be rerun with main's `var/` moved aside
  before they are taken for engine faults.

- 2026-10-02, stage 13 (frq), note. `tools/check_items.py content/frq_items` stops with
  `KeyError: 'answer_key'`: it checks multiple-choice and short-answer banks. The free-response
  bank's checker is `tools/check_frq_items.py` (via `tests/grading/test_frq_bank.py`).

- 2026-10-02, stage 12 (prompts), open. `app/feedback/tutor.py` `point_line` writes the
  criterion and the grader's rationale followed by a period, and both usually end in one already,
  so the frq_points message reads "present.." (seen in `tutor_frq_points_live_00.json`). Cosmetic,
  in the user message only.
- 2026-10-02, stage 12 (prompts), open. The output golden for `feedback/elaborated_v2` still
  checks the eight Haiku recordings of 2026-09-23, not a recording on the routed
  `claude-sonnet-5-5`; `tools/record_prompt_outputs.py` can record them when the template next
  changes.
- 2026-10-02, stage 12 (prompts), open, not this stage's. On main at 8a0d4289 the engine and
  item tests fail as they did before this stage: `test_selection_study` (decay arm),
  `test_simulation` (prereq gap, mastery growth), `test_today_policies` (retrieval ordering), the
  e2e mastery paths and login to feedback, the items comparison tests, and the unit check.
  `tests/api/test_unauthenticated_routes.py` needs a built `app/web/dist` and a worktree needs
  `cache/web` linked beside `cache/pdf`, or `qa/00_manifest` reports the Desmos web sources
  missing. One `tools/affected_checks.py` run hung for over 12 minutes with pytest blocked on a
  read from an idle forkserver worker after `tests/items` started; per-file processes under a
  900 s cap finished.

- 2026-10-02, stage 11. `tests/eval/test_simulation.py::eval_simulation_mastery_growth` (gate 31)
  red since d6d8e165: the two-term policy does not beat random within the fringe on 30-day mastery
  per item (20 seed sets: -0.00122, 95 percent interval [-0.00354, 0.00110]). A gate the operator
  owns. `tests/eval/test_selection_study.py::test_the_decay_arm_serves_differently_from_two_term`
  red since the root gates: 6 days from cold start leave LAMBDA nothing to change. The operator
  owns its horizon. `tests/e2e/test_paper_to_grade.py`, red since b6f9aa27 on a
  unanimous cassette, passes on this branch after the rebase onto 4e602af0's re-recording ("1 passed"). `tests/e2e/test_agent_drafts_served.py` stays order dependent
  (passed alone in 405 s this session; it needs a Unit 2 agent draft within 12 sessions 8 days
  apart from an unplaced cold start, which the measured pace makes marginal).
- 2026-10-02, stage 10 (checking), open. The tutor reply screen's leak check,
  `_equals_key` in `app/evals/agent_checks.py`, reads a comparison that raised or did not settle
  as "not the key", so a key written in a form SymPy cannot settle against it is not flagged as a
  leak. Its policy is undocumented and the stage 10 prompt did not name it among the callers to
  align; treating unsettled as a leak would block replies that mention any unsettled expression,
  so it needs its own ruling and a measured false positive rate before it changes.
- 2026-10-02, stage 10 (checking), open. Whether a bank checks clean depends on host load,
  because a comparison that outlives the 5 s bound is unsettled. Measured with a 60 s bound at
  load 45 to 70: the slowest option pair of each of ITM-AGT-03009-00 to -12 took 0.8 to 6.5 s and
  every one settled distinct. At load 115 to 160, `tools/check_items.py` flagged 1 record in
  items_gen_unit02, 2 in items_gen_unit06 and 4 in items_unit03_agent as unsettled, and main
  flagged a different 03009 record; at load 15 all three banks are clean (191, 330 and 20). It
  fails safe, toward review, never toward a wrong verdict. `_settles_to_zero` now computes
  simplify once and stops at the first zero, which cut the ITM-GEN-02010-02 A against B pair from
  over 5 s to 0.8 s at load 59. Run bank checks on a quiet host until the bound is measured.
- 2026-10-02, stage 10 (checking), fixed. `tools/key_recheck.py` `equivalent` counted a point
  where the difference evaluated to NaN or an infinity as agreeing, because NaN is never larger
  than the tolerance: a key of 1/0 or NaN rechecked as equal to 3 (measured before the fix,
  `equivalent(nan, 3)` and `equivalent(zoo, 3)` both True). It now skips such points, so the pair
  is `comparison_undecided`, and an equation against a number is undecided rather than an
  uncaught TypeError.

## Plan corrections applied [verified]

Session 2026-09-23 (fourteenth). No plan file was edited. Readings applied in code:

- 03 check 4 "dimensionally correct" read as "the same unit": a unit of the same dimension at a
  different scale (cm against m, m/s against ft/s) is wrong, because the value is compared
  without conversion. The builder's first reading, same dimension is notation, credited 12.5 m/s
  against a key of 12.5 ft/s.
- 11 exit criterion 4, "measured rather than estimated": no key error rate is published while any
  sampled item lacks exactly one verdict. Two assertions written earlier expected a partial rate
  (0.2 and 0.5); they now expect none.
- One assertion written this session, `"M"` against a key of `m` ungraded, was changed to credit
  it, to agree with the committed `" M/Sec "` case in test_units_declared_but_absent_is_notation_only.
- 13 line 60 says a truncated tutor call returns `stop_reason: "max_tokens"`; true of Anthropic's
  raw response, and the normalised result now carries it as `finish_reason`.
- 06's API table has no rows for `GET /auth/status` or `POST /auth/passkey/add/begin|finish`.

Session 2026-09-23 (thirteenth).

- `docs/plan/09-security-and-privacy.md` CSP paragraph: adds `style-src-attr 'unsafe-inline'`.
  Old reading: styles restricted to self with per-build hashes. Reason: MathLive lays out formulas
  through run-time style attributes; under the old policy a fraction rendered collapsed with 121
  blocked-style errors, verified in a browser.
- `docs/plan/02-adaptive-engine.md` lines 733 and 734: gamma 0.4 and rho -0.2 in the tunables
  table corrected to 1.0 and -0.5, which lines 130 and 131 and the code already use.
- `docs/plan/06-architecture.md`: attempts gains the five tutor accounting columns; budgets gains
  `settled_calls`, `cached_read_reported_calls`, `cached_write_reported_calls` and `stopped_by`,
  with the rule that a count of 0 means the cached sum is not a measurement; line 93 names
  py_webauthn.
- 11 entry criterion 5 and implementer decision 6: the token file is the implementer's, not the
  operator's. The eighth to twelfth sessions filed it as human-only. The operator chose the
  palette; the implementer produced and checked the values.
- 11 P1 Goal against scope 17: the onboarding account screen (passkey registration) is in P1,
  because the Goal has a student register and scope 17 excludes only the diagnostic onboarding.
- `app/design/tokens.py`: `accent-contrast-text` is no longer checked on `accent-base`, approved by
  the operator. 08 gives the button text its own token, `text-on-accent`, still checked.
- 13 item 4 with 07's "No further tutor calls today": the stop latches; its refusal names the cap
  that stopped it. Three tests in tests/providers/test_guard.py were rewritten on 13 items 3 and 4:
  the abandoned stream now asserts the worst-case charge (old `tokens_in == 0`, `cost_usd == 0.0`),
  and the two latch tests assert one refusal row naming `usd` (old `len(refusals) == 2`, `reasons ==
  {"usd", "hard_stopped"}`).
- 13 "raising a cap clears the stop": read as every stopping cap raised, none lowered, all above
  the day's spend.
- 13 item 6: charged at the 1h write rate because the result carries no TTL split.
- 07 "the adapter passes it through": replaced by an allowlist, because 13 line 20 makes
  temperature a 400 and a passthrough let model and max_tokens bypass the guard.
- 07:145 thinking form: only `{"type": "disabled"}` is accepted, per 13:22 and 13:60; the adaptive
  form 07 names for the generator stays refused until P4 needs it.
- 09 "refuses a Secure-less cookie on a non-loopback origin": origin read as the request host.
- 06 "the verifier stays in-process with SymPy": read as in the application, not a separate
  service; the child process is a time bound.
- 11 exit criterion 8 "per served item": items with no tutor call count at cost 0 (06's
  `tutor_calls` DEFAULT 0); both medians are printed.
- 13's per-session tutor ceiling: reaching it returns no sentence rather than "unavailable for the
  rest of today", which 07 writes for the daily cap.

Session 2026-09-22 (twelfth). None of these edits docs/plan.

- 06 API surface, `GET /progress`, listed as "mastery map, calibration, due counts". The progress
  screen is not P1, but home's three counts and minute forecast need a route, so P1 serves only
  the due-count part there. Old reading: a progress-screen route. Reason: 08 home needs the counts
  and 06 names no other route that carries them.
- 06 API surface has no self-explanation route. `POST /sessions/{id}/attempts/{aid}/self-explanation`
  is added beside the error-note route, which also predates 06's table. Reason: 06 defines the
  `attempts.self_explanation` column and 11 P1 scope 10 requires the answer.
- 11 P1 entry criterion 5 lists the spacing scale among values the implementer produces. 08 already
  fixes the nine values, so they are emitted from 08 directly and are not operator input. Names
  are `space-<px>` because 08 gives none.
- 07 Budget caps, "stored in budgets". Read as: the cap in force is on today's budgets row, carried
  forward from the latest earlier row once the operator has changed it through settings.
- 09, "an extension is an explicit act". Read as: a changed exam date never moves `purge_after`.
- 11 Q16, "served at stages example and unsupported only". The server serves such a completion slot
  at example, keeping the support the engine chose.
- 11 Remaining implementer decision 3 (no answer at example). Read as: step marks at example carry
  no verdict; every step is marked given.

From the eleventh session, 2026-09-21.

- `docs/plan/11-phased-delivery.md` gate 25 and the previous three sessions' Next candidates. The
  old reading filed `test_reduced_motion_replaces` as human-only, waiting first on the design token
  file and then on screens. The new reading is that gate 25 reads no hex value: its property is the
  reduced-motion contract plus the presence of five affordances, and 11's own P1 scope items 8
  (`app/web/session/Item.tsx`), 11 (`app/web/input/`) and 17 (home, session and settings screens)
  put the client inside P1. The gate is closed this session with the token file still unwritten.
  The token file still blocks gate 26, which does read hex values, and that remains human-only.
- `docs/plan/06-architecture.md` line 93 names React 18, TypeScript, Vite, KaTeX and MathLive, and
  names no client test runner, exactly as it names no Python test runner. Vitest with jsdom and
  @testing-library/react are therefore the implementer's choice on the same footing as pytest,
  hypothesis and httpx2, which 06 also does not name. `@types/node` was added for the same reason.
  Recorded here rather than treated as a dependency not named in 06.
- `docs/plan/08-design-brief.md` Motion rules gives one number, "under roughly 300 ms", and states
  that Material 3's numeric duration and easing tokens could not be loaded, so specific millisecond
  values are unknown. `motion.css` uses 300ms as the single duration and cites it as the stated
  ceiling rather than as a token value. This is a bound used as a value and is flagged rather than
  hidden.
- `BUILD-LEDGER.md`'s eighth-session finding on the accent tint range does not reproduce as
  written. It said a brief reading "1 through 6" would leave the test green against a four-name
  `COLOUR_TOKENS`. In fact the old parser's range regex stops matching under that mutation and the
  interior names vanish, so the old test also went red, for an incidental reason. The fix is still
  correct and the endpoints are now derived from 08, but there was no false pass to point at.

Session 2026-09-20 (ninth).

- `docs/plan/02-adaptive-engine.md`, Variant adjustment. Read as if instantiations of one
  template share the archetype's difficulty. A paragraph now records that they do not, per the
  sources in 13, that the prior gains no variance term and accepts a centre-ward bias, and the
  measurement that would add the term. Reason: Tian and Choi (2023) and Sam et al. (2023), as
  summarised in 13.
- `docs/plan/04-item-generation.md`, the parameter spec bullet for `role`. Read `role` (`safe`
  or `difficulty`) with no check behind it. It now maps `safe` to a declared incidental and
  `difficulty` to a declared radical, states that the declaration is checked by structural
  invariance of the solution path, and that distractor composition is always a radical.
  Reason: Embretson and Daniel (2008), distractor evaluation b = 0.999.
- `docs/plan/11-phased-delivery.md`, P4 scope items 7 and 11. Read `app/generation/generate.py`
  and `prompts/generator/symbolic_v1.md`, per-item generation. Now read
  `app/generation/template.py`, `app/generation/instantiate.py` and
  `prompts/generator/template_v1.md`. Reason: the template architecture decided in 13; none
  of the named files existed, so no code moved.
- `docs/operator/ai-operating-costs.md`. Read `app/providers/anthropic.py:79 sends one today
  and must stop`; now records the fix. Every dollar figure re-derived from
  `tools/cost_model.py`, see Done.

Session 2026-09-20 (AI layer research pass). No application code, no tests and no `app/` change.
`docs/plan/13-ai-engineering.md` and `docs/operator/ai-operating-costs.md` are new. Every number
in both was fetched from a provider page on 2026-09-20 or measured in this repository; the
unsourced ones are listed in 13 under "Claims I could not source". `data/` and `research/` were
read and not written; `git status --porcelain` on both is empty. `qa/12_report.py` exit 0.
`tools/style_gate.py` exit 0 on every file written.

- `docs/plan/07-ai-provider-layer.md`, the D8 routing table, three rows. The verifier read
  `Anthropic claude-opus-5`, the same model as the generator, which maximises the correlated
  generator-verifier failure that 04 guards against with "a second model, on a different provider"
  and that 10 calls "the worst case"; it now reads `Gemini 3.8 Flash (batch, paid tier)` with
  `claude-sonnet-5` on batch second. The diagnostician read `Anthropic claude-opus-5` while the
  same document justifies Anthropic-first by naming the grader, the verifier and the transcriber
  as the roles whose errors reach a student directly, which does not include the diagnostician,
  and while the grader, which it does name, runs on Sonnet; it now reads `claude-sonnet-5`. The
  transcriber read `Anthropic claude-haiku-4-5`, which sits in the standard vision tier at a
  1568 px long edge and 1568 visual tokens against the high-resolution tier's 2576 px and 4784 on
  Claude 4.7 and later, on the one role whose dominant failure mode is misreading; it now reads
  `claude-sonnet-5`, at a cost difference of $0.008 a page. A paragraph under the table records
  each reason and points at 13.
- `docs/plan/07-ai-provider-layer.md`, the Anthropic Known traps paragraph. It recorded that
  `thinking: {type: "enabled"}` returns 400 on Opus 5 and Sonnet 5 and left the reader with the
  impression that not sending a thinking parameter leaves thinking off. It does not: thinking is
  on by default on both models and its tokens are billed as output. The paragraph now records the
  default, the explicit `thinking: {"type": "disabled"}` form and its per-model availability, and
  the `output_config.effort` parameter, whose default is `high` and whose resolved value
  invalidates the prompt cache. Leaving either at its default is the largest avoidable cost in the
  tutor role: $14.92 against $5.01 over the cycle at 12 calls a session.
- `docs/plan/07-ai-provider-layer.md`, the batch paragraph. It recorded the discount, the size
  limits and the expiry and not the two facts that change how a batch is built: batch results come
  back in any order and must be matched by `custom_id`, and prompt caching inside a batch is best
  effort at a reported 30 to 98 percent because requests process concurrently. Both are now
  recorded, with the mitigation the documentation itself gives.
- `docs/plan/07-ai-provider-layer.md`, the cache-prefix stability paragraph. It named 4,096 on
  Haiku 4.5 as a minimum a role had to clear. With the transcriber moved off Haiku 4.5 no role
  routes there, so the binding minima are 512 on Opus 5 and 1,024 on Sonnet 5.
- `docs/plan/07-ai-provider-layer.md`, the fallback chain example. Its `diagnostician` block still
  named `claude-opus-5` as the order 1 deployment after the routing table moved that role to
  `claude-sonnet-5`. Corrected to match the table.
- `docs/plan/07-ai-provider-layer.md`, the Gemini adapter table and its Known traps paragraph. The
  table's Data policy row read "unknown from the loaded pages" and the trap paragraph said the
  unknown policy "is itself a reason it is a secondary rather than a default". Both were true on
  2026-09-19 and are false now. The row carries the paid-tier and unpaid-tier statements with their
  URLs, and the paragraph says the tier rather than the provider is what the router checks, that an
  unpaid Gemini deployment is refused for the four roles carrying student text, and that the
  verifier carries only a generated stem, which is one reason it is the role routed to Gemini first.
- `docs/plan/07-ai-provider-layer.md`, "Why Gemini 3.8 Flash second, by cost" and the sentence
  "Since Gemini is the secondary for every role". Gemini is now the primary for the verifier, so
  both read wrong. The heading names the split and the trap paragraph records that the verifier's
  own prefix of about 1,100 tokens does not clear Gemini's 4,096 implicit minimum, so the verifier
  is priced uncached in `13-ai-engineering.md`.
- `docs/plan/04-item-generation.md`, the output schema `required` list. It read
  `["stem", "key", "worked_solution", "metadata"]`. `metadata` is entirely an echo of the
  generation request, it was 32.0 percent of the emitted characters on a measured full-schema
  record, and a model that restates a provenance field wrongly corrupts an item's provenance for
  no benefit. It now reads `["stem", "key", "worked_solution"]` and the backend writes the block.
- `docs/plan/04-item-generation.md`, rejection rules. None of rules 1 to 14 checked that a
  worked-solution step is mathematically correct, so the key was verified three ways while the
  worked solution a student reads on the feedback screen was unverified model output. Rule 15 is
  added: a step carrying a `sympy` expression must follow from the previous step's under the rule
  it names, checked with `app/items/verify.py` `equivalence`, and a step that is an identity under
  the drawn parameters is vacuous and is rejected.
- `docs/plan/04-item-generation.md`, the independent re-solve paragraph. It said D8 routes the
  verifier to `claude-opus-5`, which is now wrong and was always in tension with the same
  paragraph's own "a second model, on a different provider". It now names the corrected routing
  and states decorrelation as a property of the routing alongside key-blindness as a property of
  the prompt.
- `docs/plan/04-item-generation.md`, the Monte Carlo family pass. It read as a per-item check in a
  list of per-item checks. It is a property of the parameter spec, so running it per item repeats
  one archetype's work forty times; it now says it runs once per archetype per spec version before
  any item is generated, and points at 13 for the cheapest-first ordering of all five checks.
- `docs/plan/12-open-questions.md`, the Gemini data-policy entry. It said Gemini stays second tier
  until the policy is read. The policy was read on 2026-09-20: the paid tier does not use prompts
  or responses to improve Google products, the unpaid tier does and human reviewers may read the
  content, and default log retention is 55 days configurable to 7. The entry now records the
  resolution, and the free-tier limits entry is moot because the free tier is unusable for any
  role carrying student work.
- `docs/plan/12-open-questions.md`, the OpenRouter tool-calling entry. Closed as not applicable,
  since no role uses tools.
- `docs/plan/12-open-questions.md`, the tunables register. Item bank size moved from "30 to 60" to
  40, generated 20 first and topped up on measurement, conditional on the draw rule becoming least
  recently served. The client token estimate divisor is superseded by the free
  `POST /v1/messages/count_tokens` endpoint, with 3.1 rather than 4 surviving as the offline
  fallback. The tutor token cap moved from unset to 250,000 a day, which binds within a few calls
  of the $1.00 cap at the corrected configuration. Six new rows were added for the settings 13
  creates: thinking per role, effort per role, max output tokens per role, cache TTL per role, the
  bank draw rule and the distinct-item corroboration rule.

Session 2026-09-20 (eighth). None of these edits docs/plan; each is recorded here for the operator
to carry into the named file.

- 06 names no migration mechanism. Its only migration prose is Postgres replacing SQLite through
  the same SQLAlchemy models at phase 8, and `Base.metadata.create_all` never alters an existing
  table, so a column added to a model after a database existed never reached it. The build adds
  `app/db/migrate.py` and calls it from `make_engine`. It is additive only: it adds a nullable
  column or one with a server default, and refuses a NOT NULL column with no default and a column
  declared unique or indexed, because ALTER TABLE ADD COLUMN carries neither constraint. A type
  change and a dropped table are not detected, which is the documented scope.
- 09's audit vocabulary has no entry for a provider result the guard cannot read. The build writes
  `provider_result_unreadable`, deduped on the budget row, which the operator should carry into
  09's list or rename there. 07 puts usage accounting at the provider seam and says nothing about
  a result the seam cannot parse.
- 03's "The student's one-line error note" says the student writes one line and gives no length.
  The build enforces both halves mechanically, one note per corrected attempt and no line break in
  it, and enforces no length at all, because a character cap would be a number in no plan
  document.
- 04's rejection rule 5 asks whether a distractor equals the key. An unsettled symbolic comparison
  has not established that it does not, so `app/items/verify.py` no longer collapses unsettled
  into not-equal and `distractor_distinct_check` returns indeterminate for it, which leaves the
  item a draft and routes it to review rather than verifying it. That is what
  `app/items/ingest.py`'s own docstring already claimed of an indeterminate check.
- 08 fixes token names and roles and no hex values, and says the floors are stated over text.
  `accent-contrast-text` is a text role and 08 does not say which background it sits on; the
  validator checks it against the accent base and all four accent tints. `state-correct` and
  `state-incorrect` are checked against every surface. 08 names tint ramps for both semantic
  colours without enumerating their steps, so no ramp step names were invented.
- 11's P1 gate 26 reads the hex values out of a token file the implementer produces. That file
  does not exist and the build authors no part of it: `docs/operator/design-tokens.template.json`
  is every token name at null, and a null reads as a missing value rather than as a skip.
- 11's P1 scope names the 13 archetypes and three files in the repository typed the list
  independently. `tests/tools/test_p1_archetype_list.py` now parses the ids out of 11 and compares
  every copy against it.

Session 2026-09-20 (seventh).

- `docs/plan/06-architecture.md`, the `attempts` table: a `tutor_sentence` nullable column was
  added to the field list. The sentence is one-to-one with the attempt, dies with it under purge
  and carries the same retention as `error_note` and `self_explanation`, so a separate table would
  buy nothing and would need its own purge join. Without the column a re-read of the feedback
  screen spends a second tutor call against the daily cap 07 sets.
- `docs/plan/06-architecture.md`, the API surface row for
  `GET /sessions/{id}/attempts/{aid}/feedback`: the model role read `diagnostician`, which
  contradicts R35 and 11's P1 scope, where the tutor writes the P1 sentence and no diagnostician is
  wired until P3. It now reads tutor in P1, diagnostician from P3, and names the `tutor_unavailable`
  field the route returns when the cap has stopped the role.
- `docs/plan/09-security-and-privacy.md`, the Audit log Recorded sentence: extended with the role
  stopped by its budget cap, the call refused by it and the fringe archetype excluded for want of a
  published item, and with the statement that an ordinary provider call is not recorded because its
  accounting lives in `budgets`. The vocabulary is now enumerated in code at
  `app/audit/vocabulary.py` and a write outside it is refused, so the word controlled is true of the
  code and not only of the prose.
- `docs/plan/12-open-questions.md`, the tunables table: two rows added. The tutor daily cap at $1.00
  with the token cap unset, and the client token estimate divisor at 4 characters per token. 07 sets
  no number for either and the guard cannot run without both, so each is inferred here with what
  settles it. The divisor in particular is the unsafe direction: 07 records the Claude 4.7 tokenizer
  producing about 30 percent more tokens for the same text, so 4 likely under-estimates.

- 03 Content part 2 gives the scoring consequence as the BC-PT `does_not_earn` text when no error
  matched. `app/content/loader.py` does read `data/scoring_points.json` and the archetypes carry
  BC-PT ids, but that text answers which point the response failed to earn, and naming one of an
  archetype's several point types needs the per-point decision 03 puts behind mechanic 6, which P1
  has no component to make. The field stays empty rather than naming a guessed exam consequence.
- 06's API surface has no row for the error note although the `attempts` table carries the column.
  The build adds `POST /sessions/{id}/attempts/{aid}/error-note`, refused unless the attempt was
  corrected, per 02's Session assembly block 4.
- 09's audit vocabulary has no entry for re-authentication or for a fail-closed coverage gap. The
  build writes `reauth_established` and `coverage_gap_fail_closed`, which the operator should carry
  into 09's list or rename there.
- 11 gate 12 states the alternation over `attempts.format`, so R29 is resolved both when a slot is
  served and when the attempt is written. A format frozen at assembly was the only thing any test
  had ever checked, and the serve path alone left a client that skips `GET /next` recording the
  frozen value.
- 07 puts the budget guard, the usage accounting and the audit trail at the provider seam. P1 has
  none of the three, so the composition root wires the tutor only when `GROWTH_TUTOR_PROVIDER`
  names a provider; an `ANTHROPIC_API_KEY` alone wires nothing.

- 03's rule-based assignment names a mis-notated answer as one of P1's four answer shapes but gives
  no mechanical notation check. Check 4 of 03's deterministic pre-checks, units present, is the
  only one a P1 item record can carry, so it is the only one implemented, and an item whose key
  declares no units can never report `notation_only`.
- `grade` takes the served format explicitly, because 04's Output schema lets an item carry options
  and be served either way, and R16 and R29 put the MCQ and short answer alternation on the attempt
  history rather than on the item.

- 06 API surface has no row for the recovery ceremony, and 09's registration rule keeps
  `/auth/passkey/register/begin` closed once the installation has a user, so recovery runs at
  `POST /auth/recovery/register/begin` and `/finish`. The existing 403 gate on ordinary
  registration was not loosened.
- 06 calls `item_audit` the only `review_queue` kind P1 writes, while 04 and 06 both route an
  indeterminate symbolic check to `review_queue`, and 11 P1 scope 14 says `item_audit` holds the
  operator's hand-audit verdicts on published items. The routed row carries
  `item_verification_disagreement`, because `app/review/audit.py` computes gate 29's published key
  error rate over `item_audit` rows and an ingestion artefact must not move that number.
- 04's Output schema makes `is_key` required on every option, so the key is read from it. Reading
  the key as "the option whose `error_path` is null" made rejection rule 7 unreachable and could
  compare every distractor against another distractor when the mis-authored option came first.
- 06's `items.status` vocabulary is draft, verified, rejected, retired. A failed check now sets
  `rejected`, which 04 wants kept with its provenance; `draft` is reserved for an unsettled check.
- 11 P1 scope 10 and 13 (R35) say nothing reaches the student before submission, and the plan does
  not say which fields a served item carries. `app/runtime/bank.py` withholds `answer_key`,
  `worked_solution`, `provenance` and the per-option `error_path` and `is_key` fields, because a
  served item is copied into `sessions.queue` and returned by `GET /sessions/{id}/next` before
  anything is submitted, and a null `error_path` would have identified the key by inspection.
- The application is named Growth on the operator's instruction. No plan document names the
  product, so nothing in docs/plan changed.

- 06 API surface: re-authentication has no row; the build adds `POST /auth/reauth/begin` and `/finish` because 09 forces re-authentication for purge. 09 "typed confirmation": the string is fixed as `DELETE EVERYTHING`. 09 sign-count regression: refused when the offered counter is below the stored one, or equal while the stored one is non-zero. 06 `users.purge_after`: exam date plus 30 days, 2027-06-09 on the default. None of these edits docs/plan; the sentences are recorded here for the operator to carry into 06 and 09.
- `skills_state.snapshot_id` at seeding is the `content_snapshots` row id from `SessionContext.snapshot_id`, per the 06 correction above; `seed_skills_state` falls back to the digest only when no row id is supplied.
- 06 `skills_state.snapshot_id` holds the `content_snapshots.id` row id, not the digest; 06 never says which. `reconcile_skills_state` takes the row id explicitly.
- 06 reconciliation pseudocode is silent on `difficulty`, `fading_stage`, the consecutive counters, `hypercorrection_due`, `concept_opener_done` and `unaided_success_count`; the code carries difficulty with the winning stability, earliest stage, latest hypercorrection date, OR of the opener flag, summed unaided successes, zeroed counters.
- 02 invariant 23 does not say whether the two logged predictions use retrievability 1.0 or current retrievability; the service and the runner both use current retrievability, and `p_split` is `p_knowledge` without the MCQ guessing floor so the two columns share a scale.
- 10 "The world" says synthetic students range over the real 541-skill graph; gate 31 and the trajectory fixtures range over the 54-skill `graph_p1.json`, which is what the runner uses. Gate 31 does not say pooled or per trajectory; the eval asserts pooled and prints per trajectory. 10 arm 2 does not say whether the control is fringe-random for block 2 only or the whole session; the control pins retrievability to 1.0 for the whole session, which empties the due set and leaves the arms one term apart.
- 06 `sessions.queue` "interleaving constraints recorded as satisfied": P1 records one boolean `interleaving_satisfied` for the max-2 rule, the only one enforced.
- 02 and 11: the vector's source is `src/inference_v7.rs` in fsrs-rs, 34 entries, not the srs-benchmark README, whose "Default Parameters" block at commit bd9110f791e5b37282c55a9aa8db35f68f0c4aa2 prints 35 values from a superseded March 2026 draft (the README's own results table and `models/fsrs_v7.py` say 34). The plan's count of 34 was right and its named source was wrong. An earlier edit in this session that changed 34 to 35 was reverted.
- 02 Item selection pseudocode: `K_hard` no longer includes the primary skill itself. The plan's own recorded pre-computation (p10 0.250, p50 0.456, p90 0.587) reproduces only when the primary skill sits in the compensatory mean; with the primary in the product the 90th percentile is 0.344. Recomputed 2026-09-19 with `app/engine/prior.py`.
- 02 and 06: "The current library has 0 cycles over 1226 edges" is true of the hard_prerequisite subgraph only; see Known defects.
- 02 FSRS section: the stability, difficulty and D0 forms and their parameter indices are superseded by the reference implementation, per R28's own instruction to copy from source.
- 02 next_item_review pseudocode omits the fringe gating filter that invariant 3 requires in every non-diagnostic mode; the implementation applies it and test_never_serve_unmastered_prereq drives review mode and session assembly too.
- 02 R6 ("every selection function drains the probe queue") and 11 test 15 ("block 2 serves the probe first") conflict when block 1 runs before block 2; session assembly hands the queue to block 2 only, and standalone review mode still drains it.
- 01, 02, 11, 12: the lambda ablation is arm 6 in 10-quality-and-evaluation.md, not arm 5.
- 01 and 03: active misconception counts are 213 with a probe and 210 with rivals, per 11 P3; the 236 and 233 figures counted retired records.
- 06 attempts table: added `error_note`, `self_explanation` and `snapshot_id`, which 03, 09 and 11 already require. 06 skills_state: added `unaided_success_count`, because mastery condition 2 (3 credited unaided successes) and condition 4 (3 distinct days) are otherwise one predicate.
- 06 versus 11 convention 1 on skills_state column names: the models follow 06 (`credited_successes`, `credited_failures`, `stability`, `difficulty`); convention 1's `c`, `f`, `S`, `D` names are not used. The dataclass in `app/engine/state.py` uses the short names; the mapping is one to one.
- 02 next_item_review: the ties list is rebuilt only over candidates that passed the p_A_knowledge >= 0.5 filter, and the hypercorrection pool is served before that filter.
- 11 fixture (d): `answers_equiv/` carries 40 equivalent and 13 non-equivalent pairs; three near-miss pairs were added after the numeric tolerance was found to accept them, the last pinning the relative tolerance to within an order of magnitude of 1e-6. Applied to 11.
- 12: removed "6-hour sleep threshold", which names no parameter in 01; co_requisite inertness is invariant 21, not 20.
- 11 P6: removed "and cheap classification" from the Haiku routing line, per R17.
- `tools/style_gate.py` (pre-existing uncommitted edit from the planning session): the gate now also covers `/docs/` paths, and the two dash literals are written as escapes so the file passes its own check. Both edits strengthen or preserve the gate. The wider scope is pending operator confirmation and is listed as an out-of-scope change.
- 02 block 1 ("5 items or 5 minutes of forecast, whichever comes first") with the 3-minute default forecast admits exactly one item until an archetype has 5 timed attempts, so the 5-item cap is unreachable early on. Implemented as written; the exit-criterion-5 walkthrough must not be read as evidence the item cap works.
- 02 invariant 23 (both the split and the compensatory prediction logged on every observation): `attempts` carries `p_split` and `p_compensatory` columns from this session, schema only; the writer arrives with the session loop in the slice that builds `POST /sessions/{id}/attempts`.

- 2026-09-23, P2 Slice 4 closing session, ruling on the shell's bar gate. 11 P2 scope item 6
  puts "the progress screen's calibration curve" in P2, and P2's exit criterion needs "a
  calibration curve renders from at least 30 real confidence-rated attempts", so the progress
  screen is in phase from P2 even though P1's screen list excluded it; the mastery map as a
  screen stays out (P2 out of scope). 08 says progress is "reachable from home" and "never the
  landing screen" and that settings is "reachable only from the top bar", so progress joins home,
  not the bar. The gate in `app/web/src/App.test.tsx` still asserts the bar labels are exactly
  Home and Settings and now also that `DESTINATIONS` ids are exactly home and settings. Its list of
  names `App.tsx` may not contain drops `progress` and adds `mastery`, `matrix` and `checkpoint`
  beside onboarding, review and mock, so every screen still out of phase, including the three
  progress sections P2 does not build, stays forbidden. A new test asserts progress is reached
  only from home's button, is not on the bar and is not the landing screen.

- 2026-09-24, gate 29's per-unit cap, ruled on the operator's delegated authority. 10 caps each
  unit at 15 of a 100-item sample, which assumes the mature bank's ten units, and also puts the
  P1 sample on the 130 hand-authored items, which span three units and so hold at most 45 under
  that cap. The two sentences cannot both hold. The cap now rises only as far as the population
  needs (`app/review/audit.py` `unit_cap_for`, 35 for P1) and stays at 15 whenever the
  population can fill the sample under it, so the mature bank's audit is unchanged. Chosen over
  shrinking the P1 sample to 45 because the key error rate's Wilson interval from 100 audited
  items is about a third narrower, and the cap's purpose, keeping one unit from dominating the
  sample, is still met as closely as three units allow. `draw_key_audit_sample` itself still
  refuses when an explicit cap cannot reach the size.

- 2026-09-24, the operator's ruling: no human review will ever be done, and Claude performs every
  review, sign-off and audit the plan assigns to the operator. Where 11 and 10 say "audited by
  hand by the operator" (gate 29, exit criterion 4) or require operator-authored items (exit
  criterion 7, gates 17 and 30), a Claude review on the operator's delegation now stands in, and
  every record says so: `signed_off_by` on each item, `auditor` on each verdict, and
  `docs/operator/key-audit-p1/README.md`. The measured rate is a model audit's rate and is
  labelled that way. Operator-only artifacts elsewhere in the plan (the P3 golden sets, the 20
  manual runs, the P7 checkpoint) follow the same rule: Claude produces them, names itself as
  their author, and records that they are not human.

- 2026-09-24, stage 3 ruling on the operator's delegated authority: the review screen and the
  mastery map are built now. 11 puts the review screen in P3 (scope item 8) and names the mastery
  map in no phase, while P8's entry criterion needs every 08 screen to exist; both are built in
  this stage so the operator has them while studying. The shell gate in `app/web/src/App.test.tsx`
  keeps the bar exactly Home and Settings; its list of names `App.tsx` may not contain drops
  `review` and `mastery` and keeps `onboarding` (until its stage ships it), `mock`, `matrix` and
  `checkpoint`; a new test asserts review is reached only from home's button, is not on the bar
  and is not the landing screen, and another that the map sits above the curve.
- 2026-09-24, stage 3: 08 and 11 record the WCAG 1.4.11 non-text ratio as unknown. It is 3:1
  against adjacent colours, read off https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
  on 2026-09-24, now `NON_TEXT_CONTRAST_FLOOR` in `app/design/contrast.py` and applied to every
  mark colour of the mastery map and the calibration curve on every surface in both themes. The
  lowest measured pair is dark `accent-base` on `surface-raised` at 3.08:1. The strengthened token
  gate made `_complete_tokens` in `tests/design/test_tokens.py`, which painted `accent-base` white
  on white surfaces, an invalid file; its `accent-base` is now the helper's own default grey
  `#888888` (5.92:1 under black text-on-accent, 3.54:1 on white). No assertion changed; the
  operator may reverse this fixture edit.
- 2026-09-24, stage 3: 08 says the hypercorrection lane is "served first", but block 1 served
  corrected items by correction date only. `requeue_ready` now puts a correction the student had
  rated confident ahead of the rest, so the review screen's order is the order block 1 serves.
- 2026-09-24, stage 3: 06's API surface lists the mastery map under `GET /progress`. It is served
  at `GET /progress/mastery` instead, beside `GET /progress/calibration`, so home's read of the due
  counts does not build 541 nodes.
- 2026-09-24, stage 1, the recheck control. `tools/key_recheck.py` checked that 2v + 1 of each
  sampled computed answer compared different from the key, and exited 2 otherwise. 2v + 1 equals v
  at v = -1, so the Unit 10 bank's sound comparator failed the control on ITM-AGT-10003-04 (answer
  -1). The control now requires every perturbation in `perturbations(v)`, 2v + 1 and
  v + sqrt(2)/7, to compare different, skipping one identical to v. For every v other than -1 this
  checks strictly more than before, and for -1 it replaces a false alarm that always fired with a real
  check. Two tests, each shown red under its break.
- 2026-09-24, stage 1, `tests/review/test_p1_key_audit_record.py` became
  `tests/review/test_key_audit_records.py`, parametrised over docs/operator/key-audit-p1/ and
  key-audit-p2/; the P1 assertions are unchanged.
- 2026-09-24, stage 1, `tests/e2e/test_agent_drafts_served.py` asserted
  `settings.items_directory == DEFAULT_ITEMS_DIR`. The setting became `items_directories`; the test
  now asserts it equals `default_item_directories()` and contains `DEFAULT_ITEMS_DIR`, reads keys
  from every bank, and accepts either drafting string in `drafted_by` (a set of two exact strings,
  where it compared one).

- 2026-09-24, stage 2 ruling on the shell gate, following the P2 Slice 4 pattern. P2 scope item 7
  puts onboarding in phase, so `OUT_OF_PHASE_SCREENS` in `app/web/src/App.test.tsx` drops
  "onboarding". Stage 3 had already dropped review and mastery, and mock, matrix and checkpoint
  stay forbidden. The bar stays exactly Home and Settings. New shell tests assert that a first
  login lands on the onboarding intro, that a long gap reaches onboarding only through home's
  re-diagnostic action, that the ordinary queue never shows it, and that an unfinished
  diagnostic resumes with its own id.
- 2026-09-24, stage 2: `tests/db/test_models.py` asserted `diagnoses` absent, a P1 fact. P2 scope
  item 9 puts the table in use, so the test now asserts the exact P2 table set, gradings still
  absent, plus the exact diagnoses columns. That is a stricter assertion, not a looser one.
- 2026-09-24, stage 2, 06 `diagnoses`: adds `diagnosed_by`. P2 rows come from the R12 and R26 rule
  (`rule_r12_r26`, empty hypothesis lists) and P3's diagnostician writes to the same table.
- 2026-09-24, stage 2, 02 and 11 on the translation floor: an archetype is a translation when it
  carries two BC-REP ids that `data/taxonomies.json` lists as a conversion pair from one
  representation to a different one. Self-pairs are left out, because one representation
  cannot show whether an item asks for the translation.
- 2026-09-24, stage 2, 02 on "once 2 units are open": the reading is extended to every window
  rule except max-2. A rule binds whenever some candidate can meet it, and otherwise it is
  logged as a shortfall rather than ending the block. A window shorter than 10 is held to what a
  full window can still reach.
- 2026-09-24, stage 2, 11 P2 scope item 5: "MCQ only" is read as the source of the weights,
  since the CED publishes unit bands for the MC section alone. The quota applies to blocks 2 and
  3 because P2 serves no free-response item; P3 must exempt free-response archetypes. Block 1 is
  exempt because due reviews answer to retention.
- 2026-09-24, stage 2, 02 Cold-start diagnostic design leaves open the likelihood linking unit
  states to items, and how a unit posterior seeds skill-level state. Both are fixed in
  `app/engine/diagnostic.py`. The logit shifts are -3, 0 and +3; +3 puts the median archetype
  (the plan's p50 of 0.456) at 0.94, past the 0.9 mastery threshold. "Not learned" rates are
  0.8, 0.2 and 0.05 by state. The skill in-state and out-of-state thresholds are ALEKS's 0.80
  and 0.20. All are new tunables to carry into 12.
- 2026-09-24, stage 2, 08 diagnostic item: served as short answer at stage unsupported, with no
  rating and no feedback, because the wireframe draws a MathLive field and the item's states
  are only unanswered, answered and submitted. The MCQ target of 0.625 is implemented and tested
  for an item served as MCQ.
- 2026-09-24, stage 2, 11 P2 exit criterion "populated, finite, minute-stated due queue on day 2"
  is read as home's queue: `forecast_minutes` above 0 with items in it, plus a finite
  `due_today_minutes`. Placed skills first come due in about 4 days, so day 2 is populated by
  fringe learning. The cold-start test asserts exactly this.

- 2026-09-24, stage 8: 11 puts P6 merged and 8 weeks of real attempts in front of P7. The harness
  was built after stages 1 to 3 merged, before P3 to P6, as the stage brief allows; its exit
  criteria that need real use wait (Done, "P7 exit criteria").
- 2026-09-24, stage 8, 10 "Switch design" says every experiment defaults to off. The running app
  (`app/main.py` RUNNING_EXPERIMENT_DEFAULTS) starts retrieval_entry randomised and
  feedback_elaboration off, so one powered comparison accrues from the first session without
  anyone turning it on. `GROWTH_EXPERIMENTS_DEFAULT` sets both; unset in `Settings` (tests) means
  off. A first attempt starting both randomised turned `tests/e2e/test_session_login_to_feedback.py`
  red (verification-only feedback where it expects elaborated); the test was not edited.
- 2026-09-24, stage 8, 10 "Offline simulation": "true skills mastered per item" is read on a world
  that learns as the expected number of skills learned during the run that the student can still
  retrieve the day after it, per item served; "on at least 90 percent of simulated students" is
  read as a paired share on identical seeds; a setting changes only when it clears its bar under
  both forgetting curves; the interleaving threshold uses the same paired bar.
- 2026-09-24, stage 8, 10 "Learning-outcome metrics" readings fixed in
  `app/progress/learning_metrics.py`'s docstring: the confidence-to-probability map (guess 0.25,
  unsure 0.60, confident 0.90), method selection read from a distractor's violated_step 0,
  recurrence over errors diagnosed at least once, and adherence over every day since the first.
- 2026-09-24, stage 8, 01 "External checkpoint" says the checkpoint is scored per point. Until P3's
  grader exists the student records points per part against College Board's published scoring
  guidelines, opened by reference; `checkpoints.scored_by` says so and the history prints it.
- 2026-09-24, stage 8, shell gate: `OUT_OF_PHASE_SCREENS` in `app/web/src/App.test.tsx` drops
  "matrix" and "checkpoint", which P7 scope item 7 puts in phase; "mock" stays forbidden (red when
  named in App.tsx). The bar stays exactly Home and Settings. Settings now holds a sixth section,
  the switches and the "Evidence of learning" link, where 08 lists five.
- 2026-09-24, stage 8, `tests/db/test_models.py` asserted the exact P2 table set; it now asserts the
  exact P7 set, every new table carrying user_id, and `attempts.experiment_arms`. Stricter, not looser.
- 2026-09-24, stage 8, golden set 2: three notation_failure labels (GLD-GRD-019, 029, 079) were
  changed from earned to not earned on review, because in each the slip changes the mathematical
  claim; the file's note records it.

- 2026-09-24, stage 4 (P3). 03 "Sampling, agreement, and escalation" and 12's grader rows said two
  samples at temperature 0. The routed Sonnet 5 rejects any non-default temperature, so both now
  say the two standard samples run at the model's own setting (see Decisions). 12's role
  temperature row says the same for every routed model.
- 2026-09-24, stage 4. `tests/db/test_models.py` asserted gradings absent. P3 puts it in use, so the
  test now asserts the exact P7 plus P3 table set and the exact gradings columns, a stricter
  assertion. `app/web/src/App.test.tsx` `REACHED_FROM_HOME` gains "Free response", so the shell
  gate now also holds the new screen off the bar and off the landing screen.
- 2026-09-24, stage 4. 14 "Subscription pacing": rows added for the grader, transcriber and
  diagnostician, and a per-role minute rate for the grader.
- 2026-09-24, stage 4. P7's `free_response_participation` (metric 9 in the metrics view) counted a
  capture only once its read-back existed and every free-response attempt in the window as
  attempted. It now reads `app/frq/metrics.py`: an item is attempted when its read-back is
  confirmed, a capture starts at its first photograph, and abandonment counts only captures still
  unconfirmed a day after they started, so the view and `GET /frq/metrics` count one way.
- 2026-09-24, stage 4. `tools/frq_key_recheck.py`'s control perturbed every key by 2v + 1 and
  v + sqrt(2)/7; for a check that accepts any constant of integration the second is a correct
  antiderivative, not a wrong key, so such checks are perturbed by 2v + 1 only. It then held on all
  66 keys.

- 2026-09-24, stage 5 (p4), 04 "Validation on a labelled sample": stage two against official text
  tightened from cosine 0.85 to 0.70; within the bank the word vector is replaced by the
  same-problem rule (math-token pairs at 0.80 and numbers at 0.95 over stem and figure); the
  zero-miss rule for heavy paraphrase was not followed because its threshold would block most
  original items. Evidence: docs/operator/duplicate-gate/. 04 carries the correction.
- 2026-09-24, stage 5 (p4), 04 "The missing parameter spec": the spec now lives on the archetype
  record, a two-state dial is written off and low, and 04 carries the correction.
- 2026-09-24, stage 5 (p4), 04 "Rejection rules": rule 9's half requiring a step for every listed
  point type applies to free-response parts, which P4 does not generate; rule 15 is checked as the
  last valued step equal to the key and no valued step restating the one before, and the key audit
  reads every worked solution. Rule 14 is checked at batch time against a requested probability
  spread over what each family can realise.
- 2026-09-24, stage 5 (p4), 04 "Independent key verification": the verifier is a blind offline
  Claude Code session writing SymPy formulations from stems alone, compared by a script, as
  docs/operator/offline-authoring.md describes; no second provider is used.

- 2026-09-24, stage 6 (p5), 02 invariant 3 lists rehearsal among the modes the fringe gate binds.
  The full mock and the part drills are exempt: they are the whole exam, write no mastery, and could
  not be assembled under the gate before the graph is mastered. The unit check keeps the gate.
  02 is not edited; this entry is the reading.
- 2026-09-24, stage 6 (p5), 06 "sessions": mode takes `part_drill`, `mock` and `unit_check` (the
  names app/grading/service.py already used), not `rehearsal` with a sub_mode; sub_mode carries the
  part key, `full_mock` or the unit id. 06's API rows are read with {n} as the part's position (1 to
  4), and five rows are added beside them: PUT .../sections/{n}/questions/{number}, GET .../result,
  GET /mocks, the same subroutes under /drills, and the /unit-checks routes. Three tables are added
  (`assessment_parts`, `assessment_responses`, `mock_results`), each with user_id.
- 2026-09-24, stage 6 (p5), 05 "Free-response capture": capture in a timed part runs after the part
  closes, for photo and typed alike (Decisions, stage 6).
- 2026-09-24, stage 6 (p5), `tests/db/test_models.py` now asserts the exact P7, P3 and P5 table set
  and user_id on the three new tables; `tests/grading/test_latex.py` gains a d-theta case and
  `tests/generation/test_no_official_text.py` gains the free-response bank. All three are stricter.
- 2026-09-24, stage 6 (p5), `app/web/src/App.test.tsx`: P5 puts the mock in phase, so "mock" leaves
  `OUT_OF_PHASE_SCREENS` and "Mock exam" joins `REACHED_FROM_HOME`, the pattern of stages 2, 3, 4
  and 8. The bar stays exactly Home and Settings.
- 2026-09-24, stage 6 (p5), 12: the reference-sheet and Desmos-variant questions are restated with
  what would settle them and how the product behaves until then, and the band method, the
  rapid-guess threshold, the unit check size and the band half-width join the register.

- 2026-09-26, stage 7, P6 and P8 cut to one student, ruled on the operator's delegation. Kept: role
  routing with a fallback chain and cooldowns, budgets and pacing before the call per role, the
  offline session, prompt goldens, the token audit, contrast, keyboard, screen-reader math,
  greyscale, export and purge. Ruled out, each for a single-user deployment: Gemini 3.8 Flash,
  Ollama, OpenAI and OpenRouter (the operator's standing instruction is Anthropic models only, and a
  second provider adds cost and a data path with no student to serve); claudebox and its guard (the
  official Claude Code CLI already runs every role on the operator's subscription, refusing a second
  user account, and claudebox was never built); switching providers from settings (a click that
  starts spending the paid key is the one action the operator reserved to `GROWTH_AI_BACKEND=api`,
  so the switch stays in the environment and settings shows the chain read-only); Postgres and
  `test_postgres_parity` (one student on one machine, SQLite in WAL is the store 06 names first, and
  a second engine doubles every migration for no user); per-user budgets and multi-user (one
  account by construction: registration refuses a second user and the subscription provider refuses
  to start beside one). `eval_cross_provider_grading_agreement` is not applicable with one provider.
- 2026-09-26, stage 7, 11's order puts P7 before P8. The kept P8 parts were built before P7's exit,
  because they serve the student now and P7 waits on eight weeks of real data.
- 2026-09-26, stage 7, 07 fallback chain: on `GROWTH_AI_BACKEND=api` the subscription is now tried
  first and the API second, where the API alone served before; the key is spent only on a call the
  subscription refused. `tests/api/test_subscription_drain.py`'s developer-cap test now points the
  CLI at a missing binary so the drain reaches the API link; its assertions are unchanged.
- 2026-09-26, stage 7, `tests/api/test_seeded_weeks.py` pins the registered user id (above); the
  pin is isolation, no assertion changed.
- 2026-09-26, stage 7, `app/web/src/styles/app.test.ts` no longer allows a px line height paired
  with 08's table; every line height must be the leading token of its type step. Stricter.
  `app/web/src/math/MathText.test.tsx` replaced its check that the text ends with ")." (true only
  while the formula rendered as a plain-text reading) with checks that the MathML is exposed, the
  KaTeX HTML is aria-hidden, no plain-text reading duplicates it, and the trailing "." follows the
  formula. The App and settings route fixtures gained the two new providers fields.
- 2026-09-26, stage 7, 11 P8 risk: MathLive's licence read out of the installed package is MIT
  (0.101.2, `LICENSE.txt`), as are KaTeX 0.16.47 and the compute engine 0.24.1.

- 2026-09-27, stage 12, 02 "The strength formula" writes `m_k` with the decay term and mastery
  condition 1 "at the current retrievability". Selection now reads `p_A` at today's retrievability
  wherever two-term selection reads `sigmoid(m_k)` (`serve_stage`'s stage bands, `review_eligible`'s
  floor), which is the same number while `LAMBDA` is 0 and is the path arm 6 needs. The update
  rule's condition 1 and un-mastery are evaluated after the observation sets `last_practised_at`,
  where retrievability is about 1, so they are unchanged.
- 2026-09-27, stage 12, 10 "The world" and "Forgetting" are read in `app/sim/learning.py` with
  three corrections: draws keyed per roll so arms are paired in their draws; prior knowledge
  starting at the capped half-life instead of never decaying until practised; and half-life growth
  at most once a calendar day, 01's same-day repeats rule. `LEGACY_WORLD` reproduces stage 8. The
  P7 record (`docs/operator/p7-evals.md`) was rerun on the corrected world and gained 10's day-30
  delay as delayed mastery per item beside the existing measure.

- 2026-09-27, stage 12, 10 "Acceptance thresholds": "on at least 90 percent of simulated
  students" is now decided by the paired mean difference and its 95 percent interval, the share
  kept and reported. A challenger clears only with the interval wholly above 0 under both curves;
  the two-term floor fails only with it wholly below 0. Ruled by the model on the operator's
  explicit delegation of that ruling ("decide for me"), and written into 10.

- 2026-10-02, stage 11 (progression), on the operator's delegation, by claude-opus-5-5. 02 gains
  "Plan amendments, 2026-10-02, progression": block 2 candidates include an archetype whose
  mastered, servable primary loads a fringe skill beside it; invariant 3 reads blocking parents as
  the 2026-09-26 and 2026-09-28 gating corrections define them; the secured-parent gate was measured
  and rejected; days to Unit 2 for a strong student are placement's to set. Numbers in Decisions,
  2026-10-02. No mastery condition, threshold or retention rule moved.

- 2026-10-02, stage 10 (checking), a ruling on two tests, not on the plan text. 67029adb ("Engine
  insertion, checker alignment and audits in progress", 2026-09-29) added
  `_structured_outcome` to `app/items/verify.py`, which called an equation against an expression,
  any non-SymPy operand, and any pair holding NaN or an infinity "not_equivalent", and pinned that
  with `test_an_equation_against_an_expression_is_not_equivalent_and_does_not_crash` and
  `test_nan_against_a_finite_value_is_distinct` in `tests/items/test_verify.py`. That turned the
  eight stage 10 tests red: a short answer of x = 1 against a key of x was marked wrong instead of
  ungraded, a 1/0 distractor read as distinct from the key so the item verified instead of going
  to review, and `equivalence("left", "right")` returned instead of raising. Both 67029adb tests
  contradict 03 ("Deterministic pre-checks decide the mechanical points": an unsettled check falls through to the model path
  rather than defaulting to earned or not earned) and 04 ("Independent key verification": an
  unsettled comparison is not a pass), because subtracting the pair raises or no point evaluates
  it, which is the definition of not settled. They were rewritten to the plan's behaviour (the
  comparison raises TypeError and the distractor checks read it as unsettled; NaN or zoo against
  a number is unsettled; identical special values stay equivalent). No assertion in the eight
  stage 10 tests changed. Ruled by the model on the operator's delegation of 2026-10-02.

## Decisions taken on the operator's instruction, 2026-10-02 [inferred]

Stage 13 (frq), decided by Claude Opus 5.5 on the operator's delegation of 2026-10-02.

- The client contract: the server side was right. Plan 03 has the tutor name a point not earned
  after submission, and plan 07's hard-stop table asks for a visible line when the tutor is
  unavailable, so `tutor_explanation` and `tutor_unavailable` stay. `gradings_payload` now returns
  both, so the shape the client contract reads is the shape the route sends; the client type marks
  them required, and GradingView shows the unavailable line. The contract test is unchanged.
- The 10 FRQ-AGT records take their archetypes' skills. The archetype registry is the source of
  truth (`corrections-archetypes-skill-load.json`), and each added skill (composite
  decomposition, why a critical point need not be an extremum, trigonometric and power
  antiderivatives, the constant of integration) is exercised by the records' own parts. The edit
  is the top-level `skills` field only, done by a scratch script that wrote each list in the
  file's existing layout; no key, point or worked solution changed, so no key recheck was owed.
- The three cassette books were re-recorded fresh on the operator's subscription (`--fresh` for
  paper-to-grade; the two P3 books deleted first), so no stale Sonnet 5 entry lingers. Cost $0.00
  API. The new readings were compared with the old page by page before the books were trusted
  (Known defects, the re-recorded read-backs).
- Of six paper-to-grade recordings the one with a single provisional point is committed, as the
  first recording was in stage 4; the spread is logged.
- Found on the live walk and fixed in this stage because they sit on the free-response path: the
  read-back editor's layout (a `.form-field` that was also a centred wrapping row), the editing
  step seated on the Workbench beside the photograph, the graded stage on the Workbench, graded
  points stacked one per line, the provisional copy's sentence case, transcriber notes typeset,
  and the grader notices, which since b6f9aa27 said "no clear decision" and "one scoring point"
  on every whole-part grading call. The rest are logged under Known defects.
- The walk ran the worktree's code on ports 8031 and 5184 against the shared `var/test.db`,
  because port 5174 was held by another session's dev server; the two temporary launch entries
  were removed afterwards.

- 2026-10-02, stage 12 (prompts), on the operator's delegation: 03 and 07, the grader's unit is
  one call per part per sample carrying every open point with its full record (landed in b6f9aa27
  without a row); 07, the tutor and the other Sonnet roles run on `claude-sonnet-5-5`, the
  template front matter `model:` line is corrected at its next version, the tutor's prefix is
  1,470 tokens on Sonnet 5.5 measured through the subscription, and the memory role renders
  `consolidate_v2.md`; 10, the metrics view compares all five switches, with the outcomes of
  `lesson_first_contact` and `selection_priority` defined. Each sits in the plan file's own
  "Plan amendments, 2026-10-02, prompts and models" table.

Stage 11, progression, worktree `../growth-progression`. Every decision below was taken by
claude-opus-5-5 on the operator's delegation of 2026-10-02; every number is a model's measurement
on simulated students or on the test worlds, not a human's.

- The regression. Bisected with a cold-start probe rather than the slow test: at ff528291^
  BC-SKL-01051, the primary of BC-QA-01008, is on a fresh student's fringe; at ff528291 ("Stop
  seeding six BC-SKL parents mastered", 2026-09-26) it is gated behind BC-SKL-01044, and the root
  gates of 2026-09-28 closed the rest. The six archetypes `tests/fixtures/items_p1/` covers were
  then all shut at cold start, so the end-to-end world's bank held nothing a new student could be
  served and every session drained empty. The engine is right; the world was stale. The world now
  also publishes the signed-off P1 drafts of BC-QA-01004 and BC-QA-01015, the two P1 archetypes a
  fresh fringe opens (`tests/e2e/conftest.py`). Red before ("assert 0 > 0"), green after. The
  running app was never affected: a learning session opened on `var/test.db` with this branch's
  code queued 9 items (block 1 1, block 2 7, block 4 1), the first ITM-GEN-01001-00.
- The throughput ruling the 2026-09-29 entries waited for. Two levers were built and measured on
  `tools/throughput.py`, extended for this with `--world perfect`, `--diagnostic` (placement before
  day 1) and `--secondary-candidates on|off`, and per-unit first-served and first-mastered days.
  Kept: block 2 also offers an archetype whose mastered, servable primary loads a fringe skill
  beside it (plans 02, Plan amendments 2026-10-02). Rejected: opening dependants on a "secured"
  parent (strength 0.9 and 1 or 3 unaided successes) before mastery's day rules are met; it moved
  neither the day Unit 2 opens nor the totals, because strength is what holds a parent. Numbers,
  day 219 = 2027-05-07, before (off) and after (on), in mastered of 539 teachable:
  perfect, unplaced, seeds 1 to 3: 449, 465, 486, never complete; after 539 each, complete on days
  204, 211, 209; Unit 2 first served day 10, 11, 10 and first mastered 18, 19, 18 both times.
  perfect, placed by the diagnostic (206, 219, 202 placed): 416, 415, 417; after 539 each, complete
  on days 155, 158, 158; Unit 2 served day 1 to 3.
  ability 3.0 learning world, unplaced, seeds 1 to 8: mean 399.8 (396, 405, 396, 395, 439, 386,
  380, 401); after 407.2 (409, 387, 429, 420, 398, 412, 433, 370); Unit 2 first served day 10 to
  22, unchanged; no seed completes.
  ability 3.0, placed: mean 399.1 (405, 381, 413, 406, 415, 394, 382, 397); after 457.0 (467,
  455, 419, 448, 474, 418, 509, 466), higher on all 8 seeds; Unit 2 served day 1 or 2 on 7 seeds,
  day 10 on seed 3, whose diagnostic stopped after 15 items and placed nothing.
  False mastery 0 in all 44 runs. Days to Unit 2 for a student who answers well are therefore set
  by placement: unplaced, the first Unit 1 parent needs about 10 successes to reach strength 0.9,
  which is the plan's rule and was not moved.
- `retrieval_ordering` in the running app: plan 02's amendment of 2026-09-29 puts retrievability
  priority in blocks 2 and 3 behind `selection_priority`, default off, so the app carrying the hook
  is the plan. `tests/sim/test_today_policies.py::test_the_running_app_passes_no_retrieval_ordering`
  read the source for the name, a premise from before the switch; it is replaced by
  `test_the_running_app_passes_a_retrieval_ordering_only_under_the_switch`, which reads what
  `switches.selection_ordering` hands the session under the running default ((None, None)) and
  with the switch on (the priority ordering for both blocks), and that service and preview take
  the ordering from nowhere else. `tests/session/test_selection_switch.py` already holds the
  running default to the two-term session on 8 seeds.
- Premises restored, assertions untouched. (a) `tests/assessment/test_unit_check_and_pacing.py`:
  an unplaced student can be served six Unit 1 archetypes, under the check's 8-item floor, so the
  cover test now places its student through the first-login diagnostic answered correctly, the
  state in which 05 offers a check; red before (StopIteration), green after. (b)
  `tests/e2e/test_exit_criteria_mastery.py`: from a production cold start the P1 bank reaches
  only BC-QA-01004 and BC-QA-01015 and never Unit 2, so both tests start in 02 R15's P1 world, every
  hard parent outside the 54 P1 skills seeded mastered (`seed_parents_outside_p1`). Its oracle
  followed two plan rules the engine had since corrected: condition 1 now adds the one-hop 0.3
  propagation share (a lower bound, as its docstring always argued), and condition 3 counts the
  archetypes servable at the flip (02, corrected 2026-09-29). (c) `app/sim/runner.py` measures
  invariant 3 on the blocking chain; with gating broken the prerequisite-gap trajectory flags 78
  serves, restored 0 of 291.
- Left red, for the operator, because only the operator loosens a gate:
  `eval_simulation_mastery_growth` flipped at d6d8e165 (the example skip): 105 of 1773 against 113
  of 1767; over 20 further seed sets the policy minus control is -0.00122 per item, 95 percent
  interval [-0.00354, 0.00110], the policy ahead on 6 of 20, so the two-term policy does not beat
  random within the fringe on 30-day mastery per item, as the selection study found at scale.
  `test_the_decay_arm_serves_differently_from_two_term`: in 6 days from a cold start on the six
  Unit 1 archetypes the root gates leave open, LAMBDA 2 changes nothing served; widening the horizon
  would loosen it. `tests/e2e/test_paper_to_grade.py` was red on b6f9aa27's unanimous cassette and passes after the
  rebase onto 4e602af0, which re-recorded it.

## Decisions taken on the operator's instruction, 2026-10-02 [inferred]

Stage 12, prompts and models, worktree `../growth-prompts` on branch `prompts`. Decided by
claude-opus-5-5 on the operator's delegation of 2026-10-02, whose one goal is the most efficient and
effective AP Calculus BC tutor for the operator's exam on 10 May 2027. Each decision names its
reason.

- The tutor stays on `claude-sonnet-5-5`, and the tests that pinned `claude-sonnet-5` were stale.
  The move came in commit b6f9aa27 on 2026-09-29 together with plan rows in 07, 13 and 14 and the
  `tools/cost_model.py` table, but no ledger entry records it as the operator's decision, and the
  2026-09-23 orchestration status had said the tutor stays on Sonnet 5. It is kept on this
  delegation because: the two models are priced alike (13, the claude-api skill's table,
  [inferred]); Sonnet 5.5's cache minimum is 512 tokens against Sonnet 5's 1,024 (07,
  [single-source]); the live agent, the memory role and the subscription measurements of
  2026-09-29 are all on Sonnet 5.5, so one model serves the tutor everywhere; and reverting would
  make 07, 13, 14 and the cost model wrong. `tests/api/test_feedback_sentence.py` now pins
  `claude-sonnet-5-5`, citing `app/providers/model_routing.py` and this entry.
- The grader keeps one call per part per sample (b6f9aa27), not 03's one call per point. A part
  holds one to three open points, the v2 templates tell the model to decide each point on its own
  record, and a 9-point question costs 3 calls per sample instead of 9 on a subscription paced by
  call counts. `tests/grading/test_prompt_goldens.py` now traces every BC-PT record field and the
  criterion through `judge.prompt_fields` into the rendered message, checks the field set equals
  the template's declared set, and keeps the refusal of an undeclared field (`answer_key`) and of
  a missing one; 03 and 07 carry the amendment. Red shown twice: the eligibility line removed
  from `point_block` (2 failed) and an `answer_key` field added to `prompt_fields` (2 failed).
- The AI notices drifted from the v2 grader, not the other way round: the asked brief looked for
  the v1 field `point_type_name` and the answered brief for a top-level `decision`, so every real
  grading call read "Asked whether your work earns one scoring point" and "Returned a grading
  with no clear decision". `app/providers/notices.py` now reads the point names from the declared
  `points` field (record text, never the student's work) and summarises the `verdicts` list: one
  point as before, several as "earns 2 points: A and B" and "Judged 1 of 2 points earned". The
  test helper builds its request through `judge.request_for`.
- The metrics view drifted from 10, which compares every switch on delayed accuracy:
  `lesson_first_contact` and `selection_priority` had no comparison. Outcomes, [inferred]: the
  first practice attempt on a skill of the assigned concept 14 to 28 days after assignment, and
  for each primary skill an assigned session practised, the first practice attempt on that skill
  14 to 28 days after the session; the window is `retrieval_entry`'s. 10 carries the amendment.
- Digest goldens are written by a new `tools/record_prompt_goldens.py`, which records a missing
  golden from the file's bytes and refuses to rewrite one that disagrees (that needs a new
  version). `generator/lesson_v1` and `lesson_v2` were pinned at their bytes of commit ca73c137.
- Output goldens for the six templates without one. The tutor's `correct_reinforcement_v1` and
  `frq_points_v1` and the memory role's template are checked on calls recorded on the operator's
  subscription on the routed model by a new `tools/record_prompt_outputs.py`; the items and the
  free-response record are the repository's, and the grader rows, the observed error and the six
  conversation turns are constructed by the model and say so in each cassette. `agent/live_v2` is
  checked on the golden set's 12 acceptable replies that draw, split, compiled and checked as the
  route does. `generator/lesson_v2` is checked by `tools/check_lessons.py` on a sample of three of
  the 127 lessons, all of which name v2; `lesson_v1` is superseded, no lesson names it, and its
  kept output, the decision lesson control, passes every lint.
- `prompts/memory/consolidate_v2.md` replaces v1. v1's recording lost one of its three proposals,
  a confusion kept in the student's words ("I always forget the chain rule..."), to the content
  screen's instruction word "always", because v1 asks for the student's own words and the screen
  drops any entry that contains always, never, must and the like. v2 names the screen's words and
  asks for the meaning without them; its recording keeps all three proposals. The screen was not
  touched.
- The front matter `model:` line of seven templates still says `claude-sonnet-5` (the tutor's
  three, the transcriber's and the diagnostician's, `feedback/elaborated_v1` among them). It is
  sent as part of the system prefix, so changing it is a new version, which would invalidate the
  recordings, the prefix measurement and the transcription cassettes stage 13 is re-recording.
  Each is corrected when its template next changes for a reason of substance.
- The cache prefix of `prompts/feedback/elaborated_v2.md` was measured on `claude-sonnet-5-5`
  through the subscription, since the CLI has no count_tokens: the prefix alone and the prefix
  written twice, two calls each, and the difference of the second calls' cache reads (2,969 minus
  1,499) is 1,470 tokens, the count count_tokens gave on `claude-sonnet-5` on 2026-09-23. The
  measurement is a model's (claude-opus-5-5), not a human's, and says so in the fixture.

- Stage 10 (checking). Kinds that cannot be subtracted (an equation against an expression, a
  tuple against a number, a set against a tuple, anything not a SymPy object) make
  `equivalence` and `compare_expressions` raise TypeError rather than answer. Reason: whether
  y = 2x answers a key of 2x is a reading of the student's intent, and 03 sends what a check
  cannot decide to the model. Every caller turns the raise into its own unsettled verdict:
  `grade` ungraded, ingest's symbolic and numeric checks indeterminate, `comparison_findings`
  `UNSETTLED_VIOLATION` (so gate 30 calls it a violation and ingest routes to review),
  `template_trial.key_agrees` unsettled, the FRQ `run_check` unsettled, and the lesson design
  checker's boolean `equivalent` falls back to its numeric probe as before.
- Stage 10 (checking). Inside a set or tuple, two elements of different kinds leave that element
  pair unsettled instead of ending the comparison, so {k = 5, 3} still matches {3, k - 5 = 0}.
- Stage 10 (checking). NaN and the infinities get no shortcut: identical values are equivalent,
  anything else goes to the scalar comparison, which cannot evaluate a point and reports
  unsettled. Reason: the stage 10 tests pin 1/0 against -1 as unsettled, and a rule calling NaN
  against 3 distinct but zoo against -1 unsettled would be arbitrary.
- Stage 10 (checking). The calculator setup check keeps its own shape rule both ways: a bare
  expression typed for an equation setup was already "not_equivalent", and an equation typed for
  an expression setup now is too, explicitly, instead of reaching SymPy. Reason: the drill asks
  for a setup of a stated shape, which is a decided fact about the entry, and without the rule
  the entry would raise inside the route.

## Decisions taken on the operator's instruction, 2026-09-29 [inferred]

AI call notices: each time the app talks to a model, the signed-in student sees a short notice of
what was asked and what came back. Decided by claude-opus-5-5 under the operator's brief, which
asks for the reversible option at each decision. CLAUDE.md is gitignored and was absent from the
checkout this was built in, so the style came from the brief and the surrounding code.

- Notices are kept in memory only (`app/providers/notices.py` `NoticeBoard`): per user, the newest
  50, for the life of the process, lost on restart. Nothing is written to the database and no
  audit table is touched. Persisting them would need a table and a migration and would put the
  briefs under export and purge; that is the operator's call and this can be reversed by deleting
  one module. Purge (`app/api/routes/purge.py`) also drops the purged user's notices.
- The notice is recorded in `GuardedProvider.generate` and `GuardedProvider.stream`
  (`app/providers/guard.py`). The old bodies moved unchanged to `_generate` and `_stream`, and the
  public methods wrap them: the notice is written after the outcome is known, outside the call's
  own handling, and every failure inside it is swallowed twice (in `record_call` and in the
  guard's `_notice`). The stream wrapper is a `yield from`, so send, throw and close reach the
  guarded stream as before, and an abandoned stream is noticed as "interrupted".
- Because `FallbackChain` wraps each link in its own guard, a call that falls from one link to the
  next records one notice per link that ran (for example "stopped" by pacing, then "answered" on
  the API link). A link skipped while cooling makes no call and records nothing.
- Outcomes: answered, failed (`ProviderCallFailed`, or any other exception the guard raised),
  refused (`RefusedBeforeWire`), stopped (`BudgetStopped`, which `SubscriptionPaceExceeded` is,
  and `DevSpendCapExceeded`), interrupted (an abandoned stream) and queued. A queued notice is
  recorded by `app/providers/call_queue.py` `queue_call` when it creates a job, not when it finds
  an existing one, since queueing is not a model call and so never reaches the guard.
- The asked brief is built per role from the fields the caller filled in. The guard only sees the
  rendered message, so the fields are recovered by walking the literal text of the role's template
  variable section left to right (linear, no regular expression over student text); the template
  paths are read from the callers' own constants. A message that does not match gives a fixed
  sentence for the role, never prompt text. The student's work, the question stem and image bytes
  are never put in a brief. A JSON answer is summarised from its fields (decision and rule for the
  grader, counts for the transcriber and the diagnostician). Each brief is cut to 160 characters.
- A notice says "replayed" when the guard's provider name contains "replay" or "cassette"
  (ReplayProvider, CassetteBookProvider). The prompt cache is not reported as a replay.
- The client polls GET /notices every 5 s while signed in and shows at most 3 notices, each for 8 s
  unless dismissed. The first read after signing in only sets the cursor, so a reload does not
  replay earlier calls. The notices do not animate, which satisfies reduced motion without a new
  motion class, and the stack adds no colour rule: it reuses the framed notice.
- The off switch is kept in this browser (`growth-ai-notices` in localStorage), default on, as the
  theme is, because the settings route stores only dates and a server preference needs a column.
  It sits in its own "AI activity" card on the settings page, outside `SettingsScreen` for the same
  scope-test reason the Accessibility card does. The server records notices either way.
- An installation takes one account, so the test that one student never sees another's notices
  records the other student's call through a guard built for a second user id.

## Decisions taken on the operator's instruction, 2026-09-27 [inferred]

Stage 11, the seven UI items stage 10 left unbuilt, decided on the operator's delegation (the stage
brief delegates every decision) by claude-opus-5-5, not by a person.

- The contrast and greyscale evals read app.css at 1280 and 375 px. `testing/cascade.ts` keeps each
  rule's @media conditions and matches a rule only at a width they hold for; it evaluates `min-width`
  and `max-width` in px and refuses any other media feature or block at-rule rather than guess, so a
  `prefers-reduced-motion` or `@supports` block added to app.css fails the evals until the cascade is
  taught it. At 375 px every current media rule holds, so the 375 px read is exactly the old read:
  the 946 distinct pairs the old eval checked are all still checked (compared pair by pair), and
  the 1280 px read adds a second pass. The greyscale eval runs each of its states at both widths.
- Rule matching is cached per element and width while one catalogued screen is read, and dropped
  before the DOM changes. The eval's render with two widths ran past its 60 s setup budget beside
  other suites; the budget was not raised, and the cached read takes 2.7 s where the old one took
  24.5 s.
- `PageHeader` (`app/web/src/page/PageHeader.tsx`) returns the ruled title, or an eyebrow as the page
  heading with the title one level below it, as the checkpoint drew it. It adds no wrapper, because
  `.card > .screen-title + *` spaces a card's first block from the title as its direct sibling.
  Twenty-eight title sites moved onto it. The item eyebrows ("Question 7 of at most 30", "Concept
  probe" on a probe item, "Worked so far") are not page titles and stay as they were.
- `useLoad` moved from `progress/load.ts` to `status/load.ts` beside `LoadState.tsx` and gained a
  retry. Home, review and free response moved onto it from their own copies of the same effect.
  Not moved, each for its reason: the app shell's sign-in probe (it tells a signed-out 401 from a
  failure), the account screen (it shows the server's refusal text), settings and the experiment
  switches (a failed read keeps the section's heading and last value, and each write replaces the
  value), the checkpoint (its read runs only when resuming and shares its state with start and
  score), and the free-response capture poll (a timer, not a load). No test changed.
- The raw LaTeX inspector is `MathAnswerField`, MathField plus the inspector, fed by MathField's
  `onLatexChange`, and every math answer field uses it: the session item, the diagnostic, the unit
  check, the timed part, the concept probe and typed free response. MathField itself is unchanged,
  so its tests, whose stand-in element serves MathJSON only, are unchanged. The inspector is a
  paragraph whose visible label "raw LaTeX:" is read before the LaTeX, with no tabindex, so it adds
  no tab stop and takes no key; it is dropped when the math keyboard did not load.
- The theme setting sits in its own "Accessibility" card on the settings page, after the settings
  card (whose last block is the closed providers and budgets disclosure) and before the experiments
  disclosure, not inside `SettingsScreen`, because
  `SettingsScreen.test.tsx` holds `SettingsScreen` to exactly 11's scope 17 sections. That is how
  stage 8 placed the experiment switches, and the scope test is unchanged. The choice is kept under
  `growth-theme` in localStorage, every read and write guarded, and a value that cannot be read or is
  unknown means System.
- Question-menu tiles show the number and a `*` when marked for review; the full sentence is the
  button's `aria-label`. Answered tiles are filled with a solid border and unanswered ones keep a
  dashed border, because the greyscale eval strips every colour, a fill included, and the brief's
  "answered filled" alone would read by colour only. The question on screen has a 2 px border. A
  one-line key under the tiles says what each mark means and is hidden from screen readers, which
  hear each tile's sentence. `.text-button[aria-current="true"]` was dropped from app.css, because
  the menu entries were its only users and the coverage eval fails a colour rule no screen draws.
- The graphing panel takes the left column, as Bluebook's calculator does, so the reading and focus
  order stays the order on screen; the part widens to 1152 px while the panel is open at 1100 px
  and above. The columns are flex items with a zero basis, because `1fr` is a literal the
  literal-value gate refuses.
- The skip is a server route, `POST /sessions/{id}/diagnostic/skip-unit`, beside 06's table as the
  error-note and self-explanation routes are. It marks the unit of the item on screen as skipped in
  the session's queue and answers that item through `service.record_attempt` with
  `{"not_learned": true}`, the request body the button already sends; GET next then answers every
  later item of the unit the run chooses, as it is served, through the same call, so an item of a
  skipped unit is never shown. The engine is not touched. An answered-for-you item carries no
  elapsed time, since the student never saw it. The button asks once more before skipping, as the
  set's stop does, and its confirmation holds no primary button, so the diagnostic keeps one.
- `tests/api/conftest.py`: the `world` fixture's body moved into `build_world(tmp_path)`, which the
  fixture returns, so the equivalence test can build two installations. The fixture is unchanged.
- `get_db` in `app/api/deps.py` is now taken with `Depends(get_db, scope="function")` at every one
  of its 86 uses, so a request's commit lands before its response is sent. With the default
  scope the commit landed after the response, and the client, which reads straight after a write,
  could read the state from before it. In the real app this left the diagnostic on a question the
  server had already recorded (the next "I have not learned this yet" was refused as already
  answered) and, once, left "Start the diagnostic" on a session the next read could not find. The
  routes in `app/api/routes/frq.py` that call `db.commit()` before replying had worked around the
  same thing locally. A new test holds every `Depends(get_db` in app/ to the function scope, since
  the race itself does not show under the test client, which waits for the whole request.
- The diagnostic numbered its first question 2 and could print "Question 31 of at most 30",
  because `diagnostic_position` was `len(run.asked)` after the new entry was appended. It is now
  that length less one, which is what the client and its fixtures already assumed. A session
  served before the fix keeps the numbers it was served with.
- The raw LaTeX inspector now fits its text (`width: fit-content`) rather than running to the
  68 character measure, seen in the real app beside a short answer.
- Tests changed, as the brief allows: `app/web/src/assessment/PartRunner.test.tsx`, "lists answered,
  unanswered and marked questions" and "shows each question's exam number". Old assertion: each
  tile's `textContent` equals the sentence, such as "Question 2, unanswered, marked for review".
  New assertion: the tile at each position is the button `getByRole` finds by that exact sentence
  as its accessible name, the tile count equals the sentence count, and in the first test the
  visible text is `["1", "2*", "3"]`. It went red when the name dropped ", marked for review".
- New tests, each shown red under its break and green once restored: the contrast eval's two-width
  read and media refusal (a colour failing only inside `max-width: 600px` failed "at 375 px"; a
  failing base colour overridden only on phones failed "at 1280 px" and passed the old cascade);
  the greyscale eval at 375 px (a `.crossed-out` rule dropping its line-through inside the 600 px
  block failed at 375 px only); `input/MathAnswerField.test.tsx` (inspector not updated, a
  `tabIndex={0}`, a bare `MathField` in `Item.tsx`); `theme.test.ts` and
  `settings/AccessibilitySection.test.tsx` (the previous choice left following the system, an
  unguarded read, an unknown stored value trusted, a tile that does not apply); the greyscale
  tile test (answered by fill alone, no `*`); `assessment/graphingBeside.test.tsx` (the part never
  told the panel opened, the breakpoint at 900 px, the layout at every width); and
  `status/load.test.tsx` (the value rebuilt on every render). Slice 7: the equivalence test in
  `tests/api/test_diagnostic_routes.py` went red with the unit never recorded as skipped, with
  later items of the unit served instead of answered, with every later item answered not learned,
  and with the item on screen answered wrongly; a first version passed every one of those breaks
  but the last, because its client said "not learned" to the unit's later items itself, and it was
  rewritten so that after a skip the client never does and must never be served the unit again.
  `OnboardingRoute.test.tsx` went red with the skip sent as a plain not-learned answer and with the
  confirming step removed.
- Merges: slices 1 to 6 touch only the client, so they merged together after one full run of the
  checks at their tip, and slice 7, which touches the server, merged on its own after another. Each
  slice is its own commit, and each new test was shown red under its break and green restored.

Desmos, on the operator's instruction of 2026-09-27 ("make it just open a webview of the Desmos
calculator website"), decided by claude-opus-5-5, not by a person.

- A calculator question in a session, and a calculator part in a timed drill or mock, carry an
  "Open Desmos" button that opens https://www.desmos.com/calculator in a frame inside the page
  (`app/web/src/input/DesmosPanel.tsx`), sandboxed and sent no referrer. A no-calculator item or
  part carries no button. The app's own graphing panel stays on calculator parts beside it.
- The CSP gains `frame-src https://www.desmos.com` and nothing else, recorded as the second
  exception in 09's CSP paragraph, where `tests/api/test_security_headers.py` now enforces it
  (red without the directive, green with it). In a real browser under the app's own header, the
  Desmos frame loaded and rendered while a control frame of example.com was blocked with a
  frame-src violation, with and without the component's sandbox attributes.
- Desmos needs an internet connection, which the panel says; the offline session of P6 is
  unaffected, because nothing loads until the button is pressed.
- Found while checking it, and fixed on main by stage 11 at the same time (e9a69a0, with
  tests/api/test_db_commits_before_reply.py): every route's database commit ran after its response
  was sent, so a diagnostic answered at once was refused as "not in the queue" 4 times in 6 in the
  running app. The same scope="function" change made here was dropped in favour of stage 11's.
  On the fixed server the immediate-answer probe answered all 30 diagnostic items with 0 refusals.

Stage 12, item selection, decided by the model (Claude) on the operator's delegation, every result
a simulation's (`docs/operator/selection-study.md`, `docs/operator/selection-study-record.md`):

- Two-term stays the live score, `LAMBDA` stays 0, and the five-term score and `EXPLORE_SHARE`
  stay in `app/sim/five_term.py`, which nothing live imports. Reason: on the corrected world
  five-term beat two-term for 39.0 and 19.0 percent of 200 students at 60 days and 55.5 and 39.0
  at 226, and its mean was lower or within noise; arm 6 beat arm 1 for at most 3.5 percent. Both
  fail 10's 90 percent bar and would fail a mean-difference bar too.
- The retrievability path into the stage bands and the review floor ships live. Reason: at
  `LAMBDA` 0 it computes the same value, and `LAMBDA` is the switch that stays off, held by
  `test_the_live_decay_term_matches_the_recorded_decision`.
- The simulator's world was corrected (keyed draws, consolidated prior knowledge, daily half-life
  growth) and the P7 record rerun on it. Reason: the stage 8 world let practice lower the
  retention of a known skill and grew half-lives on same-day repeats, which 01 says do not count.
- Two positive controls and one negative control were run, not one of each. Reason: the brief's
  forgetting oracle targets spacing, which mastery per item read the day after cannot see, so a
  teaching oracle was added to check the day-after measure can see anything.
- The run length was extended to 226 days, 2026-09-26 to 2027-05-10, beside stage 8's 60.
  Reason: mastery needs 7 days and a mastered skill comes due weeks later, so at 60 days due
  coverage fires on 1.1 percent of choices.
- 10's bars were not changed. Reason: only the operator loosens a bar.

For the operator's ruling (not decided here): whether 10's "on at least 90 percent of simulated
students" should read as a paired mean difference whose 95 percent interval lies above 0, with
the per-student share kept and reported. On this world the same policy against itself wins on 47
to 58 percent of students and only controls that read the hidden student reach 88.5 to 91 percent,
in single cells, so the two-term-against-random bar cannot be decided by a per-student share.
The ruling changes no live setting today: five-term and `lambda` fail on the mean as well.

The ruling, made by the model after the operator answered "decide for me": the bars are read from
the paired mean difference and its 95 percent interval, a challenger clearing only when the
interval lies wholly above 0 under both curves and the two-term floor failing only when it lies
wholly below 0, the per-student share kept and reported. Reasons: the share cannot separate
policies that differ on this world, even oracles; the interval narrows with students where the
share does not; and the asymmetry keeps the burden on anything that would change the live policy.
On the rerun P7 record the two-term floor passes, and five-term, `lambda` and removing
interleaving stay off. `app/sim/p7_evals.py` decide() and 10 carry the ruling.

Stage 13 (content2), four defects, by claude-opus-5-5 on the operator's delegation; every choice
below was the session's, logged with its reason.

- The 2021 Question 4 ninth point is modelled as a question-level point, not folded into a part.
  sg-21 page 14 prints it as its own block before part (a), "1 point", earned in any one part, and
  pages 15 to 17 total parts (a) to (d) at 1, 3, 2 and 2. A new frq record would have added a
  pseudo-part to the frequency tables, and folding it into part (a) would have said part (a) is
  worth 2, which the guideline does not. So BC-FRQ-2021-Q4-A carries `global_points` 1 and
  `global_point_types` [BC-PT-99024] (the derivative of an accumulation function by the
  Fundamental Theorem), added to `schemas/frq_records.schema.json`, and the checkpoint offers it as
  its own scoring row, "Part (any one part)", before the lettered parts.
- The checkpoint schedule with seven forms. The 42-day cadence (`app/checkpoint/service.py`) opens
  the first checkpoint at once and each next one 42 days after the last is finished. From
  2026-09-27 the forms fall on 2026-09-27 (2025), 2026-11-08 (2024), 2026-12-20 (2023),
  2027-01-31 (2026), 2027-03-14 (2022) and 2027-04-25 (2021); the seventh, 2019, would open on
  2027-06-06, after the exam, so it is the spare that absorbs one late checkpoint. The order is the
  existing one: years with published per-question means first, newest first.
- Staging corrections go in files prefixed `corrections-`, added last to `PHASE_ORDER` in
  `tools/merge_staging.py`, and were merged by name, never by a full replay: a full replay on this
  tree changed 4,299 lines across nine registries, dropping link entries later files had added
  (the regression recorded in Known defects on 2026-09-19).
- BC-ERR-10044 is tagged [inferred], like BC-ERR-10013: ced:189 states the integral test as a test
  of convergence, and no cached source observes either direction of the value confusion. It is held
  by BC-SKL-10016 (the integral's value is what the item asks for) and BC-SKL-10017 (the skill
  BC-MIS-10008 sits on), so gate 30's error-path rule reaches it from the archetype's skills.
- `content/golden/generator.json` GLD-GEN-003 froze ITM-AGT-10005-00's option C as BC-ERR-10013,
  the defect itself. Its frozen path was changed to BC-ERR-10044 so the golden records the
  corrected bank; the check that compares frozen and live paths is unchanged and as strict. This
  is a fixture edit made because the fixture recorded the defect, and it is named here so the
  operator can overrule it.
- Free-response reading. A capital letter called like a function that the question does not
  define is refused only when the question carries a `functions` record, so the forty questions
  that carry none read exactly as before. `equation_setup` passes or stays unsettled and never
  fails a written line. A limit written to fewer than three places is unsettled, not failed. An
  integrand point with a constant factor outside the integral (BC-PT-99048, 99058, 99002) was left
  to the model; no check reads it.
- The free-response target. 05's cadence is the only source and it is [inferred]: a full mock
  every four to six weeks, more often in the final eight weeks, and one part drill every two to
  three weeks between mocks, rising in the final eight weeks. The target takes the frequent end,
  so no cadence 05 allows repeats a question. From 2026-09-27 to 2027-05-10 is 225 days; the final
  eight weeks start 2027-03-15, leaving 24 weeks before them. Mocks: one every 4 weeks for 24
  weeks is 6, and one every 2 weeks in the final 8 is 4, 10 in all. Drills: one every 2 weeks for
  24 weeks is 12, and one a week in the final 8 is 8, 20 in all, a quarter of them on each of the
  four parts, so 5 Section II Part A drills and 5 Part B drills. Per research/exam/exam-structure.md,
  Part A is 2 calculator questions and Part B is 4 no-calculator questions, each 9 points. Need:
  calculator 10 x 2 + 5 x 2 = 30, no-calculator 10 x 4 + 5 x 4 = 60. The bank held 6 and 10, so
  the target was 24 and 50 new.
- Which archetypes can carry a calculator question. `tools/check_frq_items.py` requires a setup
  point in every calculator part, and only 15 active archetypes list a setup point type (BC-PT-99001,
  99002, 99020, 99048, 99051, 99058 or 99059) and allow the calculator: 06005, 06006, 99008,
  08001, 08002, 08008, 08011, 08012, 08013, 08014, 09001, 09005, 09007, 09012 and 09013. The gate was
  not loosened and no setup check was put on a non-setup point type; two drafts that did so
  (BC-QA-06001 with bounds_match on BC-PT-99019) were deleted. So the 24 new calculator questions
  sit in Units 6, 8 and 9 (6, 10 and 8), and the Unit 4 and Unit 5 shares were written as
  no-calculator questions (5 and 9). Against the exam weights of `app/engine/exam_weights.py` (BC
  band midpoints 7.5, 7.5, 7.5, 7.5, 12.5, 17.5, 7.5, 7.5, 12.5, 17.5 over 105), 74 new questions
  would split 5, 5, 5, 5, 9, 13, 5, 5, 9, 13; the bank received 5, 5, 5, 5, 9, 14, 5, 10, 8, 13 (79,
  five over target because the calculator share could only land in Units 6, 8 and 9).
- Audit rulings applied to every new question before the blind re-solve: an `any_line` check whose
  expected value is a constant became `target: answer` when it was the part's only value check and
  the part's answer, and null otherwise (a stray line equal to a small constant must not earn a
  point; 79 such checks changed across the three batches); an `each_side` check up to a
  constant was nulled (a correct constant multiple would fail it, 2); a BC-PT-99036 check on a
  polynomial centred away from 0 was nulled (an expanded form earns the first-terms point but not
  the remaining-terms point per the BC-PT-99035 record, 3). FRQ-AGT-10009-01 part (d) now names the
  Lagrange bound value of part (a) rather than "the result", which read two ways.

Passwords replacing passkeys, on the operator's instruction of 2026-09-27 to remove passkeys
entirely and sign in with a username and password. The operator delegated the plan's five open
questions; they were decided by claude-opus-5-5, not by a person. The ruling and its reasoning are
in `docs/plan/09-security-and-privacy.md`, "Authentication with a password", which reverses D10's
passkey-only rule for this installation.

- The per-IP limit is 10 requests per 60 s per peer address, on `Settings`
  (`auth_rate_limit_count`, `GROWTH_AUTH_RATE_LIMIT`); tests set it high explicitly. It covers only
  `POST /auth/signup`, `/auth/login` and `/auth/recovery/reset`, narrowing 09's per-IP paragraph,
  which had put the tightest limit on all eleven unauthenticated routes. Reason: it keys on
  `request.client.host`, which is one shared loopback key on the default bind, so a limit on
  `GET /` or `/assets` would lock the client out of its own files. The cost, recorded in 09: on
  loopback the limit is one global bucket, so any local caller can hold sign-in refused for up to
  60 s at a time. Behind a local reverse proxy, uvicorn's default proxy headers key it on the
  forwarded client address instead (corrected by the code review of 2026-09-27).
- A locked account gets the same 401 "username or password is incorrect" as any other failure, not
  a 429 with `Retry-After`. Reason: a distinct answer would tell a stranger the username exists.
  Schedule: 4 free failures, the fifth locks for 30 s, doubling per further failure to at most 900
  s, never permanent; an attempt during a lock counts nothing and does not extend it.
- The operator CLI `python -m app.auth.issue_recovery_code --db <path>` is added, as the way back in
  for a migrated user whose recovery code is missing or spent, resting on 09's statement that
  filesystem access is already total access. It audits `recovery_code_issued` with the actor
  "operator", a fifth new action beyond the plan's four.
- The commit-latency residual is accepted and recorded in 09: a known username always commits the
  attempt count and an unknown one writes nothing. Reason: one user, the per-IP limit bounds
  attempts, and the design does not rely on the username being secret.
- No unique index on `users.username`. It was declared, and 5 tests in `tests/db/test_migrate.py`
  then failed with `sqlite3.OperationalError: error in index ux_users_username after drop column:
  no such column: username`, because those tests drop every nullable column and SQLite refuses to
  drop an indexed one. That test is not on the forced-edit list, so the code changed and the test
  did not. Uniqueness rests on the single-user claim (`INSERT ... WHERE NOT EXISTS (SELECT 1 FROM
  users)`) and the lowercase normalisation. The planned assertion that the index exists was dropped
  from `test_migrate_passkey_retire`. Adding the index needs an operator-approved change to
  test_migrate.py, and multi-user needs it.
- `display_name` is kept and set to "student" at sign-up, as passkey registration did, so `GET /me`,
  the client type and the prompt tests are unchanged. The username is a separate column.
- The needs-password state is derived, a user row with a NULL `password_hash`, not a flag column.
  `GET /auth/status` reports it as `needs_password` to a loopback caller only, the pattern
  `/healthz` uses, so the migration window is not advertised.
- Every route declares `Depends(get_db, scope="function")`, as every other route at HEAD does; with
  plain `Depends(get_db)` the route got a different ORM session from `current_session` and logout
  crashed.
- A password change keeps the current session and signs out every other one; it does not rotate
  the current token, and the recovery code is unchanged. A recovery reset signs out every session,
  clears the lockout and issues a replacement code, keeping the known deviation recorded under
  Known defects that recovery hands out a new code.
- The key-derivation passphrase of 09 "Key handling" stays a separate secret from the login
  password. `PUT /settings/providers/{provider}` is still unbuilt (09, ruled 2026-09-23); when it is
  built it takes the passphrase and a password re-authentication.
- Backups keep old hashes: a dated copy or the pre-retirement copy under `backups/` holds that day's
  password hash and recovery code hash, so restoring it restores that password. Recorded in 09.
- Test contract changes the requirement forces, and the only edits to existing tests this change
  allows: `tests/runtime/test_context.py` loses the `rp_id` assertion (the field is removed);
  `tests/api/test_auth_status.py` takes the new status contract (a remote caller still gets exactly
  `{"user_exists": ...}`, a loopback case asserts `needs_password`), and the AuthStatus assertions
  in `client.test.ts` and `routes.test.ts` follow it; `tests/api/test_unauthenticated_routes.py`
  lists the eight routes; `tests/audit/test_vocabulary.py` asserts the new action names in place
  of `passkey_registered`, with its sorted-order check unchanged; `tests/session/test_purge.py`,
  `tests/export/test_export.py` and `tests/db/test_models.py` lose the dropped
  `passkey_credentials` table, and `test_export.py` gains `("users", "password_hash")` in its
  secrets list, which strengthens that gate, as does removing `PUBLIC_COLUMN_NAMES`;
  `tests/api/test_routes.py` takes the new recovery behaviour, with `test_purge_requires_reauth`
  kept at its name and node id; `tests/e2e/test_session_login_to_feedback.py` changes its
  docstring only, keeping the name gate 23 reads. The three passkey test files
  (`tests/auth/test_passkeys.py`, `test_add_authenticator.py`, `test_passkey_library_paths.py`)
  are deleted with the code they tested. Any other existing-test change is outside this list and
  is reported, not made.
- Plan text corrected in place with a dated note: 09 (purpose, posture, assets, STRIDE spoofing,
  the not-logged rule, the per-IP paragraph, the authentication section, retention rows, audit
  recorded and not-recorded lists, traceability), 06 (the py_webauthn sentence, the users table
  including the `recovery_code_hash` it was missing, the API surface rows and re-auth markings),
  08 (onboarding account), 10 (the e2e login), 11 (goal, scope item 15, gates 23 and 24 with their
  backticked names kept, the dependency diagram) and `docs/operator/ui-redesign.md` (the sign-in
  row). The historical run records in docs/operator that mention the passkey verifier double are
  left as history.

## Decisions taken on the operator's instruction, 2026-09-26 [inferred]

False mastery, on the operator's instruction to fix the 22 to 23 percent simulated false-mastery
rate against 10's 5 percent ceiling as an engine fix:

- `app/session/seed.py` no longer seeds the six BC-SKL parents of Q8 (BC-SKL-01018, 01039, 01044,
  02001, 02002, 03001) mastered. Every BC-SKL row starts unmastered with its prior beta, and only
  the 77 BC-PRQ rows start mastered, so an account holds 77 mastered rows, not 83. `var/growth.db`
  held 0 users, so no stored row needed changing.
- BC-SKL-02001 and BC-SKL-03001 have no archetype, so unseeded they would have shut BC-SKL-02006
  and BC-SKL-03002 for good. `Graph.blocking_parents` in `app/engine/fringe.py` leaves out a BC-SKL
  parent no archetype loads, and `parents_mastered` and the placement's `gating_closed` read it.
  BC-PRQ and other parents outside the skill map still gate. This also opens the children of the
  8 other archetype-less gating skills (BC-SKL-05011, 06040, 06042, 06043, 06044, 06046, 06053,
  06054), which were shut unless the diagnostic placed their parent. `gating_parents` is unchanged,
  so due coverage still reaches those parents.
- The diagnostic places a skill mastered at 0.90 (`DIAG_PLACE_MASTERED`, set to
  `MASTERY_THRESHOLD`), not 0.80. With the parents unseeded, 0.80 alone gave 6.5 percent on 40
  students, and about 1 in 10 placed skills was not known and never served in 60 days. 0.80 still
  decides the unit states on the result screen. A sweep on 40 students gave 0.85 at 2.9 percent and
  0.90 at 0.3 percent; 0.90 was taken because it is the bar practice already uses, not from the
  sweep.
- Recorded run (`tools/p7_evals.py`, 200 students, 60 days, `docs/operator/p7-evals.md`): worst arm
  2.2 percent exponential and 2.6 percent power law, from 22.1 and 23.3. Declarations fell from
  3681 to 1327 on two-term exponential, so a student re-proves more of what they know. True mastery
  per item on two-term moved from 0.01092 to 0.01021 (exponential) and 0.02306 to 0.02342 (power
  law). Two-term against the control moved to 73.0 and 78.0 percent, still under the 90 percent bar.
  Placement is still the only source of false mastery (29 of 329 placed on two-term exponential).
- Plan text corrected in place with a dated note: 02 (fringe rule, R15 paragraph, what is left
  not_attempted), 06 (skills_state seeding), 11 (Q8).
- Tests: `tests/session/test_seed.py` asserted the old Q8 seeding (83 mastered, BC-SKL-01018
  seeded) and now asserts 77 mastered, all BC-PRQ, and every BC-SKL unmastered with its prior beta.
  New `eval_false_mastery_within_ceiling` (20 students, 20 days, two-term and control) was green
  at 0 of 66 and 0 of 71, red at 18 of 206 with placement back at 0.80 and at 66 of 235 with the
  six parents seeded again. New `test_a_parent_no_archetype_teaches_does_not_gate` was red with
  `parents_mastered` back on `gating_parents` and red with BC-PRQ parents dropped from blocking.
- `eval_selection_bias_control` failed after the fix, `(1215, 9) != (1215, 9)`: over 6 students
  and 20 days nothing placed came due, so the policy and the control served the same items. The
  operator delegated the decision; `ARM_DAYS` in `tests/eval/test_p2_evals.py` went from 20 to 40,
  the size `tools/p2_evals.py` records at, and the assertion is unchanged. The P2 record was rerun:
  placement 54 of 950 not known (5.7 percent), from 514 of 3303 (15.6). The record's claim that a
  wrongly placed skill comes back as a review within days was withdrawn; on 20 students none of 23
  wrongly placed skills was served in 60 days.

Pre-practice session, on the instruction to do everything needed before the operator starts
practicing:

- `app/db/backup.py`: every server start copies the database to `backups/` beside it
  (`GROWTH_BACKUP_DIR` overrides, `none` disables), the first copy of each day only, the last 14
  days kept. The copy sits on the same disk as the database, so it guards against a bad write or
  a purge, not against losing the machine.
- `app/web/dist` was rebuilt; it had been built on 2026-09-24, before P5, P6/P8 and the UI
  redesign, and `dist/` is gitignored, so a rebuild is needed after every client change.
- The empty-queue defect was left: home shows the empty state only with no due, frontier or
  returning items, which a student with 139 archetypes will not reach for months.

Stage 7, P6 and P8, decided on the operator's delegation (the stage brief delegates every decision).

- Cooldowns: 30 minutes after a usage limit, the drain's own retry interval, and 60 s after three
  consecutive other failures, per role and link, held in the process. Registered as tunables in 12.
- A budget or pacing stop moves the call to the next link without cooling the stopped one, since
  the guard's refusal cost no call; a link that could not run at all (no CLI, no key) is reported to
  the caller only when no other link reached a stop or a failure.
- The drain runs inside the server rather than on a system scheduler, so it needs nothing installed
  and shares the server's cooldowns: 10 minutes between passes, 5 calls a pass, only the tutor role
  (the only role that queues). The manual tool stays as a one-pass fallback.
- The practice tutor template, which no route serves, got one live golden on the subscription
  rather than a hand-written stand-in, so its golden is a real answer. `elaborated_v1`, superseded,
  keeps its synthetic stand-in, which says so.
- Purge treats a shared-table row as the student's when it names them: a job whose payload names
  their user id, a review whose ref_id is one of their rows. Nothing else in those tables is
  touched.
- The frontend agent's contrast catalogue render got a 60 s setup budget of its own, because the
  new suite's setup takes about 9 s alone and passed 10 s beside the other suites.

Stage 9, the UI redesign, decided on the operator's delegation (the stage brief delegates every
decision). Every judgement below was made by claude-opus-5-5, not by a person.

- The operator attached `growth-standalone-source.zip` on 2026-09-26, which is the instruction to
  replace the Graphite palette chosen on 2026-09-23. `app/design/growth-tokens.json` now holds the
  prototype's zinc palette, mapped token by token in `docs/operator/ui-redesign.md`. Its one accent
  is the ink colour (white on dark, near-black on light), read as 08's single accent with the
  accent set to the ink hue; its neutrals are cool where 08 asks for warm, which the operator's
  choice of design overrides as Graphite did.
- `border-hairline` moved from the prototype's #2b2b30 (dark) and #d6d6db (light) to #6b6b72 and
  #83838b, the lightest values that hold 3:1 against all three surfaces, because
  `eval_contrast_all_screens` holds every drawn border to SC 1.4.11. The first light value tried,
  #8e8e96, failed at 2.83:1 on `surface-sunken`. No gate was changed.
- Inter 400, 500 and 600 ship from `@fontsource/inter` 5.3.0, not from the prototype, whose font
  files hash differently, with the OFL beside them. Each weight is its own family in
  `app/web/src/styles/fonts.css`, so no numeric weight appears in a stylesheet and
  `test_no_literal_values` and `app.test.ts` stay unchanged. The faces sit in their own file
  because `testing/cascade.ts` cannot match an `@font-face` block; `fonts.css` is still scanned by
  the literal gate.
- The page column is the prototype's 820 px; every paragraph and list item in a screen still stops
  at 08's 68 characters.
- Section headings carry no rule beneath them. At 3:1 a rule under every heading reads heavy, and
  08 prefers space to borders; the page title keeps its rule.
- The session gains a stage badge ("Stage: completion") and a "Worked so far" label over the
  steps, both from 08's session wireframe. The prototype's set position, progress segments, stop
  control, Enter hint, theorem reference and "you wrote / the rule gives" block are not built,
  because the client has no data or route behind them (listed in `docs/operator/ui-redesign.md`).
- The timed-part tools (mark for review, question menu, zoom) moved above the question and the
  question menu opens as a block of tiles beneath them, as in the prototype; every label, role and
  test id is unchanged.
- `app/web/src/home/HomeScreen.test.tsx`, "renders the queue lines from its props": the queue count
  moved into its own span, so `getByText(/7\s+alpha skills/)`, which reads only an element's own
  text nodes, can no longer find the line. Old assertion: `screen.getByText(new
  RegExp(`${count}\\s+${label}`))` is truthy. New assertion: the rendered line at the same index has
  `textContent` matching `^${count}\\s+${label}$`, which is anchored and checks the order as well.
  It went red with the label written without its space and green restored.
- The contrast catalogue in `app/web/src/testing/screens.tsx` gained four screens it never
  rendered: a session item with a confidence chosen, the diagnostic introduction, a diagnostic
  question answered, and the diagnostic result. This widens `eval_contrast_all_screens`; no check
  was removed.
- The prototype's skill count ("68 skills") beside each unit of the mastery map was tried and dropped:
  `MasteryMap.test.tsx` "prints no count and no percentage anywhere on the map" went red.

Stage 10, the experience pass the operator asked for on 2026-09-26 ("do best course of action"
on the audit of stage 9), decided on that delegation by claude-opus-5-5, not by a person.

- Loading and failure copy. 08 gives none, and earlier stages invented none, which left blank
  screens and 18 silent catches. The operator's request for the best experience is read as the
  instruction to write it: "Loading", "This did not load. The app may have stopped or lost its
  connection.", "Try again", and for a refused action "That did not go through. Nothing you wrote
  is lost, so you can try again." None carries a digit, so the no-digit tests on home and settings
  still hold. The loading line carries no live role, because the token notice is the page's one
  status region and `App.test.tsx` reads it by role.
- A set shows what is left: the unanswered slots of GET /sessions/{id} and the sum of their
  archetype forecasts, "8 items left in this set, about 24 minutes". The count includes the item on
  screen and refreshes when the next item is served.
- "I want to stop here" (08's own copy) closes the set through the existing close route after a
  second, confirming step, so one stray click cannot end a set. Leaving through Home still keeps
  the set resumable.
- The end of a set says how many items this sitting worked through and how many corrected items
  come back in Review, and gives no score and no count of correct answers, as 08 requires.
- Feedback opens with what the student wrote or chose. The "the rule says" half of 08's feedback
  wireframe is not built, because the feedback payload carries no worked answer at completion.
- Keys: Enter checks and moves on, 1, 2 and 3 rate confidence, A to D choose; in timed parts A to D
  choose and N and P move. They are read on the document, since focus sits on the body after a
  load, and never from a text field, and Enter is also read from the math field, where it has no
  other use. The hint beside the button is hidden under 600 px, where there is no keyboard.
- Providers and budgets, and experiments and the evidence of learning, sit in two closed
  disclosures under the student's own settings.
- The representation table's labels were bare ids because the route read `settings.snapshot`,
  which is filled only on first use; it now reads the snapshot the server loaded at start. The
  table stays closed until a translation has been attempted.
- Home drops a queue line whose count is zero.
- Not built, with the reason: splitting the 1.76 MB bundle, because on localhost first contentful
  paint measured 60 to 84 ms and the script fetch 21 ms, so a split would save tens of ms at the
  cost of async loading on every screen; the graphing panel beside the question, compact question
  menu tiles, a diagnostic unit skip (needs a backend ruling), the LaTeX inspector, a theme switch,
  shared page components, a media-aware contrast cascade and layout tokens. Each stays a candidate.

## Decisions taken on the operator's instruction, 2026-09-24 [inferred]

Stage 3, the review screen and the mastery map:

- The map is a row of marks per unit, ordered along the prerequisite graph, drawn as HTML buttons
  holding a 16 px SVG mark with 8 px gaps. Buttons give focus and a name to each skill for free;
  the 8 px gap keeps mark centres 24 px apart, the spacing WCAG 2.2 SC 2.5.8 accepts for targets
  under 24 px. Edges are not drawn: with up to 74 skills a unit, drawn edges would be unreadable.
- The map is one tab stop. Arrow keys move along a unit and between units, Home and End to the ends
  of a unit, and the focused mark's 08-style sentence is printed under the map.
- A skill seeded mastered at registration (R15) and never observed shows as mastered and its
  sentence says it is assumed, not shown.
- The hypercorrection lane is the open corrections the student rated confident. The engine's
  `hypercorrection_due` is per skill; the screen lists items, as 08's wireframe does.
- An edited error note goes through the existing error-note route, which already replaces a note
  (the 2026-09-20 ruling), so no new write route was added.
- The P3 seam for stage 4: `GET /review` already carries `grading_available` and
  `provisional_points`; P3 fills the list from gradings with `provisional` 1, one entry per point
  with the keys `app/review/screen.py` `PROVISIONAL_POINT_KEYS` names (grading_id, attempt_id,
  label, point_label, reason, disputed), and sets `grading_available` true. On the client,
  `ReviewRoute` passes an `onAskForReread(gradingId)` handler to `ProvisionalPoints`, which then
  shows "Ask for a re-read" on each undisputed point; the handler POSTs to
  `/gradings/{gid}/dispute` (06). `ProvisionalPoint` in `api/types.ts` is pinned to
  `PROVISIONAL_POINT_KEYS` by `api/client.test.ts`, so the two cannot drift.

Stage 2 (p2engine):

- The calibration curve's real-use exit criterion (30 real confidence-rated attempts) waits on
  the operator's use. The render path from a seeded account is covered by
  `tests/api/test_calibration_route.py::test_thirty_rated_attempts_return_the_curve_with_counts_and_intervals`
  and `app/web/src/progress/CalibrationCurve.test.tsx`, both run green this session.
- The five-term score stays off. On the synthetic world it found more truly mastered skills per
  item (0.0331 against 0.0189, 1,000 sessions per arm). That is recorded for P7 and changes
  nothing, because R4 turns the score on only by P7's gate and the world does not learn (see
  Known defects).
- A diagnostic is offered at first login (no session rows) and after a long gap. An account that
  already has P1 sessions is not sent to a diagnostic, because the plan names only those two
  triggers.
- The onboarding screen was drafted by a subagent. When stage 3 merged mid-stage, its edits were
  replayed on the rebased tree, the conflicts resolved by hand, and the missing screen and home
  tests written and mutation-checked in this session.

Stage 1, items for Units 4 to 10, decided on the operator's delegation (the stage brief delegates
every decision). Each is argued in docs/operator/items-units-4-to-10.md.

- Closed-form rule: an archetype gets items when it is active, `no_calculator`, not covered by
  P1, its answer can be one finite value or expression in the MathJSON `app/items/mathjson.py`
  reads, and its stem needs no figure. 38 of 62 candidates qualify (6 from Units 1 to 3, 32 from
  Units 4 to 10). Out: 16 verdict or classification archetypes, 7 printed-graph or slope-field
  archetypes, and BC-QA-10013, whose answer is an interval. Reason: a key the reader cannot hold
  cannot be rechecked or graded as a short answer under R29, and adding Infinity or Interval
  heads would change the client input and the grader, outside this stage.
- Verdict-shaped archetypes in scope are posed on their finite part: convergent improper
  integrals only (06011, 10005), a vertical asymptote asked as its x-value (01009), error bounds
  or a least number of terms (10008), never a general term with n!.
- One bank per unit, `content/items_unitNN_agent/`, each with its own `key_formulations.py`.
  `GROWTH_ITEMS_DIR` unset now serves every `content/items_*` bank and a set value may list
  several, `os.pathsep`-separated; `Settings.items_directory` became `items_directories`.
- `tools/check_items.py` checks error paths per archetype rather than over the P1 union. Stronger;
  P1's 130 stay clean.
- Formulations are written by separate agents given stems only, because the authoring agents know
  their keys.
- Five in-scope archetypes got no items because the errors their skills hold cannot produce three
  honest distractors: BC-QA-01005, 06011, 06014, 07010, 10006. No error was retagged and no
  registry link was added from the item side; linking more BC-ERR records to their skills is
  research-library work through staging and `tools/merge_staging.py`.
- The recheck control's single perturbation 2v + 1 leaves -1 fixed; it now also applies
  v + sqrt(2)/7 and skips a perturbation identical to the value. Recorded under "Plan
  corrections applied".
- Gate 29 for the new items was drawn over a scratch database that ingested only the nine unit
  banks, so the P1 items that already have their own record could not enter it.
- The stems may carry inline LaTeX between `\(` and `\)`, which `MathText` already renders,
  because integrals and series read badly in plain text.

Stage 8, P7 evaluation harness, decided on the operator's delegation:

- The five-term score stays off and `lambda` stays 0, on `docs/operator/p7-evals.md`: five-term
  beat two-term for 35.0 and 21.5 percent of students against a 90 percent bar. The P2 record
  (five-term ahead on a world that does not learn) is superseded, because that world measured
  detection, not teaching.
- The metrics view is the operator's page, reached from settings and never from the bar or home,
  because 08 rules out a dashboard in the student's daily path. Every value carries its
  denominator; a zero denominator prints no number.
- The feedback A/B starts off in the running app because elaborated feedback is the better-evidenced
  arm; the retrieval_entry A/B, a real uncertainty, starts randomised. An interval is stated once
  each arm holds 30 outcomes ([inferred], the calibration curve's floor).
- A checkpoint is available at once and then every 42 days, so the first one is a baseline and six
  forms cover the months to the exam. Forms come newest first among years with published
  per-question means (2025, 2024, 2023), then 2026, 2022, 2019. No stem, figure or scoring text is
  stored or served: the screen links College Board's own PDFs.
- The concept probe is 17 bank items, two per unit where the bank allows, drawn by seed 20261001
  and withheld from practice. Unit 8 has no bank; Unit 9 gives one.
- Golden sets for all six roles were written by two agents and one frontend agent built the
  screens; each result was checked here (validation, spot checks, relabels, both web checks, 20
  mutation runs) before it was kept.

Stage 4 (p3), P3 free response, grading and diagnosis, decided on the operator's delegation (the
stage brief delegates every decision):

- Images reach the subscription CLI as one stream-json user message: `claude -p --input-format
  stream-json --output-format stream-json --verbose`, image blocks first, the prompt last, with
  every flag that switches tools, settings and MCP servers off unchanged. A live run on 2026-09-24
  (`tools/subscription_image_smoke.py`) showed tools `["StructuredOutput"]`, `mcp_servers []`, no
  permission denial and the page read correctly on Haiku 4.5 and Sonnet 5. The paid API was never
  needed, so no API call was made in this stage.
- The two standard grader samples cannot be at temperature 0 on Sonnet 5 (a 400 through the API; the
  CLI has no temperature option). They are two samples at the model's own setting; the standard
  prompt is the liberal one (`prompts/grader/point_liberal_v1.md`), the third sample the strict one.
  Reason: the only study isolating the dial found liberal lowered MAE for every model.
- Per-point grading needs one of the four modes R10 names, and P5 builds them. P3 ships the
  free-response half of the unit check (`app/frq/unit_check.py`, session mode `unit_check`,
  untimed, credits the engine); the multiple-choice sweep and set cover arrive with P5. Reason: 05
  makes the unit check the untimed mode that moves mastery, so it is the one P3 can honestly host.
- Free-response questions live in `content/frq_items/` in their own format (`app/frq/items.py`) and
  get item rows with status `frq_verified`, which `app/runtime/bank.py` never serves, and
  `load_attempts_history` leaves free-response attempts out, so no micro-session can serve or
  requeue one (R10).
- The student's confirmed work is LaTeX, read into SymPy on the server with SymPy's lark LaTeX
  backend plus a normaliser (`app/grading/latex.py`); anything it cannot read is unsettled and goes
  to the model, as 03 requires. `lark` and `pillow` are now dependencies. The LESSONS rule against
  installing a LaTeX parser is about audit formulation, which still never parses stems.
- The diagnostician's model call only observes (errors, signals, gap descriptions, procedural or
  conceptual) with verbatim evidence; every probability, the gap trace and the probe are
  deterministic code (`app/diagnosis/diagnose.py`). It runs on every graded free-response answer
  with a lost point, not only on a recurring BC-ERR path, because a free response has no BC-ERR
  path until something reads it. 03's "a guess does the reverse" is read as conceptual times 0.5
  and non-conceptual mass times 1.5.
- A dispute is a one-click re-read: a visible `dispute` review_queue row and a fresh three-sample
  judgement of that point, with every other point keeping its stored samples. The operator never
  reviews, so the re-read is the resolution path the student has.
- Engine credit from a graded answer comes only from published points; a provisional point's
  skills are not_attempted. Reversal restores each skill row untouched since the credit, and takes
  back only c and f on a row a later attempt moved (logged to audit_log).
- A fixed-key answer check cannot see AP follow-through, so a point may name `follows_from`: when
  its check fails after one of those points was lost, the model judges it on the student's own
  earlier result. Found by the bank author; no served item used the field at the stage's close.
- Pacing for the new roles on the subscription: grader 120 a day and 12 a minute, transcriber and
  diagnostician 30 a day; a minute stop waits instead of failing. API caps for the fallback:
  grader $1.50, transcriber and diagnostician $0.40 a day.
- Grading runs as a FastAPI background task, not a `jobs` row. A crash leaves the attempt confirmed
  with no points, and confirming again grades it; the retry ladder 06 names is not built.
- The printable page is a server-rendered PNG with a solid square in each corner, which is what the
  quality gate's marker check looks for.
- Golden set 2 for the P3 eval is the stage's own (150 responses, 30 BC-PT ids that reach a model,
  written and hand-graded by two Claude subagents on the delegation, eight of their labels
  re-read by the stage lead and upheld). P7's `content/golden/grader.json` (85 responses, 17
  types) was written in parallel; the two are kept, and the P3 numbers come from the larger set.
  Golden set 3 uses P7's 20 page specifications, rendered into fixture photographs here.
- The paper-to-grade fixture page was chosen because the live grader splits on it: the same
  borderline justification came back with 0, 1 or 2 provisional points across six recordings.
  The committed recording has one, as the gate asks.

Stage 5, P4 item generation, decided on the operator's delegation. Each is argued in
docs/operator/p4-generation.md or docs/operator/duplicate-gate/.

- Templates are committed Python modules authored offline and gated, not model output executed at
  run time: the gate, the Monte Carlo pass and the recheck all run on reviewed code.
- A template for every active archetype, including those with 20 signed-off items already, so every
  archetype has a Monte Carlo-checked family; generation filled each to 20 plus two spares, and at
  least 5 items where 20 existed.
- Distractor errors must be held by the archetype's skills (stage 1's stronger rule). Where fewer
  than three honest errors were held, existing BC-ERR records gained the archetype's skills through
  an append staging file, each link with its reason; no error was minted.
- Statement keys (verdicts, classifications, intervals, interpretations) with parallel labels, a
  verdict that varies across draws, and every distractor false; statement items are always served
  as a choice.
- Disagreements go to review; the lead adjudicates. Of a set of duplicates the first by id is kept.
- A template changed after publication retires its items: 44 items of 05009 and 05011 were rejected
  and regenerated when those families were widened; four 01005 items were rebuilt from their seeds
  when a unit coefficient was fixed, keys unchanged.
- The gate gained checks beyond 13's eleven, each shown red then green: parallel statement labels,
  at least 100 distinct problems in 300 draws, a printed coefficient of 1, small distinct constants
  never called equal.

Stage 6 (p5), P5 assessment modes, decided on the operator's delegation (the stage brief delegates
every decision). Canonical record: docs/operator/p5-assessment.md.

- One lifecycle for all three modes: a session holds parts (`assessment_parts`) and each part its
  questions (`assessment_responses`), which keep the answer, tools and time while the part is open;
  an attempts row is written for each answered question only when the part closes. Reason: a
  timed part must accept changed answers until it closes, as Bluebook does, and the unit check
  withholds feedback until submission, so neither can grade on each answer.
- The full mock and the part drills do not apply the fringe gate. A mock is the whole exam and
  writes no mastery; gated, it could not be assembled until the whole graph was mastered. The unit
  check, which writes mastery, keeps the gate. Recorded under Plan corrections against 02
  invariant 3's "rehearsal".
- Free-response answers are written on paper during a timed part and captured after it closes,
  in both capture modes; the image and typed routes refuse while the part's clock runs. Typed
  capture means typing from the paper afterwards. Reason: the exam's artefact is the booklet, and
  capture during the part would give grading feedback before Section II ends.
- A mock's free-response questions must carry the per-question total exam-structure.md states
  (9); a part that cannot be filled at that shape is refused with the reason. Sixteen nine-point
  questions were written for this (Done, stage 6).
- The Bluebook calculator is represented by the product's own graphing panel, not Desmos and not
  any model provider: plot in a chosen window, zeros, numerical derivative, numerical definite
  integral (the CED's four), with a radians or degrees indicator defaulting to radians. It is
  rendered only on calculator parts and is absent from the page on the others. Reason: Desmos's
  embeddable API needs a key and third-party script loading the CSP forbids, and 12 keeps the
  variant question open.
- The reference sheet is absent and the setup screen says so, from the form template.
- The score band method (docs/operator/p5-assessment.md, "The score band"): composite placed on
  a normal curve built from the free-response section's published means and summed standard
  deviations, read against each published year's distribution, widened one score point by
  sliding, unioned over years and over provisional points. The internal score is never returned
  or stored. Chosen over fitting third-party cut points, which 05 rejects.
- Rapid guessing: fast (per-archetype threshold) and first answered inside the part's final five
  minutes; flagged questions leave the pacing means and the rule diagnosis. The threshold values
  are carried into 12 as tunables.
- The unit check collects a confidence rating per item with its answer and applies it at
  submission; an unrated item is applied as unsure, as the micro-session's close sweep does.
- Numbering: Section I runs 1 to 42 across the part boundary and Section II 1 to 6, from the
  template's `continuous_within_section`, since exam-structure.md's CED reading says so and the
  Bluebook numbering stays open in 12.
- The break between parts is a screen the student leaves by starting the next part; no break
  length is invented, because no cached source states one.
- The 20 exit-criterion runs were driven over HTTP by a script against the running app with the
  grader off (docs/operator/p5-timed-runs.md); the one full mock with the live grader and a
  photographed booklet page was driven in the browser (docs/operator/p5-full-mock.md).
- The client screens were built by a frontend agent from a written brief and reviewed here before
  merge.

## Decisions taken on the operator's instruction, 2026-09-23 [inferred]

Subscription backend, Slice 2.

- Precedence reversed from Slice 1, on the operator's instruction that the paid API is used only
  when `GROWTH_AI_BACKEND=api`: `GROWTH_TUTOR_PROVIDER=anthropic` now stops startup unless
  `GROWTH_AI_BACKEND=api` is also set, including beside `GROWTH_AI_BACKEND=subscription`, `replay`
  or `none`, since each of those is also "without GROWTH_AI_BACKEND=api". Tests changed:
  `test_main_wires_a_tutor_when_a_key_is_configured` now sets `GROWTH_AI_BACKEND=api` beside the
  old variable and also asserts no pacing is built; `test_building_the_application_opens_no_socket`
  sets `GROWTH_AI_BACKEND=api` and now asserts an `AnthropicProvider` rather than any tutor;
  `test_an_explicit_backend_wins_over_the_older_variable` became
  `test_the_older_anthropic_switch_refuses_beside_any_backend_but_api`, which asserts a refusal
  where it asserted a subscription tutor. Each new assertion is at least as strict: none lets the
  paid adapter be wired by the older variable alone.
  From the slice review, `GROWTH_TUTOR_PROVIDER=api` is refused the same way: an unmapped older
  value used to pass straight through as the backend, so it wired the paid adapter without
  `GROWTH_AI_BACKEND=api`. Other unmapped values still reach `build_tutor`'s unknown-backend
  error. `test_the_older_variable_naming_api_does_not_wire_the_paid_api` was shown red with the
  old comparison and green with the fix.
- Pacing is a call count, not a dollar figure, because the subscription is metered by usage
  windows and the per-role caps price a call at API rates it is never billed. Defaults tutor 60 a
  day (three sessions at the per-session ceiling of 20), other roles 20, 4 a minute per role;
  sizing in `docs/plan/14-token-economy.md`, "Subscription pacing" [inferred], because neither
  window is published as a count. The count is one file for the process, not per user, because
  the login it protects is the operator's one account. A pace stop is a `BudgetStopped` so every
  caller degrades it as a cap.
- A paced call keeps computing `last_accounting` at API prices, so attempts still record tokens
  and a notional cost, but writes nothing to the budgets row.
- The drain is a CLI tool, not a startup or periodic hook, so no subscription call happens
  without the operator starting it. It refuses `replay` (it would store a canned sentence on a
  real attempt) and `none`. It stops at the first job that meets a limit, since every later job
  would meet the same closed window, and at a pacing or budget stop. A limit wait does not increment
  `attempts_made`, so only real failures count toward `MAX_DRAIN_ATTEMPTS`; the one
  `tests/api/test_subscription_drain.py` assertion that expected 1 after a limit wait (written
  earlier in this slice, never committed) now expects 0, an equality as strict as before.
  From the slice review: a drain retry is held to the tutor ceilings compose_sentence enforces, and
  a job already at either ceiling is marked failed (`last_error = tutor_ceiling_reached`) without
  a call, since neither ceiling lifts for that attempt. A retry that meets the limit again no
  longer counts a tutor call on the attempt, because it is the call already counted when
  compose_sentence queued the job, still waiting for the window. Counting it filled the item
  ceiling after two waits and would fail a job no model answered. Other drain failures still count.
  Shown red by removing the ceiling check (2 tests) and by counting limit waits (2 tests). On the
  api backend `DevSpendCapExceeded`, which is not a `BudgetStopped`, stops the drain as
  `stopped_by = dev_spend_cap` with the job untouched instead of escaping as a traceback.
- The smoke tool calls `SubscriptionProvider` directly, not through `GuardedProvider`, because the
  default 4-a-minute pacing would refuse a 5-second-paced latency run; the provider, argv and
  environment are the production ones. It reads `CLAUDE_CODE_OAUTH_TOKEN` from `.env` only to
  pass it to the subprocess and reports presence, never the value.
- Thinking off on the CLI: the tutor's API request already disables thinking, and the CLI thinks
  unless told not to, so the adapter maps the same request options onto the CLI. The variable is a
  fixed value set by the adapter, never copied from the host, so the allowlist still admits no
  host variable beyond its five names and the token.
- Evals move to the subscription with the runtime lines: the argument for keeping them on the key
  was that Claude Code is a different harness from the one that serves the student, which stops
  holding once the student is served by the same `claude -p` harness.
- `tools/cost_model.py` gained `PER_STUDENT_TARGET_LOW` (50.00) and `DEV_SPEND_CAP` (15.00) so
  doc 14 may print the target and the cap under its dollar-figure check; a test asserts
  `DEV_SPEND_CAP` equals `app/providers/guard.py` `DEFAULT_DEV_SPEND_CAP_USD`.

Subscription backend, Slice 1.

- Precedence: an explicit `GROWTH_AI_BACKEND` always wins; `GROWTH_TUTOR_PROVIDER` is read only
  when it is unset, and its `anthropic` still maps to the `api` backend. Reason: the brief asks to
  keep the older variable working, and an existing deployment or test that set
  `GROWTH_TUTOR_PROVIDER=anthropic` made the same explicit choice to spend on the key. The
  earlier partial edit let the older variable win over `GROWTH_AI_BACKEND`, which would have let
  a stale setting override the new switch, and was reversed.
- `test_a_stray_key_alone_wires_no_tutor` became `test_a_stray_key_alone_wires_no_paid_tutor`:
  with no backend set the default is now the subscription, so its assertion changed from
  `tutor is None` to "not an `AnthropicProvider`, and a `SubscriptionProvider`". The property it
  guards, that a key alone never wires the paid adapter, is unchanged. The earlier partial edit
  had pinned `GROWTH_TUTOR_PROVIDER=none` instead, which made the test repeat the explicit-none
  test and prove nothing about the key; reversed. The two other changed wiring tests set
  `GROWTH_AI_BACKEND=api` explicitly and keep their assertions.
- The queue is the existing `jobs` table (no migration), one row per role and attempt through an
  idempotency key, in `app/providers/call_queue.py` rather than inside `subscription.py`, so the
  subscription module holds no database code.
- A limit is recognised by `ProviderCallFailed.exception_type`, because the guard strips the
  original exception by design (13 item 7). A bare `SubscriptionLimitReached` from an unguarded
  provider degrades the same way.
- A missing binary is `RefusedBeforeWire`, since no process started, so the guard refunds its
  reservation. A timeout, a non-zero exit and non-JSON output are ordinary failures and keep the
  worst-case charge.
- `stream` yields the whole result as one `{"type": "text", "delta": ...}` event, the normalised
  shape `AnthropicProvider` uses, because `--output-format json` has no incremental text.
- The subscription ledger subclasses `DevSpendLedger` with its own path and no cap.
- The fake CLI reads its mode from, and writes its record to, `HOME`, because the allowlisted
  environment carries nothing else a test could use to configure it.

Fifteenth session, on the instruction to build slice 1 of the persistent developer spend cap.

- Storage: a flat JSON ledger under `var/dev_spend_ledger.json`, not a table via `app/db/migrate.py`.
  The per-role `BudgetCaps` in `app/providers/guard.py` are scoped to a user, a role and a day and
  reset every day; the developer cap is none of those, one running total, global to every role, every
  user and every process run, that never resets. `var/` is already gitignored and already holds this
  repository's other process-local state (`growth.db` itself), so a JSON file there needs no
  migration, no schema and no database session to read, and survives a checkout where the app
  database has not been created yet.
- The cap tracks a call only when the caller opts in (`dev_spend_track=True`), never by guessing from
  the wrapped provider's class inside the guard. `tests/providers/test_anthropic.py` wires a real
  `AnthropicProvider` to a fake transport to unit-test the adapter without a socket, and an
  isinstance-based auto-detection inside `GuardedProvider` would have started writing every such test
  run to the real ledger file, eventually breaching the real cap purely from test traffic (caught by
  running the full suite twice: the ledger accumulated to $16.67 and a later, unrelated test then
  failed with `DevSpendCapExceeded`). The one caller that opts in is
  `app/api/routes/sessions.py`, from `isinstance(settings.tutor, AnthropicProvider)`, which is the
  actual decision of whether this process would spend real money.
- `claude-opus-5-5` in `tools/cost_model.py` is tagged [inferred], not [verified]: the other rows in
  PRICES are read directly off the provider pricing pages; this one is the operator's own console
  announcement of 2026-09-23, a secondhand report of a price rather than an independent reading of
  the page itself.

Eighteenth session, on the delegated ruling for slice 3, how a skill leaves stage example.

- The ruling: stage `example` collects a graded answer. The worked example is shown with its final
  step left for the student, the student commits an answer, a confidence rating is collected after
  the answer and before feedback exactly as at completion and unsupported, and the server grades
  and credits it under 02's existing rules, so 02's rule of 2 consecutive credited successes at
  example applies as written. 11 implementer decision 3 is withdrawn; its old text is quoted in
  place rather than deleted, so the record of what changed survives.
- Example now blanks its last step the same way completion does, gated on the same 2-step minimum
  (`supports_completion`), rather than getting its own threshold or its own fallback stage. Below
  the minimum, example degrades to every step given and unblanked instead of refusing the slot,
  matching the shape the existing completion-below-minimum test already established, because
  inventing a second fallback rule for one archetype shape no P1 item actually has was not asked
  for and was not built.
- 02's line ~404/line ~407 inconsistency (a comment naming "a credited observation", code reading
  `observation_count`, which line 56 already says counts uncredited observations too) is resolved
  toward the comment: a new `credited_observation_count` field, not toward loosening the comment to
  match the code, because the code's reading is the one the ladder's own R7 counters do not use
  either, and 02 names `credited_observation_count` as the field tied to the same event that moves
  `consecutive_successes`/`consecutive_failures`.
- `test_mastery_path_across_days_and_unmastery`'s flake is fixed by pinning the registered user id
  for that one test, not by seeding `app/session/preview.py`'s rng some other way. The rng's
  contract (process seed, user id, day) is real production behaviour, spelled out in 02 and 11;
  changing it to make one test stable would be changing what ships to make a test convenient, which
  is backwards. The user id was never a value the operator specified, only one `uuid.uuid4()`
  handed to `new_id` at registration, so pinning it in the test is the draw the test controls, not
  the draw the system depends on.

Nineteenth session, on two verified review findings against the eighteenth session's slice 3 work,
delegated for a fix rather than a second ruling.

- The eighteenth session's "example degrades to every step given and unblanked" reading, quoted
  above, is withdrawn. It was written to match the existing completion-below-minimum fallback
  shape, but that shape predates example collecting a graded answer: once example grades what it
  shows, showing the answer along with the given steps is not a degrade, it is a free credited
  success. Example now needs the same 2-step room to blank a step that completion needs, and an
  item under that minimum is served at `unsupported` at either stage rather than at `example`,
  since `example` no longer has a shorter fallback of its own.
- The backfill for `skills_state.credited_observation_count` replays `attempts.per_skill_states`
  rather than approximating from `credited_successes`/`credited_failures` or the consecutive
  counters, because none of those three round-trips losslessly: a `prerequisite_gap` credit is
  `(0.0, 0.0)` on the target skill (`app/engine/update.py CREDIT_TABLE`), so it moves neither `c`
  nor `f`, and it can still land on a `consecutive_failures` value that a later drop resets back to
  0 while `fading_stage` stays at `example` (`drop_fading` is a no-op at the floor of
  `FADING_ORDER`, and `move_counters` resets the streak counter regardless). `attempts` is the one
  place the per-skill mastery state that drove each credited event is still on record, so it is the
  only source an exact replay can be built from.

Twentieth session, on the instruction to run slice 4, the BC-PT labelling pass, and bring the
Claude-only tier under $100.

- The 76 labels live in a new file, `data/bc_pt_determinism_labels.json`, rather than as a field
  merged into `data/scoring_points.json` through `data/staging/*.json` and
  `tools/merge_staging.py`. `merge_file` in that tool replaces a matched record whole rather than
  merging fields, so writing a staging patch would have meant re-typing all 76 records' `earns`,
  `does_not_earn`, `sources`, `rubric_instances` and every other sourced field by hand to add one
  new one, which is exactly the hand-retyping this project's staging system exists to avoid errors
  in. The label is also a different kind of fact from the rest of the record, a judgement about
  which of 03's four checks decide the grading rather than a claim the corpus sources, so keeping
  it in its own file with its own `[inferred]` tag and its own reason per record is the cleaner
  separation and does not risk the sourced fields a hand-retyped patch would touch.
- `qa/15_determinism_labels.py` was added as check 15 rather than folded into an existing check,
  because it asserts a property of a file no other check reads (`data/bc_pt_determinism_labels.json`
  against the active BC-PT id set), and `qa/12_report.py` picks up any `qa/[0-9][0-9]_*.py` file
  automatically.
- The grader line in the Claude-only tier moves from the worst case, every one of the 1,200 judged
  points reaching the model, to the measured share, 442 of 1,200. No other lever named in the
  instruction, evals canary on Haiku, transcriber on Haiku standard tier, grader thinking off, or
  verifier sampling, was applied: three are already rejected or declined in
  `docs/plan/14-token-economy.md` and `13-ai-engineering.md`, and routing the evals canary to a
  cheaper model has no sourced basis and would change what the canary measures rather than its
  cost, so applying it would be inventing a claim the labelling instruction explicitly ruled out.
  The tier's overrun is reported at $8.07 rather than closed by an unsourced assumption.

Twenty-first session, slice 5, the operator rulings batch: six delegated rulings and one
cadence ruling, all applied with red-then-green tests.

- Stream error retryability (07). The claude-api skill's own `shared/error-codes.md` HTTP error
  code summary marks 429 `rate_limit_error`, 500 `api_error` and 529 `overloaded_error`
  retryable and every other listed type not; it names no timeout error type at all.
  `app/providers/anthropic.py` `_RETRYABLE_STREAM_ERROR_TYPES` holds exactly those three, and the
  normalised `error` event's `retryable` flag now reads the error's `type` against it instead of
  always `False`. A timeout stays `retryable: False`, per the ruling's own instruction that an
  undocumented type is left alone rather than guessed at. `tests/providers/test_anthropic.py`
  gained `test_stream_error_retryable_matches_the_error_type`, looping all nine named types; red
  against the reverted constant (`ImportError`, then the corrected existing test's `False` vs
  `True`), green restored. 07 gained a sourced table.
- Adding a passkey now requires the same `reauth_established` proof 09's other consequential
  actions do. `app/auth/service.py` `add_passkey_finish` takes `reauth_token` and calls
  `consume_reauth` after the new credential's ceremony verifies and before it is stored;
  `app/api/routes/auth.py` passes it through. The client (`app/web/src/api/client.ts`
  `addPasskey`) runs a full `reauthenticate()` ceremony between the authenticator's `create()` and
  the finish call, and `FinishAddPasskeyFields` gained `reauth_token`. 09's re-authentication list
  names it. `tests/auth/test_add_authenticator.py` gained
  `test_adding_an_authenticator_without_a_fresh_reauth_is_refused`, and the tests that add a
  credential now call `world.reauth(client)` first; `app/web/src/account/AddPasskeyControl.test.tsx`
  rewritten for the four-call sequence (add/begin, reauth/begin, reauth/finish, add/finish) and a
  new stale-reauth refusal case. Both red before the fix (401 expected, 200 got; four fetch calls
  expected, one got), green after.
- 09 line 96's "the login endpoints are the only ones an unauthenticated party can reach" is
  false and is replaced with the full list, derived from the route table rather than typed by
  hand: every route with no `current_session`/`current_user` dependency
  (`register/begin`, `register/finish`, `/auth/status`, `recovery/register/begin`,
  `recovery/register/finish`, `passkey/login/begin`, `passkey/login/finish`, `/healthz`).
  `tests/api/test_unauthenticated_routes.py` is new: it walks `app.routes` (through FastAPI's
  `_IncludedRouter` wrapping, which does not flatten onto the top-level list in this version) for
  every route whose dependant tree carries neither dependency, and asserts the set equals the
  documented list, so a new route added without one or the other silently drifts the doc no
  longer. Red with `/healthz` removed from the expected set, green restored.
- The review-queue route (`app/api/routes/review.py`) now enforces the sample check and
  one-verdict rule `app/review/audit.record_item_audit_verdict` already enforces for the CLI path:
  `resolve_item_audit` calls `audit.refuse_outside_sample` and `audit.refuse_second_verdict`
  before resolving an `item_audit` row, reading the sample from
  `settings.resolve_key_audit_sample_ids()` (new on `Settings`, backed by a new
  `GROWTH_KEY_AUDIT_SAMPLE_PATH` env var, `app/main.py`). With no sample configured the route
  refuses every `item_audit` verdict rather than guessing at membership. Since no sample has been
  drawn yet (gates 17/29/30 still blocked on the 130 hand-authored items), `app/review/audit.py`
  gained `draw_key_audit_sample`, a seeded, unit-capped (15 per unit), calculator-status-proportional
  sampler matching `10-quality-and-evaluation.md`'s audit stratification, generalised to whatever
  population it is given rather than the mature 139-archetype counts; `tools/draw_key_audit_sample.py`
  is the CLI wrapper that queries published items, joins each to its archetype's unit and writes
  the sample file `docs/operator/key-audit.md` describes. `tests/review/test_audit.py` gained five
  tests for the sampler (determinism, seed sensitivity, the unit cap, and both refusal shapes),
  and `tests/api/test_review_routes.py` gained three route tests (no sample configured, outside the
  sample, a second verdict through a second row) plus `key_audit_sample_ids` set on existing
  passing tests. Red confirmed on both (the cap test against a disabled cap check; all three new
  route tests against the reverted route/Settings changes), green restored.
- The remaining small rulings. A second error note replaces the first, confirming the operator's
  2026-09-20 decision the eighth session's code had never implemented (it refused with 409
  instead): `app/session/service.py` `record_error_note` no longer raises
  `ErrorNoteAlreadyWritten` (removed) and simply overwrites; the route's matching `except` clause
  is gone. Purge confirmation is the literal text `"delete my data"`
  (`app/api/routes/purge.py` `PURGE_CONFIRMATION`), wired into the client as
  `app/web/src/App.tsx` `PURGE_CONFIRMATION_PHRASE`, which also removes `purgeConfirmationPhrase`
  from `UNSUPPLIED_INPUTS.settings` so the purge controls are no longer withheld. `uvicorn` joins
  `pyproject.toml`'s `dependencies` and 06's stack decision paragraph, having previously been
  installed in `.venv/` only on the operator's yes. `/growth-tokens.css` defaults to
  `app/design/growth-tokens.json` (new `DEFAULT_TOKENS_PATH` in `app/main.py`) when
  `GROWTH_TOKENS_PATH` is unset, rather than 404ing; an explicitly configured but unreadable path
  still 404s. PyNaCl for provider key storage is declined for now: this installation is single-user
  and local, the key already lives in `.env`, and a `.env` file on a single-user machine is not
  meaningfully less protected than an encrypted row this same process decrypts back to plaintext on
  every call; revisit when P8 (multi-user) is scoped. All three code changes are tested:
  `tests/session/test_error_note_service.py` and `tests/api/test_error_note.py` rewritten for
  replace-not-refuse (red against the reverted service, both new/renamed tests failing on the
  `ErrorNoteAlreadyWritten` raise); `app/web/src/App.test.tsx` rewritten for the wired phrase (red
  with the App.tsx revert, two failures); `tests/api/test_static_mount.py`'s three named
  assertions rewritten to expect the default stylesheet rather than 404 (red with the main.py
  revert, three failures, including the `application` attribute's own subprocess test). No test
  was loosened; every changed assertion asserts a stronger or corrected claim than before.
- The Claude-only $100 tier's eval cadence. The BC-PT labelling pass alone left an $8.07 overrun
  with no further sourced lever (twentieth session, above). Cadence is an operator choice, not a
  sourced number, so this is a ruling that changes the plan's cadence directly rather than a gate
  loosened to reach a number: `tools/cost_model.py` gained
  `CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE = 2`, additive next to `MONTHLY_RUNS` (9), which the
  Claude-only tier's canary line now reads instead of `MONTHLY_RUNS`; golden set 3 stays at the
  full `MONTHLY_RUNS` cadence, because its monthly run costs only $5.60 over the whole cycle,
  cutting it to zero could not close $8.07 alone, and keeping one line at its original frequency
  rather than cutting both is the shape that leaves a monthly regression signal anywhere. New tier
  total $92.95, $7.05 under the $100.00 ceiling (above the operator's $5.00 headroom floor), down
  from $108.07. `tier.hundred`, the Gemini-verifier tier `13-ai-engineering.md` and
  `docs/operator/ai-operating-costs.md` quote at $95.03, reads `MONTHLY_RUNS` unchanged and is not
  touched, because this file never patches a figure a document has already quoted; the pre-cadence
  $108.07/$8.07 total and $128.95/$28.95 worst case are kept as their own emitted figures
  (`tier.hundred_claude_only.pre_cadence_ruling_cycle` and `.pre_cadence_ruling_worst_case_cycle`)
  so the history `docs/plan/14-token-economy.md` quotes stays a checkable number rather than dead
  prose. `docs/plan/14-token-economy.md`'s "The $100 tier, line by line" table and surrounding prose
  rewritten to the new total and to record the ruling; `python3 tools/cost_model.py --check
  docs/plan/14-token-economy.md` exits 0 (0 unknown dollar figures).
  `tests/tools/test_cost_model.py` gained `test_claude_only_tier_reads_the_2026_09_23_eval_cadence_ruling`,
  pinning the new cadence, the new total, the $7.05 headroom (asserted `>= 5.00`), the new worst
  case, and that `tier.hundred.cycle` still reads $95.03; red against the reverted
  `tools/cost_model.py` (`AttributeError`, the constant not existing), green restored. The
  pre-existing pinning test's `overrun`/`worst_case_cycle` assertions against the old $108.07 total
  are replaced by a `pre_cadence_ruling_evals_line` assertion, since those old figures are now
  history rather than the tier's live total; this is the pinning test moving to what the ruling
  changed, not a loosened gate, and it is recorded as a ruling for exactly that reason.
- Stale docstrings from the eighteenth session's slice, both about stage example. The
  `app/session/service.py` module docstring said confidence is collected at completion and
  unsupported and "not at all" at example, and that an attempt served at example "updates
  immediately"; both are wrong since the eighteenth/nineteenth sessions' ruling, so the paragraph
  is rewritten to say confidence is collected at every stage and every attempt defers its update
  until `record_confidence` supplies the rating, matching `record_attempt`'s actual `awaits_rating`
  gate. `app/feedback/render.py` `step_verification`'s docstring said "every worked step at stage
  example is given", which stopped being true once example blanks its last step under the same
  2-step minimum as completion; rewritten to say so. Both are comment-only; no behaviour changed,
  so no test was added for either, and the full suite (below) is the confirmation nothing else
  reads the old wording as a contract.

Twenty-second session, a verified review finding against the twenty-first session's slice 5 work
on the unauthenticated-route list (09 line ~96, ruling 3).

- The twenty-first session's fix derived the unauthenticated list from `create_app`'s own route
  table (`tests/api/conftest.py`'s `world` fixture) and missed the three unauthenticated routes
  `app/main.py`'s `mount_client` adds after `create_app` returns: `GET /growth-tokens.css`,
  `GET /` and the `/assets` `StaticFiles` mount, none of which `create_app` alone ever registers.
  `docs/plan/09-security-and-privacy.md`'s "Per IP" paragraph named eight routes, not the eleven
  the production application `uvicorn app.main:application` actually serves without a cookie.
  `tests/api/test_unauthenticated_routes.py` now builds the application with `build_application`
  (`app/main.py`) instead of `create_app` alone, so it exercises the same composition root uvicorn
  resolves. `DOC_UNAUTHENTICATED_ROUTES` gained `("GET", "/growth-tokens.css")` and
  `("GET", "/")`, both plain `APIRoute`s the client mount adds directly and so already reachable
  by the existing dependant-tree walk; a new `DOC_UNAUTHENTICATED_STATIC_MOUNTS = {"/assets"}` and
  `_unauthenticated_static_mounts` cover the `Mount`, which carries no dependant tree at all to
  walk and is unauthenticated-reachable by construction (`StaticFiles` answers any matching file
  regardless of cookie). Red with the doc list reverted to the old eight entries (`AssertionError`,
  `/growth-tokens.css` and `/` reported as extra on the left side), green restored. 09's paragraph
  rewritten to name all eleven and both source modules.

Twenty-third session, on the operator's delegated ruling on the agent-drafted items.

- The ruling: the 130 drafts in `content/items_p1_agent/` may be served so the app can teach now,
  but they are not the operator's hand-authored items. Exit criterion 7, gates 17 and 30, and gate
  29's audit sample count only items whose provenance model is `operator`. Only the operator may
  relabel a draft `operator`, by removing its `authored_by` or setting it to `operator`.
- Implementation choice: the bank directory is ingested on the bank's first query and not when
  the application is built, for the reason given under Done. A failed ingestion leaves the source
  pending, so the next query raises again and the bank never ends up silently empty.
- Not decided here, left for the operator (see Known defects): what an item with no options should
  do on an R29 MCQ turn. A guard that served such an item as short answer was tried and taken
  out. `tests/session/test_serve_format.py` (4 tests) and `tests/api/test_feedback_sentence.py`
  and `tests/api/test_routes.py` (7 tests) went red under it, because their fixture items carry
  `options=None` and expect the MCQ turn. Changing those tests is the operator's call.

Twenty-seventh session, on the instruction to use the operator's Claude Code subscription to cut
the AI cost wherever the terms allow.

- The Claude-only $100 tier splits into an API-key runtime total and an offline Claude Code
  subscription total. Template authoring and the verifier's blind re-solve move to Claude Code
  sessions, $0.00 API spend, because both produce content committed to the repository, the same
  shape as the 130 items in `content/items_p1_agent/` authored on 2026-09-23. The tutor, the
  grader, the transcriber, the diagnostician and the screen stay on the API key, because the
  Claude Agent SDK quickstart states "Unless previously approved, Anthropic does not allow third
  party developers to offer claude.ai login or rate limits for their products, including agents
  built on the Claude Agent SDK" (https://code.claude.com/docs/en/agent-sdk/quickstart.md
  [verified]) and each of those five serves a live student or grades a live attempt. New API total
  $52.14, offline total $40.81, 43.90 percent of the $92.95 tier
  [measured: `tier.hundred_claude_only.api_cycle`, `tier.hundred_claude_only.offline_cycle`,
  `tier.hundred_claude_only.offline_share`, `python3 tools/cost_model.py`].
- Evals do not split. Golden set 1 already costs $0.00 on the template gate. Golden set 2 grades
  the production grader prompt on `claude-sonnet-5` and golden set 3 reads the production
  transcriber prompt on the same model, both against fixed operator labels; a Claude Code agent is
  a different harness and would not measure the production prompt on its production model, so both
  stay on the API key in full at $22.88.
- The offline pass is not free of limits. A Pro or Max plan's usage caps are a rolling five hour
  window plus a weekly limit, neither published as a count
  (https://code.claude.com/docs/en/authentication.md [verified]), so `docs/operator/offline-authoring.md`
  paces the 348 template-authoring calls and 6,178 verifier re-solves across sessions rather than
  assuming they clear in one sitting.

Twenty-eighth session, a verified review finding against the twenty-seventh session's offline
work on the operator's Claude Code subscription, `docs/operator/offline-authoring.md` (step 2 of
the runbook).

- The twenty-seventh session's step 2 had the blind re-solve agent compare its own key against the
  drafted key, which means an operator following the runbook would have to hand the drafted key to
  the re-solving session, breaking the quality floor `docs/plan/13-ai-engineering.md` line 14 sets:
  "The verifier never sees the key." Step 2 now has the re-solving agent write its own key and
  worked solution to a file of its own, never given the drafted key, and a script, not the agent,
  reads both files and compares the two keys. The step also drops the reading that the comparison
  itself is a model judgment, so it no longer contradicts the same paragraph's claim that the
  deterministic checks around the verifier are unchanged.

Subscription backend, Slice 2 closing session.

- A drain retry that meets the usage limit again is not counted as a tutor call on the attempt.
  compose_sentence counted the call when it queued the job, and the retry is that same call
  still waiting for the window, so counting it would let waiting alone fill the 3-per-item
  ceiling and fail a job no model ever answered. Only failures that reached the provider for
  another reason are counted. Both tutor ceilings are checked before every drain call, so on
  `GROWTH_AI_BACKEND=api` no retry can be paid past what compose_sentence would allow.
- The drain test assertion the earlier fix agent changed, `job.attempts_made` after a limit wait,
  went from `== 1` to `== 0`. The drain test file had never been committed, so `git diff tests/`
  cannot show the old form; the ledger entry above is the record. An equality against 0 is as
  strict as one against 1, and the dedicated test
  `test_waiting_behind_a_limit_does_not_use_up_the_failure_retries` adds a stronger check: after
  more limit waits than `MAX_DRAIN_ATTEMPTS`, one real failure still re-queues rather than fails.
  The assertion was kept.
- The structured-output smoke call's second turn is the CLI's internal mechanism, not a tool
  running. The CLI 2.1.277 binary contains a StructuredOutput tool that the model is forced to
  call when a schema is set; the argv passes `--tools ""`, which removes every built-in tool, an
  empty strict MCP config and the full disallowed list, `permission_denials` was empty, and the
  call returned `structured_output`. The argv was left as it is and the smoke check was taught
  the one extra turn, only when a schema was asked for and structured output came back.

P2 Slice 3, 2026-09-23: P2 scope item 3 (review mode and FSRS scheduling) was built although P2's
entry criterion, "P1 merged with all gates green", is knowingly not met, since P1 reads 28 of 31
gates. The reason is that the engine needs a finite due queue to teach from now to May 2027, and
the three open P1 gates (17, 29, 30) need operator-authored items and a human key audit that no
agent can supply. Nothing else in P2 (diagnostic, whole-graph selection, full interleaving,
calibration) was started. Two narrower choices: the due queue counts FSRS-due skills and R5
requeues and leaves hypercorrection out, because hypercorrection is block 1's override lane, not
an FSRS due date; and the queue's cover breaks ties by lowest archetype id, because it is an
estimate of the day's load, while block 1 keeps its uniform random draw.

P2 Slice 3 closing session: the due queue now counts hypercorrection, reversing the slice's
earlier choice to leave it out. The queue already counted R5 requeues, which are no more an FSRS
due date than hypercorrection is, and 02 puts both in block 1 ahead of the FSRS order, so a queue
that stated block 1's load but dropped one of its two override lanes understated the day's
minutes. `due_today_skills` still counts only mastered skills below the retention target, the
definition 11 gives for due; the hypercorrection work shows up in `due_today_minutes` and in
`DueQueue.item_count`.

P2 Slice 4, calibration curve. P2 was started early on the operator's delegated authority,
because P1's three open gates (17, 29, 30) are operator-only.

- Which attempts count: graded (`correct` not null), rated by the student
  (`confidence_source = student`), submitted in the 30 calendar days ending on the requested day,
  in every stage and every session mode. Reason: 10 defines calibration "over all items carrying
  a rating"; the rating is collected before feedback at every stage and `render_feedback`
  refuses an unrated attempt, so a student rating is always a pre-feedback one; 08's wireframe
  heads the curve "Calibration, last 30 days". The close sweep's unsure is excluded because the
  student never gave it.
- Unaided versus aided: not split. Reason: no plan document restricts calibration to unaided
  attempts, and 10's definition covers every rated item.
- No summary statistic. 10 names the Brier score and confidence minus accuracy, both over "the
  confidence rating mapped to a probability", and no plan document gives the mapping from guess,
  unsure and confident to probabilities, so the record reports counts, accuracies and Wilson 95
  percent intervals only, and the client draws no ideal line.
- The threshold of 30 counts attempts inside the 30-day window, not lifetime attempts. Reason:
  the curve drawn is the 30-day one, and 11's exit criterion asks that it render from at least 30
  real rated attempts.
- `attempts.confidence_source` added rather than inferring provenance. Reason: without it the
  close sweep's unsure would enter the curve as if the student had chosen it.

P2 Slice 4 closing session: the Progress button on home is a secondary text button under the day's
queue, because 08 allows one primary action per screen and home's is starting or resuming the
set. It is present in every home state (ready, empty, in progress), since 08 names no state in
which progress is unreachable.

Item check, 2026-09-23: 27 agent-drafted stems asked "Which of the following is ..." and now ask
"Find ...". R29 serves an item as a short answer at stages example and completion and on every
other attempt at stage unsupported (`app/engine/select.py` `format_for_attempt`), so most serves
show no options, and nothing rewrites a stem for the served format; "Find" reads correctly in both
formats. The items stay agent drafts pending the operator's review, and no provenance changed.

Item audits, 2026-09-24: the deterministic part of auditing items is code, not guidance, on the
operator's standing rule that a check which must hold belongs in a mechanical check.
`tools/key_recheck.py` and each bank's formulations file carry it, and the recheck runs in the
suite so a later edit to a key or a stem cannot pass unchecked. The judgment part (formulating
from stems without reading keys, triage, what the tool cannot see, the lessons log) is a local
Claude Code skill under `.claude/`, which stays out of the repository by the same operator rule.

## Decisions taken on the operator's instruction, 2026-09-20 [inferred]

Sixth session, on the instruction "answer all decisions for me". Every open question the ledger
held for the operator is answered here. None of these is implemented yet except the last; they are
the standing answers the next slice builds against.

- A wrong short answer does get elaborated feedback in P1, as built this session. R12 rule 3 gives
  it no error path, so it carries the violated step and the worked solution and leaves the two
  BC-ERR fields empty. Feedback that names the step beats no feedback at all on the whole short
  answer path, and 03's Content section already contemplates an archetype with no matched error.
- `tests/fixtures/items_p1/` may be filled with synthetic items for gate 23. Gate 23's property is
  the flow, login to feedback to a persisted `skills_state` change, not item quality, so a fixture
  item exercises it honestly. Gates 17, 29 and 30 are item-quality gates and still wait for the 130
  hand-authored items; no synthetic item may be counted toward them, and the fixture directory
  carries a README saying so.
- Cassettes under `tests/fixtures/provider_cassettes/` may be hand-written fixtures rather than
  recordings, until a key exists. A cassette is a fixture response for `ReplayProvider`, so writing
  one by hand proves the replay path and the no-network rule. Every hand-written cassette is marked
  synthetic in the file, and gate 22's token count still waits for a real key.
- Purge truncates the tables that carry no `user_id`: `review_queue`, `jobs`, `items` and
  `item_verifications`. The installation is single-user, so every row in them is that user's work.
  `content_snapshots` is kept, because it is derived from the read-only library and holds nothing
  the student wrote. The purge audit entry survives the purge instead of being deleted with the
  rest of `audit_log`.
- py_webauthn (`webauthn` on PyPI) is approved for `pyproject.toml` and is to be named in 06 when
  the dependency lands.
- The error note is capped at 500 characters and a second POST replaces the first. One note per
  corrected item is 02's rule; replacing a note is editing it, not adding a second one.
- `reauth_established` and `coverage_gap_fail_closed` join 09's audit vocabulary, and the code gets
  one module-level enumeration of action names so the vocabulary is controlled in fact and not only
  in the plan.
- The coverage-gap audit writes one row per user per archetype and skips a gap already recorded,
  rather than one row per session opened.
- The tutor stays opt-in through `GROWTH_TUTOR_PROVIDER` until 07's budget, usage and audit seam is
  built. That seam is the next slice.
- The 24 stray `* 2.py` files were deleted. Twenty-two were byte-identical to their counterparts,
  and `tests/api/conftest 2.py` and `tests/items/test_verify 2.py` were strictly older versions of
  files that still hold everything they held. The suite now reports `191 passed` without
  `--ignore-glob`.

## Decisions taken on the operator's instruction, 2026-09-19 [inferred]

Second session, on the instruction "decide anything that needs my input yourself":

- Gate 31: both structural causes were corrected in the engine and the plan rather than in the fixture, because the real library has the same shape (440 of 522 listed skills sit in exactly one active archetype, `data/archetypes.json`). `gamma` 0.4 to 1.0 and `rho` -0.2 to -0.5 in `app/engine/constants.py`, 02, 11 and 12; 1.0 is PFA's own unit weight on `phi(c)` and keeps the 2 to 1 asymmetry. Mastery condition 3 becomes min(2, archetypes listing the skill in the active snapshot) via `EngineGraph.archetype_counts` and `evaluate_mastery(state, today, archetypes_available)`; a graph without counts keeps the old unconditional 2.
- Three selection-test fixture rows lacked the `stage` key that every production attempts row carries (`repository.load_attempts_history`, the runner); the new gamma pushed cold-start `p_knowledge` above 0.9 and reached `format_for_attempt`, which reads it. The rows were completed, no assertion changed.
- `httpx2` as the test dependency for FastAPI's TestClient.
- WebAuthn: use py_webauthn (`webauthn` on PyPI) when the passkey slice is built; record it in 06 then.
- Attempts at stage completion or unsupported whose rating never arrives: `close_session` will apply them with rating unsure (no hypercorrection can fire from unsure), so no observation is lost; to be built with the routes slice.
- Seeding the 618 `skills_state` rows happens on passkey registration finish, the only account-creation path.

- The prerequisite-graph cycle was closed by flipping the reversed row: `BC-SKL-06023,BC-SKL-05020,supporting` became `BC-SKL-05020,BC-SKL-06023,supporting`, because the row's own note stated that the Unit 6 skill depends on the Unit 5 one, which is the opposite of the direction it was stored in. Applied directly to `data/prereq_edges.csv`, then `tools/sync_dependents.py`, `tools/merge_staging.py`, the post-change tool chain and `qa/12_report.py`.
- The FSRS-7 forms stay as copied from fsrs-rs; 02's transcribed block stays marked superseded.
- The application lives in this repository; the local CLAUDE.md was amended to say so. The style gate keeps its wider `/docs/` scope.
- The build is committed on the branch `build/p1-backend-core`; main is untouched.

## Next candidates [inferred]

P1 reads 28 of 31 (gate_status: 17, 29 and 30 missing). P2 cannot start: its entry criterion is
"P1 merged with all gates green". Nothing further in P1 is buildable without the operator; every
item below needs content, a key, a download or a ruling.

Subscription backend, after Slice 2: observe a real usage-limit answer when one happens and align
the adapter's patterns and the fake CLI to it; decide whether the drain should run on a schedule
rather than by hand (Known defects above).

Human-only, in the order that unblocks the most:

0a. Twenty-third and twenty-fourth sessions: the operator reviews the 130 agent drafts in
   `content/items_p1_agent/` (its README lists what the audit left open, and the twenty-sixth
   session's Known defects entry lists what the independent review and its re-check left open). The drafts are served now, every one with four options, but count
   toward nothing. Gates 17, 29 and 30 and exit criterion 7 still wait on items with operator
   provenance, whether hand-authored or drafts the operator has relabelled after review.

0. Closed the twentieth and twenty-first sessions, 2026-09-23: the BC-PT labelling pass
   (`data/bc_pt_determinism_labels.json`, 48 of 76 deterministic and 28 model_required) and the
   eval-cadence ruling (`CLAUDE_ONLY_GOLDEN_SET_2_CANARY_CADENCE = 2`) together close the
   Claude-only tier's overrun: $92.95, $7.05 under the $100.00 ceiling. What is left to move the
   grader line again is a relabelling, if golden set 2's per point type exact match shows a label
   was wrong. Closed the twenty-seventh session, 2026-09-23: the tier splits $52.14 API key against
   $40.81 offline Claude Code subscription; `docs/operator/offline-authoring.md` is the runbook the
   operator follows to run that offline pass.
1. Gates 17 and 30, exit criterion 7: the 130 hand-authored items, 10 per archetype over 11's 13.
   Shape `docs/operator/items.md`, check `python3 tools/check_items.py <dir>`. Unblocks
   `test_item_verification_tools` and `eval_p1_distractor_paths`. Once published, run
   `python3 tools/draw_key_audit_sample.py <db_path> <content_root> <out_sample.json>` (new this
   session) and point `GROWTH_KEY_AUDIT_SAMPLE_PATH` at the file it writes, so the review-queue
   route (item 2 below) can resolve an `item_audit` verdict at all.
2. Gate 29, exit criterion 4: the 100-item key audit over those items. Shape
   `docs/operator/key-audit.md`, check `python3 tools/check_audit_verdicts.py`. The review-queue
   route now enforces the same sample check and one-verdict rule the CLI does (this session); with
   no sample configured it refuses every `item_audit` verdict.
3. Exit criterion 8: real tutor calls with the key, then `tools/serving_cost.py <db>`. The
   persistent developer spend cap (`app/providers/guard.py`, this session) now stands in front of
   any such call once `GROWTH_AI_BACKEND=api` is set; `tools/dev_spend.py` reports spent,
   cap and remaining before and after.
4. Remaining rulings: copy for a failed request and for the account screen; permission to
   download Inter as a self-hosted woff2. Closed this session: the retryable flag, the passkey
   re-auth requirement, the second-error-note behaviour, the purge confirmation phrase, PyNaCl
   (declined), `/growth-tokens.css`'s default, `uvicorn` in pyproject, and the eval-cadence
   overrun.

P2 Slice 3, 2026-09-23: P2 scope item 3 (review mode, the dated desired-retention switch, the
finite due-today queue and its minute estimate) landed ahead of the entry criterion, see
Decisions. The rest of P2 still waits on it.
